#!/usr/bin/env python3
"""글 발행 보조 도구.

  python3 tools/post.py prep              커밋 전: 이미지 최적화 + lazy·치수 속성
  python3 tools/post.py thumb <이미지>     4:3 썸네일 생성
  python3 tools/post.py notify <URL...>   배포 후: IndexNow 전송

prep 은 여러 번 돌려도 안전하다(이미 처리된 것은 건너뛴다).
"""
import os, re, sys, glob, json, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY  = "1e2a057fedcc3740992d46287650f91d"
HOST = "quentinjeon.github.io"
MAX_W = 1600            # 본문 폭이 ~700px 이라 이 이상은 낭비
BIG   = 300 * 1024      # 이 크기를 넘으면 다시 압축


def _img():
    try:
        from PIL import Image
        return Image
    except ImportError:
        sys.exit("Pillow 가 필요합니다:  pip3 install --user pillow")


def dims(path):
    """SVG 는 헤더에서, 나머지는 PIL 로 치수를 읽는다."""
    if path.lower().endswith('.svg'):
        head = open(path, encoding='utf-8', errors='replace').read(2000)
        w = re.search(r'\bwidth="([\d.]+)', head)
        h = re.search(r'\bheight="([\d.]+)', head)
        if w and h:
            return round(float(w.group(1))), round(float(h.group(1)))
        vb = re.search(r'viewBox="[\d.\-]+ [\d.\-]+ ([\d.]+) ([\d.]+)"', head)
        return (round(float(vb.group(1))), round(float(vb.group(2)))) if vb else None
    try:
        return _img().open(path).size
    except Exception:
        return None


def optimize():
    """큰 이미지를 줄인다.

    되돌릴 수 없는 손실 작업이므로 두 가지를 지킨다.
      1) 이미 규격에 맞는 파일은 건드리지 않는다(JPEG 재인코딩은 화질만 깎인다).
      2) 결과가 원본보다 크면 버린다 — 메모리에서 비교한 뒤에 기록한다.
    """
    import io
    Image = _img()
    saved = skipped = 0
    for dp, _, fs in os.walk(os.path.join(ROOT, 'assets/images')):
        if 'thumbs' in dp:
            continue
        for f in fs:
            if not f.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue
            p = os.path.join(dp, f)
            before = os.path.getsize(p)
            if before < BIG:
                continue
            im = Image.open(p)
            w, h = im.size
            is_png = p.lower().endswith('.png')

            too_wide = w > MAX_W
            raw_png = is_png and im.mode != 'P'      # 아직 양자화 전
            if not (too_wide or raw_png):
                skipped += 1
                continue

            if too_wide:                              # 가로 기준(세로로 긴 캡처 보호)
                im = im.convert('RGB').resize((MAX_W, round(h * MAX_W / w)), Image.LANCZOS)
            else:
                im = im.convert('RGB')

            buf = io.BytesIO()
            if is_png:
                im.quantize(colors=256, method=Image.MEDIANCUT,
                            dither=Image.Dither.NONE).save(buf, format='PNG', optimize=True)
            else:
                im.save(buf, format='JPEG', quality=85, optimize=True, progressive=True)

            after = buf.tell()
            rel = os.path.relpath(p, ROOT)
            if after >= before:                       # 기록하지 않는다
                skipped += 1
                print(f"  유지({before//1024}KB, 줄지 않음)  {rel}")
                continue
            open(p, 'wb').write(buf.getvalue())
            saved += before - after
            print(f"  {before//1024:>5}KB → {after//1024:>4}KB  {rel}")
    print(f"이미지 절감 {saved//1024}KB · 손대지 않음 {skipped}개")


def attrs():
    """본문 이미지에 loading=lazy·decoding=async·width·height 를 붙인다."""
    pat = re.compile(r'!\[([^\]]*)\]\((?:https://' + re.escape(HOST) + r')?(/assets/images/[^)\s]+)\)(\{:[^}]*\})?')
    done = skip = miss = 0
    for f in sorted(glob.glob(os.path.join(ROOT, '_posts/*.md')) +
                    glob.glob(os.path.join(ROOT, '_pages/*.md'))):
        s = open(f, encoding='utf-8').read()
        orig = s

        def repl(m):
            nonlocal done, skip, miss
            alt, src, ial = m.group(1), m.group(2), m.group(3)
            if ial and 'loading' in ial:
                skip += 1
                return m.group(0)
            d = dims(os.path.join(ROOT, src.lstrip('/')))
            if not d:
                miss += 1
                print(f"  ! 치수를 못 읽음: {src}")
                return m.group(0)
            done += 1
            return (f'![{alt}]({src})'
                    f'{{: loading="lazy" decoding="async" width="{d[0]}" height="{d[1]}"}}')

        s = pat.sub(repl, s)
        if s != orig:
            open(f, 'w', encoding='utf-8').write(s)
            print(f"  수정: {os.path.relpath(f, ROOT)}")
    print(f"속성 추가 {done} · 이미 있음 {skip} · 실패 {miss}")


def thumb(src):
    """목록용 4:3(720x540) 썸네일. 박스가 4:3 + cover 라 비율을 맞춰야 안 잘린다."""
    Image = _img()
    src = src if os.path.isabs(src) else os.path.join(ROOT, src.lstrip('/'))
    im = Image.open(src).convert('RGB')
    w, h = im.size
    cw = round(h * 4 / 3)
    box = (0, 0, cw, h) if cw <= w else (0, 0, w, round(w * 3 / 4))
    out = im.crop(box).resize((720, 540), Image.LANCZOS)
    name = os.path.splitext(os.path.basename(src))[0].split('-')[0] + '.jpg'
    dst = os.path.join(ROOT, 'assets/images/thumbs', name)
    out.save(dst, quality=88, optimize=True)
    print(f"썸네일 {out.size} → /assets/images/thumbs/{name}  ({os.path.getsize(dst)//1024}KB)")
    print(f"front matter 에 추가:  header:\\n    teaser: /assets/images/thumbs/{name}")


def notify(urls):
    """IndexNow 전송.

    참여 검색엔진: Bing · Naver · Yandex · Seznam.cz · Yep (indexnow.org 공지 기준).
    구글은 참여하지 않으므로 Search Console 에서 따로 요청해야 한다.
    """
    urls = [u if u.startswith('http') else f'https://{HOST}{u}' for u in urls]
    body = json.dumps({"host": HOST, "key": KEY,
                       "keyLocation": f"https://{HOST}/{KEY}.txt",
                       "urlList": urls}, ensure_ascii=False)
    code = subprocess.run(
        ['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}',
         '-X', 'POST', '-H', 'Content-Type: application/json; charset=utf-8',
         '--data', body, 'https://api.indexnow.org/indexnow'],
        capture_output=True, text=True).stdout.strip()
    for u in urls:
        print("  " + u)
    meaning = {'200': '접수 + 키 검증 완료', '202': '접수, 키 검증 대기',
               '400': '형식 오류', '403': '키 불일치 — 키 파일 확인',
               '422': '호스트 불일치', '429': '요청 과다'}
    print(f"IndexNow → HTTP {code}  ({meaning.get(code, '문서 확인 필요')})")
    print("\n이 요청은 Bing · Naver · Yandex · Seznam · Yep 로 전달됩니다.")
    print("구글만 IndexNow 에 참여하지 않으므로 따로 요청하세요.")
    print("  구글: Search Console → URL 검사 → 색인 생성 요청")


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    if cmd == 'prep':
        print("[1/2] 이미지 최적화"); optimize()
        print("\n[2/2] 본문 이미지 속성"); attrs()
    elif cmd == 'thumb' and len(sys.argv) > 2:
        thumb(sys.argv[2])
    elif cmd == 'notify' and len(sys.argv) > 2:
        notify(sys.argv[2:])
    else:
        print(__doc__)

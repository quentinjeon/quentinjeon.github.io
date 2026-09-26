# 글 올릴 때 하는 일

## 자동으로 되는 것 (손댈 필요 없음)

배포하면 알아서 갱신됩니다.

- 사이트맵 `/sitemap.xml`, Atom `/feed.xml`, RSS 2.0 `/rss.xml`
- 구조화 데이터 `BlogPosting` + `Person`
- og:image, 트위터 카드 (teaser 가 없으면 기본 이미지)
- GA4 수집, 뉴스레터 폼·팝업
- `/labs/`, `/ax/`, `/work/` 목록에 새 글 노출

## 손이 필요한 것

### 1. 글 쓰기 — front matter 최소 항목

```yaml
---
layout: single
title: "제목"
seo_title: "짧은 제목"          # title 이 45자 넘을 때만
excerpt: "목록에 보일 한두 문장"
description: "검색 결과에 보일 설명. 40~60자"
categories: [labs]              # labs / ax+도메인 / work
tags: [태그, 태그]
toc: true
toc_sticky: true
header:
  teaser: /assets/images/thumbs/이름.jpg
---
```

- `categories: [ax, energy]` 처럼 두 개면 URL 이 `/ax/energy/글slug/` 가 됩니다
- `description` 이 없으면 사이트 기본 문구가 그대로 복제됩니다. 꼭 쓰세요
- 본문 맨 앞에 `# 제목` 을 쓰지 마세요. 테마가 이미 H1 을 찍습니다

### 2. 썸네일 만들기

```bash
python3 tools/post.py thumb assets/images/새이미지.png
```

목록 썸네일 박스가 4:3 이라 비율이 안 맞으면 잘립니다. 이 명령이 720x540 으로 맞춰줍니다.

### 3. 커밋 전 정리

```bash
python3 tools/post.py prep
```

- 300KB 넘는 이미지를 1600px 로 줄이고 압축 (이미 규격이면 건드리지 않음)
- 본문 이미지에 `loading=lazy` `decoding=async` `width` `height` 부여

여러 번 돌려도 안전합니다. 결과가 원본보다 크면 기록하지 않습니다.

### 4. 커밋 · 푸시

```bash
git add -A && git commit -m "메시지" && git push
```

GitHub Pages 빌드에 **1~3분** 걸립니다.

### 5. 배포 확인 후 색인 요청

```bash
python3 tools/post.py notify /labs/새글-slug/
```

한 번 보내면 **Bing · Naver · Yandex · Seznam.cz · Yep** 에 전달됩니다.
`200`(키 검증까지 완료) 또는 `202`(접수, 검증 대기) 면 성공입니다.

**구글만 IndexNow 에 참여하지 않습니다.** 구글은 수동으로:

| 검색엔진 | 경로 |
|---|---|
| 구글 | Search Console → URL 검사 → 주소 입력 → 색인 생성 요청 |
| 네이버 | IndexNow 로 이미 전달됨. 급하면 서치어드바이저 → 요청 → 웹 페이지 수집 |

---

## 자동으로 색인되나?

**아니요.** 정확히는 이렇습니다.

| 단계 | 자동 여부 |
|---|---|
| 사이트맵·RSS 에 새 글 등재 | ✅ 배포 시 자동 |
| 검색엔진이 존재를 알게 됨 | ⚠️ 언젠가는 자동, 요청하면 빨라짐 |
| 크롤러가 실제로 방문 | ❌ 검색엔진이 정함 |
| 검색 결과에 등재 | ❌ 내용을 보고 검색엔진이 판단 |

색인 요청은 **크롤 시점을 앞당기는 것**까지입니다. 등재를 보장하지 않습니다.

신규 도메인은 초기에 느립니다. 글이 쌓이고 크롤 이력이 생기면 요청 없이도 며칠 안에 잡힙니다.

## 한 달에 한 번쯤 볼 것

- GA4 → 어떤 글이 읽히는지, `nl_subscribe` 전환이 어느 폼에서 나오는지
- Search Console → 색인 생성 → 페이지 (미색인 사유)
- 네이버 서치어드바이저 → 사이트 최적화 (항목별 점검)
- 빙 → AI Performance (Copilot·ChatGPT 답변에 인용됐는지)

# docs — 글감과 원고

발행 위치별로 나눠 둡니다. **폴더가 곧 배포처**입니다.

```
docs/
├── ax/              AX Insight — 현장에 적용한 설계·구축 이야기
│   ├── construction/
│   ├── energy/
│   ├── commerce/
│   └── foundation/  도메인이 애매하면 여기
├── labs/            Scholar Labs — 논문·개념 학습 기록
├── work/            프로젝트 회고
└── _theme-sample/   minimal-mistakes 테마가 가져온 데모 사이트 (건드리지 않음)
```

## 폴더 이름

`제목_YYYY-MM-DD`. 폴더명만 보고 어떤 글인지 알 수 있게 합니다.

## 배포 위치를 정하는 기준

| 물음 | 답 | 위치 |
|---|---|---|
| 특정 도메인의 현장 이야기인가 | 예 | `ax/<도메인>` |
| AX 공통 구조·방법론인가 | 예 | `ax/foundation` |
| 논문·개념 학습 기록인가 | 예 | `labs` |
| 만든 시스템 자체를 소개하는가 | 예 | `work` (단, 목록은 `_data/projects.yml` 로 관리) |

정해진 폴더가 그대로 front matter 의 `categories` 가 됩니다.

```yaml
# docs/ax/foundation/... 에 있으면
categories:
  - ax
  - foundation      # → /ax/foundation/<slug>/

# docs/labs/... 에 있으면
categories:
  - labs            # → /labs/<slug>/
```

`ax` 하위 도메인은 `_data/domains.yml` 에 등록된 것만 씁니다.
새 도메인을 만들려면 그 파일에 먼저 추가하고 `_pages/ax-<slug>.md` 를 만들어야 합니다.

## 여기 없는 것

운영 문서(발행 절차·색인 요청 가이드·점검 보고서)는 `tools/` 에 있습니다.
개인·고객 자료는 공개 저장소에 두지 않습니다.

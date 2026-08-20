---
permalink: /work/hunmin-ai/
title: "훈민 AI — 군 문서 작성 지원"
layout: single
author_profile: true
toc: true
toc_sticky: true
---

`Next.js 14 + FastAPI` · [저장소](https://github.com/quentinjeon/hunminai)

지식 라이브러리 / 편집기 / AI 에이전트 3패널 웹 애플리케이션.

**문제**: 군 문서는 내용보다 **형식 규정 위반으로 반려**된다. 그리고 규정은 사람 머릿속에 있다.

- 실시간 규정 준수 검증 + 준수율 점수(0~100), `F8`로 다음 오류 이동
- hwplib.js WASM으로 브라우저에서 HWP 처리
- I~III급 비밀 등급을 문서 속성으로 관리
- WebSocket + Redis Pub/Sub 실시간 다중 편집

---

---

[← 프로젝트 전체](/work/){: .btn .btn--inverse}

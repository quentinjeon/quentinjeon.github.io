---
permalink: /work/open-my-chatbot/
title: "open-my-chatbot — 커머스 CS 상담 챗봇"
layout: single
author_profile: true
toc: true
toc_sticky: true
---

`Python + LangGraph` · [저장소](https://github.com/quentinjeon/open-my-chatbot)

**조회된 데이터 없이는 답변을 생성하지 않는** 근거 기반 응답 시스템.

**문제**: 상담 챗봇의 실패는 "모른다"가 아니라 **"모르면서 지어낸다"**.

- L1~L9 + L8.5 상태 그래프 — 질문수신 → 의도분류 → 엔티티추출 → 데이터검색 → 문맥결합 → 정책판단 → 이관판단 → 응답구성 → **응답검증** → 클로징
- DataBus/Provider 추상화로 JSON(MVP) → RDB → VectorStore → MCP → 외부API를 상위 코드 수정 없이 교체
- L7 점수 기반 에스컬레이션 — 판단 불가 시 컨텍스트와 함께 상담사 이관
- 개인 기억 + 집단 지식 2층 메모리, L8.5가 금지 표현·오답 패턴 차단

### 커머스 도구

| 프로젝트 | 한 줄 | 스택 |
|---|---|---|
| **Banafit AI Studio** | 패션 이커머스 이미지 워크플로우. 업로드 → 조건 → 프롬프트 레이어 스택 → 배치 생성 → 반복 정제 **6단계 상태 머신** | Gemini 2.5 Flash Image |
| **DeepRe** | 고객 리뷰에 3가지 스타일(감사·정중·문제해결) 답변 자동 생성. 웹훅 URL을 화면에서 실시간 변경 | Next.js 14 + n8n |
| **쿠팡 크롤링 시스템** | 랜덤 간격(균등/정규/지수 분포) + 인간 행동 시뮬레이션 + 워커 풀 + 실패 자동 복구 | Node.js + Chrome Extension |
| **스마트스토어 AI 스크래퍼** | AI 에이전트가 브라우저를 직접 제어해 동적 페이지 스크래핑 | browser-use |

---

---

[← 프로젝트 전체](/work/){: .btn .btn--inverse}

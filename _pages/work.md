---
permalink: /work/
title: "프로젝트"
excerpt: "현장 운영 시스템, AI 에이전트 아키텍처, 도구와 실험, 교육 자산."
layout: single
author_profile: true
toc: true
toc_sticky: true
---

도메인은 식품 제조 · 커머스 · 에너지 · 투자로 다르지만, 관통하는 작업은 하나입니다.
**사람이 규칙을 머릿속에 들고 하던 업무를, 시스템이 규칙을 들고 있는 구조로 옮기는 것.**

[설계 원칙 6가지 보기 →](/principles/){: .btn .btn--inverse}

---

# 케이스 스터디

실제 현장 문제를 푼 운영 시스템입니다. 화면과 숫자를 함께 실었습니다.

## [HACCP FLOW — 식품 제조 기록 시스템](/work/haccp-flow/)

[![HACCP FLOW](/assets/images/work/haccp-01-main.jpg)](/work/haccp-flow/)

식품 제조 현장의 **말과 클릭을 HACCP 공식 기록으로** 바꾸는 시스템. 생산 1회마다 11종의 서류가 필요하고 빈칸 하나가 인증취소로 이어지는 환경에서, **어느 칸이 왜 비었는지를 시스템이 항상 알고 있게** 만들었습니다.

키워드 라우팅으로 LLM 토큰 **-70%**, 응답시간 **-61%**. 그리고 작업 시각은 **의도적으로 자동화하지 않았습니다.**

[케이스 읽기 →](/work/haccp-flow/){: .btn .btn--primary}

## [온라인몰 수익률 관리 시스템](/work/margin-system/)

[![온라인몰 수익률](/assets/images/work/margin-01-dashboard.jpg)](/work/margin-system/)

**총매출은 다들 압니다. 이익을 모릅니다.** 엑셀 3장을 넣으면 채널별 수수료(6.8~24.0%)·원가·물류비를 반영한 기여이익과 **적자 딜**을 즉시 드러냅니다.

매핑률 99.9%, 남은 0.1%는 건수와 금액으로 화면에 남깁니다. 테스트 65건.

[케이스 읽기 →](/work/margin-system/){: .btn .btn--primary}

---

# AI 에이전트 · 파이프라인

## agent-wallet — 자율 사고·글쓰기 에이전트
`Python 3.12` · 비공개

공시 클러스터링·분봉 임팩트 시그널을 받아 스스로 판단해 글을 쓰고 3채널에 발행하는 에이전트.

**문제**: LLM이 글을 쓰는 건 쉽다. 자율로 돌리면서 **사고를 안 내는 게** 어렵다.

- 프롬프트 1회 호출 → `observe → filter → think → draft → review → act → learn` **7단계 trace**. `trace_id` 하나로 글 한 편의 일대기를 재현
- 가드레일 3종: `kill_switch` · `publish_limit` · `balance_floor`
- self-review 5체크 + 1회 retry, `review_fail_streak 5회 시 자동 kill-switch`
- 트랜잭션은 SQLite, 의미 회상은 LanceDB 벡터 검색으로 저장소 역할 분리
- 테스트 96건, structlog JSON 로그 전 단계 표준화

## OpenClaw — 멀티에이전트 자동매매
`Python + Next.js` · [저장소](https://github.com/quentinjeon/openclaw-trade)

5개 전문 에이전트가 파이프라인으로 협력: `MarketAnalyzer → Strategy → RiskManager → Execution → Portfolio`

**문제**: 자동매매 봇은 **왜 그 주문을 냈는지 설명하지 못한다.**

- 단계별 산출물이 타입을 가짐 — `MarketSignal → TradingSignal → ApprovedOrder → TradeResult`
- `RiskManagerAgent`가 단일 게이트: 최대 포지션 크기·동시 포지션 수·일일 손실 한도·연속 손실 횟수
- WebSocket 실시간 대시보드로 에이전트 의사결정 로그 스트림 노출
- 페이퍼트레이딩 모드 우선

## open-my-chatbot — 커머스 CS 상담 챗봇
`Python + LangGraph` · [저장소](https://github.com/quentinjeon/open-my-chatbot)

**조회된 데이터 없이는 답변을 생성하지 않는** 근거 기반 응답 시스템.

**문제**: 상담 챗봇의 실패는 "모른다"가 아니라 **"모르면서 지어낸다"**.

- L1~L9 + L8.5 상태 그래프 — 질문수신 → 의도분류 → 엔티티추출 → 데이터검색 → 문맥결합 → 정책판단 → 이관판단 → 응답구성 → **응답검증** → 클로징
- DataBus/Provider 추상화로 JSON(MVP) → RDB → VectorStore → MCP → 외부API를 상위 코드 수정 없이 교체
- L7 점수 기반 에스컬레이션 — 판단 불가 시 컨텍스트와 함께 상담사 이관
- 개인 기억 + 집단 지식 2층 메모리, L8.5가 금지 표현·오답 패턴 차단

## 훈민 AI — 군 문서 작성 지원
`Next.js 14 + FastAPI` · [저장소](https://github.com/quentinjeon/hunminai)

지식 라이브러리 / 편집기 / AI 에이전트 3패널 웹 애플리케이션.

**문제**: 군 문서는 내용보다 **형식 규정 위반으로 반려**된다. 그리고 규정은 사람 머릿속에 있다.

- 실시간 규정 준수 검증 + 준수율 점수(0~100), `F8`로 다음 오류 이동
- hwplib.js WASM으로 브라우저에서 HWP 처리
- I~III급 비밀 등급을 문서 속성으로 관리
- WebSocket + Redis Pub/Sub 실시간 다중 편집

## GraphRAG 워크플로우
`Node.js + Airflow` · [저장소](https://github.com/quentinjeon/dag.graph.rag.airflow)

Weaviate(벡터) + Neo4j(그래프)를 결합하고 Airflow DAG로 자동화한 질의응답 파이프라인.

**문제**: 순수 벡터 RAG는 "관련 문서"는 찾지만 **"개념 간 관계"는 못 찾는다.**

벡터 검색 + 질문에서 엔티티 추출 + Neo4j 관계 탐색 → 통합 컨텍스트 → 응답 생성. 응답에 `type: vector` / `type: graph`로 **소스를 구분해 반환**. 6단계 Airflow DAG로 재현 가능하게 스케줄링.

---

# 도구 · 실험

| 프로젝트 | 한 줄 | 스택 |
|---|---|---|
| **promptfoo 평가 프로토타입** | CSV 업로드 → 프롬프트 평가 → 결과 다운로드를 30분 내에. 의도 분류 11개 카테고리에서 모델 성능 비교 | FastAPI + Promptfoo CLI |
| **DeepRe** | 고객 리뷰에 3가지 스타일(감사·정중·문제해결) 답변 자동 생성. 웹훅 URL을 화면에서 실시간 변경 | Next.js 14 + n8n |
| **DART 재무정보 분석** | DART API + 네이버 금융으로 3개년 시계열 재무비율(ROE·영업이익률·부채비율·PER) 자동 산출 | Python |
| **심층 웹 리서치 보고서 생성기** | Firecrawl 웹 수집 + PDF/DOCX 업로드 → 보고서 → DOCX/PDF 출력 | Streamlit |
| **Banafit AI Studio** | 패션 이커머스 이미지 워크플로우. 업로드 → 조건 → 프롬프트 레이어 스택 → 배치 생성 → 반복 정제 **6단계 상태 머신** | Gemini 2.5 Flash Image |
| **쿠팡 크롤링 시스템** | 랜덤 간격(균등/정규/지수 분포) + 인간 행동 시뮬레이션 + 워커 풀 + 실패 자동 복구 | Node.js + Chrome Extension |
| **스마트스토어 AI 스크래퍼** | AI 에이전트가 브라우저를 직접 제어해 동적 페이지 스크래핑 | browser-use |
| **Gemini Live Talking Head** | 사진 업로드 → 립싱크 아바타 + 실시간 양방향 음성 대화 + 라이브 전사 | Gemini Live API |
| **AI Mindful Assistant** | 음성 우선 명상 코치. 감정 점수(1~10) 추적 + 시계열 리포트 | React 19 |
| **Audio → Script** | 영어 학습 오디오를 Whisper로 전사. 모델 5종 크기별 정확도/속도 트레이드오프 정리 | Streamlit + Whisper |
| **Duplicate Image Finder** | 해시 기반 정확 중복 + ViT 기반 유사 중복(임계값 조절) + 차이점 설명 | Streamlit + ViT |
| **LangChain RAG 챗봇** | PDF 업로드 → Pinecone 벡터 검색 → 응답. MongoDB 세션 관리, Docker Compose 배포 | Next.js + FastAPI |

---

# 교육 자산

## AI 논문을 위한 확률·수학 인터랙티브 교재
**36챕터 · QA 36/36 PASS**

"초등학생도 이해할 수 있는 비유"와 "논문 수준의 수식"을 **같은 페이지에서** 제공하는 인터랙티브 HTML 교재.

**문제**: 수식을 이해하지 못한 채 딥러닝 코드만 쓰는 상태. 기존 교재는 **너무 쉽거나 너무 어렵거나** 둘 중 하나.

- 3층위 동시 제공 — Layer 1 일상 비유 / Layer 2 직관 해설 / Layer 3 MathJax 수식·논문 기호
- 경사하강법 시뮬레이터 등 인터랙티브 실습
- Phase별 졸업 기준 정의 — Phase 1 논문 수식 50% 독해 → Phase 3 논문 Contribution을 수식 수준에서 비판

## 바이브코딩 커리큘럼

15단계 제작 순서 + 실습 5단계(데이터 이해 → PRD 작성 → docs 재작성 → mock → 개발). 단계마다 **"확인할 숫자"**를 명시해 학습자가 스스로 검증할 수 있게 구성했습니다.

`sales` 저장소 안에 시스템과 커리큘럼이 함께 있습니다.

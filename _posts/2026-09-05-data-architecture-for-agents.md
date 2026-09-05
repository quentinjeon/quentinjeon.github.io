---
layout: single
title: "데이터 아키텍처 개념정리 — Lake·Warehouse·Mart에서 Agent Action까지"
excerpt: "Table·Join·View, ETL과 ELT, Lake·Warehouse·Mart, Star Schema, 마트 갱신 방식을 정리하고, 그 데이터 계층이 Agent의 State와 Allowed Action으로 어떻게 이어지는지까지 연결합니다."
categories:
  - ax
  - foundation
tags:
  - 데이터 아키텍처
  - Data Warehouse
  - Data Lake
  - Data Mart
  - ETL
  - ELT
  - Star Schema
  - Agent State
  - Action Space
  - Enterprise AX
toc: true
toc_sticky: true
header:
  teaser: /assets/images/thumbs/data-arch.jpg
---

Agent를 만들다 보면 결국 같은 질문에 도달합니다.
**"이 Agent가 지금 읽고 있는 상태는 어디서 온 데이터인가?"**

이 글은 그 앞단을 정리한 것입니다. Table부터 시작해 Lake·Warehouse·Mart를 거쳐,
그 데이터가 Agent의 State가 되고 다시 허용된 Action으로 이어지는 흐름까지 한 줄로 잇습니다.

> 이 문서의 핵심 질문 “기업의 데이터가 어떻게 정리되어 Agent가 읽을 수 있는 상태가 되고, 그 상태를 바탕으로 Agent가 허용된 Action을 선택·실행하는가?”

## 0. 전체 개념 지도

먼저 큰 그림을 잡고, 이후 각 계층을 하나씩 내려갑니다.

[![원천 시스템에서 분석·AI 활용까지의 전체 데이터 흐름](/assets/images/data-arch-01-overview.png)](/assets/images/data-arch-01-overview.png)
*그림 1. 원천 시스템에서 분석·AI 활용까지의 전체 데이터 흐름 — 클릭하면 원본 크기로 볼 수 있습니다.*

> 한 줄 요약 원천 시스템의 데이터를 ETL/ELT로 수집·변환하고, Lake/Warehouse에 저장·통합한 뒤, 업무 목적별 Mart를 만들어 BI·ML·Agent가 활용한다.

- MSSQL·MySQL·ERP·CRM은 보통 원천 시스템(Source / Operational System)이다.
- Data Warehouse는 “DB 제품들이 모인 곳”이라기보다, 여러 원천의 데이터가 정제·표준화·통합된 분석 저장소다.
- Data Mart는 Join 기능 자체가 아니라, 특정 업무 목적에 맞게 완성된 분석 데이터 영역이다.

## 1. Table · Join · View

데이터를 저장하고, 연결하고, 재사용하는 가장 기본적인 단위입니다.

[![Table, Join, View의 관계](/assets/images/data-arch-02-table-join-view.png)](/assets/images/data-arch-02-table-join-view.png)
*그림 2. Table, Join, View의 관계 — 클릭하면 원본 크기로 볼 수 있습니다.*

| 개념 | 정의 | Agent 관점 |
|---|---|---|
| Table | 행·열 형태로 데이터를 저장하는 기본 단위 | 고객·계약·현장·하자 등 상태의 원천 |
| Join | 공통 키를 기준으로 여러 테이블을 연결하는 연산 | 분리된 상태를 하나의 Context로 결합 |
| View | 조회 쿼리 결과를 가상 테이블처럼 재사용하는 DB 객체 | Agent가 읽기 쉬운 형태로 조회 인터페이스를 제공 가능 |

> 중요한 구분 View와 Mart는 다르다. View는 쿼리 결과를 재사용하는 DB 객체이고, Mart는 특정 분석·업무 목적을 위해 구성된 데이터 영역이다.

## 2. ETL과 ELT

차이는 “Transform을 언제 수행하느냐”입니다.

[![ETL과 ELT의 처리 순서 비교](/assets/images/data-arch-03-etl-elt.png)](/assets/images/data-arch-03-etl-elt.png)
*그림 3. ETL과 ELT의 처리 순서 비교 — 클릭하면 원본 크기로 볼 수 있습니다.*

- ETL: Extract → Transform → Load. 적재 전에 정제·변환한다.
- ELT: Extract → Load → Transform. 먼저 저장하고, 강력한 Warehouse/Lakehouse 컴퓨팅에서 변환한다.
- 현대 클라우드 데이터 플랫폼에서는 ELT 패턴이 자주 사용되지만, 실제 선택은 보안·비용·지연시간·데이터 품질 요구에 따라 달라진다.

> Agent 연결 Agent가 안정적으로 동작하려면 “원천 데이터를 가져오는 과정”과 “Agent가 읽는 상태를 만드는 변환 과정”을 분리해 설계하는 편이 관리에 유리하다.

## 3. Data Lake

원본 중심의 대규모·유연한 저장 계층입니다.

[![Data Lake가 수용하는 다양한 데이터 형식](/assets/images/data-arch-04-data-lake.png)](/assets/images/data-arch-04-data-lake.png)
*그림 4. Data Lake가 수용하는 다양한 데이터 형식 — 클릭하면 원본 크기로 볼 수 있습니다.*

- CSV·JSON·로그뿐 아니라 PDF·이미지·음성·영상·센서 데이터까지 폭넓게 보관할 수 있다.
- 장점은 유연성과 원본 보존이다. 단점은 메타데이터·거버넌스가 약하면 “Data Swamp”가 될 수 있다는 점이다.
- RAG/멀티모달 Agent에서는 문서·이미지·로그 등 비정형 데이터의 원천 저장 계층으로 연결될 수 있다.

> 비유 Data Lake는 “원재료 창고”에 가깝다. 일단 다양한 재료를 보존하고, 실제 분석이나 Agent 업무에 필요한 형태로 후속 가공한다.

## 4. Data Warehouse

전사 데이터를 공통 기준으로 통합한 분석용 저장소입니다.

[![여러 원천 데이터를 공통 기준으로 통합하는 Data Warehouse](/assets/images/data-arch-05-data-warehouse.png)](/assets/images/data-arch-05-data-warehouse.png)
*그림 5. 여러 원천 데이터를 공통 기준으로 통합하는 Data Warehouse — 클릭하면 원본 크기로 볼 수 있습니다.*

- 단순히 여러 DB를 한 곳에 복사하는 것이 아니라, 코드·ID·시간·단위·업무 기준을 표준화한다.
- 예: ERP의 P-1001, 쇼핑몰의 A100이 동일 상품이라면 공통 product_id로 매핑해 전사 분석이 가능해진다.
- Warehouse는 전사 KPI, 리포트, 분석 모델, Mart의 공통 기반이 된다.

> 교정 포인트 “MSSQL과 MySQL이 Warehouse 안에 들어간다”기보다는, 그 시스템의 데이터가 추출되어 Warehouse의 공통 모델로 통합된다고 이해하는 편이 정확하다.

## 5. Data Mart

특정 부서·업무·분석 목적을 위해 가공된 데이터 영역입니다.

[![Enterprise Data Warehouse에서 업무별 Data Mart로 분기](/assets/images/data-arch-06-data-mart.png)](/assets/images/data-arch-06-data-mart.png)
*그림 6. Enterprise Data Warehouse에서 업무별 Data Mart로 분기 — 클릭하면 원본 크기로 볼 수 있습니다.*

- 예: marketing_daily 마트에는 날짜, 제품, 캠페인, 광고비, 주문수, 매출, ROAS처럼 마케팅 의사결정에 필요한 필드만 둔다.
- Mart를 만들 때 Join, 집계, 파생지표 계산, 필터링, 비즈니스 규칙 적용 등이 수행될 수 있다.
- 따라서 사용자가 느낀 “여러 테이블을 합쳐 보기 좋은 형태를 만든다”는 감각은 맞지만, Mart의 본질은 Join 기능이 아니라 목적별 완성 데이터다.

> Agent용 Mart 패턴 특정 Agent가 반복적으로 같은 상태를 필요로 한다면 Agent용 Mart/View/Feature Table을 둘 수 있다. 다만 이것은 선택 가능한 설계 패턴이지, 모든 Agent에 필수인 표준 구성은 아니다.

## 6. Fact · Dimension · Star Schema

분석 질의를 빠르고 이해하기 쉽게 만드는 대표적인 DW 모델링 방식입니다.

[![fact_sales를 중심으로 Dimension이 연결되는 Star Schema](/assets/images/data-arch-07-star-schema.png)](/assets/images/data-arch-07-star-schema.png)
*그림 7. fact_sales를 중심으로 Dimension이 연결되는 Star Schema — 클릭하면 원본 크기로 볼 수 있습니다.*

| 구성 | 역할 | 예 |
|---|---|---|
| Fact | 업무 사건과 측정값을 저장 | 매출, 수량, 비용, 클릭, 주문 |
| Dimension | Fact를 설명하는 기준·속성 | 제품, 고객, 날짜, 캠페인, 현장 |
| Star Schema | 중앙 Fact + 주변 Dimension 구조 | 분석 쿼리 단순화, BI 친화적 구조 |

> Agent 연결 Agent가 “현재 고객의 계약과 현장, 최근 하자 이력, 위험도”를 판단해야 한다면, 잘 모델링된 키와 관계가 Context 생성의 정확도를 좌우한다.

## 7. Data Mart 갱신과 배포

“배포한다”는 감각은 맞지만, 데이터 실무에서는 적재·갱신·Refresh·Publish라는 표현을 더 자주 씁니다.

[![Full Refresh, Incremental, Batch, Streaming 비교](/assets/images/data-arch-08-refresh-modes.png)](/assets/images/data-arch-08-refresh-modes.png)
*그림 8. Full Refresh, Incremental, Batch, Streaming 비교 — 클릭하면 원본 크기로 볼 수 있습니다.*

- Full Refresh: 기존 결과를 전체 재계산한다. 단순하지만 데이터가 크면 비용이 크다.
- Incremental Load: 마지막 처리 이후 새로 생기거나 변경된 데이터만 반영한다.
- Batch: 매시간·매일처럼 스케줄에 따라 주기적으로 처리한다.
- Streaming: 이벤트가 발생하는 즉시 또는 거의 실시간으로 반영한다.

> 실무 표현 “매일 새벽 2시에 Warehouse의 주문·상품·광고 데이터를 Join/집계해서 mart_marketing_daily를 Incremental로 갱신하고, BI에 Publish한다.”라고 말하면 상당히 정확하다.

## 8. 왜 이 개념이 Agent · Action 설계에 중요한가

데이터 구조는 Agent가 세상을 보는 방식, Action 구조는 Agent가 세상에 개입하는 방식을 결정합니다.

[![그림 9. 에이전트 구조 전체 흐름 — Data → State → Decision → Action → New State](/assets/images/data-arch-09-agent-flow.png)](/assets/images/data-arch-09-agent-flow.png)
*그림 9. 에이전트 구조 전체 흐름 — Data → State → Decision → Action → New State — 클릭하면 원본 크기로 볼 수 있습니다.*

- Data Layer: Lake, Warehouse, Mart, View, API 등을 통해 신뢰 가능한 데이터를 제공한다.
- State / Context: 현재 업무 판단에 필요한 정보만 묶는다. “현재 무엇이 사실인가?”를 표현하는 계층이다.
- Decision: Rule, Policy, LLM 또는 이들의 조합이 다음 행동을 판단한다.
- Allowed Actions: 현재 State, 사용자 권한, 업무 정책에 따라 실행 가능한 Action만 남긴다.
- Action / Tool: ERP 조회·수정, CRM 티켓 생성, 문자/메일 발송, 승인 요청 등 실제 시스템에 변화를 만든다.
- Control Plane: RBAC, 승인(HITL), 감사로그, 예외처리, 재시도, 안전장치를 통해 실행을 통제한다.


### 계층별로 나눠 보면

위 루프에서 실제 설계가 갈리는 지점은 세 곳입니다. **무엇을 상태로 볼 것인가**, **그 상태에서 무엇을 허용할 것인가**, 그리고 **허용된 것을 어떻게 실행할 것인가**입니다.

[![그림 9-1. State / Context와 Agent Mart — 원천을 다 뒤지지 않고 판단에 필요한 상태만 구조화한다](/assets/images/data-arch-10-state-context.png)](/assets/images/data-arch-10-state-context.png)
*그림 9-1. State / Context와 Agent Mart — 원천을 다 뒤지지 않고 판단에 필요한 상태만 구조화한다 — 클릭하면 원본 크기로 볼 수 있습니다.*

[![그림 9-2. Decision과 Allowed Actions — 모든 행동이 아니라 현재 허용된 행동만 좁혀 고른다](/assets/images/data-arch-11-decision-allowed-actions.png)](/assets/images/data-arch-11-decision-allowed-actions.png)
*그림 9-2. Decision과 Allowed Actions — 모든 행동이 아니라 현재 허용된 행동만 좁혀 고른다 — 클릭하면 원본 크기로 볼 수 있습니다.*

[![그림 9-3. Action / Tool 실행 구조 — 결정이 실제 시스템 변경으로 이어지는 지점](/assets/images/data-arch-12-action-tool.png)](/assets/images/data-arch-12-action-tool.png)
*그림 9-3. Action / Tool 실행 구조 — 결정이 실제 시스템 변경으로 이어지는 지점 — 클릭하면 원본 크기로 볼 수 있습니다.*

> 가장 중요한 문장 Table · Join · View · Mart는 Agent가 세상을 “어떻게 볼 것인가”를 설계하는 문제이고, Tool · Action은 Agent가 세상에 “무엇을 할 수 있는가”를 설계하는 문제다.

## 9. 예시: 건설 하자 처리 Agent

Raw Data를 그대로 LLM에 던지는 대신, 업무 상태와 행동공간을 구조화합니다.

[![그림 10. 건설 하자 Agent — 접수부터 상태 갱신까지 Data → State → Decision → Action](/assets/images/data-arch-13-defect-agent-example.png)](/assets/images/data-arch-13-defect-agent-example.png)
*그림 10. 건설 하자 Agent — 접수부터 상태 갱신까지 Data → State → Decision → Action — 클릭하면 원본 크기로 볼 수 있습니다.*

| 레이어 | 예시 | 설계 포인트 |
|---|---|---|
| 원천 데이터 | ERP, CRM, 계약 DB, 하자 DB, 현장 DB, PDF, 사진 | 원천별 ID·권한·갱신주기를 파악 |
| Context / State | 보증기간, 하자유형, 재발횟수, 담당팀, 현재상태, 위험도 | Agent의 판단에 필요한 최소 상태를 명확히 정의 |
| Decision | 보증 유효 여부, 위험도, 담당자 미배정 여부 | Rule/Policy와 LLM의 책임 범위를 분리 |
| Allowed Action | 조회, 담당자 배정, 유상수리 안내, 상담원 연결 | 상태·권한에 따라 행동공간을 선제적으로 축소 |
| Execution | CRM 티켓, 문자, ERP 업데이트 | 실행 전 승인·검증·감사로그 적용 |

> Action Space Pruning 전체 Tool을 LLM에게 무제한으로 노출하기보다, State + Policy + 권한으로 “현재 가능한 행동”을 먼저 좁힌 뒤 Agent가 선택하게 만들면 안전성과 예측가능성이 높아진다.

## 10. 데이터 개념과 Agent 개념의 대응

두 영역을 연결해 기억하면 구조가 훨씬 빠르게 잡힙니다.

| 데이터 개념 | Agent/업무 자동화에서의 역할 | 주의 |
|---|---|---|
| Data Lake | 문서·사진·로그 등 원본 근거 저장 | 직접 조회만으로는 품질·검색성이 낮을 수 있음 |
| Data Warehouse | 전사 공통 데이터와 기준 제공 | 실시간 트랜잭션 DB와 역할 구분 필요 |
| Data Mart / View | 특정 Agent/업무에 필요한 읽기 모델 제공 | Agent Mart가 항상 필요한 것은 아님 |
| Table / Join | 상태 데이터와 관계를 구성 | 키 품질과 데이터 정합성이 핵심 |
| State / Context | 현재 판단에 필요한 업무 상태 | 너무 많으면 Context 오염, 너무 적으면 오판 |
| Policy / Rule | 행동 가능 범위와 조건 통제 | LLM 추론과 결정권한을 혼동하지 않기 |
| Tool / Action | 외부 시스템 조회·변경 | 읽기와 쓰기 Action의 위험도 차등 관리 |
| Audit / Event | 실행 결과를 기록하고 새 상태로 반영 | 추적성·재현성·책임소재 확보 |

> 전체 루프 Observation/Data → State/Context → Policy/Decision → Allowed Actions → Tool Execution → Event/Log → New State. 이 루프가 기업용 Agent의 기본 동작 구조다.

[![그림 11. Feedback Loop와 운영 로그 — 실행 결과가 다시 데이터가 되어 다음 판단을 바꾼다](/assets/images/data-arch-14-feedback-loop.png)](/assets/images/data-arch-14-feedback-loop.png)
*그림 11. Feedback Loop와 운영 로그 — 실행 결과가 다시 데이터가 되어 다음 판단을 바꾼다 — 클릭하면 원본 크기로 볼 수 있습니다.*

## 11. 실제 Agent 설계 시 체크리스트

데이터와 Action을 한 번에 설계할 때 확인할 항목입니다.

> 1. State 정의 Agent가 판단하기 위해 반드시 알아야 하는 현재 사실은 무엇인가?

> 2. Source of Truth 각 State 값의 원천 시스템은 어디이며 누가 수정 권한을 갖는가?

> 3. Join Key 고객·계약·현장·상품·사건을 연결하는 공통 키가 신뢰 가능한가?

> 4. Freshness State는 실시간, 시간 단위, 일 단위 중 어느 수준으로 갱신되어야 하는가?

> 5. Read Model Agent용 View/Mart/API를 따로 둘 필요가 있는가?

> 6. Action Space Agent가 가능한 모든 Action은 무엇이며, 상태별 허용 Action은 무엇인가?

> 7. Authorization 사용자·Agent·Tool별 권한(RBAC/ABAC)을 어떻게 적용하는가?

> 8. HITL 금액·계약·삭제·고객 통지 등 어떤 Action에 사람 승인이 필요한가?

> 9. Audit 누가, 어떤 State에서, 왜, 어떤 Action을 실행했는지 재현 가능한가?

> 10. Feedback Loop 실행 결과가 새로운 Event/State로 돌아와 다음 판단에 반영되는가?

### 최종 정리

데이터 엔지니어링의 관점에서는 “원천 데이터를 신뢰 가능한 분석·업무 데이터로 만드는 것”이 핵심이고, Agent 엔지니어링의 관점에서는 “그 상태를 바탕으로 가능한 행동을 통제하고 실행하는 것”이 핵심입니다.

따라서 기업용 Agent를 설계할 때는 LLM 프롬프트만 보지 말고, Data Model → State Model → Decision Policy → Action Model → Control/Audit를 하나의 시스템으로 설계해야 합니다.

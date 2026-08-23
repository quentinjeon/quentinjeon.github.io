---
layout: single
title: "문서와 대화하는 챗봇에서, 일을 끝내는 에이전트까지"
excerpt: "문서 질의응답 · 폴더 워크스페이스 · 커넥터와 툴 · 다중 워커 · 자율 실행. 전부 에이전트라 부르지만 서로 다른 수준의 아키텍처다. 5단계로 구분하고 하나로 합친다."
categories:
  - ax
  - foundation
tags:
  - AI Agent
  - Agent Architecture
  - RAG
  - Multi-Agent
  - Orchestration
  - Human-in-the-loop
  - Tool Permission
  - Vibe Agent Workspace
toc: true
toc_sticky: true
header:
  teaser: /assets/images/thumbs/folder-agent.jpg
---

**폴더형 에이전트 5단계 아키텍처.**

요즘은 문서에 질문하는 기능도 에이전트라고 부르고, 여러 파일을 읽는 시스템도 에이전트라고 부른다. Gmail이나 Notion에 연결되면 더 강한 에이전트처럼 보이고, 여러 개의 AI가 역할을 나눠 일하면 멀티 에이전트라고 부른다.

하지만 이 구조들을 한 단어로만 묶으면 무엇을 만들고 있는지 불분명해진다.

문서와 대화하는 시스템, 폴더 전체를 이해하는 시스템, 외부 시스템에서 실제 행동을 수행하는 시스템, 여러 워커를 조율하는 시스템, 목표가 완료될 때까지 반복 실행하는 시스템은 서로 다른 수준의 아키텍처다.

이 글에서는 이를 다음 5단계로 구분한다.

```text
1단계: 문서와 대화
2단계: 폴더·워크스페이스와 대화
3단계: 커넥터·툴 사용
4단계: 여러 워커 작업 분배
5단계: 반복 실행과 자율 운영
```

그리고 마지막에는 이 다섯 단계를 하나의 통합 아키텍처로 연결한다.

---

### 먼저, 에이전트를 한 문장으로 정의해보자

에이전트는 단순히 문서를 읽거나 답변을 생성하는 모델이 아니다.

> **에이전트는 목표를 해석하고, 현재 상태를 읽고, 다음 행동을 선택하고, 필요한 툴과 워커를 실행하고, 결과를 검증하며, 완료 조건을 충족할 때까지 상태를 갱신하는 시스템이다.**

이를 구성요소로 표현하면 다음과 같다.

```text
Agent
= Workspace
+ Knowledge
+ Memory
+ Planner
+ Workers
+ Tools
+ Connectors
+ Execution Loop
+ Governance
```

각 요소의 역할은 분명하다.

| 구성요소 | 역할 |
|---|---|
| 문서 | 에이전트가 읽는 지식 |
| 폴더·워크스페이스 | 목적, 규칙, 상태, 작업, 산출물을 담는 작업공간 |
| 메모리 | 이전 결정, 실행 이력, 현재 작업 상태 |
| 커넥터 | Gmail, Drive, Notion, DB 등 외부 시스템에 접근하는 통로 |
| 툴 | 검색, 읽기, 쓰기, 전송, 실행 등 실제 행동 |
| 워커 | 명확한 입력을 받아 전문 작업을 수행하는 실행 단위 |
| 오케스트레이터 | 작업을 분해하고 워커와 툴을 선택하는 조정자 |
| 러너 | 계획된 작업을 실제로 실행하는 런타임 |
| 정책 엔진 | 권한, 승인, 금지사항, 위험 통제 |
| 검증기 | 결과가 완료 기준과 근거 요건을 충족하는지 확인 |

---

## 1단계. 문서와 대화

[![1단계 — 문서와 대화](/assets/images/folder-agent-01-document-chat.svg)](/assets/images/folder-agent-01-document-chat.svg)
*STEP 1. 문서와 대화 — 단일 문서 기반 질의 — 클릭하면 원본 크기로 볼 수 있습니다.*

1단계는 하나의 문서 또는 제한된 문서 묶음 안에서 답을 찾는 구조다.

```text
사용자 질문
   ↓
질문 분석
   ↓
문서 검색
   ↓
관련 문단 추출
   ↓
답변 생성
   ↓
근거 제시
   ↓
충분성 검사
```

예를 들어 사용자가 계약서를 올리고 다음과 같이 질문한다고 하자.

> 이 계약서의 계약 기간은 언제까지인가?

시스템은 계약서에서 기간과 관련된 조항을 찾고, 해당 문장을 근거로 답변한다.

### 1단계의 핵심 구성요소

```text
Document Loader
Chunker
Embedding Model
Vector Index
Retriever
Answer Generator
Citation Formatter
Sufficiency Checker
```

가장 중요한 것은 마지막의 `Sufficiency Checker`다. 관련 문장을 찾았다는 이유만으로 답변을 확정하면 안 된다.

다음 조건을 확인해야 한다.

- 질문에 직접 대응하는 근거가 있는가
- 조항의 앞뒤 조건과 예외를 함께 확인했는가
- 폐지되거나 이전 버전의 문서를 인용하지 않았는가
- 답변이 문서에 없는 내용을 추측하지 않았는가
- 인용 위치를 사용자가 다시 확인할 수 있는가

### 1단계가 잘하는 일

- 계약서 조항 확인
- 매뉴얼 사용법 질의
- 보고서 요약
- 특정 규정 검색
- 회의록 핵심 내용 추출
- 문서 기반 비교표 작성

### 1단계의 한계

1단계 시스템은 문서 안에서 답할 수는 있지만, 프로젝트 전체의 현재 상태를 알지는 못한다.

```text
문서의 내용은 안다.
프로젝트의 맥락은 모른다.
```

예를 들어 계약서와 회의록의 내용이 다르거나, 최신 견적서가 별도 파일에 존재한다면 단일 문서 질의만으로는 해결할 수 없다.

따라서 1단계는 엄밀히 말하면 완전한 에이전트라기보다 **문서 기반 어시스턴트**에 가깝다.

### 1단계 종료 조건

```text
근거 충족도 >= 기준값
질문 범위 충족도 >= 기준값
다른 문서와 비교할 필요 없음
외부 시스템에서 최신 정보를 가져올 필요 없음
실제 행동을 수행할 필요 없음
```

이 조건을 만족하지 못하면 2단계로 올라간다.

---

## 2단계. 폴더·워크스페이스와 대화

[![2단계 — 폴더·워크스페이스와 대화](/assets/images/folder-agent-02-workspace-chat.svg)](/assets/images/folder-agent-02-workspace-chat.svg)
*STEP 2. 폴더·워크스페이스와 대화 — 문서 간 맥락 이해 — 클릭하면 원본 크기로 볼 수 있습니다.*

2단계부터 시스템은 하나의 문서가 아니라 **업무 공간 전체**를 이해한다.

```text
workspace/
├── AGENT.md
├── GOAL.md
├── CONTEXT.md
├── RULES.md
├── TASKS.md
├── POLICIES.md
├── inputs/
├── memory/
├── drafts/
├── outputs/
└── logs/
```

여기서 폴더는 단순한 파일 저장소가 아니다.

> **폴더는 목적, 지식, 규칙, 기억, 작업, 산출물, 실행 이력을 담는 상태 컨테이너다.**

에이전트는 현재 폴더를 읽으면서 다음을 이해한다.

```text
이 프로젝트의 목표가 무엇인가
현재 어떤 작업이 진행 중인가
어떤 문서가 공식 원본인가
이전에 어떤 결정이 내려졌는가
어떤 산출물이 이미 만들어졌는가
아직 해결되지 않은 쟁점은 무엇인가
```

### 2단계의 실행 흐름

```text
사용자 요청
   ↓
워크스페이스 식별
   ↓
GOAL / CONTEXT / RULES 로드
   ↓
관련 문서 후보 탐색
   ↓
다중 문서 비교
   ↓
일치·불일치·누락 탐지
   ↓
프로젝트 맥락을 반영한 답변
   ↓
상태 또는 산출물 업데이트
```

### 2단계가 1단계와 다른 점

| 구분 | 1단계 | 2단계 |
|---|---|---|
| 검색 범위 | 단일 문서 또는 제한된 문서 | 프로젝트 폴더 전체 |
| 문맥 | 질문과 문서 내용 | 목표, 규칙, 진행상태, 과거 결정 |
| 비교 | 제한적 | 문서 간 비교 가능 |
| 상태 | 거의 없음 | 작업 상태와 산출물 상태를 관리 |
| 기억 | 대화 컨텍스트 중심 | 프로젝트 메모리 활용 |
| 결과 | 답변 | 답변, 비교, 상태 갱신, 초안 생성 |

### 문서 간 충돌을 처리하는 방법

폴더 단위로 일하기 시작하면 가장 먼저 나타나는 문제가 문서 간 불일치다.

예를 들면 다음과 같다.

```text
계약서: 납기 10월 31일
회의록: 납기 11월 15일로 협의
일정표: 납기 11월 30일
```

이때 시스템은 임의로 하나를 고르면 안 된다.

올바른 답변 구조는 다음과 같다.

```text
1. 공식 기준
2. 다른 문서의 내용
3. 충돌 지점
4. 최신성·권위·승인 여부
5. 현재 적용할 수 있는 기준
6. 확인이 필요한 담당자
```

### 현업 적용 예시: 법령과 내부정책이 다른 경우

법령과 내부정책은 하나의 문장으로 합치면 안 된다.

```text
Legal Knowledge Base
├── 법률
├── 시행령
├── 시행규칙
├── 고시
└── 유권해석

Internal Policy Base
├── 사규
├── 안전규정
├── 보안정책
├── 업무매뉴얼
└── SOP
```

검색은 각각 수행하고, 비교 단계에서 합친다.

```text
법령 검색
   ┐
   ├── 적용범위 비교
   ┘
내부정책 검색
       ↓
시행일·버전 확인
       ↓
의무·금지·허용·권고 분류
       ↓
충돌 유형 판정
       ↓
우선 적용 기준과 실제 조치 제시
```

답변은 최소한 다음 형식을 가져야 한다.

```text
[결론]
법령 기준과 내부정책 기준이 다릅니다.

[법령 기준]
관련 법령 제○조는 A를 요구합니다.

[내부정책 기준]
내부규정 제○조는 B를 요구합니다.

[차이 및 충돌]
내부정책이 법령 기준보다 완화되어 있습니다.

[실제 조치]
법령 기준을 우선 적용하고 내부정책 개정을 검토해야 합니다.
```

중요한 것은 답변의 유창함이 아니라 **권위, 최신성, 적용범위, 시행시점**을 분리해서 보여주는 것이다.

---

## 3단계. 커넥터·툴 사용

[![3단계 — 커넥터·툴 사용](/assets/images/folder-agent-03-connectors-tools.svg)](/assets/images/folder-agent-03-connectors-tools.svg)
*STEP 3. 커넥터·툴 사용 — 외부 시스템 연동 및 실행 — 클릭하면 원본 크기로 볼 수 있습니다.*

3단계부터 시스템은 정보를 읽는 수준을 넘어 실제 행동을 수행한다.

```text
Google Drive
Gmail
Notion
Slack
GitHub
Database
ERP
CRM
Calendar
Internal API
```

여기서 커넥터와 툴을 구분해야 한다.

```text
Connector = 외부 시스템에 접근하는 통로
Tool      = 그 시스템에서 수행하는 구체적인 행동
```

예를 들어 Gmail은 커넥터고, 그 안에서 실행하는 기능은 툴이다.

```text
Gmail Connector
├── search_email
├── read_thread
├── download_attachment
├── create_draft
├── send_email
└── add_label
```

### 3단계의 실행 흐름

```text
사용자 요청
   ↓
워크스페이스 상태 확인
   ↓
외부 정보 필요 여부 판단
   ↓
커넥터 선택
   ↓
툴 호출
   ↓
외부 시스템 결과 수집
   ↓
결과 검증
   ↓
폴더 상태 또는 산출물 업데이트
```

예를 들어 사용자가 다음과 같이 요청한다고 하자.

> 최근 고객 요청사항까지 확인해서 제안서를 수정해줘.

시스템은 다음 순서로 작동한다.

```text
1. 현재 제안서 폴더 확인
2. Gmail에서 고객명과 최근 기간으로 검색
3. 관련 메일과 첨부파일 읽기
4. 요구사항을 기존 PRD와 비교
5. 수정 대상 섹션 식별
6. 제안서 초안 수정
7. outputs/에 새 버전 저장
8. 변경사항과 근거를 사용자에게 보고
```

### 툴 실행에는 권한과 승인 정책이 필요하다

모든 툴을 같은 수준으로 취급하면 위험하다.

```text
낮은 위험
- search
- read
- summarize

중간 위험
- create_draft
- update_internal_file
- create_calendar_draft

높은 위험
- send_email
- delete_file
- publish_content
- execute_payment
- modify_production_data
```

따라서 툴마다 실행 정책을 설정해야 한다.

```yaml
tool: gmail.send_email
risk_level: high
approval_required: true
allowed_roles:
  - communication_agent
audit_log: required
```

좋은 에이전트는 많은 툴을 가진 시스템이 아니라, **언제 어떤 툴을 사용할지 판단하고 위험한 행동을 통제하는 시스템**이다.

---

## 4단계. 여러 워커 작업 분배

[![4단계 — 여러 워커 작업 분배](/assets/images/folder-agent-04-multi-worker-orchestration.svg)](/assets/images/folder-agent-04-multi-worker-orchestration.svg)
*STEP 4. 여러 워커에게 작업 분배 — 다중 전문 에이전트 협업 — 클릭하면 원본 크기로 볼 수 있습니다.*

작업이 복잡해지면 하나의 에이전트가 모든 문맥을 들고 모든 판단을 수행하는 방식은 비효율적이다.

이때 오케스트레이터가 작업을 분해하고, 전문 워커에게 나눈다.

```text
Orchestrator
├── Research Worker
├── Document Analysis Worker
├── Financial Analysis Worker
├── Writer Worker
├── Validator Worker
├── Communication Worker
└── File Generator Worker
```

워커는 에이전트와 다르다.

> **워커는 명확한 입력을 받아 명확한 출력을 만드는 전문 실행 단위다.**

> **오케스트레이터는 어떤 워커에게 어떤 일을 어떤 순서로 맡길지 결정한다.**

### 4단계의 실행 흐름

```text
목표 수신
   ↓
작업 분해
   ↓
하위 작업 간 의존성 분석
   ↓
병렬·순차 실행 계획
   ↓
워커별 입력 패키지 생성
   ↓
워커 실행
   ↓
결과 수집
   ↓
통합
   ↓
교차 검증
```

### 제안서 작성 예시

```text
Research Worker
- 고객 요청사항 수집
- 이전 미팅 결정 확인

Analysis Worker
- 요구사항 구조화
- 문제·기회·우선순위 분석

Financial Worker
- 구축비·운영비·ROI 계산

Writer Worker
- 제안서 본문 작성

Validator Worker
- 누락, 충돌, 수치 오류 검증

File Worker
- Markdown, PPT, PDF 산출물 생성
```

오케스트레이터는 각 워커에게 전체 프로젝트를 통째로 넘기지 않는다. 필요한 맥락만 선별하여 전달한다.

```yaml
task_id: proposal-section-03
worker: writer
objective: "도입 범위와 단계별 추진안을 작성한다."
inputs:
  - requirements_summary.md
  - architecture_decision.md
  - pricing_assumptions.xlsx
constraints:
  - "고객이 요청하지 않은 기능은 포함하지 않는다."
  - "1단계와 2단계 범위를 명확히 분리한다."
output:
  - drafts/proposal-section-03.md
```

### 여러 워커를 쓰기 좋은 조건

- 전문 영역이 명확히 나뉘는가
- 하위 작업을 독립적으로 수행할 수 있는가
- 병렬 처리가 실제 시간을 줄이는가
- 작성자와 검증자를 분리할 필요가 있는가
- 결과물 종류가 여러 개인가
- 단일 모델 컨텍스트에 모든 자료를 넣는 것이 비효율적인가

워커 수가 많다고 좋은 아키텍처는 아니다. 작은 작업을 과도하게 분해하면 조율 비용이 실행 비용보다 커진다.

---

## 5단계. 반복 실행과 자율 운영

[![5단계 — 반복 실행과 자율 운영](/assets/images/folder-agent-05-autonomous-loop.svg)](/assets/images/folder-agent-05-autonomous-loop.svg)
*STEP 5. 반복 실행과 자율 운영 — 계획→실행→검증→재실행 — 클릭하면 원본 크기로 볼 수 있습니다.*

5단계에서는 한 번의 실행으로 끝내지 않는다.

목표를 기준으로 결과를 검증하고, 부족하면 원인을 분석하고, 계획을 수정하여 다시 실행한다.

```text
Observe
   ↓
Decide
   ↓
Act
   ↓
Verify
   ↓
Update
   └────────→ 반복
```

이를 실제 업무 흐름으로 풀면 다음과 같다.

```text
목표 확인
   ↓
현재 상태 관찰
   ↓
작업 계획
   ↓
워커·툴 실행
   ↓
결과 검증
   ↓
완료 기준 미충족
   ↓
원인 분석
   ↓
재계획
   ↓
재실행
```

### 5단계에서 가장 중요한 것은 완료 조건이다

완료 조건이 없으면 에이전트는 끝없이 수정하거나, 반대로 너무 일찍 멈출 수 있다.

```yaml
completion_criteria:
  requirement_coverage: 1.0
  evidence_coverage: 0.9
  unresolved_high_risk_issue_count: 0
  validation_passed: true
  human_approval_required: true
```

예를 들어 제안서 작업이라면 다음처럼 검증할 수 있다.

```text
요구사항 12개가 모두 반영되었는가
금액 합계가 일치하는가
일정 간 충돌이 없는가
고객이 요청하지 않은 범위가 추가되지 않았는가
모든 핵심 주장에 근거가 있는가
최종 발송 전에 사람이 승인했는가
```

### 재시도에도 제한이 필요하다

자율 실행은 무제한 실행을 의미하지 않는다.

```yaml
execution_policy:
  max_iterations: 5
  max_tool_calls: 30
  max_cost_usd: 5
  stop_on_repeated_error: 2
  require_human_on:
    - legal_conflict
    - external_send
    - destructive_action
    - budget_exceeded
```

### 사람 승인이 필요한 지점

다음 행동은 자율 실행보다 승인 게이트가 우선되어야 한다.

- 외부 이메일 발송
- 고객 시스템에 데이터 반영
- 파일 삭제 또는 덮어쓰기
- 계약 조건 변경
- 법령과 내부정책의 직접 충돌
- 금전 지급 또는 비용 확정
- 대외 공개
- 개인정보 또는 민감정보 처리

5단계의 핵심은 사람을 제거하는 것이 아니다.

> **사람이 판단해야 할 시점까지 시스템이 자료를 모으고, 비교하고, 실행하고, 검증하여 의사결정 비용을 줄이는 것**이 핵심이다.

---

## 6. 전체 통합 아키텍처

[![전체 통합 아키텍처](/assets/images/folder-agent-06-integrated-architecture.svg)](/assets/images/folder-agent-06-integrated-architecture.svg)
*전체 아키텍처 통합도 및 메모리·에스컬레이션 흐름 — 클릭하면 원본 크기로 볼 수 있습니다.*

다섯 단계를 하나의 시스템으로 합치면 다음과 같은 계층 구조가 된다.

### 6.1 사용자·트리거 계층

```text
사용자 요청
관리자 요청
일정 트리거
이메일 수신
파일 변경
API 이벤트
정기 실행
```

### 6.2 에이전트 제어 평면

```text
Intent Router
Workspace Resolver
Goal Interpreter
Planner
Task Decomposer
Context Loader
Tool / Worker Router
Verifier
Retry Controller
Completion Judge
```

이 계층은 실제 문서를 직접 처리하는 것보다 **무엇을 어떻게 처리할지 판단하는 역할**을 맡는다.

### 6.3 워크스페이스·상태 계층

```text
GOAL.md
CONTEXT.md
RULES.md
TASKS.md
POLICIES.md
memory/
inputs/
outputs/
runs/
logs/
```

여기에는 현재 프로젝트의 상태와 실행 이력이 저장된다.

### 6.4 문서·지식·메모리 계층

```text
Document Store
Vector Index
Metadata Index
Legal Knowledge Base
Internal Policy Base
Working Memory
Episodic Memory
Semantic Memory
Artifact Registry
```

중요한 원칙은 모든 자료를 하나의 벡터DB에 넣고 끝내지 않는 것이다.

문서 유형, 권위, 버전, 적용 범위, 시행일, 프로젝트, 고객, 보안등급을 메타데이터로 관리해야 한다.

### 6.5 워커·툴·커넥터 실행 계층

```text
Workers
   ↓
Tools
   ↓
Connectors
   ↓
External Systems
```

- 워커는 전문 작업을 수행한다.
- 툴은 실제 행동을 정의한다.
- 커넥터는 외부 시스템과 연결한다.
- 외부 시스템은 실제 데이터와 업무가 존재하는 곳이다.

### 6.6 정책·승인·관찰 계층

```text
Policy Engine
RBAC
Human Approval
Audit Log
Cost Monitor
Execution Monitor
Error Alert
Quality Evaluation
Version Control
```

이 계층은 모든 단계에 가로로 걸쳐 있어야 한다.

정책 엔진이 마지막에만 작동하면 이미 위험한 행동이 실행된 뒤일 수 있다. 따라서 계획 단계, 툴 선택 단계, 실행 직전, 실행 후 검증 단계에 모두 개입해야 한다.

---

## 진짜 핵심은 단계적 에스컬레이션이다

이 다섯 단계는 무조건 1단계부터 순서대로 실행하는 고정 파이프라인이 아니다.

시스템은 가장 낮은 비용으로 해결 가능한 단계에서 시작하고, 필요한 경우에만 상위 단계로 올라가야 한다.

```text
LEVEL 1. 문서 대화
    ↓ 근거 또는 범위 부족
LEVEL 2. 워크스페이스 탐색
    ↓ 외부 정보 또는 행동 필요
LEVEL 3. 커넥터·툴 실행
    ↓ 작업 복잡도 증가
LEVEL 4. 다중 워커 오케스트레이션
    ↓ 완료 기준 미충족
LEVEL 5. 재계획·반복 실행
    ↓ 고위험 또는 불확실
HUMAN APPROVAL
```

다만 사용자의 요청이 처음부터 실행을 포함하면 바로 3단계에서 시작할 수 있다.

```text
“메일을 찾아줘.”
→ 3단계

“제안서를 조사·작성·검증해서 완성해줘.”
→ 4단계

“매주 데이터를 확인하고 이상이 있으면 보고서를 갱신해줘.”
→ 5단계
```

단계 선택은 실패 여부만으로 결정하면 안 된다.

```text
근거 충족도
요구사항 충족도
정보 최신성
외부 행동 필요 여부
작업 복잡도
병렬화 가능성
위험도
완료 기준 충족 여부
```

이 기준을 조합하여 실행 단계를 선택해야 한다.

---

## 구현할 때 가장 먼저 정해야 할 것

### 1. 무엇을 만드는가

```text
프로젝트 폴더를 읽고
문서 간 관계를 파악하고
필요한 외부 시스템에 접근하고
전문 워커에게 작업을 나누고
완료 기준까지 결과를 검증하는
폴더형 에이전트 실행 시스템
```

### 2. 무엇을 만들지 않는가

```text
모든 요청에 여러 워커를 호출하지 않는다.
모든 대화를 장기 기억으로 저장하지 않는다.
근거 없이 외부 데이터를 수정하지 않는다.
사람 승인 없이 고위험 행동을 실행하지 않는다.
폴더가 존재한다는 이유만으로 에이전트라고 부르지 않는다.
LLM 하나에 모든 책임을 맡기지 않는다.
```

### 3. 다 됐다는 것을 어떻게 아는가

```text
요청한 범위가 모두 처리되었는가
각 주장에 확인 가능한 근거가 있는가
상태와 산출물이 올바른 위치에 저장되었는가
문서 간 충돌이 표시되었는가
외부 행동이 정책에 따라 승인되었는가
검증기가 완료 조건을 통과시켰는가
실행 이력과 오류가 로그에 남았는가
```

이 세 가지가 PRD의 핵심이다.

---

## 권장 개발 순서

처음부터 5단계 자율 에이전트를 만들 필요는 없다.

### Phase 1. 문서와 폴더

```text
문서 업로드
RAG 검색
근거 인용
폴더 구조 인식
다중 문서 비교
워크스페이스 상태 저장
```

### Phase 2. 툴과 커넥터

```text
Drive 읽기
Gmail 검색
파일 생성
초안 작성
DB 조회
권한과 감사로그
```

### Phase 3. 워커 오케스트레이션

```text
작업 분해
워커별 입력·출력 계약
병렬 실행
결과 병합
독립 검증
```

### Phase 4. 자율 실행

```text
완료 기준
실패 분류
재시도
재계획
비용 제한
승인 게이트
운영 모니터링
```

가장 현실적인 MVP는 1단계와 2단계를 견고하게 만든 뒤, 3단계의 일부 툴을 붙이는 것이다.

---

## GitHub 저장소 구조

GitHub에 올릴 때는 다음 구조를 권장한다.

```text
folder-agent-architecture/
├── README.md
└── images/
    ├── 01-document-chat.png
    ├── 02-workspace-chat.png
    ├── 03-connectors-tools.png
    ├── 04-multi-worker-orchestration.png
    ├── 05-autonomous-loop.png
    └── 06-integrated-architecture.png
```

이 글을 `README.md`로 사용하면 저장소 첫 화면에서 전체 내용을 바로 볼 수 있다.

이미지 파일명은 공백과 한글을 피하고 영문 소문자와 하이픈을 사용하는 편이 관리하기 쉽다.

---

## 마무리

문서와 대화하는 것부터 시작할 수 있다.

그다음에는 폴더 전체의 맥락을 이해하게 만들고, 커넥터와 툴을 제공해 실제 행동을 수행하게 한다. 작업이 복잡해지면 여러 워커에게 역할을 나누고, 결과가 기준에 미달하면 다시 계획하고 실행하게 만든다.

그러나 에이전트를 구성하는 것은 폴더, 문서, 툴, 워커의 존재 자체가 아니다.

```text
문서는 지식을 제공한다.
폴더는 맥락과 상태를 제공한다.
메모리는 이전 결정과 실행 이력을 제공한다.
커넥터는 외부 세계로 가는 통로를 제공한다.
툴은 실제 행동을 제공한다.
워커는 전문 실행 능력을 제공한다.
오케스트레이터는 순서와 역할을 결정한다.
러너는 계획을 실행한다.
정책 엔진은 위험한 행동을 통제한다.
검증기는 완료 여부를 판정한다.
```

이 모든 요소가 목표를 중심으로 연결되고 다음 루프가 작동할 때 비로소 에이전트가 된다.

```text
Observe → Decide → Act → Verify → Update
```

결국 폴더형 에이전트는 다음과 같이 정의할 수 있다.

> **폴더형 에이전트는 폴더를 목적·지식·규칙·기억·작업·산출물의 상태 컨테이너로 사용하고, 그 상태를 기준으로 문서, 워커, 툴, 커넥터를 선택하여 목표가 완료될 때까지 실행과 검증을 반복하는 시스템이다.**

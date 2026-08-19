---
layout: single
title: "프롬프트를 넘어 폴더로 AI 조직을 만든다: 내가 정의한 'Vibe Agent Workspace'"
excerpt: "폴더는 Agent가 아니라 Agent Workspace다. 자연어와 폴더로 AI 작업자와 AI 조직을 설계하는 파일시스템 기반 멀티에이전트 구조."
categories:
  - AI
tags:
  - Agent
  - Multi-Agent
  - Vibe Coding
  - Context Engineering
  - Workspace Engineering
toc: true
toc_sticky: true
header:
  teaser: /assets/images/vibe-agent-00-overview.png
---

최근 기업 AI 프로젝트를 하면서 한 가지 생각이 계속 들었다.

우리는 왜 AI를 항상 하나의 채팅창 안에서만 일하게 할까?

ChatGPT나 Claude를 쓰다 보면 처음에는 꽤 잘 작동한다.
요구사항을 설명하고, 자료를 넣고, PRD를 만들고, 코드를 작성하고, 다시 검토시킨다.

그런데 프로젝트가 조금만 커지면 문제가 생긴다.

```text
시장조사
+
고객 요구사항
+
회의록
+
PRD
+
코드
+
수정사항
+
테스트 결과
```

모든 정보가 하나의 대화 안에 쌓이기 시작한다.

그리고 어느 순간 AI에게 이런 말을 반복하게 된다.

> "아까 이야기했던 그 조건 기억하지?"
> "개발자 관점 말고 PM 관점에서 다시 봐줘."
> "이건 전에 결정했던 내용이야."

결국 AI의 성능 문제라기보다 업무 구조의 문제라는 생각이 들었다.

그래서 나는 최근 Agent를 조금 다른 방식으로 바라보기 시작했다.

## 처음 가설은 단순했다

처음에는 이렇게 생각했다.

폴더에 프롬프트와 파일을 넣고, 폴더를 크게 확장하면 Agent처럼 사용할 수 있지 않을까?

예를 들어:

```text
sales-agent/
├── prompt.md
├── customer.md
├── products.xlsx
└── result.md
```

처음 보면 꽤 그럴듯하다.

하지만 이것만으로는 Agent라고 부르기 어렵다.

폴더는 스스로 판단하지 않는다.
프롬프트가 있다고 해서 일을 시작하지도 않는다.

결국 이것은 잘 정리된 Context Folder일 뿐이다.

그래서 정의를 조금 바꿨다.

> **Folder = Agent가 아니라, Folder = Agent Workspace다.**

그리고 Agent를 다음처럼 정의했다.

```text
Agent
=
Role
+
Goal
+
Knowledge
+
Memory
+
State
+
Tools
+
Execution Loop
```

즉 폴더는 Agent 자체가 아니라,
AI 작업자의 역할, 기억, 업무, 자료, 결과물을 보관하는 작업 공간이다.

이 정의를 기준으로 시스템 전체를 다시 설계하기 시작했다.

## Vibe Agent Workspace

내가 이 구조에 붙인 이름은 Vibe Agent Workspace다.

[![Vibe Agent Workspace 전체 구조](/assets/images/vibe-agent-00-overview.png)](/assets/images/vibe-agent-00-overview.png)
*Vibe Agent Workspace 전체 구조 — 클릭하면 원본 크기로 볼 수 있습니다.*

한 문장으로 정의하면 다음과 같다.

> 자연어로 AI 작업자의 역할과 업무 방식을 정의하고, 각각의 작업자에게 독립적인 폴더 기반 Workspace를 부여한 뒤, Task와 Artifact를 통해 서로 협업하게 만드는 파일시스템 기반 Multi-Agent 시스템

조금 쉽게 표현하면 이렇다.

사람에게 책상 하나씩 주듯
AI에게 폴더 하나씩을 준다.

그리고 그 폴더 안에

```text
업무 지침
목표
참고자료
기억
해야 할 일
작업 중 자료
완료 결과물
```

을 넣는다.

## 왜 이런 생각을 하게 됐나

나는 최근 기업 대상으로 AI 프로젝트와 교육을 진행하면서 거의 반복적으로 같은 패턴을 봤다.

기업에서 AI를 적용한다고 하면 처음에는 대부분 이렇게 시작한다.

> "우리 회사 자료를 ChatGPT가 읽게 하면 안 되나요?"
> "이 업무 자동화할 수 없나요?"
> "엑셀 넣으면 분석해주는 시스템 만들고 싶습니다."

나도 실제 프로젝트에서 비슷한 문제들을 계속 다뤘다.

건설사의 사내 기준 문서를 검색하는 RAG 시스템을 설계하기도 했고,
영업 상담 내용을 자동으로 정리해서 CRM에 저장하는 Workflow를 만들기도 했다.

또 식품 제조업에서는 음성이나 자연어로 생산 상황을 기록하면 HACCP 관련 서류의 빈 항목을 찾아 추가 입력을 요청하는 구조도 설계했다.

상품정보, 채널정보, 월별 매출 데이터를 넣으면

```text
상품별 매출
상품별 이익
채널별 이익
상품 × 채널 수익성
```

을 분석하는 대시보드도 만들었다.

겉으로 보면 전혀 다른 프로젝트다.

그런데 업무 구조를 쪼개보면 거의 항상 같았다.

```text
INPUT
↓
PROCESS
↓
OUTPUT
```

그리고 Process를 더 잘게 쪼개면 결국 이렇게 변한다.

```text
누군가 자료를 읽는다
↓
누군가 판단한다
↓
누군가 결과물을 만든다
↓
누군가 검토한다
↓
다음 사람이 이어서 일한다
```

사실 회사가 일하는 방식 그대로다.

그렇다면 AI 역시 하나의 거대한 Prompt로 모든 일을 처리하게 하는 것보다 역할을 나눠주는 것이 자연스럽지 않을까?

## 내가 기존에 사용하던 Vibe Coding 방식

나는 AI를 활용한 시스템 개발을 설명할 때 거의 항상 다음 5단계를 사용한다.

```text
STEP 1
문제를 말한다

↓

STEP 2
Input / Process / Output으로 나눈다

↓

STEP 3
docs/PRD.md를 작성한다

↓

STEP 4
mock/index.html을 만든다

↓

STEP 5
실제 개발한다
```

예를 들어 누군가 이렇게 말한다.

> "매달 매출 엑셀 정리하는 데 너무 오래 걸립니다."

그러면 바로 개발하지 않는다.
먼저 업무를 분해한다.

**Input**

```text
상품정보.xlsx
채널정보.xlsx
월별매출.xlsx
```

**Process**

```text
상품 매칭
채널 매칭
매출 계산
원가 계산
이익 계산
이익률 계산
전월 비교
```

**Output**

```text
상품별 매출
채널별 매출
상품별 이익률
상품 × 채널 분석
월간 대시보드
```

그다음 PRD를 만든다.

이 방식은 꽤 잘 작동했다.

그런데 한 가지 한계가 있었다.

Process가 커지기 시작하면 누가 그 Process를 수행할 것인지 다시 분리해야 한다.

여기서 Vibe Agent라는 개념이 자연스럽게 이어졌다.

## Vibe Coding 다음은 Vibe Agent다

Vibe Coding의 질문은 이것이다.

> 무엇을 만들 것인가?

반면 Vibe Agent의 질문은 다르다.

> 누가 이 일을 할 것인가?

기존 흐름을 확장하면 다음과 같다.

```text
문제 정의
↓
Input / Process / Output
↓
업무 분해
↓
역할 분해
↓
Agent 정의
↓
Agent Workspace 생성
↓
Handoff 정의
↓
Orchestrator 연결
```

이렇게 되면 단순히 Software를 만드는 것이 아니라
Software 안에서 일하는 AI 작업자까지 설계하게 된다.

## 폴더 하나를 AI 작업자 하나로 본다

[![Agent Workspace 폴더 구조](/assets/images/vibe-agent-01-workspace.png)](/assets/images/vibe-agent-01-workspace.png)
*Agent Workspace 폴더 구조 — 클릭하면 원본 크기로 볼 수 있습니다.*

예를 들어 Planner Agent를 만든다고 해보자.

```text
agents/
└── planner/
    ├── AGENT.md
    ├── GOAL.md
    ├── RULES.md
    ├── TOOLS.md
    ├── HANDOFF.md
    │
    ├── knowledge/
    ├── memory/
    ├── inbox/
    ├── workspace/
    ├── outbox/
    └── logs/
```

각 파일의 역할은 명확하다.

### AGENT.md

이 AI가 누구인지 정의한다.

```text
당신은 Product Planner다.

주요 역할:
- 요구사항 분석
- 문제 정의
- PRD 작성
- 기능 우선순위 결정
```

### GOAL.md

무엇을 완료해야 하는지 정의한다.

```text
사용자의 요구사항을
개발 가능한 PRD로 변환한다.
```

완료 조건도 넣는다.

```text
문제 정의 존재
사용자 정의 존재
Input / Process / Output 존재
기능 요구사항 존재
Acceptance Criteria 존재
```

### RULES.md

무엇을 하면 안 되는지 정의한다.

```text
입력에 없는 사실을 만들지 않는다.

불확실한 내용은 Assumption으로 표시한다.

중요한 판단은 Human Review 대상으로 보낸다.
```

### TOOLS.md

이 Agent가 사용할 수 있는 도구를 정의한다.

```text
파일 읽기
파일 쓰기
웹 검색
DB 조회
Python
```

반대로 허용하지 않는 도구도 정의한다.

```text
프로덕션 배포
데이터 삭제
외부 이메일 발송
```

### HANDOFF.md

업무를 누구에게 넘길지 정의한다.

```text
Researcher의 결과를 받을 수 있다.

완료된 PRD는 Developer에게 전달한다.

Reviewer가 수정 요청하면 다시 Planner가 작업한다.
```

이렇게 하면 Prompt 한 개를 잘 만드는 것보다 훨씬 구조적이다.

## 중요한 것은 Agent끼리 '채팅'하게 만드는 것이 아니다

Multi-Agent라는 말을 들으면 흔히 AI들이 서로 대화하는 모습을 떠올린다.

하지만 내가 이 구조에서 중요하게 보는 부분은 조금 다르다.

> **Agent 간 Chat보다 Artifact Handoff가 중요하다.**

[![Task · Artifact · Handoff 구조](/assets/images/vibe-agent-03-handoff.png)](/assets/images/vibe-agent-03-handoff.png)
*Task · Artifact · Handoff 구조 — 클릭하면 원본 크기로 볼 수 있습니다.*

예를 들어:

```text
Planner
↓
prd.md

Developer
↓
build.md

Reviewer
↓
review-report.md
```

즉 AI가 서로 말만 주고받는 것이 아니라 업무 결과물을 파일로 남긴다.

실제 회사에서도 그렇다.

기획자가 개발자에게

> "내가 아까 말했던 것 기억하지?"

라고 하는 것보다

```text
PRD
요구사항 문서
디자인
티켓
```

을 전달하는 편이 훨씬 안정적이다.

AI 역시 동일하다.

### 이것이 중요한 이유: 기록이 남는다

Artifact 기반으로 협업하면 다음이 가능하다.

```text
누가 만들었는가

어떤 Task에서 만들었는가

몇 번째 버전인가

누가 검토했는가

수정 전 결과는 무엇인가
```

예를 들어 하나의 PRD를 다음처럼 관리할 수 있다.

```text
prd-v1.md
prd-v2.md
prd-v3.md
```

그리고 상태도 존재한다.

```text
CREATED
↓
READY
↓
RUNNING
↓
REVIEW
↓
COMPLETED
```

검토에서 문제가 발생하면

```text
REVIEW
↓
REVISION
↓
RUNNING
```

으로 돌아간다.

여기까지 가면 단순 Prompt Engineering보다는 AI Workflow System에 가까워진다.

## 실제 사례: 영업 상담 자동화

예를 들어 내가 만들었던 영업 상담 자동화 구조를 Agent 방식으로 다시 생각해볼 수 있다.

기존에는 다음 Workflow였다.

```text
상담내용 입력
↓
AI 요약
↓
관심사항 추출
↓
다음 할 일 추출
↓
CRM 저장
↓
담당자 알림
```

이걸 Agent 구조로 바꾸면 다음처럼 볼 수 있다.

**Intake Agent**

```text
상담 원문 확인
고객정보 확인
입력 누락 체크
```

↓

**Sales Analyst Agent**

```text
상담 요약
관심사항 추출
다음 할 일 추출
```

↓

**Reviewer Agent**

```text
가격이나 계약 내용을
AI가 임의로 만들지 않았는지 검토
```

↓

**CRM Agent**

```text
확정된 내용을 DB에 기록
```

기존 n8n Workflow를 없애는 것이 아니다.
오히려 n8n은 이런 구조의 Process 실행 엔진으로 사용할 수 있다.

## 실제 사례: 건설 RAG 시스템

건설사 프로젝트도 마찬가지다.

사내 기준, 현장 시방서, 법규, 안전자료가 모두 섞여 있는 환경에서 모든 자료를 하나의 RAG에 넣는 것은 가능하다.

하지만 실제 업무에서는 질문마다 필요한 지식 영역이 다르다.

예를 들어 질문이

> "이 공종의 사내 기준이 어떻게 돼?"

라면

```text
Internal Standard Agent
```

가 처리할 수 있다.

반면

> "법적으로 이 기준을 따라야 해?"

라면

```text
Regulation Agent
```

가 처리한다.

사고 사례가 필요하면

```text
Safety Agent
```

가 처리한다.

위에서 전체 질문을 판단하는 것은

```text
Knowledge Router
```

또는 Orchestrator다.

즉 실제로 내가 설계했던 지식 라우터 역시 Folder-based Agent 구조로 자연스럽게 확장할 수 있다.

## 실제 사례: HACCP 생산관리

식품 제조 현장에서 생각하면 더 명확하다.

사용자가 음성으로 말한다.

> "오늘 오전 9시에 생산 시작했고 원료 A 20kg 사용했습니다."

이를 하나의 AI가 모든 서류로 변환하게 할 수도 있다.

하지만 역할을 나누면 다음과 같다.

```text
Voice Intake Agent
↓
Production Record Agent
↓
HACCP Validation Agent
↓
Missing Field Agent
↓
Document Agent
```

HACCP Validation Agent는

```text
필수 기록 누락
관리 기준 초과
서류 간 불일치
```

를 확인한다.

Missing Field Agent는

> "가열 종료 온도가 입력되지 않았습니다."

처럼 사용자에게 추가 정보를 요청한다.

최종 Document Agent가 생산일지를 생성한다.

이렇게 보면 Agent는 무언가 굉장히 추상적인 기술이 아니라 업무 분장을 AI에게 적용하는 것에 가깝다.

## Context를 역할별로 분리하는 것이 핵심이다

[![Context · Knowledge · Memory 구조](/assets/images/vibe-agent-04-context.png)](/assets/images/vibe-agent-04-context.png)
*Context · Knowledge · Memory 구조 — 클릭하면 원본 크기로 볼 수 있습니다.*

또 하나 중요한 개념이 있다.

모든 파일을 모든 Agent에게 넣으면 다시 처음 문제로 돌아간다.

```text
Huge Context
```

가 되는 것이다.

따라서 각 Agent는 필요한 Context만 읽어야 한다.

예를 들어 Developer Agent에게

```text
과거 영업회의
광고 카피
회사 연혁
```

까지 항상 넣을 이유는 없다.

Task를 기준으로 필요한 정보만 검색한다.

```text
Task
↓
Relevant Context Search
↓
Knowledge Search
↓
Memory Retrieval
↓
Prompt Assembly
↓
Agent Execution
```

내가 생각하는 핵심은 여기다.

> 파일을 저장하는 것이 중요한 게 아니라, 필요한 순간에 필요한 파일만 읽게 하는 것이 중요하다.

이것은 결국 Context Engineering 문제다.

### Knowledge와 Memory도 분리한다

처음에는 이 둘을 같은 폴더에 넣어도 된다.

하지만 규모가 커지면 반드시 구분하는 것이 좋다.

**Knowledge** — 비교적 안정적인 참고자료다.

```text
매뉴얼
제품정보
기술문서
가격표
사내 규정
```

**Memory** — 업무 과정에서 새롭게 생긴 정보다.

```text
지난번 고객이 거절했던 조건

과거 리뷰에서 반복적으로 지적된 내용

프로젝트에서 결정된 사항

Agent가 이전 작업에서 실패했던 이유
```

쉽게 말하면

> Knowledge는 무엇을 알고 있는가
> Memory는 무엇을 경험했는가

다.

## 그래서 Orchestrator가 필요하다

[![Orchestrator · Agent Routing](/assets/images/vibe-agent-02-orchestrator.png)](/assets/images/vibe-agent-02-orchestrator.png)
*Orchestrator · Agent Routing — 클릭하면 원본 크기로 볼 수 있습니다.*

Agent가 여러 개 생기면 새로운 문제가 발생한다.

누가 어떤 일을 해야 하는가?

이를 판단하는 역할이 Orchestrator다.

사용자가

> "신규 서비스 기획하고 MVP까지 만들어줘."

라고 요청하면 Orchestrator가 먼저 작업을 분해한다.

```text
Requirement Analysis
↓
Research
↓
PRD
↓
Architecture
↓
Development
↓
Review
```

그다음 Agent Capability를 기준으로 업무를 배분한다.

```text
Research → Researcher

PRD → Planner

Architecture → Developer

Code → Developer

Review → Reviewer
```

업무가 복잡해지면 Dependency도 관리한다.

```text
          Research
         ↗
Requirement
         ↘
          Data Analysis
              ↓
             PRD
              ↓
         Architecture
              ↓
         Development
              ↓
            Review
```

즉 Orchestrator는 일종의 AI PM이다.

## 모든 일을 자동으로 맡겨서는 안 된다

[![Human Approval · Permission · Observability](/assets/images/vibe-agent-05-governance.png)](/assets/images/vibe-agent-05-governance.png)
*Human Approval · Permission · Observability — 클릭하면 원본 크기로 볼 수 있습니다.*

Agent라는 개념이 나오면 쉽게

> "그럼 AI가 전부 알아서 하게 하면 되겠네."

라는 방향으로 간다.

나는 오히려 반대로 생각한다.

Agent가 많아질수록 Permission과 Human Approval이 더 중요해진다.

예를 들어 다음 작업은 자동 실행시키면 위험하다.

```text
외부 이메일 발송
프로덕션 배포
데이터 삭제
결제
개인정보 처리
```

따라서 구조는 다음처럼 되어야 한다.

```text
AI 판단
↓
Human Approval
↓
실행
```

그리고 Agent마다 권한도 달라야 한다.

```text
Researcher
→ Web 가능
→ DB Write 불가

Developer
→ Code Write 가능
→ Deploy 제한

Reviewer
→ Read 가능
→ Deploy 불가
```

Agent의 자율성을 높이는 것보다 중요한 것은

> Agent가 어디까지 판단할 수 있는지를 명확하게 만드는 것

이라고 생각한다.

## Prompt Engineering을 넘어 Workspace Engineering으로

이 구조를 정리하면서 내가 가장 흥미롭게 느낀 부분은 이것이다.

AI 활용의 중심이 점점 이동하고 있다.

처음에는

```text
Prompt Engineering
```

이었다.

그다음은

```text
Context Engineering
```

이다.

그리고 Agent 시스템에서는

```text
Role
Context
Memory
Tool
State
Workflow
```

까지 설계해야 한다.

나는 이것을 조금 넓게

```text
Workspace Engineering
```

이라고 부르고 싶다.

좋은 Prompt 하나를 작성하는 것이 아니라,
AI가 일하기 좋은 작업환경을 설계하는 것이다.

실제 사람에게도

```text
업무 역할
자료
권한
프로세스
업무 도구
결과물 저장 위치
```

가 필요하다.

AI도 크게 다르지 않다.

## Vibe Agent가 의미하는 것

내가 생각하는 Vibe Agent의 핵심은 Agent Framework 자체를 없애자는 것이 아니다.

LangGraph나 n8n 같은 기술은 여전히 중요하다.

다만 개발을 시작하는 순서를 바꾸는 것이다.

기존 방식이

```text
Agent Framework
↓
Node
↓
Tool
↓
State
↓
Code
```

였다면,

Vibe Agent는 이렇게 시작한다.

```text
이 AI는 무슨 일을 하지?

↓
무슨 자료를 봐야 하지?

↓
어디까지 판단할 수 있지?

↓
무엇을 결과물로 남겨야 하지?

↓
그다음 누구에게 넘겨야 하지?
```

그리고 이를 자연어와 폴더로 정의한다.

그 이후 필요하면

```text
Python
LangGraph
n8n
Database
Vector DB
```

를 붙인다.

기술부터 시작하는 대신 업무 구조부터 시작하는 방식이다.

## 가장 단순한 MVP는 이렇게 만들 수 있다

처음부터 거대한 Multi-Agent Platform을 만들 필요는 없다.

나는 오히려 다음 정도면 충분하다고 본다.

```text
project/

├── context/

├── agents/
│   ├── planner/
│   ├── developer/
│   └── reviewer/
│
├── tasks/
│
├── artifacts/
│
└── shared-memory/
```

그리고 Agent마다

```text
AGENT.md
GOAL.md
RULES.md
HANDOFF.md
```

정도만 만든다.

첫 Workflow도 간단하게 시작한다.

```text
USER
↓
Planner
↓
Developer
↓
Reviewer
↓
Final Output
```

이 구조가 제대로 작동하면 그다음에 Researcher를 추가하고,
Memory를 추가하고,
Tool Permission을 추가하고,
Orchestrator를 강화하면 된다.

## 결국 내가 만들고 싶은 것은 Agent Builder가 아니다

처음에는 "폴더로 Agent를 만들면 재미있겠다" 정도의 아이디어였다.

하지만 구조를 계속 정리하다 보니 조금 다르게 보이기 시작했다.

궁극적으로 만들고 싶은 것은

```text
AI Agent
```

하나가 아니다.

```text
AI Organization
```

에 가깝다.

예를 들어:

```text
company/

├── product/
│   ├── planner/
│   └── researcher/
│
├── development/
│   ├── developer/
│   └── reviewer/
│
└── sales/
    ├── sales-agent/
    └── sales-analyst/
```

폴더 구조 자체가 조직 구조가 된다.

각 Agent는 자신의 Context와 Memory를 가진다.
그리고 Task와 Artifact를 통해 협업한다.

## 정리

처음 가설은 이랬다.

> 폴더에 Prompt와 File을 넣고 크게 만들면 Agent가 되는 것 아닐까?

지금은 이렇게 정리하고 있다.

> 폴더 자체는 Agent가 아니다. 폴더는 Agent Workspace다.

Agent는

```text
Role
+
Goal
+
Knowledge
+
Memory
+
State
+
Tools
+
Execution Loop
```

를 가진다.

그리고 여러 Agent가 협업하려면

```text
Task
Artifact
Handoff
Orchestrator
Human Approval
Observability
```

가 필요하다.

이 구조에서 내가 가장 중요하게 생각하는 문장은 하나다.

> **바이브코딩이 자연어로 소프트웨어를 만드는 것이라면, 바이브에이전트는 자연어와 폴더로 AI 조직을 만드는 것이다.**

아직은 하나의 설계 방법론에 가깝다.

하지만 내가 실제로 했던 기업 RAG, 영업 자동화, HACCP 문서화, 매출 분석 시스템을 이 구조로 다시 바라보니 의외로 많은 업무가 같은 패턴으로 설명됐다.

그래서 다음 단계에서는 실제로 이 Folder-as-Agent Workspace를 코드로 만들고,

```text
Agent 생성
→ Task 할당
→ Context Retrieval
→ Artifact 생성
→ Handoff
→ Review
```

가 실제 파일시스템 위에서 동작하는 MVP를 만들어볼 생각이다.

Prompt를 더 잘 쓰는 방법보다, AI가 더 잘 일할 수 있는 구조를 만드는 것.

아마 앞으로 Agent를 만드는 과정에서 더 중요한 질문은

> "어떤 Prompt를 쓸까?"

보다

> "이 AI에게 어떤 책상과 업무 체계를 만들어줄까?"

가 될지도 모르겠다.

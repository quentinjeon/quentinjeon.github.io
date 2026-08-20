---
layout: single
title: "폴더를 에이전트로 만들 수 있을까? ② — 폴더형 AI 에이전트를 실제 시스템으로"
excerpt: "폴더 자체가 에이전트인 게 아니다. 정의·실행·Tool·Artifact를 분리하고 Policy·Approval·Event Log를 얹으면 추적 가능하고 재실행 가능한 Multi-Agent Workspace가 된다."
series: vibe-agent-workspace
part: 2
categories:
  - ax
  - foundation
tags:
  - Agent
  - Multi-Agent
  - Agent Workspace
  - Tool Permission
  - Orchestrator
  - Audit Trail
toc: true
toc_sticky: true
header:
  teaser: /assets/images/thumbs/vibe-agent-v2.jpg
---

{% include series-nav.html %}

> 1편에서는 **“폴더를 에이전트의 작업공간으로 볼 수 있는가?”**라는 아이디어를 정리했다.  
> 2편에서는 한 단계 더 나아가, 이 개념을 실제로 구현 가능한 시스템 구조로 바꿔본다.
>
> 핵심은 단순하다.
>
> **폴더 자체가 에이전트인 것이 아니라, 폴더에 역할·목표·규칙·도구·지식이 선언되어 있고 실행기가 그 정의를 읽어 하나의 Agent Run을 만든다.**

---

[![Vibe Agent Workspace v2 아키텍처 한눈에 보기](/assets/images/vibe-agent-v2-00-overview.png)](/assets/images/vibe-agent-v2-00-overview.png)
*Vibe Agent Workspace v2 전체 아키텍처 — 설계 원칙 · 디렉터리 구조 · 역할 · Tool 권한 · 실행 격리 — 클릭하면 원본 크기로 볼 수 있습니다.*


## 먼저 결론부터

처음 이 아이디어를 생각했을 때는 구조가 단순했다.

```text
agents/
├── planner/
├── researcher/
├── developer/
└── reviewer/
```

각 폴더 안에 프롬프트와 지식 파일을 넣고 서로 결과물을 주고받으면, 여러 AI 작업자가 협업하는 것처럼 만들 수 있다고 생각했다.

이 방향 자체는 틀리지 않았다.

다만 실제 시스템으로 만들려고 하면 곧바로 몇 가지 문제가 생긴다.

```text
Agent 정의와 실행 중 파일이 섞이면?
동시에 두 Task를 실행하면?
Tool 코드는 Agent마다 복사해야 하나?
Developer가 마음대로 파일을 삭제하면?
Reviewer가 반려했을 때 원본은 어떻게 보존하지?
중간에 프로세스가 죽으면 어디서 다시 시작하지?
```

그래서 구조를 조금 더 엄밀하게 다시 정의했다.

최종적으로는 다음 4가지를 분리하는 것이 핵심이었다.

```text
Agent Definition
실행 중 상태(Runtime)
Tool
Artifact / Handoff
```

그리고 그 위에

```text
Policy
Approval
Event Log
```

을 얹는다.

이렇게 하면 “폴더 기반 에이전트”가 단순한 프롬프트 정리 방식이 아니라 **추적 가능하고 재실행 가능한 Multi-Agent Workspace**가 된다.

---

## 전체 구조

```text
사용자 요청
   ↓
Orchestrator
   ↓
Planner
   ↓
Researcher (필요 시)
   ↓
Developer
   ↓
Reviewer
   ↓
Human Approval (필요 시)
   ↓
Final Output
```

하지만 중요한 것은 Agent의 숫자가 아니다.

내가 이번 구조에서 가장 중요하게 본 것은 아래 세 가지다.

### 1. 정의와 실행을 분리한다

Agent의 역할과 규칙은 장기적으로 유지된다.

반면 특정 요청을 처리하면서 생기는 파일, 로그, 임시 결과물은 매번 달라진다.

둘을 한 폴더에 넣으면 언젠가는 반드시 충돌한다.

### 2. Tool 구현과 Tool 권한을 분리한다

`fs.write`라는 파일 쓰기 Tool이 있다고 해보자.

Tool 코드는 하나만 존재한다.

하지만 Planner와 Developer가 사용할 수 있는 파일 경로는 달라야 한다.

즉,

```text
Tool = 능력
Agent tools.yaml = 그 능력을 사용할 수 있는 범위
```

로 나눈다.

### 3. Agent끼리 대화시키기보다 Artifact를 전달한다

Multi-Agent 시스템을 만들면 흔히 이런 그림을 그린다.

```text
Planner ↔ Developer ↔ Reviewer
```

그런데 실제 운영에서는 자유 대화보다 **파일 계약**이 훨씬 관리하기 쉽다.

그래서 나는 다음 구조를 기본으로 잡았다.

```text
Task
  ↓
Artifact
  ↓
Handoff
  ↓
다음 Task
```

이제 각 하부 시스템을 하나씩 보자.

---

## 01. Agent 폴더는 “정의”, Runtime 폴더는 “실행”

[![01. 폴더 구조 상세 — 정의(불변)와 실행(가변)의 분리](/assets/images/vibe-agent-v2-01-folder-architecture.png)](/assets/images/vibe-agent-v2-01-folder-architecture.png)
*01. 폴더 구조 상세 — 정의(불변)와 실행(가변)의 분리 — 클릭하면 원본 크기로 볼 수 있습니다.*

가장 먼저 수정한 부분이다.

처음에는 Agent 폴더 안에 모든 것을 넣고 싶었다.

```text
agents/
└── planner/
    ├── AGENT.md
    ├── GOAL.md
    ├── RULES.md
    ├── memory/
    ├── inbox/
    ├── workspace/
    ├── outbox/
    └── logs/
```

직관적으로는 좋다.

Planner라는 AI 작업자에게 책상 하나를 통째로 주는 느낌이다.

하지만 문제가 있다.

Planner가 동시에 두 개의 일을 하면 어떻게 될까?

```text
Task A
Task B
```

두 작업이 같은 `workspace/`, `outbox/`, `logs/`를 사용하게 된다.

파일이 섞이고, 로그가 섞이고, 어떤 결과가 어느 요청에서 만들어졌는지 알기 어려워진다.

그래서 **정적 정의와 가변 실행 상태를 완전히 분리**했다.

### Agent 정의 영역

```text
agents/planner/
├── AGENT.md
├── GOAL.md
├── RULES.md
├── HANDOFF.md
├── tools.yaml
├── knowledge/
└── prompts/
```

이 폴더는 Planner가 누구인지 설명한다.

예를 들면 다음과 같다.

```text
AGENT.md
→ 역할과 책임

GOAL.md
→ 무엇을 완료해야 하는가

RULES.md
→ 하지 말아야 할 것과 판단 기준

HANDOFF.md
→ 어떤 입력을 받고 어떤 산출물을 넘길 것인가

tools.yaml
→ 어떤 Tool을 어느 범위에서 사용할 수 있는가
```

이 영역은 쉽게 말하면 **Agent의 직무기술서 + 운영규칙**이다.

### 실행 영역

실제 작업이 시작되면 별도의 run 폴더가 생성된다.

```text
runtime/
└── runs/
    └── run-20260821-001/
        ├── tasks/
        ├── agents/
        │   ├── planner/
        │   │   ├── inbox/
        │   │   ├── workspace/
        │   │   ├── outbox/
        │   │   └── logs/
        │   └── developer/
        ├── artifacts/
        ├── approvals/
        └── events.jsonl
```

이 구조의 장점은 명확하다.

```text
Agent Definition = 재사용
Agent Run        = 매 실행마다 새로 생성
```

그래서 동시에 여러 작업을 실행해도 충돌하지 않는다.

```text
run-001
run-002
run-003
```

각 run은 독립된 실행 세계가 된다.

이게 첫 번째 핵심이다.

> **Agent 폴더는 컨테이너가 아니라 정의 템플릿이다.  
> 실제 작업 공간은 run 단위로 생성한다.**

---

## 02. Tool은 한 번만 만들고, Agent는 권한만 선언한다

[![02. Tool 정의와 권한 구조 — 구현은 중앙에, 권한은 Agent 에](/assets/images/vibe-agent-v2-02-tool-permission.png)](/assets/images/vibe-agent-v2-02-tool-permission.png)
*02. Tool 정의와 권한 구조 — 구현은 중앙에, 권한은 Agent 에 — 클릭하면 원본 크기로 볼 수 있습니다.*

두 번째로 중요하게 본 것은 Tool이다.

AI Agent 시스템을 만들다 보면 기능이 계속 추가된다.

```text
파일 읽기
파일 쓰기
웹 검색
DB 조회
테스트 실행
메일 발송
배포
```

그런데 Agent마다 Tool 코드를 따로 가지고 있게 만들면 문제가 생긴다.

예를 들어 Planner와 Developer가 모두 `fs.read`를 사용한다고 해보자.

Agent별로 Tool을 복사하면 구조가 이렇게 된다.

```text
agents/planner/tools/fs-read/
agents/developer/tools/fs-read/
agents/reviewer/tools/fs-read/
```

처음에는 괜찮아 보인다.

하지만 나중에는 버전이 갈라진다.

```text
Planner fs.read v1.0
Developer fs.read v1.2
Reviewer fs.read v0.9
```

보안 패치도 각각 해야 한다.

그래서 Tool은 중앙에서 한 번만 정의한다.

```text
tools/
├── registry.yaml
├── fs-read/
│   ├── tool.yaml
│   ├── src/
│   └── tests/
├── fs-write/
├── text-search/
└── run-tests/
```

그리고 Agent에는 Tool의 구현이 아니라 **사용 권한**만 둔다.

```text
agents/developer/tools.yaml
```

예를 들어 Developer는 다음과 같이 선언할 수 있다.

```yaml
agent: developer

tools:
  - id: fs.read
    version: "^1.0"
    constraints:
      roots:
        - "${PROJECT_ROOT}"
        - "${RUN_DIR}/agents/developer/inbox"

  - id: fs.write
    version: "^1.0"
    constraints:
      roots:
        - "${RUN_DIR}/agents/developer/workspace"
        - "${RUN_DIR}/agents/developer/outbox"
```

이제 Developer는 `fs.write`를 쓸 수 있지만 아무 파일이나 수정할 수는 없다.

---

### 실제 실행 권한은 “교집합”이다

여기서 중요한 개념이 하나 나온다.

Agent에게 Tool 권한이 있다고 해서 바로 실행되는 것은 아니다.

실제 한 번의 Tool 호출이 실행 가능한 범위는 여러 조건의 **교집합**으로 결정한다.

```text
Tool의 원래 능력
      ∩
전역 정책이 허용한 범위
      ∩
Agent에게 허용된 범위
      ∩
현재 Task가 요구한 범위
      ∩
사용자가 승인한 범위
      ↓
실제 실행 가능 범위
```

예를 들어 `deploy.production`이라는 Tool이 있다고 하자.

Developer가 자신의 `tools.yaml`에 이렇게 적었다고 해서

```yaml
allow:
  - deploy.production
```

자동 배포가 가능해져서는 안 된다.

전역 정책이

```text
production 배포 = 사람 승인 필요
```

라고 정해놨다면 Agent의 선언으로 이를 무시할 수 없다.

즉,

> **Agent는 권한을 더 받을 수는 있어도 전역 정책을 넘어설 수 없다.**

이 구조가 있어야 Agent를 실제 업무 시스템에 연결할 수 있다.

---

## 03. Agent 간 협업의 핵심은 Task · Artifact · Handoff

[![03. Task · Artifact · Handoff 스키마](/assets/images/vibe-agent-v2-03-task-artifact-handoff.png)](/assets/images/vibe-agent-v2-03-task-artifact-handoff.png)
*03. Task · Artifact · Handoff 스키마 — 클릭하면 원본 크기로 볼 수 있습니다.*

이번 시스템에서 가장 중요하게 생각한 부분 중 하나다.

Agent끼리 그냥 대화를 시키는 방식은 구현은 쉽지만 운영하기 어렵다.

왜냐하면 이런 질문에 답하기 힘들기 때문이다.

```text
이 파일은 누가 만들었나?
어떤 요청 때문에 만들어졌나?
어떤 입력을 참고했나?
Reviewer가 무엇을 검토했나?
수정 전 버전은 어디 있나?
```

그래서 Agent 간 협업을 **명시적 계약**으로 바꿨다.

### Task

Task는 “해야 할 일”이다.

```yaml
task_id: task-001
run_id: run-001
owner: planner
status: READY
acceptance_criteria:
  - 요구사항이 정리되어 있다.
  - 구현 범위와 제외 범위가 구분되어 있다.
```

Task에는 단순한 프롬프트가 아니라 완료 조건이 들어간다.

즉,

```text
무엇을 할 것인가
누가 할 것인가
어떤 입력을 사용하는가
언제 완료라고 판단할 것인가
```

를 정의한다.

---

### Artifact

Artifact는 Agent가 만든 결과물이다.

예를 들면:

```text
plan.md
research.md
README-draft.md
test-result.json
report.pdf
```

하지만 파일만 저장하지 않는다.

Artifact 메타데이터를 같이 저장한다.

```yaml
artifact_id: artifact-001
task_id: task-001
run_id: run-001
created_by: planner
type: plan
version: 1
status: submitted
```

중요한 점은 **수정한다고 원본을 덮어쓰지 않는 것**이다.

```text
artifact v1
     ↓
Reviewer REVISION
     ↓
artifact v2
     ↓
Reviewer APPROVED
```

이렇게 버전을 남겨야 어떤 판단 때문에 결과가 바뀌었는지 추적할 수 있다.

---

### Handoff

Handoff는 단순히 파일을 복사하는 것이 아니다.

나는 Handoff를 다음처럼 정의했다.

> **검증된 Artifact를 다음 Task의 입력으로 연결하는 이벤트**

예를 들어

```text
Planner
  ↓
plan.md
  ↓
Handoff
  ↓
Developer
```

이다.

Handoff에서는 최소한 이런 검사를 한다.

```text
스키마가 맞는가?
필수 파일이 존재하는가?
완료 조건을 충족했는가?
Reviewer 확인이 필요한가?
```

검증에 실패하면 다음 Agent로 넘기지 않는다.

이 구조를 사용하면 Agent들이 서로 자유롭게 떠드는 구조보다 훨씬 명확해진다.

```text
Task → Artifact → Handoff → Task
```

이것이 실제 Multi-Agent 시스템의 업무 흐름이 된다.

---

## 04. 실행 흐름은 “Agent 대화”가 아니라 상태 머신으로 관리한다

[![04. 실행 흐름과 상태 머신](/assets/images/vibe-agent-v2-04-execution-flow.png)](/assets/images/vibe-agent-v2-04-execution-flow.png)
*04. 실행 흐름과 상태 머신 — 클릭하면 원본 크기로 볼 수 있습니다.*

이제 시스템이 실제로 움직이는 모습을 보자.

기본 흐름은 다음과 같다.

```text
사용자 요청
   ↓
Orchestrator
   ↓
Planner
   ↓
Researcher
   ↓
Developer
   ↓
Reviewer
   ↓
Human Approval
   ↓
Final Output
```

모든 요청에서 Researcher나 Human Approval이 필요한 것은 아니다.

Orchestrator가 Task를 보고 필요한 역할만 호출한다.

예를 들어 단순 문서 수정이라면

```text
Planner
→ Developer
→ Reviewer
```

만 실행될 수 있다.

외부 조사가 필요하면

```text
Planner
→ Researcher
→ Developer
→ Reviewer
```

가 된다.

---

### Task 상태 머신

Agent 시스템에서 “현재 어디까지 진행되었는가?”를 알 수 있어야 한다.

그래서 Task는 상태를 가진다.

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

그리고 예외 상태를 둔다.

```text
REVISION
BLOCKED
FAILED
```

#### REVISION

Reviewer가 결과를 보고 수정이 필요하다고 판단한다.

```text
REVIEW
  ↓
REVISION
  ↓
RUNNING
```

이때 기존 Artifact를 수정하는 것이 아니라 새로운 버전을 생성한다.

#### BLOCKED

외부 입력이나 승인이 없어서 진행할 수 없는 상태다.

예를 들어:

```text
사용자 확인 필요
API Credential 필요
Human Approval 필요
```

#### FAILED

Tool 실행 오류나 계약 위반 등으로 해당 실행을 계속할 수 없는 상태다.

---

### 모든 행동을 Event로 남긴다

이 시스템의 또 다른 중요한 요소가 `events.jsonl`이다.

```text
runtime/runs/<run-id>/events.jsonl
```

모든 주요 행동을 append-only 로그로 기록한다.

예를 들면:

```text
run.created
task.created
task.assigned
tool.requested
tool.started
tool.completed
artifact.created
artifact.reviewed
handoff.created
approval.requested
approval.granted
run.completed
```

그래서 나중에 `run_id` 하나만 알면 전체 과정을 복원할 수 있다.

```text
누가
언제
무슨 Task에서
어떤 Tool을 사용했고
어떤 Artifact를 만들었으며
누가 승인했는가
```

를 다시 볼 수 있다.

이것은 단순 로그가 아니라 **Agent 시스템의 감사 추적(Audit Trail)**이다.

---

## 05. 그래서 MVP는 무엇부터 만들어야 할까?

[![05. MVP 구현 로드맵과 운영](/assets/images/vibe-agent-v2-05-mvp-roadmap.png)](/assets/images/vibe-agent-v2-05-mvp-roadmap.png)
*05. MVP 구현 로드맵과 운영 — 클릭하면 원본 크기로 볼 수 있습니다.*

여기까지 설계하다 보면 욕심이 생긴다.

```text
Vector DB
Kubernetes
Agent 자동 생성
복잡한 DAG
실시간 UI
멀티 모델 라우팅
```

전부 만들고 싶어진다.

하지만 이번 MVP에서는 과감하게 제외하기로 했다.

MVP가 증명해야 하는 것은 딱 하나다.

> **한 번의 작업 흐름을 처음부터 끝까지 추적하고, 실패하면 복구하고, 다시 실행해도 결과를 재현할 수 있는가?**

그래서 첫 번째 Vertical Slice를 이렇게 잡았다.

```text
프로젝트 폴더를 읽고
README 개선안을 작성한다
```

단순해 보이지만 이 한 작업 안에 거의 모든 핵심 요소가 들어간다.

---

### 0단계 — 계약 고정

먼저 코드보다 계약을 만든다.

```text
Task Schema
Artifact Schema
Handoff Schema
Tool Schema
Approval Schema
State Machine
Event 규칙
```

이 단계에서는 LLM을 붙이지 않아도 된다.

샘플 JSON/YAML만 가지고

```text
정상 데이터는 통과하는가?
잘못된 상태 전이는 막히는가?
필수 metadata 누락을 탐지하는가?
```

를 확인한다.

---

### 1단계 — Single Agent Run

첫 번째 실제 실행은 Planner 하나만 사용한다.

```text
사용자 요청
   ↓
Planner
   ↓
plan.md
```

여기서 확인할 것은 다음이다.

```text
run 디렉터리가 생성되는가?
Planner 정의가 로드되는가?
fs.read / fs.write가 동작하는가?
Artifact가 등록되는가?
events.jsonl에 기록되는가?
```

이것만 성공해도 기반 구조의 절반은 검증된다.

---

### 2단계 — Multi-Agent Handoff

그 다음에 Agent를 연결한다.

```text
Planner
   ↓
Developer
   ↓
Reviewer
```

이 단계에서는 Handoff와 Artifact 버전을 검증한다.

예를 들어 Reviewer가 반려하면

```text
README v1
   ↓
REVISION
   ↓
README v2
```

가 되어야 한다.

원본을 덮어쓰면 안 된다.

---

### 3단계 — 권한과 Human Approval

그다음부터 시스템이 실제 업무 자동화에 가까워진다.

고위험 Tool을 하나 mock으로 만든다.

예를 들어:

```text
deploy.production
email.send
db.delete
```

실제로 배포하거나 메일을 보내지는 않고, 승인 흐름만 구현한다.

```text
Agent 요청
   ↓
Approval Request
   ↓
Human Review
   ↓
Approved / Denied
   ↓
Tool 실행
```

그리고 승인 이후 실행 대상이 바뀌면 기존 승인을 무효화해야 한다.

---

### 4단계 — 복구와 운영 지표

마지막으로 운영 가능성을 검증한다.

프로세스를 일부러 중간에 종료한다.

```text
RUNNING
   ↓
process crash
```

그리고 다시 시작했을 때 마지막 완료 지점에서 복구한다.

이때 자동 재시도는 모든 Tool에 허용하면 안 된다.

예를 들어

```text
텍스트 변환
파일 읽기
```

같은 것은 다시 실행해도 안전하지만,

```text
메일 발송
결제
DB 삭제
```

는 중복 실행되면 문제가 된다.

그래서 Tool마다 idempotency와 retry 정책이 필요하다.

---

## MVP에서 일부러 하지 않는 것

이번 MVP에서는 다음을 미룬다.

```text
Kubernetes 기반 Agent 상시 컨테이너
Vector DB 장기 기억
Agent가 Agent를 무제한 생성
복잡한 DAG 편집기
모델 자동 선택
실시간 다중 사용자 협업 UI
운영 DB 직접 수정
```

이런 기능은 나중에 추가해도 된다.

지금 중요한 것은 화려한 Agent 데모가 아니다.

```text
Task가 추적되는가?
Artifact가 보존되는가?
Handoff가 검증되는가?
권한이 강제되는가?
승인이 남는가?
실패 후 복구되는가?
```

이 여섯 가지가 먼저다.

---

## 이 구조를 만들면서 바뀐 생각

처음에는 이렇게 생각했다.

> 폴더 안에 프롬프트와 파일을 잘 넣으면 그것이 Agent가 될 수 있지 않을까?

지금은 조금 다르게 정의한다.

> **폴더는 Agent 그 자체가 아니라 Agent를 구성하기 위한 선언적 인터페이스다.**

그리고 Agent가 실제로 일하려면 실행기가 필요하다.

```text
Folder
+
Definition
+
Tool Permission
+
Runtime
+
State Machine
+
Artifact Contract
+
Orchestrator
=
실행 가능한 Agent System
```

즉 폴더는 출발점이다.

하지만 폴더라는 익숙한 인터페이스를 잘 설계하면 복잡한 Agent Framework 없이도 상당히 많은 것을 표현할 수 있다.

---

## 왜 굳이 폴더인가?

여전히 폴더 기반 구조가 매력적이라고 생각하는 이유가 있다.

### 1. 사람이 바로 읽을 수 있다

```text
agents/developer/AGENT.md
agents/developer/RULES.md
agents/developer/tools.yaml
```

코드를 열지 않아도 Developer가 무엇을 하는지 알 수 있다.

---

### 2. Git으로 버전 관리하기 쉽다

Agent 설정 자체가 파일이기 때문에

```text
Git commit
Diff
Branch
Review
Rollback
```

을 그대로 사용할 수 있다.

AI Agent를 관리하기 위해 새로운 관리 체계를 전부 만들 필요가 없다.

---

### 3. AI가 직접 수정하기도 쉽다

LLM은 파일 시스템을 다루는 데 익숙하다.

그래서 나중에는 이런 것도 가능하다.

```text
Reviewer:
"Developer의 RULES.md에 테스트 필수 조건을 추가하는 것이 좋겠습니다."

Planner:
"변경 제안 Artifact를 생성합니다."

Human:
"승인"

System:
agents/developer/RULES.md v1.3 생성
```

Agent 시스템 자체가 자신의 운영 규칙을 개선하는 구조로 확장될 수 있다.

물론 이때도 무조건 Human Approval을 거쳐야 한다.

---

## 결국 핵심은 “에이전트를 많이 만드는 것”이 아니다

최근 Agent 관련 데모를 보면 Agent 숫자가 강조되는 경우가 많다.

```text
10 Agents
50 Agents
100 Agents
```

하지만 실제 기업 업무에서는 Agent 숫자보다 중요한 것이 있다.

```text
누가 어떤 권한을 가지고 있는가
무엇을 근거로 판단했는가
결과물이 어디에 남는가
누가 검토했는가
실패하면 어디서 복구하는가
```

결국 Agent System도 업무 시스템이다.

그래서 나는 이 구조를

**“AI들이 자유롭게 대화하는 시스템”**보다는

**“AI 작업자들이 명확한 계약에 따라 협업하는 작업공간”**

으로 만들고 싶다.

---

## 최종 구조를 한 문장으로 정리하면

```text
Agent는 역할을 가진 정의이고,
Tool은 외부 세계에 영향을 주는 능력이며,
Task는 해야 할 일이고,
Artifact는 보존되는 결과이며,
Handoff는 검증된 전달이고,
Runtime은 한 번의 실행 공간이며,
Policy와 Approval은 행동을 제한하고,
Event Log는 모든 과정을 증명한다.
```

이 모든 것을 폴더와 파일 계약으로 연결하는 것이 **Vibe Agent Workspace v2**의 핵심이다.

---

## 다음 편에서 해볼 것

3편에서는 이 구조를 실제 코드로 옮겨볼 생각이다.

첫 번째 목표는 거창한 서비스가 아니다.

```text
사용자:
"이 프로젝트 README를 개선해줘."

        ↓

Orchestrator
        ↓
Planner
        ↓
Developer
        ↓
Reviewer
        ↓
Final Artifact
```

이 한 흐름을 실제로 실행한다.

그리고 실행이 끝났을 때 아래 질문에 모두 답할 수 있게 만드는 것이 목표다.

```text
어떤 Task가 생성됐는가?
어떤 Agent가 실행됐는가?
어떤 Tool을 사용했는가?
어떤 Artifact가 생성됐는가?
Reviewer는 무엇을 검토했는가?
Revision은 몇 번 발생했는가?
모든 이벤트를 run_id 하나로 재구성할 수 있는가?
```

여기까지 된다면 비로소 폴더 기반 Agent 아이디어가 **개념에서 시스템으로 넘어갔다**고 볼 수 있을 것 같다.

---

## 핵심 요약

```text
1편
Folder를 Agent Workspace로 볼 수 있는가?

                ↓

2편
정의 / 실행 / Tool / Artifact를 분리하고
Policy · Approval · Event Log를 추가한다.

                ↓

3편
실제 Orchestrator와 Agent Runner를 구현한다.
```

내가 만들고 싶은 것은 거대한 Agent Framework가 아니다.

**사람이 폴더를 열어보면 이해할 수 있고,  
AI도 같은 구조를 읽고 실행할 수 있는 Agent Workspace.**

그것이 이번 구조의 목표다.
# 폴더 및 Tool 아키텍처

## 1. 전제와 설계 원칙

이 기획에서 "폴더가 에이전트화된다"는 말은 **폴더마다 역할·목표·규칙·지식·허용 능력이 선언되어 있고, 실행기가 그 선언을 읽어 독립 작업자를 구성한다**는 뜻이다.

폴더 자체가 곧 컨테이너라는 뜻은 아니다.

| 개념 | 의미 | 수명 |
|---|---|---|
| Agent definition | 역할과 행동 계약을 담은 템플릿 | 버전과 함께 장기 유지 |
| Agent run | 특정 Task를 수행하는 Agent 인스턴스 | 한 실행 동안 유지 |
| Tool | 외부 세계를 읽거나 바꾸는 명시적 능력 | 독립적으로 버전 관리 |
| Container | Agent run이나 위험한 Tool을 격리하는 실행 수단 | 필요할 때 생성·폐기 |
| Artifact | 다음 Agent나 사람이 소비하는 버전 있는 산출물 | 보존 정책에 따라 유지 |

설계 원칙은 다음과 같다.

1. **정의와 상태를 분리한다.** `agents/`는 거의 불변이고 `runtime/`은 가변이다.
2. **능력과 사용 권한을 분리한다.** `tools/`가 능력을 구현하고 `agents/*/tools.yaml`이 사용 범위를 선언한다.
3. **모든 변경은 Task와 연결한다.** 파일, Tool 호출, 승인, Artifact에 `task_id`와 `run_id`를 남긴다.
4. **공유는 파일 계약으로 한다.** Agent 간 자유 대화보다 검증 가능한 Handoff를 우선한다.
5. **승인은 실행 직전에 확인한다.** 계획 단계 승인만으로 실제 외부 변경을 자동 허용하지 않는다.

## 2. 권장 전체 디렉터리

```text
vibe-agent-workspace/
├── workspace.yaml
│
├── agents/
│   ├── planner/
│   │   ├── AGENT.md
│   │   ├── GOAL.md
│   │   ├── RULES.md
│   │   ├── HANDOFF.md
│   │   ├── tools.yaml
│   │   ├── knowledge/
│   │   └── prompts/
│   ├── researcher/
│   ├── developer/
│   └── reviewer/
│
├── orchestrator/
│   ├── ORCHESTRATOR.md
│   ├── routing.yaml
│   ├── state-machine.yaml
│   └── prompts/
│
├── tools/
│   ├── registry.yaml
│   ├── fs-read/
│   │   ├── tool.yaml
│   │   ├── src/
│   │   └── tests/
│   ├── fs-write/
│   │   ├── tool.yaml
│   │   ├── src/
│   │   └── tests/
│   ├── web-search/
│   │   ├── tool.yaml
│   │   ├── src/
│   │   └── tests/
│   └── run-tests/
│       ├── tool.yaml
│       ├── src/
│       ├── tests/
│       └── Dockerfile          # 격리가 필요할 때만
│
├── policies/
│   ├── tool-access.yaml
│   ├── approvals.yaml
│   ├── data-classification.yaml
│   └── retention.yaml
│
├── schemas/
│   ├── task.schema.json
│   ├── artifact.schema.json
│   ├── handoff.schema.json
│   ├── tool.schema.json
│   ├── approval.schema.json
│   └── tools/
│       ├── fs-write.input.schema.json
│       └── fs-write.output.schema.json
│
├── shared/
│   ├── context/
│   │   ├── business.md
│   │   ├── product.md
│   │   └── constraints.md
│   ├── knowledge/
│   └── memory/
│       ├── decisions.md
│       └── lessons.md
│
└── runtime/
    ├── queue/
    └── runs/
        └── run-20260821-001/
            ├── run.yaml
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

### 기존 이미지와 달라지는 부분

2026-08-20 이미지에서는 `agents/planner/` 아래에 `memory`, `inbox`, `workspace`, `outbox`, `logs`가 함께 있다. 개념 설명으로는 직관적이지만 실제 운영에서는 다음 문제가 생긴다.

- 동일 Planner가 Task A와 Task B를 동시에 수행하면 파일명이 충돌한다.
- 어떤 로그가 어느 실행에 속하는지 경로만으로 알기 어렵다.
- Agent 정의를 배포할 때 실행 중 생성된 데이터까지 함께 복사될 수 있다.
- 실패한 run을 재현하거나 정리하기 어렵다.

따라서 v2에서는 Agent의 고정 정의만 `agents/`에 두고, 실행 중 생기는 폴더는 `runtime/runs/<run-id>/agents/<agent-id>/` 아래에 생성한다.

## 3. Tool은 정확히 어디에 정의하는가

### 3.1 최종 권장안

Tool 하나는 다음 네 위치에 나뉘어 표현된다.

```text
tools/<tool-id>/tool.yaml          # Tool 자체의 계약
tools/<tool-id>/src/               # 실제 구현
tools/<tool-id>/tests/             # 계약·권한·회귀 테스트
agents/<agent-id>/tools.yaml       # 이 Agent가 Tool을 쓰는 방식
```

그리고 두 개의 중앙 파일이 통제한다.

```text
tools/registry.yaml                # 사용 가능한 Tool과 버전 목록
policies/tool-access.yaml          # 조직 전체의 허용/금지 상한선
```

권한 판정은 아래 순서로 교집합을 취한다.

```text
Tool의 원래 능력
  ∩ 전역 정책이 허용한 범위
  ∩ Agent에 부여된 범위
  ∩ 현재 Task가 요구한 범위
  ∩ 사용자가 승인한 범위
= 실제 한 번의 Tool 호출이 실행할 수 있는 범위
```

Agent의 선언으로 전역 정책을 넓힐 수는 없다. 예를 들어 전역 정책이 `deploy.production`을 사람 승인 대상으로 정했다면 Developer의 `tools.yaml`이 이를 자동 실행으로 바꿀 수 없다.

### 3.2 `TOOLS.md`는 어떻게 다룰까

기존 이미지의 `TOOLS.md`는 사람에게 설명하기 좋지만 기계가 안정적으로 검증하기 어렵다. 다음처럼 역할을 나누는 것이 좋다.

- `tools.yaml`: 실행기가 읽는 유일한 권한 원본
- `TOOLS.md`: 왜 이 Tool이 필요한지, 실패 시 어떻게 행동할지 설명하는 선택 문서

동일한 Tool 목록을 두 파일에 반복해 적지 않는다. 필요하면 `tools.yaml`에서 `TOOLS.md`의 표를 자동 생성한다.

### 3.3 Agent 전용 Tool의 예외

정말 한 Agent에서만 쓰는 작은 로직도 처음에는 `tools/<tool-id>/`에 둔다. "현재 한 곳에서만 사용"과 "Agent 정체성에 종속"은 다르기 때문이다.

다음 조건을 모두 만족할 때만 `agents/<agent-id>/private-tools/`를 예외로 허용한다.

- 다른 Agent에서 재사용할 가능성이 낮다.
- 해당 Agent의 프롬프트·지식과 분리하면 의미가 없다.
- 파일·네트워크·DB·외부 서비스에 부작용을 만들지 않는 순수 변환이다.

MVP에서는 이 예외를 만들지 않는 편이 단순하다.

## 4. Tool 계약 예시

### 4.1 Tool 자체의 매니페스트

```yaml
# tools/fs-write/tool.yaml
id: fs.write
version: 1.0.0
description: 허용된 작업공간 안에서 파일을 생성하거나 수정한다.

executor:
  type: sandboxed-process
  entrypoint: src/main
  timeout_seconds: 30

input_schema: ../../schemas/tools/fs-write.input.schema.json
output_schema: ../../schemas/tools/fs-write.output.schema.json

effects:
  - filesystem_write
risk: medium
approval: policy

audit:
  log_arguments: true
  redact_fields: []
  record_file_hash_before_after: true
```

여기에는 누가 사용하는지가 아니라 이 Tool이 **본질적으로 무엇을 할 수 있고 어떤 부작용이 있는지**를 기록한다.

### 4.2 Agent별 Tool binding

```yaml
# agents/developer/tools.yaml
agent: developer
tools:
  - id: fs.read
    version: "^1.0"
    constraints:
      roots:
        - "${RUN_DIR}/agents/developer/inbox"
        - "${RUN_DIR}/agents/developer/workspace"
        - "${PROJECT_ROOT}"

  - id: fs.write
    version: "^1.0"
    constraints:
      roots:
        - "${RUN_DIR}/agents/developer/workspace"
        - "${RUN_DIR}/agents/developer/outbox"
      deny_patterns:
        - "**/.env"
        - "**/credentials/**"

  - id: tests.run
    version: "^1.0"
    constraints:
      network: false
      max_seconds: 300
```

`${RUN_DIR}`와 `${PROJECT_ROOT}`는 실행기가 검증된 절대 경로로 치환한다. Tool 구현이 Agent가 전달한 임의 경로를 그대로 신뢰하면 안 된다.

### 4.3 Registry

```yaml
# tools/registry.yaml
tools:
  - id: fs.read
    version: 1.0.0
    path: ./fs-read
    enabled: true

  - id: fs.write
    version: 1.0.0
    path: ./fs-write
    enabled: true

  - id: tests.run
    version: 1.0.0
    path: ./run-tests
    enabled: true
```

Agent는 구현 경로를 직접 참조하지 않고 `id + version`으로만 요청한다. Registry가 실제 실행기를 해석한다.

## 5. Tool을 전부 컨테이너로 만들어야 하는가

아니다. 컨테이너 여부는 폴더 구조가 아니라 위험도와 의존성으로 결정한다.

| 실행 방식 | 적합한 Tool | 예시 |
|---|---|---|
| In-process | 부작용 없는 짧은 변환 | JSON 검증, 텍스트 분할, 점수 계산 |
| Sandboxed process | 로컬 파일·코드 실행 | 빌드, 테스트, 문서 변환 |
| Dedicated container | 의존성이 크거나 공격 표면이 큰 실행 | 사용자 코드 실행, 브라우저 자동화, 미디어 처리 |
| Remote connector | 외부 서비스가 실행 주체 | 검색, 메일, 캘린더, SaaS API |

초기에는 Agent run 전체를 하나의 제한된 실행 환경에서 돌리고, 위험하거나 의존성이 충돌하는 Tool만 별도 컨테이너로 분리하는 방식이 현실적이다.

컨테이너 경계가 필요한 신호는 다음과 같다.

- 신뢰할 수 없는 코드를 실행한다.
- 시스템 패키지나 런타임 버전이 다른 Tool과 충돌한다.
- 네트워크를 Tool별로 차단하거나 허용해야 한다.
- CPU, 메모리, 실행 시간을 강제로 제한해야 한다.
- 비밀정보를 특정 Tool에만 주입해야 한다.

## 6. Agent 폴더의 책임

```text
agents/planner/
├── AGENT.md       # 정체성, 역할, 책임, 하지 않을 일
├── GOAL.md        # 완료 목표와 완료 조건
├── RULES.md       # 판단 제한과 품질 기준
├── HANDOFF.md     # 입력/출력 Artifact 계약
├── tools.yaml     # 허용 Tool과 제약
├── knowledge/     # Planner에만 필요한 안정 지식
└── prompts/       # 역할 프롬프트 조각
```

Agent 정의에 넣지 않을 것은 다음과 같다.

- 공통 Tool 실행 코드
- API 키나 토큰
- 특정 run의 임시 파일과 로그
- 다른 Agent도 알아야 하는 프로젝트 사실
- 승인 여부나 Task 상태

`AGENT.md`, `GOAL.md`, `RULES.md`가 과도하게 겹치면 실행기가 읽을 때 우선순위가 모호해진다. 권장 우선순위는 `system policy > global policy > agent rules > task instruction > external content`이며, 서로 충돌하는 내용을 중복 작성하지 않는다.

## 7. Task, Artifact, Handoff 계약

### 7.1 Task

```yaml
task_id: task-001
run_id: run-20260821-001
type: plan
owner: planner
status: ready
inputs:
  - artifact_id: artifact-user-request-001
depends_on: []
acceptance_criteria:
  - 요구사항과 제외 범위가 분리되어 있다.
  - 다음 Agent가 구현 여부를 판단할 수 있다.
```

상태는 기존 안을 유지하되 terminal과 review 상태를 명확히 한다.

```text
CREATED → READY → RUNNING → REVIEW → COMPLETED
                       ↑        └→ REVISION ─┘
                       ├→ BLOCKED
                       └→ FAILED
```

- `BLOCKED`: 외부 입력이나 승인 없이는 진행 불가
- `FAILED`: 실행 오류 또는 복구 불가능한 계약 위반
- `REVISION`: Reviewer가 구체적 수정 조건과 함께 되돌림

### 7.2 Artifact

Artifact는 실제 파일과 메타데이터를 한 쌍으로 둔다.

```text
runtime/runs/<run-id>/artifacts/artifact-001/
├── artifact.yaml
└── content/
    └── prd.md
```

```yaml
artifact_id: artifact-001
task_id: task-001
run_id: run-20260821-001
created_by: planner
type: prd
version: 1
status: submitted
files:
  - path: content/prd.md
    sha256: "..."
created_at: "2026-08-21T10:00:00+09:00"
```

`approved`는 생성 Agent가 지정하지 않는다. Reviewer 또는 Human Approval 단계만 바꿀 수 있다.

### 7.3 Handoff

Handoff는 파일을 복사하는 행위가 아니라 **입력 계약을 충족한 Artifact의 소유권을 다음 Task에 연결하는 이벤트**다.

```yaml
handoff_id: handoff-001
from_task: task-001
to_task: task-002
artifacts:
  - artifact-001
checks:
  schema_valid: true
  acceptance_criteria_met: true
  reviewer_required: false
```

다음 Agent의 `inbox/`에는 원본 복사본보다 읽기 전용 참조나 검증된 staging copy를 제공한다. 원본 Artifact를 직접 수정하지 않는다.

## 8. Context, Knowledge, Memory 분리

| 계층 | 질문 | 예시 | 갱신 방식 |
|---|---|---|---|
| Context | 지금 프로젝트에서 사실인가? | 고객, 목표, 제약, 현재 구조 | 프로젝트 책임자가 갱신 |
| Knowledge | 반복해서 참고할 검증된 정보인가? | 매뉴얼, 규정, API 명세 | 검토 후 버전 관리 |
| Memory | 실행 경험에서 배운 것은 무엇인가? | 결정, 실패 원인, 교훈 | run 종료 후 승격 심사 |
| Run state | 지금 실행이 어디까지 왔는가? | Task 상태, 임시 파일, 로그 | 실행 중 자동 갱신 |

Agent의 로컬 Memory를 프롬프트에 무제한 누적하지 않는다. 각 run 종료 후 후보를 만들고, 중복·민감정보·잘못된 추론을 검토한 뒤 `shared/memory/` 또는 Agent memory로 승격한다.

## 9. Permission과 Human Approval

### 9.1 효과 기반 권한

Tool 이름만 보지 말고 실제 효과를 기준으로 분류한다.

| 효과 | 기본 위험도 | 기본 정책 |
|---|---:|---|
| 로컬 읽기 | 낮음 | 허용 경로 내 자동 |
| run 작업공간 쓰기 | 중간 | 허용 경로 내 자동 + diff 기록 |
| 프로젝트 원본 수정 | 중간~높음 | Task 범위 내 허용, 변경 기록 |
| 네트워크 읽기 | 중간 | 출처 기록, 민감정보 전송 금지 |
| 외부 메시지·메일 발송 | 높음 | 사람 승인 |
| DB 쓰기·삭제 | 높음 | 사람 승인 + 대상 미리보기 |
| 배포·결제·권한 변경 | 매우 높음 | 사람 승인 + 재인증 |

### 9.2 승인 레코드

```yaml
approval_id: approval-001
run_id: run-20260821-001
task_id: task-007
requested_by: developer
action: deploy.production
summary: v1.3.0을 production에 배포
scope_hash: "..."
status: pending
expires_at: "2026-08-21T18:00:00+09:00"
```

승인은 `scope_hash`와 결합한다. 승인 후 대상, 인자, Artifact가 바뀌면 기존 승인은 무효다.

## 10. Observability 최소 기준

모든 이벤트는 `runtime/runs/<run-id>/events.jsonl`에 append-only로 기록한다.

필수 이벤트는 다음과 같다.

- `run.created`, `run.completed`, `run.failed`
- `task.created`, `task.assigned`, `task.state_changed`
- `tool.requested`, `tool.started`, `tool.completed`, `tool.denied`
- `artifact.created`, `artifact.reviewed`, `artifact.published`
- `handoff.created`, `handoff.accepted`, `handoff.rejected`
- `approval.requested`, `approval.granted`, `approval.denied`, `approval.expired`

로그에는 최소한 `time`, `run_id`, `task_id`, `agent_id`, `event`, `tool_id`, `duration_ms`, `result`, `error_code`를 둔다. 프롬프트 전문, 비밀정보, 개인정보는 기본 로그 대상에서 제외한다.

## 11. 최종 결정 요약

| 질문 | 결정 |
|---|---|
| Agent 폴더가 컨테이너인가? | 정의 템플릿이다. 실제 컨테이너는 run 또는 고위험 Tool의 실행 경계다. |
| Tool 구현은 어디에 두는가? | `tools/<tool-id>/` |
| Agent 폴더에는 무엇을 두는가? | `tools.yaml` 허용 목록과 제약만 둔다. |
| Agent별 `inbox/outbox/logs`는 어디에 두는가? | `runtime/runs/<run-id>/agents/<agent-id>/` |
| Tool별 Dockerfile이 필요한가? | 격리가 필요한 Tool에만 둔다. |
| 공통 정책은 어디에서 강제하는가? | `policies/`와 Orchestrator의 실행 게이트에서 강제한다. |
| Agent 간 전달 단위는 무엇인가? | 검증된 Artifact와 Handoff 이벤트다. |

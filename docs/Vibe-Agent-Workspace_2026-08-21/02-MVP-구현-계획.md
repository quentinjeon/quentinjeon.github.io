# MVP 구현 계획

## 1. MVP가 증명해야 할 것

MVP의 목적은 많은 Agent나 Tool을 만드는 것이 아니다. 다음 한 흐름이 추적 가능하고 재실행 가능하다는 것을 증명하는 것이다.

```text
사용자 요청
  → Orchestrator가 Task 생성
  → Planner가 계획 Artifact 작성
  → Developer가 작업 Artifact 작성
  → Reviewer가 승인 또는 수정 요청
  → 필요한 경우 Human Approval
  → Final Output 발행
```

성공 기준은 다음과 같다.

1. 한 Task의 모든 Tool 호출과 Artifact를 `run_id`로 찾을 수 있다.
2. Agent마다 허용하지 않은 Tool 호출은 실행 전에 차단된다.
3. 두 run을 동시에 실행해도 파일과 로그가 섞이지 않는다.
4. Reviewer가 `REVISION`을 주면 기존 Artifact를 덮어쓰지 않고 새 버전이 생긴다.
5. 외부 발송이나 배포를 흉내 낸 고위험 Tool은 승인 전 실행되지 않는다.
6. 실행 중 중단 후 Task 상태를 읽어 이어서 진행할 수 있다.

## 2. 초기 범위를 작게 잡는다

### Agent

| Agent | MVP 책임 | 제외 |
|---|---|---|
| Planner | 요청을 Task와 완료 조건으로 변환 | 장기 일정 최적화 |
| Developer | 승인된 작업 계획에 따라 파일 산출물 생성 | 실서비스 자동 배포 |
| Reviewer | 완료 조건과 변경 내용을 검토 | 무제한 자동 수정 |
| Researcher | 외부 조사가 필요한 Task에서만 선택 실행 | 상시 크롤링 |

### Tool

MVP Tool은 아래 6개면 충분하다.

| Tool ID | 역할 | 위험도 |
|---|---|---:|
| `fs.read` | 허용된 파일 읽기 | 낮음 |
| `fs.write` | run 작업공간의 파일 쓰기 | 중간 |
| `text.search` | 프로젝트 내부 검색 | 낮음 |
| `tests.run` | 제한된 명령으로 검증 실행 | 중간 |
| `artifact.submit` | 파일을 Artifact로 등록 | 중간 |
| `approval.request` | 고위험 작업 승인 요청 | 낮음 |

`web.search`, 실제 메일 발송, 실제 배포, DB 변경은 계약이 안정된 뒤 추가한다. Researcher는 MVP 초기에는 로컬 자료 조사만 수행해도 된다.

## 3. 단계별 구현

### 0단계 — 계약 고정

만들 것:

- `workspace.yaml`
- Task, Artifact, Handoff, Tool, Approval 스키마
- 상태 머신과 이벤트 이름
- Tool ID 명명 규칙

검증:

- 정상 예시와 오류 예시가 모두 스키마 검사를 통과/실패한다.
- `COMPLETED` 이후 `RUNNING`으로 되돌리는 잘못된 상태 전이를 거부한다.
- Artifact의 `task_id`, `run_id`, `created_by` 누락을 거부한다.

완료 조건:

- 실행 코드 없이도 한 run의 파일 구조를 샘플 데이터로 설명할 수 있다.

### 1단계 — 단일 Agent run

만들 것:

- run 디렉터리 생성기
- Planner 정의 로더
- `fs.read`, `fs.write`, `artifact.submit`
- append-only event logger

검증:

- Planner가 사용자 요청을 읽고 `plan.md`를 Artifact로 제출한다.
- Agent가 허용 경로 밖에 쓰려고 하면 거부되고 `tool.denied`가 기록된다.
- 동일 입력으로 두 run을 만들면 서로 다른 디렉터리와 이벤트 로그를 갖는다.

완료 조건:

- `run_id` 하나만으로 입력, 출력, Tool 호출, 상태 변화를 재구성할 수 있다.

### 2단계 — Multi-Agent Handoff

만들 것:

- Orchestrator의 Task 분해와 담당 Agent 지정
- Planner → Developer → Reviewer Handoff
- Artifact 버전과 read-only input staging
- `REVISION` 루프

검증:

- Developer가 Planner의 Artifact를 입력으로 받는다.
- Developer는 Planner의 원본 Artifact를 수정할 수 없다.
- Reviewer가 반려하면 이유와 완료 조건이 새 Task 또는 revision record로 남는다.
- 수정본은 `version: 2`가 되고 `version: 1`은 보존된다.

완료 조건:

- Agent 간 대화 기록 없이 Artifact와 Handoff만으로 전체 흐름을 설명할 수 있다.

### 3단계 — 권한과 사람 승인

만들 것:

- 전역 `tool-access` 정책
- Agent별 Tool binding 검사
- 승인 요청·허용·거부·만료 상태
- 실제 부작용 대신 안전한 mock high-risk Tool

검증:

- Agent binding이 허용해도 전역 정책이 금지하면 실행되지 않는다.
- 승인 전에는 고위험 Tool이 실행되지 않는다.
- 승인 후 실행 인자가 바뀌면 `scope_hash` 불일치로 다시 승인을 요구한다.
- 승인·거부·만료가 모두 이벤트 로그에 남는다.

완료 조건:

- "누가, 무엇을, 어떤 범위로 승인했고 실제 무엇이 실행됐는가"를 한 화면 또는 한 보고서로 확인할 수 있다.

### 4단계 — 복구와 운영 지표

만들 것:

- 중단된 run 복구
- 실패 재시도 정책
- run 요약 보고서
- 최소 운영 지표

검증:

- `RUNNING` 중 프로세스를 종료한 뒤 마지막 완료 이벤트에서 재개한다.
- 부작용 없는 Tool만 자동 재시도한다.
- 같은 Tool call을 중복 실행하지 않도록 idempotency key를 사용한다.

완료 조건:

- 성공률, 평균 실행 시간, revision 비율, handoff 실패율, 사람 개입률을 계산할 수 있다.

## 4. 테스트 시나리오

첫 vertical slice는 "프로젝트 폴더를 읽고 README 개선안을 작성한다"로 잡는다. 외부 서비스 없이도 모든 핵심 계약을 시험할 수 있기 때문이다.

### 정상 흐름

1. 사용자가 대상 폴더와 개선 목표를 입력한다.
2. Planner가 파일 목록과 제약을 확인하고 계획 Artifact를 만든다.
3. Developer가 허용된 작업공간에서 README 수정본을 만든다.
4. Reviewer가 완료 조건과 diff를 검사한다.
5. 승인되면 Final Output으로 발행한다.

### 실패·경계 흐름

- Developer가 허용 범위 밖 파일을 수정한다 → Tool 거부
- Reviewer가 근거 누락을 발견한다 → `REVISION`
- Artifact 메타데이터와 실제 파일 해시가 다르다 → Handoff 거부
- 동일 run을 두 번 재개한다 → 중복 실행 방지
- high-risk mock Tool을 호출한다 → Human Approval 대기

## 5. 구현 순서에서 미룰 것

다음 항목은 매력적이지만 MVP의 핵심 증명과 무관하므로 뒤로 미룬다.

- Kubernetes와 Agent별 상시 컨테이너
- Vector DB 기반 장기 기억
- Agent가 Agent를 동적으로 무제한 생성하는 기능
- 복잡한 DAG 시각화 편집기
- 모델 자동 선택과 비용 최적화
- 실시간 협업 UI
- 운영 DB를 직접 수정하는 Tool

먼저 파일 기반 계약과 권한 게이트가 맞는지 확인해야 이후 인프라 선택이 쉬워진다.

## 6. Tool 추가 체크리스트

새 Tool은 아래 질문에 답하지 못하면 Registry에 등록하지 않는다.

- Tool ID와 버전은 무엇인가?
- 입력과 출력 스키마가 있는가?
- 파일, 네트워크, DB, 외부 사람에게 어떤 효과를 만드는가?
- 접근 가능한 경로·도메인·레코드 범위는 무엇인가?
- 재시도해도 안전한가?
- 타임아웃과 자원 제한은 무엇인가?
- 어떤 정보가 로그에 남고 무엇을 가려야 하는가?
- 사람 승인이 필요한 조건은 무엇인가?
- 최소 1개의 성공, 거부, 실패 테스트가 있는가?

## 7. v1 이미지에서 v2로 옮기는 순서

| 기존 개념 | v2 위치 | 전환 방식 |
|---|---|---|
| `agents/*/AGENT.md` | 동일 | 유지 |
| `GOAL.md`, `RULES.md`, `HANDOFF.md` | 동일 | 중복 규칙만 정리 |
| `TOOLS.md` | `tools.yaml` + 선택적 설명 문서 | 실행 권한을 구조화 |
| Agent의 `knowledge/` | Agent 전용 지식만 유지 | 공통 지식은 `shared/knowledge/`로 이동 |
| Agent의 `memory/` | 검토된 Agent memory만 유지 | run 중 memory는 `runtime/`에 저장 |
| Agent의 `inbox/workspace/outbox/logs` | `runtime/runs/<run-id>/agents/*/` | run 생성 시 자동 생성 |
| Shared Workspace의 Tasks/Artifacts/Logs | `runtime/runs/<run-id>/` | run 단위 격리 |
| Shared Context/Memory | `shared/` | 장기 자산만 유지 |
| Permission 표 | `policies/tool-access.yaml` | 실행 게이트로 강제 |
| Human Approval | `runtime/.../approvals/` | 영속 승인 레코드화 |

## 8. 다음 설계 결정

MVP 계약을 고정한 뒤에만 아래를 선택한다.

1. Orchestrator 구현 언어와 실행 방식
2. 상태 저장을 파일만으로 할지 SQLite를 함께 쓸지
3. LLM provider adapter 인터페이스
4. 로컬 Tool sandbox 기술
5. UI가 읽을 event/query API

초기 기본안은 **파일을 source of truth로 두고, 조회 성능이 필요할 때 SQLite 인덱스를 재생성 가능하게 추가하는 것**이다. 이 방식은 2026-08-20안의 파일 기반 철학을 유지하면서도 운영 화면을 확장할 수 있다.


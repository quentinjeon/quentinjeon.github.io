# Vibe Agent Workspace v2 기획

> 작성일: 2026-08-21  
> 상태: 구조 설계안 — 구현 전 검토용  
> 이전 자료: [`../Vibe-Agent-Workspace_2026-08-20/`](../Vibe-Agent-Workspace_2026-08-20/)

## 1. 이번 기획의 결론

폴더를 AI 작업자의 작업공간으로 보는 방향은 유지한다. 다만 **Agent의 정의**, **실행 중 상태**, **Tool의 구현**은 서로 다른 수명주기와 보안 경계를 가지므로 폴더도 분리한다.

가장 중요한 결정은 다음 한 문장이다.

> **Tool 코드는 루트 `tools/`에 한 번만 정의하고, 각 Agent 폴더에는 사용할 Tool의 ID·권한·제약만 선언한다.**

권장 위치는 다음과 같다.

| 구분 | 권장 위치 | 담는 내용 |
|---|---|---|
| Agent 정의 | `agents/<agent-id>/` | 역할, 목표, 규칙, handoff 계약, Tool 허용 목록 |
| Tool 구현 | `tools/<tool-id>/` | 실행 코드, 입출력 스키마, 위험도, 테스트, 필요 시 컨테이너 정의 |
| Tool 목록 | `tools/registry.yaml` | Tool ID와 버전, 구현 위치, 활성 상태 |
| Agent별 Tool 연결 | `agents/<agent-id>/tools.yaml` | 허용 Tool, 인자 제한, 접근 경로, 승인 조건 |
| 공통 권한 정책 | `policies/` | 삭제·외부 발송·배포 등 전 Agent 공통 제한 |
| 실행 인스턴스 | `runtime/runs/<run-id>/` | task, inbox, 작업 파일, 산출물, 로그, 승인 기록 |

`agents/planner/TOOLS.md` 안에 실행 코드를 넣거나 Agent별로 같은 Tool을 복사하는 방식은 권장하지 않는다. 그렇게 하면 Tool 버전, 보안 패치, 감사 로그가 Agent마다 갈라진다.

## 2. 현재 폴더 확인 결과

현재 `portfolio/`는 실행 코드 저장소가 아니라 포트폴리오 자료 저장소에 가깝다.

- `docs/`: 전략 문서, Vibe Agent Workspace 이미지 6장, 건설사 AX 글과 이미지
- `resume/`: 이력서 입력 자료와 향후 산출물 위치
- `포트폴리오-컨텐츠-정의.md`: 포트폴리오 사이트 콘텐츠 설계

아직 `agents/`, `tools/`, `orchestrator/`, `runtime/` 구현은 없다. 따라서 아래 구조는 현재 폴더를 억지로 Agent화한 결과가 아니라, **향후 별도 시스템으로 구현할 목표 구조**다. 이번 `2026-08-21` 폴더에는 설계와 MVP 계획만 둔다.

## 3. 2026-08-20안에서 유지할 것과 보완할 것

### 유지할 핵심

- `Folder = Agent Workspace`라는 이해하기 쉬운 운영 모델
- Planner, Researcher, Developer, Reviewer의 역할 분리
- 대화보다 Task·Artifact·Handoff 중심의 협업
- `CREATED → READY → RUNNING → REVIEW → COMPLETED` 상태 관리
- Knowledge와 Memory의 분리
- 최소 권한, Human Approval, 실행 로그

### v2에서 보완할 핵심

- Agent 폴더 안의 `inbox/workspace/outbox/logs`는 단일 작업에는 쉽지만 동시 실행 시 충돌한다. 가변 상태는 `runtime/runs/<run-id>/`로 이동한다.
- `TOOLS.md`만으로는 프로그램이 권한을 강제하기 어렵다. 실행 가능한 `tools.yaml`과 중앙 정책을 둔다.
- 모든 폴더를 곧바로 물리 컨테이너로 만들지 않는다. **Agent 폴더는 정의 템플릿**, `run`은 실행 인스턴스, 컨테이너는 위험한 실행을 격리하는 수단으로 구분한다.
- Artifact에는 파일만 두지 않고 `artifact_id`, 생성 Agent, 입력 Task, 버전, 검토 상태, 해시를 함께 기록한다.
- Human Approval은 화면상의 버튼이 아니라 재시작 후에도 복구 가능한 승인 레코드로 저장한다.

## 4. 목표 구조 한눈에 보기

```text
vibe-agent-workspace/
├── agents/                     # 누구인가, 무엇을 할 수 있는가
│   ├── planner/
│   ├── researcher/
│   ├── developer/
│   └── reviewer/
├── orchestrator/               # 요청 분해, 라우팅, 상태 전이
├── tools/                      # Tool의 실제 정의와 구현
│   ├── registry.yaml
│   ├── fs-read/
│   ├── fs-write/
│   ├── web-search/
│   └── run-tests/
├── policies/                   # 전역 권한·승인·보안 정책
├── schemas/                    # Task, Artifact, Handoff 공통 스키마
├── shared/
│   ├── context/                # 프로젝트 사실과 제약
│   ├── knowledge/              # 검증된 재사용 지식
│   └── memory/                 # 팀 의사결정과 교훈
└── runtime/
    └── runs/<run-id>/          # 한 번의 실행에서만 생기는 가변 상태
```

상세한 폴더 책임, Tool 선언 예시, 컨테이너 경계는 [`01-폴더-및-Tool-아키텍처.md`](01-폴더-및-Tool-아키텍처.md)에 정리했다. 실제 구현 순서와 완료 기준은 [`02-MVP-구현-계획.md`](02-MVP-구현-계획.md)에 있다.

## 5. 이번 기획의 범위

이 문서는 특정 프레임워크나 LLM 벤더를 고르는 문서가 아니다. 먼저 바뀌기 어려운 파일 계약과 운영 원칙을 정한다.

- 포함: 폴더 책임, Agent/Tool 경계, Task·Artifact·Handoff 구조, 권한과 승인, 로그, MVP 순서
- 제외: UI 상세 디자인, 모델 선정, 벡터 DB 선정, Kubernetes 도입, 대규모 조직용 멀티테넌시

## 6. 설계 판단을 검증하는 질문

아래 질문에 모두 답할 수 있으면 구조가 제대로 작동하는 것이다.

1. 특정 Agent가 어떤 Tool을 어떤 제한으로 쓸 수 있는가?
2. 같은 Tool을 여러 Agent가 써도 구현과 버전은 하나로 관리되는가?
3. 두 Task가 같은 Agent를 동시에 실행해도 작업 파일과 로그가 섞이지 않는가?
4. 산출물이 어느 Task와 입력에서 만들어졌는지 추적 가능한가?
5. 삭제·배포·외부 전송은 실행 전에 승인이 필요한가?
6. 중간에 프로세스가 종료되어도 Task와 승인 상태를 복원할 수 있는가?

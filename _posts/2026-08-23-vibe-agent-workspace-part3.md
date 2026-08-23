---
layout: single
title: "폴더를 에이전트로 만들 수 있을까? ③ — Orchestrator와 Agent Runner를 실제 코드로"
excerpt: "설계를 312줄로 옮기고 실제로 돌렸다. 상태 전이표, 권한 교집합, 리비전 루프, 그리고 run_id 하나로 실행 전체를 복원하는 이벤트 로그. 이 글의 로그는 전부 실행 결과 그대로다."
series: vibe-agent-workspace
part: 3
categories:
  - ax
  - foundation
tags:
  - Agent
  - Multi-Agent
  - Agent Workspace
  - Orchestrator
  - Agent Runner
  - Tool Permission
  - State Machine
  - Event Log
  - Audit Trail
toc: true
toc_sticky: true
header:
  teaser: /assets/images/thumbs/vibe-agent-v3.jpg
---

{% include series-nav.html %}

2편 마지막에 이렇게 적었다.

> 3편에서는 이 구조를 실제 코드로 옮겨볼 생각이다. (…) 실행이 끝났을 때 아래 질문에 모두 답할 수 있게 만드는 것이 목표다.

그래서 이번에는 설명을 줄이고 코드를 썼다. **전부 합쳐 312줄이다.** 그리고 실제로 돌렸다.

이 글에 나오는 로그와 출력은 전부 그 실행 결과를 그대로 붙인 것이다. 지어낸 예시가 아니다.

---

## 무엇을 만들었는가

2편에서 정한 계약을 코드로 옮기고, `README를 개선해줘` 한 흐름을 끝까지 돌렸다.

```text
contracts.py     66줄   Task · Artifact · Event + 상태 전이표
tools.py         54줄   Tool 레지스트리 + 권한 교집합
runner.py        39줄   Planner · Developer · Reviewer
orchestrator.py  82줄   상태 머신 구동 + 이벤트 기록
test_guards.py   30줄   가드레일이 실제로 막는지 검증
replay.py        41줄   run_id 하나로 실행 전체 복원
```

프레임워크를 쓰지 않았다. LangGraph도, CrewAI도 없다.
**이 규모에서 필요한 건 프레임워크가 아니라 계약 세 개와 상태표 하나였다.**

---

## 1. 상태 전이를 표로 박아둔다

2편에서 Task 상태 머신을 그림으로 그렸다. 그림은 지켜지지 않는다. 코드가 지켜야 한다.

```python
ALLOWED = {
    TaskState.CREATED:  {TaskState.READY, TaskState.BLOCKED},
    TaskState.READY:    {TaskState.RUNNING, TaskState.BLOCKED},
    TaskState.RUNNING:  {TaskState.REVIEW, TaskState.FAILED, TaskState.BLOCKED},
    TaskState.REVIEW:   {TaskState.COMPLETED, TaskState.REVISION},
    TaskState.REVISION: {TaskState.RUNNING},
    TaskState.BLOCKED:  {TaskState.READY, TaskState.FAILED},
    TaskState.COMPLETED: set(),
    TaskState.FAILED:    set(),
}

def to(self, new: TaskState) -> None:
    if new not in ALLOWED[self.state]:
        raise IllegalTransition(f"{self.task_id}: {self.state.value} → {new.value} 는 허용되지 않는다")
    self.state = new
```

`COMPLETED` 와 `FAILED` 의 값이 빈 집합인 게 핵심이다. **끝난 Task는 되살아나지 못한다.**
재시도가 필요하면 `REVISION` 을 거쳐 새 버전을 만들어야 한다. 기존 산출물을 덮어쓰는 경로가 아예 없다.

---

## 2. 권한은 선언이 아니라 교집합이다

2편에서 "Tool 구현과 Tool 권한을 분리한다"고 썼다. 실제로 분리하면 이렇게 된다.

```python
# 워크스페이스가 정한 상한 — Agent 가 아무리 요구해도 이 밖으로는 못 나간다
WORKSPACE_GRANTS = {"fs.read", "fs.write", "fs.list"}

# Agent 가 요구하는 권한
AGENT_REQUESTS = {
    "planner":   {"fs.read", "fs.list"},
    "developer": {"fs.read", "fs.write"},
    "reviewer":  {"fs.read"},
}

def allowed_for(agent: str) -> set[str]:
    return WORKSPACE_GRANTS & AGENT_REQUESTS.get(agent, set())
```

한 줄짜리 교집합이지만 성질이 다르다.

Agent 정의 파일은 사람이 자주 고친다. 거기에 `fs.delete` 를 적어 넣어도 워크스페이스가 허용하지 않으면 실행되지 않는다.
**권한의 최종 결정권이 Agent 쪽이 아니라 워크스페이스 쪽에 있다.**

---

## 3. 그래서 정말 막히는가

여기서 멈추면 또 그림이다. 막히는지 직접 확인했다.

```python
tools.WORKSPACE_GRANTS.discard("fs.write")   # 워크스페이스가 쓰기 권한을 회수
tools.call("developer", "fs.write", path="x", content="y")
```

`test_guards.py` 실행 결과다.

```text
상태 머신
  차단됨 ✓  CREATED 에서 곧장 COMPLETED
            → t: CREATED → COMPLETED 는 허용되지 않는다
  차단됨 ✓  CREATED 에서 곧장 RUNNING
            → t: CREATED → RUNNING 는 허용되지 않는다

권한 (워크스페이스 ∩ Agent)
  차단됨 ✓  reviewer 가 파일 쓰기
            → reviewer 는 fs.write 권한이 없다
  차단됨 ✓  planner 가 파일 쓰기
            → planner 는 fs.write 권한이 없다
  차단됨 ✓  미등록 tool 호출
            → 등록되지 않은 tool: net.post

정상 경로는 통과해야 한다
  통과 ✓  CREATED → READY → RUNNING (현재 RUNNING)
  통과 ✓  developer 가 fs.read → 'hi'

워크스페이스가 권한을 회수하면 Agent 선언과 무관하게 막힌다
  차단됨 ✓  developer 가 파일 쓰기
            → developer 는 fs.write 권한이 없다
```

마지막 줄이 제일 중요하다. `developer` 는 자기 정의에 `fs.write` 를 갖고 있는데도 막혔다.
**권한을 회수하는 쪽이 실제로 이긴다.**

---

## 4. Agent끼리 대화시키지 않는다

2편에서 "Agent끼리 대화시키기보다 Artifact를 전달한다"고 썼다. 코드로 보면 Agent 함수의 시그니처가 그걸 강제한다.

```python
def run_developer(task: Task, log, plan: str, revision: int) -> Artifact: ...
def run_reviewer(task: Task, log, draft: Artifact) -> tuple[bool, list[str]]: ...
```

Developer는 Reviewer를 모른다. Reviewer도 Developer를 모른다.
둘 다 **Task를 받아 Artifact를 내놓을 뿐**이고, 누구에게 넘길지는 Orchestrator가 정한다.

Reviewer가 하는 일도 대화가 아니라 판정이다.

```python
checks = {
    "설치 섹션 존재": "## 설치" in content,
    "사용법 섹션 존재": "## 사용법" in content,
    "라이선스 섹션 존재": "## 라이선스" in content,
}
failed = [k for k, ok in checks.items() if not ok]
return (not failed), failed
```

의도적으로 문자열 검사로 뒀다. LLM에게 "이 문서 괜찮아?"를 묻는 순간 **판정 결과가 매번 달라지고 재현이 안 된다.**
검증 가능한 것은 코드로 검증하고, LLM은 생성 쪽에만 둔다. 2편에서 정한 원칙 그대로다.

---

## 5. 루프에는 상한이 있어야 한다

Developer → Reviewer 루프의 전부다.

```python
while True:
    r.move(t_dev, TaskState.RUNNING)
    draft = runner.run_developer(t_dev, r.log, plan.content, t_dev.revision)
    r.move(t_dev, TaskState.REVIEW)

    ok, failed = runner.run_reviewer(t_dev, r.log, draft)
    if ok:
        r.move(t_dev, TaskState.COMPLETED); break
    if t_dev.revision >= MAX_REVISION:
        r.move(t_dev, TaskState.REVISION)
        r.log("escalated_to_human", t_dev, "reviewer", reason="max_revision_exceeded", failed=failed)
        r.move(t_dev, TaskState.RUNNING); r.move(t_dev, TaskState.BLOCKED)
        break
    r.move(t_dev, TaskState.REVISION)
    t_dev.revision += 1
```

`while True` 를 쓰면서 탈출구를 세 개 뒀다. 통과, 상한 초과, 그리고 상태 전이 위반 시 예외.

상한을 넘으면 `FAILED` 가 아니라 **`BLOCKED` 로 보낸다.** 실패한 게 아니라 사람 판단이 필요한 상태이기 때문이다.
`escalated_to_human` 이벤트가 함께 남으니 나중에 "왜 멈췄나"를 로그만 보고 알 수 있다.

---

## 6. 실행 결과

`orchestrator.py` 를 돌리면 이벤트 **31건**이 나온다. 앞부분은 이렇게 생겼다.

```json
{"seq": 1, "run_id": "run-2026-08-23-001", "kind": "run_started", "payload": {"goal": "이 프로젝트 README를 개선해줘"}}
{"seq": 2, "run_id": "run-2026-08-23-001", "kind": "task_created", "task_id": "task-1", "agent": "planner", "payload": {"objective": "README 개선 계획 수립", "granted": ["fs.list", "fs.read"]}}
{"seq": 3, "run_id": "run-2026-08-23-001", "kind": "task_state_changed", "task_id": "task-1", "agent": "planner", "payload": {"from": "CREATED", "to": "READY"}}
{"seq": 5, "run_id": "run-2026-08-23-001", "kind": "tool_called", "task_id": "task-1", "agent": "planner", "payload": {"tool": "fs.read", "path": "README.md"}}
{"seq": 6, "run_id": "run-2026-08-23-001", "kind": "artifact_created", "task_id": "task-1", "agent": "planner", "payload": {"artifact_id": "art-plan-1", "path": "drafts/plan.md", "version": 1}}
```

`task_created` 에 **부여된 권한이 함께 찍히는 것**을 눈여겨볼 만하다.
사고가 났을 때 "그때 이 Agent가 무슨 권한이었나"를 코드가 아니라 로그에서 답할 수 있어야 한다.

---

## 7. 7개 질문에 답하기

2편이 3편에 던진 질문은 일곱 개였다. `replay.py` 는 **이벤트 로그만 읽는다.** 실행 중 메모리를 참조하지 않는다.

실제 출력이다.

```text
run_id: run-2026-08-23-001  ·  이벤트 31건

1. 어떤 Task가 생성됐는가?
   task-1  README 개선 계획 수립  (권한 ['fs.list', 'fs.read'])
   task-2  README 초안 작성  (권한 ['fs.read', 'fs.write'])

2. 어떤 Agent가 실행됐는가?
   planner    이벤트 8건
   developer  이벤트 16건
   reviewer   이벤트 5건

3. 어떤 Tool을 사용했는가?
   planner    fs.read   1회
   developer  fs.read   2회
   developer  fs.write  2회
   reviewer   fs.read   2회

4. 어떤 Artifact가 생성됐는가?
   art-plan-1     v1  drafts/plan.md  ← planner
   art-readme-1   v1  drafts/README.v1.md  ← developer
   art-readme-2   v2  drafts/README.v2.md  ← developer

5. Reviewer는 무엇을 검토했는가?
   1차: O 설치 섹션 존재  O 사용법 섹션 존재  X 라이선스 섹션 존재  → 반려
   2차: O 설치 섹션 존재  O 사용법 섹션 존재  O 라이선스 섹션 존재  → 통과

6. Revision은 몇 번 발생했는가?
   1회
   1차 사유: ['라이선스 섹션 존재']

7. 모든 이벤트를 run_id 하나로 재구성할 수 있는가?
   run_id 종류 1개 · seq 연속 True
   상태 전이: READY → RUNNING → REVIEW → REVISION → RUNNING → REVIEW → COMPLETED
```

일곱 개 다 답이 나왔다.

특히 4번이 마음에 든다. `README.v1.md` 와 `README.v2.md` 가 **둘 다 남아 있다.**
Reviewer가 반려했을 때 v1을 고친 게 아니라 v2를 새로 만들었기 때문이다. 반려된 초안이 증거로 남는다.

---

## 8. 돌려보고 나서 바뀐 생각

### 상태 머신이 문서보다 코드에 있어야 하는 이유를 이제 안다

2편을 쓸 때는 상태 다이어그램을 그리는 게 설계라고 생각했다.
막상 코드로 옮기니 `ALLOWED` 표 하나가 다이어그램 전체보다 강했다.

그림은 어겨도 아무 일도 안 일어난다. 표는 어기면 예외가 난다.

### 이벤트 설계가 Agent 설계보다 어려웠다

Agent 세 개를 만드는 데는 39줄이 들었다. 무엇을 이벤트로 남길지 정하는 데 훨씬 오래 걸렸다.

처음엔 `tool_called` 에 도구 이름만 남겼다. 그러면 "어떤 파일을 읽었나"를 알 수 없다.
`task_created` 에 권한을 안 남겼더니 "그때 왜 이게 실행됐나"를 못 되짚었다.

**로그는 나중에 물어볼 질문을 미리 정해야 설계된다.** 다행히 2편에서 그 질문 일곱 개를 먼저 적어뒀다.

### 프레임워크를 안 쓴 게 결과적으로 맞았다

312줄 중에 프레임워크가 대신해줬을 부분은 거의 없다.
어려운 건 오케스트레이션 배관이 아니라 **어디서 멈추고 누구에게 넘길지 정하는 일**이었고, 그건 어차피 직접 정해야 한다.

### 아직 안 한 것

정직하게 적어둔다.

```text
LLM 을 실제로 붙이지 않았다 — Agent 자리에 결정적 함수를 넣어 재현 가능하게 뒀다
파일시스템이 인메모리다 — 실제 디스크·Git 연동 없음
Human Approval 이 BLOCKED 로 표시만 되고 실제 승인 UI 가 없다
동시 실행이 없다 — Task 가 순차적으로만 돈다
비용·토큰 상한이 없다
```

LLM을 안 붙인 건 게으름이 아니라 순서 문제였다.
**모델을 먼저 붙이면 실패가 모델 탓인지 구조 탓인지 구분이 안 된다.** 구조가 결정적으로 도는 걸 확인하고 나서 붙이는 편이 낫다.

---

## 정리

```text
1편  폴더를 Agent Workspace 로 볼 수 있는가          — 개념
2편  정의/실행/Tool/Artifact 분리 + Policy·Event    — 설계
3편  Orchestrator 와 Runner 를 312줄로 구현하고 실행  — 검증
```

3편에서 확인하고 싶었던 건 하나였다.

**폴더 기반 Agent 아이디어가 코드로 옮겨질 때 무너지는가.**

안 무너졌다. 다만 무너지지 않은 이유가 아이디어가 좋아서가 아니라,
**계약 세 개(Task·Artifact·Event)와 상태표 하나를 먼저 고정했기 때문**이라는 게 이번에 얻은 결론이다.

다음은 LLM을 붙이는 일이다. 그때 이 로그 구조가 진짜 값을 하는지 보게 될 것 같다.

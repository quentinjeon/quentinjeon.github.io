"""Orchestrator — 상태 머신을 돌리고 모든 행동을 run_id 하나로 묶어 기록한다."""
import json, sys
from datetime import datetime, timezone
import tools, runner
from contracts import Task, TaskState, Event

MAX_REVISION = 2


class Run:
    def __init__(self, run_id: str, clock):
        self.run_id, self.seq, self.events, self.clock = run_id, 0, [], clock

    def log(self, kind, task=None, agent=None, **payload):
        self.seq += 1
        e = Event(self.seq, self.run_id, self.clock(), kind,
                  task.task_id if task else None, agent, payload)
        self.events.append(e)
        return e

    def move(self, task: Task, new: TaskState):
        old = task.state
        task.to(new)                                  # 허용되지 않는 전이면 여기서 예외
        self.log("task_state_changed", task, task.agent, **{"from": old.value, "to": new.value})


def improve_readme(run_id="run-2026-08-23-001", clock=None):
    clock = clock or (lambda: datetime.now(timezone.utc).isoformat(timespec="seconds"))
    r = Run(run_id, clock)
    tools.FS["README.md"] = "# demo\n\n데모 프로젝트다.\n"

    r.log("run_started", None, None, goal="이 프로젝트 README를 개선해줘")

    # 1) Planner
    t_plan = Task("task-1", "README 개선 계획 수립", "planner", ["README.md"])
    r.log("task_created", t_plan, "planner", objective=t_plan.objective,
          granted=sorted(tools.allowed_for("planner")))
    r.move(t_plan, TaskState.READY); r.move(t_plan, TaskState.RUNNING)
    plan = runner.run_planner(t_plan, r.log)
    r.log("artifact_created", t_plan, "planner", artifact_id=plan.artifact_id,
          path=plan.path, version=plan.version)
    r.move(t_plan, TaskState.REVIEW); r.move(t_plan, TaskState.COMPLETED)
    r.log("handoff", t_plan, "planner", to="developer", artifact=plan.artifact_id)

    # 2) Developer → Reviewer 루프
    t_dev = Task("task-2", "README 초안 작성", "developer", [plan.path])
    r.log("task_created", t_dev, "developer", objective=t_dev.objective,
          granted=sorted(tools.allowed_for("developer")))
    r.move(t_dev, TaskState.READY)

    draft = None
    while True:
        r.move(t_dev, TaskState.RUNNING)
        draft = runner.run_developer(t_dev, r.log, plan.content, t_dev.revision)
        r.log("artifact_created", t_dev, "developer", artifact_id=draft.artifact_id,
              path=draft.path, version=draft.version)
        r.move(t_dev, TaskState.REVIEW)
        r.log("handoff", t_dev, "developer", to="reviewer", artifact=draft.artifact_id)

        ok, failed = runner.run_reviewer(t_dev, r.log, draft)
        if ok:
            r.move(t_dev, TaskState.COMPLETED); break
        if t_dev.revision >= MAX_REVISION:
            r.move(t_dev, TaskState.REVISION)     # 상한 초과 → 사람에게 넘긴다
            r.log("escalated_to_human", t_dev, "reviewer", reason="max_revision_exceeded", failed=failed)
            r.move(t_dev, TaskState.RUNNING); r.move(t_dev, TaskState.BLOCKED)
            break
        r.move(t_dev, TaskState.REVISION)
        t_dev.revision += 1
        r.log("revision_requested", t_dev, "reviewer", attempt=t_dev.revision, failed=failed)

    r.log("run_finished", None, None, final_state=t_dev.state.value,
          revisions=t_dev.revision, final_artifact=draft.artifact_id)
    return r


if __name__ == "__main__":
    # 재현 가능한 실행: 시계를 고정한다
    ticks = iter(f"2026-08-23T0{h}:{m:02d}:00+00:00" for h in [1] for m in range(0, 60))
    r = improve_readme(clock=lambda: next(ticks))
    for e in r.events:
        print(json.dumps(e.as_dict(), ensure_ascii=False))

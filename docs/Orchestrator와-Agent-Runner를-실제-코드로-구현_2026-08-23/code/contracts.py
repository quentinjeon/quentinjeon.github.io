"""Task · Artifact · Event — 3편의 모든 코드가 이 세 계약 위에서만 움직인다."""
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any


class TaskState(str, Enum):
    CREATED = "CREATED"; READY = "READY"; RUNNING = "RUNNING"
    REVIEW = "REVIEW"; REVISION = "REVISION"; BLOCKED = "BLOCKED"
    COMPLETED = "COMPLETED"; FAILED = "FAILED"


# 허용된 전이만 통과시킨다. 여기 없는 전이는 코드가 거부한다.
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


@dataclass
class Task:
    task_id: str
    objective: str
    agent: str
    inputs: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    state: TaskState = TaskState.CREATED
    revision: int = 0

    def to(self, new: TaskState) -> None:
        if new not in ALLOWED[self.state]:
            raise IllegalTransition(f"{self.task_id}: {self.state.value} → {new.value} 는 허용되지 않는다")
        self.state = new


@dataclass
class Artifact:
    artifact_id: str
    task_id: str
    path: str
    version: int
    content: str
    produced_by: str


@dataclass
class Event:
    seq: int
    run_id: str
    ts: str
    kind: str
    task_id: str | None = None
    agent: str | None = None
    payload: dict[str, Any] = field(default_factory=dict)

    def as_dict(self): return asdict(self)


class IllegalTransition(Exception): ...
class PermissionDenied(Exception): ...

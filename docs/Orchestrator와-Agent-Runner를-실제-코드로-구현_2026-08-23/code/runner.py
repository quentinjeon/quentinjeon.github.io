"""Agent Runner — Agent 는 서로 대화하지 않는다. Task 를 받아 Artifact 를 낸다."""
import tools
from contracts import Task, Artifact

# 데모를 재현 가능하게 두려고 LLM 자리에 결정적 함수를 넣었다.
# 실제로는 이 자리에 모델 호출이 들어가고, 계약(입력 Task / 출력 Artifact)은 그대로다.

def run_planner(task: Task, log) -> Artifact:
    readme = tools.call("planner", "fs.read", path="README.md")
    log("tool_called", task, "planner", tool="fs.read", path="README.md")
    missing = [s for s in ("## 설치", "## 사용법", "## 라이선스") if s not in readme]
    plan = "\n".join(f"- {s} 섹션을 추가한다" for s in missing) or "- 변경 없음"
    return Artifact("art-plan-1", task.task_id, "drafts/plan.md", 1, plan, "planner")


def run_developer(task: Task, log, plan: str, revision: int) -> Artifact:
    base = tools.call("developer", "fs.read", path="README.md")
    log("tool_called", task, "developer", tool="fs.read", path="README.md")
    body = base.rstrip() + "\n\n## 설치\n\n```bash\npip install demo\n```\n\n## 사용법\n\n```bash\ndemo run\n```\n"
    if revision >= 1:                      # Reviewer 지적을 반영한 2차 시도
        body += "\n## 라이선스\n\nMIT\n"
    ver = revision + 1
    path = f"drafts/README.v{ver}.md"
    tools.call("developer", "fs.write", path=path, content=body)
    log("tool_called", task, "developer", tool="fs.write", path=path)
    return Artifact(f"art-readme-{ver}", task.task_id, path, ver, body, "developer")


def run_reviewer(task: Task, log, draft: Artifact) -> tuple[bool, list[str]]:
    content = tools.call("reviewer", "fs.read", path=draft.path)
    log("tool_called", task, "reviewer", tool="fs.read", path=draft.path)
    checks = {
        "설치 섹션 존재": "## 설치" in content,
        "사용법 섹션 존재": "## 사용법" in content,
        "라이선스 섹션 존재": "## 라이선스" in content,
    }
    failed = [k for k, ok in checks.items() if not ok]
    log("review_done", task, "reviewer", checks=checks, passed=not failed)
    return (not failed), failed

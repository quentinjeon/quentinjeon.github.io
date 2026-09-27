"""가드레일이 '문서상 규칙'이 아니라 실제로 막는지 확인한다."""
import tools
from contracts import Task, TaskState, IllegalTransition, PermissionDenied

def check(label, fn):
    try:
        fn(); print(f"  통과 안 됨 ✗  {label} — 막혔어야 하는데 실행됐다")
    except (IllegalTransition, PermissionDenied) as e:
        print(f"  차단됨 ✓  {label}\n            → {e}")

print("상태 머신")
t = Task("t", "o", "developer")
check("CREATED 에서 곧장 COMPLETED", lambda: t.to(TaskState.COMPLETED))
check("CREATED 에서 곧장 RUNNING",   lambda: t.to(TaskState.RUNNING))

print("\n권한 (워크스페이스 ∩ Agent)")
check("reviewer 가 파일 쓰기",  lambda: tools.call("reviewer", "fs.write", path="x", content="y"))
check("planner 가 파일 쓰기",   lambda: tools.call("planner", "fs.write", path="x", content="y"))
check("미등록 tool 호출",       lambda: tools.call("developer", "net.post", url="http://x"))

print("\n정상 경로는 통과해야 한다")
t2 = Task("t2", "o", "developer")
t2.to(TaskState.READY); t2.to(TaskState.RUNNING)
print(f"  통과 ✓  CREATED → READY → RUNNING (현재 {t2.state.value})")
tools.FS["a.md"] = "hi"
print(f"  통과 ✓  developer 가 fs.read → {tools.call('developer','fs.read',path='a.md')!r}")

print("\n워크스페이스가 권한을 회수하면 Agent 선언과 무관하게 막힌다")
tools.WORKSPACE_GRANTS.discard("fs.write")
check("developer 가 파일 쓰기", lambda: tools.call("developer", "fs.write", path="x", content="y"))

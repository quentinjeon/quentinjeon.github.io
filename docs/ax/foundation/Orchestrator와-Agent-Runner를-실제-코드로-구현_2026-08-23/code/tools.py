"""Tool 구현은 한 곳에만. Agent 는 '쓰겠다'고 선언만 하고, 실제 허용은 교집합으로 정한다."""
from contracts import PermissionDenied

REGISTRY: dict[str, dict] = {}


def tool(name: str, risk: str = "low"):
    def deco(fn):
        REGISTRY[name] = {"fn": fn, "risk": risk}
        return fn
    return deco


# 워크스페이스가 선언한 상한 — Agent 가 아무리 요구해도 이 밖으로는 못 나간다.
WORKSPACE_GRANTS = {"fs.read", "fs.write", "fs.list"}

# Agent 별 요구 권한
AGENT_REQUESTS = {
    "planner":   {"fs.read", "fs.list"},
    "developer": {"fs.read", "fs.write"},
    "reviewer":  {"fs.read"},
}


def allowed_for(agent: str) -> set[str]:
    """실제 실행 권한 = 워크스페이스 허용 ∩ Agent 요구"""
    return WORKSPACE_GRANTS & AGENT_REQUESTS.get(agent, set())


def call(agent: str, name: str, **kw):
    if name not in REGISTRY:
        raise PermissionDenied(f"등록되지 않은 tool: {name}")
    if name not in allowed_for(agent):
        raise PermissionDenied(f"{agent} 는 {name} 권한이 없다")
    return REGISTRY[name]["fn"](**kw)


FS: dict[str, str] = {}          # 데모용 인메모리 파일시스템


@tool("fs.read")
def _read(path: str) -> str:
    return FS.get(path, "")


@tool("fs.write", risk="medium")
def _write(path: str, content: str) -> int:
    FS[path] = content
    return len(content)


@tool("fs.list")
def _list(prefix: str = "") -> list[str]:
    return sorted(p for p in FS if p.startswith(prefix))

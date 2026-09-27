"""run_id 하나로 실행 전체를 되짚는다 — 2편이 3편에 던진 7개 질문에 로그만으로 답한다."""
import json, sys
from collections import Counter

ev = [json.loads(l) for l in open("events.jsonl", encoding="utf-8")]
q = lambda k: [e for e in ev if e["kind"] == k]

print(f"run_id: {ev[0]['run_id']}  ·  이벤트 {len(ev)}건\n")
print("1. 어떤 Task가 생성됐는가?")
for e in q("task_created"):
    print(f"   {e['task_id']}  {e['payload']['objective']}  (권한 {e['payload']['granted']})")

print("\n2. 어떤 Agent가 실행됐는가?")
for a, n in Counter(e["agent"] for e in ev if e["agent"]).items():
    print(f"   {a:<10} 이벤트 {n}건")

print("\n3. 어떤 Tool을 사용했는가?")
for a, t in Counter((e["agent"], e["payload"]["tool"]) for e in q("tool_called")).items():
    print(f"   {a[0]:<10} {a[1]:<9} {t}회")

print("\n4. 어떤 Artifact가 생성됐는가?")
for e in q("artifact_created"):
    p = e["payload"]
    print(f"   {p['artifact_id']:<14} v{p['version']}  {p['path']}  ← {e['agent']}")

print("\n5. Reviewer는 무엇을 검토했는가?")
for i, e in enumerate(q("review_done"), 1):
    p = e["payload"]
    marks = "  ".join(f"{'O' if v else 'X'} {k}" for k, v in p["checks"].items())
    print(f"   {i}차: {marks}  → {'통과' if p['passed'] else '반려'}")

print("\n6. Revision은 몇 번 발생했는가?")
rv = q("revision_requested")
print(f"   {len(rv)}회" + ("".join(f"\n   {r['payload']['attempt']}차 사유: {r['payload']['failed']}" for r in rv)))

print("\n7. 모든 이벤트를 run_id 하나로 재구성할 수 있는가?")
ids = {e["run_id"] for e in ev}
seqs = [e["seq"] for e in ev]
print(f"   run_id 종류 {len(ids)}개 · seq 연속 {seqs == list(range(1, len(ev)+1))}")
print(f"   상태 전이: " + " → ".join(
    e["payload"]["to"] for e in ev if e["kind"] == "task_state_changed" and e["task_id"] == "task-2"))

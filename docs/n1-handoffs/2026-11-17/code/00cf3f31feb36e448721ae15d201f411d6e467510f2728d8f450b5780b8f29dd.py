"""Bind the admitted kickoff to the actual running child and its first tool invocation."""
import datetime
import hashlib
import json
import sys
from pathlib import Path

FILES = Path(__file__).resolve().parent
ROOT = Path(r"C:\Users\stop-\n1-kanji-workspace")
sys.path.insert(0, str(ROOT / "review-tools"))
from common import COORDINATOR, freeze_json, frozen, require, sha, start_guard, write_frozen

CHILD = "c222bfef-4874-456d-b830-1b09165b1f40"


def main(snapshot):
    guard, _ = start_guard("B134 actual author launch observation")
    try:
        raw = snapshot.read_bytes()
        status = json.loads(raw)
        require(len(status["sessions"]) == status["summary"]["total"], "Incomplete post-launch status")
        author = next(row for row in status["sessions"] if row["id"] == CHILD)
        active = {row["id"] for row in status["sessions"]
                  if row.get("is_running") or row.get("activity", {}).get("status") != "idle"}
        require(author["name"] == "B134 kanji authoring"
                and author["activity"]["status"] == "busy"
                and author["creator_session_id"] == COORDINATOR
                and not author["awaiting_user_input"] and not author["awaiting_plan_approval"]
                and active == {COORDINATOR, CHILD}, "Launch activity or ownership differs")
        admission_raw = frozen(FILES / "b134-launch-admission-001.json")
        admission = json.loads(admission_raw)
        kickoff_raw = frozen(FILES / "b134-author-kickoff.txt", admission["kickoffSha256"])
        prefix, size, initial, first_tool = hashlib.sha256(), 0, None, None
        events = FILES.parent.parent / CHILD / "events.jsonl"
        with events.open("rb") as stream:
            for line in stream:
                guard.check()
                prefix.update(line)
                size += len(line)
                row = json.loads(line)
                if row["type"] == "user.message" and initial is None:
                    initial = row
                elif row["type"] == "tool.execution_start" and initial is not None:
                    first_tool = row
                    break
        require(initial is not None and first_tool is not None, "No actual kickoff/tool execution")
        content = initial["data"]["content"]
        require(content == kickoff_raw.decode("utf-8").rstrip("\n"), "Delivered kickoff differs")
        admitted_at = admission["observedAtEpochMs"] / 1000
        delivered_at = datetime.datetime.fromisoformat(initial["timestamp"].replace("Z", "+00:00")).timestamp()
        require(admission["admitted"] and 0 <= delivered_at - admitted_at <= 120,
                "Kickoff was outside its admission window")
        snapshot_ref = write_frozen(FILES / "b134-post-launch-full-status-001.json", raw)
        executions = {}
        for batch, name in ((133, "preserve-delivery-runs-002"), (133, "b134-tool-derivation-001"),
                            (133, "b134-preparation-execution-001"), (134, "author-admission-execution-001")):
            folder = ROOT / f"scratch-{batch}" / "review" / name
            receipt_raw = (folder / "receipt.json").read_bytes()
            receipt = json.loads(receipt_raw)
            log_raw = (folder / "output.log").read_bytes()
            require(receipt["exitCode"] == receipt["childExitCodeAfterCleanup"] == 0
                    and not receipt["memory"]["breach"] and receipt["cleanupError"] is None
                    and receipt["logSha256"] == sha(log_raw), "Execution evidence binding differs")
            for filename, data in (("receipt.json", receipt_raw), ("output.log", log_raw)):
                path = folder / filename
                path.chmod(0o444)
                frozen(path, sha(data))
            executions[name] = {"receiptSha256": sha(receipt_raw), "logSha256": sha(log_raw)}
        result = {
            "batch": 134, "session": CHILD, "observedBusy": True,
            "admissionSha256": sha(admission_raw), "kickoffSha256": sha(kickoff_raw),
            "initialUserEventId": initial["id"], "deliveredAt": initial["timestamp"],
            "observedAgentMode": initial["data"].get("agentMode"),
            "firstTool": first_tool["data"].get("toolName"),
            "firstToolAt": first_tool["timestamp"], "eventPrefixBytes": size,
            "eventPrefixSha256": prefix.hexdigest(), "fullStatus": snapshot_ref,
            "executions": executions, "modelOverride": None,
            "qualification": "Exact kickoff after host removal of final newline; delivery within120seconds; "
                             "actual busy child and tool activity. No authoring or review acceptance.",
        }
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Launch observation RAM breach")
    result["memory"] = memory
    print(freeze_json(FILES / "b134-launch-observation-001.json", result))


if __name__ == "__main__":
    main(Path(sys.argv[1]))

"""Observe actual prior context before dispatch; byte counts are not token predictions."""
import hashlib
import json
from pathlib import Path

from b130_context_confirmation import ROOT, binding
from common import freeze_json, frozen, require, start_guard
from finalize_b130_followup_v2 import check_proofs, read_binding


def main():
    preparation_path = ROOT / "confirmation-003-preparation.json"
    preparation = json.loads(frozen(preparation_path, "f0338fad27f5a3c28171cccaa207808992e5e7d61eb32d6af8ac1185a9735b8e"))
    proof = json.loads(frozen(ROOT / "delta-evidence-001" / "verification.json",
                              "0288e16198420c4e8b8b14a109ce6af2ac7cf4b8572468639b923aa59affa5a9"))
    runtime = read_binding(proof["proofs"]["runtime"])[1]
    sources = read_binding(proof["proofs"]["sourceReuse"])[1]
    check_proofs(preparation["candidate"], proof, runtime, sources,
                 proof["proofs"]["runtime"], proof["proofs"]["sourceReuse"])
    guard, _ = start_guard("B130 follow-up context observation")
    rows = []
    try:
        for planned in preparation["runs"]:
            path = Path.home() / ".copilot" / "session-state" / planned["session"] / "events.jsonl"
            before = path.stat()
            digest, last_usage, compactions = hashlib.sha256(), None, []
            with path.open("rb") as stream:
                for line in stream:
                    require(line.endswith(b"\n"), "Incomplete reviewer event")
                    digest.update(line)
                    event = json.loads(line)
                    if event.get("type") == "session.usage_record":
                        usage = event["data"]["usage"]
                        last_usage = {"timestamp": event["timestamp"], **{key: usage.get(key) for key in
                                      ("model", "inputTokens", "outputTokens", "maxPromptTokens")}}
                    elif str(event.get("type", "")).startswith("session.compaction"):
                        compactions.append(event["type"])
                    guard.check()
            after = path.stat()
            require(before.st_size == after.st_size and before.st_mtime_ns == after.st_mtime_ns
                    and last_usage is not None and not compactions, "Reviewer changed or compacted")
            require(not (ROOT / "confirm" / f"{planned['run']}-admission.json").exists(),
                    "Already admitted")
            rows.append({**planned, "eventsBytes": after.st_size, "eventsSha256": digest.hexdigest(),
                         "lastUsage": last_usage, "observedCompactions": compactions,
                         "remainingToReportedMaximum": last_usage["maxPromptTokens"] - last_usage["inputTokens"]})
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Capacity observation breached RAM guard")
    result = freeze_json(ROOT / "followup003-capacity-observation-001.json", {
        "batch": 130, "candidate": preparation["candidate"], "preparation": binding(preparation_path),
        "reviewers": rows, "actualMechanicalProofsPassFollowupFinalizerCheck": True,
        "limits": "Read-only pre-admission observation, not token prediction or final context acceptance. "
                  "No review launched and no final confirmation accepted.",
        "memory": memory, "producer": binding(__file__),
    })
    print(json.dumps({"observation": result, "reviewers": rows}))


if __name__ == "__main__":
    main()

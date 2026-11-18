"""Observe current same-family reviewer capacity without admitting or messaging either."""
import hashlib
import json
from pathlib import Path

from b130_context_confirmation import ROOT
from common import freeze_json, frozen, require, sha, start_guard

SESSIONS = {"claude": "a446a6a9-6aed-407e-9bd8-b2508bc2941f",
            "gpt": "232e66de-5462-45bf-ad20-74316e4e006d"}


def main():
    guard, _ = start_guard("B130 integration confirmation capacity observation")
    rows = []
    try:
        for family, session in SESSIONS.items():
            path = Path.home() / ".copilot" / "session-state" / session / "events.jsonl"
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
                    and last_usage is not None, "Reviewer changed during observation")
            rows.append({"family": family, "session": session, "eventsBytes": after.st_size,
                         "eventsSha256": digest.hexdigest(), "lastUsage": last_usage,
                         "observedCompactions": compactions,
                         "remainingToReportedMaximum": last_usage["maxPromptTokens"] - last_usage["inputTokens"]})
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Capacity observation breached RAM guard")
    record = freeze_json(ROOT / "integration-capacity-observation-001.json", {
        "reviewers": rows, "memory": memory,
        "limits": "Current bounded usage observation only; not a token prediction, admission or "
                  "context acceptance. Raw events remain local. No reviewer contacted or launched.",
        "producerSha256": sha(frozen(Path(__file__))),
    })
    print(json.dumps({"observation": record, "reviewers": rows}))


if __name__ == "__main__":
    main()

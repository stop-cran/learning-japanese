import collections
import json
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, start_guard, write_frozen

SESSION = "adb64370-2aa5-4eb8-9e28-c5cf3111bf2b"
ROOT = WS / "scratch-134" / "review"
LIFECYCLE = ROOT / "fresh-independent-002" / "lifecycle-011"
OUTPUT = ROOT / "fresh-002-launch-hold-001"


def main():
    require(not OUTPUT.exists(), "Preserve the previous launch-failure capture")
    guard, _ = start_guard("B134 failed prompt-only bootstrap preservation")
    try:
        source = Path.home() / ".copilot" / "session-state" / SESSION / "events.jsonl"
        raw = source.read_bytes()
        events = [json.loads(line) for line in raw.decode("utf-8").splitlines()]
        preflight = json.loads(frozen(
            LIFECYCLE / "audit-configs-015" / "preflight.json",
            "f9cf056904cb37379f6e207c665366118383f5291dddc30f4643cac75d89ed94"))
        spec = preflight["runs"]["claude"]
        starts = [event["data"] for event in events if event["type"] == "session.start"]
        users = [event["data"] for event in events if event["type"] == "user.message"]
        tools = [event["data"] for event in events if event["type"] == "tool.execution_start"]
        results = [event["data"] for event in events if event["type"] == "tool.execution_complete"]
        usages = [event["data"]["usage"] for event in events if event["type"] == "session.usage_record"]
        require(len(starts) == 1 and starts[0]["sessionId"] == SESSION
                and starts[0]["selectedModel"] == "claude-opus-5.5"
                and starts[0]["contextTier"] == "long_context", "Launch identity differs")
        require(users[0]["content"] == spec["kickoffText"] and len(users) > 1
                and all(user["content"] == "" and user["source"] == "autopilot"
                        for user in users[1:]), "Unexpected extra user activity")
        require(len(tools) == len(results) == 1 and tools[0]["toolName"] == "view"
                and tools[0]["arguments"] == {"path": spec["prompt"]["path"],
                                              "forceReadLargeFiles": True}
                and results[0]["toolCallId"] == tools[0]["toolCallId"]
                and results[0]["success"] is True
                and results[0]["result"]["content"].encode("utf-8")
                == frozen(spec["prompt"]["path"], spec["prompt"]["sha256"]),
                "Activity was not limited to one exact prompt read")
        require(usages and all(usage["model"] == "claude-opus-5.5"
                               and usage["maxPromptTokens"] == 952000 for usage in usages)
                and not any("compaction" in event["type"] for event in events),
                "Observed context differs")
        for suffix in ("launch", "bootstrap", "core-authorization", "phase1", "extension", "final", "acceptance"):
            require(not (LIFECYCLE / f"{spec['run']}-{suffix}.json").exists(),
                    "Unexpected successful review artifact: " + suffix)
        require(not Path(spec["report"]).exists() and source.read_bytes() == raw,
                "Unexpected report or changing event record")
        snapshot = write_frozen(OUTPUT / "events.jsonl", raw)
        require(frozen(snapshot["path"], snapshot["sha256"]) == raw, "Snapshot readback differs")
        guard.check()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Preservation RAM breach")
    print(json.dumps(freeze_json(OUTPUT / "quarantine.json", {
        "status": "QUARANTINED_PROMPT_ONLY_AUTOPILOT_LAUNCH_NOT_REVIEW",
        "run": spec["run"], "session": SESSION, "candidate": preflight["candidate"],
        "events": snapshot, "eventTypes": dict(collections.Counter(event["type"] for event in events)),
        "extraAutopilotUserTurns": len(users) - 1, "promptReads": 1, "coreReads": 0,
        "actualSelectedModel": starts[0]["selectedModel"], "contextTier": starts[0]["contextTier"],
        "maxPromptTokens": 952000, "peakInputTokens": max(usage["inputTokens"] for usage in usages),
        "compactionEvents": [], "reportCreated": False, "reviewAccepted": False,
        "failureReceipt": {
            "path": str(ROOT / "b134-lifecycle-run-a2b00d975a8f4f62a6b664849527190d" / "receipt.json"),
            "sha256": sha(frozen(
                ROOT / "b134-lifecycle-run-a2b00d975a8f4f62a6b664849527190d" / "receipt.json")),
        },
        "cause": "Coordinator chose autopilot at launch despite a mandatory prompt-only wait. "
                 "Host continuation prompts violated the frozen launch/bootstrap contract.",
        "remedy": "Do not reuse this session. A separately admitted FRESH-003 pair must use "
                  "interactive launch mode, unchanged measured core and all original guards.",
        "limits": "Raw events remain local. No source review, semantic verdict, closure or delivery credit.",
        "memory": memory,
    })))


if __name__ == "__main__":
    main()

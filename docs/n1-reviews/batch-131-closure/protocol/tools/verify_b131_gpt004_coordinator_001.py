"""Independently bind the GPT004 handoff and replay controls in a fresh output namespace."""
import difflib
import json
import sys
from pathlib import Path
from unittest.mock import patch

from b131_review_v4_common import (
    DEFAULT_PREFLIGHT, HERE, IMMUTABLE_BINDINGS, RECORDS, TOOLS,
    freeze_json, frozen, load_module, require, sha, start_guard)
from b131_preflight_004 import verify_protocol, verify_subset

OUTPUT = RECORDS / "preparation004-coordinator-verification-001.json"
REPLAY = RECORDS / "preparation004-coordinator-controls-001"


def bound(path, digest):
    raw = frozen(Path(path), digest)
    return {"path": str(path), "sha256": sha(raw), "bytes": len(raw)}


def main():
    require(len(sys.argv) == 3, "Expected handoff path and independently received SHA256")
    require(not OUTPUT.exists() and not REPLAY.exists(), "Preserve previous verification outputs")
    handoff_path = Path(sys.argv[1])
    handoff_binding = bound(handoff_path, sys.argv[2])
    handoff = json.loads(frozen(handoff_path, sys.argv[2]))
    require(handoff["status"] == "VERIFIED_GPT004_PREPARATION_ONLY", "Handoff is not ready")
    guard, _ = start_guard("B131 GPT004 independent coordinator verification")
    try:
        bindings = []
        for item in handoff["artifacts"] + [handoff["commands"]]:
            value = bound(item["path"], item["sha256"])
            require(value["bytes"] == item["bytes"], "Handoff artifact length differs")
            bindings.append(value)
            guard.check()
        for path, digest in IMMUTABLE_BINDINGS:
            bindings.append(bound(path, digest))
        require(handoff["contextProfiles"] == {
            "claude": {"selectedModel": "claude-opus-5.5", "maxPromptTokens": 952000, "prePhase2Gate": 740000},
            "gpt": {"selectedModel": "gpt-6.1-sol", "maxPromptTokens": 922000, "prePhase2Gate": 710000},
        }, "Unexpected context profiles")
        require(handoff["forecastPhase1Tokens"] == 526615
                and handoff["projectedStartupWorstCase"] == 698784
                and handoff["startupGate"] == 700000 and handoff["gptPrePhase2Gate"] == 710000,
                "Conservative forecast or gate differs")
        require(not handoff["memory"]["breach"], "Preparer RAM breach")
        validation = json.loads(frozen(handoff["tests"]["path"], handoff["tests"]["sha256"]))
        require(validation["status"] == "PASS" and validation["tests"] == 39
                and validation["failures"] == validation["errors"] == 0
                and not validation["memory"]["breach"], "Expected focused controls did not pass")
        bound(Path(handoff["tests"]["path"]).parent / "output.log", validation["outputSha256"])
        bound(validation["testTool"]["path"], validation["testTool"]["sha256"])

        before = frozen(TOOLS / "step_b131_neutral_006.py",
            "b7bb9866b6ba1cfde4899bdd8563d17fbdbd953f6911c1872e56e406a9340df7").decode("utf-8")
        after = frozen(TOOLS / "step_b131_neutral_007.py").decode("utf-8")
        actual_diff = "".join(difflib.unified_diff(
            before.splitlines(keepends=True), after.splitlines(keepends=True),
            fromfile="step_b131_neutral_006.py", tofile="step_b131_neutral_007.py"))
        require(actual_diff == frozen(HERE / "fresh-step007.diff").decode("utf-8"),
                "Reviewed lifecycle diff does not describe the actual source")
        preflight = json.loads(frozen(DEFAULT_PREFLIGHT))
        protocol = verify_protocol(preflight)
        evidence = verify_subset(guard, initial=True)
        tests = load_module("b131004_coordinator_replayed_controls", TOOLS / "test_b131_gpt004.py")
        original_loader = tests.load_module

        def replay_loader(name, path):
            module = original_loader(name, path)
            if Path(path) == HERE / "test-controls-004.py":
                module.ROOT = REPLAY
            return module

        with patch.object(tests, "ROOT", REPLAY), patch.object(tests, "load_module", replay_loader):
            require(tests.main() == 0, "Coordinator replay failed")
        replay = json.loads(frozen(REPLAY / "result.json"))
        require(replay["status"] == "PASS" and replay["tests"] == 39
                and replay["failures"] == replay["errors"] == 0,
                "Coordinator controls incomplete")
        for item in bindings:
            require(bound(item["path"], item["sha256"]) == item, "Bound artifact changed during replay")
        require(verify_protocol(preflight) == protocol, "Report destinations changed during replay")
        memory = guard.finish()
        require(not memory["breach"], "Coordinator RAM breach")
        result = {
            "status": "PASS_PREPARATION_ONLY", "handoff": handoff_binding,
            "bindings": bindings, "protocol": protocol, "evidence": evidence,
            "replayedControls": bound(REPLAY / "result.json", sha(frozen(REPLAY / "result.json"))),
            "replayedLog": bound(REPLAY / "output.log", replay["outputSha256"]),
            "memory": memory,
            "tool": bound(Path(__file__), sha(frozen(Path(__file__)))),
            "limits": "Fresh admission and independent GPT004 review remain required. GPT003 stays HOLD. "
                      "No reviewer findings, candidate edits, semantic acceptance or publication."
        }
        print(json.dumps(freeze_json(OUTPUT, result)))
    except (Exception, KeyboardInterrupt):
        guard.finish()
        raise


if __name__ == "__main__":
    main()

"""Recheck immutable protocol bindings and rerun its controls in fresh isolated outputs."""
import json
from pathlib import Path

from b131_review_v2_common import (
    HERE, RECORDS, TOOLS, freeze_json, frozen, load_module, require, sha, start_guard)
from verify_b131_preparation_002 import verify


HANDOFF = HERE / "preparation-handoff-003.json"
HANDOFF_SHA = "208cc84fd841b33e431dda247599daf3b2e77a279357cc26bfbb9501eade0cfc"
OUTPUT = RECORDS / "compact002-protocol-coordinator-verification-001.json"
TEST_ROOT = RECORDS / "compact002-protocol-coordinator-tests-001"


def main():
    require(not OUTPUT.exists() and not TEST_ROOT.exists(), "Preserve previous verification attempts")
    guard, _ = start_guard("B131 compact002 coordinator protocol qualification")
    try:
        handoff = json.loads(frozen(HANDOFF, HANDOFF_SHA))
        require(handoff["status"] == "VERIFIED_CAPACITY_GATED_PREPARATION_ONLY",
                "Unexpected preparation handoff")
        bindings = []
        for group, rows in handoff["files"].items():
            for row in rows:
                guard.check()
                raw = frozen(row["path"], row["sha256"])
                require(len(raw) == row["bytes"], "Handoff length mismatch: " + row["path"])
                bindings.append({"group": group, "path": row["path"], "sha256": sha(raw)})
        for name in ("verifiedPreflight", "supersedes", "remainderQueryClarification"):
            row = handoff[name]
            raw = frozen(row["path"], row["sha256"])
            if "bytes" in row:
                require(len(raw) == row["bytes"], "Handoff ancillary length mismatch: " + name)

        qualification = verify(guard)
        test = load_module("b131_compact002_coordinator_controls",
                           TOOLS / "test_b131_compact_002.py")
        test.ROOT = TEST_ROOT
        require(test.main() == 0, "Coordinator replay of protocol controls failed")
        result_path = TEST_ROOT / "result.json"
        result = json.loads(frozen(result_path))
        require(result["status"] == "PASS" and result["tests"] == 24
                and result["failures"] == result["errors"] == 0
                and not result["memory"]["breach"], "Incomplete coordinator controls")
        frozen(TEST_ROOT / "output.log", result["outputSha256"])
        repeated = verify(guard)
        require(repeated == qualification, "Protocol changed during coordinator verification")
        memory = guard.finish()
        require(not memory["breach"], "Coordinator protocol verification RAM breach")
        proof = {
            "status": "PASS_PREPARATION_ONLY",
            "handoff": {"path": str(HANDOFF), "sha256": HANDOFF_SHA},
            "bindings": bindings,
            "qualification": qualification,
            "replayedControls": {
                "path": str(result_path), "sha256": sha(frozen(result_path)),
                "tests": result["tests"], "outputSha256": result["outputSha256"]},
            "tool": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
            "memory": memory,
            "limits": "Immutable protocol qualification and actual isolated control replay only. "
                      "No reviewer admission, semantic acceptance or publication. "
                      "Actual full-roster/RAM admission, no-compaction context and selected-evidence "
                      "phase2 gates remain mandatory."
        }
        print(json.dumps(freeze_json(OUTPUT, proof)))
    except (Exception, KeyboardInterrupt):
        guard.finish()
        raise


if __name__ == "__main__":
    main()

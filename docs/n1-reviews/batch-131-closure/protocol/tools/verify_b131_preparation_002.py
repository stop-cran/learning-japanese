"""Repeatable read-only qualification; not reviewer admission or launch permission."""
import json
from pathlib import Path

from b131_review_v2_common import (
    HERE, RUNS, freeze_json, frozen, require, sha, start_guard)
from b131_preflight_002 import verify_protocol, verify_subset


def verify(guard):
    subset = verify_subset(guard, initial=True)
    path = HERE / "prompts/preflight-compact-002.json"
    protocol = verify_protocol(json.loads(frozen(path)))
    result_path = HERE / "validation-001/result.json"
    tests = json.loads(frozen(result_path))
    require(tests["status"] == "PASS" and tests["tests"] == 24
            and tests["failures"] == tests["errors"] == 0
            and not tests["memory"]["breach"], "Focused current validation did not pass")
    frozen(tests["testTool"]["path"], tests["testTool"]["sha256"])
    frozen(result_path.parent / "output.log", tests["outputSha256"])
    for spec in json.loads(frozen(path))["runs"].values():
        require(not Path(spec["report"]).exists(), "Reviewer report unexpectedly exists")
    for run in RUNS:
        for suffix in ("-admission.json", "-launch.json", "-extension.json", "-phase2-message.txt"):
            require(not (HERE / (run + suffix)).exists(), "Unexpected actual reviewer lifecycle output")
        require(not (HERE / run).exists(), "Unexpected actual reviewer audit directory")
    return {
        "status": "PREFLIGHT_PREPARATION_READY_ONLY", "subset": subset, "protocol": protocol,
        "protocolPreflight": {"path": str(path), "sha256": sha(frozen(path))},
        "tests": {"path": str(result_path), "sha256": sha(frozen(result_path)), "passed": tests["tests"]},
        "reviewerAdmitted": False, "reviewerLaunched": False,
        "limits": "Fresh full-roster/RAM admission, actual model/context telemetry and runtime phase2 "
                  "capacity/evidence gates remain required. This is not permission or a no-compaction guarantee."}


def main():
    guard, _ = start_guard("B131002 repeatable read-only preparation verification")
    try:
        result = verify(guard)
        result["memory"] = guard.finish()
        require(not result["memory"]["breach"], "Preparation verification RAM breach")
        print(json.dumps(result, ensure_ascii=False))
    except (Exception, KeyboardInterrupt):
        guard.finish()
        raise


if __name__ == "__main__":
    main()

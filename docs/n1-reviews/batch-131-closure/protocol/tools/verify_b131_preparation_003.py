"""Repeatable fresh003 path/evidence qualification; never admit, launch or message a reviewer."""
import json
from pathlib import Path

from b131_review_v3_common import (
    DEFAULT_PREFLIGHT, HERE, RUNS, frozen, require, sha, start_guard)
from b131_preflight_003 import verify_protocol, verify_subset
from b131_path_readiness_004 import path_inventory


def verify(guard):
    evidence = verify_subset(guard, initial=True)
    spec = json.loads(frozen(DEFAULT_PREFLIGHT))
    frozen(spec["pathReadiness"]["path"], spec["pathReadiness"]["sha256"])
    protocol = verify_protocol(spec)
    inventory = path_inventory(spec)
    readiness_path = HERE / "path-readiness-004.json"
    readiness = json.loads(frozen(readiness_path))
    require(readiness["status"] == "PASS" and readiness["reviewerPathInventory"] == inventory,
            "Corrected path readiness does not match the actual builder")
    test_path = HERE / "validation-002/result.json"
    tests = json.loads(frozen(test_path))
    require(tests["status"] == "PASS" and tests["tests"] == 32
            and tests["existingControls"] == 24 and tests["newPathControls"] == 7
            and tests["newCompleteCreateReadbackControl"] == 1
            and tests["errors"] == tests["failures"] == 0 and not tests["memory"]["breach"],
            "All existing and new focused controls must pass")
    frozen(tests["testTool"]["path"], tests["testTool"]["sha256"])
    frozen(test_path.parent / "output.log", tests["outputSha256"])
    inventory_test_path = HERE / "validation-paths-004/result.json"
    extra_tests = json.loads(frozen(inventory_test_path))
    require(extra_tests["status"] == "PASS" and extra_tests["tests"] == 3
            and extra_tests["errors"] == extra_tests["failures"] == 0
            and not extra_tests["memory"]["breach"], "Inventory controls must pass")
    frozen(extra_tests["testTool"]["path"], extra_tests["testTool"]["sha256"])
    frozen(inventory_test_path.parent / "output.log", extra_tests["outputSha256"])
    for run in RUNS:
        for suffix in ("-admission.json", "-launch.json", "-phase1.json", "-extension.json",
                       "-phase2-message.txt", "-final.json", "-acceptance.json"):
            require(not (HERE / (run + suffix)).exists(), "Unexpected actual003 lifecycle artifact")
        require(not (HERE / run).exists(), "Unexpected actual003 audit directory")
    return {
        "status": "VERIFIED_FRESH003_PREPARATION_ONLY", "evidence": evidence, "protocol": protocol,
        "reviewerPathInventory": inventory,
        "preflight": {"path": str(DEFAULT_PREFLIGHT), "sha256": sha(frozen(DEFAULT_PREFLIGHT))},
        "activePathReadiness": {"path": str(readiness_path), "sha256": sha(frozen(readiness_path))},
        "tests": {"path": str(test_path), "sha256": sha(frozen(test_path)), "passed": 32},
        "inventoryTests": {"path": str(inventory_test_path), "sha256": sha(frozen(inventory_test_path)), "passed": 3},
        "limits": "Not reviewer admission. Fresh full-roster/RAM admission, actual model/context/no-compaction "
                  "and unchanged700000/740000 capacity gates remain mandatory. No guarantee against future path races.",
        "notPerformed": ["No reviewer admitted/launched/messaged",
                         "No retired reviewer events, phase1 list, report or final opened",
                         "No teaching edits, commits, pushes or publication"]}


def main():
    guard, _ = start_guard("B131003 fresh preparation verification")
    try:
        result = verify(guard)
        result["memory"] = guard.finish()
        require(not result["memory"]["breach"], "Fresh preparation verification RAM breach")
        print(json.dumps(result, ensure_ascii=False))
    except (Exception, KeyboardInterrupt):
        guard.finish()
        raise


if __name__ == "__main__":
    main()

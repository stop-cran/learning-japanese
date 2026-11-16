"""Verify immutable derivations and explicitly load the hyphenated fixture modules."""
import io
import json
import unittest
from pathlib import Path

from common import WS, freeze_json, frozen, load_module, require, sha, write_frozen

HERE = WS / "scratch-127" / "review" / "confirm"
PREPARATION_SHA = "8a10f48fda2d73d540c4f563cb6ff8b853d9f5b6756336e4b02fcd6ea126b1a3"


def main():
    previous = json.loads(frozen(HERE / "tooling-preflight.json", PREPARATION_SHA))
    require(previous["status"] == "HOLD" and previous["exitCode"] == 5,
            "Unexpected prior fixture invocation")
    for item in previous["derivations"]:
        original = frozen(item["source"]["path"], item["source"]["sha256"])
        output = frozen(item["output"]["path"], item["output"]["sha256"])
        require(output == original.replace(b"B125", b"B127")
                and output.replace(b"B127", b"B125") == original,
                "Confirmation derivation differs")
    engine = previous["engineDerivation"]
    original = frozen(engine["source"]["path"], engine["source"]["sha256"])
    derived = frozen(engine["output"]["path"], engine["output"]["sha256"])
    require(derived.replace(engine["after"].encode("ascii"), engine["before"].encode("ascii"))
            == original, "Confirmation engine differs")
    frozen(engine["helper"]["path"], engine["helper"]["sha256"])
    renderer = load_module("b127_verified_renderer", HERE / "renderer.py")
    renderer.self_test()
    suites = []
    for index, name in enumerate(("test-audit-confirm-isolated.py", "test-confirm-structure.py")):
        module = load_module(f"b127_confirmation_fixture_{index}", HERE / name)
        suites.append(unittest.defaultTestLoader.loadTestsFromModule(module))
    require(sum(suite.countTestCases() for suite in suites) == 21, "Incomplete protocol fixture suite")
    helper_tests = Path(__file__).with_name("test_b127_lifecycle_process.py")
    frozen(helper_tests)
    module = load_module("b127_confirmation_process_fixtures", helper_tests)
    suites.append(unittest.defaultTestLoader.loadTestsFromModule(module))
    log = io.StringIO()
    result = unittest.TextTestRunner(stream=log, verbosity=2).run(unittest.TestSuite(suites))
    log_text = log.getvalue()
    print(log_text, flush=True)
    log_binding = write_frozen(HERE / "tooling-tests-recovery-001.txt", log_text.encode("utf-8"))
    record = {
        **previous,
        "status": "PASS_PREPARATION_ONLY" if result.wasSuccessful() else "HOLD",
        "exitCode": 0 if result.wasSuccessful() else 1,
        "tests": log_binding,
        "testCount": result.testsRun,
        "protocolTestCount": 21,
        "boundedProcessTestCount": 4,
        "recovery": "Explicit module loading executes the unchanged hyphenated tests which "
                    "unittest discovery skipped. Original failed invocation and all bytes preserved.",
        "originalPreflightSha256": PREPARATION_SHA,
        "verifier": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "helperTests": {"path": str(helper_tests), "sha256": sha(frozen(helper_tests))},
    }
    print(json.dumps(freeze_json(HERE / "tooling-preflight-recovery-001.json", record)), flush=True)
    require(result.wasSuccessful() and result.testsRun == 25, "Confirmation/tool helper tests failed")


if __name__ == "__main__":
    main()

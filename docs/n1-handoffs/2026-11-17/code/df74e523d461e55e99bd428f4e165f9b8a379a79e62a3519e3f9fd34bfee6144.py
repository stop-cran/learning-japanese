"""Derive B125 confirmation gates from the verified, isolated B124 fixtures."""
import json
import subprocess
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, load_module, require, sha, write_frozen

SOURCE = WS / "scratch-124" / "review" / "confirm"
OUTPUT = WS / "scratch-125" / "review" / "confirm"
RECOVERY_SHA = "c21693f20db0cbeefc2ac01a924a98fc1fdb29863f8a353605ab7ebd4eb742e2"


def main():
    producer = frozen(Path(__file__))
    recovery_path = SOURCE / "tooling-preflight-recovery-001.json"
    recovery = json.loads(frozen(recovery_path, RECOVERY_SHA))
    require(recovery["status"] == "PASS_PREPARATION_ONLY"
            and recovery["testCount"] == 21, "Source tooling was not accepted")
    original = json.loads(frozen(SOURCE / "tooling-preflight.json",
                                 recovery["originalPreflightSha256"]))
    fixtures = json.loads(frozen(SOURCE / "test-fixture-derivation-001.json",
                                 recovery["fixtureDerivationSha256"]))
    selected = list(recovery["productionOutputs"])
    selected.append(fixtures["test"]["output"])
    selected.append(next(item["output"] for item in original["derivations"]
                         if Path(item["output"]["path"]).name == "test-confirm-structure.py"))
    require({Path(item["path"]).name for item in selected} == {
        "audit-confirm.py", "check-confirm-structure.py", "renderer.py",
        "test-audit-confirm-isolated.py", "test-confirm-structure.py",
    }, "Incomplete confirmation tooling")
    inputs = [(Path(item["path"]), frozen(item["path"], item["sha256"])) for item in selected]
    require(not OUTPUT.exists(), "Preserve existing B125 confirmation directory")
    derivations = []
    for source, raw in inputs:
        require(b"B125" not in raw, "Unexpected destination identity in source")
        derived = raw.replace(b"B124", b"B125")
        require(derived.replace(b"B125", b"B124") == raw, "Nonreversible batch substitution")
        compile(derived, source.name, "exec")
        derivations.append({
            "source": {"path": str(source), "sha256": sha(raw)},
            "output": write_frozen(OUTPUT / source.name, derived),
            "reverseExact": True,
            "soleDelta": "B124 to B125; production rules and all fixture assertions unchanged",
        })
    renderer = load_module("b125_confirmation_renderer", OUTPUT / "renderer.py")
    renderer.self_test()
    test = subprocess.run(
        [sys.executable, "-B", "-m", "unittest", "test-audit-confirm-isolated",
         "test-confirm-structure"],
        cwd=OUTPUT, capture_output=True,
    )
    raw_log = test.stdout + test.stderr
    log = write_frozen(OUTPUT / "tooling-tests.txt", raw_log)
    record = {
        "batch": 125,
        "status": "PASS_PREPARATION_ONLY" if test.returncode == 0 else "HOLD",
        "sourceRecovery": {"path": str(recovery_path), "sha256": RECOVERY_SHA},
        "derivations": derivations,
        "exitCode": test.returncode,
        "tests": log,
        "rendererChecks": 3,
        "producer": {"path": str(Path(__file__)), "sha256": sha(producer)},
        "limits": "No candidate, confirmation packet, reviewer launch or publication acceptance. "
                  "Uses the already verified per-invocation fixture isolation, without replaying "
                  "or overwriting the historical B124 fixture failure.",
    }
    print(json.dumps(freeze_json(OUTPUT / "tooling-preflight.json", record)))
    print(raw_log.decode("utf-8"))
    require(test.returncode == 0, "Confirmation fixture suite failed")


if __name__ == "__main__":
    main()

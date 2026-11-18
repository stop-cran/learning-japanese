"""Verify prepared confirmation tools and their real controls, without admitting a reviewer."""
import json
from pathlib import Path

from b134_initial_records import INITIALS, actual_initial, disposition_ids
from common import TOOLS, WS, freeze_json, frozen, require, sha
from prepare_b134_confirmation_engine import OUT, SOURCES, derive

ROOT = WS / "scratch-134" / "review"
RUNNER_SHA = "52d7b2a997aa707358556d7cbb0fa621e4383df45bf67c84b52bd729a52ad283"
GUARD_SHA = "46c721d63970e352a2c5c9d21c5d67b216e88a160b0966e65e2e407c0cb41c84"
EXECUTIONS = {
    "confirmation-initial-controls-001": 4,
    "confirmation-initial-binding-execution-001": 0,
    "confirmation-engine-preparation-execution-001": 0,
    "confirmation-engine-controls-001": 8,
}


def main():
    derivation_raw = frozen(OUT / "derivation.json",
                            "4a6ff447b046dcccaee76effea561d804471fba5735978bd3b7502e45202d932")
    derivation = json.loads(derivation_raw)
    expected = []
    for name in SOURCES:
        target, raw, record = derive(name)
        require(frozen(target) == raw, "Derived executable differs: " + name)
        expected.append({**record, "output": {"path": str(target), "sha256": sha(raw), "bytes": len(raw)}})
    require(derivation["derivations"] == expected, "Derivation record differs from exact replay")
    initial_path = ROOT / "confirmation-initial-bindings-001" / "index.json"
    initial_raw = frozen(initial_path, "52b412392c5ccebf1bdf363583ceb24b3c889bce9f7a5f29a6b33e0175103eb1")
    initial = json.loads(initial_raw)
    for family in INITIALS:
        spec, refs, derivatives, claims = actual_initial(family)
        saved = initial["initials"][family]
        require(saved["spec"] == spec and saved["refs"] == refs and saved["claims"] == claims,
                "Normalized initial differs")
        require(saved["dispositionIds"] == disposition_ids(frozen(refs["report"]["path"]), claims),
                "A disposition identity was dropped")
        for name, raw in derivatives.items():
            ref = saved["derivatives"][name]
            require(frozen(ref["path"], ref["sha256"]) == raw, "Initial derivative changed")
    executions = []
    for name, tests in EXECUTIONS.items():
        path = ROOT / name
        raw = frozen(path / "receipt.json")
        receipt = json.loads(raw)
        log = frozen(path / "output.log", receipt["logSha256"])
        require(receipt["exitCode"] == receipt["childExitCodeAfterCleanup"] == 0
                and receipt["cleanupError"] is None and receipt["memory"]["breach"] is None
                and receipt["runnerSha256"] == RUNNER_SHA and receipt["guardSha256"] == GUARD_SHA
                and receipt["waitTimeoutSeconds"] == .1 and receipt["cleanupTimeoutSecondsPerStage"] == 10,
                "Failed or incompatible execution: " + name)
        if tests:
            normalized = log.replace(b"\r\n", b"\n")
            require(f"Ran {tests} tests".encode() in normalized and b"\nOK\n" in normalized,
                    "Missing control evidence")
        executions.append({"directory": str(path), "tests": tests, "receiptSha256": sha(raw),
                           "logSha256": sha(log)})
    helpers = [
        "b134_initial_records.py", "test_b134_initial_records.py", "prepare_b134_confirmation_engine.py",
        "test_b134_confirmation_engine.py", "verify_b134_confirmation_preparation.py",
    ]
    result = {
        "batch": 134, "status": "PREPARATION_VERIFIED_NOT_ADMITTED",
        "derivation": {"path": str(OUT / "derivation.json"), "sha256": sha(derivation_raw)},
        "initialBindings": {"path": str(initial_path), "sha256": sha(initial_raw)},
        "tools": [{"path": str(TOOLS / name), "sha256": sha(frozen(TOOLS / name))} for name in helpers],
        "executions": executions, "tests": sum(EXECUTIONS.values()),
        "originalDispositionCounts": {family: len(item["dispositionIds"])
                                      for family, item in initial["initials"].items()},
        "limits": [
            "Original initial records and reports preserved; normalized identities are not new verdicts.",
            "No actual signed reconciliation source dossier, confirmation build, admission or reviewer execution.",
            "Synthetic controls and real initial-binding verification do not establish teaching correctness.",
            "The original author remains the only content writer; no teaching, publication or delivery credit.",
        ],
    }
    print(json.dumps(freeze_json(OUT / "preparation-verification.json", result)))


if __name__ == "__main__":
    main()

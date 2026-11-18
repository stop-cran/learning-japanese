"""Verify execution receipts for the exact B129 reconciliation snapshot."""
import json
from pathlib import Path

from common import GUARD_SHA, WS, frozen, load_module, require, sha
from verify_b129_evidence_v2 import ORDER, verify_execution
from verify_b129_payload import LINK_HELPER, LINK_HELPER_SHA, MEMBERS
from verify_b129_revision_runtime import BASE, PARENT, REPO

HERE = WS / "scratch-129" / "reconciliation-001"
FILES = {"admission.json", "summary.json",
         *(f"{name}.{suffix}" for name in ORDER for suffix in ("json", "log"))}
EXECUTION_HELPER_SHA = "f19d587797ef3574e35498aa57b12e5939d9f7f7b74feb6670d60c8af4323d02"


def memory_ok(value):
    return (value["breach"] is None
            and value["freeRamBeforeBytes"] > 2 * 1024 ** 3
            and value["minimumObservedFreeRamBytes"] >= 1024 ** 3
            and value["abortThresholdBytes"] == 1024 ** 3
            and value["samplingIntervalSeconds"] == 0.25)


def commands():
    lean = WS / "lean"
    return {
        "lint": [lean / "n1_batch_tool.py", "lint", "--base", BASE, "--no-jmdict", *MEMBERS],
        "quiz-safety": [lean / "quiz_safety.py", *MEMBERS],
        "linkplan": [lean / "n1_linkplan.py", "verify", BASE, *MEMBERS],
        "reading-exposure": [HERE / "check_reading.py"],
        "validate": [REPO / "tools" / "validate.py"],
        "manifest": [REPO / "tools" / "build_manifest.py"],
        "unittest": ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"],
        "budget": [REPO / "tools" / "check_content_budget.py"],
        "vocabulary": [REPO / "tools" / "grammar_vocabulary.py", "check"],
        "manifest-rebuild": [REPO / "tools" / "build_manifest.py"],
    }


def check_context(summary, admission, mode, candidate, manifest_sha, runner_sha, common_sha):
    require(mode in {"author", "committed"}, "Unknown gate mode")
    head = PARENT if mode == "author" else candidate
    require(summary["batch"] == "129-reconciliation-001" and summary["mode"] == mode
            and summary["status"] == "PASS" and summary["batchScopeBase"] == BASE
            and summary["requiredCommitParent"] == PARENT and summary["startingHead"] == head
            and summary["checks"] == list(ORDER) and summary["serial"] is True
            and summary["manifestSha256"] == manifest_sha
            and summary["runnerSha256"] == runner_sha
            and summary["commonHelperSha256"] == common_sha
            and summary["guardSha256"] == GUARD_SHA
            and summary["waitTimeoutSeconds"] == 0.1
            and summary["cleanupTimeoutSecondsPerStage"] == 10
            and set(summary["logs"]) == set(ORDER)
            and memory_ok(summary["finalMemory"]), "Gate summary context differs")
    require(admission["head"] == head and admission["mode"] == mode
            and admission["batchScopeBase"] == BASE and admission["commitParent"] == PARENT
            and admission["manifestBeforeSha256"] == manifest_sha
            and memory_ok(admission["memory"]), "Gate admission context differs")


def verify(directory, mode, candidate, manifest_sha, runner_sha, common_sha, recon_sha, guard):
    directory = Path(directory).resolve()
    require(directory.parent == HERE and directory.is_dir(), "Unexpected gate directory")
    require({path.name for path in directory.iterdir()} == FILES, "Incomplete gate file set")
    frozen(Path(__file__).with_name("verify_b129_evidence_v2.py"), EXECUTION_HELPER_SHA)
    frozen(LINK_HELPER, LINK_HELPER_SHA)
    helper = load_module("b129_revision_gate_bindings", LINK_HELPER)
    captured = {name: (directory / name).read_bytes() for name in FILES}
    summary, admission = (json.loads(captured[name]) for name in ("summary.json", "admission.json"))
    check_context(summary, admission, mode, candidate, manifest_sha, runner_sha, common_sha)
    bindings = helper.gate_bindings(directory, {"repo": str(REPO)}, manifest_sha, runner_sha, guard)
    receipts = {}
    for row in bindings:
        name = row["gate"]
        receipt_raw, log = captured[name + ".json"], captured[name + ".log"]
        require(row["receiptSha256"] == summary["logs"][name]["receiptSha256"] == sha(receipt_raw)
                and row["logSha256"] == summary["logs"][name]["logSha256"] == sha(log),
                f"Gate evidence changed: {name}")
        receipt = json.loads(receipt_raw)
        require(receipt["reconciliationHelperSha256"] == recon_sha
                and receipt["cleanupScope"] == "Own immediate child PID only."
                and memory_ok(receipt["memory"]), f"Reconciliation gate helper differs: {name}")
        receipts[name] = receipt
    verify_execution(receipts, commands(), common_sha)
    require(all((directory / name).read_bytes() == raw for name, raw in captured.items()),
            "Gate files changed during verification")
    return {
        "mode": mode, "directory": str(directory), "summarySha256": sha(captured["summary.json"]),
        "admissionSha256": sha(captured["admission.json"]), "gates": bindings,
        "firstStartedAt": receipts[ORDER[0]]["startedAt"],
        "lastCompletedAt": receipts[ORDER[-1]]["completedAt"],
        "files": {name: sha(raw) for name, raw in sorted(captured.items())},
        "limits": "Bound execution evidence only; not semantic, native/device or publication acceptance.",
    }, captured

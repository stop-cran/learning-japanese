"""Verify B130 reconciliation's wrapper and unchanged ten-gate implementation."""
import json
from pathlib import Path

from common import GUARD_SHA, WS, frozen, load_module, require, sha
from b129_revision_gates import memory_ok
from verify_b129_evidence_v2 import ORDER, verify_execution
from verify_b130_payload import BASE, LINK_HELPER, LINK_HELPER_SHA, MEMBERS, REPO
from verify_b130_revision_runtime_v2 import PARENT

HERE = WS / "scratch-130"
FILES = {"admission.json", "summary.json",
         *(f"{name}.{suffix}" for name in ORDER for suffix in ("json", "log"))}
HELPERS = {
    "b129_revision_gates.py": "4e4b638c43d6f7a1d928208a0d09fe31e06e22d7d1c0091af6aff1ed6e3e2e25",
    "verify_b129_evidence_v2.py": "f19d587797ef3574e35498aa57b12e5939d9f7f7b74feb6670d60c8af4323d02",
}


def commands():
    lean = WS / "lean"
    return {
        "lint": [lean / "n1_batch_tool.py", "lint", "--base", BASE, "--no-jmdict", *MEMBERS],
        "quiz-safety": [lean / "quiz_safety.py", *MEMBERS],
        "linkplan": [lean / "n1_linkplan.py", "verify", BASE, *MEMBERS],
        "reading-exposure": [HERE / "check_reading_b130.py"],
        "validate": [REPO / "tools" / "validate.py"],
        "manifest": [REPO / "tools" / "build_manifest.py"],
        "unittest": ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"],
        "budget": [REPO / "tools" / "check_content_budget.py"],
        "vocabulary": [REPO / "tools" / "grammar_vocabulary.py", "check"],
        "manifest-rebuild": [REPO / "tools" / "build_manifest.py"],
    }


def check_context(summary, admission, mode, candidate, manifest_sha,
                  wrapper_sha, implementation_sha, common_sha):
    require(mode in ("author", "committed"), "Unknown gate mode")
    head = PARENT if mode == "author" else candidate
    require(summary["batch"] == 130 and summary["revision"] == "reconciliation-001"
            and summary["mode"] == mode and summary["status"] == "PASS"
            and summary["parent"] == PARENT and summary["publishedBase"] == BASE
            and summary["startingHead"] == head and summary["checks"] == list(ORDER)
            and summary["serial"] is True and summary["manifestSha256"] == manifest_sha
            and summary["runnerSha256"] == wrapper_sha
            and summary["gateImplementationSha256"] == implementation_sha
            and summary["commonHelperSha256"] == common_sha
            and summary["guardSha256"] == GUARD_SHA
            and summary["waitTimeoutSeconds"] == 0.1
            and summary["cleanupTimeoutSecondsPerStage"] == 10
            and set(summary["logs"]) == set(ORDER)
            and memory_ok(summary["finalMemory"]), "Gate summary context differs")
    require(admission["head"] == head and admission["mode"] == mode
            and admission["parent"] == PARENT and memory_ok(admission["memory"]),
            "Gate admission context differs")


def verify(directory, mode, candidate, manifest_sha, wrapper_sha, implementation_sha, common_sha, guard):
    directory = Path(directory).resolve()
    require(directory.parent == HERE and directory.is_dir(), "Unexpected gate directory")
    require({path.name for path in directory.iterdir()} == FILES, "Incomplete gate file set")
    for name, digest in HELPERS.items():
        frozen(Path(__file__).with_name(name), digest)
    frozen(LINK_HELPER, LINK_HELPER_SHA)
    helper = load_module("b130_revision_gate_bindings", LINK_HELPER)
    captured = {name: (directory / name).read_bytes() for name in FILES}
    summary, admission = (json.loads(captured[name]) for name in ("summary.json", "admission.json"))
    check_context(summary, admission, mode, candidate, manifest_sha,
                  wrapper_sha, implementation_sha, common_sha)
    bindings = helper.gate_bindings(directory, {"repo": str(REPO)}, manifest_sha, implementation_sha, guard)
    receipts = {}
    for row in bindings:
        name = row["gate"]
        receipt_raw, log = captured[name + ".json"], captured[name + ".log"]
        require(row["receiptSha256"] == summary["logs"][name]["receiptSha256"] == sha(receipt_raw)
                and row["logSha256"] == summary["logs"][name]["logSha256"] == sha(log),
                "Gate evidence changed: " + name)
        receipt = json.loads(receipt_raw)
        require(receipt["cleanupScope"] == "Own immediate child PID only."
                and memory_ok(receipt["memory"]), "Gate memory or cleanup scope differs")
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
        "limits": "Exact host execution receipts, separate wrapper/implementation identities and "
                  "published-base commands only. Log-content/source semantics, signed tree equality "
                  "and acceptance remain separate requirements.",
    }, captured

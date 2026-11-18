"""Verify the frozen integration bundle and exact original gate execution evidence."""
import json
import re
from pathlib import Path

from b129_revision_gates import memory_ok
from b130_delta_gates import commands
from common import WS, freeze_json, frozen, load_module, require, sha, start_guard
from verify_b129_evidence_v2 import ORDER, verify_execution
from verify_b130_integration_runtime import BASE, CLOSURE, INCOMING, ROOT
from verify_b130_payload import LINK_HELPER, LINK_HELPER_SHA, REPO

CANDIDATE = "37a53e75446bacad8ade4e212404b121d4a01af1"
TREE = "aefcaa2d5acf213f4614eff97854fcc17fb5c2b6"
MANIFEST = "23583ae2a885bd67212f8a541415a08bd6411c05763e1813bbd13145a7399495"
AUTHOR = WS / "scratch-130" / "integration-001-author"
BUNDLE = AUTHOR / "handoff-001"
IMPLEMENTATION = "9d9d302e713c4ac14563caaf83f71f0036e51b97fdd4817f7c2c5e81aeb6465c"
COMMON = "7809e589e7ac8691e9e3081f40f33eed329bce10c10c6696f03fd03486dde530"
ENVELOPE = "5222576aa9baed02616ebf944176fe74fa23656054ef5b7f4a8fe4f382117c88"
INTEGRATION = "f51ae2f730eaa28daa712a33d3eb077ebbf09411ff8cb87a32f2c5f8cd31c269"


def check_context(summary, admission, mode):
    head = CLOSURE if mode == "author" else CANDIDATE
    require(mode in ("author", "committed") and summary["status"] == "PASS"
            and summary["mode"] == admission["mode"] == mode
            and summary["head"] == admission["head"] == head
            and summary["tree"] == admission["tree"] == TREE
            and summary["parentsInOrder"] == admission["parents"] == [CLOSURE, INCOMING]
            and summary["publishedBaseScope"] == BASE and summary["checks"] == list(ORDER)
            and summary["commandsUnchanged"] is True and summary["serial"] is True
            and summary["manifestSha256"] == MANIFEST
            and summary["runnerSha256"] == ENVELOPE
            and summary["gateImplementationSha256"] == IMPLEMENTATION
            and summary["commonHelperSha256"] == COMMON
            and summary["integrationHelperSha256"] == INTEGRATION
            and set(summary["logs"]) == set(ORDER)
            and memory_ok(admission["memory"]) and memory_ok(summary["finalMemory"]),
            "Integration gate context differs")


def main():
    handoff_raw = frozen(BUNDLE / "handoff.json",
                         "b58ec4ef527005d930674b9d47ed461feadba86aa8b4ae9d739ba3173df8383d")
    inventory_raw = frozen(BUNDLE / "evidence-inventory.json",
                           "7cf235af7db00e154c518928581ecf4ac056afcf7785c0e7df1d6075cbd77f32")
    handoff, inventory = json.loads(handoff_raw), json.loads(inventory_raw)
    runtime_path = ROOT / "integration-runtime-001" / "verification.json"
    runtime_raw = frozen(runtime_path, "5a8aacbd6e0303acc9794a1689f4f329b9b4f4a556b9a91f94f24af1db31a08a")
    runtime = json.loads(runtime_raw)
    require(runtime["status"] == "PASS_INTEGRATION_RUNTIME_ONLY" and runtime["candidate"] == CANDIDATE
            and runtime["manifestSha256"] == MANIFEST and not runtime["reviewAccepted"]
            and not runtime["publicationAccepted"] and memory_ok(runtime["memory"]),
            "Independent runtime proof differs")
    require(handoff["candidate"] == CANDIDATE and handoff["parentsInOrder"] == [CLOSURE, INCOMING]
            and handoff["tree"] == TREE and handoff["clean"] and handoff["manifestSha256"] == MANIFEST
            and handoff["contentVersion"] == runtime["contentVersion"] == "3df59f6cf1dee0f2"
            and handoff["accounting"] == {"publishedDelivered": 261, "frozenTotal": 1228,
                                         "undelivered": 967, "localUnpublishedDrafts": 3, "deliveryCredit": 0},
            "Handoff describes another candidate or advances accounting")
    frozen(LINK_HELPER, LINK_HELPER_SHA)
    helper = load_module("b130_integration_gate_receipts", LINK_HELPER)
    guard, _ = start_guard("B130 integration evidence verification")
    gate_sets = {}
    try:
        require(inventory["selfExcluded"] is True and len(inventory["files"]) == 101
                and {p.relative_to(BUNDLE).as_posix() for p in BUNDLE.rglob("*") if p.is_file()}
                == set(inventory["files"]) | {"evidence-inventory.json"}, "Incomplete integration bundle")
        for name, digest in inventory["files"].items():
            path = BUNDLE / name
            require(path.resolve().is_relative_to(BUNDLE) and not Path(name).is_absolute(),
                    "Bundle path escapes its root")
            frozen(path, digest)
            guard.check()
        for name, binding in handoff["receiptBindings"].items():
            require(Path(binding["originalDirectory"]) == AUTHOR / name
                    and binding["bundledDirectory"] == f"evidence/{name}", "Receipt location differs")
            for relative, digest in binding["files"].items():
                frozen(BUNDLE / "evidence" / name / relative, digest)
                require(sha((AUTHOR / name / relative).read_bytes()) == digest, "Original receipt changed")
        require(sha(frozen(BUNDLE / "tooling/original/run_b130_gates.py")) == IMPLEMENTATION
                and sha(frozen(BUNDLE / "tooling/original/b130_common.py")) == COMMON
                and sha(frozen(BUNDLE / "tooling/run_integration_gates.py")) == ENVELOPE
                and sha(frozen(BUNDLE / "tooling/integration_common.py")) == INTEGRATION,
                "Gate producer binding differs")
        prior = json.loads(frozen(ROOT / "delta-evidence-001" / "verification.json",
                                  "0288e16198420c4e8b8b14a109ce6af2ac7cf4b8572468639b923aa59affa5a9"))
        warnings = prior["retainedQuizSafetyWarnings"]
        require(len(warnings) == 83 and handoff["nonfatalNotesMentionWarnings"] == warnings,
                "Retained warnings changed")
        for mode in ("author", "committed"):
            directory = BUNDLE / "evidence" / f"{mode}-gates-001"
            summary_raw = frozen(directory / "summary.json")
            summary = json.loads(summary_raw)
            admission = json.loads(frozen(directory / "admission.json"))
            check_context(summary, admission, mode)
            rows = helper.gate_bindings(directory, {"repo": str(REPO)}, MANIFEST, IMPLEMENTATION, guard)
            receipts = {}
            for row in rows:
                name = row["gate"]
                require(summary["logs"][name] == {key: row[key] for key in ("receiptSha256", "logSha256")},
                        "Summary/actual receipt mismatch")
                receipt = json.loads(frozen(directory / f"{name}.json", row["receiptSha256"]))
                require(receipt["cleanupScope"] == "Own immediate child PID only."
                        and memory_ok(receipt["memory"]), "Cleanup/resource scope changed")
                receipts[name] = receipt
            verify_execution(receipts, commands(), COMMON)
            quiz_log = frozen(directory / "quiz-safety.log").decode().replace("\r\n", "\n")
            require([line for line in quiz_log.splitlines() if line.startswith("WARN  ")] == warnings,
                    "Actual quiz-warning output differs")
            tests = frozen(directory / "unittest.log").decode().replace("\r\n", "\n")
            require(re.search(r"Ran 431 tests in [^\n]+\n\nOK(?:\n|$)", tests), "Actual431-test output absent")
            gate_sets[mode] = {
                "summarySha256": sha(summary_raw), "gates": rows,
                "firstStartedAt": receipts[ORDER[0]]["startedAt"],
                "lastCompletedAt": receipts[ORDER[-1]]["completedAt"],
            }
            preserved = json.loads(frozen(BUNDLE / "evidence" / f"{mode}-preserve-001" / "summary.json"))
            require(preserved["status"] == "PASS" and preserved["mode"] == mode
                    and preserved["head"] == (CLOSURE if mode == "author" else CANDIDATE)
                    and preserved["tree"] == TREE and preserved["parentsInOrder"] == [CLOSURE, INCOMING]
                    and preserved["trackedBlobsCompared"] == runtime["trackedPaths"] == 40297
                    and preserved["allOtherTrackedBlobsAndModesUnchanged"] == 40294
                    and preserved["runtimeEntries"] == 8730 and preserved["otherRuntimeEntriesHashEqual"] == 8728
                    and preserved["changedRuntimePaths"] == runtime["runtimeChanged"]
                    and preserved["manifestSha256"] == MANIFEST
                    and preserved["noN1ContentSupportSourceReviewProgressNotesOrOtherTrackedChanges"] is True,
                    "Author preservation contradicts independent signed-tree proof")
        require(gate_sets["author"]["lastCompletedAt"] <= gate_sets["committed"]["firstStartedAt"],
                "Pre-sign and committed gate executions overlap")
        for path in (BUNDLE / "evidence").glob("*/memory.json"):
            require(memory_ok(json.loads(frozen(path))), "Other integration operation breached RAM")
        require(memory_ok(json.loads(frozen(BUNDLE / "memory.json"))), "Handoff collection breached RAM")
        for name, expected_exit in (("merge-001", 1), ("signing-001", 0)):
            directory = BUNDLE / "evidence" / name
            receipt = json.loads(frozen(directory / "command.json"))
            require(receipt["exitCode"] == expected_exit and receipt["timedOut"] is False
                    and receipt["childWaitSeconds"] == 0.1 and receipt["cleanupTimeoutSecondsPerStage"] == 10
                    and sha(frozen(directory / "stdout.log")) == receipt["stdoutSha256"]
                    and sha(frozen(directory / "stderr.log")) == receipt["stderrSha256"],
                    "Merge/signing receipt differs")
        require(handoff["mergeResolution"]["expectedConflictOnly"] == ["manifest.json"]
                and handoff["mergeResolution"]["attributeAdjustments"] == [], "Unexpected merge intervention")
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Integration evidence RAM breach")
    result = {
        "status": "PASS_INTEGRATION_BINDINGS_ONLY", "batch": 130, "candidate": CANDIDATE,
        "parents": [CLOSURE, INCOMING], "manifestSha256": MANIFEST, "contentVersion": "3df59f6cf1dee0f2",
        "runtimeProof": {"path": str(runtime_path), "sha256": sha(runtime_raw)},
        "authorHandoffSha256": sha(handoff_raw), "bundleInventorySha256": sha(inventory_raw),
        "bundleFilesVerified": 101, "gateSets": gate_sets, "actualTestsPerGateSet": 431,
        "retainedQuizSafetyWarnings": warnings, "memory": memory,
        "reviewAccepted": False, "publicationAccepted": False,
        "limits": "Mechanical bindings, actual unchanged host commands and receipts only. All earlier "
                  "lexical/image/unread-index/latent-reading/native/device/font/old-APK limits remain. "
                  "No inherited counter-language approval, integrated confirmation or delivery credit. "
                  "Do not give a reviewer the combined handoff/inventory/producers; use selected neutral "
                  "evidence and only that recipient's own prior report/response/mapping.",
        "producerSha256": sha(frozen(Path(__file__))),
    }
    print(json.dumps(freeze_json(ROOT / "integration-evidence-001.json", result)))


if __name__ == "__main__":
    main()

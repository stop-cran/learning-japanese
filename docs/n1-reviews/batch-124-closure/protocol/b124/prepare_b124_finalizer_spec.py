"""Bind B124 closure support, retaining failed runs without relabeling them."""
import json
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha
from finalize_b124 import RUNTIME_PROOF_SHA, check_history

REVIEW = WS / "scratch-124" / "review"
CANDIDATE = "beba46248ea0da6faa1c34b64f5c700565be5b23"
DOCUMENTATION_SHA = "cbd96e89ff2b970672eca3b8316f970b80fe9692f3c396d689950a1340ead591"


def main(archive_path):
    from common import load_batch

    config = load_batch(124)
    provenance_path = Path(config["repo"]) / "docs" / "n1-reviews" / "batch-124-closure" / "provenance.json"
    provenance_raw = frozen(provenance_path)
    check_history(json.loads(provenance_raw), CANDIDATE, config)
    archive_raw = frozen(archive_path)
    archive = json.loads(archive_raw)
    require(archive["status"] == "PASS" and archive["candidate"] == CANDIDATE
            and archive["provenanceSha256"] == sha(provenance_raw) and len(archive["chains"]) == 8,
            "Actual six-run archive has not passed")
    supporting = []

    def add(path, name):
        raw = frozen(path)
        require(name not in {item["archivePath"] for item in supporting}, "Duplicate support path")
        supporting.append({"path": str(path), "sha256": sha(raw), "archivePath": name})

    for name in (
        "source-contract.json", "source-selection-verification-001.json",
        "coordinator-candidate-verification.json", "coordinator-evidence-freeze-001.json",
        "coordinator-review-evidence-freeze-002.json", "reconciliation-001-source-adjudication.json",
        "reconciliation-handoff-capture-001.json", "reconciliation-001-author-admission.json",
        "reconciliation-002-author-admission.json", "response-correction-001-admission.json",
        "reconciliation-002-confirmation-preparation.json",
        "prepared-chain-retention-verification-001.json",
        "prepared-chain-retention-verification-002.json", "closure-spec-001.json",
    ):
        add(REVIEW / name, "verification/coordinator/" + name)
    add(REVIEW / "confirm" / "N1-B124-CLAUDE-CONFIRM-001-adjudication-preliminary-001.json",
        "verification/coordinator/claude-first-confirmation-preliminary.json")
    for family in ("CLAUDE", "GPT"):
        name = f"N1-B124-{family}-CONFIRM-002-scoped-identity.json"
        add(REVIEW / "confirm" / name, "verification/coordinator/" + name)
    for name in ("reconciliation-001-handoff.json", "reconciliation-002-handoff.json",
                 "response-correction-001-handoff.json"):
        add(REVIEW.parent / name, "verification/author/" + name)
    for directory in ("reconciliation-001-neutral", "reconciliation-002-neutral"):
        for path in sorted((REVIEW / directory).iterdir()):
            require(path.is_file() and path.suffix in (".json", ".md"), "Unexpected neutral evidence")
            add(path, f"verification/{directory}/{path.name}")
    captures = []
    for directory in sorted(REVIEW.iterdir()):
        receipt_path = directory / "receipt.json"
        if not directory.is_dir() or not receipt_path.exists():
            continue
        receipt_raw = receipt_path.read_bytes()
        receipt = json.loads(receipt_raw)
        log_path = directory / "output.log"
        log_raw = log_path.read_bytes()
        require(receipt["exitCode"] is not None
                and receipt["exitCode"] == receipt["childExitCodeAfterCleanup"]
                and receipt["logSha256"] == sha(log_raw)
                and receipt["waitTimeoutSeconds"] == 0.1
                and receipt["memory"]["breach"] is None
                and receipt["memory"]["minimumObservedFreeRamBytes"] >= 1024 ** 3,
                f"Incomplete or inconsistent completed run: {directory}")
        for path, raw in ((receipt_path, receipt_raw), (log_path, log_raw)):
            path.chmod(0o444)
            require(frozen(path, sha(raw)) == raw, "Post-run capture changed bytes")
            add(path, f"verification/execution/{directory.name}/{path.name}")
        captures.append({"directory": directory.name, "exitCode": receipt["exitCode"],
                         "receiptSha256": sha(receipt_raw), "logSha256": sha(log_raw)})
    for name in (
        "finalize_b124.py", "test_finalize_b124.py", "prepare_b124_finalizer_spec.py",
        "verify_b124_reconciliation.py", "test_verify_b124_reconciliation.py",
        "verify_b124_reconciliation_002.py", "test_verify_b124_reconciliation_002.py",
        "verify_b124_response_correction.py", "test_verify_b124_response_correction.py",
        "prepare_b124_confirmations.py", "prepare_b124_confirmations_002.py",
        "test_prepare_b124_confirmations_002.py", "prepare_b124_confirmation_test_recovery.py",
        "scoped_confirmation_admission.py", "check_confirmation_identity.py",
        "prepare_b124_publication_tools.py",
    ):
        add(Path(__file__).parent / name, "protocol/b124/" + name)
    add(REVIEW.parent / "run-checks-closure-001.py", "protocol/b124/run-checks-closure-001.py")
    capture_path = REVIEW / "closure-support-capture-001.json"
    freeze_json(capture_path, {
        "candidate": CANDIDATE, "completedRuns": captures,
        "limits": "ReadOnly capture after execution; failed exit codes remain failed. "
                  "No claim that these outer receipts were immutable while running. "
                  "Raw event streams, complete external captures and unrelated-session status stay local.",
    })
    add(capture_path, "verification/coordinator/closure-support-capture-001.json")
    runtime_path = REVIEW / "coordinator-reconciliation-verification-002.json"
    doc_path = REVIEW / "coordinator-response-correction-verification-001.json"
    frozen(runtime_path, RUNTIME_PROOF_SHA)
    frozen(doc_path, DOCUMENTATION_SHA)
    print(json.dumps(freeze_json(REVIEW / "finalizer-spec-001.json", {
        "candidate": CANDIDATE,
        "verification": {"path": str(runtime_path), "sha256": RUNTIME_PROOF_SHA},
        "documentationVerification": {"path": str(doc_path), "sha256": DOCUMENTATION_SHA},
        "archiveVerification": {"path": str(archive_path), "sha256": sha(archive_raw)},
        "supportingArtifacts": supporting,
    })))


if __name__ == "__main__":
    main(Path(sys.argv[1]))

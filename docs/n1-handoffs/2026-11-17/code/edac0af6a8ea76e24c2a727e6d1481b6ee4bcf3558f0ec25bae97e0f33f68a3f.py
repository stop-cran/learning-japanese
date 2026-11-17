"""Persist B122 closure only after both original reviewers confirm its exact revision.

Adapted from finalize_b121_v2.py, SHA-256
f8370a3cb911f16b12135b78a2875517e656c3dee365b3475e321faecfe5abed.
"""
import json
import sys
from pathlib import Path

from common import CHECKS, WS, freeze_json, frozen, git, json_bytes, load_batch, require, sha, start_guard, write_frozen
from verify_b122_revision_v2 import SIGNER, check_gate

INITIALS = {"claude": "N1-B122-CLAUDE-001", "gpt": "N1-B122-GPT-001"}
VERDICTS = {"claude": "CLEAN", "gpt": "NEEDS FIX"}
PROOF_SHA = "ff04d8bd487315f769a572c75e0fbeafa50f3aaf76b18408c2fe96b84c16214a"
SELECTION_SHA = "164e412f4397d9e95e1cfd83968c4f1e09382fc30e0f5ec66fc0557605224dd9"


def check_closure(provenance, proof, candidate, config):
    require(provenance["reviewedSnapshot"] == candidate
            and provenance["initialSnapshot"] == config["candidate"]
            and provenance["base"] == config["base"] and provenance["publication"] == "PENDING"
            and provenance["members"] == config["members"] == ["\u60a0"],
            "Closure snapshot, scope or publication state differs")
    lineage = provenance["reviewLineage"]
    initials = [item for item in lineage if item["role"] == "initial"]
    finals = [item for item in lineage if item["finalAcceptance"]]
    require(len(lineage) == 4 and len(initials) == len(finals) == 2
            and {item["run"] for item in initials} == set(INITIALS.values())
            and {item["family"] for item in finals} == {"claude", "gpt"}
            and len(provenance["finalRuns"]) == 2
            and set(provenance["finalRuns"]) == {item["run"] for item in finals}
            and not provenance["excludedInitialRuns"] and not provenance["intermediateRuns"],
            "Expected two valid initials and two first original-reviewer confirmations")
    for family, initial in INITIALS.items():
        first = next(item for item in initials if item["run"] == initial)
        last = next(item for item in finals if item["family"] == family)
        require(first["family"] == family and first["snapshot"] == config["candidate"]
                and not first["finalAcceptance"] and first["rawVerdict"] == VERDICTS[family]
                and last["run"] == f"{initial}-CONFIRM-001" and last["role"] == "final"
                and last["session"] == first["session"] and last["snapshot"] == candidate
                and last["rawVerdict"] == "CONFIRMED" and last["confirmationAcceptedOnSnapshot"]
                and last["priorRun"] is None, "Confirmation changed reviewer, verdict or lineage")
    require(proof["status"] == "PASS" and proof["candidate"] == candidate
            and proof["initial"] == config["candidate"] and proof["base"] == config["base"]
            and proof["baselineRuntimePreservedExceptRequiredWrappers"]
            and proof["originalMetadataStrokesGuardsAndSourceReceiptsPreserved"]
            and proof["sourceMembersPublishedBeforeBatch"] == 251
            and proof["sourceMembersInCandidate"] == 252 and proof["runtimeEntries"] == 8706
            and proof["linguisticAcceptance"] is False and proof["publicationAccepted"] is False
            and not proof["memory"]["breach"], "Revision verification differs")
    require([item["gate"] for item in proof["gates"]] == list(CHECKS), "Incomplete gate set")


def make_ledger(config, candidate, provenance, provenance_sha, proof):
    return {
        "schemaVersion": 1, "batch": "122", "baseCommit": config["base"],
        "initialSnapshot": config["candidate"], "reviewedSnapshot": candidate,
        "membership": ["\u60a0"], "sourceRows": [367],
        "status": "textual-review-closed-publication-pending",
        "drafted": ["\u60a0"], "reviewClosed": ["\u60a0"], "published": [], "runtimePublished": False,
        "accounting": {"frozenPendingRecords": 1228, "publishedPendingRecordsWithCards": 251,
                       "reviewClosedPendingRecordsWithCards": 252, "n2Placements": 6,
                       "publishedN1Additions": 245, "undelivered": 977, "notStarted": 976,
                       "overallN1TaskComplete": False},
        "declaringWords": {"\u60a0": ["\u60a0\u3005"]}, "requiredLinkPairs": 1, "newWordArticles": 0,
        "runtimeCandidate": {"contentVersion": proof["contentVersion"],
                             "manifestSha256": proof["manifestSha256"],
                             "runtimeEntries": proof["runtimeEntries"]},
        "review": {"status": "closed-with-disclosed-limits", "finalRuns": provenance["finalRuns"],
                   "closure": "../n1-reviews/batch-122-closure/provenance.json",
                   "closureProvenanceSha256": provenance_sha, "remainingActionableFindings": [],
                   "remainingConsequentialClaims": [], "historicalReportsPreserved": True,
                   "excludedInitialRuns": [],
                   "identity": "Independent Claude001 CLEAN and GPT001 NEEDS FIX initials, "
                               "source-based reconciliation and serial confirmations by both original reviewers."},
        "sourceEvidence": {"initial": "batch-122/source-receipt.json",
                           "reconciliation": "batch-122-reconciliation/",
                           "signedArtifactSha256": proof["sourceProof"]["signedArtifacts"]},
        "limits": [
            "Bounded textual and host review, not exhaustive linguistic or arbitrary-pool acceptance.",
            "No new Kotlin, native, phone, installed-APK or fallback-rendering acceptance.",
            "Publication, CI and exact served ZIP remain pending; review closure is not delivery.",
            "Original reports, optional judgments, source qualifications and failed preparation evidence remain preserved.",
        ],
    }


def finalize(candidate, gates, proof_path):
    config = load_batch(122)
    repo, records = Path(config["repo"]), WS / "scratch-122" / "review"
    closure = repo / "docs" / "n1-reviews" / "batch-122-closure"
    provenance_raw, proof_raw = frozen(closure / "provenance.json"), frozen(proof_path, PROOF_SHA)
    provenance, proof = json.loads(provenance_raw), json.loads(proof_raw)
    check_closure(provenance, proof, candidate, config)
    selection_raw = frozen(records / "coordinator-reconciliation-selection-001.json", SELECTION_SHA)
    selection = json.loads(selection_raw)
    require(selection["candidate"] == candidate and selection["status"] == "PASS", "Selection proof differs")
    require(git(config, "rev-parse", "HEAD").decode().strip() == candidate
            and git(config, "show", "-s", "--format=%G?|%GF|%ae|%ce", candidate).decode().strip()
            == f"G|{SIGNER}|stop-cran@list.ru|stop-cran@list.ru", "Signed revision changed")
    require(not git(config, "diff", "--name-only") and not git(config, "diff", "--cached", "--name-only"),
            "Tracked revision changed")
    untracked = git(config, "ls-files", "--others", "--exclude-standard", "-z").decode("utf-8").split("\0")
    require(all(not path or path.startswith("docs/n1-reviews/batch-122-closure/") for path in untracked),
            "Unrelated untracked files")
    ledger_path = repo / "docs" / "n1-sources" / "batch-122-progress.json"
    previous = git(config, "show", f"{candidate}:docs/n1-sources/batch-122-progress.json")
    require(ledger_path.read_bytes() == previous, "Draft progress ledger changed")
    old = json.loads(previous)
    require(old["status"] == "local-candidate-awaiting-independent-review" and not old["published"]
            and old["runtimePublished"] is False and old["membership"] == config["members"]
            and old["accounting"]["publishedPendingRecordsWithCards"] == 251,
            "Unexpected prior progress state")
    guard, _ = start_guard("B122 closure validation")
    try:
        for path, digest in provenance["recordedFileSha256"].items():
            frozen(closure / path, digest)
            guard.check()
        require(sha(git(config, "show", f"{candidate}:manifest.json")) == proof["manifestSha256"],
                "Confirmed manifest changed")
        for path, digest in proof["sourceProof"]["signedArtifacts"].items():
            require(sha(git(config, "show", f"{candidate}:{path}")) == digest, f"Signed source changed: {path}")
            guard.check()
        artifacts = {
            "verification/reconciliation-002.json": proof_raw,
            "verification/reconciliation-selection-001.json": selection_raw,
            "verification/original-progress.json": previous,
        }
        summary = proof["gateSummary"]
        require(Path(summary["path"]) == gates / "summary.json", "Gate directory differs")
        artifacts["gates/summary.json"] = frozen(gates / "summary.json", summary["sha256"])
        for item in proof["gates"]:
            name = item["gate"]
            raw, log = frozen(gates / f"{name}.json", item["receiptSha256"]), frozen(gates / f"{name}.log", item["logSha256"])
            check_gate(json.loads(raw), log, name, proof["manifestSha256"], config["repo"])
            artifacts[f"gates/{name}.json"], artifacts[f"gates/{name}.log"] = raw, log
            guard.check()
        for name in ("coordinator-candidate-verification.json", "source-contract.json",
                     "source-selection-verification-001.json", "revision-verifier-derivation.json",
                     "revision-verifier-v2-derivation.json", "coordinator-reconciliation-adjudication-001.json",
                     "confirmation-preparation-admission-refused-001.json"):
            artifacts[f"verification/{name}"] = frozen(records / name)
        for directory in ("revision-verifier-v2-tests-001", "reconciliation-verification-001",
                          "reconciliation-verification-002", "reconciliation-selection-001",
                          "confirmation-admission-tests-001", "claude-confirmation-legacy-admission-001",
                          "claude-confirmation-scoped-admission-001", "gpt-confirmation-scoped-admission-001",
                          "claude-confirmation-final-001", "gpt-confirmation-final-001",
                          "claude-confirmation-acceptance-001", "gpt-confirmation-acceptance-001",
                          "closure-finalizer-tests-001", "closure-finalizer-tests-002"):
            for name in ("receipt.json", "output.log"):
                artifacts[f"verification/runs/{directory}/{name}"] = frozen(records / directory / name)
        for name in ("verify_b122_revision.py", "test_verify_b122_revision.py",
                     "test_verify_b122_revision_summary.py", "prepare_b122_revision.py",
                     "verify_b122_revision_v2.py", "test_verify_b122_revision_v2.py",
                     "prepare_b122_revision_v2.py", "verify_reconciliation_sources.py",
                     "verify_b122_reconciliation_selection.py", "prepare_b122_confirmations.py",
                     "scoped_admission.py", "test_scoped_admission.py",
                     "scoped_confirmation_admission.py", "test_scoped_confirmation_admission.py",
                     "finalize_b121_v2.py", "finalize_b122.py", "test_finalize_b122.py",
                     "record_publication.py", "test_record_publication.py"):
            artifacts[f"protocol/tools/{name}"] = frozen(Path(__file__).with_name(name))
        artifacts["protocol/guarded-test-v2.py"] = frozen(records / "guarded-test-v2.py")
        for name, raw in artifacts.items():
            write_frozen(closure / name, raw)
        ledger = make_ledger(config, candidate, provenance, sha(provenance_raw), proof)
        freeze_json(closure / "validation-provenance.json", {
            "batch": 122, "candidate": candidate, "reviewClosureSha256": sha(provenance_raw),
            "recordedFileSha256": {name: sha(raw) for name, raw in artifacts.items()}, "publication": "PENDING",
        })
        require(ledger_path.read_bytes() == previous, "Progress changed during closure")
        ledger_path.chmod(0o644)
        ledger_path.write_bytes(json_bytes(ledger))
        require(ledger_path.read_bytes() == json_bytes(ledger), "Progress readback mismatch")
        ledger_path.chmod(0o444)
        print(json.dumps({"path": str(ledger_path), "sha256": sha(json_bytes(ledger)),
                          "status": ledger["status"], "publicationAccepted": False}))
    finally:
        require(not guard.finish()["breach"], "Closure RAM guard breached")


if __name__ == "__main__":
    finalize(sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]))

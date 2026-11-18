"""Bind B123's two preserved revisions to independently accepted final confirmations."""
import json
import sys
from pathlib import Path

from common import (CHECKS, WS, freeze_json, frozen, git, json_bytes, load_batch,
                    require, sha, start_guard, write_frozen)
from verify_b123_revision_v2 import SIGNER, check_gate
from verify_b123_revision_v3 import PARENT, PRIOR_SHA

INITIALS = {"claude": "N1-B123-CLAUDE-001", "gpt": "N1-B123-GPT-001"}
FINALS = {"claude": "N1-B123-CLAUDE-CONFIRM-002", "gpt": "N1-B123-GPT-CONFIRM-002"}
CANDIDATE = "047970a055903c0337d73823288695938648dd1d"
PROOF_SHA = "c7a9b6721556e4db4d7619d4f677a75957c834c6ce31cc03d40b8ce86ea11713"
SELECTION_SHA = "e6242f59ed47fed5a58a5af2a1260616cea3bdc158fb2f3a84776ae29bf9ae43"
PRIOR_SELECTION_SHA = "25de95031769bf33c53ffe8c9f3a0c9b05d2d0198c90f455797ab611c2b9f742"


def check_closure(provenance, proof, prior, candidate, config):
    require(candidate == CANDIDATE and provenance["reviewedSnapshot"] == candidate
            and provenance["initialSnapshot"] == config["candidate"]
            and provenance["base"] == config["base"] and provenance["publication"] == "PENDING"
            and provenance["members"] == config["members"] == ["\u7bc4"],
            "Closure snapshot, scope or publication state differs")
    lineage = provenance["reviewLineage"]
    initials = [item for item in lineage if item["role"] == "initial"]
    finals = [item for item in lineage if item["finalAcceptance"]]
    require(len(lineage) == 4 and len(initials) == len(finals) == 2
            and {item["run"] for item in initials} == set(INITIALS.values())
            and {item["family"] for item in finals} == {"claude", "gpt"}
            and len(provenance["finalRuns"]) == 2
            and set(provenance["finalRuns"]) == set(FINALS.values())
            and not provenance["excludedInitialRuns"] and not provenance["intermediateRuns"],
            "Expected two valid initials and two original-reviewer confirmations")
    for family, run in INITIALS.items():
        first = next(item for item in initials if item["run"] == run)
        last = next(item for item in finals if item["family"] == family)
        require(first["family"] == family and first["snapshot"] == config["candidate"]
                and not first["finalAcceptance"] and first["rawVerdict"] == "NEEDS FIX"
                and last["run"] == FINALS[family] and last["role"] == "final"
                and last["session"] == first["session"] and last["snapshot"] == candidate
                and last["rawVerdict"] == "CONFIRMED" and last["confirmationAcceptedOnSnapshot"]
                and last["priorRun"] is None, "Confirmation changed reviewer, verdict or lineage")
    require(prior["status"] == proof["status"] == "PASS"
            and prior["candidate"] == proof["parent"] == PARENT
            and proof["candidate"] == candidate
            and prior["initial"] == proof["initial"] == config["candidate"]
            and prior["base"] == proof["base"] == config["base"]
            and proof["priorRevisionProof"]["sha256"] == PRIOR_SHA
            and prior["baselineRuntimePreservedExceptRequiredWrappers"]
            and prior["originalMetadataStrokesGuardsAndSourceReceiptsPreserved"]
            and proof["firstRevisionTeachingAndSourcesPreservedExceptFocusedCardAndManifest"]
            and proof["newGuard"] == "\u666e", "Revision chain or preservation proof differs")
    for item in (prior, proof):
        require(item["sourceMembersPublishedBeforeBatch"] == 252
                and item["sourceMembersInCandidate"] == 253 and item["runtimeEntries"] == 8708
                and item["linguisticAcceptance"] is False and item["publicationAccepted"] is False
                and not item["memory"]["breach"]
                and [gate["gate"] for gate in item["gates"]] == list(CHECKS),
                "Revision accounting, gates or acceptance limits differ")


def make_ledger(config, candidate, provenance, provenance_sha, proof, prior):
    sources = {**prior["sourceProof"]["signedArtifacts"], **proof["sourceProof"]["signedArtifacts"]}
    return {
        "schemaVersion": 1, "batch": "123", "baseCommit": config["base"],
        "initialSnapshot": config["candidate"], "reviewedSnapshot": candidate,
        "membership": ["\u7bc4"], "sourceRows": [810],
        "status": "textual-review-closed-publication-pending",
        "drafted": ["\u7bc4"], "reviewClosed": ["\u7bc4"], "published": [], "runtimePublished": False,
        "accounting": {"frozenPendingRecords": 1228, "publishedPendingRecordsWithCards": 252,
                       "reviewClosedPendingRecordsWithCards": 253, "n2Placements": 6,
                       "publishedN1Additions": 246, "undelivered": 976, "notStarted": 975,
                       "overallN1TaskComplete": False},
        "declaringWords": {"\u7bc4": ["\u7bc4\u56f2"]}, "requiredLinkPairs": 1, "newWordArticles": 0,
        "runtimeCandidate": {"contentVersion": proof["contentVersion"],
                             "manifestSha256": proof["manifestSha256"],
                             "runtimeEntries": proof["runtimeEntries"]},
        "review": {"status": "closed-with-disclosed-limits", "finalRuns": provenance["finalRuns"],
                   "closure": "../n1-reviews/batch-123-closure/provenance.json",
                   "closureProvenanceSha256": provenance_sha, "remainingActionableFindings": [],
                   "remainingConsequentialClaims": [], "historicalReportsPreserved": True,
                   "excludedInitialRuns": [],
                   "identity": "Independent Claude001 and GPT001 NEEDS FIX initials, two signed "
                               "source-based revisions and serial confirmations by the original reviewers."},
        "sourceEvidence": {"initial": "batch-123/source-receipt.json",
                           "reconciliations": ["batch-123/reconciliation-001/",
                                               "batch-123/reconciliation-002/"],
                           "signedArtifactSha256": sources},
        "limits": [
            "Bounded textual and host review, not exhaustive linguistic or arbitrary-pool acceptance.",
            "No new Kotlin, native, phone, installed-APK or fallback-rendering acceptance.",
            "Publication, CI and exact served ZIP remain pending; review closure is not delivery.",
            "Original reports, source qualifications and failed preparation evidence remain preserved.",
        ],
    }


def finalize(candidate):
    config = load_batch(123)
    repo, records = Path(config["repo"]), WS / "scratch-123" / "review"
    closure = repo / "docs" / "n1-reviews" / "batch-123-closure"
    provenance_raw = frozen(closure / "provenance.json")
    provenance = json.loads(provenance_raw)
    proof_raw = frozen(records / "coordinator-reconciliation-verification-002.json", PROOF_SHA)
    prior_raw = frozen(records / "coordinator-reconciliation-verification-001.json", PRIOR_SHA)
    proof, prior = json.loads(proof_raw), json.loads(prior_raw)
    check_closure(provenance, proof, prior, candidate, config)
    require(git(config, "rev-parse", "HEAD").decode().strip() == candidate
            and git(config, "show", "-s", "--format=%G?|%GF|%ae|%ce", candidate).decode().strip()
            == f"G|{SIGNER}|stop-cran@list.ru|stop-cran@list.ru", "Signed revision changed")
    require(not git(config, "diff", "--name-only") and not git(config, "diff", "--cached", "--name-only"),
            "Tracked revision changed")
    untracked = git(config, "ls-files", "--others", "--exclude-standard", "-z").decode("utf-8").split("\0")
    require(all(not p or p.startswith("docs/n1-reviews/batch-123-closure/") for p in untracked),
            "Unrelated untracked files")
    ledger_path = repo / "docs" / "n1-sources" / "batch-123-progress.json"
    previous = git(config, "show", f"{candidate}:docs/n1-sources/batch-123-progress.json")
    old = json.loads(previous)
    require(ledger_path.read_bytes() == previous
            and old["status"] == "authoring-draft-unreviewed-unpublished"
            and not old["published"] and not old["reviewClosed"] and old["runtimePublished"] is False
            and old["membership"] == config["members"]
            and old["accounting"]["publishedPendingRecordsWithCards"] == 252,
            "Unexpected prior progress state")
    artifacts = {
        "verification/reconciliation-001.json": prior_raw,
        "verification/reconciliation-002.json": proof_raw,
        "verification/original-progress.json": previous,
    }
    guard, _ = start_guard("B123 closure validation")
    try:
        for path, digest in provenance["recordedFileSha256"].items():
            frozen(closure / path, digest)
            guard.check()
        require(sha(git(config, "show", f"{candidate}:manifest.json")) == proof["manifestSha256"],
                "Confirmed manifest changed")
        for index, item, selection_sha in ((1, prior, PRIOR_SELECTION_SHA), (2, proof, SELECTION_SHA)):
            selection_name = f"coordinator-reconciliation-selection-{index:03}.json"
            selection_raw = frozen(records / selection_name, selection_sha)
            selection = json.loads(selection_raw)
            require(selection["status"] == "PASS" and selection["candidate"] == item["candidate"],
                    "Source selection proof differs")
            artifacts[f"verification/{selection_name}"] = selection_raw
            for path, digest in item["sourceProof"]["signedArtifacts"].items():
                require(sha(git(config, "show", f"{candidate}:{path}")) == digest,
                        f"Signed source changed: {path}")
                guard.check()
        gates = Path(proof["gateSummary"]["path"]).parent
        artifacts["gates/summary.json"] = frozen(gates / "summary.json", proof["gateSummary"]["sha256"])
        frozen(Path(proof["runner"]["path"]), proof["runner"]["sha256"])
        for item in proof["gates"]:
            name = item["gate"]
            raw = frozen(gates / f"{name}.json", item["receiptSha256"])
            log = frozen(gates / f"{name}.log", item["logSha256"])
            check_gate(json.loads(raw), log, name, proof["manifestSha256"],
                       config["repo"], proof["runner"]["sha256"])
            artifacts[f"gates/{name}.json"], artifacts[f"gates/{name}.log"] = raw, log
            guard.check()
        for name in ("coordinator-candidate-verification.json", "source-contract.json",
                     "source-selection-verification-001.json",
                     "reconciliation-001-source-adjudication.json",
                     "reconciliation-002-source-adjudication.json",
                     "confirmation-preparation-recovery-001.json"):
            artifacts[f"verification/{name}"] = frozen(records / name)
        for name in ("verify_b123_revision_v2.py", "verify_b123_revision_v3.py",
                     "verify_b123_reconciliation_selection.py", "verify_b123_followup_selection.py",
                     "scoped_admission.py", "scoped_confirmation_admission.py",
                     "finalize_b123.py", "test_finalize_b123.py",
                     "record_publication.py", "test_record_publication.py"):
            artifacts[f"protocol/tools/{name}"] = frozen(Path(__file__).with_name(name))
        artifacts["protocol/guarded-test-v2.py"] = frozen(records / "guarded-test-v2.py")
        for name, raw in artifacts.items():
            write_frozen(closure / name, raw)
        freeze_json(closure / "validation-provenance.json", {
            "batch": 123, "candidate": candidate, "reviewClosureSha256": sha(provenance_raw),
            "recordedFileSha256": {name: sha(raw) for name, raw in artifacts.items()},
            "publication": "PENDING",
        })
        ledger = make_ledger(config, candidate, provenance, sha(provenance_raw), proof, prior)
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
    finalize(sys.argv[1])

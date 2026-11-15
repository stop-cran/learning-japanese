"""Persist both B118 reconciliations and final confirmations without claiming delivery."""
import json
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, git, load_batch, require, sha, start_guard, write_frozen
from verify_b118_revision import verify_gates



def second_reconciliation(config, candidate, proof):
    records = WS / "scratch-118" / "review"
    prior_raw = frozen(WS / "scratch-118" / "revision-verification-001" / "revision-verification.json",
                       proof["priorProofSha256"])
    prior = json.loads(prior_raw)
    require(prior["status"] == "PASS" and prior["candidate"] == proof["prior"]
            and git(config, "rev-parse", f"{candidate}^").decode().strip() == prior["candidate"]
            and prior["base"] == proof["base"] and prior["initial"] == proof["initial"],
            "Earlier proof or lineage differs")
    require(proof["dictionaryProof"] == prior["sourceProof"], "Dictionary proof changed")
    freeze_raw = frozen(records / "reconciliation-002-freeze.json")
    handoff = json.loads(freeze_raw)
    require(handoff["candidate"] == candidate, "Handoff belongs to another candidate")
    for path, digest in handoff["files"].items():
        frozen(WS / path, digest)
    newer = records / "reconciliation-002"
    artifacts = {
        "revision-verification-001.json": prior_raw,
        "reconciliation-002/freeze.json": freeze_raw,
    }
    for name in ("author-response-gpt-001-confirm-002.md", "pair-dispositions.json",
                 "source-receipt.json", "target-source-receipt.json",
                 "kanjidic2-extraction.json", "changed-file-inventory.json"):
        artifacts[f"reconciliation-002/{name}"] = frozen(newer / name)
    for name in ("pair-dispositions.json", "source-receipt.json"):
        require(artifacts[f"reconciliation-002/{name}"] == git(
            config, "show", f"{candidate}:docs/n1-sources/batch-118/reconciliation-002/{name}"),
            f"Second correction evidence differs: {name}")
    require(sha(artifacts["reconciliation-002/source-receipt.json"])
            == proof["captureProof"]["receiptSha256"]
            and sha(artifacts["reconciliation-002/target-source-receipt.json"])
            == proof["captureProof"]["targetReceiptSha256"], "Capture proof differs")
    return artifacts


def finalize(candidate, gates, proof_path):
    config = load_batch(118)
    repo = Path(config["repo"])
    closure = repo / "docs" / "n1-reviews" / "batch-118-closure"
    provenance_raw = frozen(closure / "provenance.json")
    provenance = json.loads(provenance_raw)
    require(git(config, "rev-parse", "HEAD").decode().strip() == candidate
            and git(config, "show", "-s", "--format=%G?|%ae|%ce", candidate).decode().strip()
            == "G|stop-cran@list.ru|stop-cran@list.ru", "Signed correction changed")
    require(not git(config, "diff", "--name-only") and not git(config, "diff", "--cached", "--name-only"),
            "Tracked files changed since confirmation")
    untracked = git(config, "ls-files", "--others", "--exclude-standard", "-z").decode().split("\0")
    require(all(not path or path.startswith("docs/n1-reviews/batch-118-closure/") for path in untracked),
            "Unrelated untracked files")
    require(provenance["reviewedSnapshot"] == candidate and provenance["publication"] == "PENDING",
            "Closure snapshot or publication state differs")
    finals = [item for item in provenance["reviewLineage"] if item["finalAcceptance"]]
    require(len(finals) == 2 and {item["family"] for item in finals} == {"claude", "gpt"}
            and all(item["snapshot"] == candidate and item["rawVerdict"] == "CONFIRMED" for item in finals),
            "Both original families must confirm the signed correction")
    require([item["run"] for item in provenance["excludedInitialRuns"]] == ["N1-B118-CLAUDE-001"],
            "Excluded initial structure hold was not preserved")
    for path, digest in provenance["recordedFileSha256"].items():
        frozen(closure / path, digest)
    proof_raw = frozen(proof_path)
    proof = json.loads(proof_raw)
    require(proof["status"] == "PASS" and proof["candidate"] == candidate
            and proof["initial"] == config["candidate"] and proof["base"] == config["base"]
            and proof["priorRuntimeChangedOnlyTargetCard"]
            and proof["earlierMetadataStrokesGuardsBodyAndReceiptsPreserved"]
            and proof["sourceMembersPublishedBeforeBatch"] == 246
            and proof["sourceMembersInCandidate"] == 247
            and proof["linguisticAcceptance"] is False
            and proof["publicationAccepted"] is False
            and not proof["memory"]["breach"], "Revision proof does not match")
    manifest_raw = git(config, "show", f"{candidate}:manifest.json")
    require(sha(manifest_raw) == proof["manifestSha256"], "Verified manifest changed")
    guard, _ = start_guard("B118 final closure receipts")
    try:
        receipts = verify_gates(gates, manifest_raw, config, guard)
        require(receipts == proof["gates"], "Verified gate receipts changed")
        artifacts = {"revision-verification.json": proof_raw,
                     **second_reconciliation(config, candidate, proof)}
        for item in receipts:
            for suffix in ("json", "log"):
                name = f"{item['gate']}.{suffix}"
                artifacts[f"gates/{name}"] = frozen(gates / name)
        reconciliation = WS / "scratch-118" / "review" / "reconciliation-001"
        for name in ("author-response-claude-002.md", "author-response-gpt-001.md",
                     "pair-dispositions.json", "source-extraction.json", "changed-file-inventory.json"):
            artifacts[f"reconciliation/{name}"] = frozen(reconciliation / name)
        source_prefix = "docs/n1-sources/batch-118/reconciliation-001"
        for name in ("kanjidic2-records.xml", "source-extraction.json", "pair-dispositions.json"):
            require(frozen(reconciliation / name) == git(config, "show", f"{candidate}:{source_prefix}/{name}"),
                    f"Signed correction evidence differs: {name}")
        require(sha(artifacts["reconciliation/source-extraction.json"]) == proof["dictionaryProof"]["receiptSha256"],
                "Source proof describes another extraction")
        for name in ("verify_b118_revision.py", "verify_reconciliation_sources.py", "finalize_b118.py",
                     "record_publication.py", "test_record_publication.py",
                     "verify_b118_revision_v2.py", "test_verify_b118_revision_v2.py",
                     "finalize_b118_v2.py", "derive_finalize_b118_v2.py",
                     "finalize-b118-v2-derivation.json"):
            artifacts[f"protocol/tools/{name}"] = frozen(Path(__file__).with_name(name))
        for name, raw in artifacts.items():
            write_frozen(closure / name, raw)
        manifest = json.loads(manifest_raw)
        ledger = {
            "schemaVersion": 1, "batch": "118", "baseCommit": config["base"],
            "initialSnapshot": config["candidate"], "reviewedSnapshot": candidate,
            "membership": ["析"], "sourceRows": [528],
            "status": "textual-review-closed-publication-pending",
            "drafted": ["析"], "reviewClosed": ["析"], "published": [], "runtimePublished": False,
            "accounting": {"frozenPendingRecords": 1228, "publishedPendingRecordsWithCards": 246,
                           "reviewClosedPendingRecordsWithCards": 247, "n2Placements": 6,
                           "publishedN1Additions": 240, "undelivered": 982, "notStarted": 981,
                           "overallN1TaskComplete": False},
            "declaringWords": {"析": ["分析"]}, "requiredLinkPairs": 1, "newWordArticles": 0,
            "runtimeCandidate": {"contentVersion": manifest["contentVersion"],
                                 "manifestSha256": sha(manifest_raw), "runtimeEntries": proof["runtimeEntries"]},
            "review": {"status": "closed-with-disclosed-limits", "finalRuns": provenance["finalRuns"],
                       "closure": "../n1-reviews/batch-118-closure/provenance.json",
                       "closureProvenanceSha256": sha(provenance_raw),
                       "remainingActionableFindings": [], "remainingConsequentialClaims": [],
                       "historicalReportsPreserved": True,
                       "identity": "Accepted independent Claude-002 and GPT-001 initials, followed by "
                                   "same-reviewer confirmations. Claude-001 remains excluded for structure failure."},
            "sourceEvidence": {"initial": "batch-118/source-receipt.json",
                               "reconciliation": "batch-118/reconciliation-001/source-extraction.json",
                               "reconciliationReceiptSha256": proof["dictionaryProof"]["receiptSha256"],
                               "secondReconciliation": "batch-118/reconciliation-002/source-receipt.json",
                               "secondReconciliationReceiptSha256": proof["captureProof"]["receiptSha256"],
                               "priorRevision": proof["prior"],
                               "priorProofSha256": proof["priorProofSha256"]},
            "limits": [
                "Bounded textual and host review, not exhaustive linguistic or arbitrary-pool acceptance.",
                "No new Kotlin, native, phone, installed-APK, PDF-glyph or stroke-geometry acceptance.",
                "Publication, CI and exact served ZIP remain pending; review closure is not delivery.",
                "Raw reports and localized citation caveats remain unchanged; the excluded run is not acceptance.",
            ],
        }
        freeze_json(closure / "validation-provenance.json", {
            "batch": 118, "candidate": candidate, "reviewClosureSha256": sha(provenance_raw),
            "recordedFileSha256": {name: sha(raw) for name, raw in artifacts.items()}, "publication": "PENDING",
        })
        print(json.dumps(freeze_json(repo / "docs" / "n1-sources" / "batch-118-progress.json", ledger)))
    finally:
        require(not guard.finish()["breach"], "Finalization RAM guard breached")


if __name__ == "__main__":
    finalize(sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]))

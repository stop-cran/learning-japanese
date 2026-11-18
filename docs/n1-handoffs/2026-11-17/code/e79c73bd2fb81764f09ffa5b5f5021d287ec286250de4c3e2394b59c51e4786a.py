"""Persist B119's accepted textual closure without counting it as published."""
import json
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, git, load_batch, require, sha, start_guard, write_frozen
from verify_b119_revision import INTERMEDIATE, SUPPORT, verify_gates


def verify_closure(provenance, proof, candidate, config):
    require(provenance["reviewedSnapshot"] == candidate and provenance["publication"] == "PENDING",
            "Closure snapshot or publication state differs")
    finals = [item for item in provenance["reviewLineage"] if item["finalAcceptance"]]
    require(len(finals) == 2 and {item["family"] for item in finals} == {"claude", "gpt"}
            and all(item["snapshot"] == candidate and item["rawVerdict"] == "CONFIRMED" for item in finals),
            "Both original families must confirm the signed correction")
    require(not provenance["excludedInitialRuns"], "Unexpected excluded initial run")
    require(proof["status"] == "PASS" and proof["candidate"] == candidate
            and proof["prior"] == INTERMEDIATE and proof["initial"] == config["candidate"]
            and proof["base"] == config["base"]
            and proof["baselineRuntimePreservedExceptRequiredWrappers"]
            and proof["originalMetadataStrokesGuardsAndSourceReceiptsPreserved"]
            and proof["sourceMembersPublishedBeforeBatch"] == 247
            and proof["sourceMembersInCandidate"] == 249
            and proof["linguisticAcceptance"] is False and proof["publicationAccepted"] is False
            and not proof["memory"]["breach"], "Revision proof does not match")


def finalize(candidate, gates, proof_path):
    config = load_batch(119)
    repo = Path(config["repo"])
    closure = repo / "docs" / "n1-reviews" / "batch-119-closure"
    provenance_raw = frozen(closure / "provenance.json")
    provenance = json.loads(provenance_raw)
    require(git(config, "rev-parse", "HEAD").decode().strip() == candidate
            and git(config, "show", "-s", "--format=%G?|%ae|%ce", candidate).decode().strip()
            == "G|stop-cran@list.ru|stop-cran@list.ru", "Signed correction changed")
    require(not git(config, "diff", "--name-only") and not git(config, "diff", "--cached", "--name-only"),
            "Tracked files changed since confirmation")
    untracked = git(config, "ls-files", "--others", "--exclude-standard", "-z").decode().split("\0")
    require(all(not path or path.startswith("docs/n1-reviews/batch-119-closure/") for path in untracked),
            "Unrelated untracked files")
    proof_raw = frozen(proof_path)
    proof = json.loads(proof_raw)
    verify_closure(provenance, proof, candidate, config)
    for path, digest in provenance["recordedFileSha256"].items():
        frozen(closure / path, digest)
    manifest_raw = git(config, "show", f"{candidate}:manifest.json")
    require(sha(manifest_raw) == proof["manifestSha256"], "Verified manifest changed")
    records = WS / "scratch-119" / "review"
    guard, _ = start_guard("B119 final closure receipts")
    try:
        receipts = verify_gates(gates, manifest_raw, config, guard)
        require(receipts == proof["gates"], "Verified gate receipts changed")
        artifacts = {"revision-verification.json": proof_raw,
                     "revision-hold-001.json": frozen(records / "revision-hold-001.json")}
        supplemental_raw = frozen(records / "revision-supplement-verification-002.json")
        supplemental = json.loads(supplemental_raw)
        require(supplemental["candidate"] == candidate and supplemental["status"] == "PASS"
                and not supplemental["memory"]["breach"], "Supplementary verification differs")
        artifacts["revision-supplement-verification-002.json"] = supplemental_raw
        for item in receipts:
            for suffix in ("json", "log"):
                name = f"{item['gate']}.{suffix}"
                artifacts[f"gates/{name}"] = frozen(gates / name)
        for number in (1, 2):
            subdir = f"reconciliation-{number:03d}"
            directory = records / subdir
            for name in ("author-response-claude-001.md", "author-response-gpt-001.md",
                         "pair-dispositions.json", "source-extraction.json", "changed-file-inventory.json"):
                artifacts[f"{subdir}/{name}"] = frozen(directory / name)
            for name in ("kanjidic2-records.xml", "jmdict-records.xml", "source-extraction.json",
                         "pair-dispositions.json", "n1-kanji-source-20261102.json", "source-index-rows.json"):
                require(frozen(directory / name) == git(
                    config, "show", f"{candidate}:docs/n1-sources/batch-119/{subdir}/{name}"),
                    f"Signed correction evidence differs: {subdir}/{name}")
        require(sha(artifacts["reconciliation-002/source-extraction.json"])
                == proof["sourceProof"]["receiptSha256"], "Source proof describes another extraction")
        for name in ("verify_b119_revision.py", "test_verify_b119_revision.py", "verify_b119_supplement.py",
                     "verify_b118_revision.py", "verify_reconciliation_sources.py",
                     "prepare_b119_confirmation.py", "finalize_b119.py", "test_finalize_b119.py",
                     "record_publication.py", "test_record_publication.py"):
            artifacts[f"protocol/tools/{name}"] = frozen(Path(__file__).with_name(name))
        for name, raw in artifacts.items():
            write_frozen(closure / name, raw)
        manifest = json.loads(manifest_raw)
        ledger = {
            "schemaVersion": 1, "batch": "119", "baseCommit": config["base"],
            "initialSnapshot": config["candidate"], "reviewedSnapshot": candidate,
            "membership": list(SUPPORT), "sourceRows": [225, 345],
            "status": "textual-review-closed-publication-pending",
            "drafted": list(SUPPORT), "reviewClosed": list(SUPPORT), "published": [], "runtimePublished": False,
            "accounting": {"frozenPendingRecords": 1228, "publishedPendingRecordsWithCards": 247,
                           "reviewClosedPendingRecordsWithCards": 249, "n2Placements": 6,
                           "publishedN1Additions": 241, "undelivered": 981, "notStarted": 979,
                           "overallN1TaskComplete": False},
            "declaringWords": {c: [word] for c, word in SUPPORT.items()},
            "requiredLinkPairs": 2, "newWordArticles": 0,
            "runtimeCandidate": {"contentVersion": manifest["contentVersion"],
                                 "manifestSha256": sha(manifest_raw), "runtimeEntries": proof["runtimeEntries"]},
            "review": {"status": "closed-with-disclosed-limits", "finalRuns": provenance["finalRuns"],
                       "closure": "../n1-reviews/batch-119-closure/provenance.json",
                       "closureProvenanceSha256": sha(provenance_raw),
                       "remainingActionableFindings": [], "remainingConsequentialClaims": [],
                       "historicalReportsPreserved": True,
                       "identity": "Independent Claude-001 and GPT-001 initials on the same freeze, "
                                   "then serial confirmations by those original reviewers."},
            "sourceEvidence": {"initial": "batch-119/source-receipt.json",
                               "firstReconciliation": "batch-119/reconciliation-001/source-extraction.json",
                               "reconciliation": "batch-119/reconciliation-002/source-extraction.json",
                               "reconciliationReceiptSha256": proof["sourceProof"]["receiptSha256"],
                               "priorRevision": INTERMEDIATE,
                               "priorHold": "../n1-reviews/batch-119-closure/revision-hold-001.json"},
            "limits": [
                "Bounded textual and host review, not exhaustive linguistic or arbitrary-pool acceptance.",
                "No new Kotlin, native, phone, installed-APK, PDF-glyph or stroke-geometry acceptance.",
                "Publication, CI and exact served ZIP remain pending; review closure is not delivery.",
                "Original reports, citation caveats and the preconfirmation source/label hold are preserved.",
            ],
        }
        freeze_json(closure / "validation-provenance.json", {
            "batch": 119, "candidate": candidate, "reviewClosureSha256": sha(provenance_raw),
            "recordedFileSha256": {name: sha(raw) for name, raw in artifacts.items()}, "publication": "PENDING",
        })
        print(json.dumps(freeze_json(repo / "docs" / "n1-sources" / "batch-119-progress.json", ledger)))
    finally:
        require(not guard.finish()["breach"], "Finalization RAM guard breached")


if __name__ == "__main__":
    finalize(sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]))

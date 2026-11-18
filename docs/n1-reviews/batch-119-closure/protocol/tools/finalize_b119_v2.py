"""Close the corrected B119 snapshot while preserving both earlier confirmations."""
import json
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, git, load_batch, require, sha, start_guard, write_frozen
from verify_b119_followup import PRIOR, PROOF_SHA, SUPPLEMENT_SHA
from verify_b119_revision import SUPPORT, verify_gates


def verify_closure(provenance, proof, candidate, config):
    require(provenance["reviewedSnapshot"] == candidate and provenance["publication"] == "PENDING"
            and not provenance["excludedInitialRuns"], "Wrong closure or excluded initial")
    final = [item for item in provenance["reviewLineage"] if item["finalAcceptance"]]
    historical = [item for item in provenance["reviewLineage"] if item["role"] == "intermediate"]
    require(len(final) == 2 and {item["family"] for item in final} == {"claude", "gpt"}
            and all(item["snapshot"] == candidate and item["rawVerdict"] == "CONFIRMED"
                    and item["priorRun"] == f"N1-B119-{item['family'].upper()}-001-CONFIRM-001"
                    for item in final), "Both families must confirm the exact follow-up")
    require(len(historical) == 2
            and {(item["family"], item["rawVerdict"]) for item in historical}
            == {("claude", "CONFIRMED"), ("gpt", "NEEDS FIX")}
            and all(item["snapshot"] == PRIOR for item in historical),
            "Both previous confirmations must remain in their actual states")
    require(proof["status"] == "PASS" and proof["candidate"] == candidate and proof["prior"] == PRIOR
            and proof["initial"] == config["candidate"] and proof["base"] == config["base"]
            and proof["priorVerification"]["sha256"] == PROOF_SHA
            and proof["priorSupplement"]["sha256"] == SUPPLEMENT_SHA
            and proof["baselineRuntimePreservedExceptRequiredWrappers"]
            and proof["originalMetadataStrokesGuardsAndSourceReceiptsPreserved"]
            and proof["oldEvidencePreserved"] and proof["boundedDelta"]["addedGuard"] == "丸"
            and proof["sourceMembersPublishedBeforeBatch"] == 247
            and proof["sourceMembersInCandidate"] == 249
            and not proof["linguisticAcceptance"] and not proof["publicationAccepted"]
            and not proof["memory"]["breach"], "Follow-up proof mismatch")


def finalize(candidate, gates, proof_path):
    config = load_batch(119)
    repo = Path(config["repo"])
    closure = repo / "docs" / "n1-reviews" / "batch-119-closure"
    provenance_raw = frozen(closure / "provenance.json")
    provenance, proof = json.loads(provenance_raw), json.loads(frozen(proof_path))
    verify_closure(provenance, proof, candidate, config)
    require(git(config, "rev-parse", "HEAD").decode().strip() == candidate
            and git(config, "show", "-s", "--format=%G?|%ae|%ce", candidate).decode().strip()
            == "G|stop-cran@list.ru|stop-cran@list.ru", "Signed candidate changed")
    require(not git(config, "diff", "--name-only") and not git(config, "diff", "--cached", "--name-only"),
            "Tracked candidate changed")
    untracked = git(config, "ls-files", "--others", "--exclude-standard", "-z").decode().split("\0")
    require(all(not p or p.startswith("docs/n1-reviews/batch-119-closure/") for p in untracked),
            "Unrelated untracked files")
    for path, digest in provenance["recordedFileSha256"].items():
        frozen(closure / path, digest)
    manifest_raw = git(config, "show", f"{candidate}:manifest.json")
    require(sha(manifest_raw) == proof["manifestSha256"], "Verified manifest changed")
    records = WS / "scratch-119" / "review"
    guard, _ = start_guard("B119 follow-up closure")
    try:
        require(verify_gates(gates, manifest_raw, config, guard) == proof["gates"],
                "Verified follow-up gates changed")
        artifacts = {"revision-verification-003.json": frozen(proof_path),
                     "revision-hold-001.json": frozen(records / "revision-hold-001.json")}
        for name, reference in (("revision-verification-002.json", proof["priorVerification"]),
                                ("revision-supplement-verification-002.json", proof["priorSupplement"])):
            artifacts[name] = frozen(Path(reference["path"]), reference["sha256"])
        for item in proof["gates"]:
            for extension in ("json", "log"):
                name = f"{item['gate']}.{extension}"
                artifacts[f"gates/{name}"] = frozen(gates / name)
        for number in (1, 2, 3):
            subdir = f"reconciliation-{number:03d}"
            for name in ("author-response-claude-001.md", "author-response-gpt-001.md",
                         "pair-dispositions.json", "source-extraction.json", "changed-file-inventory.json"):
                artifacts[f"{subdir}/{name}"] = frozen(records / subdir / name)
        for path, digest in proof["newEvidenceSha256"].items():
            raw = frozen(repo / path, digest)
            require(raw == git(config, "show", f"{candidate}:{path}"), "New signed evidence changed")
        for name in ("verify_b119_followup.py", "test_verify_b119_followup.py",
                     "verify_b119_revision.py", "test_verify_b119_revision.py",
                     "verify_b119_supplement.py", "verify_b118_revision.py",
                     "verify_reconciliation_sources.py", "prepare_b119_confirmation.py",
                     "finalize_b119.py", "test_finalize_b119.py", "finalize_b119_v2.py",
                     "test_finalize_b119_v2.py", "record_publication.py", "test_record_publication.py"):
            artifacts[f"protocol/tools/{name}"] = frozen(Path(__file__).with_name(name))
        for name, raw in artifacts.items():
            write_frozen(closure / name, raw)
        ledger = {
            "schemaVersion": 1, "batch": "119", "baseCommit": config["base"],
            "initialSnapshot": config["candidate"], "reviewedSnapshot": candidate,
            "membership": list(SUPPORT), "sourceRows": [225, 345],
            "status": "textual-review-closed-publication-pending",
            "drafted": list(SUPPORT), "reviewClosed": list(SUPPORT), "published": [],
            "runtimePublished": False,
            "accounting": {"frozenPendingRecords": 1228, "publishedPendingRecordsWithCards": 247,
                           "reviewClosedPendingRecordsWithCards": 249, "n2Placements": 6,
                           "publishedN1Additions": 241, "undelivered": 981, "notStarted": 979,
                           "overallN1TaskComplete": False},
            "declaringWords": {c: [word] for c, word in SUPPORT.items()},
            "requiredLinkPairs": 2, "newWordArticles": 0,
            "runtimeCandidate": {"contentVersion": json.loads(manifest_raw)["contentVersion"],
                                 "manifestSha256": sha(manifest_raw), "runtimeEntries": proof["runtimeEntries"]},
            "review": {"status": "closed-with-disclosed-limits", "finalRuns": provenance["finalRuns"],
                       "closure": "../n1-reviews/batch-119-closure/provenance.json",
                       "closureProvenanceSha256": sha(provenance_raw),
                       "remainingActionableFindings": [], "remainingConsequentialClaims": [],
                       "historicalReportsPreserved": True,
                       "identity": "Independent initials, then two serial confirmation rounds "
                                   "from each original reviewer with snapshot-specific acceptance."},
            "sourceEvidence": {"initial": "batch-119/source-receipt.json",
                               "reconciliation": "batch-119/reconciliation-003/source-extraction.json",
                               "preservedRounds": [1, 2, 3], "priorRevision": PRIOR,
                               "priorHold": "../n1-reviews/batch-119-closure/revision-hold-001.json"},
            "limits": [
                "Bounded textual and host review, not exhaustive linguistic or arbitrary-pool acceptance.",
                "No new Kotlin, native, phone, installed-APK, PDF-glyph or stroke-geometry acceptance.",
                "Publication, CI and exact served ZIP remain pending; review closure is not delivery.",
                "All original reports, earlier acceptances and holds remain snapshot-specific.",
            ],
        }
        freeze_json(closure / "validation-provenance.json", {
            "batch": 119, "candidate": candidate, "reviewClosureSha256": sha(provenance_raw),
            "recordedFileSha256": {name: sha(raw) for name, raw in artifacts.items()}, "publication": "PENDING",
        })
        print(json.dumps(freeze_json(repo / "docs" / "n1-sources" / "batch-119-progress.json", ledger)))
    finally:
        require(not guard.finish()["breach"], "Closure RAM guard breached")


if __name__ == "__main__":
    finalize(sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]))

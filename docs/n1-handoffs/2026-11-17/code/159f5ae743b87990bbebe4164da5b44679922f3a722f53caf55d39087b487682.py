"""Finalize B117 with unchanged earlier proofs and the signed third-round evidence."""
import json
import sys
from pathlib import Path

from common import freeze_json, frozen, git, load_batch, require, sha, start_guard, write_frozen
from finalize_b117_v2 import SOURCE_ROOT, require_sources
from verify_b117_revision import verify_gates


def require_prior_sources(before, after):
    previous = set(before.rstrip(b"\0").split(b"\0"))
    current = set(after.rstrip(b"\0").split(b"\0"))
    require(before and b"" not in previous and previous <= current,
            "Earlier source tree was removed, modified or renamed")
    return len(previous)


def require_round3(candidate, parent, proof, raw_index, raw_receipt):
    index, receipt = json.loads(raw_index), json.loads(raw_receipt)
    require(proof["status"] == "PASS" and proof["candidate"] == candidate
            and proof["batch"] == index["batch"] == receipt["batch"] == 117
            and proof["parent"] == index["parent"] == receipt["parent"] == parent
            and proof["sourceEvidenceIndex"] == f"{SOURCE_ROOT}/reconciliation-003/source-evidence-index.json"
            and proof["sourceEvidenceIndexSha256"] == receipt["sourceEvidence"]["indexSha256"] == sha(raw_index),
            "Round-3 proof does not bind this revision and receipt")
    expected = {
        "KANJIDIC2": (index["kanjidic2"]["sha256"], index["kanjidic2"]["completeRecords"], 0),
        "JMdict": (index["jmdict"]["sha256"], index["jmdict"]["completeEntries"],
                   len(index["jmdict"]["exactWrittenQueries"])),
    }
    records = proof["dictionaryRecords"]
    require(len(records) == 2 and {
        item["source"]: (item["extractionSha256"], item["completeRecordsVerified"],
                         item["exactWrittenQueriesVerified"]) for item in records
    } == expected and all(item["inputSha256"] == index["pinnedInputs"][item["source"]]["sha256"]
                          for item in records), "Round-3 dictionary proof is incomplete")
    added, declined = receipt["addedGuards"], receipt["declinedComparisons"]
    counterparts = {c for values in added.values() for c in values} | {p.split("/")[1] for p in declined}
    targets = set(added) | {p.split("/")[0] for p in declined}
    require(proof["guardAppendsVerified"] == added and proof["declinedComparisons"] == declined
            and set(index["comparisonCards"]) == counterparts
            and proof["comparisonCardsVerified"] == len(counterparts)
            and proof["characterSourcesVerified"] == len(index["characterSources"]) == len(targets)
            and {item["source"] for item in index["characterSources"]} == targets
            and proof["existingTargetRecordsVerified"] == len(index["existingTargetSourceRecords"])
            and proof["counterpartCardCitedIdsVerified"] == sorted(index["jmdict"]["counterpartCardCitedIds"])
            and proof["priorSourceEvidencePreserved"] is True
            and proof["scopeVerified"] == sorted({f"kanji/{c}.md" for c in added} | {"manifest.json"})
            and not proof["memory"]["breach"], "Round-3 scope or preservation proof is incomplete")


def finalize(candidate, gates, revision_path, first_path, second_path, third_path):
    config = load_batch(117)
    repo = Path(config["repo"])
    closure = repo / "docs" / "n1-reviews" / "batch-117-closure"
    provenance_bytes = frozen(closure / "provenance.json")
    provenance = json.loads(provenance_bytes)
    parent = git(config, "rev-parse", f"{candidate}^").decode().strip()
    require(git(config, "rev-parse", "HEAD").decode().strip() == candidate, "Revision is no longer HEAD")
    for commit in (candidate, parent):
        require(git(config, "show", "-s", "--format=%G?|%ae|%ce", commit).decode().strip()
                == "G|stop-cran@list.ru|stop-cran@list.ru", "Invalid revision signature")
    require(not git(config, "diff", "--name-only") and not git(config, "diff", "--cached", "--name-only"),
            "Tracked files changed since closure")
    untracked = git(config, "ls-files", "--others", "--exclude-standard", "-z").decode().split("\0")
    require(all(not p or p.startswith("docs/n1-reviews/batch-117-closure/") for p in untracked),
            "Unrelated untracked files")
    require(provenance["reviewedSnapshot"] == candidate and provenance["publication"] == "PENDING",
            "Closure describes another revision or publication state")
    finals = [item for item in provenance["reviewLineage"] if item["finalAcceptance"]]
    require(len(finals) == 2 and {item["family"] for item in finals} == {"claude", "gpt"}
            and all(item["snapshot"] == candidate and item["rawVerdict"] == "CONFIRMED" for item in finals),
            "Both families must confirm the signed revision")
    for path, digest in provenance["recordedFileSha256"].items():
        require(sha(frozen(closure / path)) == digest, f"Changed closure file: {path}")
    revision_bytes, first_bytes, second_bytes, third_bytes = (
        frozen(path) for path in (revision_path, first_path, second_path, third_path))
    revision, first, second, third = (
        json.loads(raw) for raw in (revision_bytes, first_bytes, second_bytes, third_bytes))
    require(revision["status"] == "PASS" and revision["candidate"] == candidate
            and revision["base"] == config["base"] and revision["initial"] == config["candidate"]
            and revision["originalMetadataStrokesGuardsAndSourceReceiptsPreserved"]
            and revision["baselineRuntimePreservedExceptRequiredWrappers"], "Revision verification differs")
    indexes = [git(config, "show", f"{candidate}:{SOURCE_ROOT}/reconciliation-{n:03d}/source-evidence-index.json")
               for n in (1, 2, 3)]
    require_sources(parent, git(config, "rev-parse", f"{parent}^").decode().strip(),
                    config["members"], first, indexes[0], second, indexes[1])
    require_round3(candidate, parent, third, indexes[2],
                   git(config, "show", f"{candidate}:{SOURCE_ROOT}/reconciliation-003/correction-receipt.json"))
    trees = [git(config, "ls-tree", "-r", "-z", rev, "--", SOURCE_ROOT) for rev in (parent, candidate)]
    preserved = require_prior_sources(*trees)
    manifest_bytes = git(config, "show", f"{candidate}:manifest.json")
    require(sha(manifest_bytes) == revision["manifestSha256"], "Revision manifest changed")
    guard, _ = start_guard("B117 final closure receipts, three source rounds")
    try:
        receipts = verify_gates(gates, manifest_bytes, guard)
        require(receipts == revision["gates"], "Gate receipts changed after revision verification")
        artifacts = {
            "revision-verification.json": revision_bytes,
            "source-verification.json": first_bytes,
            "round2-source-verification.json": second_bytes,
            "round3-source-verification.json": third_bytes,
        }
        for name in ("finalize_b117.py", "finalize_b117_v2.py", "finalize_b117_v3.py",
                     "test_finalize_b117_v2.py", "test_finalize_b117_v3.py"):
            artifacts[f"protocol/tools/{name}"] = frozen(Path(__file__).with_name(name))
        for proof in (second, third):
            item = proof["tool"]
            artifacts[f"protocol/tools/{Path(item['path']).name}"] = frozen(Path(item["path"]), item["sha256"])
        for name in ("round3-verifier-derivation.json", "three-round-tooling-proof.json",
                     "three-round-tooling-tests.txt"):
            artifacts[f"protocol/confirmation/{name}"] = frozen(third_path.parent / name)
        for receipt in receipts:
            for suffix in ("json", "log"):
                name = f"{receipt['gate']}.{suffix}"
                artifacts[f"gates/{name}"] = (gates / name).read_bytes()
        for name, raw in artifacts.items():
            write_frozen(closure / name, raw)
        preservation = freeze_json(closure / "earlier-source-preservation.json", {
            "status": "PASS", "earlierCandidate": parent, "candidate": candidate,
            "sourceRoot": SOURCE_ROOT, "preservedEntries": preserved,
            "earlierTreeSha256": sha(trees[0]), "currentTreeSha256": sha(trees[1]),
            "method": "Every earlier recursive tree entry (path, mode, type and Git blob) remains exact.",
            "earlierProofCandidates": [first["candidate"], second["candidate"]],
            "earlierProofBytesRewritten": False,
        })
        manifest = json.loads(manifest_bytes)
        ledger = {
            "schemaVersion": 1, "batch": "117", "baseCommit": config["base"],
            "initialSnapshot": config["candidate"], "reviewedSnapshot": candidate,
            "membership": config["members"], "sourceRows": [821, 830, 844, 1045],
            "status": "textual-review-closed-publication-pending",
            "drafted": config["members"], "reviewClosed": config["members"], "published": [],
            "runtimePublished": False,
            "accounting": {
                "frozenPendingRecords": 1228, "publishedPendingRecordsWithCards": 242,
                "reviewClosedPendingRecordsWithCards": 246, "n2Placements": 6,
                "publishedN1Additions": 236, "undelivered": 986, "notStarted": 982,
                "overallN1TaskComplete": False,
            },
            "declaringWords": {"紀": ["世紀"], "索": ["索引"], "維": ["維持"], "賃": ["家賃"]},
            "requiredLinkPairs": 4, "newWordArticles": 0,
            "runtimeCandidate": {
                "contentVersion": manifest["contentVersion"], "manifestSha256": sha(manifest_bytes),
                "runtimeEntries": revision["runtimeEntries"],
            },
            "review": {
                "status": "closed-with-disclosed-limits", "finalRuns": provenance["finalRuns"],
                "closure": "../n1-reviews/batch-117-closure/provenance.json",
                "closureProvenanceSha256": sha(provenance_bytes),
                "remainingActionableFindings": [], "remainingConsequentialClaims": [],
                "historicalReportsPreserved": True,
                "identity": "Original GPT and continuing fresh Claude-family replacement; the original Claude context-compacted run is quarantined.",
            },
            "sourceEvidence": {
                "initial": "batch-117/evidence-index.json",
                "reconciliation": "batch-117/reconciliation-001/source-evidence-index.json",
                "reconciliationIndexSha256": sha(indexes[0]), "sourceVerificationSha256": sha(first_bytes),
                "reconciliation002": "batch-117/reconciliation-002/source-evidence-index.json",
                "reconciliation002IndexSha256": sha(indexes[1]), "round2SourceVerificationSha256": sha(second_bytes),
                "reconciliation003": "batch-117/reconciliation-003/source-evidence-index.json",
                "reconciliation003IndexSha256": sha(indexes[2]), "round3SourceVerificationSha256": sha(third_bytes),
                "earlierProofCandidate": parent, "earlierSourcePreservationSha256": preservation["sha256"],
            },
            "limits": [
                "Bounded textual and host review, not exhaustive linguistic or arbitrary-pool acceptance.",
                "No new Kotlin, native, phone, installed-APK, PDF-glyph or stroke-geometry acceptance; the single-borrow Starter 由/ユイ residual remains.",
                "Publication, CI and exact served ZIP remain pending; review closure is not delivery.",
                "Original reports, source qualifications, held runs and historical audit corrections remain explicit.",
            ],
        }
        freeze_json(closure / "validation-provenance.json", {
            "batch": 117, "candidate": candidate, "reviewClosureSha256": sha(provenance_bytes),
            "recordedFileSha256": {**{name: sha(raw) for name, raw in artifacts.items()},
                                  "earlier-source-preservation.json": preservation["sha256"]},
            "publication": "PENDING",
        })
        print(json.dumps(freeze_json(repo / "docs" / "n1-sources" / "batch-117-progress.json", ledger)))
    finally:
        require(not guard.finish()["breach"], "Closure receipt RAM guard breached")


if __name__ == "__main__":
    finalize(sys.argv[1], *(Path(arg) for arg in sys.argv[2:]))

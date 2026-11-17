"""Persist B117's verified closure and delivery ledger without publishing it."""
import json
import sys
from pathlib import Path

from common import (WS, freeze_json, frozen, git, load_batch, require, sha,
                    write_frozen)
from verify_b117_revision import verify_gates


def require_source_proof(proof, index_bytes):
    index = json.loads(index_bytes)
    require(proof["status"] == "PASS"
            and proof["sourceEvidenceIndexSha256"] == sha(index_bytes),
            "Source proof does not bind the signed revision")
    expected = {
        "KANJIDIC2": (index["kanjidic2"]["sha256"], index["kanjidic2"]["completeRecords"]),
        "JMdict": (index["jmdict"]["sha256"], index["jmdict"]["completeEntries"]),
    }
    actual = {
        item["source"]: (item["extractionSha256"], item["completeRecordsVerified"])
        for item in proof["dictionaryRecords"]
    }
    require(actual == expected and proof["comparisonCardsVerified"] == len(index["comparisonCards"])
            and proof["baseline"] == index["baseline"] and not proof["memory"]["breach"],
            "Source proof is incomplete or describes different evidence")
    for item in proof["dictionaryRecords"]:
        require(item["inputSha256"] == index["pinnedInputs"][item["source"]]["sha256"],
                "Source proof uses another dictionary input")


def finalize(candidate, gates, revision_path, source_path):
    config = load_batch(117)
    repo = Path(config["repo"])
    closure = repo / "docs" / "n1-reviews" / "batch-117-closure"
    provenance_path = closure / "provenance.json"
    provenance_bytes = frozen(provenance_path)
    provenance = json.loads(provenance_bytes)
    require(git(config, "rev-parse", "HEAD").decode().strip() == candidate,
            "Revision is no longer HEAD")
    require(git(config, "show", "-s", "--format=%G?|%ae|%ce", candidate).decode().strip()
            == "G|stop-cran@list.ru|stop-cran@list.ru", "Invalid revision signature")
    require(not git(config, "diff", "--name-only") and not git(config, "diff", "--cached", "--name-only"),
            "Tracked files changed since closure")
    untracked = git(config, "ls-files", "--others", "--exclude-standard", "-z").decode().split("\0")
    require(all(not path or path.startswith("docs/n1-reviews/batch-117-closure/") for path in untracked),
            "Unrelated untracked files")
    require(provenance["reviewedSnapshot"] == candidate and provenance["publication"] == "PENDING",
            "Closure describes another revision or publication state")
    finals = [item for item in provenance["reviewLineage"] if item["finalAcceptance"]]
    require(len(finals) == 2 and {item["family"] for item in finals} == {"claude", "gpt"}
            and all(item["snapshot"] == candidate and item["rawVerdict"] == "CONFIRMED" for item in finals),
            "Both families must confirm the signed revision")
    for path, digest in provenance["recordedFileSha256"].items():
        require(sha(frozen(closure / path)) == digest, f"Changed closure file: {path}")

    revision_bytes, source_bytes = frozen(revision_path), frozen(source_path)
    revision, source = json.loads(revision_bytes), json.loads(source_bytes)
    require(revision["status"] == "PASS" and revision["candidate"] == candidate
            and revision["base"] == config["base"] and revision["initial"] == config["candidate"]
            and revision["originalMetadataStrokesGuardsAndSourceReceiptsPreserved"]
            and revision["baselineRuntimePreservedExceptRequiredWrappers"],
            "Revision verification is missing or does not match")
    source_index = git(config, "show",
                       f"{candidate}:docs/n1-sources/batch-117/reconciliation-001/source-evidence-index.json")
    require_source_proof(source, source_index)
    manifest_bytes = git(config, "show", f"{candidate}:manifest.json")
    require(sha(manifest_bytes) == revision["manifestSha256"], "Revision manifest changed")
    from common import start_guard
    guard, _ = start_guard("B117 final closure receipts")
    try:
        receipts = verify_gates(gates, manifest_bytes, guard)
        require(receipts == revision["gates"], "Gate receipts changed after revision verification")
        artifacts = {
            "revision-verification.json": revision_bytes,
            "source-verification.json": source_bytes,
        }
        for receipt in receipts:
            for suffix in ("json", "log"):
                name = f"{receipt['gate']}.{suffix}"
                artifacts[f"gates/{name}"] = (gates / name).read_bytes()
        for name, raw in artifacts.items():
            write_frozen(closure / name, raw)
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
            },
            "sourceEvidence": {
                "initial": "batch-117/evidence-index.json",
                "reconciliation": "batch-117/reconciliation-001/source-evidence-index.json",
                "reconciliationIndexSha256": sha(source_index),
                "sourceVerificationSha256": sha(source_bytes),
            },
            "limits": [
                "Bounded textual and host review, not exhaustive linguistic or arbitrary-pool acceptance.",
                "No new Kotlin, native, phone, installed-APK, PDF-glyph or stroke-geometry acceptance.",
                "Publication, CI and exact served ZIP remain pending; review closure is not delivery.",
                "All original reports, source qualifications and historical audit corrections remain explicit.",
            ],
        }
        attachment = {
            "batch": 117, "candidate": candidate, "reviewClosureSha256": sha(provenance_bytes),
            "recordedFileSha256": {name: sha(raw) for name, raw in artifacts.items()},
            "publication": "PENDING",
        }
        freeze_json(closure / "validation-provenance.json", attachment)
        result = freeze_json(repo / "docs" / "n1-sources" / "batch-117-progress.json", ledger)
        print(json.dumps(result))
    finally:
        require(not guard.finish()["breach"], "Closure receipt RAM guard breached")


if __name__ == "__main__":
    finalize(sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4]))

"""Finalize B117 with both signed reconciliation source proofs; v1 stays frozen."""
import json
import sys
from pathlib import Path

from common import freeze_json, frozen, git, load_batch, require, sha, start_guard, write_frozen
from finalize_b117 import require_source_proof
from verify_b117_revision import verify_gates


SOURCE_ROOT = "docs/n1-sources/batch-117"


def require_sources(candidate, parent, members, first, first_index, second, second_index):
    require(first["candidate"] == second["candidate"] == candidate,
            "Source proofs describe another signed candidate")
    require_source_proof(first, first_index)
    index = json.loads(second_index)
    require(second["status"] == "PASS" and second["batch"] == index["batch"] == 117
            and second["parent"] == index["parent"] == parent
            and second["sourceEvidenceIndex"] == f"{SOURCE_ROOT}/reconciliation-002/source-evidence-index.json"
            and second["sourceEvidenceIndexSha256"] == sha(second_index),
            "Round-2 proof does not bind this signed source index")
    expected = {
        "KANJIDIC2": (index["kanjidic2"]["sha256"], index["kanjidic2"]["completeRecords"], 0),
        "JMdict": (index["jmdict"]["sha256"], index["jmdict"]["completeEntries"],
                   len(index["jmdict"]["exactWrittenQueries"])),
    }
    records = second["dictionaryRecords"]
    actual = {item["source"]: (item["extractionSha256"], item["completeRecordsVerified"],
                               item["exactWrittenQueriesVerified"]) for item in records}
    require(len(records) == 2 and actual == expected
            and all(item["inputSha256"] == index["pinnedInputs"][item["source"]]["sha256"]
                    for item in records),
            "Round-2 dictionary families are incomplete or use another input")
    require(second["comparisonCardsVerified"] == len(index["comparisonCards"])
            and second["characterSourcesVerified"] == len(members) == len(index["characterSources"])
            and {item["source"] for item in index["characterSources"]} == set(members)
            and second["priorSourceEvidencePreserved"] is True
            and second["scopeVerified"] == sorted({f"kanji/{c}.md" for c in members} | {"manifest.json"})
            and not second["memory"]["breach"],
            "Round-2 comparison, character, preservation or scope proof is incomplete")


def finalize(candidate, gates, revision_path, first_path, second_path):
    config = load_batch(117)
    repo = Path(config["repo"])
    closure = repo / "docs" / "n1-reviews" / "batch-117-closure"
    provenance_bytes = frozen(closure / "provenance.json")
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
    revision_bytes, first_bytes, second_bytes = (
        frozen(path) for path in (revision_path, first_path, second_path))
    revision, first, second = (json.loads(raw) for raw in (revision_bytes, first_bytes, second_bytes))
    require(revision["status"] == "PASS" and revision["candidate"] == candidate
            and revision["base"] == config["base"] and revision["initial"] == config["candidate"]
            and revision["originalMetadataStrokesGuardsAndSourceReceiptsPreserved"]
            and revision["baselineRuntimePreservedExceptRequiredWrappers"],
            "Revision verification is missing or does not match")
    indexes = [git(config, "show", f"{candidate}:{SOURCE_ROOT}/reconciliation-{n:03d}/source-evidence-index.json")
               for n in (1, 2)]
    require_sources(candidate, git(config, "rev-parse", f"{candidate}^").decode().strip(),
                    config["members"], first, indexes[0], second, indexes[1])
    manifest_bytes = git(config, "show", f"{candidate}:manifest.json")
    require(sha(manifest_bytes) == revision["manifestSha256"], "Revision manifest changed")
    guard, _ = start_guard("B117 final closure receipts, both reconciliations")
    try:
        receipts = verify_gates(gates, manifest_bytes, guard)
        require(receipts == revision["gates"], "Gate receipts changed after revision verification")
        artifacts = {
            "revision-verification.json": revision_bytes,
            "source-verification.json": first_bytes,
            "round2-source-verification.json": second_bytes,
            "protocol/tools/finalize_b117.py": frozen(Path(__file__).with_name("finalize_b117.py")),
            "protocol/tools/finalize_b117_v2.py": frozen(Path(__file__)),
            "protocol/tools/test_finalize_b117_v2.py": frozen(Path(__file__).with_name("test_finalize_b117_v2.py")),
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
                "reconciliationIndexSha256": sha(indexes[0]), "sourceVerificationSha256": sha(first_bytes),
                "reconciliation002": "batch-117/reconciliation-002/source-evidence-index.json",
                "reconciliation002IndexSha256": sha(indexes[1]),
                "round2SourceVerificationSha256": sha(second_bytes),
            },
            "limits": [
                "Bounded textual and host review, not exhaustive linguistic or arbitrary-pool acceptance.",
                "No new Kotlin, native, phone, installed-APK, PDF-glyph or stroke-geometry acceptance.",
                "Publication, CI and exact served ZIP remain pending; review closure is not delivery.",
                "All original reports, source qualifications and historical audit corrections remain explicit.",
            ],
        }
        freeze_json(closure / "validation-provenance.json", {
            "batch": 117, "candidate": candidate, "reviewClosureSha256": sha(provenance_bytes),
            "recordedFileSha256": {name: sha(raw) for name, raw in artifacts.items()},
            "publication": "PENDING",
        })
        print(json.dumps(freeze_json(repo / "docs" / "n1-sources" / "batch-117-progress.json", ledger)))
    finally:
        require(not guard.finish()["breach"], "Closure receipt RAM guard breached")


if __name__ == "__main__":
    finalize(sys.argv[1], *(Path(arg) for arg in sys.argv[2:]))

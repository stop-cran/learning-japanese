"""Finalize four correction rounds without relabeling earlier proofs or acceptances."""
import json
import sys
from pathlib import Path

from common import freeze_json, frozen, git, load_batch, require, sha, start_guard, write_frozen
from finalize_b117_v2 import SOURCE_ROOT, require_sources
from finalize_b117_v3 import require_prior_sources, require_round3
from verify_b117_revision import verify_gates
from verify_b117_round4 import PARENT, ROOT, require_focused


def require_round4(candidate, proof, raw_index, raw_receipt, manifest, target):
    index, receipt = json.loads(raw_index), json.loads(raw_receipt)
    require(proof["status"] == "PASS" and proof["candidate"] == candidate
            and proof["batch"] == index["batch"] == receipt["batch"] == 117
            and proof["parent"] == index["parent"] == receipt["parent"] == PARENT
            and proof["sourceEvidenceIndex"] == f"{ROOT}/source-evidence-index.json"
            and proof["sourceEvidenceIndexSha256"] == receipt["sourceEvidence"]["indexSha256"] == sha(raw_index)
            and proof["manifestSha256"] == sha(manifest) and proof["targetSha256"] == sha(target),
            "Round-4 proof does not bind the signed correction")
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
                          for item in records), "Round-4 dictionary proof is incomplete")
    require(proof["comparisonCardsVerified"] == len(index["comparisonCards"]) == 3
            and set(index["comparisonCards"]) == {"銀", "語", "休"}
            and proof["characterSourcesVerified"] == len(index["characterSources"]) == 1
            and index["characterSources"][0]["source"] == "維"
            and proof["modelSnapshotsVerified"] == proof["focusedCheck"]["models"]
            == {name: item["sha256"] for name, item in index["models"].items()}
            and set(index["models"]) == {"reading_options.py", "reading_exposure.py", "n1lib.py"}
            and proof["focusedTool"]["sha256"] == receipt["validation"]["focusedCheck"]["sha256"]
            and proof["priorSourceEvidencePreserved"] is True
            and proof["scopeVerified"] == ["kanji/維.md", "manifest.json"]
            and not proof["memory"]["breach"], "Round-4 scope, model or preservation proof is incomplete")
    require_focused(proof["focusedCheck"])


def finalize(candidate, gates, revision_path, first_path, second_path, third_path, fourth_path):
    config = load_batch(117)
    repo = Path(config["repo"])
    closure = repo / "docs" / "n1-reviews" / "batch-117-closure"
    provenance_bytes = frozen(closure / "provenance.json")
    provenance = json.loads(provenance_bytes)
    parent = git(config, "rev-parse", f"{candidate}^").decode().strip()
    earlier = git(config, "rev-parse", f"{parent}^").decode().strip()
    require(parent == PARENT and git(config, "rev-parse", "HEAD").decode().strip() == candidate,
            "Round-4 ancestry or HEAD changed")
    for commit in (candidate, parent, earlier):
        require(git(config, "show", "-s", "--format=%G?|%ae|%ce", commit).decode().strip()
                == "G|stop-cran@list.ru|stop-cran@list.ru", "Invalid signed correction ancestry")
    require(not git(config, "diff", "--name-only") and not git(config, "diff", "--cached", "--name-only"),
            "Tracked files changed since closure")
    untracked = git(config, "ls-files", "--others", "--exclude-standard", "-z").decode().split("\0")
    require(all(not p or p.startswith("docs/n1-reviews/batch-117-closure/") for p in untracked),
            "Unrelated untracked files")
    require(provenance["reviewedSnapshot"] == candidate and provenance["publication"] == "PENDING",
            "Closure describes another snapshot or publication state")
    finals = [item for item in provenance["reviewLineage"] if item["finalAcceptance"]]
    require(len(finals) == 2 and {item["family"] for item in finals} == {"claude", "gpt"}
            and all(item["snapshot"] == candidate and item["rawVerdict"] == "CONFIRMED" for item in finals),
            "Both families must confirm the final signed snapshot")
    for path, digest in provenance["recordedFileSha256"].items():
        require(sha(frozen(closure / path)) == digest, f"Changed closure file: {path}")
    paths = (revision_path, first_path, second_path, third_path, fourth_path)
    raw = [frozen(path) for path in paths]
    revision, first, second, third, fourth = [json.loads(value) for value in raw]
    require(revision["status"] == "PASS" and revision["candidate"] == candidate
            and revision["base"] == config["base"] and revision["initial"] == config["candidate"]
            and revision["originalMetadataStrokesGuardsAndSourceReceiptsPreserved"]
            and revision["baselineRuntimePreservedExceptRequiredWrappers"], "Revision verification differs")
    blob = lambda path: git(config, "show", f"{candidate}:{path}")
    indexes = [blob(f"{SOURCE_ROOT}/reconciliation-{n:03d}/source-evidence-index.json") for n in (1, 2, 3, 4)]
    require_sources(earlier, git(config, "rev-parse", f"{earlier}^").decode().strip(),
                    config["members"], first, indexes[0], second, indexes[1])
    require_round3(parent, earlier, third, indexes[2],
                   blob(f"{SOURCE_ROOT}/reconciliation-003/correction-receipt.json"))
    manifest_bytes = blob("manifest.json")
    require_round4(candidate, fourth, indexes[3], blob(f"{ROOT}/correction-receipt.json"),
                   manifest_bytes, blob("kanji/維.md"))
    require(sha(manifest_bytes) == revision["manifestSha256"], "Revision manifest changed")
    trees = [git(config, "ls-tree", "-r", "-z", rev, "--", SOURCE_ROOT) for rev in (earlier, parent, candidate)]
    preserved = [require_prior_sources(trees[n], trees[n + 1]) for n in (0, 1)]
    guard, _ = start_guard("B117 final closure receipts, four source rounds")
    try:
        receipts = verify_gates(gates, manifest_bytes, guard)
        require(receipts == revision["gates"], "Gate receipts changed after revision verification")
        artifacts = dict(zip(("revision-verification.json", "source-verification.json",
                              "round2-source-verification.json", "round3-source-verification.json",
                              "round4-source-verification.json"), raw))
        for name in ("finalize_b117.py", "finalize_b117_v2.py", "finalize_b117_v3.py", "finalize_b117_v4.py", "finalize_b117_v5.py",
                     "test_finalize_b117_v2.py", "test_finalize_b117_v3.py", "test_finalize_b117_v4.py",
                     "verify_b117_round4.py", "test_verify_b117_round4.py"):
            artifacts[f"protocol/tools/{name}"] = frozen(Path(__file__).with_name(name))
        for item in (second["tool"], third["tool"], fourth["tool"], fourth["focusedTool"]):
            artifacts[f"protocol/tools/{Path(item['path']).name}"] = frozen(Path(item["path"]), item["sha256"])
        for name in ("round3-verifier-derivation.json", "three-round-tooling-proof.json",
                     "three-round-tooling-tests.txt", "round4-lineage-tooling-proof.json",
                     "round4-lineage-tooling-tests.txt", "round4-finalization-tooling-proof.json",
                     "round4-finalization-tooling-tests.txt", "replay-publication-tooling-proof.json"):
            artifacts[f"protocol/confirmation/{name}"] = frozen(fourth_path.parent / name)
        for receipt in receipts:
            for suffix in ("json", "log"):
                name = f"{receipt['gate']}.{suffix}"
                artifacts[f"gates/{name}"] = frozen(gates / name)
        for name in ("focused-check.json", "focused-check.log", "summary.json", "suite-summary.json"):
            artifacts[f"gates/{name}"] = frozen(gates / name)
        require(sha(artifacts["gates/focused-check.json"]) == fourth["focusedAuthorResultSha256"],
                "Focused author result changed")
        for name, data in artifacts.items():
            write_frozen(closure / name, data)
        preservation = freeze_json(closure / "earlier-source-preservation.json", {
            "status": "PASS", "earlierCandidates": [earlier, parent], "candidate": candidate,
            "sourceRoot": SOURCE_ROOT, "preservedEntriesByTransition": preserved,
            "treeSha256ByRevision": {rev: sha(tree) for rev, tree in zip((earlier, parent, candidate), trees)},
            "method": "Every earlier recursive tree entry retains path, mode, type and Git blob.",
            "earlierProofCandidates": [first["candidate"], second["candidate"], third["candidate"]],
            "earlierProofBytesRewritten": False,
        })
        manifest = json.loads(manifest_bytes)
        source_evidence = {"initial": "batch-117/evidence-index.json",
                           "earlierSourcePreservationSha256": preservation["sha256"]}
        for n, (index, proof_bytes) in enumerate(zip(indexes, raw[1:]), 1):
            source_evidence[f"reconciliation{n:03d}"] = {
                "index": f"batch-117/reconciliation-{n:03d}/source-evidence-index.json",
                "indexSha256": sha(index), "sourceVerificationSha256": sha(proof_bytes),
                "proofCandidate": json.loads(proof_bytes)["candidate"],
            }
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
            "runtimeCandidate": {"contentVersion": manifest["contentVersion"],
                                 "manifestSha256": sha(manifest_bytes),
                                 "runtimeEntries": revision["runtimeEntries"]},
            "review": {
                "status": "closed-with-disclosed-limits", "finalRuns": provenance["finalRuns"],
                "closure": "../n1-reviews/batch-117-closure/provenance.json",
                "closureProvenanceSha256": sha(provenance_bytes),
                "remainingActionableFindings": [], "remainingConsequentialClaims": [],
                "historicalReportsPreserved": True,
                "identity": "Original GPT and a fresh Claude-family bounded replay; earlier valid replacement snapshots are preserved and both context-compacted Claude runs are quarantined.",
            },
            "sourceEvidence": source_evidence,
            "limits": [
                "Bounded textual and host review, not exhaustive linguistic or arbitrary-pool acceptance.",
                "The former Starter+target+由/ユイ exposure is repaired in the four named host-model pools; no Kotlin/native/device or arbitrary-pool equivalence claim.",
                "No new phone, installed-APK, PDF-glyph or stroke-geometry acceptance.",
                "Publication, CI and exact served ZIP remain pending; review closure is not delivery.",
                "Historical source proofs, reports, accepted snapshots and held-run limitations remain unchanged.",
            ],
        }
        freeze_json(closure / "validation-provenance.json", {
            "batch": 117, "candidate": candidate, "reviewClosureSha256": sha(provenance_bytes),
            "recordedFileSha256": {**{name: sha(data) for name, data in artifacts.items()},
                                  "earlier-source-preservation.json": preservation["sha256"]},
            "publication": "PENDING",
        })
        print(json.dumps(freeze_json(repo / "docs" / "n1-sources" / "batch-117-progress.json", ledger)))
    finally:
        require(not guard.finish()["breach"], "Closure RAM guard breached")


if __name__ == "__main__":
    finalize(sys.argv[1], *(Path(arg) for arg in sys.argv[2:]))

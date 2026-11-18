"""Persist B121 closure only after both original reviewers confirm its exact revision."""
import json
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, git, json_bytes, load_batch, require, sha, start_guard, write_frozen
from verify_b121_revision import SIGNER, check_gate

INITIALS = {"claude": "N1-B121-CLAUDE-002", "gpt": "N1-B121-GPT-001"}
HELD = "N1-B121-CLAUDE-001"
HOLD_SHA = "56fe95ed8578345b60286e256658e3c5a588811bc811850476fbe2f72218e353"


def check_closure(provenance, proof, candidate, config):
    require(provenance["reviewedSnapshot"] == candidate
            and provenance["initialSnapshot"] == config["candidate"]
            and provenance["base"] == config["base"] and provenance["publication"] == "PENDING"
            and provenance["members"] == config["members"] == ["\u5fb3"],
            "Closure snapshot, scope or publication state differs")
    lineage = provenance["reviewLineage"]
    initials = [item for item in lineage if item["role"] == "initial"]
    finals = [item for item in lineage if item["finalAcceptance"]]
    require(len(lineage) == 4 and len(initials) == len(finals) == 2
            and {item["run"] for item in initials} == set(INITIALS.values())
            and {item["family"] for item in finals} == {"claude", "gpt"}
            and len(provenance["finalRuns"]) == 2
            and set(provenance["finalRuns"]) == {item["run"] for item in finals},
            "Expected two selected initials and two original-reviewer confirmations")
    for family, initial in INITIALS.items():
        first = next(item for item in initials if item["run"] == initial)
        last = next(item for item in finals if item["family"] == family)
        require(first["family"] == family and first["snapshot"] == config["candidate"]
                and not first["finalAcceptance"] and first["rawVerdict"] == "NEEDS FIX"
                and last["run"] == f"{initial}-CONFIRM-001" and last["role"] == "final"
                and last["session"] == first["session"] and last["snapshot"] == candidate
                and last["rawVerdict"] == "CONFIRMED" and last["confirmationAcceptedOnSnapshot"],
                "Confirmation changed reviewer, verdict or candidate")
    excluded = provenance["excludedInitialRuns"]
    require(len(excluded) == 1 and excluded[0]["run"] == HELD
            and excluded[0]["snapshot"] == config["candidate"]
            and excluded[0]["status"] == "HOLD_STRUCTURE_FAILED"
            and excluded[0]["holdSha256"] == HOLD_SHA
            and excluded[0]["reviewAccepted"] is False and excluded[0]["finalAcceptance"] is False,
            "Held initial was omitted, changed or promoted")
    require(proof["status"] == "PASS" and proof["candidate"] == candidate
            and proof["initial"] == config["candidate"] and proof["base"] == config["base"]
            and proof["baselineRuntimePreservedExceptRequiredWrappers"]
            and proof["originalMetadataStrokesGuardsAndSourceReceiptsPreserved"]
            and proof["sourceMembersPublishedBeforeBatch"] == 250
            and proof["sourceMembersInCandidate"] == 251
            and proof["linguisticAcceptance"] is False and proof["publicationAccepted"] is False
            and not proof["memory"]["breach"], "Revision verification differs")


def make_ledger(config, candidate, provenance, provenance_sha, proof):
    return {
        "schemaVersion": 1, "batch": "121", "baseCommit": config["base"],
        "initialSnapshot": config["candidate"], "reviewedSnapshot": candidate,
        "membership": ["\u5fb3"], "sourceRows": [347],
        "status": "textual-review-closed-publication-pending",
        "drafted": ["\u5fb3"], "reviewClosed": ["\u5fb3"], "published": [], "runtimePublished": False,
        "accounting": {"frozenPendingRecords": 1228, "publishedPendingRecordsWithCards": 250,
                       "reviewClosedPendingRecordsWithCards": 251, "n2Placements": 6,
                       "publishedN1Additions": 244, "undelivered": 978, "notStarted": 977,
                       "overallN1TaskComplete": False},
        "declaringWords": {"\u5fb3": ["\u9053\u5fb3"]}, "requiredLinkPairs": 1, "newWordArticles": 0,
        "runtimeCandidate": {"contentVersion": proof["contentVersion"],
                             "manifestSha256": proof["manifestSha256"],
                             "runtimeEntries": proof["runtimeEntries"]},
        "review": {"status": "closed-with-disclosed-limits", "finalRuns": provenance["finalRuns"],
                   "closure": "../n1-reviews/batch-121-closure/provenance.json",
                   "closureProvenanceSha256": provenance_sha, "remainingActionableFindings": [],
                   "remainingConsequentialClaims": [], "historicalReportsPreserved": True,
                   "excludedInitialRuns": provenance["excludedInitialRuns"],
                   "identity": "Independent Claude002 and GPT001 NEEDS FIX initials, source-based "
                               "reconciliation and serial confirmations by those original reviewers. "
                               "Claude001 remains excluded and preserved as structure-held evidence."},
        "sourceEvidence": {"initial": "batch-121/source-receipt.json",
                           "reconciliation": "batch-121/reconciliation-001/",
                           "signedArtifactSha256": proof["sourceProof"]["signedArtifacts"]},
        "limits": [
            "Bounded textual and host review, not exhaustive linguistic or arbitrary-pool acceptance.",
            "No new Kotlin, native, phone, installed-APK or fallback-rendering acceptance.",
            "Publication, CI and exact served ZIP remain pending; review closure is not delivery.",
            "Original reports, source qualifications and the held initial remain preserved.",
        ],
    }


def finalize(candidate, gates, proof_path):
    config = load_batch(121)
    repo = Path(config["repo"])
    records = WS / "scratch-121" / "review"
    closure = repo / "docs" / "n1-reviews" / "batch-121-closure"
    provenance_raw, proof_raw = frozen(closure / "provenance.json"), frozen(proof_path)
    provenance, proof = json.loads(provenance_raw), json.loads(proof_raw)
    check_closure(provenance, proof, candidate, config)
    require(git(config, "rev-parse", "HEAD").decode().strip() == candidate
            and git(config, "show", "-s", "--format=%G?|%GF|%ae|%ce", candidate).decode().strip()
            == f"G|{SIGNER}|stop-cran@list.ru|stop-cran@list.ru", "Signed revision changed")
    require(not git(config, "diff", "--name-only") and not git(config, "diff", "--cached", "--name-only"),
            "Tracked revision changed")
    untracked = git(config, "ls-files", "--others", "--exclude-standard", "-z").decode("utf-8").split("\0")
    require(all(not path or path.startswith("docs/n1-reviews/batch-121-closure/") for path in untracked),
            "Unrelated untracked files")
    ledger_path = repo / "docs" / "n1-sources" / "batch-121-progress.json"
    previous = git(config, "show", f"{candidate}:docs/n1-sources/batch-121-progress.json")
    require(ledger_path.read_bytes() == previous, "Draft progress ledger changed")
    old_ledger = json.loads(previous)
    require(old_ledger["status"] == "local-authoring-review-pending"
            and not old_ledger["published"] and old_ledger["runtimePublished"] is False,
            "Unexpected prior progress state")
    guard, _ = start_guard("B121 closure validation")
    try:
        for path, digest in provenance["recordedFileSha256"].items():
            frozen(closure / path, digest)
            guard.check()
        raw_manifest = git(config, "show", f"{candidate}:manifest.json")
        require(sha(raw_manifest) == proof["manifestSha256"], "Confirmed manifest changed")
        for path, digest in proof["sourceProof"]["signedArtifacts"].items():
            require(sha(git(config, "show", f"{candidate}:{path}")) == digest,
                    f"Verified signed source changed: {path}")
            guard.check()
        artifacts = {"verification/reconciliation-001.json": proof_raw,
                     "verification/original-progress.json": previous}
        summary = proof["gateSummary"]
        require(Path(summary["path"]) == gates / "summary.json", "Gate directory differs")
        artifacts["gates/summary.json"] = frozen(gates / "summary.json", summary["sha256"])
        for item in proof["gates"]:
            name = item["gate"]
            raw = frozen(gates / f"{name}.json", item["receiptSha256"])
            log = frozen(gates / f"{name}.log", item["logSha256"])
            check_gate(json.loads(raw), log, name, proof["manifestSha256"], config["repo"])
            artifacts[f"gates/{name}.json"], artifacts[f"gates/{name}.log"] = raw, log
            guard.check()
        for name in ("coordinator-candidate-verification.json", "coordinator-runtime-glyph-check.json",
                     "source-contract.json", "revision-verifier-v2-derivation.json",
                     "source-selection-verification-001.json", "finalizer-v2-derivation.json"):
            artifacts[f"verification/{name}"] = frozen(records / name)
        for name in ("verify_b121_revision.py", "test_verify_b121_revision.py",
                     "verify_reconciliation_sources.py", "finalize_b121.py", "test_finalize_b121.py",
                     "record_publication.py", "test_record_publication.py",
                     "verify_b121_revision_v2.py", "test_verify_b121_revision_v2.py",
                     "prepare_b121_revision_v2.py", "verify_b121_source_selection.py",
                     "finalize_b121_v2.py", "test_finalize_b121_v2.py", "derive_b121_finalizer_v2.py"):
            artifacts[f"protocol/tools/{name}"] = frozen(Path(__file__).with_name(name))
        for name, raw in artifacts.items():
            write_frozen(closure / name, raw)
        ledger = make_ledger(config, candidate, provenance, sha(provenance_raw), proof)
        freeze_json(closure / "validation-provenance.json", {
            "batch": 121, "candidate": candidate, "reviewClosureSha256": sha(provenance_raw),
            "recordedFileSha256": {name: sha(raw) for name, raw in artifacts.items()},
            "publication": "PENDING",
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

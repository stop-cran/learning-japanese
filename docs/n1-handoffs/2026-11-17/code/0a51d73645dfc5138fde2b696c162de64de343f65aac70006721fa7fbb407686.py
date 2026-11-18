"""Close the third B123 revision without relabeling the earlier held review."""
import json
import sys
from pathlib import Path

from common import CHECKS, WS, freeze_json, frozen, git, json_bytes, load_batch, require, sha, start_guard, write_frozen
from finalize_b123 import (
    INITIALS, PRIOR_SELECTION_SHA, PROOF_SHA, SELECTION_SHA, make_ledger as earlier_ledger,
)
from verify_b123_revision_v2 import SIGNER, check_gate
from verify_b123_revision_v3 import PRIOR_SHA as FIRST_PROOF_SHA
from verify_b123_revision_v4 import PARENT

FINALS = {family: f"N1-B123-{family.upper()}-CONFIRM-003" for family in INITIALS}
HISTORY = {family: f"N1-B123-{family.upper()}-CONFIRM-002" for family in INITIALS}


def check_history(provenance, candidate, config):
    require(candidate != PARENT and provenance["reviewedSnapshot"] == candidate
            and provenance["initialSnapshot"] == config["candidate"]
            and provenance["base"] == config["base"] and provenance["publication"] == "PENDING"
            and provenance["members"] == config["members"] == ["\u7bc4"]
            and not provenance["excludedInitialRuns"], "Closure scope or snapshot differs")
    lineage = provenance["reviewLineage"]
    require(len(lineage) == 6 and len({row["run"] for row in lineage}) == 6
            and len(provenance["finalRuns"]) == len(provenance["intermediateRuns"]) == 2
            and set(provenance["finalRuns"]) == set(FINALS.values())
            and set(provenance["intermediateRuns"]) == set(HISTORY.values()),
            "Expected both initials, both historical confirmations and both new finals")
    for family in INITIALS:
        rows = [row for row in lineage if row["family"] == family]
        require([row["run"] for row in rows] == [INITIALS[family], HISTORY[family], FINALS[family]],
                "Reviewer lineage skips, substitutes or reorders a run")
        first, previous, final = rows
        require(first["role"] == "initial" and first["snapshot"] == config["candidate"]
                and first["rawVerdict"] == "NEEDS FIX" and not first["finalAcceptance"]
                and first["session"] == previous["session"] == final["session"],
                "Initial verdict or original reviewer changed")
        require(previous["role"] == "intermediate" and previous["snapshot"] == PARENT
                and previous["rawVerdict"] == ("CONFIRMED" if family == "claude" else "UNVERIFIED")
                and previous["confirmationAcceptedOnSnapshot"] is (family == "claude")
                and not previous["finalAcceptance"] and previous["priorRun"] is None,
                "Historical confirmation was relabeled or moved")
        require(final["role"] == "final" and final["snapshot"] == candidate
                and final["rawVerdict"] == "CONFIRMED" and final["finalAcceptance"]
                and final["confirmationAcceptedOnSnapshot"] and final["priorRun"] == previous["run"],
                "Final confirmation is not accepted on the exact successor")


def check_proofs(first, second, current, candidate, config):
    require(second["candidate"] == current["parent"] == PARENT
            and first["candidate"] == second["parent"]
            and current["candidate"] == candidate
            and second["priorRevisionProof"]["sha256"] == FIRST_PROOF_SHA
            and current["priorRevisionProof"]["sha256"] == PROOF_SHA
            and current["earlierSignedSourcesAndNonScopedRuntimePreserved"]
            and current["newGuards"][:2] == ["\u672c", "\u5ea6"],
            "Signed revision lineage or preservation differs")
    for item in (first, second, current):
        require(item["status"] == "PASS" and item["initial"] == config["candidate"]
                and item["base"] == config["base"] and not item["memory"]["breach"]
                and item["runtimeEntries"] == 8708 and item["sourceMembersPublishedBeforeBatch"] == 252
                and item["sourceMembersInCandidate"] == 253 and item["linguisticAcceptance"] is False
                and item["publicationAccepted"] is False
                and [row["gate"] for row in item["gates"]] == list(CHECKS),
                "Revision proof, accounting or committed gates differ")


def make_ledger(config, candidate, provenance, provenance_sha, first, second, current):
    ledger = earlier_ledger(config, candidate, provenance, provenance_sha, second, first)
    ledger["runtimeCandidate"] = {key: current[key] for key in
                                  ("contentVersion", "manifestSha256", "runtimeEntries")}
    ledger["review"]["identity"] = (
        "Independent original initials and serial snapshot-specific confirmations. Earlier "
        "CONFIRMED and UNVERIFIED results remain historical; both original reviewers confirmed "
        "the third signed revision.")
    ledger["sourceEvidence"]["reconciliations"].append("batch-123/reconciliation-003/")
    ledger["sourceEvidence"]["signedArtifactSha256"].update(current["signedSourceArtifacts"])
    ledger["sourceEvidence"]["newDictionaryCapturePolicy"] = (
        "Full new third-party captures remain local. Contributor evidence contains attributed "
        "references, original summaries and necessary short phrases, not complete new entries.")
    return ledger


def finalize(candidate):
    config = load_batch(123)
    repo, records = Path(config["repo"]), WS / "scratch-123" / "review"
    closure = repo / "docs" / "n1-reviews" / "batch-123-closure"
    provenance_raw = frozen(closure / "provenance.json")
    provenance = json.loads(provenance_raw)
    proofs_raw = [
        frozen(records / "coordinator-reconciliation-verification-001.json", FIRST_PROOF_SHA),
        frozen(records / "coordinator-reconciliation-verification-002.json", PROOF_SHA),
        frozen(records / "coordinator-reconciliation-verification-003.json"),
    ]
    first, second, current = map(json.loads, proofs_raw)
    check_history(provenance, candidate, config)
    check_proofs(first, second, current, candidate, config)
    require(git(config, "rev-parse", "HEAD").decode().strip() == candidate
            and git(config, "show", "-s", "--format=%P", candidate).decode().strip() == PARENT
            and git(config, "show", "-s", "--format=%G?|%GF|%ae|%ce", candidate).decode().strip()
            == f"G|{SIGNER}|stop-cran@list.ru|stop-cran@list.ru", "Signed successor changed")
    require(not git(config, "diff", "--name-only") and not git(config, "diff", "--cached", "--name-only"),
            "Tracked revision changed")
    untracked = git(config, "ls-files", "--others", "--exclude-standard", "-z").decode("utf-8").split("\0")
    require(all(not path or path.startswith("docs/n1-reviews/batch-123-closure/") for path in untracked),
            "Unrelated untracked files")
    ledger_path = repo / "docs" / "n1-sources" / "batch-123-progress.json"
    previous = git(config, "show", f"{candidate}:docs/n1-sources/batch-123-progress.json")
    old = json.loads(previous)
    require(ledger_path.read_bytes() == previous and old["status"] == "authoring-draft-unreviewed-unpublished"
            and not old["published"] and not old["reviewClosed"] and old["runtimePublished"] is False
            and old["membership"] == ["\u7bc4"]
            and old["accounting"]["publishedPendingRecordsWithCards"] == 252,
            "Unexpected prior progress state")
    artifacts = {"verification/original-progress.json": previous}
    artifacts.update({f"verification/reconciliation-{i:03}.json": raw
                      for i, raw in enumerate(proofs_raw, 1)})
    guard, _ = start_guard("B123 third-revision closure")
    try:
        for path, digest in provenance["recordedFileSha256"].items():
            frozen(closure / path, digest)
            guard.check()
        require(sha(git(config, "show", f"{candidate}:manifest.json")) == current["manifestSha256"],
                "Confirmed manifest changed")
        for index, item, digest in ((1, first, PRIOR_SELECTION_SHA), (2, second, SELECTION_SHA)):
            name = f"coordinator-reconciliation-selection-{index:03}.json"
            raw = frozen(records / name, digest)
            selection = json.loads(raw)
            require(selection["status"] == "PASS" and selection["candidate"] == item["candidate"],
                    "Earlier source proof differs")
            artifacts[f"verification/{name}"] = raw
        source_sets = [first["sourceProof"]["signedArtifacts"], second["sourceProof"]["signedArtifacts"],
                       current["signedSourceArtifacts"]]
        for sources in source_sets:
            for path, digest in sources.items():
                require(sha(git(config, "show", f"{candidate}:{path}")) == digest,
                        f"Signed source changed: {path}")
                guard.check()
        adjudication_raw = frozen(records / "reconciliation-003-source-adjudication.json")
        adjudication = json.loads(adjudication_raw)
        require(adjudication["candidate"] == candidate
                and adjudication["status"] == "READY_FOR_INDEPENDENT_CONFIRMATIONS"
                and adjudication["openClaimIds"] == []
                and set(adjudication["pairDecisions"]) == {f"Q{i}" for i in range(1, 10)},
                "Nine-pair source adjudication is missing or held")
        artifacts["verification/reconciliation-003-source-adjudication.json"] = adjudication_raw
        gates = Path(current["gateSummary"]["path"]).parent
        artifacts["gates/summary.json"] = frozen(gates / "summary.json", current["gateSummary"]["sha256"])
        frozen(current["runner"]["path"], current["runner"]["sha256"])
        for item in current["gates"]:
            name = item["gate"]
            raw = frozen(gates / f"{name}.json", item["receiptSha256"])
            log = frozen(gates / f"{name}.log", item["logSha256"])
            check_gate(json.loads(raw), log, name, current["manifestSha256"],
                       config["repo"], current["runner"]["sha256"])
            artifacts[f"gates/{name}.json"], artifacts[f"gates/{name}.log"] = raw, log
            guard.check()
        for name in ("coordinator-candidate-verification.json", "source-contract.json",
                     "source-selection-verification-001.json", "reconciliation-001-source-adjudication.json",
                     "reconciliation-002-source-adjudication.json", "confirmation-preparation-recovery-001.json",
                     "followup-003-han-source-reference.json"):
            artifacts[f"verification/{name}"] = frozen(records / name)
        for name in ("verify_b123_revision_v2.py", "verify_b123_revision_v3.py", "verify_b123_revision_v4.py",
                     "test_verify_b123_revision_v4.py", "verify_b123_reconciliation_selection.py",
                     "verify_b123_followup_selection.py", "scoped_admission.py", "scoped_confirmation_admission.py",
                     "finalize_b123.py", "test_finalize_b123.py", "finalize_b123_v2.py", "test_finalize_b123_v2.py",
                     "prepare_b123_confirmations_003.py", "test_prepare_b123_confirmations_003.py",
                     "record_publication.py", "test_record_publication.py"):
            artifacts[f"protocol/tools/{name}"] = frozen(Path(__file__).with_name(name))
        artifacts["protocol/guarded-test-v2.py"] = frozen(records / "guarded-test-v2.py")
        artifacts["protocol/superseded-closure-spec-001.json"] = frozen(WS / "scratch-123" / "closure-spec-001.json")
        for name, raw in artifacts.items():
            write_frozen(closure / name, raw)
        freeze_json(closure / "validation-provenance.json", {
            "batch": 123, "candidate": candidate, "reviewClosureSha256": sha(provenance_raw),
            "recordedFileSha256": {name: sha(raw) for name, raw in artifacts.items()}, "publication": "PENDING",
        })
        ledger = make_ledger(config, candidate, provenance, sha(provenance_raw), first, second, current)
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

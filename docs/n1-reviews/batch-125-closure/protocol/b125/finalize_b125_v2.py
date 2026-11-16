"""Close all three B125 corrections and preserve accepted, held and protocol-VOID history."""
import copy
import json
import sys
from pathlib import Path

from common import (CHECKS, TOOLS, WS, freeze_json, frozen, git, json_bytes, load_batch,
                    require, sha, start_guard, write_frozen)
from closure_quarantine_v2 import STATUS
from b125_followup_lineage import check_history as check_followup_history
from finalize_b125 import check_proofs as check_first_two

SECOND = "dbca5192a4308dc6e8d954af37775e0fcd1986ea"
CANDIDATE = "f2d2ddf87a0f1a721920241a88a61e28a98fa6f2"
FIRST = "49d0b00d438969b157e739360f8639c6a9b0d950"
SIGNER = "D4C9A275A218AF747B787AFA9D94B9D311BD26A7"
PROOFS = {
    1: "98ef2e3b7edbe9eb2b4081cba9e547c215ba644ad8bdb40cfbf3856689d695a8",
    2: "ab5977465cacf873bd565e2761a1bafbdfcc1d044c8bf7ae06a7f214660e196d",
    3: "b0429c6363d34443b3d7bc9e3d385c2b22d6c0ea40c8fc4a49f2306e15687ff5",
}
INITIALS = {"claude": "N1-B125-CLAUDE-001", "gpt": "N1-B125-GPT-002"}
FINALS = {family: f"N1-B125-{family.upper()}-CONFIRM-002" for family in INITIALS}
EXCLUDED = "N1-B125-GPT-001"
QUARANTINE_SHA = "e9d7a15c40d4150145fa097fb67d00ce94dda4576789903f42064a2c2932195f"


def check_history(provenance, config):
    check_followup_history(provenance, config, CANDIDATE)


def check_proofs(first, second, current, config):
    check_first_two(first, second, config)
    require(current["candidate"] == CANDIDATE and current["parent"] == SECOND
            and current["originalCandidate"] == config["candidate"]
            and current["status"] == "PASS" and current["batch"] == 125
            and current["runtimeEntries"] == 8712
            and current["signature"] == second["signature"]
            and current["additionalGuards"] == list("\u4f4e\u77ed\u5c0f\u5bb9")
            and current["unrelatedRuntimeAndFrozenMetadataPreserved"] is True
            and current["runtimeChanged"] == ["kanji/\u4fb5.md"]
            and current["parentInventoryCards"] == 1245
            and current["exactMetadataAndPracticeMatches"] == []
            and current["explicitReadingReplayByteIdentical"] is True
            and current["reviewAccepted"] is False and current["confirmationAccepted"] is False
            and set(current["gates"]) == {"author", "committed"},
            "Signed S1 source/inventory/runtime proof differs")
    for gates in current["gates"].values():
        require(len(gates) == len(CHECKS) and {row["gate"] for row in gates} == set(CHECKS),
                "Incomplete S1 correction gate inventory")


def make_ledger(old, config, provenance, provenance_sha, current):
    require(old["status"] == "author-draft-not-reviewed-or-published"
            and old["membership"] == ["\u4fb5"] and old["sourceRows"] == [48]
            and old["reviewClosed"] == old["published"] == [] and old["runtimePublished"] is False
            and old["accounting"] == {
                "frozenPendingRecords": 1228, "publishedPendingRecordsWithCards": 254,
                "publishedN1Additions": 248, "n2Placements": 6, "undelivered": 974,
                "overallN1TaskComplete": False,
            }, "Unexpected prior ledger or accounting")
    ledger = copy.deepcopy(old)
    ledger.update(initialSnapshot=config["candidate"], reviewedSnapshot=CANDIDATE,
                  status="textual-review-closed-publication-pending", reviewClosed=["\u4fb5"])
    ledger["accounting"].update(reviewClosedPendingRecordsWithCards=255, notStarted=973)
    ledger["runtimeCandidate"] = {key: current[key] for key in
                                  ("manifestSha256", "contentVersion", "runtimeEntries")}
    ledger["review"] = {
        "status": "closed-with-disclosed-limits", "finalRuns": provenance["finalRuns"],
        "intermediateRuns": provenance["intermediateRuns"], "closure": "../n1-reviews/batch-125-closure/provenance.json",
        "closureProvenanceSha256": provenance_sha, "remainingActionableFindings": [],
        "remainingConsequentialClaims": [], "historicalReportsPreserved": True,
        "excludedInitialRuns": [EXCLUDED],
        "identity": "Independent Claude001 and replacement GPT002 initials, followed by two isolated "
                    "original-reviewer second confirmations on the third signed correction; both first "
                    "confirmations retain their accepted/held historical states. GPT001 is "
                    "preserved only as excluded coordinator phase-two delivery VOID evidence.",
    }
    ledger["correctionSources"] = ["batch-125-reconciliation/", "batch-125-reconciliation-002/",
                                   "batch-125-reconciliation-003/"]
    ledger["limits"] = [
        "Bounded textual and host review, not exhaustive linguistic or arbitrary-pool acceptance.",
        "Nineteen added direct guards conservatively protect broad-English choices, not universal "
        "synonymy, equal frequency or transitive exclusions.",
        "No new Kotlin, native, phone, installed-APK or fallback-rendering acceptance.",
        "Publication, CI and exact served ZIP remain pending; review closure is not delivery.",
        "All raw reports and limits remain; GPT001 and historical Q4/Q9 and S1 holds are not relabelled.",
        "The positive appearance-source branch is scoped against current titles/readings; ordinary "
        "frequency, arbitrary/future pools and multi-borrow safety are not established.",
        "Complete external captures and mixed segments containing them remain local.",
    ]
    return ledger


def finalize(archive_path):
    config = load_batch(125)
    repo, records = Path(config["repo"]), WS / "scratch-125" / "review"
    closure = repo / "docs" / "n1-reviews" / "batch-125-closure"
    provenance_raw = frozen(closure / "provenance.json")
    provenance = json.loads(provenance_raw)
    check_history(provenance, config)
    proof_raw = {number: frozen(records / f"reconciliation-{number:03}-independent-proof.json", digest)
                 for number, digest in PROOFS.items()}
    first, second, current = [json.loads(proof_raw[number]) for number in (1, 2, 3)]
    check_proofs(first, second, current, config)
    archive_raw = frozen(archive_path)
    archive = json.loads(archive_raw)
    require(archive["status"] == "PASS" and archive["candidate"] == CANDIDATE
            and archive["provenanceSha256"] == sha(provenance_raw) and len(archive["chains"]) == 10,
            "Actual accepted and excluded archives were not verified")
    require(git(config, "rev-parse", "HEAD").decode().strip() == CANDIDATE
            and not git(config, "diff", "--name-only")
            and not git(config, "diff", "--cached", "--name-only"), "Tracked candidate changed")
    untracked = git(config, "ls-files", "--others", "--exclude-standard", "-z").decode().split("\0")
    require(all(not path or path.startswith("docs/n1-reviews/batch-125-closure/") for path in untracked),
            "Unrelated untracked files")
    for commit, parent in ((FIRST, config["candidate"]), (SECOND, FIRST), (CANDIDATE, SECOND)):
        require(git(config, "show", "-s", "--format=%P%n%G?|%GF|%ae|%ce", commit).decode().strip()
                == f"{parent}\nG|{SIGNER}|stop-cran@list.ru|stop-cran@list.ru", "Signed lineage differs")
    require(sha(git(config, "show", f"{CANDIDATE}:manifest.json")) == current["manifestSha256"],
            "Confirmed manifest differs")
    ledger_path = repo / "docs" / "n1-sources" / "batch-125-progress.json"
    previous = git(config, "show", f"{CANDIDATE}:docs/n1-sources/batch-125-progress.json")
    require(ledger_path.read_bytes() == previous, "Progress changed")
    ledger = make_ledger(json.loads(previous), config, provenance, sha(provenance_raw), current)
    artifacts = {
        "verification/original-progress.json": previous,
        "verification/reconciliation-001.json": proof_raw[1],
        "verification/reconciliation-002.json": proof_raw[2],
        "verification/reconciliation-003.json": proof_raw[3],
        "verification/s1-parent-inventory.json": frozen(
            WS / "scratch-125" / "reconciliation-003-inventory-002" / "card-inventory.json",
            current["parentInventorySha256"]),
        "verification/actual-archive.json": archive_raw,
        "verification/confirmation-recovery.json": frozen(
            records / "confirmation-001-recovery-verification.json",
            "ef2d222ccb90b15488a1a65226b7151a3f6b06c4faf8ea19bafedec425676e5e"),
    }
    guard, _ = start_guard("B125 closure finalization")
    try:
        for path, digest in provenance["recordedFileSha256"].items():
            frozen(closure / path, digest)
            guard.check()
        for number, proof in ((1, first), (2, second), (3, current)):
            for mode, gates in proof["gates"].items():
                directory = WS / "scratch-125" / (proof["gateSets"][mode]["directory"] if number == 3
                                               else f"reconciliation-{number:03}-{mode}-gates-001")
                prefix = f"gates/reconciliation-{number:03}/{mode}"
                summary_raw = frozen(directory / "summary.json")
                summary = json.loads(summary_raw)
                require(summary["batch"] == 125 and summary["status"] == "PASS"
                        and summary["manifestSha256"] == proof["manifestSha256"]
                        and summary["head"] == (proof["parent"] if mode == "author" else proof["candidate"])
                        and summary["parent"] == proof["parent"]
                        and set(summary["checks"]) == set(CHECKS), "Gate summary differs")
                artifacts[f"{prefix}/summary.json"] = summary_raw
                for row in gates:
                    name = row["gate"]
                    receipt = frozen(directory / f"{name}.json", row["receiptSha256"])
                    log = frozen(directory / f"{name}.log", row["logSha256"])
                    value = json.loads(receipt)
                    require(value["exitCode"] == value["childExitCodeAfterCleanup"] == 0
                            and not value["memory"]["breach"] and value["logSha256"] == sha(log),
                            "Correction gate receipt differs")
                    artifacts[f"{prefix}/{name}.json"] = receipt
                    artifacts[f"{prefix}/{name}.log"] = log
                    guard.check()
        for name in ("finalize_b125_v2.py", "test_finalize_b125_v2.py", "prepare_b125_finalizer_v2.py",
                     "b125_followup_lineage.py", "test_b125_followup_lineage.py",
                     "verify_b125_reconciliation_003.py", "test_verify_b125_reconciliation_003.py",
                     "prepare_b125_confirmations_002.py", "test_prepare_b125_confirmations_002.py",
                     "finalize_b125.py", "test_finalize_b125.py", "verify_b125_reconciliation_001.py",
                     "verify_b125_reconciliation_002.py", "prepare_b125_confirmations.py",
                     "test_prepare_b125_confirmations.py", "scoped_confirmation_admission.py",
                     "scoped_admission.py"):
            artifacts[f"protocol/b125/{name}"] = frozen(TOOLS / name)
        for relative, binding in current["evidenceReceipts"].items():
            source = WS / "scratch-125" / relative
            prefix = "evidence/s1/" + relative.removesuffix(".json")
            artifacts[prefix + ".json"] = frozen(source, binding["receiptSha256"])
            artifacts[prefix + ".log"] = frozen(source.with_suffix(".log"), binding["logSha256"])
        for source in sorted((WS / "scratch-125" / "reconciliation-003-scripts").glob("*.py")):
            artifacts["protocol/b125/reconciliation-003/" + source.name] = frozen(source)
        for name in ("reconciliation-001-gates.py", "reconciliation-002-gates.py"):
            artifacts[f"protocol/b125/{name}"] = frozen(WS / "scratch-125" / name)
        artifacts["protocol/b125/bounded-correction-runner.py"] = frozen(
            WS / "scratch-124" / "run-reconciliation-002-checks.py")
        artifacts["protocol/b125/source-record-verifier.py"] = frozen(
            WS / "scratch-124" / "review" / "verify-source-records.py")
        for name, raw in artifacts.items():
            require(name not in provenance["recordedFileSha256"], "Duplicate closure artifact")
            write_frozen(closure / name, raw)
            guard.check()
        freeze_json(closure / "validation-provenance.json", {
            "batch": 125, "candidate": CANDIDATE, "reviewClosureSha256": sha(provenance_raw),
            "recordedFileSha256": {name: sha(raw) for name, raw in artifacts.items()}, "publication": "PENDING",
        })
        require(ledger_path.read_bytes() == previous, "Progress changed during finalization")
        ledger_path.chmod(0o644)
        ledger_path.write_bytes(json_bytes(ledger))
        require(ledger_path.read_bytes() == json_bytes(ledger), "Ledger readback differs")
        ledger_path.chmod(0o444)
        print(json.dumps({"candidate": CANDIDATE, "status": ledger["status"],
                          "ledgerSha256": sha(json_bytes(ledger)), "published": False}))
    finally:
        require(not guard.finish()["breach"], "Finalization RAM guard breached")


if __name__ == "__main__":
    finalize(Path(sys.argv[1]))

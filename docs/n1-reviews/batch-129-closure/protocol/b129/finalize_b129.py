"""Finalize accepted B129 review evidence; delivery remains a separate gate."""
import json
import sys
from pathlib import Path

from common import (CHECKS, TOOLS, WS, freeze_json, frozen, git, json_bytes, load_batch,
                    require, sha, start_guard, write_frozen)

CANDIDATE = "1b27107972311bdb9f485d0dc4879670a76cdc43"
SIGNER = "D4C9A275A218AF747B787AFA9D94B9D311BD26A7"
MEMBERS = ["\u8309", "\u7d79", "\u8679"]
INITIALS = {f: f"N1-B129-{f.upper()}-001" for f in ("claude", "gpt")}
FINALS = {"claude": "N1-B129-CLAUDE-REPLACEMENT-CONFIRM-004",
          "gpt": "N1-B129-GPT-CONFIRM-003"}
REVIEWERS = {"claude": "6b850696-09e6-4774-b35a-09d67befffe6",
             "gpt": "8d91db13-ecbb-4d48-8888-78c682edec78"}
REPLACEMENT = "711353da-a1bd-46a3-bb47-8daa9ac4176b"
ROOT = WS / "scratch-129" / "review"
PROOF_SHA = "3378793385dbd2a8d895f60aab5d01d7d9b5e33dbb50e2d4e4484b7a7b9d3029"


def check_history(provenance, candidate, config):
    require(candidate == CANDIDATE and provenance["batch"] == 129
            and provenance["reviewedSnapshot"] == candidate
            and provenance["initialSnapshot"] == config["candidate"]
            and provenance["base"] == config["base"]
            and provenance["members"] == config["members"] == MEMBERS
            and provenance["publication"] == "PENDING"
            and provenance["excludedInitialRuns"] == provenance["intermediateRuns"] == []
            and set(provenance["finalRuns"]) == set(FINALS.values())
            and len(provenance["finalRuns"]) == 2, "Unexpected closure scope")
    rows = provenance["reviewLineage"]
    require(len(rows) == len({row["run"] for row in rows}) == 4, "Four accepted review runs required")
    for family in INITIALS:
        selected = [row for row in rows if row["family"] == family]
        require([row["run"] for row in selected] == [INITIALS[family], FINALS[family]],
                "Family lineage differs")
        initial, final = selected
        require(initial["role"] == "initial" and initial["snapshot"] == config["candidate"]
                and initial["session"] == REVIEWERS[family]
                and initial["rawVerdict"] == ("CLEAN" if family == "claude" else "NEEDS FIX")
                and not initial["finalAcceptance"] and not initial["confirmationAcceptedOnSnapshot"],
                "Initial report relabelled")
        require(final["role"] == "final" and final["snapshot"] == candidate
                and final["rawVerdict"] == "CONFIRMED" and final["priorRun"] is None
                and final["finalAcceptance"] and final["confirmationAcceptedOnSnapshot"],
                "Final report not accepted on candidate")
        if family == "claude":
            require(final["session"] == REPLACEMENT
                    and final["reviewerOrigin"] == "fresh-context-replacement"
                    and final["originalSession"] == REVIEWERS[family]
                    and final["replacementFor"] == "N1-B129-CLAUDE-CONFIRM-003",
                    "Replacement attribution differs")
        else:
            require(final["session"] == REVIEWERS[family]
                    and final["reviewerOrigin"] == "original", "Original GPT identity differs")
    held = provenance["excludedConfirmationRuns"]
    require(len(held) == 1 and held[0]["run"] == "N1-B129-CLAUDE-CONFIRM-003"
            and held[0]["status"] == "VOID_CONTEXT_COMPACTION"
            and not held[0]["reviewEvidenceAccepted"] and not held[0]["confirmationAccepted"]
            and not held[0]["reportWritten"] and held[0]["linguisticVerdict"] is None,
            "Executed failed confirmation was lost or relabelled")


def check_proof(proof, candidate, config):
    require(proof["batch"] == 129 and proof["status"] == "PASS_MECHANICAL_ONLY"
            and proof["candidate"] == candidate == CANDIDATE
            and proof["parent"] == config["candidate"] and proof["base"] == config["base"]
            and proof["signature"] == {"fingerprint": SIGNER, "ownerVerified": True}
            and proof["runtimeEntries"] == 8724
            and proof["runtimeChanged"] == ["kanji/\u7d79.md", "kanji/\u8679.md"]
            and not proof["reviewAccepted"] and not proof["publicationAccepted"]
            and not proof["memory"]["breach"], "Mechanical proof differs")
    require(set(proof["gateSets"]) == {"author", "committed"}, "Missing host gates")
    for gates in proof["gateSets"].values():
        require(len(gates["gates"]) == len(CHECKS)
                and {item["gate"] for item in gates["gates"]} == set(CHECKS), "Gate set differs")


def make_ledger(old, config, provenance, provenance_sha, proof):
    require(old["status"] == "local-authoring-candidate"
            and [row["kanji"] for row in old["members"]] == MEMBERS
            and [row["sourceRow"] for row in old["members"]] == [931, 841, 967]
            and old["deliveredSourceMembers"] == 258 and old["undeliveredSourceMembers"] == 970
            and old["localDraftsNotDelivered"] == 3, "Author progress differs")
    return {
        "batch": 129, "base": config["base"], "governingIssue": old["governingIssue"],
        "status": "textual-review-closed-publication-pending", "membership": MEMBERS,
        "sourceRows": [931, 841, 967], "sourceMembers": old["members"],
        "initialSnapshot": config["candidate"], "reviewedSnapshot": CANDIDATE,
        "reviewClosed": MEMBERS, "published": [], "runtimePublished": False,
        "accounting": {"frozenPendingRecords": 1228, "publishedPendingRecordsWithCards": 258,
                       "publishedN1Additions": 252, "n2Placements": 6, "undelivered": 970,
                       "reviewClosedPendingRecordsWithCards": 261, "localUnreviewedDrafts": 0,
                       "notStarted": 967, "overallN1TaskComplete": False},
        "runtimeCandidate": {key: proof[key] for key in
                             ("manifestSha256", "contentVersion", "runtimeEntries")},
        "review": {"status": "closed-with-disclosed-limits", "finalRuns": provenance["finalRuns"],
                   "intermediateRuns": [], "closure": "../n1-reviews/batch-129-closure/provenance.json",
                   "closureProvenanceSha256": provenance_sha, "remainingActionableFindings": [],
                   "remainingConsequentialClaims": [], "historicalReportsPreserved": True,
                   "identity": "Qualified Claude CLEAN and GPT NEEDS FIX initials remain unchanged. "
                               "Original GPT and disclosed fresh Claude replacement confirmed. "
                               "Original Claude confirmation003 remains executed VOID, not accepted."},
        "correctionSources": ["batch-129-reconciliation/"],
        "originalAuthorProgress": "../n1-reviews/batch-129-closure/verification/original-progress.json",
        "limits": [
            "Bounded textual/host review, not exhaustive linguistic or arbitrary/custom-pool acceptance.",
            "No new Kotlin/native/device, installed-APK, image, font-rendering or stroke-geometry acceptance.",
            "Six latent reading collisions and separate one-additional-holder risks for 橋/攻/責 remain.",
            "Historical gloss allocation and noose/swing source discrepancy remain explicitly qualified.",
            "Optional 競 guard deferred; no transitive guard or universal zero-exposure inference.",
            "Publication, CI and exact served ZIP remain pending; review closure is not delivery.",
            "Complete external captures and co-located chain material remain local.",
        ],
    }


def finalize():
    config = load_batch(129)
    repo = Path(config["repo"])
    closure = repo / "docs" / "n1-reviews" / "batch-129-closure"
    provenance_raw = frozen(closure / "provenance.json")
    provenance = json.loads(provenance_raw)
    proof_raw = frozen(ROOT / "revision-evidence-proof-001" / "verification.json", PROOF_SHA)
    proof = json.loads(proof_raw)
    check_history(provenance, CANDIDATE, config)
    check_proof(proof, CANDIDATE, config)
    archive_raw = frozen(ROOT / "closure-archive-verification-001.json")
    archive = json.loads(archive_raw)
    require(archive["status"] == "PASS" and archive["candidate"] == CANDIDATE
            and archive["provenanceSha256"] == sha(provenance_raw)
            and len(archive["chains"]) == 7, "Accepted and held chains not verified")
    guard, _ = start_guard("B129 closure finalization")
    try:
        require(git(config, "rev-parse", "HEAD").decode().strip() == CANDIDATE
                and git(config, "show", "-s", "--format=%P%n%G?|%GF|%ae|%ce", CANDIDATE).decode().strip()
                == f"{config['candidate']}\nG|{SIGNER}|stop-cran@list.ru|stop-cran@list.ru"
                and not git(config, "diff", "--name-only")
                and not git(config, "diff", "--cached", "--name-only"), "Signed candidate changed")
        untracked = git(config, "ls-files", "--others", "--exclude-standard", "-z").decode().split("\0")
        require(all(not path or path.startswith("docs/n1-reviews/batch-129-closure/")
                    for path in untracked), "Unrelated untracked paths")
        require(sha(git(config, "show", f"{CANDIDATE}:manifest.json")) == proof["manifestSha256"],
                "Reviewed manifest differs")
        for path, digest in provenance["recordedFileSha256"].items():
            frozen(closure / path, digest)
            guard.check()
        progress = repo / "docs" / "n1-sources" / "batch-129-progress.json"
        previous = git(config, "show", f"{CANDIDATE}:docs/n1-sources/batch-129-progress.json")
        require(progress.read_bytes() == previous, "Author progress changed")
        ledger = make_ledger(json.loads(previous), config, provenance, sha(provenance_raw), proof)
        artifacts = {"verification/original-progress.json": previous,
                     "verification/reconciliation-001.json": proof_raw,
                     "verification/actual-archive.json": archive_raw}
        for key in ("runtimeProof", "sourceProof"):
            item = proof[key]
            artifacts[f"verification/{key}.json"] = frozen(item["path"], item["sha256"])
        for relative, item in proof["capturedEvidence"].items():
            artifacts["verification/captured/" + relative] = frozen(item["path"], item["sha256"])
        for name in ("closure-v2-derivation.json", "closure-v3-derivation.json",
                     "closure-spec-001.json", "confirmation-003-preparation.json",
                     "confirmation-003-evidence-bindings.json", "context-replacement-tooling-001.json",
                     "claude-replacement-preparation-004.json", "noose-readonly-capture-001.json",
                     "N1-B129-CLAUDE-001-citation-erratum.json"):
            artifacts["verification/tooling/" + name] = frozen(ROOT / name)
        for name in ("finalize_b129.py", "test_finalize_b129.py", "run_b129_closure_checks.py"):
            artifacts["protocol/b129/" + name] = frozen(TOOLS / name)
        noose = ROOT / "confirm" / f"{FINALS['claude']}-noose-serialization.json"
        artifacts["verification/noose-serialization.json"] = frozen(noose)
        executions = {
            "closure-v2-preparation-execution-001": 1, "closure-v2-tests-execution-002": 0,
            "closure-v3-preparation-execution-001": 0, "replacement-claude-final-execution-004": 0,
            "replacement-claude-acceptance-execution-004": 1,
            "replacement-claude-acceptance-execution-005": 0,
            "closure-archive-execution-001": 1, "closure-archive-execution-002": 0,
            "closure-archive-verification-execution-001": 0,
        }
        for name, code in executions.items():
            directory = ROOT / name
            receipt_raw = (directory / "receipt.json").read_bytes()
            receipt = json.loads(receipt_raw)
            log = (directory / "output.log").read_bytes()
            require(sha(log) == receipt["logSha256"] and receipt["exitCode"] == code
                    and receipt["childExitCodeAfterCleanup"] == code
                    and not receipt["cleanupError"] and not receipt["memory"]["breach"],
                    "Execution provenance differs: " + name)
            for filename, raw in (("receipt.json", receipt_raw), ("output.log", log)):
                artifacts[f"verification/executions/{name}/{filename}"] = raw
        require(not set(artifacts) & set(provenance["recordedFileSha256"]), "Duplicate artifacts")
        for name, raw in artifacts.items():
            write_frozen(closure / name, raw)
            guard.check()
        freeze_json(closure / "validation-provenance.json", {
            "batch": 129, "candidate": CANDIDATE, "reviewClosureSha256": sha(provenance_raw),
            "recordedFileSha256": {name: sha(raw) for name, raw in artifacts.items()},
            "publication": "PENDING",
        })
        require(progress.read_bytes() == previous, "Progress changed during finalization")
        progress.chmod(0o644)
        progress.write_bytes(json_bytes(ledger))
        require(progress.read_bytes() == json_bytes(ledger), "Progress readback differs")
        progress.chmod(0o444)
        print(json.dumps({"candidate": CANDIDATE, "status": ledger["status"], "published": False}))
    finally:
        require(not guard.finish()["breach"], "Closure RAM breach")


if __name__ == "__main__":
    finalize()

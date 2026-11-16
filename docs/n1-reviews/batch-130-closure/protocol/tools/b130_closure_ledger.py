"""Build B130 closure accounting after separate source, archive and signature checks.

Pure ledger construction does not write a closure or accept a candidate. The
finalizer must bind the actual confirmations and mechanical proofs before use.
"""
import copy
import json
import re

from common import frozen, require, sha
from verify_b130_revision_runtime_v2 import BASE, GPT_OPEN, INITIAL_SHA, MEMBERS, PARENT, ROOT

REVIEWERS = {
    "claude": "b6bd4627-73cc-452b-9a56-2b9407c9a0cf",
    "gpt": "827ecfff-5750-4a20-baa7-7f0952d31ca1",
}
EXCLUDED = {
    "N1-B130-CLAUDE-001": "HOLD_CONTEXT_COMPACTED",
    "N1-B130-CLAUDE-002": "VOID_PREMATURE_SELECTION",
    "N1-B130-CLAUDE-003": "VOID_COORDINATOR_PHASE2_MESSAGE_MISMATCH",
}
SOURCE_ROWS = [191, 419, 879]


def initial_history():
    history = {}
    for family, digest in INITIAL_SHA.items():
        run = f"N1-B130-{family.upper()}-004"
        accepted = json.loads(frozen(ROOT / f"{run}-acceptance.json", digest))
        item = accepted["adjudication"]
        adjudication = json.loads(frozen(item["path"], item["sha256"]))
        expected = GPT_OPEN if family == "gpt" else []
        require(accepted["run"] == adjudication["run"] == run
                and accepted["candidate"] == adjudication["candidate"] == PARENT
                and accepted["reviewAccepted"] is True
                and accepted["verdict"] == adjudication["verdict"] == "NEEDS FIX"
                and adjudication["openClaimIds"] == expected
                and adjudication["publicationAccepted"] is False,
                "Historical initial evidence changed")
        history[family] = {"run": run, "acceptanceSha256": digest,
                           "adjudicationSha256": item["sha256"],
                           "openClaimIds": list(expected)}
    return history


def check_history(provenance, candidate, config, finals):
    require(re.fullmatch(r"[0-9a-f]{40}", candidate) and candidate != PARENT
            and config["batch"] == provenance["batch"] == 130
            and config["candidate"] == provenance["initialSnapshot"] == PARENT
            and config["base"] == provenance["base"] == BASE
            and config["members"] == provenance["members"] == MEMBERS
            and provenance["reviewedSnapshot"] == candidate
            and provenance["publication"] == "PENDING"
            and provenance["intermediateRuns"] == []
            and not provenance.get("excludedConfirmationRuns"),
            "Unexpected B130 closure scope or new confirmation history")
    history = initial_history()
    require(len(finals) == 2 and {item["family"] for item in finals} == set(REVIEWERS)
            and len({item["run"] for item in finals}) == 2
            and len(provenance["finalRuns"]) == 2
            and set(provenance["finalRuns"]) == {item["run"] for item in finals},
            "Two distinct family confirmations required")
    rows = provenance["reviewLineage"]
    require(len(rows) == len({row["run"] for row in rows}) == 4
            and {row["family"] for row in rows} == set(REVIEWERS),
            "Unexpected accepted review lineage")
    for family, session in REVIEWERS.items():
        selected = [row for row in rows if row["family"] == family]
        accepted = next(item for item in finals if item["family"] == family)
        require(len(selected) == 2, "Initial and final review required for each family")
        initial, final = selected
        require(initial["run"] == history[family]["run"]
                and initial["role"] == "initial" and initial["snapshot"] == PARENT
                and initial["session"] == session and initial["rawVerdict"] == "NEEDS FIX"
                and initial["priorRun"] is None
                and initial["finalAcceptance"] is False
                and initial["confirmationAcceptedOnSnapshot"] is False,
                "Initial evidence was relabelled")
        require(re.fullmatch(rf"N1-B130-{family.upper()}-CONFIRM-\d{{3}}", accepted["run"])
                and accepted["batch"] == 130 and accepted["candidate"] == candidate
                and accepted["verdict"] == "CONFIRMED"
                and accepted["confirmationAccepted"] is True and accepted["openClaimIds"] == []
                and final["run"] == accepted["run"] and final["role"] == "final"
                and final["snapshot"] == candidate and final["session"] == session
                and final["rawVerdict"] == "CONFIRMED" and final["priorRun"] is None
                and final["finalAcceptance"] is True
                and final["confirmationAcceptedOnSnapshot"] is True,
                "Final confirmation is not accepted on this candidate by its original reviewer")
    held = provenance["excludedInitialRuns"]
    require(len(held) == 3 and {row["run"] for row in held} == set(EXCLUDED),
            "All three excluded initials must remain recorded")
    for row in held:
        raw = frozen(ROOT / f"{row['run']}-hold.json")
        original = json.loads(raw)
        require(row["status"] == original["status"] == EXCLUDED[row["run"]]
                and row["session"] == original["session"]
                and row["snapshot"] == original["candidate"] == PARENT
                and row["holdSha256"] == sha(raw)
                and row["reviewAccepted"] is False and row["finalAcceptance"] is False,
                "Excluded initial was changed or accepted")
    return history


def make_ledger(old, config, provenance, provenance_sha, runtime, finals):
    candidate = runtime["candidate"]
    history = check_history(provenance, candidate, config, finals)
    require(re.fullmatch(r"[0-9a-f]{64}", provenance_sha)
            and runtime["batch"] == 130 and runtime["status"] == "PASS_RUNTIME_ONLY"
            and runtime["parent"] == PARENT and runtime["base"] == BASE
            and runtime["runtimeEntries"] == 8730
            and runtime["reviewAccepted"] is False and runtime["publicationAccepted"] is False
            and runtime["claimResolutionAccepted"] is False
            and runtime["initialOpenClaimIds"] == {"claude": [], "gpt": GPT_OPEN}
            and not runtime["memory"]["breach"],
            "Runtime evidence or its semantic boundary changed")
    require(old["batch"] == 130 and old["base"] == BASE
            and old["status"] == "local-unreviewed-author-candidate"
            and old["members"] == MEMBERS and old["sourceRows"] == SOURCE_ROWS
            and old["frozenTotal"] == 1228 and old["publishedDelivered"] == 261
            and old["undelivered"] == 967 and old["localUnpublishedDrafts"] == 3
            and old["deliveryNotIncremented"] is True,
            "Original B130 progress differs")
    return {
        "batch": 130, "base": BASE, "governingIssue": 60,
        "status": "textual-review-closed-publication-pending",
        "membership": list(MEMBERS), "sourceRows": list(SOURCE_ROWS),
        "supports": copy.deepcopy(old["supports"]),
        "initialSnapshot": PARENT, "reviewedSnapshot": candidate,
        "reviewClosed": list(MEMBERS), "published": [], "runtimePublished": False,
        "accounting": {
            "frozenPendingRecords": 1228, "publishedPendingRecordsWithCards": 261,
            "publishedN1Additions": 255, "n2Placements": 6, "undelivered": 967,
            "reviewClosedPendingRecordsWithCards": 264, "localUnreviewedDrafts": 0,
            "notStarted": 964, "overallN1TaskComplete": False,
        },
        "runtimeCandidate": {key: runtime[key] for key in
                             ("manifestSha256", "contentVersion", "runtimeEntries")},
        "review": {
            "status": "closed-with-disclosed-limits",
            "finalRuns": list(provenance["finalRuns"]), "intermediateRuns": [],
            "closure": "../n1-reviews/batch-130-closure/provenance.json",
            "closureProvenanceSha256": provenance_sha,
            "remainingActionableFindings": [], "remainingConsequentialClaims": [],
            "historicalReportsPreserved": True, "initialHistory": history,
            "excludedInitialRuns": [
                {key: row[key] for key in ("run", "status", "holdSha256")}
                for row in provenance["excludedInitialRuns"]
            ],
            "identity": "Both attempt004 initials remain NEEDS FIX. Their original reviewers "
                        "confirmed the revised snapshot separately. The 24 GPT initial questions "
                        "remain historical evidence; final acceptance does not rewrite them. "
                        "Excluded Claude001/002/003 remain unaccepted.",
        },
        "correctionSources": ["batch-130-reconciliation/"],
        "originalAuthorProgress": "../n1-reviews/batch-130-closure/verification/original-progress.json",
        "originalAuthorWarnings": copy.deepcopy(old["warnings"]),
        "limits": [
            "Bounded textual/host review, not exhaustive linguistic or arbitrary/custom-pool acceptance.",
            "No new native/device, installed-APK, image, font-rendering or stroke-geometry acceptance.",
            "Latent readings and multiple-borrow-pool risks remain outside tested-pool acceptance.",
            "Historical forms, dictionary disagreements and broad-family sense allocations remain qualified.",
            "Every initial and final report's recorded limits remain applicable; closure does not erase them.",
            "Complete external captures and co-located chain material remain local.",
            "Publication, CI and exact served ZIP remain pending; review closure is not delivery.",
        ],
    }

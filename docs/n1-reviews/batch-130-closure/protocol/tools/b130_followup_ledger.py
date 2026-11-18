"""Build B130 closure accounting after separate source, archive and signature checks.

Pure ledger construction does not write a closure or accept a candidate. The
finalizer must bind the actual confirmations and mechanical proofs before use.
"""
import copy
import json
import re

from common import frozen, require, sha
from b130_fresh_closure_history import check_fresh_history
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


from b130_followup_closure_history import check_history, PREVIOUS, historical_confirmations


def make_ledger(old, config, provenance, provenance_sha, runtime, finals):
    candidate = runtime["candidate"]
    history = check_history(provenance, candidate, config, finals)
    require(re.fullmatch(r"[0-9a-f]{64}", provenance_sha)
            and runtime["batch"] == 130 and runtime["status"] == "PASS_RUNTIME_ONLY"
            and runtime["parent"] == PREVIOUS and runtime["base"] == BASE
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
            "finalRuns": list(provenance["finalRuns"]),
            "intermediateRuns": list(provenance["intermediateRuns"]),
            "historicalConfirmations": [
                {key: row[key] for key in ("run", "family", "session", "candidate",
                                           "verdict", "confirmationAccepted", "openClaimIds")}
                for row in historical_confirmations()
            ],
            "preparedOnlyConfirmationRuns": copy.deepcopy(provenance["preparedOnlyConfirmationRuns"]),
            "confirmationOrigins": copy.deepcopy(provenance["confirmationOrigins"]),
            "closure": "../n1-reviews/batch-130-closure/provenance.json",
            "closureProvenanceSha256": provenance_sha,
            "remainingActionableFindings": [], "remainingConsequentialClaims": [],
            "historicalReportsPreserved": True, "initialHistory": history,
            "excludedInitialRuns": [
                {key: row[key] for key in ("run", "status", "holdSha256")}
                for row in provenance["excludedInitialRuns"]
            ],
            "identity": "Both attempt004 initials remain NEEDS FIX, attributed to their original sessions. "
                        "The same fresh sessions separately confirmed the later delta. Claude002 remains "
                        "accepted only on its earlier snapshot; GPT002 remains valid UNVERIFIED "
                        "evidence with D18 open on that snapshot. "
                        "Original confirmation001 preparations remain unexecuted, not failed. "
                        "The 24 GPT initial questions "
                        "remain historical evidence; final acceptance does not rewrite them. "
                        "Excluded Claude001/002/003 remain unaccepted.",
        },
        "publicationGates": ["Owner-signed publication", "CI", "Exact served ZIP/runtime equality"],
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
        ],
    }

"""Build the B134 review-closed ledger without granting publication credit."""
import json

from b134_review_history import bound, validate_history, validate_resolution
from common import json_bytes, require, sha
from record_b130_publication import delivery_accounting
from run_b134_closure_checks import BASE, BATCH, CANDIDATE, MEMBERS

COUNTS = {
    "frozenPendingRecords": 1228,
    "publishedPendingRecordsWithCards": 271,
    "publishedN1Additions": 265,
    "n2Placements": 6,
    "undelivered": 957,
}


def validate_archived_resolution(closure, read, original_claims):
    ref = closure["resolution"]
    bound(ref, closure["recordedFileSha256"])
    raw = read(ref["path"], ref["sha256"])
    require(sha(raw) == ref["sha256"], "Archived claim resolution bytes differ")
    validate_resolution(json.loads(raw), closure, closure["reviewedSnapshot"], original_claims)


def validate_progress(ledger, reviewed, manifest, closure_raw):
    closure = json.loads(closure_raw)
    validate_history(closure, reviewed)
    checks = closure["publicationChecks"]
    require(checks["uuidFindings"] == checks["externalWindowFindings"] == 0,
            "Closure has unresolved publication-retention findings")
    require(ledger["batch"] == BATCH and ledger["members"] == MEMBERS
            and ledger["base"] == BASE and ledger["initialSnapshot"] == CANDIDATE
            and ledger["reviewedSnapshot"] == reviewed and ledger["sourceRows"] == [831]
            and ledger["supports"] == [[MEMBERS[0], MEMBERS[0]]]
            and ledger["status"] == "textual-review-closed-publication-pending"
            and ledger["published"] == [] and ledger["runtimePublished"] is False
            and ledger["reviewClosed"] == MEMBERS, "Unexpected B134 closure ledger")
    review = ledger["review"]
    require(review["status"] == "closed-with-disclosed-limits"
            and review["closureProvenanceSha256"] == sha(closure_raw)
            and review["finalRuns"] == closure["finalRuns"]
            and review["mode"] == closure["reviewMode"]
            and review["originalReviewerConfirmation"] is False
            and review["historicalReportsPreserved"] is True
            and review["remainingActionableFindings"] == []
            and review["remainingConsequentialClaims"] == [],
            "Unbound, misattributed or incomplete review closure")
    require(ledger["manifestSha256"] == sha(manifest)
            and ledger["contentVersion"] == json.loads(manifest)["contentVersion"],
            "Ledger manifest binding differs")
    counts = ledger["accounting"]
    require(all(type(counts[key]) is int and counts[key] == value for key, value in COUNTS.items())
            and counts["reviewClosedPendingRecordsWithCards"] == 272
            and counts["localUnreviewedDrafts"] == 0 and counts["notStarted"] == 956
            and counts["overallN1TaskComplete"] is False,
            "Review closure must not advance delivery or whole-set credit")
    return delivery_accounting({**ledger, "membership": ledger["members"]})


def closed_progress(original, closure_raw, manifest, resolution, original_claims):
    closure = json.loads(closure_raw)
    reviewed = closure["reviewedSnapshot"]
    validate_archived_resolution(closure, lambda path, digest: json_bytes(resolution), original_claims)
    require(original["batch"] == BATCH and original["base"] == BASE
            and original["members"] == MEMBERS and original["sourceRows"] == [831]
            and original["supports"] == [[MEMBERS[0], MEMBERS[0]]]
            and original["status"] == "local-unreviewed-authoring-candidate"
            and original["runtimePublished"] is False
            and original["reviewClosed"] == original["published"] == [],
            "Original author ledger was replaced or credited")
    counts = original["accounting"]
    require(all(type(counts[key]) is int and counts[key] == value for key, value in COUNTS.items())
            and counts["localUnreviewedDrafts"] == 1
            and counts["overallN1TaskComplete"] is False,
            "Original B134 accounting differs")
    require(isinstance(closure["limits"], list) and closure["limits"]
            and all(isinstance(item, str) and item.strip() for item in closure["limits"]),
            "Explicit current review limits are required")
    result = {
        "batch": BATCH, "base": BASE, "governingIssue": 60,
        "status": "textual-review-closed-publication-pending",
        "members": MEMBERS, "sourceRows": original["sourceRows"], "supports": original["supports"],
        "initialSnapshot": CANDIDATE, "reviewedSnapshot": reviewed,
        "reviewClosed": MEMBERS, "published": [], "runtimePublished": False,
        "manifestSha256": sha(manifest), "contentVersion": json.loads(manifest)["contentVersion"],
        "accounting": {
            **COUNTS, "reviewClosedPendingRecordsWithCards": 272,
            "localUnreviewedDrafts": 0, "notStarted": 956, "overallN1TaskComplete": False,
        },
        "review": {
            "status": "closed-with-disclosed-limits", "mode": closure["reviewMode"],
            "originalReviewerConfirmation": False, "finalRuns": closure["finalRuns"],
            "closure": "../n1-reviews/batch-134-closure/provenance.json",
            "closureProvenanceSha256": sha(closure_raw), "historicalReportsPreserved": True,
            "remainingActionableFindings": [], "remainingConsequentialClaims": [],
        },
        "originalAuthorProgress": "../n1-reviews/batch-134-closure/verification/original-progress.json",
        "originalAuthorWarnings": original["authorWarnings"],
        "publicationGates": ["Owner-signed publication", "CI", "Exact served ZIP/runtime equality"],
        "limits": closure["limits"],
    }
    validate_progress(result, reviewed, manifest, closure_raw)
    return result

"""Validate the disclosed Claude context replacement and unaccepted review history."""
from common import require

REVISION = "b1acf155fb8c7e1066a5c3baf88ae98ab92c29ac"
ORIGINAL = "83ee993b-d768-4da6-94b0-9b5e584fc044"
FRESH = "928ed3cb-7f93-476e-85cb-1b7b6f05f1ef"
OBSERVATION = "326ac28d688f60c739eeaf1b9393c77eb55478374aebd01f9a59412a0576fcad"
PRIOR_FINAL = "8018b596365bfc6ebf8c35e06ef9327c38bd9a27cd4a651787d56a717c033e20"
PRIOR_ADJUDICATION = "8bba057dd162f4e32c8fa6e0c9243692643dc312fd2e4d2d8548ae1fe2ccf326"


def bound(ref, inventory, expected=None):
    require(inventory.get(ref["path"]) == ref["sha256"]
            and (expected is None or ref["sha256"] == expected), "Unbound review-origin evidence")


def validate_final_identity(entry, originals, inventory):
    original = originals[entry["family"]]
    if entry["session"] == original:
        require("reviewerOrigin" not in entry, "Spurious replacement identity")
        return
    require(entry["family"] == "claude" and entry["role"] == "confirmation"
            and entry["run"] == "N1-B133-CLAUDE-CONFIRM-003"
            and entry["snapshot"] == REVISION and entry["session"] == FRESH
            and entry["originalSession"] == original == ORIGINAL
            and entry["reviewerOrigin"] == "fresh-context-replacement"
            and entry["replacementReason"] == "pre-admission-context-capacity",
            "Undisclosed or substituted final reviewer")
    bound(entry["contextObservation"], inventory, OBSERVATION)
    bound(entry["priorFinal"], inventory, PRIOR_FINAL)
    bound(entry["priorAdjudication"], inventory)
    require(entry["priorAdjudication"]["originalSha256"] == PRIOR_ADJUDICATION,
            "Prior adjudication derivative lost its original binding")


def validate_history(closure):
    if closure["reviewedSnapshot"] != REVISION:
        return
    require(set(closure["finalRuns"]) == {
        "N1-B133-GPT-CONFIRM-003", "N1-B133-CLAUDE-CONFIRM-003",
    }, "Final runs do not cover the corrected teaching")
    require(set(closure["intermediateRuns"]) == {
        "N1-B133-CLAUDE-CONFIRM-001", "N1-B133-GPT-CONFIRM-002",
    }, "Intermediate accepted history missing")
    by_run = {row["run"]: row for row in closure["reviewLineage"]}
    require(all(run in by_run and by_run[run]["role"] == "confirmation"
                and by_run[run]["snapshot"] != REVISION for run in closure["intermediateRuns"]),
            "Intermediate review promoted to current acceptance")
    historical = closure["nonAcceptedReviews"]
    require(len(historical) == 2 and {row["run"] for row in historical} == {
        "N1-B133-GPT-CONFIRM-001", "N1-B133-CLAUDE-CONFIRM-002",
    }, "Unaccepted review history omitted")
    for row in historical:
        require(row["reviewAccepted"] is False and row["confirmation"] == "UNVERIFIED"
                and row["run"] not in by_run, "Unaccepted review promoted into accepted lineage")
        for field in ("report", "final", "adjudication", "context", "structure", "audit-summary"):
            bound(row[field], closure["recordedFileSha256"])

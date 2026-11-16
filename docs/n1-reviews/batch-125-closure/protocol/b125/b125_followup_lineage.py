"""Validate B125 closure without relabelling either first confirmation."""
from common import require
from finalize_b125 import CANDIDATE as PRIOR_SNAPSHOT
from finalize_b125 import EXCLUDED, INITIALS, QUARANTINE_SHA, STATUS

HISTORICAL = {family: f"N1-B125-{family.upper()}-CONFIRM-001" for family in INITIALS}
FINALS = {family: f"N1-B125-{family.upper()}-CONFIRM-002" for family in INITIALS}


def check_history(provenance, config, candidate):
    require(candidate != PRIOR_SNAPSHOT
            and provenance["batch"] == 125 and provenance["reviewedSnapshot"] == candidate
            and provenance["initialSnapshot"] == config["candidate"]
            and provenance["base"] == config["base"] and provenance["publication"] == "PENDING"
            and provenance["members"] == config["members"] == ["\u4fb5"]
            and len(provenance["intermediateRuns"]) == 2
            and set(provenance["intermediateRuns"]) == set(HISTORICAL.values())
            and len(provenance["finalRuns"]) == 2
            and set(provenance["finalRuns"]) == set(FINALS.values()),
            "Closure snapshot or six-run inventory differs")
    lineage = provenance["reviewLineage"]
    require(len(lineage) == len({row["run"] for row in lineage}) == 6,
            "Both initial, historical and final reports must be preserved")
    for family in INITIALS:
        rows = [row for row in lineage if row["family"] == family]
        require([row["run"] for row in rows] == [INITIALS[family], HISTORICAL[family], FINALS[family]],
                "Original-family lineage skips or reorders a report")
        initial, prior, final = rows
        require(initial["role"] == "initial" and initial["snapshot"] == config["candidate"]
                and initial["rawVerdict"] == "NEEDS FIX" and initial["finalAcceptance"] is False
                and initial["confirmationAcceptedOnSnapshot"] is False and initial["priorRun"] is None,
                "Initial evidence was relabelled")
        require(prior["role"] == "intermediate" and prior["snapshot"] == PRIOR_SNAPSHOT
                and prior["rawVerdict"] == ("CONFIRMED" if family == "claude" else "UNVERIFIED")
                and prior["confirmationAcceptedOnSnapshot"] is (family == "claude")
                and prior["finalAcceptance"] is False and prior["priorRun"] is None
                and prior["session"] == initial["session"],
                "Historical accepted or held confirmation was relabelled")
        require(final["role"] == "final" and final["snapshot"] == candidate
                and final["rawVerdict"] == "CONFIRMED" and final["finalAcceptance"] is True
                and final["confirmationAcceptedOnSnapshot"] is True
                and final["priorRun"] == HISTORICAL[family] and final["session"] == initial["session"],
                "Final snapshot, original reviewer or prior-run link differs")
    excluded = provenance["excludedInitialRuns"]
    require(len(excluded) == 1 and excluded[0]["run"] == EXCLUDED
            and excluded[0]["status"] == STATUS and excluded[0]["snapshot"] == config["candidate"]
            and excluded[0]["reviewAccepted"] is False and excluded[0]["finalAcceptance"] is False
            and excluded[0]["quarantineSha256"] == QUARANTINE_SHA
            and EXCLUDED not in {row["run"] for row in lineage},
            "The protocol-VOID run was omitted, relabelled or accepted")

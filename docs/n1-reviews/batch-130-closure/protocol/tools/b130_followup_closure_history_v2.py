"""Preserve accepted Claude002 and unaccepted GPT002 before any later final acceptance."""
import json
import re

from b130_closure_ledger import BASE, EXCLUDED, MEMBERS, PARENT, REVIEWERS, initial_history
from b130_context_confirmation import ROOT
from b130_followup_lineage_v2 import PRIOR_SHA, require_followup_identity
from b130_fresh_closure_history import confirmation_origins
from common import frozen, require, sha

PREVIOUS = "d440617274eef6ea7611e60f147d6483f29ca710"
HISTORICAL = {family: f"N1-B130-{family.upper()}-CONFIRM-002" for family in REVIEWERS}
from b130_delta_closure_support import FINALS, check_additional_history


def historical_confirmations():
    rows = []
    for family, digest in PRIOR_SHA.items():
        path = ROOT / "confirm" / f"{HISTORICAL[family]}-acceptance.json"
        row = json.loads(frozen(path, digest))
        require(row["candidate"] == PREVIOUS and row["run"] == HISTORICAL[family]
                and row["family"] == family and row["reviewEvidenceAccepted"] is True
                and row["confirmationAccepted"] is (family == "claude")
                and row["verdict"] == ("CONFIRMED" if family == "claude" else "UNVERIFIED")
                and row["openClaimIds"] == ([] if family == "claude" else ["D18"]),
                "Historical confirmation was relabelled")
        rows.append(row)
    return rows


def verify_followup(final, candidate):
    family = final["family"]
    spec = json.loads(frozen(ROOT / "confirm" / f"{FINALS[family]}-spec.json"))
    initial = json.loads(frozen(spec["acceptance"]["path"], spec["acceptance"]["sha256"]))
    launch = json.loads(frozen(ROOT / f"{initial['run']}-launch.json"))
    require_followup_identity(spec, initial, launch, ROOT)
    require(final["candidate"] == spec["candidate"] == candidate
            and final["session"] == spec["session"] and final["run"] == spec["run"],
            "Final acceptance differs from bound continuing-reviewer spec")


def check_history(provenance, candidate, config, finals):
    require(re.fullmatch(r"[0-9a-f]{40}", candidate) and candidate not in (PARENT, PREVIOUS)
            and config["batch"] == provenance["batch"] == 130
            and config["candidate"] == provenance["initialSnapshot"] == PARENT
            and config["base"] == provenance["base"] == BASE
            and config["members"] == provenance["members"] == MEMBERS
            and provenance["reviewedSnapshot"] == candidate and provenance["publication"] == "PENDING"
            and not provenance.get("excludedConfirmationRuns")
            and len(provenance["intermediateRuns"]) == 2
            and set(provenance["intermediateRuns"]) == set(HISTORICAL.values())
            and len(provenance["finalRuns"]) == 2
            and set(provenance["finalRuns"]) == set(FINALS.values()),
            "Unexpected follow-up scope or skipped executed history")
    prior = historical_confirmations()
    prepared, origins = confirmation_origins(prior, PREVIOUS)
    require(provenance["preparedOnlyConfirmationRuns"] == prepared
            and provenance["confirmationOrigins"] == origins, "Fresh origin or prepared history differs")
    require(len(finals) == 2 and {row["family"] for row in finals} == set(REVIEWERS),
            "Two distinct family finals required")
    history = initial_history()
    rows = provenance["reviewLineage"]
    require(len(rows) == len({row["run"] for row in rows}) == 6, "Six accepted-evidence runs required")
    for family, original_session in REVIEWERS.items():
        selected = [row for row in rows if row["family"] == family]
        old = next(row for row in prior if row["family"] == family)
        accepted = next(row for row in finals if row["family"] == family)
        require([row["run"] for row in selected]
                == [history[family]["run"], HISTORICAL[family], FINALS[family]],
                "Review lineage skips or reorders a run")
        initial, previous, final = selected
        require(initial["role"] == "initial" and initial["snapshot"] == PARENT
                and initial["session"] == original_session and initial["rawVerdict"] == "NEEDS FIX"
                and initial["priorRun"] is None and initial["finalAcceptance"] is False
                and initial["confirmationAcceptedOnSnapshot"] is False, "Initial evidence was relabelled")
        require(previous["role"] == "intermediate" and previous["snapshot"] == PREVIOUS
                and previous["session"] == old["session"] != original_session
                and previous["rawVerdict"] == old["verdict"] and previous["priorRun"] is None
                and previous["confirmationAcceptedOnSnapshot"] is old["confirmationAccepted"]
                and previous["finalAcceptance"] is False, "Historical acceptance or hold was relabelled")
        require(accepted["run"] == FINALS[family] and accepted["candidate"] == candidate
                and accepted["session"] == old["session"] and accepted["verdict"] == "CONFIRMED"
                and accepted["confirmationAccepted"] is True and accepted["openClaimIds"] == []
                and final["role"] == "final" and final["snapshot"] == candidate
                and final["session"] == old["session"] and final["rawVerdict"] == "CONFIRMED"
                and final["priorRun"] == HISTORICAL[family] and final["finalAcceptance"] is True
                and final["confirmationAcceptedOnSnapshot"] is True,
                "Final does not close the subsequent snapshot")
        verify_followup(accepted, candidate)
    held = provenance["excludedInitialRuns"]
    require(len(held) == 3 and {row["run"] for row in held} == set(EXCLUDED),
            "Excluded initials missing or duplicated")
    for row in held:
        raw = frozen(ROOT / f"{row['run']}-hold.json")
        original = json.loads(raw)
        require(row["status"] == original["status"] == EXCLUDED[row["run"]]
                and row["session"] == original["session"] and row["snapshot"] == PARENT
                and row["holdSha256"] == sha(raw) and row["reviewAccepted"] is False
                and row["finalAcceptance"] is False, "Excluded initial was relabelled")
    check_additional_history(provenance, finals)
    return history

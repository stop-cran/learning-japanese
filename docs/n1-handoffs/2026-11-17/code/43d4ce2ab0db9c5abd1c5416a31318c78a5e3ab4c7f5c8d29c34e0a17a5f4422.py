"""Continue the disclosed fresh-context B133 Claude reviewer for CONFIRM-003.

The first fresh-context confirmation (N1-B133-CLAUDE-CONFIRM-002, session 928ed3cb) returned UNVERIFIED
and was accepted only as evidence. Its continuation on the owner-signed reconciliation-003 snapshot keeps
the same disclosed origin (frozen capacity observation, original session, replacement reason) and must be
run in exactly that session, bound to its frozen CONFIRM-002 final and the coordinator's adjudication.
CONFIRM-002 itself is still validated by the unchanged first module.
"""
import json
import re
from pathlib import Path

import b133_fresh_confirmation as first
from common import frozen, require

REASON = first.REASON
CONTINUATION_RUN = "N1-B133-CLAUDE-CONFIRM-003"
PRIOR_FINAL_SHA256 = "8018b596365bfc6ebf8c35e06ef9327c38bd9a27cd4a651787d56a717c033e20"
ADJUDICATION_SHA256 = "8bba057dd162f4e32c8fa6e0c9243692643dc312fd2e4d2d8548ae1fe2ccf326"
PRIOR_REPORT_SOURCE = "evidence/claude-confirm-002-report.md"
ADJUDICATION_SOURCE = "evidence/claude-confirm-002-adjudication.json"
TRAILER = "\nFRESH CONTEXT AND HISTORICAL ATTRIBUTION\n"


def prior_final_path():
    from confirm_b133_v2 import OUT
    return OUT / (first.PLANNED_RUN + "-final.json")


def adjudication_path():
    return first.root() / "claude-confirm-002-adjudication-001.json"


def prior():
    final = json.loads(frozen(prior_final_path(), PRIOR_FINAL_SHA256))
    adjudication = json.loads(frozen(adjudication_path(), ADJUDICATION_SHA256))
    require(final["run"] == adjudication["run"] == first.PLANNED_RUN
            and final["candidate"] == adjudication["candidate"] == first.CANDIDATE_002
            and final["session"] == adjudication["session"]
            and final["originalSession"] == adjudication["originalSession"]
            and final["replacementReason"] == REASON and final["confirmation"] == "UNVERIFIED"
            and adjudication["confirmation"] == "UNVERIFIED"
            and adjudication["reviewerOrigin"] == "fresh-context-replacement"
            and adjudication["status"] == "EVIDENCE_ONLY_NOT_ACCEPTED_AS_CONFIRMATION"
            and adjudication["finalSha256"] == PRIOR_FINAL_SHA256
            and adjudication["reportSha256"] == final["report"]["sha256"],
            "Prior fresh confirmation record differs")
    return final, adjudication


def continuation(spec):
    return spec["run"] != first.PLANNED_RUN


def fresh_origin(spec):
    if not continuation(spec):
        return first.fresh_origin(spec)
    from admit_b133_source_reconciliation import INITIALS
    family = spec["family"]
    observation = json.loads(frozen(first.observation_path(), spec["contextObservation"]["sha256"]))
    final, _ = prior()
    require(spec["run"] == CONTINUATION_RUN and family == first.FAMILY
            and spec["contextObservation"] == first.binding(first.observation_path())
            and observation["status"] == "NOT_ADMITTED_CONTEXT_RISK" and observation["family"] == family
            and observation["originalSession"] == spec["originalSession"] == INITIALS[family]["session"]
            and observation["plannedRun"] == first.PLANNED_RUN
            and observation["lowerBound"]["peakLowerBound"] >= observation["lowerBound"]["gate"]
            and final["originalSession"] == spec["originalSession"]
            and isinstance(spec["session"], str) and spec["session"] == final["session"] != spec["originalSession"]
            and re.fullmatch(r"[0-9a-f]{40}", spec["candidate"]) and spec["candidate"] != first.CANDIDATE_002,
            "Fresh-context continuation is not the disclosed CONFIRM-002 reviewer")
    return True


def fresh_bindings(spec):
    rows = first.fresh_bindings(spec)
    if continuation(spec):
        rows += [first.binding(Path(__file__)), first.binding(prior_final_path(), PRIOR_FINAL_SHA256),
                 first.binding(adjudication_path(), ADJUDICATION_SHA256)]
    return rows


def replacement_prompt(text, spec):
    replaced = first.replacement_prompt(text)
    if not continuation(spec):
        return replaced
    final, _ = prior()
    supplied = {row["source"]: {"path": row["path"], "sha256": row["sha256"]} for row in spec["additionalSources"]}
    require(supplied.get(PRIOR_REPORT_SOURCE) == final["report"]
            and supplied.get(ADJUDICATION_SOURCE) == {"path": str(adjudication_path()),
                                                      "sha256": ADJUDICATION_SHA256},
            "Continuation must supply its own CONFIRM-002 report and adjudication")
    require(replaced.count(TRAILER) == 1, "Unexpected attribution trailer")
    return replaced[:replaced.index(TRAILER)] + TRAILER + (
        "You are the same-family fresh-context reviewer that wrote " + first.PLANNED_RUN + " on "
        + first.CANDIDATE_002 + " (" + PRIOR_REPORT_SOURCE + "). That confirmation returned UNVERIFIED and "
        "was accepted only as evidence; the coordinator's adjudication of it is " + ADJUDICATION_SOURCE + ". "
        "You are not the author of the original initial report or of the original reviewer's CONFIRM-001; "
        "both remain accepted historical evidence with their own limits. The original session's retained "
        "context is too large to receive this complete chain within the unchanged capacity gate, so this "
        "confirmation was never admitted there; that is not a failed or withheld review. This is informed "
        "bounded confirmation of a new owner-signed snapshot, not a new blind initial review or a claim that "
        "you retain the original reviewer's firsthand context. What you remember from your earlier "
        "confirmation is not evidence by itself: read the entire chain and independently assess the actual "
        "signed snapshot, the cumulative changes and every supplied disposition within the stated scope, "
        "including each qualified precaution and its Note. Your earlier report and the adjudication are "
        "evidence to check, not conclusions to inherit. No missing or consequential uncertain claim can "
        "support CONFIRMED. All source, access, context, reporting, isolation and final-audit requirements "
        "remain unchanged. No publication or delivery credit is authorized.\n")

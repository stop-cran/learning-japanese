"""Validate additive cc374 history after actual authorized confirmation collection.

This checks archive structure and obligation preservation, not reviewer execution,
authorization transport or teaching correctness. Those remain collector duties.
"""
import copy
import re
from pathlib import Path

from common import frozen, load_module, require

SOURCE = Path(__file__).with_name("b134_review_history.py")
SOURCE_SHA = "45919be9c74393759393061259a62f255c1bc856c462cd584abbb9869625c47e"
frozen(SOURCE, SOURCE_SHA)
prior = load_module("b134_pinned_initial_and_fresh_history", SOURCE)
PRIOR = "355cccb840d22e7313e79f234eb93d1367e00352"
REVISED = "cc374051efa75199212a87c9abf08d7391419055"
MODE = "fresh-independent-reviews-plus-authorized-descendant-confirmations"
ROLE = "same-reviewer-revision-confirmation"
SESSIONS = {
    "claude": "83324022-f15a-43cd-b54a-b9da86b500ff",
    "gpt": "53c8fc4d-7652-40d4-9482-036bf448237e",
}
OBLIGATIONS = {
    "claude": ("F1", "O1", "O2", "O3"),
    "gpt": ("F1", "F2", "C1", "C2", "C3", "C4", "C5", "C6"),
}
PROOFS = {
    "scope": "6fa5d0d4cdfe4a8e2f9ca06f703c8e1bf7da0d9ce9576771174e818e6c636d6e",
    "gates": "8fa34d64fe16c821c8593778bd0af242c6420329cedea0c432b9f6294abe644a",
}
HOLD_SHA = "7818401b23e1c29522736cea57ab1d5118f9b69f6e3fe995a08d87c01fbc5683"
HELD_CLAUDE_SHA = "18eb73b8484e457d748f7abe64b44ddfed47a25121ae6682320bc4eedf09057c"


def prior_projection(closure):
    projected = copy.deepcopy(closure)
    projected["reviewLineage"] = [
        entry for entry in projected["reviewLineage"] if entry["role"] != ROLE
    ]
    projected["reviewedSnapshot"] = PRIOR
    projected["reviewMode"] = prior.MODE
    return projected


def validate_history(closure, reviewed):
    require(reviewed == REVISED and closure["schemaVersion"] == 2
            and closure["reviewedSnapshot"] == REVISED and closure["priorReviewedSnapshot"] == PRIOR
            and closure["reviewMode"] == MODE and len(closure["reviewLineage"]) == 6,
            "Expected explicit descendant history with six separate review roles")
    projected = prior_projection(closure)
    prior.validate_history(projected, PRIOR)
    entries = closure["reviewLineage"]
    by_run = {entry["run"]: entry for entry in entries}
    require(len(by_run) == 6 and len({entry["session"] for entry in entries}) == 4,
            "Confirmations must reuse their own fresh reviewers without merging review roles")
    confirmations = [entry for entry in entries if entry["role"] == ROLE]
    require([entry["family"] for entry in confirmations] == ["claude", "gpt"]
            and closure["confirmationRuns"] == [entry["run"] for entry in confirmations],
            "Two separately attributed serial family confirmations are required")
    inventory = closure["recordedFileSha256"]
    for entry in confirmations:
        family = entry["family"]
        earlier_run = "N1-B134-" + family.upper() + "-FRESH-003"
        require(earlier_run in closure["finalRuns"], "Confirmation does not extend FRESH003")
        earlier = by_run[earlier_run]
        require(entry["session"] == earlier["session"] == SESSIONS[family]
                and entry["priorRun"] == earlier_run
                and entry["priorSnapshot"] == earlier["snapshot"] == PRIOR
                and entry["snapshot"] == REVISED
                and entry["mode"] == "revision"
                and re.fullmatch("N1-B134-" + family.upper() + r"-REVISION-\d{3}", entry["run"])
                and entry["verdict"] == "CONFIRMED"
                and entry["priorRawVerdict"] == earlier["verdict"] == "NEEDS FIX"
                and entry["reviewAccepted"] is True
                and entry["confirmationAccepted"] is True
                and entry["originalReviewerConfirmation"] is False
                and entry["acceptedNewFindings"] == entry["openClaimIds"] == []
                and entry["publicationAccepted"] is False and entry["deliveryCredit"] == 0,
                "Misattributed, unaccepted or scope-expanded descendant confirmation")
        for field in (*prior.REVIEW_REFS, "authorization", "preflight", "admission"):
            prior.bound(entry[field], inventory)
        if family == "claude":
            require(HELD_CLAUDE_SHA not in (
                entry["acceptance"]["sha256"], entry["acceptance"].get("originalSha256")),
                    "A historical held acceptance cannot become prospective authorization")
        tokens = entry["dispositions"]
        require(set(tokens) == set(OBLIGATIONS[family]), "Confirmation lost an original obligation")
        for identity, token in tokens.items():
            allowed = ({"DISPUTE ACCEPTED", "DECLINE ACCEPTED"} if family == "claude" and identity == "F1"
                       else {"DECLINE ACCEPTED"} if family == "claude"
                       else {"RESOLVED"} if identity in ("F1", "F2")
                       else {"DISPUTE ACCEPTED"})
            require(token in allowed, "Unresolved confirmation disposition")
    for key, digest in PROOFS.items():
        prior.bound(closure["revisionProofs"][key], inventory, digest)
    prior.bound(closure["continuationHistory"]["scopeHold"], inventory, HOLD_SHA)


def validate_resolution(resolution, closure, reviewed, original_claims):
    validate_history(closure, reviewed)
    entries = closure["reviewLineage"]
    expected = {entry["run"]: entry["adjudication"]["sha256"] for entry in entries}
    require(resolution["mode"] == MODE and resolution["reviewedSnapshot"] == REVISED
            and resolution["priorReviewedSnapshot"] == PRIOR
            and resolution["adjudicationSha256"] == expected
            and len(resolution["dispositions"]) == 41,
            "Descendant resolution must bind all six roles and retain all41 obligations")
    projected_closure = prior_projection(closure)
    projected = copy.deepcopy(resolution)
    projected["mode"], projected["reviewedSnapshot"] = prior.MODE, PRIOR
    projected["adjudicationSha256"] = {
        entry["run"]: expected[entry["run"]] for entry in projected_closure["reviewLineage"]
    }
    prior.validate_resolution(projected, projected_closure, PRIOR, original_claims)
    confirmations = {entry["family"]: entry for entry in entries if entry["role"] == ROLE}
    by_id = {(row["run"], row["id"]): row for row in resolution["dispositions"]}
    for family, confirmation in confirmations.items():
        for identity in OBLIGATIONS[family]:
            row = by_id[(confirmation["priorRun"], identity)]
            require(confirmation["report"] in row["evidence"]
                    and confirmation["adjudication"] in row["evidence"],
                    "Fresh claim resolution lacks its own actual descendant confirmation evidence")
            expected_status = ("withdrawn" if family == "claude" and identity == "F1"
                               else "optional" if family == "claude"
                               else "resolved" if identity in ("F1", "F2") else "withdrawn")
            require(row["status"] == expected_status,
                    "Literal confirmation tokens must not rewrite original claim dispositions")

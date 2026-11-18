"""Reassign one bounded, context-held delta without inheriting its conclusions."""
import json
from pathlib import Path

from common import frozen, require
from confirm_v5 import run_number, verify_prior


def read(item):
    return json.loads(frozen(Path(item["path"]), item["sha256"]))


def require_replay_identity(spec, source, held):
    expected = {**source, "run": spec["run"], "session": spec["session"],
                "replayedFrom": spec["replayedFrom"], "unavailable": spec["unavailable"]}
    if "reviewerOrigin" in expected:
        expected["priorReviewerOrigin"] = expected.pop("reviewerOrigin")
    require(spec == expected, "Replay changes the frozen assignment's scope or lineage")
    require(spec["session"] != source["session"] == held["session"]
            and spec["family"] == source["family"] == held["family"]
            and source["run"] == held["run"]
            and spec["candidate"] == source["candidate"] == held["candidate"],
            "Replay is not a fresh same-family replacement on the held snapshot")
    require(source["basis"] == "accepted-confirmation"
            and run_number(spec["batch"], source["run"]) < run_number(spec["batch"], spec["run"]),
            "Only a later replay of an accepted-snapshot delta is supported")
    require(held["status"] == "HELD_CONTEXT_COMPACTION"
            and held["reviewEvidenceAccepted"] is False
            and held["confirmationAccepted"] is False, "The prior execution is not held")


def verify_replay(spec, config, records):
    source, held = read(spec["replayedFrom"]), read(spec["unavailable"])
    require_replay_identity(spec, source, held)
    initial, prior, previous = verify_prior(source, config, records)
    launch = json.loads(frozen(records / f"{initial['run']}-launch.json"))
    require(spec["session"] != launch["session"]
            and spec["session"] != prior["session"], "Replay must use a fresh reviewer")
    mechanics, context, structure, audit = (read(held[key])
                                           for key in ("final", "context", "structure", "audit"))
    require(mechanics["status"] == "HOLD"
            and mechanics["run"] == held["run"] and mechanics["session"] == held["session"]
            and mechanics["candidate"] == held["candidate"]
            and mechanics["confirmation"] == held["verdict"]
            and all(mechanics[key] == held[key] for key in ("report", "context", "structure", "audit"))
            and context["status"] == "FAIL" and context["compactions"]
            and structure["status"] == "PASS"
            and audit["eventsSha256"] == context["eventsSha256"]
            and audit["final"] and audit["reviewerIdle"] and not audit["recordIncomplete"]
            and not audit["breaches"] and not audit["unexpectedUserMessages"]
            and audit["fetches"] == 0 and audit["writes"] == audit["readbacks"] == 1
            and audit["readbackVerified"] and audit["chainRead"] == audit["chainRequired"],
            "Replay lacks a complete context-held execution audit")
    frozen(Path(held["report"]["path"]), held["report"]["sha256"])
    return initial, prior, previous


def render_replay_prompt(text):
    replacements = (
        ("confirmation of your own accepted B117 previous confirmation",
         "fresh same-family replacement review of a delta after an accepted B117 confirmation"),
        ("names your prior confirmation report", "names the prior reviewer's confirmation report"),
        ("Your own previous confirmation report:", "Prior reviewer's accepted confirmation report:"),
        ("your own unchanged previous confirmation report", "the prior reviewer's unchanged confirmation report"),
        ("Read your own full report", "Read the supplied prior full report"),
        ("Your prior report has no numbered", "The prior report has no numbered"),
        ("including changes not requested by you", "including changes not requested in the prior report"),
        ("No other reviewer's report or held-run observations are supplied or authorized.",
         "Only the explicitly supplied same-family historical reports are context. "
         "No held-run conclusions or other-family reports are supplied or authorized."),
        ("Your prior CONFIRMED report remains accepted", "The prior reviewer's CONFIRMED report remains accepted"),
    )
    for old, new in replacements:
        require(text.count(old) == 1, f"Replay prompt anchor changed: {old}")
        text = text.replace(old, new)
    return text + (
        "\nFRESH BOUNDED REPLACEMENT\n"
        "You did not author any historical report and have no retained firsthand review context. "
        "Re-establish the actual subsequent delta from the complete sources in this chain. "
        "Earlier unchanged teaching remains covered by the separately archived accepted reviews; "
        "do not claim a fresh full-batch review or automatic acceptance of this new snapshot. "
        "The unavailable execution and its conclusions are excluded. Preserve prior limitations "
        "and report any missing consequential evidence as UNVERIFIED.\n"
    )

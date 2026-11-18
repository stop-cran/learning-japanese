"""Preserve unexecuted preparation and actual fresh-reviewer attribution at closure."""
import json
from pathlib import Path

from b130_context_confirmation import OBSERVATION_SHA, ROOT, binding
from b130_closure_ledger import REVIEWERS
from common import TOOLS, freeze_json, frozen, require, sha, write_frozen
from confirm_b130_fresh_context import preflight

SOURCE_SHA = "83b981fa3e595d2506849e313cb8a270243b5399c0710ef3f924223480f1d2a4"
PREPARED_SHA = {
    "claude": "4e5948a878885fb2566c0ad3ee5c01dacf957227e5d7a8fe9b3c38fe114f4307",
    "gpt": "8eba200ba8709696f929d1a521e930e8b1b3e3866efa879fba8c18e67ec71f09",
}


def origin_row(family, final, candidate, record, prepared, record_sha):
    require(family in REVIEWERS
            and prepared["run"] == f"N1-B130-{family.upper()}-CONFIRM-001"
            and prepared["session"] == record["originalSession"] == REVIEWERS[family]
            and record["session"] == final["session"] != REVIEWERS[family]
            and record["run"] == final["run"] == f"N1-B130-{family.upper()}-CONFIRM-002"
            and record["candidate"] == prepared["candidate"] == final["candidate"] == candidate
            and record["replacementReason"] == "pre-admission-context-capacity"
            and record["contextObservation"]["sha256"] == OBSERVATION_SHA
            and record["segments"] == prepared["segments"]
            and record["sourceCount"] == prepared["sourceCount"],
            "Fresh confirmation identity, actual snapshot or preserved scope differs")
    return {
        "reason": record["replacementReason"], "originalSession": prepared["session"],
        "session": record["session"], "run": record["run"],
        "preflightSha256": record_sha, "preparedRun": prepared["run"],
        "preparedPreflightSha256": PREPARED_SHA[family],
        "contextObservationSha256": OBSERVATION_SHA,
    }


def confirmation_origins(finals, candidate):
    require(len(finals) == 2 and {row["family"] for row in finals} == set(REVIEWERS),
            "Two fresh family confirmations required")
    origins, prepared_rows = {}, []
    for family in REVIEWERS:
        final = next(row for row in finals if row["family"] == family)
        run = f"N1-B130-{family.upper()}-CONFIRM-002"
        require(final["run"] == run, "New executed history requires an explicit successor")
        path = ROOT / "confirm" / f"{run}-preflight.json"
        record, config = preflight(path)
        require(config["expectedFamily"] == family, "Confirmation family differs")
        prior_run = f"N1-B130-{family.upper()}-CONFIRM-001"
        prior_path = path.with_name(prior_run + "-preflight.json")
        prepared = json.loads(frozen(prior_path, PREPARED_SHA[family]))
        prior_config = json.loads(frozen(prepared["config"]["path"], prepared["config"]["sha256"]))
        require(not path.with_name(prior_run + "-admission.json").exists()
                and not Path(prior_config["report"]).exists()
                and record["replayedFrom"] == binding(path.with_name(prior_run + "-spec.json")),
                "Unexecuted predecessor was admitted, reported or relabelled")
        origins[family] = origin_row(family, final, candidate, record, prepared, sha(frozen(path)))
        prepared_rows.append({
            "run": prior_run, "family": family, "session": prepared["session"],
            "status": "PREPARED_NOT_EXECUTED", "preflightSha256": PREPARED_SHA[family],
            "confirmationAccepted": False, "reviewEvidenceAccepted": False,
        })
    return prepared_rows, origins


def check_fresh_history(provenance, candidate, finals):
    prepared, origins = confirmation_origins(finals, candidate)
    require(provenance.get("preparedOnlyConfirmationRuns") == prepared
            and provenance.get("confirmationOrigins") == origins,
            "Fresh origin or unexecuted preparation missing from closure history")


def derive_text(text):
    text = text.replace("\r\n", "\n")
    replacements = (
        ("from common import frozen, require, sha",
         "from common import frozen, require, sha\n"
         "from b130_fresh_closure_history import check_fresh_history"),
        ("    history = initial_history()\n",
         "    check_fresh_history(provenance, candidate, finals)\n    history = initial_history()\n"),
        ('and final["snapshot"] == candidate and final["session"] == session',
         'and final["snapshot"] == candidate and final["session"] == accepted["session"]'),
        ("Final confirmation is not accepted on this candidate by its original reviewer",
         "Final confirmation is not accepted on this candidate by its recorded fresh reviewer"),
        ('            "finalRuns": list(provenance["finalRuns"]), "intermediateRuns": [],',
         '            "finalRuns": list(provenance["finalRuns"]), "intermediateRuns": [],\n'
         '            "preparedOnlyConfirmationRuns": copy.deepcopy(provenance["preparedOnlyConfirmationRuns"]),\n'
         '            "confirmationOrigins": copy.deepcopy(provenance["confirmationOrigins"]),'),
        ('"identity": "Both attempt004 initials remain NEEDS FIX. Their original reviewers "\n'
         '                        "confirmed the revised snapshot separately. The 24 GPT initial questions "',
         '"identity": "Both attempt004 initials remain NEEDS FIX, attributed to their original sessions. "\n'
         '                        "Fresh same-family sessions separately confirmed the revised snapshot. "\n'
         '                        "Original confirmation001 preparations remain unexecuted, not failed. "\n'
         '                        "The 24 GPT initial questions "'),
    )
    for before, after in replacements:
        require(text.count(before) == 1, "Unexpected closure successor anchor")
        text = text.replace(before, after)
    return text


def main():
    source = TOOLS / "b130_closure_ledger.py"
    derived = derive_text(frozen(source, SOURCE_SHA).decode("utf-8"))
    compile(derived, "b130_closure_ledger_v2.py", "exec")
    result = write_frozen(TOOLS / "b130_closure_ledger_v2.py", derived.encode("utf-8"))
    print(json.dumps(freeze_json(ROOT / "fresh-closure-ledger-preparation-001.json", {
        "source": binding(source), "output": result, "producer": binding(__file__),
        "scope": "Explicit fresh-context origin and retained unexecuted001 preparation only. "
                 "Actual two accepted002 confirmations, unchanged initial and excluded history, "
                 "all historical questions, current runtime and archive proofs remain required. "
                 "Pure helper preparation is not review closure, final adjudication or publication.",
        "confirmationAccepted": False, "publicationAccepted": False,
    })))


if __name__ == "__main__":
    main()

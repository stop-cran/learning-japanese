"""Archive actual fresh confirmations without relabelling their original reviewers."""
import json
from pathlib import Path

from b130_fresh_closure_history import confirmation_origins
from common import TOOLS, freeze_json, frozen, require, sha, write_frozen
from b130_context_confirmation import ROOT, binding

SOURCE_SHA = "28d974b35f1d20c7c67bdd2919b4237ca984d4e11f0de6d81315e63f40906de5"
NEW_TOOLS = ("close_b130_fresh.py", "b130_fresh_archive.py", "test_b130_fresh_archive.py")


def ledger_acceptance(accepted, preflight):
    """Derive the omitted acceptance batch from its bound, verified preflight."""
    require(preflight["batch"] == 130
            and all(accepted[key] == preflight[key] for key in ("run", "candidate", "session"))
            and accepted["run"] == f"N1-B130-{accepted['family'].upper()}-CONFIRM-002"
            and ("batch" not in accepted or accepted["batch"] == preflight["batch"]),
            "Acceptance/preflight identity differs")
    return {**accepted, "batch": preflight["batch"]}


def require_origin(spec, mechanics, launch, accepted, family, candidate, origins):
    origin = origins[family]
    require(spec["run"] == mechanics["run"] == accepted["run"] == origin["run"]
            and spec["session"] == mechanics["session"] == accepted["session"] == origin["session"]
            and spec["originalSession"] == accepted["originalSession"]
            == launch["session"] == origin["originalSession"]
            and origin["session"] != origin["originalSession"]
            and spec["candidate"] == mechanics["candidate"] == accepted["candidate"] == candidate
            and origin["reason"] == "pre-admission-context-capacity"
            and "prior" not in spec,
            "Fresh confirmation attribution differs from verified origin")


def retain_preparations(records, prepared, origins, copy):
    for row in prepared:
        run = row["run"]
        require(row["status"] == "PREPARED_NOT_EXECUTED", "Preparation was executed")
        for suffix in ("spec.json", "preflight.json", "config.json", "prompt.txt",
                       "kickoff.txt", "chain.json"):
            copy(records / "confirm" / f"{run}-{suffix}", f"prepared-only/{run}/{suffix}")
        origin = origins[row["family"]]
        copy(records / "confirm" / f"{origin['run']}-bootstrap.json",
             f"runs/{origin['run']}/bootstrap.json")
    copy(records / "confirmation-capacity-observation-001.json",
         "protocol/confirmation-capacity-observation-001.json")


def derive_text(text):
    text = text.replace("\r\n", "\n")
    replacements = (
        ("from b130_excluded_initials_v3 import archive_excluded",
         "from b130_excluded_initials_v3 import archive_excluded\n"
         "from b130_fresh_closure_history import confirmation_origins\n"
         "from b130_fresh_archive import NEW_TOOLS, require_origin, retain_preparations"),
        ('and not set(additional_tools) & {',
         'and not set(additional_tools) & set(NEW_TOOLS)\n'
         '            and not set(additional_tools) & {'),
        ('    require({item["run"] for item in finals} == set(final_runs), "Run mismatch")',
         '    require({item["run"] for item in finals} == set(final_runs), "Run mismatch")\n'
         '    require(not intermediate_runs, "New executed history requires an explicit successor")\n'
         '    prepared, origins = confirmation_origins(finals, candidate)'),
        ('            require(spec["session"] == mechanics["session"] == launch["session"],\n'
         '                    "Confirmation changed reviewer")',
         '            require_origin(spec, mechanics, launch, accepted, family, candidate, origins)'),
        ('        copy(preflight_path, "protocol/selected-initial-preflight.json")',
         '        retain_preparations(records, prepared, origins, copy)\n'
         '        copy(preflight_path, "protocol/selected-initial-preflight.json")'),
        ('"verify_b130_attempt004_prompts_v2.py", *additional_tools):',
         '"verify_b130_attempt004_prompts_v2.py", *NEW_TOOLS, *additional_tools):'),
        ('            "reviewLineage": lineage, "excludedInitialRuns": excluded,',
         '            "reviewLineage": lineage, "excludedInitialRuns": excluded,\n'
         '            "preparedOnlyConfirmationRuns": prepared, "confirmationOrigins": origins,'),
        ('            "independence": "Independent initials share the frozen source packet. Confirmations use "\n'
         '                            "the original reviewer, its own report, the actual runtime delta and "\n'
         '                            "explicitly selected author responses and source evidence. Intermediate "\n'
         '                            "confirmations retain their raw verdicts and snapshot-specific acceptance; "\n'
         '                            "neither accepted nor unaccepted earlier snapshots are final acceptance of this revision.",',
         '            "independence": "Independent attempt004 initials retain their original authors and NEEDS FIX "\n'
         '                            "verdicts. Fresh same-family sessions separately read the original family report, "\n'
         '                            "own-family response and frozen delta evidence. Original confirmation001 "\n'
         '                            "preparations were never executed; their preserved metadata is not a review. "\n'
         '                            "Raw bootstrap and execution events remain local. Excluded initials remain unaccepted.",'),
    )
    for before, after in replacements:
        require(text.count(before) == 1, "Unexpected fresh archive derivation anchor")
        text = text.replace(before, after)
    return text


def main():
    source = TOOLS / "close_b130_compact_v4.py"
    text = derive_text(frozen(source, SOURCE_SHA).decode("utf-8"))
    compile(text, "close_b130_fresh.py", "exec")
    output = write_frozen(TOOLS / "close_b130_fresh.py", text.encode("utf-8"))
    print(json.dumps(freeze_json(ROOT / "fresh-archive-tooling-001.json", {
        "source": binding(source), "producer": binding(__file__), "output": output,
        "scope": "Fresh002 identity and prepared-only001 preservation. Existing execution, "
                 "source retention, signed-candidate and excluded-initial checks remain. "
                 "No actual closure or review acceptance.",
    })))


if __name__ == "__main__":
    main()

"""Correct the003 acceptance adapter and remove obsolete scan wording before use."""
import json

from b130_context_confirmation import ROOT, binding
from b130_followup_closure_history import FINALS, HISTORICAL
from common import TOOLS, freeze_json, frozen, require, write_frozen
from prepare_b130_followup_engine import replace_once


def ledger_acceptance(accepted, preflight):
    family = accepted["family"]
    require(family in FINALS and preflight["batch"] == 130
            and all(accepted[key] == preflight[key] for key in ("run", "candidate", "session"))
            and accepted["run"] == FINALS[family] and preflight["priorRun"] == HISTORICAL[family]
            and ("batch" not in accepted or accepted["batch"] == preflight["batch"]),
            "Follow-up acceptance/preflight identity differs")
    return {**accepted, "batch": preflight["batch"]}


def main():
    outputs = []
    for source_name, name, replacements in (
        ("confirm_b130_followup.py", "confirm_b130_followup_v2.py", (
            ('"retained the original D18 effect-allocation question")',
             '"retained the original D18 effect-allocation question").replace(\n'
             '            "and to each scan decision", "and to the proposed precaution")'),
        )),
        ("finalize_b130_followup.py", "finalize_b130_followup_v2.py", (
            ("from b130_fresh_archive import ledger_acceptance",
             "from prepare_b130_followup_ready import ledger_acceptance"),
            ('("finalize_b130_followup.py", "test_finalize_b130_followup.py"):',
             '("finalize_b130_followup.py", "test_finalize_b130_followup.py",\n'
             '                     "finalize_b130_followup_v2.py", "prepare_b130_followup_ready.py",\n'
             '                     "test_b130_followup_ready.py"):'),
        )),
    ):
        source = TOOLS / source_name
        text = frozen(source).decode("utf-8").replace("\r\n", "\n")
        for before, after in replacements:
            text = replace_once(text, before, after)
        compile(text, name, "exec")
        outputs.append({"source": binding(source),
                        "output": write_frozen(TOOLS / name, text.encode("utf-8"))})
    print(json.dumps(freeze_json(ROOT / "followup-ready-tooling-001.json", {
        "producer": binding(__file__), "outputs": outputs,
        "scope": "The unexecuted predecessor finalizer reused a002-only batch adapter. Its explicit "
                 "successor accepts only matching003/preflight/prior002 attribution. Prompt removes "
                 "a leftover reference to a nonexistent new scan; audit/access rules unchanged. "
                 "No actual003 acceptance or closure exists yet.",
    })))


if __name__ == "__main__":
    main()

"""Extend closure provenance for the two real002 outcomes and later same-session003 finals."""
import ast
import json

from b130_context_confirmation import ROOT, binding
from b130_followup_closure_history import HISTORICAL, PREVIOUS, historical_confirmations
from b130_followup_lineage import require_followup_identity
from b130_fresh_archive import require_origin
from common import TOOLS, freeze_json, frozen, require, write_frozen
from prepare_b130_followup_engine import replace_once

FOLLOWUP_TOOLS = ("close_b130_followup.py", "prepare_b130_followup_closure.py",
                  "b130_followup_closure_history.py", "test_b130_followup_closure_history.py",
                  "b130_followup_ledger.py", "test_b130_followup_closure.py")


def archive_origins(intermediates):
    expected = historical_confirmations()
    require(len(intermediates) == 2
            and {row["run"]: row for row in intermediates}
            == {row["run"]: row for row in expected}, "Intermediate evidence differs")
    from b130_fresh_closure_history import confirmation_origins
    return confirmation_origins(intermediates, PREVIOUS)


def require_archive_origin(spec, mechanics, launch, accepted, family, candidate, origins):
    if spec["run"] == HISTORICAL[family]:
        require_origin(spec, mechanics, launch, accepted, family, PREVIOUS, origins)
        return
    initial = json.loads(frozen(spec["acceptance"]["path"], spec["acceptance"]["sha256"]))
    require_followup_identity(spec, initial, launch, ROOT)
    require(spec["run"] == mechanics["run"] == accepted["run"]
            and spec["session"] == mechanics["session"] == accepted["session"] == origins[family]["session"]
            and spec["candidate"] == mechanics["candidate"] == accepted["candidate"] == candidate,
            "Final follow-up attribution differs")


def derive_archive(text):
    text = text.replace("\r\n", "\n")
    for before, after in (
        ("from b130_fresh_archive import NEW_TOOLS, require_origin, retain_preparations",
         "from b130_fresh_archive import NEW_TOOLS, retain_preparations\n"
         "from prepare_b130_followup_closure import FOLLOWUP_TOOLS, archive_origins, require_archive_origin"),
        ('and not set(additional_tools) & set(NEW_TOOLS)',
         'and not set(additional_tools) & (set(NEW_TOOLS) | set(FOLLOWUP_TOOLS))'),
        ('    require(not intermediate_runs, "New executed history requires an explicit successor")\n'
         '    prepared, origins = confirmation_origins(finals, candidate)\n', ''),
        ('    require({item["run"] for item in intermediates} == set(intermediate_runs), "Intermediate run mismatch")',
         '    require({item["run"] for item in intermediates} == set(intermediate_runs), "Intermediate run mismatch")\n'
         '    prepared, origins = archive_origins(intermediates)'),
        ('require_origin(spec, mechanics, launch, accepted, family, candidate, origins)',
         'require_archive_origin(spec, mechanics, launch, accepted, family, candidate, origins)'),
        ('*NEW_TOOLS, *additional_tools):', '*NEW_TOOLS, *FOLLOWUP_TOOLS, *additional_tools):'),
        ('"preparations were never executed; their preserved metadata is not a review. "',
         '"preparations were never executed; their preserved metadata is not a review. "\n'
         '                            "Claude002 remains CONFIRMED only on its earlier snapshot; GPT002 remains "\n'
         '                            "valid UNVERIFIED evidence with D18 open there. Later003 confirmations "\n'
         '                            "check a subsequent delta in those same fresh sessions. "'),
    ):
        text = replace_once(text, before, after)
    return text


def derive_ledger(text):
    text = text.replace("\r\n", "\n")
    old_function = next(ast.get_source_segment(text, node) for node in ast.parse(text).body
                        if isinstance(node, ast.FunctionDef) and node.name == "check_history")
    text = replace_once(text, old_function,
                        "from b130_followup_closure_history import check_history, PREVIOUS, historical_confirmations")
    for before, after in (
        ('and runtime["parent"] == PARENT and runtime["base"] == BASE',
         'and runtime["parent"] == PREVIOUS and runtime["base"] == BASE'),
        ('"finalRuns": list(provenance["finalRuns"]), "intermediateRuns": [],',
         '"finalRuns": list(provenance["finalRuns"]),\n'
         '            "intermediateRuns": list(provenance["intermediateRuns"]),\n'
         '            "historicalConfirmations": [\n'
         '                {key: row[key] for key in ("run", "family", "session", "candidate",\n'
         '                                           "verdict", "confirmationAccepted", "openClaimIds")}\n'
         '                for row in historical_confirmations()\n'
         '            ],'),
        ('"Fresh same-family sessions separately confirmed the revised snapshot. "',
         '"The same fresh sessions separately confirmed the later delta. Claude002 remains "\n'
         '                        "accepted only on its earlier snapshot; GPT002 remains valid UNVERIFIED "\n'
         '                        "evidence with D18 open on that snapshot. "'),
        ('        "correctionSources": ["batch-130-reconciliation/"],',
         '        "publicationGates": ["Owner-signed publication", "CI", "Exact served ZIP/runtime equality"],\n'
         '        "correctionSources": ["batch-130-reconciliation/"],'),
        ('            "Publication, CI and exact served ZIP remain pending; review closure is not delivery.",\n', ''),
    ):
        text = replace_once(text, before, after)
    return text


def main():
    outputs = []
    for source_name, name, derive in (
        ("close_b130_fresh.py", "close_b130_followup.py", derive_archive),
        ("b130_closure_ledger_v2.py", "b130_followup_ledger.py", derive_ledger),
    ):
        source = TOOLS / source_name
        text = derive(frozen(source).decode("utf-8"))
        compile(text, name, "exec")
        outputs.append({"source": binding(source),
                        "output": write_frozen(TOOLS / name, text.encode("utf-8"))})
    print(json.dumps(freeze_json(ROOT / "followup-closure-preparation-001.json", {
        "producer": binding(__file__), "outputs": outputs,
        "history": binding(TOOLS / "b130_followup_closure_history.py"),
        "scope": "Preserve actual accepted002/UNVERIFIED002 outcomes and prepared-only001 history. "
                 "Actual003 acceptance, signed follow-up proof, finalizer, archive verification "
                 "and publication are still required. No closure or delivery credit.",
    })))


if __name__ == "__main__":
    main()

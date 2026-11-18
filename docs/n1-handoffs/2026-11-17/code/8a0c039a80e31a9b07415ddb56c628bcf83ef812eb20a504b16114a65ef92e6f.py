"""Derive explicit mixed-final closure adapters; retain existing checks and raw evidence."""
import json

from b130_context_confirmation import ROOT, binding
from common import TOOLS, freeze_json, frozen, require, write_frozen
from prepare_b130_followup_engine import replace_once


def main():
    definitions = (
        ("b130_followup_closure_history.py", "b130_followup_closure_history_v2.py", (
            ("from b130_followup_lineage import", "from b130_followup_lineage_v2 import"),
            ('FINALS = {family: f"N1-B130-{family.upper()}-CONFIRM-003" for family in REVIEWERS}',
             "from b130_delta_closure_support import FINALS, check_additional_history"),
            ("    return history", "    check_additional_history(provenance, finals)\n    return history"),
        )),
        ("close_b130_followup.py", "close_b130_followup_v2.py", (
            ("from prepare_b130_followup_closure import FOLLOWUP_TOOLS, archive_origins, require_archive_origin",
             "from b130_delta_closure_support import (FOLLOWUP_TOOLS, archive_origins,\n"
             "    require_archive_origin, retain_additional_history)"),
            ("        retain_preparations(records, prepared, origins, copy)",
             "        retain_preparations(records, prepared, origins, copy)\n"
             "        prepared_followups, control_adjudications = retain_additional_history(\n"
             "            finals, copy, dump, audit_support)"),
            ('            "preparedOnlyConfirmationRuns": prepared, "confirmationOrigins": origins,',
             '            "preparedOnlyConfirmationRuns": prepared, "confirmationOrigins": origins,\n'
             '            "preparedOnlyFollowups": prepared_followups,\n'
             '            "runtimeControlAdjudications": control_adjudications,'),
            ('"valid UNVERIFIED evidence with D18 open there. Later003 confirmations "',
             '"valid UNVERIFIED evidence with D18 open there. Later GPT003/Claude004 confirmations "'),
            ('"check a subsequent delta in those same fresh sessions. "',
             '"check a subsequent delta in those same fresh sessions. Claude003 was never admitted. "\n'
             '                            "Both exact runtime completion reminders are separately adjudicated; "\n'
             '                            "their original HOLD audits and unchanged raw logs are retained. "'),
        )),
        ("b130_followup_ledger.py", "b130_followup_ledger_v2.py", (
            ("from b130_followup_closure_history import", "from b130_followup_closure_history_v2 import"),
            ('            "intermediateRuns": list(provenance["intermediateRuns"]),',
             '            "intermediateRuns": list(provenance["intermediateRuns"]),\n'
             '            "preparedOnlyFollowups": provenance["preparedOnlyFollowups"],\n'
             '            "runtimeControlAdjudications": provenance["runtimeControlAdjudications"],'),
        )),
        ("finalize_b130_followup_v2.py", "finalize_b130_followup_v3.py", (
            ("from b130_followup_closure_history import", "from b130_followup_closure_history_v2 import"),
            ("from b130_followup_ledger import", "from b130_followup_ledger_v2 import"),
            ("from prepare_b130_followup_ready import ledger_acceptance",
             "from b130_delta_closure_support import ledger_acceptance, LOCAL_ONLY_EXECUTIONS"),
            ('            require(Path(name).name == name and code in (0, 1, 5), "Invalid execution record")',
             '            require(Path(name).name == name and code in (0, 1, 5)\n'
             '                    and name not in LOCAL_ONLY_EXECUTIONS, "Invalid or local-only execution record")'),
            ('"Acceptance batch derives from each bound003 preflight; all original "',
             '"Acceptance binds actual GPT003/Claude004 preflights and exact control adjudications; all original "'),
        )),
        ("run_b130_closure_checks.py", "run_b130_delta_closure_checks.py", (
            ("from b130_closure_ledger_v2 import check_history",
             "from b130_followup_closure_history_v2 import check_history, FINALS"),
            ("from b130_fresh_archive import ledger_acceptance",
             "from b130_delta_closure_support import ledger_acceptance"),
            ("from b130_revision_gates import commands", "from b130_delta_gates import commands"),
            ("from finalize_b130 import CANDIDATE, check_proofs",
             "from verify_b130_delta_evidence import CANDIDATE\n"
             "from finalize_b130_followup_v3 import check_proofs"),
            ('"reconciliation-001.json"', '"reconciliation-002.json"'),
            ('"source-proof.json"', '"source-reuse-proof.json"'),
            ("    check_proofs(proof, runtime, sources)",
             '    spec = json.loads(frozen(closure / "verification" / "finalizer-spec.json"))\n'
             '    check_proofs(CANDIDATE, proof, runtime, sources, spec["runtimeProof"], spec["sourceReuseProof"])'),
            ('    for family in ("claude", "gpt"):\n'
             '        run = f"N1-B130-{family.upper()}-CONFIRM-002"',
             '    for family, run in FINALS.items():'),
        )),
    )
    planned = []
    for source_name, name, replacements in definitions:
        source = TOOLS / source_name
        text = frozen(source).decode().replace("\r\n", "\n")
        for before, after in replacements:
            text = replace_once(text, before, after)
        compile(text, name, "exec")
        require(not (TOOLS / name).exists(), "Preserve previous tool: " + name)
        planned.append((source, name, text.encode()))
    outputs = [{"source": binding(source), "output": write_frozen(TOOLS / name, data)}
               for source, name, data in planned]
    print(json.dumps(freeze_json(ROOT / "delta-closure-tooling-001.json", {
        "producer": binding(__file__), "support": binding(TOOLS / "b130_delta_closure_support.py"),
        "outputs": outputs,
        "scope": "Explicit GPT003/Claude004 finals, unchanged six actual review runs, separate unused "
                 "Claude003, original HOLD/control-adjudication retention and local-only payload guard. "
                 "No actual archive/finalization, publication or delivery credit.",
    })))


if __name__ == "__main__":
    main()

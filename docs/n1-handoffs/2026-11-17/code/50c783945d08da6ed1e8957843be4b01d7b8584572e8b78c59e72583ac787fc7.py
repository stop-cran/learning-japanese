"""Derive an additive replacement builder; retain every frozen earlier tool."""
import ast
import json
from pathlib import Path

from common import TOOLS, WS, freeze_json, frozen, require, write_frozen
from confirm_v2 import binding

SOURCE_SHA = "c08acedfd7322ddd9b16bf3a4b4314085bebcf664c8513ab71fc348e4c389c15"
OUT = WS / "scratch-123" / "review" / "confirm"


def derive():
    source = TOOLS / "confirm_followup.py"
    text = frozen(source, SOURCE_SHA).decode("utf-8")
    node = next(n for n in ast.parse(text).body
                if isinstance(n, ast.FunctionDef) and n.name == "verify_prior")
    old = ast.get_source_segment(text, node)
    text = text.replace(old, "def verify_prior(spec, config, records):\n"
                            "    return verify_replacement(spec, config, records)")
    changes = (
        ("from replacement_lineage import require_followup_identity",
         "from b123_unavailable_context import verify_replacement, render_replacement_prompt"),
        ('    bindings.append(binding(Path(__file__).with_name("replacement_lineage.py")))',
         '    bindings.extend(spec[key] for key in ("replayedFrom", "unavailable"))\n'
         '    bindings.extend(binding(Path(__file__).with_name(name)) for name in\n'
         '                    ("b123_unavailable_context.py", "confirm_followup.py", "replacement_lineage.py"))'),
        ("    prompt_text = render_followup_prompt(renderer, renderer_spec, packet_info, chain, prompt_path)",
         "    prompt_text = render_replacement_prompt(\n"
         "        render_followup_prompt(renderer, renderer_spec, packet_info, chain, prompt_path))"),
    )
    for before, after in changes:
        require(text.count(before) == 1, f"Unexpected builder anchor: {before}")
        text = text.replace(before, after)
    text = text.replace('"""Same-reviewer deltas after either an accepted or an unaccepted confirmation.',
                        '"""Fresh same-family delta after a refused compacted original context.')
    compile(text, "confirm_b123_context_replacement.py", "exec")
    output = write_frozen(TOOLS / "confirm_b123_context_replacement.py", text.encode("utf-8"))
    helper = TOOLS / "b123_unavailable_context.py"
    helper.chmod(0o444)
    void_run = "N1-B123-CLAUDE-CONFIRM-003"
    refused_run = "N1-B123-CLAUDE-CONFIRM-004"
    refused = OUT.parent / "claude-confirmation-scoped-admission-004"
    source_spec = json.loads(frozen(OUT / f"{refused_run}-spec.json"))
    unavailable = freeze_json(OUT / f"{refused_run}-unavailable.json", {
        "run": refused_run, "session": source_spec["session"], "family": source_spec["family"],
        "candidate": source_spec["candidate"], "status": "UNLAUNCHED_CONTEXT_COMPACTION",
        "reviewEvidenceAccepted": False, "confirmationAccepted": False,
        "context": binding(OUT / f"{void_run}-context-diagnosis.json"),
        "voidExecution": binding(OUT / f"{void_run}-superseded.json"),
        "admissionRefusal": binding(refused / "receipt.json"),
        "admissionLog": binding(refused / "output.log"),
        "reason": "Original context compacted. CONFIRM-004 was refused before delivery; "
                  "CONFIRM-003 remains separately VOID for its actual execution breaches. "
                  "No clean held execution or acceptance is fabricated.",
    })
    return freeze_json(OUT.parent / "context-replacement-tooling-001.json", {
        "source": binding(source), "output": output, "helper": binding(helper),
        "producer": binding(Path(__file__)), "unavailable": unavailable,
        "delta": "Verify the exact unlaunched source assignment and reproducible context refusal; "
                 "correct historical report ownership and emphasize dependent output ordering. "
                 "No audit, context, structure, source, RAM or final acceptance gate changed.",
        "reviewersLaunched": False,
    })


if __name__ == "__main__":
    print(json.dumps(derive()))

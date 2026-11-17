"""Derive B130 fresh-reviewer follow-ups, preserving the shared delta/audit contract."""
import json

from b130_context_confirmation import ROOT, binding
from common import TOOLS, freeze_json, frozen, require, write_frozen


def replace_once(text, before, after):
    require(text.count(before) == 1, "Follow-up derivation anchor changed")
    return text.replace(before, after)


def derive_engine(text):
    text = text.replace("\r\n", "\n")
    for before, after in (
        ("require, review_dir, start_guard, verify_packet, write_frozen)",
         "require, review_dir, start_guard, write_frozen)\nfrom b130_compact_common import verify_packet"),
        ("from confirm_v2 import admit, binding, clean, final, revision_diff",
         "from confirm_b130_fresh_context import binding, clean, final, revision_diff\n"
         "from b130_followup_admission import admit"),
        ("from replacement_lineage import require_followup_identity",
         "from b130_followup_lineage import require_followup_identity"),
        ('Path(__file__).with_name("replacement_lineage.py")',
         'Path(__file__).with_name("b130_followup_lineage.py")'),
        ('Path(__file__).with_name("confirm_v2.py")',
         'Path(__file__).with_name("confirm_b130_fresh_context.py")'),
        ('    prompt = prompt_text.encode("utf-8")',
         '    if spec["basis"] == "held-confirmation":\n'
         '        prompt_text = prompt_text.replace("recorded a gloss-overlap scan",\n'
         '                                          "retained the original D18 effect-allocation question")\n'
         '    prompt = prompt_text.encode("utf-8")'),
        ('"\\nCONTINUING REPLACEMENT IDENTITY\\n"', '"\\nCONTINUING FRESH-REVIEWER IDENTITY\\n"'),
        ('"You are continuing your own prior replacement confirmation. The original "',
         '"You are continuing your own prior fresh-context confirmation. The original "'),
        ('    result = {"run": run, "batch": spec["batch"], "session": spec["session"], "candidate": spec["candidate"],',
         '    result = {"originalSession": spec["originalSession"], "reviewerOrigin": spec["reviewerOrigin"],\n'
         '              "run": run, "batch": spec["batch"], "session": spec["session"], "candidate": spec["candidate"],'),
    ):
        text = replace_once(text, before, after)
    return text


def derive_admission(text):
    text = text.replace("\r\n", "\n")
    text = replace_once(text, "from scoped_admission import assess_status",
                        "from scoped_admission import assess_status\n"
                        "from b130_followup_lineage import require_followup_preflight")
    text = replace_once(text,
        '    require(record.get("replacementReason") == "pre-admission-context-capacity"\n'
        '            and record["session"] != record["originalSession"]\n'
        '            and record["replayedFrom"] and record["contextObservation"],\n'
        '            "Fresh-context origin missing")',
        '    require_followup_preflight(record, config)')
    text = replace_once(text,
        "A new same-family reviewer confirms the historical original review with disclosed attribution.",
        "The same fresh002 reviewer checks its own prior confirmation and the subsequent delta.")
    return text


def main():
    outputs = []
    for source_name, name, derive in (
        ("confirm_followup.py", "confirm_b130_followup.py", derive_engine),
        ("b130_fresh_confirmation_admission.py", "b130_followup_admission.py", derive_admission),
    ):
        source = TOOLS / source_name
        text = derive(frozen(source).decode("utf-8"))
        compile(text, name, "exec")
        outputs.append({"source": binding(source),
                        "output": write_frozen(TOOLS / name, text.encode("utf-8"))})
    print(json.dumps(freeze_json(ROOT / "followup-engine-preparation-001.json", {
        "producer": binding(__file__), "outputs": outputs,
        "lineage": binding(TOOLS / "b130_followup_lineage.py"),
        "scope": "Only actual fresh002 reviewer continuation, compact packet choice and truthful "
                 "attribution. Existing accepted-versus-held basis, delta, ordered-read, report "
                 "and final-audit checks remain. No candidate, admission or reviewer launch.",
    })))


if __name__ == "__main__":
    main()

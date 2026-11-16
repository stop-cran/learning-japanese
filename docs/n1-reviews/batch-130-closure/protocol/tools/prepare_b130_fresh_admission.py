"""Retain scoped admission mechanics while accurately naming a fresh reviewer."""
import json

from common import TOOLS, freeze_json, frozen, require, write_frozen
from b130_context_confirmation import ROOT, binding

SOURCE_SHA = "db651dfb041992853e998a23a98d86c851d3cb14360f910e928478242d7d00c6"


def derive_text(text):
    text = text.replace("\r\n", "\n")
    replacements = (
        ("Admit a reused original reviewer", "Admit a disclosed fresh-context reviewer"),
        ("Original reviewer", "Fresh reviewer"),
        ("original-reviewer", "fresh-reviewer"),
        ("originalSessionNameUnique", "reviewerSessionNameUnique"),
        ("originalReviewer", "reviewerSession"),
        ("The existing original reviewer is reused, not a new named session.",
         "A new same-family reviewer confirms the historical original review with disclosed attribution."),
    )
    for before, after in replacements:
        require(before in text, "Unexpected scoped admission label")
        text = text.replace(before, after)
    anchor = "    record, config = preflight(path)\n"
    require(text.count(anchor) == 1, "Unexpected scoped preflight call")
    return text.replace(anchor, anchor +
        '    require(record.get("replacementReason") == "pre-admission-context-capacity"\n'
        '            and record["session"] != record["originalSession"]\n'
        '            and record["replayedFrom"] and record["contextObservation"],\n'
        '            "Fresh-context origin missing")\n')


def main():
    source = TOOLS / "scoped_confirmation_admission.py"
    derived = derive_text(frozen(source, SOURCE_SHA).decode("utf-8"))
    compile(derived, "b130_fresh_confirmation_admission.py", "exec")
    result = write_frozen(TOOLS / "b130_fresh_confirmation_admission.py", derived.encode("utf-8"))
    print(json.dumps(freeze_json(ROOT / "fresh-confirmation-admission-tooling-001.json", {
        "source": binding(source), "output": result, "producer": binding(__file__),
        "scope": "Only reviewer attribution labels and an additional fresh-context-origin guard "
                 "change. Original scoped activity, complete snapshot, context, RAM, prefix, "
                 "candidate, signature and preflight binding checks remain required.",
    })))


if __name__ == "__main__":
    main()

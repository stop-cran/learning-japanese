"""Preserve original004 evidence while checking only the signed D18 precaution delta."""
import json

from b130_context_confirmation import ROOT, binding
from b130_followup_closure_history import PREVIOUS
from common import TOOLS, freeze_json, frozen, write_frozen
from prepare_b130_followup_engine import replace_once

SOURCE = "verify_b130_revision_runtime_v3.py"
SOURCE_SHA = "8ef584f020b1a9b939be2a70e422854c42f85a7b02e2f27ce23cafe0837b0e48"
OUTPUT = "verify_b130_delta_runtime.py"


def derive(text):
    text = text.replace("\r\n", "\n")
    for before, after in (
        ('PARENT = "ce1b5c895fac90852143f322a115c2de4e768e20"',
         'INITIAL = "ce1b5c895fac90852143f322a115c2de4e768e20"\n'
         f'PARENT = "{PREVIOUS}"'),
        ('accepted["candidate"] == adjudication["candidate"] == final["candidate"] == PARENT',
         'accepted["candidate"] == adjudication["candidate"] == final["candidate"] == INITIAL'),
        ('and facts["cards"] and set(facts["cards"]) <= set(MEMBERS)',
         'and facts["cards"] == {"拍": {"allowedAddedGuards": ["響"], "requiredAddedGuards": ["響"]}}'),
        ('require(expected_cards and expected_cards <= CARDS, "Invalid runtime correction scope")',
         'require(expected_cards == {"kanji/拍.md"}, "Invalid runtime correction scope")\n'
         '    require(changes.get(NOTES) == "M", "Missing additive authoring-notes entry")'),
        ('"B130 signed reconciliation runtime verification"',
         '"B130 second signed reconciliation runtime verification"'),
        ('"bodyAcceptance": "Pending substantive review of the exact signed diff.",',
         '"bodyAcceptance": "Pending substantive review of the exact signed diff; "\n'
         '                                  "the direct pair is a precaution, not established synonymy.",'),
    ):
        text = replace_once(text, before, after)
    return text


def main():
    source = TOOLS / SOURCE
    text = derive(frozen(source, SOURCE_SHA).decode("utf-8"))
    compile(text, OUTPUT, "exec")
    print(json.dumps(freeze_json(ROOT / "delta-runtime-tooling-001.json", {
        "producer": binding(__file__), "source": binding(source),
        "output": write_frozen(TOOLS / OUTPUT, text.encode("utf-8")),
        "scope": "Runtime-only verification of the signed direct child of d4406172. Original004 "
                 "initial reviews keep their original candidate. Only 拍 plus manifest may change "
                 "in runtime; metadata adds exactly 響. No semantic, confirmation or delivery acceptance.",
    })))


if __name__ == "__main__":
    main()

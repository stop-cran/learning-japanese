"""Derive a truthful retry without rewriting the failed producer or its partial outputs."""
import json

from b130_context_confirmation import ROOT, binding
from common import TOOLS, freeze_json, frozen, require, write_frozen
from prepare_b130_followup_engine import replace_once


def main():
    source = TOOLS / "prepare_b130_claude004.py"
    text = frozen(source, "ad6094b77234048ec60d13690ac93e2b640c0af5c2ca3beaa058082c8b6ea2c3").decode()
    text = replace_once(text, 'OUTPUT = ROOT / "confirmation-004-claude-neutral"',
                        'OUTPUT = ROOT / "confirmation-004-neutral"')
    text = replace_once(text, "def derive_tools():", """def verify_prepared_tool(path, data):
    require(frozen(path) == data, "Earlier derived tool bytes changed")
    return binding(path)


def derive_tools():""")
    text = replace_once(text, '"output": write_frozen(TOOLS / name, text.encode())',
                        '"output": verify_prepared_tool(TOOLS / name, text.encode())')
    text = replace_once(text, '"memory": memory, "producer": binding(__file__),',
                        '"memory": memory, "producer": binding(__file__),\n'
                        '        "earlierFailedPreparation": binding(ROOT / "claude004-preparation-repair-001.json"),')
    name = "prepare_b130_claude004_v2.py"
    compile(text, name, "exec")
    failed = ROOT / "claude004-preparation-execution-001"
    receipt = json.loads(frozen(failed / "receipt.json"))
    require(receipt["exitCode"] == receipt["childExitCodeAfterCleanup"] == 1
            and receipt["cleanupError"] is None and not receipt["memory"]["breach"],
            "Failure history differs")
    frozen(failed / "output.log", receipt["logSha256"])
    output = write_frozen(TOOLS / name, text.encode())
    print(json.dumps(freeze_json(ROOT / "claude004-preparation-repair-001.json", {
        "source": binding(source), "output": output,
        "retainedFailure": [binding(failed / name) for name in ("receipt.json", "output.log")],
        "retainedPartialXml": [binding(ROOT / "confirmation-004-claude-neutral" / name)
                              for name in ("jmdict-families.xml", "kanjidic2-records.xml")],
        "scope": "Neutral-disclosure check correctly refused a family-named output path. New producer "
                 "uses a separate neutral path and verifies exact prior generated tool bytes instead "
                 "of overwriting them. No spec/chain/admission/report existed for this failed attempt.",
        "producer": binding(__file__),
    })))


if __name__ == "__main__":
    main()

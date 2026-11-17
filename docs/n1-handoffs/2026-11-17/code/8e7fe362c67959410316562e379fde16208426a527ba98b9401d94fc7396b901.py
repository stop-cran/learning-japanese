import json

from b130_context_confirmation import ROOT, binding
from b130_followup_closure_history import PREVIOUS
from common import TOOLS, freeze_json, frozen, write_frozen
from prepare_b130_followup_engine import replace_once


def derive(text):
    text = text.replace("\r\n", "\n")
    text = replace_once(text, "from verify_b130_revision_runtime_v2 import PARENT",
                        f'PARENT = "{PREVIOUS}"')
    return replace_once(text, 'summary["revision"] == "reconciliation-001"',
                        'summary["revision"] == "reconciliation-002"')


def main():
    source = TOOLS / "b130_revision_gates.py"
    text = derive(frozen(source, "3a9c1baa713bdce7e7380a120d42fdafa46733f2b1b0c890cf0a51f227e7e0f7")
                  .decode("utf-8"))
    compile(text, "b130_delta_gates.py", "exec")
    print(json.dumps(freeze_json(ROOT / "delta-gate-tooling-001.json", {
        "producer": binding(__file__), "source": binding(source),
        "output": write_frozen(TOOLS / "b130_delta_gates.py", text.encode("utf-8")),
        "scope": "Only parent and reconciliation label change. Identical ten published-base commands, "
                 "receipt/log hashes, serial order, cleanup and RAM verification.",
    })))


if __name__ == "__main__":
    main()

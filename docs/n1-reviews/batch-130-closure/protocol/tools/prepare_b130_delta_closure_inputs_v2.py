"""Use the actual successful closure-input retry and disclose present-time protocol freezing."""
import json
import sys

from b130_context_confirmation import ROOT, binding
from common import TOOLS, freeze_json, frozen, load_module, require, write_frozen
from prepare_b130_followup_engine import replace_once


def main():
    require(len(sys.argv) == 2 and sys.argv[1] in ("closure", "finalizer"), "closure|finalizer required")
    source = TOOLS / "prepare_b130_delta_closure_inputs.py"
    text = frozen(source, "cd0906d5de3d8eaf1000331be717894c2739e3fe3391de95e70ea5f094d471e9").decode()
    text = replace_once(text, '"delta-closure-inputs-execution-001": 0,',
                        '"delta-closure-inputs-execution-001": 1, "delta-closure-inputs-execution-002": 0,')
    text = replace_once(text, '"delta-closure-test-fix-001.json", "delta-closure-spec-001.json",',
                        '"delta-closure-test-fix-001.json", "delta-closure-spec-001.json",\n'
                        '    "delta-closure-inputs-repair-001.json",')
    text = replace_once(text, '"prelaunch readiness or admission. Successor history tests are separately bound.",',
                        '"prelaunch readiness or admission. The old75-test receipt/log were initially writable "\n'
                        '                 "at closure preparation. Their current exit/log hash/cleanup/RAM and "\n'
                        '                 "75-test output were checked, then those bytes were frozen now; "\n'
                        '                 "no historical read-only state is asserted. Successor history tests "\n'
                        '                 "are separately bound.",')
    name = "prepare_b130_delta_closure_inputs_retry.py"
    compile(text, name, "exec")
    output = TOOLS / name
    if output.exists():
        require(frozen(output) == text.encode(), "Prior explicit retry changed")
    else:
        write_frozen(output, text.encode())
        freeze_json(ROOT / "delta-closure-inputs-repair-001.json", {
            "source": binding(source), "output": binding(output), "producer": binding(__file__),
            "failure": binding(ROOT / "delta-closure-inputs-execution-001" / "receipt.json"),
            "scope": "Original attempt failed before writing readiness/spec on a writable historical "
                     "protocol receipt. Failed001 remains failure; actual successful input retry will "
                     "be002. Old receipt is verified/frozen now, not claimed historically read-only.",
        })
    module = load_module("b130_delta_closure_input_retry", output)
    (module.prepare_closure if sys.argv[1] == "closure" else module.prepare_finalizer)()


if __name__ == "__main__":
    main()

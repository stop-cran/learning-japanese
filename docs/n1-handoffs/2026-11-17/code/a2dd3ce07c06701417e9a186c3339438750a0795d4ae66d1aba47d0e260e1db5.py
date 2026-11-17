"""Use the bound mechanical session for initial acceptances, which omit that field."""
from b130_context_confirmation import ROOT, binding
from common import TOOLS, freeze_json, frozen, write_frozen
from prepare_b130_followup_engine import replace_once

source = TOOLS / "test_b130_delta_closure.py"
text = frozen(source, "081dae0f96473184ad9d0a2f65e8386a1c398dea5cec5fca0eec65b9a8f3e09a").decode()
text = replace_once(text, '"session": row["session"],',
                    '"session": json.loads(frozen(row["final"]["path"], row["final"]["sha256"]))["session"],')
compile(text, "test_b130_delta_closure_v2.py", "exec")
output = write_frozen(TOOLS / "test_b130_delta_closure_v2.py", text.encode())
print(freeze_json(ROOT / "delta-closure-test-fix-001.json", {
    "source": binding(source), "output": output, "producer": binding(__file__),
    "scope": "Correct test-fixture initial-session lookup only; no production checker or evidence change. "
             "Original failed test and execution remain preserved.",
}))

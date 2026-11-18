"""Output-routing-only successor: preserve001 and freeze tested runtime002."""
from pathlib import Path

original = Path(__file__).with_name("stage-tested-runtime.py")
raw = original.read_bytes()
assert raw.count(b"selected-runtime-001") == 2, "Unexpected staging implementation"
derived = raw.replace(b"selected-runtime-001", b"selected-runtime-002")
assert derived.replace(b"selected-runtime-002", b"selected-runtime-001") == raw
exec(compile(derived, str(original), "exec"), {**globals(), "__file__": str(original)})

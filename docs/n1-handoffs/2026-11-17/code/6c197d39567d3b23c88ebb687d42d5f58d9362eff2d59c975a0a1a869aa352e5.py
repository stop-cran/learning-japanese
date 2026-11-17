"""Same complete neutral checks, using the explicit pinned continuation-v2 adapter."""
from pathlib import Path

source = Path(__file__).with_name("check-actual-readiness.py")
raw = source.read_bytes()
replacements = {
    b"selected-runtime-002": b"selected-runtime-003",
    b"import b134_integration_confirmation_v1 as tool":
        b"import b134_revision_confirmation_v2 as driver\ntool = driver.legacy",
    b"revision-confirmation-claude-002": b"revision-confirmation-claude-003",
    b"revision-confirmation-gpt-001": b"revision-confirmation-gpt-002",
    b"actual-readiness.json": b"actual-readiness-v2.json",
}
derived = raw
for before, after in replacements.items():
    assert derived.count(before) == 1, "Readiness adapter anchor differs"
    derived = derived.replace(before, after)
exec(compile(derived, str(source), "exec"), {**globals(), "__file__": str(source)})

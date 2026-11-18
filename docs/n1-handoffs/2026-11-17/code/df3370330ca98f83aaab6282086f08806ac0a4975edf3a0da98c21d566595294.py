"""Preserve the prepared verifier and normalize Markdown line endings before parsing."""
from pathlib import Path

from common import freeze_json, frozen, require, sha, write_frozen
from confirm_v2 import binding

HERE = Path(__file__).resolve().parent
source = HERE / "verify_b120_correction.py"
raw = frozen(source)
changes = [(b"parse(before)", b'parse(before.replace("\\r\\n", "\\n"))'),
           (b"parse(after)", b'parse(after.replace("\\r\\n", "\\n"))')]
derived = raw
for before, after in changes:
    require(derived.count(before) == 1, "Parse anchor changed")
    derived = derived.replace(before, after)
reversed_bytes = derived
for before, after in reversed(changes):
    reversed_bytes = reversed_bytes.replace(after, before)
require(reversed_bytes == raw, "Verifier reverse proof failed")
compile(derived, "verify_b120_correction_v2.py", "exec")
verifier = write_frozen(HERE / "verify_b120_correction_v2.py", derived)
test_source = HERE / "test_verify_b120_correction.py"
test_raw = frozen(test_source)
test = test_raw.replace(b"from verify_b120_correction import", b"from verify_b120_correction_v2 import")
anchor = b"    def test_metadata_old_guard_and_unrelated_teaching_must_remain(self):"
extra = (
    b"    def test_actual_crlf_markdown_uses_the_same_preservation_rules(self):\n"
    b'        before = (CARD + BODY).replace("\\n", "\\r\\n")\n'
    b'        after = (GUARD + BODY).replace("Metadata:", NOTE + "Metadata:").replace("\\n", "\\r\\n")\n'
    b"        self.assertEqual(verify_pair_change(before, after)[\"changedBodyPassages\"], 1)\n\n"
)
if b"\r\n" in test_raw:
    extra = extra.replace(b"\n", b"\r\n")
require(test.count(anchor) == 1, "Test anchor changed")
test = test.replace(anchor, extra + anchor)
compile(test, "test_verify_b120_correction_v2.py", "exec")
tests = write_frozen(HERE / "test_verify_b120_correction_v2.py", test)
print(freeze_json(HERE / "b120-correction-v2-derivation.json", {
    "source": binding(source), "testSource": binding(test_source),
    "verifier": verifier, "tests": tests, "reverseExact": True,
    "change": "Normalize CRLF to LF before existing Markdown parsing; retain raw signed/source hashes.",
    "priorFailure": "The prepared verifier failed on the actual CRLF card at parse(...).items "
                    "with AttributeError; no verification receipt was written.",
}))

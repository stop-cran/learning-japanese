"""Preserve the failed v2 and compare the supplement's text with normalized log text."""
from pathlib import Path

from common import TOOLS, freeze_json, frozen, require, sha, write_frozen
from verify_b128_reconciliation import REVIEW


def main():
    previous = frozen(REVIEW / "reconciliation-verifier-v2-derivation.json")
    import json
    record = json.loads(previous)
    source = TOOLS / "verify_b128_reconciliation_v2.py"
    original = frozen(source, record["output"]["sha256"])
    before = b'== pin(COMMITTED_GATES / "budget.log"),'
    after = b'== pin(COMMITTED_GATES / "budget.log").replace(b"\\r\\n", b"\\n"),'
    require(original.count(before) == 1, "Budget comparison changed")
    derived = original.replace(before, after)
    require(derived.replace(after, before) == original, "Verifier derivation is not reversible")
    compile(derived, "verify_b128_reconciliation_v3.py", "exec")
    tests_path = TOOLS / "test_verify_b128_reconciliation_v2.py"
    tests = frozen(tests_path)
    old_import = b"import verify_b128_reconciliation_v2 as v"
    new_import = b"import verify_b128_reconciliation_v3 as v"
    require(tests.count(old_import) == 1, "Recovery test import changed")
    derived_tests = tests.replace(old_import, new_import)
    require(derived_tests.replace(new_import, old_import) == tests, "Test derivation is not reversible")
    target = write_frozen(TOOLS / "verify_b128_reconciliation_v3.py", derived)
    target_tests = write_frozen(TOOLS / "test_verify_b128_reconciliation_v3.py", derived_tests)
    print(freeze_json(REVIEW / "reconciliation-verifier-v3-derivation.json", {
        "source": {"path": str(source), "sha256": sha(original)}, "output": target,
        "testSource": {"path": str(tests_path), "sha256": sha(tests)}, "tests": target_tests,
        "reverseExact": True,
        "reason": "The supplement was produced with text-mode reads and contains LF; the committed "
                  "Windows budget log has CRLF. Compare normalized text only for this redundant "
                  "summary. The original raw log, supplement and all execution hashes remain pinned.",
        "priorDerivationSha256": sha(previous), "producerSha256": sha(Path(__file__).read_bytes()),
    }))


if __name__ == "__main__":
    main()

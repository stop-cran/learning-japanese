"""Preserve the first verifier while handling Git's CR-terminated primary fingerprint."""
from pathlib import Path

from common import TOOLS, freeze_json, frozen, require, sha, write_frozen
from verify_b127_reconciliation import REVIEW


def main():
    source = TOOLS / "verify_b127_reconciliation.py"
    original = frozen(source, "27311173b29b78fef459066933257441026ccc9735b51364c6384e2ed73369a1")
    before = (
        'git(config, "show", "-s", "--format=%P|%G?|%GF|%GP|%ae|%ce", CANDIDATE).decode().strip()'
    ).encode()
    after = (
        '"|".join(field.strip() for field in git(config, "show", "-s", '
        '"--format=%P|%G?|%GF|%GP|%ae|%ce", CANDIDATE).decode().strip().split("|"))'
    ).encode()
    require(original.count(before) == 1 and after not in original, "Unexpected signature check")
    derived = original.replace(before, after)
    require(derived.replace(after, before) == original, "Non-reversible derivation")
    compile(derived, "verify_b127_reconciliation_v2.py", "exec")
    target = write_frozen(TOOLS / "verify_b127_reconciliation_v2.py", derived)
    print(freeze_json(REVIEW / "reconciliation-verifier-v2-derivation.json", {
        "source": {"path": str(source), "sha256": sha(original)}, "output": target,
        "before": before.decode(), "after": after.decode(), "reverseExact": True,
        "reason": "The observed Git %GP output retains one CR before its field separator on Windows. "
                  "Trim whitespace at each field boundary, retaining exact checks of all six fields.",
        "diagnostic": str(REVIEW / "reconciliation-signature-diagnostic-001"),
        "producerSha256": sha(Path(__file__).read_bytes()),
    }))


if __name__ == "__main__":
    main()

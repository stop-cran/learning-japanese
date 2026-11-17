"""Import-only repair of frozen protocol014; execute its real CLI without rebinding config."""
import sys
from pathlib import Path

ORIGINAL = Path(r"C:\Users\stop-\n1-kanji-workspace\scratch-134\review\fresh-independent-002\lifecycle-011\protocol-014")
sys.path.insert(0, str(ORIGINAL))
from b134_common import BASE, CANDIDATE, frozen, sha, write_frozen, freeze_json
from common import load_module
from b134_initial_records import INITIALS

OLD_AUDIT_SHA = "1fbc57b7f26cfbf099de828dbeb9b34d643a643262b5fa1b2c42329bedde81f6"
ROOT = Path(__file__).resolve().parent


def main(argv=None):
    source = ORIGINAL / "audit-review-b134-014.py"
    frozen(source, OLD_AUDIT_SHA)
    frozen(Path(__file__))
    auditor = load_module("b134_protocol014_import_repair", source)
    # These are precisely the three missing names; all original main checks remain.
    auditor.BASE, auditor.CANDIDATE, auditor.INITIALS = BASE, CANDIDATE, INITIALS
    code = auditor.main(argv)
    return code


if __name__ == "__main__":
    sys.exit(main())

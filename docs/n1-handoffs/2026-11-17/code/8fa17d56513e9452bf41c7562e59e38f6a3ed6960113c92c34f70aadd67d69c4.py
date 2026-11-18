"""Run frozen controller014 with an explicitly pinned import-only auditor repair."""
import sys
from pathlib import Path

ORIGINAL = Path(r"C:\Users\stop-\n1-kanji-workspace\scratch-134\review\fresh-independent-002\lifecycle-011\protocol-014")
sys.path.insert(0, str(ORIGINAL))
from b134_common import frozen
from common import load_module

OLD_CONTROLLER_SHA = "940638df7a5ef763f2e5b932115bb447d85129577d3a0770b72138f6baa605df"
AUDIT_SHA = "9e5b4466dc0f095dac12c505269b64c89401ae2366bc9c2e823a1f161f501479"


def main():
    source = ORIGINAL / "step-b134-014.py"
    frozen(source, OLD_CONTROLLER_SHA)
    auditor = Path(__file__).with_name("audit-entry.py")
    frozen(auditor, AUDIT_SHA)
    controller = load_module("b134_protocol014_repair_controller", source)
    controller.AUDIT_PATH, controller.AUDIT_SHA = auditor, AUDIT_SHA
    return controller.main()


if __name__ == "__main__":
    sys.exit(main())

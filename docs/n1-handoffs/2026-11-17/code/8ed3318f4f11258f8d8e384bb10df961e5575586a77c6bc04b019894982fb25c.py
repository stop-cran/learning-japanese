"""Frozen014 lifecycle + import-only auditor repair + D/E delimiter repair.

Original config/bootstrap/authorization and both original producer hashes are checked
unchanged. Only child invocation of the pinned original checker is redirected to the
pinned external checker entry; its output carries old/new/executed checker hashes.
No new acceptance is created except by the original explicit final/accept actions.
"""
import sys
from pathlib import Path

ORIGINAL = Path(r"C:\Users\stop-\n1-kanji-workspace\scratch-134\review\fresh-independent-002\lifecycle-011\protocol-014")
sys.path.insert(0, str(ORIGINAL))
from b134_common import frozen
from common import load_module

CONTROLLER_SHA = "940638df7a5ef763f2e5b932115bb447d85129577d3a0770b72138f6baa605df"
AUDIT_SHA = "9e5b4466dc0f095dac12c505269b64c89401ae2366bc9c2e823a1f161f501479"
OLD_CHECKER_SHA = "f68265d947785a19aaa79480303bb1481b13ea5670ee2a25181ea50dba4aac2d"
CHECKER_SHA = "3f512c1b0fd5f96dc4bffa0e816b4be89faa8f77355ec43f1f5e7c24531cecf8"


def load_controller():
    source = ORIGINAL / "step-b134-014.py"
    frozen(source, CONTROLLER_SHA)
    auditor = Path(__file__).parent.parent / "lifecycle-runtime-repair-001" / "audit-entry.py"
    checker = Path(__file__).with_name("checker-entry.py")
    old_checker = ORIGINAL / "check-report-structure-b134-014.py"
    frozen(auditor, AUDIT_SHA)
    frozen(old_checker, OLD_CHECKER_SHA)
    frozen(checker, CHECKER_SHA)
    controller = load_module("b134_protocol014_report_checker_repair", source)
    controller.AUDIT_PATH, controller.AUDIT_SHA = auditor, AUDIT_SHA
    original_child = controller.child

    def child(*args):
        if args and Path(args[0]) == old_checker:
            frozen(old_checker, OLD_CHECKER_SHA)
            frozen(checker, CHECKER_SHA)
            return original_child(checker, *args[1:])
        return original_child(*args)

    controller.child = child
    return controller


if __name__ == "__main__":
    sys.exit(load_controller().main())

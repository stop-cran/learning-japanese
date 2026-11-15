"""Isolate repeated audit fixture outputs without modifying production audit gates."""
import json
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha
from derive_selected_followups import derive_file


def main():
    review = WS / "scratch-124" / "review"
    out = review / "confirm"
    preflight_path = out / "tooling-preflight.json"
    preflight = json.loads(frozen(preflight_path))
    log = frozen(preflight["tests"]["path"], preflight["tests"]["sha256"])
    require(preflight["exitCode"] == 1 and b"FileExistsError" in log
            and b"test_slice_binding_integrity_and_errors" in log,
            "Expected repeated-fixture output collision was not recorded")
    for item in preflight["derivations"]:
        frozen(item["source"]["path"], item["source"]["sha256"])
        frozen(item["output"]["path"], item["output"]["sha256"])
    test = derive_file(str(out / "test-audit-confirm.py"),
                       str(out / "test-audit-confirm-isolated.py"), [
        ('        module.OUTPUT_BASE = self.root / "audits"\n',
         '        module.OUTPUT_BASE = self.root / "audits"\n'
         '        self.audit_invocations = 0\n'),
        ('    def run_main(self, record, offset=None, prefix_sha=None, final=True):\n',
         '    def run_main(self, record, offset=None, prefix_sha=None, final=True):\n'
         '        module.OUTPUT_BASE = self.root / f"audits-{self.audit_invocations}"\n'
         '        self.audit_invocations += 1\n'),
    ])
    print(json.dumps(freeze_json(out / "test-fixture-derivation-001.json", {
        "failedPreflight": {"path": str(preflight_path), "sha256": sha(frozen(preflight_path))},
        "test": test,
        "producer": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "scope": "Repeated calls in one fixture had the same run/output root and collided "
                 "when the clock returned the same timestamp. Each fixture call now has "
                 "its own temporary output root. Every assertion and production audit byte "
                 "is unchanged. No tests or gates have been disabled; run the complete "
                 "21-test suite before accepting this recovery.",
    })))


if __name__ == "__main__":
    main()

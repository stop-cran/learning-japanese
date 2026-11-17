import json
import unittest
from pathlib import Path

from b130_context_confirmation import ROOT
from b130_excluded_initials_v3 import archive_excluded
from b130_void_initial_audit import bounded_void_initial, excluded_audit_support
from common import WS, frozen, load_module, sha


class RealExcludedAuditTests(unittest.TestCase):
    def test_real_excluded_archive_uses_real_bounded_support(self):
        support = load_module("b130_real_bound_audit_test", WS / "scratch-115" / "assemble-closure.py")
        contents = {}

        def copy(path, name, expected=None):
            contents[name] = frozen(path, expected)
            return {"path": name, "sha256": sha(contents[name])}

        def binding(item, name):
            return copy(Path(item["path"]), name, item["sha256"])

        def dump(name, item):
            contents[name] = json.dumps(item, ensure_ascii=False).encode()

        def chain(path, name):
            manifest = json.loads(frozen(path))
            return {"path": name, "segments": len(manifest["segments"])}

        paths = [ROOT / f"N1-B130-CLAUDE-00{n}-hold.json" for n in (1, 2, 3)]
        held = json.loads(frozen(paths[0]))
        result = archive_excluded(paths, 130, held["candidate"], set(), copy, binding, dump,
                                  chain, excluded_audit_support(support), ROOT)
        self.assertEqual(len(result), 3)
        self.assertFalse(any(row["reviewAccepted"] or row["finalAcceptance"] for row in result))
        for n in (2, 3):
            held = json.loads(frozen(paths[n - 1]))
            audit = json.loads(frozen(held["audit"]["path"], held["audit"]["sha256"]))
            with self.assertRaises(AssertionError):
                support.bounded_audit(Path(held["audit"]["path"]))
            summary = json.loads(contents[f"excluded-initials/N1-B130-CLAUDE-00{n}/audit-summary.json"])
            self.assertEqual(summary["status"], "VOID")
            self.assertEqual(summary["breaches"], audit["breaches"])
            self.assertEqual(summary["unexpectedUserMessages"], audit["unexpectedUserMessages"])
            self.assertFalse(summary["reviewAccepted"])
            self.assertNotIn("calls", summary)

    def test_no_accepted_audit_can_enter_void_representation(self):
        final = json.loads(frozen(ROOT / "confirm" / "N1-B130-GPT-CONFIRM-003-final.json"))
        with self.assertRaises(ValueError):
            bounded_void_initial(final["audit"]["path"])


if __name__ == "__main__":
    unittest.main()

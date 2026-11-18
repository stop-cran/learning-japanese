import copy
import json
import unittest

from b131_base_binding import (
    CANDIDATE_BASE, SOURCE_BASE, verify_baseline_trees, verify_scan_bindings,
)
from common import sha


class BaseBindingTests(unittest.TestCase):
    def scan_fixture(self):
        scans = {
            "scans/example.json": json.dumps({"base": SOURCE_BASE, "matches": []}).encode(),
            "scans-002/example.json": json.dumps({"base": SOURCE_BASE, "matches": ["x"]}).encode(),
        }
        return {"originalScans": {path: sha(raw) for path, raw in scans.items()}}, scans

    def test_exact_original_scans_are_accepted_but_rewritten_bytes_are_not(self):
        record, scans = self.scan_fixture()
        self.assertEqual(verify_scan_bindings(record, scans), record["originalScans"])
        scans["scans/example.json"] += b"\n"
        with self.assertRaisesRegex(ValueError, "bytes changed"):
            verify_scan_bindings(record, scans)

    def test_relabelling_is_rejected_even_with_a_matching_recomputed_hash(self):
        record, scans = self.scan_fixture()
        path = "scans/example.json"
        scans[path] = scans[path].replace(SOURCE_BASE.encode(), CANDIDATE_BASE.encode())
        record["originalScans"][path] = sha(scans[path])
        with self.assertRaisesRegex(ValueError, "relabelled"):
            verify_scan_bindings(record, scans)

    def test_missing_and_unrecorded_scans_are_rejected(self):
        record, scans = self.scan_fixture()
        missing, extra = copy.deepcopy(scans), copy.deepcopy(scans)
        del missing["scans/example.json"]
        extra["scans-003/example.json"] = b"{}"
        for changed in (missing, extra):
            with self.subTest(paths=list(changed)):
                with self.assertRaisesRegex(ValueError, "inventory"):
                    verify_scan_bindings(record, changed)

    def test_names_modes_and_blob_changes_cannot_hide_behind_equal_counts(self):
        original = b"100644 blob " + b"a" * 40 + b"\tkanji/example.md\0"
        record = {"baselineKanjiTreeSha256": sha(original), "baselineKanjiEntries": 1}
        self.assertEqual(verify_baseline_trees(record, original, original), 1)
        for incoming in (
            original.replace(b"100644", b"100755"),
            original.replace(b"example.md", b"renamed.md"),
            original.replace(b"a" * 40, b"b" * 40),
        ):
            with self.subTest(incoming=incoming):
                with self.assertRaisesRegex(ValueError, "trees differ"):
                    verify_baseline_trees(record, original, incoming)


if __name__ == "__main__":
    unittest.main()

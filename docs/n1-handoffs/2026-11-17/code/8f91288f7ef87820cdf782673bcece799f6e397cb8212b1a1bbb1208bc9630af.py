import copy
import gzip
import unittest
from types import SimpleNamespace

from b133_closure_retention import retain_overlapping_chains
from close_b132 import publication_findings
from common import json_bytes, sha


class RetentionControls(unittest.TestCase):
    def test_overlap_moves_only_exact_payload_to_local_retention(self):
        raw = ("漢" * 32).encode()
        row = {"path": "01-piece.txt", "index": 1, "sha256": sha(raw),
               "parts": [{"source": "card", "sha256": sha(raw), "a": 1, "b": 1}]}
        retention = {"archivedSegmentIndices": [1], "localOnlySegments": []}
        manifest = json_bytes({"segments": [row]})
        files = {"chains/demo/manifest.json": manifest,
                 "chains/demo/retention.json": json_bytes(retention),
                 "chains/demo/01-piece.txt.gz": gzip.compress(raw),
                 "report.md": b"Original report unchanged."}
        guard = SimpleNamespace(check=lambda: None)
        before = copy.deepcopy(files)
        result = retain_overlapping_chains(files, {"漢" * 32}, set(), guard, {"demo": retention})
        self.assertEqual(len(result), 1)
        self.assertEqual(files["chains/demo/manifest.json"], manifest)
        self.assertEqual(files["report.md"], before["report.md"])
        self.assertEqual(retention["archivedSegmentIndices"], [])
        self.assertEqual(retention["localOnlySegments"][0]["sha256"], sha(raw))
        self.assertEqual(publication_findings(files, {"漢" * 32}, set(), guard), ([], []))
        self.assertEqual(gzip.decompress(before["chains/demo/01-piece.txt.gz"]), raw)

    def test_reports_and_unknown_identities_cannot_be_silently_removed(self):
        guard = SimpleNamespace(check=lambda: None)
        for files in (
            {"report.md": ("漢" * 32).encode()},
            {"report.md": b"12345678-1234-1234-1234-123456789abc"},
        ):
            before = copy.deepcopy(files)
            with self.assertRaises(ValueError):
                retain_overlapping_chains(files, {"漢" * 32}, set(), guard, {})
            self.assertEqual(files, before)


if __name__ == "__main__":
    unittest.main()

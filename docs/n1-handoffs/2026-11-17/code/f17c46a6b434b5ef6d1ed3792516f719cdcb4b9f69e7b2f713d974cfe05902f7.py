import gzip
import json
import unittest

from archive_b124_chains import prepare
from common import json_bytes, sha


class ArchiveChainsTests(unittest.TestCase):
    def fixture(self, source):
        raw = b"synthetic source contents\n"
        path = r"C:\synthetic\01.txt"
        manifest = {"segments": [{
            "index": 1, "path": path, "sha256": sha(raw),
            "parts": [{"source": source, "sha256": sha(raw), "a": 1, "b": 1}],
        }]}
        return json_bytes(manifest), {path: raw}

    def test_complete_external_extract_and_mixed_segment_stay_local(self):
        manifest_raw, segments = self.fixture("evidence/external-snapshots/01-extract.txt")
        manifest = json.loads(manifest_raw)
        manifest["segments"][0]["parts"].append({
            "source": "repo/kanji/example.md", "sha256": "a" * 64, "a": 1, "b": 2,
        })
        manifest_raw = json_bytes(manifest)
        files, retention = prepare(manifest_raw, segments)
        self.assertEqual(set(files), {"manifest.json", "retention.json"})
        self.assertEqual(files["manifest.json"], manifest_raw)
        self.assertEqual(retention["archivedSegmentIndices"], [])
        self.assertEqual(retention["localOnlySegments"][0]["index"], 1)
        self.assertEqual(retention["localOnlySegments"][0]["sha256"],
                         sha(next(iter(segments.values()))))
        self.assertNotIn(b"synthetic source contents", b"".join(files.values()))

    def test_metadata_only_segment_is_archived_byte_exactly(self):
        manifest_raw, segments = self.fixture("evidence/external-snapshots/manifest.json")
        files, retention = prepare(manifest_raw, segments)
        self.assertEqual(gzip.decompress(files["01.txt.gz"]), next(iter(segments.values())))
        self.assertEqual(retention["archivedSegmentIndices"], [1])
        self.assertEqual(retention["localOnlySegments"], [])

    def test_tampered_or_missing_local_only_segment_is_rejected(self):
        manifest_raw, segments = self.fixture("evidence/external-snapshots/01-extract.txt")
        with self.assertRaisesRegex(ValueError, "hash differs"):
            prepare(manifest_raw, {path: raw + b"changed" for path, raw in segments.items()})
        with self.assertRaisesRegex(ValueError, "segment set differs"):
            prepare(manifest_raw, {})


if __name__ == "__main__":
    unittest.main()

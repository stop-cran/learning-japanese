import copy
import gzip
import json
import unittest

from archive_b124_chains_v2 import prepare
from common import json_bytes, sha
from verify_b128_archive import verify_chain


class ArchiveVerificationTests(unittest.TestCase):
    def fixture(self, prefix=""):
        public, private = b"reviewed licensed source\n", b"complete external capture\n"
        segments = [
            {"index": index, "path": rf"C:\synthetic\{index:02}.txt",
             "sha256": sha(raw), "bytes": len(raw),
             "parts": [{"source": source, "sha256": sha(raw), "a": 1, "b": 1}]}
            for index, raw, source in (
                (1, public, "repo/kanji/example.md"),
                (2, private, prefix + "evidence/external-snapshots/01-extract.txt"),
            )
        ]
        files, retention = prepare(json_bytes({"segments": segments}),
                                   {segments[0]["path"]: public, segments[1]["path"]: private})
        binding = {
            "segments": 2, "manifestSha256": sha(files["manifest.json"]),
            "retentionSha256": sha(files["retention.json"]),
            "archivedSegmentIndices": [1], "localOnlySegmentIndices": [2],
        }
        return files, binding, private

    def test_mixed_archive_preserves_reviewed_bytes_and_omission(self):
        files, binding, _ = self.fixture()
        result = verify_chain(files, binding)
        self.assertEqual(result["archivedSegments"], 1)
        self.assertEqual(result["localOnlySegments"], 1)

    def test_adding_omitted_capture_is_rejected(self):
        files, binding, private = self.fixture()
        files["02.txt.gz"] = gzip.compress(private, mtime=0)
        with self.assertRaisesRegex(ValueError, "local-only segment published"):
            verify_chain(files, binding)

    def test_rehashed_false_retention_inventory_is_rejected(self):
        files, binding, _ = self.fixture()
        retention = json.loads(files["retention.json"])
        retention["localOnlySegments"][0]["sources"][0]["lastLine"] = 2
        files["retention.json"] = json_bytes(retention)
        binding["retentionSha256"] = sha(files["retention.json"])
        with self.assertRaisesRegex(ValueError, "inventory"):
            verify_chain(files, binding)

    def test_missing_changed_and_oversized_public_segments_are_rejected(self):
        files, binding, _ = self.fixture()
        for replacement in (None, gzip.compress(b"different\n"), gzip.compress(b"x" * 100000)):
            with self.subTest(replacement_size=None if replacement is None else len(replacement)):
                changed = copy.deepcopy(files)
                if replacement is None:
                    del changed["01.txt.gz"]
                else:
                    changed["01.txt.gz"] = replacement
                with self.assertRaises(ValueError):
                    verify_chain(changed, binding)


    def test_wrapped_capture_is_omitted_and_cannot_be_restored(self):
        files, binding, private = self.fixture("original-packet/")
        self.assertEqual(verify_chain(files, binding)["localOnlySegments"], 1)
        files["02.txt.gz"] = gzip.compress(private, mtime=0)
        with self.assertRaisesRegex(ValueError, "local-only segment published"):
            verify_chain(files, binding)


if __name__ == "__main__":
    unittest.main()

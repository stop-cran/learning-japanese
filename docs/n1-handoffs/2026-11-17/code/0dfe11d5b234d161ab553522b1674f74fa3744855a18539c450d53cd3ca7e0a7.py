import gzip
import json
import unittest

from archive_b129_chains import prepare
from common import WS, frozen, json_bytes, sha
from verify_b130_archive import verify_chain


class B130ArchiveRetentionTests(unittest.TestCase):
    def binding(self, files, retention):
        return {
            "segments": retention["originalSegments"],
            "manifestSha256": sha(files["manifest.json"]),
            "retentionSha256": sha(files["retention.json"]),
            "archivedSegmentIndices": retention["archivedSegmentIndices"],
            "localOnlySegmentIndices": [row["index"] for row in retention["localOnlySegments"]],
        }

    def test_complete_source_labels_and_colocated_material_stay_local(self):
        for source in ("external-reconciliation/source.txt", "original-source-sections/source.txt",
                       "original-packet/evidence/external-snapshots/01-extract.txt"):
            with self.subTest(source=source):
                raw = b"reviewed public evidence\ncomplete external article\n"
                manifest = {"segments": [{
                    "index": 1, "path": r"C:\synthetic\01.txt", "bytes": len(raw), "sha256": sha(raw),
                    "parts": [
                        {"source": "repo/kanji/example.md", "sha256": "a" * 64, "a": 1, "b": 1},
                        {"source": source, "sha256": "b" * 64, "a": 1, "b": 1},
                    ],
                }]}
                files, retention = prepare(json_bytes(manifest), {manifest["segments"][0]["path"]: raw})
                binding = self.binding(files, retention)
                self.assertEqual(verify_chain(files, binding)["localOnlySegments"], 1)
                self.assertEqual(set(files), {"manifest.json", "retention.json"})
                files["01.txt.gz"] = gzip.compress(raw, mtime=0)
                with self.assertRaisesRegex(ValueError, "local-only segment published"):
                    verify_chain(files, binding)

    def test_actual_b130_core_archives_exact_public_segments_only(self):
        raw = frozen(
            WS / "scratch-130" / "review" / "core-chain.json",
            "2d4c53f2daf0f5e26f14bbc685b13d8aa854e243a40fb5f94ad445b23afe52bd",
        )
        manifest = json.loads(raw)
        files, retention = prepare(raw, {
            row["path"]: frozen(row["path"], row["sha256"]) for row in manifest["segments"]
        })
        result = verify_chain(files, self.binding(files, retention))
        self.assertGreater(result["localOnlySegments"], 0)
        self.assertGreater(result["archivedSegments"], 0)
        self.assertEqual(result["originalSegments"], len(manifest["segments"]))


if __name__ == "__main__":
    unittest.main()

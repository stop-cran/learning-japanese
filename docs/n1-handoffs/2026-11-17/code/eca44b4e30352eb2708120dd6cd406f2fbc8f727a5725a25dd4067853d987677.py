import gzip
import tempfile
import unittest
from pathlib import Path

from close_b132_reconciled import keep_confirmation_chain
from common import freeze_json, sha, write_frozen


class ReconciledRetentionTests(unittest.TestCase):
    def test_complete_reconciliation_captures_never_enter_archive(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            rows = []
            for index, source in enumerate(("source-reconciliation-001/external/marker.txt",
                                             "survey-001/external/target.txt", "snapshot/kanji/target.md"), 1):
                raw = ("synthetic source " + source + "\n").encode()
                path = root / (str(index) + ".txt")
                write_frozen(path, raw)
                rows.append({"index": index, "path": str(path), "sha256": sha(raw), "bytes": len(raw),
                             "parts": [{"source": source, "sha256": sha(raw), "a": 1, "b": 1}]})
            manifest = root / "manifest.json"
            freeze_json(manifest, {"segments": rows})
            files = {}
            retained = keep_confirmation_chain(files, "synthetic", manifest)
            self.assertEqual(retained["archivedSegmentIndices"], [3])
            self.assertEqual([row["index"] for row in retained["localOnlySegments"]], [1, 2])
            compressed = [raw for name, raw in files.items() if name.endswith(".gz")]
            self.assertEqual(len(compressed), 1)
            self.assertIn(b"snapshot/kanji/target.md", gzip.decompress(compressed[0]))
            for path in root.iterdir():
                path.chmod(0o644)


if __name__ == "__main__":
    unittest.main()

import contextlib
import gzip
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import verify_b130_archive_v2 as verifier
from archive_b129_chains import prepare
from common import freeze_json, json_bytes, sha, write_frozen


class HeldArchiveTests(unittest.TestCase):
    def run_fixture(self, directory, tamper_held=False):
        root = Path(directory)
        config = {"repo": str(root), "candidate": "a" * 40, "base": "b" * 40, "members": ["X"]}
        closure = root / "docs" / "n1-reviews" / "batch-130-closure"
        reviews, inventory = [], {}
        for label in ("accepted", "held"):
            raw = b"complete reviewed source\n"
            segment = {
                "index": 1, "path": rf"C:\synthetic\{label}.txt", "bytes": len(raw), "sha256": sha(raw),
                "parts": [{"source": "repo/kanji/X.md", "sha256": sha(raw), "a": 1, "b": 1}],
            }
            files, retention = prepare(json_bytes({"segments": [segment]}), {segment["path"]: raw})
            if label == "held" and tamper_held:
                files["held.txt.gz"] = gzip.compress(b"tampered but rehashed publication file\n", mtime=0)
            for name, data in files.items():
                relative = f"{label}/{name}"
                write_frozen(closure / relative, data)
                inventory[relative] = sha(data)
            reviews.append({
                "run": label,
                "chains": [{
                    "path": label, "segments": 1,
                    "manifestSha256": sha(files["manifest.json"]),
                    "retentionSha256": sha(files["retention.json"]),
                    "archivedSegmentIndices": retention["archivedSegmentIndices"],
                    "localOnlySegmentIndices": [],
                }],
            })
        freeze_json(closure / "provenance.json", {
            "batch": 130, "initialSnapshot": config["candidate"], "reviewedSnapshot": "c" * 40,
            "base": config["base"], "members": config["members"],
            "recordedFileSha256": inventory, "reviewLineage": [reviews[0]],
            "excludedInitialRuns": [reviews[1]],
        })
        guard = Mock()
        guard.finish.return_value = {"breach": None}
        output = root / "result.json"
        with patch.object(verifier, "load_batch", return_value=config), \
                patch.object(verifier, "start_guard", return_value=(guard, None)), \
                contextlib.redirect_stdout(io.StringIO()):
            verifier.main(output)
        return json.loads(output.read_bytes())

    def test_verifier_includes_unaccepted_held_chain(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_fixture(directory)
            self.assertEqual([row["run"] for row in result["chains"]], ["accepted", "held"])
            self.assertEqual(result["status"], "PASS")

    def test_rehashing_tampered_held_publication_bytes_cannot_skip_original_chain_binding(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "Published segment differs"):
                self.run_fixture(directory, tamper_held=True)


if __name__ == "__main__":
    unittest.main()

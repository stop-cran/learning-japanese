import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import verify_b118_revision as verifier
from common import sha, write_frozen


class GateBindingTests(unittest.TestCase):
    def test_manifest_hash_and_startup_threshold_are_required(self):
        manifest = b"manifest"
        for wrong_hash, memory in ((False, 3 * 1024 ** 3), (True, 3 * 1024 ** 3),
                                   (False, 2 * 1024 ** 3)):
            with self.subTest(wrong_hash=wrong_hash, memory=memory), tempfile.TemporaryDirectory() as temp:
                directory = Path(temp)
                log = write_frozen(directory / "manifest.log", b"success")
                write_frozen(directory / "manifest.json", json.dumps({
                    "gate": "manifest", "exitCode": 0, "logSha256": log["sha256"],
                    "manifestSha256": sha(b"other" if wrong_hash else manifest),
                    "memory": {"breach": None, "freeRamBeforeBytes": memory,
                               "minimumObservedFreeRamBytes": 2 * 1024 ** 3},
                }).encode())
                with patch.object(verifier, "CHECKS", ("manifest",)):
                    if wrong_hash or memory <= 2 * 1024 ** 3:
                        with self.assertRaises(ValueError):
                            verifier.verify_gates(directory, manifest, {}, Mock())
                    else:
                        self.assertEqual(len(verifier.verify_gates(directory, manifest, {}, Mock())), 1)
                for path in directory.iterdir():
                    path.chmod(0o644)


if __name__ == "__main__":
    unittest.main()

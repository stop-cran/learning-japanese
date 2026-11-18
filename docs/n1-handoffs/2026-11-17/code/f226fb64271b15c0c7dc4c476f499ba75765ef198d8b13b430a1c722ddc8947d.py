import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

from common import CHECKS, sha
from verify_b117_revision import verify_gates


class RevisionGateTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="n1-revision-gates-")
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.manifest = b'{"contentVersion":"fixture"}'
        for name in CHECKS:
            if name == "reading-exposure":
                name = "reading-exposure-supplemental"
                log = "Supplemental source-attested reading: 維=ゆい; original audit unchanged.\n"
            else:
                log = "PASS\n"
            self.write_gate(name, log.encode("utf-8"))

    def write_gate(self, name, log):
        (self.root / f"{name}.log").write_bytes(log)
        receipt = {
            "gate": name, "exitCode": 0, "logSha256": sha(log),
            "memory": {"breach": False, "minimumObservedFreeRamBytes": 2 * 1024 ** 3},
            "manifestSha256": sha(self.manifest), "manifestReproducible": True,
        }
        (self.root / f"{name}.json").write_text(json.dumps(receipt), encoding="utf-8")

    def test_accepts_author_runner_supplemental_receipt(self):
        receipts = verify_gates(self.root, self.manifest, Mock())
        self.assertEqual(len(receipts), 10)
        self.assertIn("reading-exposure-supplemental", [r["gate"] for r in receipts])

    def test_original_audit_cannot_substitute_for_supplemental_audit(self):
        self.write_gate("reading-exposure-supplemental", b"Original audit: PASS\n")
        with self.assertRaisesRegex(ValueError, "Supplemental reading was not included"):
            verify_gates(self.root, self.manifest, Mock())

    def test_changed_manifest_cannot_use_old_receipts(self):
        with self.assertRaisesRegex(ValueError, "Gate manifest mismatch"):
            verify_gates(self.root, self.manifest + b"\n", Mock())


if __name__ == "__main__":
    unittest.main()

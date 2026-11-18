import os
import tempfile
import unittest
from pathlib import Path

import verify_b128_reconciliation_v2 as v


CANDIDATE = "7b3fd5c13c20f4b456723abe3de0ac42c4390bd4"


class ResumeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.directory = Path(self.temp.name)
        source = v.SCRATCH / "reconciliation-handoff-001"
        for path in source.iterdir():
            (self.directory / path.name).write_bytes(path.read_bytes())

    def tearDown(self):
        for path in self.directory.iterdir():
            os.chmod(path, 0o666)
        self.temp.cleanup()

    def test_exact_completed_recovery_passes(self):
        result = v.check_resume(self.directory, CANDIDATE)
        self.assertTrue(result["originalFailedAttemptPreserved"])
        self.assertEqual(result["authorizedRetryCount"], 1)
        self.assertEqual(len(result["bindings"]), 6)

    def test_extra_unbound_file_rejected(self):
        (self.directory / "extra.json").write_text("{}")
        with self.assertRaisesRegex(ValueError, "Handoff directory differs"):
            v.check_resume(self.directory, CANDIDATE)

    def test_missing_supplement_rejected(self):
        (self.directory / "resume-memory.json").unlink()
        with self.assertRaisesRegex(ValueError, "Handoff directory differs"):
            v.check_resume(self.directory, CANDIDATE)

    def test_changed_supplement_rejected(self):
        (self.directory / "resume-evidence.json").write_text("{}")
        with self.assertRaisesRegex(ValueError, "Changed evidence"):
            v.check_resume(self.directory, CANDIDATE)

    def test_other_successor_rejected(self):
        with self.assertRaisesRegex(ValueError, "Recovery supplement scope"):
            v.check_resume(self.directory, v.PARENT)


if __name__ == "__main__":
    unittest.main()

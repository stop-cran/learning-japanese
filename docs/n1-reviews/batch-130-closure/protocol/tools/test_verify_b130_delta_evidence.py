import unittest

from verify_b130_delta_evidence import FAILED, check_failed


class AbortedAttemptTests(unittest.TestCase):
    def test_abort_remains_an_abort_not_a_completed_gate_set(self):
        files = {path.name: path.read_bytes() for path in FAILED.iterdir()}
        row = check_failed(files)
        self.assertIsNone(row["exitCode"])
        self.assertEqual(row["childExitCodeAfterCleanup"], 1)
        self.assertIsNotNone(row["memory"]["breach"])
        with self.assertRaises(ValueError):
            check_failed({**files, "summary.json": b'{"status":"PASS"}'})
        with self.assertRaises(ValueError):
            check_failed({**files, "validate.log": b"success"})


if __name__ == "__main__":
    unittest.main()

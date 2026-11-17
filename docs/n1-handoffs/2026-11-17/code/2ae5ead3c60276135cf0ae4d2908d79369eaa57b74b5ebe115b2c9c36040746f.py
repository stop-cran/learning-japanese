import unittest

from close_b132_reconciled_v2 import CLOSURE, HERE, REPO, closure_report_path


class ClosureDestinationTests(unittest.TestCase):
    def test_real_execution_report_does_not_create_an_untracked_repo_sibling(self):
        destination = REPO / CLOSURE
        self.assertEqual(closure_report_path("real", destination).parent, HERE)
        self.assertFalse(closure_report_path("real", destination).is_relative_to(REPO))

    def test_dry_report_remains_next_to_scratch_output(self):
        output = HERE / "test-dry"
        self.assertEqual(closure_report_path("dry", output), HERE / "test-dry-report.json")


if __name__ == "__main__":
    unittest.main()

import unittest

import verify_b130_revision_runtime_v2 as previous
from verify_b130_revision_runtime_v3 import check_notes


class ReconciliationNotesTests(unittest.TestCase):
    def setUp(self):
        self.before = b"# Notes\r\n\r\n## Batch 130: original\r\nOriginal bytes.\r\n"
        self.insertion = (b"## Batch 130 reconciliation 001: local author successor\r\n"
                          b"Reconciliation remains unconfirmed.\r\n\r\n")
        self.after = self.before.replace(b"## Batch 130:", self.insertion + b"## Batch 130:")

    def test_numbered_reconciliation_heading_is_valid_insert_only_note(self):
        check_notes(self.before, self.after)
        with self.assertRaisesRegex(ValueError, "Unlabelled"):
            previous.check_notes(self.before, self.after)
        check_notes(self.before, self.after.replace(b"130 reconciliation 001:", b"130:"))

    def test_wrong_batch_malformed_number_and_unlabelled_insertions_are_rejected(self):
        for heading in (b"## Batch 131 reconciliation 001:", b"## Batch 1300:",
                        b"## Batch 130 reconciliation x01:", b"## Batch 130 reconciliation 01:",
                        b"## Batch 130 reconciliation 001 without colon"):
            changed = self.after.replace(b"## Batch 130 reconciliation 001:", heading)
            with self.subTest(heading=heading), self.assertRaisesRegex(ValueError, "Unlabelled"):
                check_notes(self.before, changed)

    def test_prior_text_and_raw_line_endings_cannot_be_changed(self):
        for changed in (self.after.replace(b"Original bytes.", b"Rewritten bytes."),
                        self.after.replace(b"\r\n", b"\n"),
                        self.after.replace(b"Original bytes.\r\n", b"")):
            with self.subTest(changed=changed), self.assertRaisesRegex(ValueError, "Existing"):
                check_notes(self.before, changed)


if __name__ == "__main__":
    unittest.main()

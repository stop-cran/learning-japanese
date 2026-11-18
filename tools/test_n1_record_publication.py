import unittest

import n1_record_publication as rec

COMMIT = "a" * 40


class RecordPublicationTest(unittest.TestCase):
    def test_accounting_moves_members_from_undelivered_to_delivered(self):
        before = {"publishedPendingRecordsWithCards": 271, "publishedN1Additions": 265,
                  "n2Placements": 6, "undelivered": 957, "overallN1TaskComplete": False}
        after = rec.advance_accounting(before, 1)
        self.assertEqual((after["publishedPendingRecordsWithCards"], after["publishedN1Additions"],
                          after["undelivered"]), (272, 266, 956))
        self.assertFalse(after["overallN1TaskComplete"])
        self.assertEqual(before["undelivered"], 957)

    def test_refuses_ci_for_other_commit_or_failure(self):
        rec.check_ci({"headSha": COMMIT, "conclusion": "success"}, COMMIT)
        for run in ({"headSha": "b" * 40, "conclusion": "success"},
                    {"headSha": COMMIT, "conclusion": "failure"}):
            with self.assertRaises(SystemExit):
                rec.check_ci(run, COMMIT)

    def test_refuses_zip_receipt_with_failed_check(self):
        good = {"commit": COMMIT, **{k: True for k in rec.ZIP_TRUE_KEYS}}
        rec.check_zip(good, COMMIT)
        with self.assertRaises(SystemExit):
            rec.check_zip({**good, "manifestEqual": False}, COMMIT)
        with self.assertRaises(SystemExit):
            rec.check_zip({**good, "commit": "b" * 40}, COMMIT)


if __name__ == "__main__":
    unittest.main()

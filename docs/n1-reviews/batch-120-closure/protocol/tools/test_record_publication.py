import copy
import unittest

from record_publication import comment_body, delivery_accounting

LEDGER = {"membership": ["析"], "accounting": {
    "frozenPendingRecords": 1228, "publishedPendingRecordsWithCards": 246, "reviewClosedPendingRecordsWithCards": 247,
    "n2Placements": 6, "publishedN1Additions": 240, "undelivered": 982, "notStarted": 981}}


class PublicationAccountingTests(unittest.TestCase):
    def test_derives_counts_from_consistent_ledger(self):
        self.assertEqual(delivery_accounting(LEDGER),
                         {"delivered": 247, "n1Additions": 241, "n2Placements": 6, "remaining": 981})

    def test_rejects_inconsistent_ledger(self):
        for field, value in (("publishedPendingRecordsWithCards", 245), ("publishedN1Additions", 241),
                             ("undelivered", 981), ("notStarted", 982), ("frozenPendingRecords", 1229)):
            ledger = copy.deepcopy(LEDGER)
            ledger["accounting"][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                delivery_accounting(ledger)

    def test_comment_reports_batch_and_counts(self):
        body = comment_body(118, ["析"], "a" * 40, "https://x/c", "https://x/ci",
                            {"verifiedRuntimeHashes": 8700, "contentVersion": "v"},
                            delivery_accounting(LEDGER), {"reviewIdentity": "R.", "changeSummary": "S."})
        self.assertIn("B118 **析** is published at [aaaaaaaa](https://x/c). R. S.", body)
        self.assertIn("**8,700 runtime hashes**", body)
        self.assertIn("batch-118-closure", body)
        self.assertIn("**247/1,228 delivered** (241 N1 additions and 6 earlier N2 placements); **981 remain**", body)


if __name__ == "__main__":
    unittest.main()

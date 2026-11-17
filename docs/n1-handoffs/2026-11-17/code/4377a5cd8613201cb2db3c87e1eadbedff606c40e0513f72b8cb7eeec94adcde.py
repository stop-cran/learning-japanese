import copy
import json
import unittest

from common import WS, frozen, load_batch
from finalize_b125_v2 import CANDIDATE, FINALS, PROOFS, check_proofs, make_ledger
from b125_followup_lineage import HISTORICAL


class ThreeCorrectionFinalizerTests(unittest.TestCase):
    def setUp(self):
        self.config = load_batch(125)
        self.proofs = [json.loads(frozen(
            WS / "scratch-125" / "review" / f"reconciliation-{number:03}-independent-proof.json", digest))
            for number, digest in PROOFS.items()]

    def test_all_three_real_verified_proofs_are_accepted(self):
        check_proofs(*self.proofs, self.config)

    def test_s1_proof_cannot_change_snapshot_inventory_or_runtime_scope(self):
        for key, value in (("candidate", "c" * 40), ("parent", self.config["candidate"]),
                           ("parentInventoryCards", 1244), ("exactMetadataAndPracticeMatches", ["hit"]),
                           ("explicitReadingReplayByteIdentical", False),
                           ("unrelatedRuntimeAndFrozenMetadataPreserved", False),
                           ("confirmationAccepted", True)):
            changed = copy.deepcopy(self.proofs)
            changed[2][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                check_proofs(*changed, self.config)
        changed = copy.deepcopy(self.proofs)
        changed[2]["gates"]["committed"].pop()
        with self.assertRaises(ValueError):
            check_proofs(*changed, self.config)

    def test_review_closure_keeps_delivery_pending_and_both_historical_runs(self):
        old = {"status": "author-draft-not-reviewed-or-published", "membership": ["\u4fb5"],
               "sourceRows": [48], "reviewClosed": [], "published": [], "runtimePublished": False,
               "accounting": {"frozenPendingRecords": 1228, "publishedPendingRecordsWithCards": 254,
                              "publishedN1Additions": 248, "n2Placements": 6, "undelivered": 974,
                              "overallN1TaskComplete": False}}
        provenance = {"finalRuns": list(FINALS.values()), "intermediateRuns": list(HISTORICAL.values())}
        ledger = make_ledger(old, self.config, provenance, "fixture", self.proofs[2])
        self.assertEqual(ledger["reviewedSnapshot"], CANDIDATE)
        self.assertEqual(ledger["review"]["intermediateRuns"], list(HISTORICAL.values()))
        self.assertEqual(len(ledger["correctionSources"]), 3)
        self.assertFalse(ledger["runtimePublished"])
        self.assertEqual(ledger["published"], [])
        self.assertEqual(ledger["accounting"]["publishedPendingRecordsWithCards"], 254)
        self.assertFalse(ledger["accounting"]["overallN1TaskComplete"])
        self.assertEqual(old["reviewClosed"], [])


if __name__ == "__main__":
    unittest.main()

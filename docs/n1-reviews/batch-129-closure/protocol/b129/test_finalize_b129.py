import copy
import json
import unittest

from common import WS, frozen, load_batch
from finalize_b129 import CANDIDATE, ROOT, check_history, check_proof, make_ledger
from record_publication import delivery_accounting


class FinalizerTests(unittest.TestCase):
    def setUp(self):
        self.config = load_batch(129)
        self.provenance = json.loads(frozen(
            WS / "b129-worktree" / "docs" / "n1-reviews" / "batch-129-closure" / "provenance.json"))
        self.proof = json.loads(frozen(ROOT / "revision-evidence-proof-001" / "verification.json"))

    def test_exact_recorded_history_and_mechanical_proof(self):
        check_history(self.provenance, CANDIDATE, self.config)
        check_proof(self.proof, CANDIDATE, self.config)

    def test_misattributed_replacement_or_laundered_failure_cannot_close(self):
        for field, value in (("session", "wrong"), ("reviewerOrigin", "original"),
                             ("rawVerdict", "NEEDS FIX"), ("confirmationAcceptedOnSnapshot", False)):
            changed = copy.deepcopy(self.provenance)
            changed["reviewLineage"][1][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                check_history(changed, CANDIDATE, self.config)
        changed = copy.deepcopy(self.provenance)
        changed["excludedConfirmationRuns"][0]["confirmationAccepted"] = True
        with self.assertRaises(ValueError):
            check_history(changed, CANDIDATE, self.config)

    def test_review_closure_does_not_increment_delivered_count(self):
        old = json.loads((WS / "b129-worktree" / "docs" / "n1-sources" / "batch-129-progress.json").read_bytes())
        before = copy.deepcopy(old)
        ledger = make_ledger(old, self.config, self.provenance, "a" * 64, self.proof)
        self.assertEqual(old, before)
        self.assertFalse(ledger["runtimePublished"])
        self.assertEqual(ledger["published"], [])
        self.assertEqual(ledger["accounting"]["publishedPendingRecordsWithCards"], 258)
        self.assertEqual(delivery_accounting(ledger), {
            "delivered": 261, "n1Additions": 255, "n2Placements": 6, "remaining": 967,
        })


if __name__ == "__main__":
    unittest.main()

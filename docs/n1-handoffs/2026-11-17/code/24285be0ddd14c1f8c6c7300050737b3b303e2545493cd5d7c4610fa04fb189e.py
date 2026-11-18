import copy
import unittest

from finalize_b128 import FINALS, INITIALS, REVIEWERS, check_history, make_ledger
from record_publication import delivery_accounting


class B128FinalizerTests(unittest.TestCase):
    def fixture(self):
        config = {"candidate": "a" * 40, "base": "b" * 40, "members": ["\u5507"]}
        candidate = "c" * 40
        lineage = []
        for family in INITIALS:
            lineage.extend([
                {"run": INITIALS[family], "family": family, "role": "initial",
                 "snapshot": config["candidate"], "session": REVIEWERS[family],
                 "rawVerdict": "NEEDS FIX" if family == "claude" else "UNVERIFIED",
                 "priorRun": None, "finalAcceptance": False, "confirmationAcceptedOnSnapshot": False},
                {"run": FINALS[family], "family": family, "role": "final",
                 "snapshot": candidate, "session": REVIEWERS[family], "rawVerdict": "CONFIRMED",
                 "priorRun": None, "finalAcceptance": True, "confirmationAcceptedOnSnapshot": True},
            ])
        provenance = {
            "batch": 128, "reviewedSnapshot": candidate, "initialSnapshot": config["candidate"],
            "base": config["base"], "members": config["members"], "publication": "PENDING",
            "excludedInitialRuns": [], "intermediateRuns": [], "finalRuns": list(FINALS.values()),
            "reviewLineage": lineage,
        }
        return config, candidate, provenance

    def test_accepts_exact_four_run_lineage(self):
        config, candidate, provenance = self.fixture()
        check_history(provenance, candidate, config)

    def test_rejects_reviewer_replacement_old_snapshot_and_relabelled_verdict(self):
        config, candidate, provenance = self.fixture()
        for index, key, value in (
            (1, "session", "replacement"),
            (3, "snapshot", config["candidate"]),
            (2, "rawVerdict", "CLEAN"),
            (3, "confirmationAcceptedOnSnapshot", False),
        ):
            with self.subTest(key=key):
                altered = copy.deepcopy(provenance)
                altered["reviewLineage"][index][key] = value
                with self.assertRaises(ValueError):
                    check_history(altered, candidate, config)

    def test_closure_does_not_claim_delivery(self):
        config, candidate, provenance = self.fixture()
        old = {
            "status": "local-unreviewed-authoring-candidate", "membership": ["\u5507"],
            "sourceRows": [159], "reviewClosed": [], "published": [], "runtimePublished": False,
            "accounting": {
                "frozenPendingRecords": 1228, "publishedPendingRecordsWithCards": 257,
                "publishedN1Additions": 251, "n2Placements": 6, "undelivered": 971,
                "localUnreviewedDrafts": 1,
            },
        }
        before = copy.deepcopy(old)
        proof = {"manifestSha256": "d" * 64, "contentVersion": "e" * 16, "runtimeEntries": 8718}
        result = make_ledger(old, config, candidate, provenance, "f" * 64, proof)
        self.assertEqual(old, before)
        self.assertFalse(result["runtimePublished"])
        self.assertEqual(result["published"], [])
        self.assertEqual(result["accounting"]["publishedPendingRecordsWithCards"], 257)
        self.assertEqual(result["accounting"]["undelivered"], 971)
        self.assertEqual(result["accounting"]["localUnreviewedDrafts"], 0)
        self.assertEqual(delivery_accounting(result), {
            "delivered": 258, "n1Additions": 252, "n2Placements": 6, "remaining": 970,
        })


if __name__ == "__main__":
    unittest.main()

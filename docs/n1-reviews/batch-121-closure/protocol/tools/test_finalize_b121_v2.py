import copy
import unittest

from finalize_b121_v2 import HELD, HOLD_SHA, INITIALS, check_closure, make_ledger
from record_publication import delivery_accounting


class ClosureTests(unittest.TestCase):
    def fixture(self):
        candidate = "a" * 40
        config = {"candidate": "b" * 40, "base": "c" * 40, "members": ["\u5fb3"]}
        lineage = []
        for family, run in INITIALS.items():
            lineage.extend([
                {"run": run, "family": family, "role": "initial", "session": family,
                 "snapshot": config["candidate"], "rawVerdict": "NEEDS FIX", "finalAcceptance": False},
                {"run": run + "-CONFIRM-001", "family": family, "role": "final", "session": family,
                 "snapshot": candidate, "rawVerdict": "CONFIRMED", "finalAcceptance": True,
                 "confirmationAcceptedOnSnapshot": True},
            ])
        provenance = {
            "reviewedSnapshot": candidate, "initialSnapshot": config["candidate"], "base": config["base"],
            "publication": "PENDING", "members": config["members"], "reviewLineage": lineage,
            "finalRuns": [item["run"] for item in lineage if item["finalAcceptance"]],
            "excludedInitialRuns": [{"run": HELD, "snapshot": config["candidate"],
                                    "status": "HOLD_STRUCTURE_FAILED", "holdSha256": HOLD_SHA,
                                    "reviewAccepted": False, "finalAcceptance": False}],
        }
        proof = {
            "status": "PASS", "candidate": candidate, "initial": config["candidate"], "base": config["base"],
            "baselineRuntimePreservedExceptRequiredWrappers": True,
            "originalMetadataStrokesGuardsAndSourceReceiptsPreserved": True,
            "sourceMembersPublishedBeforeBatch": 250, "sourceMembersInCandidate": 251,
            "linguisticAcceptance": False, "publicationAccepted": False, "memory": {"breach": None},
            "contentVersion": "version", "manifestSha256": "manifest", "runtimeEntries": 8704,
            "sourceProof": {"signedArtifacts": {}},
        }
        return candidate, config, provenance, proof

    def test_requires_both_original_reviewers_on_exact_revision(self):
        candidate, config, provenance, proof = self.fixture()
        check_closure(provenance, proof, candidate, config)
        for key, value in (("snapshot", config["candidate"]), ("rawVerdict", "NEEDS FIX"),
                           ("session", "replacement"), ("confirmationAcceptedOnSnapshot", False)):
            broken = copy.deepcopy(provenance)
            broken["reviewLineage"][-1][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                check_closure(broken, proof, candidate, config)

    def test_held_initial_cannot_be_dropped_or_promoted(self):
        candidate, config, provenance, proof = self.fixture()
        for key, value in (("reviewAccepted", True), ("holdSha256", "changed"), ("finalAcceptance", True)):
            broken = copy.deepcopy(provenance)
            broken["excludedInitialRuns"][0][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                check_closure(broken, proof, candidate, config)
        with self.assertRaises(ValueError):
            check_closure({**provenance, "excludedInitialRuns": []}, proof, candidate, config)

    def test_review_closure_does_not_count_as_delivery(self):
        candidate, config, provenance, proof = self.fixture()
        ledger = make_ledger(config, candidate, provenance, "provenance", proof)
        self.assertEqual(ledger["published"], [])
        self.assertFalse(ledger["runtimePublished"])
        self.assertEqual(ledger["accounting"]["publishedPendingRecordsWithCards"], 250)
        self.assertEqual(ledger["accounting"]["undelivered"], 978)
        self.assertEqual(delivery_accounting(ledger),
                         {"delivered": 251, "n1Additions": 245, "n2Placements": 6, "remaining": 977})
        with self.assertRaises(ValueError):
            check_closure(provenance, {**proof, "publicationAccepted": True}, candidate, config)


if __name__ == "__main__":
    unittest.main()

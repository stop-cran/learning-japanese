import copy
import unittest

from common import CHECKS
from finalize_b125 import (CANDIDATE, EXCLUDED, FINALS, FIRST, INITIALS, QUARANTINE_SHA,
                          SIGNER, STATUS, check_history, check_proofs, make_ledger)
from record_publication import delivery_accounting


class B125FinalizerTests(unittest.TestCase):
    def fixture(self):
        config = {"candidate": "a" * 40, "base": "b" * 40, "members": ["\u4fb5"]}
        lineage = []
        for family in INITIALS:
            base = {"family": family, "session": family, "priorRun": None}
            lineage.extend([
                {**base, "run": INITIALS[family], "role": "initial", "snapshot": config["candidate"],
                 "rawVerdict": "NEEDS FIX", "finalAcceptance": False, "confirmationAcceptedOnSnapshot": False},
                {**base, "run": FINALS[family], "role": "final", "snapshot": CANDIDATE,
                 "rawVerdict": "CONFIRMED", "finalAcceptance": True, "confirmationAcceptedOnSnapshot": True},
            ])
        provenance = {
            "batch": 125, "reviewedSnapshot": CANDIDATE, "initialSnapshot": config["candidate"],
            "base": config["base"], "members": config["members"], "publication": "PENDING",
            "intermediateRuns": [], "finalRuns": list(FINALS.values()), "reviewLineage": lineage,
            "excludedInitialRuns": [{"run": EXCLUDED, "status": STATUS, "snapshot": config["candidate"],
                                     "reviewAccepted": False, "finalAcceptance": False,
                                     "quarantineSha256": QUARANTINE_SHA}],
        }
        common = {"batch": 125, "status": "PASS", "runtimeEntries": 8712,
                  "reviewAccepted": False, "confirmationAccepted": False,
                  "gates": {mode: [{"gate": name} for name in CHECKS] for mode in ("author", "committed")}}
        first = {**copy.deepcopy(common), "candidate": FIRST, "parent": config["candidate"],
                 "openClaimIds": ["Q4", "Q9"]}
        current = {**copy.deepcopy(common), "candidate": CANDIDATE, "parent": FIRST,
                   "originalCandidate": config["candidate"], "addedDirectGuards": ["\u51cc", "\u5360"],
                   "signature": {"status": "G", "fingerprint": SIGNER, "signer": "stop-cran@list.ru"},
                   "manifestSha256": "hash", "contentVersion": "version"}
        return config, provenance, first, current

    def test_original_reviewers_and_exact_snapshot_are_required(self):
        config, provenance, *_ = self.fixture()
        check_history(provenance, config)
        for index, key, value in ((2, "run", EXCLUDED), (1, "session", "replacement"),
                                  (1, "snapshot", FIRST), (3, "finalAcceptance", False)):
            changed = copy.deepcopy(provenance)
            changed["reviewLineage"][index][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                check_history(changed, config)

    def test_void_cannot_be_dropped_relabelled_or_accepted(self):
        config, provenance, *_ = self.fixture()
        for key, value in (("status", "HOLD_STRUCTURE_FAILED"), ("reviewAccepted", True),
                           ("finalAcceptance", True), ("quarantineSha256", "other")):
            changed = copy.deepcopy(provenance)
            changed["excludedInitialRuns"][0][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                check_history(changed, config)
        with self.assertRaises(ValueError):
            check_history({**provenance, "excludedInitialRuns": []}, config)

    def test_both_corrections_and_complete_gate_sets_are_required(self):
        config, _, first, current = self.fixture()
        check_proofs(first, current, config)
        for proof, key, value in ((first, "openClaimIds", []), (current, "parent", config["candidate"]),
                                  (current, "confirmationAccepted", True)):
            changed = copy.deepcopy(proof)
            changed[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                check_proofs(changed if proof is first else first, changed if proof is current else current, config)
        changed = copy.deepcopy(current)
        changed["gates"]["committed"].pop()
        with self.assertRaises(ValueError):
            check_proofs(first, changed, config)

    def test_review_closed_accounting_does_not_claim_delivery(self):
        config, provenance, _, current = self.fixture()
        old = {
            "status": "author-draft-not-reviewed-or-published", "membership": ["\u4fb5"],
            "sourceRows": [48], "reviewClosed": [], "published": [], "runtimePublished": False,
            "accounting": {"frozenPendingRecords": 1228, "publishedPendingRecordsWithCards": 254,
                           "publishedN1Additions": 248, "n2Placements": 6, "undelivered": 974,
                           "overallN1TaskComplete": False},
        }
        ledger = make_ledger(old, config, provenance, "closure", current)
        self.assertEqual(ledger["published"], [])
        self.assertFalse(ledger["runtimePublished"])
        self.assertEqual(ledger["accounting"]["publishedPendingRecordsWithCards"], 254)
        self.assertEqual(ledger["review"]["excludedInitialRuns"], [EXCLUDED])
        self.assertEqual(delivery_accounting(ledger),
                         {"delivered": 255, "n1Additions": 249, "n2Placements": 6, "remaining": 973})
        self.assertEqual(old["reviewClosed"], [])


if __name__ == "__main__":
    unittest.main()

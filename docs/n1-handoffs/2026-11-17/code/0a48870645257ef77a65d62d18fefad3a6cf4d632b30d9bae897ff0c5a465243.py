import copy
import unittest

from common import CHECKS
from finalize_b123_v2 import (
    FINALS, FIRST_PROOF_SHA, HISTORY, INITIALS, PARENT, PROOF_SHA,
    check_history, check_proofs, make_ledger,
)
from record_publication import delivery_accounting


class ThirdRevisionClosureTests(unittest.TestCase):
    def fixture(self):
        config = {"candidate": "a" * 40, "base": "b" * 40, "members": ["\u7bc4"]}
        candidate = "c" * 40
        lineage = []
        for family in INITIALS:
            lineage.extend([
                {"run": INITIALS[family], "family": family, "session": family, "role": "initial",
                 "snapshot": config["candidate"], "rawVerdict": "NEEDS FIX", "finalAcceptance": False},
                {"run": HISTORY[family], "family": family, "session": family, "role": "intermediate",
                 "snapshot": PARENT, "rawVerdict": "CONFIRMED" if family == "claude" else "UNVERIFIED",
                 "confirmationAcceptedOnSnapshot": family == "claude", "finalAcceptance": False, "priorRun": None},
                {"run": FINALS[family], "family": family, "session": family, "role": "final",
                 "snapshot": candidate, "rawVerdict": "CONFIRMED", "confirmationAcceptedOnSnapshot": True,
                 "finalAcceptance": True, "priorRun": HISTORY[family]},
            ])
        provenance = {"reviewedSnapshot": candidate, "initialSnapshot": config["candidate"],
                      "base": config["base"], "publication": "PENDING", "members": config["members"],
                      "reviewLineage": lineage, "finalRuns": list(FINALS.values()),
                      "intermediateRuns": list(HISTORY.values()), "excludedInitialRuns": []}
        shared = {"status": "PASS", "initial": config["candidate"], "base": config["base"],
                  "sourceMembersPublishedBeforeBatch": 252, "sourceMembersInCandidate": 253,
                  "runtimeEntries": 8708, "linguisticAcceptance": False, "publicationAccepted": False,
                  "memory": {"breach": None}, "gates": [{"gate": name} for name in CHECKS]}
        first = {**copy.deepcopy(shared), "candidate": "d" * 40,
                 "sourceProof": {"signedArtifacts": {"first": "one"}}}
        second = {**copy.deepcopy(shared), "candidate": PARENT, "parent": first["candidate"],
                  "priorRevisionProof": {"sha256": FIRST_PROOF_SHA},
                  "sourceProof": {"signedArtifacts": {"second": "two"}},
                  "contentVersion": "old", "manifestSha256": "old"}
        current = {**copy.deepcopy(shared), "candidate": candidate, "parent": PARENT,
                   "priorRevisionProof": {"sha256": PROOF_SHA},
                   "earlierSignedSourcesAndNonScopedRuntimePreserved": True,
                   "newGuards": ["\u672c", "\u5ea6"], "signedSourceArtifacts": {"third": "three"},
                   "contentVersion": "new", "manifestSha256": "new"}
        return config, candidate, provenance, first, second, current

    def test_preserves_held_history_and_requires_same_reviewers_on_successor(self):
        config, candidate, provenance, *_ = self.fixture()
        check_history(provenance, candidate, config)
        for index, key, value in (
            (4, "rawVerdict", "CONFIRMED"), (4, "confirmationAcceptedOnSnapshot", True),
            (1, "confirmationAcceptedOnSnapshot", False), (5, "snapshot", PARENT),
            (5, "session", "replacement"), (5, "priorRun", None),
            (5, "confirmationAcceptedOnSnapshot", False),
        ):
            broken = copy.deepcopy(provenance)
            broken["reviewLineage"][index][key] = value
            with self.subTest(index=index, key=key), self.assertRaises(ValueError):
                check_history(broken, candidate, config)
        with self.assertRaises(ValueError):
            check_history({**provenance, "intermediateRuns": []}, candidate, config)

    def test_requires_all_three_actual_revision_proofs(self):
        config, candidate, _, first, second, current = self.fixture()
        check_proofs(first, second, current, candidate, config)
        for key, value in (("parent", config["candidate"]), ("priorRevisionProof", {"sha256": "wrong"}),
                           ("gates", []), ("publicationAccepted", True),
                           ("newGuards", ["\u672c"]), ("memory", {"breach": "low RAM"})):
            with self.subTest(key=key), self.assertRaises(ValueError):
                check_proofs(first, second, {**current, key: value}, candidate, config)

    def test_ledger_keeps_sources_and_current_manifest_without_premature_delivery(self):
        config, candidate, provenance, first, second, current = self.fixture()
        ledger = make_ledger(config, candidate, provenance, "closure", first, second, current)
        self.assertEqual(ledger["sourceEvidence"]["signedArtifactSha256"],
                         {"first": "one", "second": "two", "third": "three"})
        self.assertEqual(ledger["runtimeCandidate"]["manifestSha256"], "new")
        self.assertEqual(ledger["published"], [])
        self.assertFalse(ledger["runtimePublished"])
        self.assertEqual(ledger["accounting"]["undelivered"], 976)
        self.assertEqual(delivery_accounting(ledger),
                         {"delivered": 253, "n1Additions": 247, "n2Placements": 6, "remaining": 975})


if __name__ == "__main__":
    unittest.main()

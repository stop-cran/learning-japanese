import copy
import unittest

from common import CHECKS
from finalize_b122 import INITIALS, VERDICTS, check_closure, make_ledger
from record_publication import delivery_accounting


class ClosureTests(unittest.TestCase):
    def fixture(self):
        candidate = "a" * 40
        config = {"candidate": "b" * 40, "base": "c" * 40, "members": ["\u60a0"]}
        lineage = []
        for family, run in INITIALS.items():
            lineage.extend([
                {"run": run, "family": family, "role": "initial", "session": family,
                 "snapshot": config["candidate"], "rawVerdict": VERDICTS[family], "finalAcceptance": False},
                {"run": run + "-CONFIRM-001", "family": family, "role": "final", "session": family,
                 "snapshot": candidate, "rawVerdict": "CONFIRMED", "finalAcceptance": True,
                 "confirmationAcceptedOnSnapshot": True, "priorRun": None},
            ])
        provenance = {
            "reviewedSnapshot": candidate, "initialSnapshot": config["candidate"], "base": config["base"],
            "publication": "PENDING", "members": config["members"], "reviewLineage": lineage,
            "finalRuns": [item["run"] for item in lineage if item["finalAcceptance"]],
            "excludedInitialRuns": [], "intermediateRuns": [],
        }
        proof = {
            "status": "PASS", "candidate": candidate, "initial": config["candidate"], "base": config["base"],
            "baselineRuntimePreservedExceptRequiredWrappers": True,
            "originalMetadataStrokesGuardsAndSourceReceiptsPreserved": True,
            "sourceMembersPublishedBeforeBatch": 251, "sourceMembersInCandidate": 252,
            "linguisticAcceptance": False, "publicationAccepted": False, "memory": {"breach": None},
            "contentVersion": "version", "manifestSha256": "manifest", "runtimeEntries": 8706,
            "sourceProof": {"signedArtifacts": {}}, "gates": [{"gate": name} for name in CHECKS],
        }
        return candidate, config, provenance, proof

    def test_requires_both_original_reviewers_on_exact_revision(self):
        candidate, config, provenance, proof = self.fixture()
        check_closure(provenance, proof, candidate, config)
        for key, value in (("snapshot", config["candidate"]), ("rawVerdict", "NEEDS FIX"),
                           ("session", "replacement"), ("confirmationAcceptedOnSnapshot", False),
                           ("priorRun", "unrecorded")):
            broken = copy.deepcopy(provenance)
            broken["reviewLineage"][-1][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                check_closure(broken, proof, candidate, config)

    def test_cannot_relabel_initials_or_insert_a_held_or_skipped_run(self):
        candidate, config, provenance, proof = self.fixture()
        for index, wrong in ((0, "NEEDS FIX"), (2, "CLEAN")):
            broken = copy.deepcopy(provenance)
            broken["reviewLineage"][index]["rawVerdict"] = wrong
            with self.subTest(index=index), self.assertRaises(ValueError):
                check_closure(broken, proof, candidate, config)
        for field in ("excludedInitialRuns", "intermediateRuns"):
            with self.subTest(field=field), self.assertRaises(ValueError):
                check_closure({**provenance, field: ["unrecorded"]}, proof, candidate, config)

    def test_rejects_missing_gates_or_changed_runtime_accounting(self):
        candidate, config, provenance, proof = self.fixture()
        for key, value in (("gates", proof["gates"][:-1]), ("runtimeEntries", 8704),
                           ("sourceMembersInCandidate", 251), ("publicationAccepted", True)):
            with self.subTest(key=key), self.assertRaises(ValueError):
                check_closure(provenance, {**proof, key: value}, candidate, config)

    def test_review_closure_does_not_count_as_delivery(self):
        candidate, config, provenance, proof = self.fixture()
        ledger = make_ledger(config, candidate, provenance, "provenance", proof)
        self.assertEqual(ledger["published"], [])
        self.assertFalse(ledger["runtimePublished"])
        self.assertEqual(ledger["accounting"]["publishedPendingRecordsWithCards"], 251)
        self.assertEqual(ledger["accounting"]["undelivered"], 977)
        self.assertEqual(delivery_accounting(ledger),
                         {"delivered": 252, "n1Additions": 246, "n2Placements": 6, "remaining": 976})


if __name__ == "__main__":
    unittest.main()

import copy
import unittest

from common import CHECKS
from finalize_b123 import (CANDIDATE, FINALS, INITIALS, PARENT, PRIOR_SHA,
                           check_closure, make_ledger)
from record_publication import delivery_accounting


class ClosureTests(unittest.TestCase):
    def fixture(self):
        config = {"candidate": "b" * 40, "base": "c" * 40, "members": ["\u7bc4"]}
        lineage = []
        for family, run in INITIALS.items():
            lineage.extend([
                {"run": run, "family": family, "role": "initial", "session": family,
                 "snapshot": config["candidate"], "rawVerdict": "NEEDS FIX", "finalAcceptance": False},
                {"run": FINALS[family], "family": family, "role": "final", "session": family,
                 "snapshot": CANDIDATE, "rawVerdict": "CONFIRMED", "finalAcceptance": True,
                 "confirmationAcceptedOnSnapshot": True, "priorRun": None},
            ])
        provenance = {
            "reviewedSnapshot": CANDIDATE, "initialSnapshot": config["candidate"], "base": config["base"],
            "publication": "PENDING", "members": config["members"], "reviewLineage": lineage,
            "finalRuns": list(FINALS.values()), "excludedInitialRuns": [], "intermediateRuns": [],
        }
        shared = {
            "status": "PASS", "initial": config["candidate"], "base": config["base"],
            "sourceMembersPublishedBeforeBatch": 252, "sourceMembersInCandidate": 253,
            "runtimeEntries": 8708, "linguisticAcceptance": False, "publicationAccepted": False,
            "memory": {"breach": None}, "gates": [{"gate": name} for name in CHECKS],
            "sourceProof": {"signedArtifacts": {}},
        }
        prior = {**copy.deepcopy(shared), "candidate": PARENT,
                 "baselineRuntimePreservedExceptRequiredWrappers": True,
                 "originalMetadataStrokesGuardsAndSourceReceiptsPreserved": True}
        proof = {**copy.deepcopy(shared), "candidate": CANDIDATE, "parent": PARENT,
                 "priorRevisionProof": {"sha256": PRIOR_SHA}, "newGuard": "\u666e",
                 "firstRevisionTeachingAndSourcesPreservedExceptFocusedCardAndManifest": True,
                 "contentVersion": "version", "manifestSha256": "manifest"}
        return config, provenance, proof, prior

    def test_requires_both_original_reviewers_on_exact_candidate(self):
        config, provenance, proof, prior = self.fixture()
        check_closure(provenance, proof, prior, CANDIDATE, config)
        for key, value in (("snapshot", PARENT), ("rawVerdict", "NEEDS FIX"),
                           ("session", "replacement"), ("confirmationAcceptedOnSnapshot", False),
                           ("priorRun", "unrecorded"), ("run", "N1-B123-GPT-CONFIRM-001")):
            broken = copy.deepcopy(provenance)
            broken["reviewLineage"][-1][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                check_closure(broken, proof, prior, CANDIDATE, config)
        with self.assertRaises(ValueError):
            check_closure({**provenance, "finalRuns": [FINALS["claude"]]},
                          proof, prior, CANDIDATE, config)

    def test_cannot_relabel_or_omit_history(self):
        config, provenance, proof, prior = self.fixture()
        for index in (0, 2):
            broken = copy.deepcopy(provenance)
            broken["reviewLineage"][index]["rawVerdict"] = "CLEAN"
            with self.subTest(index=index), self.assertRaises(ValueError):
                check_closure(broken, proof, prior, CANDIDATE, config)
        for key in ("excludedInitialRuns", "intermediateRuns"):
            with self.subTest(key=key), self.assertRaises(ValueError):
                check_closure({**provenance, key: ["unrecorded"]}, proof, prior, CANDIDATE, config)
        with self.assertRaises(ValueError):
            check_closure(provenance, {**proof, "parent": config["candidate"]}, prior, CANDIDATE, config)

    def test_requires_both_verified_revisions_and_all_gates(self):
        config, provenance, proof, prior = self.fixture()
        for target in ("prior", "proof"):
            for key, value in (("gates", []), ("runtimeEntries", 8706),
                               ("sourceMembersInCandidate", 252), ("publicationAccepted", True),
                               ("memory", {"breach": "low RAM"})):
                args = {"prior": prior, "proof": proof}
                args[target] = {**args[target], key: value}
                with self.subTest(target=target, key=key), self.assertRaises(ValueError):
                    check_closure(provenance, args["proof"], args["prior"], CANDIDATE, config)

    def test_review_closure_is_not_delivery_and_keeps_both_source_sets(self):
        config, provenance, proof, prior = self.fixture()
        prior["sourceProof"]["signedArtifacts"] = {"first-source": "first-sha"}
        proof["sourceProof"]["signedArtifacts"] = {"second-source": "second-sha"}
        ledger = make_ledger(config, CANDIDATE, provenance, "provenance", proof, prior)
        self.assertEqual(ledger["published"], [])
        self.assertFalse(ledger["runtimePublished"])
        self.assertEqual(ledger["accounting"]["publishedPendingRecordsWithCards"], 252)
        self.assertEqual(ledger["accounting"]["undelivered"], 976)
        self.assertEqual(ledger["sourceEvidence"]["signedArtifactSha256"],
                         {"first-source": "first-sha", "second-source": "second-sha"})
        self.assertEqual(delivery_accounting(ledger),
                         {"delivered": 253, "n1Additions": 247, "n2Placements": 6, "remaining": 975})


if __name__ == "__main__":
    unittest.main()

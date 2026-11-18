import copy
import unittest

from finalize_b119 import INTERMEDIATE, verify_closure


class ClosureGateTests(unittest.TestCase):
    def test_requires_both_families_on_exact_verified_candidate(self):
        candidate = "a" * 40
        config = {"candidate": "b" * 40, "base": "c" * 40}
        provenance = {
            "reviewedSnapshot": candidate, "publication": "PENDING", "excludedInitialRuns": [],
            "reviewLineage": [
                {"family": family, "snapshot": candidate, "rawVerdict": "CONFIRMED", "finalAcceptance": True}
                for family in ("claude", "gpt")
            ],
        }
        proof = {
            "status": "PASS", "candidate": candidate, "prior": INTERMEDIATE,
            "initial": config["candidate"], "base": config["base"],
            "baselineRuntimePreservedExceptRequiredWrappers": True,
            "originalMetadataStrokesGuardsAndSourceReceiptsPreserved": True,
            "sourceMembersPublishedBeforeBatch": 247, "sourceMembersInCandidate": 249,
            "linguisticAcceptance": False, "publicationAccepted": False, "memory": {"breach": None},
        }
        verify_closure(provenance, proof, candidate, config)
        for key, value in (("snapshot", "d" * 40), ("rawVerdict", "NEEDS FIX"), ("family", "claude")):
            broken = copy.deepcopy(provenance)
            broken["reviewLineage"][1][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                verify_closure(broken, proof, candidate, config)
        for key, value in (("sourceMembersInCandidate", 248), ("publicationAccepted", True),
                           ("prior", config["base"]), ("baselineRuntimePreservedExceptRequiredWrappers", False)):
            with self.subTest(key=key), self.assertRaises(ValueError):
                verify_closure(provenance, {**proof, key: value}, candidate, config)


if __name__ == "__main__":
    unittest.main()

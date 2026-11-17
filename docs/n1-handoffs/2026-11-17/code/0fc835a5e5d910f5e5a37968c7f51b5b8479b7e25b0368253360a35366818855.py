import copy
import unittest

from finalize_b119_v3 import PRIOR, PROOF_SHA, SUPPLEMENT_SHA, verify_closure


class FollowupClosureTests(unittest.TestCase):
    def test_preserves_history_and_requires_both_final_acceptances(self):
        candidate = "a" * 40
        config = {"candidate": "b" * 40, "base": "c" * 40}
        provenance = {
            "reviewedSnapshot": candidate, "publication": "PENDING", "excludedInitialRuns": [],
            "reviewLineage": [
                {"family": family, "snapshot": snapshot, "rawVerdict": verdict,
                 "role": role, "finalAcceptance": role == "final",
                 "priorRun": f"N1-B119-{family.upper()}-001-CONFIRM-001" if role == "final" else None}
                for role, snapshot in (("intermediate", PRIOR), ("final", candidate))
                for family, verdict in (("claude", "CONFIRMED"),
                                        ("gpt", "NEEDS FIX" if role == "intermediate" else "CONFIRMED"))
            ],
        }
        proof = {
            "candidate": candidate, "prior": PRIOR, "initial": config["candidate"], "base": config["base"],
            "status": "PASS", "priorVerification": {"sha256": PROOF_SHA},
            "priorSupplement": {"sha256": SUPPLEMENT_SHA},
            "baselineRuntimePreservedExceptRequiredWrappers": True,
            "originalMetadataStrokesGuardsAndSourceReceiptsPreserved": True,
            "oldEvidencePreserved": True, "boundedDelta": {"addedGuard": "丸"},
            "sourceMembersPublishedBeforeBatch": 247, "sourceMembersInCandidate": 249,
            "linguisticAcceptance": False, "publicationAccepted": False, "memory": {"breach": None},
        }
        verify_closure(provenance, proof, candidate, config)
        for index, key, value in ((1, "rawVerdict", "CONFIRMED"), (0, "snapshot", candidate),
                                  (3, "rawVerdict", "NEEDS FIX"), (3, "family", "claude"),
                                  (3, "priorRun", None)):
            broken = copy.deepcopy(provenance)
            broken["reviewLineage"][index][key] = value
            with self.subTest(index=index, key=key), self.assertRaises(ValueError):
                verify_closure(broken, proof, candidate, config)
        with self.assertRaises(ValueError):
            verify_closure(provenance, {**proof, "sourceMembersInCandidate": 248}, candidate, config)


if __name__ == "__main__":
    unittest.main()

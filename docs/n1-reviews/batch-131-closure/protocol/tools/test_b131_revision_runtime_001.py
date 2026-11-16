"""Focused initial-review binding checks for the B131 successor verifier."""
import copy
import unittest

from verify_b131_revision_runtime_001 import INITIALS, PARENT, check_initial


def records(family):
    base = {"run": INITIALS[family][1], "candidate": PARENT}
    report = {"path": "frozen-report", "sha256": "a" * 64}
    accepted = {**base, "reviewAccepted": True, "verdict": "NEEDS FIX",
                "acceptedFindings": ["F1"], "report": report}
    adjudication = {**base, "claimsAdjudicated": True, "verdict": "NEEDS FIX",
                    "acceptedFindings": ["F1"], "report": report,
                    "publicationAccepted": False, "openClaimIds": ["D22"]}
    final = {**base, "status": "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION",
             "problems": []}
    return accepted, adjudication, final


class InitialBindings(unittest.TestCase):
    def test_preserves_unresolved_claims_for_both_families(self):
        for family in INITIALS:
            values = records(family)
            result = check_initial(family, *values)
            self.assertEqual(["D22"], result)
            result.clear()
            self.assertEqual(["D22"], values[1]["openClaimIds"])

    def test_rejects_held_wrong_snapshot_and_unadjudicated_reviews(self):
        changes = [(0, "reviewAccepted", False), (1, "claimsAdjudicated", False),
                   (1, "candidate", "b" * 40), (2, "status", "HOLD"),
                   (2, "problems", ["missing source"]), (1, "publicationAccepted", True)]
        for index, key, value in changes:
            with self.subTest(key=key):
                values = records("gpt")
                values[index][key] = value
                with self.assertRaises((ValueError, RuntimeError)):
                    check_initial("gpt", *values)

    def test_rejects_cross_run_report_and_findings_substitution(self):
        changes = [(0, "run", "N1-B131-GPT-003"), (1, "acceptedFindings", []),
                   (1, "verdict", "CLEAN"),
                   (1, "report", {"path": "another-report", "sha256": "b" * 64})]
        for index, key, value in changes:
            with self.subTest(key=key):
                values = copy.deepcopy(records("gpt"))
                values[index][key] = value
                with self.assertRaises((ValueError, RuntimeError)):
                    check_initial("gpt", *values)

    def test_rejects_lost_or_ambiguous_open_claim_inventory(self):
        for claims in (None, "D22", ["D22", "D22"], [22]):
            with self.subTest(claims=claims):
                values = records("gpt")
                values[1]["openClaimIds"] = claims
                with self.assertRaises((ValueError, RuntimeError)):
                    check_initial("gpt", *values)


if __name__ == "__main__":
    unittest.main()

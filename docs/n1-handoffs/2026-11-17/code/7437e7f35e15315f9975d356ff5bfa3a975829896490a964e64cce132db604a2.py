import unittest

from common import load_module
from prepare_b132_confirmation_engine import OUT


class ConfirmationClaimTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.checker = load_module("b132_claim_checker", OUT / "check-confirm-structure.py")

    def report(self, consistency="CLEAN"):
        return f"""# B132 confirmation - N1-B132-GPT-CONFIRM-001

## Snapshot
Commit: synthetic
Model: synthetic

## Scope
Chain: 1
Fetches: 0

## Dispositions
- Q1 - RESOLVED - Synthetic source-backed decision.
- Q2 - DISPUTE ACCEPTED - Synthetic second decision.

## Verdicts
Correctness: CLEAN
Scoped coverage: CLEAN
Consistency and quiz safety: {consistency}
Comprehensibility: CLEAN

## Confirmation
Verdict: CONFIRMED
Basis: Synthetic fixture, not review evidence.

## Findings
None.

## Optional
None.

## Limits
- L1: Synthetic fixture.
"""

    def test_explicit_q_dispositions_are_required(self):
        args = ("N1-B132-GPT-CONFIRM-001", "synthetic", ["Q1", "Q2"], {"sources": []}, "CONFIRMED")
        self.assertEqual(self.checker.check(self.report(), *args)["status"], "PASS")
        missing = self.report().replace("- Q2 - DISPUTE ACCEPTED - Synthetic second decision.\n", "")
        self.assertEqual(self.checker.check(missing, *args)["status"], "FAIL")

    def test_unverified_facet_cannot_be_confirmed(self):
        result = self.checker.check(self.report("UNVERIFIED"), "N1-B132-GPT-CONFIRM-001",
                                    "synthetic", ["Q1", "Q2"], {"sources": []}, "CONFIRMED")
        self.assertEqual(result["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()

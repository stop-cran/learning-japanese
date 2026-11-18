import copy
import json
import unittest

import verify_b130_revision_runtime as previous
import verify_b130_revision_runtime_v2 as current
from common import frozen


class OpenInitialClaimTests(unittest.TestCase):
    def evidence(self, family):
        accepted = json.loads(frozen(
            current.ROOT / f"N1-B130-{family.upper()}-004-acceptance.json",
            current.INITIAL_SHA[family]))
        adjudication = json.loads(frozen(
            accepted["adjudication"]["path"], accepted["adjudication"]["sha256"]))
        final = json.loads(frozen(accepted["final"]["path"], accepted["final"]["sha256"]))
        return accepted, adjudication, final

    def test_real_accepted_initials_preserve_the_unresolved_gpt_claims(self):
        for family in ("claude", "gpt"):
            accepted, adjudication, final = self.evidence(family)
            saved = copy.deepcopy(adjudication)
            current.check_initial(family, accepted, adjudication, final)
            self.assertEqual(saved, adjudication)
        with self.assertRaises(ValueError):
            previous.check_initial("gpt", *self.evidence("gpt"))

    def test_missing_relabelled_or_unbound_initial_evidence_is_rejected(self):
        accepted, adjudication, final = self.evidence("gpt")
        for field, value in (
            ("openClaimIds", []),
            ("openClaimIds", current.GPT_OPEN[:-1]),
            ("openClaimIds", current.GPT_OPEN + ["D99"]),
            ("unresolvedComparisons", adjudication["unresolvedComparisons"][:-1]),
            ("candidate", "0" * 40),
            ("acceptedFindings", []),
        ):
            bad = copy.deepcopy(adjudication)
            bad[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                current.check_initial("gpt", accepted, bad, final)
        bad = copy.deepcopy(adjudication)
        bad["unresolvedComparisons"][0]["disposition"] = "Harmless"
        with self.assertRaises(ValueError):
            current.check_initial("gpt", accepted, bad, final)
        for field, value in (("reviewAccepted", False), ("run", "N1-B130-GPT-001"), ("report", {})):
            with self.subTest(field=field), self.assertRaises(ValueError):
                current.check_initial("gpt", {**accepted, field: value}, adjudication, final)
        with self.assertRaises(ValueError):
            current.check_initial("gpt", accepted, adjudication, {**final, "status": "HOLD"})

    def test_runtime_output_does_not_close_or_alias_initial_claims(self):
        claims = {"claude": [], "gpt": list(current.GPT_OPEN)}
        result = current.claim_boundary(claims)
        self.assertEqual(claims, result["initialOpenClaimIds"])
        self.assertFalse(result["claimResolutionAccepted"])
        claims["gpt"].clear()
        self.assertEqual(current.GPT_OPEN, result["initialOpenClaimIds"]["gpt"])
        for invalid in (claims, {"gpt": current.GPT_OPEN},
                        {"claude": ["Q1"], "gpt": current.GPT_OPEN}):
            with self.assertRaises(ValueError):
                current.claim_boundary(invalid)


if __name__ == "__main__":
    unittest.main()

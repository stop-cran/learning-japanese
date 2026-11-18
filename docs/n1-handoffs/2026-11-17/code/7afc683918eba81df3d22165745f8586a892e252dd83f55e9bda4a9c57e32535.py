import json
import unittest

from close_b130_fresh import require_confirmation
from common import frozen
from prepare_b130_closure_inputs import CANDIDATE, ROOT, accepted_finals


class UnverifiedClosureTests(unittest.TestCase):
    def test_actual_unverified_report_cannot_be_used_as_final_acceptance(self):
        accepted = json.loads(frozen(ROOT / "confirm" / "N1-B130-GPT-CONFIRM-002-acceptance.json"))
        self.assertTrue(accepted["reviewEvidenceAccepted"])
        self.assertFalse(accepted["confirmationAccepted"])
        self.assertEqual(accepted["openClaimIds"], ["D18"])
        with self.assertRaisesRegex(ValueError, "not accepted"):
            require_confirmation(accepted, CANDIDATE)
        with self.assertRaisesRegex(ValueError, "Two actual accepted confirmations"):
            accepted_finals()


if __name__ == "__main__":
    unittest.main()

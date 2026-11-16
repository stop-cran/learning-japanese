import copy
import unittest

from b130_followup_closure_history import FINALS, HISTORICAL
from prepare_b130_followup_ready import ledger_acceptance


class FollowupAcceptanceTests(unittest.TestCase):
    def test_derives_batch_only_for_the_matching003_and_prior002(self):
        accepted = {"family": "gpt", "run": FINALS["gpt"], "candidate": "a" * 40, "session": "reviewer"}
        preflight = {**accepted, "batch": 130, "priorRun": HISTORICAL["gpt"]}
        self.assertEqual(ledger_acceptance(accepted, preflight), {**accepted, "batch": 130})
        self.assertNotIn("batch", accepted)
        for key, value in (("priorRun", "N1-B130-GPT-CONFIRM-001"), ("candidate", "b" * 40),
                           ("session", "other"), ("batch", 129)):
            changed = copy.deepcopy(preflight)
            changed[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                ledger_acceptance(accepted, changed)
        with self.assertRaises(ValueError):
            ledger_acceptance({**accepted, "run": HISTORICAL["gpt"]},
                              {**preflight, "run": HISTORICAL["gpt"]})


if __name__ == "__main__":
    unittest.main()

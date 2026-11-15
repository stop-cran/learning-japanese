import unittest
from types import SimpleNamespace

from close_selected_v2 import require_historical_confirmation
from confirm_followup import render_followup_prompt, require_prior_state


class AcceptedFollowupTests(unittest.TestCase):
    def setUp(self):
        self.spec = {"batch": 118, "basis": "accepted-confirmation", "priorVerdict": "CONFIRMED", "openClaimIds": []}
        self.prior = {
            "verdict": "CONFIRMED", "confirmationAccepted": True, "reviewEvidenceAccepted": True,
            "openClaimIds": [], "acceptedNewFindings": [], "candidate": "prior",
        }

    def test_accepted_snapshot_can_receive_a_new_delta_without_relabeling(self):
        original = dict(self.prior)
        require_prior_state(self.spec, self.prior, [])
        require_historical_confirmation(self.prior, "new")
        self.assertEqual(self.prior, original)

    def test_open_or_unaccepted_snapshot_cannot_masquerade_as_accepted(self):
        for change in ({"confirmationAccepted": False}, {"reviewEvidenceAccepted": False},
                       {"verdict": "NEEDS FIX"}, {"openClaimIds": ["F1"]},
                       {"acceptedNewFindings": ["F1"]}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                require_prior_state(self.spec, {**self.prior, **change}, [])
        with self.assertRaises(ValueError):
            require_prior_state(self.spec, self.prior, ["F1"])
        with self.assertRaises(ValueError):
            require_prior_state({**self.spec, "priorVerdict": "NEEDS FIX"}, self.prior, [])

    def test_accepted_prior_cannot_be_relabelled_as_held(self):
        with self.assertRaises(ValueError):
            require_prior_state({**self.spec, "basis": "held-confirmation"}, self.prior, [])

    def test_existing_needs_fix_path_still_requires_unaccepted_evidence(self):
        prior = {**self.prior, "confirmationAccepted": False, "verdict": "NEEDS FIX",
                 "acceptedNewFindings": ["F1"], "openClaimIds": ["F1"]}
        require_prior_state({"basis": "confirmation"}, prior, ["F1"])
        require_historical_confirmation(prior, "new")
        with self.assertRaises(ValueError):
            require_historical_confirmation(prior, "prior")

    def test_historical_snapshot_is_not_final_acceptance(self):
        with self.assertRaises(ValueError):
            require_historical_confirmation(self.prior, "prior")
        with self.assertRaises(ValueError):
            require_historical_confirmation({**self.prior, "openClaimIds": ["F1"]}, "new")

    def test_prompt_preserves_accepted_status_and_delta_scope(self):
        def render(spec, *args):
            self.assertEqual(spec["basis"], "confirmation")
            return f"Perform ONE read-only confirmation of your own accepted B{spec['batch']} adjudicated previous confirmation."

        text = render_followup_prompt(SimpleNamespace(render_prompt=render), self.spec, {}, {}, None)
        self.assertIn("accepted B118 previous confirmation", text)
        second = render_followup_prompt(SimpleNamespace(render_prompt=render),
                                        {**self.spec, "batch": 119}, {}, {}, None)
        self.assertIn("accepted B119 previous confirmation", second)
        self.assertIn("remains accepted on its earlier snapshot", text)
        self.assertIn("checks only the subsequent actual delta", text)
        with self.assertRaises(ValueError):
            render_followup_prompt(SimpleNamespace(render_prompt=lambda *args: "changed"),
                                   self.spec, {}, {}, None)


if __name__ == "__main__":
    unittest.main()

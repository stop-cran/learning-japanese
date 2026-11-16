import copy
import unittest
from unittest.mock import patch

import b130_followup_closure_history as follow
from b130_fresh_closure_history import confirmation_origins
from test_b130_closure_ledger import ClosureLedgerTests


class FollowupClosureHistoryTests(unittest.TestCase):
    def fixture(self):
        baseline = ClosureLedgerTests()
        baseline.setUp()
        previous = follow.historical_confirmations()
        rows, finals = [], []
        for family in follow.REVIEWERS:
            initial = next(row for row in baseline.provenance["reviewLineage"]
                           if row["family"] == family and row["role"] == "initial")
            old = next(row for row in previous if row["family"] == family)
            rows.extend([initial, {
                "run": old["run"], "family": family, "session": old["session"],
                "role": "intermediate", "snapshot": follow.PREVIOUS,
                "rawVerdict": old["verdict"], "priorRun": None, "finalAcceptance": False,
                "confirmationAcceptedOnSnapshot": old["confirmationAccepted"],
            }, {
                "run": follow.FINALS[family], "family": family, "session": old["session"],
                "role": "final", "snapshot": baseline.candidate, "rawVerdict": "CONFIRMED",
                "priorRun": old["run"], "finalAcceptance": True, "confirmationAcceptedOnSnapshot": True,
            }])
            finals.append({**old, "run": follow.FINALS[family], "candidate": baseline.candidate,
                           "verdict": "CONFIRMED", "confirmationAccepted": True, "openClaimIds": []})
        prepared, origins = confirmation_origins(previous, follow.PREVIOUS)
        provenance = {**baseline.provenance, "reviewLineage": rows,
                      "intermediateRuns": list(follow.HISTORICAL.values()),
                      "finalRuns": list(follow.FINALS.values()),
                      "preparedOnlyConfirmationRuns": prepared, "confirmationOrigins": origins}
        return provenance, baseline.candidate, baseline.config, finals

    def test_synthetic_finals_preserve_actual_unequal_intermediate_outcomes(self):
        args = self.fixture()
        before = copy.deepcopy(args)
        with patch.object(follow, "verify_followup") as verify:
            history = follow.check_history(*args)
            self.assertEqual(verify.call_count, 2)
        self.assertEqual(args, before)
        self.assertEqual(len(history["gpt"]["openClaimIds"]), 24)

    def test_erased_held_review_or_transferred_acceptance_is_rejected(self):
        provenance, candidate, config, finals = self.fixture()
        for index, field, value in ((1, "confirmationAcceptedOnSnapshot", False),
                                    (4, "confirmationAcceptedOnSnapshot", True),
                                    (4, "rawVerdict", "CONFIRMED"),
                                    (5, "priorRun", None), (2, "snapshot", follow.PREVIOUS)):
            changed = copy.deepcopy(provenance)
            changed["reviewLineage"][index][field] = value
            with self.subTest(field=field), patch.object(follow, "verify_followup"), \
                    self.assertRaises(ValueError):
                follow.check_history(changed, candidate, config, finals)
        changed = copy.deepcopy(provenance)
        changed["intermediateRuns"] = []
        with patch.object(follow, "verify_followup"), self.assertRaises(ValueError):
            follow.check_history(changed, candidate, config, finals)


if __name__ == "__main__":
    unittest.main()

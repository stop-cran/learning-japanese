import unittest
from unittest.mock import patch

import b130_followup_closure_history as history
from common import TOOLS, frozen
from prepare_b130_followup_closure import archive_origins, derive_archive, derive_ledger
from test_b130_closure_ledger import ClosureLedgerTests
from test_b130_followup_closure_history import FollowupClosureHistoryTests


class FollowupClosureTests(unittest.TestCase):
    def test_archive_origin_retains_actual_hold_and_rejects_relabelled_copy(self):
        rows = history.historical_confirmations()
        prepared, origins = archive_origins(rows)
        self.assertEqual(len(prepared), 2)
        self.assertEqual(origins["gpt"]["run"], history.HISTORICAL["gpt"])
        changed = [rows[0], {**rows[1], "confirmationAccepted": True}]
        with self.assertRaises(ValueError):
            archive_origins(changed)
        text = derive_archive(frozen(TOOLS / "close_b130_fresh.py").decode("utf-8"))
        compile(text, "followup_archive_test", "exec")
        self.assertIn("require_historical_confirmation", text)
        self.assertIn("archive_origins(intermediates)", text)
        self.assertIn("require_archive_origin", text)

    def test_ledger_keeps_delivery_and_distinguishes_lifecycle_gates_from_limits(self):
        provenance, candidate, config, finals = FollowupClosureHistoryTests().fixture()
        baseline = ClosureLedgerTests()
        baseline.setUp()
        runtime = {**baseline.runtime, "parent": history.PREVIOUS}
        text = derive_ledger(frozen(TOOLS / "b130_closure_ledger_v2.py").decode("utf-8"))
        namespace = {"__name__": "followup_ledger_test"}
        exec(compile(text, "followup_ledger_test", "exec"), namespace)
        with patch.object(history, "verify_followup"):
            ledger = namespace["make_ledger"](baseline.old, config, provenance, "a" * 64, runtime, finals)
        self.assertEqual(ledger["accounting"]["publishedPendingRecordsWithCards"], 261)
        self.assertEqual(ledger["accounting"]["undelivered"], 967)
        self.assertFalse(ledger["runtimePublished"])
        self.assertEqual(ledger["review"]["historicalConfirmations"][1]["openClaimIds"], ["D18"])
        self.assertNotIn("remain pending", " ".join(ledger["limits"]))
        self.assertEqual(len(ledger["publicationGates"]), 3)


if __name__ == "__main__":
    unittest.main()

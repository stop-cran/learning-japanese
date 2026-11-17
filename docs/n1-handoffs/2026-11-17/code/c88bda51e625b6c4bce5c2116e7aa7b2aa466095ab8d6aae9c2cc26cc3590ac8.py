import copy
import json
import unittest
from unittest.mock import patch

import b130_fresh_closure_history as fresh
from common import TOOLS
import test_b130_closure_ledger as original_tests


class FreshOriginTests(unittest.TestCase):
    def test_actual_preflight_discloses_new_session_without_claiming_review_acceptance(self):
        root = fresh.ROOT / "confirm"
        prepared = json.loads((root / "N1-B130-CLAUDE-CONFIRM-001-preflight.json").read_bytes())
        record = json.loads((root / "N1-B130-CLAUDE-CONFIRM-002-preflight.json").read_bytes())
        final = {key: record[key] for key in ("run", "candidate", "session")}
        row = fresh.origin_row("claude", final, record["candidate"], record, prepared, "a" * 64)
        self.assertNotEqual(row["session"], row["originalSession"])
        self.assertNotIn("confirmationAccepted", row)
        for field, value in (("originalSession", "wrong"), ("session", prepared["session"]),
                             ("candidate", "b" * 40), ("sourceCount", 0),
                             ("replacementReason", "audited-original-context-compaction")):
            with self.subTest(field=field), self.assertRaises(ValueError):
                fresh.origin_row("claude", final, record["candidate"],
                                 {**record, field: value}, prepared, "a" * 64)


class FreshClosureTests(original_tests.ClosureLedgerTests):
    def setUp(self):
        super().setUp()
        for final in self.finals:
            final["run"] = final["run"][:-3] + "002"
            final["session"] = "synthetic-fresh-" + final["family"]
        for row in self.provenance["reviewLineage"]:
            if row["role"] == "final":
                row["run"] = row["run"][:-3] + "002"
                row["session"] = "synthetic-fresh-" + row["family"]
        self.provenance["finalRuns"] = [row["run"] for row in self.finals]
        self.prepared = [{"run": "synthetic-unexecuted-preparation"}]
        self.origins = {"claude": {"session": "synthetic-fresh-claude"},
                        "gpt": {"session": "synthetic-fresh-gpt"}}
        self.provenance["preparedOnlyConfirmationRuns"] = copy.deepcopy(self.prepared)
        self.provenance["confirmationOrigins"] = copy.deepcopy(self.origins)
        namespace = {"__name__": "fresh_closure_test"}
        exec(compile(fresh.derive_text((TOOLS / "b130_closure_ledger.py").read_text(encoding="utf-8")),
                     "fresh_closure_test", "exec"), namespace)
        for module, name, value in (
            (original_tests, "make_ledger", namespace["make_ledger"]),
            (original_tests, "check_history", namespace["check_history"]),
            (fresh, "confirmation_origins", lambda *_: (self.prepared, self.origins)),
        ):
            replacement = patch.object(module, name, value)
            replacement.start()
            self.addCleanup(replacement.stop)

    def test_prepared_runs_and_fresh_origin_cannot_be_omitted_or_relabelled(self):
        for field in ("preparedOnlyConfirmationRuns", "confirmationOrigins"):
            before = self.provenance[field]
            self.provenance[field] = {}
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.ledger()
            self.provenance[field] = before
        ledger = self.ledger()
        self.assertEqual(ledger["review"]["confirmationOrigins"], self.origins)
        self.assertEqual(ledger["review"]["preparedOnlyConfirmationRuns"], self.prepared)
        self.assertIn("Fresh same-family sessions", ledger["review"]["identity"])
        self.assertNotIn("Their original reviewers confirmed", ledger["review"]["identity"])


if __name__ == "__main__":
    unittest.main()

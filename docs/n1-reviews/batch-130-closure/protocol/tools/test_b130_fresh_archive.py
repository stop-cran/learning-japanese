import copy
import json
import unittest
from unittest.mock import Mock

import b130_fresh_archive as fresh
from common import TOOLS, frozen


class FreshArchiveTests(unittest.TestCase):
    def setUp(self):
        root = fresh.ROOT / "confirm"
        self.accepted = json.loads(frozen(root / "N1-B130-CLAUDE-CONFIRM-002-acceptance.json"))
        self.preflight = json.loads(frozen(root / "N1-B130-CLAUDE-CONFIRM-002-preflight.json"))
        self.spec = json.loads(frozen(root / "N1-B130-CLAUDE-CONFIRM-002-spec.json"))
        self.final = json.loads(frozen(root / "N1-B130-CLAUDE-CONFIRM-002-final.json"))
        self.origin = {
            "run": self.accepted["run"], "session": self.accepted["session"],
            "originalSession": self.accepted["originalSession"],
            "reason": "pre-admission-context-capacity",
        }

    def test_batch_is_derived_from_actual_bound_preflight_without_editing_acceptance(self):
        before = copy.deepcopy(self.accepted)
        row = fresh.ledger_acceptance(self.accepted, self.preflight)
        self.assertEqual(row["batch"], 130)
        self.assertEqual(self.accepted, before)
        for changed in ({**self.preflight, "batch": 129},
                        {**self.preflight, "session": "wrong"}):
            with self.assertRaises(ValueError):
                fresh.ledger_acceptance(self.accepted, changed)
        with self.assertRaises(ValueError):
            fresh.ledger_acceptance({**self.accepted, "batch": 129}, self.preflight)

    def test_original_and_fresh_identity_cannot_be_interchanged(self):
        launch = {"session": self.accepted["originalSession"]}
        args = (self.final, launch, self.accepted, "claude",
                self.accepted["candidate"], {"claude": self.origin})
        fresh.require_origin(self.spec, *args)
        for field, value in (("session", launch["session"]), ("originalSession", "wrong"),
                             ("candidate", "0" * 40), ("prior", {})):
            with self.subTest(field=field), self.assertRaises(ValueError):
                fresh.require_origin({**self.spec, field: value}, *args)

    def test_prepared_retention_never_copies_raw_events_or_implies_execution(self):
        rows = [{"run": "N1-B130-CLAUDE-CONFIRM-001", "family": "claude",
                 "status": "PREPARED_NOT_EXECUTED"}]
        copy_file = Mock()
        fresh.retain_preparations(fresh.ROOT, rows, {"claude": self.origin}, copy_file)
        names = [call.args[1] for call in copy_file.call_args_list]
        self.assertEqual(len(names), 8)
        self.assertFalse(any(name.endswith(".jsonl") or "admission" in name for name in names))
        with self.assertRaises(ValueError):
            fresh.retain_preparations(fresh.ROOT, [{**rows[0], "status": "CONFIRMED"}],
                                      {"claude": self.origin}, copy_file)

    def test_successor_keeps_archive_mechanics_and_retention(self):
        text = fresh.derive_text(frozen(TOOLS / "close_b130_compact_v4.py",
                                       fresh.SOURCE_SHA).decode("utf-8"))
        namespace = {"__name__": "fresh_archive_test"}
        exec(compile(text, "fresh_archive_test", "exec"), namespace)
        from b130_excluded_initials_v3 import archive_excluded
        from archive_b129_chains import prepare
        self.assertIs(namespace["archive_excluded"], archive_excluded)
        self.assertIs(namespace["prepare_public_chain"], prepare)
        self.assertIn("preparedOnlyConfirmationRuns", text)
        self.assertNotIn('"Confirmation changed reviewer"', text)
        for bad in ((fresh.NEW_TOOLS[0],), ("a.py", "a.py"), ("x\\y.py",)):
            with self.assertRaisesRegex(ValueError, "Additional tools"):
                namespace["archive"](130, "0" * 40, ("a", "b"),
                                     preflight_path=TOOLS / "unused", additional_tools=bad)


if __name__ == "__main__":
    unittest.main()

import unittest
from copy import deepcopy

from b123_unavailable_context import require_identity, render_replacement_prompt


class UnavailableContextTests(unittest.TestCase):
    def setUp(self):
        self.source = {
            "batch": 123, "run": "N1-B123-CLAUDE-CONFIRM-004",
            "session": "old", "family": "claude", "candidate": "signed",
            "basis": "accepted-confirmation", "prior": {"path": "prior", "sha256": "p"},
            "revisedSources": ["card", "complete-sources"], "additionalSources": ["short-quotes"],
        }
        self.spec = {**self.source, "run": "N1-B123-CLAUDE-REPLACEMENT-CONFIRM-005",
                     "session": "fresh", "replayedFrom": {"path": "source", "sha256": "s"},
                     "unavailable": {"path": "unavailable", "sha256": "u"}}
        self.unavailable = {
            "run": self.source["run"], "session": "old", "family": "claude",
            "candidate": "signed", "status": "UNLAUNCHED_CONTEXT_COMPACTION",
            "reviewEvidenceAccepted": False, "confirmationAccepted": False,
        }

    def test_replacement_preserves_source_scope_and_historical_identity(self):
        original = deepcopy(self.source)
        require_identity(self.spec, self.source, self.unavailable)
        self.assertEqual(self.source, original)

    def test_changed_scope_or_reused_identity_is_rejected(self):
        for change in ({"session": "old"}, {"family": "gpt"}, {"candidate": "changed"},
                       {"additionalSources": []}, {"revisedSources": ["card"]},
                       {"run": self.source["run"]}, {"basis": "held-confirmation"},
                       {"reviewerOrigin": {}}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                require_identity({**self.spec, **change}, self.source, self.unavailable)

    def test_an_executed_or_accepted_run_cannot_be_called_unlaunched(self):
        for change in ({"confirmationAccepted": True}, {"reviewEvidenceAccepted": True},
                       {"status": "HELD_CONTEXT_COMPACTION"}, {"status": "VOID_EXECUTION"},
                       {"run": "N1-B123-CLAUDE-CONFIRM-003"}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                require_identity(self.spec, self.source, {**self.unavailable, **change})

    def test_unknown_prompt_cannot_keep_false_report_ownership(self):
        with self.assertRaises(ValueError):
            render_replacement_prompt("Unexpected renderer output")


if __name__ == "__main__":
    unittest.main()

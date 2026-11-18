import unittest
from copy import deepcopy

from replay_lineage import require_replay_identity, render_replay_prompt


class ReplayTests(unittest.TestCase):
    def setUp(self):
        self.source = {
            "batch": 117, "run": "N1-B117-CLAUDE-REPLACEMENT-CONFIRM-005",
            "session": "old", "family": "claude", "candidate": "signed",
            "basis": "accepted-confirmation", "prior": {"path": "prior", "sha256": "p"},
            "reviewerOrigin": {"path": "origin", "sha256": "o"},
            "revisedSources": ["target", "complete-sources"], "originalSources": ["rubric"],
        }
        self.spec = {**self.source, "run": "N1-B117-CLAUDE-REPLAY-CONFIRM-006", "session": "fresh",
                     "replayedFrom": {"path": "source", "sha256": "s"},
                     "unavailable": {"path": "held", "sha256": "h"}}
        self.spec["priorReviewerOrigin"] = self.spec.pop("reviewerOrigin")
        self.held = {
            "run": self.source["run"], "session": "old", "family": "claude", "candidate": "signed",
            "status": "HELD_CONTEXT_COMPACTION", "reviewEvidenceAccepted": False,
            "confirmationAccepted": False,
        }

    def test_exact_scope_is_preserved_without_relabeling_prior_identity(self):
        original = deepcopy(self.source)
        require_replay_identity(self.spec, self.source, self.held)
        self.assertEqual(original, self.source)
        self.assertNotIn("reviewerOrigin", self.spec)

    def test_changed_scope_identity_snapshot_or_held_state_is_rejected(self):
        for change in ({"session": "old"}, {"family": "gpt"}, {"candidate": "different"},
                       {"revisedSources": ["target"]}, {"priorReviewerOrigin": {}},
                       {"run": self.source["run"]}, {"basis": "confirmation"}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                require_replay_identity({**self.spec, **change}, self.source, self.held)
        for change in ({"confirmationAccepted": True}, {"reviewEvidenceAccepted": True},
                       {"status": "ACCEPTED"}, {"run": "different"}, {"session": "other"}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                require_replay_identity(self.spec, self.source, {**self.held, **change})

    def test_ownership_rewording_is_fail_closed(self):
        with self.assertRaises(ValueError):
            render_replay_prompt("Unexpected renderer output")


if __name__ == "__main__":
    unittest.main()

import unittest

from close_v2 import require_context_hold, require_identity


class ReplacementClosureTests(unittest.TestCase):
    def test_preserves_raw_held_verdict_without_treating_it_as_acceptance(self):
        mechanics = {"run": "run", "candidate": "sha", "session": "old", "status": "HOLD",
                     "confirmation": "CONFIRMED", "report": {"sha256": "report"},
                     "context": {"sha256": "context"}}
        held = {**mechanics, "status": "HELD_CONTEXT_COMPACTION", "verdict": "CONFIRMED",
                "reviewEvidenceAccepted": False, "confirmationAccepted": False}
        context = {"status": "FAIL", "compactions": [{"type": "session.compaction_start"}]}
        require_context_hold(held, mechanics, context)
        for patch in ({"confirmationAccepted": True}, {"reviewEvidenceAccepted": True},
                      {"verdict": "NEEDS FIX"}, {"candidate": "different"},
                      {"report": {"sha256": "different"}}):
            with self.subTest(patch=patch), self.assertRaises(ValueError):
                require_context_hold({**held, **patch}, mechanics, context)

    def test_requires_explicit_replacement_provenance_for_changed_reviewer(self):
        require_identity({"session": "old"}, "old", {}, {"session": "old"})
        with self.assertRaises(ValueError):
            require_identity({"session": "new"}, "new", {}, {"session": "old"})
        with self.assertRaises(ValueError):
            require_identity({"session": "new", "unavailable": {}}, "new", {}, {"session": "old"})
        with self.assertRaises(ValueError):
            require_identity({"session": "old"}, "new", {}, {"session": "old"})


if __name__ == "__main__":
    unittest.main()

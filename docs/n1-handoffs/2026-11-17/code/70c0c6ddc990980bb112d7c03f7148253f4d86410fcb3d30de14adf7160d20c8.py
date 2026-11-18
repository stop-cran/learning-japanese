import unittest
from pathlib import Path

from common import load_module
from confirm_replacement import replacement_prompt, require_replacement


class ReplacementTests(unittest.TestCase):
    def setUp(self):
        self.spec = {"session": "fresh", "originalSession": "original",
                     "family": "claude", "candidate": "signed"}
        self.initial, self.launch = {"reviewAccepted": True}, {"session": "original"}
        self.held = {"session": "original", "family": "claude", "candidate": "signed",
                     "status": "HELD_CONTEXT_COMPACTION", "confirmationAccepted": False,
                     "reviewEvidenceAccepted": False}
        self.context = {"status": "FAIL", "compactions": [{"type": "session.compaction_start"}]}
        self.prior = {"session": "original", "family": "claude",
                      "reviewEvidenceAccepted": True, "confirmationAccepted": False}

    def test_exhausted_original_cannot_be_reused_or_relabeled(self):
        require_replacement(self.spec, self.initial, self.launch, self.held, self.context, self.prior)
        for patch in ({"session": "original"}, {"originalSession": "other"}, {"family": "gpt"},
                      {"candidate": "other"}):
            with self.subTest(patch=patch), self.assertRaises(ValueError):
                require_replacement({**self.spec, **patch}, self.initial, self.launch,
                                    self.held, self.context, self.prior)

    def test_no_replacement_without_a_real_unaccepted_context_failure(self):
        for held, context in (({**self.held, "reviewEvidenceAccepted": True}, self.context),
                              (self.held, {**self.context, "status": "PASS"}),
                              (self.held, {**self.context, "compactions": []})):
            with self.subTest(held=held, context=context), self.assertRaises(ValueError):
                require_replacement(self.spec, self.initial, self.launch, held, context, self.prior)

    def test_prompt_discloses_replacement_without_changing_access_or_report_rules(self):
        root = Path(__file__).parent.parent / "scratch-117" / "review" / "confirm"
        renderer = load_module("replacement_test_renderer", root / "renderer.py")
        text = renderer.render_prompt({"run": "test", "scope": ["card"], "dispositionIds": ["F1"]},
                                      {"candidate": "signed", "freeze": "base", "originalReport": "report",
                                       "report": "output"}, {"segments": [{"path": "segment"}]}, "prompt")
        changed = replacement_prompt(text)
        self.assertIn("fresh same-family reviewer", changed)
        self.assertNotIn("your own", changed)
        self.assertEqual(text[text.index("ACCESS RULES"):text.index("TASKS")],
                         changed[changed.index("ACCESS RULES"):changed.index("TASKS")])
        self.assertEqual(text[text.index("REPORT CONTRACT"):],
                         changed[changed.index("REPORT CONTRACT"):changed.index("\nREPLACEMENT IDENTITY")])


if __name__ == "__main__":
    unittest.main()

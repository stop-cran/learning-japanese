import copy
import json
import tempfile
import unittest
from pathlib import Path

from grammar_vocabulary import (
    INVENTORY, annotations, apply_review, context_hash, coverage_problems, initial_inventory, write_json,
)


class VocabularyCoverageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "grammar").mkdir()
        (self.root / "docs").mkdir()
        self.path = self.root / "grammar" / "sample.json"
        self.exercise = {"id": "example", "prompt": "𠮷野は____。", "acceptedAnswers": ["です"]}
        write_json(self.path, {"exercises": [self.exercise]})
        self.inventory = initial_inventory(self.root, "baseline")
        self.proposal = {
            "reviewer": "Synthetic test fixture; not a linguistic review",
            "exercises": [{
                "file": "sample.json", "exerciseId": "example",
                "contextSha256": context_hash(self.exercise),
                "notes": "Exact occurrence and explicit function/blank/punctuation exclusions.",
                "segments": [["𠮷野", "よしの", "𠮷野", "Yoshino"],
                             ["は", "function"], ["____", "grammar-target"], ["。", "punctuation"]],
            }],
        }

    def test_review_is_revision_bound_and_has_complete_unicode_coverage(self):
        self.assertEqual([], coverage_problems(self.root, self.inventory))
        self.assertTrue(coverage_problems(self.root, self.inventory, require_complete=True))
        apply_review(self.root, self.inventory, self.proposal)
        self.assertEqual([], coverage_problems(self.root, self.inventory, require_complete=True))
        saved = json.loads((self.root / INVENTORY).read_text(encoding="utf-8"))
        self.assertEqual(self.inventory, saved)
        data = json.loads(self.path.read_text(encoding="utf-8"))
        self.assertEqual(2, data["exercises"][0]["vocabulary"]["spans"][0]["end"])
        for field, value in (("prompt", "別の____。"), ("acceptedAnswers", ["でした"]),
                             ("translation", "A different interpretation."),
                             ("options", [{"id": "different", "label": "でした"}]),
                             ("vocabulary", {"spans": []}), ("vocabulary", None), ("vocabulary", "bad")):
            changed = copy.deepcopy(data)
            changed["exercises"][0][field] = value
            write_json(self.path, changed)
            self.assertTrue(coverage_problems(self.root, saved), field)
        write_json(self.path, data)
        saved["records"][0]["exclusions"].pop()
        self.assertTrue(coverage_problems(self.root, saved))

    def test_level_changes_preserve_pending_proposals_and_reviewed_coverage(self):
        for level in (5, 3):
            write_json(self.path, {"exercises": [self.exercise | {"jlpt": level}]})
            self.assertEqual([], coverage_problems(self.root, self.inventory))
        apply_review(self.root, self.inventory, self.proposal)
        reviewed = json.loads(self.path.read_text(encoding="utf-8"))
        for level in (4, 1, None):
            with self.subTest(level=level):
                changed = copy.deepcopy(reviewed)
                exercise = changed["exercises"][0]
                if level is None:
                    exercise.pop("jlpt")
                else:
                    exercise["jlpt"] = level
                write_json(self.path, changed)
                self.assertEqual([], coverage_problems(self.root, self.inventory, require_complete=True))

    def test_new_prompt_and_changed_review_input_cannot_silently_reuse_coverage(self):
        with self.assertRaisesRegex(ValueError, "entire original prompt"):
            annotations("𠮷野は____。", self.proposal["exercises"][0]["segments"][:-1])
        self.proposal["exercises"][0]["contextSha256"] = "stale"
        with self.assertRaisesRegex(ValueError, "Context changed"):
            apply_review(self.root, self.inventory, self.proposal)
        write_json(self.path, {"exercises": [self.exercise, self.exercise | {"id": "new"}]})
        self.assertTrue(any("no coverage record" in p for p in coverage_problems(self.root, self.inventory)))


if __name__ == "__main__":
    unittest.main()

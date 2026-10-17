"""Regression tests for the grammar exercise authoring format."""
import copy
import json
import tempfile
import unittest
from pathlib import Path

from validate_grammar import check_grammar


VALID = {
    "schemaVersion": 1,
    "id": "sample-set",
    "title": "Sample",
    "article": "articles/sample.md",
    "constructions": [{"id": "alpha", "label": "甲"}, {"id": "beta", "label": "乙"}],
    "relationships": [{"id": "alpha-vs-beta", "label": "contrast", "constructions": ["alpha", "beta"]}],
    "exercises": [
        {
            "id": "alpha-example", "target": "alpha", "relationship": "alpha-vs-beta", "prompt": "A ____.", "translation": "A.",
            "evidence": "Context.", "explanation": "Reason.", "answer": "alpha", "acceptedAnswers": ["甲"],
            "options": [{"id": "alpha", "label": "甲", "rationale": "Fits."}, {"id": "beta", "label": "乙", "rationale": "Does not fit."}],
        },
        {
            "id": "beta-example", "target": "beta", "relationship": "alpha-vs-beta", "prompt": "B ____.", "translation": "B.",
            "evidence": "Context.", "explanation": "Reason.", "answer": "beta", "acceptedAnswers": ["乙"],
            "options": [{"id": "alpha", "label": "甲", "rationale": "Does not fit."}, {"id": "beta", "label": "乙", "rationale": "Fits."}],
        },
    ],
}


class GrammarValidationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "grammar").mkdir()
        (self.root / "articles").mkdir()
        (self.root / "articles" / "sample.md").write_text("# Sample\n", encoding="utf-8")

    def check(self, mutate=None):
        data = copy.deepcopy(VALID)
        if mutate:
            mutate(data)
        (self.root / "grammar" / "sample-set.json").write_text(json.dumps(data), encoding="utf-8")
        problems = []
        count = check_grammar(lambda path, message: problems.append(message), self.root)
        return count, problems

    def test_valid_set(self):
        count, problems = self.check()
        self.assertEqual(1, count)
        self.assertEqual([], problems)

    def test_rejects_incomplete_relationship_coverage(self):
        _, problems = self.check(lambda data: data["exercises"].pop())
        self.assertTrue(any("every construction" in message for message in problems), problems)

    def test_rejects_multiple_blanks_and_missing_alternative_rationale(self):
        def mutate(data):
            data["exercises"][0]["prompt"] = "A ____ and ____."
            data["exercises"][0]["options"][1]["rationale"] = ""
        _, problems = self.check(mutate)
        self.assertTrue(any("exactly one" in message for message in problems), problems)
        self.assertTrue(any("rationale" in message for message in problems), problems)

    def test_rejects_missing_article(self):
        (self.root / "articles" / "sample.md").unlink()
        _, problems = self.check()
        self.assertTrue(any("does not exist" in message for message in problems), problems)

    def test_malformed_nested_values_report_errors_instead_of_crashing(self):
        def mutate(data):
            data["relationships"][0]["constructions"] = [["not", "an", "id"]]
            data["exercises"][0]["target"] = []
            data["exercises"][0]["options"][0]["id"] = {}
        _, problems = self.check(mutate)
        self.assertTrue(problems)


if __name__ == "__main__":
    unittest.main()

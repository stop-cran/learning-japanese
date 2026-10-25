"""Counter transport and answer-key regressions, independent of language review."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from validate_counters import answer_key, check_counters


class CounterTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        (self.root / "counters").mkdir()
        (self.root / "articles").mkdir()
        (self.root / "articles" / "counts.md").write_text("# Counts\n", encoding="utf-8")
        self.expression = {
            "id": "age-expression-1", "cue": "20 years old.", "written": "二十歳",
            "writtenAnswers": ["二十歳", "20歳", "二十才", "20才"],
            "reading": "はたち", "readingAnswers": ["はたち", "にじゅっさい", "にじっさい"],
            "explanation": "Age, not duration.",
        }
        self.file = {
            "schemaVersion": 2, "id": "age", "counter": "歳", "reading": "さい",
            "title": "Age", "level": 5, "group": "everyday", "article": "articles/counts.md",
            "sources": ["https://example.org/reference"], "expressions": [self.expression],
        }

    def validate(self, value=None, name="age"):
        (self.root / "counters" / f"{name}.json").write_text(
            json.dumps(value if value is not None else self.file, ensure_ascii=False), encoding="utf-8")
        errors = []
        check_counters(lambda path, message: errors.append(message), self.root)
        return errors

    def test_complete_forms_use_narrow_keys(self):
        self.assertEqual([], self.validate())
        self.assertEqual(answer_key("20歳"), answer_key(" ２０ 歳 "))
        self.assertNotEqual(answer_key("十十歳"), answer_key("二十歳"))
        self.assertNotEqual(answer_key("歳"), answer_key("二十歳"))
        self.assertEqual(answer_key("ニジュッサイ", True), answer_key("にじゅっさい", True))
        self.assertNotEqual(answer_key("にじゅっさい", True), answer_key("にじゆっさい", True))

    def test_bad_shapes_and_ambiguous_normalized_duplicates_are_rejected(self):
        for field, value in (
                ("writtenAnswers", ["歳"]), ("writtenAnswers", ["二十歳", "20歳", "２０歳"]),
                ("readingAnswers", ["はたち", "ハタチ"]), ("readingAnswers", ["二十歳"]),
                ("readingAnswers", None), ("cue", ""), ("id", "not-stable"),
                ("explanation", "x" * 1001)):
            with self.subTest(field=field, value=value):
                changed = copy.deepcopy(self.file)
                changed["expressions"][0][field] = value
                self.assertTrue(self.validate(changed))
        for field, value in (("schemaVersion", 9), ("schemaVersion", True), ("group", "mystery"),
                             ("article", "articles/missing.md"), ("sources", None),
                             ("expressions", []), ("level", True), ("schemaVersion", "2"),
                             ("cards", None), ("reverse", False), ("vocabulary", "invalid"),
                             ("vocabulary", {"test": {"reading": 1}})):
            with self.subTest(field=field):
                changed = copy.deepcopy(self.file)
                changed[field] = value
                self.assertTrue(self.validate(changed))
        self.assertTrue(self.validate({**self.file, "unknown": True}))

    def test_duplicate_id_is_rejected_across_files(self):
        self.assertEqual([], self.validate())
        other = copy.deepcopy(self.file)
        other["id"] = "other"
        self.assertTrue(any("duplicate expression ID" in problem for problem in self.validate(other, "other")))

    def test_v1_metadata_is_optional_and_only_for_canonical_reading(self):
        card = dict(id="hon-pen-1", kind="plain", text="ペンが三{}あります。", en="Three pens.",
                    noun="ペン", phrase="三本", reading="さんぼん", good=["本", "三本"],
                    kana=["さんぼん"], distractors=["匹", "冊", "回"])
        old = dict(schemaVersion=1, id="hon", counter="本", reading="ほん", title="Long things",
                   level=5, cards=[card])
        self.assertEqual([], self.validate(old, "hon"))
        card["readingAnswers"] = ["さんぼん"]
        self.assertEqual([], self.validate(old, "hon"))
        card["readingAnswers"] = ["みっつ"]
        self.assertTrue(self.validate(old, "hon"))
        for bad in (None, "", {}, False):
            card["readingAnswers"] = bad
            self.assertTrue(self.validate(old, "hon"))


if __name__ == "__main__":
    unittest.main()

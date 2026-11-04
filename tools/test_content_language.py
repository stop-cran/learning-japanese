"""Language transport and localized authoring regressions; not linguistic certification."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from build_manifest import build_manifest
from content_language import read_language
import validate


class ContentLanguageTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        (self.root / "articles").mkdir()
        (self.root / "articles" / "example.md").write_text("# Example\n", encoding="utf-8")

    def language(self, base="ru", target="ja"):
        (self.root / "content-language.json").write_text(
            json.dumps({"baseLanguage": base, "targetLanguage": target}), encoding="utf-8")

    def test_legacy_and_explicit_english_keep_old_reader_schema(self):
        legacy = build_manifest(self.root)
        self.assertEqual(("en", "ja", 1), (legacy["baseLanguage"], legacy["targetLanguage"], legacy["schemaVersion"]))
        self.language("en")
        self.assertEqual(legacy, build_manifest(self.root))

    def test_russian_fails_closed_for_old_reader_and_metadata_changes_version(self):
        english = build_manifest(self.root)
        self.language()
        russian = build_manifest(self.root)
        self.assertEqual(("ru", "ja", 2), (russian["baseLanguage"], russian["targetLanguage"], russian["schemaVersion"]))
        self.assertEqual(english["files"], russian["files"])
        self.assertNotEqual(english["contentVersion"], russian["contentVersion"])
        self.assertEqual(russian, build_manifest(self.root))

    def test_invalid_language_declarations_stop_generation(self):
        for value in ({}, [], {"baseLanguage": "ru"}, {"baseLanguage": [], "targetLanguage": "ja"},
                      {"baseLanguage": "RU", "targetLanguage": "ja"}, {"baseLanguage": "ru", "targetLanguage": "en"},
                      {"baseLanguage": "en", "targetLanguage": "ja", "extra": 1}):
            with self.subTest(value=value):
                (self.root / "content-language.json").write_text(json.dumps(value), encoding="utf-8")
                with self.assertRaises(ValueError):
                    build_manifest(self.root)
        for raw in ('{', '{"baseLanguage":"en","baseLanguage":"ru","targetLanguage":"ja"}'):
            (self.root / "content-language.json").write_text(raw, encoding="utf-8")
            with self.assertRaises(ValueError):
                read_language(self.root)

    def test_russian_sections_and_facts_are_validated_without_english_headings(self):
        self.language()
        meta = {"kanji": "日", "title": "солнце, день"}
        body = """# 日 — солнце, день
**Черты:** 4 · **Ключ (радикал):** 日 (№ 72) · **JLPT:** N5
## Значение и происхождение
Значение.
## Чтения
Чтения.
## Частые слова
Слова.
## Примечания
Примечания.
"""
        with patch.object(validate, "ROOT", self.root), patch.object(validate, "errors", []):
            validate.check_body(self.root / "kanji" / "日.md", meta, body)
            self.assertEqual([], validate.errors)
            validate.check_body(self.root / "kanji" / "日.md", meta, body.replace("## Чтения", "## Readings"))
            self.assertTrue(validate.errors)

    def test_kana_only_russian_words_can_omit_combination_section(self):
        self.language()
        body = "# もしもし\n## Значение\nЗначение.\n## Синонимы и антонимы\nСлова.\n## Оттенки значения\nПримечание.\n"
        with patch.object(validate, "ROOT", self.root), patch.object(validate, "errors", []):
            validate.check_body(self.root / "words" / "もしもし.md", {"kanji": []}, body)
            self.assertEqual([], validate.errors)
            validate.check_body(self.root / "words" / "もしもし.md", {"kanji": ["日"]}, body)
            self.assertTrue(validate.errors)

    def test_localized_reading_rows_still_require_their_own_linked_example(self):
        self.language()
        (self.root / "words").mkdir()
        (self.root / "words" / "日.md").touch()
        meta = {"kanji": "日", "title": "солнце, день", "quizKunyomi": ["ひ"]}
        body = """# 日 — солнце, день
**Черты:** 4 · **Ключ (радикал):** 日 (№ 72) · **JLPT:** N5
## Значение и происхождение
Солнце.
## Чтения
| Чтение | Тип | Примеры |
| --- | --- | --- |
| ひ | кун | [日](../words/日.md) ひ |
## Частые слова
日.
## Примечания
Примечание.
"""
        with patch.object(validate, "ROOT", self.root), patch.object(validate, "errors", []):
            path = self.root / "kanji" / "日.md"
            validate.check_body(path, meta, body)
            self.assertEqual([], validate.errors)
            validate.check_body(path, meta, body.replace("[日](../words/日.md)", "日"))
            self.assertTrue(any("own" in error for error in validate.errors))


if __name__ == "__main__":
    unittest.main()

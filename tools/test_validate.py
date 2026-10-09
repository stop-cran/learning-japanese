"""Regression tests for authoring rules and the Android front-matter subset."""
import copy
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import validate


REPO = validate.ROOT
KANJI_HEADER = """kanji: 日
title: sun, day
jlpt: 5
tags: [jlpt-n5, starter]
strokes: 4
radical: 日
radicalNumber: 72
onyomi: [ニチ, ジツ]
kunyomi: [ひ, -び, -か]
distractors: [月, 口]"""
KANJI_BODY = """# 日 — sun, day

**Strokes:** 4 · **Key (radical):** 日 (no. 72) · **Phonetic:** none · **JLPT:** N5

## Meaning and origin
Meaning.
## Readings
Readings.
## Common words
Words.
## Notes
Notes.
"""
WORD_HEADER = """word: 土地
reading: とち
title: land; plot
type: kango
kanji: [土, 地]
tags: [kango]"""
WORD_BODY = """# 土地 (とち) — land

## Meaning
Meaning.
## How the kanji combine
Combination.
## Synonyms and antonyms
Synonyms.
## Distinctive meaning
Nuance.
"""


class ValidateTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        for folder in ("kanji", "words", "articles", "strokes"):
            (self.root / folder).mkdir()
        self.root_patch = patch.object(validate, "ROOT", self.root)
        self.root_patch.start()
        self.addCleanup(self.root_patch.stop)
        errors_patch = patch.object(validate, "errors", [])
        errors_patch.start()
        self.addCleanup(errors_patch.stop)
        self.kanji_path = self.write("kanji/日.md", KANJI_HEADER, KANJI_BODY)
        self.word_path = self.write("words/土地.md", WORD_HEADER, WORD_BODY)
        for char in ("月", "口"):
            (self.root / "kanji" / f"{char}.md").touch()
        self.stroke_path = self.root / "strokes" / "日.json"
        self.stroke_data = {
            "schemaVersion": 1, "kanji": "日", "viewBox": [0, 0, 109, 109], "strokeCount": 4,
            "strokes": [{"id": index, "points": [[0, 0], [1.5, 2]]} for index in range(1, 5)],
        }
        self.write_strokes(self.stroke_data)

    def write(self, name, header, body=""):
        path = self.root / name
        path.write_text(f"---\n{header}\n---\n{body}", encoding="utf-8")
        return path

    def assert_error(self, text):
        self.assertTrue(any(text in error for error in validate.errors), validate.errors)

    def write_strokes(self, data):
        self.stroke_path.write_text(json.dumps(data), encoding="utf-8")

    def check_card(self, path):
        meta, body = validate.parse(path)
        self.assertIsNotNone(meta, validate.errors)
        if path.parent.name == "kanji":
            validate.check_kanji(path, meta, {})
        else:
            validate.check_word(path, meta)
        validate.check_body(path, meta, body)
        validate.check_links(path, body)
        return meta

    def test_valid_fixtures_and_optional_phonetic(self):
        self.check_card(self.kanji_path)
        self.check_card(self.word_path)
        body = KANJI_BODY.replace("**Phonetic:** none", "**Phonetic:** not identified here")
        self.write("kanji/日.md", KANJI_HEADER, body)
        meta = self.check_card(self.kanji_path)
        self.assertNotIn("phonetic", meta)
        body = KANJI_BODY.replace("**Phonetic:** none", "**Phonetic:** 日")
        self.write("kanji/日.md", KANJI_HEADER + "\nphonetic: 日", body)
        meta = self.check_card(self.kanji_path)
        self.assertEqual("日", meta["phonetic"])
        self.assertEqual([], validate.errors)

    def test_app_optional_fields_do_not_weaken_authoring_requirements(self):
        for path, header, required, checker in (
                (self.kanji_path, "kanji: 日\ntitle: sun, day", validate.KANJI_REQUIRED,
                 lambda p, m: validate.check_kanji(p, m, {})),
                (self.word_path, "word: 土地\nreading: とち\ntitle: land", validate.WORD_REQUIRED,
                 validate.check_word)):
            with self.subTest(folder=path.parent.name):
                validate.errors.clear()
                self.write(path.relative_to(self.root), header)
                meta, _ = validate.parse(path)
                self.assertIsInstance(meta, dict)
                self.assertEqual([], validate.errors)
                checker(path, meta)
                for key in required:
                    if key not in meta:
                        self.assert_error(f"missing field '{key}'")

    def test_empty_reading_arrays_are_supported(self):
        for fields in (("onyomi",), ("kunyomi",), ("onyomi", "kunyomi")):
            for empty in ("[]", "[ ]"):
                with self.subTest(fields=fields, spelling=empty):
                    validate.errors.clear()
                    header = KANJI_HEADER
                    for key, readings in (("onyomi", "[ニチ, ジツ]"), ("kunyomi", "[ひ, -び, -か]")):
                        if key in fields:
                            header = header.replace(f"{key}: {readings}", f"{key}: {empty}")
                    self.write("kanji/日.md", header, KANJI_BODY)
                    meta = self.check_card(self.kanji_path)
                    for key in fields:
                        self.assertEqual([], meta[key])
                    self.assertEqual([], validate.errors)

    def test_free_tags_do_not_require_starter_or_a_closed_structure_enum(self):
        for tags in ("[jlpt-n5, structure-unclassified]", "[jlpt-n5, custom-study-tag]", "[jlpt-n5]"):
            with self.subTest(tags=tags):
                validate.errors.clear()
                header = KANJI_HEADER.replace("[jlpt-n5, starter]", tags)
                body = KANJI_BODY.replace("**Phonetic:** none", "**Phonetic:** not identified here")
                self.write("kanji/日.md", header, body)
                meta = self.check_card(self.kanji_path)
                self.assertNotIn("starter", meta["tags"])
                self.assertEqual([], validate.errors)
        self.write("words/土地.md", WORD_HEADER.replace("tags: [kango]", "tags: [custom-study-tag]"), WORD_BODY)
        self.check_card(self.word_path)
        self.assertEqual([], validate.errors)

    def test_android_accepts_flat_quotes_comments_and_empty_lists(self):
        header = KANJI_HEADER.replace("title: sun, day", 'title: "sun, day"')
        header = header.replace("[ニチ, ジツ]", '["ニチ", \'ジツ\']').replace("[ひ, -び, -か]", "[ ]")
        header += "\n\n  # Full-line comments are supported.\n"
        self.write("kanji/日.md", header, KANJI_BODY)
        self.check_card(self.kanji_path)
        self.assertEqual([], validate.errors)

    def test_yaml_accepted_but_android_incompatible(self):
        cases = (
            ("quoted comma", "tags: [jlpt-n5, starter]", 'tags: [jlpt-n5, "one,two"]'),
            ("block list", "onyomi: [ニチ, ジツ]", "onyomi:\n  - ニチ\n  - ジツ"),
            ("multiline list", "onyomi: [ニチ, ジツ]", "onyomi: [ニチ,\n  ジツ]"),
            ("scalar comment", "title: sun, day", "title: sun, day # gloss"),
            ("list comment", "tags: [jlpt-n5, starter]", "tags: [jlpt-n5, starter] # tags"),
            ("scalar escape", "title: sun, day", r'title: "sun\u002c day"'),
            ("list escape", "onyomi: [ニチ, ジツ]", r'onyomi: ["\u30CB\u30C1", ジツ]'),
            ("escaped quote", "title: sun, day", r'title: "sun \"day\""'),
            ("doubled quote", "title: sun, day", "title: 'sun''s day'"),
            ("folded scalar", "title: sun, day", "title: >-\n  sun, day"),
            ("literal scalar", "title: sun, day", "title: |-\n  sun, day"),
            ("multiline colon value", "title: sun, day", "title: |-\n  sun: day"),
            ("quoted key", "title: sun, day", '"title": sun, day'),
            ("trailing comma", "onyomi: [ニチ, ジツ]", "onyomi: [ニチ, ジツ,]"),
            ("scalar spelling", "radicalNumber: 72", "radicalNumber: 0x48"),
        )
        for name, original, replacement in cases:
            with self.subTest(name=name):
                validate.errors.clear()
                self.write("kanji/日.md", KANJI_HEADER.replace(original, replacement), KANJI_BODY)
                meta, _ = validate.parse(self.kanji_path)
                self.assertIsInstance(meta, dict)
                self.assert_error("Android")
                self.assertFalse(any("invalid front matter YAML" in error for error in validate.errors))

    def test_nel_does_not_become_android_whitespace(self):
        for name, original in (("kanji/日.md", KANJI_HEADER), ("words/土地.md", WORD_HEADER)):
            for header in (
                    "\x85" + original,
                    original.replace("\ntitle:", "\n\x85title:"),
                    original.replace("\ntype:", "\n\x85type:") if name.startswith("words")
                    else original.replace("\njlpt:", "\n\x85jlpt:"),
                    original.replace("\ntype:", "\x85\ntype:") if name.startswith("words")
                    else original.replace("\njlpt:", "\x85\njlpt:"),
                    original + "\n\x85",
                    original + "\n\x85# comment",
                    original.replace("tags: [", "tags: [\x85")):
                with self.subTest(name=name, header=header):
                    validate.errors.clear()
                    path = self.write(name, header)
                    meta, _ = validate.parse(path)
                    self.assertIsInstance(meta, dict)
                    self.assert_error("Android")

    def test_kotlin_header_blank_and_comment_rules(self):
        self.assertEqual({"title": "value"}, validate.parse_android_header(
            "\u00a0# comment\n\u2007\n\u3000title:\u00a0value\u202f"))
        self.assertEqual({"title": "value\x85"}, validate.parse_android_header("title: value\x85"))
        self.assertEqual({"tags": ["\x85"]}, validate.parse_android_header("tags: [\x85]"))
        self.assertEqual({"tags": ["\x85tag\x85"]}, validate.parse_android_header("tags: [\x85tag\x85]"))
        self.assertIsNone(validate.parse_android_header("\x85# comment"))
        self.assertIsNone(validate.parse_android_header("\x85"))
        header = KANJI_HEADER + "\n# comment\x85"
        self.write("kanji/日.md", header, KANJI_BODY)
        self.check_card(self.kanji_path)
        self.assertEqual([], validate.errors)

    def test_multiline_yaml_cannot_shadow_a_known_android_field(self):
        self.write("words/土地.md", WORD_HEADER + "\nnote: |\n  type: gairaigo", WORD_BODY)
        meta, _ = validate.parse(self.word_path)
        self.assertEqual("kango", meta["type"])
        self.assert_error("'type' is interpreted differently by YAML and Android")

    def test_android_header_boundaries_bom_and_crlf(self):
        for bom in ("", "\ufeff"):
            for newline in ("\n", "\r\n"):
                for closing in ("---", "--- ", "---note: ignored"):
                    with self.subTest(bom=bool(bom), newline=newline, closing=closing):
                        validate.errors.clear()
                        text = f"---\n{KANJI_HEADER}\n{closing}\n\n{KANJI_BODY}"
                        self.kanji_path.write_bytes((bom + text.replace("\n", newline)).encode("utf-8"))
                        meta, body = validate.parse(self.kanji_path)
                        self.assertEqual("sun, day", meta["title"])
                        self.assertEqual(KANJI_BODY, body)
                        self.check_card(self.kanji_path)
                        self.assertEqual([], validate.errors)

    def test_early_android_closer_cannot_hide_missing_fields(self):
        header = KANJI_HEADER.replace("\ntitle:", "\n---note: ignored\ntitle:")
        self.write("kanji/日.md", header, KANJI_BODY)
        meta, body = validate.parse(self.kanji_path)
        self.assertEqual({"kanji": "日"}, meta)
        self.assertTrue(body.startswith("title: sun, day\n"))
        validate.check_kanji(self.kanji_path, meta, {})
        self.assert_error("missing field 'title'")

    def test_terminal_marker_and_bare_cr_match_android(self):
        self.kanji_path.write_bytes(f"---\n{KANJI_HEADER}\n--- trailing text".encode("utf-8"))
        meta, body = validate.parse(self.kanji_path)
        self.assertEqual("日", meta["kanji"])
        self.assertEqual("", body)
        text = f"---\r{KANJI_HEADER}\r---\r"
        self.kanji_path.write_bytes(text.encode("utf-8"))
        meta, body = validate.parse(self.kanji_path)
        self.assertIsNone(meta)
        self.assertEqual(text, body)
        self.assertEqual([], validate.errors)

    def test_cr_only_card_has_no_android_front_matter(self):
        text = f"---\n{KANJI_HEADER}\n---\n{KANJI_BODY}".replace("\n", "\r")
        self.kanji_path.write_bytes(text.encode("utf-8"))
        meta, body = validate.parse(self.kanji_path)
        self.assertIsNone(meta)
        self.assertEqual(text, body)
        self.assertEqual([], validate.errors)

    def test_header_interior_bare_cr_is_not_normalized(self):
        cases = (
            (KANJI_HEADER.replace("\ntitle:", "\rtitle:"),
             "kanji", "日\rtitle: sun, day", "日"),
            (KANJI_HEADER.replace("title: sun, day", 'title: "sun\rday"'),
             "title", "sun\rday", "sun day"),
        )
        for header, key, android_value, yaml_value in cases:
            with self.subTest(key=key):
                validate.errors.clear()
                self.assertEqual(android_value, validate.parse_android_header(header)[key])
                self.kanji_path.write_bytes(f"---\n{header}\n---\n{KANJI_BODY}".encode("utf-8"))
                meta, body = validate.parse(self.kanji_path)
                self.assertEqual(yaml_value, meta[key])
                self.assertEqual(KANJI_BODY, body)
                self.assert_error(f"'{key}' is interpreted differently by YAML and Android")

    def test_articles_keep_ordinary_markdown_after_thematic_breaks(self):
        path = self.root / "articles" / "example.md"
        for header in ("Intro paragraph.", "[unfinished Markdown", "- first\n- second",
                       "\x85# comment", "\x85"):
            with self.subTest(header=header):
                validate.errors.clear()
                text = f"---\n{header}\n---\n\n# Example\n\nText.\n"
                path.write_bytes(("\ufeff" + text.replace("\n", "\r\n")).encode("utf-8"))
                meta, body = validate.parse(path)
                self.assertIsNone(meta)
                self.assertEqual(text, body)
                validate.check_links(path, body)
                self.assertEqual([], validate.errors)
        text = "---\nIntro without a second thematic break.\n# Example\n"
        path.write_bytes(text.encode("utf-8"))
        self.assertEqual((None, text), validate.parse(path))

    def test_article_flat_front_matter_and_optional_title(self):
        for header in ('title: "A, B"\ntags: [example]', "tags: []", "# comment", ""):
            with self.subTest(header=header):
                validate.errors.clear()
                path = self.write("articles/example.md", header, "\n# Heading\n")
                meta, body = validate.parse(path)
                self.assertIsInstance(meta, dict)
                self.assertEqual("# Heading\n", body)
                self.assertEqual([], validate.errors)
        path = self.root / "articles" / "example.md"
        path.write_bytes(b"---\ntitle: First\n---early\ntitle: Second\n---\n# Heading\n")
        meta, body = validate.parse(path)
        self.assertEqual({"title": "First"}, meta)
        self.assertEqual("title: Second\n---\n# Heading\n", body)
        self.assertEqual([], validate.errors)

    def test_article_mapping_shaped_unsupported_yaml_is_rejected(self):
        for header, error in (
                ("tags:\n  - example", "Android front matter"),
                (r'title: "A\u0042"', "'title' is interpreted differently"),
                ("title: Example # draft", "'title' is interpreted differently"),
                ("title: |-\n  subtitle: Example", "'title' is interpreted differently"),
                ("title: [\nunfinished", "invalid front matter YAML"),
                ("\x85title: Example", "'title' is interpreted differently"),
                ("title: Example\n\x85# comment", "Android front matter")):
            with self.subTest(header=header):
                validate.errors.clear()
                path = self.write("articles/example.md", header, "# Heading\n")
                validate.parse(path)
                self.assert_error(error)

    def test_article_plain_fallback_keeps_header_links_visible(self):
        path = self.write("articles/example.md", "Introduction.\n[missing](missing.md)", "# Heading\n")
        meta, body = validate.parse(path)
        self.assertIsNone(meta)
        self.assertTrue(body.startswith("---\nIntroduction.\n"))
        validate.check_links(path, body)
        self.assert_error("broken link: missing.md")

    def test_non_mapping_or_invalid_yaml_is_an_error(self):
        for header in ("", "false", "null", "42", "a scalar", "[one, two]", "- one\n- two",
                       "tags: [", "title: 2026-99-99"):
            with self.subTest(header=header):
                validate.errors.clear()
                path = self.write("words/土地.md", header, WORD_BODY)
                meta, _ = validate.parse(path)
                self.assertIsNone(meta)
                self.assertTrue(validate.errors)

    def test_bad_field_types_are_errors_not_exceptions(self):
        kanji, _ = validate.parse(self.kanji_path)
        word, _ = validate.parse(self.word_path)
        for path, original, checker in (
                (self.kanji_path, kanji, lambda p, m: validate.check_kanji(p, m, {})),
                (self.word_path, word, validate.check_word)):
            bad_values = {key: (None, {}, []) for key in original}
            for key in ("tags", "kanji") if path == self.word_path else validate.KANJI_LISTS:
                bad_values[key] = (None, "not a list", [False], [{}], [[]])
            if path == self.kanji_path:
                for key in validate.KANJI_INTS:
                    bad_values[key] = (True, False, "5", 5.0, None, {})
                bad_values["phonetic"] = (False, None, [])
            for key, values in bad_values.items():
                for value in values:
                    with self.subTest(folder=path.parent.name, key=key, value=value):
                        validate.errors.clear()
                        meta = copy.deepcopy(original)
                        meta[key] = value
                        checker(path, meta)
                        self.assert_error(f"'{key}' must be")
            for value in (None, [], True, "text"):
                with self.subTest(non_mapping=value):
                    validate.errors.clear()
                    checker(path, value)
                    self.assert_error("must be a mapping")

    def test_missing_fields_are_explicit_errors(self):
        for path, required, checker in (
                (self.kanji_path, validate.KANJI_REQUIRED, lambda p, m: validate.check_kanji(p, m, {})),
                (self.word_path, validate.WORD_REQUIRED, validate.check_word)):
            original, _ = validate.parse(path)
            for key in required:
                with self.subTest(folder=path.parent.name, key=key):
                    validate.errors.clear()
                    meta = dict(original)
                    del meta[key]
                    checker(path, meta)
                    self.assert_error(f"missing field '{key}'")

    def test_integer_fields_remain_yaml_integers(self):
        for key, original in (("jlpt", "5"), ("strokes", "4"), ("radicalNumber", "72")):
            for replacement in ("true", f"'{original}'"):
                with self.subTest(key=key, replacement=replacement):
                    validate.errors.clear()
                    header = KANJI_HEADER.replace(f"{key}: {original}", f"{key}: {replacement}")
                    self.write("kanji/日.md", header, KANJI_BODY)
                    self.check_card(self.kanji_path)
                    self.assert_error(f"'{key}' must be a YAML integer")

    def test_rare_kana_okurigana_and_affix_readings(self):
        meta, _ = validate.parse(self.kanji_path)
        meta["onyomi"] = ["ヰ", "ヱ", "ヵ", "ヶ"]
        meta["kunyomi"] = ["ゐる", "ゑ", "やす.む", "-び", "おお-"]
        validate.check_kanji(self.kanji_path, meta, {})
        self.assertEqual([], validate.errors)

    def test_word_jlpt_is_optional_and_independent_of_written_kanji(self):
        self.check_card(self.word_path)
        for level in range(1, 6):
            with self.subTest(level=level):
                self.write("words/土地.md", WORD_HEADER + f"\njlpt: {level}", WORD_BODY)
                meta = self.check_card(self.word_path)
                self.assertEqual(level, meta["jlpt"])
                self.assertEqual([], validate.errors)
        header = WORD_HEADER.replace("土地", "カレー").replace("とち", "カレー")
        header = header.replace("type: kango", "type: gairaigo").replace("[土, 地]", "[]")
        path = self.write("words/カレー.md", header + "\njlpt: 5", WORD_BODY)
        meta = self.check_card(path)
        self.assertEqual([], meta["kanji"])
        self.assertEqual(5, meta["jlpt"])
        self.assertEqual([], validate.errors)

    def test_word_jlpt_rejects_invalid_types_and_ranges(self):
        for value in ("true", "false", "'5'", "5.0", "null", "", "[]", "[5]", "{}",
                      "0", "6", "-1", "2147483648"):
            with self.subTest(value=value):
                validate.errors.clear()
                self.write("words/土地.md", WORD_HEADER + f"\njlpt: {value}", WORD_BODY)
                self.check_card(self.word_path)
                self.assert_error("'jlpt' must be")

    def test_word_jlpt_android_interpretation_cannot_be_shadowed(self):
        for extra in ("\njlpt: 5 # level", "\njlpt: 0x5",
                      "\njlpt: 5\nnote: |\n  jlpt: 4",
                      "\nnote: |\n  jlpt: 5"):
            with self.subTest(extra=extra):
                validate.errors.clear()
                self.write("words/土地.md", WORD_HEADER + extra, WORD_BODY)
                self.check_card(self.word_path)
                self.assert_error("'jlpt' is interpreted differently by YAML and Android")

    def test_word_jlpt_rejects_duplicate_declarations_even_when_values_match(self):
        for first in ("5", "4", "null", "", "[5]", "'5'"):
            with self.subTest(first=first):
                validate.errors.clear()
                self.write("words/土地.md", WORD_HEADER + f"\njlpt: {first}\njlpt: 5", WORD_BODY)
                self.check_card(self.word_path)
                self.assert_error("'jlpt' must be a single top-level unquoted integer")

    def test_word_jlpt_rejects_same_value_multiline_shadowing_and_quoted_keys(self):
        for extra in ("\njlpt: 5\nnote: |\n  jlpt: 5",
                      "\n'jlpt': 5", '\n"jlpt": 5'):
            with self.subTest(extra=extra):
                validate.errors.clear()
                self.write("words/土地.md", WORD_HEADER + extra, WORD_BODY)
                self.check_card(self.word_path)
                self.assert_error("'jlpt' must be a single top-level unquoted integer")

    def test_word_jlpt_comments_and_unrelated_scalar_text_are_not_declarations(self):
        for extra in ("\n# jlpt: 4\njlpt: 5", "\n  # jlpt: 4\njlpt: 5",
                      "\nnote: 'jlpt: 4'\njlpt: 5"):
            with self.subTest(extra=extra):
                validate.errors.clear()
                self.write("words/土地.md", WORD_HEADER + extra, WORD_BODY)
                self.check_card(self.word_path)
                self.assertEqual([], validate.errors)

    def test_word_jlpt_raw_declaration_rule_does_not_change_legacy_kanji_behavior(self):
        self.write("kanji/日.md", KANJI_HEADER + "\njlpt: 5", KANJI_BODY)
        self.check_card(self.kanji_path)
        self.assertEqual([], validate.errors)

    def test_word_quiz_exclusions_are_optional_and_allow_one_sided_references(self):
        other_header = WORD_HEADER.replace("土地", "場所").replace("とち", "ばしょ")
        other_header = other_header.replace("[土, 地]", "[場, 所]")
        other = self.write("words/場所.md", other_header, WORD_BODY.replace("土地", "場所"))
        self.check_card(other)
        for extra in ("", "\nquiz_exclusions: []", "\nquiz_exclusions: [ ]",
                      "\nquiz_exclusions: [場所]", "\nquiz_exclusions: ['場所']",
                      '\nquiz_exclusions: ["場所"]'):
            with self.subTest(extra=extra):
                self.write("words/土地.md", WORD_HEADER + extra, WORD_BODY)
                self.check_card(self.word_path)
                self.assertEqual([], validate.errors)

    def test_word_quiz_exclusions_reject_non_lists_and_nonstring_items(self):
        for value in ("null", "true", "5", "{}", "場所", "'[]'", "[1]", "[true]", "[null]", "[{}]"):
            with self.subTest(value=value):
                validate.errors.clear()
                self.write("words/土地.md", WORD_HEADER + f"\nquiz_exclusions: {value}", WORD_BODY)
                self.check_card(self.word_path)
                self.assert_error("'quiz_exclusions'")

    def test_word_quiz_exclusions_reject_duplicate_and_shadowed_declarations(self):
        for extra in ("\nquiz_exclusions: []\nquiz_exclusions: []",
                      "\nquiz_exclusions: null\nquiz_exclusions: []",
                      "\nquiz_exclusions: []\nnote: |\n  quiz_exclusions: []",
                      "\n'quiz_exclusions': []", '\n"quiz_exclusions": []',
                      "\nquiz_exclusions: [] # comment", "\nquiz_exclusions:\n  - 場所"):
            with self.subTest(extra=extra):
                validate.errors.clear()
                self.write("words/土地.md", WORD_HEADER + extra, WORD_BODY)
                validate.parse(self.word_path)
                self.assert_error("'quiz_exclusions' must be a single top-level")
        for indent in (" ", "\t", "\u00a0", "\u2003"):
            with self.subTest(indent=repr(indent)):
                validate.errors.clear()
                self.write("words/土地.md", WORD_HEADER + f"\n{indent}quiz_exclusions: []", WORD_BODY)
                validate.parse(self.word_path)
                self.assert_error("'quiz_exclusions' must be a single top-level")

    def test_word_quiz_exclusions_reject_duplicate_self_and_unknown_ids(self):
        (self.root / "words" / "場所.md").touch()
        original, _ = validate.parse(self.word_path)
        for choices, message in (
                (["場所", "場所"], "must not contain repeated entries"),
                (["土地"], "must not include the word itself"),
                (["不明"], "has no word article with that exact ID"),
                ([""], "has no word article with that exact ID"),
                (["場所 "], "has no word article with that exact ID"),
                (["../words/場所"], "has no word article with that exact ID"),
                (["..\\words\\場所"], "has no word article with that exact ID")):
            with self.subTest(choices=choices):
                validate.errors.clear()
                validate.check_word(self.word_path, dict(original, quiz_exclusions=choices))
                self.assert_error(message)
        validate.errors.clear()
        validate.check_word(self.word_path, dict(original, quiz_exclusions=["場所"]), set())
        self.assert_error("has no word article with that exact ID")

    def test_word_quiz_exclusions_ignore_comments_and_unrelated_scalar_text(self):
        for extra in ("\n# quiz_exclusions: [不明]\nquiz_exclusions: []",
                      "\n  # quiz_exclusions: [不明]\nquiz_exclusions: []",
                      "\nnote: 'quiz_exclusions: [不明]'\nquiz_exclusions: []"):
            with self.subTest(extra=extra):
                self.write("words/土地.md", WORD_HEADER + extra, WORD_BODY)
                self.check_card(self.word_path)
                self.assertEqual([], validate.errors)

    def test_word_quiz_exclusion_rule_does_not_change_legacy_kanji_behavior(self):
        self.write("kanji/日.md", KANJI_HEADER + "\nquiz_exclusions: []\nquiz_exclusions: []", KANJI_BODY)
        self.check_card(self.kanji_path)
        self.assertEqual([], validate.errors)

    def test_word_keys_reject_encoded_tagged_and_anchored_duplicate_exclusions(self):
        for key in (r'"\u0071uiz_exclusions"', r'"\x71uiz_exclusions"',
                    r'"\U00000071uiz_exclusions"', "!!str quiz_exclusions",
                    "!<tag:yaml.org,2002:str> quiz_exclusions", "&key quiz_exclusions"):
            with self.subTest(key=key):
                validate.errors.clear()
                self.write("words/土地.md", WORD_HEADER + f"\n{key}: [場所]\nquiz_exclusions: []", WORD_BODY)
                self.check_card(self.word_path)
                self.assert_error("word front matter keys must be unquoted")

    def test_word_key_rule_covers_encoded_levels_and_other_keys(self):
        for extra in (r'"\u006alpt": 4' + "\njlpt: 5",
                      "!!str jlpt: 4\njlpt: 5",
                      r'"\u0074itle": hidden' + "\ntitle: land; plot",
                      "!!str title: hidden\ntitle: land; plot"):
            with self.subTest(extra=extra):
                validate.errors.clear()
                self.write("words/土地.md", WORD_HEADER + "\n" + extra, WORD_BODY)
                self.check_card(self.word_path)
                self.assert_error("word front matter keys must be unquoted")

    def test_word_plain_keys_allow_comments_values_and_space_before_colon(self):
        for extra in ("\n# !!str quiz_exclusions: [場所]\nquiz_exclusions: []",
                      "\nnote: '!!str quiz_exclusions: [場所]'",
                      "\nnote: " + r"""'"\u0071uiz_exclusions": [場所]'""",
                      "\n_note-2 : ordinary value"):
            with self.subTest(extra=extra):
                self.write("words/土地.md", WORD_HEADER.replace("title:", "title :") + extra, WORD_BODY)
                self.check_card(self.word_path)
                self.assertEqual([], validate.errors)

    def test_word_plain_key_rule_preserves_legacy_kanji_parsing(self):
        self.write("kanji/日.md", KANJI_HEADER + "\n" + r'"\u006alpt": 4' + "\njlpt: 5", KANJI_BODY)
        self.check_card(self.kanji_path)
        self.assertEqual([], validate.errors)

    def test_word_closing_marker_prefix_cannot_hide_declarations(self):
        for marker in ("---not-a-delimiter: ignored", "---: ignored", "----: ignored",
                       "--- notes: ignored", "---#not-separated: ignored"):
            with self.subTest(marker=marker):
                validate.errors.clear()
                header = WORD_HEADER + "\n" + marker + "\n" + r'"\u0071uiz_exclusions": [場所]'
                self.write("words/土地.md", header + "\nquiz_exclusions: []", WORD_BODY)
                self.check_card(self.word_path)
                self.assert_error("word front matter must end with a standalone '---' delimiter")

    def test_word_closing_marker_allows_whitespace_and_separated_comments(self):
        for closing in ("---", "--- \t", "--- # closing comment", "---\u00a0# closing comment"):
            with self.subTest(closing=closing):
                text = f"---\n{WORD_HEADER}\nquiz_exclusions: []\n{closing}\n{WORD_BODY}"
                self.word_path.write_text(text, encoding="utf-8")
                self.check_card(self.word_path)
                self.assertEqual([], validate.errors)

    def test_word_closing_rule_preserves_legacy_kanji_parsing(self):
        self.write("kanji/日.md", KANJI_HEADER + "\n---not-a-delimiter: ignored", KANJI_BODY)
        meta, _ = validate.parse(self.kanji_path)
        self.assertEqual("日", meta["kanji"])
        self.assertEqual([], validate.errors)

    def test_word_kanji_includes_uncatalogued_and_supplementary_han(self):
        for word, reading, characters, missing in (
                ("土地", "とち", ["土", "地"], "地"),
                ("安心", "あんしん", ["安", "心"], "心"),
                ("土曜日", "どようび", ["土", "曜", "日"], "曜"),
                ("金曜日", "きんようび", ["金", "曜", "日"], "曜"),
                ("𠮷ヶ丘", "よしがおか", ["𠮷", "丘"], "𠮷"),
                ("﨑", "さき", ["﨑"], "﨑"),
                ("〇", "まる", ["〇"], "〇")):
            with self.subTest(word=word):
                validate.errors.clear()
                path = self.root / "words" / f"{word}.md"
                meta = {"word": word, "reading": reading, "title": "gloss", "type": "wago",
                        "kanji": characters[:], "tags": []}
                validate.check_word(path, meta)
                self.assertEqual([], validate.errors)
                meta["kanji"].remove(missing)
                validate.check_word(path, meta)
                self.assert_error("missing written Han characters: " + missing)

    def test_word_kana_okurigana_and_iteration_marks_are_not_missing_kanji(self):
        for word, reading, characters in (("休む", "やすむ", ["休"]), ("時々", "ときどき", ["時"]),
                                          ("ヶ", "け", []), ("カレー", "カレー", [])):
            with self.subTest(word=word):
                meta = {"word": word, "reading": reading, "title": "gloss", "type": "wago",
                        "kanji": characters, "tags": []}
                validate.check_word(self.root / "words" / f"{word}.md", meta)
        self.assertEqual([], validate.errors)

    def test_word_kanji_entries_must_be_characters_in_the_word(self):
        meta, _ = validate.parse(self.word_path)
        for extra, message in (("土地", "single character"), ("日", "does not occur")):
            with self.subTest(extra=extra):
                validate.errors.clear()
                meta["kanji"] = ["土", "地", extra]
                validate.check_word(self.word_path, meta)
                self.assert_error(message)

    def test_distractors_need_two_distinct_existing_nonself_cards(self):
        original, _ = validate.parse(self.kanji_path)
        for choices in (None, [], ["月"], ["月", "月"], ["日", "月"], ["月", "地"], ["月", "../kanji/口"]):
            with self.subTest(choices=choices):
                validate.errors.clear()
                meta = copy.deepcopy(original)
                if choices is None:
                    del meta["distractors"]
                else:
                    meta["distractors"] = choices
                validate.check_kanji(self.kanji_path, meta, {})
                self.assert_error("at least 2 distinct existing nonself")
        validate.errors.clear()
        original["distractors"] = ["月", "口", "日"]
        validate.check_kanji(self.kanji_path, original, {})
        self.assert_error("must not include the card itself")

    def test_duplicate_distractors_are_rejected_with_two_valid_alternatives(self):
        for choices in ("[月, 口, 口]", "[月, 口, 月]"):
            with self.subTest(choices=choices):
                validate.errors.clear()
                header = KANJI_HEADER.replace("distractors: [月, 口]", f"distractors: {choices}")
                self.write("kanji/日.md", header, KANJI_BODY)
                self.check_card(self.kanji_path)
                self.assert_error("'distractors' must not contain repeated entries")
                self.assertEqual(1, len(validate.errors))

    def test_jlpt_tags_and_radical_number(self):
        original, _ = validate.parse(self.kanji_path)
        for tags in ([], ["starter"], ["jlpt-n4"], ["jlpt-n5", "jlpt-n4"]):
            with self.subTest(tags=tags):
                validate.errors.clear()
                meta = dict(original, tags=tags)
                validate.check_kanji(self.kanji_path, meta, {})
                self.assert_error("'tags' must include 'jlpt-n5'")
        for number in (0, 215, -1):
            with self.subTest(radicalNumber=number):
                validate.errors.clear()
                validate.check_kanji(self.kanji_path, dict(original, radicalNumber=number), {})
                self.assert_error("'radicalNumber' must be 1-214")
        for number in (1, 214):
            validate.errors.clear()
            validate.check_kanji(self.kanji_path, dict(original, radicalNumber=number), {})
            self.assertEqual([], validate.errors)

    def test_required_body_sections_presence_order_and_duplicates(self):
        for path, body, sections in (
                (self.kanji_path, KANJI_BODY, validate.KANJI_SECTIONS),
                (self.word_path, WORD_BODY, validate.WORD_SECTIONS)):
            meta, _ = validate.parse(path)
            first, second = (f"## {section}" for section in sections[:2])
            for invalid in (body.replace(first, "## Other"),
                            body.replace(first, "PLACEHOLDER").replace(second, first).replace("PLACEHOLDER", second),
                            body + "\n" + first):
                with self.subTest(folder=path.parent.name, body=invalid):
                    validate.errors.clear()
                    validate.check_body(path, meta, invalid)
                    self.assert_error("sections once each, in order")
            validate.errors.clear()
            fenced = body + f"\n```markdown\n{first}\n```\n~~~markdown\n{second}\n~~~\n"
            validate.check_body(path, meta, fenced)
            self.assertEqual([], validate.errors)

    def test_kanji_h1_matches_metadata(self):
        meta, _ = validate.parse(self.kanji_path)
        for heading in ("# 日 — wrong title", "# 月 — sun, day", "## 日 — sun, day"):
            with self.subTest(heading=heading):
                validate.errors.clear()
                validate.check_body(self.kanji_path, meta, KANJI_BODY.replace("# 日 — sun, day", heading))
                self.assert_error("single H1 matching metadata")

    def test_kanji_facts_line_is_before_sections(self):
        meta, _ = validate.parse(self.kanji_path)
        facts = next(line for line in KANJI_BODY.splitlines() if line.startswith("**Strokes:"))
        for body in (KANJI_BODY.replace(facts, ""), KANJI_BODY.replace(facts, "") + facts,
                     KANJI_BODY.replace("**Phonetic:** none · ", "")):
            with self.subTest(body=body):
                validate.errors.clear()
                validate.check_body(self.kanji_path, meta, body)
                self.assert_error("needs a facts line")

    def test_existing_link_and_stroke_checks_still_report_errors(self):
        validate.check_links(self.word_path, "[missing](missing.md)")
        self.assert_error("broken link")
        meta, _ = validate.parse(self.kanji_path)
        validate.check_kanji(self.kanji_path, dict(meta, strokes=5), {})
        self.assert_error("strokes count 5 does not match")

    def test_minimal_strokes_need_only_two_points_and_no_optional_type(self):
        self.assertEqual(4, validate.check_strokes(self.stroke_path))
        self.assertEqual([], validate.errors)
        data = copy.deepcopy(self.stroke_data)
        data["source"] = "ignored provenance"
        data["viewBox"] = []
        for stroke in data["strokes"]:
            stroke["id"] = -1
            stroke["points"] = [[-1, 0.5], [2, 3]]
        self.write_strokes(data)
        self.assertEqual(4, validate.check_strokes(self.stroke_path))
        self.assertEqual([], validate.errors)
        data["strokeCount"] = 0
        data["strokes"] = []
        self.write_strokes(data)
        self.assertEqual(0, validate.check_strokes(self.stroke_path))
        self.assertEqual([], validate.errors)

    def test_order_variants_accept_empty_and_nondefault_permutations(self):
        for variants in ([], [[1, 3, 2, 4]], [[4, 3, 2, 1], [2, 1, 3, 4]]):
            with self.subTest(variants=variants):
                self.write_strokes(dict(self.stroke_data, orderVariants=variants))
                self.check_card(self.kanji_path)
                self.assertEqual([], validate.errors)

    def test_order_variants_require_nested_integer_permutations(self):
        cases = [None, {}, "orders", 1, True]
        for order in (None, {}, "1324", 1, True, [], [1, 3, 2], [1, 3, 2, 4, 5],
                      [1, 2, 3, 4], [1, 3, 2, 2], [0, 3, 2, 4], [1, 3, 2, 5],
                      [1, "3", 2, 4], [True, 3, 2, 4], [1.0, 3, 2, 4],
                      [1, None, 2, 4], [1, {}, 2, 4], [1, [3], 2, 4],
                      [1, 2**31, 2, 4]):
            cases.append([order])
        for variants in cases:
            with self.subTest(variants=variants):
                validate.errors.clear()
                self.write_strokes(dict(self.stroke_data, orderVariants=variants))
                self.assertEqual(4, validate.check_strokes(self.stroke_path))
                self.assert_error("orderVariants")
                self.assertEqual(1, len(validate.errors))

    def test_order_variants_do_not_allocate_from_invalid_declared_count(self):
        for count in (3, 2**31 - 1, None, "4"):
            with self.subTest(count=count):
                validate.errors.clear()
                self.write_strokes(dict(self.stroke_data, strokeCount=count,
                                        orderVariants=[[1, 3, 2, 4]]))
                validate.check_strokes(self.stroke_path)
                self.assert_error("'strokeCount'")
                self.assertEqual(1, len(validate.errors))

    def test_main_reports_invalid_order_variants(self):
        self.write_strokes(dict(self.stroke_data, orderVariants=[[1, 2, 3, 4]]))
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(1, validate.main())
        self.assertIn("strokes/日.json: orderVariants[0]", output.getvalue())

    def test_copied_strokes_with_matching_counts_have_wrong_identity(self):
        other = self.root / "strokes" / "月.json"
        other.write_text(json.dumps(dict(self.stroke_data, kanji="月")), encoding="utf-8")
        self.stroke_path.write_bytes(other.read_bytes())
        self.check_card(self.kanji_path)
        self.assert_error("strokes/日.json: 'kanji' must match the strokes file name '日'")
        self.assertEqual(1, len(validate.errors))

    def test_strokes_require_importer_fields(self):
        for key in ("schemaVersion", "kanji", "viewBox", "strokeCount", "strokes"):
            with self.subTest(key=key):
                validate.errors.clear()
                data = copy.deepcopy(self.stroke_data)
                del data[key]
                self.write_strokes(data)
                validate.check_strokes(self.stroke_path)
                self.assert_error(f"'{key}'")

    def test_strokes_schema_numeric_types_and_counts(self):
        cases = {
            "schemaVersion": (0, 2, True, 1.0, "1", None),
            "kanji": (True, ["日"], None),
            "viewBox": (None, {}, "0 0 109 109", [False], [float("nan")],
                        [float("inf")], [10**400], ["0"]),
            "strokeCount": (True, False, 4.0, "4", None, 2**31, -2**31 - 1, 3),
            "strokes": (None, {}, "strokes", []),
        }
        for key, values in cases.items():
            for value in values:
                with self.subTest(key=key, value=value):
                    validate.errors.clear()
                    data = copy.deepcopy(self.stroke_data)
                    data[key] = value
                    self.write_strokes(data)
                    validate.check_strokes(self.stroke_path)
                    self.assertTrue(validate.errors)
                    self.assertTrue(all(error.startswith("strokes/日.json:") for error in validate.errors))

    def test_stroke_entries_ids_types_and_finite_two_dimensional_points(self):
        bad_strokes = [None, [], {}, "stroke",
                       {"id": False, "points": [[0, 0], [1, 1]]},
                       {"id": 1.0, "points": [[0, 0], [1, 1]]},
                       {"id": 2**31, "points": [[0, 0], [1, 1]]},
                       {"id": 1, "type": None, "points": [[0, 0], [1, 1]]},
                       {"id": 1, "type": False, "points": [[0, 0], [1, 1]]}]
        for points in (None, [], [[0, 0]], [[0], [1, 2]], [[0, 0, 0], [1, 2]],
                       [0, 1], ["xy", "xy"], [[False, 0], [1, 2]], [["0", 0], [1, 2]],
                       [[float("nan"), 0], [1, 2]], [[float("-inf"), 0], [1, 2]],
                       [[10**400, 0], [1, 2]]):
            bad_strokes.append({"id": 1, "points": points})
        for stroke in bad_strokes:
            with self.subTest(stroke=stroke):
                validate.errors.clear()
                data = copy.deepcopy(self.stroke_data)
                data["strokes"][0] = stroke
                self.write_strokes(data)
                validate.check_strokes(self.stroke_path)
                self.assert_error("strokes[0]")

    def test_malformed_or_non_object_strokes_json_is_an_error(self):
        for text in ("", "{", "[]", "null", "4", "true"):
            with self.subTest(text=text):
                validate.errors.clear()
                self.stroke_path.write_bytes(text.encode("utf-8"))
                self.assertIsNone(validate.check_strokes(self.stroke_path))
                self.assert_error("strokes JSON")

    def test_imported_pages_reject_existing_non_imported_link_targets(self):
        (self.root / "docs").mkdir()
        (self.root / "docs" / "jlpt-levels.md").touch()
        (self.root / "README.md").touch()
        (self.root / "strokes" / "source.md").touch()
        (self.root / "kanji" / "nested").mkdir()
        (self.root / "kanji" / "nested" / "note.md").touch()
        for folder in ("kanji", "words", "articles"):
            for target in ("../docs/jlpt-levels.md", "../docs/%6Alpt-levels.md#policy",
                           "../kanji/../docs/jlpt-levels.md", "../README.md",
                           "../strokes/source.md", "../kanji/nested/note.md"):
                with self.subTest(folder=folder, target=target):
                    validate.errors.clear()
                    validate.check_links(self.root / folder / "page.md", f"[source]({target})")
                    self.assert_error("relative link targets non-imported content")
                    self.assertEqual(1, len(validate.errors))

    def test_imported_pages_allow_navigation_https_and_fragments(self):
        article = self.root / "articles" / "navigation.md"
        article.touch()
        for source in (self.kanji_path, self.word_path, article):
            for destination in (self.kanji_path, self.word_path, article):
                with self.subTest(source=source.name, destination=destination.name):
                    target = "../" + destination.relative_to(self.root).as_posix() + "#meaning"
                    validate.check_links(source, f"[page]({target})")
                    self.assertEqual([], validate.errors)
            validate.check_links(source, "[encoded](../kanji/%E6%97%A5.md) "
                                 "[source](https://example.org/docs/jlpt-levels.md) [section](#meaning)")
        self.assertEqual([], validate.errors)

    def test_docs_can_link_to_other_docs_normally(self):
        docs = self.root / "docs"
        docs.mkdir()
        (docs / "jlpt-levels.md").touch()
        validate.check_links(docs / "content-format.md", "[policy](jlpt-levels.md#sources)")
        self.assertEqual([], validate.errors)

    def test_cli_reports_invalid_metadata_without_traceback(self):
        for path in (self.root / "kanji").glob("*.md"):
            path.unlink()
        self.write("words/土地.md", "false", WORD_BODY)
        output = io.StringIO()
        with redirect_stdout(output):
            result = validate.main()
        self.assertEqual(1, result)
        self.assertIn("front matter must be a mapping", output.getvalue())
        self.assertIn("1 error(s)", output.getvalue())

    def test_cli_reports_utf8_errors_for_each_file_and_continues(self):
        for char in ("月", "口"):
            (self.root / "kanji" / f"{char}.md").unlink()
        paths = (self.kanji_path, self.word_path, self.stroke_path,
                 self.root / "articles" / "bad.md")
        for path in paths:
            path.write_bytes(b"\xff")
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(1, validate.main())
        self.assertEqual(4, len(validate.errors))
        for path in paths:
            self.assert_error(f"{path.relative_to(self.root).as_posix()}: not valid UTF-8")
        self.assertIn("4 error(s)", output.getvalue())
        self.assertNotIn("Traceback", output.getvalue())

    def test_cli_reports_deep_yaml_and_json_without_tracebacks(self):
        for char in ("月", "口"):
            (self.root / "kanji" / f"{char}.md").unlink()
        depth = sys.getrecursionlimit() + 100
        nested = "[" * depth + "0" + "]" * depth
        self.write("kanji/日.md", KANJI_HEADER + "\nnested: " + nested, KANJI_BODY)
        self.write("articles/deep.md", "nested: " + nested, "# Deep\n")
        output = io.StringIO()
        # The C JSON decoder's nesting threshold differs across platforms.
        with patch.object(validate.json, "loads", side_effect=RecursionError), redirect_stdout(output):
            self.assertEqual(1, validate.main())
        self.assertEqual(3, len(validate.errors))
        self.assert_error("kanji/日.md: front matter YAML nesting is too deep")
        self.assert_error("articles/deep.md: front matter YAML nesting is too deep")
        self.assert_error("strokes/日.json: strokes JSON nesting is too deep")
        self.assertNotIn("Traceback", output.getvalue())

    def test_valid_current_files(self):
        with patch.object(validate, "ROOT", REPO):
            for folder, names in (("kanji", ("日", "休")), ("words", ("休む", "休日"))):
                for name in names:
                    with self.subTest(folder=folder, name=name):
                        self.check_card(REPO / folder / f"{name}.md")
        self.assertEqual([], validate.errors)


if __name__ == "__main__":
    unittest.main()

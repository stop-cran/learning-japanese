import unittest

from audit_n1_pilot import offered_keys, quiz_readings, reading_key, reconciled_baseline_manifest


class N1PilotReadingProjectionTest(unittest.TestCase):
    def test_folds_katakana_and_removes_separators(self):
        self.assertEqual(reading_key(" -カン・. \t"), "かん")

    def test_takes_first_three_distinct_stems_in_source_order(self):
        self.assertEqual(offered_keys(["スイ", "エ", "ケイ", "セイ"]), ["すい", "え", "けい"])

    def test_preserves_first_okurigana_variant_not_preferred_modern_verb(self):
        self.assertEqual(offered_keys(["あつか.い", "あつか.う", "あつか.る", "こ.く"]),
                         ["あつかい", "こく"])

    def test_deduplicates_affix_stem_and_ignores_empty_keys(self):
        self.assertEqual(offered_keys(["", "-・ ", "うじ", "-うじ"]), ["うじ"])

    def test_omission_preserves_legacy_full_list(self):
        self.assertEqual(quiz_readings({"onyomi": ["ソウ", "キュウ"]}, "onyomi"),
                         ["ソウ", "キュウ"])

    def test_explicit_empty_disables_kind(self):
        self.assertEqual(quiz_readings({"onyomi": ["ソウ", "キュウ"], "quizOnyomi": []},
                                      "onyomi"), [])

    def test_curated_verb_replaces_first_source_stem_without_changing_full_list(self):
        full = ["あつか.い", "あつか.う", "あつか.る", "こ.く"]
        meta = {"kunyomi": full, "quizKunyomi": ["あつか.う"]}
        self.assertEqual(offered_keys(quiz_readings(meta, "kunyomi")), ["あつかう"])
        self.assertEqual(meta["kunyomi"], full)

    def test_rejects_normalized_instead_of_exact_raw_reading(self):
        with self.assertRaisesRegex(ValueError, "exact distinct source subset"):
            quiz_readings({"kunyomi": ["あつか.う"], "quizKunyomi": ["あつかう"]}, "kunyomi")

    def test_rejects_duplicate_or_malformed_selections(self):
        for selected in (["カン", "カン"], ["カン", ""], "カン", None, [1]):
            with self.subTest(selected=selected), self.assertRaises(ValueError):
                quiz_readings({"onyomi": ["カン"], "quizOnyomi": selected}, "onyomi")


class N1IntegratedMainManifestTest(unittest.TestCase):
    def setUp(self):
        self.before = {"images": {"images/a.webp": "a" * 64},
                       "scenes": {"scenes/a.json": "b" * 64}}
        self.after = {"images": {}, "scenes": {"scenes/a.json": "c" * 64}}
        self.changes = [
            {"section": "images", "path": "images/a.webp", "before": "a" * 64,
             "after": None, "sourceCommit": "d" * 40},
            {"section": "scenes", "path": "scenes/a.json", "before": "b" * 64,
             "after": "c" * 64, "sourceCommit": "d" * 40},
        ]

    def test_exact_main_removal_and_scene_change_preserve_frozen_baseline(self):
        self.assertEqual(reconciled_baseline_manifest(self.before, self.after, self.changes),
                         self.after)
        self.assertEqual(self.before["images"]["images/a.webp"], "a" * 64)
        self.assertEqual(reconciled_baseline_manifest(self.before, self.after, []), self.before)

    def test_rejects_wrong_before_after_duplicate_or_unpinned_provenance(self):
        for field, value in (("before", "e" * 64), ("after", "e" * 64),
                             ("sourceCommit", "main")):
            rows = [{**self.changes[0], field: value}]
            with self.subTest(field=field), self.assertRaises(ValueError):
                reconciled_baseline_manifest(self.before, self.after, rows)
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            reconciled_baseline_manifest(self.before, self.after,
                                         [self.changes[0], self.changes[0]])

    def test_cannot_override_kanji_or_word_baseline(self):
        for section in ("files", "words", "kanji"):
            row = {**self.changes[0], "section": section, "path": f"{section}/a.md"}
            with self.subTest(section=section), self.assertRaisesRegex(ValueError, "image or scene"):
                reconciled_baseline_manifest(self.before, self.after, [row])


if __name__ == "__main__":
    unittest.main()

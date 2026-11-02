import unittest

from audit_n1_pilot import offered_keys, quiz_readings, reading_key


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


if __name__ == "__main__":
    unittest.main()

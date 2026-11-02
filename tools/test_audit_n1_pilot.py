import unittest

from audit_n1_pilot import offered_keys, reading_key


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


if __name__ == "__main__":
    unittest.main()

import unittest
import xml.etree.ElementTree as ET

from audit_n1_batch import lexical_pair, runtime_delta


class N1BatchRuntimeDeltaTest(unittest.TestCase):
    def setUp(self):
        self.before = {"contentVersion": "old", "files": {"words/a.md": "a"},
                       "images": {"images/a.webp": "b"}}
        self.after = {"contentVersion": "new",
                      "files": {"words/a.md": "c", "kanji/x.md": "d"},
                      "images": {"images/a.webp": "b"}}

    def test_exact_additions_and_recorded_reused_change(self):
        runtime_delta(self.before, self.after, {"kanji/x.md"}, {"words/a.md"})

    def test_rejects_unaccounted_addition(self):
        with self.assertRaisesRegex(ValueError, "additions differ"):
            runtime_delta(self.before, self.after, set(), {"words/a.md"})

    def test_rejects_removed_baseline(self):
        self.after["images"].clear()
        with self.assertRaisesRegex(ValueError, "removed"):
            runtime_delta(self.before, self.after, {"kanji/x.md"}, {"words/a.md"})

    def test_rejects_unrecorded_baseline_change(self):
        with self.assertRaisesRegex(ValueError, "Changed baseline"):
            runtime_delta(self.before, self.after, {"kanji/x.md"}, set())

    def test_cannot_allow_image_changes_as_reused_word_passage(self):
        self.after["images"]["images/a.webp"] = "changed"
        with self.assertRaisesRegex(ValueError, "Changed baseline"):
            runtime_delta(self.before, self.after, {"kanji/x.md"},
                          {"words/a.md", "images/a.webp"})

    def test_rejects_missing_recorded_change(self):
        self.after["files"]["words/a.md"] = "a"
        with self.assertRaisesRegex(ValueError, "Changed baseline"):
            runtime_delta(self.before, self.after, {"kanji/x.md"}, {"words/a.md"})


class N1BatchLexicalPairTest(unittest.TestCase):
    def setUp(self):
        self.entry = ET.fromstring("""<entry>
<k_ele><keb>A</keb></k_ele><k_ele><keb>B</keb></k_ele>
<r_ele><reb>a</reb><re_restr>A</re_restr></r_ele>
<r_ele><reb>b</reb></r_ele>
<r_ele><reb>katakana</reb><re_nokanji/></r_ele>
</entry>""")

    def test_accepts_exact_spelling_and_applicable_reading(self):
        self.assertTrue(lexical_pair(self.entry, "A", "a"))
        self.assertTrue(lexical_pair(self.entry, "A", "b"))
        self.assertTrue(lexical_pair(self.entry, "B", "b"))

    def test_rejects_restricted_reading_for_other_spelling(self):
        self.assertFalse(lexical_pair(self.entry, "B", "a"))

    def test_rejects_no_kanji_reading(self):
        self.assertFalse(lexical_pair(self.entry, "A", "katakana"))

    def test_rejects_absent_spelling_or_reading(self):
        self.assertFalse(lexical_pair(self.entry, "C", "b"))
        self.assertFalse(lexical_pair(self.entry, "A", "c"))


if __name__ == "__main__":
    unittest.main()

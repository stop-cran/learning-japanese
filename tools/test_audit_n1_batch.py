import unittest
import xml.etree.ElementTree as ET

from audit_n1_batch import lexical_pair, reused_changes, runtime_delta


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


class N1BatchReusedChangesTest(unittest.TestCase):
    def setUp(self):
        self.old = "---\nword: A\nreading: a\nquiz_exclusions: [B]\n---\nA is a noun.\n"
        self.rows = [{"before": "A is a noun.", "after": "[A](../kanji/A.md) is a noun."}]
        self.new = self.old.replace("A is a noun.", self.rows[0]["after"])

    def test_accepts_legacy_link_only_edit(self):
        reused_changes(self.old, self.new, self.rows)

    def test_accepts_multiple_exact_edits_and_additive_exclusions(self):
        self.rows.append({"before": "quiz_exclusions: [B]", "after": "quiz_exclusions: [B, C]"})
        reused_changes(self.old, self.new.replace("[B]", "[B, C]"), self.rows, ["B", "C"])

    def test_accepts_first_recorded_exclusion(self):
        old = self.old.replace("quiz_exclusions: [B]\n", "")
        new = old.replace("reading: a\n", "reading: a\nquiz_exclusions: [C]\n")
        reused_changes(old, new, [{"before": "reading: a\n",
                                  "after": "reading: a\nquiz_exclusions: [C]\n"}], ["C"])

    def test_rejects_unrecorded_metadata_change(self):
        rows = [{"before": "reading: a", "after": "reading: b"}]
        with self.assertRaisesRegex(ValueError, "metadata changed"):
            reused_changes(self.old, self.old.replace("reading: a", "reading: b"), rows)

    def test_rejects_removed_original_exclusion(self):
        rows = [{"before": "[B]", "after": "[C]"}]
        with self.assertRaisesRegex(ValueError, "additive safeguards"):
            reused_changes(self.old, self.old.replace("[B]", "[C]"), rows, ["C"])

    def test_rejects_duplicate_exclusion(self):
        with self.assertRaisesRegex(ValueError, "additive safeguards"):
            reused_changes(self.old, self.new, self.rows, ["B", "B"])

    def test_rejects_unrecorded_prose(self):
        with self.assertRaisesRegex(ValueError, "exact edits"):
            reused_changes(self.old, self.new + "Extra prose.\n", self.rows)

    def test_rejects_ambiguous_replacement(self):
        with self.assertRaisesRegex(ValueError, "exactly once"):
            reused_changes(self.old + "A is a noun.\n", self.new, self.rows)


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

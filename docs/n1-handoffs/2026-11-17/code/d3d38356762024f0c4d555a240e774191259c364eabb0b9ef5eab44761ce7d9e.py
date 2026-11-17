import copy
import unittest

from prepare_b133_source_facts_v2 import (
    additional_scope, union_selection, verify_plain_spelling_membership, verify_query_counts)
from test_prepare_b133_source_facts import B133SourcePredicateTests


class B133AdditionalSourceTests(unittest.TestCase):
    def test_exact_selectors_include_all_linked_words_and_only_baseline_comparisons(self):
        chars = "ABCDEF"
        documents = {f"additional/comparison-cards/{char}.md":
                     f"[word](../words/word{char}.md)\n".encode() for char in chars}
        exact = set(chars) | {"word" + char for char in chars}
        receipt = {"allExactSpellings": sorted(exact)}
        self.assertEqual(additional_scope(documents.__getitem__, receipt, chars, set(chars)), exact)
        for altered in ({"allExactSpellings": sorted(exact - {"wordF"})},
                        {"allExactSpellings": sorted(exact | {"unrequested"})},
                        {"allExactSpellings": sorted(exact) + ["wordF"]}):
            with self.subTest(receipt=altered), self.assertRaises(ValueError):
                additional_scope(documents.__getitem__, altered, chars, set(chars))
        with self.assertRaises(ValueError):
            additional_scope(documents.__getitem__, receipt, chars, set("ABCDE"))
        with self.assertRaises(ValueError):
            additional_scope(documents.__getitem__, receipt, "ABCDEE", set(chars))

    def test_plain_membership_retains_complete_overlaps_and_absences(self):
        raw = (b"<JMdict><entry><ent_seq>1</ent_seq><k_ele><keb>A</keb></k_ele>"
               b"<k_ele><keb>B</keb></k_ele></entry></JMdict>")
        selected = union_selection("additional/test.xml", spellings=["A", "B", "missing"])
        membership = {"1": ["A", "B"]}
        counts = {"A": 1, "B": 1, "missing": 0}
        verify_plain_spelling_membership(raw, membership, selected)
        verify_query_counts(membership, ["A", "B", "missing"], counts)
        for altered in ({"1": ["A"]}, {"1": ["A", "A", "B"]}, {"1": ["A", "B"], "2": ["B"]}):
            with self.subTest(membership=altered), self.assertRaises(ValueError):
                verify_plain_spelling_membership(raw, altered, selected)
        for change in ("missing", "false-positive", "boolean"):
            altered = copy.deepcopy(counts)
            if change == "missing":
                del altered["missing"]
            else:
                altered["missing"] = 1 if change == "false-positive" else False
            with self.subTest(change=change), self.assertRaises(ValueError):
                verify_query_counts(membership, ["A", "B", "missing"], altered)


if __name__ == "__main__":
    unittest.main()

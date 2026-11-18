import unittest

from prepare_b132_source_facts import (
    union_selection, verify_plain_spelling_membership, verify_query_counts)


class B132SourcePredicateTests(unittest.TestCase):
    def test_absent_queries_remain_in_receipt_counts(self):
        membership = {"1": ["A"], "2": ["A", "B"]}
        verify_query_counts(membership, ["A", "B", "absent"], {"A": 2, "B": 1, "absent": 0})
        for counts in ({"A": 2, "B": 1}, {"A": 2, "B": 0, "absent": 0},
                       {"A": 2, "B": True, "absent": 0}, {"A": 2, "B": 1, "absent": 0, "extra": 0}):
            with self.subTest(counts=counts), self.assertRaises(ValueError):
                verify_query_counts(membership, ["A", "B", "absent"], counts)

    def test_supplemental_plain_spellings_keep_every_matching_predicate(self):
        raw = b"""<JMdict><entry><ent_seq>1</ent_seq>
            <k_ele><keb>A</keb></k_ele><k_ele><keb>B</keb></k_ele>
            </entry></JMdict>"""
        selection = union_selection("supplement.xml", spellings=["A", "B", "absent"])
        verify_plain_spelling_membership(raw, {"1": ["A", "B"]}, selection)
        for membership in ({"1": ["A"]}, {"1": ["A", "B", "B"]},
                           {"1": ["A", "B"], "2": ["A"]}, {"1": ["A", "C"]}):
            with self.subTest(membership=membership), self.assertRaises(ValueError):
                verify_plain_spelling_membership(raw, membership, selection)


if __name__ == "__main__":
    unittest.main()

import unittest

from prepare_b130_source_facts import union_selection, verify_query_membership


class MembershipTests(unittest.TestCase):
    def setUp(self):
        self.raw = b"""<JMdict>
          <entry><ent_seq>1</ent_seq><k_ele><keb>prefixX</keb></k_ele>
            <r_ele><reb>Y</reb></r_ele></entry>
          <entry><ent_seq>2</ent_seq><k_ele><keb>Y</keb></k_ele></entry>
        </JMdict>"""
        self.selection = union_selection("fixture.xml", contains=["X"], spellings=["Y"],
                                         readings=["Y", "zero-match"])
        self.membership = {"1": ["contains:X", "exact-reading:Y"], "2": ["exact-spelling:Y"]}

    def test_complete_predicates_keep_zero_match_queries(self):
        verify_query_membership(self.raw, self.membership, self.selection)
        self.assertIn("exact-reb:zero-match", self.selection["queries"])

    def test_rejects_missing_or_mislabelled_predicates(self):
        for predicates in (["contains:X"], ["contains:X", "exact-spelling:Y"],
                           ["contains:X", "exact-reading:Y", "exact-reading:Y"]):
            with self.subTest(predicates=predicates), self.assertRaises(ValueError):
                verify_query_membership(self.raw, {**self.membership, "1": predicates}, self.selection)

    def test_rejects_extra_missing_and_duplicate_families(self):
        for membership in ({"1": self.membership["1"]}, {**self.membership, "3": ["contains:X"]}):
            with self.subTest(membership=membership), self.assertRaises(ValueError):
                verify_query_membership(self.raw, membership, self.selection)
        duplicate = self.raw.replace(b"</JMdict>", b"<entry><ent_seq>1</ent_seq></entry></JMdict>")
        with self.assertRaises(ValueError):
            verify_query_membership(duplicate, self.membership, self.selection)

    def test_contains_spelling_does_not_match_reading(self):
        raw = b"<JMdict><entry><ent_seq>1</ent_seq><r_ele><reb>prefixX</reb></r_ele></entry></JMdict>"
        with self.assertRaises(ValueError):
            verify_query_membership(raw, {"1": ["contains:X"]}, self.selection)


if __name__ == "__main__":
    unittest.main()

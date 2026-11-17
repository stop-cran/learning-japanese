import unittest
import xml.etree.ElementTree as ET

from prepare_b129_review_contract import query_index


class QueryIndexTests(unittest.TestCase):
    def test_mixed_queries_preserve_all_matching_predicates_and_empty_queries(self):
        records = {"2": ET.fromstring("<entry><ent_seq>2</ent_seq><k_ele><keb>AB</keb></k_ele>"
                                     "<r_ele><reb>ab</reb></r_ele></entry>"),
                   "10": ET.fromstring("<entry><ent_seq>10</ent_seq><k_ele><keb>A</keb></k_ele></entry>")}
        selections = [{"mode": "union", "queries": ["contains-keb:A", "exact-reb:ab", "exact-reb:missing"]},
                      {"mode": "exact", "queries": ["AB"]}]
        self.assertEqual(query_index(records, selections), {
            "contains-keb:A": ["2", "10"], "exact-keb:AB": ["2"],
            "exact-reb:ab": ["2"], "exact-reb:missing": []})

    def test_unselected_family_fails_closed(self):
        records = {"1": ET.fromstring("<entry><ent_seq>1</ent_seq><k_ele><keb>A</keb></k_ele></entry>")}
        with self.assertRaisesRegex(ValueError, "omits"):
            query_index(records, [{"mode": "exact", "queries": ["B"]}])


if __name__ == "__main__":
    unittest.main()

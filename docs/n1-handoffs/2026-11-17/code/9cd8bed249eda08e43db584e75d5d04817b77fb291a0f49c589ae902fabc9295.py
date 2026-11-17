import unittest
import xml.etree.ElementTree as ET

from prepare_b129_source_facts import literal_assignment, union_selection
from source_query_union import selects


class SourceFactsTests(unittest.TestCase):
    def test_union_keeps_zero_match_queries_and_distinct_predicates(self):
        selection = union_selection("fixture.xml", contains=["X"], spellings=["Y"],
                                    readings=["Y", "missing"])
        self.assertEqual(selection["queries"],
                         ["contains-keb:X", "exact-keb:Y", "exact-reb:Y", "exact-reb:missing"])
        for body in ("<k_ele><keb>prefixX</keb></k_ele>", "<k_ele><keb>Y</keb></k_ele>",
                     "<r_ele><reb>Y</reb></r_ele>"):
            node = ET.fromstring("<entry>" + body + "</entry>")
            self.assertTrue(selects(node, "entry", "1", selection["mode"], selection["queries"]))
        self.assertFalse(selects(ET.fromstring("<entry><r_ele><reb>prefixX</reb></r_ele></entry>"),
                                 "entry", "1", selection["mode"], selection["queries"]))

    def test_literal_query_recovery_never_executes_producer(self):
        source = b'EXACT = {"present", "zero-match"}\nraise RuntimeError("must not execute")\n'
        self.assertEqual(literal_assignment(source, "EXACT"), {"present", "zero-match"})
        with self.assertRaises(ValueError):
            literal_assignment(b"EXACT = make_queries()", "EXACT")
        with self.assertRaises(ValueError):
            literal_assignment(b"EXACT = {'first'}\nEXACT = {'replacement'}", "EXACT")


if __name__ == "__main__":
    unittest.main()

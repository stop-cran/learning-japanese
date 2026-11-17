import unittest
import xml.etree.ElementTree as ET

from verify_b134_reconciliation import compare_records, records, verify_membership


class ReconciliationSources(unittest.TestCase):
    def test_exact_membership_includes_zero_counts(self):
        counts = {"exact-spelling:x": 1, "exact-reading:y": 0}
        actual = {"1": ["exact-spelling:x"]}
        self.assertEqual(verify_membership(actual, actual, counts, list(counts)), counts)
        with self.assertRaisesRegex(ValueError, "predicate"):
            verify_membership(actual, actual, {"exact-spelling:x": 1}, list(counts))
        with self.assertRaisesRegex(ValueError, "counts"):
            verify_membership(actual, actual, {**counts, "exact-reading:y": 1}, list(counts))

    def test_invented_or_duplicate_membership_rejected(self):
        actual = {"1": ["exact-spelling:x"]}
        counts = {"exact-spelling:x": 1}
        for recorded in ({"2": ["exact-spelling:x"]}, {"1": ["exact-spelling:x"] * 2}):
            with self.assertRaises(ValueError):
                verify_membership(actual, recorded, counts, list(counts))

    def test_complete_records_preserve_qualified_senses(self):
        raw = (b"<JMdict><entry><ent_seq>1</ent_seq><sense><stagk>x</stagk>"
               b"<misc>archaism</misc><gloss>first</gloss><gloss>second</gloss>"
               b"</sense></entry></JMdict>")
        expected = records(raw, "entry", "ent_seq")
        compare_records(expected, records(raw, "entry", "ent_seq"))
        root = ET.fromstring(raw)
        root.find("entry/sense").remove(root.find("entry/sense/misc"))
        with self.assertRaisesRegex(ValueError, "incomplete"):
            compare_records(expected, records(ET.tostring(root), "entry", "ent_seq"))
        with self.assertRaisesRegex(ValueError, "membership"):
            compare_records(expected, {})


if __name__ == "__main__":
    unittest.main()

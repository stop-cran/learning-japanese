import io
import unittest
import xml.etree.ElementTree as ET

from verify_b123_reconciliation_selection import verify_selection
from verify_reconciliation_sources import element_value


class Guard:
    def check(self):
        pass


def entry(identity, spelling, gloss):
    return (f"<entry><ent_seq>{identity}</ent_seq><k_ele><keb>{spelling}</keb></k_ele>"
            f"<sense><misc>usually kana</misc><gloss>{gloss}</gloss></sense></entry>")


def records(*entries):
    return {ET.fromstring(raw).findtext("ent_seq"): element_value(ET.fromstring(raw))
            for raw in entries}


class ExactSelectionTests(unittest.TestCase):
    def test_exact_spelling_or_id_without_substring_or_reading_match(self):
        first, explicit = entry("1", "A", "model"), entry("2", "B", "restricted")
        excluded = entry("3", "AB", "substring")
        reading = "<entry><ent_seq>4</ent_seq><r_ele><reb>A</reb></r_ele></entry>"
        document = f"<JMdict>{first}{explicit}{excluded}{reading}</JMdict>".encode()
        found, hits = verify_selection(io.BytesIO(document), "entry", "ent_seq",
                                       {"A", "unmatched"}, {"2"}, records(first, explicit), Guard())
        self.assertEqual(found, ["1", "2"])
        self.assertEqual(hits, {"A": ["1"], "unmatched": []})

    def test_rejects_missing_extra_altered_and_duplicate_records(self):
        first, second = entry("1", "A", "one"), entry("2", "A", "two")
        document = f"<JMdict>{first}{second}</JMdict>".encode()
        for expected in (records(first), records(first, second, entry("3", "B", "extra")),
                         records(first, entry("2", "A", "changed"))):
            with self.subTest(expected=expected), self.assertRaises(ValueError):
                verify_selection(io.BytesIO(document), "entry", "ent_seq",
                                 {"A"}, set(), expected, Guard())
        with self.assertRaisesRegex(ValueError, "Duplicate input"):
            verify_selection(io.BytesIO(f"<JMdict>{first}{first}</JMdict>".encode()),
                             "entry", "ent_seq", {"A"}, set(), records(first), Guard())
        with self.assertRaisesRegex(ValueError, "Explicit entry ID missing"):
            verify_selection(io.BytesIO(f"<JMdict>{first}</JMdict>".encode()),
                             "entry", "ent_seq", {"A"}, {"999"}, records(first), Guard())

    def test_kanjidic_selects_exact_literal_and_preserves_all_fields(self):
        raw = "<character><literal>A</literal><misc><stroke_count>15</stroke_count></misc></character>"
        other = "<character><literal>AA</literal></character>"
        expected = {"A": element_value(ET.fromstring(raw))}
        found, hits = verify_selection(
            io.BytesIO(f"<kanjidic2>{raw}{other}</kanjidic2>".encode()),
            "character", "literal", {"A"}, set(), expected, Guard())
        self.assertEqual((found, hits), (["A"], {"A": ["A"]}))


if __name__ == "__main__":
    unittest.main()

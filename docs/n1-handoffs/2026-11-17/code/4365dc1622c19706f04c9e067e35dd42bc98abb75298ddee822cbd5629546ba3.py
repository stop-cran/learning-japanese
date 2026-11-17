import io
import unittest

from common import frozen, load_module
from verify_b125_sources import VERIFIER_PATH, VERIFIER_SHA, scan_records


class Guard:
    def check(self):
        pass


class ScanTests(unittest.TestCase):
    def test_all_meaning_groups_and_title_polysemy_are_scanned(self):
        raw = b"""<kanjidic2><character><literal>X</literal><reading_meaning>
        <rmgroup><meaning>unrelated</meaning></rmgroup>
        <rmgroup><meaning>invade</meaning><meaning m_lang="fr">raid</meaning></rmgroup>
        </reading_meaning></character><character><literal>Y</literal></character></kanjidic2>"""
        result = scan_records(io.BytesIO(raw), {"X": "rest", "Y": "raid"}, ["invade", "raid"], Guard())
        self.assertEqual(["invade"], result["matches"]["X"]["meaningHits"])
        self.assertEqual(["raid"], result["matches"]["Y"]["titleHits"])
        self.assertEqual([], result["missingRecords"])

    def test_empty_overlap_keeps_missing_records_explicit(self):
        result = scan_records(io.BytesIO(b"<kanjidic2/>"), {"X": "rest"}, ["invade"], Guard())
        self.assertEqual({}, result["matches"])
        self.assertEqual(["X"], result["missingRecords"])

    def test_duplicate_record_rejected(self):
        raw = b"<kanjidic2><character><literal>X</literal></character><character><literal>X</literal></character></kanjidic2>"
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            scan_records(io.BytesIO(raw), {"X": "rest"}, ["invade"], Guard())


class CompleteRecordTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        frozen(VERIFIER_PATH, VERIFIER_SHA)
        cls.verifier = load_module("tested_b125_source_engine", VERIFIER_PATH)
        cls.verifier.MEMBER = "X"

    def test_complete_record_passes_but_removed_restriction_fails(self):
        raw = b"""<JMdict><entry><ent_seq>1</ent_seq><k_ele><keb>XY</keb></k_ele>
        <r_ele><reb>reading</reb><re_restr>XY</re_restr></r_ele>
        <sense><stagk>XY</stagk><gloss>meaning</gloss></sense></entry></JMdict>"""
        selection = {"name": "test", "mode": "contains-member", "queries": {"X"},
                     "expected": self.verifier.records(raw, "entry", "ent_seq")}
        self.assertEqual([["1"]], self.verifier.verify_stream(
            io.BytesIO(raw), "entry", "ent_seq", [selection], Guard()))
        selection["expected"] = self.verifier.records(
            raw.replace(b"<stagk>XY</stagk>", b""), "entry", "ent_seq")
        with self.assertRaisesRegex(ValueError, "Incomplete or altered"):
            self.verifier.verify_stream(io.BytesIO(raw), "entry", "ent_seq", [selection], Guard())

    def test_omitted_family_is_not_accepted_as_empty_selection(self):
        raw = b"<JMdict><entry><ent_seq>1</ent_seq><k_ele><keb>XY</keb></k_ele></entry></JMdict>"
        selection = {"name": "test", "mode": "contains-member", "queries": {"X"}, "expected": {}}
        with self.assertRaisesRegex(ValueError, "Missing applicable"):
            self.verifier.verify_stream(io.BytesIO(raw), "entry", "ent_seq", [selection], Guard())


if __name__ == "__main__":
    unittest.main()

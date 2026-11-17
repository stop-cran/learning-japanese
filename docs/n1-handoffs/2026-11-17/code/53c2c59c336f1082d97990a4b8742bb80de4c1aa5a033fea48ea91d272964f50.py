import io
import unittest

from verify_b129_revision_sources import selection, verify_stream


class Guard:
    def check(self):
        pass


ENTRY = (
    b"<entry><ent_seq>1</ent_seq><k_ele><keb>spell</keb></k_ele>"
    b"<r_ele><reb>read</reb><re_restr>spell</re_restr></r_ele>"
    b"<sense><stagk>spell</stagk><gloss>first</gloss></sense>"
    b"<sense><misc>archaic</misc><gloss>second</gloss></sense></entry>"
)
XML = b"<JMdict>" + ENTRY + b"</JMdict>"


def member():
    queries = {
        "exact-spelling:spell": ["1"], "exact-reading:read": ["1"],
        "entry-id-cited-by-actual-comparison:1": ["1"], "exact-reading:absent": [],
    }
    return {"queries": queries, "recordPredicates": {"1": list(queries)[:3]},
            "zeroMatches": ["exact-reading:absent"]}


class CompleteCorrectionSources(unittest.TestCase):
    def test_exact_union_preserves_zero_matches_and_entire_family(self):
        selected = selection(XML, member(), "entry", "ent_seq")
        result = verify_stream(io.BytesIO(XML), "entry", "ent_seq", [selected], Guard())[0]
        self.assertEqual(result["identities"], ["1"])
        self.assertEqual(result["zeroMatches"], ["exact-reading:absent"])

    def test_rejects_missing_secondary_sense_and_restriction(self):
        for removed in (b"<sense><misc>archaic</misc><gloss>second</gloss></sense>",
                        b"<re_restr>spell</re_restr>"):
            with self.subTest(removed=removed):
                selected = selection(XML.replace(removed, b""), member(), "entry", "ent_seq")
                with self.assertRaisesRegex(ValueError, "Incomplete or altered"):
                    verify_stream(io.BytesIO(XML), "entry", "ent_seq", [selected], Guard())

    def test_rejects_unselected_matching_family_and_duplicates(self):
        selected = selection(XML, member(), "entry", "ent_seq")
        for additional, message in ((ENTRY.replace(b">1<", b">2<"), "Missing applicable"),
                                    (ENTRY, "Duplicate identity")):
            with self.subTest(message=message):
                original = b"<JMdict>" + ENTRY + additional + b"</JMdict>"
                with self.assertRaisesRegex(ValueError, message):
                    verify_stream(io.BytesIO(original), "entry", "ent_seq", [selected], Guard())

    def test_rejects_false_negative_and_reverse_membership(self):
        for field in ("queries", "recordPredicates", "zeroMatches"):
            with self.subTest(field=field):
                membership = member()
                if field == "queries":
                    membership[field]["exact-reading:read"] = []
                elif field == "recordPredicates":
                    membership[field]["1"] = ["exact-spelling:spell"]
                else:
                    membership[field] = []
                selected = selection(XML, membership, "entry", "ent_seq")
                with self.assertRaises(ValueError):
                    verify_stream(io.BytesIO(XML), "entry", "ent_seq", [selected], Guard())

    def test_rejects_unsupported_predicate_and_duplicate_extraction(self):
        membership = member()
        membership["queries"]["substring:spell"] = ["1"]
        with self.assertRaisesRegex(ValueError, "Unsupported selector"):
            selection(XML, membership, "entry", "ent_seq")
        with self.assertRaisesRegex(ValueError, "Duplicate or missing"):
            selection(b"<JMdict>" + ENTRY + ENTRY + b"</JMdict>",
                      member(), "entry", "ent_seq")

    def test_literal_does_not_match_compound_or_reading(self):
        raw = b"<kanjidic2><character><literal>X</literal></character></kanjidic2>"
        membership = {"queries": {"literal:X": ["X"], "literal:XY": []},
                      "recordPredicates": {"X": ["literal:X"]}, "zeroMatches": ["literal:XY"]}
        selected = selection(raw, membership, "character", "literal")
        result = verify_stream(io.BytesIO(raw), "character", "literal", [selected], Guard())[0]
        self.assertEqual(result["identities"], ["X"])


if __name__ == "__main__":
    unittest.main()

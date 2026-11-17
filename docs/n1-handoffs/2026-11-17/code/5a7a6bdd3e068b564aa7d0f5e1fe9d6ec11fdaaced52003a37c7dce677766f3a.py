import io
import unittest
import xml.etree.ElementTree as ET
from unittest.mock import Mock

from source_query_union import element_value, verify_stream

RAW = b"""<JMdict>
<entry><ent_seq>1</ent_seq><k_ele><keb>lips</keb></k_ele><r_ele><reb>lip</reb>
<re_restr>lips</re_restr></r_ele><sense><stagk>lips</stagk><gloss>lip</gloss></sense></entry>
<entry><ent_seq>2</ent_seq><k_ele><keb>edge</keb></k_ele><r_ele><reb>rim</reb></r_ele></entry>
<entry><ent_seq>3</ent_seq><r_ele><reb>shore</reb></r_ele></entry>
<entry><ent_seq>4</ent_seq><k_ele><keb>edged</keb></k_ele><r_ele><reb>shores</reb></r_ele></entry>
</JMdict>"""


class UnionTests(unittest.TestCase):
    def selection(self, mode="union", queries=None, ids=("1", "2", "3")):
        entries = ET.fromstring(RAW).findall("entry")
        return {"name": "fixture", "mode": mode,
                "queries": queries or ["contains-keb:lip", "exact-keb:edge", "exact-reb:shore"],
                "expected": {node.findtext("ent_seq"): element_value(node) for node in entries
                             if node.findtext("ent_seq") in ids}}

    def run_selection(self, selection, raw=RAW):
        return verify_stream(io.BytesIO(raw), "entry", "ent_seq", [selection], Mock())

    def test_union_preserves_exactness_and_reading_only_families(self):
        self.assertEqual(self.run_selection(self.selection()), [["1", "2", "3"]])

    def test_missing_family_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Missing applicable family"):
            self.run_selection(self.selection(ids=("1", "2")))

    def test_unrequested_family_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Unexpected or missing"):
            self.run_selection(self.selection(ids=("1", "2", "3", "4")))

    def test_nested_restriction_change_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Incomplete or altered record"):
            self.run_selection(self.selection(), RAW.replace(b"<re_restr>lips</re_restr>", b""))

    def test_existing_modes_retain_selection_behavior(self):
        for mode, queries, ids in [
            ("contains-member", ["lip"], ("1",)),
            ("contains-any", ["lip", "edge"], ("1", "2", "4")),
            ("exact", ["edge"], ("2",)),
        ]:
            with self.subTest(mode=mode):
                self.assertEqual(self.run_selection(self.selection(mode, queries, ids)), [list(ids)])

    def test_invalid_union_selector_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Invalid union selector"):
            self.run_selection(self.selection(queries=["unknown:lip"]))


if __name__ == "__main__":
    unittest.main()

import gzip
import hashlib
import unittest
import xml.etree.ElementTree as ET

from extract_n1_jmdict import extract


class ExtractN1JMdictTest(unittest.TestCase):
    def setUp(self):
        self.raw = gzip.compress(b"""<?xml version="1.0"?>
<!DOCTYPE JMdict [<!ENTITY rare "rare">]>
<JMdict><entry><ent_seq>1</ent_seq>
<k_ele><keb>A</keb><ke_inf>&rare;</ke_inf></k_ele>
<k_ele><keb>B</keb></k_ele>
<r_ele><reb>a</reb><re_restr>A</re_restr></r_ele>
<sense><stagk>A</stagk><misc>&rare;</misc><gloss>first</gloss></sense>
<sense><stagk>B</stagk><gloss>second</gloss></sense>
</entry><entry><ent_seq>2</ent_seq><sense><gloss>other</gloss></sense></entry></JMdict>""")
        self.sha = hashlib.sha256(self.raw).hexdigest()

    def test_preserves_complete_family_and_restrictions(self):
        selected = ET.fromstring(extract(self.raw, self.sha, ["1"]))
        entry = selected.find("entry")
        self.assertEqual(len(selected.findall("entry")), 1)
        self.assertEqual([e.text for e in entry.findall("k_ele/keb")], ["A", "B"])
        self.assertEqual(entry.findtext("r_ele/re_restr"), "A")
        self.assertEqual(len(entry.findall("sense")), 2)
        self.assertEqual(entry.findtext("k_ele/ke_inf"), "rare")
        self.assertEqual(entry.findtext("sense/misc"), "rare")
        self.assertEqual(entry.findall("sense")[1].findtext("stagk"), "B")

    def test_preserves_selection_order(self):
        selected = ET.fromstring(extract(self.raw, self.sha, ["2", "1"]))
        self.assertEqual([e.text for e in selected.findall("entry/ent_seq")], ["2", "1"])

    def test_rejects_hash_mismatch(self):
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            extract(self.raw, "0" * 64, ["1"])

    def test_rejects_missing_entry(self):
        with self.assertRaisesRegex(ValueError, "Missing JMdict"):
            extract(self.raw, self.sha, ["3"])

    def test_rejects_empty_or_duplicate_selection(self):
        for ids in ([], ["1", "1"]):
            with self.subTest(ids=ids), self.assertRaisesRegex(ValueError, "distinct"):
                extract(self.raw, self.sha, ids)


if __name__ == "__main__":
    unittest.main()

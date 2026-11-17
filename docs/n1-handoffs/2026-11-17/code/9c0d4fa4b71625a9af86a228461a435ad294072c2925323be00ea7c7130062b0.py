import unittest
from pathlib import Path

import compact_xml_v1 as codec

PACKET = Path(r"C:\Users\stop-\n1-kanji-workspace\scratch-134\review\fresh-independent-002"
              r"\projected-successor-008\packet")
JMDICT = dict(root="JMdict", record="entry", separator=1,
              aliases=["#=ent_seq", "K=k_ele", "R=r_ele", "S=sense", "g=gloss[xml:lang=eng]",
                       "kp=ke_pri", "rp=re_pri", "ki=ke_inf", "ri=re_inf"],
              bare={"k_ele": "keb", "r_ele": "reb"})
KANJIDIC = dict(root="kanjidic2", record="character", separator=2,
                aliases=["rad=rad_value[rad_type=classical]", "on=reading[r_type=ja_on]",
                         "kun=reading[r_type=ja_kun]", "m=meaning"],
                bare={"character": "literal"})
SAMPLE = dict(root="r", record="e", separator=1, aliases=["g=gloss[xml:lang=eng]"], bare={"k": "keb"})


def sample(body):
    return f"<r>\n{body}\n</r>\n".encode("utf-8")


class CompactXmlTests(unittest.TestCase):
    def test_real_sources_round_trip_byte_exactly(self):
        for name, config in (("evidence/jmdict-families.xml", JMDICT),
                             ("evidence/kanjidic2-review-projection.xml", KANJIDIC)):
            raw = (PACKET / name).read_bytes()
            encoded = codec.encode(raw, **config)
            self.assertEqual(codec.decode(encoded), raw)
            self.assertLess(len(encoded), len(raw))

    def test_nested_bare_empty_and_unaliased_attribute_order(self):
        raw = sample('<e><id>1</id><k><keb>紫</keb><p>x</p></k><s><g2><a>1</a><b></b></g2>'
                     '<gloss xml:lang="eng">a = b "q"</gloss><gloss g_type="lit" xml:lang="eng">c</gloss>'
                     '<gloss xml:lang="eng" g_type="lit">d</gloss></s></e>')
        encoded = codec.encode(raw, **SAMPLE)
        text = encoded.decode("utf-8")
        self.assertIn("k 紫 | p=x", text)
        self.assertIn("g2{a=1 | b=}", text)
        self.assertIn('g=a = b "q"', text)
        self.assertIn("gloss[g_type=lit,xml:lang=eng]=c", text)
        self.assertIn("gloss[xml:lang=eng,g_type=lit]=d", text)
        self.assertEqual(codec.decode(encoded), raw)

    def test_unencodable_inputs_are_rejected(self):
        bad = {
            "separator in value": "<e><id>a | b</id></e>",
            "record separator in value": "<e><id>a ¦ b</id></e>",
            "brace in value": "<e><id>a{b</id></e>",
            "entity": "<e><id>a&amp;b</id></e>",
            "mixed content": "<e><s>text<a>1</a></s></e>",
            "padded value": "<e><id> a</id></e>",
            "tail whitespace": "<e><s><a>1</a> <b>2</b></s></e>",
            "self closing": "<e><id/></e>",
        }
        for label, body in bad.items():
            with self.subTest(label), self.assertRaises(ValueError):
                codec.encode(sample(body), **SAMPLE)
        with self.assertRaises(ValueError):
            codec.encode(sample("<e><gloss>x</gloss></e>"), **dict(SAMPLE, aliases=["gloss=gloss[x=y]"]))

    def test_tampered_encodings_are_rejected(self):
        raw = (PACKET / "evidence/jmdict-families.xml").read_bytes()
        encoded = codec.encode(raw, **JMDICT).decode("utf-8")
        tampered = {
            "gloss text": encoded.replace("g=inflorescence of shiso", "g=inflorescence of perilla", 1),
            "record dropped": "\n".join(line for i, line in enumerate(encoded.split("\n")) if i != 30),
            "alias meaning": encoded.replace("%alias g=gloss[xml:lang=eng]", "%alias g=gloss[xml:lang=fre]"),
            "declared hash": encoded.replace("%source-sha256 7", "%source-sha256 8", 1),
            "unbalanced": encoded.replace("¦ S pos=", "¦ S{pos=", 1),
        }
        for label, text in tampered.items():
            with self.subTest(label), self.assertRaises((ValueError, KeyError, IndexError)):
                codec.decode(text.encode("utf-8"))


if __name__ == "__main__":
    unittest.main()

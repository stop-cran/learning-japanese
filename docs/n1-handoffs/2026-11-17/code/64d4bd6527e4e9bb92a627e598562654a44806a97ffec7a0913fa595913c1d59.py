import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from common import sha
from verify_b134_preparation_capacity import envelope, verify_chain, verify_projection


class PreparationCapacityTests(unittest.TestCase):
    def test_projection_preserves_japanese_attributes_and_misc(self):
        original = (b'<kanjidic2><character><literal>X</literal><codepoint>x</codepoint>'
                    b'<misc><stroke_count>12</stroke_count></misc><reading_meaning><rmgroup>'
                    b'<reading r_type="ja_on" on_type="kan">S</reading>'
                    b'<reading r_type="pinyin">z</reading><meaning>purple</meaning>'
                    b'<meaning m_lang="fr">violet</meaning></rmgroup><nanori>N</nanori>'
                    b'</reading_meaning></character></kanjidic2>')
        projected = original.replace(b'<codepoint>x</codepoint>', b'').replace(
            b'<reading r_type="pinyin">z</reading>', b'').replace(
            b'<meaning m_lang="fr">violet</meaning>', b'')
        verify_projection(original, projected)
        for changed in (projected.replace(b' on_type="kan"', b''),
                        projected.replace(b'<stroke_count>12', b'<stroke_count>11'),
                        projected.replace(b'<nanori>N</nanori>', b'')):
            with self.assertRaisesRegex(ValueError, "Unauthorized projection"):
                verify_projection(original, changed)

    def test_chain_rejects_missing_changed_or_reordered_lines(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            raw, content = b'header\none\ntwo\nfooter\n', b'one\ntwo\n'
            source = dict(source="x", sha256=sha(content), selectedSha256=sha(content),
                          sourceLines=2, selectedLines=2)
            part = dict(source, a=1, b=2, segmentStart=2, segmentEnd=3)
            segment = dict(index=1, path=str(root / "segment"), sha256=sha(raw),
                           bytes=len(raw), lines=4, parts=[part])
            chain = dict(sources=[source], segments=[segment])
            with patch("verify_b134_preparation_capacity.frozen", return_value=raw):
                self.assertEqual(verify_chain({"x": content}, chain, root), [("x", content)])
                for field, value in (("b", 1), ("a", 2), ("segmentStart", 3)):
                    broken = copy.deepcopy(chain)
                    broken["segments"][0]["parts"][0][field] = value
                    with self.assertRaises(ValueError):
                        verify_chain({"x": content}, broken, root)
                with self.assertRaises(ValueError):
                    verify_chain({"x": b"two\none\n"}, chain, root)

    def test_envelope_accounts_for_interaction_and_oversized_lines(self):
        self.assertEqual(envelope(b"x\n" * 6950), 2100)
        self.assertEqual(envelope(b"x\n" * 6951), 6300)
        with self.assertRaisesRegex(ValueError, "Oversized source line"):
            envelope(b"x" * 13900 + b"\n")
        with self.assertRaisesRegex(ValueError, "Unframed source"):
            envelope(b"missing newline")


if __name__ == "__main__":
    unittest.main()

import tempfile
import unittest
from pathlib import Path

from common import sha
from prepare_b134_reconciliation_captures import checked_capture, extract, extractor_type


class CapturePreparationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser_type = extractor_type()

    def test_complete_text_and_image_omissions_are_preserved(self):
        raw = (
            '<article><h2>Publisher</h2><p>First sense</p><p>Second sense; example</p>'
            '<img src="glyph.png" alt="rare glyph"><img src="missing.png">'
            '<script>not a definition</script><style>not a definition</style>'
            '</article><article>Other publisher and sense</article>'
        ).encode()
        text, images = extract(raw, self.parser_type)
        for expected in (
            b"First sense", b"Second sense; example", b"Other publisher and sense",
            b"[image alt: rare glyph]", b"[image without alt text]",
        ):
            self.assertIn(expected, text)
        self.assertNotIn(b"not a definition", text)
        self.assertEqual(images, [
            {"src": "glyph.png", "alt": "rare glyph"}, {"src": "missing.png", "alt": None},
        ])

    def test_changed_input_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "capture.html"
            path.write_bytes(b"<p>Changed sense</p>")
            with self.assertRaisesRegex(ValueError, "Captured input changed"):
                checked_capture(path, sha(b"<p>Original sense</p>"))

    def test_unclosed_hidden_region_and_empty_capture_are_rejected(self):
        for raw in (b"<p>Definition</p><script>unfinished", b"<style>only CSS</style>"):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                extract(raw, self.parser_type)


if __name__ == "__main__":
    unittest.main()

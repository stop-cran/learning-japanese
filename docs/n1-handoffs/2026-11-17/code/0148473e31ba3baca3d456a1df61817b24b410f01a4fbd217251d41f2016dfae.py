import unittest

from weblio_sections import extract, original


def section(name, body):
    return f"<!--\u958b\u59cb {name} -->{body}<!--\u7d42\u4e86 {name}-->"


class WeblioSectionsTests(unittest.TestCase):
    def test_complete_sections_keep_order_and_source_identity(self):
        raw = (
            section("Dictionary A", "<p>first sense</p><p>second sense</p>")
            + "<div>advertisement outside sources</div>"
            + section("Dictionary B", "<p>different reading</p><p>qualification</p>")
        ).encode("utf-8")
        text, error = extract(raw)
        self.assertIsNone(error)
        self.assertEqual(
            text,
            "Weblio source section: Dictionary A\nfirst sense\nsecond sense\n\n"
            "Weblio source section: Dictionary B\ndifferent reading\nqualification\n",
        )

    def test_original_daijisen_body_is_unchanged(self):
        raw = (
            original.START + '<p>A &amp; B</p><script>unrelated()</script>'
            '<p>C<br>D</p>' + original.END
        ).encode("utf-8")
        expected, old_error = original.extract(raw)
        actual, error = extract(raw)
        self.assertIsNone(old_error)
        self.assertIsNone(error)
        self.assertEqual(actual.split("\n", 1)[1], expected)

    def test_ambiguous_sections_fail_closed_without_partial_output(self):
        for raw in (
            section("A", "one") + section("A", "two"),
            "<!--\u958b\u59cb A -->one<!--\u7d42\u4e86 B-->",
            "<!--\u958b\u59cb A -->one",
            "<!--\u958b\u59cb A -->" + section("B", "nested") + "<!--\u7d42\u4e86 A-->",
            section("A", "one") + section("B", "<script>empty()</script>"),
            section("", "unnamed"),
            section("A", "one") + "<!--\u958b\u59cb broken",
            "no dictionary boundaries",
        ):
            with self.subTest(raw=raw):
                text, error = extract(raw.encode("utf-8"))
                self.assertIsNone(text)
                self.assertIsInstance(error, str)
                self.assertTrue(error)

    def test_invalid_utf8_is_not_replaced(self):
        text, error = extract(b"\xff")
        self.assertIsNone(text)
        self.assertIn("UTF-8", error)


if __name__ == "__main__":
    unittest.main()

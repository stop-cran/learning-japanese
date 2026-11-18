import unittest

from verify_b118_revision_v2 import inserted_lines


class InsertedLinesTest(unittest.TestCase):
    def test_returns_only_insertions(self):
        self.assertEqual(inserted_lines("a\nb\nc", "a\nx\nb\nc\ny"), ["x", "y"])

    def test_rejects_changed_earlier_text(self):
        with self.assertRaises(ValueError):
            inserted_lines("a\nb\nc", "a\nB\nc")

    def test_rejects_deleted_earlier_text(self):
        with self.assertRaises(ValueError):
            inserted_lines("a\nb\nc", "a\nc\nz")


if __name__ == "__main__":
    unittest.main()

import unittest

from prepare_b133_confirmation_sources import sections


class PublisherSectionTests(unittest.TestCase):
    def test_selected_section_preserves_all_senses_and_examples(self):
        raw = ("Page\nPublisher A\nSense 1\nExample\nSense 2\n出典 A\nAdvertisement\n"
               "Publisher B\nDifferent sense\n出典 B\n").encode("utf-8")
        selected = sections(raw, ["Publisher A"])
        self.assertEqual(selected, [(2, 6, "Publisher A",
                                     "Publisher A\nSense 1\nExample\nSense 2\n出典 A\n".encode("utf-8"))])

    def test_missing_or_duplicate_publisher_is_not_silently_truncated(self):
        for raw in (b"Nothing\n", "A\n出典 A\nA\n出典 A\n".encode("utf-8")):
            with self.assertRaises(ValueError):
                sections(raw, ["A"])


if __name__ == "__main__":
    unittest.main()

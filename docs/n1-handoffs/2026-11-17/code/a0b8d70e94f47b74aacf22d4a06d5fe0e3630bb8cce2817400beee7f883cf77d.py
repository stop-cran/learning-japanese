import unittest

from verify_b133_teaching_revision import verify_article


class TeachingBoundaryTests(unittest.TestCase):
    def test_only_exact_exclusion_append_and_notes_change_are_allowed(self):
        before = b"---\nquiz_exclusions: [a, b]\ntitle: unchanged\n---\n## Readings\nsame\n## Notes\nOld.\nMetadata: old\n"
        after = before.replace(b"[a, b]", b"[a, b, c]").replace(b"Old.", b"Expanded note.")
        verify_article(before, after, ["c"])
        for changed in (
            after.replace(b"[a, b, c]", b"[b, a, c]"),
            after.replace(b"unchanged", b"changed"),
            after.replace(b"same", b"different"),
            after.replace(b"Metadata: old", b"Missing citation boundary"),
        ):
            with self.assertRaises(ValueError):
                verify_article(before, changed, ["c"])


if __name__ == "__main__":
    unittest.main()

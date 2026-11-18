import difflib
import unittest

from verify_b129_revision_evidence import PARENT, PREFIX, check_teaching


class TeachingPreservationTests(unittest.TestCase):
    def setUp(self):
        self.old, self.new = {}, {}
        self.cards = (("\u7d79", 1), ("\u8679", 3))
        for character, count in self.cards:
            path = f"kanji/{character}.md"
            self.old[path] = "---\nquiz_exclusions: [A]\n---\n\n# Card\n\nOriginal claim.\n"
            self.new[path] = self.old[path].replace("[A]", "[A, B]") + (
                "- Additional qualified note.\n" * count)
        self.patch = self.make_patch()

    def make_patch(self):
        lines = []
        for character, _ in self.cards:
            path = f"kanji/{character}.md"
            lines.extend(difflib.unified_diff(
                self.old[path].splitlines(keepends=True), self.new[path].splitlines(keepends=True),
                fromfile=PARENT + ":" + path, tofile="candidate:" + path))
        return "".join(lines).encode()

    def blob(self, path, revision=None):
        if path == PREFIX + "teaching-diff.patch":
            return self.patch
        return (self.old if revision == PARENT else self.new)[path].encode()

    def test_only_the_expected_note_insertions_are_allowed(self):
        result = check_teaching(self.blob)
        self.assertEqual([len(result[f"kanji/{character}.md"]) for character, _ in self.cards], [1, 3])

    def test_changed_original_claim_is_rejected(self):
        path = f"kanji/{self.cards[0][0]}.md"
        self.new[path] = self.new[path].replace("Original claim.", "Rewritten claim.")
        self.patch = self.make_patch()
        with self.assertRaises(ValueError):
            check_teaching(self.blob)

    def test_stale_saved_patch_is_rejected(self):
        self.patch += b"+Unrecorded change\n"
        with self.assertRaises(ValueError):
            check_teaching(self.blob)


if __name__ == "__main__":
    unittest.main()

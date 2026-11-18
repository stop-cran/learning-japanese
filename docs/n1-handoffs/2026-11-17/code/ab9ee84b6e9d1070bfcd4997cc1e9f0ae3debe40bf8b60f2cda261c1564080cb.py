import copy
import unittest

from verify_b129_revision_runtime import (
    NOTES, PREFIX, RAINBOW, REQUIRED_GUARDS, SILK,
    check_metadata, check_notes, check_paths, check_runtime,
)


class RevisionRuntimeTests(unittest.TestCase):
    def cards(self):
        old = {
            "kanji": RAINBOW, "title": "rainbow", "onyomi": ["A", "B"],
            "quizOnyomi": [], "distractors": ["X", "Y", "Z"],
            "quiz_exclusions": ["old1", "old2"],
        }
        new = copy.deepcopy(old)
        new["quiz_exclusions"] += sorted(REQUIRED_GUARDS)
        return old, new

    def test_scoped_guard_additions_preserve_metadata_and_old_order(self):
        old, new = self.cards()
        self.assertEqual(sorted(REQUIRED_GUARDS), check_metadata(old, new, REQUIRED_GUARDS))
        for key, value in (
            ("onyomi", ["B", "A"]), ("quizOnyomi", ["A"]), ("title", "ring"),
            ("quiz_exclusions", ["old2", "old1", *sorted(REQUIRED_GUARDS)]),
            ("quiz_exclusions", ["old1", *sorted(REQUIRED_GUARDS)]),
            ("quiz_exclusions", new["quiz_exclusions"] + ["unassigned"]),
            ("quiz_exclusions", new["quiz_exclusions"] + [new["quiz_exclusions"][-1]]),
            ("quiz_exclusions", ["old1", "old2"]),
        ):
            changed = copy.deepcopy(new)
            changed[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                check_metadata(old, changed, REQUIRED_GUARDS)

    def test_rejects_even_allowed_guard_on_curated_option(self):
        old, new = self.cards()
        new["quiz_exclusions"].append("X")
        with self.assertRaisesRegex(ValueError, "excluded curated option"):
            check_metadata(old, new, REQUIRED_GUARDS | {"X"})

    def test_only_new_cards_can_change_runtime(self):
        target = f"kanji/{RAINBOW}.md"
        before = {target: ("old", False), "words/support.md": ("word", False),
                  "images/image.png": ("image", True)}
        after = {**before, target: ("new", False)}
        check_runtime(before, after, {target})
        for path, value in (
            ("words/support.md", ("changed", False)),
            ("images/image.png", ("image", False)),
            (f"kanji/{SILK}.md", ("extra", False)),
        ):
            changed = {**after, path: value}
            with self.subTest(path=path), self.assertRaises(ValueError):
                check_runtime(before, changed, {target})
        with self.assertRaises(ValueError):
            check_runtime(before, after, {target, f"kanji/{SILK}.md"})

    def test_correction_cannot_modify_original_evidence_or_add_new_runtime(self):
        allowed = {f"kanji/{RAINBOW}.md": "M", "manifest.json": "M",
                   PREFIX + "pair-dispositions.json": "A", NOTES: "M"}
        check_paths(allowed)
        for path, status in (
            ("docs/n1-sources/batch-129/source-receipt.json", "M"),
            (PREFIX + "pair-dispositions.json", "M"),
            ("words/support.md", "M"), ("kanji/new.md", "A"),
            (f"kanji/{SILK}.md", "D"),
        ):
            with self.subTest(path=path, status=status), self.assertRaises(ValueError):
                check_paths({**allowed, path: status})

    def test_notes_preserve_all_existing_lines(self):
        old = b"# Notes\r\n\r\n## Batch 128: previous\r\nold text\r\n"
        added = b"### Batch 129: bounded reconciliation\r\nnew text\r\n\r\n"
        new = old.replace(b"## Batch 128:", added + b"## Batch 128:")
        check_notes(old, new)
        for changed in (
            new.replace(b"old text", b"rewritten text"),
            new.replace(b"129:", b"130:"),
            new.replace(b"\r\n", b"\n"),
        ):
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                check_notes(old, changed)


if __name__ == "__main__":
    unittest.main()

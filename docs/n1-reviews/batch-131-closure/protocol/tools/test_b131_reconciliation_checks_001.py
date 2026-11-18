import copy
import unittest

import b131_reconciliation_checks_001 as checks


class ReconciliationScopeTests(unittest.TestCase):
    def setUp(self):
        self.char = "\u971c"
        self.other = "\u885b"
        self.added = "\u6c37"
        self.path = f"kanji/{self.char}.md"
        self.old = {"kanji": self.char, "title": "frost", "onyomi": ["\u30bd\u30a6"],
                    "kunyomi": ["\u3057\u3082"], "quizKunyomi": ["\u3057\u3082"],
                    "quiz_exclusions": ["\u767d", "\u5bd2"], "distractors": ["\u53e4"]}
        self.new = copy.deepcopy(self.old)
        self.new["quiz_exclusions"].append(self.added)

    def test_scoped_guard_preserves_metadata_and_existing_order(self):
        self.assertEqual([self.added], checks.check_metadata(
            self.old, self.new, {self.added}, {self.added}))
        mutations = []
        for key, value in (("onyomi", []), ("title", "ice"), ("quizKunyomi", []),
                           ("quiz_exclusions", [self.added]),
                           ("quiz_exclusions", ["\u5bd2", "\u767d", self.added]),
                           ("quiz_exclusions", ["\u767d", "\u5bd2", self.added, self.added]),
                           ("quiz_exclusions", ["\u767d", "\u5bd2", "\u96ea"])):
            bad = copy.deepcopy(self.new)
            bad[key] = value
            mutations.append(bad)
        for bad in mutations:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                checks.check_metadata(self.old, bad, {self.added}, {self.added})
        for forbidden in (self.char, "\u53e4"):
            bad = copy.deepcopy(self.old)
            bad["quiz_exclusions"].append(forbidden)
            with self.subTest(forbidden=forbidden), self.assertRaises(ValueError):
                checks.check_metadata(self.old, bad, {forbidden}, {forbidden})

    def test_path_scope_rejects_source_rewrites_support_changes_and_removals(self):
        valid = {self.path: "M", "manifest.json": "M",
                 checks.PREFIX + "source-reuse.json": "A", checks.NOTES: "M"}
        checks.check_paths(valid, {self.path})
        for name, status in (("docs/n1-sources/batch-131/selection.json", "M"),
                             ("words/support.md", "M"), (f"strokes/{self.char}.json", "M"),
                             (f"kanji/{self.other}.md", "M"),
                             (checks.PREFIX + "source-reuse.json", "M"), (self.path, "D")):
            with self.subTest(name=name), self.assertRaises(ValueError):
                checks.check_paths({**valid, name: status}, {self.path})
        with self.assertRaises(ValueError):
            checks.check_paths({self.path: "M"}, {self.path})

    def test_runtime_requires_exact_delta_and_preserves_binary_classification(self):
        before = {self.path: ("old", False), "words/support.md": ("same", False),
                  "images/example.png": ("image", True)}
        after = {**before, self.path: ("new", False)}
        checks.check_runtime(before, after, {self.path})
        for bad in ({**after, "extra.md": ("extra", False)},
                    {key: value for key, value in after.items() if key != "words/support.md"},
                    {**after, "words/support.md": ("changed", False)},
                    {**after, self.path: ("new", True)}):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                checks.check_runtime(before, bad, {self.path})

    def test_notes_are_additive_and_identify_this_batch(self):
        old = b"# Notes\n\n## Batch 130: prior\nKeep.\n"
        checks.check_notes(old, old + b"\n## Batch 131 reconciliation 001: guards\nNew.\n")
        for bad in (old.replace(b"Keep.", b"Changed."),
                    old + b"\n## Batch 132: wrong batch\nNew.\n", old):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                checks.check_notes(old, bad)


if __name__ == "__main__":
    unittest.main()

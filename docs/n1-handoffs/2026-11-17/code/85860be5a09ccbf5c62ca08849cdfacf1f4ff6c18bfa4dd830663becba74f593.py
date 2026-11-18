import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("rev002", HERE / "verify-b134-revision002.py")
rev = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rev)

REPO = r"C:\Users\stop-\n1-kanji-workspace\b134-worktree"
OLD = subprocess.run(["git", "--no-pager", "-C", REPO, "show", f"{rev.REVIEWED}:{rev.TARGET}"],
                     check=True, capture_output=True).stdout.decode("utf-8")
NOTE = ("- Historical court usage records 濃 alone for deep purple, and 紫 can name soy\n"
        "  sauce while 食 means food; 濃 and 食 are excluded as answers on this card.")


def revise(text, extra=("濃", "食"), note=NOTE):
    text = text.replace("\r\n", "\n")
    line = next(l for l in text.split("\n") if l.startswith("quiz_exclusions:"))
    text = text.replace(line, line[:-1] + "".join(", " + c for c in extra) + "]")
    return text.rstrip("\n") + "\n" + note + "\n" if note else text


class CardDelta(unittest.TestCase):
    def test_exact_two_guards_with_note_pass(self):
        result = rev.check_card_delta(OLD, revise(OLD))
        self.assertEqual((result["priorExclusions"], result["exclusions"]), (56, 58))
        self.assertTrue(result["appendedInOrder"])
        self.assertEqual(result["changedSections"], ["## Notes"])
        self.assertEqual(result["addedNotesBullets"], 1)

    def test_rejects_wrong_exclusion_sets(self):
        for extra in (("濃",), ("濃", "食", "赤"), ("濃", "濃"), ("食", "紅")):
            with self.subTest(extra=extra), self.assertRaises(ValueError):
                rev.check_card_delta(OLD, revise(OLD, extra))

    def test_rejects_changes_outside_notes_or_altered_old_note(self):
        mutations = [
            revise(OLD).replace("title: purple; violet", "title: purple"),
            revise(OLD).replace("distractors: [古, 右, 川]", "distractors: [古, 右, 濃]"),
            revise(OLD).replace("names purple or violet", "names purple"),
            revise(OLD).replace("12 strokes. The", "12 strokes; the"),
            revise(OLD, note="- A note explaining only 濃."),
            revise(OLD, note=None),
        ]
        for text in mutations:
            with self.assertRaises(ValueError):
                rev.check_card_delta(OLD, text)


class Inventory(unittest.TestCase):
    ok = [("M", rev.TARGET), ("M", "manifest.json"),
          ("A", "docs/n1-sources/batch-134-revision-002/evidence.json")]

    def test_additive_new_directory_passes(self):
        prefix, paths = rev.check_inventory(self.ok, lambda p: False)
        self.assertEqual(prefix, "docs/n1-sources/batch-134-revision-002/")
        self.assertEqual(len(paths), 1)

    def test_rejects_scope_violations(self):
        cases = [
            (self.ok, lambda p: True),
            (self.ok[:2], lambda p: False),
            (self.ok[:2] + [("M", "docs/n1-sources/batch-134-revision-002/x.json")], lambda p: False),
            (self.ok + [("A", "docs/n1-sources/batch-134-other/x.json")], lambda p: False),
            (self.ok + [("M", "kanji/濃.md")], lambda p: False),
            (self.ok[1:], lambda p: False),
        ]
        for changes, existed in cases:
            with self.assertRaises(ValueError):
                rev.check_inventory(changes, existed)


class Manifest(unittest.TestCase):
    old = {"contentVersion": "a", "kanji": {rev.TARGET: "1", "kanji/濃.md": "2"}}

    def test_only_target_and_version_change(self):
        new = {"contentVersion": "b", "kanji": {rev.TARGET: "9", "kanji/濃.md": "2"}}
        self.assertEqual(rev.check_manifest_delta(self.old, new)["contentVersion"], "b")

    def test_rejects_other_runtime_change(self):
        new = {"contentVersion": "b", "kanji": {rev.TARGET: "9", "kanji/濃.md": "3"}}
        with self.assertRaises(ValueError):
            rev.check_manifest_delta(self.old, new)


if __name__ == "__main__":
    unittest.main(verbosity=2)

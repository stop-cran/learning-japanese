import copy
import unittest

from verify_b131_payload import runtime_entries, verify_metadata, verify_runtime_delta


class PayloadPreservationTests(unittest.TestCase):
    def test_full_reading_order_and_source_scalars_cannot_drift(self):
        row = {"kanji": "X", "metadata": {
            "onyomi": ["A", "B", "C"], "kunyomi": ["D", "E"], "radical": "R",
            "strokes": 8, "radicalNumber": 140,
        }}
        card = {"kanji": "X", "jlpt": "1", "tags": ["jlpt-n1"],
                "onyomi": ["A", "B", "C"], "kunyomi": ["D", "E"], "radical": "R",
                "strokes": "8", "radicalNumber": "140", "quizOnyomi": ["A"], "quizKunyomi": []}
        verify_metadata(card, row)
        for field, value in (
            ("onyomi", ["B", "A", "C"]), ("onyomi", ["A", "B"]), ("kunyomi", ["D"]),
            ("radical", "S"), ("strokes", "9"), ("radicalNumber", "141"),
            ("jlpt", "2"), ("quizOnyomi", ["Z"]), ("quizOnyomi", []),
        ):
            changed = copy.deepcopy(card)
            changed[field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                verify_metadata(changed, row)

    def test_only_selected_additions_and_linked_word_hashes_change(self):
        before = {"words/W.md": ("old-word", False), "kanji/A.md": ("old-card", False),
                  "images/p.png": ("old-image", True)}
        added = {"kanji/X.md", "strokes/X.json", "kanji/Y.md", "strokes/Y.json"}
        after = {**before, **{path: ("new-" + path, False) for path in added}}
        after["words/W.md"] = ("linked-word", False)
        verify_runtime_delta(before, after, added, {"words/W.md"})
        for change in ("remove-old", "extra-new", "change-card", "change-image", "change-kind", "missing-link"):
            changed = dict(after)
            if change == "remove-old":
                del changed["kanji/A.md"]
            elif change == "extra-new":
                changed["words/extra.md"] = ("extra", False)
            elif change == "change-card":
                changed["kanji/A.md"] = ("other", False)
            elif change == "change-image":
                changed["images/p.png"] = ("other-image", True)
            elif change == "change-kind":
                changed["images/p.png"] = ("old-image", False)
            else:
                changed["words/W.md"] = before["words/W.md"]
            with self.subTest(change=change), self.assertRaises(ValueError):
                verify_runtime_delta(before, changed, added, {"words/W.md"})

    def test_manifest_cannot_hide_duplicate_paths_across_sections(self):
        self.assertEqual(
            {"words/W.md": ("word", False), "images/p.png": ("image", True)},
            runtime_entries({"files": {"words/W.md": "word"}, "images": {"images/p.png": "image"},
                             "contentVersion": "version"}))
        with self.assertRaisesRegex(ValueError, "Duplicate manifest path"):
            runtime_entries({"files": {"words/W.md": "word"}, "images": {"words/W.md": "image"}})


if __name__ == "__main__":
    unittest.main()

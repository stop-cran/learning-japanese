import copy
import unittest

from verify_b130_revision_runtime import (
    NOTES, PARENT, PREFIX, check_initial, check_metadata, check_notes, check_paths, check_runtime,
)


class RevisionRuntimeTests(unittest.TestCase):
    def test_only_declared_guard_additions_preserve_source_metadata(self):
        old = {"kanji": "\u8017", "title": "decrease; wear down through use",
               "onyomi": ["A", "B"], "quizOnyomi": ["A"],
               "distractors": ["\u53f3", "\u5ddd", "\u672c"], "quiz_exclusions": ["\u6e1b", "\u6bba"]}
        new = {**old, "quiz_exclusions": [*old["quiz_exclusions"], "\u64e6", "\u6469"]}
        required = {"\u64e6", "\u6469"}
        self.assertEqual(["\u64e6", "\u6469"], check_metadata(old, new, required, required))
        for key, value in (
            ("onyomi", ["B", "A"]), ("quizOnyomi", ["B"]), ("title", "different"),
            ("quiz_exclusions", ["\u6bba", "\u6e1b", "\u64e6", "\u6469"]),
            ("quiz_exclusions", ["\u6e1b", "\u64e6", "\u6469"]),
            ("quiz_exclusions", [*new["quiz_exclusions"], "\u64e6"]),
            ("quiz_exclusions", [*new["quiz_exclusions"], "\u524a"]),
            ("quiz_exclusions", [*old["quiz_exclusions"], "\u64e6"]),
        ):
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                check_metadata(old, {**new, key: value}, required, required)
        for invalid in ("\u53f3", "\u8017"):
            with self.subTest(invalid=invalid), self.assertRaisesRegex(ValueError, "Self-exclusion"):
                check_metadata(old, {**new, "quiz_exclusions": [*new["quiz_exclusions"], invalid]},
                               required | {invalid}, required)

    def test_no_runtime_additions_removals_or_other_changes(self):
        target = "kanji/\u8017.md"
        before = {target: ("old", False), "words/support.md": ("word", False),
                  "images/image.png": ("image", True)}
        after = {**before, target: ("new", False)}
        check_runtime(before, after, {target})
        bad = [
            {**after, "words/support.md": ("changed", False)},
            {**after, "images/image.png": ("image", False)},
            {**after, "kanji/new.md": ("extra", False)},
            {path: value for path, value in after.items() if path != "words/support.md"},
        ]
        for changed in bad:
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                check_runtime(before, changed, {target})
        with self.assertRaises(ValueError):
            check_runtime(before, after, {target, "kanji/\u62cd.md"})

    def test_original_evidence_and_unselected_cards_cannot_change(self):
        cards = {"kanji/\u8017.md"}
        allowed = {next(iter(cards)): "M", "manifest.json": "M", NOTES: "M",
                   PREFIX + "pair-dispositions.json": "A"}
        check_paths(allowed, cards)
        for path, status in (
            ("docs/n1-sources/batch-130/source-receipt.json", "M"),
            (PREFIX + "pair-dispositions.json", "M"),
            ("words/support.md", "M"), ("kanji/\u62cd.md", "M"),
            ("kanji/new.md", "A"), ("kanji/\u8017.md", "D"),
        ):
            with self.subTest(path=path, status=status), self.assertRaises(ValueError):
                check_paths({**allowed, path: status}, cards)

    def test_authoring_notes_are_insert_only_and_batch_labelled(self):
        before = b"# Notes\r\n\r\n## Batch 129: previous\r\nexisting text\r\n"
        after = before.replace(b"## Batch 129:",
                               b"### Batch 130: reconciliation\r\nnew text\r\n\r\n## Batch 129:")
        check_notes(before, after)
        for changed in (after.replace(b"existing", b"rewritten"),
                        after.replace(b"130:", b"131:"), after.replace(b"\r\n", b"\n")):
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                check_notes(before, changed)

    def test_only_bound_accepted_attempt004_can_authorize_runtime_check(self):
        report = {"path": "report", "sha256": "a" * 64}
        common = {"candidate": PARENT, "run": "N1-B130-GPT-004"}
        accepted = {**common, "reviewAccepted": True, "verdict": "NEEDS FIX",
                    "acceptedFindings": ["F1"], "report": report}
        adjudication = {**common, "verdict": "NEEDS FIX", "acceptedFindings": ["F1"],
                        "report": report, "openClaimIds": [], "publicationAccepted": False}
        final = {**common, "status": "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION",
                 "problems": []}
        check_initial("gpt", accepted, adjudication, final)
        for target, key, value in (
            (accepted, "reviewAccepted", False), (accepted, "run", "N1-B130-GPT-001"),
            (adjudication, "candidate", "b" * 40), (adjudication, "openClaimIds", ["C1"]),
            (adjudication, "acceptedFindings", []), (adjudication, "report", {}),
            (final, "status", "HOLD"), (final, "problems", ["incomplete"]),
        ):
            changed = copy.deepcopy(target)
            changed[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                check_initial("gpt", changed if target is accepted else accepted,
                              changed if target is adjudication else adjudication,
                              changed if target is final else final)


if __name__ == "__main__":
    unittest.main()

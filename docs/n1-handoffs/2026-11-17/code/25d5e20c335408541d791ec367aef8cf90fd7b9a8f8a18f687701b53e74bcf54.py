import unittest

from verify_b123_revision_v4 import (
    CARD, PREFIX, check_delta, check_followup_metadata, check_source_reference,
)


class HeldComparisonTests(unittest.TestCase):
    def test_required_guards_preserve_old_and_allow_only_scoped_additions(self):
        before = {"title": "model; standard", "onyomi": ["\u30cf\u30f3"], "kunyomi": [],
                  "distractors": list("\u8eca\u66f8\u9054"),
                  "quiz_exclusions": list("\u6a19\u7d00\u93e1\u69d8\u683c\u666e")}
        for additions in ("\u672c\u5ea6", "\u672c\u5ea6\u50cf\u7406", "\u672c\u5ea6\u50cf\u56f2\u65b9\u8a08\u6e2c\u91cf\u7406"):
            after = {**before, "quiz_exclusions": before["quiz_exclusions"] + list(additions)}
            self.assertEqual(check_followup_metadata(before, after), list(additions))
        for additions in ("", "\u672c", "\u5ea6\u672c", "\u672c\u5ea6\u672c", "\u672c\u5ea6\u5149"):
            after = {**before, "quiz_exclusions": before["quiz_exclusions"] + list(additions)}
            with self.subTest(additions=additions), self.assertRaises(ValueError):
                check_followup_metadata(before, after)
        changed = {**before, "title": "example",
                   "quiz_exclusions": before["quiz_exclusions"] + list("\u672c\u5ea6")}
        with self.assertRaises(ValueError):
            check_followup_metadata(before, changed)

    def test_old_sources_and_other_runtime_cannot_be_changed(self):
        valid = f"M\t{CARD}\nM\tmanifest.json\nA\t{PREFIX}source-manifest.json\n"
        self.assertEqual(check_delta(valid), [PREFIX + "source-manifest.json"])
        for delta in (
            valid + "M\tdocs/n1-sources/batch-123/reconciliation-002/pair-disposition.json\n",
            valid + "M\tkanji/\u672c.md\n",
            valid.replace("A\t", "M\t"),
            valid.replace("M\tmanifest.json\n", ""),
        ):
            with self.subTest(delta=delta), self.assertRaises(ValueError):
                check_delta(delta)

    def test_source_reference_binds_capture_and_bounded_exact_quotes(self):
        source = {"character": "x", "url": "https://example.test/x",
                  "raw": {"sha256": "raw"}, "extract": {"sha256": "extract"}}
        reference = {"character": "x", "url": source["url"],
                     "rawSha256": "raw", "extractSha256": "extract",
                     "summary": "Original summary.", "limitations": "Bounded evidence.",
                     "quotes": [{"text": "phrase", "lines": [2, 2]}]}
        extract = b"heading\nshort phrase here\n"
        check_source_reference(reference, source, extract)
        check_source_reference({**reference, "quotes": []}, source, extract)
        for changed in (
            {**reference, "extractSha256": "changed"},
            {**reference, "summary": ""},
            {**reference, "quotes": [{"text": "not present", "lines": [2, 2]}]},
            {**reference, "quotes": [{"text": "phrase", "lines": [1, 1]}]},
            {**reference, "quotes": [{"text": "x" * 81, "lines": [1, 2]}]},
        ):
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                check_source_reference(changed, source, extract)


if __name__ == "__main__":
    unittest.main()

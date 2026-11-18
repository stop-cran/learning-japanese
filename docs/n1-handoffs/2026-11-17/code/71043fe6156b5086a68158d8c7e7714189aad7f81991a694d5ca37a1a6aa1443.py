import copy
import json
import unittest
from pathlib import Path

from prepare_b130_revision_external import EVIDENCE, verify_capture


class B130ExternalObservationTests(unittest.TestCase):
    def setUp(self):
        declarations = json.loads((EVIDENCE / "external-capture-bindings.json").read_bytes())
        analysis = json.loads((EVIDENCE / "authored-source-analysis-001.json").read_bytes())
        self.samples = []
        for item in declarations["captures"]:
            raw_path = Path(item["localRawCapture"])
            self.samples.append((item, raw_path.read_bytes(), raw_path.with_suffix(".txt").read_bytes(),
                                 analysis["externalEntries"][item["character"]]))

    def test_actual_complete_captures_extract_without_refetching(self):
        for item, raw, text, analysis in self.samples:
            with self.subTest(character=item["character"]):
                result = verify_capture(item, raw, text, analysis)
                self.assertIn(item["finalUrl"].encode(), result)
                self.assertGreater(len(result), 1000)

    def test_wrong_identity_changed_bytes_or_invented_excerpt_is_rejected(self):
        item, raw, text, analysis = self.samples[0]
        for change in ("url", "raw", "text", "excerpt"):
            with self.subTest(change=change):
                updated, amended = copy.deepcopy(item), copy.deepcopy(analysis)
                source, extracted = raw, text
                if change == "url":
                    updated["url"] = "https://kotobank.jp/word/incorrect"
                elif change == "raw":
                    source += b"changed"
                elif change == "text":
                    extracted += b"changed"
                else:
                    amended["shortExcerpt"] = "This quoted definition does not exist in this source."
                with self.assertRaises(ValueError):
                    verify_capture(updated, source, extracted, amended)


if __name__ == "__main__":
    unittest.main()

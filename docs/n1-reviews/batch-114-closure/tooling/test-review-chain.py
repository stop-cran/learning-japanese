"""Bounded eligibility/chain fixtures; no session or delivery probe."""
import json
import tempfile
import unittest
from pathlib import Path

from review_chain import build_chain, validate_selection


REFERENCE = {
    "newCards": ["一", "二"], "otherRequiredCards": [],
    "cards": [{"card": "一", "distractors": ["三"], "quiz_exclusions": ["四"]},
              {"card": "二", "distractors": ["三"], "quiz_exclusions": []}],
}


class Guard:
    def check(self):
        pass


class ReviewChainTests(unittest.TestCase):
    def test_bad_d_details(self):
        for details in ("一 no colon", ": overlap", "九: overlap", "一, 九: overlap",
                        "一:", "一: \t", "、/: overlap"):
            with self.subTest(details=details):
                self.assertFalse(validate_selection(f"D1 五 - {details}\nE: none", REFERENCE)["valid"])

    def test_single_and_multiple_new_cards(self):
        for names in ("一", "一, 二", "一、二", "一 and 二", "一/二", "一・二"):
            with self.subTest(names=names):
                self.assertTrue(validate_selection(f"D1 五 - {names}: overlap\nE: none", REFERENCE)["valid"])

    def test_eligibility(self):
        for char in ("一", "三", "四"):
            with self.subTest(char=char):
                self.assertFalse(validate_selection(f"D1 {char} - 二: overlap\nE: none", REFERENCE)["valid"])
        self.assertFalse(validate_selection("D: none\nE1 五 - reason", REFERENCE)["valid"])
        self.assertTrue(validate_selection("D: none\nE1 四 - reason", REFERENCE)["valid"])

    def test_duplicates_and_order(self):
        result = validate_selection("D1 五 - 一: first\nD2 五 - 二: second\nE1 四 - reason", REFERENCE)
        self.assertTrue(result["valid"])
        self.assertEqual([e["character"] for e in result["entries"]], ["五", "五", "四"])
        self.assertEqual([e["label"] for e in result["entries"]], ["D1", "D2", "E1"])

    def test_caps_and_declarations(self):
        self.assertFalse(validate_selection(
            "\n".join(f"D{i} 五 - 一: overlap" for i in range(1, 42)) + "\nE: none", REFERENCE)["valid"])
        self.assertFalse(validate_selection("D1 五 - 一: overlap", REFERENCE)["valid"])
        self.assertFalse(validate_selection("D2 五 - 一: overlap\nE: none", REFERENCE)["valid"])
        self.assertFalse(validate_selection("D: none\nD: none\nE: none", REFERENCE)["valid"])

    def test_empty_other_required_is_valid_not_missing(self):
        self.assertTrue(validate_selection("D: none\nE: none", REFERENCE)["valid"])
        bad = {k: v for k, v in REFERENCE.items() if k != "otherRequiredCards"}
        self.assertFalse(validate_selection("D: none\nE: none", bad)["valid"])

    def test_chain_preserves_crlf_unicode_and_partial_ranges(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = ("字 with CRLF\r\n" * 2500).encode("utf-8")
            manifest = build_chain([("source.txt", source, 2400)], root / "chain", root / "manifest.json", Guard(), "fixture")
            copied = []
            self.assertGreater(len(manifest["segments"]), 1)
            for segment in manifest["segments"]:
                data = Path(segment["path"]).read_bytes()
                self.assertLess(len(data), 16000)
                lines = [line + b"\n" for line in data.split(b"\n")[:-1]]
                for part in segment["parts"]:
                    copied.extend(lines[part["segmentStart"] - 1:part["segmentEnd"]])
            self.assertEqual(b"".join(copied), ("字 with CRLF\r\n" * 2400).encode("utf-8"))
            self.assertEqual(json.loads((root / "manifest.json").read_bytes()), manifest)
            for path in root.rglob("*"):
                if path.is_file():
                    path.chmod(0o600)


if __name__ == "__main__":
    unittest.main()

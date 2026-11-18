import sys
import unittest
from pathlib import Path

WS = Path(r"C:\Users\stop-\n1-kanji-workspace")
OUT = WS / "scratch-134" / "review" / "fresh-independent-002" / "projected-successor-008"
sys.path.insert(0, str(OUT / "tools"))

from capacity008 import FIT, source_class
from capacity008_units import full_units


class CapacityClassificationTests(unittest.TestCase):
    def test_nested_native_extract_uses_inherited_extract_coefficient(self):
        self.assertEqual(source_class("reconciliation/evidence/native-紫-kotobank-extract.txt"),
                         ("extract", FIT["extract"] * 1.10))

    def test_nested_check_logs_use_inherited_check_coefficient(self):
        self.assertEqual(source_class("reconciliation/checks/quiz-safety.log"),
                         ("checks", FIT["checks"] * 1.10))
        self.assertEqual(source_class("reconciliation/checks/validate.json"),
                         ("checks", FIT["checks"] * 1.10))

    def test_parent_teaching_sources_keep_content_classes(self):
        self.assertEqual(source_class("parent/kanji/紫.md"), ("cards", FIT["cards"] * 1.10))
        self.assertEqual(source_class("parent/words/紫.md"), ("docs", FIT["docs"] * 1.10))

    def test_all_three_identity_indexes_use_title_index_coefficient(self):
        for path in (
            "evidence/published-title-index-e17.txt",
            "evidence/parent-title-index-ba80.txt",
            "evidence/title-index.txt",
        ):
            self.assertEqual(source_class(path), ("titleidx", FIT["titleidx"] * 1.10))

    def test_complete_union_uses_inherited_full_kd_coefficient(self):
        self.assertEqual(source_class("evidence/kanjidic2-complete-union.xml"), ("full-kd", 1.0))

    def test_optional_full_kd_unit_inventory_is_complete(self):
        raw = (OUT / "packet" / "evidence" / "kanjidic2-complete-union.xml").read_bytes()
        self.assertEqual(len(full_units(raw)), 85)


if __name__ == "__main__":
    unittest.main()

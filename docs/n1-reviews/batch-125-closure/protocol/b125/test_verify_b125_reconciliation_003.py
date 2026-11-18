import copy
import unittest

from verify_b125_reconciliation_003 import PARENT, verify_inventory


class CompleteInventoryTests(unittest.TestCase):
    def fixture(self):
        row = {"kanji": "x", "title": "fixture", "onyomi": ["on"], "kunyomi": ["kun"],
               "quizOnyomi": None, "quizKunyomi": [], "tags": [], "sha256": "hash"}
        return {"parent": PARENT, "count": 1, "cards": [copy.deepcopy(row)]}, {"x": row}

    def test_exact_inventory_retains_absent_versus_empty_practice(self):
        inventory, actual = self.fixture()
        verify_inventory(inventory, actual, lambda x: x)
        inventory["cards"][0]["quizKunyomi"] = None
        with self.assertRaises(ValueError):
            verify_inventory(inventory, actual, lambda x: x)

    def test_missing_duplicate_or_changed_card_is_rejected(self):
        inventory, actual = self.fixture()
        for change in ({"count": 2}, {"cards": []}, {"cards": inventory["cards"] * 2}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                verify_inventory({**inventory, **change}, actual, lambda x: x)
        inventory["cards"][0]["title"] = "changed"
        with self.assertRaises(ValueError):
            verify_inventory(inventory, actual, lambda x: x)

    def test_external_reading_in_raw_or_explicit_practice_is_not_hidden(self):
        for field in ("onyomi", "kunyomi", "quizOnyomi", "quizKunyomi"):
            inventory, actual = self.fixture()
            actual["x"][field] = ["external-label"]
            inventory["cards"] = [copy.deepcopy(actual["x"])]
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "external exact reading key"):
                verify_inventory(inventory, actual, lambda x: "\u307f\u306b\u304f\u3044" if x == "external-label" else x)


if __name__ == "__main__":
    unittest.main()

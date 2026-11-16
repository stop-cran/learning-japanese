import copy
import json
import unittest

from prepare_b125_confirmations_002 import PARENT, inventory_lines


class InventoryDerivativeTests(unittest.TestCase):
    def fixture(self):
        return {"parent": PARENT, "count": 1, "cards": [{
            "kanji": "x", "title": "exact; title", "onyomi": ["ON"], "kunyomi": ["ku.n"],
            "quizOnyomi": None, "quizKunyomi": [], "tags": ["tag"], "sha256": "hash",
        }]}

    def test_only_hashes_are_omitted_without_mutating_or_normalizing_source(self):
        value = self.fixture()
        before = copy.deepcopy(value)
        rows = [json.loads(line) for line in inventory_lines(value).decode().splitlines()]
        self.assertEqual(value, before)
        self.assertEqual(rows, [{k: v for k, v in value["cards"][0].items() if k != "sha256"}])
        self.assertIsNone(rows[0]["quizOnyomi"])
        self.assertEqual(rows[0]["quizKunyomi"], [])

    def test_missing_extra_or_duplicate_entries_are_rejected(self):
        value = self.fixture()
        for changed in ({**value, "count": 2}, {**value, "cards": value["cards"] * 2}):
            with self.assertRaises(ValueError):
                inventory_lines(changed)
        value["cards"][0]["unexpected"] = "not silently removed"
        with self.assertRaises(ValueError):
            inventory_lines(value)


if __name__ == "__main__":
    unittest.main()

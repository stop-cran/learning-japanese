import copy
import unittest

from verify_b134_payload import verify_support_inventory


class SupportInventoryTests(unittest.TestCase):
    def fixture(self):
        support = {"\u7d2b": ["\u7d2b"]}
        return support, {"supports": [["\u7d2b", "\u7d2b"]], "proseException": None}

    def test_complete_declared_support_inventory_is_required(self):
        support, selection = self.fixture()
        self.assertEqual(selection["supports"], verify_support_inventory(support, selection))
        for change in ("drop-member", "drop-word", "extra-word", "wrong-word"):
            altered = copy.deepcopy(support)
            if change == "drop-member":
                del altered["\u7d2b"]
            elif change == "drop-word":
                altered["\u7d2b"] = []
            elif change == "extra-word":
                altered["\u7d2b"].append("extra")
            else:
                altered["\u7d2b"] = ["wrong"]
            with self.subTest(change=change), self.assertRaises(ValueError):
                verify_support_inventory(altered, selection)

    def test_pair_omission_duplication_and_unapproved_changes_fail(self):
        support, selection = self.fixture()
        pairs = selection["supports"]
        variations = [[], pairs + pairs, [["\u7d2b", "wrong"]], pairs + [["extra", "extra"]]]
        for altered in variations:
            with self.subTest(pairs=altered), self.assertRaises(ValueError):
                verify_support_inventory(support, {"supports": altered, "proseException": None})
        with self.assertRaises(ValueError):
            verify_support_inventory(support, {"supports": pairs, "proseException": "unapproved"})


if __name__ == "__main__":
    unittest.main()

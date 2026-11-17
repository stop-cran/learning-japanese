import copy
import unittest

from verify_b133_payload import verify_support_inventory


class SupportInventoryTests(unittest.TestCase):
    def fixture(self):
        support = {"\u7434": ["\u7434"], "\u925b": ["\u925b\u7b46"], "\u6edd": ["\u6edd"]}
        pairs = [["\u7434", "\u7434"], ["\u925b", "\u925b\u7b46"], ["\u6edd", "\u6edd"]]
        return support, {"supports": pairs, "proseException": None}

    def test_complete_declared_support_inventory_is_required_for_every_member(self):
        support, selection = self.fixture()
        self.assertEqual(selection["supports"], verify_support_inventory(support, selection))
        for char in support:
            for change in ("drop-member", "drop-word", "extra-word", "wrong-word"):
                altered = copy.deepcopy(support)
                if change == "drop-member":
                    del altered[char]
                elif change == "drop-word":
                    altered[char] = []
                elif change == "extra-word":
                    altered[char].append("extra")
                else:
                    altered[char] = ["wrong"]
                with self.subTest(char=char, change=change), self.assertRaises(ValueError):
                    verify_support_inventory(altered, selection)

    def test_pair_omission_duplication_order_and_prose_exception_fail(self):
        support, selection = self.fixture()
        pairs = selection["supports"]
        variations = [pairs[:i] + pairs[i + 1:] for i in range(len(pairs))]
        variations += [pairs + [pairs[-1]], list(reversed(pairs)), pairs + [["extra", "extra"]]]
        for altered in variations:
            with self.subTest(pairs=altered), self.assertRaises(ValueError):
                verify_support_inventory(support, {"supports": altered, "proseException": None})
        with self.assertRaises(ValueError):
            verify_support_inventory(support, {"supports": pairs, "proseException": "unapproved"})


if __name__ == "__main__":
    unittest.main()

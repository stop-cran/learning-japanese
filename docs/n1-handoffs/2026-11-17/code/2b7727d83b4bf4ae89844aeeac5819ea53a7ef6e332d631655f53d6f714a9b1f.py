import unittest
from verify_b132_payload_v2 import verify_support_inventory

class SupportInventoryTests(unittest.TestCase):
    def test_exact_declared_support_and_reciprocal_pair_are_required(self):
        support = {"\u5893": ["\u5893"]}
        selection = {"supports": [["\u5893", "\u5893"]], "proseException": None}
        self.assertEqual(selection["supports"], verify_support_inventory(support, selection))
        for declared in ({}, {"\u5893": []}, {"\u5893": ["\u5893", "extra"]},
                         {"\u5893": ["\u5893"], "other": ["other"]}):
            with self.subTest(declared=declared), self.assertRaises(ValueError):
                verify_support_inventory(declared, selection)

    def test_pair_omission_duplication_and_unapproved_prose_changes_fail(self):
        support = {"\u5893": ["\u5893"]}
        for pairs, exception in (
            ([], None), ([["\u5893", "extra"]], None),
            ([["\u5893", "\u5893"], ["\u5893", "\u5893"]], None),
            ([["\u5893", "\u5893"]], "unexpected prose change"),
        ):
            with self.subTest(pairs=pairs, exception=exception), self.assertRaises(ValueError):
                verify_support_inventory(support, {"supports": pairs, "proseException": exception})


if __name__ == "__main__":
    unittest.main()

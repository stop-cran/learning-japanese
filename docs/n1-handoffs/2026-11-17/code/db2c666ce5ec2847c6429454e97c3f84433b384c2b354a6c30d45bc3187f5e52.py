import json
import unittest

from prepare_b129_confirmations_v3 import compact_membership, factor_rows


class FactoringTests(unittest.TestCase):
    def test_queries_preserve_order_zero_matches_and_inverse(self):
        value = {"queries": {"a": ["1", "2"], "b": [], "c": ["1"]},
                 "recordPredicates": {"1": ["a", "c"], "2": ["a"]}, "zeroMatches": ["b"]}
        lines = [json.loads(line) for line in compact_membership(json.dumps(value).encode()).splitlines()]
        self.assertEqual(lines[1:], [["a", ["1", "2"]], ["b", []], ["c", ["1"]]])
        value["recordPredicates"]["1"] = ["a"]
        with self.assertRaises(ValueError):
            compact_membership(json.dumps(value).encode())

    def test_factored_rows_are_identical_after_shared_fields_are_restored(self):
        rows = [{"pair": ["A", "B"], "guard": False, "guardSemantics": "direct", "coverage": "bounded"},
                {"pair": ["A", "C"], "guard": True, "guardSemantics": "direct", "coverage": "bounded"}]
        raw = ("\n".join(json.dumps(item) for item in [{}, *rows]) + "\n").encode()
        factored = [json.loads(line) for line in factor_rows(raw).splitlines()]
        self.assertEqual([{**row, **factored[0]["sharedRowFields"]} for row in factored[1:]], rows)
        rows[1]["coverage"] = "different"
        with self.assertRaises(ValueError):
            factor_rows(("\n".join(json.dumps(item) for item in [{}, *rows]) + "\n").encode())


if __name__ == "__main__":
    unittest.main()

import unittest
from pathlib import Path

from closure_paths import resolve_binding
from common import WS


class ClosurePathTests(unittest.TestCase):
    def test_both_recorded_bases_resolve_to_the_same_original(self):
        expected = WS / "scratch-117" / "review" / "confirm" / "receipt.json"
        for raw in (r"..\scratch-117\review\confirm\receipt.json",
                    r"scratch-117\review\confirm\receipt.json"):
            resolved, rule = resolve_binding(raw)
            self.assertEqual(expected, resolved)
            self.assertIsNotNone(rule)

    def test_absolute_bindings_are_unchanged(self):
        path = WS / "scratch-117" / "receipt.json"
        self.assertEqual((path, None), resolve_binding(path))

    def test_unknown_and_escaping_relative_paths_fail(self):
        for raw in (r"..\..\receipt.json", r"receipt.json", r"scratch-116\review\confirm\a.json",
                    r"scratch-117\review\confirm\..\..\secret",
                    r"..\scratch-117\review\confirm\..\secret"):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                resolve_binding(raw)


if __name__ == "__main__":
    unittest.main()

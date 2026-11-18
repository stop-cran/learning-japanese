import copy
import json
import unittest

from common import frozen
from verify_b130_integration_closure import BUNDLE, check_context


class ClosureContextTests(unittest.TestCase):
    def test_exact_contexts_and_changed_admissions(self):
        for mode, attempt in (("author", "author-gates-001"), ("committed", "committed-gates-002")):
            directory = BUNDLE / "evidence" / attempt
            summary = json.loads(frozen(directory / "summary.json"))
            admission = json.loads(frozen(directory / "admission.json"))
            check_context(summary, admission, mode)
            for kind in ("tree", "parent", "order", "scope", "ram"):
                with self.subTest(mode=mode, kind=kind):
                    wrong, admit = copy.deepcopy(summary), copy.deepcopy(admission)
                    if kind == "tree":
                        admit["tree"] = "0" * 40
                    elif kind == "parent":
                        wrong["parent"] = "0" * 40
                    elif kind == "order":
                        wrong["checks"] = list(reversed(wrong["checks"]))
                    elif kind == "scope":
                        wrong["publishedBaseScope"] = wrong["head"]
                    else:
                        admit["memory"]["freeRamBeforeBytes"] = 2 * 1024**3
                    with self.assertRaises(ValueError):
                        check_context(wrong, admit, mode)


if __name__ == "__main__":
    unittest.main()

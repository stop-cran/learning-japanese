import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import confirm_b133
from b133_confirmation_capacity import confirmation_cost


class Guard:
    def check(self):
        pass


class CapacityTests(unittest.TestCase):
    def test_exact_complete_chain_uses_existing_calibration_without_changing_gate(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sources = [("initial-report/report.md", b"Prior report.\n", None),
                       ("evidence/external/source-extract.txt", b"Complete section.\n", None)]
            chain = confirm_b133.build_chain(sources, root / "segments", root / "chain.json", Guard(), "fixture")
            result = confirmation_cost(chain)
            self.assertEqual(result["chainBytes"], sum(row["bytes"] for row in chain["segments"]))
            self.assertLess(result["tokens"], result["chainBytes"])
            self.assertGreater(result["tokens"], len(sources[0][1]))
            changed = copy.deepcopy(chain)
            changed["sources"][0]["selectedLines"] += 1
            with self.assertRaises(ValueError):
                confirmation_cost(changed)
            changed = copy.deepcopy(chain)
            changed["segments"][0]["parts"][0]["a"] = 2
            with self.assertRaises(ValueError):
                confirmation_cost(changed)

    def test_capacity_never_relaxes_the_existing_startup_gate(self):
        import confirm_b133_v2 as controller
        estimate = {"chainBytes": 200000, "tokens": 90000, "method": "synthetic"}
        observed = {"status": "PASS", "family": "claude", "lastInputTokens": 551959}
        with patch.object(controller, "confirmation_cost", return_value=estimate):
            result = controller.capacity(observed, {"segments": [object()]}, 8000)
            self.assertEqual(result["projectedPeak"], 691959)
            self.assertEqual(result["gate"], 700000)
            with self.assertRaises(ValueError):
                controller.capacity({**observed, "lastInputTokens": 560000},
                                    {"segments": [object()]}, 8000)


if __name__ == "__main__":
    unittest.main()

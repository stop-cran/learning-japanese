import copy
import json
import unittest

from common import frozen
from verify_b130_integration_evidence import BUNDLE, check_context


class IntegrationEvidenceTests(unittest.TestCase):
    def test_actual_both_gate_contexts_and_changed_scope(self):
        for mode in ("author", "committed"):
            directory = BUNDLE / "evidence" / f"{mode}-gates-001"
            summary = json.loads(frozen(directory / "summary.json"))
            admission = json.loads(frozen(directory / "admission.json"))
            check_context(summary, admission, mode)
            for field, value in (("parentsInOrder", list(reversed(summary["parentsInOrder"]))),
                                 ("commandsUnchanged", False), ("serial", False),
                                 ("manifestSha256", "0" * 64)):
                with self.subTest(mode=mode, field=field), self.assertRaises(ValueError):
                    check_context({**summary, field: value}, admission, mode)
            bad = copy.deepcopy(admission)
            bad["memory"]["minimumObservedFreeRamBytes"] = 1024 ** 3 - 1
            with self.assertRaises(ValueError):
                check_context(summary, bad, mode)


if __name__ == "__main__":
    unittest.main()

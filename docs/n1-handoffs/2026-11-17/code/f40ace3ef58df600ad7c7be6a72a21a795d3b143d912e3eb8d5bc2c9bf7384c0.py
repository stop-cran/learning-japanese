import copy
import json
import unittest

from b130_context_held_initials import require_context_hold
from common import WS, frozen


class ContextHeldClosureTests(unittest.TestCase):
    def fixture(self):
        root = WS / "scratch-130" / "review"
        held = json.loads(frozen(root / "N1-B130-CLAUDE-001-hold.json"))
        records = [json.loads(frozen(held[key]["path"], held[key]["sha256"]))
                   for key in ("final", "structure", "context")]
        return held, *records

    def test_actual_compacted_report_can_be_preserved_but_never_accepted(self):
        held, mechanics, structure, context = self.fixture()
        require_context_hold(held, mechanics, structure, context, 130, held["candidate"])
        for field in ("reviewAccepted", "finalAcceptance"):
            with self.subTest(field=field), self.assertRaises(ValueError):
                require_context_hold({**held, field: True}, mechanics, structure, context, 130, held["candidate"])

    def test_unrelated_failure_or_different_evidence_is_not_relabelled(self):
        for field, value in (
            ("status", "PASS"), ("compactions", []),
            ("errors", ["Unrelated context error"]),
        ):
            held, mechanics, structure, context = self.fixture()
            with self.subTest(field=field), self.assertRaises(ValueError):
                require_context_hold(held, mechanics, structure, {**context, field: value}, 130, held["candidate"])
        held, mechanics, structure, context = self.fixture()
        bad = copy.deepcopy(held)
        bad["context"]["sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            require_context_hold(bad, mechanics, structure, context, 130, held["candidate"])
        with self.assertRaises(ValueError):
            require_context_hold(held, {**mechanics, "problems": mechanics["problems"] + ["another failure"]},
                                 structure, context, 130, held["candidate"])


if __name__ == "__main__":
    unittest.main()

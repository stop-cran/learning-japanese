import copy
import unittest

from common import CHECKS
from finalize_b123_v3 import (
    FINALS, HISTORY, INITIALS, PARENT, REPLACED, REPLACEMENT_ORIGIN, check_history, make_ledger,
)
from record_publication import delivery_accounting
import test_finalize_b123_v2 as v2_tests


class ReplacementFinalClosureTests(unittest.TestCase):
    def fixture(self):
        config, candidate, provenance, first, second, current = v2_tests.ThirdRevisionClosureTests.fixture(self)
        lineage = []
        for family in INITIALS:
            original = {"family": family, "session": family, "reviewerOrigin": "original",
                        "replacementFor": None, "replayedFrom": None, "originalSession": None}
            lineage.extend([
                {**original, "run": INITIALS[family], "role": "initial", "snapshot": config["candidate"],
                 "rawVerdict": "NEEDS FIX", "finalAcceptance": False},
                {**original, "run": HISTORY[family], "role": "intermediate", "snapshot": PARENT,
                 "rawVerdict": "CONFIRMED" if family == "claude" else "UNVERIFIED",
                 "confirmationAcceptedOnSnapshot": family == "claude", "finalAcceptance": False,
                 "priorRun": None},
            ])
            final = {**original, "run": FINALS[family], "role": "final", "snapshot": candidate,
                     "rawVerdict": "CONFIRMED", "confirmationAcceptedOnSnapshot": True,
                     "finalAcceptance": True, "priorRun": HISTORY[family]}
            if family in REPLACED:
                final.update({"session": "fresh", "reviewerOrigin": REPLACEMENT_ORIGIN,
                              "replacementFor": REPLACED[family], "originalSession": family,
                              "replayedFrom": f"runs/{FINALS[family]}/replayed-from-spec.json"})
            lineage.append(final)
        provenance.update({"reviewLineage": lineage, "finalRuns": list(FINALS.values())})
        return config, candidate, provenance, first, second, current

    def test_accepts_only_attributed_claude_replacement_and_original_gpt(self):
        config, candidate, provenance, *_ = self.fixture()
        check_history(provenance, candidate, config)
        claude_final = 2
        gpt_final = 5
        for index, key, value in (
            (claude_final, "reviewerOrigin", "original"), (claude_final, "replacementFor", None),
            (claude_final, "session", "claude"), (claude_final, "originalSession", "other"),
            (claude_final, "replayedFrom", None), (claude_final, "priorRun", None),
            (gpt_final, "session", "fresh"), (gpt_final, "reviewerOrigin", REPLACEMENT_ORIGIN),
            (gpt_final, "replacementFor", "N1-B123-GPT-CONFIRM-003"),
            (1, "reviewerOrigin", REPLACEMENT_ORIGIN), (4, "rawVerdict", "CONFIRMED"),
        ):
            broken = copy.deepcopy(provenance)
            broken["reviewLineage"][index][key] = value
            with self.subTest(index=index, key=key), self.assertRaises(ValueError):
                check_history(broken, candidate, config)

    def test_rejects_superseded_or_void_finals(self):
        config, candidate, provenance, *_ = self.fixture()
        for run in ("N1-B123-CLAUDE-CONFIRM-003", "N1-B123-CLAUDE-REPLACEMENT-CONFIRM-005"):
            broken = copy.deepcopy(provenance)
            broken["reviewLineage"][2]["run"] = run
            broken["finalRuns"] = [run, FINALS["gpt"]]
            with self.subTest(run=run), self.assertRaises(ValueError):
                check_history(broken, candidate, config)

    def test_ledger_names_replacement_without_premature_delivery(self):
        config, candidate, provenance, first, second, current = self.fixture()
        ledger = make_ledger(config, candidate, provenance, "closure", first, second, current)
        self.assertIn("replacement", ledger["review"]["identity"])
        self.assertNotIn("both original reviewers confirmed", ledger["review"]["identity"])
        self.assertEqual(ledger["review"]["replacements"],
                         [{"run": FINALS["claude"], "replacementFor": REPLACED["claude"],
                           "reviewerOrigin": REPLACEMENT_ORIGIN}])
        self.assertEqual(ledger["review"]["finalRuns"], list(FINALS.values()))
        self.assertEqual(ledger["published"], [])
        self.assertEqual(delivery_accounting(ledger),
                         {"delivered": 253, "n1Additions": 247, "n2Placements": 6, "remaining": 975})


if __name__ == "__main__":
    unittest.main()

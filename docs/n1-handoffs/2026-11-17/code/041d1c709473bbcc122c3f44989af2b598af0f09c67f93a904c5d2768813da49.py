import copy
import unittest

from common import CHECKS
from prepare_b125_candidate import (
    BASE, BOUNDED_RUNNER_SHA, CANDIDATE, GATE_RUNNER_SHA, verify_summary,
)


class SummaryTests(unittest.TestCase):
    def test_two_distinct_runner_bindings_and_exact_candidate_are_required(self):
        value = {
            "batch": 125, "mode": "committed", "head": CANDIDATE, "base": BASE,
            "status": "PASS", "checks": list(CHECKS), "manifestSha256": "manifest",
            "runnerSha256": GATE_RUNNER_SHA, "boundedRunnerSha256": BOUNDED_RUNNER_SHA,
        }
        verify_summary(value, "committed", CANDIDATE, "manifest")
        for field, replacement in (("head", BASE), ("boundedRunnerSha256", GATE_RUNNER_SHA),
                                   ("runnerSha256", BOUNDED_RUNNER_SHA),
                                   ("checks", list(CHECKS)[:-1]), ("mode", "author")):
            changed = copy.deepcopy(value)
            changed[field] = replacement
            with self.subTest(field=field), self.assertRaises(ValueError):
                verify_summary(changed, "committed", CANDIDATE, "manifest")


if __name__ == "__main__":
    unittest.main()

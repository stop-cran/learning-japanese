import copy
import sys
import unittest

import prepare_b127_candidate as module


class GateBindingTests(unittest.TestCase):
    def setUp(self):
        self.summary = {
            "batch": "127", "mode": "committed", "status": "PASS", "base": module.BASE,
            "startingHead": module.CANDIDATE, "checks": list(module.ORDER),
            "manifestSha256": "manifest", "runnerSha256": "runner", "commonHelperSha256": "helper",
            "guardSha256": module.GUARD_SHA, "serial": True, "waitTimeoutSeconds": 0.1,
            "cleanupTimeoutSecondsPerStage": 10, "finalMemory": {"breach": None},
        }
        self.commands = {name: [name] for name in module.ORDER}
        self.receipts = {
            name: {"command": [sys.executable, "-B", name], "commonHelperSha256": "helper",
                   "cleanupTimeoutSecondsPerStage": 10, "cleanupError": None, "activeError": None,
                   "startedAt": f"2026-11-16T00:00:{index * 2:02}+00:00",
                   "completedAt": f"2026-11-16T00:00:{index * 2 + 1:02}+00:00"}
            for index, name in enumerate(module.ORDER)
        }

    def summary_check(self, value):
        module.verify_summary(value, "committed", module.CANDIDATE, "manifest", "runner", "helper")

    def test_exact_snapshot_and_execution_pass(self):
        self.summary_check(self.summary)
        module.verify_execution(self.receipts, self.commands, "helper")

    def test_stale_snapshot_or_reordered_checks_fail(self):
        for key, value in (("startingHead", module.BASE), ("checks", list(reversed(module.ORDER)))):
            altered = copy.deepcopy(self.summary)
            altered[key] = value
            with self.assertRaisesRegex(ValueError, "Gate summary"):
                self.summary_check(altered)

    def test_overlap_fails(self):
        self.receipts["quiz-safety"]["startedAt"] = self.receipts["lint"]["startedAt"]
        with self.assertRaisesRegex(ValueError, "overlap"):
            module.verify_execution(self.receipts, self.commands, "helper")

    def test_wrong_executed_command_fails(self):
        self.receipts["lint"]["command"][-1] = "different-command"
        with self.assertRaisesRegex(ValueError, "executed gate command"):
            module.verify_execution(self.receipts, self.commands, "helper")

    def test_cleanup_failure_cannot_be_accepted(self):
        self.receipts["lint"]["cleanupError"] = "timeout"
        with self.assertRaisesRegex(ValueError, "cleanup"):
            module.verify_execution(self.receipts, self.commands, "helper")


if __name__ == "__main__":
    unittest.main()

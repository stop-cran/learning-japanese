import copy
import sys
import unittest

import b129_revision_gates as gates


class RevisionGateTests(unittest.TestCase):
    def setUp(self):
        memory = {
            "breach": None, "freeRamBeforeBytes": 3 * 1024 ** 3,
            "minimumObservedFreeRamBytes": 2 * 1024 ** 3,
            "abortThresholdBytes": 1024 ** 3, "samplingIntervalSeconds": 0.25,
        }
        self.summary = {
            "batch": "129-reconciliation-001", "mode": "committed", "status": "PASS",
            "batchScopeBase": gates.BASE, "requiredCommitParent": gates.PARENT,
            "startingHead": "c" * 40, "checks": list(gates.ORDER), "serial": True,
            "manifestSha256": "m", "runnerSha256": "r", "commonHelperSha256": "h",
            "guardSha256": gates.GUARD_SHA, "waitTimeoutSeconds": 0.1,
            "cleanupTimeoutSecondsPerStage": 10, "finalMemory": memory,
            "logs": {name: {} for name in gates.ORDER},
        }
        self.admission = {
            "head": "c" * 40, "mode": "committed", "batchScopeBase": gates.BASE,
            "commitParent": gates.PARENT, "manifestBeforeSha256": "m", "memory": memory,
        }

    def check(self, mode="committed"):
        gates.check_context(self.summary, self.admission, mode, "c" * 40, "m", "r", "h")

    def test_exact_snapshot_and_author_predecessor(self):
        self.check()
        self.summary.update(mode="author", startingHead=gates.PARENT)
        self.admission.update(mode="author", head=gates.PARENT)
        self.check("author")

    def test_wrong_snapshot_or_changed_manifest_rejected(self):
        for field in ("head", "commitParent", "batchScopeBase", "manifestBeforeSha256"):
            with self.subTest(field=field):
                original = self.admission[field]
                self.admission[field] = "wrong"
                with self.assertRaises(ValueError):
                    self.check()
                self.admission[field] = original

    def test_missing_gate_or_low_memory_rejected(self):
        original = copy.deepcopy(self.summary)
        self.summary["checks"].pop()
        with self.assertRaises(ValueError):
            self.check()
        self.summary = original
        self.summary["finalMemory"]["minimumObservedFreeRamBytes"] = 1024 ** 3 - 1
        with self.assertRaises(ValueError):
            self.check()

    def test_overlapping_execution_or_wrong_command_rejected(self):
        receipts = {}
        for index, name in enumerate(gates.ORDER):
            receipts[name] = {
                "startedAt": f"2026-11-16T08:{index:02d}:00+00:00",
                "completedAt": f"2026-11-16T08:{index:02d}:30+00:00",
                "command": [sys.executable, "-B", *map(str, gates.commands()[name])],
                "commonHelperSha256": "h", "cleanupTimeoutSecondsPerStage": 10,
                "activeError": None, "cleanupError": None,
            }
        gates.verify_execution(receipts, gates.commands(), "h")
        receipts[gates.ORDER[1]]["startedAt"] = receipts[gates.ORDER[0]]["startedAt"]
        with self.assertRaises(ValueError):
            gates.verify_execution(receipts, gates.commands(), "h")
        receipts[gates.ORDER[1]]["startedAt"] = "2026-11-16T08:01:00+00:00"
        receipts["lint"]["command"][-1] = "wrong-member"
        with self.assertRaises(ValueError):
            gates.verify_execution(receipts, gates.commands(), "h")


if __name__ == "__main__":
    unittest.main()

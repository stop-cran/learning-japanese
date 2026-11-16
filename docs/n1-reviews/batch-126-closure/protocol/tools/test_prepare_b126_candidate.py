import copy
import unittest

from prepare_b126_candidate import BASE, GUARD_SHA, ORDER, verify_serial, verify_summary


class CandidateGateTests(unittest.TestCase):
    def test_summary_binds_actual_snapshot_and_serial_runner(self):
        value = {
            "batch": "126", "mode": "committed", "status": "PASS", "base": BASE,
            "startingHead": "candidate", "checks": list(ORDER), "manifestSha256": "manifest",
            "runnerSha256": "runner", "guardSha256": GUARD_SHA, "serial": True,
            "waitTimeoutSeconds": 0.1, "finalMemory": {"breach": None},
        }
        verify_summary(value, "committed", "candidate", "manifest", "runner")
        for key, replacement in (
            ("startingHead", BASE), ("checks", list(reversed(ORDER))),
            ("manifestSha256", "different"), ("runnerSha256", "different"),
            ("serial", False), ("waitTimeoutSeconds", 1), ("finalMemory", {"breach": "low RAM"}),
        ):
            changed = copy.deepcopy(value)
            changed[key] = replacement
            with self.subTest(key=key), self.assertRaises(ValueError):
                verify_summary(changed, "committed", "candidate", "manifest", "runner")

    def test_overlapping_reversed_or_naive_gate_times_fail(self):
        receipts = {
            name: {"startedAt": f"2026-11-16T01:{i:02d}:00+00:00",
                   "completedAt": f"2026-11-16T01:{i:02d}:30+00:00"}
            for i, name in enumerate(ORDER)
        }
        verify_serial(receipts)
        for started, completed in (
            ("2026-11-16T01:00:29+00:00", "2026-11-16T01:01:30+00:00"),
            ("2026-11-16T01:01:31+00:00", "2026-11-16T01:01:30+00:00"),
            ("2026-11-16T01:01:00", "2026-11-16T01:01:30"),
        ):
            changed = copy.deepcopy(receipts)
            changed[ORDER[1]] = {"startedAt": started, "completedAt": completed}
            with self.subTest(started=started), self.assertRaises(ValueError):
                verify_serial(changed)


if __name__ == "__main__":
    unittest.main()

import copy
import unittest

from run_b133_closure_checks import BASE, CANDIDATE, ORDER
from verify_b133_teaching_revision_v2 import check_summary, inventory_files

REV = "1" * 40
MEM = {"freeRamBeforeBytes": 4 << 30, "freeRamAfterBytes": 4 << 30, "minimumObservedFreeRamBytes": 4 << 30,
       "peakWorkingSetBytes": 1, "peakScope": "x", "abortThresholdBytes": 1 << 30,
       "samplingIntervalSeconds": 0.25, "additionalChecks": "x", "breach": None}


def fixtures():
    admission = {"head": REV, "parent": CANDIDATE, "originalBatchBase": BASE, "mode": "committed", "memory": MEM}
    summary = {"status": "PASS", "mode": "committed", "head": REV, "parent": CANDIDATE,
               "originalBatchBase": BASE, "checks": list(ORDER), "serial": True, "manifestSha256": "m",
               "runnerSha256": "w", "originalRunnerSha256": "r",
               "logs": {n: {"logSha256": "a", "receiptSha256": "b"} for n in ORDER}, "finalMemory": MEM}
    return summary, admission


class ActualSchemaTests(unittest.TestCase):
    def test_inventory_requires_hash_and_size_objects_without_self_entry(self):
        good = {"files": {"after-x.md": {"sha256": "a" * 64, "bytes": 3}}}
        self.assertEqual(inventory_files(good), good["files"])
        for bad in ({"files": {"x": "a" * 64}}, {"files": {}},
                    {"files": {"inventory.json": {"sha256": "a" * 64, "bytes": 1}}},
                    {"files": {"x": {"sha256": "a" * 64, "bytes": "3"}}}):
            with self.assertRaises(Exception):
                inventory_files(bad)

    def test_committed_summary_binds_revision_wrapper_and_original_runner(self):
        summary, admission = fixtures()
        check_summary(summary, admission, REV, "m", "w", "r")
        for key, value in (("mode", "author"), ("head", CANDIDATE), ("runnerSha256", "r"),
                           ("originalRunnerSha256", "w"), ("checks", ORDER[:-1]), ("manifestSha256", "x")):
            changed = copy.deepcopy(summary)
            changed[key] = value
            with self.assertRaises(Exception):
                check_summary(changed, admission, REV, "m", "w", "r")
        stale = dict(admission, mode="author", head=CANDIDATE)
        with self.assertRaises(Exception):
            check_summary(summary, stale, REV, "m", "w", "r")


if __name__ == "__main__":
    unittest.main()

import copy
import unittest
from datetime import datetime, timedelta, timezone

from admit_b133_source_reconciliation import AUTHOR, COORDINATOR, assess_snapshot


class AdmissionControls(unittest.TestCase):
    def setUp(self):
        self.now = datetime.now(timezone.utc)
        self.status = {
            "summary": {"total": 3},
            "sessions": [
                {"id": COORDINATOR, "activity": {"status": "busy"}, "is_running": True},
                {"id": AUTHOR, "activity": {"status": "idle"}, "is_running": False},
                {"id": "unrelated", "activity": {"status": "idle"}, "is_running": False},
            ],
        }
        self.roster = [{"id": row["id"]} for row in self.status["sessions"]]

    def check(self, status=None, roster=None, observed=None):
        return assess_snapshot(status if status is not None else self.status,
                               roster if roster is not None else self.roster,
                               observed if observed is not None else self.now, self.now)

    def test_complete_live_snapshot_and_exact_time_boundary(self):
        self.assertEqual(self.check(), 3)
        self.assertEqual(self.check(observed=self.now - timedelta(seconds=119)), 3)
        for observed in (self.now - timedelta(seconds=120), self.now + timedelta(seconds=1)):
            with self.subTest(observed=observed), self.assertRaises(ValueError):
                self.check(observed=observed)

    def test_unknown_busy_running_and_waiting_sessions_block(self):
        for index in (1, 2):
            for change in ({"activity": {"status": "unknown"}}, {"activity": {"status": "busy"}},
                           {"is_running": True}, {"awaiting_user_input": True},
                           {"awaiting_plan_approval": True}):
                status = copy.deepcopy(self.status)
                status["sessions"][index].update(change)
                with self.subTest(index=index, change=change), self.assertRaises(ValueError):
                    self.check(status=status)
        status = copy.deepcopy(self.status)
        del status["sessions"][1]["is_running"]
        with self.assertRaises(ValueError):
            self.check(status=status)

    def test_filtered_mismatched_and_duplicate_snapshots_block(self):
        for roster in (self.roster[:-1], [self.roster[0], self.roster[1], self.roster[1]],
                       [self.roster[0], self.roster[1], {"id": "different"}]):
            with self.subTest(roster=roster), self.assertRaises(ValueError):
                self.check(roster=roster)
        status = copy.deepcopy(self.status)
        status["summary"]["total"] += 1
        with self.assertRaises(ValueError):
            self.check(status=status)


if __name__ == "__main__":
    unittest.main()

import unittest

from common import COORDINATOR
from scoped_admission import FLOOR, REPOSITORY, assess_status


NAME = "B122 Claude review 001"


def session(identity, state="idle", **extra):
    return {"id": identity, "name": identity, "activity": {"status": state},
            "is_running": state == "busy", **extra}


def snapshot(*sessions):
    rows = [session(COORDINATOR, "busy"), *sessions]
    return {"summary": {"total": len(rows)}, "sessions": rows}


class ScopedAdmissionTests(unittest.TestCase):
    def test_unrelated_android_work_does_not_reserve_machine(self):
        status = snapshot(session("android", "busy", project_repo="stop-cran/kanji-cards-android"))
        result = assess_status(status, NAME, FLOOR + 1)
        self.assertTrue(result["statusAllowsAdmission"])
        self.assertEqual([s["id"] for s in result["unrelatedActiveSessions"]], ["android"])
        self.assertEqual(len(result["activeSessions"]), 2)

    def test_active_author_or_reviewer_blocks(self):
        for role in ("author", "reviewer"):
            with self.subTest(role=role):
                result = assess_status(
                    snapshot(session(role, "busy", coordinating_creator_session_id=COORDINATOR)),
                    NAME, FLOOR + 1)
                self.assertFalse(result["statusAllowsAdmission"])
                self.assertEqual(result["blockingSessions"][0]["id"], role)

    def test_descendants_are_found_independent_of_snapshot_order(self):
        result = assess_status(snapshot(
            session("grandchild", "busy", creator_session_id="child"),
            session("child", creator_session_id=COORDINATOR),
        ), NAME, FLOOR + 1)
        self.assertFalse(result["statusAllowsAdmission"])
        self.assertIn("grandchild", result["scope"]["sessionIds"])

    def test_uncoordinated_content_session_still_blocks(self):
        result = assess_status(
            snapshot(session("content", "busy", project_repo=REPOSITORY)), NAME, FLOOR + 1)
        self.assertFalse(result["statusAllowsAdmission"])

    def test_unknown_and_running_scoped_states_fail_closed(self):
        for state, running in (("unknown", False), ("idle", True)):
            with self.subTest(state=state):
                status = snapshot(session("child", state, is_running=running,
                                          creator_session_id=COORDINATOR))
                self.assertFalse(assess_status(status, NAME, FLOOR + 1)["statusAllowsAdmission"])

    def test_same_name_blocks_even_if_unrelated_and_idle(self):
        status = snapshot(session("duplicate", name=NAME))
        self.assertFalse(assess_status(status, NAME, FLOOR + 1)["statusAllowsAdmission"])

    def test_ram_floor_remains_exclusive(self):
        for available in (FLOOR - 1, FLOOR):
            with self.subTest(available=available):
                result = assess_status(snapshot(), NAME, available)
                self.assertFalse(result["startupFloorMet"])
                self.assertFalse(result["statusAllowsAdmission"])
        self.assertTrue(assess_status(snapshot(), NAME, FLOOR + 1)["statusAllowsAdmission"])

    def test_rejects_filtered_or_ambiguous_snapshots(self):
        invalid = [
            {"summary": {"total": 1}, "sessions": []},
            {"summary": {"total": 1}, "sessions": [session("not-coordinator")]},
            snapshot(session(COORDINATOR)),
            snapshot(session(None)),
        ]
        for status in invalid:
            with self.subTest(status=status):
                with self.assertRaises(ValueError):
                    assess_status(status, NAME, FLOOR + 1)


if __name__ == "__main__":
    unittest.main()

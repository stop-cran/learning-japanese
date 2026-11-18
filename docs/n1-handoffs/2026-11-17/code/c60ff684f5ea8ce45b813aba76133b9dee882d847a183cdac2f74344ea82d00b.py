import unittest

from common import COORDINATOR
from scoped_admission import FLOOR, REPOSITORY
from scoped_confirmation_admission import assess_confirmation_status
from test_scoped_admission import session, snapshot


class ConfirmationAdmissionTests(unittest.TestCase):
    def status(self, *others, **reviewer):
        return snapshot(session("reviewer", name="Original review",
                                creator_session_id=COORDINATOR, **reviewer), *others)

    def test_original_reviewer_is_reused_while_unrelated_android_runs(self):
        result = assess_confirmation_status(
            self.status(session("android", "busy", project_repo="stop-cran/kanji-cards-android")),
            "reviewer", FLOOR + 1)
        self.assertTrue(result["statusAllowsAdmission"])
        self.assertTrue(result["originalSessionNameUnique"])
        self.assertEqual([s["id"] for s in result["unrelatedActiveSessions"]], ["android"])

    def test_active_n1_author_or_other_reviewer_blocks(self):
        for extra in (
            session("author", "busy", creator_session_id=COORDINATOR),
            session("another", "busy", project_repo=REPOSITORY),
        ):
            with self.subTest(extra=extra):
                self.assertFalse(assess_confirmation_status(
                    self.status(extra), "reviewer", FLOOR + 1)["statusAllowsAdmission"])

    def test_busy_unknown_or_running_original_reviewer_blocks(self):
        for state, running in (("busy", True), ("unknown", False), ("idle", True)):
            with self.subTest(state=state):
                self.assertFalse(assess_confirmation_status(
                    self.status(state=state, is_running=running),
                    "reviewer", FLOOR + 1)["statusAllowsAdmission"])

    def test_floor_is_still_exclusive(self):
        for available in (FLOOR - 1, FLOOR):
            with self.subTest(available=available):
                self.assertFalse(assess_confirmation_status(
                    self.status(), "reviewer", available)["statusAllowsAdmission"])

    def test_missing_duplicate_foreign_or_blocked_original_is_rejected(self):
        invalid = [
            snapshot(),
            self.status(session("duplicate", name="Original review")),
            snapshot(session("reviewer", name="Original review")),
            self.status(awaiting_user_input=True),
            self.status(awaiting_plan_approval=True),
        ]
        for status in invalid:
            with self.subTest(status=status), self.assertRaises(ValueError):
                assess_confirmation_status(status, "reviewer", FLOOR + 1)

    def test_full_snapshot_validation_is_retained(self):
        status = self.status()
        status["summary"]["total"] += 1
        with self.assertRaises(ValueError):
            assess_confirmation_status(status, "reviewer", FLOOR + 1)


if __name__ == "__main__":
    unittest.main()

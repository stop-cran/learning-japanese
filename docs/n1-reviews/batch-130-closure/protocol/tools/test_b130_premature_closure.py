import json
import unittest
from unittest.mock import Mock

from b130_excluded_initials_v2 import archive_excluded, require_premature_hold
from common import WS, frozen


class PrematureClosureTests(unittest.TestCase):
    def fixture(self):
        root = WS / "scratch-130" / "review"
        path = root / "N1-B130-CLAUDE-002-hold.json"
        held = json.loads(frozen(path))
        phase, audit = [json.loads(frozen(held[key]["path"], held[key]["sha256"]))
                        for key in ("phase1", "audit")]
        return root, path, held, phase, audit

    def test_actual_incomplete_run_is_preservable_only_as_excluded(self):
        _, _, held, phase, audit = self.fixture()
        require_premature_hold(held, phase, audit, 130, held["candidate"])
        for field in ("reviewAccepted", "finalAcceptance"):
            with self.subTest(field=field), self.assertRaises(ValueError):
                require_premature_hold({**held, field: True}, phase, audit, 130, held["candidate"])

    def test_completed_coverage_different_events_or_allowed_phase2_are_rejected(self):
        _, _, held, phase, audit = self.fixture()
        for field, value in (("readyForPhase2", True), ("coreRead", 87), ("eventsSha256", "0" * 64)):
            with self.subTest(field=field), self.assertRaises(ValueError):
                require_premature_hold(held, {**phase, field: value}, audit, 130, held["candidate"])

    def test_archive_does_not_invent_report_or_phase2_and_rejects_duplicate_acceptance(self):
        root, path, held, _, _ = self.fixture()
        copied, bound, dumped, chained = Mock(), Mock(), Mock(), Mock(return_value={"segments": 87})
        support = Mock()
        support.bounded_audit.return_value = {"status": "VOID"}
        args = (130, held["candidate"], set(), copied, bound, dumped, chained, support, root)
        result = archive_excluded([path], *args)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["coreRead"], 79)
        self.assertIsNone(result[0]["rawVerdict"])
        self.assertFalse(result[0]["reviewAccepted"])
        self.assertEqual(chained.call_count, 1)
        archived_names = [call.args[1] for callback in (copied, bound, dumped)
                          for call in callback.call_args_list]
        self.assertFalse(any("report.md" in name or "phase2" in name or "extension" in name
                             for name in archived_names))
        with self.assertRaisesRegex(ValueError, "accepted or duplicated"):
            archive_excluded([path], 130, held["candidate"], {held["run"]},
                             copied, bound, dumped, chained, support, root)
        with self.assertRaisesRegex(ValueError, "accepted or duplicated"):
            archive_excluded([path, path], *args)


if __name__ == "__main__":
    unittest.main()

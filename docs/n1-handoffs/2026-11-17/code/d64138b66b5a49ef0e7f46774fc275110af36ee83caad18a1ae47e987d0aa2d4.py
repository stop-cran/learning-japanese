import copy
import unittest

from closure_quarantine import STATUS, require_phase2_void


class PhaseTwoQuarantineTests(unittest.TestCase):
    def fixture(self):
        run, candidate = "N1-B125-GPT-001", "c" * 40
        audit_ref = {"path": "audit.json", "sha256": "a" * 64, "eventsSha256": "e" * 64}
        quarantine = {
            "run": run, "session": "reviewer", "status": STATUS,
            "reviewAccepted": False, "publicationAccepted": False,
            "candidate": candidate, "audit": audit_ref,
        }
        mechanics = {
            "batch": 125, "candidate": candidate, "run": run, "session": "reviewer",
            "status": "HOLD", "problems": ["audit VOID"], "finalAudit": dict(audit_ref),
        }
        audit = {
            "session": "reviewer", "status": "VOID", "breaches": ["phase gap"],
            "final": True, "reviewerIdle": True, "recordIncomplete": False,
            "unexpectedUserMessages": 1, "eventsSha256": "e" * 64,
        }
        context = {"status": "PASS", "compactions": [], "eventsSha256": "e" * 64}
        structure = {"status": "PASS", "overall": "NEEDS FIX"}
        diagnosis = {
            "run": run, "eventsSha256": "e" * 64, "phase2ExactMatch": False,
            "expectedPhase2Message": "segment.txt\nMissing entries: none",
            "userMessages": [{"content": "kickoff"}, {"content": "segment.txt"}],
        }
        return [quarantine, mechanics, audit, context, structure, diagnosis, 125, candidate]

    def test_preserves_void_despite_passing_report_structure(self):
        values = self.fixture()
        before = copy.deepcopy(values)
        require_phase2_void(*values)
        self.assertEqual(values, before)
        self.assertFalse(values[0]["reviewAccepted"])

    def test_rejects_acceptance_identity_and_success_relabelling(self):
        for index, field, value in (
            (0, "reviewAccepted", True), (0, "publicationAccepted", True),
            (0, "status", "HOLD_STRUCTURE_FAILED"), (0, "candidate", "d" * 40),
            (1, "run", "N1-B125-GPT-002"), (1, "session", "other"),
            (1, "status", "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION"),
            (2, "status", "FINAL_AUDIT_NEEDS_CLAIM_CHECK"),
            (2, "unexpectedUserMessages", 0), (2, "recordIncomplete", True),
            (3, "compactions", [1]), (4, "status", "FAIL"),
        ):
            values = self.fixture()
            values[index][field] = value
            with self.subTest(index=index, field=field), self.assertRaises(ValueError):
                require_phase2_void(*values)

    def test_rejects_changed_bindings_or_a_different_transition_failure(self):
        for change in (
            lambda v: v[0]["audit"].update(sha256="b" * 64),
            lambda v: v[3].update(eventsSha256="f" * 64),
            lambda v: v[5].update(phase2ExactMatch=True),
            lambda v: v[5].update(expectedPhase2Message="segment.txt"),
            lambda v: v[5]["userMessages"][1].update(content="different.txt"),
        ):
            values = self.fixture()
            change(values)
            with self.subTest(change=change), self.assertRaises(ValueError):
                require_phase2_void(*values)


if __name__ == "__main__":
    unittest.main()

import copy
import unittest

from b120_held_evidence import ERROR, RUN, SESSION, SNAPSHOT, verify_hold, verify_lineage


class HeldEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.mechanics = {
            "run": RUN, "candidate": SNAPSHOT, "session": SESSION,
            "status": "HOLD", "confirmation": "UNVERIFIED",
            **{key: {"sha256": key} for key in ("report", "audit", "context", "structure")},
        }
        self.hold = {
            **self.mechanics, "family": "claude", "status": "HELD_STRUCTURE",
            "rawVerdict": "UNVERIFIED", "reviewEvidenceAccepted": False,
            "confirmationAccepted": False, "publicationAccepted": False, "openClaimIds": ["O1/L1"],
        }
        self.audit = {
            "final": True, "reviewerIdle": True, "recordIncomplete": False, "breaches": [],
            "unexpectedUserMessages": [], "chainRead": 35, "chainRequired": 35,
            "writes": 1, "readbacks": 1, "readbackVerified": True, "fetches": 0,
            "messages": ["UNVERIFIED"], "actualResponseModels": ["claude-opus-5-5"],
            "eventsSha256": "events",
        }
        self.context = {"status": "PASS", "compactions": [], "eventsSha256": "events"}
        self.structure = {"status": "FAIL", "errors": [ERROR], "confirmation": "UNVERIFIED"}

    def check(self):
        verify_hold(self.hold, self.mechanics, self.audit, self.context, self.structure)

    def test_preserves_failure_without_mutation(self):
        before = copy.deepcopy((self.hold, self.mechanics, self.audit, self.context, self.structure))
        self.check()
        self.assertEqual(before, (self.hold, self.mechanics, self.audit, self.context, self.structure))

    def test_rejects_relabelled_acceptance_or_fixed_report(self):
        for target, key, value in (
            (self.hold, "reviewEvidenceAccepted", True),
            (self.hold, "confirmationAccepted", True),
            (self.hold, "publicationAccepted", True),
            (self.mechanics, "status", "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION"),
            (self.hold, "report", {"sha256": "rewritten"}),
            (self.structure, "status", "PASS"),
        ):
            with self.subTest(key=key):
                old = target[key]
                target[key] = value
                with self.assertRaises(ValueError):
                    self.check()
                target[key] = old

    def test_rejects_extra_failures_incomplete_reads_and_changed_identity(self):
        for target, key, value in (
            (self.structure, "errors", [ERROR, "second failure"]),
            (self.audit, "chainRead", 34),
            (self.audit, "actualResponseModels", ["different-model"]),
            (self.context, "eventsSha256", "changed"),
            (self.context, "compactions", ["compaction"]),
        ):
            with self.subTest(key=key):
                old = target[key]
                target[key] = value
                with self.assertRaises(ValueError):
                    self.check()
                target[key] = old


class ClosureLineageTests(unittest.TestCase):
    def setUp(self):
        candidate = "new-owner-signed-correction"
        initial = "8637cccb25507a1123559041ebba5401203de2db"
        self.proof = {
            "reviewedSnapshot": candidate, "initialSnapshot": initial, "publication": "PENDING",
            "excludedInitialRuns": [], "intermediateRuns": ["N1-B120-GPT-001-CONFIRM-001"],
            "finalRuns": ["N1-B120-CLAUDE-001-CONFIRM-002", "N1-B120-GPT-001-CONFIRM-002"],
            "reviewLineage": [],
        }
        for family, session in (("claude", SESSION), ("gpt", "524dc618-ae8f-4474-b698-6896a0507aed")):
            for role in (("initial", "final") if family == "claude" else ("initial", "intermediate", "final")):
                self.proof["reviewLineage"].append({
                    "run": f"N1-B120-{family.upper()}-001"
                           + ("" if role == "initial" else "-CONFIRM-001" if role == "intermediate" else "-CONFIRM-002"),
                    "family": family, "session": session, "role": role,
                    "snapshot": initial if role == "initial" else candidate if role == "final" else SNAPSHOT,
                    "rawVerdict": "UNVERIFIED" if role == "initial" else "CONFIRMED",
                    "finalAcceptance": role == "final", "confirmationAcceptedOnSnapshot": role != "initial",
                    "priorRun": "N1-B120-GPT-001-CONFIRM-001" if role == "final" and family == "gpt" else None,
                })

    def test_accepts_two_finals_with_only_passing_gpt_history(self):
        verify_lineage(self.proof, self.proof["reviewedSnapshot"])

    def test_held_run_cannot_be_inserted_as_an_accepted_predecessor(self):
        self.proof["reviewLineage"].append({
            **self.proof["reviewLineage"][1], "run": RUN, "role": "intermediate",
            "snapshot": SNAPSHOT, "finalAcceptance": False,
        })
        with self.assertRaises(ValueError):
            verify_lineage(self.proof, self.proof["reviewedSnapshot"])

    def test_prior_acceptance_does_not_transfer_to_new_snapshot(self):
        for field, value in (("snapshot", SNAPSHOT), ("confirmationAcceptedOnSnapshot", False),
                             ("priorRun", RUN), ("rawVerdict", "UNVERIFIED")):
            proof = copy.deepcopy(self.proof)
            proof["reviewLineage"][-1][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                verify_lineage(proof, proof["reviewedSnapshot"])


if __name__ == "__main__":
    unittest.main()

import copy
import unittest

from close_b126 import BASE, CANDIDATE, MEMBER, RUNS, check_history, check_review


class CleanInitialReviewTests(unittest.TestCase):
    def evidence(self):
        run, session, model, _ = RUNS["gpt"]
        report = {"path": "report.md", "sha256": "f" * 64}
        accepted = {"run": run, "candidate": CANDIDATE, "reviewAccepted": True,
                    "verdict": "CLEAN", "acceptedFindings": [], "report": report}
        final = {"run": run, "candidate": CANDIDATE, "session": session,
                 "status": "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION", "problems": []}
        audit = {"session": session, "final": True, "reviewerIdle": True,
                 "recordIncomplete": False, "breaches": [], "unexpectedUserMessages": 0,
                 "fetches": 0, "writes": 1, "readbacks": 1, "readbackVerified": True,
                 "messages": ["D: none\nE: none", "CLEAN"], "actualResponseModels": [model],
                 "coreRead": 23, "coreRequired": 23, "extensionRead": 2, "extensionRequired": 2,
                 "eventsSha256": "e" * 64}
        context = {"status": "PASS", "compactions": [], "contextTiers": ["long_context"],
                   "eventsSha256": audit["eventsSha256"]}
        structure = {"status": "PASS", "overall": "CLEAN", "findings": 0,
                     "facets": {key: "CLEAN" for key in ("correctness", "coverage", "consistency", "clarity")}}
        adjudication = {"run": run, "verdict": "CLEAN", "acceptedFindings": [],
                        "openClaimIds": [], "report": report}
        return [accepted, final, audit, context, structure, adjudication]

    def test_clean_initial_needs_no_fake_confirmation(self):
        check_review(*self.evidence(), "gpt")

    def test_rejects_nonclean_stale_or_incomplete_review(self):
        cases = [
            (0, "verdict", "NEEDS FIX"), (0, "candidate", "0" * 40),
            (0, "reviewAccepted", False), (0, "acceptedFindings", ["F1"]),
            (1, "session", "another-session"), (1, "problems", ["failure"]),
            (2, "actualResponseModels", ["claude-opus-5-5"]), (2, "reviewerIdle", False),
            (2, "extensionRead", 1), (2, "readbackVerified", False), (2, "writes", 2),
            (2, "breaches", ["extra read"]), (2, "fetches", 1), (2, "messages", ["CLEAN"]),
            (3, "compactions", [{}]), (3, "eventsSha256", "x"),
            (4, "findings", 1), (5, "openClaimIds", ["Q1"]),
        ]
        for index, key, value in cases:
            with self.subTest(index=index, key=key):
                values = copy.deepcopy(self.evidence())
                values[index][key] = value
                with self.assertRaises(ValueError):
                    check_review(*values, "gpt")

    def test_rejects_adjudication_of_another_report(self):
        values = copy.deepcopy(self.evidence())
        values[5]["report"] = {"path": "other.md", "sha256": "a" * 64}
        with self.assertRaises(ValueError):
            check_review(*values, "gpt")

    def test_history_preserves_initial_roles(self):
        value = {
            "batch": 126, "members": [MEMBER], "base": BASE, "initialSnapshot": CANDIDATE,
            "reviewedSnapshot": CANDIDATE, "publication": "PENDING", "intermediateRuns": [],
            "excludedInitialRuns": [], "finalRuns": [r[0] for r in RUNS.values()],
            "reviewLineage": [
                {"run": run, "family": family, "session": session, "snapshot": CANDIDATE,
                 "role": "initial", "rawVerdict": "CLEAN", "finalAcceptance": True,
                 "confirmationAcceptedOnSnapshot": False, "priorRun": None,
                 "actualModels": [model], "chains": [{}, {}]}
                for family, (run, session, model, _) in RUNS.items()
            ],
        }
        check_history(value)
        for key, change in (("role", "final"), ("confirmationAcceptedOnSnapshot", True),
                            ("snapshot", "0" * 40), ("finalAcceptance", False)):
            with self.subTest(key=key):
                changed = copy.deepcopy(value)
                changed["reviewLineage"][1][key] = change
                with self.assertRaises(ValueError):
                    check_history(changed)


if __name__ == "__main__":
    unittest.main()

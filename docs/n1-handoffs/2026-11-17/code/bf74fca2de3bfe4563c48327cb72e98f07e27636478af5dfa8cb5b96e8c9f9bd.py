import copy
import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "revision_input", Path(__file__).with_name("assemble-b134-revision-input.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def fixture(family):
    ids = ["F1", "O1", "O2", "O3"] if family == "claude" else ["F1", "F2", *("C" + str(i) for i in range(1, 7))]
    statuses = (["withdrawn", "optional", "optional", "optional"] if family == "claude"
                else ["unresolved", "unresolved", *(["withdrawn"] * 6)])
    run = "N1-B134-" + family.upper() + "-FRESH-003"
    collection = {
        "status": "PASS_ACCEPTED_REVIEW_COLLECTION_NOT_CLOSURE",
        "review": {"spec": {"run": run, "family": family, "snapshot": module.PRIOR,
                            "session": family + "-original-session"}},
        "requiredDispositionIds": ids,
    }
    original = {
        "run": run, "candidate": module.PRIOR, "claimsAdjudicated": True,
        "verdict": "NEEDS FIX",
        "decisions": [{"id": name, "status": status, "reason": "Original " + name}
                      for name, status in zip(ids, statuses, strict=True)],
    }
    identity = {
        "candidate": module.CANDIDATE, "session": family + "-original-session",
        "family": family, "run": "N1-B134-" + family.upper() + "-REVISION-001",
        "scope": "bounded revision", "priorRawVerdict": "NEEDS FIX",
        "producer": {"path": "producer", "sha256": "a" * 64},
    }
    accepted = {
        **identity, "batch": 134, "mode": "revision",
        "confirmationAccepted": True, "reviewEvidenceAccepted": True,
        "verdict": "CONFIRMED", "acceptedNewFindings": [], "openClaimIds": [],
        "publicationAccepted": False, "deliveryCredit": 0, "final": {"path": "final"},
        "report": {"path": "report"},
    }
    final = {
        **identity, "mode": "revision", "confirmation": "CONFIRMED",
        "status": "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION",
        "report": accepted["report"],
    }
    decision = {
        **identity, "verdict": "CONFIRMED", "acceptedNewFindings": [], "openClaimIds": [],
        "rawAuditWasClean": True, "controlAdjudicationApplied": False,
        "reportReadCompletely": True, "claimChecks": ["actual check"],
        "limitsPreserved": ["bounded"], "final": accepted["final"], "report": accepted["report"],
        "dispositions": {
            name: module.STATUS["resolved" if status == "unresolved" else status]
            for name, status in zip(ids, statuses, strict=True)
        },
    }
    return [family, collection, original, accepted, final, decision]


class RevisionInputTests(unittest.TestCase):
    def test_preserves_prior_decisions_and_resolves_only_two(self):
        results = []
        for family in module.FAMILIES:
            values = fixture(family)
            before = copy.deepcopy(values)
            results.extend(module.confirmation_dispositions(*values))
            self.assertEqual(values, before)
        self.assertEqual(len(results), 12)
        self.assertEqual([(r["run"], r["id"]) for r in results if r["status"] == "resolved"],
                         [("N1-B134-GPT-FRESH-003", "F1"), ("N1-B134-GPT-FRESH-003", "F2")])

    def test_rejects_stale_substituted_and_unaccepted_confirmation(self):
        mutations = [
            (3, "candidate", module.PRIOR), (3, "session", "substitute"),
            (3, "confirmationAccepted", False), (3, "mode", "integration"),
            (3, "openClaimIds", ["F1"]), (3, "deliveryCredit", 1),
            (4, "priorRawVerdict", "CLEAN"), (5, "rawAuditWasClean", False),
            (5, "controlAdjudicationApplied", True),
        ]
        for index, key, value in mutations:
            with self.subTest(key=key):
                values = fixture("gpt")
                values[index][key] = value
                with self.assertRaises(ValueError):
                    module.confirmation_dispositions(*values)

    def test_rejects_missing_disputed_or_extra_claim(self):
        for change in ("missing", "extra", "disputed"):
            with self.subTest(change=change):
                values = fixture("gpt")
                dispositions = values[5]["dispositions"]
                if change == "missing":
                    del dispositions["F2"]
                elif change == "extra":
                    dispositions["F3"] = "RESOLVED"
                else:
                    dispositions["C1"] = "DISPUTE REJECTED"
                with self.assertRaises(ValueError):
                    module.confirmation_dispositions(*values)

    def test_rejects_rewritten_original_finding(self):
        values = fixture("gpt")
        values[2]["decisions"][0]["status"] = "resolved"
        with self.assertRaises(ValueError):
            module.confirmation_dispositions(*values)


if __name__ == "__main__":
    unittest.main()

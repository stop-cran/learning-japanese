import copy
import unittest

from b132_confirmation_records import validate_confirmation


class ConfirmationRecordTests(unittest.TestCase):
    def values(self):
        identity = {"run": "N1-B132-GPT-CONFIRM-002", "session": "synthetic", "candidate": "b" * 40}
        spec = {"family": "gpt", "role": "confirmation", "run": identity["run"], "session": "synthetic",
                "snapshot": identity["candidate"], "confirmation": "CONFIRMED"}
        acceptance = {**identity, "reviewAccepted": True, "confirmation": "CONFIRMED"}
        final = {**identity, "status": "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION",
                 "confirmation": "CONFIRMED"}
        audit = {"session": "synthetic", "final": True, "status": "FINAL_AUDIT_NEEDS_CLAIM_CHECK",
                 "bootstrapVerified": True, "reviewerIdle": True, "recordIncomplete": False,
                 "breaches": [], "unexpectedUserMessages": 0, "fetches": 0, "writes": 1, "readbacks": 1,
                 "readbackVerified": True, "chainRequired": 29, "chainRead": 29,
                 "messages": ["CONFIRMED"], "actualResponseModels": ["gpt-6.1-sol"], "eventsSha256": "a" * 64}
        context = {"status": "PASS", "errors": [], "compactions": [], "family": "gpt",
                   "eventsSha256": "a" * 64}
        structure = {"status": "PASS", "confirmation": "CONFIRMED", "findings": 0, "nonAccepting": []}
        adjudication = {**identity, "claimsAdjudicated": True, "openClaimIds": [], "acceptedFindings": [],
                        "claimChecks": ["synthetic"], "dispositions": {"Q1": "resolved", "Q2": "resolved"}}
        return [spec, acceptance, final, audit, context, structure, adjudication, identity]

    def test_numeric_zero_actual_schema_is_required(self):
        values = self.values()
        validate_confirmation(*values)
        for value in ([], 1, False):
            changed = copy.deepcopy(values)
            changed[3]["unexpectedUserMessages"] = value
            with self.assertRaises(ValueError):
                validate_confirmation(*changed)

    def test_missing_claim_partial_read_and_wrong_context_rejected(self):
        for index, key, value in ((6, "dispositions", {"Q1": "resolved"}), (3, "chainRead", 28),
                                  (4, "compactions", ["compaction"]), (1, "reviewAccepted", False),
                                  (7, "candidate", "c" * 40), (3, "fetches", 1)):
            changed = self.values()
            changed[index][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate_confirmation(*changed)


if __name__ == "__main__":
    unittest.main()

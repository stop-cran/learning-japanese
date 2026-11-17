import copy
import json
import unittest

import b134_replacement_records as records
from common import json_bytes, sha


def fixture(family, edit=None):
    store = {}

    def put(name, value):
        raw = value if isinstance(value, bytes) else json_bytes(value)
        store[name] = raw
        return {"path": name, "sha256": sha(raw)}

    run, snapshot = "N1-B134-" + family.upper() + "-FRESH-003", "3" * 40
    session = "00000000-0000-4000-8000-000000000001"
    identity = {"run": run, "candidate": snapshot}
    report = put("report.md", b"### F1: Synthetic finding\n### O1: Synthetic optional point\n")
    values = {
        "audit": {
            "run": run, "session": session, "final": True, "status": "FINAL_AUDIT_NEEDS_CLAIM_CHECK",
            "bootstrapVerified": True, "reviewerIdle": True, "recordIncomplete": False, "breaches": [],
            "unexpectedUserMessages": 0, "fetches": 0, "writes": 1, "readbacks": 1,
            "readbackVerified": True, "messages": ["D: none\nE: none\nO: none", "NEEDS FIX"],
            "coreRead": 81, "coreRequired": 81, "extensionRead": 7, "extensionRequired": 7,
            "actualResponseModels": [family + "-fixture"],
            "capacityTelemetry": {
                "status": "PASS", "errors": [], "compactions": [], "family": family,
                "contextProfile": records.PROFILES[family],
                "observedMaxPromptTokens": [records.PROFILES[family]["maxPromptTokens"]],
                "actualPeakInputTokens": 600000,
            },
            "eventsSha256": "e" * 64, "eventsBytes": 100, "reportBinding": "normalized",
        },
        "config": {**identity, "expectedFamily": family, "report": report["path"],
                   "contextProfile": records.PROFILES[family],
                   "files": [put("input.txt", b"Full synthetic input\n")]},
        "final": {**identity, "session": session, "status": records.MECHANICAL_STATUS, "problems": [],
                  "report": report, "structure": {"status": "PASS", "overall": "NEEDS FIX"}},
        "adjudication": {
            **identity, "reportSha256": report["sha256"], "claimsAdjudicated": True,
            "verdict": "NEEDS FIX", "claimChecks": [
                {"claim": "Synthetic", "evidence": "Synthetic", "disposition": "Synthetic"}],
            "acceptedFindings": ["F1"], "openClaimIds": ["D1", "O1"], "coordinatorClaimIds": ["C1"],
        },
        "acceptance": {**identity, "reviewAccepted": True, "verdict": "NEEDS FIX",
                       "reportSha256": report["sha256"]},
    }
    if edit:
        edit(values)
    values["final"]["audit"] = put("audit.json", values["audit"])
    final = put("final.json", values["final"])
    values["adjudication"]["finalSha256"] = values["acceptance"]["finalSha256"] = final["sha256"]
    values["acceptance"]["adjudication"] = put("adjudication.json", values["adjudication"])
    spec = {**identity, "family": family, "session": session, "role": "replacement-independent",
            "snapshot": snapshot, "verdict": "NEEDS FIX", "originalReviewerConfirmation": False,
            "originalSession": records.INITIALS[family]["session"],
            "acceptance": put("acceptance.json", values["acceptance"])}
    preflight = put("preflight.json", {"candidate": snapshot, "runs": {
        family: {"run": run, "report": report["path"], "auditConfig": put("config.json", values["config"])}
    }})
    return spec, preflight, final, store


class ReplacementControls(unittest.TestCase):
    def test_collection_preserves_raw_verdict_and_all_original_bytes(self):
        for family in records.INITIALS:
            spec, preflight, final, store = fixture(family)
            before = copy.deepcopy(store)
            refs, derivatives, claims = records.collect_replacement_record(
                spec, preflight, final, lambda path, digest: store[path])
            self.assertEqual(store, before)
            self.assertEqual(refs["final"], final)
            self.assertEqual(claims["acceptedFindings"], ["F1"])
            self.assertFalse(json.loads(derivatives["audit-summary"])["originalReviewerConfirmation"])
            self.assertEqual(json.loads(derivatives["claims"])["allReportAndAdjudicationIds"],
                             ["F1", "O1", "D1", "C1"])
            for path in store:
                changed = dict(store)
                changed[path] += b" "
                with self.subTest(family=family, path=path), self.assertRaises(ValueError):
                    records.collect_replacement_record(spec, preflight, final, lambda p, digest: changed[p])

    def test_original_or_rejected_identity_cannot_be_relabelled(self):
        for family in records.INITIALS:
            original, preflight, final, store = fixture(family)
            for key, value in (
                ("session", records.INITIALS[family]["session"]), ("session", records.FAILED_SESSION),
                ("originalReviewerConfirmation", True), ("role", "confirmation"),
                ("run", "N1-B134-" + family.upper() + "-CONFIRM-003"),
            ):
                spec = {**original, key: value}
                with self.subTest(family=family, key=key), self.assertRaises(ValueError):
                    records.collect_replacement_record(spec, preflight, final, lambda p, digest: store[p])

    def test_partial_runtime_missing_claims_and_changed_profiles_are_rejected(self):
        for family in records.INITIALS:
            for name, key, wrong in (
                ("audit", "coreRead", 80), ("audit", "extensionRead", True),
                ("audit", "unexpectedUserMessages", False), ("audit", "reviewerIdle", False),
                ("audit", "actualResponseModels", ["different-family"]),
                ("config", "files", []), ("final", "problems", ["failure"]),
                ("adjudication", "claimChecks", []), ("adjudication", "coordinatorClaimIds", None),
                ("acceptance", "reviewAccepted", False),
            ):
                spec, preflight, final, store = fixture(
                    family, lambda values: values[name].update({key: wrong}))
                with self.subTest(family=family, key=key), self.assertRaises(ValueError):
                    records.collect_replacement_record(spec, preflight, final, lambda p, digest: store[p])
            for change in (
                {"observedMaxPromptTokens": [200000]},
                {"compactions": ["session.compaction_start"]},
                {"actualPeakInputTokens": 1000000},
            ):
                spec, preflight, final, store = fixture(
                    family, lambda values: values["audit"]["capacityTelemetry"].update(change))
                with self.subTest(family=family, change=change), self.assertRaises(ValueError):
                    records.collect_replacement_record(spec, preflight, final, lambda p, digest: store[p])


if __name__ == "__main__":
    unittest.main()

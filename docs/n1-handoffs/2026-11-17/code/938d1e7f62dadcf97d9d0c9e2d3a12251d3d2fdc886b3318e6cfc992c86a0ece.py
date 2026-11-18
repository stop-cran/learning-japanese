import copy
import json
import unittest

import b132_closure_records_v2 as records
from common import json_bytes, sha


def fixture(edit=None):
    store = {}

    def put(name, value):
        raw = json_bytes(value)
        store[name] = raw
        return {"path": name, "sha256": sha(raw)}

    run, session = "N1-B132-CLAUDE-001", "11111111-2222-4333-8444-555555555555"
    identity = {"run": run, "candidate": records.CANDIDATE}
    report = put("report.md", {"fixture": "not real review evidence"})
    audit = {
        "run": run, "session": session, "final": True, "status": "FINAL_AUDIT_NEEDS_CLAIM_CHECK",
        "bootstrapVerified": True, "reviewerIdle": True, "recordIncomplete": False, "breaches": [],
        "unexpectedUserMessages": 0, "fetches": 0, "writes": 1, "readbacks": 1, "readbackVerified": True,
        "messages": ["D: none\nE: none", "UNVERIFIED"], "coreRead": 37, "coreRequired": 37,
        "extensionRead": 1, "extensionRequired": 1, "actualResponseModels": ["claude-fixture"],
        "capacityTelemetry": {"status": "PASS", "errors": [], "compactions": [], "family": "claude"},
        "eventsSha256": "e" * 64, "eventsBytes": 100, "reportBinding": "line-endings-normalized",
    }
    config = {**identity, "expectedFamily": "claude", "report": report["path"]}
    final = {**identity, "session": session, "status": records.MECHANICAL_STATUS, "problems": [],
             "report": report, "structure": {"status": "PASS", "overall": "UNVERIFIED"}}
    adjudication = {
        **identity, "reportSha256": report["sha256"], "claimsAdjudicated": True,
        "verdict": "UNVERIFIED", "claimChecks": [
            {"claim": "synthetic unresolved claim", "evidence": "synthetic", "disposition": "open"}],
        "acceptedFindings": [], "openClaimIds": ["Q1"], "coordinatorClaimIds": [],
    }
    acceptance = {**identity, "reviewAccepted": True, "verdict": "UNVERIFIED",
                  "reportSha256": report["sha256"]}
    values = {"audit": audit, "config": config, "final": final,
              "adjudication": adjudication, "acceptance": acceptance}
    if edit:
        edit(values)
    final["audit"] = put("audit.json", audit)
    final_ref = put("final.json", final)
    adjudication["finalSha256"] = acceptance["finalSha256"] = final_ref["sha256"]
    acceptance["adjudication"] = put("adjudication.json", adjudication)
    spec = {"run": run, "family": "claude", "session": session, "role": "initial",
            "snapshot": records.CANDIDATE, "verdict": "UNVERIFIED",
            "acceptance": put("acceptance.json", acceptance)}
    preflight = put("preflight.json", {
        "candidate": records.CANDIDATE,
        "runs": {"claude": {"run": run, "report": report["path"], "auditConfig": put("config.json", config)}},
    })
    return spec, preflight, final_ref, store


class ActualInitialSchemaControls(unittest.TestCase):
    def test_exact_initial_schema_produces_explicit_bounded_derivatives(self):
        spec, preflight, final, store = fixture()
        refs, derivatives, claims = records.collect_initial_record(
            spec, preflight, final, lambda path, digest: store[path])
        self.assertEqual(refs["final"], final)
        self.assertEqual(claims["openClaimIds"], ["Q1"])
        summary = json.loads(derivatives["audit-summary"])
        self.assertNotIn("messages", summary)
        self.assertEqual(summary["originalAuditSha256"], refs["audit"]["sha256"])
        self.assertEqual(json.loads(derivatives["context"])["capacityTelemetry"]["status"], "PASS")
        self.assertEqual(json.loads(derivatives["structure"])["originalFinalSha256"], final["sha256"])
        for path in store:
            changed = copy.deepcopy(store)
            changed[path] += b" "
            with self.subTest(path=path), self.assertRaises(ValueError):
                records.collect_initial_record(spec, preflight, final, lambda path, digest: changed[path])

    def test_bound_but_invalid_execution_or_adjudication_is_rejected(self):
        cases = [
            ("acceptance", "reviewAccepted", False), ("audit", "unexpectedUserMessages", 1),
            ("audit", "unexpectedUserMessages", False), ("audit", "bootstrapVerified", False),
            ("audit", "coreRead", 36), ("audit", "extensionRequired", 0),
            ("audit", "actualResponseModels", ["gpt-fixture"]), ("audit", "messages", ["CLEAN"]),
            ("audit", "capacityTelemetry", {"status": "HOLD", "errors": ["compaction"],
                                           "compactions": ["start"], "family": "claude"}),
            ("final", "problems", ["failure"]), ("final", "session", "another-session"),
            ("config", "report", "different-report.md"), ("adjudication", "claimsAdjudicated", False),
            ("adjudication", "claimChecks", []), ("adjudication", "openClaimIds", ["Q1", "Q1"]),
            ("adjudication", "reportSha256", "0" * 64), ("acceptance", "reportSha256", "0" * 64),
        ]
        for name, key, wrong in cases:
            spec, preflight, final, store = fixture(lambda values: values[name].update({key: wrong}))
            with self.subTest(name=name, key=key), self.assertRaises(ValueError):
                records.collect_initial_record(spec, preflight, final, lambda path, digest: store[path])


if __name__ == "__main__":
    unittest.main()

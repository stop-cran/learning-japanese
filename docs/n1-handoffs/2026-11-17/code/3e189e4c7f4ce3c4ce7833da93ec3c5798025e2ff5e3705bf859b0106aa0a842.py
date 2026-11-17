import copy
import json
import unittest

import b134_initial_records as records
from common import json_bytes, sha


def fixture(family, edit=None):
    store = {}

    def put(name, value):
        raw = value if isinstance(value, bytes) else json_bytes(value)
        store[name] = raw
        return {"path": name, "sha256": sha(raw)}

    run = "N1-B134-" + family.upper() + "-001"
    known = records.INITIALS[family]
    session, verdict = known["session"], known["verdict"]
    identity = {"run": run, "candidate": records.CANDIDATE}
    report = put("report.md", b"### F1: Synthetic finding\n### O1: Synthetic optional point\n")
    values = {
        "audit": {
            "run": run, "session": session, "final": True, "status": "FINAL_AUDIT_NEEDS_CLAIM_CHECK",
            "bootstrapVerified": True, "reviewerIdle": True, "recordIncomplete": False, "breaches": [],
            "unexpectedUserMessages": 0, "fetches": 0, "writes": 1, "readbacks": 1,
            "readbackVerified": True, "messages": ["D: none\nE: none\nO: none", verdict],
            "coreRead": 49, "coreRequired": 49, "extensionRead": 7, "extensionRequired": 7,
            "actualResponseModels": [family + "-fixture"],
            "capacityTelemetry": {"status": "PASS", "errors": [], "compactions": [], "family": family},
            "eventsSha256": "e" * 64, "eventsBytes": 100, "reportBinding": "normalized",
        },
        "config": {**identity, "expectedFamily": family, "report": report["path"]},
        "final": {**identity, "session": session, "status": records.MECHANICAL_STATUS, "problems": [],
                  "report": report, "structure": {"status": "PASS", "overall": verdict}},
        "adjudication": {
            **identity, "reportSha256": report["sha256"], "claimsAdjudicated": True,
            "verdict": verdict, "claimChecks": [
                {"claim": "Synthetic", "evidence": "Synthetic", "disposition": "Synthetic"}],
            "acceptedFindings": [], "openClaimIds": ["O1", "O2", "O3"],
            "coordinatorClaimIds": ["C1", "C2"],
        },
        "acceptance": {**identity, "reviewAccepted": True, "verdict": verdict,
                       "reportSha256": report["sha256"]},
    }
    if family == "gpt":
        values["adjudication"].update(
            acceptedFindings=[{"id": "F1", "disposition": "partially accepted",
                               "reason": "Synthetic", "coordinatorSeverity": "minor"}],
            openClaimIds=["D1", "L3", "E9", "CLAUDE-C1", "CLAUDE-C2"])
        del values["adjudication"]["coordinatorClaimIds"]
    if edit:
        edit(values)
    values["final"]["audit"] = put("audit.json", values["audit"])
    final = put("final.json", values["final"])
    values["adjudication"]["finalSha256"] = values["acceptance"]["finalSha256"] = final["sha256"]
    values["acceptance"]["adjudication"] = put("adjudication.json", values["adjudication"])
    spec = {**identity, "family": family, "session": session, "role": "initial",
            "snapshot": records.CANDIDATE, "verdict": verdict,
            "acceptance": put("acceptance.json", values["acceptance"])}
    preflight = put("preflight.json", {"candidate": records.CANDIDATE, "runs": {
        family: {"run": run, "report": report["path"], "auditConfig": put("config.json", values["config"])}
    }})
    return spec, preflight, final, store


class InitialControls(unittest.TestCase):
    def test_both_claim_schemas_keep_original_bindings_and_all_ids(self):
        for family in records.INITIALS:
            spec, preflight, final, store = fixture(family)
            before = copy.deepcopy(store)
            refs, derivatives, claims = records.collect_initial_record(
                spec, preflight, final, lambda path, digest: store[path])
            self.assertEqual(store, before)
            self.assertEqual(refs["final"], final)
            self.assertEqual(json.loads(derivatives["claims"])["originalAdjudication"],
                             refs["adjudication"])
            required = records.disposition_ids(store["report.md"], claims)
            self.assertEqual(required, ["F1", "O1", "O2", "O3", "C1", "C2"] if family == "claude"
                             else ["F1", "O1", "D1", "L3", "E9", "CLAUDE-C1", "CLAUDE-C2"])
            self.assertNotIn("messages", json.loads(derivatives["audit-summary"]))
            for path in store:
                changed = dict(store)
                changed[path] += b" "
                with self.subTest(family=family, path=path), self.assertRaises(ValueError):
                    records.collect_initial_record(spec, preflight, final, lambda p, digest: changed[p])

    def test_partial_or_mixed_family_execution_is_not_accepted(self):
        for family in records.INITIALS:
            for name, key, wrong in (
                ("audit", "coreRead", 48), ("audit", "extensionRead", True),
                ("audit", "unexpectedUserMessages", False), ("audit", "reviewerIdle", False),
                ("audit", "actualResponseModels", ["different-family"]),
                ("audit", "capacityTelemetry", {"status": "PASS", "errors": [], "family": family,
                                               "compactions": ["session.compaction_start"]}),
                ("final", "problems", ["failure"]), ("adjudication", "claimChecks", []),
                ("adjudication", "reportSha256", "0" * 64), ("acceptance", "reviewAccepted", False),
            ):
                spec, preflight, final, store = fixture(
                    family, lambda values: values[name].update({key: wrong}))
                with self.subTest(family=family, name=name, key=key), self.assertRaises(ValueError):
                    records.collect_initial_record(spec, preflight, final, lambda p, digest: store[p])

    def test_normalization_rejects_lost_duplicated_or_malformed_claims(self):
        _, _, _, store = fixture("gpt")
        original = json.loads(store["adjudication.json"])
        for change in (
            lambda value: value["acceptedFindings"][0].pop("reason"),
            lambda value: value["acceptedFindings"].append(value["acceptedFindings"][0]),
            lambda value: value["acceptedFindings"].append("F2"),
            lambda value: value["openClaimIds"].remove("CLAUDE-C1"),
            lambda value: value["openClaimIds"].append("D1"),
            lambda value: value["openClaimIds"].append("../unexpected"),
        ):
            altered = copy.deepcopy(original)
            change(altered)
            with self.assertRaises(ValueError):
                records.normalize_claims(altered, "gpt")
        with self.assertRaises(ValueError):
            records.normalize_claims(original, "claude")
        with self.assertRaises(ValueError):
            records.disposition_ids(b"### O1: One\n### O1: Duplicate\n",
                                    records.normalize_claims(original, "gpt"))

    def test_original_reviewer_identity_cannot_be_substituted(self):
        spec, preflight, final, store = fixture("gpt")
        spec["session"] = records.INITIALS["claude"]["session"]
        with self.assertRaises(ValueError):
            records.collect_initial_record(spec, preflight, final, lambda p, digest: store[p])


if __name__ == "__main__":
    unittest.main()

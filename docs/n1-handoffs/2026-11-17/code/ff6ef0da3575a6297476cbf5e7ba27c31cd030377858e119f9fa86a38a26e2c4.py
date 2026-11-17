import copy
import json
import unittest
from unittest.mock import patch

import b133_closure_records as records
from common import json_bytes, sha
from test_b132_closure_records_v2 import fixture
from test_record_b133_publication import fixture as closure_fixture


def initial_fixture(edit=None):
    with patch("test_b132_closure_records_v2.records.CANDIDATE", records.CANDIDATE):
        spec, preflight, final, store = fixture(edit)
    old, new = "N1-B132-CLAUDE-001", "N1-B133-CLAUDE-001"

    def replace(name):
        value = json.loads(store[name])

        def update(item):
            if isinstance(item, dict):
                for key, child in item.items():
                    if key == "sha256" and item.get("path") in store:
                        continue
                    item[key] = update(child)
                if "sha256" in item and item.get("path") in store:
                    item["sha256"] = sha(store[item["path"]])
                return item
            if isinstance(item, list):
                return [update(child) for child in item]
            return new if item == old else item

        value = update(value)
        if name in ("adjudication.json", "acceptance.json"):
            value["finalSha256"] = sha(store["final.json"])
        store[name] = json_bytes(value)

    for name in ("audit.json", "config.json", "final.json", "adjudication.json",
                 "acceptance.json", "preflight.json"):
        replace(name)
    spec["run"] = new
    for ref in (spec["acceptance"], preflight, final):
        ref["sha256"] = sha(store[ref["path"]])
    return spec, preflight, final, store


class InitialControls(unittest.TestCase):
    def test_actual_schema_and_original_hashes_are_retained_without_event_payloads(self):
        spec, preflight, final, store = initial_fixture()
        refs, derivatives, claims = records.collect_initial_record(
            spec, preflight, final, lambda path, digest: store[path])
        self.assertEqual(claims["openClaimIds"], ["Q1"])
        self.assertEqual(refs["final"], final)
        summary = json.loads(derivatives["audit-summary"])
        self.assertNotIn("messages", summary)
        self.assertEqual(summary["originalAuditSha256"], refs["audit"]["sha256"])
        self.assertEqual(json.loads(derivatives["structure"])["originalFinalSha256"], final["sha256"])
        for path in store:
            changed = copy.deepcopy(store)
            changed[path] += b" "
            with self.subTest(path=path), self.assertRaises(ValueError):
                records.collect_initial_record(spec, preflight, final, lambda path, digest: changed[path])

    def test_incomplete_execution_or_unadjudicated_claims_are_rejected(self):
        cases = [
            ("acceptance", "reviewAccepted", False),
            ("audit", "unexpectedUserMessages", 1),
            ("audit", "coreRead", 36),
            ("audit", "actualResponseModels", ["gpt-fixture"]),
            ("audit", "capacityTelemetry", {"status": "HOLD", "errors": ["compaction"],
                                           "compactions": ["start"], "family": "claude"}),
            ("final", "session", "another-session"),
            ("adjudication", "claimChecks", []),
            ("adjudication", "coordinatorClaimIds", ["C1", "C1"]),
        ]
        for name, key, wrong in cases:
            spec, preflight, final, store = initial_fixture(lambda values: values[name].update({key: wrong}))
            with self.subTest(name=name, key=key), self.assertRaises(ValueError):
                records.collect_initial_record(spec, preflight, final, lambda path, digest: store[path])


def reconciled_fixture():
    closure, _, manifest = closure_fixture()
    initial = next(row for row in closure["reviewLineage"] if row["role"] == "initial")
    for row in closure["reviewLineage"]:
        if row["role"] == "initial":
            row.update(acceptedFindings=[], openClaimIds=[], coordinatorClaimIds=[])
    initial["coordinatorClaimIds"] = ["C1", "C2", "C3"]
    for row in list(closure["reviewLineage"]):
        confirmation = copy.deepcopy(row)
        confirmation.update(run=row["run"] + "-confirm", role="confirmation", confirmation="CONFIRMED")
        closure["reviewLineage"].append(confirmation)
    closure["finalRuns"] = ["claude-confirm", "gpt-confirm"]
    evidence = {"path": "verification/sources.json", "sha256": "e" * 64}
    closure["recordedFileSha256"][evidence["path"]] = evidence["sha256"]
    closure["limits"] = ["Synthetic fixture; no real teaching or publication acceptance."]
    resolution = {
        "batch": records.BATCH, "initialSnapshot": records.CANDIDATE,
        "reviewedSnapshot": closure["reviewedSnapshot"],
        "remainingActionableFindings": [], "remainingConsequentialClaims": [],
        "adjudicationSha256": {row["run"]: row["adjudication"]["sha256"]
                              for row in closure["reviewLineage"]},
        "dispositions": [
            {"run": initial["run"], "id": claim, "status": "source-backed-no-change",
             "reason": "Synthetic disposition.", "evidence": [evidence]}
            for claim in initial["coordinatorClaimIds"]
        ],
    }
    original = {
        "batch": records.BATCH, "base": records.BASE, "members": records.MEMBERS,
        "sourceRows": [707, 1120, 643], "status": "local-unreviewed-author-candidate",
        "publishedDelivered": 268, "undelivered": 960, "frozenTotal": 1228,
        "localUnpublishedDrafts": 3, "deliveryNotIncremented": True,
        "supports": [], "warnings": {},
    }
    return closure, manifest, resolution, original


class ReconciliationControls(unittest.TestCase):
    def test_all_coordinator_claims_need_bound_dispositions(self):
        closure, _, resolution, _ = reconciled_fixture()
        args = (closure["reviewLineage"], closure["reviewedSnapshot"], closure["recordedFileSha256"])
        records.validate_resolution(resolution, *args)
        for change in (
            lambda value: value["dispositions"].pop(),
            lambda value: value["dispositions"].append(value["dispositions"][0]),
            lambda value: value["dispositions"][0].update(status="optional"),
            lambda value: value["dispositions"][0]["evidence"][0].update(sha256="0" * 64),
            lambda value: value.update(remainingConsequentialClaims=["C1"]),
        ):
            altered = copy.deepcopy(resolution)
            change(altered)
            with self.assertRaises(ValueError):
                records.validate_resolution(altered, *args)

    def test_textual_closure_never_advances_delivery(self):
        closure, manifest, resolution, original = reconciled_fixture()
        result = records.closed_progress(original, json_bytes(closure), manifest, resolution)
        self.assertEqual(result["published"], [])
        self.assertFalse(result["runtimePublished"])
        self.assertEqual(result["accounting"]["publishedPendingRecordsWithCards"], 268)
        self.assertEqual(result["accounting"]["undelivered"], 960)
        self.assertEqual(result["accounting"]["reviewClosedPendingRecordsWithCards"], 271)
        unconfirmed = copy.deepcopy(closure)
        unconfirmed["finalRuns"] = ["claude", "gpt"]
        with self.assertRaises(ValueError):
            records.closed_progress(original, json_bytes(unconfirmed), manifest, resolution)
        original["publishedDelivered"] = 271
        with self.assertRaises(ValueError):
            records.closed_progress(original, json_bytes(closure), manifest, resolution)


if __name__ == "__main__":
    unittest.main()

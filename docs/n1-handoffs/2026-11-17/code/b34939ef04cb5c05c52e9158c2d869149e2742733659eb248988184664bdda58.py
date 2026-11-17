import copy
import json
import unittest

import b132_closure_records as records
from common import json_bytes, sha
from test_record_b132_publication import fixture as publication_fixture


def record_fixture():
    store = {}

    def put(name, value):
        raw = json_bytes(value)
        store[name] = raw
        return {"path": name, "sha256": sha(raw)}

    run = "N1-B132-CLAUDE-001"
    session = "11111111-2222-4333-8444-555555555555"
    identity = {"run": run, "candidate": records.CANDIDATE}
    report = put("report.md", {"text": "synthetic fixture only"})
    audit = put("audit.json", {
        "final": True, "reviewerIdle": True, "recordIncomplete": False, "breaches": [],
        "unexpectedUserMessages": [], "fetches": 0, "writes": 1, "readbacks": 1,
        "readbackVerified": True, "session": session, "coreRead": 2, "coreRequired": 2,
        "extensionRead": 1, "extensionRequired": 1, "eventsSha256": "e" * 64,
        "actualResponseModels": ["claude-fixture"],
    })
    context = put("context.json", {"status": "PASS", "compactions": [], "eventsSha256": "e" * 64})
    structure = put("structure.json", {"status": "PASS", "overall": "CLEAN"})
    preflight = put("preflight.json", {
        "candidate": records.CANDIDATE, "runs": {"claude": {"run": run, "report": report["path"]}},
    })
    final = put("final.json", {
        **identity, "session": session, "status": records.MECHANICAL_STATUS,
        "finalAudit": audit, "context": context, "structure": structure,
        "preflight": preflight["path"], "preflightSha256": preflight["sha256"],
    })
    adjudication = put("adjudication.json", {
        **identity, "claimsAdjudicated": True, "final": final, "report": report,
        "verdict": "CLEAN", "acceptedFindings": [],
    })
    acceptance = put("acceptance.json", {
        **identity, "reviewAccepted": True, "verdict": "CLEAN", "report": report,
        "final": final, "adjudication": adjudication, "acceptedFindings": [],
    })
    spec = {"run": run, "family": "claude", "role": "initial", "snapshot": records.CANDIDATE,
            "session": session, "verdict": "CLEAN", "acceptance": acceptance}
    return spec, store


class ClosureRecordControls(unittest.TestCase):
    def test_exact_frozen_graph_and_report_are_required(self):
        spec, store = record_fixture()
        refs, _ = records.collect_record(spec, lambda path, digest: store[path])
        self.assertEqual(set(refs), {*records.REFERENCE_FIELDS, "audit", "preflight"})
        for name in store:
            changed = dict(store)
            changed[name] += b" "
            with self.subTest(name=name), self.assertRaises(ValueError):
                records.collect_record(spec, lambda path, digest: changed[path])

    def test_rejects_crosswired_or_incomplete_accepted_records(self):
        spec, store = record_fixture()
        values = {name[:-5]: json.loads(raw) for name, raw in store.items() if name.endswith(".json")}

        def check(value, selected=spec):
            records.validate_record(selected, *(value[name] for name in
                                    ("acceptance", "final", "audit", "context", "structure",
                                     "adjudication", "preflight")))

        check(values)
        cases = [
            ("acceptance", "reviewAccepted", False), ("adjudication", "claimsAdjudicated", False),
            ("adjudication", "candidate", "0" * 40), ("preflight", "candidate", "0" * 40),
            ("final", "status", "PASS"), ("final", "session", "a" * 36),
            ("audit", "writes", 2), ("audit", "recordIncomplete", True),
            ("audit", "extensionRead", 0), ("audit", "coreRequired", 0),
            ("audit", "unexpectedUserMessages", ["injected"]), ("audit", "fetches", 1),
            ("audit", "actualResponseModels", ["gpt-fixture"]), ("audit", "actualResponseModels", []),
            ("context", "compactions", ["compaction"]), ("context", "eventsSha256", "0" * 64),
            ("structure", "overall", "NEEDS FIX"),
        ]
        for name, key, wrong in cases:
            changed = copy.deepcopy(values)
            changed[name][key] = wrong
            with self.subTest(name=name, key=key), self.assertRaises(ValueError):
                check(changed)
        changed = copy.deepcopy(values)
        changed["adjudication"]["report"]["sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            check(changed)
        with self.assertRaises(ValueError):
            check(values, {**spec, "family": "gpt"})

    def test_confirmation_keeps_its_own_schema_and_original_session(self):
        spec, store = record_fixture()
        values = {name[:-5]: json.loads(raw) for name, raw in store.items() if name.endswith(".json")}
        run = "N1-B132-CLAUDE-CONFIRM-001"
        spec.update(run=run, role="confirmation", confirmation="CONFIRMED")
        for name in ("acceptance", "final", "adjudication"):
            values[name]["run"] = run
        values["acceptance"]["confirmation"] = "CONFIRMED"
        values["final"].update(confirmation="CONFIRMED", report=values["acceptance"]["report"])
        values["adjudication"] = {"run": run, "dispositions": {"F1": "fixture"}}
        values["preflight"] = {"run": run, "session": spec["session"], "candidate": records.CANDIDATE}
        values["structure"] = {"status": "PASS", "confirmation": "CONFIRMED"}
        values["audit"].update(chainRead=3, chainRequired=3)

        def check(value):
            records.validate_record(spec, *(value[name] for name in
                                    ("acceptance", "final", "audit", "context", "structure",
                                     "adjudication", "preflight")))

        check(values)
        for name, key, wrong in (("final", "confirmation", "NEEDS FIX"),
                                 ("preflight", "session", "another-session"),
                                 ("audit", "chainRead", 2)):
            changed = copy.deepcopy(values)
            changed[name][key] = wrong
            with self.subTest(name=name, key=key), self.assertRaises(ValueError):
                check(changed)

    def test_resolution_cannot_drop_claims_or_advance_delivery(self):
        closure, _, manifest = publication_fixture()
        closure["limits"] = ["No delivery or whole-set credit before verified publication."]
        for entry in closure["reviewLineage"]:
            entry.update(acceptedFindings=["F1"], openClaimIds=["Q1"], coordinatorClaimIds=[])
        resolution = {
            "batch": 132, "initialSnapshot": records.CANDIDATE,
            "reviewedSnapshot": records.CANDIDATE, "remainingActionableFindings": [],
            "remainingConsequentialClaims": [],
            "adjudicationSha256": {entry["run"]: entry["adjudication"]["sha256"]
                                   for entry in closure["reviewLineage"]},
            "dispositions": [
                {"run": family, "id": claim, "status": "source-backed-no-change",
                 "reason": "Synthetic test evidence", "evidence": [closure["reviewLineage"][0]["report"]]}
                for family in ("claude", "gpt") for claim in ("F1", "Q1")
            ],
        }
        original = {
            "batch": 132, "members": records.MEMBERS, "base": records.BASE, "sourceRows": [197],
            "status": "local-unreviewed-author-candidate", "publishedDelivered": 267,
            "undelivered": 961, "deliveryNotIncremented": True, "supports": [["target", "support"]],
            "warnings": {"fixture": "not real review evidence"},
        }
        progress = records.closed_progress(original, json_bytes(closure), manifest, resolution)
        self.assertEqual(progress["accounting"]["publishedPendingRecordsWithCards"], 267)
        self.assertEqual(progress["accounting"]["undelivered"], 961)
        self.assertEqual(progress["published"], [])
        self.assertIs(progress["runtimePublished"], False)
        self.assertEqual(progress["originalAuthorWarnings"], original["warnings"])
        for key, wrong in (("remainingConsequentialClaims", ["Q1"]), ("adjudicationSha256", {}),
                           ("dispositions", resolution["dispositions"][:-1])):
            with self.subTest(key=key), self.assertRaises(ValueError):
                records.closed_progress(original, json_bytes(closure), manifest, {**resolution, key: wrong})
        with self.assertRaises(ValueError):
            records.closed_progress({**original, "publishedDelivered": 268},
                                    json_bytes(closure), manifest, resolution)
        changed = copy.deepcopy(resolution)
        changed["dispositions"][0]["evidence"][0]["sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            records.closed_progress(original, json_bytes(closure), manifest, changed)
        changed_closure = copy.deepcopy(closure)
        changed_closure["reviewLineage"][0]["coordinatorClaimIds"] = ["C1"]
        with self.assertRaises(ValueError):
            records.closed_progress(original, json_bytes(changed_closure), manifest, resolution)

    def test_archive_paths_cannot_escape_or_replace_provenance(self):
        self.assertEqual(records.archive_path("review/run/acceptance.json"), "review/run/acceptance.json")
        for name in ("", ".", "../outside", "/absolute", "C:/file", "x\\y", "x//y", "./x",
                     "x/../y", "provenance.json"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                records.archive_path(name)


if __name__ == "__main__":
    unittest.main()

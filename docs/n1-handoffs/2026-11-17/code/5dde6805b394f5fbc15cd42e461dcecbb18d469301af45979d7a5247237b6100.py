import copy
import unittest

from b133_confirmation_records import collect_confirmation, disposition_ids
from common import json_bytes, sha
from test_b133_closure_records import initial_fixture


def fixture(edit=None):
    initial_spec, initial_preflight, initial_final, store = initial_fixture()
    initial = {"spec": initial_spec, "preflight": initial_preflight, "final": initial_final}

    def put(name, value):
        raw = value if isinstance(value, bytes) else json_bytes(value)
        store[name] = raw
        return {"path": name, "sha256": sha(raw), "bytes": len(raw)}

    identity = {"run": "N1-B133-CLAUDE-CONFIRM-001", "session": initial_spec["session"],
                "candidate": "b" * 40}
    spec = {**identity, "family": "claude", "role": "confirmation",
            "snapshot": identity["candidate"], "confirmation": "CONFIRMED"}
    report = put("confirmation.md", b"Synthetic fixture, not a real confirmation.\n")
    prefix = b'{"type":"session.start","timestamp":"2026-11-17T01:00:00Z"}\n'
    event = {"type": "user.message", "timestamp": "2026-11-17T01:01:20Z",
             "data": {"content": "synthetic kickoff"}}
    values = {
        "event": event,
        "audit": {
            "session": identity["session"], "final": True, "status": "FINAL_AUDIT_NEEDS_CLAIM_CHECK",
            "bootstrapVerified": True, "reviewerIdle": True, "recordIncomplete": False, "breaches": [],
            "unexpectedUserMessages": 0, "fetches": 0, "writes": 1, "readbacks": 1,
            "readbackVerified": True, "chainRead": 1, "chainRequired": 1,
            "messages": ["CONFIRMED"], "actualResponseModels": ["claude-fixture"],
            "reportBinding": "exact", "offset": len(prefix), "prefixSha256": sha(prefix),
        },
        "context": {"status": "PASS", "errors": [], "compactions": [], "family": "claude"},
        "structure": {"status": "PASS", "confirmation": "CONFIRMED", "findings": 0, "nonAccepting": []},
        "adjudication": {
            "run": identity["run"], "candidate": identity["candidate"], "claimsAdjudicated": True,
            "acceptedFindings": [], "openClaimIds": [], "coordinatorClaimIds": [],
            "dispositions": {"Q1": "Synthetic source-backed disposition."},
            "claimChecks": [{"claim": "Synthetic", "evidence": "Synthetic", "disposition": "Synthetic"}],
        },
        "final": {**identity, "confirmation": "CONFIRMED",
                  "status": "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION", "report": report},
        "acceptance": {**identity, "batch": 133, "reviewAccepted": True,
                       "confirmation": "CONFIRMED", "report": report},
        "preflight": {
            **identity, "batch": 133, "segments": 1, "initialAcceptance": initial_spec["acceptance"],
            "initialReport": {"path": "report.md", "sha256": sha(store["report.md"])},
        },
        "admission": {**identity, "admitted": True, "observedAt": "2026-11-17T01:00:00Z",
                      "offset": len(prefix), "prefixSha256": sha(prefix),
                      "prefix": put("prefix.jsonl", prefix)},
        "config": {**identity, "expectedFamily": "claude", "report": report["path"],
                   "dispositionIds": ["Q1"], "maxWebFetches": 0, "prompt": "prompt.txt",
                   "kickoff": "kickoff.txt", "chainManifest": "chain.json"},
    }
    if edit:
        edit(values)
    slice_raw = json_bytes(values["event"]).replace(b"\n", b"") + b"\n"
    events = prefix + slice_raw
    spec["events"] = put("events.jsonl", events)
    values["audit"].update(eventsSha256=sha(events), eventsBytes=len(events),
                           sliceSha256=sha(slice_raw), sliceBytes=len(slice_raw))
    values["context"]["eventsSha256"] = sha(events)
    values["preflight"]["chain"] = put("chain.json", {
        "segments": [put("segment.txt", b"Complete synthetic source.\n")]})
    values["preflight"]["kickoff"] = put("kickoff.txt", b"Synthetic kickoff.\n")
    prompt = put("prompt.txt", b"Synthetic prompt.\n")
    values["config"]["files"] = [
        {"path": name, "sha256": sha(store[name])}
        for name in ("acceptance.json", "final.json", "report.md", "adjudication.json",
                     "audit.json", "preflight.json", "config.json", "chain.json", "kickoff.txt")
    ] + [prompt]
    values["preflight"]["config"] = put("confirmation-config.json", values["config"])
    for field in ("config", "chain", "kickoff"):
        values["admission"][field] = values["preflight"][field]
    spec["admission"] = put("admission.json", values["admission"])
    spec["preflight"] = put("confirmation-preflight.json", values["preflight"])
    for field in ("audit", "context", "structure"):
        values["final"][field] = put("confirmation-" + field + ".json", values[field])
    values["acceptance"]["final"] = put("confirmation-final.json", values["final"])
    values["adjudication"].update(
        finalSha256=values["acceptance"]["final"]["sha256"], reportSha256=report["sha256"])
    values["acceptance"]["adjudication"] = put("confirmation-adjudication.json", values["adjudication"])
    spec["acceptance"] = put("confirmation-acceptance.json", values["acceptance"])
    return spec, initial, store


class ConfirmationControls(unittest.TestCase):
    def test_collection_retains_initial_identity_and_excludes_raw_event_payloads(self):
        spec, initial, store = fixture()
        refs, derivatives, adjudication = collect_confirmation(
            spec, initial, lambda path, digest: store[path])
        self.assertEqual(refs["initialAcceptance"], initial["spec"]["acceptance"])
        self.assertEqual(set(adjudication["dispositions"]), {"Q1"})
        summary = derivatives["audit-summary"]
        self.assertNotIn(b'"messages"', summary)
        self.assertNotIn(b'"content"', summary)
        self.assertIn(b'"rawExecutionPayloadsRemainLocal": true', summary)
        for name in store:
            changed = copy.deepcopy(store)
            changed[name] += b" "
            with self.subTest(path=name), self.assertRaises(ValueError):
                collect_confirmation(spec, initial, lambda path, digest: changed[path])

    def test_nonacceptance_partial_execution_and_missing_dispositions_fail_closed(self):
        cases = [
            ("acceptance", "reviewAccepted", False),
            ("audit", "unexpectedUserMessages", False),
            ("audit", "chainRead", 0), ("audit", "chainRead", True),
            ("audit", "reviewerIdle", False), ("audit", "actualResponseModels", ["gpt-fixture"]),
            ("context", "compactions", ["compaction"]),
            ("structure", "findings", False), ("structure", "nonAccepting", ["unresolved"]),
            ("adjudication", "dispositions", {}), ("adjudication", "dispositions", {"Q1": ""}),
            ("adjudication", "coordinatorClaimIds", ["C9"]),
            ("adjudication", "claimChecks", ["unsupported"]),
            ("preflight", "candidate", "c" * 40), ("config", "dispositionIds", []),
            ("admission", "admitted", False), ("admission", "prefixSha256", "0" * 64),
            ("event", "timestamp", "2026-11-17T01:02:00Z"),
            ("event", "timestamp", "2026-11-17T00:59:59Z"),
            ("event", "timestamp", "2026-11-17T01:01:20"),
        ]
        for name, key, value in cases:
            spec, initial, store = fixture(lambda values: values[name].update({key: value}))
            with self.subTest(name=name, key=key), self.assertRaises(ValueError):
                collect_confirmation(spec, initial, lambda path, digest: store[path])

    def test_replacement_reviewer_or_initial_report_cannot_be_substituted(self):
        for target in ("session", "family"):
            spec, initial, store = fixture()
            spec[target] = "aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee" if target == "session" else "gpt"
            with self.subTest(target=target), self.assertRaises(ValueError):
                collect_confirmation(spec, initial, lambda path, digest: store[path])
        spec, initial, store = fixture(lambda values: values["preflight"].update(
            initialReport={"path": "confirmation.md", "sha256": sha(b"not original")}))
        with self.assertRaises(ValueError):
            collect_confirmation(spec, initial, lambda path, digest: store[path])

    def test_optional_points_and_all_claim_classes_keep_distinct_dispositions(self):
        claims = {"acceptedFindings": ["F1"], "openClaimIds": ["Q1"], "coordinatorClaimIds": ["C1", "C2"]}
        report = b"### F1: Finding\n### O1: Optional point\n"
        self.assertEqual(disposition_ids(report, claims), ["F1", "O1", "Q1", "C1", "C2"])
        with self.assertRaises(ValueError):
            disposition_ids(report + b"### O1: Duplicate\n", claims)


if __name__ == "__main__":
    unittest.main()

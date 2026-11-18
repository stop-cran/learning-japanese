import copy
import datetime
import json
import tempfile
import unittest
from pathlib import Path

import confirm_b134 as controller
from b134_confirmation_capacity import confirmation_cost
from b134_confirmation_records import collect_confirmation
from b134_initial_records import MECHANICAL_STATUS, disposition_ids, normalize_claims
from common import COORDINATOR, json_bytes, load_module, sha
from test_b134_initial_records import fixture as initial_fixture

NOW = datetime.datetime(2026, 11, 17, 5, 0, tzinfo=datetime.timezone.utc)


class Guard:
    def check(self):
        pass


def spec(family="gpt", **changes):
    value = {
        "family": family, "run": "N1-B134-" + family.upper() + "-CONFIRM-001",
        "session": controller.INITIALS[family]["session"], "candidate": controller.CANDIDATE,
        "teachingChange": False, "scope": ["\u7d2b"], "revisedSources": ["kanji/\u7d2b.md"],
        "additionalSources": [], "basis": "adjudicated-initial",
        "priorVerdict": controller.INITIALS[family]["verdict"],
        "basisText": "Synthetic B134 follow-up, not evidence or a requested outcome.",
    }
    value.update(changes)
    return value


def report(ids, run="N1-B134-GPT-CONFIRM-001"):
    lines = "\n".join(f"- {item} - RESOLVED - Synthetic source-backed decision." for item in ids)
    return f"""# B134 confirmation - {run}

## Snapshot
Commit: {controller.CANDIDATE}
Model: synthetic

## Scope
Chain: 1
Fetches: 0

## Dispositions
{lines}

## Verdicts
Correctness: CLEAN
Scoped coverage: CLEAN
Consistency and quiz safety: CLEAN
Comprehensibility: CLEAN

## Confirmation
Verdict: CONFIRMED
Basis: Synthetic fixture, not review evidence.

## Findings
None.

## Optional
None.

## Limits
- L1: Synthetic fixture.
"""


def confirmation_fixture(edit=None):
    initial_spec, initial_preflight, initial_final, store = initial_fixture("gpt")
    initial = {"spec": initial_spec, "preflight": initial_preflight, "final": initial_final}
    required = disposition_ids(store["report.md"],
                               normalize_claims(json.loads(store["adjudication.json"]), "gpt"))

    def put(name, value):
        raw = value if isinstance(value, bytes) else json_bytes(value)
        store[name] = raw
        return {"path": name, "sha256": sha(raw), "bytes": len(raw)}

    identity = {"run": "N1-B134-GPT-CONFIRM-001", "session": initial_spec["session"],
                "candidate": "b" * 40}
    result_spec = {**identity, "family": "gpt", "role": "confirmation",
                   "snapshot": identity["candidate"], "confirmation": "CONFIRMED"}
    report_ref = put("confirmation.md", b"Synthetic fixture, not a real confirmation.\n")
    prefix = b'{"type":"session.start","timestamp":"2026-11-17T05:00:00Z"}\n'
    values = {
        "event": {"type": "user.message", "timestamp": "2026-11-17T05:01:20Z",
                  "data": {"content": "synthetic kickoff"}},
        "audit": {
            "session": identity["session"], "final": True, "status": "FINAL_AUDIT_NEEDS_CLAIM_CHECK",
            "bootstrapVerified": True, "reviewerIdle": True, "recordIncomplete": False, "breaches": [],
            "unexpectedUserMessages": 0, "fetches": 0, "writes": 1, "readbacks": 1,
            "readbackVerified": True, "chainRead": 1, "chainRequired": 1,
            "messages": ["CONFIRMED"], "actualResponseModels": ["gpt-fixture"],
            "reportBinding": "exact", "offset": len(prefix), "prefixSha256": sha(prefix),
        },
        "context": {"status": "PASS", "errors": [], "compactions": [], "family": "gpt"},
        "structure": {"status": "PASS", "confirmation": "CONFIRMED", "findings": 0, "nonAccepting": []},
        "adjudication": {
            "run": identity["run"], "candidate": identity["candidate"], "claimsAdjudicated": True,
            "acceptedFindings": [], "openClaimIds": [], "coordinatorClaimIds": [],
            "dispositions": dict.fromkeys(required, "Synthetic source-backed disposition."),
            "claimChecks": [{"claim": "Synthetic", "evidence": "Synthetic", "disposition": "Synthetic"}],
        },
        "final": {**identity, "confirmation": "CONFIRMED", "status": MECHANICAL_STATUS,
                  "report": report_ref},
        "acceptance": {**identity, "batch": 134, "reviewAccepted": True,
                       "confirmation": "CONFIRMED", "report": report_ref},
        "preflight": {
            **identity, "batch": 134, "segments": 1, "initialAcceptance": initial_spec["acceptance"],
            "initialReport": {"path": "report.md", "sha256": sha(store["report.md"])},
        },
        "admission": {**identity, "admitted": True, "observedAt": "2026-11-17T05:00:00Z",
                      "offset": len(prefix), "prefixSha256": sha(prefix),
                      "prefix": put("prefix.jsonl", prefix)},
        "config": {**identity, "expectedFamily": "gpt", "report": report_ref["path"],
                   "dispositionIds": required, "maxWebFetches": 0, "prompt": "prompt.txt",
                   "kickoff": "kickoff.txt", "chainManifest": "chain.json"},
    }
    if edit:
        edit(values)
    sliced = json.dumps(values["event"], separators=(",", ":")).encode() + b"\n"
    events = prefix + sliced
    result_spec["events"] = put("events.jsonl", events)
    values["audit"].update(eventsSha256=sha(events), eventsBytes=len(events),
                           sliceSha256=sha(sliced), sliceBytes=len(sliced))
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
    result_spec["admission"] = put("admission.json", values["admission"])
    result_spec["preflight"] = put("confirmation-preflight.json", values["preflight"])
    for field in ("audit", "context", "structure"):
        values["final"][field] = put("confirmation-" + field + ".json", values[field])
    values["acceptance"]["final"] = put("confirmation-final.json", values["final"])
    values["adjudication"].update(
        finalSha256=values["acceptance"]["final"]["sha256"], reportSha256=report_ref["sha256"])
    values["acceptance"]["adjudication"] = put("confirmation-adjudication.json", values["adjudication"])
    result_spec["acceptance"] = put("confirmation-acceptance.json", values["acceptance"])
    return result_spec, initial, store, required


class ConfirmationControls(unittest.TestCase):
    def test_actual_originals_and_new_ids_are_bound(self):
        for family in controller.INITIALS:
            refs, original, required = controller.initial(family, controller.INITIALS[family]["session"])
            self.assertEqual(sha(original), refs["report"]["sha256"])
            if family == "gpt":
                self.assertEqual(len(required), 24)
                self.assertTrue({"F1", "O1", "D20", "E9", "L3", "CLAUDE-C1", "CLAUDE-C2"} <= set(required))
            else:
                self.assertEqual(required, ["O1", "O2", "O3", "C1", "C2"])

    def test_spec_requires_original_family_snapshot_and_complete_scoped_card(self):
        self.assertEqual(controller.validate_spec(spec()), "gpt")
        for value in (spec(session=controller.INITIALS["claude"]["session"]), spec(scope=[]),
                      spec(scope=["\u7434"]), spec(revisedSources=[]), spec(priorVerdict="CLEAN"),
                      spec(candidate="b" * 40), spec(revisedSources=["../outside.md"]),
                      spec(revisedSources=["kanji/\u7d2b.md", "C:/outside.md"]),
                      spec(run="N1-B133-GPT-CONFIRM-001"), spec(teachingChange=1)):
            with self.assertRaises(ValueError):
                controller.validate_spec(value)
        self.assertEqual(controller.validate_spec(spec(candidate="b" * 40, teachingChange=True)), "gpt")

    def test_serial_admission_rejects_busy_unknown_stale_and_incomplete_snapshots(self):
        session = controller.INITIALS["gpt"]["session"]
        rows = [{"id": COORDINATOR, "activity": {"status": "busy"}, "is_running": True},
                {"id": session, "activity": {"status": "idle"}, "is_running": False}]
        status, roster = {"summary": {"total": 2}, "sessions": rows}, [{"id": row["id"]} for row in rows]
        self.assertEqual(controller.check_snapshot(status, roster, session, NOW, NOW), 2)
        for change in ({"activity": {"status": "busy"}}, {"activity": {"status": "unknown"}},
                       {"is_running": None}, {"awaiting_plan_approval": True}, {"awaiting_user_input": True}):
            altered = copy.deepcopy(status)
            altered["sessions"][1].update(change)
            with self.assertRaises(ValueError):
                controller.check_snapshot(altered, roster, session, NOW, NOW)
        for observed in (NOW - datetime.timedelta(seconds=120), NOW + datetime.timedelta(seconds=1)):
            with self.assertRaises(ValueError):
                controller.check_snapshot(status, roster, session, observed, NOW)
        with self.assertRaises(ValueError):
            controller.check_snapshot(status, roster[:1], session, NOW, NOW)

    def test_complete_source_reconstruction_and_strict_capacity_boundary(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sources = [("initial-report/report.md", b"Prior report.\n", None),
                       ("evidence/external/source-extract.txt", b"Complete source.\n", None)]
            chain = controller.build_chain(sources, root / "segments", root / "chain.json", Guard(), "fixture")
            measured = confirmation_cost(chain)
            self.assertEqual(measured["chainBytes"], sum(row["bytes"] for row in chain["segments"]))
            self.assertLess(measured["tokens"], measured["chainBytes"])
            altered = copy.deepcopy(chain)
            altered["sources"][0]["selectedLines"] += 1
            with self.assertRaises(ValueError):
                confirmation_cost(altered)
            observed = {"status": "PASS", "family": "claude",
                        "lastInputTokens": 700000 - measured["tokens"] - 8000 - 12000 - 30000 - 1}
            self.assertEqual(controller.capacity(observed, chain, 8000)["projectedPeak"], 699999)
            with self.assertRaises(ValueError):
                controller.capacity({**observed, "lastInputTokens": observed["lastInputTokens"] + 1}, chain, 8000)

    def test_disposition_contract_covers_d_e_l_and_qualified_coordinator_ids(self):
        checker = load_module("b134_confirmation_checker_test", controller.OUT / "check-confirm-structure.py")
        required = ["F1", "O1", "D20", "E9", "L3", "CLAUDE-C1"]
        text = report(required)
        args = ("N1-B134-GPT-CONFIRM-001", controller.CANDIDATE, required, {"sources": []}, "CONFIRMED")
        self.assertEqual(checker.check(text, *args)["status"], "PASS")
        for altered in (
            text.replace("- D20 - RESOLVED - Synthetic source-backed decision.\n", ""),
            text.replace("CLAUDE-C1 - RESOLVED", "CLAUDE-C1 - NOT RESOLVED"),
            text.replace("Correctness: CLEAN", "Correctness: UNVERIFIED"),
            text.replace("B134 confirmation", "B133 confirmation"),
            text.replace("- L3 -", "- ../../../L3 -"),
        ):
            self.assertEqual(checker.check(altered, *args)["status"], "FAIL")
        rendered = controller.render(spec(), {"path": "own-report.md"},
                                     {"segments": [{"path": "first.txt"}]}, Path("prompt.txt"),
                                     Path("report.md"), required).decode()
        self.assertIn(spec()["basisText"], rendered)
        self.assertIn("- CLAUDE-C1 - <disposition>", rendered)
        self.assertNotIn("B133", rendered)

    def test_acceptance_preserves_originals_and_rejects_changed_inputs(self):
        value, initial, store, required = confirmation_fixture()
        refs, _, adjudication = collect_confirmation(value, initial, lambda p, digest: store[p])
        self.assertEqual(set(adjudication["dispositions"]), set(required))
        self.assertEqual(refs["initialAcceptance"], initial["spec"]["acceptance"])
        for path in store:
            altered = dict(store)
            altered[path] += b" "
            with self.subTest(path=path), self.assertRaises(ValueError):
                collect_confirmation(value, initial, lambda p, digest: altered[p])

    def test_acceptance_rejects_lost_claims_partial_reads_stale_delivery_and_compaction(self):
        for name, key, wrong in (
            ("adjudication", "dispositions", {}), ("adjudication", "openClaimIds", ["D1"]),
            ("audit", "chainRead", 0), ("audit", "reviewerIdle", False),
            ("audit", "actualResponseModels", ["claude-fixture"]), ("audit", "fetches", 1),
            ("context", "compactions", ["session.compaction_start"]),
            ("structure", "nonAccepting", ["D1"]), ("admission", "admitted", False),
            ("admission", "prefixSha256", "0" * 64), ("config", "dispositionIds", []),
            ("event", "timestamp", "2026-11-17T05:02:00Z"),
        ):
            value, initial, store, _ = confirmation_fixture(lambda values: values[name].update({key: wrong}))
            with self.subTest(name=name, key=key), self.assertRaises(ValueError):
                collect_confirmation(value, initial, lambda p, digest: store[p])

    def test_single_phase_auditor_accepts_complete_reads_and_rejects_partial_or_parallel_reads(self):
        auditor = load_module("b134_confirmation_auditor_test", controller.OUT / "audit-confirm.py")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            paths = {name: root / (name + ".txt") for name in ("prompt", "kickoff", "segment", "report")}
            for name, path in paths.items():
                path.write_bytes((name + " synthetic content.\n").encode())
            config = {name: str(path) for name, path in paths.items() if name != "segment"}
            config.update(coordinator=COORDINATOR, expectedFamily="gpt",
                          completionContract="entire-message-enum-v1", maxWebFetches=0)
            events = [
                {"type": "user.message", "data": {"content": paths["kickoff"].read_text(),
                                                "source": "agent-" + COORDINATOR}},
                {"type": "session.usage_record", "data": {"usage": {"responseModel": "gpt-fixture"}}},
            ]

            def call(name, args, returned=""):
                cid = str(len(events))
                events.extend([
                    {"type": "assistant.message", "data": {"model": "gpt-fixture", "apiCallId": cid,
                     "toolRequests": [{"name": name, "arguments": args, "toolCallId": cid}]}},
                    {"type": "tool.execution_complete", "data": {"toolCallId": cid, "success": True,
                                                               "result": {"content": returned}}},
                ])

            for name in ("prompt", "segment"):
                call("view", {"path": str(paths[name]), "forceReadLargeFiles": True}, paths[name].read_text())
            body = paths["report"].read_text()
            patch_text = "*** Begin Patch\n*** Add File: " + str(paths["report"]) + "\n"
            patch_text += "".join("+" + line + "\n" for line in body.splitlines()) + "*** End Patch\n"
            call("apply_patch", patch_text)
            call("view", {"path": str(paths["report"]), "forceReadLargeFiles": True}, body)
            call("send_session_message", {"session_id": COORDINATOR, "message": "CONFIRMED"})
            events.append({"type": "assistant.turn_end", "data": {}})
            chain = {"segments": [{"path": str(paths["segment"])}]}
            actual = auditor.audit(events, config, chain, final=True)
            self.assertEqual(actual["status"], "FINAL_AUDIT_NEEDS_CLAIM_CHECK", actual["breaches"])
            altered = copy.deepcopy(events)
            altered[5]["data"]["result"]["content"] = "Truncated source."
            self.assertEqual(auditor.audit(altered, config, chain, final=True)["status"], "VOID")
            altered = copy.deepcopy(events)
            altered[2]["data"]["toolRequests"].append(altered[2]["data"]["toolRequests"][0])
            self.assertEqual(auditor.audit(altered, config, chain, final=True)["status"], "VOID")


if __name__ == "__main__":
    unittest.main()

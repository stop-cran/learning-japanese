"""Undelivered end-to-end B134 two-phase protocol and collector controls."""
import copy
import importlib.util
import json
import sys
import uuid
import unittest
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "tools"))
sys.path.insert(0, r"C:\Users\stop-\n1-kanji-workspace\review-tools")

import b134_common as common
import b134_runtime as runtime
from b134_capacity import PROFILES, load_forecast
from b134_runtime import expected_message, extension_sources
from b134_common import CORE, CORE_SHA, PACKET, SUMS_SHA, frozen, sha, write_frozen
from b134_replacement_records import collect_replacement_record
from review_chain_with_optional import build_chain, optional_unit_map, validate_selection


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


AUDIT = load_module("b134_synthetic_audit_013", "audit-review-b134-013.py")
STRUCTURE = load_module("b134_synthetic_structure_013", "check-report-structure-b134-013.py")
PREPARE = load_module("b134_synthetic_prepare_013", "prepare-extension-b134-013.py")


def request_event(rows, number, name, arguments, content):
    call_id = f"synthetic-{number}"
    rows.extend([
        {"type": "assistant.message", "data": {
            "model": "claude-opus-5.5", "apiCallId": call_id,
            "toolRequests": [{"toolCallId": call_id, "name": name, "arguments": arguments}],
        }},
        {"type": "tool.execution_start", "data": {
            "toolCallId": call_id, "toolName": name, "arguments": arguments,
        }},
        {"type": "tool.execution_complete", "data": {
            "toolCallId": call_id, "success": True, "result": {"content": content},
        }},
    ])


class SyntheticProtocol(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.core = json.loads(frozen(CORE, CORE_SHA))
        cls.sums = json.loads(frozen(PACKET / "SHA256SUMS.json", SUMS_SHA))
        cls.reference = json.loads(frozen(PACKET / "eligibility-reference.json",
                                          cls.sums["eligibility-reference.json"]))
        cls.units = optional_unit_map(json.loads(frozen(
            PACKET / "evidence/kanjidic2-full-unit-index.json",
            cls.sums["evidence/kanjidic2-full-unit-index.json"])))
        cls.forecast = load_forecast()
        card = cls.reference["cards"][0]
        excluded = set(card["quiz_exclusions"]) | set(card["distractors"]) | set(cls.reference["newCards"])
        cls.character = next(
            chr(codepoint) for codepoint in range(0x4E00, 0x9FFF)
            if chr(codepoint) not in excluded and f"repo/kanji/{chr(codepoint)}.md" in cls.sums
        )
        cls.selection = f"D1 {cls.character} - 紫: synthetic overlap\nE: none\nO: none"
        cls.run_id = "N1-B134-CLAUDE-FRESH-002"
        cls.session = "synthetic-b134-session"

    def _config(self, case):
        preflight = json.loads(frozen(common.HERE / "audit-configs-015" / "preflight.json"))
        spec = preflight["runs"]["claude"]
        config = json.loads(frozen(spec["auditConfig"]["path"], spec["auditConfig"]["sha256"]))
        config = {**config, "report": str(case / "reports" / "review.md")}
        return spec, config

    def _bootstrap_prefix(self, config):
        rows = [json.loads(line) for line in frozen(
            common.ROOT / "meter-011-claude-bootstrap-001" / "events.jsonl",
            "0332c7aa374ddaec83912b8b243a6cfed0aa1cf736bff5de00ffb9b0b0872924",
        ).decode("utf-8").splitlines()]
        for event in rows:
            data = event.get("data", {})
            if event.get("type") == "session.start":
                data["sessionId"] = self.session
            elif event.get("type") == "user.message":
                data["content"] = config["kickoffText"]
            elif event.get("type") == "assistant.message" and data.get("toolRequests"):
                data["toolRequests"][0]["arguments"]["path"] = config["prompt"]
            elif event.get("type") == "tool.execution_start":
                data["arguments"]["path"] = config["prompt"]
            elif event.get("type") == "tool.execution_complete":
                data["result"]["content"] = frozen(
                    config["prompt"], config["promptSha256"]).decode("utf-8")
            elif event.get("type") == "assistant.message":
                data["content"] = config["bootstrapResponseText"]
        return rows

    def test_synthetic_two_phase_and_report_readback(self):
        case = common.HERE / ("synthetic-validation-012-" + uuid.uuid4().hex)
        self.assertFalse(case.exists(), "Preserve previous synthetic validation")
        report = case / "reports" / "review.md"
        report.parent.mkdir(parents=True)
        spec, config = self._config(case)
        prefix = self._bootstrap_prefix(config)
        rows = copy.deepcopy(prefix)
        config = {**config, "_bootstrapSnapshotEventCount": len(prefix)}
        rows.append({"type": "user.message", "data": {
            "content": config["coreReleaseMessage"], "source": "agent-" + config["coordinator"],
        }})
        number = 2
        for segment in self.core["segments"]:
            request_event(rows, number, "view", {
                "path": segment["path"], "forceReadLargeFiles": True, "view_range": None,
            }, frozen(segment["path"], segment["sha256"]).decode("utf-8"))
            number += 1
        request_event(rows, number, "send_session_message", {
            "session_id": config["coordinator"], "message": self.selection,
        }, "synthetic coordinator receipt")
        number += 1
        rows.append({"type": "assistant.turn_end", "data": {}})
        first = AUDIT.audit(rows, config, self.core, self.reference, session=self.session)
        self.assertEqual(first["status"], "PHASE1_READY", first["breaches"])
        first["session"] = self.session
        self.assertEqual(first["coreRead"], first["coreRequired"])
        self.assertTrue(first["bootstrapVerified"] and first["coreReleaseVerified"])
        self.assertEqual(first["capacityTelemetry"]["contextProfile"], PROFILES["claude"])
        self.assertTrue(validate_selection(self.selection, self.reference, self.units)["valid"])

        audit_dir = case / self.run_id / "audit-synthetic"
        events_raw = b"".join((json.dumps(row, ensure_ascii=False) + "\n").encode() for row in rows)
        write_frozen(audit_dir / "events.jsonl", events_raw)
        first["eventsSha256"] = sha(events_raw)
        phase1_audit = audit_dir / "audit.json"
        write_frozen(phase1_audit, (json.dumps(first, ensure_ascii=False) + "\n").encode())
        phase1_list = audit_dir / "phase1-list.txt"
        write_frozen(phase1_list, self.selection.encode("utf-8"))
        write_frozen(case / (self.run_id + "-phase1.json"), (json.dumps({
            "auditDir": str(audit_dir), "session": self.session, "readyForPhase2": True,
        }) + "\n").encode())
        config_path = case / "audit-config.json"
        write_frozen(config_path, (json.dumps(config, ensure_ascii=False) + "\n").encode("utf-8"))
        args = ["prepare-extension", "--config", str(config_path),
                "--reply", str(phase1_list), "--phase1-audit", str(phase1_audit)]
        with patch.object(PREPARE, "HERE", case):
            with patch.object(common, "HERE", case):
                with patch.object(sys, "argv", args):
                    PREPARE.main()
        extension = json.loads(frozen(case / (self.run_id + "-extension.json")))
        phase2 = frozen(case / (self.run_id + "-phase2-message.txt")).decode("utf-8")
        self.assertIn("Missing entries: none", phase2)
        self.assertGreater(len(extension["sources"]), 0)

        rows = copy.deepcopy(rows)
        rows.append({"type": "user.message", "data": {
            "content": phase2, "source": "agent-" + config["coordinator"],
        }})
        for segment in extension["segments"]:
            request_event(rows, number, "view", {
                "path": segment["path"], "forceReadLargeFiles": True, "view_range": None,
            }, frozen(segment["path"], segment["sha256"]).decode("utf-8"))
            number += 1
        title = f"# B134 fresh independent review — {self.run_id}"
        body = f"""{title}

## Overall verdict
Verdict: UNVERIFIED

## Facet verdicts
### Correctness
Verdict: UNVERIFIED
Basis: Synthetic protocol control.
### Scoped coverage
Verdict: UNVERIFIED
Basis: Synthetic protocol control.
### Consistency/quiz safety
Verdict: UNVERIFIED
Basis: Synthetic protocol control.
### Comprehensibility
Verdict: UNVERIFIED
Basis: Synthetic protocol control.

## Segments read
Core chain: 1-64; no re-views
Extension chain: 1-{len(extension["segments"])}; no re-views

## Phase-1 D/E lists
D: D1 {self.character}
E: none
O: none
Missing entries: none

## D/E cards read
| ID | Character | Displayed title | Related new card(s) | Reason | Disposition |
| --- | --- | --- | --- | --- | --- |
| D1 | {self.character} | Synthetic title | 紫 | Potential overlap; repo/kanji/{self.character}.md:1 | Harmless; repo/kanji/{self.character}.md:1 |

## Per-card results
| Card | Correctness | Scoped coverage | Consistency/quiz safety | Comprehensibility | Evidence |
| --- | --- | --- | --- | --- | --- |
| 紫 | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | Synthetic protocol control. |

## Findings
None.

## Optional points
None.

## Limits
- L1: Synthetic protocol control only.
"""
        request_event(rows, number, "create", {"path": str(report), "file_text": body},
                      "synthetic report created")
        number += 1
        report.write_text(body, encoding="utf-8", newline="\n")
        request_event(rows, number, "view", {
            "path": str(report), "forceReadLargeFiles": True, "view_range": None,
        }, body)
        number += 1
        request_event(rows, number, "send_session_message", {
            "session_id": config["coordinator"], "message": "UNVERIFIED",
        }, "synthetic coordinator receipt")
        rows.append({"type": "assistant.turn_end", "data": {}})
        with patch.object(common, "HERE", case), patch.object(runtime, "HERE", case), \
                patch.object(AUDIT, "LIFECYCLE", case):
            final = AUDIT.audit(rows, config, self.core, self.reference, extension, self.selection,
                                phase2, final=True, session=self.session)
        self.assertEqual(final["status"], "FINAL_AUDIT_NEEDS_CLAIM_CHECK", final["breaches"])
        self.assertTrue(final["readbackVerified"])
        self.assertEqual(final["extensionRead"], final["extensionRequired"])
        selection = validate_selection(self.selection, self.reference, self.units)
        checked = STRUCTURE.check(body, self.run_id, self.core, extension, self.reference,
                                  selection, phase2, "UNVERIFIED")
        self.assertEqual(checked["status"], "PASS", checked["errors"])
        wrong_completion = STRUCTURE.check(body, self.run_id, self.core, extension, self.reference,
                                           selection, phase2, "CLEAN")
        self.assertEqual(wrong_completion["status"], "FAIL")
        broken = STRUCTURE.check(body.replace("## Limits", "## Bad"), self.run_id, self.core,
                                 extension, self.reference, selection, phase2, "UNVERIFIED")
        self.assertEqual(broken["status"], "FAIL")
        bad_readback = copy.deepcopy(rows)
        read_request = next(request for event in bad_readback if event.get("type") == "assistant.message"
                            for request in event.get("data", {}).get("toolRequests", [])
                            if request.get("name") == "view" and request.get("arguments", {}).get("path") == str(report))
        read_id = read_request["toolCallId"]
        read_complete = next(event for event in bad_readback
                             if event.get("type") == "tool.execution_complete"
                             and event.get("data", {}).get("toolCallId") == read_id)
        read_complete["data"]["result"]["content"] = "tampered synthetic readback"
        with patch.object(common, "HERE", case), patch.object(runtime, "HERE", case), \
                patch.object(AUDIT, "LIFECYCLE", case):
            rejected = AUDIT.audit(bad_readback, config, self.core, self.reference, extension,
                                   self.selection, phase2, final=True, session=self.session)
        self.assertEqual(rejected["status"], "VOID")
        self.assertTrue(any("readback differs" in item.lower() for item in rejected["breaches"]))

    def test_replacement_collector_binds_bootstrap_refs(self):
        records = {}

        def put(path, value):
            raw = value if isinstance(value, bytes) else (
                json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
            records[path] = raw
            return {"path": path, "sha256": sha(raw)}

        def read(path, digest):
            raw = records[path]
            if sha(raw) != digest:
                raise ValueError("Synthetic record hash mismatch")
            return raw

        candidate = "355cccb840d22e7313e79f234eb93d1367e00352"
        session = "123e4567-e89b-42d3-a456-426614174000"
        run = "N1-B134-CLAUDE-FRESH-002"
        report_ref = put("report.md", b"# synthetic report\n")
        input_ref = put("input.json", b"frozen synthetic input\n")
        profile = __import__("b134_replacement_records").PROFILES["claude"]
        config = {
            "candidate": candidate, "run": run, "expectedFamily": "claude",
            "report": report_ref["path"], "files": [input_ref],
            "contextProfile": profile, "bootstrapRecordPath": "bootstrap.json",
            "coreAuthorizationPath": "authorization.json",
        }
        config_ref = put("config.json", config)
        snapshot_ref = put("bootstrap-events.jsonl", b'{"type":"session.start"}\n')
        bootstrap_ref = put("bootstrap.json", {
            "status": "PROMPT_ONLY_BOOTSTRAP_PASS", "run": run, "sessionId": session,
            "candidate": candidate, "configSha256": config_ref["sha256"],
            "eventSnapshotPath": snapshot_ref["path"], "eventSnapshotSha256": snapshot_ref["sha256"],
        })
        authorization_ref = put("authorization.json", {
            "status": "CORE_RELEASE_AUTHORIZED", "run": run, "sessionId": session,
            "candidate": candidate, "configSha256": config_ref["sha256"],
            "bootstrapRecordSha256": bootstrap_ref["sha256"],
            "eventSnapshotPath": snapshot_ref["path"], "eventSnapshotSha256": snapshot_ref["sha256"],
        })
        preflight = {"candidate": candidate, "runs": {"claude": {
            "run": run, "report": report_ref["path"], "auditConfig": config_ref,
        }}}
        preflight_ref = put("preflight.json", preflight)
        audit = {
            "run": run, "session": session, "eventsSha256": "a" * 64, "eventsBytes": 1,
            "status": "FINAL_AUDIT_NEEDS_CLAIM_CHECK", "final": True, "breaches": [],
            "bootstrapVerified": True, "actualResponseModels": ["claude-opus-5.5"],
            "reviewerIdle": True, "recordIncomplete": False, "unexpectedUserMessages": 0,
            "fetches": 0, "writes": 1, "readbacks": 1, "readbackVerified": True,
            "messages": ["D: none\nE: none\nO: none", "UNVERIFIED"],
            "coreRead": 64, "coreRequired": 64, "extensionRead": 1, "extensionRequired": 1,
            "reportBinding": "exact",
            "capacityTelemetry": {
                "status": "PASS", "errors": [], "compactions": [], "family": "claude",
                "contextProfile": profile, "observedMaxPromptTokens": [952000],
                "actualPeakInputTokens": 1000,
            },
            "bootstrapRecord": bootstrap_ref, "coreAuthorization": authorization_ref,
            "bootstrapEventSnapshot": snapshot_ref,
        }
        audit_ref = put("audit.json", audit)
        final = {
            "run": run, "session": session, "candidate": candidate,
            "status": "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION", "problems": [],
            "audit": audit_ref, "report": report_ref,
            "structure": {"status": "PASS", "overall": "UNVERIFIED"},
        }
        final_ref = put("final.json", final)
        adjudication_ref = put("adjudication.json", {
            "run": run, "candidate": candidate, "finalSha256": final_ref["sha256"],
            "reportSha256": report_ref["sha256"], "claimsAdjudicated": True,
            "verdict": "UNVERIFIED", "claimChecks": [{
                "claim": "synthetic", "evidence": "fixture only", "disposition": "unverified",
            }],
            "acceptedFindings": [], "openClaimIds": [], "coordinatorClaimIds": [],
        })
        acceptance_ref = put("acceptance.json", {
            "run": run, "candidate": candidate, "reviewAccepted": True,
            "verdict": "UNVERIFIED", "finalSha256": final_ref["sha256"],
            "reportSha256": report_ref["sha256"], "adjudication": adjudication_ref,
        })
        spec = {
            "family": "claude", "run": run, "session": session, "snapshot": candidate,
            "role": "replacement-independent", "originalSession": "3847f453-7c80-4ede-88d3-6771cca5f794",
            "originalReviewerConfirmation": False, "verdict": "UNVERIFIED",
            "acceptance": acceptance_ref,
        }
        refs, _, _ = collect_replacement_record(spec, preflight_ref, final_ref, read)
        self.assertEqual(refs["bootstrap"], bootstrap_ref)
        self.assertEqual(refs["coreAuthorization"], authorization_ref)
        self.assertEqual(refs["bootstrapEventSnapshot"], snapshot_ref)


if __name__ == "__main__":
    unittest.main()

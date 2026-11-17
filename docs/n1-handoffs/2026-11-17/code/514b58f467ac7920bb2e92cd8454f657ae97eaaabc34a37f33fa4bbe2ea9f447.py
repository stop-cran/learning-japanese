"""Synthetic, undelivered B134 protocol controls and two-phase audit."""
import copy
import datetime
import importlib.util
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
from b134_common import CORE, CORE_SHA, HERE, PACKET, PROTOCOL, SUMS_SHA, frozen, sha, start_guard, write_frozen
from b134_capacity import load_forecast, phase2_gate, telemetry
from b134_runtime import expected_message, extension_sources, validate_prepared_extension, verify_chain
from review_chain_with_optional import build_chain, validate_selection

ROOT = HERE / "synthetic-validation-001"


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, PROTOCOL / filename)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


AUDIT = module("b134_test_auditor", "audit-review-b134-001.py")
STRUCTURE = module("b134_test_structure", "check-report-structure-b134-001.py")
PREPARE = module("b134_test_extension", "prepare-extension-b134-001.py")
STEP = module("b134_test_step", "step-b134-001.py")


def events_for(config, core, skip_final=False):
    rows = [{"type": "session.start", "data": {"contextTier": "long_context", "selectedModel": "gpt-6.1-sol"}},
            {"type": "user.message", "data": {"content": frozen(config["kickoff"]).decode("ascii"),
                                               "source": "agent-" + config["coordinator"]}},
            {"type": "session.usage_record", "data": {"usage": {
                "inputTokens": 320000, "maxPromptTokens": 922000,
                "model": "gpt-fixture", "responseModel": "gpt-fixture"}}}]
    counter = 0

    def call(name, args, result):
        nonlocal counter
        counter += 1
        cid = "fixture-" + str(counter)
        rows.extend([
            {"type": "assistant.message", "data": {"model": "gpt-fixture", "apiCallId": cid,
                "toolRequests": [{"toolCallId": cid, "name": name, "arguments": args}]}},
            {"type": "tool.execution_complete", "data": {"toolCallId": cid, "success": True,
                                                           "result": {"content": result}}}])
    paths = [config["prompt"]] + [row["path"] for row in core["segments"]]
    if skip_final:
        paths.pop()
    for path in paths:
        call("view", {"path": path, "forceReadLargeFiles": True}, frozen(path).decode("utf-8"))
    call("send_session_message", {"session_id": config["coordinator"],
                                  "message": "D: none\nE: none\nO: none"}, "fixture-only accepted")
    rows.append({"type": "assistant.turn_end", "data": {}})
    return rows


class Controls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = json.loads(frozen(HERE / "audit-configs-001" / "audit-gpt-001.json"))
        cls.core = json.loads(frozen(CORE, CORE_SHA))
        sums = json.loads(frozen(PACKET / "SHA256SUMS.json", SUMS_SHA))
        cls.reference = json.loads(frozen(PACKET / "eligibility-reference.json", sums["eligibility-reference.json"]))
        cls.forecast = load_forecast()
        cls.events = events_for(cls.config, cls.core)

    def test_selection_rejections(self):
        fake = {"newCards": ["甲"], "otherRequiredCards": [],
                "cards": [{"distractors": ["乙"], "quiz_exclusions": ["丙"]}]}
        self.assertTrue(validate_selection("D: none\nE: none\nO: none", fake)["valid"])
        self.assertFalse(validate_selection("D1 乙 - 甲: fixture\nE: none", fake)["valid"])
        self.assertFalse(validate_selection("D1 丁 - 甲: fixture\nD2 丁 - 甲: fixture\nE: none", fake)["valid"])
        self.assertFalse(validate_selection("D: none\nE1 丁 - fixture", fake)["valid"])

    def test_coverage_and_compaction_rejected(self):
        missing = AUDIT.audit_base(events_for(self.config, self.core, True), self.config,
                                   self.core, self.reference)
        self.assertEqual(missing["status"], "VOID")
        self.assertTrue(any("complete core coverage" in x for x in missing["breaches"]))
        self.assertEqual(telemetry(self.events, self.forecast, "gpt")["status"], "PASS")
        bad = self.events + [{"type": "session.compaction_start", "data": {}}]
        self.assertEqual(telemetry(bad, self.forecast, "gpt")["status"], "HOLD")
        missing_usage = [e for e in self.events if e["type"] != "session.usage_record"]
        self.assertEqual(telemetry(missing_usage, self.forecast, "gpt")["status"], "HOLD")
        self.assertFalse(phase2_gate(bad, self.forecast, 1, "gpt")["sendPhase2Message"])
        near_limit = copy.deepcopy(self.events)
        next(e for e in near_limit if e["type"] == "session.usage_record")["data"]["usage"]["inputTokens"] = 920000
        self.assertFalse(phase2_gate(near_limit, self.forecast, 1, "gpt")["sendPhase2Message"])

    def test_serial_roster_and_adapter(self):
        now = STEP.now()
        coordinator = self.config["coordinator"]
        rows = [{"id": coordinator, "name": "coordinator", "activity": {"status": "busy"}},
                {"id": "fixture", "name": "fixture", "activity": {"status": "idle"}, "is_running": False}]
        status = {"summary": {"total": 2}, "sessions": rows}
        roster = [{"id": row["id"]} for row in rows]
        self.assertEqual(STEP.roster_check(status, roster, "fresh reviewer", now), 2)
        busy = copy.deepcopy(status)
        busy["sessions"][1]["activity"]["status"] = "busy"
        with self.assertRaises(ValueError):
            STEP.roster_check(busy, roster, "fresh reviewer", now)
        with self.assertRaises(ValueError):
            STEP.roster_check(status, roster, "fresh reviewer", now - datetime.timedelta(seconds=121))
        with patch.object(STEP, "HERE", ROOT / "no-prior"), \
             patch.object(STEP, "inputs", return_value=({"run": self.config["run"]}, self.config)):
            with self.assertRaises(FileNotFoundError):
                STEP.admit("gpt", "unused")
        code, output, receipt = STEP.child("-c", "import b134_capacity; print('CHILD_IMPORT_OK')")
        self.assertEqual(code, 0)
        self.assertIn("CHILD_IMPORT_OK", output)
        self.assertTrue((Path(receipt) / "receipt.json").is_file())
        self.assertFalse((Path(receipt) / "receipt.json").stat().st_mode & 0o200)

    def test_substantive_adjudication_binding(self):
        run = self.config["run"]
        case = ROOT / "adjudication"
        report = case / "report.md"
        report_raw = b"synthetic report only\n"
        write_frozen(report, report_raw)
        final = {"status": "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION",
                 "report": {"sha256": sha(report_raw)}, "structure": {"overall": "UNVERIFIED"}}
        final_raw = (json.dumps(final) + "\n").encode()
        write_frozen(case / (run + "-final.json"), final_raw)
        adj = {"candidate": self.config["candidate"], "run": run, "finalSha256": sha(final_raw),
               "reportSha256": sha(report_raw), "claimsAdjudicated": True, "verdict": "UNVERIFIED",
               "claimChecks": [{"claim": "fixture claim", "evidence": "fixture", "disposition": "unverified"}]}
        bad_path = case / "invalid.json"
        write_frozen(bad_path, (json.dumps({**adj, "verdict": "CLEAN"}) + "\n").encode())
        wrong_report = case / "wrong-report.json"
        write_frozen(wrong_report, (json.dumps({**adj, "reportSha256": "0" * 64}) + "\n").encode())
        good_path = case / "valid.json"
        write_frozen(good_path, (json.dumps(adj) + "\n").encode())
        config = {**self.config, "report": str(report)}
        with patch.object(STEP, "HERE", case), patch.object(STEP, "inputs", return_value=({}, config)):
            with self.assertRaises(ValueError):
                STEP.accept("gpt", bad_path)
            with self.assertRaises(ValueError):
                STEP.accept("gpt", wrong_report)
            other_report = case / "altered-report.md"
            write_frozen(other_report, b"altered synthetic report\n")
            with patch.object(STEP, "inputs", return_value=({}, {**config, "report": str(other_report)})):
                with self.assertRaises(ValueError):
                    STEP.accept("gpt", good_path)
            self.assertFalse((case / (run + "-acceptance.json")).exists())
            STEP.accept("gpt", good_path)
        self.assertTrue((case / (run + "-acceptance.json")).is_file())

    def test_expired_during_admission(self):
        case = ROOT / "admission"
        case.mkdir(parents=True, exist_ok=True)
        observed = STEP.now()
        coordinator = self.config["coordinator"]
        rows = [{"id": coordinator, "name": "coordinator", "activity": {"status": "busy"}},
                {"id": "fixture", "name": "fixture", "activity": {"status": "idle"}}]
        status = case / "status.json"
        roster = case / "roster.json"
        request = case / "request.json"
        status.write_text(json.dumps({"summary": {"total": 2}, "sessions": rows}), encoding="utf-8")
        roster.write_text(json.dumps([{"id": r["id"]} for r in rows]), encoding="utf-8")
        request.write_text(json.dumps({"statusPath": str(status), "rosterPath": str(roster),
                                       "observedAt": observed.isoformat()}), encoding="utf-8")
        spec = {"run": self.config["run"], "launch": {"sessionName": "fresh reviewer"}}
        class Guard:
            def finish(self):
                return {"breach": None}
        class Resource:
            def available_ram(self):
                return 3 * 1024 ** 3
        class FakeGit:
            def __init__(self, *args):
                pass
            def __call__(self, *args):
                if args[0] == "rev-parse":
                    return (STEP.CANDIDATE + "\n").encode()
                if args[0] == "status":
                    return b""
                return f"{STEP.BASE}|G|{STEP.FINGERPRINT}|{STEP.OWNER}|{STEP.OWNER}\n".encode()
        proof = json.dumps({"candidate": STEP.CANDIDATE, "base": STEP.BASE, "status": "PASS",
                            "memory": {"breach": None}}).encode()
        with patch.object(STEP, "HERE", case), patch.object(STEP, "inputs", return_value=(spec, self.config)), \
             patch.object(STEP, "now", side_effect=[observed, observed + datetime.timedelta(seconds=121)]), \
             patch.object(STEP, "start_guard", return_value=(Guard(), Resource())), \
             patch.object(STEP, "Git", FakeGit), patch.object(STEP, "frozen", return_value=proof), \
             patch.object(STEP, "verify_packet"), patch.object(STEP, "validate_report_destination"):
            with self.assertRaisesRegex(ValueError, "expired during verification"):
                STEP.admit("claude", str(request))
        self.assertFalse(list(case.glob("*-admission-*")))

    def test_synthetic_nonempty_extension(self):
        case = ROOT / "nonempty"
        packet = case / "packet"
        fake = {"newCards": ["甲"], "otherRequiredCards": [],
                "cards": [{"distractors": ["乙"], "quiz_exclusions": ["丙"]}]}
        files = {
            "eligibility-reference.json": (json.dumps(fake, ensure_ascii=False) + "\n").encode(),
            "repo/kanji/丁.md": b"synthetic fixture article\n",
            "repo/kanji/丙.md": b"synthetic exclusion article\n",
            "evidence/jmdict-families.xml": (
                "<JMdict>\n<entry><ent_seq>1</ent_seq><k_ele><keb>丁</keb></k_ele></entry>\n"
                "</JMdict>\n").encode(),
        }
        sums = {}
        for name, raw in files.items():
            sums[name] = write_frozen(packet / name, raw)["sha256"]
        text = "D1 丁 - 甲: fixture\nD2 戊 - 甲: fixture\nE1 丙 - fixture\nO: none"
        with patch("b134_runtime.PACKET", packet):
            sources, missing, matches = extension_sources(text, sums)
        self.assertEqual(len(sources), 2)
        self.assertEqual(missing, ["D2 戊 - 甲: fixture"])
        self.assertEqual(matches, {"丁": ["1"], "戊": [], "丙": []})
        guard, _ = start_guard("B134 synthetic nonempty extension")
        try:
            chain = build_chain(sources, case / "chains", case / "manifest.json", guard, "synthetic only")
            self.assertEqual(verify_chain(chain, sources)["sources"], 2)
        finally:
            self.assertFalse(guard.finish()["breach"])
        message = expected_message(chain, missing, matches)
        self.assertIn("Missing entries:\nD2 戊 - 甲: fixture", message)
        self.assertIn("No exact-keb match in frozen union: 戊 丙", message)

    def test_synthetic_two_phase(self):
        case = ROOT / "two-phase"
        report = case / "report" / "synthetic.md"
        report.parent.mkdir(parents=True)
        config = {**self.config, "report": str(report)}
        first = AUDIT.audit(self.events, config, self.core, self.reference)
        self.assertEqual(first["status"], "PHASE1_READY", first["breaches"])
        audit_dir = case / config["run"] / "audit-fixture"
        events_raw = b"".join((json.dumps(e, ensure_ascii=False) + "\n").encode() for e in self.events)
        write_frozen(audit_dir / "events.jsonl", events_raw)
        first["eventsSha256"] = sha(events_raw)
        audit_path = audit_dir / "audit.json"
        write_frozen(audit_path, (json.dumps(first, ensure_ascii=False) + "\n").encode())
        reply_path = audit_dir / "phase1-list.txt"
        write_frozen(reply_path, b"D: none\nE: none\nO: none")
        config_path = case / "config.json"
        write_frozen(config_path, (json.dumps(config, ensure_ascii=False) + "\n").encode())
        args = ["prepare-extension", "--config", str(config_path),
                "--reply", str(reply_path), "--phase1-audit", str(audit_path)]
        with patch.object(PREPARE, "HERE", case), patch.object(sys, "argv", args):
            PREPARE.main()
        extension = json.loads(frozen(case / (config["run"] + "-extension.json")))
        message = frozen(case / (config["run"] + "-phase2-message.txt")).decode()
        with patch("b134_runtime.HERE", case):
            valid = validate_prepared_extension(config, extension, "D: none\nE: none\nO: none", message, audit_path)
            self.assertEqual(valid["status"], "PASS")
            with self.assertRaises(ValueError):
                validate_prepared_extension(config, extension, "D: none\nE: none\nO: none",
                                            message.split("\n")[0], audit_path)
        body = """# B134 initial review — N1-B134-GPT-001

## Overall verdict
Verdict: UNVERIFIED
## Facet verdicts
### Correctness
Verdict: UNVERIFIED
Basis: synthetic only
### Scoped coverage
Verdict: UNVERIFIED
Basis: synthetic only
### Consistency/quiz safety
Verdict: UNVERIFIED
Basis: synthetic only
### Comprehensibility
Verdict: UNVERIFIED
Basis: synthetic only
## Segments read
Core chain: fixture
Extension chain: fixture
## Phase-1 D/E lists
D: none
E: none
O: none
Missing entries: none
## D/E cards read
None read.
## Per-card results
| Card | Correctness | Scoped coverage | Consistency/quiz safety | Comprehensibility | Evidence |
| --- | --- | --- | --- | --- | --- |
| 紫 | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | synthetic |
## Findings
None.
## Optional points
None.
## Limits
- L1: synthetic fixture only
"""
        rows = copy.deepcopy(self.events)
        rows.append({"type": "user.message", "data": {"content": message,
                                                       "source": "agent-" + config["coordinator"]}})

        def call(name, args, result):
            cid = "fixture-final-" + str(len(rows))
            rows.extend([{"type": "assistant.message", "data": {"model": "gpt-fixture", "apiCallId": cid,
                          "toolRequests": [{"toolCallId": cid, "name": name, "arguments": args}]}},
                         {"type": "tool.execution_complete", "data": {"toolCallId": cid, "success": True,
                                                                        "result": {"content": result}}}])
        for segment in extension["segments"]:
            call("view", {"path": segment["path"], "forceReadLargeFiles": True},
                 frozen(segment["path"]).decode("utf-8"))
        call("create", {"path": str(report), "file_text": body}, "fixture-only created")
        report.write_text(body, encoding="utf-8", newline="\n")
        call("view", {"path": str(report), "forceReadLargeFiles": True}, body)
        call("send_session_message", {"session_id": config["coordinator"], "message": "UNVERIFIED"},
             "fixture-only accepted")
        rows.append({"type": "assistant.turn_end", "data": {}})
        write_frozen(case / (config["run"] + "-phase1.json"),
                     (json.dumps({"auditDir": str(audit_dir)}) + "\n").encode())
        with patch("b134_common.HERE", case), patch("b134_runtime.HERE", case):
            final = AUDIT.audit(rows, config, self.core, self.reference, extension,
                                "D: none\nE: none\nO: none", message, final=True)
        self.assertEqual(final["status"], "FINAL_AUDIT_NEEDS_CLAIM_CHECK", final["breaches"])
        self.assertTrue(final["readbackVerified"])
        selection = validate_selection("D: none\nE: none\nO: none", self.reference)
        checked = STRUCTURE.check(body, config["run"], self.core, extension, self.reference,
                                  selection, message, "UNVERIFIED")
        self.assertEqual(checked["status"], "PASS", checked)
        broken = STRUCTURE.check(body.replace("## Limits", "## Bad"), config["run"], self.core,
                                 extension, self.reference, selection, message, "UNVERIFIED")
        self.assertNotEqual(broken["status"], "PASS")


def main():
    if ROOT.exists():
        raise ValueError("Preserve existing validation")
    guard, _ = start_guard("B134 synthetic protocol controls")
    try:
        result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Controls))
        if not result.wasSuccessful():
            raise SystemExit(1)
    finally:
        if guard.finish()["breach"]:
            raise RuntimeError("Synthetic validation RAM breach")


if __name__ == "__main__":
    main()

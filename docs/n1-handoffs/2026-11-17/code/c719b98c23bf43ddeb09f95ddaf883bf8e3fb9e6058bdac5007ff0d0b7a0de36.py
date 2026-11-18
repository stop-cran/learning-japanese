"""Synthetic controller finalization, acceptance and admission-readiness controls."""
import datetime
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("b134_step_controller_011", HERE / "step-b134-011.py")
step = importlib.util.module_from_spec(spec)
spec.loader.exec_module(step)


class ControllerControls(unittest.TestCase):
    def test_roster_readiness_rejects_stale_incomplete_and_busy(self):
        observed = datetime.datetime.now(datetime.timezone.utc)
        coordinator = step.COORDINATOR
        rows = [
            {"id": coordinator, "name": "coordinator", "activity": {"status": "busy"}},
            {"id": "synthetic-reviewer", "name": "other", "activity": {"status": "idle"},
             "is_running": False},
        ]
        status = {"summary": {"total": 2}, "sessions": rows}
        roster = [{"id": row["id"]} for row in rows]
        self.assertEqual(step.roster_check(status, roster, "new reviewer", observed), 2)
        busy = json.loads(json.dumps(status))
        busy["sessions"][1]["activity"]["status"] = "busy"
        with self.assertRaises(ValueError):
            step.roster_check(busy, roster, "new reviewer", observed)
        with self.assertRaises(ValueError):
            step.roster_check(status, roster, "new reviewer",
                              observed - datetime.timedelta(seconds=121))
        with self.assertRaises(ValueError):
            step.roster_check(status, roster[:-1], "new reviewer", observed)

    def test_final_readback_and_acceptance_records(self):
        with tempfile.TemporaryDirectory(prefix="b134-controller-final-") as directory:
            case = Path(directory)
            run = "N1-B134-CLAUDE-FRESH-002"
            session = "123e4567-e89b-42d3-a456-426614174000"
            report = case / "review.md"
            report_raw = b"synthetic report only\n"
            report.write_bytes(report_raw)
            report.chmod(0o444)
            ext = case / f"{run}-extension.json"
            ext.write_bytes(b"{}\n")
            ext.chmod(0o444)
            message = case / f"{run}-phase2-message.txt"
            message.write_text("synthetic phase 2\n", encoding="utf-8")
            message.chmod(0o444)
            phase_dir = case / "phase1-audit"
            phase_dir.mkdir()
            phase_events = b'{"type":"session.start"}\n'
            (phase_dir / "events.jsonl").write_bytes(phase_events)
            (phase_dir / "events.jsonl").chmod(0o444)
            (phase_dir / "phase1-list.txt").write_text("D: none\nE: none\nO: none", encoding="utf-8")
            (phase_dir / "phase1-list.txt").chmod(0o444)
            (phase_dir / "audit.json").write_text("{}\n", encoding="utf-8")
            (phase_dir / "audit.json").chmod(0o444)
            step.write_frozen(case / f"{run}-phase1.json", (json.dumps({
                "readyForPhase2": True, "session": session, "auditDir": str(phase_dir),
            }) + "\n").encode())
            final_events = phase_events + b'{"type":"assistant.turn_end"}\n'
            audit_dir = case / "final-audit"
            audit_dir.mkdir()
            step.write_frozen(audit_dir / "events.jsonl", final_events)
            audit_result = {
                "status": "FINAL_AUDIT_NEEDS_CLAIM_CHECK", "breaches": [],
                "unexpectedUserMessages": 0, "reviewerIdle": True,
                "coreRead": 90, "coreRequired": 90, "extensionRead": 1, "extensionRequired": 1,
                "writes": 1, "readbacks": 1, "readbackVerified": True, "fetches": 0,
                "messages": ["D: none\nE: none\nO: none", "UNVERIFIED"],
                "eventsSha256": step.sha(final_events),
            }
            audit_path = audit_dir / "audit.json"
            step.write_frozen(audit_path, (json.dumps(audit_result) + "\n").encode())
            config = {
                "run": run, "report": str(report), "coreManifest": str(case / "core.json"),
                "reference": str(case / "reference.json"),
                "reportStructureChecker": str(case / "structure-checker.py"),
            }
            spec_value = {"run": run, "report": str(report),
                          "auditConfig": {"path": str(case / "audit-config.json")}}

            def fake_audit(*args):
                return audit_path, audit_result, "synthetic audit receipt"

            def fake_child(*args):
                return 0, json.dumps({"status": "PASS", "overall": "UNVERIFIED"}), "checker receipt"

            with patch.object(step, "HERE", case), patch.object(step, "inputs",
                    return_value=(spec_value, config)), patch.object(step, "audit", side_effect=fake_audit), \
                    patch.object(step, "child", side_effect=fake_child):
                self.assertEqual(step.final("claude", session), 0)
                final_path = case / f"{run}-final.json"
                final_raw = step.frozen(final_path)
                final_record = json.loads(final_raw)
                self.assertEqual(final_record["status"], "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION")
                adjudication = case / "adjudication.json"
                step.write_frozen(adjudication, (json.dumps({
                    "candidate": step.CANDIDATE, "run": run,
                    "finalSha256": step.sha(final_raw), "reportSha256": step.sha(report_raw),
                    "claimsAdjudicated": True, "verdict": "UNVERIFIED",
                    "coordinatorClaimIds": [],
                    "claimChecks": [{"claim": "synthetic", "evidence": "fixture",
                                     "disposition": "unverified"}],
                }) + "\n").encode())
                original = step.INITIALS["claude"]["session"]
                spec_value.update(role="replacement-independent",
                                  originalSession=original, originalReviewerConfirmation=False)
                config["report"] = str(report)
                self.assertIsNone(step.accept("claude", adjudication))
                acceptance = json.loads(step.frozen(case / f"{run}-acceptance.json"))
                self.assertTrue(acceptance["reviewAccepted"])
                self.assertEqual(acceptance["finalSha256"], step.sha(final_raw))


if __name__ == "__main__":
    unittest.main()

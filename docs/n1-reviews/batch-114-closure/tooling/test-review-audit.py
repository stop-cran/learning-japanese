"""Synthetic event-parser fixtures plus a mechanism-only regression on the accepted B113-009 record.

No session, IPC or delivery probe. Regression assertions use counts and statuses only; no B113 content
flows into any B114 artifact.
"""
import importlib.util
import io
import json
import stat
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("review_audit", HERE / "audit-review.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

PARENT = "fixture-parent-0001"
MODEL = "claude-fixture-5.5"
LIST = "D: none\nE: none"
REFERENCE = {
    "newCards": ["一", "二"], "otherRequiredCards": [],
    "cards": [{"card": "一", "distractors": ["三"], "quiz_exclusions": ["四"]},
              {"card": "二", "distractors": ["三"], "quiz_exclusions": []}],
}
B113 = Path(r"C:\Users\stop-\n1-kanji-workspace\scratch-113")


class Fixture(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.cleanup)
        self.root = root = Path(self.temporary.name)
        self.prompt, self.kickoff = root / "prompt.txt", root / "kickoff.txt"
        self.report = str(root / "report.md")
        self.prompt.write_bytes(b"fixture instructions\n")
        self.kickoff_text = f"Read {self.prompt} using one view call, then follow it."
        self.kickoff.write_bytes(self.kickoff_text.encode("utf-8"))
        self.core_files = [root / "core-1.txt", root / "core-2.txt"]
        self.ext = root / "ext-1.txt"
        for index, path in enumerate(self.core_files + [self.ext]):
            path.write_bytes(f"segment {index}\nNEXT\n".encode("utf-8"))
        self.config = {"run": "FIXTURE-RUN", "kickoff": str(self.kickoff), "prompt": str(self.prompt),
                       "report": self.report, "coordinator": PARENT, "expectedFamily": "claude"}
        self.core = {"segments": [{"path": str(p), "sha256": module.digest(p.read_bytes())} for p in self.core_files]}
        self.extension = {"segments": [{"path": str(self.ext), "sha256": module.digest(self.ext.read_bytes())}]}
        self.phase2 = f"{self.ext}\nMissing entries: none"
        self.reset()

    def cleanup(self):
        for path in self.root.rglob("*"):
            if path.is_file():
                path.chmod(stat.S_IREAD | stat.S_IWRITE)
        self.temporary.cleanup()

    def reset(self):
        if Path(self.report).exists():
            Path(self.report).chmod(stat.S_IREAD | stat.S_IWRITE)
        Path(self.report).unlink(missing_ok=True)
        self.counter = 0
        self.events = [{"type": "session.start", "data": {}}, self.user(self.kickoff_text),
                       {"type": "session.usage_record", "data": {"usage": {
                           "model": MODEL, "responseModel": "claude-fixture-5-5"}}}]
        for path in [self.prompt] + self.core_files:
            self.view(path)

    def user(self, content, source="agent-" + PARENT):
        data = {"content": content, "transformedContent":
                f"<cross_session_message>\nfrom_session_id: {PARENT}\n</cross_session_message>\n{content}"}
        if source is not None:
            data["source"] = source
        return {"type": "user.message", "data": data}

    def call(self, name, args, returned="ok", api=None, text="", success=True):
        self.counter += 1
        cid = f"call-{self.counter}"
        self.events += [
            {"type": "assistant.message", "data": {"content": text, "model": MODEL,
                                                   "apiCallId": api or f"api-{self.counter}", "toolRequests": [
                                                       {"toolCallId": cid, "name": name, "arguments": args}]}},
            {"type": "tool.execution_start", "data": {"toolCallId": cid, "toolName": name, "arguments": args,
                                                      "model": MODEL}},
            {"type": "tool.execution_complete", "data": {"toolCallId": cid, "success": success,
                                                         "result": {"content": returned}}},
        ]

    def view(self, path, **extra):
        self.call("view", {"path": str(path), "forceReadLargeFiles": True},
                  Path(path).read_bytes().decode("utf-8"), **extra)

    def end_turn(self):
        self.events.append({"type": "assistant.turn_end", "data": {}})

    def phase_one(self, message=LIST):
        self.call("send_session_message", {"session_id": PARENT, "message": message}, "accepted")
        self.end_turn()

    def finish(self, write="create", text="fixture report\n", disk=None):
        self.phase_one()
        self.events.append(self.user(self.phase2))
        self.view(self.ext)
        if write == "create":
            self.call("create", {"path": self.report, "file_text": text}, "Created file")
        else:
            body = "".join("+" + line + "\n" for line in text.splitlines())
            self.call("apply_patch", f"*** Begin Patch\n*** Add File: {self.report}\n{body}*** End Patch\n")
        Path(self.report).write_bytes((text if disk is None else disk).encode("utf-8"))
        self.view(self.report)
        self.call("send_session_message", {"session_id": PARENT, "message": self.report + "\nCLEAN"}, "accepted")
        self.end_turn()

    def result(self, final=False, incomplete=False, phase1=LIST):
        return module.audit(self.events, self.config, self.core, REFERENCE, self.extension, phase1,
                            self.phase2, final, incomplete)

    def assertVoid(self, fragment):
        result = self.result()
        self.assertEqual(result["status"], "VOID")
        self.assertTrue(any(fragment in breach for breach in result["breaches"]), result["breaches"])


class AuditTests(Fixture):
    def test_phase_one_ready_requires_ended_turn(self):
        self.call("send_session_message", {"session_id": PARENT, "message": LIST}, "accepted")
        self.assertEqual(self.result()["status"], "PENDING")
        self.end_turn()
        result = self.result()
        self.assertEqual(result["status"], "PHASE1_READY")
        self.assertEqual(result["phase1ListSha256"], module.digest(LIST.encode("utf-8")))
        self.assertEqual(result["actualResponseModels"], ["claude-fixture-5-5"])

    def test_partial_tail_is_pending_and_corrupt_middle_raises(self):
        events, incomplete = module.load_events(b'{"type": "a"}\n{"type": ')
        self.assertEqual((len(events), incomplete), (1, True))
        self.phase_one()
        self.assertEqual(self.result(incomplete=True)["status"], "PENDING")
        with self.assertRaises(json.JSONDecodeError):
            module.load_events(b'{"type": \n{"type": "a"}\n')

    def test_kickoff_bytes_and_provenance(self):
        self.events[1]["data"]["content"] += "\n"
        self.assertVoid("kickoff is not byte-equal")
        self.reset()
        self.events[1]["data"]["source"] = "agent-someone-else"
        self.assertVoid("Kickoff provenance")

    def test_truncated_bootstrap_or_segment_is_void(self):
        for index, fragment in ((5, "Bootstrap read"), (8, "View output differs")):
            with self.subTest(index=index):
                self.reset()
                self.events[index]["data"]["result"]["content"] = "truncated"
                self.assertVoid(fragment)

    def test_multiple_calls_in_one_response_are_void(self):
        self.view(self.core_files[1], api="shared")
        self.view(self.core_files[1], api="shared")
        self.assertVoid("More than one tool call")

    def test_scope_reread_range_and_executed_argument_rules(self):
        (self.root / "other.txt").write_bytes(b"x\n")
        self.view(self.root / "other.txt")
        self.assertVoid("Out-of-scope view")
        self.reset()
        self.view(self.prompt)
        self.assertVoid("Instruction file re-read")
        self.reset()
        self.call("view", {"path": str(self.core_files[0]), "forceReadLargeFiles": True, "view_range": [1, 2]})
        self.assertVoid("without view_range")
        self.reset()
        self.call("view", {"path": str(self.core_files[0])}, self.core_files[0].read_bytes().decode("utf-8"))
        self.assertEqual(self.result()["breaches"], [])
        self.call("view", {"path": str(self.core_files[1]), "forceReadLargeFiles": False})
        self.assertVoid("without view_range")
        self.reset()
        self.view(self.core_files[0])
        self.events[-2]["data"]["arguments"] = {"path": str(self.prompt), "forceReadLargeFiles": True}
        self.assertVoid("Executed arguments differ")

    def test_selection_and_frozen_list_binding(self):
        self.phase_one("D1 五 - no colon\nE: none")
        self.assertVoid("Selection:")
        self.reset()
        self.phase_one("D1 五 - 一: number\nE: none")
        self.assertVoid("differs from the frozen list")

    def test_fetch_rules(self):
        url = "https://example.org/fixture"
        self.call("web_fetch", {"url": url}, text=f"Fetching {url} to confirm a reading.")
        self.assertEqual(self.result()["breaches"], [])
        cases = [("Fetching nothing in particular", url), (None, "http://example.org/a"),
                 (None, "https://localhost/a"), (None, "https://10.0.0.1/a")]
        for text, target in cases:
            with self.subTest(target=target, text=text):
                self.reset()
                self.call("web_fetch", {"url": target}, text=text or f"Fetching {target} to confirm a reading.")
                self.assertEqual(self.result()["status"], "VOID")
        self.reset()
        for number in range(4):
            target = f"https://example.org/{number}"
            self.call("web_fetch", {"url": target}, text=f"Fetching {target} to confirm a reading.")
        self.assertVoid("over-cap fetch")

    def test_model_family_rules(self):
        self.events[2]["data"]["usage"]["responseModel"] = "gpt-fixture"
        self.assertVoid("Unexpected response model")
        self.reset()
        self.events[3]["data"]["model"] = "gpt-fixture"
        self.assertVoid("Unexpected assistant model")

    def test_complete_create_run_needs_claim_check_and_ended_turn(self):
        self.finish()
        result = self.result(final=True)
        self.assertEqual((result["status"], result["breaches"], result["reportBinding"]),
                         ("FINAL_AUDIT_NEEDS_CLAIM_CHECK", [], "exact"))
        self.assertIn("Every report claim", result["acceptanceLimit"])
        self.events.pop()
        self.assertEqual(self.result(final=True)["status"], "PENDING")

    def test_apply_patch_with_crlf_disk_report(self):
        self.finish("apply_patch", "line one\nline two\n", "line one\r\nline two\r\n")
        result = self.result(final=True)
        self.assertEqual((result["status"], result["reportBinding"]),
                         ("FINAL_AUDIT_NEEDS_CLAIM_CHECK", "line-endings-normalized"))

    def test_report_tamper_and_bad_patch_are_void(self):
        self.finish()
        Path(self.report).write_bytes(b"tampered\n")
        result = self.result(final=True)
        self.assertEqual(result["status"], "VOID")
        self.assertIn("Report readback differs from the report on disk", result["breaches"])
        self.assertIsNone(module.patch_text(f"*** Begin Patch\n*** Add File: {self.report}x\n+a\n*** End Patch", self.report))
        self.assertIsNone(module.patch_text(f"*** Begin Patch\n*** Add File: {self.report}\n a\n*** End Patch", self.report))
        self.assertEqual(module.patch_text(f"*** Begin Patch\n*** Add File: {self.report}\n+a\n+\n*** End Patch\n",
                                           self.report), "a\n\n")

    def test_report_readback_must_be_forced(self):
        self.finish()
        self.events[-7]["data"]["toolRequests"][0]["arguments"].pop("forceReadLargeFiles")
        result = self.result(final=True)
        self.assertEqual(result["status"], "VOID")
        self.assertIn("Report readback is not a forced full read", result["breaches"])

    def test_phase_two_binding(self):
        self.finish()
        self.events[self.events.index(self.user(self.phase2))]["data"].pop("source")
        self.assertEqual(self.result(final=True)["status"], "FINAL_AUDIT_NEEDS_CLAIM_CHECK")
        self.reset()
        self.phase_one()
        self.events.append(self.user(self.phase2, source="agent-someone-else"))
        result = self.result()
        self.assertEqual((result["status"], result["unexpectedUserMessages"]), ("HOLD", 1))

    def test_gap_completion_and_task_complete_rules(self):
        self.phase_one()
        self.view(self.core_files[0])
        self.assertVoid("phase gap")
        self.reset()
        self.finish()
        self.call("task_complete", {})
        self.assertEqual(self.result(final=True)["status"], "PENDING")
        self.end_turn()
        self.assertEqual(self.result(final=True)["status"], "FINAL_AUDIT_NEEDS_CLAIM_CHECK")
        self.view(self.core_files[0])
        self.assertVoid("after task completion")
        self.reset()
        self.finish()
        self.view(self.ext)
        self.assertVoid("after the completion message")
        self.reset()
        self.call("task_complete", {})
        self.assertVoid("Premature task completion")


class MainTests(Fixture):
    def setUp(self):
        super().setUp()
        self.addCleanup(setattr, module, "OUTPUT_BASE", module.OUTPUT_BASE)
        module.OUTPUT_BASE = self.root / "audits"
        core_manifest, extension_manifest = self.root / "core.json", self.root / "ext.json"
        core_manifest.write_bytes(json.dumps(self.core).encode("utf-8"))
        extension_manifest.write_bytes(json.dumps(self.extension).encode("utf-8"))
        reference = self.root / "reference.json"
        reference.write_bytes(json.dumps(REFERENCE, ensure_ascii=False).encode("utf-8"))
        self.phase1_file, self.phase2_file = self.root / "phase1.txt", self.root / "phase2.txt"
        self.phase1_file.write_bytes(LIST.encode("utf-8"))
        self.phase2_file.write_bytes(self.phase2.encode("utf-8"))
        self.config.update(coreManifest=str(core_manifest), reference=str(reference), files=[
            {"path": str(p), "sha256": module.digest(p.read_bytes())} for p in (self.prompt, self.kickoff)])
        self.config_file = self.root / "config.json"
        self.config_file.write_bytes(json.dumps(self.config).encode("utf-8"))
        for path in [core_manifest, extension_manifest, reference, self.phase1_file, self.phase2_file,
                     self.prompt, self.kickoff, self.config_file] + self.core_files + [self.ext]:
            path.chmod(stat.S_IREAD)
        self.args = ["--session", "fixture-0001", "--config", str(self.config_file),
                     "--events-file", str(self.root / "events.jsonl")]
        self.final_args = self.args + ["--extension", str(extension_manifest), "--phase1-list",
                                       str(self.phase1_file), "--phase2-message", str(self.phase2_file), "--final"]

    def run_main(self, args, record=None):
        record = record if record is not None else "".join(
            json.dumps(e, ensure_ascii=False) + "\n" for e in self.events).encode("utf-8")
        events_file = self.root / "events.jsonl"
        if events_file.exists():
            events_file.chmod(stat.S_IREAD | stat.S_IWRITE)
        events_file.write_bytes(record)
        with redirect_stdout(io.StringIO()) as stdout:
            code = module.main(args)
        audit_path = Path(stdout.getvalue().strip().splitlines()[-1].removeprefix("Audit: "))
        self.assertEqual((audit_path.parent / "events.jsonl").read_bytes(), record)
        return code, json.loads(audit_path.read_bytes()), audit_path.parent

    def test_final_ok_phase1_file_integrity_and_audit_error(self):
        self.finish()
        Path(self.report).chmod(stat.S_IREAD)
        code, result, _ = self.run_main(self.final_args)
        self.assertEqual((code, result["status"], result["breaches"]), (0, "FINAL_AUDIT_NEEDS_CLAIM_CHECK", []))
        self.reset()
        self.phase_one()
        code, result, folder = self.run_main(self.args)
        self.assertEqual((code, result["status"]), (0, "PHASE1_READY"))
        self.assertEqual((folder / "phase1-list.txt").read_bytes(), LIST.encode("utf-8"))
        code, result, _ = self.run_main(self.args, b'{"type": \n{"type": "a"}\n')
        self.assertEqual((code, result["status"]), (2, "AUDIT_ERROR"))
        self.prompt.chmod(stat.S_IREAD | stat.S_IWRITE)
        code, result, folder = self.run_main(self.args)
        self.assertEqual((code, result["status"]), (1, "VOID"))
        self.assertFalse((folder / "phase1-list.txt").exists())


@unittest.skipUnless((B113 / "run-009").is_dir(), "B113-009 record unavailable")
class AcceptedRecordRegression(unittest.TestCase):
    def test_accepted_009_record_has_no_mechanism_breach(self):
        config = {"run": "B113-009-REGRESSION", "coordinator": "2451b10d-02a9-46ab-82d5-d90993f0cb8b",
                  "kickoff": str(B113 / "prompts-113" / "kickoff-009.txt"),
                  "prompt": str(B113 / "prompts-113" / "initial-claude-113-009.txt"),
                  "report": r"C:\Users\stop-\n1-kanji-workspace\reports-113\initial-claude-m5.md",
                  "expectedFamily": "claude"}
        chain = json.loads((B113 / "chain-v4" / "chain-manifest.json").read_bytes())
        core = {"segments": [s for s in chain["segments"] if s["kind"] == "required"]}
        extension = json.loads((B113 / "chain-m6a" / "ext-manifest.json").read_bytes())
        reference = json.loads((B113 / "m6-eligibility-reference.json").read_bytes())
        record = (B113 / "run-009" / "audit-20261113T1356425838058" / "events.jsonl").read_bytes()
        events, incomplete = module.load_events(record)
        result = module.audit(events, config, core, reference, extension,
                              (B113 / "run-009" / "phase1-list.txt").read_bytes().decode("utf-8"),
                              (B113 / "run-009" / "phase2-reply.txt").read_bytes().decode("utf-8"),
                              final=True, record_incomplete=incomplete)
        summary = {key: result[key] for key in ("status", "breaches", "coreRead", "coreRequired", "extensionRead",
                                                "extensionRequired", "writes", "readbackVerified", "reportBinding")}
        self.assertEqual(summary, {"status": "FINAL_AUDIT_NEEDS_CLAIM_CHECK", "breaches": [], "coreRead": 49,
                                   "coreRequired": 49, "extensionRead": 10, "extensionRequired": 10, "writes": 1,
                                   "readbackVerified": True, "reportBinding": summary["reportBinding"]})
        self.assertIn(summary["reportBinding"], ("exact", "line-endings-normalized"))


if __name__ == "__main__":
    unittest.main()

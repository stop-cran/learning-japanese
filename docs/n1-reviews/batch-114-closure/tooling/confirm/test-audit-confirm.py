"""Synthetic fixtures for audit-confirm.py. No session, IPC or delivery probe."""
import importlib.util
import io
import json
import stat
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("confirm_audit", HERE / "audit-confirm.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

PARENT = "fixture-parent-0001"
MODEL = "claude-fixture-5.5"


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
        self.segments = [root / "seg-1.txt", root / "seg-2.txt"]
        for index, path in enumerate(self.segments):
            path.write_bytes(f"segment {index}\nNEXT\n".encode("utf-8"))
        self.config = {"run": "FIXTURE-RUN", "kickoff": str(self.kickoff), "prompt": str(self.prompt),
                       "report": self.report, "coordinator": PARENT, "expectedFamily": "claude"}
        self.chain = {"segments": [{"path": str(p), "sha256": module.digest(p.read_bytes())} for p in self.segments]}
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
        self.events = [self.user(self.kickoff_text),
                       {"type": "session.usage_record", "data": {"usage": {
                           "model": MODEL, "responseModel": "claude-fixture-5-5"}}}]
        for path in [self.prompt] + self.segments:
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

    def write(self, how="create", text="fixture report\n", disk=None):
        if how == "create":
            self.call("create", {"path": self.report, "file_text": text}, "Created file")
        else:
            body = "".join("+" + line + "\n" for line in text.splitlines())
            self.call("apply_patch", f"*** Begin Patch\n*** Add File: {self.report}\n{body}*** End Patch\n")
        Path(self.report).write_bytes((text if disk is None else disk).encode("utf-8"))

    def finish(self, how="create", text="fixture report\n", disk=None, verdict="Confirmation: CONFIRMED"):
        self.write(how, text, disk)
        self.view(self.report)
        self.call("send_session_message", {"session_id": PARENT, "message": self.report + "\n" + verdict}, "ok")
        self.call("task_complete", {"summary": "done"})
        self.end_turn()

    def result(self, final=True, incomplete=False):
        return module.audit(self.events, self.config, self.chain, final, incomplete)

    def assertVoid(self, fragment, final=True):
        result = self.result(final)
        self.assertEqual(result["status"], "VOID")
        self.assertTrue(any(fragment in breach for breach in result["breaches"]), result["breaches"])


class AuditTests(Fixture):
    def test_complete_run_needs_claim_check_and_ended_turn(self):
        self.finish()
        result = self.result()
        self.assertEqual((result["status"], result["breaches"], result["reportBinding"], result["chainRead"]),
                         ("FINAL_AUDIT_NEEDS_CLAIM_CHECK", [], "exact", 2))
        self.events.pop()
        self.assertEqual(self.result()["status"], "PENDING")

    def test_each_verdict_and_crlf_patch(self):
        for verdict in ("NEEDS FIX", "UNVERIFIED - one claim open"):
            with self.subTest(verdict=verdict):
                self.reset()
                self.finish(verdict=verdict)
                self.assertEqual(self.result()["status"], "FINAL_AUDIT_NEEDS_CLAIM_CHECK")
        self.reset()
        self.finish("apply_patch", "a\nb\n", "a\r\nb\r\n")
        result = self.result()
        self.assertEqual((result["status"], result["reportBinding"]),
                         ("FINAL_AUDIT_NEEDS_CLAIM_CHECK", "line-endings-normalized"))

    def test_bad_completion_messages_are_void(self):
        for verdict in ("CLEAN", "CONFIRMED or NEEDS FIX", "CONFIRMED\nextra", "CONFIRMED " + "a" * 64):
            with self.subTest(verdict=verdict):
                self.reset()
                self.finish(verdict=verdict)
                self.assertVoid("Invalid completion message")
        self.reset()
        self.write()
        self.call("send_session_message", {"session_id": PARENT, "message": self.report + "\nCONFIRMED"})
        self.assertVoid("premature completion")

    def test_kickoff_bytes_provenance_and_prekickoff_activity(self):
        self.events[0]["data"]["content"] += "\n"
        self.assertVoid("kickoff is not byte-equal")
        self.reset()
        self.events[0]["data"]["source"] = "agent-someone-else"
        self.assertVoid("Kickoff provenance")
        self.reset()
        self.events.insert(0, {"type": "assistant.message", "data": {"content": "late", "model": MODEL}})
        self.assertVoid("Activity before the kickoff")
        self.reset()
        self.events = [{"type": "session.info", "data": {}}]
        self.assertEqual(self.result(False)["status"], "PENDING")

    def test_bootstrap_truncation_order_and_scope(self):
        self.events[4]["data"]["result"]["content"] = "truncated"
        self.assertVoid("Bootstrap read")
        self.reset()
        self.events = self.events[:5]
        self.view(self.segments[1])
        self.assertVoid("out of order", final=False)
        self.reset()
        (self.root / "other.txt").write_bytes(b"x\n")
        self.view(self.root / "other.txt")
        self.assertVoid("Out-of-scope view", final=False)
        self.reset()
        self.view(self.prompt)
        self.assertVoid("Instruction file re-read", final=False)
        self.reset()
        self.call("view", {"path": str(self.segments[0]), "view_range": [1, 2]})
        self.assertVoid("without view_range", final=False)
        self.reset()
        self.view(self.segments[1], api="api-3")
        self.assertVoid("More than one tool call", final=False)

    def test_write_before_coverage_and_double_write(self):
        self.events = self.events[:8]
        self.write()
        self.assertVoid("before complete chain coverage", final=False)
        self.reset()
        self.write()
        self.write()
        self.assertVoid("repeated write", final=False)

    def test_fetch_rules(self):
        url = "https://example.org/fixture"
        self.call("web_fetch", {"url": url}, text=f"Fetching {url} to confirm a reading.")
        self.assertEqual(self.result(False)["breaches"], [])
        self.reset()
        self.call("web_fetch", {"url": url}, text="Fetching")
        self.assertVoid("same-response URL", final=False)
        self.reset()
        for number in range(4):
            target = f"https://example.org/{number}"
            self.call("web_fetch", {"url": target}, text=f"Fetching {target} to confirm a reading.")
        self.assertVoid("over-cap fetch", final=False)

    def test_post_message_and_task_complete_rules(self):
        self.finish()
        self.view(self.segments[0])
        self.assertVoid("after task completion")
        self.reset()
        self.write()
        self.view(self.report)
        self.call("send_session_message", {"session_id": PARENT, "message": self.report + "\nCONFIRMED"})
        self.view(self.segments[0])
        self.assertVoid("after the completion message", final=False)
        self.reset()
        self.call("task_complete", {})
        self.assertVoid("Premature task completion", final=False)

    def test_unexpected_user_holds_and_model_family(self):
        self.finish()
        self.events.append(self.user("continue"))
        self.events.append({"type": "assistant.turn_end", "data": {}})
        result = self.result()
        self.assertEqual((result["status"], result["unexpectedUserMessages"]), ("HOLD", 1))
        self.reset()
        self.events[1]["data"]["usage"]["responseModel"] = "gpt-fixture"
        self.assertVoid("Unexpected response model", final=False)

    def test_report_tamper_is_void(self):
        self.finish()
        Path(self.report).write_bytes(b"tampered\n")
        self.assertVoid("Report readback differs from the report on disk")


class MainTests(Fixture):
    def setUp(self):
        super().setUp()
        self.addCleanup(setattr, module, "OUTPUT_BASE", module.OUTPUT_BASE)
        module.OUTPUT_BASE = self.root / "audits"
        manifest = self.root / "chain.json"
        manifest.write_bytes(json.dumps(self.chain).encode("utf-8"))
        self.config.update(chainManifest=str(manifest), files=[
            {"path": str(p), "sha256": module.digest(p.read_bytes())} for p in (self.prompt, self.kickoff)])
        self.config_file = self.root / "config.json"
        self.config_file.write_bytes(json.dumps(self.config).encode("utf-8"))
        for path in [manifest, self.prompt, self.kickoff, self.config_file] + self.segments:
            path.chmod(stat.S_IREAD)
        history = [self.user("old initial kickoff"),
                   {"type": "assistant.message", "data": {"content": "old", "model": MODEL, "toolRequests": [
                       {"toolCallId": "old-1", "name": "view", "arguments": {"path": "elsewhere"}}]}},
                   {"type": "assistant.turn_end", "data": {}}]
        self.prefix = "".join(json.dumps(e) + "\n" for e in history).encode("utf-8")

    def run_main(self, record, offset=None, prefix_sha=None, final=True):
        events_file = self.root / "events.jsonl"
        if events_file.exists():
            events_file.chmod(stat.S_IREAD | stat.S_IWRITE)
        events_file.write_bytes(record)
        args = ["--session", "fixture-0001", "--config", str(self.config_file), "--events-file", str(events_file),
                "--offset", str(len(self.prefix) if offset is None else offset),
                "--prefix-sha256", prefix_sha or module.digest(self.prefix)] + (["--final"] if final else [])
        with redirect_stdout(io.StringIO()) as stdout:
            code = module.main(args)
        audit_path = Path(stdout.getvalue().strip().splitlines()[-1].removeprefix("Audit: "))
        self.assertEqual((audit_path.parent / "events.jsonl").read_bytes(), record)
        return code, json.loads(audit_path.read_bytes())

    def test_slice_binding_integrity_and_errors(self):
        self.finish()
        Path(self.report).chmod(stat.S_IREAD)
        body = "".join(json.dumps(e, ensure_ascii=False) + "\n" for e in self.events).encode("utf-8")
        code, result = self.run_main(self.prefix + body)
        self.assertEqual((code, result["status"], result["breaches"]), (0, "FINAL_AUDIT_NEEDS_CLAIM_CHECK", []))
        self.assertEqual(result["sliceSha256"], module.digest(body))
        code, result = self.run_main(self.prefix + body, offset=0, prefix_sha=module.digest(b""))
        self.assertEqual((code, result["status"]), (1, "VOID"))
        code, result = self.run_main(b"x" + self.prefix[1:] + body)
        self.assertEqual((code, result["status"]), (2, "AUDIT_ERROR"))
        code, result = self.run_main(self.prefix, final=False)
        self.assertEqual((code, result["status"]), (0, "PENDING"))
        self.prompt.chmod(stat.S_IREAD | stat.S_IWRITE)
        code, result = self.run_main(self.prefix + body)
        self.assertEqual((code, result["status"]), (1, "VOID"))


if __name__ == "__main__":
    unittest.main()

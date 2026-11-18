"""Controls for runtime-004 using the preserved actual authorized GPT delivery bytes."""
import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

from common import frozen, load_module

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RUNTIME = load_module("b134_authorized_runtime004_under_test", HERE / "b134_authorized_confirmation_v3.py")
PREFLIGHT = ROOT / "authorized-gpt-confirmation-002" / "preflight.json"
ADMISSION = json.loads(frozen(ROOT / "authorized-gpt-admit-001" / "admission.json"))
RAW = frozen(ROOT / "authorized-gpt-final-001" / "events.jsonl")
SUFFIX = RUNTIME.legacy.parse_events(RAW[ADMISSION["offset"]:])
STORED_SHA = "cd978c7fdca267ba768ddac59c6ada138ffb12443b8c3c02f844064559877ac2"
BOUNDED = "Bounded returned-byte/read/write/completion audit failed"


def rows(report, patch=None, names=("view", "apply_patch", "view", "send_session_message"),
         success=True, completions=1):
    patch = ("*** Begin Patch\n*** Add File: " + str(report) + "\n+# T\n+\n+line two\n*** End Patch\n"
             if patch is None else patch)
    events = []
    for index, name in enumerate(names):
        arguments = patch if name.endswith("apply_patch") else {"path": str(report)}
        events.append({"type": "assistant.message", "data": {"toolRequests": [
            {"toolCallId": "call-" + str(index), "name": name, "arguments": arguments}]}})
        for _ in range(completions):
            events.append({"type": "tool.execution_complete",
                           "data": {"toolCallId": "call-" + str(index), "success": success}})
    return events


class AddFileTransportControls(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.report = Path(self.directory.name) / "review.md"
        self.report.write_bytes(b"# T\r\n\r\nline two\r\n")

    def tearDown(self):
        self.directory.cleanup()

    def check(self, events, native=()):
        return RUNTIME.single_add_file_crlf(events, str(self.report), list(native))

    def test_synthetic_exact_crlf_expansion_binds(self):
        bound = self.check(rows(self.report))
        self.assertEqual(bound["rule"], RUNTIME.RULE)
        self.assertEqual(bound["requestedSha256"], hashlib.sha256(b"# T\n\nline two\n").hexdigest())
        self.assertEqual(bound["toolCallId"], "call-1")
        prefixed = rows(self.report, names=("view", "functions.apply_patch", "send_session_message"))
        self.assertIsNotNone(self.check(prefixed))

    def test_stored_byte_mutations_rejected(self):
        for stored in (b"# T\n\nline two\n", b"# T\r\n\r\nline 2\r\n", b"# T\r\n\r\nline two\r\n\r\n",
                       b"# T\r\n\nline two\r\n", b"# T\r\r\n\r\nline two\r\n"):
            self.report.write_bytes(stored)
            self.assertIsNone(self.check(rows(self.report)), stored)

    def test_tool_mutations_rejected(self):
        self.assertIsNone(self.check(rows(self.report), native=[{"name": "create"}]))
        for names in (("apply_patch", "apply_patch"), ("view", "apply_patch", "powershell"),
                      ("create", "apply_patch"), ("edit", "apply_patch"), ("view",),
                      ("apply_patch", "send_session_message", "send_session_message")):
            self.assertIsNone(self.check(rows(self.report, names=names)), names)
        self.assertIsNone(self.check(rows(self.report, success=False)))
        self.assertIsNone(self.check(rows(self.report, completions=0)))
        self.assertIsNone(self.check(rows(self.report, completions=2)))
        events = rows(self.report)
        events[2]["data"]["toolRequests"][0]["arguments"] = {"patch": "x"}
        self.assertIsNone(self.check(events))
        events = rows(self.report)
        events[2]["data"]["toolRequests"][0].pop("toolCallId")
        self.assertIsNone(self.check(events))

    def test_patch_mutations_rejected(self):
        header = "*** Begin Patch\n*** Add File: " + str(self.report) + "\n"
        for patch in (
            header.replace("Add File", "Update File") + "+# T\n+\n+line two\n*** End Patch\n",
            header.replace("review.md", "other.md") + "+# T\n+\n+line two\n*** End Patch\n",
            header + "+# T\n+\n+line two\n*** End Patch",
            header + "+# T\n+\n+line two\n",
            header + "+# T\n \n+line two\n*** End Patch\n",
            header + "+# T\n*** Add File: x\n+line two\n*** End Patch\n",
            header + "+# T\r\n+\r\n+line two\r\n*** End Patch\n",
            "*** Begin Patch\n" + header + "+# T\n+\n+line two\n*** End Patch\n",
        ):
            self.assertIsNone(self.check(rows(self.report, patch=patch)), patch)


class ActualGptControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record, cls.config, _, cls.chain = RUNTIME.legacy.preflight(str(PREFLIGHT))
        cls.stored = frozen(cls.config["report"], STORED_SHA)

    def test_wiring(self):
        self.assertIs(RUNTIME.legacy.audit_snapshot, RUNTIME.active.audit_snapshot)
        self.assertIs(RUNTIME.active.selected_audit, RUNTIME.widened_audit)
        self.assertEqual(Path(RUNTIME.legacy.__file__).resolve(), HERE / "b134_authorized_confirmation_v3.py")
        self.assertEqual(RUNTIME.legacy.PINS["authorizedActualEventV2"][1], RUNTIME.ACTIVE_SHA)

    def test_actual_bytes_bind_exactly(self):
        bound = RUNTIME.single_add_file_crlf(SUFFIX, self.config["report"], [])
        self.assertEqual(bound["hostEditKind"], "apply_patch-add-file")
        self.assertEqual(bound["requestedSha256"],
                         hashlib.sha256(self.stored.replace(b"\r\n", b"\n")).hexdigest())
        self.assertIsNone(RUNTIME.single_add_file_crlf(SUFFIX, self.config["report"], [{"name": "create"}]))
        events = copy.deepcopy(SUFFIX)
        call = next(c for r in events if r["type"] == "assistant.message"
                    for c in (r.get("data") or {}).get("toolRequests", []) if c["name"] == "apply_patch")
        call["arguments"] = call["arguments"].replace("Chain:", "Chain;", 1)
        self.assertIsNone(RUNTIME.single_add_file_crlf(events, self.config["report"], []))

    def test_actual_full_audit_passes_and_retains_auditor_note(self):
        audit, _, structure = RUNTIME.legacy.audit_snapshot(RAW, self.record, self.config, self.chain, ADMISSION)
        self.assertEqual(audit["reportBinding"], "line-endings-normalized")
        self.assertEqual(audit["notes"], [RUNTIME.selected.NORMALIZATION_NOTE])
        self.assertEqual(audit["transportBinding"]["rule"], RUNTIME.RULE)
        self.assertEqual(audit["transportBinding"]["storedSha256"], STORED_SHA)
        self.assertEqual(structure["status"], "PASS")
        self.assertEqual(structure["confirmation"], "CONFIRMED")
        self.assertEqual(frozen(self.config["report"], STORED_SHA), self.stored)

    def test_actual_full_audit_rejects_without_widened_predicate(self):
        original = RUNTIME.selected.single_add_file_crlf
        RUNTIME.selected.single_add_file_crlf = lambda *args: None
        try:
            with self.assertRaisesRegex(Exception, BOUNDED):
                RUNTIME.legacy.audit_snapshot(RAW, self.record, self.config, self.chain, ADMISSION)
        finally:
            RUNTIME.selected.single_add_file_crlf = original


if __name__ == "__main__":
    sys.exit(not unittest.main(argv=[sys.argv[0], "-v"], exit=False).result.wasSuccessful())

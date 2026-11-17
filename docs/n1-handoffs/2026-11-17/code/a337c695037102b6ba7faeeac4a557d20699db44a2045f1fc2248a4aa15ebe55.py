import copy
import tempfile
import unittest
from pathlib import Path

from common import load_module

repair = load_module("b134_native_create_repair",
                     Path(__file__).with_name("b134_revision_confirmation_v3.py"))


class NativeCreateTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(
            prefix="native-create-control-", dir=Path(__file__).parent)
        self.addCleanup(self.directory.cleanup)
        self.path = str(Path(self.directory.name) / "report.md")
        self.text = "# Synthetic report\n"
        Path(self.path).write_bytes(self.text.encode("utf-8"))
        self.args = {"path": self.path, "file_text": self.text}
        self.events = [
            {"type": "assistant.message", "data": {"toolRequests": [
                {"name": "create", "toolCallId": "write", "arguments": self.args}]}},
            {"type": "tool.execution_start", "data": {
                "toolCallId": "write", "toolName": "create", "arguments": self.args}},
            {"type": "tool.execution_complete", "data": {
                "toolCallId": "write", "success": True,
                "fileEdits": [{"path": self.path, "kind": "create"}]}},
        ]

    def test_native_create_requires_exact_host_creation_and_bytes(self):
        original = copy.deepcopy(self.events)
        repair.check_native_create(self.events, self.path)
        self.assertEqual(self.events, original)
        Path(self.path).write_bytes(b"changed")
        with self.assertRaises(ValueError):
            repair.check_native_create(self.events, self.path)

    def test_edit_other_path_failed_duplicate_and_unmatched_write_rejected(self):
        changes = (
            lambda e: e[2]["data"].update(fileEdits=[{"path": self.path, "kind": "edit"}]),
            lambda e: e[2]["data"].update(fileEdits=[]),
            lambda e: e[2]["data"].update(success=False),
            lambda e: e[2]["data"].update(toolCallId="unmatched"),
            lambda e: e[0]["data"]["toolRequests"].append(
                copy.deepcopy(e[0]["data"]["toolRequests"][0])),
            lambda e: e[0]["data"]["toolRequests"][0]["arguments"].update(path="elsewhere"),
            lambda e: e[0]["data"]["toolRequests"][0]["arguments"].update(overwrite=True),
        )
        for change in changes:
            events = copy.deepcopy(self.events)
            change(events)
            with self.subTest(change=change), self.assertRaises(ValueError):
                repair.check_native_create(events, self.path)

    def test_existing_add_file_path_is_unchanged_and_prepare_is_forbidden(self):
        repair.check_native_create([], self.path)
        with self.assertRaises(ValueError):
            repair.main(["prepare"])


if __name__ == "__main__":
    unittest.main()

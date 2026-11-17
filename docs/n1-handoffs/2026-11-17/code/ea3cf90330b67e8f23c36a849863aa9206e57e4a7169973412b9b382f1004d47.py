import copy
import unittest
from pathlib import Path

from common import WS, load_module

repair = load_module("b134_external_completion_repair",
                     Path(__file__).with_name("b134_revision_confirmation_v5.py"))


class ExternalMessageTests(unittest.TestCase):
    def setUp(self):
        self.session = repair.legacy.OWN["claude"]
        args = {"session_id": repair.legacy.COORDINATOR, "message": "CONFIRMED"}
        request = {
            "requestId": "11111111-2222-3333-4444-555555555555",
            "sessionId": self.session, "toolCallId": "completion",
            "toolName": "send_session_message", "arguments": args,
            "workingDirectory": str(WS.parent),
        }
        self.events = [
            {"type": "assistant.message", "data": {"toolRequests": [{
                "name": "send_session_message", "arguments": args,
                "toolCallId": "completion"}]}},
            {"type": "tool.execution_start", "data": {
                "toolName": "send_session_message", "arguments": args,
                "toolCallId": "completion"}},
            {"type": "external_tool.requested", "data": request},
            {"type": "external_tool.completed", "data": {"requestId": request["requestId"]}},
            {"type": "tool.execution_complete", "data": {
                "toolCallId": "completion", "success": True}},
        ]

    def test_exact_completion_transport_is_preserved(self):
        before = copy.deepcopy(self.events)
        repair.check_external_message(self.events, self.session)
        self.assertEqual(self.events, before)
        repair.check_external_message([], self.session)

    def test_unmatched_unknown_extra_reordered_and_cross_session_requests_fail(self):
        changes = (
            lambda e: e[2]["data"].update(sessionId="different"),
            lambda e: e[2]["data"].update(toolName="powershell"),
            lambda e: e[2]["data"].update(workingDirectory="different"),
            lambda e: e[2]["data"]["arguments"].update(message="Extra instructions"),
            lambda e: e[2]["data"]["arguments"].update(session_id="different"),
            lambda e: e[2]["data"].update(extra="unknown"),
            lambda e: e[3]["data"].update(requestId="different"),
            lambda e: e[4]["data"].update(success=False),
            lambda e: e.pop(3),
            lambda e: e.append(copy.deepcopy(e[2])),
            lambda e: e.insert(1, e.pop(3)),
        )
        for change in changes:
            events = copy.deepcopy(self.events)
            change(events)
            with self.subTest(change=change), self.assertRaises(ValueError):
                repair.check_external_message(events, self.session)


if __name__ == "__main__":
    unittest.main()

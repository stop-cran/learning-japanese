import copy
import json
import unittest

from adjudicate_b130_gpt003_control import INDEX, RAW, RAW_AUDIT_SHA, classify_control
from common import frozen


class PostCompletionControlTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        audit = json.loads(frozen(RAW / "audit.json", RAW_AUDIT_SHA))
        raw = frozen(RAW / "events.jsonl", audit["eventsSha256"])
        cls.events = [json.loads(line) for line in raw[audit["offset"]:].splitlines()]

    def test_exact_completed_review_keeps_every_raw_event(self):
        result = classify_control(self.events)
        self.assertEqual(self.events[INDEX]["type"], "user.message")
        self.assertEqual(result[INDEX]["data"], self.events[INDEX]["data"])
        self.assertEqual([i for i, pair in enumerate(zip(result, self.events)) if pair[0] != pair[1]], [INDEX])

    def test_changed_notice_is_not_classified(self):
        events = copy.deepcopy(self.events)
        events[INDEX]["data"]["content"] = "Additional review direction"
        with self.assertRaises(ValueError):
            classify_control(events)

    def test_new_post_completion_read_is_rejected(self):
        events = copy.deepcopy(self.events)
        event = next(e for e in events[INDEX:] if e["type"] == "tool.execution_start")
        event["data"]["toolName"] = "view"
        with self.assertRaises(ValueError):
            classify_control(events)

    def test_notice_before_successful_verdict_is_rejected(self):
        events = copy.deepcopy(self.events)
        start = next(e for e in events if e["type"] == "tool.execution_start"
                     and e["data"]["toolName"] == "send_session_message")
        completion = next(e for e in events if e["type"] == "tool.execution_complete"
                          and e["data"]["toolCallId"] == start["data"]["toolCallId"])
        completion["data"]["success"] = False
        with self.assertRaises(ValueError):
            classify_control(events)


if __name__ == "__main__":
    unittest.main()

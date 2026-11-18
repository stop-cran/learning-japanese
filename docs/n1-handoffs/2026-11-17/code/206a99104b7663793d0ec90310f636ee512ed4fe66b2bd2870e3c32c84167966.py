"""Controls for runtime-003 using the preserved actual authorized Claude delivery bytes."""
import copy
import json
import sys
import unittest
from pathlib import Path

from common import frozen, load_module

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RUNTIME = load_module("b134_authorized_runtime003_under_test", HERE / "b134_authorized_confirmation_v2.py")
ADMISSION = json.loads(frozen(ROOT / "authorized-claude-admit-001" / "admission.json"))
RAW = (ROOT / "authorized-claude-final-001" / "events.jsonl").read_bytes()
SUFFIX = RUNTIME.legacy.parse_events(RAW[ADMISSION["offset"]:])
USER = next(index for index, row in enumerate(SUFFIX) if row["type"] == "user.message")
START = next(index for index, row in enumerate(SUFFIX)
             if index > USER and row["type"] == "assistant.turn_start")


def rejects(test, function, *args):
    with test.assertRaises(Exception):
        function(*args)


class ActualDeliveryControls(unittest.TestCase):
    def test_selected_runtime_rejects_actual_shape(self):
        source = (ROOT / "authorization-runtime-002" / "b134_authorized_confirmation_v1.py").read_text("utf-8")
        self.assertIn('row["data"].get("agentMode") == "interactive"', source)
        self.assertNotIn("agentMode", SUFFIX[USER]["data"])

    def test_actual_message_and_turn_pass(self):
        self.assertTrue(RUNTIME.authorization_message(SUFFIX[USER], ADMISSION["kickoff"]))
        self.assertTrue(RUNTIME.delivered_turn_mode(SUFFIX))
        self.assertIs(RUNTIME.selected.authorization_message, RUNTIME.authorization_message)
        self.assertIs(RUNTIME.legacy.audit_snapshot, RUNTIME.audit_snapshot)
        self.assertEqual(Path(RUNTIME.legacy.__file__).resolve(), HERE / "b134_authorized_confirmation_v2.py")

    def test_message_mutations_rejected(self):
        row = copy.deepcopy(SUFFIX[USER])
        row["data"]["agentMode"] = "autopilot"
        rejects(self, RUNTIME.authorization_message, row, ADMISSION["kickoff"])
        row = copy.deepcopy(SUFFIX[USER])
        row["timestamp"] = RUNTIME.selected.authority()["timestamp"]
        rejects(self, RUNTIME.authorization_message, row, ADMISSION["kickoff"])
        rejects(self, RUNTIME.authorization_message, SUFFIX[USER], ADMISSION["kickoff"] + " ")
        row = copy.deepcopy(SUFFIX[USER])
        row["data"]["content"] = row["data"]["content"].replace("bounded", "unbounded", 1)
        rejects(self, RUNTIME.authorization_message, row, ADMISSION["kickoff"])

    def test_turn_mutations_rejected(self):
        for key, bad in (("agentMode", "autopilot"), ("agentMode", None), ("turnId", "1"),
                         ("interactionId", "00000000-0000-0000-0000-000000000000")):
            events = copy.deepcopy(SUFFIX)
            if bad is None:
                events[START]["data"].pop(key)
            else:
                events[START]["data"][key] = bad
            rejects(self, RUNTIME.delivered_turn_mode, events)
        rejects(self, RUNTIME.delivered_turn_mode, SUFFIX[:START])
        rejects(self, RUNTIME.delivered_turn_mode, SUFFIX + [copy.deepcopy(SUFFIX[USER])])
        events = copy.deepcopy(SUFFIX)
        events[USER]["data"].pop("turnId")
        rejects(self, RUNTIME.delivered_turn_mode, events)


if __name__ == "__main__":
    sys.exit(not unittest.main(argv=[sys.argv[0], "-v"], exit=False).result.wasSuccessful())

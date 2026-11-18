import importlib.util
import json
import shutil
import stat
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("filter_continuations", HERE / "filter-continuations-v2.py")
fc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fc)


def nudge(**overrides):
    data = {"content": "", "source": "autopilot", "isAutopilotContinuation": True,
            "transformedContent": "<current_datetime>2026-11-13T21:09:52.933+01:00</current_datetime>\n\n"
                                  + fc.BOILERPLATE}
    data.update(overrides)
    return {"type": "user.message", "data": data, "id": "n"}


def reply(*tools):
    return {"type": "assistant.message",
            "data": {"content": "waiting", "toolRequests": [{"name": name} for name in tools]}}


KICKOFF = {"type": "user.message", "data": {"content": "kick", "source": "agent-x"}}


class FilterTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        for path in self.tmp.rglob("*"):
            path.chmod(stat.S_IWRITE | stat.S_IREAD)
        shutil.rmtree(self.tmp)

    def make(self, events, flagged, **audit):
        run = self.tmp / "run" / "audit-1"
        run.mkdir(parents=True)
        record = ("\n".join(json.dumps(event) for event in events) + "\n").encode("utf-8")
        (run / "events.jsonl").write_bytes(record)
        body = {"status": "HOLD", "breaches": [], "eventsSha256": fc.digest(record),
                "unexpectedUserMessages": len(flagged),
                "notes": [f"Unexpected user message at event {i}; adjudicate before acceptance" for i in flagged]}
        body.update(audit)
        (run / "audit.json").write_text(json.dumps(body))
        for path in run.iterdir():
            path.chmod(stat.S_IREAD)
        return run / "audit.json"

    def test_exact_nudges_removed_and_rest_byte_preserved(self):
        events = [KICKOFF, reply("view"), nudge(), reply(), nudge(), reply("task_complete")]
        root, result = fc.adjudicate(self.make(events, [2, 4]), self.tmp)
        kept = (root / "events-filtered.jsonl").read_bytes().decode("utf-8").split("\n")
        self.assertEqual([json.loads(line) for line in kept if line], [KICKOFF, reply("view"), reply(), reply("task_complete")])
        self.assertEqual([item["event"] for item in result["removed"]], [2, 4])

    def test_rejections(self):
        cases = {
            "content": ([KICKOFF, nudge(content="hint")], [1], {}),
            "source": ([KICKOFF, nudge(source="user")], [1], {}),
            "flag": ([KICKOFF, nudge(isAutopilotContinuation=False)], [1], {}),
            "text": ([KICKOFF, nudge(transformedContent="<current_datetime>1</current_datetime>\n\nGo on")], [1], {}),
            "tool": ([KICKOFF, nudge(), reply("view")], [1], {}),
            "breach": ([KICKOFF, nudge()], [1], {"breaches": ["x"]}),
            "hash": ([KICKOFF, nudge()], [1], {"eventsSha256": "0"}),
            "count": ([KICKOFF, nudge()], [1], {"unexpectedUserMessages": 2}),
        }
        for name, (events, flagged, audit) in cases.items():
            with self.subTest(name):
                with self.assertRaises(fc.Rejected):
                    fc.adjudicate(self.make(events, flagged, **audit), self.tmp)
                shutil.rmtree(self.tmp / "run", onerror=lambda f, p, e: (Path(p).chmod(stat.S_IWRITE), f(p)))

    def test_only_exact_crlf_note_is_tolerated(self):
        events = [KICKOFF, nudge(), reply()]
        notes = ["Unexpected user message at event 1; adjudicate before acceptance", next(iter(fc.ALLOWED_NOTES))]
        root, result = fc.adjudicate(self.make(events, [1], notes=notes), self.tmp)
        self.assertEqual(result["retainedNotes"], [next(iter(fc.ALLOWED_NOTES))])
        shutil.rmtree(self.tmp / "run", onerror=lambda f, p, e: (Path(p).chmod(stat.S_IWRITE), f(p)))
        with self.assertRaises(fc.Rejected):
            fc.adjudicate(self.make(events, [1], notes=notes[:1] + ["Report on disk differs"]), self.tmp.joinpath("x"))

    def test_tool_after_next_real_user_message_is_left_to_frozen_auditor(self):
        events = [KICKOFF, nudge(), reply(), {"type": "user.message", "data": {"content": "phase2", "source": "agent-x"}},
                  reply("view")]
        fc.adjudicate(self.make(events, [1]), self.tmp)


if __name__ == "__main__":
    unittest.main()

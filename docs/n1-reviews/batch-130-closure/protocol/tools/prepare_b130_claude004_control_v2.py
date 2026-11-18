"""Finish the prior derivation, normalizing test-source CRLF before its structural insertion."""
import json

from b130_context_confirmation import ROOT, binding
from common import TOOLS, freeze_json, frozen, require, write_frozen
from prepare_b130_followup_engine import replace_once
from adjudicate_b130_gpt003_control import event_sha


def main():
    raw_path = ROOT / "confirm" / "N1-B130-CLAUDE-CONFIRM-004" / "audit-20261116T135840716486"
    raw_audit = json.loads(frozen(raw_path / "audit.json",
                                 "273bfcc4aa5c10b57fa90dbfa2efc8be1a37530ce244ef03346952cbb53dea99"))
    events = [json.loads(line) for line in
              frozen(raw_path / "events.jsonl", raw_audit["eventsSha256"])[raw_audit["offset"]:].splitlines()]
    require(len(events) == 268 and events[257]["type"] == "tool.execution_start"
            and events[257]["data"]["toolName"] == "task_complete"
            and events[257]["data"]["arguments"]["summary"].startswith("CONFIRMED:"),
            "Observed permitted completion differs")
    task_sha = event_sha(events[257])
    source = TOOLS / "adjudicate_b130_gpt003_control.py"
    text = frozen(source, "77c62423589d302b45f32150f4cb35696067d8125f822bc9731a8eb7549706c9").decode()
    for before, after in (
        ("GPT003", "Claude004"),
        ("N1-B130-GPT-CONFIRM-003", "N1-B130-CLAUDE-CONFIRM-004"),
        ("audit-20261116T135432101545", "audit-20261116T135840716486"),
        ("7eef215b321520bec0bd6b973d88356621c0c454a7fef9aa24f9f81984b81348",
         "273bfcc4aa5c10b57fa90dbfa2efc8be1a37530ce244ef03346952cbb53dea99"),
        ("f67673fab30a9d356b0d4f7298f20338f63a0d9a292ffc22f91a3ed1aa3bf823",
         "3f1214fcf0b7a0e35bc51596253aecac72a2e2dd8a3646a7101c9815874b5bee"),
        ("INDEX = 403", "INDEX = 253"),
        ("len(events) == 418", "len(events) == 268"),
        ('later[0][1]["arguments"] == {"summary": "CONFIRMED"}',
         f'event_sha(events[later[0][0]]) == "{task_sha}"'),
    ):
        text = replace_once(text, before, after)
    name = "adjudicate_b130_claude004_control.py"
    compile(text, name, "exec")
    require(frozen(TOOLS / name) == text.encode(), "Earlier generated classifier changed")
    output = binding(TOOLS / name)
    test_source = TOOLS / "test_b130_gpt003_control.py"
    tests = frozen(test_source).decode().replace("\r\n", "\n")
    tests = replace_once(tests, "from adjudicate_b130_gpt003_control import",
                         "from adjudicate_b130_claude004_control import")
    tests = replace_once(tests, '\n\nif __name__ == "__main__":', '''

    def test_changed_completion_summary_is_rejected(self):
        events = copy.deepcopy(self.events)
        event = next(e for e in events[INDEX:] if e["type"] == "tool.execution_start")
        event["data"]["arguments"]["summary"] += "\\nNew unreviewed claim."
        with self.assertRaises(ValueError):
            classify_control(events)


if __name__ == "__main__":''')
    test_name = "test_b130_claude004_control.py"
    compile(tests, test_name, "exec")
    test_output = write_frozen(TOOLS / test_name, tests.encode())
    print(json.dumps(freeze_json(ROOT / "claude004-control-tooling-001.json", {
        "source": binding(source), "output": output, "testSource": binding(test_source),
        "testOutput": test_output, "rawAudit": binding(raw_path / "audit.json"),
        "exactCompletionEventSha256": task_sha,
        "scope": "Same exact-event classifier, separately bound to the inspected Claude004 tail. "
                 "Its single permitted task_complete uses a longer summary consistent with the "
                 "unchanged report; the entire completion event is pinned, not allowed by prefix alone. "
                 "No report rewrite, new source read or second verdict send occurred. First producer "
                 "stopped after classifier creation because its test insertion expected LF, not CRLF. "
                 "This retry verifies that classifier byte-for-byte and normalizes only the copied tests.",
        "earlierProducer": binding(TOOLS / "prepare_b130_claude004_control.py"),
        "producer": binding(__file__),
    })))


if __name__ == "__main__":
    main()

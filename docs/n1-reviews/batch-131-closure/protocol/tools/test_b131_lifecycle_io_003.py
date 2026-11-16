"""Exercise the actual bounded lifecycle adapter on synthetic context data only."""
import json
import tempfile
import unittest
from pathlib import Path

from b131_neutral_common_001 import HERE
from b131_lifecycle_process_002 import python


class LifecycleIoTests(unittest.TestCase):
    def test_exact_json_stdout_for_success_and_expected_refusal(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "synthetic-context-events.jsonl"
            events = [{"type": "session.start", "data": {"contextTier": "long_context"}},
                      {"type": "session.usage_record", "data": {"usage": {"maxPromptTokens": 952000}}}]
            for compacted in (False, True):
                if compacted:
                    events.append({"type": "session.compaction_start", "data": {}})
                path.write_text("".join(json.dumps(e) + "\n" for e in events), encoding="utf-8")
                code, stdout, stderr = python(HERE / "check-run-context.py", path)
                value = json.loads(stdout)
                self.assertEqual(value["status"], "FAIL" if compacted else "PASS")
                self.assertEqual(code, 1 if compacted else 0)
                self.assertNotIn('"runnerSha256"', stdout)

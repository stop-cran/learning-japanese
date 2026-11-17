import copy
import json
import unittest

from b134_token_meter import COORDINATOR, PROFILES, audit
from common import json_bytes, sha


def event_bytes(events):
    return b"".join((json.dumps(row, ensure_ascii=False) + "\n").encode() for row in events)


def fixture(full=False):
    data = {"prompt": b"Measure only.\n", "kickoff": b"Read prompt", "one": b"First source.\n",
            "two": b"Last source.\n"}
    ref = lambda name: {"path": name, "sha256": sha(data[name])}
    spec = {
        "purpose": "token-measurement-only", "reviewAccepted": False,
        "family": "claude", "session": "meter-session", "prompt": ref("prompt"),
        "kickoff": ref("kickoff"), "segments": [ref("one"), ref("two")],
        "core": {"path": "manifest", "sha256": "a" * 64},
    }
    events = []

    def event(kind, value):
        events.append({"type": kind, "data": value})

    def user(text):
        event("user.message", {"content": text, "source": "agent-" + COORDINATOR})

    def usage(tokens):
        event("session.usage_record", {"usage": {
            "inputTokens": tokens, "maxPromptTokens": PROFILES["claude"]["maxPromptTokens"],
            "responseModel": "claude-fixture",
        }})

    def view(path):
        cid = "view-" + path
        args = {"path": path, "forceReadLargeFiles": True}
        event("assistant.message", {"apiCallId": "api-" + path, "toolRequests": [
            {"name": "view", "arguments": args, "toolCallId": cid}]})
        event("tool.execution_start", {"toolName": "view", "arguments": args, "toolCallId": cid})
        event("tool.execution_complete", {"toolCallId": cid, "success": True,
                                         "result": {"content": data[path].decode()}})

    event("session.start", {"sessionId": spec["session"], "selectedModel": "claude-opus-5.5",
                            "contextTier": "long_context"})
    user("Read prompt")
    usage(50000)
    view("prompt")
    usage(51000)
    event("assistant.turn_end", {})
    bootstrap_raw = event_bytes(events)
    bootstrap = audit(events, bootstrap_raw, spec, lambda path, digest: data[path])
    if full:
        user("one")
        view("one")
        usage(61000)
        view("two")
        usage(71000)
        event("assistant.turn_end", {})
    raw = event_bytes(events)
    return events, raw, spec, data, bootstrap


class TokenMeterControls(unittest.TestCase):
    def test_exact_bootstrap_and_full_read_measure_tokens_without_a_review(self):
        events, raw, spec, data, bootstrap = fixture(True)
        result = audit(events, raw, spec, lambda path, digest: data[path], bootstrap)
        self.assertEqual(result["coreGrowthTokens"], 20000)
        self.assertEqual(result["coreGrowthWithTenPercentReserve"], 22000)
        self.assertFalse(result["reviewAccepted"])
        self.assertNotIn("verdict", result)

    def test_runtime_or_source_breaches_invalidate_measurement(self):
        mutations = (
            lambda e, s: e[0]["data"].update(contextTier=None),
            lambda e, s: e[0]["data"].update(selectedModel="gpt-6.1-sol"),
            lambda e, s: e.append({"type": "session.compaction_start", "data": {}}),
            lambda e, s: e[2]["data"]["usage"].update(maxPromptTokens=200000),
            lambda e, s: e[5]["data"]["result"].update(content="truncated"),
            lambda e, s: s.update(reviewAccepted=True),
            lambda e, s: s["segments"].reverse(),
        )
        for index, mutate in enumerate(mutations):
            events, raw, spec, data, bootstrap = fixture(True)
            mutate(events, spec)
            raw = event_bytes(events)
            with self.subTest(index=index), self.assertRaises((ValueError, KeyError)):
                audit(events, raw, spec, lambda path, digest: data[path], bootstrap)

    def test_bootstrap_or_final_usage_cannot_be_substituted(self):
        events, raw, spec, data, bootstrap = fixture(True)
        for field, value in (("session", "another-session"), ("eventsSha256", "0" * 64),
                             ("coreManifestSha256", "b" * 64)):
            changed = copy.deepcopy(bootstrap)
            changed[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                audit(events, raw, spec, lambda path, digest: data[path], changed)
        final_usage = next(i for i in range(len(events) - 1, -1, -1)
                           if events[i]["type"] == "session.usage_record")
        events.pop(final_usage)
        with self.assertRaises(ValueError):
            audit(events, event_bytes(events), spec, lambda path, digest: data[path], bootstrap)


if __name__ == "__main__":
    unittest.main()

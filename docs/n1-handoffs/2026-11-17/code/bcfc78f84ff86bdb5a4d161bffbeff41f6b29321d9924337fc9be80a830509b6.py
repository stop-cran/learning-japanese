import copy
import json
import unittest

from b134_token_meter import CAPS, COORDINATOR, PROFILES, audit, measured_forecasts, verify_core
from common import sha


def event_bytes(events):
    return b"".join((json.dumps(row, ensure_ascii=False) + "\n").encode() for row in events)


def fixture(full=False, family="claude"):
    data = {"prompt": b"Measure only.\n", "kickoff": b"Read prompt", "one": b"First source.\n",
            "two": b"Last source.\n"}
    ref = lambda name: {"path": name, "sha256": sha(data[name])}
    spec = {
        "purpose": "token-measurement-only", "reviewAccepted": False,
        "family": family, "session": family + "-meter-session", "prompt": ref("prompt"),
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
            "inputTokens": tokens, "maxPromptTokens": PROFILES[family]["maxPromptTokens"],
            "responseModel": family + "-fixture",
        }})

    def view(path):
        cid = "view-" + path
        args = {"path": path, "forceReadLargeFiles": True}
        event("assistant.message", {"apiCallId": "api-" + path, "toolRequests": [
            {"name": "view", "arguments": args, "toolCallId": cid}]})
        event("tool.execution_start", {"toolName": "view", "arguments": args, "toolCallId": cid})
        event("tool.execution_complete", {"toolCallId": cid, "success": True,
                                         "result": {"content": data[path].decode()}})

    event("session.start", {"sessionId": spec["session"], "selectedModel": PROFILES[family]["selectedModel"],
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
    def test_chain_must_reconstruct_every_complete_source(self):
        data = {"source": b"one\ntwo\n"}
        segment = b"envelope\none\ntwo\nend\n"
        core = {
            "sources": [{"source": "source", "sha256": sha(data["source"]),
                         "selectedSha256": sha(data["source"]), "sourceLines": 2, "selectedLines": 2}],
            "segments": [{"index": 1, "path": "segment", "sha256": sha(segment), "bytes": len(segment),
                          "parts": [{"source": "source", "sha256": sha(data["source"]),
                                     "a": 1, "b": 2, "segmentStart": 2, "segmentEnd": 3}]}],
        }
        self.assertEqual(verify_core(core, data, lambda path, digest: segment), len(segment))
        mutations = (
            lambda c: c["sources"][0].update(selectedLines=1),
            lambda c: c["segments"][0]["parts"][0].update(a=2),
            lambda c: c["segments"][0]["parts"][0].update(b=1, segmentEnd=2),
            lambda c: c["segments"][0]["parts"][0].update(segmentStart=1),
        )
        for index, mutate in enumerate(mutations):
            changed = copy.deepcopy(core)
            mutate(changed)
            with self.subTest(index=index), self.assertRaises(ValueError):
                verify_core(changed, data, lambda path, digest: segment)

    def test_exact_bootstrap_and_full_read_measure_tokens_without_a_review(self):
        for family in PROFILES:
            events, raw, spec, data, bootstrap = fixture(True, family)
            result = audit(events, raw, spec, lambda path, digest: data[path], bootstrap)
            with self.subTest(family=family):
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
            lambda e, s: e[-2]["data"]["usage"].update(inputTokens=700001),
            lambda e, s: e[3]["data"].update(content="A teaching finding"),
            lambda e, s: e[3]["data"].update(apiCallId=None),
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

    def test_capacity_keeps_all_tiers_reserves_and_exact_source_binding(self):
        meters = []
        for family in PROFILES:
            events, raw, spec, data, bootstrap = fixture(True, family)
            meters.append(audit(events, raw, spec, lambda path, digest: data[path], bootstrap))
        trials = [{"caps": {"D": d, "E": e}, "articleForecastIncludingEnvelopes": 200000}
                  for d, e in CAPS]
        result = measured_forecasts(meters, "a" * 64, trials)
        self.assertEqual(result["chosenCaps"], {"D": 25, "E": 10})
        self.assertEqual(result["trials"][0]["startupForecast"], 364000)
        trials[0]["articleForecastIncludingEnvelopes"] = 536000
        self.assertEqual(measured_forecasts(meters, "a" * 64, trials)["trials"][0]["outcome"],
                         "PASS_ESTIMATE")
        trials[0]["articleForecastIncludingEnvelopes"] += 1
        self.assertEqual(measured_forecasts(meters, "a" * 64, trials)["trials"][0]["outcome"],
                         "HOLD_ESTIMATE")
        with self.assertRaises(ValueError):
            measured_forecasts(meters, "b" * 64, trials)
        with self.assertRaises(ValueError):
            measured_forecasts(meters[:1], "a" * 64, trials)
        with self.assertRaises(ValueError):
            measured_forecasts(meters, "a" * 64, trials[-1:])


if __name__ == "__main__":
    unittest.main()

import copy
import datetime
import json
import math
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import b134_token_meter as meter
from b134_token_meter import CAPS, COORDINATOR, PROFILES, audit, measured_forecasts, verify_core
from common import json_bytes, sha


def event_bytes(events):
    return b"".join((json.dumps(row, ensure_ascii=False) + "\n").encode() for row in events)


def fixture(full=False, family="claude", completion="text"):
    data = {"prompt": b"Measure only.\n", "kickoff": b"Read prompt", "one": b"First source.\n",
            "two": b"Last source.\n"}
    ref = lambda name: {"path": name, "sha256": sha(data[name])}
    spec = {
        "purpose": "token-measurement-only", "reviewAccepted": False,
        "family": family, "session": family + "-meter-session", "prompt": ref("prompt"),
        "kickoff": ref("kickoff"), "segments": [ref("one"), ref("two")],
        "core": {"path": "manifest", "sha256": "a" * 64},
    }
    if completion == "text":
        spec["completion"] = "text"
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
        if completion == "text":
            event("assistant.message", {"content": "MEASUREMENT COMPLETE"})
        else:
            args = {"pattern": "task_complete"}
            event("assistant.message", {"apiCallId": "api-search", "content": "", "toolRequests": [
                {"name": "tool_search_tool", "arguments": args, "toolCallId": "search"}]})
            event("tool.execution_start", {"toolName": "tool_search_tool", "arguments": args,
                                           "toolCallId": "search"})
            event("tool.execution_complete", {"toolCallId": "search", "success": True,
                                             "result": {"content": meter.UNAVAILABLE_COMPLETION}})
            event("assistant.turn_end", {})
            usage(71500)
            event("assistant.message", {"content": "task_complete is unavailable.\n\nMEASUREMENT COMPLETE."})
        event("assistant.turn_end", {})
    raw = event_bytes(events)
    return events, raw, spec, data, bootstrap


class TokenMeterControls(unittest.TestCase):
    def test_aliases_keep_complete_card_title_index_and_full_record_classes(self):
        inherited = Mock(return_value=("docs", .354 * 1.10))
        for name, expected in (
            ("parent/kanji/card.md", ("cards", .502 * 1.10)),
            ("evidence/baseline-title-index.txt", ("titleidx", .531 * 1.10)),
            ("evidence/kanjidic2-complete-union.xml", ("full-kd", 1.0)),
        ):
            with self.subTest(name=name):
                self.assertEqual(meter.measurement_source_class(name, inherited), expected)
        inherited.assert_not_called()
        meter.measurement_source_class("reconciliation/checks/lint.log", inherited)
        inherited.assert_called_once_with("checks/lint.log")

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
            lambda e, s: next(row for row in reversed(e) if row["type"] == "session.usage_record"
                              )["data"]["usage"].update(inputTokens=700001),
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

    def test_text_completion_rejects_tool_completion_search_and_premature_signal(self):
        def final_text(events):
            return next(i for i in range(len(events) - 1, -1, -1)
                        if events[i]["type"] == "assistant.message")

        def tool_complete(events):
            events[final_text(events)] = {"type": "assistant.message", "data": {
                "apiCallId": "api-complete", "toolRequests": [{
                    "name": "task_complete", "arguments": {"summary": "MEASUREMENT COMPLETE"},
                    "toolCallId": "complete"}]}}

        def search_first(events):
            events.insert(final_text(events), {"type": "assistant.message", "data": {
                "apiCallId": "api-search", "toolRequests": [{
                    "name": "tool_search_tool", "arguments": {"pattern": "task_complete"},
                    "toolCallId": "search"}]}})

        mutations = (
            tool_complete, search_first,
            lambda e: e[final_text(e)]["data"].update(content="MEASUREMENT COMPLETE. All read."),
            lambda e: e.pop(final_text(e)),
        )
        for index, mutate in enumerate(mutations):
            events, raw, spec, data, bootstrap = fixture(True)
            mutate(events)
            with self.subTest(index=index), self.assertRaises(ValueError):
                audit(events, event_bytes(events), spec, lambda path, digest: data[path], bootstrap)
        events, raw, spec, data, _ = fixture()
        events.insert(len(events) - 1, {"type": "assistant.message",
                                        "data": {"content": "MEASUREMENT COMPLETE"}})
        with self.assertRaises(ValueError):
            audit(events, event_bytes(events), spec, lambda path, digest: data[path])

    def test_legacy_unavailable_completion_is_disclosed_conservative_and_bounded(self):
        events, raw, spec, data, bootstrap = fixture(True, completion="legacy")
        result = audit(events, raw, spec, lambda path, digest: data[path], bootstrap)
        self.assertEqual((result["coreGrowthTokens"], result["postFinalSourceInputTokens"]), (20500, 71000))
        self.assertEqual(result["completionDeviation"]["unavailableToolSearch"]["result"],
                         meter.UNAVAILABLE_COMPLETION)
        self.assertEqual(result["completionDeviation"]["finalMessage"],
                         "task_complete is unavailable.\n\nMEASUREMENT COMPLETE.")
        g_events, g_raw, g_spec, g_data, g_bootstrap = fixture(True, "gpt")
        gpt = audit(g_events, g_raw, g_spec, lambda path, digest: g_data[path], g_bootstrap)
        forecast = measured_forecasts([result, gpt], "a" * 64, [
            {"caps": {"D": d, "E": e}, "articleForecastIncludingEnvelopes": 200000} for d, e in CAPS])
        self.assertEqual(forecast["trials"][0]["measuredCoreBoundIncludingDrift"],
                         math.ceil(20500 * 1.10) + 12000)
        self.assertEqual([row["family"] for row in forecast["completionDeviations"]], ["claude"])

        def find(events, kind, key, value):
            return next(row for row in events if row["type"] == kind and row["data"].get(key) == value)

        def second_search(events):
            last = next(i for i in range(len(events) - 1, -1, -1) if events[i]["type"] == "assistant.message")
            events.insert(last, {"type": "assistant.message", "data": {
                "apiCallId": "api-search-2", "toolRequests": [{
                    "name": "tool_search_tool", "arguments": {"pattern": "task_complete"},
                    "toolCallId": "search-2"}]}})

        mutations = (
            lambda e, s: find(e, "assistant.message", "apiCallId", "api-search")["data"]["toolRequests"][0]
            .update(arguments={"pattern": "shell"}),
            lambda e, s: find(e, "tool.execution_complete", "toolCallId", "search")["data"]["result"]
            .update(content="Found task_complete"),
            lambda e, s: e[-2]["data"].update(content="task_complete is unavailable."),
            lambda e, s: s.update(completion="text"),
            second_search,
        )
        for index, mutate in enumerate(mutations):
            events, raw, spec, data, bootstrap = fixture(True, completion="legacy")
            if index == 4:
                mutate(events)
            else:
                mutate(events, spec)
            with self.subTest(index=index), self.assertRaises(ValueError):
                audit(events, event_bytes(events), spec, lambda path, digest: data[path], bootstrap)

    def test_only_the_bound_legacy_preparation_omits_text_completion_and_none_admit(self):
        current = sha(Path(meter.__file__).read_bytes())

        def build(producer, completion):
            plain = {"path": "x", "sha256": "0" * 64}
            run = {"prompt": plain, "kickoff": plain, "core": plain, "segments": []}
            if completion:
                run["completion"] = completion
            ref = {"path": "x", "sha256": producer}
            return json_bytes({
                "status": "PREPARED_MEASUREMENT_ONLY_NOT_REVIEW_ADMISSION", "producerSha256": producer,
                "producer": ref, "controls": ref, "packetInventory": ref, "sourceForecast": None,
                "runs": {"claude": run}, "startupGate": 700000, "coreForecastTokens": 1,
                "measurementOnlyStartupBound": 110001})

        def load(raw, legacy=None):
            table = {sha(raw): legacy} if legacy else {}
            with patch.object(meter, "frozen", side_effect=lambda p, d=None: raw if p == "prep" else b"x"), \
                    patch.object(meter, "LEGACY_PREPARATIONS", table):
                return meter.load_preparation("prep", "claude")[1]

        self.assertEqual(load(build(current, "text"))["completion"], "text")
        self.assertNotIn("completion", load(build("f" * 64, None), "f" * 64))
        for raw, legacy in ((build(current, None), None), (build("f" * 64, "text"), "f" * 64),
                            (build("f" * 64, None), None)):
            with self.subTest(legacy=legacy), self.assertRaises(ValueError):
                load(raw, legacy)
        guard = Mock()
        guard.finish.return_value = {"breach": None}
        with patch.object(meter, "start_guard", return_value=(guard, Mock())), \
                patch.object(meter, "load_preparation", return_value=({}, {"launch": {}}, b"")), \
                patch.object(meter, "frozen") as read, self.assertRaises(ValueError):
            meter.admit(Path("prep"), "claude", Path("request"), meter.ROOT / "never-written-legacy-admission")
        read.assert_not_called()

    def test_label_distinguishes_session_name_and_rejects_unsafe_labels(self):
        self.assertEqual(meter.session_name("claude"), "B134 CLAUDE token measurement")
        self.assertEqual(meter.session_name("gpt", "011"), "B134 GPT token measurement 011")
        for label in ("", "a b", "../x", "x" * 25, "011\n"):
            with self.subTest(label=label), self.assertRaises(ValueError):
                meter.session_name("claude", label)

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

    def test_corrected_forecast_must_describe_exact_core_and_inherited_coefficients(self):
        source = b"one\ntwo\n"
        core = {"sources": [{"source": "checks/log.log"}], "segments": [{"bytes": 28}]}
        coefficient = .522 * 1.10
        cost = math.ceil(len(source) * coefficient)
        forecast = {
            "sourceClassification": {"sources": [{"source": "checks/log.log", "class": "checks",
                "coefficient": coefficient, "bytes": len(source), "tokens": cost}]},
            "packetManifestSha256": "a" * 64, "startupGate": 700000,
            "bootstrapTokens": 80000, "reportTokens": 30000, "optionalUnitAllowance": 20000,
            "finalCoreSources": 1, "finalCoreSegments": 1, "finalPayloadBytes": len(source),
            "finalChainBytes": 28, "finalEnvelopeBytes": 28 - len(source),
            "coreTokens": cost + math.ceil((28 - len(source)) * .574),
        }
        sources = {"checks/log.log": source}
        self.assertEqual(meter.checked_source_forecast(forecast, core, sources, "a" * 64),
                         forecast["coreTokens"])
        mutations = (
            lambda f: f.update(packetManifestSha256="b" * 64),
            lambda f: f.update(finalCoreSegments=2),
            lambda f: f.update(coreTokens=f["coreTokens"] - 1),
            lambda f: f.update(optionalUnitAllowance=0),
            lambda f: f["sourceClassification"]["sources"][0].update(coefficient=.3894),
            lambda f: f["sourceClassification"]["sources"].clear(),
        )
        for index, mutate in enumerate(mutations):
            changed = copy.deepcopy(forecast)
            mutate(changed)
            with self.subTest(index=index), self.assertRaises(ValueError):
                meter.checked_source_forecast(changed, core, sources, "a" * 64)

    def test_record_command_binds_real_shape_bootstrap_and_final_snapshots(self):
        events, _, spec, data, _ = fixture(True)
        session = "00000000-0000-4000-8000-000000000134"
        spec["session"] = events[0]["data"]["sessionId"] = session
        moment = datetime.datetime.now(datetime.timezone.utc).isoformat()
        for event in events:
            event["timestamp"] = moment
        first_end = next(i for i, event in enumerate(events) if event["type"] == "assistant.turn_end")
        initial_raw, full_raw = event_bytes(events[:first_end + 1]), event_bytes(events)
        data.update(preparation=b"preparation", status=b"status", roster=b"[]", request=b"request")
        refs = {name: {"path": name, "sha256": sha(data[name])}
                for name in ("preparation", "status", "roster", "request")}
        admission = {
            "purpose": "token-measurement-only", "reviewAccepted": False, "admitted": True,
            "family": "claude", "createdAt": moment, **refs,
        }
        data["admission"] = json_bytes(admission)
        guard = Mock()
        guard.finish.return_value = {"breach": None}
        emitted = {}

        def fake_read(path, expected=None):
            raw = data[str(path)]
            if expected is not None:
                self.assertEqual(sha(raw), expected)
            return raw

        def fake_write(path, raw):
            emitted[str(path)] = raw
            data[str(path)] = raw
            return {"path": str(path), "sha256": sha(raw), "bytes": len(raw)}

        output = meter.ROOT / "token-meter-synthetic-command-never-written"
        with patch.object(meter, "frozen", side_effect=fake_read), \
                patch.object(meter, "write_frozen", side_effect=fake_write), \
                patch.object(meter, "freeze_json", side_effect=lambda p, v: fake_write(p, json_bytes(v))), \
                patch.object(meter, "load_preparation", return_value=({}, spec, b"preparation")), \
                patch.object(meter, "start_guard", return_value=(guard, Mock())), \
                patch.object(Path, "read_bytes", return_value=initial_raw), \
                patch("builtins.print"):
            meter.record("bootstrap", Path("admission"), session, output)
            bootstrap = json.loads(emitted[str(output / "audit.json")])
            self.assertEqual(bootstrap["eventsSha256"], sha(initial_raw))
            with patch.object(Path, "read_bytes", return_value=full_raw):
                meter.record("final", Path("admission"), session, output.with_name(output.name + "-final"),
                             output / "audit.json")
            final = json.loads(emitted[str(output.with_name(output.name + "-final") / "audit.json")])
            self.assertEqual(final["coreGrowthTokens"], 20000)
            self.assertEqual(final["admission"]["sha256"], sha(data["admission"]))
            self.assertFalse(final["reviewAccepted"])


if __name__ == "__main__":
    unittest.main()

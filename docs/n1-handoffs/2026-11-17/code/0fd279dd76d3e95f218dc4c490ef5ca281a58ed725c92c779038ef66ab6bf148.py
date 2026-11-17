"""Focused bounded-unit access, independent forecasts and complete two-phase audit controls."""
import copy
import importlib.util
import json
import math
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

WS = Path(r"C:\Users\stop-\n1-kanji-workspace")
ROOT = WS / "scratch-134" / "review"
HERE = ROOT / "neutral-preparation-001" / "projected-successor-001"
PROTOCOL = HERE / "protocol-001"
sys.path.insert(0, str(PROTOCOL))
sys.path.insert(0, str(HERE / "tools"))
from b134_common import PACKET, frozen, sha, freeze_json, write_frozen, require, start_guard
from b134_capacity import load_forecast, phase2_gate, startup_bound
from b134_runtime import extension_sources, verify_chain, expected_message
from review_chain_with_optional import OPTIONAL_UNITS, build_chain, validate_selection
from capacity004_units import extension_upper, chain_cost
import b134_common
import b134_runtime

CASE = HERE / "optional-validation-001"


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, PROTOCOL / filename)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


FIXTURE = module("optional004_fixture", "test-synthetic-protocol-b134-001.py")
AUDIT, PREPARE, STRUCTURE = FIXTURE.AUDIT, FIXTURE.PREPARE, FIXTURE.STRUCTURE


def jsonl(events):
    return b"".join((json.dumps(e, ensure_ascii=False) + "\n").encode() for e in events)


class Controls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        require(not CASE.exists(), "Preserve optional validation")
        cls.sums = json.loads(frozen(PACKET / "SHA256SUMS.json"))
        cls.reference = json.loads(frozen(PACKET / "eligibility-reference.json"))
        cls.forecast = load_forecast()
        cls.core = json.loads(frozen(HERE / "core-chain-001.json"))
        cls.preflight = json.loads(frozen(HERE / "audit-configs-001" / "preflight.json"))
        cls.config = json.loads(frozen(cls.preflight["runs"]["gpt"]["auditConfig"]["path"]))
        cls.results = {}

    def test_01_all_individual_units_are_whole_readable_and_fit(self):
        costs = []
        guard, _ = start_guard("B134 all individual complete optional units")
        try:
            for index, (unit, name) in enumerate(OPTIONAL_UNITS.items(), 1):
                reply = f"D: none\nE: none\nO1 {unit} - synthetic access control"
                selection = validate_selection(reply, self.reference)
                self.assertTrue(selection["valid"], selection["errors"])
                sources, missing, matches = extension_sources(reply, self.sums)
                self.assertEqual(len(sources), 1)
                self.assertEqual(sources[0][1], frozen(PACKET / name, self.sums[name]))
                self.assertEqual((missing, matches), ([], {}))
                upper = extension_upper(sources)
                self.assertLessEqual(upper["tokens"], self.forecast["optionalUnitAllowance"])
                case = CASE / "individual-units" / str(index)
                chain = build_chain(sources, case / "chain", case / "manifest.json", guard, "synthetic optional unit")
                coverage = verify_chain(chain, sources)
                self.assertLessEqual(coverage["tokens"], upper["tokens"])
                self.assertLessEqual(coverage["bytes"], upper["payloadBytes"] + upper["envelopeBytesUpper"])
                costs.append({"unit": unit, "source": name, "upper": upper, "actualChain": coverage})
            self.assertEqual(len(costs), 62)
            self.assertEqual(max(r["upper"]["tokens"] for r in costs),
                             self.forecast["largestOptionalUnitTokens"])
            self.results["individualUnits"] = costs
        finally:
            self.assertFalse(guard.finish()["breach"])

    def test_02_invalid_whole_file_duplicate_unknown_and_numbering_reject(self):
        for optional in (
            "O1 evidence/kanjidic2-records.xml - prohibited whole file",
            "O1 K:龘 - absent literal",
            "O1 evidence/source-metadata.json - not a unit",
            "O2 K:紫 - wrong numbering",
            "O1 K:紫 - one\nO2 K:紫 - repeated",
            "O: none\nO1 K:紫 - conflicting",
            "O1 K:紫",
        ):
            with self.subTest(optional=optional):
                result = validate_selection("D: none\nE: none\n" + optional, self.reference)
                self.assertFalse(result["valid"])
        self.assertFalse(validate_selection("D: none\nE: none", self.reference)["valid"])

    def test_03_excess_requests_hold_without_partial_output(self):
        reply = ("D: none\nE: none\nO1 evidence/font-cmap.json - synthetic\n"
                 "O2 evidence/xml-presentation.json - synthetic\n"
                 "O3 evidence/dictionary-index.json - synthetic")
        selection = validate_selection(reply, self.reference)
        self.assertTrue(selection["valid"])
        with self.assertRaisesRegex(ValueError, "optional evidence allowance exceeded"):
            extension_sources(reply, self.sums)
        self.assertFalse((CASE / "over-allowance" / "chain").exists())

    def test_04_independently_recompute_every_trial_and_envelope_bound(self):
        rates = {"docs": .354 * 1.10, "jlpt": .374 * 1.10, "cards": .502 * 1.10,
                 "evjson": .522 * 1.10, "extract": .446 * 1.10, "jmdict": .543 * 1.10,
                 "titleidx": .531 * 1.10, "kd-projection": .715}
        total_payload = 0
        tokens = 0
        for row in self.forecast["perSource"]:
            raw = frozen(PACKET / row["source"], row["sha256"])
            self.assertEqual(row["bytes"], len(raw))
            rate = rates[row["class"]]
            self.assertEqual(row["tpb"], rate)
            self.assertEqual(row["tokens"], math.ceil(len(raw) * rate))
            if row["source"].endswith(".json") or row["source"].startswith(("diffs/", "checks/")):
                self.assertEqual(row["class"], "evjson")
            total_payload += len(raw)
            tokens += math.ceil(len(raw) * rate)
        segment_bytes = sum(len(frozen(r["path"], r["sha256"])) for r in self.core["segments"])
        tokens += math.ceil((segment_bytes - total_payload) * .574)
        self.assertEqual(tokens, self.forecast["coreTokens"])
        excluded = set(self.reference["newCards"]) | set(self.reference["otherRequiredCards"]) | {
            c for r in self.reference["cards"] for c in r["distractors"]}
        targets = {c for r in self.reference["cards"] for c in r["quiz_exclusions"]} - excluded
        eligible = {"D": [], "E": []}
        for name, digest in self.sums.items():
            if name.startswith("repo/kanji/") and name.endswith(".md") and Path(name).stem not in excluded:
                raw = frozen(PACKET / name, digest)
                self.assertLessEqual(len(raw), 13900)
                # This matches build_chain's whole-source flush condition, not the forecast helper.
                score = math.ceil(len(raw) * .502 * 1.10) + math.ceil(2100 * .574)
                eligible["E" if Path(name).stem in targets else "D"].append((score, raw))
        observed_trials = []
        guard, _ = start_guard("B134 anonymous worst-size chain controls")
        try:
            for index, trial in enumerate(self.forecast["trials"], 1):
                cap = trial["caps"]
                rows = sorted(eligible["D"], reverse=True)[:cap["D"]]
                rows += sorted(eligible["E"], reverse=True)[:cap["E"]]
                payload = sum(len(raw) for _, raw in rows)
                envelope = 2100 * (len(rows) + 1)
                article_tokens = sum(math.ceil(len(raw) * .502 * 1.10) for _, raw in rows)
                article_tokens += math.ceil(envelope * .574)
                self.assertEqual(payload, trial["articleUpper"]["payloadBytes"])
                self.assertEqual(article_tokens, trial["articleUpper"]["tokens"])
                peak = tokens + article_tokens + 20000 + 80000 + 30000
                self.assertEqual(peak, trial["startupPeak"])
                self.assertEqual(trial["passes"], peak <= 700000)
                sources = [(f"synthetic-sized-article-{j}.md", raw, None)
                           for j, (_, raw) in enumerate(rows)]
                target = CASE / "anonymous-worst-size" / str(index)
                chain = build_chain(sources, target / "chain", target / "manifest.json", guard, "synthetic bound only")
                actual_envelope = sum(s["bytes"] for s in chain["segments"]) - payload
                self.assertLessEqual(actual_envelope, envelope)
                observed_trials.append({"caps": cap, "peak": peak, "anonymousChainBytes":
                                        sum(s["bytes"] for s in chain["segments"]),
                                        "measuredEnvelope": actual_envelope, "reservedEnvelope": envelope})
            self.assertEqual(next(t["caps"] for t in self.forecast["trials"] if t["passes"]),
                             {"D": 25, "E": 10})
            self.results["independentForecastTrials"] = observed_trials
        finally:
            self.assertFalse(guard.finish()["breach"])

    def test_05_exact_phase2_boundaries_both_families(self):
        for family, model, nominal, limit in (
            ("claude", "claude-opus-5.5", 952000, 740000),
            ("gpt", "gpt-6.1-sol", 922000, 710000),
        ):
            extension = self.forecast["maximumExtensionTokens"]
            last = limit - 7000 - extension - 30000
            events = [{"type": "session.start", "data": {"selectedModel": model, "contextTier": "long_context"}},
                      {"type": "session.usage_record", "data": {"usage": {
                          "inputTokens": last, "maxPromptTokens": nominal,
                          "model": family + "-fixture", "responseModel": family + "-fixture"}}}]
            self.assertTrue(phase2_gate(events, self.forecast, extension, family)["sendPhase2Message"])
            events[-1]["data"]["usage"]["inputTokens"] += 1
            self.assertFalse(phase2_gate(events, self.forecast, extension, family)["sendPhase2Message"])
            self.assertEqual(startup_bound(self.forecast, family, len(frozen(
                self.preflight["runs"][family]["prompt"]["path"])))["status"], "PASS_ESTIMATE")
        with self.assertRaises(ValueError):
            phase2_gate(events, self.forecast, self.forecast["maximumExtensionTokens"] + 1, "gpt")

    def test_06_full_two_phase_optional_access_and_rejections(self):
        case = CASE / "two-phase"
        report = case / "report" / "synthetic.md"
        report.parent.mkdir(parents=True)
        config = {**self.config, "report": str(report)}
        reply = "D: none\nE: none\nO1 K:紫 - synthetic complete record\nO2 evidence/dictionary-index.json - synthetic"
        events = FIXTURE.events_for(config, self.core)
        events[-3]["data"]["toolRequests"][0]["arguments"]["message"] = reply
        first = AUDIT.audit(events, config, self.core, self.reference)
        self.assertEqual(first["status"], "PHASE1_READY", first["breaches"])
        audit_dir = case / config["run"] / "phase1"
        first["eventsSha256"] = sha(jsonl(events))
        write_frozen(audit_dir / "events.jsonl", jsonl(events))
        freeze_json(audit_dir / "audit.json", first)
        write_frozen(audit_dir / "phase1-list.txt", reply.encode())
        cfg = freeze_json(case / "config.json", config)
        args = ["prepare-extension", "--config", cfg["path"], "--reply", str(audit_dir / "phase1-list.txt"),
                "--phase1-audit", str(audit_dir / "audit.json")]
        with patch.object(PREPARE, "HERE", case), patch.object(sys, "argv", args):
            PREPARE.main()
        extension = json.loads(frozen(case / (config["run"] + "-extension.json")))
        message = frozen(case / (config["run"] + "-phase2-message.txt")).decode()
        self.assertIn("Optional evidence units:", message)
        body = (HERE / "synthetic-validation-001" / "two-phase" / "report" / "synthetic.md").read_text("utf-8")
        body = body.replace("O: none", "O: O1 K:紫, O2 evidence/dictionary-index.json")
        final = copy.deepcopy(events)
        final.append({"type": "user.message", "data": {"content": message,
                      "source": "agent-" + config["coordinator"]}})

        def call(name, args, result):
            cid = "optional-final-" + str(len(final))
            final.extend([
                {"type": "assistant.message", "data": {"model": "gpt-fixture", "apiCallId": cid,
                 "toolRequests": [{"toolCallId": cid, "name": name, "arguments": args}]}},
                {"type": "tool.execution_complete", "data": {"toolCallId": cid, "success": True,
                                                           "result": {"content": result}}}])
        for segment in extension["segments"]:
            call("view", {"path": segment["path"], "forceReadLargeFiles": True}, frozen(segment["path"]).decode())
        call("create", {"path": str(report), "file_text": body}, "synthetic exclusive creation")
        with report.open("xb") as stream:
            stream.write(body.encode())
        call("view", {"path": str(report), "forceReadLargeFiles": True}, frozen(report).decode()
             if not report.stat().st_mode & 0o200 else report.read_text("utf-8"))
        call("send_session_message", {"session_id": config["coordinator"], "message": "UNVERIFIED"}, "synthetic")
        final.append({"type": "assistant.turn_end", "data": {}})
        freeze_json(case / (config["run"] + "-phase1.json"), {"auditDir": str(audit_dir)})
        with patch.object(b134_common, "HERE", case), patch.object(b134_runtime, "HERE", case):
            checked = AUDIT.audit(final, config, self.core, self.reference, extension, reply, message, final=True)
        self.assertEqual(checked["status"], "FINAL_AUDIT_NEEDS_CLAIM_CHECK", checked["breaches"])
        selection = validate_selection(reply, self.reference)
        self.assertEqual(STRUCTURE.check(body, config["run"], self.core, extension, self.reference,
                                        selection, message, "UNVERIFIED")["status"], "PASS")
        bad_body = body.replace("O: O1 K:紫, O2 evidence/dictionary-index.json", "O: none")
        self.assertNotEqual(STRUCTURE.check(bad_body, config["run"], self.core, extension, self.reference,
                                           selection, message, "UNVERIFIED")["status"], "PASS")
        for mutation in ("wrong-optional-return", "prohibited-direct-file", "unread-optional-segment"):
            altered = copy.deepcopy(final)
            index = next(i for i, e in enumerate(altered) if e["type"] == "assistant.message"
                         and e["data"].get("toolRequests", [{}])[0].get("arguments", {}).get("path")
                         == extension["segments"][0]["path"])
            if mutation == "wrong-optional-return":
                altered[index + 1]["data"]["result"]["content"] = "not the complete original record"
            elif mutation == "prohibited-direct-file":
                altered[index]["data"]["toolRequests"][0]["arguments"]["path"] = str(
                    PACKET / "evidence" / "kanjidic2-records.xml")
            else:
                del altered[index:index + 2]
            rejected = AUDIT.audit_base(altered, config, self.core, self.reference,
                                         extension, reply, message, final=True)
            self.assertEqual(rejected["status"], "VOID")
        self.results["fullOptionalTwoPhase"] = {"status": "PASS_SYNTHETIC_ONLY",
            "phase1ListSha256": sha(reply.encode()), "phase2MessageSha256": sha(message.encode()),
            "actualExtension": checked["extensionEvidenceCapacity"]["coverage"],
            "negativeOptionalReads": 3, "missingOptionalReportRejected": True}


if __name__ == "__main__":
    guard, _ = start_guard("B134 bounded optional evidence controls")
    try:
        result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Controls))
        if not result.wasSuccessful():
            raise SystemExit(1)
        print(json.dumps(freeze_json(HERE / "optional-validation-001.json", {
            "status": "PASS_BOUNDED_OPTIONAL_ACCESS_FORECAST_AND_AUDIT",
            "testsRun": result.testsRun, **Controls.results,
            "limits": "Synthetic protocol controls, no reviewer or teaching acceptance."})))
    finally:
        require(not guard.finish()["breach"], "Optional validation RAM breach")

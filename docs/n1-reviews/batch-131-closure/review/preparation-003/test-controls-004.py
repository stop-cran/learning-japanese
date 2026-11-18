"""Focused fabricated controls; no real reviewer session/log/list is opened or delivered."""
import copy
import io
import json
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from b131_review_v3_common import (
    CALIBRATION, CALIBRATION_SHA, FORECAST, HERE, PACKET, TOOLS, freeze_json, frozen,
    json_bytes, load_batch, load_module, require, sha, start_guard, verify_packet, write_frozen)
from b131_review_v2_derivations import (
    selected_supplements, verify_delta, verify_jm, verify_kd, verify_supplements)
import b131_capacity_002 as capacity
import b131_preflight_003 as preflight
import b131_runtime_003 as runtime
import prepare_chain_b131_003 as prepare

sys.path.insert(0, str(HERE))
import review_chain

ROOT = HERE / "validation-002"
AUDITOR = load_module("b131002_auditor_tests", HERE / "audit-review.py")


def fixture_events(config, core, text, tokens=500000):
    """Entirely generated, undelivered tool events reading frozen neutral fixtures."""
    events = [{"type": "session.start", "data": {"contextTier": "long_context"}},
              {"type": "user.message", "data": {"content": frozen(config["kickoff"]).decode("ascii"),
                                                "source": "agent-" + config["coordinator"]}},
              {"type": "session.usage_record", "data": {"usage": {
                  "inputTokens": tokens, "maxPromptTokens": 952000,
                  "model": "claude-fabricated", "responseModel": "claude-fabricated"}}}]
    counter = 0

    def call(name, args, result):
        nonlocal counter
        counter += 1
        cid = "fixture-" + str(counter)
        events.extend([
            {"type": "assistant.message", "data": {
                "model": "claude-fabricated", "apiCallId": "fixture-api-" + str(counter),
                "toolRequests": [{"toolCallId": cid, "name": name, "arguments": args}]}},
            {"type": "tool.execution_complete", "data": {
                "toolCallId": cid, "success": True, "result": {"content": result}}}])
    for path in [config["prompt"], *[row["path"] for row in core["segments"]]]:
        call("view", {"path": path, "forceReadLargeFiles": True}, frozen(path).decode("utf-8"))
    call("send_session_message", {"session_id": config["coordinator"], "message": text}, "fixture-only accepted")
    events.append({"type": "assistant.turn_end", "data": {}})
    return events


class Controls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.guard, _ = start_guard("B131002 focused synthetic validation")
        cls.config = load_batch(131)
        _, cls.sums, _ = verify_packet(cls.config, cls.guard)
        cls.proof = json.loads(frozen(HERE / "derivation-verification-002.json"))
        cls.reference = json.loads(frozen(PACKET / "eligibility-reference.json"))
        cls.full_jm = frozen(PACKET / "evidence/jmdict-families.xml")
        cls.jm = frozen(PACKET / "evidence/jmdict-review-core.xml")
        cls.full_kd = frozen(PACKET / "evidence/kanjidic2-records.xml")
        cls.kd = frozen(PACKET / "evidence/kanjidic2-review-projection.xml")
        cls.index = json.loads(frozen(PACKET / "evidence/dictionary-index.json"))
        cls.partition = cls.proof["jmdictPartition"]
        cls.forecast = json.loads(frozen(FORECAST))
        cls.chain = json.loads(frozen(HERE / "core-chain-compact-002.json"))
        cls.catalog = json.loads(frozen(PACKET / "evidence/jmdict-extension-index.json"))["characters"]
        cls.calibration = json.loads(frozen(CALIBRATION, CALIBRATION_SHA))
        cls.prompts = json.loads(frozen(HERE / "prompts/preflight-compact-003.json"))
        cls.audit_config = json.loads(frozen(cls.prompts["runs"]["claude"]["auditConfig"]))
        cls.eligible = capacity.eligible_costs(cls.sums, cls.reference, cls.catalog)
        # Selection is alphabetical/mechanical test data, never a linguistic candidate recommendation.
        cls.synthetic_character = next(row["character"] for row in cls.eligible["D"]
                                       if row["supplementalDictionaryBytes"] > 0 and row["articleBytes"] > 0)
        cls.synthetic_list = "D1 " + cls.synthetic_character + " - " + cls.reference["newCards"][0] + ": fixture-only\nE: none"
        cls.events = fixture_events(cls.audit_config, cls.chain, cls.synthetic_list)
        cls.sequence = 0

    @classmethod
    def tearDownClass(cls):
        cls.memory = cls.guard.finish()
        require(not cls.memory["breach"], "Validation RAM breach")

    def setUp(self):
        self.guard.check()
        type(self).sequence += 1
        self.case = ROOT / "fixtures" / f"{self.sequence:03d}-{self._testMethodName}"

    def actual_forecast(self, catalog=None):
        return capacity.compute_forecast(self.chain, self.calibration, self.sums, self.reference,
                                         self.catalog if catalog is None else catalog)

    def test_exact_projection_and_per_record_removals(self):
        self.assertEqual(verify_kd(self.full_kd, self.kd), self.proof["kanjidicRecords"])
        self.assertEqual((len(self.kd), len(self.proof["kanjidicRecords"])), (105248, 182))

    def test_tampered_projection_rejected(self):
        changed = self.kd.replace(b"<literal>", b"<literal altered=\"yes\">", 1)
        with self.assertRaisesRegex(ValueError, "exact permitted removal"):
            verify_kd(self.full_kd, changed)

    def test_exact_jmdict_partition(self):
        self.assertEqual(verify_jm(self.full_jm, self.jm, self.reference, self.index, self.partition), self.partition)
        self.assertEqual((self.partition["total"], self.partition["core"], self.partition["remainder"]), (874, 615, 259))
        self.assertEqual((self.partition["coreRecordBytes"], len(self.jm)), (249780, 249799))

    def test_missing_extra_and_wrong_partition_rejected(self):
        lines = self.jm.splitlines(keepends=True)
        for tampered in (b"".join(lines[:1] + lines[2:]), b"".join(lines[:-1] + [lines[1], lines[-1]])):
            with self.subTest(length=len(tampered)), self.assertRaises(ValueError):
                verify_jm(self.full_jm, tampered, self.reference, self.index, self.partition)
        changed = copy.deepcopy(self.partition)
        changed["coreIds"][0] = changed["remainderIds"][0]
        with self.assertRaisesRegex(ValueError, "exact rule"):
            verify_jm(self.full_jm, self.jm, self.reference, self.index, changed)

    def test_title_delta_and_mismatch(self):
        before, after = (frozen(PACKET / "evidence" / name) for name in
                         ("baseline-title-index.txt", "title-index.txt"))
        delta = frozen(PACKET / "evidence/title-index-delta.txt")
        self.assertEqual(verify_delta(before, after, delta), self.proof["titleDelta"])
        with self.assertRaisesRegex(ValueError, "delta differs"):
            verify_delta(before, after, delta + b"+unrequested\n")

    def test_forecast_reproducibility_and_chosen_largest_cap(self):
        computed = self.actual_forecast()
        self.assertEqual(computed, self.actual_forecast())
        self.assertTrue(all(self.forecast[key] == value for key, value in computed.items()))
        self.assertEqual(computed["chosenCaps"], {"D": 25, "E": 10})
        self.assertEqual(computed["projectedWorstCasePeak"], 698784)
        self.assertTrue(all(not row["passes"] for row in computed["trials"] if row["D"] > 25))

    def test_forecast_above_gate_has_no_permitted_cap(self):
        trials, chosen = capacity.choose_cap(700000, self.eligible)
        self.assertIsNone(chosen)
        self.assertTrue(all(not row["passes"] and row["projectedWorstCasePeak"] > 700000 for row in trials))

    def test_omitted_worst_case_dictionary_cost_rejected(self):
        changed = self.actual_forecast({})
        self.assertLess(changed["trials"][0]["worstCaseExtension"]["supplementalDictionaryBytes"],
                        self.forecast["trials"][0]["worstCaseExtension"]["supplementalDictionaryBytes"])
        with patch("b131_preflight_002.compute_forecast", return_value=changed):
            with self.assertRaisesRegex(ValueError, "not reproducible"):
                preflight.verify_subset(self.guard)

    def test_phase1_over_cap_list_rejected(self):
        cap = self.forecast["chosenCaps"]["D"]
        text = "\n".join(f"D{i} {row['character']} - {self.reference['newCards'][0]}: fixture-only"
                         for i, row in enumerate(self.eligible["D"][:cap + 1], 1)) + "\nE: none"
        result = review_chain.validate_selection(text, self.reference)
        self.assertFalse(result["valid"])
        self.assertTrue(any("cap" in error for error in result["errors"]))

    def test_core_chain_coverage_and_sha(self):
        sources = [(row["source"], frozen(PACKET / row["source"]), None) for row in self.chain["sources"]]
        self.assertEqual(preflight.verify_chain(self.chain, sources)["segments"], 66)
        changed = copy.deepcopy(self.chain)
        changed["segments"][0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "Changed input"):
            preflight.verify_chain(changed, sources)
        changed = copy.deepcopy(self.chain)
        changed["segments"][-1]["parts"].pop()
        with self.assertRaises(ValueError):
            preflight.verify_chain(changed, sources)

    def test_prompt_pair_identity_and_nonidentity(self):
        left, right = [frozen(spec["prompt"]) for spec in self.prompts["runs"].values()]
        self.assertEqual(preflight.normalize_prompt(left), preflight.normalize_prompt(right))
        self.assertNotEqual(preflight.normalize_prompt(left), preflight.normalize_prompt(right + b"\nnot identity"))

    def test_complete_preflight(self):
        self.assertEqual(preflight.verify_subset(self.guard)["status"], "VERIFIED_IMMUTABLE_SUBSET_ONLY")
        self.assertEqual(preflight.verify_protocol(self.prompts)["status"], "PASS_PAIRED_PROTOCOL")

    def test_preflight_bad_binding_rejected(self):
        changed = copy.deepcopy(self.audit_config)
        changed["files"][0]["sha256"] = "0" * 64
        original = preflight.frozen
        config_path = self.prompts["runs"]["claude"]["auditConfig"]
        def altered(path, expected=None):
            return json_bytes(changed) if str(path) == config_path else original(path, expected)
        with patch.object(preflight, "frozen", side_effect=altered), self.assertRaisesRegex(ValueError, "Changed input"):
            preflight.verify_protocol(self.prompts)

    def test_exact_selected_supplements_deduplicated_in_union_order(self):
        characters = [row["character"] for row in self.eligible["D"] if row["supplementalDictionaryBytes"]][:5]
        selected, matches = selected_supplements(self.full_jm, self.partition, characters)
        self.assertTrue(selected)
        self.assertEqual(verify_supplements(self.full_jm, self.partition, characters, selected), matches)
        ids = [identity for identity, _ in selected]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertFalse(set(ids) & set(self.partition["coreIds"]))
        self.assertEqual(ids, [identity for identity in self.partition["remainderIds"] if identity in ids])

    def test_omitted_matching_and_altered_supplemental_records_rejected(self):
        selected, _ = selected_supplements(self.full_jm, self.partition, [self.synthetic_character])
        self.assertTrue(selected)
        for changed in (selected[1:], [(selected[0][0], selected[0][1] + b"altered")] + selected[1:]):
            with self.subTest(length=len(changed)), self.assertRaisesRegex(ValueError, "omitted/altered"):
                verify_supplements(self.full_jm, self.partition, [self.synthetic_character], changed)

    def test_no_dictionary_match_has_no_substitute(self):
        selected, matches = selected_supplements(self.full_jm, self.partition, ["\u9fff"])
        self.assertEqual(selected, [])
        self.assertEqual(matches["\u9fff"], {"matchingCoreIds": [], "matchingRemainderIds": []})

    def test_phase1_audit_peak_and_compaction_hold(self):
        result = AUDITOR.audit(self.events, self.audit_config, self.chain, self.reference)
        self.assertEqual(result["status"], "PHASE1_READY", result["breaches"])
        self.assertEqual(result["capacityTelemetry"]["actualPeakInputTokens"], 500000)
        self.assertEqual(result["capacityTelemetry"]["actualMinusForecast"], 507000 - 526615)
        events = self.events + [{"type": "session.compaction_start", "data": {"currentTokens": 765000}}]
        held = AUDITOR.audit(events, self.audit_config, self.chain, self.reference)
        self.assertEqual(held["status"], "HOLD_CONTEXT_COMPACTED")
        self.assertTrue(held["capacityTelemetry"]["compactions"])

    def test_missing_actual_tokens_or_small_context_hold(self):
        for field in ("inputTokens", "maxPromptTokens"):
            events = copy.deepcopy(self.events)
            events[2]["data"]["usage"].pop(field)
            held = AUDITOR.audit(events, self.audit_config, self.chain, self.reference)
            self.assertEqual(held["status"], "HOLD_CONTEXT_UNVERIFIED")

    def test_pre_phase2_boundary_hold_and_omitted_cost(self):
        selection = review_chain.validate_selection(self.synthetic_list, self.reference)
        _, _, _, cost = prepare.extension_sources(selection, self.sums, self.partition)
        self.assertGreater(cost["supplementalDictionaryBytes"], 0)
        bound = 740000 - 7000 - 30000 - cost["tokens"]
        events = copy.deepcopy(self.events)
        events[2]["data"]["usage"]["inputTokens"] = bound
        self.assertTrue(capacity.phase2_gate(events, self.forecast, cost)["sendPhase2Message"])
        events[2]["data"]["usage"]["inputTokens"] += 1
        self.assertEqual(capacity.phase2_gate(events, self.forecast, cost)["status"], "HOLD_PRE_PHASE2_CAPACITY")
        altered = dict(cost)
        altered["supplementalDictionaryBytes"] = 0
        with self.assertRaisesRegex(ValueError, "altered or omitted"):
            capacity.phase2_gate(self.events, self.forecast, altered)

    def build_synthetic_extension(self, held=False):
        """Real chain builder, fabricated phase1 only, isolated outputs; never a launch/admission."""
        run = self.audit_config["run"]
        events = copy.deepcopy(self.events)
        if held:
            events[2]["data"]["usage"]["inputTokens"] = 739000
        result = AUDITOR.audit(events, self.audit_config, self.chain, self.reference)
        self.assertEqual(result["status"], "PHASE1_READY", result["breaches"])
        event_raw = b"".join((json.dumps(event, ensure_ascii=False) + "\n").encode("utf-8") for event in events)
        audit_dir = self.case / run / "audit-synthetic"
        write_frozen(audit_dir / "events.jsonl", event_raw)
        write_frozen(audit_dir / "phase1-list.txt", self.synthetic_list.encode("utf-8"))
        result.update(session="synthetic-undelivered-002", eventsSha256=sha(event_raw))
        freeze_json(audit_dir / "audit.json", result)
        write_frozen(self.case / "derivation-verification-002.json", frozen(HERE / "derivation-verification-002.json"))
        with patch.object(prepare, "HERE", self.case), redirect_stdout(io.StringIO()):
            code = prepare.main(["131", "--run", run, "--reply", str(audit_dir / "phase1-list.txt"),
                                 "--phase1-audit", str(audit_dir / "audit.json")])
        return code, self.case / f"{run}-phase2-message.txt", audit_dir / "audit.json"

    def test_real_extension_builder_and_capacity_evidence_verifier(self):
        code, message_path, audit_path = self.build_synthetic_extension()
        self.assertEqual(code, 0)
        chain = json.loads(frozen(self.case / f"{self.audit_config['run']}-extension.json"))
        with patch.object(runtime, "HERE", self.case):
            result = runtime.validate_prepared_extension(self.audit_config, chain, self.synthetic_list,
                                                          frozen(message_path).decode("utf-8"), audit_path)
        self.assertEqual(result["status"], "PASS")
        self.assertGreater(result["independentlyRecomputedSupplementalDictionaryBytes"], 0)

    def test_actual_hold_creates_no_phase2_message_or_chain(self):
        code, message_path, _ = self.build_synthetic_extension(held=True)
        self.assertEqual(code, 1)
        self.assertFalse(message_path.exists())
        self.assertFalse((self.case / f"{self.audit_config['run']}-extension.json").exists())
        held = json.loads(frozen(self.case / f"{self.audit_config['run']}-pre-phase2-capacity.json"))
        self.assertEqual(held["status"], "HOLD_PRE_PHASE2_CAPACITY")
        self.assertFalse(held["sendPhase2Message"])

    def test_coherently_omitted_dictionary_capacity_rejected(self):
        _, message_path, audit_path = self.build_synthetic_extension()
        run = self.audit_config["run"]
        chain = json.loads(frozen(self.case / f"{run}-extension.json"))
        ext_preflight = json.loads(frozen(self.case / f"{run}-extension-preflight.json"))
        old_capacity_path = ext_preflight["capacity"]["path"]
        altered = json.loads(frozen(old_capacity_path))
        cost = altered["extension"]
        wrong = capacity.extension_tokens(cost["articleBytes"], 0, cost["articleCount"], 0)
        altered.update(capacity.phase2_gate(self.events, self.forecast, wrong))
        raw = json_bytes(altered)
        ext_preflight["capacity"]["sha256"] = sha(raw)
        original = runtime.frozen
        def changed(path, expected=None):
            if str(path) == old_capacity_path:
                self.assertEqual(expected, sha(raw))
                return raw
            if str(path) == str(self.case / f"{run}-extension-preflight.json"):
                return json_bytes(ext_preflight)
            return original(path, expected)
        with patch.object(runtime, "HERE", self.case), patch.object(runtime, "frozen", side_effect=changed):
            with self.assertRaisesRegex(ValueError, "capacity proof omitted/changed"):
                runtime.validate_prepared_extension(self.audit_config, chain, self.synthetic_list,
                                                    frozen(message_path).decode("utf-8"), audit_path)

    def test_audit_cli_preserves_snapshot_and_requires_no_compaction(self):
        cfg = dict(self.audit_config, run="FIXTURE-CLAUDE-002")
        cfg_path = self.case / "fixture-config.json"
        freeze_json(cfg_path, cfg)
        events = self.events + [{"type": "session.compaction_complete", "data": {}}]
        event_raw = b"".join((json.dumps(event, ensure_ascii=False) + "\n").encode("utf-8") for event in events)
        event_path = self.case / "fabricated-events.jsonl"
        write_frozen(event_path, event_raw)
        stream = io.StringIO()
        with patch.object(AUDITOR, "OUTPUT_BASE", self.case / "audit-output"), redirect_stdout(stream):
            AUDITOR.main(["--session", "synthetic-002", "--config", str(cfg_path), "--events-file", str(event_path)])
        audit_path = Path(next(line[7:] for line in stream.getvalue().splitlines() if line.startswith("Audit: ")))
        result = json.loads(frozen(audit_path))
        self.assertEqual(result["status"], "HOLD_CONTEXT_COMPACTED")
        self.assertEqual(frozen(audit_path.parent / "events.jsonl"), event_raw)
        self.assertFalse((audit_path.parent / "phase1-list.txt").exists())

    def test_bounded_lifecycle_adapter_exact_json_success_and_refusal(self):
        adapter = load_module("b131002_lifecycle_adapter_tests", TOOLS / "b131_lifecycle_process_004.py")
        events = [{"type": "session.start", "data": {"contextTier": "long_context"}},
                  {"type": "session.usage_record", "data": {"usage": {"maxPromptTokens": 952000}}}]
        for index, compacted in enumerate((False, True)):
            rows = events + ([{"type": "session.compaction_start", "data": {}}] if compacted else [])
            path = self.case / f"synthetic-context-{index}.jsonl"
            write_frozen(path, b"".join((json.dumps(row) + "\n").encode() for row in rows))
            code, out, _ = adapter.python(HERE / "check-run-context.py", path)
            result = json.loads(out)
            self.assertEqual(code, 1 if compacted else 0)
            self.assertEqual(result["status"], "FAIL" if compacted else "PASS")



    def test_complete_two_phase_create_readback_and_final_audit(self):
        code, message_path, audit_path = self.build_synthetic_extension()
        self.assertEqual(code, 0)
        run = self.audit_config["run"]
        extension = json.loads(frozen(self.case / (run + "-extension.json")))
        message = frozen(message_path).decode("utf-8")
        report = self.case / "report-output" / "synthetic-report.md"
        report.parent.mkdir(parents=True)
        config = dict(self.audit_config, report=str(report))
        events = copy.deepcopy(self.events)
        events.append({"type": "user.message", "data": {
            "content": message, "source": "agent-" + config["coordinator"]}})
        counter = 0
        def call(name, args, returned):
            nonlocal counter
            counter += 1
            cid = "synthetic-final-" + str(counter)
            events.extend([
                {"type": "assistant.message", "data": {"model": "claude-fabricated",
                    "apiCallId": cid, "toolRequests": [
                        {"toolCallId": cid, "name": name, "arguments": args}]}},
                {"type": "tool.execution_complete", "data": {
                    "toolCallId": cid, "success": True, "result": {"content": returned}}}])
        for segment in extension["segments"]:
            call("view", {"path": segment["path"], "forceReadLargeFiles": True},
                 frozen(segment["path"]).decode("utf-8"))
        body = "synthetic undelivered report\n"
        call("create", {"path": str(report), "file_text": body}, "fixture-only created")
        report.write_bytes(body.encode("utf-8"))
        call("view", {"path": str(report), "forceReadLargeFiles": True}, body)
        call("send_session_message", {"session_id": config["coordinator"], "message": "UNVERIFIED"},
             "fixture-only accepted")
        events.append({"type": "assistant.turn_end", "data": {}})
        freeze_json(self.case / (run + "-phase1.json"), {"auditDir": str(audit_path.parent)})
        write_frozen(self.case / "batch.json", frozen(HERE / "batch.json"))
        with patch("b131_review_v3_common.HERE", self.case), patch.object(runtime, "HERE", self.case):
            result = AUDITOR.audit(events, config, self.chain, self.reference, extension,
                                   self.synthetic_list, message, final=True)
        self.assertEqual(result["status"], "FINAL_AUDIT_NEEDS_CLAIM_CHECK", result.get("breaches"))
        self.assertTrue(result["readbackVerified"])
        self.assertTrue(report.is_file())


def main():
    require(not ROOT.exists(), "Preserve every previous validation attempt")
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Controls)
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    text = stream.getvalue()
    write_frozen(ROOT / "output.log", text.encode("utf-8"))
    record = {
        "status": "PASS" if result.wasSuccessful() else "FAIL", "tests": result.testsRun,
        "failures": len(result.failures), "errors": len(result.errors),
        "testTool": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "outputSha256": sha(text.encode("utf-8")), "memory": getattr(Controls, "memory", None),
        "scope": "Fabricated undelivered events and mechanically generated test-only characters. "
                 "No actual reviewer record/selection, admission, launch, teaching edit, commit or push.",
        "cases": [line.strip() for line in text.splitlines() if line.startswith("test_")]}
    print(text)
    print(json.dumps(freeze_json(ROOT / "result.json", record)))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())

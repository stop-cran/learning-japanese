"""Focused bootstrap, capacity-HOLD, and boundary mutation controls."""
import copy
import contextlib
import io
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent.parent
PROTOCOL = HERE / "protocol-002"
PROMPTS = HERE / "prompts-002"
GATE_PATH = PROTOCOL / "fresh-review-protocol-002.py"
SPEC = importlib.util.spec_from_file_location("fresh_review_protocol_002", GATE_PATH)
GATE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)
sys_path_added = str(GATE.PRECEDENT_PROTOCOL)
if sys_path_added not in sys.path:
    sys.path.insert(0, sys_path_added)
from review_chain_with_optional import build_chain
capacity_path = str(GATE.PRECEDENT_PROTOCOL.parent / "tools")
if capacity_path not in sys.path:
    sys.path.insert(0, capacity_path)
from capacity004 import project, xml_bytes


def fixture(family="claude"):
    profile = GATE.PROFILES[family]
    config = {
        "expectedFamily": family,
        "contextProfile": {**profile, "contextTier": "long_context"},
        "prompt": str(PROMPTS / "initial-review-002.txt"),
        "kickoff": str(PROMPTS / "kickoff-fresh-review-002.txt"),
    }
    prompt = GATE.frozen(config["prompt"]).decode("utf-8")
    kickoff = GATE.frozen(config["kickoff"]).decode("utf-8")
    rows = [
        {"type": "session.start", "data": {
            "selectedModel": profile["selectedModel"], "contextTier": "long_context"}},
        {"type": "user.message", "data": {
            "content": kickoff, "source": "agent-" + GATE.COORDINATOR}},
        {"type": "session.usage_record", "data": {"usage": {
            "inputTokens": 42000, "maxPromptTokens": profile["maxPromptTokens"],
            "model": profile["selectedModel"], "responseModel": profile["selectedModel"]}}},
        {"type": "assistant.message", "data": {"toolRequests": [{
            "toolCallId": "bootstrap-1", "name": "view",
            "arguments": {"path": config["prompt"], "forceReadLargeFiles": True}}]}},
        {"type": "tool.execution_complete", "data": {
            "toolCallId": "bootstrap-1", "toolName": "view",
            "success": True, "result": {"content": prompt}}},
        {"type": "assistant.turn_end", "data": {}},
    ]
    raw = b"".join((json.dumps(row, ensure_ascii=False) + "\n").encode("utf-8") for row in rows)
    return config, rows, raw


def two_phase_fixture(root):
    family = "claude"
    profile = GATE.PROFILES[family]
    config, rows, _ = fixture(family)
    rows = rows[:3]
    config.update({
        "run": "N1-B134-CLAUDE-FRESH-002",
        "candidate": "355cccb840d22e7313e79f234eb93d1367e00352",
        "coordinator": GATE.COORDINATOR,
        "completionContract": "entire-message-enum-v1",
        "maxWebFetches": 0,
        "report": str(root / "review-report.md"),
    })
    core = json.loads((HERE / "fresh-independent-core-001.json").read_text(encoding="utf-8"))
    reference = json.loads((HERE / "packet" / "eligibility-reference.json").read_text(encoding="utf-8"))
    counter = 0

    def call(name, args, result):
        nonlocal counter
        counter += 1
        call_id = f"synthetic-{counter}"
        rows.extend([
            {"type": "assistant.message", "data": {"model": profile["selectedModel"],
                "apiCallId": call_id, "toolRequests": [{"toolCallId": call_id, "name": name,
                                                          "arguments": args}]}},
            {"type": "tool.execution_complete", "data": {"toolCallId": call_id,
                "toolName": name, "arguments": args, "success": True, "result": {"content": result}}},
        ])

    call("view", {"path": config["prompt"], "forceReadLargeFiles": True},
         GATE.frozen(config["prompt"]).decode("utf-8"))
    rows.append({"type": "assistant.turn_end", "data": {}})
    first_segment = core["segments"][0]["path"]
    rows.append({"type": "user.message", "data": {"content": first_segment,
                 "source": "agent-" + GATE.COORDINATOR}})
    for segment in core["segments"]:
        call("view", {"path": segment["path"], "forceReadLargeFiles": True},
             GATE.frozen(segment["path"]).decode("utf-8"))
    phase1_text = "D: none\nE: none\nO: none"
    call("send_session_message", {"session_id": GATE.COORDINATOR, "message": phase1_text},
         "synthetic phase-one admission only")
    rows.append({"type": "assistant.turn_end", "data": {}})
    phase1_events = copy.deepcopy(rows)

    phase2_text = "Read the independently prepared extension now."
    rows.append({"type": "user.message", "data": {"content": phase2_text,
                 "source": "agent-" + GATE.COORDINATOR}})
    class Guard:
        def check(self):
            return None
    with tempfile.TemporaryDirectory(dir=root) as tmp:
        extension_source = ("evidence/synthetic.txt", b"synthetic extension evidence\n", None)
        extension = build_chain([extension_source], Path(tmp) / "chain",
                                Path(tmp) / "extension.json", Guard(), "synthetic extension")
        for segment in extension["segments"]:
            call("view", {"path": segment["path"], "forceReadLargeFiles": True},
                 GATE.frozen(segment["path"]).decode("utf-8"))
        report_text = "# Synthetic report\nVerdict: UNVERIFIED\n"
        report = Path(config["report"])
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(report_text, encoding="utf-8", newline="\n")
        call("create", {"path": str(report), "file_text": report_text}, "synthetic report created")
        call("view", {"path": str(report), "forceReadLargeFiles": True}, report_text)
        call("send_session_message", {"session_id": GATE.COORDINATOR, "message": "UNVERIFIED"},
             "synthetic completion")
        rows.append({"type": "assistant.turn_end", "data": {}})
        result = GATE.audit_core_boundary(
            rows, family, config, core, reference, extension,
            phase1_text, phase2_text, final=True)
    return config, core, reference, phase1_events, phase1_text, phase2_text, result


class FreshProtocolControls(unittest.TestCase):
    def test_bootstrap_cli_persists_a_non_overwriting_bound_record(self):
        config, rows, raw = fixture()
        with tempfile.TemporaryDirectory(dir=PROTOCOL) as tmp:
            root = Path(tmp)
            events_path = root / "events.jsonl"
            config_path = root / "config.json"
            output_path = root / "bootstrap-record.json"
            events_path.write_bytes(raw)
            config_path.write_text(json.dumps(config), encoding="utf-8")
            original_argv = sys.argv
            try:
                sys.argv = [str(GATE_PATH), "bootstrap", "--family", "claude",
                            "--events", str(events_path), "--config", str(config_path),
                            "--output", str(output_path)]
                with contextlib.redirect_stdout(io.StringIO()):
                    GATE.main()
                record = json.loads(output_path.read_text(encoding="utf-8"))
                self.assertEqual(record["status"], "PASS_BOOTSTRAP_WAIT")
                self.assertEqual(record["eventsSha256"], GATE.sha(raw))
                with contextlib.redirect_stdout(io.StringIO()), self.assertRaises(FileExistsError):
                    GATE.main()
            finally:
                sys.argv = original_argv

    def test_kd_projection_allowed_fields_and_sixteen_retained_mutations(self):
        source = (HERE / "packet" / "evidence" / "kanjidic2-complete-union.xml").read_bytes()
        original = ET.fromstring(source)
        expected = ET.canonicalize(ET.tostring(project(source), encoding="unicode"), strip_text=True)

        def clone():
            return copy.deepcopy(original)

        def add_dropped(path, tag, attrib=None, child=None):
            root = clone()
            record = next(node for node in root if node.findtext("literal") == "紫")
            parent = record
            for name in path:
                parent = parent.find(name)
                if parent is None:
                    parent = ET.SubElement(record, "reading_meaning")
                    parent = ET.SubElement(parent, "rmgroup")
            node = ET.SubElement(parent, tag, attrib or {})
            if child:
                ET.SubElement(node, child[0]).text = child[1]
            else:
                node.text = "before"
            node.text = "after"
            return root

        dropped_cases = (
            ((), "codepoint", {}, ("cp_value", "U+7D2B")),
            ((), "dic_number", {}, ("dic_ref", "1")),
            ((), "query_code", {}, ("q_code", "1-1-1")),
            (("reading_meaning", "rmgroup"), "meaning", {"m_lang": "es"}, None),
            (("reading_meaning", "rmgroup"), "reading", {"r_type": "pinyin"}, None),
            (("reading_meaning", "rmgroup"), "reading", {"r_type": "korean_r"}, None),
            (("reading_meaning", "rmgroup"), "reading", {"r_type": "korean_h"}, None),
            (("reading_meaning", "rmgroup"), "reading", {"r_type": "vietnam"}, None),
        )
        for case in dropped_cases:
            with self.subTest(dropped=case[1:]):
                mutated = xml_bytes(add_dropped(*case))
                result = ET.canonicalize(ET.tostring(project(mutated), encoding="unicode"), strip_text=True)
                self.assertEqual(result, expected)

        def retained(mutator):
            root = clone()
            target = next(node for node in root if node.findtext("literal") == "紫")
            group = target.find("reading_meaning/rmgroup")
            self.assertIsNotNone(group)
            mutator(target, group)
            return ET.canonicalize(ET.tostring(project(xml_bytes(root)), encoding="unicode"),
                                  strip_text=True)

        mutations = (
            lambda row, group: setattr(row.find("literal"), "text", "紫X"),
            lambda row, group: setattr(row.find("radical/rad_value"), "text", "999"),
            lambda row, group: row.find("radical/rad_value").set("rad_type", "changed"),
            lambda row, group: setattr(row.find("misc/grade"), "text", "99"),
            lambda row, group: setattr(row.find("misc/stroke_count"), "text", "99"),
            lambda row, group: setattr(row.find("misc/jlpt"), "text", "99"),
            lambda row, group: row.find("misc").set("review_mutation", "1"),
            lambda row, group: setattr(group.find("reading[@r_type='ja_on']"), "text", "あX"),
            lambda row, group: group.find("reading[@r_type='ja_on']").set("r_type", "changed"),
            lambda row, group: setattr(group.find("reading[@r_type='ja_kun']"), "text", "あX"),
            lambda row, group: group.find("reading[@r_type='ja_kun']").set("r_type", "changed"),
            lambda row, group: setattr(group.find("meaning"), "text", "changed"),
            lambda row, group: setattr(ET.SubElement(group, "nanori"), "text", "changed"),
            lambda row, group: row.find("misc").append(ET.Element("retained_extension")),
            lambda row, group: group.find("meaning").set("review_mutation", "1"),
            lambda row, group: row.__setitem__(slice(None), list(reversed(row))),
        )
        for index, mutate in enumerate(mutations, 1):
            with self.subTest(retained=index):
                self.assertNotEqual(retained(mutate), expected,
                                    f"retained-field mutation {index} was lost")

    def test_exact_bootstrap_wait_passes_for_both_profiles(self):
        for family in ("claude", "gpt"):
            with self.subTest(family=family):
                config, rows, raw = fixture(family)
                result = GATE.verify_bootstrap(rows, raw, family, config)
                self.assertEqual(result["status"], "PASS_BOOTSTRAP_WAIT")
                self.assertFalse(result["coreChainDelivered"])
                self.assertEqual(result["runtime"]["selectedModel"], GATE.PROFILES[family]["selectedModel"])
                self.assertEqual(result["runtime"]["contextTier"], "long_context")
                self.assertEqual(result["runtime"]["maxPromptTokens"], GATE.PROFILES[family]["maxPromptTokens"])

    def test_runtime_profile_and_compaction_mutations_reject(self):
        mutations = (
            lambda rows: rows[0]["data"].update(selectedModel="auto"),
            lambda rows: rows[0]["data"].update(contextTier=None),
            lambda rows: rows[2]["data"]["usage"].update(maxPromptTokens=200000),
            lambda rows: rows[2]["data"]["usage"].update(inputTokens=953000),
            lambda rows: rows.insert(3, {"type": "session.compaction_start", "data": {}}),
            lambda rows: rows.pop(2),
        )
        for mutate in mutations:
            config, rows, _ = fixture()
            mutate(rows)
            raw = b"".join((json.dumps(row, ensure_ascii=False) + "\n").encode("utf-8") for row in rows)
            with self.subTest(mutation=mutate), self.assertRaises(ValueError):
                GATE.verify_bootstrap(rows, raw, "claude", config)

    def test_prompt_only_boundary_mutations_reject(self):
        mutations = (
            lambda rows: rows[1]["data"].update(content="different kickoff"),
            lambda rows: rows[3]["data"]["toolRequests"][0]["arguments"].update(
                path="C:\\outside\\prompt.txt"),
            lambda rows: rows[3]["data"]["toolRequests"][0]["arguments"].update(view_range=[1, 2]),
            lambda rows: rows[4]["data"]["result"].update(content="truncated"),
            lambda rows: rows.insert(4, {"type": "assistant.message", "data": {"toolRequests": [{
                "toolCallId": "extra", "name": "rg", "arguments": {"pattern": "x"}}]}}),
            lambda rows: rows.append({"type": "user.message", "data": {
                "content": "continue", "source": "agent-" + GATE.COORDINATOR}}),
            lambda rows: rows.pop(),
        )
        for mutate in mutations:
            config, rows, _ = fixture()
            mutate(rows)
            raw = b"".join((json.dumps(row, ensure_ascii=False) + "\n").encode("utf-8") for row in rows)
            with self.subTest(mutation=mutate), self.assertRaises(ValueError):
                GATE.verify_bootstrap(rows, raw, "claude", config)

    def test_current_capacity_hold_refuses_core_delivery(self):
        config, rows, raw = fixture()
        bootstrap = GATE.verify_bootstrap(rows, raw, "claude", config)
        case = HERE / "protocol-002" / "fixture-bootstrap-events.jsonl"
        case.write_bytes(raw)
        try:
            with self.assertRaisesRegex(ValueError, "HOLD_ESTIMATE"):
                GATE.authorize_core(bootstrap, case)
        finally:
            case.unlink()

    def test_synthetic_two_phase_boundary_and_rejections(self):
        with tempfile.TemporaryDirectory(dir=PROTOCOL) as tmp:
            config, core, reference, phase1_events, phase1_text, phase2_text, final = two_phase_fixture(Path(tmp))
            phase1 = GATE.audit_core_boundary(phase1_events, "claude", config, core, reference)
            self.assertEqual(phase1["status"], "PHASE1_READY", phase1["breaches"])
            self.assertTrue(phase1["bootstrapBoundaryVerified"])
            self.assertEqual(final["status"], "FINAL_AUDIT_NEEDS_CLAIM_CHECK", final["breaches"])
            self.assertTrue(final["bootstrapBoundaryVerified"])
            self.assertEqual(final["messages"], [phase1_text, "UNVERIFIED"])

            bad_core = copy.deepcopy(phase1_events)
            next(row for row in bad_core if row.get("type") == "user.message"
                 and row["data"].get("content") != GATE.frozen(config["kickoff"]).decode("utf-8"))["data"]["content"] = \
                "C:\\outside\\unbound-segment.txt"
            with self.assertRaisesRegex(ValueError, "message sequence"):
                GATE.audit_core_boundary(bad_core, "claude", config, core, reference)

            bad_order = copy.deepcopy(phase1_events)
            bootstrap_end = next(i for i, row in enumerate(bad_order)
                                 if row.get("type") == "assistant.turn_end")
            bad_order.insert(bootstrap_end + 1, {
                "type": "assistant.message", "data": {"toolRequests": [{
                    "toolCallId": "premature", "name": "rg", "arguments": {"pattern": "x"}}]}})
            with self.assertRaisesRegex(ValueError, "between bootstrap wait"):
                GATE.audit_core_boundary(bad_order, "claude", config, core, reference)

            omitted = copy.deepcopy(phase1_events)
            last_core_view = next(i for i in range(len(omitted) - 1, -1, -1)
                                  if omitted[i].get("type") == "assistant.message"
                                  and any(request.get("name") == "view"
                                          and request.get("arguments", {}).get("path")
                                          == core["segments"][-1]["path"]
                                          for request in omitted[i]["data"].get("toolRequests", [])))
            omitted.pop(last_core_view + 1)
            omitted.pop(last_core_view)
            rejected = GATE.audit_core_boundary(omitted, "claude", config, core, reference)
            self.assertEqual(rejected["status"], "VOID")


if __name__ == "__main__":
    unittest.main(verbosity=2)

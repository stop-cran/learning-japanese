"""Focused B131 preparation and rejection controls; synthetic review events only."""
import copy
import importlib.util
import io
import json
import stat
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from contextlib import redirect_stdout
from datetime import datetime, timedelta, timezone
from pathlib import Path

from b131_neutral_common_001 import (
    BASE, CANDIDATE, COORDINATOR, HERE, MEMBERS, PACKET, PROOFS, RECORDS, TOOLS,
    freeze_json, frozen, load_batch, require, sha, start_guard, verify_packet, write_frozen)
from b131_review_admission_001 import validate_roster
from b129_confirmation_presentation import canonical

sys.path.insert(0, str(HERE))
import review_chain


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


class PreparationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = load_batch(131)
        cls.root, cls.sums, cls.packet_sha = verify_packet(cls.config)
        cls.chain = json.loads(frozen(HERE / "core-chain-compact-001.json"))
        cls.preflight = json.loads(frozen(HERE / "prompts" / "preflight-compact-002.json"))

    def test_exact_complete_source_union_and_empty_residuals(self):
        contract = json.loads(frozen(HERE / "source-contract.json"))
        self.assertEqual(contract["candidate"], CANDIDATE)
        self.assertEqual(contract["base"], BASE)
        self.assertEqual(len(contract["selections"]), 7)
        self.assertEqual(len(contract["files"]), 11)
        for binding in contract["files"].values():
            frozen(binding["path"], binding["sha256"])
        for filename, tag, identity, expected in (
            ("jmdict-families.xml", "entry", "ent_seq", 874),
            ("kanjidic2-records.xml", "character", "literal", 182)):
            records = {}
            for binding in contract["files"].values():
                if "\\original\\" not in binding["path"]:
                    continue
                raw = frozen(binding["path"], binding["sha256"])
                for node in ET.fromstring(raw).findall(tag):
                    key = node.findtext(identity)
                    value = canonical(ET.tostring(node, encoding="utf-8"))
                    if key in records:
                        self.assertEqual(records[key], value)
                    records[key] = value
            actual = {node.findtext(identity): canonical(ET.tostring(node, encoding="utf-8"))
                      for node in ET.fromstring(frozen(PACKET / "evidence" / filename))}
            self.assertEqual(len(actual), expected)
            self.assertEqual(records, actual)
            self.assertEqual(len(frozen(PACKET / "evidence" / filename).splitlines()), expected + 2)
        for filename in ("jmdict-final-families.xml", "jmdict-final-families-002.xml"):
            self.assertEqual(len(ET.fromstring(frozen(HERE / "source-contract" / "original" / filename))), 0)

    def test_core_is_bounded_lossless_complete_and_ordered(self):
        self.assertEqual(len(self.chain["segments"]), 114)
        accumulated = {r["source"]: bytearray() for r in self.chain["sources"]}
        for number, segment in enumerate(self.chain["segments"], 1):
            raw = frozen(segment["path"], segment["sha256"])
            self.assertLess(len(raw), 16000)
            self.assertEqual(segment["index"], number)
            self.assertEqual(segment["bytes"], len(raw))
            lines = raw.splitlines(keepends=True)
            for part in segment["parts"]:
                actual = b"".join(lines[part["segmentStart"] - 1:part["segmentEnd"]])
                expected = frozen(PACKET / part["source"], part["sha256"]).splitlines(keepends=True)
                self.assertEqual(actual, b"".join(expected[part["a"] - 1:part["b"]]))
                accumulated[part["source"]].extend(actual)
            if number < len(self.chain["segments"]):
                self.assertTrue(raw.endswith(
                    ("NEXT SEGMENT: " + self.chain["segments"][number]["path"] + "\n").encode("utf-8")))
            else:
                self.assertTrue(raw.endswith(b"END OF CHAIN. Follow the run instruction's phase boundary.\n"))
        for source in self.chain["sources"]:
            self.assertEqual(source["selectedLines"], source["sourceLines"])
            self.assertEqual(bytes(accumulated[source["source"]]), frozen(PACKET / source["source"]))
        sources = list(accumulated)
        self.assertEqual(sources[0], "REVIEW.md")
        for name in ("font-cmap.json", "xml-presentation.json", "baseline-title-index.txt", "title-index.txt",
                     "kanjidic2-records.xml", "jmdict-families.xml"):
            self.assertIn("evidence/" + name, sources)
        self.assertEqual(len([s for s in sources if s.endswith("-extract.txt")]), 6)
        packet = json.loads(frozen(PACKET / "packet.json"))
        for name in packet["modifiedExisting"]:
            self.assertIn("baseline/" + name, sources)
            self.assertIn("snapshot/" + name, sources)

    def test_full_baseline_and_candidate_title_coverage(self):
        for filename, count in (("baseline-title-index.txt", 1254), ("title-index.txt", 1257)):
            lines = frozen(PACKET / "evidence" / filename).decode("utf-8").splitlines()
            chars = [line[0] for line in lines]
            self.assertEqual(len(chars), count)
            self.assertEqual(chars, sorted(set(chars), key=ord))
            self.assertTrue(all(f"repo/kanji/{c}.md" in self.sums for c in chars))
        baseline = {line[0] for line in frozen(PACKET / "evidence" / "baseline-title-index.txt").decode().splitlines()}
        candidate = {line[0] for line in frozen(PACKET / "evidence" / "title-index.txt").decode().splitlines()}
        self.assertEqual(candidate - baseline, set(MEMBERS))

    def test_prompts_differ_only_in_identity_and_pin_all_runtime_files(self):
        prompts = []
        for key in ("claude", "gpt"):
            spec = self.preflight["runs"][key]
            raw = frozen(spec["prompt"], spec["promptSha256"])
            prompts.append(raw)
            audit = json.loads(frozen(spec["auditConfig"]))
            for binding in audit["files"]:
                frozen(binding["path"], binding["sha256"])
            self.assertEqual(audit["maxWebFetches"], 0)
            self.assertEqual(audit["completionContract"], "entire-message-enum-v1")
            self.assertEqual(audit["reportStructureContract"], "report-structure-v1")
            self.assertFalse(Path(spec["report"]).exists())
            text = raw.decode("utf-8")
            for required in ("PHASE-1 SEND GATE", "114", "1254 baseline", "Missing entries: none",
                             "one LF or CRLF", "do not read this file again"):
                self.assertIn(required, text)
            self.assertIn("content-format.md in full", text)
            self.assertNotIn("5c000bd", text)
        self.assertEqual(prompts[0].replace(b"CLAUDE", b"GPT").replace(b"-claude-", b"-gpt-"), prompts[1])
        self.assertEqual(self.preflight["packetManifestSha256"], self.packet_sha)

    def test_packet_excludes_author_analysis_and_selected_answers(self):
        forbidden = ("adjudicat", "source-analysis", "pair-disposition", "scan", "review-report", "phase1-list")
        self.assertFalse(any(any(term in name.lower() for term in forbidden) for name in self.sums))
        packet = json.loads(frozen(PACKET / "packet.json"))
        self.assertEqual(packet["wordProseChanges"], [])
        self.assertEqual(packet["linkWrappers"], 4)
        self.assertEqual(packet["sourceRows"], [977, 870, 1174])
        for name in self.sums:
            if name.endswith((".txt", ".json", ".md")):
                raw = frozen(PACKET / name)
                self.assertNotIn(b"batch-130-", raw)
                self.assertNotIn(b"scratch-130", raw)
                self.assertNotIn(b"N1-B130", raw)

    def test_selection_rejects_duplicates_curated_targets_and_bad_shapes(self):
        ref = json.loads(frozen(PACKET / "eligibility-reference.json"))
        self.assertTrue(review_chain.validate_selection("D: none\nE: none", ref)["valid"])
        forbidden_d = ref["cards"][0]["distractors"][0]
        self.assertFalse(review_chain.validate_selection(f"D1 {forbidden_d} - {MEMBERS[0]}: fixture\nE: none", ref)["valid"])
        guard = ref["cards"][0]["quiz_exclusions"][0]
        self.assertFalse(review_chain.validate_selection(
            f"D1 {guard} - {MEMBERS[0]}: fixture\nE: none", ref)["valid"])
        self.assertFalse(review_chain.validate_selection(
            f"D: none\nE1 {guard} - fixture\nE2 {guard} - fixture", ref)["valid"])

    def test_two_phase_extension_exact_message_missing_verbatim_and_no_hints(self):
        chain_builder = module("b131_extension_fixture_builder", TOOLS / "prepare_chain_b131_001.py")
        with tempfile.TemporaryDirectory() as temp:
            records = Path(temp)
            chain_builder.review_dir = lambda batch: records
            run = "B131-FIXTURE-NOT-A-REVIEW"
            directory = records / run / "audit-fixture"
            directory.mkdir(parents=True)
            ref = json.loads(frozen(PACKET / "eligibility-reference.json"))
            excluded = set(MEMBERS) | {c for row in ref["cards"] for field in ("distractors", "quiz_exclusions")
                                       for c in row[field]}
            char = next(Path(name).stem for name in self.sums if name.startswith("repo/kanji/")
                        and Path(name).stem not in excluded)
            missing = next(chr(code) for code in range(0x9fff, 0x4e00, -1)
                           if chr(code) not in excluded and f"repo/kanji/{chr(code)}.md" not in self.sums)
            reply = (f"D1 {char} - {MEMBERS[0]}: synthetic fixture\n"
                     f"D2 {missing} - {MEMBERS[1]}: synthetic missing fixture\nE: none")
            reply_binding = write_frozen(directory / "phase1-list.txt", reply.encode("utf-8"))
            audit = freeze_json(directory / "audit.json", {
                "session": "synthetic-only", "status": "PHASE1_READY", "breaches": [],
                "phase1ListSha256": reply_binding["sha256"]})
            with redirect_stdout(io.StringIO()):
                chain_builder.main(["131", "--run", run, "--reply", reply_binding["path"],
                                    "--phase1-audit", audit["path"]])
            extension = json.loads(frozen(records / f"{run}-extension.json"))
            self.assertEqual(len(extension["sources"]), 1)
            self.assertEqual(extension["sources"][0]["source"], f"repo/kanji/{char}.md [D1]")
            message = frozen(records / f"{run}-phase2-message.txt").decode("utf-8")
            self.assertEqual(message, extension["segments"][0]["path"] + "\nMissing entries:\n"
                             + f"D2 {missing} - {MEMBERS[1]}: synthetic missing fixture")
            for path in records.rglob("*"):
                if path.is_file():
                    path.chmod(stat.S_IREAD | stat.S_IWRITE)

    def test_admission_full_canonical_roster_and_refusals(self):
        now = datetime.now(timezone.utc)
        rows = [{"id": COORDINATOR, "name": "Coordinator", "activity": {"status": "busy"}},
                {"id": "fixture-idle", "name": "Unrelated", "activity": {"status": "idle"}}]
        status = {"summary": {"total": 2}, "sessions": rows}
        roster = [{"id": row["id"]} for row in rows]
        self.assertEqual(validate_roster(status, roster, "Fresh reviewer", now, now), 2)
        cases = []
        unknown = copy.deepcopy(status)
        unknown["sessions"][1]["activity"]["status"] = "unknown"
        cases.append((unknown, roster, now))
        busy = copy.deepcopy(status)
        busy["sessions"][1]["activity"]["status"] = "busy"
        cases.append((busy, roster, now))
        cases.extend([(status, roster[:1], now), (status, [roster[0], roster[0]], now),
                      (status, roster, now - timedelta(seconds=121)),
                      (status, roster, now + timedelta(seconds=1))])
        duplicate = copy.deepcopy(status)
        duplicate["sessions"][1]["name"] = "Fresh reviewer"
        cases.append((duplicate, roster, now))
        for candidate, listed, observed in cases:
            with self.assertRaises((ValueError, KeyError)):
                validate_roster(candidate, listed, "Fresh reviewer", now, observed)

    def test_context_compaction_and_standard_tier_are_refused(self):
        checker = module("b131_context_fixture_checker", HERE / "check-run-context.py")
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "events.jsonl"
            events = [{"type": "session.start", "data": {"contextTier": "long_context"}},
                      {"type": "session.usage_record", "data": {"usage": {"maxPromptTokens": 952000}}}]
            def check():
                path.write_text("".join(json.dumps(e) + "\n" for e in events), encoding="utf-8")
                return checker.check(path)
            self.assertEqual(check()["status"], "PASS")
            events.append({"type": "session.compaction_start", "data": {}})
            self.assertEqual(check()["status"], "FAIL")
            events.pop()
            events[0]["data"]["contextTier"] = "default"
            self.assertEqual(check()["status"], "FAIL")


def main():
    output = HERE / "validation-002"
    require(not output.exists(), "Preserve focused validation")
    output.mkdir()
    temporary = output / "fixture-temporary"
    temporary.mkdir()
    tempfile.tempdir = str(temporary)
    guard, _ = start_guard("B131 focused preparation validation")
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(PreparationTests)
    for name in ("test-review-chain-controls-002.py", "test-report-structure.py", "test-review-audit-controls-002.py"):
        loaded = module("b131_" + name.replace("-", "_").replace(".", "_"), HERE / name)
        suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(loaded))
    try:
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        guard.check()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Validation RAM breach")
    frozen_result = freeze_json(output / "result.json", {
        "status": "PASS" if result.wasSuccessful() else "FAIL", "batch": 131,
        "candidate": CANDIDATE, "testsRun": result.testsRun,
        "failures": [(str(test), error) for test, error in result.failures],
        "errors": [(str(test), error) for test, error in result.errors],
        "memory": memory, "fixtures": "Synthetic-only events/extension; no real reviewer launched.",
        "packetManifestSha256": sha(frozen(PACKET / "SHA256SUMS.json")),
        "producerSha256": sha(frozen(Path(__file__)))})
    print(json.dumps(frozen_result))
    require(result.wasSuccessful(), "Focused preparation validation failed")
    temporary.rmdir()


if __name__ == "__main__":
    main()

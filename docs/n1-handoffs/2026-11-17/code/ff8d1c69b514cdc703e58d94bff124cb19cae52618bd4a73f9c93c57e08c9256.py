"""Bind B129's signed packet, finite comparisons, sources, fonts and executed gates."""
import itertools
import json
import sys
import unicodedata
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

from common import GUARD_SHA, WS, freeze_json, frozen, load_module, require, sha, start_guard, write_frozen
from verify_b129_payload import BASE, HERE, MEMBERS, PREFIX, REPO, RUNNER, LINK_HELPER, LINK_HELPER_SHA
from verify_b129_sources import Git
from source_query_union import selects

ORDER = ("lint", "quiz-safety", "linkplan", "reading-exposure", "validate",
         "manifest", "unittest", "budget", "vocabulary", "manifest-rebuild")
SCRATCH = HERE.parent


def verify_query_map(raw, selection, recorded):
    prefixes = {"contains-keb": "contains", "exact-keb": "exact-spelling", "exact-reb": "exact-reading"}
    queries = selection["queries"] if selection["mode"] == "union" else [
        "exact-keb:" + query for query in selection["queries"]]
    actual = {}
    for node in ET.fromstring(raw).findall("entry"):
        identity = node.findtext("ent_seq")
        require(identity not in actual, "Duplicate query-map entry")
        matches = []
        for query in queries:
            if selects(node, "entry", identity, "union", [query]):
                kind, value = query.split(":", 1)
                matches.append(prefixes[kind] + ":" + value)
        require(matches, f"Record matches no declared query: {identity}")
        actual[identity] = set(matches)
    require(all(len(value) == len(set(value)) for value in recorded.values())
            and actual == {key: set(value) for key, value in recorded.items()},
            "Recorded query membership omits or invents a matching predicate")


def verify_summary(summary, mode, candidate, manifest_sha, runner_sha, common_sha):
    require(summary["batch"] == "129" and summary["status"] == "PASS"
            and summary["mode"] == mode and summary["base"] == BASE
            and summary["startingHead"] == (BASE if mode == "author" else candidate)
            and summary["checks"] == list(ORDER) and summary["serial"] is True
            and summary["manifestSha256"] == manifest_sha
            and summary["runnerSha256"] == runner_sha and summary["commonHelperSha256"] == common_sha
            and summary["guardSha256"] == GUARD_SHA and summary["waitTimeoutSeconds"] == 0.1
            and summary["cleanupTimeoutSecondsPerStage"] == 10 and not summary["finalMemory"]["breach"],
            "Gate summary is not bound to the expected snapshot or bounded execution")


def verify_execution(receipts, commands, common_sha):
    previous = None
    for name in ORDER:
        item = receipts[name]
        start, end = (datetime.fromisoformat(item[key]) for key in ("startedAt", "completedAt"))
        require(start.tzinfo is not None and end.tzinfo is not None and end >= start
                and (previous is None or start >= previous), "Gate execution is not serial")
        require(item["command"] == [sys.executable, "-B", *map(str, commands[name])]
                and item["commonHelperSha256"] == common_sha
                and item["cleanupTimeoutSecondsPerStage"] == 10
                and item["activeError"] is None and item["cleanupError"] is None,
                f"Gate command/helper/cleanup differs: {name}")
        previous = end


def verify_pair_member(item, card, scan, comparison_cards):
    char = item["kanji"]
    pairs = item["pairs"]
    others = [row["pair"][1] for row in pairs]
    require(item["targetTitle"] == card["title"] and len(set(others)) == len(others)
            and all(row["pair"][0] == char for row in pairs), "Pair membership/title differs")
    require(set(scan["matches"]) <= set(others)
            and {row["pair"][1] for row in pairs if row["decision"] == "guard"} == set(card["quiz_exclusions"])
            and {row["pair"][1] for row in pairs if row["decision"] == "curated"} == set(card["distractors"]),
            "Pair coverage or direct exclusions differ")
    for row in pairs:
        other = row["pair"][1]
        title, digest = comparison_cards[other]
        require(row["decision"] in {"guard", "curated", "distinct", "rejected"}
                and row["comparisonTitle"] == title and row["baselineCardSha256"] == digest
                and row["scanMatch"] is (other in scan["matches"])
                and row["targetLabelOnComparison"] and row["comparisonLabelOnTarget"],
                f"Pair snapshot or direction differs: {char}/{other}")


def main(source_path, source_sha, payload_path, payload_sha, gates_name, preservation_name, output_name):
    for name in (gates_name, preservation_name, output_name):
        require(Path(name).name == name and name not in {"", ".", ".."}, "Direct directory names required")
    output = HERE / output_name
    require(not output.exists(), "Preserve existing evidence verification")
    source_raw, payload_raw = frozen(source_path, source_sha), frozen(payload_path, payload_sha)
    source_proof, payload = json.loads(source_raw), json.loads(payload_raw)
    candidate = payload["candidate"]
    require(source_proof["candidate"] == candidate and source_proof["base"] == payload["base"] == BASE
            and source_proof["batch"] == payload["batch"] == 129
            and source_proof["status"] == payload["status"] == "PASS"
            and payload["sourceProof"]["sha256"] == source_sha
            and not source_proof["memory"]["breach"] and not payload["memory"]["breach"],
            "Source and payload proofs do not bind the same candidate")
    frozen(Path(__file__).with_name("verify_b129_sources.py"), source_proof["verifierSha256"])
    frozen(Path(__file__).with_name("verify_b129_payload.py"), payload["verifierSha256"])
    frozen(LINK_HELPER, LINK_HELPER_SHA)
    helper = load_module("b129_evidence_helpers", LINK_HELPER)
    guard, _ = start_guard("B129 signed evidence verification")
    git = Git(REPO, RUNNER, guard)
    captures, signed = {}, {}

    def blob(name):
        return git("show", f"{candidate}:{name}")

    def source(name):
        raw = blob(PREFIX + name)
        signed[PREFIX + name] = sha(raw)
        return raw

    def clean():
        require(git("rev-parse", "HEAD").decode().strip() == candidate
                and not git("status", "--porcelain=v1", "--untracked-files=all"), "Candidate changed")

    try:
        clean()
        inventory = json.loads(source("evidence-inventory.json"))
        paths = {name.removeprefix(PREFIX) for name in
                 git("ls-tree", "-r", "--name-only", candidate, "--", PREFIX).decode().splitlines()}
        require(inventory["selfExcluded"] is True
                and paths == set(inventory["files"]) | {"evidence-inventory.json"}, "Packet inventory incomplete")
        for name, digest in inventory["files"].items():
            require(not Path(name).is_absolute() and ".." not in Path(name).parts
                    and sha(source(name)) == digest, f"Packet bytes differ: {name}")
            guard.check()
        for record in source_proof["sourceRecords"]:
            require(sha(blob(record["path"])) == record["sha256"], "Verified dictionary output changed")
        jm = helper.merge_records([blob(record["path"]) for record in source_proof["sourceRecords"]
                                   if record["input"] == "n1-implementation-JMdict_e.gz"], "entry", "ent_seq")
        kd = helper.merge_records([blob(record["path"]) for record in source_proof["sourceRecords"]
                                   if record["input"] == "n1-planning-kanjidic2.xml.gz"], "character", "literal")
        require(len(jm) == 252 and set(kd) == set(MEMBERS) | set(source_proof["packetComparisonCards"]),
                "Complete source union differs")
        facts = json.loads(frozen(source_proof["facts"]["path"], source_proof["facts"]["sha256"]))
        query_maps = ("query-membership.json", "supplement-query-membership-002.json",
                      "final-query-membership.json", "additional-query-membership.json")
        require(len(facts["jmdictSelections"]) == len(query_maps), "JMdict query selection count differs")
        for selection, mapping in zip(facts["jmdictSelections"], query_maps):
            verify_query_map(source(selection["file"]), selection, json.loads(source(mapping)))
        for receipt_name in ("source-receipt.json", "supplement-receipt-002.json",
                             "final-source-receipt.json", "additional-source-receipt.json"):
            receipt = json.loads(source(receipt_name))
            inputs = receipt.get("dictionaryInputs", receipt.get("inputs"))
            if inputs is None:
                inputs = {"jmdict": receipt["input"]}
            for kind, binding in inputs.items():
                expected = source_proof["inputs"][kind]
                require(binding["filename"] == expected["filename"]
                        and binding["compressedSha256"] == expected["compressedSha256"]
                        and binding["decompressedSha256"] == expected["decompressedXmlSha256"],
                        "Signed receipt does not bind the verified original dictionary")
            outputs = receipt.get("outputs")
            if outputs is None:
                outputs = {receipt["output"]["filename"]: receipt["output"]}
            for name, binding in outputs.items():
                raw = source(name)
                canonical = {node.findtext("ent_seq") or node.findtext("literal"):
                             sha(ET.canonicalize(ET.tostring(node, encoding="unicode"),
                                                 strip_text=True).encode())
                             for node in ET.fromstring(raw)}
                require(sha(raw) == binding["sha256"] and len(raw) == binding["bytes"]
                        and canonical == binding["canonicalRecordHashes"],
                        f"Source receipt output differs: {name}")
        sys.path.insert(0, str(WS / "lean"))
        from n1lib import parse
        comparisons = {}
        for char in source_proof["packetComparisonCards"]:
            raw = source(f"comparison-cards/{char}.md")
            metadata, _ = parse(raw.decode().replace("\r\n", "\n"))
            comparisons[char] = metadata["title"], sha(raw)
        disposition = json.loads(source("pair-dispositions.json"))
        require(disposition["base"] == BASE, "Pair base differs")
        pair_members = [item for item in disposition["members"] if "kanji" in item]
        require([item["kanji"] for item in pair_members] == MEMBERS, "Pair members differ")
        for item, member in zip(pair_members, payload["members"]):
            char = item["kanji"]
            scan_raw = source(f"scans-004/{char}.json")
            scan = json.loads(scan_raw)
            require(item["scanFile"] == f"scans-004/{char}.json"
                    and item["scanSha256"] == sha(scan_raw) and item["scanRows"] == 1248,
                    "Pair scan binding differs")
            verify_pair_member(item, member["metadata"], scan, comparisons)
        new_pairs = [item for item in disposition["members"] if "newMemberPair" in item]
        require([item["newMemberPair"] for item in new_pairs] == [list(p) for p in itertools.combinations(MEMBERS, 2)]
                and all(item["decision"] == "distinct" and item["bothDirections"] for item in new_pairs),
                "New/new pair coverage differs")
        progress = json.loads(blob("docs/n1-sources/batch-129-progress.json"))
        require(progress["base"] == BASE and progress["status"] == "local-authoring-candidate"
                and progress["deliveredSourceMembers"] == 258 and progress["undeliveredSourceMembers"] == 970
                and progress["localDraftsNotDelivered"] == 3 and progress["newWordArticles"] == 0
                and progress["wordProseExceptions"] == [], "Premature publication or changed scope")
        external = json.loads(source("external-source-bindings.json"))
        require(len(external["captures"]) == 7, "External capture inventory differs")
        for item in external["captures"]:
            raw_path, text_path = Path(item["localRawCapture"]), Path(item["localTextCapture"])
            require(raw_path.parent == text_path.parent == SCRATCH / "external-pages"
                    and raw_path.with_suffix(".txt") == text_path, "External capture path differs")
            raw, text = raw_path.read_bytes(), text_path.read_bytes()
            require(sha(raw) == item["rawSha256"] and len(raw) == item["rawBytes"]
                    and sha(text) == item["textSha256"], "External capture bytes differ")
            captures["external-pages/" + raw_path.name] = raw
            captures["external-pages/" + text_path.name] = text
        font_record = json.loads(source("stroke-font-evidence.json"))
        points = font_record["codePoints"]
        require(all(item["codePoint"] == f"U+{ord(item['character']):04X}"
                    and item["unicodeName"] == unicodedata.name(item["character"]) for item in points),
                "Component code points differ")
        from fontTools.ttLib import TTFont
        font_results = []
        for item in font_record["fonts"]:
            require(item["filename"] in {"kanji_brush.ttf", "kanji_mincho.ttf", "kanji_textbook.ttf"},
                    "Unexpected bundled font")
            path = WS / "kanji-cards-android" / "app" / "src" / "main" / "res" / "font" / item["filename"]
            require(sha(path.read_bytes()) == item["sha256"] and path.stat().st_size == item["bytes"],
                    "Bundled font bytes differ")
            with TTFont(path) as font:
                cmap = font.getBestCmap()
                coverage = {point["codePoint"]: ord(point["character"]) in cmap for point in points}
            require(coverage == item["coverage"], "Bundled font cmap differs")
            font_results.append(item)
            guard.check()
        require(len({item["filename"] for item in font_results}) == 3, "Missing font")
        lean = WS / "lean"
        commands = {
            "lint": [lean / "n1_batch_tool.py", "lint", "--base", BASE, "--no-jmdict", *MEMBERS],
            "quiz-safety": [lean / "quiz_safety.py", *MEMBERS],
            "linkplan": [lean / "n1_linkplan.py", "verify", BASE, *MEMBERS],
            "reading-exposure": [SCRATCH / "check_reading_b129.py"],
            "validate": [REPO / "tools" / "validate.py"], "manifest": [REPO / "tools" / "build_manifest.py"],
            "unittest": ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"],
            "budget": [REPO / "tools" / "check_content_budget.py"],
            "vocabulary": [REPO / "tools" / "grammar_vocabulary.py", "check"],
            "manifest-rebuild": [REPO / "tools" / "build_manifest.py"],
        }
        for name in ("run_b129_gates.py", "b129_common.py", "check_reading_b129.py", "preserve_b129.py"):
            require((SCRATCH / name).read_bytes() == source("producers/" + name), "Executed producer differs")
        runner_sha = signed[PREFIX + "producers/run_b129_gates.py"]
        common_sha = signed[PREFIX + "producers/b129_common.py"]
        config = {"repo": str(REPO)}
        gate_groups = {}
        for mode, name in (("author", "author-gates-002"), ("committed", gates_name)):
            directory = SCRATCH / name
            summary_raw = (directory / "summary.json").read_bytes()
            summary = json.loads(summary_raw)
            verify_summary(summary, mode, candidate, payload["manifestSha256"], runner_sha, common_sha)
            bindings = helper.gate_bindings(directory, config, payload["manifestSha256"], runner_sha, guard)
            receipts = {}
            for binding in bindings:
                gate = binding["gate"]
                for suffix, key in (("json", "receiptSha256"), ("log", "logSha256")):
                    filename = f"{gate}.{suffix}"
                    raw = (directory / filename).read_bytes()
                    require(sha(raw) == summary["logs"][gate][key], "Gate summary binding differs")
                    if mode == "author":
                        require(raw == source(f"author-evidence/{name}/{filename}"), "Signed gate differs")
                    captures[f"{mode}/{filename}"] = raw
                receipts[gate] = json.loads(captures[f"{mode}/{gate}.json"])
            verify_execution(receipts, commands, common_sha)
            if mode == "author":
                require(summary_raw == source(f"author-evidence/{name}/summary.json"), "Signed summary differs")
            captures[f"{mode}/summary.json"] = summary_raw
            gate_groups[mode] = {"summarySha256": sha(summary_raw), "sourceDirectory": str(directory),
                                 "gates": bindings}
        preservation = json.loads((SCRATCH / preservation_name / "summary.json").read_bytes())
        require(preservation["status"] == "PASS" and preservation["mode"] == "committed"
                and preservation["base"] == BASE and preservation["head"] == candidate
                and preservation["manifestSha256"] == payload["manifestSha256"]
                and preservation["evidenceInventorySha256"] == signed[PREFIX + "evidence-inventory.json"]
                and preservation["producerSha256"] == signed[PREFIX + "producers/preserve_b129.py"]
                and not preservation["memory"]["breach"], "Preservation receipt differs")
        for name in ("summary.json", "memory.json", "runtime-hashes.json"):
            captures["preservation/" + name] = (SCRATCH / preservation_name / name).read_bytes()
        clean()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Evidence verification RAM breach")
    captured = {name: write_frozen(output / name, raw) for name, raw in captures.items()}
    print(json.dumps(freeze_json(output / "verification.json", {
        "batch": 129, "base": BASE, "candidate": candidate, "status": "PASS",
        "sourceProof": {"path": source_path, "sha256": source_sha},
        "payloadProof": {"path": payload_path, "sha256": payload_sha},
        "signedInputs": signed, "capturedInputs": captured, "gates": gate_groups,
        "completeJmdictFamilies": len(jm), "completeKanjidicRecords": len(kd),
        "finiteBaselinePairs": sum(len(item["pairs"]) for item in pair_members),
        "finiteNewPairs": len(new_pairs), "bundledFontEvidence": font_results,
        "memory": memory, "verifierSha256": sha(Path(__file__).read_bytes()),
        "limits": "Mechanical binding only. Pair judgments, original-source predicates, "
                  "reading-pool limitations and rendered/native/device acceptance are not "
                  "established by hash equality. Independent reviews and publication remain open.",
    })))


if __name__ == "__main__":
    require(len(sys.argv) == 8, "Usage: verify_b129_evidence.py SOURCE_PROOF SHA PAYLOAD_PROOF SHA "
            "COMMITTED_GATES PRESERVATION NEW_OUTPUT_DIRECTORY")
    main(*sys.argv[1:])

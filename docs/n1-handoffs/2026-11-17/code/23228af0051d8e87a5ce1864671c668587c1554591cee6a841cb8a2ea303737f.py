"""Bind B130's signed packet, finite comparisons, sources, fonts and executed gates.

Derived from verify_b129_evidence_v4.py. Handoff-specific filenames are read from a frozen
facts file prepared after inspecting the signed candidate, rather than guessed beforehand.
"""
import ast
import itertools
import json
import sys
import unicodedata
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path, PurePosixPath

from common import GUARD_SHA, WS, freeze_json, frozen, load_module, require, sha, start_guard, write_frozen
from verify_b130_payload import BASE, HERE, MEMBERS, PREFIX, REPO, RUNNER, LINK_HELPER, LINK_HELPER_SHA
from verify_b130_sources import Git
from source_query_union import selects
from b130_signed_evidence import (FINAL_VERIFIER_SHA, RESIDUAL, receipt_outputs,
                                  verify_final_proof, verify_progress)
SIGNED_HELPER_SHA = "4b5e6ca8d73f16267e888ec512f9fc6839fcb82b563c45218fb71e7ef45a35ba"

ORDER = ("lint", "quiz-safety", "linkplan", "reading-exposure", "validate",
         "manifest", "unittest", "budget", "vocabulary", "manifest-rebuild")
SCRATCH = HERE.parent
DECISIONS = {"guard", "curated", "distinct", "rejected"}
INPUT_KEYS = ("dictionaryInputs", "inputs", "originalInputs")
FONTS = {"kanji_brush.ttf", "kanji_mincho.ttf", "kanji_textbook.ttf"}
FACT_KEYS = {
    "batch", "candidate", "sourceProof", "payloadProof", "inventory", "supersededInventories",
    "queryMaps", "receipts", "expectedJmdictFamilies", "pairDispositions", "scanDirectories",
    "scanRows", "externalBindings", "fontEvidence", "producers", "commonHelper", "readingCheck",
    "requiredReadingKeys", "linkplanArgs", "wordProseExceptions", "summaryBatch", "gates",
    "preservation", "output", "finalSourceProof", "readingKeys",
}


def direct(name):
    return isinstance(name, str) and Path(name).name == name and name not in {"", ".", ".."}


def relative(name):
    path = PurePosixPath(name)
    return (isinstance(name, str) and name and "\\" not in name and not path.is_absolute()
            and ".." not in path.parts and "." not in path.parts)


def check_facts(facts):
    require(set(facts) == FACT_KEYS and facts["batch"] == 130, "Unexpected evidence facts")
    gates = facts["gates"]
    require(set(gates) == {"author", "committed"}
            and all(set(gates[mode]) == {"directory", "runner", "signedCopy"} for mode in gates)
            and gates["committed"]["signedCopy"] is None, "Gate facts differ")
    require(set(facts["preservation"]) == {"directory", "producer"}, "Preservation facts differ")
    directories = [facts["output"], facts["preservation"]["directory"],
                   *(gates[mode]["directory"] for mode in gates)]
    require(all(map(direct, directories)) and len(set(directories)) == len(directories),
            "Distinct direct scratch directory names required")
    producers = facts["producers"]
    require(all(map(direct, producers)) and len(set(producers)) == len(producers)
            and {facts["commonHelper"], facts["readingCheck"], facts["preservation"]["producer"],
                 *(gates[mode]["runner"] for mode in gates), *facts["receipts"].values()} <= set(producers),
            "Executed tools must be declared signed producers")
    names = [facts["inventory"], *facts["supersededInventories"], *facts["queryMaps"],
             *facts["queryMaps"].values(), *facts["receipts"], facts["pairDispositions"],
             *facts["scanDirectories"], *facts["externalBindings"], facts["fontEvidence"],
             facts["readingKeys"]]
    signed_copy = gates["author"]["signedCopy"]
    require(all(map(relative, names)) and (signed_copy is None or relative(signed_copy)),
            "Packet names must be safe relative paths")
    require(facts["inventory"] not in facts["supersededInventories"] and facts["scanDirectories"]
            and isinstance(facts["scanRows"], int) and isinstance(facts["expectedJmdictFamilies"], int)
            and all(isinstance(count, int) and count > 0 for count in facts["externalBindings"].values()),
            "Inventory, scan or capture expectations differ")
    require(all(char in MEMBERS and keys and len(keys) == len(set(keys))
                for char, keys in facts["requiredReadingKeys"].items()), "Required reading keys differ")
    linkplan_tail(facts["linkplanArgs"], facts["wordProseExceptions"])


def linkplan_tail(args, exceptions):
    count = len(MEMBERS)
    require(args[:2] == ["verify", BASE] and args[-count:] == MEMBERS, "Linkplan scope differs")
    middle = args[2:-count]
    remarks = REPO / "docs" / "n1-sources" / "batch-130"
    require((middle == [] and exceptions == [])
            or (len(middle) == 2 and middle[0] == "--remarks"
                and Path(middle[1]).parent == remarks and exceptions),
            "Linkplan remarks and declared prose exceptions differ")
    return args


def gate_commands(facts):
    lean = WS / "lean"
    return {
        "lint": [lean / "n1_batch_tool.py", "lint", "--base", BASE, "--no-jmdict", *MEMBERS],
        "quiz-safety": [lean / "quiz_safety.py", *MEMBERS],
        "linkplan": [lean / "n1_linkplan.py",
                     *linkplan_tail(facts["linkplanArgs"], facts["wordProseExceptions"])],
        "reading-exposure": [SCRATCH / facts["readingCheck"]],
        "validate": [REPO / "tools" / "validate.py"], "manifest": [REPO / "tools" / "build_manifest.py"],
        "unittest": ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"],
        "budget": [REPO / "tools" / "check_content_budget.py"],
        "vocabulary": [REPO / "tools" / "grammar_vocabulary.py", "check"],
        "manifest-rebuild": [REPO / "tools" / "build_manifest.py"],
    }


def verify_query_map(raw, selection, recorded):
    prefixes = {"contains-keb": "contains", "exact-keb": "exact-spelling", "exact-reb": "exact-reading"}
    require(selection["mode"] in {"union", "exact"}, "Unsupported JMdict selection mode")
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


def receipt_inputs(receipt):
    present = [key for key in INPUT_KEYS if key in receipt]
    require(len(present) == 1, "Receipt must bind exactly one dictionary-input set")
    return receipt[present[0]]


def verify_summary(summary, mode, candidate, manifest_sha, runner_sha, common_sha, batch):
    require(summary["batch"] == batch and summary["status"] == "PASS"
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


def new_pair_sets(items):
    require([item["newMemberPair"] for item in items] == [list(p) for p in itertools.combinations(MEMBERS, 2)]
            and all(item["decision"] in DECISIONS and isinstance(item["bothDirections"], str) and item["bothDirections"].strip() for item in items),
            "New/new pair coverage differs")
    guards, curated = ({char: set() for char in MEMBERS} for _ in range(2))
    for item in items:
        first, second = item["newMemberPair"]
        target = {"guard": guards, "curated": curated}.get(item["decision"])
        if target is not None:
            target[first].add(second)
            target[second].add(first)
    return guards, curated


def verify_pair_member(item, card, scans, comparison_cards, new_guards, new_curated):
    char = item["kanji"]
    pairs = item["pairs"]
    others = [row["pair"][1] for row in pairs]
    require(item["targetTitle"] == card["title"] and len(set(others)) == len(others)
            and all(row["pair"][0] == char and row["pair"][1] not in MEMBERS for row in pairs),
            "Pair membership/title differs")
    matched = set().union(*(scan["matches"] for scan in scans))
    final = set(scans[-1]["matches"])
    require(matched <= set(others)
            and {row["pair"][1] for row in pairs if row["decision"] == "guard"} | new_guards
            == set(card.get("quiz_exclusions", []))
            and {row["pair"][1] for row in pairs if row["decision"] == "curated"} | new_curated
            == set(card.get("distractors", [])),
            "Pair coverage or direct exclusions differ")
    for row in pairs:
        other = row["pair"][1]
        require(other in comparison_cards, f"Pair lacks a packet comparison snapshot: {char}/{other}")
        title, digest = comparison_cards[other]
        require(row["decision"] in DECISIONS
                and row["comparisonTitle"] == title and row["baselineCardSha256"] == digest
                and row["scanMatch"] is (other in final)
                and row["targetLabelOnComparison"] and row["comparisonLabelOnTarget"],
                f"Pair snapshot or direction differs: {char}/{other}")


from b130_signed_evidence import verify_reading_keys


def verify_excerpt(text_raw, excerpt):
    strip = lambda value: "".join(value.split())
    require(strip(excerpt) in strip(text_raw.decode("utf-8")), "Committed excerpt is absent from capture")


def load_facts(path, digest):
    path = Path(path).resolve()
    require(path.parent == HERE, "Evidence facts must be frozen in B130 review")
    raw = frozen(path, digest)
    facts = json.loads(raw)
    check_facts(facts)
    return facts, raw


def main(facts_path, facts_sha):
    facts, facts_raw = load_facts(facts_path, facts_sha)
    frozen(Path(__file__).with_name("b130_signed_evidence.py"), SIGNED_HELPER_SHA)
    output = HERE / facts["output"]
    require(not output.exists(), "Preserve existing evidence verification")
    source_path, source_sha = facts["sourceProof"]["path"], facts["sourceProof"]["sha256"]
    payload_path, payload_sha = facts["payloadProof"]["path"], facts["payloadProof"]["sha256"]
    require(Path(source_path).resolve().parent == Path(payload_path).resolve().parent == HERE,
            "Proofs must be frozen in B130 review")
    source_proof = json.loads(frozen(source_path, source_sha))
    payload = json.loads(frozen(payload_path, payload_sha))
    candidate = payload["candidate"]
    require(candidate == facts["candidate"] == source_proof["candidate"]
            and source_proof["base"] == payload["base"] == BASE
            and source_proof["batch"] == payload["batch"] == 130
            and source_proof["status"] == payload["status"] == "PASS"
            and payload["sourceProof"]["sha256"] == source_sha
            and not source_proof["memory"]["breach"] and not payload["memory"]["breach"],
            "Source and payload proofs do not bind the same candidate")
    final_path, final_sha = facts["finalSourceProof"]["path"], facts["finalSourceProof"]["sha256"]
    require(Path(final_path).resolve().parent == HERE, "Final proof must be frozen in B130 review")
    final_proof = json.loads(frozen(final_path, final_sha))
    verify_final_proof(final_proof, source_sha, candidate)
    frozen(Path(__file__).with_name("verify_b130_final_sources.py"), FINAL_VERIFIER_SHA)
    frozen(Path(__file__).with_name("verify_b130_sources.py"), source_proof["verifierSha256"])
    frozen(Path(__file__).with_name("verify_b130_payload.py"), payload["verifierSha256"])
    frozen(LINK_HELPER, LINK_HELPER_SHA)
    helper = load_module("b130_evidence_helpers", LINK_HELPER)
    commands = gate_commands(facts)
    guard, _ = start_guard("B130 signed evidence verification")
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
        inventory = json.loads(source(facts["inventory"]))
        paths = {name.removeprefix(PREFIX) for name in
                 git("ls-tree", "-r", "--name-only", candidate, "--", PREFIX).decode().splitlines()}
        require(inventory["selfExcluded"] is True
                and paths == set(inventory["files"]) | {facts["inventory"]}, "Packet inventory incomplete")
        for name in facts["supersededInventories"]:
            previous = json.loads(source(name))
            require(name in inventory["files"] and previous["selfExcluded"] is True
                    and all(inventory["files"].get(path) == digest for path, digest in previous["files"].items()),
                    f"Superseded inventory is not a byte-equal subset: {name}")
        for name, digest in inventory["files"].items():
            require(relative(name) and sha(source(name)) == digest, f"Packet bytes differ: {name}")
            guard.check()
        producers = sorted(PurePosixPath(name).name for name in paths if name.startswith("producers/"))
        require(producers == sorted(facts["producers"])
                and all(name == "producers/" + PurePosixPath(name).name
                        for name in paths if name.startswith("producers/")),
                "Signed producer inventory differs")
        for name in facts["producers"]:
            require((SCRATCH / name).read_bytes() == source("producers/" + name),
                    f"Executed producer differs: {name}")
        for record in source_proof["sourceRecords"]:
            require(sha(blob(record["path"])) == record["sha256"], "Verified dictionary output changed")
        for name, digest in final_proof["signedInputs"].items():
            require(sha(blob(name)) == digest, "Final source proof input changed")
        jm = helper.merge_records([blob(record["path"]) for record in source_proof["sourceRecords"]
                                   if record["input"] == "n1-implementation-JMdict_e.gz"]
                                  + [source(RESIDUAL)], "entry", "ent_seq")
        kd = helper.merge_records([blob(record["path"]) for record in source_proof["sourceRecords"]
                                   if record["input"] == "n1-planning-kanjidic2.xml.gz"], "character", "literal")
        require(len(jm) == facts["expectedJmdictFamilies"]
                and set(kd) == set(MEMBERS) | set(source_proof["packetComparisonCards"]),
                "Complete source union differs")
        source_facts = json.loads(frozen(source_proof["facts"]["path"], source_proof["facts"]["sha256"]))
        selections = {item["file"]: item for item in source_facts["jmdictSelections"]}
        require(set(facts["queryMaps"]) == set(selections), "JMdict query maps do not cover every selection")
        for filename, mapping in facts["queryMaps"].items():
            verify_query_map(source(filename), selections[filename], json.loads(source(mapping)))
        bound_outputs = set()
        for receipt_name, producer in facts["receipts"].items():
            receipt = json.loads(source(receipt_name))
            require(receipt.get("base", BASE) == BASE
                    and receipt["producerSha256"] == signed[PREFIX + "producers/" + producer],
                    f"Receipt producer or base differs: {receipt_name}")
            for kind, binding in receipt_inputs(receipt).items():
                expected = source_proof["inputs"][kind]
                require(binding["filename"] == expected["filename"]
                        and binding["compressedSha256"] == expected["compressedSha256"]
                        and binding["decompressedSha256"] == expected["decompressedXmlSha256"],
                        "Signed receipt does not bind the verified original dictionary")
            for name, binding in receipt_outputs(receipt).items():
                require(name not in bound_outputs, f"Output bound by two receipts: {name}")
                bound_outputs.add(name)
                raw = source(name)
                canonical = {node.findtext("ent_seq") or node.findtext("literal"):
                             sha(ET.canonicalize(ET.tostring(node, encoding="unicode"),
                                                 strip_text=True).encode())
                             for node in ET.fromstring(raw)}
                require(sha(raw) == binding["sha256"] and len(raw) == binding["bytes"]
                        and canonical == binding["canonicalRecordHashes"]
                        and binding.get("completeCanonicalEquality", True) is True,
                        f"Source receipt output differs: {name}")
        require(bound_outputs == {record["path"].removeprefix(PREFIX) for record in source_proof["sourceRecords"]}
                | {RESIDUAL},
                "Receipts do not bind exactly the verified XML outputs")
        sys.path.insert(0, str(WS / "lean"))
        from n1lib import parse
        comparisons = {}
        for char in source_proof["packetComparisonCards"]:
            raw = source(f"comparison-cards/{char}.md")
            metadata, _ = parse(raw.decode().replace("\r\n", "\n"))
            comparisons[char] = metadata["title"], sha(raw)
        disposition = json.loads(source(facts["pairDispositions"]))
        require(disposition["base"] == BASE, "Pair base differs")
        pair_members = [item for item in disposition["members"] if "kanji" in item]
        new_pairs = [item for item in disposition["members"] if "newMemberPair" in item]
        require(len(pair_members) + len(new_pairs) == len(disposition["members"])
                and [item["kanji"] for item in pair_members] == MEMBERS, "Pair members differ")
        new_guards, new_curated = new_pair_sets(new_pairs)
        final_directory = facts["scanDirectories"][-1]
        for item, member in zip(pair_members, payload["members"]):
            char = item["kanji"]
            scans = []
            for directory in facts["scanDirectories"]:
                scan_raw = source(f"{directory}/{char}.json")
                scan = json.loads(scan_raw)
                require(scan["base"] == BASE and scan["kanji"] == char
                        and len(scan["rows"]) == facts["scanRows"], f"Scan identity differs: {directory}/{char}")
                scans.append(scan)
            require(item["scanFile"] == f"{final_directory}/{char}.json"
                    and item["scanSha256"] == signed[PREFIX + item["scanFile"]]
                    and item["scanRows"] == facts["scanRows"], "Pair scan binding differs")
            verify_pair_member(item, member["metadata"], scans, comparisons, new_guards[char], new_curated[char])
        progress = json.loads(blob("docs/n1-sources/batch-130-progress.json"))
        verify_progress(progress, facts, payload)
        excerpts = 0
        for binding_name, count in facts["externalBindings"].items():
            external = json.loads(source(binding_name))
            require(len(external["captures"]) == count, f"External capture inventory differs: {binding_name}")
            texts = []
            for item in external["captures"]:
                raw_path = Path(item["localRawCapture"])
                text_path = Path(item.get("localTextCapture", raw_path.with_suffix(".txt")))
                require(raw_path.parent == SCRATCH / "external-pages" and raw_path.suffix == ".html"
                        and raw_path.with_suffix(".txt") == text_path
                        and raw_path.name.startswith(item["character"] + "-")
                        and item["character"] in MEMBERS, "External capture path differs")
                raw, text = raw_path.read_bytes(), text_path.read_bytes()
                require(sha(raw) == item["rawSha256"] and len(raw) == item["rawBytes"]
                        and sha(text) == item["textSha256"], "External capture bytes differ")
                captures["external-pages/" + raw_path.name] = raw
                captures["external-pages/" + text_path.name] = text
                texts.append(text)
                if "excerpt" in item:
                    verify_excerpt(text, item["excerpt"])
                    excerpts += 1
            if "excerpt" in external:
                require(len(texts) == 1, "File-level excerpt needs exactly one capture")
                verify_excerpt(texts[0], external["excerpt"])
                excerpts += 1
        font_record = json.loads(source(facts["fontEvidence"]))
        points = font_record["codePoints"]
        require(points and all(item["codePoint"] == f"U+{ord(item['character']):04X}"
                               and item["unicodeName"] == unicodedata.name(item["character"]) for item in points)
                and set(MEMBERS) <= {item["character"] for item in points},
                "Component code points differ")
        from fontTools.ttLib import TTFont
        font_results = []
        for item in font_record["fonts"]:
            require(item["filename"] in FONTS, "Unexpected bundled font")
            path = WS / "kanji-cards-android" / "app" / "src" / "main" / "res" / "font" / item["filename"]
            require(sha(path.read_bytes()) == item["sha256"] and path.stat().st_size == item["bytes"],
                    "Bundled font bytes differ")
            with TTFont(path) as font:
                cmap = font.getBestCmap()
                coverage = {point["codePoint"]: ord(point["character"]) in cmap for point in points}
            require(coverage == item["coverage"], "Bundled font cmap differs")
            font_results.append(item)
            guard.check()
        require({item["filename"] for item in font_results} == FONTS and len(font_results) == 3,
                "Missing or duplicate font")
        common_sha = signed[PREFIX + "producers/" + facts["commonHelper"]]
        config = {"repo": str(REPO)}
        gate_groups = {}
        for mode in ("author", "committed"):
            group = facts["gates"][mode]
            directory = SCRATCH / group["directory"]
            runner_sha = signed[PREFIX + "producers/" + group["runner"]]
            summary_raw = (directory / "summary.json").read_bytes()
            summary = json.loads(summary_raw)
            verify_summary(summary, mode, candidate, payload["manifestSha256"], runner_sha, common_sha,
                           facts["summaryBatch"])
            bindings = helper.gate_bindings(directory, config, payload["manifestSha256"], runner_sha, guard)
            receipts = {}
            for binding in bindings:
                gate = binding["gate"]
                for suffix, key in (("json", "receiptSha256"), ("log", "logSha256")):
                    filename = f"{gate}.{suffix}"
                    raw = (directory / filename).read_bytes()
                    require(sha(raw) == summary["logs"][gate][key], "Gate summary binding differs")
                    if group["signedCopy"] is not None:
                        require(raw == source(f"{group['signedCopy']}/{filename}"), "Signed gate differs")
                    captures[f"{mode}/{filename}"] = raw
                receipts[gate] = json.loads(captures[f"{mode}/{gate}.json"])
            verify_execution(receipts, commands, common_sha)
            if group["signedCopy"] is not None:
                require(summary_raw == source(f"{group['signedCopy']}/summary.json"), "Signed summary differs")
            captures[f"{mode}/summary.json"] = summary_raw
            gate_groups[mode] = {"summarySha256": sha(summary_raw), "sourceDirectory": str(directory),
                                 "runner": group["runner"], "signedCopy": group["signedCopy"],
                                 "gates": bindings}
        extras = verify_reading_keys(source("producers/" + facts["readingCheck"]),
                                     source(facts["readingKeys"]),
                                     captures["committed/reading-exposure.log"], facts["requiredReadingKeys"])
        preservation_dir = SCRATCH / facts["preservation"]["directory"]
        preservation = json.loads((preservation_dir / "summary.json").read_bytes())
        require(preservation["status"] == "PASS" and preservation["mode"] == "committed"
                and preservation["base"] == BASE and preservation["head"] == candidate
                and preservation["manifestSha256"] == payload["manifestSha256"]
                and preservation["evidenceInventorySha256"] == signed[PREFIX + facts["inventory"]]
                and preservation["producerSha256"]
                == signed[PREFIX + "producers/" + facts["preservation"]["producer"]]
                and not preservation["memory"]["breach"], "Preservation receipt differs")
        for name in ("summary.json", "memory.json", "runtime-hashes.json"):
            captures["preservation/" + name] = (preservation_dir / name).read_bytes()
        clean()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Evidence verification RAM breach")
    captured = {name: write_frozen(output / name, raw) for name, raw in captures.items()}
    print(json.dumps(freeze_json(output / "verification.json", {
        "batch": 130, "base": BASE, "candidate": candidate, "status": "PASS",
        "facts": {"path": str(Path(facts_path).resolve()), "sha256": sha(facts_raw)},
        "sourceProof": {"path": source_path, "sha256": source_sha},
        "payloadProof": {"path": payload_path, "sha256": payload_sha},
        "finalSourceProof": {"path": final_path, "sha256": final_sha},
        "signedInputs": signed, "capturedInputs": captured, "gates": gate_groups,
        "completeJmdictFamilies": len(jm), "completeKanjidicRecords": len(kd),
        "finiteBaselinePairs": sum(len(item["pairs"]) for item in pair_members),
        "finiteNewPairs": len(new_pairs), "verifiedExcerpts": excerpts,
        "supplementalReadingKeys": extras, "bundledFontEvidence": font_results,
        "memory": memory, "verifierSha256": sha(Path(__file__).read_bytes()),
        "limits": "Mechanical binding only. Pair judgments, original-source predicates, "
                  "reading-pool limitations and rendered/native/device acceptance are not "
                  "established by hash equality. Supplemental keys are bound to the producer and "
                  "log, not independently re-executed. Independent reviews and publication remain open.",
    })))


if __name__ == "__main__":
    require(len(sys.argv) == 3, "Usage: verify_b130_evidence_v2.py FROZEN_FACTS SHA256")
    main(*sys.argv[1:])

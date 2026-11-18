"""Bind B127's actual signed tree, source inventory, neutral sources and gates."""
import copy
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

from common import GUARD_SHA, WS, freeze_json, frozen, json_bytes, load_module, require, sha, start_guard, write_frozen
import verify_b127_sources as source_verifier
from verify_b127_sources import BASE, CANDIDATE, DISTRACTORS, HERE, MEMBER, PREFIX, REPO, WORD, blob, clean, git

HELPER = WS / "scratch-124" / "review" / "prepare-source-contract.py"
HELPER_SHA = "1c626c4f2e49d5761d53926c70b5891ea00b63fc7a06383aeb7d5a076772a270"
ORDER = ("lint", "quiz-safety", "linkplan", "reading-exposure", "validate",
         "manifest", "unittest", "budget", "vocabulary", "manifest-rebuild")
CONVERTER_SHA = "6993834d66221d23399547e5a17771d2d638dc68b2d08d47e9875ddc2c932081"
JOYO_SHA = "cc740aed34751e40831e4ab526408401667a428cefcf0fdd0212848eb31d67cb"
JOYO_ROW = "\u5009\n\u30bd\u30a6 \u5009\u5eab\uff0c\u7a40\u5009\n\u304f\u3089 \u5009\uff0c\u5009\u6577\u6599 \u21d4 \u8535"
DIRECT_GUARDS = list("\u5eab\u8535\u5e9c\u5ba4\u53ce\u8caf\u6025\u7a81\u4ea1\u7f6e\u5165")


def verify_summary(value, mode, head, manifest_sha, runner_sha, common_sha):
    require(value["batch"] == "127" and value["mode"] == mode and value["status"] == "PASS"
            and value["base"] == BASE and value["startingHead"] == head
            and value["checks"] == list(ORDER) and value["manifestSha256"] == manifest_sha
            and value["runnerSha256"] == runner_sha and value["commonHelperSha256"] == common_sha
            and value["guardSha256"] == GUARD_SHA and value["serial"] is True
            and value["waitTimeoutSeconds"] == 0.1 and value["cleanupTimeoutSecondsPerStage"] == 10
            and not value["finalMemory"]["breach"], "Gate summary does not bind this snapshot and runner")


def verify_execution(receipts, commands, helper_sha):
    previous = None
    for name in ORDER:
        item = receipts[name]
        start, end = (datetime.fromisoformat(item[key]) for key in ("startedAt", "completedAt"))
        require(start.tzinfo is not None and end.tzinfo is not None and end >= start
                and (previous is None or start >= previous), "Gate timestamps overlap or are invalid")
        previous = end
        require(item["command"] == [sys.executable, "-B", *map(str, commands[name])],
                f"Unexpected executed gate command: {name}")
        require(item["commonHelperSha256"] == helper_sha and item["cleanupTimeoutSecondsPerStage"] == 10
                and item["cleanupError"] is None and item["activeError"] is None,
                f"Gate cleanup or helper differs: {name}")


def runtime_entries(manifest):
    binary_sections = {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
    return {path: (digest, section in binary_sections)
            for section, entries in manifest.items() if isinstance(entries, dict)
            for path, digest in entries.items()}


def main():
    for name in ("batch.json", "source-contract", "source-contract.json", "candidate-inputs",
                 "coordinator-candidate-verification.json"):
        require(not (HERE / name).exists(), f"Preserve existing output: {name}")
    frozen(HELPER, HELPER_SHA)
    helper = load_module("b127_source_contract_helpers", HELPER)
    config = {"batch": 127, "candidate": CANDIDATE, "base": BASE, "members": [MEMBER],
              "repo": str(REPO), "expectedKanji": 1247,
              "gates": str(HERE / "candidate-inputs" / "committed")}
    signed, outputs, captures = {}, {}, {}

    def source(name):
        raw = blob(PREFIX + name)
        signed[PREFIX + name] = sha(raw)
        return raw

    guard, _ = start_guard("B127 candidate and gate binding")
    source_verifier.ACTIVE_GUARD = guard
    try:
        clean()
        proof_path = HERE / "source-selection-verification-001.json"
        proof_raw = frozen(proof_path, "449151c8b2ce6e2dbfba3a17fdd791a992b5c8ae847a1cebc4bb81a8c82a2804")
        proof = json.loads(proof_raw)
        require(proof["candidate"] == CANDIDATE and proof["base"] == BASE and proof["batch"] == 127
                and proof["status"] == "PASS" and not proof["memory"]["breach"]
                and proof["verifierSha256"] == sha(frozen(Path(source_verifier.__file__))),
                "Source proof is not bound to this candidate")
        for record in proof["sourceRecords"]:
            require(sha(blob(record["path"])) == record["sha256"], "Verified source changed")
        handoff_path = WS / "scratch-127" / "handoff-001" / "handoff.json"
        handoff_raw = handoff_path.read_bytes()
        require(sha(handoff_raw) == "b773c12e90076b5af85cfe153e70f127543b37da90dd911b73fe412ebcf4864f",
                "Author handoff changed")
        handoff = json.loads(handoff_raw)
        require(handoff["candidate"] == CANDIDATE and handoff["base"] == BASE, "Wrong handoff snapshot")
        for name, binding in handoff["bindings"].items():
            raw = source(name)
            require(sha(raw) == binding["sha256"] and len(raw) == binding["bytes"], f"Handoff binding: {name}")
        inventory_raw = source("packet-files-002.json")
        inventory = json.loads(inventory_raw)["files"]
        for name, binding in inventory.items():
            require(not Path(name).is_absolute() and ".." not in Path(name).parts, "Unsafe inventory path")
            raw = source(name)
            require(sha(raw) == binding["sha256"] and len(raw) == binding["bytes"], f"Final inventory: {name}")
            guard.check()
        changed = {}
        added = {f"kanji/{MEMBER}.md", f"strokes/{MEMBER}.json"}
        word_path = f"words/{WORD}.md"
        for line in git("diff", "--name-status", "--no-renames", BASE, CANDIDATE).decode("utf-8").splitlines():
            status, path = line.split("\t", 1)
            require((status == "A" and (path in added or path.startswith(PREFIX)
                                       or path == "docs/n1-sources/batch-127-progress.json"))
                    or (status == "M" and path in {word_path, "manifest.json", "docs/n1-authoring-notes.md"}),
                    f"Unexpected change: {status} {path}")
            changed[path] = status
        require({path[len(PREFIX):] for path in changed if path.startswith(PREFIX)}
                == set(inventory) | {"packet-files-002.json"}, "Final packet inventory is incomplete")
        require(len(inventory) + 1 == 188, "Unexpected packet size")
        notes = blob("docs/n1-authoring-notes.md").replace(b"\r\n", b"\n")
        stripped, count = re.subn(rb"(?m)^## Batch 127:.*?\n(?=## Batch )", b"", notes, flags=re.S)
        require(count == 1 and stripped == blob("docs/n1-authoring-notes.md", BASE).replace(b"\r\n", b"\n"),
                "Authoring notes exceed the new batch section")
        manifest_raw = blob("manifest.json")
        require((REPO / "manifest.json").read_bytes() == manifest_raw, "Working manifest differs from Git")
        manifest, old_manifest = json.loads(manifest_raw), json.loads(blob("manifest.json", BASE))
        flatten = lambda value: {path: digest for group in value.values() if isinstance(group, dict)
                                 for path, digest in group.items()}
        current, previous = flatten(manifest), flatten(old_manifest)
        require(current.keys() - previous.keys() == added and previous.keys() <= current.keys()
                and {p for p in previous if current[p] != previous[p]} == {word_path},
                "Unexpected runtime delta")
        require(len(current) == 8716 and len(previous) == 8714, "Runtime counts differ")
        for path, (expected, binary) in runtime_entries(manifest).items():
            raw = (REPO / Path(path)).read_bytes()
            require(sha(raw if binary else raw.replace(b"\r\n", b"\n")) == expected,
                    f"Actual runtime hash differs: {path}")
            guard.check()
        sys.path.insert(0, str(WS / "lean"))
        from n1lib import parse
        row = json.loads(source("source-row.json"))
        community = blob("docs/n1-sources/community-list-20261102.json")
        require(community == blob("docs/n1-sources/community-list-20261102.json", BASE)
                and sha(community) == "889faaefbec573e806f298766d2eee1300674c7b229bd973a35169cd2652cd73"
                and json.loads(community)[56] == MEMBER, "Community membership differs")
        card, body = parse(blob(f"kanji/{MEMBER}.md").decode("utf-8").replace("\r\n", "\n"))
        for key in ("onyomi", "kunyomi", "radical"):
            require(card[key] == row["metadata"][key], f"Source metadata differs: {key}")
        for key in ("strokes", "radicalNumber"):
            require(card[key] == str(row["metadata"][key]), f"Source metadata differs: {key}")
        require(card["kanji"] == MEMBER and card["jlpt"] == "1" and card["distractors"] == DISTRACTORS
                and card["quiz_exclusions"] == DIRECT_GUARDS and card["quizOnyomi"] == ["\u30bd\u30a6"]
                and card["quizKunyomi"] == [] and f"](../words/{WORD}.md)" in body,
                "Card fields or support link differ")
        require(source(f"baseline-{WORD}.md") == blob(word_path, BASE)
                and helper.single_wrapper(blob(word_path, BASE), blob(word_path), MEMBER),
                "Existing word change exceeds one reciprocal wrapper")
        declaring = []
        for path in old_manifest["files"]:
            if path.startswith("words/"):
                metadata, _ = parse((REPO / Path(path)).read_text(encoding="utf-8"))
                if metadata and MEMBER in metadata.get("kanji", []):
                    declaring.append(Path(path).stem)
                guard.check()
        selection = json.loads(source("selection.json"))
        require(declaring == selection["declaringArticlesAtBase"] == [WORD]
                and selection["requiredReciprocalPairs"] == [[MEMBER, WORD]]
                and selection["membership"] == [{"kanji": MEMBER, "sourceRow": 57}], "Support coverage differs")
        scans = json.loads(source("baseline-gloss-scan-002.json"))
        dispositions = json.loads(source("pair-dispositions.json"))
        require([item["kanji"] for item in dispositions["scanMatches"]] == scans["matches"]
                and {item["kanji"] for item in dispositions["scanMatches"] if item["decision"] == "guard"}
                == set(DIRECT_GUARDS), "Finite pair inventory differs")
        actual_rows = {item["kanji"]: item for item in scans["rows"]}
        for item in dispositions["scanMatches"]:
            actual = actual_rows[item["kanji"]]
            require(item["baselineTitle"] == actual["title"]
                    and item["completeSourceMeanings"] == actual["meanings"], "Pair source row differs")
        progress = json.loads(blob("docs/n1-sources/batch-127-progress.json"))
        require(progress["membership"] == [MEMBER] and progress["sourceRows"] == [57]
                and progress["published"] == progress["reviewClosed"] == []
                and progress["runtimePublished"] is False
                and progress["accounting"]["publishedPendingRecordsWithCards"] == 256
                and progress["accounting"]["undelivered"] == 972
                and progress["accounting"]["overallN1TaskComplete"] is False
                and progress["runtimeCandidate"]["manifestSha256"] == sha(manifest_raw)
                and progress["runtimeCandidate"]["contentVersion"] == manifest["contentVersion"],
                "Premature publication or wrong runtime accounting")
        pending = {item["kanji"] for item in json.loads(blob("docs/n1-sources/source-index.json"))
                   if item["statusAtFreeze"] == "pending"}
        represented = lambda entries: {Path(p).stem for p in entries if p.startswith("kanji/")}
        require(len(pending & represented(previous)) == 256 and len(pending & represented(current)) == 257
                and len(represented(current)) == 1247, "Source membership accounting differs")

        converter_path = REPO / "tools" / "generate_strokes.py"
        require(converter_path.read_bytes() == blob("tools/generate_strokes.py")
                and sha(converter_path.read_bytes()) == CONVERTER_SHA, "Converter differs")
        converter = load_module("b127_pinned_converter", converter_path)
        svg = source("05009.svg")
        svg_blob = hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest()
        receipt = json.loads(source("source-receipt.json"))
        require(svg_blob == row["kanjivgInventory"]["sha"] == receipt["kanjivg"]["gitBlob"]
                and sha(svg) == receipt["kanjivg"]["sha256"]
                and converter.convert(MEMBER, svg.decode("utf-8")) == json.loads(blob(f"strokes/{MEMBER}.json")),
                "Generated strokes do not reproduce")
        for kind in ("jmdict", "kanjidic2"):
            require(all(receipt["dictionaryInputs"][kind][key] == value
                        for key, value in proof["inputs"][kind].items()), "Source receipt input differs")
        from fontTools.ttLib import TTFont
        app = WS / "kanji-cards-android"
        app_head = git("rev-parse", "HEAD", repo=app).decode().strip()
        fonts = []
        for name in ("kanji_brush.ttf", "kanji_mincho.ttf", "kanji_textbook.ttf"):
            relative = "app/src/main/res/font/" + name
            path = app / Path(relative)
            raw = path.read_bytes()
            require(raw == git("show", f"{app_head}:{relative}", repo=app), "Font differs from app snapshot")
            with TTFont(path) as font:
                cmap = font.getBestCmap()
                coverage = {f"U+{ord(char):04X}": ord(char) in cmap for char in MEMBER + "\u4eba\u53e3\u5b80"}
            fonts.append({"filename": name, "sha256": sha(raw), "bytes": len(raw), "coverage": coverage})
            guard.check()
        font_record = json.loads(source("stroke-font-evidence.json"))
        require(font_record["fonts"] == fonts and font_record["converterSha256"] == CONVERTER_SHA
                and font_record["strokeSha256"] == sha(blob(f"strokes/{MEMBER}.json"))
                and font_record["svgSha256"] == sha(svg), "Stroke/font evidence differs")
        outputs["kvg/05009.svg"] = svg
        outputs["shape-evidence.json"] = json_bytes([{
            "kanji": MEMBER, "revision": converter.KANJIVG_REVISION, "gitBlobSha1": svg_blob,
            "sourcePath": "kanji/05009.svg", "sha256": sha(svg), "canonicalStrokes": 10,
            "groups": [dict(node.attrib) for node in ET.fromstring(svg).iter("{http://www.w3.org/2000/svg}g")],
            "bundledFonts": {"appSnapshot": app_head, "files": fonts},
            "scope": "Actual cmap evidence; contrast-only U+5B80 absent. No rendered/native/device acceptance.",
        }])
        joyo_raw = (WS / "scratch-111" / "joyo-pages.json").read_bytes()
        require(sha(joyo_raw) == JOYO_SHA and JOYO_ROW in json.loads(joyo_raw)["97"], "Pinned Joyo row differs")
        outputs["joyo-rows.json"] = json_bytes({"cacheSha256": sha(joyo_raw),
            "scope": "Pinned cached text, not fresh PDF glyph inspection.",
            "rows": [{"kanji": MEMBER, "matches": [{"printedPage": 97, "extract": JOYO_ROW}]}]})
        external = json.loads(source("external-source-bindings.json"))
        for entry in external["captures"]:
            path = Path(entry["localCapture"])
            require(path.parent == WS / "scratch-127" / "external-pages"
                    and sha(path.read_bytes()) == entry["rawSha256"] and path.stat().st_size == entry["rawBytes"]
                    and sha(path.with_suffix(".txt").read_bytes()) == entry["textSha256"], "External capture differs")

        jm = helper.merge_records([source("jmdict-selected-records.xml")], "entry", "ent_seq")
        kd = helper.merge_records([blob(item["path"]) for item in proof["sourceRecords"]
                                   if "kanjidic2" in item["path"]], "character", "literal")
        require(len(jm) == 78 and set(kd) == {MEMBER} | set(proof["comparisonCards"]), "Neutral source scope differs")
        for name, tag, entries in (
            ("jmdict-families.xml", "JMdict", [jm[key] for key in sorted(jm, key=int)]),
            ("kanjidic2-records.xml", "kanjidic2", [kd[MEMBER]] + [kd[key] for key in sorted(set(kd) - {MEMBER})]),
        ):
            root = ET.Element(tag)
            root.extend(copy.deepcopy(entry) for entry in entries)
            outputs[name] = ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"
        outputs["selection.json"] = json_bytes({"order": [MEMBER], "sourceRows": [57]})
        outputs["evidence-index.json"] = json_bytes({
            "outputs": {name: sha(raw) for name, raw in outputs.items()},
            "completeDictionaryEntries": len(jm), "dictionaryQueryEntries": helper.query_index(jm, set(), MEMBER, []),
        })
        scratch = WS / "scratch-127"
        runner_path = scratch / "run_b127_gates.py"
        for name in ("run_b127_gates.py", "b127_common.py", "check_reading_b127.py"):
            raw = (scratch / name).read_bytes()
            require(raw == source("producers/" + name), f"Executed helper differs from signed source: {name}")
            captures[name] = raw
        runner_sha, common_sha = sha(captures["run_b127_gates.py"]), sha(captures["b127_common.py"])
        lean = WS / "lean"
        commands = {
            "lint": [lean / "n1_batch_tool.py", "lint", "--base", BASE, "--no-jmdict", MEMBER],
            "quiz-safety": [lean / "quiz_safety.py", MEMBER],
            "linkplan": [lean / "n1_linkplan.py", "verify", BASE, MEMBER],
            "reading-exposure": [scratch / "check_reading_b127.py"],
            "validate": [REPO / "tools" / "validate.py"], "manifest": [REPO / "tools" / "build_manifest.py"],
            "unittest": ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"],
            "budget": [REPO / "tools" / "check_content_budget.py"],
            "vocabulary": [REPO / "tools" / "grammar_vocabulary.py", "check"],
            "manifest-rebuild": [REPO / "tools" / "build_manifest.py"],
        }
        gate_groups = {}
        for mode, name in (("author", "author-gates-003"), ("committed", "committed-gates-001")):
            directory = scratch / name
            summary_raw = (directory / "summary.json").read_bytes()
            summary = json.loads(summary_raw)
            verify_summary(summary, mode, BASE if mode == "author" else CANDIDATE,
                           sha(manifest_raw), runner_sha, common_sha)
            bindings = helper.gate_bindings(directory, config, sha(manifest_raw), runner_sha, guard)
            receipts = {}
            for item in bindings:
                gate = item["gate"]
                raw, log = ((directory / f"{gate}.{ext}").read_bytes() for ext in ("json", "log"))
                require(sha(raw) == summary["logs"][gate]["receiptSha256"]
                        and sha(log) == summary["logs"][gate]["logSha256"], "Gate binding differs")
                if mode == "author":
                    require(raw == source(f"{name}/{gate}.json") and log == source(f"{name}/{gate}.log"),
                            "Signed author gate differs")
                captures[f"{mode}/{gate}.json"], captures[f"{mode}/{gate}.log"] = raw, log
                receipts[gate] = json.loads(raw)
            verify_execution(receipts, commands, common_sha)
            if mode == "author":
                require(summary_raw == source(f"{name}/summary.json")
                        and sha(summary_raw) == progress["authorGates"]["summarySha256"], "Author summary differs")
            else:
                require(sha(summary_raw) == handoff["gates"]["summarySha256"], "Committed summary differs")
            captures[f"{mode}/summary.json"] = summary_raw
            gate_groups[mode] = {"sourceDirectory": str(directory), "summarySha256": sha(summary_raw), "gates": bindings}
        captures["handoff.json"] = handoff_raw
        clean()
    finally:
        memory = guard.finish()
        source_verifier.ACTIVE_GUARD = None
    require(not memory["breach"], "RAM breach")
    captured = {name: write_frozen(HERE / "candidate-inputs" / name, raw) for name, raw in captures.items()}
    bindings = {name: write_frozen(HERE / "source-contract" / name, raw) for name, raw in outputs.items()}
    contract = freeze_json(HERE / "source-contract.json", {
        "batch": 127, "candidate": CANDIDATE, "base": BASE, "files": bindings, "signedSources": signed,
        "method": "Complete signed records independently checked against pinned original inputs. Duplicate "
                  "identities merged only after structural equality; parsed/reserialized XML, not raw compressed "
                  "slices. Neutral source outputs contain no author judgments.",
        "dictionaryVerification": {"path": str(proof_path), "sha256": sha(proof_raw)},
        "tool": {"path": str(Path(__file__)), "sha256": sha(Path(__file__).read_bytes())},
    })
    config["sourceContract"] = {"path": contract["path"], "sha256": contract["sha256"]}
    batch = freeze_json(HERE / "batch.json", config)
    print(json.dumps(freeze_json(HERE / "coordinator-candidate-verification.json", {
        "batch": 127, "candidate": CANDIDATE, "base": BASE, "status": "PASS",
        "ownerSignature": "G", "worktreeClean": True, "changedPaths": changed, "packetFiles": len(inventory) + 1,
        "manifestSha256": sha(manifest_raw), "contentVersion": manifest["contentVersion"],
        "runtimeEntries": len(current), "baselineUnchangedEntries": len(previous) - 1,
        "sourceMembersPublishedBeforeBatch": 256, "sourceMembersInCandidate": 257,
        "baselineRuntimePreservedExceptRequiredWrappers": True, "allActualRuntimeHashesChecked": True,
        "sourceContract": contract, "batchConfig": batch, "gates": gate_groups, "capturedGateInputs": captured,
        "captureScope": "Post-execution ReadOnly captures, not retrospective immutability.",
        "completeSourceVerification": sha(proof_raw), "bundledFontEvidence": fonts,
        "reusedHelper": {"path": str(HELPER), "sha256": HELPER_SHA}, "memory": memory,
        "inventoryQualification": "Final packet-files-002.json is authoritative per the signed supplement. "
                                  "The original packet-files.json and original progress pointer remain historical.",
        "limits": "Mechanical candidate/source/gate binding. Linguistic review, arbitrary-pool, "
                  "native/device, CI, served-ZIP and publication acceptance remain open.",
    })))


if __name__ == "__main__":
    main()

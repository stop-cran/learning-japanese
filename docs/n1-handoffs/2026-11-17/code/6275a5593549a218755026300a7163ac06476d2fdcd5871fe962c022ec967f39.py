"""Bind B128's actual signed tree, source inventory, neutral sources and gates."""
import copy
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

from common import GUARD_SHA, WS, freeze_json, frozen, json_bytes, load_module, require, sha, start_guard, write_frozen
import verify_batch_sources_v2 as source_verifier

BASE = "bd0f4b842c588e581ccb31ad946eecedb63d32b8"
CANDIDATE = "fb3c98d86881bbc6a4b61f94bce44d0947a0c808"
MEMBER = WORD = "\u5507"
DISTRACTORS = list("\u53e4\u53f3\u77f3")
HERE = WS / "scratch-128" / "review"
REPO = WS / "b128-worktree"
PREFIX = "docs/n1-sources/batch-128/"
RUNNER = {"path": str(HERE / "guarded-test-v3.py"),
          "sha256": "202577b7d2b286318c377be69b44ed02681b878cf2b05b29776d00de57982f84"}
CLIENTS = {}


def git(*args, repo=REPO):
    if repo not in CLIENTS:
        CLIENTS[repo] = source_verifier.Git(repo, RUNNER, source_verifier.ACTIVE_GUARD)
    return CLIENTS[repo](*args)


def blob(path, commit=CANDIDATE):
    return git("show", f"{commit}:{path}")


def clean():
    require(git("rev-parse", "HEAD").decode().strip() == CANDIDATE
            and not git("status", "--porcelain=v1", "--untracked-files=all"), "Candidate changed")


HELPER = WS / "scratch-124" / "review" / "prepare-source-contract.py"
HELPER_SHA = "1c626c4f2e49d5761d53926c70b5891ea00b63fc7a06383aeb7d5a076772a270"
ORDER = ("lint", "quiz-safety", "linkplan", "reading-exposure", "validate",
         "manifest", "unittest", "budget", "vocabulary", "manifest-rebuild")
CONVERTER_SHA = "6993834d66221d23399547e5a17771d2d638dc68b2d08d47e9875ddc2c932081"
JOYO_SHA = "cc740aed34751e40831e4ab526408401667a428cefcf0fdd0212848eb31d67cb"
JOYO_ROW = "\u5507\n\u30b7\u30f3 \u53e3\u5507\n\u304f\u3061\u3073\u308b \u5507"
DIRECT_GUARDS = list("\u53e3\u82b1\u9707\u52d5\u6050\u6016\u5074\u8fba\u969b\u5883\u754c\u5cb8\u7554\u97f3")


def verify_summary(value, mode, head, manifest_sha, runner_sha, common_sha):
    require(value["batch"] == "128" and value["mode"] == mode and value["status"] == "PASS"
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
    helper = load_module("b128_source_contract_helpers", HELPER)
    config = {"batch": 128, "candidate": CANDIDATE, "base": BASE, "members": [MEMBER],
              "repo": str(REPO), "expectedKanji": 1248,
              "gates": str(HERE / "candidate-inputs" / "committed")}
    signed, outputs, captures = {}, {}, {}

    def source(name):
        raw = blob(PREFIX + name)
        signed[PREFIX + name] = sha(raw)
        return raw

    guard, _ = start_guard("B128 candidate and gate binding")
    source_verifier.ACTIVE_GUARD = guard
    try:
        clean()
        proof_path = HERE / "source-selection-verification-001.json"
        proof_raw = frozen(proof_path, "9f8d68a03b45d8c32d1ad7c44f6260bf29b5c87bb0b751f1c707e75aac2d0548")
        proof = json.loads(proof_raw)
        require(proof["candidate"] == CANDIDATE and proof["base"] == BASE and proof["batch"] == 128
                and proof["status"] == "PASS" and not proof["memory"]["breach"]
                and proof["verifierSha256"] == sha(frozen(Path(source_verifier.__file__))),
                "Source proof is not bound to this candidate")
        for record in proof["sourceRecords"]:
            require(sha(blob(record["path"])) == record["sha256"], "Verified source changed")
        handoff_path = WS / "scratch-128" / "handoff-001" / "handoff.json"
        handoff_raw = handoff_path.read_bytes()
        require(sha(handoff_raw) == "1e31908f0aff1569b231fcd04f535b72bcd5e7c8f5a6a281f2f45a2286e0dbda",
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
                                       or path == "docs/n1-sources/batch-128-progress.json"))
                    or (status == "M" and path in {word_path, "manifest.json", "docs/n1-authoring-notes.md"}),
                    f"Unexpected change: {status} {path}")
            changed[path] = status
        require({path[len(PREFIX):] for path in changed if path.startswith(PREFIX)}
                == set(inventory) | {"packet-files-002.json"}, "Final packet inventory is incomplete")
        require(len(inventory) > 0, "Unexpected packet size")
        notes = blob("docs/n1-authoring-notes.md").replace(b"\r\n", b"\n")
        stripped, count = re.subn(rb"(?m)^## Batch 128:.*?\n(?=## Batch )", b"", notes, flags=re.S)
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
        require(len(current) == 8718 and len(previous) == 8716, "Runtime counts differ")
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
                and json.loads(community)[158] == MEMBER, "Community membership differs")
        card, body = parse(blob(f"kanji/{MEMBER}.md").decode("utf-8").replace("\r\n", "\n"))
        for key in ("onyomi", "kunyomi", "radical"):
            require(card[key] == row["metadata"][key], f"Source metadata differs: {key}")
        for key in ("strokes", "radicalNumber"):
            require(card[key] == str(row["metadata"][key]), f"Source metadata differs: {key}")
        require(card["kanji"] == MEMBER and card["jlpt"] == "1" and card["distractors"] == DISTRACTORS
                and card["quiz_exclusions"] == DIRECT_GUARDS and card["quizOnyomi"] == []
                and card["quizKunyomi"] == ["\u304f\u3061\u3073\u308b"] and f"](../words/{WORD}.md)" in body,
                "Card fields or support link differ")
        prose = json.loads(source("stale-remarks.json"))
        require(prose == [{"file": word_path, "old": f" There is no {MEMBER} kanji card in the current collection.",
                          "new": ""}], "Unexpected prose exception")
        before = blob(word_path, BASE)
        old = prose[0]["old"].encode("utf-8")
        require(before.count(old) == 1 and old not in blob(word_path)
                and source(f"baseline-{WORD}.md") == before
                and helper.single_wrapper(before.replace(old, b""), blob(word_path), MEMBER),
                "Existing word differs beyond the reciprocal wrapper and false no-card sentence")
        config["wordProseChanges"] = prose
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
                and selection["membership"] == [{"kanji": MEMBER, "sourceRow": 159}], "Support coverage differs")
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
        progress = json.loads(blob("docs/n1-sources/batch-128-progress.json"))
        require(progress["membership"] == [MEMBER] and progress["sourceRows"] == [159]
                and progress["published"] == progress["reviewClosed"] == []
                and progress["runtimePublished"] is False
                and progress["accounting"]["publishedPendingRecordsWithCards"] == 257
                and progress["accounting"]["undelivered"] == 971
                and progress["accounting"]["overallN1TaskComplete"] is False
                and progress["runtimeCandidate"]["manifestSha256"] == sha(manifest_raw)
                and progress["runtimeCandidate"]["contentVersion"] == manifest["contentVersion"],
                "Premature publication or wrong runtime accounting")
        pending = {item["kanji"] for item in json.loads(blob("docs/n1-sources/source-index.json"))
                   if item["statusAtFreeze"] == "pending"}
        represented = lambda entries: {Path(p).stem for p in entries if p.startswith("kanji/")}
        require(len(pending & represented(previous)) == 257 and len(pending & represented(current)) == 258
                and len(represented(current)) == 1248, "Source membership accounting differs")

        converter_path = REPO / "tools" / "generate_strokes.py"
        require(converter_path.read_bytes() == blob("tools/generate_strokes.py")
                and sha(converter_path.read_bytes()) == CONVERTER_SHA, "Converter differs")
        converter = load_module("b128_pinned_converter", converter_path)
        svg = source("05507.svg")
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
                coverage = {f"U+{ord(char):04X}": ord(char) in cmap for char in MEMBER + "\u8fb0\u53e3\u8123" + "".join(DISTRACTORS)}
            fonts.append({"filename": name, "sha256": sha(raw), "bytes": len(raw), "coverage": coverage})
            guard.check()
        font_record = json.loads(source("stroke-font-evidence.json"))
        require(font_record["fonts"] == fonts and font_record["converterSha256"] == CONVERTER_SHA
                and font_record["strokeSha256"] == sha(blob(f"strokes/{MEMBER}.json"))
                and font_record["svgSha256"] == sha(svg), "Stroke/font evidence differs")
        outputs["kvg/05507.svg"] = svg
        outputs["shape-evidence.json"] = json_bytes([{
            "kanji": MEMBER, "revision": converter.KANJIVG_REVISION, "gitBlobSha1": svg_blob,
            "sourcePath": "kanji/05507.svg", "sha256": sha(svg), "canonicalStrokes": 10,
            "groups": [dict(node.attrib) for node in ET.fromstring(svg).iter("{http://www.w3.org/2000/svg}g")],
            "bundledFonts": {"appSnapshot": app_head, "files": fonts},
            "scope": "Actual cmap evidence; variant U+8123 absent. No rendered/native/device acceptance.",
        }])
        joyo_raw = (WS / "scratch-111" / "joyo-pages.json").read_bytes()
        require(sha(joyo_raw) == JOYO_SHA and JOYO_ROW in json.loads(joyo_raw)["84"], "Pinned Joyo row differs")
        outputs["joyo-rows.json"] = json_bytes({"cacheSha256": sha(joyo_raw),
            "scope": "Pinned cached text, not fresh PDF glyph inspection.",
            "rows": [{"kanji": MEMBER, "matches": [{"printedPage": 84, "extract": JOYO_ROW}]}]})
        external = json.loads(source("external-source-bindings.json"))
        for entry in external["captures"]:
            path = Path(entry["localCapture"])
            require(path.parent == WS / "scratch-128" / "external-pages"
                    and sha(path.read_bytes()) == entry["rawSha256"] and path.stat().st_size == entry["rawBytes"]
                    and sha(path.with_suffix(".txt").read_bytes()) == entry["textSha256"], "External capture differs")

        jm = helper.merge_records([source("jmdict-selected-records.xml"), source("jmdict-comparison-records.xml")],
                                  "entry", "ent_seq")
        kd = helper.merge_records([blob(item["path"]) for item in proof["sourceRecords"]
                                   if "kanjidic2" in item["path"]], "character", "literal")
        require(len(jm) == 103 and set(kd) == {MEMBER} | set(proof["packetComparisonCards"]), "Neutral source scope differs")
        for name, tag, entries in (
            ("jmdict-families.xml", "JMdict", [jm[key] for key in sorted(jm, key=int)]),
            ("kanjidic2-records.xml", "kanjidic2", [kd[MEMBER]] + [kd[key] for key in sorted(set(kd) - {MEMBER})]),
        ):
            root = ET.Element(tag)
            root.extend(copy.deepcopy(entry) for entry in entries)
            outputs[name] = ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"
        outputs["selection.json"] = json_bytes({"order": [MEMBER], "sourceRows": [159]})
        exact = set(json.loads(source("comparison-query-membership.json")))
        extra = json.loads(source("comparison-source-receipt.json"))["exactKebOrRebQueries"]
        exact |= {query for query in extra if not query.startswith("reading=")}
        query_index = helper.query_index(jm, exact, MEMBER, ["\u8123"])
        for query, expected in json.loads(source("comparison-query-membership.json")).items():
            require(query_index[query] == expected, f"Comparison query map differs: {query}")
        for query, expected in extra.items():
            if query.startswith("reading="):
                reading = query.removeprefix("reading=")
                actual = sorted(key for key, node in jm.items() if reading in
                                {item.text for item in node.findall("r_ele/reb")})
                query_index["reading:" + reading] = actual
            else:
                actual = query_index[query]
            require(actual == expected, f"Extra query map differs: {query}")
        outputs["evidence-index.json"] = json_bytes({
            "outputs": {name: sha(raw) for name, raw in outputs.items()},
            "completeDictionaryEntries": len(jm), "dictionaryQueryEntries": query_index,
        })
        scratch = WS / "scratch-128"
        runner_path = scratch / "run_b128_gates.py"
        for name in ("run_b128_gates.py", "b128_common.py", "check_reading_b128.py"):
            raw = (scratch / name).read_bytes()
            require(raw == source("producers/" + name), f"Executed helper differs from signed source: {name}")
            captures[name] = raw
        runner_sha, common_sha = sha(captures["run_b128_gates.py"]), sha(captures["b128_common.py"])
        lean = WS / "lean"
        commands = {
            "lint": [lean / "n1_batch_tool.py", "lint", "--base", BASE, "--no-jmdict", MEMBER],
            "quiz-safety": [lean / "quiz_safety.py", MEMBER],
            "linkplan": [lean / "n1_linkplan.py", "verify", BASE, "--remarks",
                         REPO / "docs" / "n1-sources" / "batch-128" / "stale-remarks.json", MEMBER],
            "reading-exposure": [scratch / "check_reading_b128.py"],
            "validate": [REPO / "tools" / "validate.py"], "manifest": [REPO / "tools" / "build_manifest.py"],
            "unittest": ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"],
            "budget": [REPO / "tools" / "check_content_budget.py"],
            "vocabulary": [REPO / "tools" / "grammar_vocabulary.py", "check"],
            "manifest-rebuild": [REPO / "tools" / "build_manifest.py"],
        }
        gate_groups = {}
        for mode, name in (("author", "author-gates-002"), ("committed", "committed-gates-001")):
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
        "batch": 128, "candidate": CANDIDATE, "base": BASE, "files": bindings, "signedSources": signed,
        "method": "Complete signed records independently checked against pinned original inputs. Duplicate "
                  "identities merged only after structural equality; parsed/reserialized XML, not raw compressed "
                  "slices. Neutral source outputs contain no author judgments.",
        "dictionaryVerification": {"path": str(proof_path), "sha256": sha(proof_raw)},
        "tool": {"path": str(Path(__file__)), "sha256": sha(Path(__file__).read_bytes())},
    })
    config["sourceContract"] = {"path": contract["path"], "sha256": contract["sha256"]}
    batch = freeze_json(HERE / "batch.json", config)
    print(json.dumps(freeze_json(HERE / "coordinator-candidate-verification.json", {
        "batch": 128, "candidate": CANDIDATE, "base": BASE, "status": "PASS",
        "ownerSignature": "G", "worktreeClean": True, "changedPaths": changed, "packetFiles": len(inventory) + 1,
        "manifestSha256": sha(manifest_raw), "contentVersion": manifest["contentVersion"],
        "runtimeEntries": len(current), "baselineUnchangedEntries": len(previous) - 1,
        "sourceMembersPublishedBeforeBatch": 257, "sourceMembersInCandidate": 258,
        "baselineRuntimePreservedExceptDeclaredWordChange": True, "wordProseChanges": prose, "allActualRuntimeHashesChecked": True,
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

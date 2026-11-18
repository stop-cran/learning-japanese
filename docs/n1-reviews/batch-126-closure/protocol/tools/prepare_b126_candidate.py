"""Bind a clean signed B126 candidate to neutral sources and its actual gate evidence."""
import copy
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

from common import (
    CHECKS, GUARD_SHA, WS, freeze_json, frozen, git, json_bytes, load_module,
    require, sha, start_guard, write_frozen,
)
from confirm_v2 import clean
from verify_b126_sources import BASE, DISTRACTORS, FINGERPRINT, HERE, MEMBER, PREFIX

HELPER = WS / "scratch-124" / "review" / "prepare-source-contract.py"
HELPER_SHA = "1c626c4f2e49d5761d53926c70b5891ea00b63fc7a06383aeb7d5a076772a270"
ORDER = ("lint", "quiz-safety", "linkplan", "reading-exposure", "validate",
         "manifest", "unittest", "budget", "vocabulary", "manifest-rebuild")
JOYO_SHA = "cc740aed34751e40831e4ab526408401667a428cefcf0fdd0212848eb31d67cb"
JOYO_ROW = "\u5098\n\u30b5\u30f3 \u5098\u4e0b\uff0c\u843d\u4e0b\u5098\n\u304b\u3055 \u5098\uff0c\u96e8\u5098\uff0c\u65e5\u5098"
CONVERTER_SHA = "6993834d66221d23399547e5a17771d2d638dc68b2d08d47e9875ddc2c932081"


def verify_summary(value, mode, head, manifest_sha, runner_sha):
    require(
        value["batch"] == "126" and value["mode"] == mode and value["status"] == "PASS"
        and value["base"] == BASE and value["startingHead"] == head
        and value["checks"] == list(ORDER) and value["manifestSha256"] == manifest_sha
        and value["runnerSha256"] == runner_sha and value["guardSha256"] == GUARD_SHA
        and value["serial"] is True and value["waitTimeoutSeconds"] == 0.1
        and not value["finalMemory"]["breach"],
        "B126 gate summary differs from the actual snapshot, order or runner",
    )


def verify_serial(receipts):
    previous = None
    for name in ORDER:
        result = receipts[name]
        started = datetime.fromisoformat(result["startedAt"])
        completed = datetime.fromisoformat(result["completedAt"])
        require(started.tzinfo is not None and completed.tzinfo is not None
                and completed >= started and (previous is None or started >= previous),
                "Gate timestamps are invalid or overlap")
        previous = completed


def main(candidate, author_name, committed_name):
    require(re.fullmatch("[0-9a-f]{40}", candidate), "A full candidate SHA is required")
    for name in (author_name, committed_name):
        require(Path(name).name == name and name not in ("", ".", ".."), "Invalid gate directory")
    for name in ("batch.json", "source-contract", "source-contract.json", "candidate-inputs",
                 "coordinator-candidate-verification.json"):
        require(not (HERE / name).exists(), f"Preserve existing output: {name}")
    frozen(HELPER, HELPER_SHA)
    helper = load_module("b126_source_contract_helpers", HELPER)
    config = {"batch": 126, "candidate": candidate, "base": BASE, "members": [MEMBER],
              "repo": str(WS / "b126-worktree"), "expectedKanji": 1246,
              "gates": str(HERE / "candidate-inputs" / "committed")}
    clean(config, candidate)
    require(git(config, "show", "-s", "--format=%P|%G?|%GF|%ae|%ce", candidate).decode().strip()
            == f"{BASE}|G|{FINGERPRINT}|stop-cran@list.ru|stop-cran@list.ru",
            "Candidate parent, owner signature or identity differs")
    require(b"Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>"
            in git(config, "show", "-s", "--format=%B", candidate), "Missing commit trailer")
    signed, outputs, captures = {}, {}, {}

    def blob(path):
        raw = git(config, "show", f"{candidate}:{path}")
        signed[path] = sha(raw)
        return raw

    old = lambda path: git(config, "show", f"{BASE}:{path}")
    source = lambda name: blob(PREFIX + name)
    guard, _ = start_guard("B126 signed candidate and neutral evidence")
    try:
        proof_path = HERE / "source-selection-verification-001.json"
        proof_raw = frozen(proof_path)
        proof = json.loads(proof_raw)
        require(proof["batch"] == 126 and proof["candidate"] == candidate and proof["base"] == BASE
                and proof["status"] == "PASS" and not proof["memory"]["breach"]
                and proof["verifierSha256"] == sha(frozen(Path(__file__).with_name("verify_b126_sources.py"))),
                "Complete source proof is not bound to this candidate and verifier")
        require(len(proof["sourceRecords"]) == 4, "Four complete source selections required")
        for item in proof["sourceRecords"]:
            require(sha(blob(item["path"])) == item["sha256"], "Verified source selection changed")
        index_raw = blob("docs/n1-sources/source-index.json")
        community_raw = blob("docs/n1-sources/community-list-20261102.json")
        require(index_raw == old("docs/n1-sources/source-index.json")
                and community_raw == old("docs/n1-sources/community-list-20261102.json")
                and json.loads(community_raw)[69] == MEMBER, "Frozen membership changed")
        index = json.loads(index_raw)
        row = next(item for item in index if item["kanji"] == MEMBER)
        require(row == json.loads(source("source-row.json")) and row["sourceRow"] == 70
                and row["statusAtFreeze"] == "pending", "Wrong source row")
        receipt = json.loads(source("source-receipt.json"))
        require(receipt["batch"] == "126" and receipt["baseCommit"] == BASE
                and receipt["membership"] == {"sourceIndexSha256": sha(index_raw),
                    "communitySha256": sha(community_raw), "row": 70, "kanji": MEMBER},
                "Source receipt membership differs")
        for kind in ("jmdict", "kanjidic2"):
            for key in ("filename", "compressedSha256", "decompressedXmlSha256"):
                require(receipt["dictionaryInputs"][kind][key] == proof["inputs"][kind][key],
                        "Dictionary input declaration differs")
        for name, binding in receipt["files"].items():
            raw = source(name)
            require(sha(raw) == binding["sha256"] and len(raw) == binding["bytes"],
                    f"Original source-receipt binding differs: {name}")
        inventory = json.loads(source("packet-files.json"))["files"]
        for name, binding in inventory.items():
            raw = source(name)
            require(sha(raw) == binding["sha256"] and len(raw) == binding["bytes"],
                    f"Final source inventory differs: {name}")
            guard.check()

        sys.path.insert(0, str(WS / "lean"))
        from n1lib import parse
        selection = json.loads(source("selection.json"))
        updated = json.loads(source("selection-002.json"))
        card, body = parse(blob(f"kanji/{MEMBER}.md").decode().replace("\r\n", "\n"))
        for key in ("onyomi", "kunyomi", "radical"):
            require(card[key] == row["metadata"][key], f"Source metadata changed: {key}")
        for key in ("strokes", "radicalNumber"):
            require(card[key] == str(row["metadata"][key]), f"Source metadata changed: {key}")
        require(card["kanji"] == MEMBER and card["jlpt"] == "1"
                and card["distractors"] == DISTRACTORS == updated["curatedChoices"]
                and card["quiz_exclusions"] == updated["directMeaningGuards"]
                and card["quizOnyomi"] == selection["quizOnyomi"] == []
                and card["quizKunyomi"] == selection["quizKunyomi"] == ["\u304b\u3055"]
                and updated["comparisonCards"] == proof["comparisonCards"],
                "Card or comparison selection differs")
        require(selection["membership"] == [{"kanji": MEMBER, "sourceRow": 70}]
                and selection["declaringArticlesAtBase"] == [MEMBER]
                and selection["requiredReciprocalPairs"] == [[MEMBER, MEMBER]]
                and f"](../words/{MEMBER}.md)" in body, "Support selection differs")
        word_path = f"words/{MEMBER}.md"
        require(source(f"baseline-{MEMBER}.md") == old(word_path)
                and helper.single_wrapper(old(word_path), blob(word_path), MEMBER),
                "Support edit is not a single reciprocal wrapper")
        manifest_raw = blob("manifest.json")
        manifest, baseline = json.loads(manifest_raw), json.loads(old("manifest.json"))
        flatten = lambda value: {path: digest for items in value.values() if isinstance(items, dict)
                                 for path, digest in items.items()}
        current, previous = flatten(manifest), flatten(baseline)
        additions = {f"kanji/{MEMBER}.md", f"strokes/{MEMBER}.json"}
        require(current.keys() - previous.keys() == additions and previous.keys() <= current.keys()
                and {path for path in previous if current[path] != previous[path]} == {word_path},
                "Unexpected runtime delta")
        for path in additions | {word_path}:
            require(sha(blob(path).replace(b"\r\n", b"\n")) == current[path], "Runtime hash differs")
        changed = {}
        for line in git(config, "diff", "--name-status", "--no-renames", BASE, candidate).decode().splitlines():
            status, path = line.split("\t", 1)
            changed[path] = status
            require((status == "A" and (path in additions or path.startswith(PREFIX)
                                       or path == "docs/n1-sources/batch-126-progress.json"))
                    or (status == "M" and path in {word_path, "manifest.json", "docs/n1-authoring-notes.md"}),
                    f"Unexpected changed file: {status} {path}")
            if path.startswith("docs/"):
                blob(path)
        require({path[len(PREFIX):] for path in changed if path.startswith(PREFIX)}
                == set(inventory) | {"packet-files.json"}, "Signed packet inventory is incomplete")
        notes = blob("docs/n1-authoring-notes.md").replace(b"\r\n", b"\n")
        stripped, count = re.subn(rb"(?m)^## Batch 126:.*?\n(?=## Batch )", b"", notes, flags=re.S)
        require(count == 1 and stripped == old("docs/n1-authoring-notes.md").replace(b"\r\n", b"\n"),
                "Authoring notes change exceeds the new B126 section")
        pending = {item["kanji"] for item in index if item["statusAtFreeze"] == "pending"}
        represented = lambda files: {Path(name).stem for name in files if name.startswith("kanji/")}
        require(len(pending & represented(previous)) == 255 and len(pending & represented(current)) == 256
                and len(represented(current)) == 1246, "Membership accounting differs")
        progress = json.loads(blob("docs/n1-sources/batch-126-progress.json"))
        require(progress["baseCommit"] == BASE and progress["membership"] == [MEMBER]
                and progress["sourceRows"] == [70] and progress["published"] == progress["reviewClosed"] == []
                and progress["runtimePublished"] is False
                and progress["accounting"]["publishedPendingRecordsWithCards"] == 255
                and progress["accounting"]["undelivered"] == 973
                and progress["accounting"]["overallN1TaskComplete"] is False
                and progress["runtimeCandidate"]["manifestSha256"] == sha(manifest_raw)
                and progress["runtimeCandidate"]["contentVersion"] == manifest["contentVersion"],
                "Premature publication claim or mismatched candidate accounting")
        declaring = []
        for path, digest in baseline["files"].items():
            if not path.startswith("words/"):
                continue
            raw = (Path(config["repo"]) / Path(path)).read_bytes().replace(b"\r\n", b"\n")
            require(sha(raw) == current[path], f"Active word differs from candidate: {path}")
            metadata, _ = parse(raw.decode())
            if metadata and MEMBER in metadata.get("kanji", []):
                declaring.append(Path(path).stem)
            guard.check()
        require(declaring == [MEMBER], "Required reciprocal pair inventory differs")

        jm = helper.merge_records([source("jmdict-selected-records.xml")], "entry", "ent_seq")
        kd = helper.merge_records([blob(item["path"]) for item in proof["sourceRecords"]
                                   if "kanjidic2" in item["path"]], "character", "literal")
        require(set(kd) == {MEMBER} | set(proof["comparisonCards"]), "Neutral character scope differs")
        queries = helper.query_index(jm, set(), MEMBER, [])
        for name, tag, entries in (
            ("jmdict-families.xml", "JMdict", [jm[key] for key in sorted(jm, key=int)]),
            ("kanjidic2-records.xml", "kanjidic2",
             [kd[MEMBER]] + [kd[key] for key in sorted(set(kd) - {MEMBER})]),
        ):
            root = ET.Element(tag)
            root.extend(copy.deepcopy(entry) for entry in entries)
            outputs[name] = ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"
        converter_path = Path(config["repo"]) / "tools" / "generate_strokes.py"
        require(converter_path.read_bytes() == blob("tools/generate_strokes.py")
                and sha(converter_path.read_bytes()) == CONVERTER_SHA, "Pinned converter changed")
        converter = load_module("b126_verified_converter", converter_path)
        svg = source("05098.svg")
        svg_blob = hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest()
        require(svg_blob == row["kanjivgInventory"]["sha"] == receipt["kanjivg"]["gitBlob"]
                and sha(svg) == receipt["kanjivg"]["sha256"]
                and converter.convert(MEMBER, svg.decode()) == json.loads(blob(f"strokes/{MEMBER}.json")),
                "Generated strokes do not reproduce")
        outputs["kvg/05098.svg"] = svg
        from fontTools.ttLib import TTFont
        app = WS / "kanji-cards-android"
        app_config = {"repo": str(app)}
        app_head = git(app_config, "rev-parse", "HEAD").decode().strip()
        font_evidence = []
        for name in ("kanji_brush.ttf", "kanji_mincho.ttf", "kanji_textbook.ttf"):
            relative = "app/src/main/res/font/" + name
            path = app / Path(relative)
            raw = path.read_bytes()
            require(raw == git(app_config, "show", f"{app_head}:{relative}"), "Bundled font differs from app HEAD")
            with TTFont(path) as font:
                cmap = font.getBestCmap()
                coverage = {f"U+{ord(char):04X}": ord(char) in cmap for char in MEMBER + "\u4eba\u5341"}
            font_evidence.append({"path": relative, "sha256": sha(raw), "coverage": coverage})
            guard.check()
        declared_fonts = json.loads(source("stroke-font-evidence.json"))
        require(declared_fonts["converterSha256"] == CONVERTER_SHA
                and declared_fonts["strokeSha256"] == sha(blob(f"strokes/{MEMBER}.json"))
                and declared_fonts["svgSha256"] == sha(svg)
                and {entry["filename"]: (entry["sha256"], entry["coverage"]) for entry in declared_fonts["fonts"]}
                == {Path(entry["path"]).name: (entry["sha256"], entry["coverage"]) for entry in font_evidence},
                "Author's font or stroke receipt differs")
        outputs["shape-evidence.json"] = json_bytes([{
            "kanji": MEMBER, "revision": converter.KANJIVG_REVISION, "gitBlobSha1": svg_blob,
            "sourcePath": "kanji/05098.svg", "sha256": sha(svg), "canonicalStrokes": 12,
            "groups": [dict(node.attrib) for node in ET.fromstring(svg).iter("{http://www.w3.org/2000/svg}g")],
            "bundledFonts": {"appSnapshot": app_head, "files": font_evidence},
            "scope": "Canonical source and bundled-font cmap coverage, not rendered or device acceptance.",
        }])
        joyo_raw = (WS / "scratch-111" / "joyo-pages.json").read_bytes()
        require(sha(joyo_raw) == JOYO_SHA and JOYO_ROW in json.loads(joyo_raw)["62"], "Pinned Joyo row differs")
        outputs["joyo-rows.json"] = json_bytes({
            "cacheSha256": sha(joyo_raw), "scope": "Pinned cached text, not fresh PDF glyph inspection.",
            "rows": [{"kanji": MEMBER, "matches": [{"printedPage": 62, "extract": JOYO_ROW}]}],
        })
        runner_path = WS / "scratch-126" / "run_b126_gates.py"
        runner_sha = sha(runner_path.read_bytes())
        gate_groups = {}
        for mode, directory_name in (("author", author_name), ("committed", committed_name)):
            directory = WS / "scratch-126" / directory_name
            summary_raw = (directory / "summary.json").read_bytes()
            summary = json.loads(summary_raw)
            verify_summary(summary, mode, BASE if mode == "author" else candidate, sha(manifest_raw), runner_sha)
            bindings = helper.gate_bindings(directory, config, sha(manifest_raw), runner_sha, guard)
            receipts = {}
            for entry in bindings:
                name = entry["gate"]
                raw = (directory / f"{name}.json").read_bytes()
                log = (directory / f"{name}.log").read_bytes()
                require(sha(raw) == entry["receiptSha256"] == summary["logs"][name]["receiptSha256"]
                        and sha(log) == entry["logSha256"] == summary["logs"][name]["logSha256"],
                        "Gate input changed during capture")
                receipts[name] = json.loads(raw)
                captures[f"{mode}/{name}.json"] = raw
                captures[f"{mode}/{name}.log"] = log
                if mode == "author":
                    require(raw == source(f"{directory_name}/{name}.json")
                            and log == source(f"{directory_name}/{name}.log"), "Signed author gates differ")
            verify_serial(receipts)
            captures[f"{mode}/summary.json"] = summary_raw
            if mode == "author":
                require(summary_raw == source(f"{directory_name}/summary.json")
                        and sha(summary_raw) == progress["authorGates"]["summarySha256"],
                        "Signed author summary differs")
            gate_groups[mode] = {"sourceDirectory": str(directory), "summarySha256": sha(summary_raw),
                                 "gates": bindings}
        captures["run_b126_gates.py"] = runner_path.read_bytes()
        require(sha(captures["run_b126_gates.py"]) == runner_sha, "Gate runner changed during capture")
        outputs["selection.json"] = json_bytes({"order": [MEMBER], "sourceRows": [70]})
        outputs["evidence-index.json"] = json_bytes({
            "outputs": {name: sha(raw) for name, raw in outputs.items()},
            "completeDictionaryEntries": len(jm), "dictionaryQueryEntries": queries,
        })
        clean(config, candidate)
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Candidate verification RAM breach")
    captured = {name: write_frozen(HERE / "candidate-inputs" / name, raw) for name, raw in captures.items()}
    bindings = {name: write_frozen(HERE / "source-contract" / name, raw) for name, raw in outputs.items()}
    contract = freeze_json(HERE / "source-contract.json", {
        "batch": 126, "candidate": candidate, "base": BASE, "files": bindings, "signedSources": signed,
        "method": "Complete signed records independently checked against pinned inputs. Duplicate identities "
                  "merged only after structural equality; XML reserialized, not raw compressed slices. "
                  "No author judgments exported.",
        "dictionaryVerification": {"path": str(proof_path), "sha256": sha(proof_raw)},
        "tool": {"path": str(Path(__file__)), "sha256": sha(Path(__file__).read_bytes())},
    })
    config["sourceContract"] = {"path": contract["path"], "sha256": contract["sha256"]}
    batch = freeze_json(HERE / "batch.json", config)
    print(json.dumps(freeze_json(HERE / "coordinator-candidate-verification.json", {
        "batch": 126, "candidate": candidate, "base": BASE, "status": "PASS",
        "ownerSignature": "G", "worktreeClean": True, "changedPaths": changed,
        "manifestSha256": sha(manifest_raw), "contentVersion": manifest["contentVersion"],
        "runtimeEntries": len(current), "sourceMembersPublishedBeforeBatch": 255,
        "sourceMembersInCandidate": 256, "baselineRuntimePreservedExceptRequiredWrappers": True,
        "sourceContract": contract, "batchConfig": batch, "gates": gate_groups,
        "capturedGateInputs": captured, "captureScope": "Verified post-execution ReadOnly copies, not retrospective immutability.",
        "completeSourceVerification": sha(proof_raw), "bundledFontEvidence": font_evidence,
        "reusedHelper": {"path": str(HELPER), "sha256": HELPER_SHA}, "memory": memory,
        "limits": "Mechanical signed-candidate/source/gate binding only; linguistic review, arbitrary-pool, "
                  "native/device, CI, served-ZIP and publication acceptance remain open.",
    })))


if __name__ == "__main__":
    require(len(sys.argv) == 4, "Usage: prepare_b126_candidate.py CANDIDATE_SHA AUTHOR_GATES COMMITTED_GATES")
    main(*sys.argv[1:])

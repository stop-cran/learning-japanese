"""Bind the actual B125 evidence schema to the existing blind-review protocol."""
import copy
import hashlib
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from common import (CHECKS, WS, freeze_json, frozen, git, json_bytes, load_module,
                    require, sha, start_guard, write_frozen)
from confirm_v2 import clean
from verify_b125_sources import (
    BASE, CANDIDATE, COMPARISONS, FALLBACK, FALLBACKS, HERE, MEMBER, PREFIX, QUERIES, SUPPLEMENT,
)

sys.path.insert(0, str(WS / "lean"))
from n1lib import parse

WORD = "\u4fb5\u5165"
HELPER = WS / "scratch-124" / "review" / "prepare-source-contract.py"
HELPER_SHA = "1c626c4f2e49d5761d53926c70b5891ea00b63fc7a06383aeb7d5a076772a270"
GATE_RUNNER_SHA = "9fb4798ae74402ea149d207c02b0b4a2a6e5c4b55bf62a1b58a2f61a38d3c1ef"
BOUNDED_RUNNER_SHA = "ecccdbaa897600e9842865d335ab4b73a5d51b33c64c250f2c3ae60d715ba299"
FINGERPRINT = "D4C9A275A218AF747B787AFA9D94B9D311BD26A7"


def verify_summary(value, mode, head, manifest_sha):
    require(value["batch"] == 125 and value["mode"] == mode and value["head"] == head
            and value["base"] == BASE and value["status"] == "PASS"
            and len(value["checks"]) == len(CHECKS) and set(value["checks"]) == set(CHECKS)
            and value["manifestSha256"] == manifest_sha
            and value["runnerSha256"] == GATE_RUNNER_SHA
            and value["boundedRunnerSha256"] == BOUNDED_RUNNER_SHA,
            "B125 gate summary differs from snapshot or runner")


def main():
    for name in ("batch.json", "source-contract", "source-contract.json",
                 "coordinator-candidate-verification.json"):
        require(not (HERE / name).exists(), f"Preserve output: {name}")
    frozen(HELPER, HELPER_SHA)
    helpers = load_module("b125_candidate_helpers", HELPER)
    config = {
        "batch": 125, "candidate": CANDIDATE, "base": BASE,
        "repo": str(WS / "b125-worktree"), "gates": str(WS / "scratch-125" / "committed-gates-001"),
        "members": [MEMBER], "expectedKanji": 1245,
    }
    clean(config, CANDIDATE)
    signature = git(config, "show", "-s", "--format=%P|%GF", CANDIDATE).decode().strip()
    require(signature == BASE + "|" + FINGERPRINT, "Candidate parent or signer differs")
    require(b"Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>"
            in git(config, "show", "-s", "--format=%B", CANDIDATE), "Commit trailer missing")
    signed = {}

    def blob(name):
        raw = git(config, "show", f"{CANDIDATE}:{name}")
        signed[name] = sha(raw)
        return raw

    def old(name):
        return git(config, "show", f"{BASE}:{name}")

    guard, _ = start_guard("B125 signed candidate binding")
    outputs = {}
    try:
        proof_raw = frozen(HERE / "source-selection-verification-001.json",
                           "9f354ac623723f9e07116c01aeb1e6987117526387ef405517746661f4cb5573")
        proof = json.loads(proof_raw)
        require(proof["batch"] == 125 and proof["candidate"] == CANDIDATE
                and proof["base"] == BASE and proof["status"] == "PASS"
                and not proof["memory"]["breach"]
                and proof["verifierSha256"] == sha((Path(__file__).parent / "verify_b125_sources.py").read_bytes()),
                "Source proof differs")
        require(len(proof["sourceRecords"]) == 6, "Six source selections required")
        for record in proof["sourceRecords"]:
            require(sha(blob(record["path"])) == record["sha256"], "Verified source changed")

        receipt_names = [(PREFIX, "source-receipt.json", "extract.py"),
                         (SUPPLEMENT, "receipt.json", "supplement.py"),
                         (FALLBACK, "receipt.json", "fallback.py")]
        receipts = {}
        for folder, name, producer in receipt_names:
            receipt = json.loads(blob(folder + name))
            require(receipt["baseCommit"] == BASE, "Source receipt base differs")
            require(receipt["producerSha256"] == sha((WS / "scratch-125" / producer).read_bytes()),
                    "Source producer changed")
            for relative, digest in receipt["files"].items():
                raw = blob(folder + relative)
                require(sha(raw) == digest, f"Source binding differs: {folder + relative}")
                if relative.startswith("comparison-cards/"):
                    require(raw == old("kanji/" + Path(relative).name), "Comparison is not exact base copy")
                guard.check()
            receipts[folder] = receipt
        receipt = receipts[PREFIX]
        require(receipt["membership"] == [{"kanji": MEMBER, "sourceRow": 48}]
                and receipt["declaringArticlesAtBase"] == [WORD]
                and receipt["requiredReciprocalPairs"] == [[WORD, MEMBER]], "Source membership differs")
        for kind, verified_input in proof["inputs"].items():
            for key in ("compressedSha256", "decompressedXmlSha256"):
                require(receipt["dictionaryInputs"][kind][key] == verified_input[key]
                        == receipts[SUPPLEMENT]["inputs"][kind][key], "Dictionary input hash differs")
        require(receipts[FALLBACK]["sourceCompressedSha256"]
                == proof["inputs"]["kanjidic2"]["compressedSha256"]
                and receipts[FALLBACK]["sourceXmlSha256"]
                == proof["inputs"]["kanjidic2"]["decompressedXmlSha256"], "Fallback input differs")

        index_raw = blob("docs/n1-sources/source-index.json")
        community_raw = blob("docs/n1-sources/community-list-20261102.json")
        require(index_raw == old("docs/n1-sources/source-index.json")
                and sha(index_raw) == receipt["sourceIndexSha256"], "Source index changed")
        require(community_raw == old("docs/n1-sources/community-list-20261102.json")
                and sha(community_raw) == receipt["communitySourceSha256"]
                and json.loads(community_raw)[47] == MEMBER, "Community source changed")
        index = json.loads(index_raw)
        row = next(item for item in index if item["kanji"] == MEMBER)
        require(row == json.loads(blob(PREFIX + "source-row.json"))
                and row["sourceRow"] == 48 and row["statusAtFreeze"] == "pending", "Wrong frozen row")
        selection = json.loads(blob(PREFIX + "selection.json"))
        card, body = parse(blob(f"kanji/{MEMBER}.md").decode().replace("\r\n", "\n"))
        require(card["kanji"] == MEMBER and card["jlpt"] == "1"
                and card["onyomi"] == row["metadata"]["onyomi"]
                and card["kunyomi"] == row["metadata"]["kunyomi"]
                and card["strokes"] == str(row["metadata"]["strokes"])
                and card["radical"] == row["metadata"]["radical"]
                and card["radicalNumber"] == str(row["metadata"]["radicalNumber"]), "Source metadata differs")
        require(card["distractors"] == selection["distractors"]
                and card["quiz_exclusions"] == selection["directMeaningGuards"]
                and selection["requiredReciprocalPairs"] == [[WORD, MEMBER]], "Selection differs")
        require(f"](../words/{WORD}.md)" in body, "Missing support link")
        require(blob(PREFIX + f"baseline-{WORD}.md") == old(f"words/{WORD}.md")
                and helpers.single_wrapper(old(f"words/{WORD}.md"), blob(f"words/{WORD}.md"), MEMBER),
                "Support edit exceeds one link wrapper")

        manifest_raw = blob("manifest.json")
        manifest, baseline = json.loads(manifest_raw), json.loads(old("manifest.json"))
        flatten = lambda value: {p: h for entries in value.values() if isinstance(entries, dict)
                                 for p, h in entries.items()}
        current, previous = flatten(manifest), flatten(baseline)
        additions = {f"kanji/{MEMBER}.md", f"strokes/{MEMBER}.json"}
        changes = {f"words/{WORD}.md"}
        require(current.keys() - previous.keys() == additions and previous.keys() <= current.keys()
                and {path for path in previous if previous[path] != current[path]} == changes,
                "Unexpected runtime delta")
        for path in additions | changes:
            require(sha(blob(path).replace(b"\r\n", b"\n")) == current[path], "Runtime hash differs")
        changed = {}
        for line in git(config, "diff", "--name-status", "--no-renames", BASE, CANDIDATE).decode().splitlines():
            status, path = line.split("\t", 1)
            changed[path] = status
            require((path in additions and status == "A") or (path in changes | {"manifest.json"} and status == "M")
                    or (status == "A" and (path.startswith((PREFIX, SUPPLEMENT, FALLBACK))
                                          or path == "docs/n1-sources/batch-125-progress.json")),
                    f"Unexpected changed file: {status} {path}")
            if path.startswith("docs/"):
                blob(path)
        pending = {item["kanji"] for item in index if item["statusAtFreeze"] == "pending"}
        represented = lambda files: {Path(name).stem for name in files if name.startswith("kanji/")}
        require(len(pending & represented(previous)) == 254 and len(pending & represented(current)) == 255
                and len(represented(current)) == 1245, "Candidate membership totals differ")
        progress = json.loads(blob("docs/n1-sources/batch-125-progress.json"))
        require(progress["membership"] == [MEMBER] and progress["sourceRows"] == [48]
                and progress["published"] == progress["reviewClosed"] == []
                and progress["runtimePublished"] is False
                and progress["accounting"]["publishedPendingRecordsWithCards"] == 254
                and progress["accounting"]["undelivered"] == 974
                and progress["accounting"]["overallN1TaskComplete"] is False, "Premature delivery claim")
        declaring = []
        for name, digest in baseline["files"].items():
            if name.startswith("words/"):
                raw = (Path(config["repo"]) / Path(name)).read_bytes().replace(b"\r\n", b"\n")
                if name not in changes:
                    require(sha(raw) == digest, f"Baseline word changed: {name}")
                metadata, _ = parse(raw.decode())
                if metadata and MEMBER in metadata.get("kanji", []):
                    declaring.append(Path(name).stem)
        require(declaring == [WORD], "Missing active reciprocal pair")

        jm = helpers.merge_records([blob(PREFIX + "jmdict-selected-records.xml"),
                                    blob(SUPPLEMENT + "jmdict-records.xml")], "entry", "ent_seq")
        kd = helpers.merge_records([blob(record["path"]) for record in proof["sourceRecords"]
                                    if "kanjidic2" in record["path"]], "character", "literal")
        require(set(kd) == {MEMBER} | COMPARISONS | FALLBACKS, "Wrong neutral character scope")
        query_ids = helpers.query_index(jm, QUERIES, MEMBER, [])
        for name, root_tag, entries in (
            ("jmdict-families.xml", "JMdict", [jm[key] for key in sorted(jm, key=int)]),
            ("kanjidic2-records.xml", "kanjidic2", [kd[MEMBER]] + [kd[key] for key in sorted(set(kd) - {MEMBER})]),
        ):
            root = ET.Element(root_tag)
            root.extend(copy.deepcopy(entry) for entry in entries)
            outputs[name] = ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"
        converter_path = Path(config["repo"]) / "tools" / "generate_strokes.py"
        require(converter_path.read_bytes() == blob("tools/generate_strokes.py")
                and sha(converter_path.read_bytes()) == "6993834d66221d23399547e5a17771d2d638dc68b2d08d47e9875ddc2c932081",
                "Pinned converter changed")
        converter = load_module("b125_verified_converter", converter_path)
        svg = blob(PREFIX + "04fb5.svg")
        svg_blob = hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest()
        require(svg_blob == row["kanjivgInventory"]["sha"] == receipt["kanjivg"]["gitBlob"]
                and converter.convert(MEMBER, svg.decode()) == json.loads(blob(f"strokes/{MEMBER}.json")),
                "Stroke geometry does not reproduce")
        outputs["kvg/04fb5.svg"] = svg
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
                coverage = {f"U+{ord(char):04X}": ord(char) in cmap for char in MEMBER + "\u4eba\u4ebb"}
            font_evidence.append({"path": relative, "sha256": sha(raw), "coverage": coverage})
            guard.check()
        outputs["shape-evidence.json"] = json_bytes([{
            "kanji": MEMBER, "revision": converter.KANJIVG_REVISION, "gitBlobSha1": svg_blob,
            "sourcePath": "kanji/04fb5.svg", "sha256": sha(svg), "canonicalStrokes": 9,
            "groups": [dict(node.attrib) for node in ET.fromstring(svg).iter("{http://www.w3.org/2000/svg}g")],
            "bundledFonts": {"appSnapshot": app_head, "files": font_evidence},
            "scope": "Canonical source and exact bundled-font cmap coverage, not rendered glyph or device acceptance.",
        }])
        joyo_raw = (WS / "scratch-111" / "joyo-pages.json").read_bytes()
        joyo_row = "\u4fb5\n\u30b7\u30f3 \u4fb5\u5165\uff0c\u4fb5\u5bb3\uff0c\u4e0d\u53ef\u4fb5\n\u304a\u304b\u3059 \u4fb5\u3059 \u21d4 \u72af\u3059\uff0c\u5192\u3059"
        require(sha(joyo_raw) == "cc740aed34751e40831e4ab526408401667a428cefcf0fdd0212848eb31d67cb"
                and joyo_row in json.loads(joyo_raw)["84"], "Pinned Joyo row differs")
        outputs["joyo-rows.json"] = json_bytes({
            "cacheSha256": sha(joyo_raw), "scope": "Pinned cached text, not fresh PDF glyph inspection.",
            "rows": [{"kanji": MEMBER, "matches": [{"printedPage": 84, "extract": joyo_row}]}],
        })
        require(sha((WS / "scratch-125" / "run-gates.py").read_bytes()) == GATE_RUNNER_SHA
                and sha((WS / "scratch-124" / "run-reconciliation-002-checks.py").read_bytes()) == BOUNDED_RUNNER_SHA,
                "Gate producer changed")
        gate_groups = {}
        for mode in ("author", "committed"):
            directory = WS / "scratch-125" / f"{mode}-gates-001"
            summary_raw = (directory / "summary.json").read_bytes()
            verify_summary(json.loads(summary_raw), mode, BASE if mode == "author" else CANDIDATE, sha(manifest_raw))
            gate_groups[mode] = {
                "summarySha256": sha(summary_raw),
                "gates": helpers.gate_bindings(directory, config, sha(manifest_raw), BOUNDED_RUNNER_SHA, guard),
            }
        outputs["selection.json"] = json_bytes({"order": [MEMBER], "sourceRows": [48]})
        outputs["evidence-index.json"] = json_bytes({
            "outputs": {name: sha(raw) for name, raw in outputs.items()},
            "completeDictionaryEntries": len(jm), "dictionaryQueryEntries": query_ids,
        })
        clean(config, CANDIDATE)
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Candidate verification RAM breach")
    bindings = {name: write_frozen(HERE / "source-contract" / name, raw) for name, raw in outputs.items()}
    contract = freeze_json(HERE / "source-contract.json", {
        "batch": 125, "candidate": CANDIDATE, "base": BASE, "files": bindings, "signedSources": signed,
        "method": "Complete signed target, exact-spelling supplement and fallback character records, "
                  "independently verified against pinned inputs. Duplicate identities merged only after "
                  "structural equality; XML reserialized, not raw compressed slices. No author judgments exported.",
        "dictionaryVerification": {"path": str(HERE / "source-selection-verification-001.json"),
                                   "sha256": sha(proof_raw)},
        "tool": {"path": str(Path(__file__)), "sha256": sha(Path(__file__).read_bytes())},
    })
    config["sourceContract"] = {"path": contract["path"], "sha256": contract["sha256"]}
    batch = freeze_json(HERE / "batch.json", config)
    print(json.dumps(freeze_json(HERE / "coordinator-candidate-verification.json", {
        "batch": 125, "candidate": CANDIDATE, "base": BASE, "status": "PASS",
        "ownerSignature": "G", "worktreeClean": True, "changedPaths": changed,
        "manifestSha256": sha(manifest_raw), "contentVersion": manifest["contentVersion"],
        "runtimeEntries": len(current), "sourceMembersPublishedBeforeBatch": 254,
        "sourceMembersInCandidate": 255, "baselineRuntimePreservedExceptRequiredWrappers": True,
        "sourceContract": contract, "batchConfig": batch, "gates": gate_groups,
        "completeSourceVerification": sha(proof_raw), "bundledFontEvidence": font_evidence,
        "reusedHelper": {"path": str(HELPER), "sha256": HELPER_SHA}, "memory": memory,
        "limits": "Mechanical signed-candidate/source/gate binding only; linguistic reviews, "
                  "arbitrary-pool, native/device, CI, served-ZIP and publication acceptance remain open.",
    })))


if __name__ == "__main__":
    main()

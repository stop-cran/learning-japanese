"""Bind B129's signed runtime delta, source metadata, support links and geometry."""
import hashlib
import json
import re
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, load_module, require, sha, start_guard
from verify_b129_sources import FINGERPRINT, Git, ORIGIN, OWNER, TRAILER

BASE = "20fda42f7b456889ae4ef82650dde227a139917c"
MEMBERS = ["\u8309", "\u7d79", "\u8679"]
SUPPORTS = {"\u8309": ["\u8309\u8389\u82b1"], "\u7d79": ["\u7d79"], "\u8679": ["\u8679"]}
REPO = WS / "b129-worktree"
HERE = WS / "scratch-129" / "review"
PREFIX = "docs/n1-sources/batch-129/"
SOURCE_VERIFIER_SHA = "9fb0aa1b179679638865582eed251f2c4fd4c9a84707f56099383808b18d0b33"
RUNNER = {"path": str(HERE / "guarded-test-v3.py"),
          "sha256": "9326cabd53fb1ac18417dcc1f39d4316af8f1b0a945bf7523a9e73a7044a6848"}
LINK_HELPER = WS / "scratch-124" / "review" / "prepare-source-contract.py"
LINK_HELPER_SHA = "1c626c4f2e49d5761d53926c70b5891ea00b63fc7a06383aeb7d5a076772a270"
CONVERTER_SHA = "6993834d66221d23399547e5a17771d2d638dc68b2d08d47e9875ddc2c932081"
BINARY_SECTIONS = {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}


def runtime_entries(manifest):
    result = {}
    for section, entries in manifest.items():
        if not isinstance(entries, dict):
            continue
        for name, digest in entries.items():
            require(name not in result, f"Duplicate manifest path: {name}")
            result[name] = (digest, section in BINARY_SECTIONS)
    return result


def verify_runtime_delta(before, after, added, words):
    require(after.keys() - before.keys() == added and before.keys() <= after.keys(),
            "Unexpected added or removed runtime paths")
    require(all(after[name][1] == before[name][1] for name in before),
            "Existing runtime file changed binary/text classification")
    require({name for name in before if after[name] != before[name]} == words,
            "Existing runtime hashes changed beyond supporting words")


def verify_metadata(card, row):
    char, source = row["kanji"], row["metadata"]
    require(card["kanji"] == char and card["jlpt"] == "1" and "jlpt-n1" in card["tags"],
            f"Card identity or N1 placement differs: {char}")
    for key in ("onyomi", "kunyomi", "radical"):
        require(card[key] == source[key], f"Complete source metadata differs: {char}/{key}")
    for key in ("strokes", "radicalNumber"):
        require(card[key] == str(source[key]), f"Source scalar differs: {char}/{key}")
    require(set(card["quizOnyomi"]) <= set(card["onyomi"])
            and set(card["quizKunyomi"]) <= set(card["kunyomi"])
            and (card["quizOnyomi"] or card["quizKunyomi"]),
            f"Practice readings are not a nonempty source subset: {char}")


def main(proof_path, expected_sha, output):
    proof_path, output = Path(proof_path).resolve(), Path(output).resolve()
    require(proof_path.parent == output.parent == HERE and not output.exists(),
            "Use frozen proof and a new output in B129 review")
    source_module = Path(__file__).with_name("verify_b129_sources.py")
    frozen(source_module, SOURCE_VERIFIER_SHA)
    proof_raw = frozen(proof_path, expected_sha)
    proof = json.loads(proof_raw)
    candidate = proof["candidate"]
    require(re.fullmatch("[0-9a-f]{40}", candidate) is not None
            and proof["batch"] == 129 and proof["base"] == BASE and proof["status"] == "PASS"
            and proof["checkoutBound"] is True and not proof["memory"]["breach"]
            and proof["verifierSha256"] == SOURCE_VERIFIER_SHA
            and [item["kanji"] for item in proof["members"]] == MEMBERS,
            "Source proof does not bind B129's signed candidate")
    frozen(LINK_HELPER, LINK_HELPER_SHA)
    link_helper = load_module("b129_link_preservation", LINK_HELPER)
    sys.path.insert(0, str(WS / "lean"))
    from n1lib import parse
    guard, _ = start_guard("B129 signed payload verification")
    git = Git(REPO, RUNNER, guard)

    def blob(path, commit=candidate):
        return git("show", f"{commit}:{path}")

    def clean():
        require(git("rev-parse", "HEAD").decode().strip() == candidate
                and not git("status", "--porcelain=v1", "--untracked-files=all"),
                "Signed candidate checkout changed")

    try:
        clean()
        require(git("remote", "get-url", "origin").decode().strip() == ORIGIN, "Wrong origin")
        require(git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", candidate).decode().strip()
                == f"{BASE}|G|{FINGERPRINT}|{OWNER}|{OWNER}", "Signature, owner or parent differs")
        signature = git("verify-commit", candidate, include_stderr=True)
        require(TRAILER in git("show", "-s", "--format=%B", candidate), "Missing coauthor trailer")
        for record in proof["sourceRecords"]:
            require(sha(blob(record["path"])) == record["sha256"], "Verified source record changed")
            guard.check()
        selection_raw, rows_raw = blob(PREFIX + "selection.json"), blob(PREFIX + "source-rows.json")
        require(sha(selection_raw) == proof["selectionSha256"]
                and sha(rows_raw) == proof["sourceRowsSha256"], "Verified source selection changed")
        selection, rows = json.loads(selection_raw), json.loads(rows_raw)
        require([row["kanji"] for row in rows] == MEMBERS, "Source-row order differs")
        added = {f"{kind}/{char}.{extension}" for char in MEMBERS
                 for kind, extension in (("kanji", "md"), ("strokes", "json"))}
        word_paths = {f"words/{word}.md" for words in SUPPORTS.values() for word in words}
        changed = {}
        for line in git("diff", "--name-status", "--no-renames", BASE, candidate).decode("utf-8").splitlines():
            status, path = line.split("\t", 1)
            require(
                (status == "A" and (path in added or path.startswith(PREFIX)
                                   or path == "docs/n1-sources/batch-129-progress.json"))
                or (status == "M" and path in word_paths | {"manifest.json", "docs/n1-authoring-notes.md"}),
                f"Out-of-scope change: {status} {path}")
            changed[path] = status
        require(added | word_paths <= changed.keys(), "Missing runtime additions or reciprocal changes")
        manifest_raw = blob("manifest.json")
        require((REPO / "manifest.json").read_bytes() == manifest_raw,
                "Working manifest differs from the signed candidate")
        manifest = json.loads(manifest_raw)
        current = runtime_entries(manifest)
        previous = runtime_entries(json.loads(blob("manifest.json", BASE)))
        verify_runtime_delta(previous, current, added, word_paths)
        require(len(previous) == 8718 and len(current) == 8724, "Unexpected runtime entry counts")
        declaring = {char: [] for char in MEMBERS}
        for path, (digest, binary) in sorted(current.items()):
            raw = (REPO / Path(path)).read_bytes()
            require(sha(raw if binary else raw.replace(b"\r\n", b"\n")) == digest,
                    f"Manifest runtime hash differs: {path}")
            if path.startswith("words/"):
                card, _ = parse(raw.decode("utf-8").replace("\r\n", "\n"))
                for char in MEMBERS:
                    if char in card.get("kanji", []):
                        declaring[char].append(Path(path).stem)
            guard.check()
        require(declaring == SUPPORTS == selection["allDeclaredSupportArticles"],
                "Complete declared-support inventory differs")
        pairs = [[char, word] for char in MEMBERS for word in SUPPORTS[char]]
        require(selection["requiredReciprocalPairs"] == pairs, "Reciprocal pair inventory differs")
        link_records, metadata_records, geometry = [], [], []
        converter_path = REPO / "tools" / "generate_strokes.py"
        converter_raw = blob("tools/generate_strokes.py")
        require(sha(converter_raw) == CONVERTER_SHA and converter_path.read_bytes() == converter_raw,
                "Pinned stroke converter differs")
        converter = load_module("b129_pinned_stroke_converter", converter_path)
        receipt = json.loads(blob(PREFIX + "source-receipt.json"))
        for row in rows:
            char = row["kanji"]
            card_raw = blob(f"kanji/{char}.md")
            card, body = parse(card_raw.decode("utf-8").replace("\r\n", "\n"))
            verify_metadata(card, row)
            metadata_records.append({"kanji": char, "sourceRow": row["sourceRow"],
                                     "articleSha256": sha(card_raw), "metadata": card})
            for word in SUPPORTS[char]:
                name = f"words/{word}.md"
                before, after = blob(name, BASE), blob(name)
                require(link_helper.single_wrapper(before, after, char),
                        f"Support changed beyond one reciprocal wrapper: {name}")
                require(f"](../words/{word}.md)" in body, f"Missing forward support link: {char}/{word}")
                link_records.append({"kanji": char, "word": word, "path": name,
                                     "beforeSha256": sha(before), "afterSha256": sha(after)})
            svg_name = f"kanjivg/{ord(char):05x}.svg"
            svg = blob(PREFIX + svg_name)
            svg_blob = hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest()
            binding = receipt["kanjivg"][char]
            require(svg_blob == row["kanjivgInventory"]["sha"] == binding["gitBlob"]
                    and len(svg) == row["kanjivgInventory"]["size"]
                    and sha(svg) == binding["sha256"] and binding["file"] == svg_name,
                    f"Canonical stroke source differs: {char}")
            stroke_raw = blob(f"strokes/{char}.json")
            stroke = json.loads(stroke_raw)
            require(converter.convert(char, svg.decode("utf-8")) == stroke
                    and stroke["kanji"] == char and stroke["strokeCount"] == row["metadata"]["strokes"],
                    f"Generated geometry differs: {char}")
            geometry.append({"kanji": char, "svgSha256": sha(svg), "svgGitBlob": svg_blob,
                             "strokeSha256": sha(stroke_raw), "strokeCount": stroke["strokeCount"]})
            guard.check()
        notes = blob("docs/n1-authoring-notes.md").replace(b"\r\n", b"\n")
        stripped, count = re.subn(rb"(?m)^## Batch 129:.*?\n(?=## Batch )", b"", notes, flags=re.S)
        require(count == 1 and stripped == blob("docs/n1-authoring-notes.md", BASE).replace(b"\r\n", b"\n"),
                "Prior authoring notes changed beyond the B129 section")
        clean()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Payload verification RAM breach")
    print(json.dumps(freeze_json(output, {
        "batch": 129, "base": BASE, "candidate": candidate, "status": "PASS",
        "sourceProof": {"path": str(proof_path), "sha256": sha(proof_raw)},
        "signatureOutput": signature.decode("utf-8", "replace"),
        "signatureOutputSha256": sha(signature), "changes": changed,
        "manifestSha256": sha(manifest_raw), "contentVersion": manifest["contentVersion"],
        "baselineRuntimeEntries": len(previous), "verifiedRuntimeEntries": len(current),
        "members": metadata_records, "supportLinks": link_records, "generatedGeometry": geometry,
        "converterSha256": CONVERTER_SHA, "linkHelperSha256": LINK_HELPER_SHA,
        "memory": memory, "verifierSha256": sha(frozen(Path(__file__))),
        "limits": "Signed payload, source metadata, complete declared-support inventory, link-only "
                  "preservation and converter equality only. Author gates, evidence completeness, "
                  "semantic pair judgments, font/reading-pool checks, independent review, native/device "
                  "and publication acceptance remain separate.",
    })))


if __name__ == "__main__":
    require(len(sys.argv) == 4, "Usage: verify_b129_payload.py SOURCE_PROOF SHA256 NEW_OUTPUT")
    main(*sys.argv[1:])

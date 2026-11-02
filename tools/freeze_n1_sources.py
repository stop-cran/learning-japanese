#!/usr/bin/env python3
"""Reproduce the immutable issue-60 source freeze, not a linguistic review.

Requires the approved downloads outside the repository and the isolated Android
worktree. Refuses to replace existing evidence; --check compares without writing.
Mutable authoring/review dispositions belong in the separate batch ledgers.
"""
import argparse
import gzip
import hashlib
import json
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
BASELINE = "57dcc2aaedd8d6b0f141d5b4c3cb9c13f6f797b2"
ANDROID_BASELINE = "2bc0234bffcb3c4a0cbafde80367d24d2638a93a"
KVG_REVISION = "70a0b7ae0c18ceb5cb358274b029cce0234a43bc"
INPUTS = {
    "n1-kanji-source-20261102.json":
        "889faaefbec573e806f298766d2eee1300674c7b229bd973a35169cd2652cd73",
    "n1-planning-kanjidic2.xml.gz":
        "af0a499d62ac4413c614adcca360e2306490c3f64fccb3510fc7caa15f901bed",
    "n1-kanjivg-tree-70a0b7ae.json":
        "76822e38201de97cdd1d439882542de6f9b01997f41f1be088942ed10387f74a",
    "n1-implementation-JMdict_e.gz":
        "2dbbfe0b1214911766bbc128a0935618b925be917e7d1c50f3536a89b0e8786d",
    "n1-UnicodeData-17.0.0.txt":
        "2e1efc1dcb59c575eedf5ccae60f95229f706ee6d031835247d843c11d96470c",
}
PILOT = {
    "幹": ["ordinary compound", "baseline support reuse"],
    "氏": ["bound suffix", "same-stem distinct metadata entries"],
    "扱": ["many readings", "source-only reading risk", "baseline support reuse"],
    "乃": ["grade-9/name-use classification", "literary/function uses", "many on readings"],
    "凹": ["alternate primary reading in reused article", "look-alike contrast"],
    "凸": ["look-alike contrast", "new support discovery"],
    "矛": ["secondary meanings", "baseline support reuse", "source-only on reading risk"],
    "鷹": ["maximum source stroke count", "grade-9 non-name usage"],
    "彗": ["system-font fallback", "four on readings"],
    "漱": ["system-font fallback", "many kun readings", "okurigana boundaries"],
    "栞": ["system-font fallback", "grade-9 non-name usage"],
    "莉": ["system-font fallback", "bound compound", "multiple on readings"],
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def git(*args, root=ROOT):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args])


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load_inputs(directory):
    data = {}
    for name, expected in INPUTS.items():
        raw = (directory / name).read_bytes()
        require(digest(raw) == expected, f"Frozen input hash mismatch: {name}")
        data[name] = raw
    return data


def baseline_inventory():
    tree = git("ls-tree", "-r", "-z", BASELINE, "--",
               "kanji", "words", "strokes", "manifest.json", "tools/generate_strokes.py")
    inventory = {}
    with subprocess.Popen(
        ["git", "--no-pager", "-C", str(ROOT), "cat-file", "--batch"],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
    ) as process:
        for item in tree.split(b"\0"):
            if not item:
                continue
            info, path_bytes = item.split(b"\t", 1)
            blob = info.split()[2].decode("ascii")
            path = path_bytes.decode("utf-8")
            process.stdin.write(blob.encode("ascii") + b"\n")
            process.stdin.flush()
            header = process.stdout.readline().split()
            require(len(header) == 3 and header[1] == b"blob", f"Not a blob: {path}")
            raw = process.stdout.read(int(header[2]))
            require(process.stdout.read(1) == b"\n", f"Truncated git blob: {path}")
            row = {"gitBlob": blob, "sha256": digest(raw), "bytes": len(raw)}
            if path.endswith(".md"):
                row["metadata"] = yaml.safe_load(raw.decode("utf-8").split("---", 2)[1])
            elif path == "manifest.json":
                row["manifest"] = json.loads(raw)
            elif path == "tools/generate_strokes.py":
                row["normalizedSha256"] = digest(raw.replace(b"\r\n", b"\n"))
            inventory[path] = row
        process.stdin.close()
        require(process.wait() == 0, "git cat-file failed")
    counts = {folder: sum(p.startswith(folder + "/") for p in inventory)
              for folder in ("kanji", "words", "strokes")}
    require(counts == {"kanji": 985, "words": 4942, "strokes": 985},
            f"Unexpected baseline: {counts}")
    return {"baselineCommit": BASELINE, "counts": counts, "files": inventory}


def metadata_record(element, radicals):
    radical = element.findtext("radical/rad_value[@rad_type='classical']")
    require(radical is not None, f"No classical radical: {element.findtext('literal')}")
    return {
        "kanji": element.findtext("literal"),
        "strokes": int(element.findtext("misc/stroke_count")),
        "strokeCountAnnotations": [
            {"count": int(e.text), "attributes": e.attrib}
            for e in element.findall("misc/stroke_count")
        ],
        "grade": element.findtext("misc/grade"),
        "radicalNumber": int(radical),
        "radical": radicals[int(radical)],
        "onyomi": [e.text for e in element.findall(".//reading[@r_type='ja_on']")],
        "kunyomi": [e.text for e in element.findall(".//reading[@r_type='ja_kun']")],
        "meanings": [e.text for e in element.findall(".//meaning") if not e.attrib],
    }


def freeze(data, android):
    require(git("rev-parse", "HEAD", root=android).decode().strip() == ANDROID_BASELINE,
            "Android worktree is not at the approved baseline")
    require(not git("status", "--porcelain", "--untracked-files=no", root=android).strip(),
            "Android tracked files are dirty")
    source = json.loads(data["n1-kanji-source-20261102.json"])
    require(len(source) == len(set(source)) == 1232 and all(len(c) == 1 for c in source),
            "Unexpected community membership")
    kd_xml = gzip.decompress(data["n1-planning-kanjidic2.xml.gz"])
    require(digest(kd_xml) ==
            "9a000ef112b4bad8f1e6e3ca1f8e9f73ed84c93a5eae93dadfa1513081dc5db8",
            "KANJIDIC2 XML hash mismatch")
    kd = ET.fromstring(kd_xml)
    characters = {e.findtext("literal"): e for e in kd.findall("character")}
    radicals = {}
    for line in data["n1-UnicodeData-17.0.0.txt"].decode("utf-8").splitlines():
        fields = line.split(";")
        cp = int(fields[0], 16)
        if 0x2F00 <= cp <= 0x2FD5:
            radicals[cp - 0x2F00 + 1] = chr(int(fields[5].split()[-1], 16))
    require(len(radicals) == 214, "Incomplete radical map")
    inventory = baseline_inventory()
    files = inventory["files"]
    existing = {Path(p).stem for p in files if p.startswith("kanji/")}
    require(set(source) & existing == set("士奇怪訳"), "Existing source membership changed")
    require("妖" in existing and "妖" not in source, "The documented 妖 exception changed")
    additions = [c for c in source if c not in existing]
    require(len(additions) == 1228 and set(PILOT) <= set(additions), "Invalid additions/pilot")
    kvg = json.loads(data["n1-kanjivg-tree-70a0b7ae.json"])
    require(kvg["sha"] == KVG_REVISION and kvg["truncated"] is False,
            "Incomplete or wrong KanjiVG tree")
    svg_entries = {e["path"]: e for e in kvg["tree"] if e["type"] == "blob"}
    pairs = [
        {"kanji": c, "article": path, "word": row["metadata"]["word"],
         "primaryReading": row["metadata"]["reading"], "status": "unverified-candidate"}
        for path, row in files.items() if path.startswith("words/")
        for c in row["metadata"]["kanji"] if c in additions
    ]
    require(len(pairs) == 810 and len({p["article"] for p in pairs}) == 757,
            "Baseline candidate-pair counts changed")
    rows = []
    for index, c in enumerate(source, 1):
        svg_path = f"kanji/{ord(c):05x}.svg"
        require(svg_path in svg_entries, f"Missing canonical SVG inventory entry: {c}")
        rows.append({
            "sourceRow": index, "kanji": c, "codePoint": f"U+{ord(c):04X}",
            "article": f"kanji/{c}.md", "strokeFile": f"strokes/{c}.json",
            "statusAtFreeze": "baseline-preserved" if c in existing else "pending",
            "assignedBatchAtFreeze": "pilot" if c in PILOT else None,
            "metadata": metadata_record(characters[c], radicals),
            "kanjivgInventory": svg_entries[svg_path],
        })
    counts = {
        "sourceMembers": len(source), "existingMembers": 4, "additions": len(additions),
        "onEntries": sum(len(r["metadata"]["onyomi"]) for r in rows
                         if r["kanji"] in additions),
        "kunEntries": sum(len(r["metadata"]["kunyomi"]) for r in rows
                          if r["kanji"] in additions),
        "grade9Additions": sum(r["metadata"]["grade"] == "9" for r in rows
                               if r["kanji"] in additions),
        "declaredCandidatePairs": len(pairs),
        "distinctCandidateArticles": len({p["article"] for p in pairs}),
        "additionsWithDeclaredCandidates": len({p["kanji"] for p in pairs}),
    }
    require((counts["onEntries"], counts["kunEntries"], counts["grade9Additions"],
             counts["additionsWithDeclaredCandidates"]) == (1598, 1705, 247, 490),
            f"Source workload does not match approval: {counts}")
    font_records = []
    for path in sorted((android / "app" / "src" / "main" / "res" / "font").glob("kanji_*.ttf")):
        with TTFont(path) as font:
            cmap = font.getBestCmap()
            missing = [c for c in source if ord(c) not in cmap]
        require(len(missing) == 40, f"Unexpected font omissions: {path.name}")
        font_records.append({
            "path": path.relative_to(android).as_posix(), "sha256": digest(path.read_bytes()),
            "missingSourceCharacters": missing,
        })
    require(len(font_records) == 3, "Expected three bundled kanji fonts")
    fallback = font_records[0]["missingSourceCharacters"]
    require(all(r["missingSourceCharacters"] == fallback for r in font_records),
            "Bundled fonts have different coverage")
    jm_xml = gzip.decompress(data["n1-implementation-JMdict_e.gz"])
    require(digest(jm_xml) ==
            "107079c692f2e49c08d45da1da227b7e021298f247d16578b44dfaa2ec9002c4",
            "JMdict XML hash mismatch")
    require(b"<!-- JMdict created: 2026-11-02 -->" in jm_xml, "Unexpected JMdict version")
    kd_packet = ET.Element("kanjidic2")
    kd_packet.append(kd.find("header"))
    for c in [*source, "妖"]:
        kd_packet.append(characters[c])
    snapshot = {
        "schemaVersion": 1, "retrieved": "2026-11-02", "baselineCommit": BASELINE,
        "androidBaselineCommit": ANDROID_BASELINE, "counts": counts,
        "expectedFinal": {"kanji": 2213, "n1Labelled": 1233},
        "scope": "Issue 60 kanji only; support words as necessary; not an official JLPT syllabus.",
        "inputs": {name: {"sha256": digest(raw), "bytes": len(raw)}
                   for name, raw in data.items()},
        "communitySource": "https://kanjiapi.dev/v1/kanji/jlpt-1",
        "kanjidic2": {
            "url": "https://www.edrdg.org/kanjidic/kanjidic2.xml.gz",
            "xmlSha256": digest(kd_xml),
            "header": {e.tag: e.text for e in kd.find("header")},
            "transformation": "Complete parsed character records for all members plus 妖 are "
                              "reserialized in n1-sources/kanjidic2-selected.xml. The source index "
                              "selects ja_on/ja_kun in source order; nanori and old JLPT labels "
                              "are not transported into teaching metadata. Raw records remain intact.",
        },
        "jmdict": {
            "url": "https://www.edrdg.org/pub/Nihongo/JMdict_e.gz",
            "creationDate": "2026-11-02", "xmlSha256": digest(jm_xml),
            "limits": "Actual frozen dictionary bytes only; applicable complete lexical families, "
                      "spelling/reading/sense restrictions and author inspection still pending.",
        },
        "unicode": {
            "url": "https://www.unicode.org/Public/17.0.0/ucd/UnicodeData.txt",
            "version": "17.0.0",
            "transformation": "Classical radical n uses the compatibility decomposition at U+2F00+n-1.",
            "license": "Unicode License V3; docs/UNICODE-LICENSE.txt",
        },
        "kanjivg": {
            "revision": KVG_REVISION,
            "treeUrl": f"https://api.github.com/repos/KanjiVG/kanjivg/git/trees/{KVG_REVISION}?recursive=1",
            "converter": files["tools/generate_strokes.py"],
            "limits": "Canonical SVG inventory and blob identities only; SVG downloads, conversion "
                      "and stroke-count reconciliation still pending.",
        },
        "baselineException": {"kanji": "妖", "disposition": "preserve documented Kanshudo N1 exception",
                              "policy": "docs/jlpt-levels.md#documented-exceptions"},
        "dictionaryAttribution": "Copyright James William Breen and EDRDG; CC BY-SA 4.0.",
        "kanjivgAttribution": "Copyright Ulrich Apel and contributors; CC BY-SA 3.0.",
        "limits": "Freeze and candidate discovery only. No draft, content review, native rendering "
                  "acceptance or publication is asserted. statusAtFreeze is immutable historical "
                  "state, not the current review ledger. Baseline Git hashes establish bytes, "
                  "not semantic correctness. Runtime paths use exact published slash/casing.",
    }
    return {
        "n1-source-snapshot.json": json_bytes(snapshot),
        "n1-sources/community-list-20261102.json": data["n1-kanji-source-20261102.json"],
        "n1-sources/baseline-inventory.json": json_bytes(inventory),
        "n1-sources/source-index.json": json_bytes(rows),
        "n1-sources/baseline-word-candidates.json": json_bytes(pairs),
        "n1-sources/kanjidic2-selected.xml":
            ET.tostring(kd_packet, encoding="utf-8", xml_declaration=True) + b"\n",
        "n1-sources/font-coverage.json": json_bytes({
            "androidCommit": ANDROID_BASELINE, "fonts": font_records,
            "targets": [{"kanji": c, "codePoint": f"U+{ord(c):04X}",
                         "nativeInspection": "pending", "disposition": "unverified"}
                        for c in fallback],
            "limits": "Cmap absence only, not a glyph failure or supported-native rendering test.",
        }),
        "n1-sources/pilot-membership.json": json_bytes({
            "batch": "pilot", "baselineCommit": BASELINE,
            "members": [{"kanji": c, "risks": risks} for c, risks in PILOT.items()],
            "assignment": "One sequential author; two serial independent model-family reviewers "
                          "must each review all 12 cards, all new support words and changed reused "
                          "passages on the same future frozen teaching snapshot.",
            "reviewerModels": [], "reviewSnapshot": None, "status": "selected-not-authored",
            "limits": "Model catalog discovery/identity and actual content review remain pending. "
                      "Risk assignments guide inspection; they do not prove lexical coverage.",
        }),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, required=True)
    parser.add_argument("--android", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs = freeze(load_inputs(args.inputs), args.android)
    for name, raw in outputs.items():
        path = ROOT / "docs" / name
        if args.check:
            require(path.read_bytes().replace(b"\r\n", b"\n") == raw.replace(b"\r\n", b"\n"),
                    f"Freeze differs: {name}")
        else:
            require(not path.exists() or path.read_bytes() == raw,
                    f"Refusing to overwrite different source evidence: {path}")
    if not args.check:
        for name, raw in outputs.items():
            path = ROOT / "docs" / name
            path.parent.mkdir(parents=True, exist_ok=True)
            if not path.exists():
                path.write_bytes(raw)
    print(f"{'Verified' if args.check else 'Wrote'} {len(outputs)} immutable source records; "
          "1,228 additions remain pending, 12 selected for the pilot.")


if __name__ == "__main__":
    main()

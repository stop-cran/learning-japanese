"""Bounded batch 090 source preparation; never writes runtime content."""
import argparse
import copy
import gzip
import hashlib
import json
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
S = R / "docs" / "n1-sources"
L = C / "logs" / "66bf937a-6379-4bd0-93f5-8a1194e23d73"
BASE = "ebfd48dc911f32be0eeb9426db2f2d35a9084044"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
CHAR = "\u5200"
PREFIX = "batch-090-"
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata, offered_keys
from build_manifest import build_manifest
from extract_n1_jmdict import extract


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    temp = path.with_suffix(path.suffix + ".636.tmp")
    assert not temp.exists(), temp
    temp.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temp) == value
    temp.replace(path)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def git(*args, root=R):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args],
                                   encoding="utf-8").strip()


def clean(root, head):
    assert git("rev-parse", "HEAD", root=root) == head
    assert git("log", "-1", "--format=%G?", root=root) == "G"
    assert not git("status", "--porcelain", root=root)


def frozen():
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    inputs = {}
    for name, record in snapshot["inputs"].items():
        raw = (C / "inputs" / name).read_bytes()
        assert len(raw) == record["bytes"] and sha(raw) == record["sha256"], name
        inputs[name] = raw
    jm = gzip.decompress(inputs["n1-implementation-JMdict_e.gz"])
    kd = gzip.decompress(inputs["n1-planning-kanjidic2.xml.gz"])
    assert sha(jm) == snapshot["jmdict"]["xmlSha256"]
    assert sha(kd) == snapshot["kanjidic2"]["xmlSha256"]
    return snapshot, inputs, ET.fromstring(jm), ET.fromstring(kd)


def start():
    clean(R, BASE)
    clean(A, APP)
    assert git("rev-parse", "origin/main") == BASE
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (635, "089", "continue")
    assert p["lastPublishedCommit"] == BASE and p["remainingAdditions"] == 1112
    assert not list(S.glob(PREFIX + "*"))
    assert not (L / "progress-before-636.json").exists()
    runner = load(C / "runner.json")
    assert runner["pid"] == 19008 and runner["status"] == "running"
    assert runner["sessionId"] == L.name
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
    assert json.loads(text.split(marker, 1)[1])["checkpoint"] == 635
    shutil.copyfile(C / "progress.json", L / "progress-before-636.json")
    state = {
        "execution": 636, "batch": "090", "startingHead": BASE, "freshOriginMain": BASE,
        "androidHead": APP, "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "ONE bounded090 source-preparation checkpoint for next absent row101 only; no runtime draft, reviewer, Android/native, publication,091 or second runner.",
        "request": {"sha256": sha(raw), "bytes": len(raw), "characters": len(text),
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded and embedded checkpoint decoded. Operative contract, complete approved issue and final635 inspected directly; historical middle parsed, not freshly semantically re-reviewed. Initial root-state print hit console encoding error after complete loading; bounded UTF-8 reads succeeded."},
        "runnerLockRole": "Win32_Process confirms shell29248 parent coordinator20368 parent live launcher19008; runner.json identifies exact session. Parent retains runner.lock; no child acquisition/deletion/unlocking.",
        "artifactPathPreflight": "Approved control helpers, committed packets and frozen workspace inputs only. No optional historical-session helper access.",
        "actualNewPermissionDenials": [],
        "worktrees": "Wholly clean dedicated content and qualified TESTONLY Android; normal signatures G. Fresh main equals content. Android1c1b7bf4 retains productionf9b59a2, not latest app main. Canonical repositories not accessed.",
    }
    p["execution636StartingState"] = state
    p.update(batch="090", stage="batch-090-source-preparation-in-progress",
             nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    print("Starting scope persisted with full live history.")


def packet():
    snapshot, inputs, jm, kd = frozen()
    assert load(C / "progress.json")["batch"] == "090"
    row = next(r for r in load(S / "source-index.json") if r["kanji"] == CHAR)
    assert row["sourceRow"] == 101
    assert json.loads(inputs["n1-kanji-source-20261102.json"])[100] == CHAR
    assert not (R / row["article"]).exists() and not (R / row["strokeFile"]).exists()
    ids = [e.findtext("ent_seq") for e in jm.findall("entry")
           if any(CHAR in k.text for k in e.findall("k_ele/keb"))]
    save(S / (PREFIX + "lexical-selection.json"), {
        "schemaVersion": 1, "batch": "090", "entryIds": ids,
        "sourceSnapshot": "docs/n1-source-snapshot.json",
        "selectionRule": "Every complete frozen family containing U+5200 in any keb; preserve all aliases/readings/restrictions/senses.",
        "limits": "Extraction alone is not inspection, per-character allocation, frequency evidence or independent review.",
    })
    (S / (PREFIX + "jmdict.xml")).write_bytes(extract(
        inputs["n1-implementation-JMdict_e.gz"],
        snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids))
    selected = ET.Element("kanjidic2")
    selected.append(copy.deepcopy(kd.find("header")))
    selected.append(copy.deepcopy(next(e for e in kd.findall("character")
                                      if e.findtext("literal") == CHAR)))
    ET.indent(selected, space="  ")
    raw = ET.tostring(selected, encoding="utf-8", xml_declaration=True) + b"\n"
    (S / (PREFIX + "kanjidic2.xml")).write_bytes(raw)
    save(S / (PREFIX + "input-metadata.json"), {
        "schemaVersion": 1, "batch": "090", "baseCommit": BASE, "sourceIndexRecord": row,
        "characters": [CHAR], "rawCharacterPacket": PREFIX + "kanjidic2.xml",
        "rawCharacterPacketSha256": sha(raw),
        "provenance": "Complete frozen character record/header, parsed and reserialized.",
        "dictionaryAttribution": "Copyright James William Breen and EDRDG; CC BY-SA4.0; repositoryNOTICE.",
    })
    candidates = []
    for path in sorted((R / "words").glob("*.md")):
        name = path.relative_to(R).as_posix()
        m = metadata(R, name)
        if CHAR in m.get("kanji", []) or CHAR in m["word"]:
            candidates.append({"article": name, "metadata": m})
    save(C / "batch-090-source-navigation.json", {
        "sourceIndexRecord": row, "candidates": candidates,
        "baselinePairs": [r for r in load(S / "baseline-word-candidates.json") if r["kanji"] == CHAR],
    })
    lines = []
    for e in ET.parse(S / (PREFIX + "jmdict.xml")).getroot().findall("entry"):
        compact = ET.fromstring(ET.tostring(e))
        for node in compact.iter():
            if node.text and not node.text.strip():
                node.text = None
            node.tail = None
        lines.append(ET.tostring(compact, encoding="unicode"))
    (C / "batch-090-full-family-reading.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"families": len(ids), "candidates": candidates}, ensure_ascii=True, indent=2))


def comparison():
    snapshot, inputs, jm, kd = frozen()
    words = ["\u4e43", "\u51f9", "\u51f8", "\u529b", "\u5207", "\u65e5\u672c",
             "\u30ca\u30a4\u30d5", "\u5305\u4e01"]
    ids = [e.findtext("ent_seq") for e in jm.findall("entry")
           if any(k.text in words for k in e.findall("k_ele/keb"))]
    ids += [e.findtext("ent_seq") for e in jm.findall("entry")
            if not e.findall("k_ele") and any(k.text == "\u30ca\u30a4\u30d5"
                                            for k in e.findall("r_ele/reb"))]
    save(S / (PREFIX + "comparison-selection.json"), {
        "schemaVersion": 1, "batch": "090", "exactSpellings": words, "entryIds": ids,
        "rule": "Complete frozen families containing an exact listed keb; kana-only ナイフ matched by reb.",
        "limits": "Bounded navigation packet, not exhaustive quiz or linguistic acceptance.",
    })
    (S / (PREFIX + "comparison-jmdict.xml")).write_bytes(extract(
        inputs["n1-implementation-JMdict_e.gz"],
        snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids))
    selected = ET.Element("kanjidic2")
    selected.append(copy.deepcopy(kd.find("header")))
    for char in "\u4e43\u51f9\u51f8\u529b\u5207\u65e5\u672c":
        selected.append(copy.deepcopy(next(e for e in kd.findall("character")
                                          if e.findtext("literal") == char)))
    ET.indent(selected, space="  ")
    (S / (PREFIX + "comparison-kanjidic2.xml")).write_bytes(
        ET.tostring(selected, encoding="utf-8", xml_declaration=True) + b"\n")
    print(json.dumps({"comparisonFamilies": len(ids), "rawCharacterRecords": 7}))


def public():
    from html.parser import HTMLParser

    class ArticleText(HTMLParser):
        def __init__(self):
            super().__init__()
            self.depth = 0
            self.parts = []

        def handle_starttag(self, tag, attrs):
            if tag == "article":
                self.depth += 1
                self.parts.append("\n[ARTICLE " + dict(attrs).get("class", "") + "]\n")
            if self.depth and tag in {"p", "h2", "h3", "br", "section"}:
                self.parts.append("\n")

        def handle_endtag(self, tag):
            if tag == "article" and self.depth:
                self.depth -= 1
                self.parts.append("\n[END ARTICLE]\n")

        def handle_data(self, data):
            if self.depth:
                self.parts.append(data)

    receipts = {}
    for name, suffix in [("katana", "%E5%88%80-44955"),
                         ("nihontou", "%E6%97%A5%E6%9C%AC%E5%88%80-110244")]:
        path = C / "inputs" / f"batch-090-{name}.html"
        raw = path.read_bytes()
        parser = ArticleText()
        parser.feed(raw.decode("utf-8"))
        text = "\n".join(line.strip() for line in "".join(parser.parts).splitlines()
                         if line.strip()) + "\n"
        assert CHAR in text
        archive = S / f"batch-090-{name}.html.gz"
        archive.write_bytes(gzip.compress(raw, mtime=0))
        target = S / f"batch-090-{name}-public-text.txt"
        target.write_text(text, encoding="utf-8")
        receipts[name] = {
            "url": "https://kotobank.jp/word/" + suffix,
            "retrievedAt": datetime.now(timezone.utc).isoformat(),
            "sourcePath": str(path), "sourceSha256": sha(raw),
            "archive": archive.name, "archiveSha256": sha(archive.read_bytes()),
            "losslessGzip": gzip.decompress(archive.read_bytes()) == raw,
            "extractedText": target.name, "extractedTextSha256": sha(target.read_bytes()),
            "extractionLimits": "Coordinator article-only HTMLParser extraction; links/formatting/images stripped, dictionary blocks retained. Only identified lexical/character headings are teaching evidence; encyclopedic history/metallurgy not independently verified.",
        }
        print(name, len(text), "characters", len(text.splitlines()), "lines")
    save(S / (PREFIX + "public-source-receipts.json"), receipts)


def audit():
    from audit_n1_batch import lexical_pair
    from fontTools.ttLib import TTFont
    from freeze_n1_sources import metadata_record

    def distinct(pairs):
        result = {}
        for key, value in pairs:
            assert key not in result, key
            result[key] = value
        return result

    for path in S.glob(PREFIX + "*.json"):
        json.loads(path.read_text(encoding="utf-8-sig"), object_pairs_hook=distinct)
    snapshot, inputs, jm, kd = frozen()
    progress = load(S / (PREFIX + "progress.json"))
    evidence_path = S / (PREFIX + "source-evidence.json")
    evidence = load(evidence_path)
    row = next(r for r in load(S / "source-index.json") if r["kanji"] == CHAR)
    named = json.loads(inputs["n1-kanji-source-20261102.json"])
    assert named == load(S / "community-list-20261102.json")
    assert len(named) == len(set(named)) == 1232 and named[100] == CHAR
    unicode_rows = [line.split(";") for line in inputs["n1-UnicodeData-17.0.0.txt"]
                    .decode("utf-8").splitlines()]
    assert next(r for r in unicode_rows if r[0] == "2F11")[5] == "<compat> 5200"
    canonical = lambda e: ET.canonicalize(ET.tostring(e, encoding="unicode"), strip_text=True)
    character = next(e for e in kd.findall("character") if e.findtext("literal") == CHAR)
    assert metadata_record(character, {18: CHAR}) == row["metadata"]
    for name, chars in [("kanjidic2.xml", CHAR),
                        ("comparison-kanjidic2.xml", "\u4e43\u51f9\u51f8\u529b\u5207\u65e5\u672c")]:
        packet_root = ET.parse(S / (PREFIX + name)).getroot()
        assert canonical(packet_root.find("header")) == canonical(kd.find("header"))
        assert [e.findtext("literal") for e in packet_root.findall("character")] == list(chars)
        for e in packet_root.findall("character"):
            original = next(o for o in kd.findall("character")
                            if o.findtext("literal") == e.findtext("literal"))
            assert canonical(e) == canonical(original)
    families = {e.findtext("ent_seq"): e for e in jm.findall("entry")}
    exact_ids = [i for i, e in families.items()
                 if any(CHAR in k.text for k in e.findall("k_ele/keb"))]
    comparison_selection = load(S / (PREFIX + "comparison-selection.json"))
    comparison_ids = [i for i, e in families.items()
                      if any(k.text in comparison_selection["exactSpellings"]
                             for k in e.findall("k_ele/keb"))]
    comparison_ids += [i for i, e in families.items()
                       if not e.findall("k_ele") and any(k.text == "\u30ca\u30a4\u30d5"
                                                       for k in e.findall("r_ele/reb"))]
    assert len(exact_ids) == 194 and len(comparison_ids) == 13
    for stem, ids in [("", exact_ids), ("comparison-", comparison_ids)]:
        selected_ids = (comparison_selection["entryIds"] if stem
                        else load(S / (PREFIX + "lexical-selection.json"))["entryIds"])
        assert ids == selected_ids
        assert (S / (PREFIX + stem + "jmdict.xml")).read_bytes() == extract(
            inputs["n1-implementation-JMdict_e.gz"],
            snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
    compact_path = C / "batch-090-full-family-reading.txt"
    compact = compact_path.read_text(encoding="utf-8").splitlines()
    original_entries = ET.parse(S / (PREFIX + "jmdict.xml")).getroot().findall("entry")
    assert len(compact) == len(original_entries) == 194
    assert all(canonical(ET.fromstring(a)) == canonical(b)
               for a, b in zip(compact, original_entries))
    archive = S / (PREFIX + "full-family-reading.txt.gz")
    archive.write_bytes(gzip.compress(compact_path.read_bytes(), mtime=0))
    decisions = [i for group in evidence["selectedLexicalDecisions"] for i in group["entryIds"]]
    assert len(decisions) == len(set(decisions)) and set(decisions) <= set(exact_ids)
    evidence["unselectedCompleteFamilyIds"] = [i for i in exact_ids if i not in decisions]
    expected = [(kind, reading) for kind, field in [("on", "onyomi"), ("kun", "kunyomi")]
                for reading in row["metadata"][field]]
    assert [(d["kind"], d["reading"]) for d in progress["readingDispositions"]] == expected
    assert progress["sourceReadingOrder"] == {k: row["metadata"][k] for k in ["onyomi", "kunyomi"]}
    selected = [d for d in progress["readingDispositions"] if d["proposedQuizSelection"]]
    assert [d["reading"] for d in selected] == ["\u30c8\u30a6", "\u304b\u305f\u306a"]
    assert all(d["sourceOnly"] == (not d["proposedQuizSelection"])
               and d["qualification"] and d["evidence"] for d in progress["readingDispositions"])
    projection = progress["proposedCuratedProjection"]
    assert projection["onKeys"] == offered_keys(projection["quizOnyomi"]) == ["\u3068\u3046"]
    assert projection["kunKeys"] == offered_keys(projection["quizKunyomi"]) == ["\u304b\u305f\u306a"]
    pairs = set()
    for m in progress["proposedSupportMapping"]:
        assert lexical_pair(families[m["entryId"]], m["word"], m["primaryReading"])
        assert m["entryId"] in exact_ids
        written = list(dict.fromkeys(c for c in m["word"] if 0x4E00 <= ord(c) <= 0x9FFF))
        assert m["allWrittenKanji"] == written
        if m["status"].startswith("verified-baseline-reuse"):
            actual = metadata(R, m["article"])
            assert actual["word"] == m["word"] and actual["reading"] == m["primaryReading"]
            assert actual["jlpt"] == m["preservedWordJlpt"] and actual["kanji"] == written
            assert actual["type"] == m["type"]
        else:
            assert not (R / m["article"]).exists() and m["preservedWordJlpt"] is None
        for char in written:
            if char == CHAR or (R / "kanji" / (char + ".md")).exists():
                pairs.add((char, m["article"]))
    assert not (R / "kanji" / "\u5243.md").exists()
    assert len(pairs) == 5 and pairs == {tuple(p) for p in progress["proposedReciprocalPairs"]}
    directions = {(f"kanji/{char}.md", article) for char, article in pairs}
    directions |= {(article, f"kanji/{char}.md") for char, article in pairs}
    assert {(d["from"], d["to"]) for d in progress["proposedDirectedLinkPlan"]} == directions
    assert progress["requiredDirectionCount"] == len(directions) == 10
    nav = load(C / "batch-090-source-navigation.json")
    baseline_pairs = {(r["kanji"], r["article"]) for r in nav["baselinePairs"]}
    assert baseline_pairs == {tuple(x) for x in progress["activatedBaselinePairs"]}
    assert {r["article"] for r in nav["candidates"]} == {x[1] for x in baseline_pairs}
    kana_candidates = []
    for path in (R / "words").glob("*.md"):
        name = path.relative_to(R).as_posix()
        m = metadata(R, name)
        if m["reading"] in ["\u306b\u307b\u3093\u3068\u3046", "\u306b\u3063\u307d\u3093\u3068\u3046"]:
            kana_candidates.append({"article": name, "metadata": m})
    assert not kana_candidates
    assert progress["membership"] == load(S / (PREFIX + "membership.json"))["membership"] == [CHAR]
    assert progress["drafted"] == progress["reviewClosed"] == progress["published"] == []
    assert all(metadata(R, x["article"])["jlpt"] == x["preservedJlpt"]
               and x["metadataChanges"] is False for x in progress["proposedReusedChanges"])
    quiz = progress["proposedQuiz"]
    assert quiz["labels"] == [metadata(R, f"kanji/{char}.md")["title"] for char in quiz["distractors"]]
    assert len(quiz["distractors"]) == len(set(quiz["distractors"])) == 3
    assert all(metadata(R, f"kanji/{char}.md")["jlpt"] == 1 for char in quiz["distractors"])
    assert all(metadata(R, path.relative_to(R).as_posix())["title"] != quiz["kanjiTitle"]
               for path in (R / "kanji").glob("*.md"))
    assert all(len(metadata(R, f"kanji/{char}.md")["distractors"]) == 3 for char in "\u529b\u5207")
    assert metadata(R, "words/\u5243\u5200.md")["quiz_exclusions"] == ["\u92ed\u3044"]
    guards = {(item["word"], other) for item in quiz["proposedDirectExclusions"]
              for other in item["exclude"]}
    assert guards == {("\u65e5\u672c\u5200", "\u5200")}
    assert all((R / "words" / (other + ".md")).exists() for _, other in guards)
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json")
    checked = sum(len(v) for v in manifest.values() if isinstance(v, dict))
    assert checked == 8426 and manifest["contentVersion"] == "c6562f11cb371053"
    assert not git("diff", BASE, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    baseline = load(S / "baseline-inventory.json")
    original = {Path(n).stem for n in baseline["files"] if n.startswith("kanji/")}
    current = {p.stem for p in (R / "kanji").glob("*.md")}
    accepted = set("\u5e79\u6c0f\u6271\u4e43\u51f9\u51f8\u77db\u9df9\u5f57\u6f31\u681e\u8389")
    for path in S.glob("batch-*-progress.json"):
        accepted.update(load(path).get("published", []))
    earlier = set("\u4fdd\u6848\u6d3e\u7b2c\u7b56\u7d50")
    assert len(accepted) == 116 and accepted <= current - original and accepted <= set(named)
    assert len(current) == 1112 and len(set(named) & current) == 126
    assert current & set(named) == (original & set(named)) | accepted | earlier
    assert len(set(named) - current) == 1106
    assert all(metadata(R, f"kanji/{char}.md")["jlpt"] == 2 for char in earlier)
    assert metadata(R, "kanji/\u5996.md")["jlpt"] == 1
    tree = json.loads(inputs["n1-kanjivg-tree-70a0b7ae.json"])
    assert not tree["truncated"] and tree["sha"] == snapshot["kanjivg"]["revision"]
    assert next(t for t in tree["tree"] if t["path"] == row["kanjivgInventory"]["path"]) == row["kanjivgInventory"]
    svg_path = C / "inputs" / "n1-05200-70a0b7ae.svg"
    svg = svg_path.read_bytes()
    blob = hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest()
    assert blob == row["kanjivgInventory"]["sha"] and len(svg) == row["kanjivgInventory"]["size"]
    paths = ET.fromstring(svg).findall(".//{http://www.w3.org/2000/svg}path")
    assert len(paths) == row["metadata"]["strokes"] == 2
    assert [p.attrib["id"] for p in paths] == ["kvg:05200-s1", "kvg:05200-s2"]
    converter = sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n"))
    assert converter == snapshot["kanjivg"]["converter"]["normalizedSha256"]
    stroke = {
        "schemaVersion": 1, "batch": "090", "revision": tree["sha"], "input": str(svg_path),
        "gitBlob": blob, "bytes": len(svg), "sha256": sha(svg),
        "sourceUrl": "https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/kanji/05200.svg",
        "dictionaryStrokeCount": 2, "sourceStrokePaths": 2, "converted": False,
        "nativeDrawingAccepted": False, "converterNormalizedSha256": converter,
        "attribution": "Ulrich Apel and contributors, KanjiVG, CC BY-SA3.0; repositoryNOTICE.",
        "limits": "Pinned SVG inspected and verified; no runtime geometry or native drawing acceptance.",
    }
    save(S / (PREFIX + "stroke-evidence.json"), stroke)
    (S / (PREFIX + "kanjivg.svg")).write_bytes(svg)
    han = sorted({char for char in progress["proposedHanText"] if 0x2E80 <= ord(char) <= 0x2FDF
                  or 0x3400 <= ord(char) <= 0x9FFF or 0xF900 <= ord(char) <= 0xFAFF
                  or 0x20000 <= ord(char) <= 0x2FFFF})
    fonts = []
    for old in load(S / "batch-089-font-preparation.json")["fonts"]:
        path = Path(old["path"])
        assert path.is_relative_to(A) and sha(path.read_bytes()) == old["sha256"]
        with TTFont(path) as font:
            cmap = font.getBestCmap()
        fonts.append({"path": str(path), "sha256": old["sha256"],
                      "keyGlyphPresence": {char: ord(char) in cmap for char in han},
                      "allProposedMissing": [char for char in han if ord(char) not in cmap]})
    rare = [char for char in han if 0x2E80 <= ord(char) <= 0x2FDF or 0x3400 <= ord(char) <= 0x4DBF
            or 0xF900 <= ord(char) <= 0xFAFF or 0x20000 <= ord(char) <= 0x2FFFF]
    assert not rare
    save(S / (PREFIX + "font-preparation.json"), {
        "schemaVersion": 1, "batch": "090", "proposedTextInventory": progress["proposedHanText"],
        "auditedHan": han, "auditedHanCount": len(han), "fonts": fonts,
        "rareHanRangeCharacters": rare,
        "unicodeRadicalCompatibility": "Frozen Unicode17.0.0 U+2F11 maps to U+5200; prose uses ordinary刀, not compatibilityglyph.",
        "mechanism": "Unchanged RareHan.kt/RareHanTest.kt read; all three actual bundled font cmaps inspected.",
        "limits": "Proposed inventory, not final runtimeHan/nativelegibility/fallbackface. Fresh fourfont/allHan rendering and non-skipped RareHan test remain required. Cmap presence/absence is not glyph acceptance.",
    })
    for receipt in load(S / (PREFIX + "public-source-receipts.json")).values():
        raw = Path(receipt["sourcePath"]).read_bytes()
        assert sha(raw) == receipt["sourceSha256"]
        archive = S / receipt["archive"]
        assert sha(archive.read_bytes()) == receipt["archiveSha256"]
        assert gzip.decompress(archive.read_bytes()) == raw
        assert sha((S / receipt["extractedText"]).read_bytes()) == receipt["extractedTextSha256"]
    evidence["actualPacketLineCounts"] = {
        name: len((S / (PREFIX + name)).read_text(encoding="utf-8").splitlines())
        for name in ["jmdict.xml", "kanjidic2.xml", "comparison-jmdict.xml", "comparison-kanjidic2.xml"]}
    evidence["familyCounts"] = {"allExactMemberFamilies": 194, "comparisonFamilies": 13,
                                "distinctCompleteFamilies": len(set(exact_ids + comparison_ids))}
    save(evidence_path, evidence)
    result = {
        "schemaVersion": 1, "execution": 636, "batch": "090", "baseCommit": BASE,
        "stage": progress["status"], "membership": [CHAR], "sourceRow": 101,
        "frozenInputHashesVerified": len(inputs), "decompressedDictionaryHashesVerified": 2,
        "exactFrozenNamedMembershipAndRowVerified": True, "completeLexicalFamilies": 194,
        "completeComparisonFamilies": 13, "allExtractedEntryIdsAccountedFor": True,
        "freshExactDictionaryExtractionsVerified": 2, "rawCharacterRecordsVerified": 8,
        "compactFullFamilyTextSemanticallyEqualToRawXml": True,
        "proposedMetadataReadingDispositionsVerified": 3,
        "proposedOnKeys": projection["onKeys"], "proposedKunKeys": projection["kunKeys"],
        "proposedNewSupportArticles": 1, "proposedReusedSupportArticles": 2,
        "proposedNavigationOnlyReusedKanjiChanges": 2,
        "existingExactKanaReadingCandidates": kana_candidates,
        "allMappedReciprocalPairs": 5, "requiredDirectedLinks": 10,
        "activatedBaselinePairs": 2, "proposedDirectWordGuards": 1,
        "pinnedSvg": stroke, "proposedHanCount": len(han),
        "fontPreparation": PREFIX + "font-preparation.json",
        "mainFontCmapAbsences": fonts[0]["allProposedMissing"],
        "inspectedArticleHashes": {name: sha((R / name).read_bytes())
                                  for name in evidence["authorInspection"]["completeExistingArticlesRead"]},
        "runtimeManifestEqualToPublishedBase": True, "runtimeHashesUnchanged": checked,
        "contentVersion": manifest["contentVersion"], "publishedAdditions": 116,
        "remainingAcceptanceAdditions": 1112, "actuallyAbsentNamedMembers": 1106,
        "separateEarlierLevelSourceMembers": sorted(earlier),
        "separateEarlierPlacementsCountedAsIssue60AcceptedBatches": False,
        "baselinePreservation": "All runtime bytes unchanged from normally signed published base; no metadata/readings/levels/exclusions/geometry changed.",
        "runtimeChanges": 0, "reviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "optionalHistoricalHelpersAccessed": False, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "limits": progress["limits"],
    }
    save(S / (PREFIX + "preparation-audit.json"), result)
    print(json.dumps({key: value for key, value in result.items()
                      if key not in ["limits", "pinnedSvg", "inspectedArticleHashes"]},
                     ensure_ascii=True, indent=2))


def record():
    checks = {}
    for name in ["source-tests", "validate", "budget", "audit", "manifest", "whitespace"]:
        path = L / f"{name}-636.txt"
        text = path.read_text(encoding="utf-8-sig")
        assert "Traceback" not in text and "FAILED" not in text
        if name == "source-tests":
            assert "Ran 43 tests" in text and "OK" in text
        elif name == "validate":
            assert "0 error(s)" in text
        elif name == "audit":
            assert '"runtimeHashesUnchanged": 8426' in text
        raw = path.read_bytes()
        archive = S / f"batch-090-{name}-636.txt.gz"
        archive.write_bytes(gzip.compress(raw, mtime=0))
        assert gzip.decompress(archive.read_bytes()) == raw
        checks[name] = {"path": str(path), "sha256": sha(raw),
                        "archive": archive.name, "archiveSha256": sha(archive.read_bytes()),
                        "losslessGzip": True, "provenance": "Direct redirected subprocess stdout/stderr; exit0 checked by wrapper."}
    recipe = S / (PREFIX + "source-recipe.py")
    recipe.write_bytes(Path(__file__).read_bytes())
    save(S / "execution-636.json", {
        "schemaVersion": 1, "execution": 636, "batch": "090", "baseCommit": BASE,
        "startingState": load(C / "progress.json")["execution636StartingState"],
        "sourceAudit": PREFIX + "preparation-audit.json", "sourcePacket": PREFIX + "progress.json",
        "sourceEvidence": PREFIX + "source-evidence.json",
        "recipe": {"durableControlPath": str(Path(__file__)), "archive": recipe.name,
                   "sha256": sha(recipe.read_bytes())},
        "checks": checks, "runtimeChanged": False, "runtimePublished": False,
        "focusedTestsPassed": 43,
        "focusedTestCommand": "python -X utf8 -B -m unittest test_freeze_n1_sources test_extract_n1_jmdict test_audit_n1_pilot test_audit_n1_batch; PYTHONPATH=tools",
        "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 116, "remainingAdditions": 1112,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": load(S / (PREFIX + "progress.json"))["nextAction"],
        "limits": load(S / (PREFIX + "progress.json"))["limits"],
    })
    print("Source evidence/checks and durable recipe archived; normal local signing next, no push.")


def seal():
    head = git("rev-parse", "HEAD")
    clean(R, head)
    clean(A, APP)
    assert head != BASE and git("rev-parse", "origin/main") == BASE
    assert git("rev-parse", "HEAD^") == BASE
    assert not git("diff", BASE, "HEAD", "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    changed = git("diff", "--name-only", BASE, "HEAD").splitlines()
    assert changed and all(name.startswith("docs/n1-sources/batch-090-") or name == "docs/n1-sources/execution-636.json"
                           for name in changed)
    before = load(L / "progress-before-636.json")
    p = load(C / "progress.json")
    allowed = {"checkpoint", "status", "stage", "batch", "nextAction", "blocker"}
    assert (p["checkpoint"], p["batch"]) == (635, "090")
    assert all(p.get(key) == value for key, value in before.items() if key not in allowed)
    issue = load(L / "issue-response-636.json")
    body = (C / "execution636-issue.txt").read_bytes().decode("utf-8")
    assert issue["user"]["login"] == "stop-cran" and issue["body"] == body
    assert issue["issue_url"].endswith("/issues/60")
    receipt = {"id": issue["id"], "url": issue["html_url"], "author": "stop-cran",
               "bodySha256": sha(body.encode("utf-8")), "verified": True}
    audit_record = load(S / (PREFIX + "preparation-audit.json"))
    state = {
        "schemaVersion": 1, "execution": 636, "checkpoint": 636, "batch": "090",
        "status": "continue", "stage": "source-prepared-not-drafted", "savedCommit": head,
        "signature": "G", "lastPublishedCommit": BASE,
        "sourcePacket": "docs/n1-sources/batch-090-progress.json",
        "sourceAudit": "docs/n1-sources/batch-090-preparation-audit.json",
        "evidence": "docs/n1-sources/execution-636.json",
        "membership": [CHAR], "sourceRow": 101, "completeDictionaryFamilies": 207,
        "lexicalFamilies": 194, "comparisonFamilies": 13, "completeRawCharacterRecords": 8,
        "metadataReadings": 3, "proposedNewSupportArticles": 1, "proposedReusedSupportArticles": 2,
        "proposedNavigationOnlyReusedKanjiChanges": 2,
        "allMappedReciprocalPairs": 5, "proposedLinkDirections": 10,
        "pinnedSvgPaths": 2, "geometryConverted": False, "proposedDirectWordGuards": 1,
        "proposedHanCount": audit_record["proposedHanCount"],
        "dedicatedWorktreesClean": True, "runtimeChanged": False, "runtimePublished": False,
        "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 116, "remainingAdditions": 1112,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "runtimeHashesUnchanged": 8426, "originalHistoricalRootKeysCompared": len(before),
        "allOriginalHistoricalValuesPreserved": True,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "issueUpdate": receipt["url"],
        "ownerIssueAuthorAndBodyVerified": True,
        "nextAction": load(S / (PREFIX + "progress.json"))["nextAction"],
    }
    p["execution636CoordinatorCheckpoint"] = state
    p["batch090SourcePreparation"] = state
    p["batch090SourcePreparationIssueReceipt"] = receipt
    p.update(checkpoint=636, status="continue", stage="batch-090-source-prepared-not-drafted",
             blocker=None, nextAction=state["nextAction"])
    save(C / "progress.json", p)
    reread = load(C / "progress.json")
    assert all(reread.get(key) == value for key, value in before.items() if key not in allowed)
    save(L / "execution-636-final-checkpoint.json", state)
    print(json.dumps(state, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["start", "packet", "comparison", "public", "audit", "record", "seal"])
    globals()[parser.parse_args().action]()

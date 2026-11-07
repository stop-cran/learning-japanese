"""Prepare one source-only checkpoint; never author or publish runtime files."""
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
L = C / "logs" / "6de9468a-e5b5-47a1-b5a1-891624b19343"
BASE = "7100a3873282b54515b9ef130766e77cf151a47b"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
CHAR = "\u5203"
PREFIX = "batch-091-"
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata, offered_keys
from build_manifest import build_manifest
from extract_n1_jmdict import extract


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    temporary = path.with_suffix(path.suffix + ".645.tmp")
    assert not temporary.exists(), temporary
    temporary.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temporary) == value
    temporary.replace(path)


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
    assert (p["checkpoint"], p["batch"], p["status"]) == (644, "090", "continue")
    assert p["lastPublishedCommit"] == BASE and p["remainingAdditions"] == 1111
    assert not list(S.glob(PREFIX + "*"))
    runner = load(C / "runner.json")
    assert runner["pid"] == 19008 and runner["status"] == "running"
    assert runner["sessionId"] == L.name
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
    assert json.loads(text.split(marker, 1)[1])["checkpoint"] == 644
    before = L / "progress-before-645.json"
    assert not before.exists()
    shutil.copyfile(C / "progress.json", before)
    state = {
        "execution": 645, "batch": "091", "startingHead": BASE, "freshOriginMain": BASE,
        "androidHead": APP, "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "ONE bounded091 source-preparation checkpoint for frozen row102刃 only; no runtime draft, reviewer, Android/native, publication,092 or second runner.",
        "request": {"sha256": sha(raw), "bytes": len(raw), "characters": len(text),
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded and checkpoint parsed. Operative contract, complete approved issue and final644 inspected directly; historical middle parsed, not freshly semantically re-reviewed. Initial output hit console encoding error after complete loading; bounded UTF-8 output succeeded."},
        "runnerLockRole": "Win32_Process confirms shell29324 parent coordinator20472 parent live launcher19008; runner.json identifies exact session. Parent retains runner.lock; no child acquisition/deletion/unlocking.",
        "artifactPathPreflight": "Approved control helpers, committed packets and frozen workspace inputs only. No optional historical-session helper access.",
        "actualNewPermissionDenials": [],
        "worktrees": "Wholly clean dedicated content and qualified TESTONLY Android; normal signatures G. Fresh main equals content. Android1c1b7bf4 retains productionf9b59a2, not latest app main. Canonical repositories not accessed.",
    }
    p["execution645StartingState"] = state
    p.update(batch="091", stage="batch-091-source-preparation-in-progress",
             nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    print("Starting scope persisted; complete historical values preserved.")


def character_packet(kd, chars, name):
    selected = ET.Element("kanjidic2")
    selected.append(copy.deepcopy(kd.find("header")))
    for char in chars:
        selected.append(copy.deepcopy(next(e for e in kd.findall("character")
                                          if e.findtext("literal") == char)))
    ET.indent(selected, space="  ")
    raw = ET.tostring(selected, encoding="utf-8", xml_declaration=True) + b"\n"
    (S / (PREFIX + name)).write_bytes(raw)


def packet():
    snapshot, inputs, jm, kd = frozen()
    assert load(C / "progress.json")["batch"] == "091"
    row = next(r for r in load(S / "source-index.json") if r["kanji"] == CHAR)
    assert row["sourceRow"] == 102
    assert json.loads(inputs["n1-kanji-source-20261102.json"])[101] == CHAR
    assert not (R / row["article"]).exists() and not (R / row["strokeFile"]).exists()
    ids = [e.findtext("ent_seq") for e in jm.findall("entry")
           if any(CHAR in k.text for k in e.findall("k_ele/keb"))]
    save(S / (PREFIX + "lexical-selection.json"), {
        "schemaVersion": 1, "batch": "091", "entryIds": ids,
        "sourceSnapshot": "docs/n1-source-snapshot.json",
        "selectionRule": "Every complete frozen family containing U+5203 in any keb; preserve every alias/reading/restriction/sense.",
        "limits": "Extraction alone is not inspection, per-character allocation, frequency evidence or independent review.",
    })
    (S / (PREFIX + "jmdict.xml")).write_bytes(extract(
        inputs["n1-implementation-JMdict_e.gz"],
        snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids))
    character_packet(kd, CHAR, "kanjidic2.xml")
    save(S / (PREFIX + "input-metadata.json"), {
        "schemaVersion": 1, "batch": "091", "baseCommit": BASE, "sourceIndexRecord": row,
        "characters": [CHAR], "rawCharacterPacket": PREFIX + "kanjidic2.xml",
        "rawCharacterPacketSha256": sha((S / (PREFIX + "kanjidic2.xml")).read_bytes()),
        "provenance": "Complete frozen character record/header parsed and reserialized.",
        "dictionaryAttribution": "Copyright James William Breen and EDRDG; CC BY-SA4.0; repositoryNOTICE.",
    })
    candidates = []
    for path in sorted((R / "words").glob("*.md")):
        name = path.relative_to(R).as_posix()
        m = metadata(R, name)
        if CHAR in m.get("kanji", []) or CHAR in m["word"]:
            candidates.append({"article": name, "metadata": m})
    save(C / "batch-091-source-navigation.json", {
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
    (C / "batch-091-full-family-reading.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"families": len(ids), "candidates": candidates}, ensure_ascii=True, indent=2))


def comparison():
    snapshot, inputs, jm, kd = frozen()
    words = ["乃", "凹", "凸", "刀", "日本刀", "ナイフ", "包丁", "切る", "端", "縁", "先端"]
    ids = [e.findtext("ent_seq") for e in jm.findall("entry")
           if any(k.text in words for k in e.findall("k_ele/keb"))
           or (not e.findall("k_ele") and any(k.text == "ナイフ" for k in e.findall("r_ele/reb")))]
    save(S / (PREFIX + "comparison-selection.json"), {
        "schemaVersion": 1, "batch": "091", "exactSpellings": words, "entryIds": ids,
        "rule": "Complete frozen families with exact listed keb; kana-only ナイフ matched by reb.",
        "limits": "Bounded navigation packet, not exhaustive quiz or linguistic acceptance.",
    })
    (S / (PREFIX + "comparison-jmdict.xml")).write_bytes(extract(
        inputs["n1-implementation-JMdict_e.gz"],
        snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids))
    character_packet(kd, "乃凹凸刀", "comparison-kanjidic2.xml")
    print(json.dumps({"comparisonFamilies": len(ids), "rawCharacterRecords": 4}))


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

    path = C / "inputs" / "batch-091-ha.html"
    raw = path.read_bytes()
    parser = ArticleText()
    parser.feed(raw.decode("utf-8"))
    text = "\n".join(line.strip() for line in "".join(parser.parts).splitlines()
                     if line.strip()) + "\n"
    assert "じん【刃】" in text and "は【刃】" in text and "やい" in text
    archive = S / (PREFIX + "ha.html.gz")
    archive.write_bytes(gzip.compress(raw, mtime=0))
    target = S / (PREFIX + "ha-public-text.txt")
    target.write_text(text, encoding="utf-8")
    save(S / (PREFIX + "public-source-receipts.json"), {
        "ha": {
            "url": "https://kotobank.jp/word/%E5%88%83-536578",
            "retrievedAt": datetime.now(timezone.utc).isoformat(),
            "sourcePath": str(path), "sourceSha256": sha(raw),
            "archive": archive.name, "archiveSha256": sha(archive.read_bytes()),
            "losslessGzip": gzip.decompress(archive.read_bytes()) == raw,
            "extractedText": target.name, "extractedTextSha256": sha(target.read_bytes()),
            "extractionLimits": "Article-only HTMLParser extraction; links/formatting and image glyphs stripped. Identified Daijisen/Nikkoku lexical and character headings are evidence, not all historical claims.",
        },
        "navigationDiagnostic": {
            "attemptedUrl": "https://kotobank.jp/word/%E5%88%83-80864",
            "actualHeadword": "白鳥庫吉",
            "disposition": "Wrong numeric URL redirected to an unrelated biography; explicitly rejected as evidence. Unsuffixed 刃 resolved to the correct 536578 entry, then exact correct HTML downloaded. No denial or permission workaround.",
        },
    })
    print("Public article extraction:", len(text.splitlines()), "lines.")


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
    assert len(named) == len(set(named)) == 1232 and named[101] == CHAR
    unicode_rows = [line.split(";") for line in inputs["n1-UnicodeData-17.0.0.txt"]
                    .decode("utf-8").splitlines()]
    assert next(r for r in unicode_rows if r[0] == "2F11")[5] == "<compat> 5200"
    canonical = lambda e: ET.canonicalize(ET.tostring(e, encoding="unicode"), strip_text=True)
    character = next(e for e in kd.findall("character") if e.findtext("literal") == CHAR)
    assert metadata_record(character, {18: "刀"}) == row["metadata"]
    for name, chars in [("kanjidic2.xml", CHAR), ("comparison-kanjidic2.xml", "乃凹凸刀")]:
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
                             for k in e.findall("k_ele/keb"))
                      or (not e.findall("k_ele")
                          and any(k.text == "ナイフ" for k in e.findall("r_ele/reb")))]
    assert len(exact_ids) == 56 and len(comparison_ids) == 22
    for stem, ids in [("", exact_ids), ("comparison-", comparison_ids)]:
        selected_ids = (comparison_selection["entryIds"] if stem
                        else load(S / (PREFIX + "lexical-selection.json"))["entryIds"])
        assert ids == selected_ids
        assert (S / (PREFIX + stem + "jmdict.xml")).read_bytes() == extract(
            inputs["n1-implementation-JMdict_e.gz"],
            snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
    compact_path = C / "batch-091-full-family-reading.txt"
    compact = compact_path.read_text(encoding="utf-8").splitlines()
    original_entries = ET.parse(S / (PREFIX + "jmdict.xml")).getroot().findall("entry")
    assert len(compact) == len(original_entries) == 56
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
    assert [d["reading"] for d in selected] == ["は"]
    assert [d["reading"] for d in progress["readingDispositions"] if d["sourceOnly"]] == ["き.る"]
    assert all(d["qualification"] and d["evidence"] for d in progress["readingDispositions"])
    projection = progress["proposedCuratedProjection"]
    assert projection["onKeys"] == offered_keys(projection["quizOnyomi"]) == []
    assert projection["kunKeys"] == offered_keys(projection["quizKunyomi"]) == ["は"]
    pairs = set()
    for mapping in progress["proposedSupportMapping"]:
        assert lexical_pair(families[mapping["entryId"]], mapping["word"], mapping["primaryReading"])
        assert mapping["entryId"] in exact_ids
        written = list(dict.fromkeys(c for c in mapping["word"] if 0x4E00 <= ord(c) <= 0x9FFF))
        assert mapping["allWrittenKanji"] == written == [CHAR]
        assert not (R / mapping["article"]).exists() and mapping["preservedWordJlpt"] is None
        for char in written:
            if char == CHAR or (R / "kanji" / (char + ".md")).exists():
                pairs.add((char, mapping["article"]))
    assert pairs == {tuple(p) for p in progress["proposedReciprocalPairs"]}
    assert len(pairs) == 1
    directions = {(f"kanji/{char}.md", article) for char, article in pairs}
    directions |= {(article, f"kanji/{char}.md") for char, article in pairs}
    assert {(d["from"], d["to"]) for d in progress["proposedDirectedLinkPlan"]} == directions
    assert progress["requiredDirectionCount"] == len(directions) == 2
    nav = load(C / "batch-091-source-navigation.json")
    assert nav["baselinePairs"] == progress["activatedBaselinePairs"] == nav["candidates"] == []
    primary_candidates = []
    for path in (R / "words").glob("*.md"):
        name = path.relative_to(R).as_posix()
        m = metadata(R, name)
        if m["reading"] == "は":
            primary_candidates.append({"article": name, "metadata": m,
                                       "sameSelectedLexicalFamily": lexical_pair(families["1369820"], m["word"], m["reading"])})
    assert all(not c["sameSelectedLexicalFamily"] for c in primary_candidates)
    assert progress["membership"] == load(S / (PREFIX + "membership.json"))["membership"] == [CHAR]
    assert progress["drafted"] == progress["reviewClosed"] == progress["published"] == []
    assert progress["proposedReusedChanges"] == []
    quiz = progress["proposedQuiz"]
    assert quiz["labels"] == [metadata(R, f"kanji/{char}.md")["title"] for char in quiz["distractors"]]
    assert len(quiz["distractors"]) == len(set(quiz["distractors"])) == 3
    assert all(metadata(R, f"kanji/{char}.md")["jlpt"] == 1 for char in quiz["distractors"])
    assert all(metadata(R, path.relative_to(R).as_posix())["title"] != quiz["kanjiTitle"]
               for path in (R / "kanji").glob("*.md"))
    assert all(len(metadata(R, f"kanji/{char}.md")["distractors"]) == 3 for char in "刀辺際")
    guards = {(item["word"], other) for item in quiz["proposedDirectExclusions"] for other in item["exclude"]}
    assert guards == {("刃", other) for other in ["刀", "日本刀", "端", "縁"]}
    assert all((R / "words" / (other + ".md")).exists() for _, other in guards)
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json")
    checked = sum(len(v) for v in manifest.values() if isinstance(v, dict))
    assert checked == 8429 and manifest["contentVersion"] == "ceee0f79a6d394df"
    assert not git("diff", BASE, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    baseline = load(S / "baseline-inventory.json")
    original = {Path(n).stem for n in baseline["files"] if n.startswith("kanji/")}
    current = {p.stem for p in (R / "kanji").glob("*.md")}
    accepted = set("幹氏扱乃凹凸矛鷹彗漱栞莉")
    for path in S.glob("batch-*-progress.json"):
        accepted.update(load(path).get("published", []))
    earlier = set("保案派第策結")
    assert len(accepted) == 117 and accepted <= current - original and accepted <= set(named)
    assert len(current) == 1113 and len(set(named) & current) == 127
    assert current & set(named) == (original & set(named)) | accepted | earlier
    assert len(set(named) - current) == 1105
    assert all(metadata(R, f"kanji/{char}.md")["jlpt"] == 2 for char in earlier)
    assert metadata(R, "kanji/妖.md")["jlpt"] == 1
    tree = json.loads(inputs["n1-kanjivg-tree-70a0b7ae.json"])
    assert not tree["truncated"] and tree["sha"] == snapshot["kanjivg"]["revision"]
    assert next(t for t in tree["tree"] if t["path"] == row["kanjivgInventory"]["path"]) == row["kanjivgInventory"]
    svg_path = C / "inputs" / "n1-05203-70a0b7ae.svg"
    svg = svg_path.read_bytes()
    blob = hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest()
    assert blob == row["kanjivgInventory"]["sha"] and len(svg) == row["kanjivgInventory"]["size"]
    paths = ET.fromstring(svg).findall(".//{http://www.w3.org/2000/svg}path")
    assert len(paths) == row["metadata"]["strokes"] == 3
    assert [p.attrib["id"] for p in paths] == ["kvg:05203-s1", "kvg:05203-s2", "kvg:05203-s3"]
    converter = sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n"))
    assert converter == snapshot["kanjivg"]["converter"]["normalizedSha256"]
    stroke = {
        "schemaVersion": 1, "batch": "091", "revision": tree["sha"], "input": str(svg_path),
        "gitBlob": blob, "bytes": len(svg), "sha256": sha(svg),
        "sourceUrl": "https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/kanji/05203.svg",
        "dictionaryStrokeCount": 3, "sourceStrokePaths": 3, "converted": False,
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
    for old in load(S / "batch-090-font-preparation.json")["fonts"]:
        path = Path(old["path"])
        assert path.is_relative_to(A) and sha(path.read_bytes()) == old["sha256"]
        with TTFont(path) as font:
            cmap = font.getBestCmap()
        fonts.append({"path": str(path), "sha256": old["sha256"],
                      "keyGlyphPresence": {char: ord(char) in cmap for char in han},
                      "allProposedMissing": [char for char in han if ord(char) not in cmap]})
    rare = [char for char in han if 0x2E80 <= ord(char) <= 0x2FDF or 0x3400 <= ord(char) <= 0x4DBF
            or 0xF900 <= ord(char) <= 0xFAFF or 0x20000 <= ord(char) <= 0x2FFFF]
    save(S / (PREFIX + "font-preparation.json"), {
        "schemaVersion": 1, "batch": "091", "proposedTextInventory": progress["proposedHanText"],
        "auditedHan": han, "auditedHanCount": len(han), "fonts": fonts,
        "rareHanRangeCharacters": rare,
        "unicodeRadicalCompatibility": "Frozen Unicode17.0.0 U+2F11 maps to ordinary刀 U+5200; no compatibility radical glyph proposed.",
        "mechanism": "Unchanged RareHan.kt/RareHanTest.kt read; all three actual bundled font cmaps inspected.",
        "limits": "Proposed inventory only, not final runtimeHan/nativelegibility/fallbackface. Fresh four-font/all-Han rendering and non-skipped RareHan test remain required. Cmap presence/absence is not glyph acceptance.",
    })
    receipt = load(S / (PREFIX + "public-source-receipts.json"))["ha"]
    raw = Path(receipt["sourcePath"]).read_bytes()
    assert sha(raw) == receipt["sourceSha256"]
    archive = S / receipt["archive"]
    assert sha(archive.read_bytes()) == receipt["archiveSha256"]
    assert gzip.decompress(archive.read_bytes()) == raw
    assert sha((S / receipt["extractedText"]).read_bytes()) == receipt["extractedTextSha256"]
    evidence["actualPacketLineCounts"] = {
        name: len((S / (PREFIX + name)).read_text(encoding="utf-8").splitlines())
        for name in ["jmdict.xml", "kanjidic2.xml", "comparison-jmdict.xml", "comparison-kanjidic2.xml"]}
    evidence["familyCounts"] = {"allExactMemberFamilies": 56, "comparisonFamilies": 22,
                                "distinctCompleteFamilies": len(set(exact_ids + comparison_ids))}
    save(evidence_path, evidence)
    result = {
        "schemaVersion": 1, "execution": 645, "batch": "091", "baseCommit": BASE,
        "stage": progress["status"], "membership": [CHAR], "sourceRow": 102,
        "frozenInputHashesVerified": len(inputs), "decompressedDictionaryHashesVerified": 2,
        "exactFrozenNamedMembershipAndRowVerified": True, "completeLexicalFamilies": 56,
        "completeComparisonFamilies": 22, "allExtractedEntryIdsAccountedFor": True,
        "freshExactDictionaryExtractionsVerified": 2, "rawCharacterRecordsVerified": 5,
        "compactFullFamilyTextSemanticallyEqualToRawXml": True,
        "proposedMetadataReadingDispositionsVerified": 5,
        "proposedOnKeys": projection["onKeys"], "proposedKunKeys": projection["kunKeys"],
        "proposedNewSupportArticles": 1, "proposedReusedSupportArticles": 0,
        "samePrimaryKanaCandidates": primary_candidates,
        "allMappedReciprocalPairs": 1, "requiredDirectedLinks": 2,
        "activatedBaselinePairs": 0, "proposedDirectWordGuards": len(guards),
        "pinnedSvg": stroke, "proposedHanCount": len(han),
        "fontPreparation": PREFIX + "font-preparation.json",
        "mainFontCmapAbsences": fonts[0]["allProposedMissing"],
        "inspectedArticleHashes": {name: sha((R / name).read_bytes())
                                  for name in evidence["authorInspection"]["completeExistingArticlesRead"]},
        "runtimeManifestEqualToPublishedBase": True, "runtimeHashesUnchanged": checked,
        "contentVersion": manifest["contentVersion"], "publishedAdditions": 117,
        "remainingAcceptanceAdditions": 1111, "actuallyAbsentNamedMembers": 1105,
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
        path = L / f"{name}-645.txt"
        text = path.read_text(encoding="utf-8-sig")
        assert "Traceback" not in text and "FAILED" not in text
        if name == "source-tests":
            assert "Ran 43 tests" in text and "OK" in text
        elif name == "validate":
            assert "0 error(s)" in text
        elif name == "audit":
            assert '"runtimeHashesUnchanged": 8429' in text
        raw = path.read_bytes()
        archive = S / f"batch-091-{name}-645.txt.gz"
        archive.write_bytes(gzip.compress(raw, mtime=0))
        assert gzip.decompress(archive.read_bytes()) == raw
        checks[name] = {"path": str(path), "sha256": sha(raw),
                        "archive": archive.name, "archiveSha256": sha(archive.read_bytes()),
                        "losslessGzip": True, "provenance": "Direct redirected subprocess stdout/stderr; exit0 checked by wrapper."}
    recipe = S / (PREFIX + "source-recipe.py")
    recipe.write_bytes(Path(__file__).read_bytes())
    save(S / "execution-645.json", {
        "schemaVersion": 1, "execution": 645, "batch": "091", "baseCommit": BASE,
        "startingState": load(C / "progress.json")["execution645StartingState"],
        "sourceAudit": PREFIX + "preparation-audit.json", "sourcePacket": PREFIX + "progress.json",
        "sourceEvidence": PREFIX + "source-evidence.json",
        "recipe": {"durableControlPath": str(Path(__file__)), "archive": recipe.name,
                   "sha256": sha(recipe.read_bytes())},
        "checks": checks, "runtimeChanged": False, "runtimePublished": False,
        "focusedTestsPassed": 43,
        "focusedTestCommand": "python -X utf8 -B -m unittest test_freeze_n1_sources test_extract_n1_jmdict test_audit_n1_pilot test_audit_n1_batch; PYTHONPATH=tools",
        "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 117, "remainingAdditions": 1111,
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
    assert changed and all(name.startswith("docs/n1-sources/batch-091-") or name == "docs/n1-sources/execution-645.json"
                           for name in changed)
    before = load(L / "progress-before-645.json")
    p = load(C / "progress.json")
    allowed = {"checkpoint", "status", "stage", "batch", "nextAction", "blocker"}
    assert (p["checkpoint"], p["batch"]) == (644, "091")
    assert all(p.get(key) == value for key, value in before.items() if key not in allowed)
    issue = load(L / "issue-response-645.json")
    body = (C / "execution645-issue.txt").read_bytes().decode("utf-8")
    assert issue["user"]["login"] == "stop-cran" and issue["body"] == body
    assert issue["issue_url"].endswith("/issues/60")
    receipt = {"id": issue["id"], "url": issue["html_url"], "author": "stop-cran",
               "bodySha256": sha(body.encode("utf-8")), "verified": True}
    audit_record = load(S / (PREFIX + "preparation-audit.json"))
    state = {
        "schemaVersion": 1, "execution": 645, "checkpoint": 645, "batch": "091",
        "status": "continue", "stage": "source-prepared-not-drafted", "savedCommit": head,
        "signature": "G", "lastPublishedCommit": BASE,
        "sourcePacket": "docs/n1-sources/batch-091-progress.json",
        "sourceAudit": "docs/n1-sources/batch-091-preparation-audit.json",
        "evidence": "docs/n1-sources/execution-645.json",
        "membership": [CHAR], "sourceRow": 102, "completeDictionaryFamilies": 78,
        "lexicalFamilies": 56, "comparisonFamilies": 22, "completeRawCharacterRecords": 5,
        "metadataReadings": 5, "proposedNewSupportArticles": 1, "proposedReusedSupportArticles": 0,
        "allMappedReciprocalPairs": 1, "proposedLinkDirections": 2,
        "pinnedSvgPaths": 3, "geometryConverted": False, "proposedDirectWordGuards": 4,
        "proposedHanCount": audit_record["proposedHanCount"],
        "dedicatedWorktreesClean": True, "runtimeChanged": False, "runtimePublished": False,
        "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 117, "remainingAdditions": 1111,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "runtimeHashesUnchanged": 8429, "originalHistoricalRootKeysCompared": len(before),
        "allOriginalHistoricalValuesPreserved": True,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "issueUpdate": receipt["url"],
        "ownerIssueAuthorAndBodyVerified": True,
        "nextAction": load(S / (PREFIX + "progress.json"))["nextAction"],
    }
    p["execution645CoordinatorCheckpoint"] = state
    p["batch091SourcePreparation"] = state
    p["batch091SourcePreparationIssueReceipt"] = receipt
    p.update(checkpoint=645, status="continue", stage="batch-091-source-prepared-not-drafted",
             blocker=None, nextAction=state["nextAction"])
    save(C / "progress.json", p)
    reread = load(C / "progress.json")
    assert all(reread.get(key) == value for key, value in before.items() if key not in allowed)
    save(L / "execution-645-final-checkpoint.json", state)
    print(json.dumps(state, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=["start", "packet", "comparison", "public", "audit", "record", "seal"])
    args = parser.parse_args()
    globals()[args.stage]()

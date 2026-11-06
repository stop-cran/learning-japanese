"""Prepare one source-only checkpoint from approved frozen workspace inputs."""
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
from html.parser import HTMLParser
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
S = R / "docs" / "n1-sources"
L = C / "logs" / "0ea99a3b-35f4-4eb7-8b2a-aa2c02e3b91a"
BASE = "6eaa018dcbcabe57d9e22ddf6b07c6b8ee2dfea6"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
CHAR = "\u51ea"
PREFIX = "batch-087-"
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata, offered_keys
from build_manifest import build_manifest
from extract_n1_jmdict import extract


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    temporary = path.with_suffix(path.suffix + ".609.tmp")
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
    assert (p["checkpoint"], p["batch"], p["status"]) == (608, "086", "continue")
    assert p["lastPublishedCommit"] == BASE and p["remainingAdditions"] == 1115
    assert not list(S.glob(PREFIX + "*"))
    assert not (L / "progress-before-609.json").exists()
    shutil.copyfile(C / "progress.json", L / "progress-before-609.json")
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
    assert json.loads(text.split(marker, 1)[1])["checkpoint"] == 608
    runner = load(C / "runner.json")
    assert runner["pid"] == 19008 and runner["status"] == "running"
    assert runner["sessionId"] == L.name
    state = {
        "execution": 609, "batch": "087", "startingHead": BASE, "freshOriginMain": BASE,
        "androidHead": APP, "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "ONE bounded087 source-preparation checkpoint only; no runtime draft, reviewer, Android/native, publication,088 or second runner.",
        "request": {"sha256": sha(raw), "bytes": len(raw), "characters": len(text),
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded and embedded checkpoint decoded. Operative contract, approved issue and final608 inspected directly; historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": "Win32_Process verified current coordinator29104 parent19008 and child15676. runner.json identifies live parent19008 and exact session. Parent retains runner.lock; child never acquires/deletes/unlocks it.",
        "artifactPathPreflight": {"durableHelper": str(Path(__file__)),
                                  "priorArt": "Approved control batch-086-source-600.py and committed source packets; existing extract/freeze/audit tools; approved frozen workspace inputs only.",
                                  "optionalHistoricalSessionHelpersAccessed": False},
        "actualNewPermissionDenials": [],
        "worktrees": "Wholly clean dedicated content and qualified TESTONLY Android; normal signatures G. Fresh origin/main equals content. Android1c1b7bf4 is atop unchanged productionf9b59a2, not latest app main. Canonical repositories not accessed.",
    }
    p["execution609StartingState"] = state
    p.update(batch="087", stage="batch-087-source-preparation-in-progress",
             nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    print("Starting scope persisted with full live history.")


def packet():
    assert load(C / "progress.json")["batch"] == "087"
    snapshot, inputs, jm, kd = frozen()
    row = next(r for r in load(S / "source-index.json") if r["kanji"] == CHAR)
    assert row["sourceRow"] == 96
    assert json.loads(inputs["n1-kanji-source-20261102.json"])[95] == CHAR
    assert not (R / row["article"]).exists() and not (R / row["strokeFile"]).exists()
    ids = [e.findtext("ent_seq") for e in jm.findall("entry")
           if any(CHAR in k.text for k in e.findall("k_ele/keb"))]
    selection = {
        "schemaVersion": 1, "batch": "087", "entryIds": ids,
        "sourceSnapshot": "docs/n1-source-snapshot.json",
        "selectionRule": "Every complete frozen family containing exact source member U+51EA in any keb; preserve all aliases/readings/restrictions/senses.",
        "limits": "Extraction alone is not inspection, per-character allocation, frequency evidence or independent review.",
    }
    save(S / (PREFIX + "lexical-selection.json"), selection)
    raw = extract(inputs["n1-implementation-JMdict_e.gz"],
                  snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
    (S / (PREFIX + "jmdict.xml")).write_bytes(raw)
    selected = ET.Element("kanjidic2")
    selected.append(copy.deepcopy(kd.find("header")))
    selected.append(copy.deepcopy(next(e for e in kd.findall("character")
                                      if e.findtext("literal") == CHAR)))
    ET.indent(selected, space="  ")
    raw_kd = ET.tostring(selected, encoding="utf-8", xml_declaration=True) + b"\n"
    (S / (PREFIX + "kanjidic2.xml")).write_bytes(raw_kd)
    save(S / (PREFIX + "input-metadata.json"), {
        "schemaVersion": 1, "batch": "087", "baseCommit": BASE, "sourceIndexRecord": row,
        "characters": [CHAR], "rawCharacterPacket": PREFIX + "kanjidic2.xml",
        "rawCharacterPacketSha256": sha(raw_kd),
        "provenance": "Complete frozen character record/header, parsed and reserialized.",
        "dictionaryAttribution": "Copyright James William Breen and EDRDG; CC BY-SA4.0; repositoryNOTICE.",
    })
    candidates = []
    for path in sorted((R / "words").glob("*.md")):
        name = path.relative_to(R).as_posix()
        m = metadata(R, name)
        if CHAR in m.get("kanji", []) or CHAR in m["word"]:
            candidates.append({"article": name, "metadata": m})
    save(C / "batch-087-source-navigation.json", {
        "sourceIndexRecord": row, "candidates": candidates,
        "baselinePairs": [r for r in load(S / "baseline-word-candidates.json") if r["kanji"] == CHAR],
    })
    print(json.dumps({"families": len(ids), "lines": len(raw.splitlines()),
                      "candidates": candidates}, ensure_ascii=True, indent=2))


def comparison():
    snapshot, inputs, jm, kd = frozen()
    words = ["\u98a8", "\u51e1", "\u51f9", "\u6b62", "\u9759\u307e\u308b",
             "\u6b62\u3080", "\u843d\u3061\u7740\u304f", "\u7a4f\u3084\u304b",
             "\u9759\u304b", "\u51b7\u9759", "\u6642\u5316", "\u548c\u3050"]
    ids = [e.findtext("ent_seq") for e in jm.findall("entry")
           if any(k.text in words for k in e.findall("k_ele/keb"))]
    save(S / (PREFIX + "comparison-selection.json"), {
        "schemaVersion": 1, "batch": "087", "exactSpellings": words, "entryIds": ids,
        "rule": "Complete frozen families with any exact keb matching one of the recorded comparison spellings; no substring allocation.",
        "limits": "Bounded navigation packet, not exhaustive quiz or linguistic acceptance.",
    })
    raw = extract(inputs["n1-implementation-JMdict_e.gz"],
                  snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
    (S / (PREFIX + "comparison-jmdict.xml")).write_bytes(raw)
    chars = "\u98a8\u51e1\u51f9\u6b62"
    selected = ET.Element("kanjidic2")
    selected.append(copy.deepcopy(kd.find("header")))
    for char in chars:
        selected.append(copy.deepcopy(next(e for e in kd.findall("character")
                                          if e.findtext("literal") == char)))
    ET.indent(selected, space="  ")
    (S / (PREFIX + "comparison-kanjidic2.xml")).write_bytes(
        ET.tostring(selected, encoding="utf-8", xml_declaration=True) + b"\n")
    print(json.dumps({"comparisonFamilies": len(ids), "lexicalLines": len(raw.splitlines()),
                      "characterRecords": len(chars)}, ensure_ascii=True))


class PublicText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.capture = False
        self.depth = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "article":
            self.capture = True
            self.depth += 1
            self.parts.append("\n[ARTICLE " + attrs.get("class", "") + "]\n")
        if self.capture:
            if tag in {"br", "p", "h2", "h3", "section"}:
                self.parts.append("\n")
            elif tag == "img":
                self.parts.append("[image:" + attrs.get("src", "") + "]")

    def handle_endtag(self, tag):
        if tag == "article" and self.capture:
            self.depth -= 1
            self.capture = self.depth > 0
            self.parts.append("\n[END ARTICLE]\n")

    def handle_data(self, data):
        if self.capture:
            self.parts.append(data)


def public():
    outputs = {}
    for name in ["nagi", "nagu"]:
        path = C / "inputs" / f"batch-087-{name}.html"
        raw = path.read_bytes()
        parser = PublicText()
        parser.feed(raw.decode("utf-8"))
        text = "\n".join(line.strip() for line in "".join(parser.parts).splitlines()
                         if line.strip()) + "\n"
        assert CHAR in text and "デジタル大辞泉" in text
        archive = S / f"batch-087-{name}.html.gz"
        archive.write_bytes(gzip.compress(raw, mtime=0))
        assert gzip.decompress(archive.read_bytes()) == raw
        text_path = S / f"batch-087-{name}-public-text.txt"
        text_path.write_text(text, encoding="utf-8")
        outputs[name] = {
            "url": "https://kotobank.jp/word/" + (CHAR if name == "nagi" else CHAR + "\u3050"),
            "sourcePath": str(path), "sourceSha256": sha(raw), "archive": archive.name,
            "archiveSha256": sha(archive.read_bytes()), "losslessGzip": True,
            "extractedText": text_path.name, "extractedTextSha256": sha(text_path.read_bytes()),
            "extractionLimits": "Coordinator HTMLParser article-only extraction; formatting/links stripped, image placeholders retained; all dictionary articles retained. Not independent upstream retrieval or historical-glyph inspection.",
        }
        print(name + "\n" + text)
    save(S / (PREFIX + "public-source-receipts.json"), outputs)


def audit():
    from audit_n1_batch import lexical_pair
    from fontTools.ttLib import TTFont
    from freeze_n1_sources import metadata_record

    def distinct_object(pairs):
        result = {}
        for key, value in pairs:
            assert key not in result, f"Duplicate evidence key: {key}"
            result[key] = value
        return result

    for path in S.glob(PREFIX + "*.json"):
        json.loads(path.read_text(encoding="utf-8-sig"), object_pairs_hook=distinct_object)
    snapshot, inputs, jm, kd = frozen()
    progress = load(S / (PREFIX + "progress.json"))
    evidence_path = S / (PREFIX + "source-evidence.json")
    evidence = load(evidence_path)
    row = next(r for r in load(S / "source-index.json") if r["kanji"] == CHAR)
    named = json.loads(inputs["n1-kanji-source-20261102.json"])
    assert named == load(S / "community-list-20261102.json")
    assert len(named) == len(set(named)) == 1232 and named[95] == CHAR
    unicode_rows = [line.split(";") for line in inputs["n1-UnicodeData-17.0.0.txt"]
                    .decode("utf-8").splitlines()]
    radical = next(r for r in unicode_rows if r[0] == "2F0F")
    assert radical[5] == "<compat> 51E0"
    canonical = lambda e: ET.canonicalize(ET.tostring(e, encoding="unicode"), strip_text=True)
    character = next(e for e in kd.findall("character") if e.findtext("literal") == CHAR)
    assert metadata_record(character, {16: "\u51e0"}) == row["metadata"]
    for name, chars in [("kanjidic2.xml", CHAR),
                        ("comparison-kanjidic2.xml", "\u98a8\u51e1\u51f9\u6b62")]:
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
    assert len(exact_ids) == 10 and len(comparison_ids) == 15
    for stem, ids in [("", exact_ids), ("comparison-", comparison_ids)]:
        selected_ids = (comparison_selection["entryIds"] if stem
                        else load(S / (PREFIX + "lexical-selection.json"))["entryIds"])
        assert ids == selected_ids
        assert (S / (PREFIX + stem + "jmdict.xml")).read_bytes() == extract(
            inputs["n1-implementation-JMdict_e.gz"],
            snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
    decision_ids = [i for group in evidence["lexicalDecisions"] for i in group["entryIds"]]
    assert len(decision_ids) == len(set(decision_ids)) == 10
    assert set(decision_ids) == set(exact_ids)
    expected = [(kind, reading) for kind, field in [("on", "onyomi"), ("kun", "kunyomi")]
                for reading in row["metadata"][field]]
    assert [(d["kind"], d["reading"]) for d in progress["readingDispositions"]] == expected
    assert progress["sourceReadingOrder"] == {k: row["metadata"][k] for k in ["onyomi", "kunyomi"]}
    assert all(not d["sourceOnly"] and d["proposedQuizSelection"]
               for d in progress["readingDispositions"])
    projection = progress["proposedCuratedProjection"]
    assert projection["onKeys"] == offered_keys(projection["quizOnyomi"]) == []
    assert projection["kunKeys"] == offered_keys(projection["quizKunyomi"]) == ["\u306a\u304e", "\u306a\u3050"]
    mapping = progress["proposedSupportMapping"]
    pairs = set()
    for m in mapping:
        assert not (R / m["article"]).exists()
        assert lexical_pair(families[m["entryId"]], m["word"], m["primaryReading"])
        assert m["entryId"] in exact_ids and m["allWrittenKanji"] == [CHAR]
        assert m["preservedWordJlpt"] is None
        pairs.add((CHAR, m["article"]))
    assert len(mapping) == len(pairs) == 2
    assert pairs == {tuple(p) for p in progress["proposedReciprocalPairs"]}
    directions = {(f"kanji/{c}.md", article) for c, article in pairs}
    directions |= {(article, f"kanji/{c}.md") for c, article in pairs}
    progress["proposedDirectedLinkPlan"] = [{"from": a, "to": b} for a, b in sorted(directions)]
    progress["requiredDirectionCount"] = 4
    progress["alreadyExistingRequiredDirections"] = []
    nav = load(C / "batch-087-source-navigation.json")
    assert nav["candidates"] == nav["baselinePairs"] == progress["activatedBaselinePairs"] == []
    kana_candidates = []
    for path in (R / "words").glob("*.md"):
        name = path.relative_to(R).as_posix()
        m = metadata(R, name)
        if m["reading"] in ["\u306a\u304e", "\u306a\u3050"]:
            kana_candidates.append({"article": name, "metadata": m})
    assert not kana_candidates
    assert progress["membership"] == load(S / (PREFIX + "membership.json"))["membership"] == [CHAR]
    assert progress["drafted"] == progress["reviewClosed"] == progress["published"] == []
    quiz = progress["proposedQuiz"]
    assert quiz["labels"] == [metadata(R, f"kanji/{c}.md")["title"] for c in quiz["distractors"]]
    assert len(quiz["distractors"]) == len(set(quiz["distractors"])) == 3
    for name in ["\u5b89", "\u5e73", "\u9759"]:
        assert len(metadata(R, f"kanji/{name}.md")["distractors"]) == 3
    guards = {(r["word"], other) for r in quiz["proposedDirectExclusions"] for other in r["exclude"]}
    assert len(guards) == 7 and all((R / "words" / f"{b}.md").exists() for _, b in guards)
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json")
    checked = sum(len(v) for v in manifest.values() if isinstance(v, dict))
    assert checked == 8416 and manifest["contentVersion"] == "86e8cb13aa72ecd0"
    assert not git("diff", BASE, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    baseline = load(S / "baseline-inventory.json")
    original = {Path(n).stem for n in baseline["files"] if n.startswith("kanji/")}
    current = {p.stem for p in (R / "kanji").glob("*.md")}
    accepted = set("\u5e79\u6c0f\u6271\u4e43\u51f9\u51f8\u77db\u9df9\u5f57\u6f31\u681e\u8389")
    for path in S.glob("batch-*-progress.json"):
        accepted.update(load(path).get("published", []))
    earlier = set("\u4fdd\u6848\u6d3e\u7b2c\u7b56\u7d50")
    assert len(accepted) == 113 and accepted <= current - original and accepted <= set(named)
    assert len(current) == 1109 and len(set(named) & current) == 123
    assert current & set(named) == (original & set(named)) | accepted | earlier
    assert len(set(named) - current) == 1109
    assert all(metadata(R, f"kanji/{c}.md")["jlpt"] == 2 for c in earlier)
    assert metadata(R, "kanji/\u5996.md")["jlpt"] == 1
    tree = json.loads(inputs["n1-kanjivg-tree-70a0b7ae.json"])
    assert not tree["truncated"] and tree["sha"] == snapshot["kanjivg"]["revision"]
    assert next(t for t in tree["tree"] if t["path"] == row["kanjivgInventory"]["path"]) == row["kanjivgInventory"]
    svg_path = C / "inputs" / "n1-051ea-70a0b7ae.svg"
    svg = svg_path.read_bytes()
    blob = hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest()
    assert blob == row["kanjivgInventory"]["sha"] and len(svg) == row["kanjivgInventory"]["size"]
    paths = ET.fromstring(svg).findall(".//{http://www.w3.org/2000/svg}path")
    assert len(paths) == row["metadata"]["strokes"] == 6
    assert [p.attrib["id"] for p in paths] == [f"kvg:051ea-s{i}" for i in range(1, 7)]
    converter = sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n"))
    assert converter == snapshot["kanjivg"]["converter"]["normalizedSha256"]
    stroke = {
        "schemaVersion": 1, "batch": "087", "revision": tree["sha"], "input": str(svg_path),
        "gitBlob": blob, "bytes": len(svg), "sha256": sha(svg),
        "sourceUrl": "https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/kanji/051ea.svg",
        "dictionaryStrokeCount": 6, "sourceStrokePaths": 6, "converted": False,
        "nativeDrawingAccepted": False, "converterNormalizedSha256": converter,
        "attribution": "Ulrich Apel and contributors, KanjiVG, CC BY-SA3.0; repositoryNOTICE.",
        "limits": "Pinned SVG inspected and verified; no converted runtime geometry or native drawing acceptance.",
    }
    save(S / (PREFIX + "stroke-evidence.json"), stroke)
    (S / (PREFIX + "kanjivg.svg")).write_bytes(svg)
    han = sorted({c for c in progress["proposedHanText"] if 0x2E80 <= ord(c) <= 0x2FDF
                  or 0x3400 <= ord(c) <= 0x9FFF or 0xF900 <= ord(c) <= 0xFAFF
                  or 0x20000 <= ord(c) <= 0x2FFFF})
    fonts = []
    for old in load(S / "batch-086-font-preparation.json")["fonts"]:
        path = Path(old["path"])
        assert sha(path.read_bytes()) == old["sha256"]
        with TTFont(path) as font:
            cmap = font.getBestCmap()
        fonts.append({"path": str(path), "sha256": old["sha256"],
                      "keyGlyphPresence": {c: ord(c) in cmap for c in han},
                      "allProposedMissing": [c for c in han if ord(c) not in cmap]})
    rare = [c for c in han if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x4DBF
            or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF]
    assert not rare
    save(S / (PREFIX + "font-preparation.json"), {
        "schemaVersion": 1, "batch": "087", "proposedTextInventory": progress["proposedHanText"],
        "auditedHan": han, "auditedHanCount": len(han), "fonts": fonts,
        "rareHanRangeCharacters": rare,
        "mechanism": "Unchanged RareHan.kt/RareHanTest.kt read; all three actual bundled font cmaps inspected.",
        "limits": "Proposed inventory only, not final runtimeHan or native legibility. Fresh fourfont/allHan rendering and non-skipped RareHan test remain required. Cmap presence/absence is not glyph/fallback-face acceptance.",
    })
    for source in load(S / (PREFIX + "public-source-receipts.json")).values():
        raw = Path(source["sourcePath"]).read_bytes()
        assert sha(raw) == source["sourceSha256"]
        archive = S / source["archive"]
        assert sha(archive.read_bytes()) == source["archiveSha256"]
        assert gzip.decompress(archive.read_bytes()) == raw
        assert sha((S / source["extractedText"]).read_bytes()) == source["extractedTextSha256"]
    evidence["actualPacketLineCounts"] = {
        n: len((S / (PREFIX + n)).read_text(encoding="utf-8").splitlines())
        for n in ["jmdict.xml", "kanjidic2.xml", "comparison-jmdict.xml", "comparison-kanjidic2.xml"]}
    evidence["familyCounts"] = {"allExactMemberFamilies": 10, "comparisonFamilies": 15,
                                "distinctCompleteFamilies": len(set(exact_ids + comparison_ids))}
    save(evidence_path, evidence)
    save(S / (PREFIX + "progress.json"), progress)
    result = {
        "schemaVersion": 1, "execution": 609, "batch": "087", "baseCommit": BASE,
        "stage": progress["status"], "membership": [CHAR], "sourceRow": 96,
        "frozenInputHashesVerified": 5, "decompressedDictionaryHashesVerified": 2,
        "exactFrozenNamedMembershipAndRowVerified": True, "completeLexicalFamilies": 10,
        "completeComparisonFamilies": 15, "allExtractedEntryIdsAccountedFor": True,
        "freshExactDictionaryExtractionsVerified": 2, "rawCharacterRecordsVerified": 5,
        "proposedMetadataReadingDispositionsVerified": 2,
        "proposedOnKeys": projection["onKeys"], "proposedKunKeys": projection["kunKeys"],
        "proposedNewSupportArticles": 2, "proposedReusedSupportArticles": 0,
        "existingExactKanaReadingCandidates": kana_candidates,
        "allMappedReciprocalPairs": 2, "requiredDirectedLinks": 4,
        "activatedBaselinePairs": 0, "proposedDirectWordGuards": 7,
        "pinnedSvg": stroke, "proposedHanCount": len(han),
        "fontPreparation": PREFIX + "font-preparation.json",
        "inspectedArticleHashes": {n: sha((R / n).read_bytes())
                                  for n in evidence["authorInspection"]["completeExistingArticlesRead"]},
        "runtimeManifestEqualToPublishedBase": True, "runtimeHashesUnchanged": checked,
        "contentVersion": manifest["contentVersion"], "publishedAdditions": 113,
        "remainingAcceptanceAdditions": 1115, "actuallyAbsentNamedMembers": 1109,
        "separateEarlierLevelSourceMembers": sorted(earlier),
        "separateEarlierPlacementsCountedAsIssue60AcceptedBatches": False,
        "baselinePreservation": "All runtime bytes unchanged from normally signed published base; no metadata/readings/levels/exclusions/geometry changed.",
        "runtimeChanges": 0, "reviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "optionalHistoricalHelpersAccessed": False, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "limits": progress["limits"],
    }
    save(S / (PREFIX + "preparation-audit.json"), result)
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ["limits", "pinnedSvg", "inspectedArticleHashes"]},
                     ensure_ascii=True, indent=2))


def record():
    checks = {}
    for name in ["source-tests", "validate", "budget", "audit", "manifest"]:
        path = L / f"{name}-609.txt"
        text = path.read_text(encoding="utf-8-sig")
        assert "Traceback" not in text and "FAILED" not in text
        if name == "source-tests":
            assert "Ran 43 tests" in text and "OK" in text
        elif name == "validate":
            assert "0 error(s)" in text
        elif name == "audit":
            assert '"runtimeHashesUnchanged": 8416' in text
        raw = path.read_bytes()
        archive = S / f"batch-087-{name}-609.txt.gz"
        archive.write_bytes(gzip.compress(raw, mtime=0))
        assert gzip.decompress(archive.read_bytes()) == raw
        checks[name] = {"path": str(path), "sha256": sha(raw),
                        "archive": archive.name, "archiveSha256": sha(archive.read_bytes()),
                        "losslessGzip": True, "provenance": "Direct redirected subprocess stdout/stderr."}
    recipe = S / (PREFIX + "source-recipe.py")
    recipe.write_bytes(Path(__file__).read_bytes())
    save(S / "execution-609.json", {
        "schemaVersion": 1, "execution": 609, "batch": "087", "baseCommit": BASE,
        "startingState": load(C / "progress.json")["execution609StartingState"],
        "sourceAudit": PREFIX + "preparation-audit.json",
        "sourcePacket": PREFIX + "progress.json", "sourceEvidence": PREFIX + "source-evidence.json",
        "recipe": {"durableControlPath": str(Path(__file__)), "archive": recipe.name,
                   "sha256": sha(recipe.read_bytes())},
        "checks": checks, "runtimeChanged": False, "runtimePublished": False,
        "focusedTestsPassed": 43,
        "focusedTestCommand": "python -X utf8 -B -m unittest test_freeze_n1_sources test_extract_n1_jmdict test_audit_n1_pilot test_audit_n1_batch; PYTHONPATH=tools",
        "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 113, "remainingAdditions": 1115,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False,
        "nextAction": load(S / (PREFIX + "progress.json"))["nextAction"],
        "limits": load(S / (PREFIX + "progress.json"))["limits"],
    })
    print("Source evidence/checks and durable recipe archived; local normal signing next; no push.")


def seal():
    head = git("rev-parse", "HEAD")
    clean(R, head)
    clean(A, APP)
    assert head != BASE and git("rev-parse", "origin/main") == BASE
    assert git("rev-parse", "HEAD^") == BASE
    assert not git("diff", BASE, "HEAD", "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    changed = git("diff", "--name-only", BASE, "HEAD").splitlines()
    assert changed and all(p.startswith("docs/n1-sources/batch-087-") or p == "docs/n1-sources/execution-609.json"
                           for p in changed)
    before = load(L / "progress-before-609.json")
    p = load(C / "progress.json")
    allowed = {"checkpoint", "status", "stage", "batch", "nextAction", "blocker"}
    assert (p["checkpoint"], p["batch"]) == (608, "087")
    assert all(p.get(k) == v for k, v in before.items() if k not in allowed)
    issue = load(L / "issue-response-609.json")
    body = (C / "execution609-issue.txt").read_bytes().decode("utf-8")
    assert issue["user"]["login"] == "stop-cran" and issue["body"] == body
    assert issue["issue_url"].endswith("/issues/60")
    receipt = {"id": issue["id"], "url": issue["html_url"], "author": "stop-cran",
               "bodySha256": sha(body.encode("utf-8")), "verified": True}
    audit_record = load(S / (PREFIX + "preparation-audit.json"))
    state = {
        "schemaVersion": 1, "execution": 609, "checkpoint": 609, "batch": "087",
        "status": "continue", "stage": "source-prepared-not-drafted", "savedCommit": head,
        "signature": "G", "lastPublishedCommit": BASE,
        "sourcePacket": "docs/n1-sources/batch-087-progress.json",
        "sourceAudit": "docs/n1-sources/batch-087-preparation-audit.json",
        "evidence": "docs/n1-sources/execution-609.json",
        "membership": [CHAR], "sourceRow": 96, "completeDictionaryFamilies": 25,
        "lexicalFamilies": 10, "comparisonFamilies": 15, "completeRawCharacterRecords": 5,
        "metadataReadings": 2, "proposedNewSupportArticles": 2, "proposedReusedSupportArticles": 0,
        "allMappedReciprocalPairs": 2, "proposedLinkDirections": 4,
        "pinnedSvgPaths": 6, "geometryConverted": False, "proposedDirectWordGuards": 7,
        "proposedHanCount": audit_record["proposedHanCount"],
        "dedicatedWorktreesClean": True, "runtimeChanged": False, "runtimePublished": False,
        "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 113, "remainingAdditions": 1115,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "runtimeHashesUnchanged": 8416, "originalHistoricalRootKeysCompared": len(before),
        "allOriginalHistoricalValuesPreserved": True,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [],
        "issueUpdate": receipt["url"], "ownerIssueAuthorAndBodyVerified": True,
        "nextAction": load(S / (PREFIX + "progress.json"))["nextAction"],
    }
    p["execution609CoordinatorCheckpoint"] = state
    p["batch087SourcePreparation"] = state
    p["batch087SourcePreparationIssueReceipt"] = receipt
    p.update(checkpoint=609, status="continue", stage="batch-087-source-prepared-not-drafted",
             blocker=None, nextAction=state["nextAction"])
    save(C / "progress.json", p)
    reread = load(C / "progress.json")
    assert all(reread.get(k) == v for k, v in before.items() if k not in allowed)
    save(L / "execution-609-final-checkpoint.json", state)
    print(json.dumps(state, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["start", "packet", "comparison", "public", "audit", "record", "seal"])
    globals()[parser.parse_args().action]()

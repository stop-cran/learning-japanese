"""Prepare batch 088 from frozen workspace inputs; never publish runtime content."""
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
L = C / "logs" / "92077a48-7110-4c68-98f0-9379e8cd9c8d"
BASE = "8a36f8cd81c0e35c330079881cac1a1f3a771e26"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
CHAR = "\u51f1"
PREFIX = "batch-088-"
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata, offered_keys
from build_manifest import build_manifest
from extract_n1_jmdict import extract


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    temporary = path.with_suffix(path.suffix + ".618.tmp")
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
    assert (p["checkpoint"], p["batch"], p["status"]) == (617, "087", "continue")
    assert p["lastPublishedCommit"] == BASE and p["remainingAdditions"] == 1114
    assert not list(S.glob(PREFIX + "*"))
    shutil.copyfile(C / "progress.json", L / "progress-before-618.json")
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
    assert json.loads(text.split(marker, 1)[1])["checkpoint"] == 617
    runner = load(C / "runner.json")
    assert runner["pid"] == 19008 and runner["status"] == "running"
    assert runner["sessionId"] == L.name
    state = {
        "execution": 618, "batch": "088", "startingHead": BASE, "freshOriginMain": BASE,
        "androidHead": APP, "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "ONE bounded088 source-preparation checkpoint only; no runtime draft, reviewer, Android/native, publication,089 or second runner.",
        "request": {"sha256": sha(raw), "bytes": len(raw), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded and embedded checkpoint decoded. Operative contract, complete approved issue and final617 inspected directly; historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": "Win32_Process confirms coordinator23364 parent19008 and shell6328. runner.json identifies live parent19008/exactsession. Parent retains runner.lock; no child acquisition/deletion/unlocking.",
        "artifactPathPreflight": "Approved control helpers, committed packets and frozen workspace inputs only. No optional historical-session helper access.",
        "actualNewPermissionDenials": [],
        "worktrees": "Wholly clean dedicated content and qualified TESTONLY Android; normal signatures G. Fresh main equals content. Android1c1b7bf4 retains productionf9b59a2, not latest app main. Canonical repositories not accessed.",
    }
    p["execution618StartingState"] = state
    p.update(batch="088", stage="batch-088-source-preparation-in-progress",
             nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    print("Starting scope persisted with full history.")


def character_packet(kd, chars, name):
    selected = ET.Element("kanjidic2")
    selected.append(copy.deepcopy(kd.find("header")))
    for char in chars:
        selected.append(copy.deepcopy(next(e for e in kd.findall("character")
                                          if e.findtext("literal") == char)))
    ET.indent(selected, space="  ")
    (S / (PREFIX + name)).write_bytes(
        ET.tostring(selected, encoding="utf-8", xml_declaration=True) + b"\n")


def packet():
    assert load(C / "progress.json")["batch"] == "088"
    snapshot, inputs, jm, kd = frozen()
    row = next(r for r in load(S / "source-index.json") if r["kanji"] == CHAR)
    assert row["sourceRow"] == 97
    assert json.loads(inputs["n1-kanji-source-20261102.json"])[96] == CHAR
    assert not (R / row["article"]).exists() and not (R / row["strokeFile"]).exists()
    ids = [e.findtext("ent_seq") for e in jm.findall("entry")
           if any(CHAR in k.text for k in e.findall("k_ele/keb"))]
    save(S / (PREFIX + "lexical-selection.json"), {
        "schemaVersion": 1, "batch": "088", "entryIds": ids,
        "sourceSnapshot": "docs/n1-source-snapshot.json",
        "selectionRule": "Every complete frozen family containing U+51F1 in any keb; preserve all aliases/readings/restrictions/senses.",
        "limits": "Extraction alone is not inspection, per-character allocation, frequency evidence or independent review.",
    })
    raw = extract(inputs["n1-implementation-JMdict_e.gz"],
                  snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
    (S / (PREFIX + "jmdict.xml")).write_bytes(raw)
    character_packet(kd, CHAR, "kanjidic2.xml")
    save(S / (PREFIX + "input-metadata.json"), {
        "schemaVersion": 1, "batch": "088", "baseCommit": BASE, "sourceIndexRecord": row,
        "characters": [CHAR], "rawCharacterPacket": PREFIX + "kanjidic2.xml",
        "rawCharacterPacketSha256": sha((S / (PREFIX + "kanjidic2.xml")).read_bytes()),
        "provenance": "Complete frozen character record/header, parsed and reserialized.",
        "dictionaryAttribution": "Copyright James William Breen and EDRDG; CC BY-SA4.0; repositoryNOTICE.",
    })
    candidates = []
    for path in sorted((R / "words").glob("*.md")):
        name = path.relative_to(R).as_posix()
        m = metadata(R, name)
        if CHAR in m.get("kanji", []) or CHAR in m["word"]:
            candidates.append({"article": name, "metadata": m})
    save(C / "batch-088-source-navigation.json", {
        "sourceIndexRecord": row, "candidates": candidates,
        "baselinePairs": [r for r in load(S / "baseline-word-candidates.json") if r["kanji"] == CHAR],
    })
    print(json.dumps({"families": len(ids), "lines": len(raw.splitlines()),
                      "candidates": candidates}, ensure_ascii=True, indent=2))


def comparison():
    snapshot, inputs, jm, kd = frozen()
    words = ["\u51e1", "\u51f8", "\u51f9", "\u52dd", "\u65cb",
             "\u5e30\u308b", "\u5e30\u5b85", "\u5e30\u308a", "\u623b\u308b",
             "\u52dd\u3061", "\u512a\u52dd", "\u52dd\u5229",
             "\u548c\u3089\u3050", "\u52dd\u9b28"]
    ids = [e.findtext("ent_seq") for e in jm.findall("entry")
           if any(k.text in words for k in e.findall("k_ele/keb"))]
    save(S / (PREFIX + "comparison-selection.json"), {
        "schemaVersion": 1, "batch": "088", "exactSpellings": words, "entryIds": ids,
        "rule": "Complete frozen families with any exact keb matching a recorded comparison spelling.",
        "limits": "Bounded navigation packet; not exhaustive quiz or linguistic acceptance.",
    })
    raw = extract(inputs["n1-implementation-JMdict_e.gz"],
                  snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
    (S / (PREFIX + "comparison-jmdict.xml")).write_bytes(raw)
    character_packet(kd, "\u51e1\u51f8\u51f9\u52dd\u65cb", "comparison-kanjidic2.xml")
    print(json.dumps({"comparisonFamilies": len(ids), "lines": len(raw.splitlines()),
                      "characterRecords": 5}))


class PublicText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "article":
            self.depth += 1
            self.parts.append("\n[ARTICLE " + attrs.get("class", "") + "]\n")
        if self.depth:
            if tag in {"br", "p", "h2", "h3", "section"}:
                self.parts.append("\n")
            elif tag == "img":
                self.parts.append("[image:" + attrs.get("src", "") + "]")

    def handle_endtag(self, tag):
        if tag == "article" and self.depth:
            self.depth -= 1
            self.parts.append("\n[END ARTICLE]\n")

    def handle_data(self, data):
        if self.depth:
            self.parts.append(data)


def public():
    receipts = {}
    for name, suffix in [("gai", "%E5%87%B1-456694"),
                         ("gaisen", "%E5%87%B1%E6%97%8B-457786")]:
        path = C / "inputs" / f"batch-088-{name}.html"
        raw = path.read_bytes()
        parser = PublicText()
        parser.feed(raw.decode("utf-8"))
        text = "\n".join(line.strip() for line in "".join(parser.parts).splitlines()
                         if line.strip()) + "\n"
        assert CHAR in text and "\u30c7\u30b8\u30bf\u30eb\u5927\u8f9e\u6cc9" in text
        archive = S / f"batch-088-{name}.html.gz"
        archive.write_bytes(gzip.compress(raw, mtime=0))
        target = S / f"batch-088-{name}-public-text.txt"
        target.write_text(text, encoding="utf-8")
        receipts[name] = {
            "url": "https://kotobank.jp/word/" + suffix,
            "retrievedAt": datetime.now(timezone.utc).isoformat(),
            "sourcePath": str(path), "sourceSha256": sha(raw),
            "archive": archive.name, "archiveSha256": sha(archive.read_bytes()),
            "losslessGzip": gzip.decompress(archive.read_bytes()) == raw,
            "extractedText": target.name, "extractedTextSha256": sha(target.read_bytes()),
            "extractionLimits": "Coordinator article-only HTMLParser extraction; links/formatting stripped, image placeholders retained, all dictionary blocks retained. Not independent upstream retrieval or historical-glyph inspection.",
        }
        print(name + "\n" + text)
    save(S / (PREFIX + "public-source-receipts.json"), receipts)


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
    assert len(named) == len(set(named)) == 1232 and named[96] == CHAR
    unicode_rows = [line.split(";") for line in inputs["n1-UnicodeData-17.0.0.txt"]
                    .decode("utf-8").splitlines()]
    assert next(r for r in unicode_rows if r[0] == "2F0F")[5] == "<compat> 51E0"
    canonical = lambda e: ET.canonicalize(ET.tostring(e, encoding="unicode"), strip_text=True)
    character = next(e for e in kd.findall("character") if e.findtext("literal") == CHAR)
    assert metadata_record(character, {16: "\u51e0"}) == row["metadata"]
    for name, chars in [("kanjidic2.xml", CHAR),
                        ("comparison-kanjidic2.xml", "\u51e1\u51f8\u51f9\u52dd\u65cb")]:
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
    assert len(exact_ids) == 7 and len(comparison_ids) == 18
    for stem, ids in [("", exact_ids), ("comparison-", comparison_ids)]:
        selected_ids = (comparison_selection["entryIds"] if stem
                        else load(S / (PREFIX + "lexical-selection.json"))["entryIds"])
        assert ids == selected_ids
        assert (S / (PREFIX + stem + "jmdict.xml")).read_bytes() == extract(
            inputs["n1-implementation-JMdict_e.gz"],
            snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
    decision_ids = [i for group in evidence["lexicalDecisions"] for i in group["entryIds"]]
    assert len(decision_ids) == len(set(decision_ids)) == 7
    assert set(decision_ids) == set(exact_ids)
    expected = [(kind, reading) for kind, field in [("on", "onyomi"), ("kun", "kunyomi")]
                for reading in row["metadata"][field]]
    assert [(d["kind"], d["reading"]) for d in progress["readingDispositions"]] == expected
    assert progress["sourceReadingOrder"] == {k: row["metadata"][k] for k in ["onyomi", "kunyomi"]}
    selected = [d for d in progress["readingDispositions"] if d["proposedQuizSelection"]]
    assert [d["reading"] for d in selected] == ["\u30ac\u30a4"]
    assert all(d["sourceOnly"] == (not d["proposedQuizSelection"])
               and d["qualification"] and d["evidence"] for d in progress["readingDispositions"])
    projection = progress["proposedCuratedProjection"]
    assert projection["onKeys"] == offered_keys(projection["quizOnyomi"]) == ["\u304c\u3044"]
    assert projection["kunKeys"] == offered_keys(projection["quizKunyomi"]) == []
    pairs = set()
    for m in progress["proposedSupportMapping"]:
        assert not (R / m["article"]).exists()
        assert lexical_pair(families[m["entryId"]], m["word"], m["primaryReading"])
        assert m["entryId"] in exact_ids and m["allWrittenKanji"] == ["\u51f1", "\u65cb"]
        assert m["preservedWordJlpt"] is None
        assert not (R / "kanji" / "\u65cb.md").exists()
        pairs.add((CHAR, m["article"]))
    assert len(pairs) == 1 and pairs == {tuple(p) for p in progress["proposedReciprocalPairs"]}
    directions = {(f"kanji/{c}.md", article) for c, article in pairs}
    directions |= {(article, f"kanji/{c}.md") for c, article in pairs}
    assert {(d["from"], d["to"]) for d in progress["proposedDirectedLinkPlan"]} == directions
    assert progress["requiredDirectionCount"] == len(directions) == 2
    nav = load(C / "batch-088-source-navigation.json")
    assert nav["candidates"] == nav["baselinePairs"] == progress["activatedBaselinePairs"] == []
    kana_candidates = []
    for path in (R / "words").glob("*.md"):
        name = path.relative_to(R).as_posix()
        m = metadata(R, name)
        if m["reading"] == "\u304c\u3044\u305b\u3093":
            kana_candidates.append({"article": name, "metadata": m})
    assert not kana_candidates
    assert progress["membership"] == load(S / (PREFIX + "membership.json"))["membership"] == [CHAR]
    assert progress["drafted"] == progress["reviewClosed"] == progress["published"] == []
    quiz = progress["proposedQuiz"]
    assert quiz["labels"] == [metadata(R, f"kanji/{c}.md")["title"] for c in quiz["distractors"]]
    assert len(quiz["distractors"]) == len(set(quiz["distractors"])) == 3
    assert all(metadata(R, f"kanji/{c}.md")["jlpt"] == 1 for c in quiz["distractors"])
    for name in ["\u52dd", "\u6b4c"]:
        assert len(metadata(R, f"kanji/{name}.md")["distractors"]) == 3
    guards = {(r["word"], other) for r in quiz["proposedDirectExclusions"] for other in r["exclude"]}
    assert len(guards) == 4 and all((R / "words" / f"{b}.md").exists() for _, b in guards)
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json")
    checked = sum(len(v) for v in manifest.values() if isinstance(v, dict))
    assert checked == 8420 and manifest["contentVersion"] == "eb3a9413cccd4f57"
    assert not git("diff", BASE, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    baseline = load(S / "baseline-inventory.json")
    original = {Path(n).stem for n in baseline["files"] if n.startswith("kanji/")}
    current = {p.stem for p in (R / "kanji").glob("*.md")}
    accepted = set("\u5e79\u6c0f\u6271\u4e43\u51f9\u51f8\u77db\u9df9\u5f57\u6f31\u681e\u8389")
    for path in S.glob("batch-*-progress.json"):
        accepted.update(load(path).get("published", []))
    earlier = set("\u4fdd\u6848\u6d3e\u7b2c\u7b56\u7d50")
    assert len(accepted) == 114 and accepted <= current - original and accepted <= set(named)
    assert len(current) == 1110 and len(set(named) & current) == 124
    assert current & set(named) == (original & set(named)) | accepted | earlier
    assert len(set(named) - current) == 1108
    assert all(metadata(R, f"kanji/{c}.md")["jlpt"] == 2 for c in earlier)
    assert metadata(R, "kanji/\u5996.md")["jlpt"] == 1
    tree = json.loads(inputs["n1-kanjivg-tree-70a0b7ae.json"])
    assert not tree["truncated"] and tree["sha"] == snapshot["kanjivg"]["revision"]
    assert next(t for t in tree["tree"] if t["path"] == row["kanjivgInventory"]["path"]) == row["kanjivgInventory"]
    svg_path = C / "inputs" / "n1-051f1-70a0b7ae.svg"
    svg = svg_path.read_bytes()
    blob = hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest()
    assert blob == row["kanjivgInventory"]["sha"] and len(svg) == row["kanjivgInventory"]["size"]
    paths = ET.fromstring(svg).findall(".//{http://www.w3.org/2000/svg}path")
    assert len(paths) == row["metadata"]["strokes"] == 12
    assert [p.attrib["id"] for p in paths] == [f"kvg:051f1-s{i}" for i in range(1, 13)]
    converter = sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n"))
    assert converter == snapshot["kanjivg"]["converter"]["normalizedSha256"]
    stroke = {
        "schemaVersion": 1, "batch": "088", "revision": tree["sha"], "input": str(svg_path),
        "gitBlob": blob, "bytes": len(svg), "sha256": sha(svg),
        "sourceUrl": "https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/kanji/051f1.svg",
        "dictionaryStrokeCount": 12, "sourceStrokePaths": 12, "converted": False,
        "nativeDrawingAccepted": False, "converterNormalizedSha256": converter,
        "attribution": "Ulrich Apel and contributors, KanjiVG, CC BY-SA3.0; repositoryNOTICE.",
        "limits": "Pinned SVG inspected and verified; no runtime geometry or native drawing acceptance.",
    }
    save(S / (PREFIX + "stroke-evidence.json"), stroke)
    (S / (PREFIX + "kanjivg.svg")).write_bytes(svg)
    han = sorted({c for c in progress["proposedHanText"] if 0x2E80 <= ord(c) <= 0x2FDF
                  or 0x3400 <= ord(c) <= 0x9FFF or 0xF900 <= ord(c) <= 0xFAFF
                  or 0x20000 <= ord(c) <= 0x2FFFF})
    fonts = []
    for old in load(S / "batch-087-font-preparation.json")["fonts"]:
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
        "schemaVersion": 1, "batch": "088", "proposedTextInventory": progress["proposedHanText"],
        "auditedHan": han, "auditedHanCount": len(han), "fonts": fonts,
        "rareHanRangeCharacters": rare,
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
        n: len((S / (PREFIX + n)).read_text(encoding="utf-8").splitlines())
        for n in ["jmdict.xml", "kanjidic2.xml", "comparison-jmdict.xml", "comparison-kanjidic2.xml"]}
    evidence["familyCounts"] = {"allExactMemberFamilies": 7, "comparisonFamilies": 18,
                                "distinctCompleteFamilies": len(set(exact_ids + comparison_ids))}
    save(evidence_path, evidence)
    result = {
        "schemaVersion": 1, "execution": 618, "batch": "088", "baseCommit": BASE,
        "stage": progress["status"], "membership": [CHAR], "sourceRow": 97,
        "frozenInputHashesVerified": 5, "decompressedDictionaryHashesVerified": 2,
        "exactFrozenNamedMembershipAndRowVerified": True, "completeLexicalFamilies": 7,
        "completeComparisonFamilies": 18, "allExtractedEntryIdsAccountedFor": True,
        "freshExactDictionaryExtractionsVerified": 2, "rawCharacterRecordsVerified": 6,
        "proposedMetadataReadingDispositionsVerified": 4,
        "proposedOnKeys": projection["onKeys"], "proposedKunKeys": projection["kunKeys"],
        "proposedNewSupportArticles": 1, "proposedReusedSupportArticles": 0,
        "existingExactKanaReadingCandidates": kana_candidates,
        "allMappedReciprocalPairs": 1, "requiredDirectedLinks": 2,
        "activatedBaselinePairs": 0, "proposedDirectWordGuards": 4,
        "pinnedSvg": stroke, "proposedHanCount": len(han),
        "fontPreparation": PREFIX + "font-preparation.json",
        "mainFontCmapAbsences": fonts[0]["allProposedMissing"],
        "inspectedArticleHashes": {n: sha((R / n).read_bytes())
                                  for n in evidence["authorInspection"]["completeExistingArticlesRead"]},
        "runtimeManifestEqualToPublishedBase": True, "runtimeHashesUnchanged": checked,
        "contentVersion": manifest["contentVersion"], "publishedAdditions": 114,
        "remainingAcceptanceAdditions": 1114, "actuallyAbsentNamedMembers": 1108,
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
        path = L / f"{name}-618.txt"
        text = path.read_text(encoding="utf-8-sig")
        assert "Traceback" not in text and "FAILED" not in text
        if name == "source-tests":
            assert "Ran 43 tests" in text and "OK" in text
        elif name == "validate":
            assert "0 error(s)" in text
        elif name == "audit":
            assert '"runtimeHashesUnchanged": 8420' in text
        raw = path.read_bytes()
        archive = S / f"batch-088-{name}-618.txt.gz"
        archive.write_bytes(gzip.compress(raw, mtime=0))
        assert gzip.decompress(archive.read_bytes()) == raw
        checks[name] = {"path": str(path), "sha256": sha(raw),
                        "archive": archive.name, "archiveSha256": sha(archive.read_bytes()),
                        "losslessGzip": True, "provenance": "Direct redirected subprocess stdout/stderr."}
    recipe = S / (PREFIX + "source-recipe.py")
    recipe.write_bytes(Path(__file__).read_bytes())
    save(S / "execution-618.json", {
        "schemaVersion": 1, "execution": 618, "batch": "088", "baseCommit": BASE,
        "startingState": load(C / "progress.json")["execution618StartingState"],
        "sourceAudit": PREFIX + "preparation-audit.json", "sourcePacket": PREFIX + "progress.json",
        "sourceEvidence": PREFIX + "source-evidence.json",
        "recipe": {"durableControlPath": str(Path(__file__)), "archive": recipe.name,
                   "sha256": sha(recipe.read_bytes())},
        "checks": checks, "runtimeChanged": False, "runtimePublished": False,
        "focusedTestsPassed": 43,
        "focusedTestCommand": "python -X utf8 -B -m unittest test_freeze_n1_sources test_extract_n1_jmdict test_audit_n1_pilot test_audit_n1_batch; PYTHONPATH=tools",
        "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 114, "remainingAdditions": 1114,
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
    assert changed and all(p.startswith("docs/n1-sources/batch-088-") or p == "docs/n1-sources/execution-618.json"
                           for p in changed)
    before = load(L / "progress-before-618.json")
    p = load(C / "progress.json")
    allowed = {"checkpoint", "status", "stage", "batch", "nextAction", "blocker"}
    assert (p["checkpoint"], p["batch"]) == (617, "088")
    assert all(p.get(k) == v for k, v in before.items() if k not in allowed)
    issue = load(L / "issue-response-618.json")
    body = (C / "execution618-issue.txt").read_bytes().decode("utf-8")
    assert issue["user"]["login"] == "stop-cran" and issue["body"] == body
    assert issue["issue_url"].endswith("/issues/60")
    receipt = {"id": issue["id"], "url": issue["html_url"], "author": "stop-cran",
               "bodySha256": sha(body.encode("utf-8")), "verified": True}
    audit_record = load(S / (PREFIX + "preparation-audit.json"))
    state = {
        "schemaVersion": 1, "execution": 618, "checkpoint": 618, "batch": "088",
        "status": "continue", "stage": "source-prepared-not-drafted", "savedCommit": head,
        "signature": "G", "lastPublishedCommit": BASE,
        "sourcePacket": "docs/n1-sources/batch-088-progress.json",
        "sourceAudit": "docs/n1-sources/batch-088-preparation-audit.json",
        "evidence": "docs/n1-sources/execution-618.json",
        "membership": [CHAR], "sourceRow": 97, "completeDictionaryFamilies": 25,
        "lexicalFamilies": 7, "comparisonFamilies": 18, "completeRawCharacterRecords": 6,
        "metadataReadings": 4, "proposedNewSupportArticles": 1, "proposedReusedSupportArticles": 0,
        "allMappedReciprocalPairs": 1, "proposedLinkDirections": 2,
        "pinnedSvgPaths": 12, "geometryConverted": False, "proposedDirectWordGuards": 4,
        "proposedHanCount": audit_record["proposedHanCount"],
        "dedicatedWorktreesClean": True, "runtimeChanged": False, "runtimePublished": False,
        "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 114, "remainingAdditions": 1114,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "runtimeHashesUnchanged": 8420, "originalHistoricalRootKeysCompared": len(before),
        "allOriginalHistoricalValuesPreserved": True,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "issueUpdate": receipt["url"],
        "ownerIssueAuthorAndBodyVerified": True,
        "nextAction": load(S / (PREFIX + "progress.json"))["nextAction"],
    }
    p["execution618CoordinatorCheckpoint"] = state
    p["batch088SourcePreparation"] = state
    p["batch088SourcePreparationIssueReceipt"] = receipt
    p.update(checkpoint=618, status="continue", stage="batch-088-source-prepared-not-drafted",
             blocker=None, nextAction=state["nextAction"])
    save(C / "progress.json", p)
    reread = load(C / "progress.json")
    assert all(reread.get(k) == v for k, v in before.items() if k not in allowed)
    save(L / "execution-618-final-checkpoint.json", state)
    print(json.dumps(state, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["start", "packet", "comparison", "public", "audit", "record", "seal"])
    globals()[parser.parse_args().action]()

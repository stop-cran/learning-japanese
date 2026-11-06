"""Prepare bounded batch 082 evidence from approved frozen workspace sources."""
import argparse
import gzip
import hashlib
import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

CONTROL = Path(r"C:\Users\stop-\n1-kanji-workspace\control")
ROOT = CONTROL.parent / "learning-japanese"
LOG = CONTROL / "logs" / "4e07c84b-3c9f-46d3-b0a3-451abe638d48"
OUT = ROOT / "docs" / "n1-sources"
BASE = "1f317f0762513720709ab0ca215f19ff021ca596"
BATCH = "082"
CHAR = "准"
EXECUTION = 554
sys.path.insert(0, str(ROOT / "tools"))
from audit_n1_pilot import metadata
from extract_n1_jmdict import extract


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def git(*args):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=ROOT, encoding="utf-8").strip()


def frozen():
    snapshot = load(ROOT / "docs" / "n1-source-snapshot.json")
    for name, info in snapshot["inputs"].items():
        raw = (CONTROL / "inputs" / name).read_bytes()
        assert len(raw) == info["bytes"] and digest(raw) == info["sha256"], name
    raw = (CONTROL / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    xml = gzip.decompress(raw)
    kd = gzip.decompress((CONTROL / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes())
    assert digest(xml) == snapshot["jmdict"]["xmlSha256"]
    assert digest(kd) == snapshot["kanjidic2"]["xmlSha256"]
    return snapshot, raw, ET.fromstring(xml), ET.fromstring(kd)


def start():
    progress = load(CONTROL / "progress.json")
    assert progress["checkpoint"] == 553 and progress["batch"] == "081"
    assert progress["lastPublishedCommit"] == BASE and progress["remainingAdditions"] == 1120
    assert git("rev-parse", "HEAD") == git("rev-parse", "origin/main") == BASE
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    assert not list(OUT.glob("batch-082-*"))
    backup = LOG / "execution-554-start-progress.json"
    assert not backup.exists()
    save(backup, progress)
    request = (LOG / "request.txt").read_bytes()
    text = request.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["checkpoint"] == 553
    progress["execution554StartingState"] = {
        "execution": EXECUTION, "batch": BATCH, "startingHead": BASE, "freshOriginMain": BASE,
        "scope": "ONE bounded source-preparation checkpoint for pending row91准 only. No runtime draft, reviewers, Android/native, publication,083 or second runner.",
        "authorization": {
            "requestSha256": digest(request), "bytes": len(request), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded and checkpoint parsed; operative contract, final553 and complete approved issue inspected directly. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "worktrees": "Dedicated content/Android clean, signed G heads1f317f07/f9b59a2; freshly fetched origin/main1f317f07. Canonical repositories not accessed.",
        "artifactPathPreflight": {
            "guide": str(CONTROL / "authoring-artifact-path-notes.txt"),
            "durableHelper": str(Path(__file__)),
            "priorArt": "Committed batch-081-source-recipe.py and existing tools/extract_n1_jmdict.py",
            "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        },
        "startedAt": datetime.now().astimezone().isoformat(),
    }
    progress.update(batch=BATCH, stage="batch-082-source-preparation-in-progress", status="continue",
                    blocker=None, nextAction="SAME082 source preparation only for row91准; preserve full history and all later acceptance gates.")
    save(CONTROL / "progress.json", progress)
    print("Source-preparation starting state persisted with full history.")


def packet(kind, spellings):
    snapshot, raw, source, kd = frozen()
    row = next(r for r in load(OUT / "source-index.json") if r["kanji"] == CHAR)
    assert row["sourceRow"] == 91 and not (ROOT / row["article"]).exists()
    named = load(CONTROL / "inputs" / "n1-kanji-source-20261102.json")
    assert len(named) == len(set(named)) == 1232 and named[90] == CHAR
    requested = set(spellings)
    entries = [
        e for e in source.findall("entry")
        if (any(CHAR in k.text for k in e.findall("k_ele/keb")) if kind == "lexical"
            else any(k.text in requested for k in e.findall("k_ele/keb"))
            or any(r.text in requested for r in e.findall("r_ele/reb")))
    ]
    ids = [e.findtext("ent_seq") for e in entries]
    selection = {
        "schemaVersion": 1, "batch": BATCH, "entryIds": ids,
        "sourceSnapshot": "docs/n1-source-snapshot.json",
        "selectionRule": "Every complete frozen family containing 准 in any keb; all aliases/restrictions/senses retained."
        if kind == "lexical" else "Every complete frozen family matching exact requested keb/reb; homographs retained.",
        "limits": "Extraction is not author inspection, frequency evidence or independent review.",
    }
    if kind != "lexical":
        selection["requestedSpellings"] = spellings
    path = OUT / f"batch-{BATCH}-{kind}-selection.json"
    assert not path.exists()
    save(path, selection)
    suffix = "jmdict" if kind == "lexical" else f"{kind}-jmdict"
    data = extract(raw, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
    path = OUT / f"batch-{BATCH}-{suffix}.xml"
    assert not path.exists()
    path.write_bytes(data)
    print(f"{kind}: {len(ids)} complete families / {len(data.splitlines())} XML lines.")
    if kind == "lexical":
        candidates = []
        for path in sorted((ROOT / "words").glob("*.md")):
            name = path.relative_to(ROOT).as_posix()
            m = metadata(ROOT, name)
            if CHAR in m.get("kanji", []) or "准" in m["word"]:
                candidates.append({"article": name, "metadata": m})
        navigation = {
            "sourceIndexRecord": row, "candidates": candidates,
            "baselinePairs": [r for r in load(OUT / "baseline-word-candidates.json") if r["kanji"] == CHAR],
        }
        save(CONTROL / "batch-082-source-navigation.json", navigation)
        print(json.dumps(navigation, ensure_ascii=True, indent=2))


def raw_records(chars):
    snapshot, raw, source, kd = frozen()
    records = {e.findtext("literal"): e for e in kd.findall("character")}
    selected = ET.Element("kanjidic2")
    selected.append(kd.find("header"))
    for char in chars:
        selected.append(records[char])
    ET.indent(selected, space="  ")
    data = ET.tostring(selected, encoding="utf-8", xml_declaration=True) + b"\n"
    path = OUT / "batch-082-kanjidic2.xml"
    assert not path.exists()
    path.write_bytes(data)
    save(OUT / "batch-082-input-metadata.json", {
        "schemaVersion": 1, "batch": BATCH, "baseCommit": BASE,
        "sourceIndexRecord": next(r for r in load(OUT / "source-index.json") if r["kanji"] == CHAR),
        "rawCharacterPacket": path.name, "rawCharacterPacketSha256": digest(data), "characters": chars,
        "provenance": "Complete frozen KANJIDIC2 character records/header reserialized without dropping fields.",
        "dictionaryAttribution": "Copyright James William Breen and EDRDG; CC BY-SA 4.0; repository NOTICE.",
    })
    print(f"Raw characters: {len(chars)} / {len(data.splitlines())} XML lines.")


def canonical(element):
    return ET.canonicalize(ET.tostring(element, encoding="unicode"), strip_text=True)


def audit():
    from audit_n1_batch import lexical_pair
    from audit_n1_pilot import offered_keys
    from build_manifest import build_manifest, sha256
    from fontTools.ttLib import TTFont
    from freeze_n1_sources import metadata_record

    snapshot, raw, source, kd = frozen()
    data = load(OUT / "batch-082-progress.json")
    evidence = load(OUT / "batch-082-source-evidence.json")
    membership = load(OUT / "batch-082-membership.json")
    row = next(r for r in load(OUT / "source-index.json") if r["kanji"] == CHAR)
    named = load(CONTROL / "inputs" / "n1-kanji-source-20261102.json")
    assert named == load(OUT / "community-list-20261102.json")
    assert len(named) == len(set(named)) == 1232 and named[90] == CHAR and row["sourceRow"] == 91
    assert data["membership"] == membership["membership"] == [CHAR]
    assert data["baseCommit"] == membership["baseCommit"] == git("rev-parse", "HEAD") == BASE
    assert data["drafted"] == data["reviewClosed"] == data["published"] == []
    assert data["status"] == "source-prepared-not-drafted"
    assert all(not (ROOT / p).exists() for p in [row["article"], row["strokeFile"], "words/准教授.md"])
    records = {e.findtext("literal"): e for e in kd.findall("character")}
    assert metadata_record(records[CHAR], {15: "冫"}) == row["metadata"]
    assert data["sourceReadingOrder"] == {k: row["metadata"][k] for k in ["onyomi", "kunyomi"]}
    dispositions = data["readingDispositions"]
    assert [(d["kind"], d["reading"]) for d in dispositions] == [
        ("on", r) for r in row["metadata"]["onyomi"]] + [
        ("kun", r) for r in row["metadata"]["kunyomi"]]
    assert not any(d["selected"] for d in dispositions)
    projection = data["proposedCuratedProjection"]
    for kind, field, keys in [("on", "quizOnyomi", "onKeys"), ("kun", "quizKunyomi", "kunKeys")]:
        assert projection[field] == [d["reading"] for d in dispositions
                                     if d["kind"] == kind and d["proposedQuizSelection"]]
        assert projection[keys] == offered_keys(projection[field])
    assert projection["quizOnyomi"] == ["ジュン"] and projection["quizKunyomi"] == []
    families, packets = {}, []
    for kind in ["lexical", "comparison", "roles"]:
        selection = load(OUT / f"batch-082-{kind}-selection.json")
        requested = set(selection.get("requestedSpellings", []))
        ids = [
            e.findtext("ent_seq") for e in source.findall("entry")
            if (any(CHAR in k.text for k in e.findall("k_ele/keb")) if kind == "lexical"
                else any(k.text in requested for k in e.findall("k_ele/keb"))
                or any(r.text in requested for r in e.findall("r_ele/reb")))
        ]
        assert ids == selection["entryIds"]
        suffix = "jmdict" if kind == "lexical" else f"{kind}-jmdict"
        path = OUT / f"batch-082-{suffix}.xml"
        packet_bytes = path.read_bytes()
        assert packet_bytes == extract(raw, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        described = [i for d in evidence[f"{kind}Decisions"] for i in d["entryIds"]]
        assert len(described) == len(set(described)) and set(described) == set(ids)
        entries = ET.fromstring(packet_bytes).findall("entry")
        families.update((e.findtext("ent_seq"), e) for e in entries)
        packets.append({"path": path.name, "families": len(entries),
                        "lines": len(packet_bytes.splitlines()), "sha256": digest(packet_bytes)})
    assert [p["families"] for p in packets] == [22, 11, 4] and len(families) == 36
    raw_bytes = (OUT / "batch-082-kanjidic2.xml").read_bytes()
    selected = ET.fromstring(raw_bytes)
    raw_meta = load(OUT / "batch-082-input-metadata.json")
    assert raw_meta["sourceIndexRecord"] == row and raw_meta["rawCharacterPacketSha256"] == digest(raw_bytes)
    assert [e.findtext("literal") for e in selected.findall("character")] == raw_meta["characters"]
    assert canonical(selected.find("header")) == canonical(kd.find("header"))
    assert all(canonical(e) == canonical(records[e.findtext("literal")]) for e in selected.findall("character"))
    assert lexical_pair(families["2178020"], "准教授", "じゅんきょうじゅ")
    assert lexical_pair(families["2178020"], "準教授", "じゅんきょうじゅ")
    assert lexical_pair(families["1344550"], "助教授", "じょきょうじゅ")
    assert not lexical_pair(families["1344550"], "助教授", "じゅんきょうじゅ")
    assert families["2178020"].findtext("sense/pos") == "noun (common) (futsuumeishi)"
    assert families["1885670"].findtext("sense/s_inf") == "now deprecated"
    for entry_id, word in [("1341500", "准える"), ("1341510", "准じる"),
                           ("1341520", "准ずる"), ("1341550", "准拠"),
                           ("1599860", "に准じて"), ("2019210", "准州")]:
        spelling = next(e for e in families[entry_id].findall("k_ele") if e.findtext("keb") == word)
        assert spelling.findtext("ke_inf") == "rarely used kanji form"
    word_meta = [metadata(ROOT, f"words/{p.name}") for p in (ROOT / "words").glob("*.md")]
    declared = [f"words/{m['word']}.md" for m in word_meta if CHAR in m.get("kanji", [])]
    assert declared == data["currentDeclaredWordPairs"] == []
    assert not [r for r in load(OUT / "baseline-word-candidates.json") if r["kanji"] == CHAR]
    assert not [m for m in word_meta if m["reading"] == "じゅんきょうじゅ"]
    assert metadata(ROOT, "words/助教授.md")["jlpt"] == 2
    mapping = data["proposedSupportMapping"]
    assert len(mapping) == 1 and mapping[0]["allWrittenKanji"] == ["准", "教", "授"]
    assert not (ROOT / "kanji" / "授.md").exists()
    expected_pairs = {(c, m["article"]) for m in mapping for c in m["allWrittenKanji"]
                      if c == CHAR or (ROOT / "kanji" / f"{c}.md").exists()}
    assert expected_pairs == {tuple(p) for p in data["proposedReciprocalPairs"]} == {
        (CHAR, "words/准教授.md"), ("教", "words/准教授.md")}
    assert {(p["from"], p["to"]) for p in data["proposedDirectedLinkPlan"]} == {
        (f"kanji/{c}.md", w) for c, w in expected_pairs} | {
        (w, f"kanji/{c}.md") for c, w in expected_pairs}
    assert [r["article"] for r in data["proposedChangedReusedPassages"]] == ["kanji/教.md", "words/助教授.md"]
    all_meta = [metadata(ROOT, f"kanji/{p.name}") for p in (ROOT / "kanji").glob("*.md")]
    quiz = data["proposedKanjiQuizAudit"]
    assert quiz["title"] not in {m["title"] for m in all_meta}
    assert len(quiz["distractors"]) == len({c["kanji"] for c in quiz["distractors"]}) == 3
    for choice in quiz["distractors"]:
        assert metadata(ROOT, f"kanji/{choice['kanji']}.md")["title"] == choice["title"]
    for char in ["準", "規", "允", "許"]:
        assert len(metadata(ROOT, f"kanji/{char}.md")["distractors"]) == 3
    assert data["proposedWordQuizAudit"]["directExclusions"] == ["助教授"]
    assert data["proposedWordQuizAudit"]["newTitle"] not in {m["title"] for m in word_meta}
    confusables = (ROOT / "docs" / "confusable-words.md").read_text(encoding="utf-8")
    assert "准教授" not in confusables and "じゅんきょうじゅ" not in confusables
    baseline = load(OUT / "baseline-inventory.json")
    exceptions = {"words/虎.md": ["酔っ払い"], "words/猿.md": ["馬鹿"],
                  "words/丘.md": ["坂", "山"], "words/冗談.md": ["ユーモア"]}
    counts = {"kanji": 0, "words": 0, "strokes": 0}
    for name, item in baseline["files"].items():
        kind = name.split("/")[0]
        if kind in ["kanji", "words"]:
            expected = dict(item["metadata"])
            if name in exceptions:
                expected["quiz_exclusions"] = exceptions[name]
            if name == "kanji/山.md":
                expected["distractors"] = ["川", "出", "木"]
            assert metadata(ROOT, name) == expected, name
            counts[kind] += 1
        elif kind == "strokes":
            assert digest((ROOT / name).read_bytes()) == item["sha256"], name
            counts[kind] += 1
    assert counts == {"kanji": 985, "words": 4942, "strokes": 985}
    original_kanji = {Path(n).stem for n in baseline["files"] if n.startswith("kanji/")}
    current_kanji = {p.stem for p in (ROOT / "kanji").glob("*.md")}
    additions = current_kanji - original_kanji
    accepted = set("幹氏扱乃凹凸矛鷹彗漱栞莉")
    for path in OUT.glob("batch-*-progress.json"):
        accepted.update(load(path).get("published", []))
    assert additions == accepted and len(additions) == 108 and additions <= set(named)
    assert metadata(ROOT, "kanji/妖.md")["jlpt"] == 1
    protected = ["kanji", "words", "articles", "strokes", "tools", "manifest.json",
                 "docs/n1-source-snapshot.json", "docs/n1-sources/source-index.json",
                 "docs/n1-sources/baseline-inventory.json", "docs/n1-sources/baseline-word-candidates.json"]
    assert not git("diff", BASE, "--", *protected)
    manifest = load(ROOT / "manifest.json")
    assert manifest == build_manifest(ROOT)
    assert (ROOT / "manifest.json").read_bytes() == subprocess.check_output(
        ["git", "--no-pager", "show", f"{BASE}:manifest.json"], cwd=ROOT)
    checked = 0
    for section, entries in manifest.items():
        if isinstance(entries, dict):
            for name, expected in entries.items():
                actual = digest((ROOT / name).read_bytes()) if section in {
                    "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(ROOT / name)
                assert actual == expected, name
                checked += 1
    assert checked == 8369 and manifest["contentVersion"] == "f1dd5d8b9d2ff535"
    tree = load(CONTROL / "inputs" / "n1-kanjivg-tree-70a0b7ae.json")
    assert not tree["truncated"] and tree["sha"] == snapshot["kanjivg"]["revision"]
    assert next(t for t in tree["tree"] if t["path"] == row["kanjivgInventory"]["path"]) == row["kanjivgInventory"]
    svg_path = CONTROL / "inputs" / "n1-051c6-70a0b7ae.svg"
    svg = svg_path.read_bytes()
    blob = hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest()
    assert blob == row["kanjivgInventory"]["sha"] and len(svg) == row["kanjivgInventory"]["size"]
    paths = ET.fromstring(svg).findall(".//{http://www.w3.org/2000/svg}path")
    assert len(paths) == row["metadata"]["strokes"] == 10
    assert [p.attrib["id"] for p in paths] == [f"kvg:051c6-s{i}" for i in range(1, 11)]
    converter = digest((ROOT / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n"))
    assert converter == snapshot["kanjivg"]["converter"]["normalizedSha256"]
    unicode_rows = (CONTROL / "inputs" / "n1-UnicodeData-17.0.0.txt").read_text(encoding="utf-8").splitlines()
    assert next(s for s in unicode_rows if s.startswith("2F0E;")).split(";")[5] == "<compat> 51AB"
    stroke = {
        "revision": tree["sha"], "input": str(svg_path), "gitBlob": blob,
        "sourceUrl": "https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/kanji/051c6.svg",
        "bytes": len(svg), "sha256": digest(svg), "dictionaryStrokeCount": 10, "sourceStrokePaths": 10,
        "converted": False, "nativeDrawingAccepted": False, "converterNormalizedSha256": converter,
        "attribution": "Ulrich Apel and contributors, KanjiVG, CC BY-SA 3.0; repository NOTICE.",
        "limits": "Whole pinned SVG inspected. Labels, including水original/phon, are source annotations, not independently established etymology or a replacement for classical冫15.",
    }
    save(OUT / "batch-082-stroke-evidence.json", stroke)
    han = sorted({c for c in data["proposedHanText"] if 0x2E80 <= ord(c) <= 0x2FDF
                  or 0x3400 <= ord(c) <= 0x9FFF or 0xF900 <= ord(c) <= 0xFAFF
                  or 0x20000 <= ord(c) <= 0x2FFFF})
    fonts = []
    for old in load(OUT / "batch-081-font-preparation.json")["fonts"]:
        path = Path(old["path"])
        assert digest(path.read_bytes()) == old["sha256"]
        with TTFont(path) as font:
            cmap = font.getBestCmap()
        fonts.append({"path": str(path), "sha256": old["sha256"],
                      "keyGlyphPresence": {c: ord(c) in cmap for c in han},
                      "allProposedMissing": [c for c in han if ord(c) not in cmap]})
    rare = [c for c in han if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x4DBF
            or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF]
    font_record = {
        "schemaVersion": 1, "batch": BATCH, "proposedTextInventory": data["proposedHanText"],
        "auditedHanCount": len(han), "auditedHan": han, "fonts": fonts, "rareHanRangeCharacters": rare,
        "mechanism": "Actual unchanged RareHan.kt/RareHanTest.kt read; all three actual bundled cmaps inspected.",
        "limits": "Proposed terms only, not a nonexistent draft. Reinventory actual runtime Han later. Cmap presence/absence is not native/phone legibility or fallback-face identification.",
    }
    save(OUT / "batch-082-font-preparation.json", font_record)
    public_bytes = []
    for name in ["character", "academic-rank"]:
        path = CONTROL / "inputs" / f"batch-082-{name}.html"
        public_bytes.append({
            "path": str(path), "bytes": path.stat().st_size, "sha256": digest(path.read_bytes()),
            "limits": "Downloaded whole page bytes; semantic inspection refers to actual web-fetch returns in source evidence.",
        })
    current_counts = {
        "kanji": len(all_meta), "words": len(word_meta), "n1Labelled": sum(m.get("jlpt") == 1 for m in all_meta),
        "namedSourceMembersPresent": len(current_kanji & set(named)),
    }
    assert current_counts == {"kanji": 1093, "words": 5049, "n1Labelled": 113, "namedSourceMembersPresent": 112}
    result = {
        "schemaVersion": 1, "execution": EXECUTION, "batch": BATCH, "stage": "source-prepared-not-drafted",
        "baseCommit": BASE, "membership": [CHAR], "sourceRow": 91,
        "frozenInputHashesVerified": 5, "decompressedDictionaryHashesVerified": 2,
        "exactFrozenNamedMembershipAndRowVerified": True, "packets": packets,
        "freshExactDictionaryExtractions": 3, "dictionaryFamilyOccurrences": 37,
        "distinctCompleteFamilies": 36, "allExtractedEntryIdsAccountedFor": True,
        "rawCharacterPacket": {"characters": 7, "sha256": digest(raw_bytes), "allRecordsAndHeaderVerified": True},
        "authorInspection": data["authorInspection"],
        "inspectedArticleHashes": {n: digest((ROOT / n).read_bytes())
                                  for n in data["authorInspection"]["completeExistingArticlesRead"]},
        "publicSourceByteReceipts": public_bytes, "pinnedSvg": stroke, "fontPreparation": font_record,
        "allMetadataReadingDispositionsVerified": 1, "proposedOnKeys": ["じゅん"], "proposedKunKeys": [],
        "originalBaselineMetadataAndStrokesPreserved": counts, "baselineMetadataExceptions": exceptions,
        "baselineKanjiDistractorException": {"kanji/山.md": ["川", "出", "木"]},
        "runtimeManifestEqualToPublishedBase": True, "manifestBytesUnchanged": True,
        "allRuntimePayloadHashesVerified": checked, "contentVersion": manifest["contentVersion"],
        "exactPublishedAdditionMembershipVerified": len(additions), "currentCounts": current_counts,
        "allMappedCurrentlyCardableReciprocalPairsEnumerated": 2, "requiredDirectedLinks": 4,
        "activatedBaselineDeclaredPairs": 0, "proposedNewWordArticles": 1,
        "proposedChangedReusedArticles": ["kanji/教.md", "words/助教授.md"], "runtimeChanges": 0,
        "reviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 108, "remainingAdditions": 1120,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [], "limits": data["limits"],
    }
    save(OUT / "batch-082-preparation-audit.json", result)
    print(json.dumps({"families": 36, "occurrences": 37, "runtimeHashesUnchanged": checked,
                      "currentCounts": current_counts, "proposedHan": len(han),
                      "cmapAbsences": [f["allProposedMissing"] for f in fonts]}, ensure_ascii=True, indent=2))


def record():
    receipts = {}
    for name in ["source-tests", "validate", "manifest", "budget", "audit"]:
        path = LOG / f"{name}-554.txt"
        text = path.read_text(encoding="utf-8-sig")
        if name == "source-tests":
            assert "Ran 9 tests" in text and "OK" in text and "FAILED" not in text and "skipped" not in text
        elif name == "validate":
            assert "0 error(s)" in text
        elif name == "manifest":
            assert "8369" in text and "f1dd5d8b9d2ff535" in text
        elif name == "budget":
            assert "ERROR" not in text and "8391" in text
        else:
            assert '"runtimeHashesUnchanged": 8369' in text
        receipts[name] = {"path": str(path), "sha256": digest(path.read_bytes())}
    audit_data = load(OUT / "batch-082-preparation-audit.json")
    recipe = OUT / "batch-082-source-recipe.py"
    recipe.write_bytes(Path(__file__).read_bytes())
    save(OUT / "execution-554.json", {
        "schemaVersion": 1, "execution": EXECUTION, "batch": BATCH, "baseCommit": BASE,
        "stage": "source-prepared-not-drafted",
        "startingState": load(CONTROL / "progress.json")["execution554StartingState"],
        "sourceAudit": "batch-082-preparation-audit.json", "sourcePacket": "batch-082-progress.json",
        "sourceEvidence": "batch-082-source-evidence.json",
        "preparationRecipe": {
            "durableControlPath": str(Path(__file__)), "archive": recipe.name, "sha256": digest(recipe.read_bytes()),
            "limits": "Later coordinators use committed packets/approved workspace inputs, not optional historical session recipes.",
        },
        "checks": receipts, "runtimeChanges": 0, "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "runtimePublished": False, "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 108, "remainingAdditions": 1120,
        "nextAction": load(OUT / "batch-082-progress.json")["nextAction"], "limits": audit_data["limits"],
    })
    print("Source recipe and execution evidence archived for normal signed LOCAL source checkpoint.")


def seal():
    original = load(LOG / "execution-554-start-progress.json")
    progress = load(CONTROL / "progress.json")
    assert progress["checkpoint"] == 553 and progress["batch"] == BATCH
    assert not git("status", "--porcelain") and git("log", "-1", "--format=%G?") == "G"
    head = git("rev-parse", "HEAD")
    assert head != BASE and git("rev-parse", "origin/main") == BASE
    assert not git("diff", BASE, "HEAD", "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    android = CONTROL.parent / "kanji-cards-android"
    assert not subprocess.check_output(["git", "status", "--porcelain"], cwd=android).strip()
    assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=android).decode().strip() == (
        "f9b59a2bc5a203c6b4de26be50021a4c720dc22c")
    allowed = {"checkpoint", "status", "stage", "batch", "nextAction", "blocker"}
    assert all(progress.get(k) == v for k, v in original.items() if k not in allowed)
    data = load(OUT / "batch-082-progress.json")
    checkpoint = {
        "schemaVersion": 1, "execution": EXECUTION, "checkpoint": EXECUTION, "batch": BATCH,
        "status": "continue", "stage": "source-prepared-not-drafted", "savedCommit": head, "signature": "G",
        "sourcePacket": "docs/n1-sources/batch-082-progress.json",
        "sourceAudit": "docs/n1-sources/batch-082-preparation-audit.json",
        "evidence": "docs/n1-sources/execution-554.json", "dedicatedWorktreesClean": True,
        "sourceRow": 91, "membership": [CHAR], "completeDictionaryFamilies": 36,
        "dictionaryFamilyOccurrences": 37, "completeRawCharacterRecords": 7,
        "completeExistingArticlesRead": 17, "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "runtimeChanged": False, "runtimePublished": False, "independentReviewersLaunched": 0,
        "freshAndroidOrNativeClaimed": False, "publishedAdditions": 108, "remainingAdditions": 1120,
        "lastPublishedCommit": BASE, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
        "proposedOnKeys": ["じゅん"], "proposedKunKeys": [], "allMappedPairs": 2, "directedLinks": 4,
        "proposedSupport": "Necessary new准教授じゅんきょうじゅ; no inferred vocabulary level; metadata includes准教授,授 absent.",
        "proposedChanges": "Only教 Common words reciprocal bullet and助教授 first successor-name navigation link. Original metadata/levels/primary readings/exclusions preserved.",
        "proposedQuizExclusion": ["助教授"], "pinnedSvgPaths": 10, "geometryConverted": False,
        "proposedHan": load(OUT / "batch-082-font-preparation.json")["auditedHanCount"],
        "fontAcceptance": "Proposed cmaps audited; actual draft/native/phone rendering pending.",
        "runtimeHashesUnchanged": 8369, "contentVersion": "f1dd5d8b9d2ff535", "focusedTestsPassed": 9,
        "originalHistoricalRootKeysCompared": len(original), "allOriginalHistoricalValuesPreserved": True,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "nextAction": data["nextAction"],
    }
    progress["execution554CoordinatorCheckpoint"] = checkpoint
    progress["batch082SourcePreparation"] = checkpoint
    progress.update(checkpoint=EXECUTION, stage="batch-082-source-prepared-not-drafted",
                    status="continue", blocker=None, nextAction=data["nextAction"])
    save(CONTROL / "progress.json", progress)
    reread = load(CONTROL / "progress.json")
    assert all(reread.get(k) == v for k, v in original.items() if k not in allowed)
    save(LOG / "execution-554-final-checkpoint.json", checkpoint)
    print(json.dumps(checkpoint, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["start", "lexical", "comparison", "roles", "raw", "audit", "record", "seal"])
    parser.add_argument("terms", nargs="*")
    args = parser.parse_args()
    if args.action == "start":
        start()
    elif args.action == "audit":
        audit()
    elif args.action == "record":
        record()
    elif args.action == "seal":
        seal()
    elif args.action == "raw":
        raw_records(args.terms)
    else:
        packet(args.action, args.terms)

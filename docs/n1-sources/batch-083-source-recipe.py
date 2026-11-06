"""Prepare batch 083 from frozen approved workspace inputs; no runtime edits."""
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
OUT = ROOT / "docs" / "n1-sources"
LOG = CONTROL / "logs" / "feb72d88-c163-479f-9838-8f25485f6881"
BASE = "21a5cb1328aadd437139a6b850f07298a2e2985d"
BATCH = "083"
CHAR = "\u51cc"
EXECUTION = 568
sys.path.insert(0, str(ROOT / "tools"))
from audit_n1_pilot import metadata
from extract_n1_jmdict import extract


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def git(*args, root=ROOT):
    return subprocess.check_output(
        ["git", "--no-pager", *args], cwd=root, encoding="utf-8"
    ).strip()


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
    p = load(CONTROL / "progress.json")
    assert p["checkpoint"] == 567 and p["batch"] == "082"
    assert p["lastPublishedCommit"] == BASE and p["remainingAdditions"] == 1119
    assert git("rev-parse", "HEAD") == git("rev-parse", "origin/main") == BASE
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    android = CONTROL.parent / "kanji-cards-android"
    assert git("rev-parse", "HEAD", root=android) == "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
    assert git("log", "-1", "--format=%G?", root=android) == "G"
    assert not git("status", "--porcelain", root=android)
    assert not list(OUT.glob("batch-083-*"))
    backup = LOG / "execution-568-start-progress.json"
    assert not backup.exists()
    save(backup, p)
    request = (LOG / "request.txt").read_bytes()
    text = request.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1
    )[1])
    assert checkpoint["checkpoint"] == 567
    p["execution568StartingState"] = {
        "execution": EXECUTION, "batch": BATCH, "startingHead": BASE, "freshOriginMain": BASE,
        "scope": "ONE bounded batch083 source-preparation checkpoint only; no runtime draft, reviewer, Android/native, publication,084 or second runner.",
        "authorization": {
            "requestSha256": digest(request), "bytes": len(request), "characters": len(text),
            "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded and embedded checkpoint decoded; operative contract, final567 and complete approved issue inspected directly. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "worktrees": "Dedicated content/Android clean, signed G heads21a5cb13/1c1b7bf4; freshly fetched main21a5cb13. Android is the qualified test-only loader revision, not latest app main; production f9b59a2 preserved. Canonical repositories not accessed.",
        "artifactPathPreflight": {
            "guide": str(CONTROL / "authoring-artifact-path-notes.txt"),
            "durableHelper": str(Path(__file__)),
            "priorArt": "Committed batch-082-source-recipe.py and tools/extract_n1_jmdict.py.",
            "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        },
        "startedAt": datetime.now().astimezone().isoformat(),
    }
    p.update(batch=BATCH, stage="batch-083-source-preparation-in-progress", status="continue",
             blocker=None, nextAction="SAME083 bounded source preparation for frozen row92 only; preserve full history and every later acceptance gate.")
    save(CONTROL / "progress.json", p)
    print("Full-history starting state persisted.")


def packet(kind, spellings):
    snapshot, raw, source, kd = frozen()
    row = next(r for r in load(OUT / "source-index.json") if r["kanji"] == CHAR)
    named = load(CONTROL / "inputs" / "n1-kanji-source-20261102.json")
    assert row["sourceRow"] == 92 and named[91] == CHAR
    assert not (ROOT / row["article"]).exists()
    requested = set(spellings)
    ids = [
        e.findtext("ent_seq") for e in source.findall("entry")
        if (any(CHAR in k.text for k in e.findall("k_ele/keb")) if kind == "lexical"
            else any(k.text in requested for k in e.findall("k_ele/keb"))
            or any(r.text in requested for r in e.findall("r_ele/reb")))
    ]
    selection = {
        "schemaVersion": 1, "batch": BATCH, "entryIds": ids,
        "sourceSnapshot": "docs/n1-source-snapshot.json",
        "selectionRule": "Every complete frozen family containing the batch character in any keb; aliases/restrictions/senses retained."
        if kind == "lexical" else "Every complete frozen family matching an exact requested keb/reb; homographs retained.",
        "limits": "Extraction is not inspection, frequency evidence or independent review.",
    }
    if kind != "lexical":
        selection["requestedSpellings"] = spellings
    path = OUT / f"batch-{BATCH}-{kind}-selection.json"
    assert not path.exists()
    save(path, selection)
    suffix = "jmdict" if kind == "lexical" else f"{kind}-jmdict"
    path = OUT / f"batch-{BATCH}-{suffix}.xml"
    assert not path.exists()
    result = extract(raw, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
    path.write_bytes(result)
    print(f"{kind}: {len(ids)} complete families / {len(result.splitlines())} XML lines.")
    if kind == "lexical":
        candidates = []
        for path in sorted((ROOT / "words").glob("*.md")):
            name = path.relative_to(ROOT).as_posix()
            m = metadata(ROOT, name)
            if CHAR in m.get("kanji", []) or CHAR in m["word"]:
                candidates.append({"article": name, "metadata": m})
        navigation = {
            "sourceIndexRecord": row, "candidates": candidates,
            "baselinePairs": [r for r in load(OUT / "baseline-word-candidates.json") if r["kanji"] == CHAR],
        }
        save(CONTROL / "batch-083-source-navigation.json", navigation)
        print(json.dumps(navigation, ensure_ascii=True, indent=2))


def records(chars, suffix="kanjidic2"):
    snapshot, raw, source, kd = frozen()
    full = {e.findtext("literal"): e for e in kd.findall("character")}
    selected = ET.Element("kanjidic2")
    selected.append(kd.find("header"))
    for char in chars:
        selected.append(full[char])
    ET.indent(selected, space="  ")
    result = ET.tostring(selected, encoding="utf-8", xml_declaration=True) + b"\n"
    path = OUT / f"batch-{BATCH}-{suffix}.xml"
    assert not path.exists()
    path.write_bytes(result)
    metadata_suffix = "input-metadata" if suffix == "kanjidic2" else f"{suffix}-metadata"
    save(OUT / f"batch-{BATCH}-{metadata_suffix}.json", {
        "schemaVersion": 1, "batch": BATCH, "baseCommit": BASE,
        "sourceIndexRecord": next(r for r in load(OUT / "source-index.json") if r["kanji"] == CHAR),
        "rawCharacterPacket": path.name, "rawCharacterPacketSha256": digest(result),
        "characters": chars,
        "provenance": "Complete frozen KANJIDIC2 records/header reserialized without dropping fields.",
        "dictionaryAttribution": "Copyright James William Breen and EDRDG; CC BY-SA 4.0; repository NOTICE.",
    })
    print(f"Raw characters: {len(chars)} / {len(result.splitlines())} XML lines.")


def canonical(element):
    return ET.canonicalize(ET.tostring(element, encoding="unicode"), strip_text=True)


def audit():
    from audit_n1_batch import lexical_pair
    from audit_n1_pilot import offered_keys
    from build_manifest import build_manifest, sha256
    from fontTools.ttLib import TTFont
    from freeze_n1_sources import metadata_record

    snapshot, raw, source, kd = frozen()
    data = load(OUT / "batch-083-progress.json")
    evidence = load(OUT / "batch-083-source-evidence.json")
    membership = load(OUT / "batch-083-membership.json")
    named = load(CONTROL / "inputs" / "n1-kanji-source-20261102.json")
    row = next(r for r in load(OUT / "source-index.json") if r["kanji"] == CHAR)
    assert named == load(OUT / "community-list-20261102.json")
    assert len(named) == len(set(named)) == 1232 and named[91] == CHAR and row["sourceRow"] == 92
    assert data["membership"] == membership["membership"] == [CHAR]
    assert data["baseCommit"] == membership["baseCommit"] == BASE
    assert data["status"] == "source-prepared-not-drafted"
    assert data["drafted"] == data["reviewClosed"] == data["published"] == []
    assert all(not (ROOT / p).exists() for p in [
        row["article"], row["strokeFile"], "words/\u51cc\u3050.md", "words/\u51cc\u99d5.md"])
    kd_records = {e.findtext("literal"): e for e in kd.findall("character")}
    assert metadata_record(kd_records[CHAR], {15: "\u51ab"}) == row["metadata"]
    assert data["sourceReadingOrder"] == {k: row["metadata"][k] for k in ["onyomi", "kunyomi"]}
    dispositions = data["readingDispositions"]
    assert [(d["kind"], d["reading"]) for d in dispositions] == [
        ("on", r) for r in row["metadata"]["onyomi"]] + [
        ("kun", r) for r in row["metadata"]["kunyomi"]]
    assert not any(d["selected"] for d in dispositions)
    for kind, field, keys in [("on", "quizOnyomi", "onKeys"), ("kun", "quizKunyomi", "kunKeys")]:
        projection = data["proposedCuratedProjection"]
        assert projection[field] == [d["reading"] for d in dispositions
                                     if d["kind"] == kind and d["proposedQuizSelection"]]
        assert projection[keys] == offered_keys(projection[field])
    families, packets = {}, []
    for kind in ["lexical", "comparison", "extra"]:
        selection = load(OUT / f"batch-{BATCH}-{kind}-selection.json")
        requested = set(selection.get("requestedSpellings", []))
        ids = [
            e.findtext("ent_seq") for e in source.findall("entry")
            if (any(CHAR in k.text for k in e.findall("k_ele/keb")) if kind == "lexical"
                else any(k.text in requested for k in e.findall("k_ele/keb"))
                or any(r.text in requested for r in e.findall("r_ele/reb")))
        ]
        assert ids == selection["entryIds"]
        suffix = "jmdict" if kind == "lexical" else f"{kind}-jmdict"
        path = OUT / f"batch-{BATCH}-{suffix}.xml"
        packet_bytes = path.read_bytes()
        assert packet_bytes == extract(raw, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        described = [i for d in evidence[f"{kind}Decisions"] for i in d["entryIds"]]
        assert len(described) == len(set(described)) and set(described) == set(ids)
        entries = ET.fromstring(packet_bytes).findall("entry")
        families.update((e.findtext("ent_seq"), e) for e in entries)
        packets.append({"path": path.name, "families": len(entries),
                        "lines": len(packet_bytes.splitlines()), "sha256": digest(packet_bytes)})
    assert [p["families"] for p in packets] == [25, 16, 3] and len(families) == 42
    raw_packets = []
    for suffix in ["kanjidic2", "support-kanjidic2"]:
        path = OUT / f"batch-{BATCH}-{suffix}.xml"
        selected = ET.fromstring(path.read_bytes())
        meta_suffix = "input-metadata" if suffix == "kanjidic2" else f"{suffix}-metadata"
        meta = load(OUT / f"batch-{BATCH}-{meta_suffix}.json")
        assert digest(path.read_bytes()) == meta["rawCharacterPacketSha256"]
        assert [e.findtext("literal") for e in selected.findall("character")] == meta["characters"]
        assert canonical(selected.find("header")) == canonical(kd.find("header"))
        assert all(canonical(e) == canonical(kd_records[e.findtext("literal")])
                   for e in selected.findall("character"))
        raw_packets.append({"path": path.name, "characters": meta["characters"],
                            "sha256": digest(path.read_bytes()), "allRecordsAndHeaderVerified": True})
    assert sum(len(p["characters"]) for p in raw_packets) == 8
    for mapping in data["proposedSupportMapping"]:
        assert lexical_pair(families[mapping["entryId"]], mapping["word"], mapping["primaryReading"])
        assert mapping["preservedWordJlpt"] is None
    assert lexical_pair(families["1606270"], "\u9675\u99d5", "\u308a\u3087\u3046\u304c")
    alternate = families["1606270"].findall("k_ele")[1]
    assert alternate.findtext("ke_inf") == "rarely used kanji form"
    assert families["2856224"].findtext("sense/s_inf") == "non-standard variant of \u8010\u3048\u5fcd\u3076"
    assert not lexical_pair(families["1554200"], "\u51cc\u3050", "\u3057\u306e\u3076")
    words = [metadata(ROOT, f"words/{p.name}") for p in (ROOT / "words").glob("*.md")]
    assert not [m for m in words if CHAR in m.get("kanji", [])]
    assert not [m for m in words if m["reading"] in ["\u3057\u306e\u3050", "\u308a\u3087\u3046\u304c"]]
    assert not [r for r in load(OUT / "baseline-word-candidates.json") if r["kanji"] == CHAR]
    assert not (ROOT / "kanji" / "\u99d5.md").exists()
    pairs = {(c, m["article"]) for m in data["proposedSupportMapping"] for c in m["allWrittenKanji"]
             if c == CHAR or (ROOT / "kanji" / f"{c}.md").exists()}
    assert pairs == {tuple(p) for p in data["proposedReciprocalPairs"]} and len(pairs) == 2
    assert {(p["from"], p["to"]) for p in data["proposedDirectedLinkPlan"]} == {
        (f"kanji/{c}.md", w) for c, w in pairs} | {(w, f"kanji/{c}.md") for c, w in pairs}
    assert data["proposedChangedReusedPassages"] == []
    kanji_meta = [metadata(ROOT, f"kanji/{p.name}") for p in (ROOT / "kanji").glob("*.md")]
    quiz = data["proposedKanjiQuizAudit"]
    assert quiz["title"] not in {m["title"] for m in kanji_meta}
    assert len(quiz["distractors"]) == len({c["kanji"] for c in quiz["distractors"]}) == 3
    for choice in quiz["distractors"]:
        assert metadata(ROOT, f"kanji/{choice['kanji']}.md")["title"] == choice["title"]
        assert choice["kanji"] != CHAR
    titles = data["proposedWordQuizAudit"]["newTitles"]
    assert not set(titles.values()) & {m["title"] for m in words}
    allowed = {m["word"] for m in words} | titles.keys()
    for word, exclusions in data["proposedWordQuizAudit"]["directExclusions"].items():
        assert len(exclusions) == len(set(exclusions)) and word not in exclusions
        assert set(exclusions) <= allowed
    baseline = load(OUT / "baseline-inventory.json")
    exceptions = {"words/\u864e.md": ["\u9154\u3063\u6255\u3044"],
                  "words/\u733f.md": ["\u99ac\u9e7f"],
                  "words/\u4e18.md": ["\u5742", "\u5c71"],
                  "words/\u5197\u8ac7.md": ["\u30e6\u30fc\u30e2\u30a2"]}
    counts = {"kanji": 0, "words": 0, "strokes": 0}
    for name, item in baseline["files"].items():
        kind = name.split("/")[0]
        if kind in ["kanji", "words"]:
            expected = dict(item["metadata"])
            if name in exceptions:
                expected["quiz_exclusions"] = exceptions[name]
            if name == "kanji/\u5c71.md":
                expected["distractors"] = ["\u5ddd", "\u51fa", "\u6728"]
            assert metadata(ROOT, name) == expected, name
            counts[kind] += 1
        elif kind == "strokes":
            assert digest((ROOT / name).read_bytes()) == item["sha256"], name
            counts[kind] += 1
    assert counts == {"kanji": 985, "words": 4942, "strokes": 985}
    original = {Path(n).stem for n in baseline["files"] if n.startswith("kanji/")}
    current = {p.stem for p in (ROOT / "kanji").glob("*.md")}
    additions = current - original
    accepted = set("\u5e79\u6c0f\u6271\u4e43\u51f9\u51f8\u77db\u9df9\u5f57\u6f31\u681e\u8389")
    for path in OUT.glob("batch-*-progress.json"):
        accepted.update(load(path).get("published", []))
    assert additions == accepted and len(additions) == 109 and additions <= set(named)
    assert metadata(ROOT, "kanji/\u5996.md")["jlpt"] == 1
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
    assert checked == 8372 and manifest["contentVersion"] == "d82e7fefe3898a70"
    tree = load(CONTROL / "inputs" / "n1-kanjivg-tree-70a0b7ae.json")
    assert not tree["truncated"] and tree["sha"] == snapshot["kanjivg"]["revision"]
    assert next(t for t in tree["tree"] if t["path"] == row["kanjivgInventory"]["path"]) == row["kanjivgInventory"]
    svg_path = CONTROL / "inputs" / "n1-051cc-70a0b7ae.svg"
    svg = svg_path.read_bytes()
    blob = hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest()
    assert blob == row["kanjivgInventory"]["sha"] and len(svg) == row["kanjivgInventory"]["size"]
    paths = ET.fromstring(svg).findall(".//{http://www.w3.org/2000/svg}path")
    assert len(paths) == row["metadata"]["strokes"] == 10
    assert [p.attrib["id"] for p in paths] == [f"kvg:051cc-s{i}" for i in range(1, 11)]
    converter = digest((ROOT / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n"))
    assert converter == snapshot["kanjivg"]["converter"]["normalizedSha256"]
    unicode = (CONTROL / "inputs" / "n1-UnicodeData-17.0.0.txt").read_text(encoding="utf-8").splitlines()
    assert next(s for s in unicode if s.startswith("2F0E;")).split(";")[5] == "<compat> 51AB"
    stroke = {
        "revision": tree["sha"], "input": str(svg_path), "gitBlob": blob,
        "sourceUrl": "https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/kanji/051cc.svg",
        "bytes": len(svg), "sha256": digest(svg), "dictionaryStrokeCount": 10, "sourceStrokePaths": 10,
        "converted": False, "nativeDrawingAccepted": False, "converterNormalizedSha256": converter,
        "attribution": "Ulrich Apel and contributors, KanjiVG, CC BY-SA 3.0; repository NOTICE.",
        "limits": "Pinned SVG fully inspected. Component annotations are not an independent etymological certification.",
    }
    save(OUT / "batch-083-stroke-evidence.json", stroke)
    han = sorted({c for c in data["proposedHanText"] if 0x2E80 <= ord(c) <= 0x2FDF
                  or 0x3400 <= ord(c) <= 0x9FFF or 0xF900 <= ord(c) <= 0xFAFF
                  or 0x20000 <= ord(c) <= 0x2FFFF})
    fonts = []
    for old in load(OUT / "batch-082-font-preparation.json")["fonts"]:
        path = Path(old["path"])
        assert digest(path.read_bytes()) == old["sha256"]
        with TTFont(path) as font:
            cmap = font.getBestCmap()
        fonts.append({"path": str(path), "sha256": old["sha256"],
                      "keyGlyphPresence": {c: ord(c) in cmap for c in han},
                      "allProposedMissing": [c for c in han if ord(c) not in cmap]})
    font_record = {
        "schemaVersion": 1, "batch": BATCH, "proposedTextInventory": data["proposedHanText"],
        "auditedHanCount": len(han), "auditedHan": han, "fonts": fonts,
        "rareHanRangeCharacters": [c for c in han if 0x2E80 <= ord(c) <= 0x2FDF
                                   or 0x3400 <= ord(c) <= 0x4DBF or 0xF900 <= ord(c) <= 0xFAFF
                                   or 0x20000 <= ord(c) <= 0x2FFFF],
        "mechanism": "Actual unchanged RareHan.kt/RareHanTest.kt read; actual bundled font cmaps inspected.",
        "limits": "Proposed terms, not a nonexistent runtime draft. Reinventorize actual runtime Han later. Cmap coverage is not native/phone legibility or identification of the fallback face.",
    }
    save(OUT / "batch-083-font-preparation.json", font_record)
    public = []
    for item in evidence["publicSources"]:
        path = CONTROL.parent / item["localBytes"]
        body = path.read_bytes()
        assert body and b"kotobank" in body
        public.append({"path": str(path), "url": item["url"],
                       "bytes": len(body), "sha256": digest(body),
                       "limits": "Byte receipt only; semantic inspection and truncation limits remain in source evidence."})
    current_counts = {
        "kanji": len(kanji_meta), "words": len(words), "n1Labelled": sum(m.get("jlpt") == 1 for m in kanji_meta),
        "namedSourceMembersPresent": len(current & set(named)),
    }
    assert current_counts == {"kanji": 1094, "words": 5050, "n1Labelled": 114, "namedSourceMembersPresent": 113}
    result = {
        "schemaVersion": 1, "execution": EXECUTION, "batch": BATCH,
        "stage": "source-prepared-not-drafted", "baseCommit": BASE, "membership": [CHAR], "sourceRow": 92,
        "frozenInputHashesVerified": 5, "decompressedDictionaryHashesVerified": 2,
        "exactFrozenNamedMembershipAndRowVerified": True, "packets": packets,
        "freshExactDictionaryExtractions": 3, "dictionaryFamilyOccurrences": 44,
        "distinctCompleteFamilies": 42, "allExtractedEntryIdsAccountedFor": True,
        "rawCharacterPackets": raw_packets, "authorInspection": data["authorInspection"],
        "inspectedArticleHashes": {n: digest((ROOT / n).read_bytes())
                                  for n in data["authorInspection"]["completeExistingArticlesRead"]},
        "publicSourceByteReceipts": public, "pinnedSvg": stroke,
        "fontPreparation": "batch-083-font-preparation.json",
        "allMetadataReadingDispositionsVerified": 2,
        "proposedOnKeys": projection["onKeys"], "proposedKunKeys": projection["kunKeys"],
        "originalBaselineMetadataAndStrokesPreserved": counts,
        "baselineMetadataExceptions": exceptions,
        "baselineKanjiDistractorException": {"kanji/\u5c71.md": ["\u5ddd", "\u51fa", "\u6728"]},
        "runtimeManifestEqualToPublishedBase": True, "manifestBytesUnchanged": True,
        "allRuntimePayloadHashesVerified": checked, "contentVersion": manifest["contentVersion"],
        "exactPublishedAdditionMembershipVerified": len(additions), "currentCounts": current_counts,
        "allMappedCurrentlyCardableReciprocalPairsEnumerated": 2, "requiredDirectedLinks": 4,
        "activatedBaselineDeclaredPairs": 0, "proposedNewWordArticles": 2,
        "proposedChangedReusedArticles": [], "runtimeChanges": 0, "reviewersLaunched": 0,
        "freshAndroidOrNativeClaimed": False, "publishedAdditions": 109, "remainingAdditions": 1119,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "processDiagnostic": "Initial lexical extraction persisted successfully; console printing then hit cp1252 UnicodeEncodeError. Print changed to ASCII escaping; existing packet retained, not re-extracted or overwritten. A guessed RareHan path was absent; actual files located and read. Neither event was an access denial.",
        "limits": data["limits"],
    }
    save(OUT / "batch-083-preparation-audit.json", result)
    print(json.dumps({"families": 42, "occurrences": 44, "runtimeHashesUnchanged": checked,
                      "currentCounts": current_counts, "proposedHan": len(han),
                      "cmapAbsences": [f["allProposedMissing"] for f in fonts]}, ensure_ascii=True, indent=2))


def record():
    receipts = {}
    for name in ["source-tests", "validate", "budget", "audit"]:
        path = LOG / f"{name}-568.txt"
        text = path.read_text(encoding="utf-8-sig")
        if name == "source-tests":
            assert "Ran 9 tests" in text and "OK" in text and "FAILED" not in text and "skipped" not in text
        elif name == "validate":
            assert "0 error(s)" in text
        elif name == "budget":
            assert "ERROR" not in text
        else:
            assert '"runtimeHashesUnchanged": 8372' in text
        receipts[name] = {"path": str(path), "sha256": digest(path.read_bytes())}
    recipe = OUT / "batch-083-source-recipe.py"
    recipe.write_bytes(Path(__file__).read_bytes())
    save(OUT / "execution-568.json", {
        "schemaVersion": 1, "execution": EXECUTION, "batch": BATCH, "baseCommit": BASE,
        "stage": "source-prepared-not-drafted",
        "startingState": load(CONTROL / "progress.json")["execution568StartingState"],
        "sourceAudit": "batch-083-preparation-audit.json", "sourcePacket": "batch-083-progress.json",
        "sourceEvidence": "batch-083-source-evidence.json",
        "preparationRecipe": {
            "durableControlPath": str(Path(__file__)), "archive": recipe.name, "sha256": digest(recipe.read_bytes()),
            "limits": "Committed packets/approved workspace inputs/control helpers only; no optional historical session recipes accessed.",
        },
        "checks": receipts, "runtimeChanges": 0, "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "runtimePublished": False, "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 109, "remainingAdditions": 1119,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "nextAction": load(OUT / "batch-083-progress.json")["nextAction"],
        "limits": load(OUT / "batch-083-progress.json")["limits"],
    })
    print("Source recipe and execution evidence archived for normal signed LOCAL checkpoint.")


def seal():
    original = load(LOG / "execution-568-start-progress.json")
    p = load(CONTROL / "progress.json")
    assert p["checkpoint"] == 567 and p["batch"] == BATCH
    assert not git("status", "--porcelain") and git("log", "-1", "--format=%G?") == "G"
    head = git("rev-parse", "HEAD")
    assert head != BASE and git("rev-parse", "origin/main") == BASE
    assert not git("diff", BASE, "HEAD", "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    android = CONTROL.parent / "kanji-cards-android"
    assert not git("status", "--porcelain", root=android)
    assert git("rev-parse", "HEAD", root=android) == "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
    allowed = {"checkpoint", "status", "stage", "batch", "nextAction", "blocker"}
    assert all(p.get(k) == v for k, v in original.items() if k not in allowed)
    data = load(OUT / "batch-083-progress.json")
    checkpoint = {
        "schemaVersion": 1, "execution": EXECUTION, "checkpoint": EXECUTION, "batch": BATCH,
        "status": "continue", "stage": "source-prepared-not-drafted", "savedCommit": head, "signature": "G",
        "sourcePacket": "docs/n1-sources/batch-083-progress.json",
        "sourceAudit": "docs/n1-sources/batch-083-preparation-audit.json",
        "evidence": "docs/n1-sources/execution-568.json", "dedicatedWorktreesClean": True,
        "sourceRow": 92, "membership": [CHAR], "completeDictionaryFamilies": 42,
        "dictionaryFamilyOccurrences": 44, "completeRawCharacterRecords": 8,
        "completeExistingArticlesRead": 14, "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "runtimeChanged": False, "runtimePublished": False, "independentReviewersLaunched": 0,
        "freshAndroidOrNativeClaimed": False, "publishedAdditions": 109, "remainingAdditions": 1119,
        "lastPublishedCommit": BASE, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
        "proposedOnKeys": data["proposedCuratedProjection"]["onKeys"],
        "proposedKunKeys": data["proposedCuratedProjection"]["kunKeys"],
        "allMappedPairs": 2, "directedLinks": 4,
        "proposedSupport": "Necessary new \u51cc\u3050\u3057\u306e\u3050 and \u51cc\u99d5\u308a\u3087\u3046\u304c; no inferred word levels; \u99d5 card absent.",
        "proposedChanges": "No reused teaching edits. Both new support articles and all written kanji/pairs/quiz overlaps remain subject to runtime audit and independent review.",
        "pinnedSvgPaths": 10, "geometryConverted": False,
        "proposedHan": load(OUT / "batch-083-font-preparation.json")["auditedHanCount"],
        "fontAcceptance": "Proposed cmaps audited; actual draft/native/phone rendering pending.",
        "runtimeHashesUnchanged": 8372, "contentVersion": "d82e7fefe3898a70", "focusedTestsPassed": 9,
        "originalHistoricalRootKeysCompared": len(original), "allOriginalHistoricalValuesPreserved": True,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "nextAction": data["nextAction"],
    }
    p["execution568CoordinatorCheckpoint"] = checkpoint
    p["batch083SourcePreparation"] = checkpoint
    p.update(checkpoint=EXECUTION, stage="batch-083-source-prepared-not-drafted",
             status="continue", blocker=None, nextAction=data["nextAction"])
    save(CONTROL / "progress.json", p)
    reread = load(CONTROL / "progress.json")
    assert all(reread.get(k) == v for k, v in original.items() if k not in allowed)
    save(LOG / "execution-568-final-checkpoint.json", checkpoint)
    print(json.dumps(checkpoint, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=[
        "start", "lexical", "comparison", "extra", "records", "support-records", "audit", "record", "seal"
    ])
    parser.add_argument("items", nargs="*")
    args = parser.parse_args()
    if args.operation == "start":
        start()
    elif args.operation == "audit":
        audit()
    elif args.operation == "record":
        record()
    elif args.operation == "seal":
        seal()
    elif args.operation == "records":
        records(args.items)
    elif args.operation == "support-records":
        records(args.items, "support-kanjidic2")
    else:
        packet(args.operation, args.items)

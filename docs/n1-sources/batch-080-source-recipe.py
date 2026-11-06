"""Prepare and verify a bounded source packet from approved frozen inputs."""
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
LOG = CONTROL / "logs" / "428f5ec8-314d-45f9-b454-fd76de95b94e"
OUT = ROOT / "docs" / "n1-sources"
BASE = "b120125ae5cdbfe9f3bcb1b0a7ae8a61e422ec8d"
CHAR = "冴"
BATCH = "080"
EXECUTION = 537
sys.path.insert(0, str(ROOT / "tools"))
from audit_n1_pilot import metadata
from extract_n1_jmdict import extract


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def git(*args):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=ROOT, encoding="utf-8").strip()


def frozen():
    snapshot = load(ROOT / "docs" / "n1-source-snapshot.json")
    for name, info in snapshot["inputs"].items():
        data = (CONTROL / "inputs" / name).read_bytes()
        assert len(data) == info["bytes"] and digest(data) == info["sha256"], name
    raw = (CONTROL / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    xml = gzip.decompress(raw)
    kd = gzip.decompress((CONTROL / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes())
    assert digest(xml) == snapshot["jmdict"]["xmlSha256"]
    assert digest(kd) == snapshot["kanjidic2"]["xmlSha256"]
    return snapshot, raw, ET.fromstring(xml), ET.fromstring(kd)


def start():
    progress = load(CONTROL / "progress.json")
    assert progress["checkpoint"] == 536 and progress["batch"] == "079"
    assert progress["lastPublishedCommit"] == BASE and progress["remainingAdditions"] == 1122
    assert git("rev-parse", "HEAD") == git("rev-parse", "origin/main") == BASE
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    backup = LOG / "execution-537-start-progress.json"
    assert not backup.exists()
    save(backup, progress)
    request = (LOG / "request.txt").read_bytes()
    text = request.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["checkpoint"] == 536
    progress["execution537StartingState"] = {
        "execution": EXECUTION, "batch": BATCH, "startingHead": BASE,
        "scope": "ONE source-preparation checkpoint for pending row89冴; no runtime draft, reviewer, Android/native, publication,081 or second runner.",
        "authorization": {
            "requestSha256": digest(request), "bytes": len(request), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded and embedded checkpoint parsed; operative contract, final536 and approved issue inspected directly. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "worktrees": "Dedicated content/Android clean, signed heads b120125a/f9b59a2; fresh origin/main b120125a. Canonical repositories not accessed.",
        "artifactPathPreflight": {
            "guide": str(CONTROL / "authoring-artifact-path-notes.txt"),
            "durableHelper": str(Path(__file__)),
            "optionalHistoricalHelpersAccessed": False,
            "actualNewPermissionDenials": [],
        },
        "startedAt": datetime.now().astimezone().isoformat(),
    }
    progress.update(batch=BATCH, stage="batch-080-source-preparation-in-progress",
                    status="continue", blocker=None,
                    nextAction="SAME080 source preparation only for row89冴; preserve full history and all later gates.")
    save(CONTROL / "progress.json", progress)
    print("Starting scope persisted with complete live history.")


def packet(kind, spellings):
    snapshot, raw, source, kd = frozen()
    row = next(r for r in load(OUT / "source-index.json") if r["kanji"] == CHAR)
    assert row["sourceRow"] == 89 and not (ROOT / row["article"]).exists()
    named = load(CONTROL / "inputs" / "n1-kanji-source-20261102.json")
    assert len(named) == len(set(named)) == 1232 and named[88] == CHAR
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
        "selectionRule": "Every complete frozen family containing 冴 in any keb; all aliases/restrictions/senses retained."
        if kind == "lexical" else "Every complete frozen family matching exact requested keb/reb; homographs retained.",
        "limits": "Extraction is not author inspection, frequency evidence or independent review.",
    }
    if kind != "lexical":
        selection["requestedSpellings"] = spellings
    selection_path = OUT / f"batch-{BATCH}-{kind}-selection.json"
    assert not selection_path.exists()
    save(selection_path, selection)
    suffix = "jmdict" if kind == "lexical" else f"{kind}-jmdict"
    data = extract(raw, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
    path = OUT / f"batch-{BATCH}-{suffix}.xml"
    assert not path.exists()
    path.write_bytes(data)
    if kind == "lexical":
        declared = []
        for p in sorted((ROOT / "words").glob("*.md")):
            name = p.relative_to(ROOT).as_posix()
            m = metadata(ROOT, name)
            if CHAR in m.get("kanji", []) or m["reading"] in {"さえる", "こおる", "ひえる"}:
                declared.append({"article": name, "metadata": m})
        save(CONTROL / "batch-080-source-navigation.json", {
            "sourceIndexRecord": row, "candidates": declared,
            "baselinePairs": [r for r in load(OUT / "baseline-word-candidates.json") if r["kanji"] == CHAR],
        })
        print(json.dumps({"row": row, "candidates": declared}, ensure_ascii=True, indent=2))
    print(f"{kind}: {len(ids)} complete families / {len(data.splitlines())} XML lines.")


def raw_records(chars):
    snapshot, raw, source, kd = frozen()
    records = {e.findtext("literal"): e for e in kd.findall("character")}
    selected = ET.Element("kanjidic2")
    selected.append(kd.find("header"))
    for char in chars:
        selected.append(records[char])
    ET.indent(selected, space="  ")
    data = ET.tostring(selected, encoding="utf-8", xml_declaration=True) + b"\n"
    path = OUT / "batch-080-kanjidic2.xml"
    assert not path.exists()
    path.write_bytes(data)
    save(OUT / "batch-080-input-metadata.json", {
        "schemaVersion": 1, "batch": BATCH, "baseCommit": BASE,
        "sourceIndexRecord": next(r for r in load(OUT / "source-index.json") if r["kanji"] == CHAR),
        "rawCharacterPacket": path.name, "rawCharacterPacketSha256": digest(data),
        "characters": chars,
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
    data = load(OUT / "batch-080-progress.json")
    evidence = load(OUT / "batch-080-source-evidence.json")
    membership = load(OUT / "batch-080-membership.json")
    row = next(r for r in load(OUT / "source-index.json") if r["kanji"] == CHAR)
    named = load(CONTROL / "inputs" / "n1-kanji-source-20261102.json")
    assert named == load(OUT / "community-list-20261102.json")
    assert len(named) == len(set(named)) == 1232 and named[88] == CHAR
    assert data["membership"] == membership["membership"] == [CHAR]
    assert data["baseCommit"] == membership["baseCommit"] == git("rev-parse", "HEAD") == BASE
    assert data["drafted"] == data["reviewClosed"] == data["published"] == []
    assert data["status"] == "source-prepared-not-drafted"
    assert all(not (ROOT / p).exists() for p in [row["article"], row["strokeFile"], "words/冴える.md"])
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
    assert projection["quizOnyomi"] == [] and projection["quizKunyomi"] == ["さ.える"]
    families, packets = {}, []
    for kind in ["lexical", "comparison", "related"]:
        selection = load(OUT / f"batch-080-{kind}-selection.json")
        requested = set(selection.get("requestedSpellings", []))
        ids = [
            e.findtext("ent_seq") for e in source.findall("entry")
            if (any(CHAR in k.text for k in e.findall("k_ele/keb")) if kind == "lexical"
                else any(k.text in requested for k in e.findall("k_ele/keb"))
                or any(r.text in requested for r in e.findall("r_ele/reb")))
        ]
        assert ids == selection["entryIds"]
        suffix = "jmdict" if kind == "lexical" else f"{kind}-jmdict"
        path = OUT / f"batch-080-{suffix}.xml"
        packet_bytes = path.read_bytes()
        assert packet_bytes == extract(raw, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        described = [i for d in evidence[f"{kind}Decisions"] for i in d["entryIds"]]
        assert len(described) == len(set(described)) and set(described) == set(ids)
        entries = ET.fromstring(packet_bytes).findall("entry")
        families.update((e.findtext("ent_seq"), e) for e in entries)
        packets.append({"path": path.name, "families": len(entries),
                        "lines": len(packet_bytes.splitlines()), "sha256": digest(packet_bytes)})
    assert [p["families"] for p in packets] == [16, 12, 8] and len(families) == 35
    raw_bytes = (OUT / "batch-080-kanjidic2.xml").read_bytes()
    selected = ET.fromstring(raw_bytes)
    raw_meta = load(OUT / "batch-080-input-metadata.json")
    assert raw_meta["sourceIndexRecord"] == row and raw_meta["rawCharacterPacketSha256"] == digest(raw_bytes)
    assert [e.findtext("literal") for e in selected.findall("character")] == raw_meta["characters"]
    assert canonical(selected.find("header")) == canonical(kd.find("header"))
    assert all(canonical(e) == canonical(records[e.findtext("literal")]) for e in selected.findall("character"))
    assert lexical_pair(families["1297050"], "冴える", "さえる")
    assert families["1877830"].findtext("sense/misc") == "rare term"
    assert families["1297050"].findall("sense")[-1].findtext("s_inf") == "original meaning; now somewhat old-fashioned"
    declared = [f"words/{p.name}" for p in (ROOT / "words").glob("*.md")
                if CHAR in metadata(ROOT, f"words/{p.name}").get("kanji", [])]
    assert declared == data["currentDeclaredWordPairs"] == []
    assert not [e for e in load(OUT / "baseline-word-candidates.json") if e["kanji"] == CHAR]
    same_primary = [p.name for p in (ROOT / "words").glob("*.md")
                    if metadata(ROOT, f"words/{p.name}")["reading"] == "さえる"]
    assert same_primary == []
    mapping = data["proposedSupportMapping"]
    expected_pairs = {(c, m["article"]) for m in mapping for c in m["allWrittenKanji"]
                      if c == CHAR or (ROOT / "kanji" / f"{c}.md").exists()}
    assert expected_pairs == {tuple(p) for p in data["proposedReciprocalPairs"]} == {(CHAR, "words/冴える.md")}
    assert {(p["from"], p["to"]) for p in data["proposedDirectedLinkPlan"]} == {
        ("kanji/冴.md", "words/冴える.md"), ("words/冴える.md", "kanji/冴.md")}
    assert not data["proposedChangedReusedPassages"]
    all_meta = [metadata(ROOT, f"kanji/{p.name}") for p in (ROOT / "kanji").glob("*.md")]
    quiz = data["proposedKanjiQuizAudit"]
    assert quiz["title"] not in {m["title"] for m in all_meta}
    assert len(quiz["distractors"]) == len({c["kanji"] for c in quiz["distractors"]}) == 3
    for choice in quiz["distractors"]:
        assert metadata(ROOT, f"kanji/{choice['kanji']}.md")["title"] == choice["title"]
    assert all((ROOT / "words" / f"{w}.md").exists() for w in data["proposedWordQuizAudit"]["directExclusions"])
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
    assert additions == accepted and len(additions) == 106 and additions <= set(named)
    assert metadata(ROOT, "kanji/妖.md")["jlpt"] == 1
    assert not git("diff", BASE, "--", "kanji", "words", "articles", "strokes", "tools", "manifest.json",
                   "docs/n1-source-snapshot.json", "docs/n1-sources/source-index.json",
                   "docs/n1-sources/baseline-inventory.json", "docs/n1-sources/baseline-word-candidates.json")
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
    assert checked == 8363 and manifest["contentVersion"] == "a01eb85b17601ac0"
    tree = load(CONTROL / "inputs" / "n1-kanjivg-tree-70a0b7ae.json")
    assert not tree["truncated"] and tree["sha"] == snapshot["kanjivg"]["revision"]
    assert next(t for t in tree["tree"] if t["path"] == row["kanjivgInventory"]["path"]) == row["kanjivgInventory"]
    svg_path = CONTROL / "inputs" / "n1-051b4-70a0b7ae.svg"
    svg = svg_path.read_bytes()
    blob = hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest()
    assert blob == row["kanjivgInventory"]["sha"] and len(svg) == row["kanjivgInventory"]["size"]
    paths = ET.fromstring(svg).findall(".//{http://www.w3.org/2000/svg}path")
    assert len(paths) == row["metadata"]["strokes"] == 7
    assert [p.attrib["id"] for p in paths] == [f"kvg:051b4-s{i}" for i in range(1, 8)]
    converter = digest((ROOT / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n"))
    assert converter == snapshot["kanjivg"]["converter"]["normalizedSha256"]
    unicode_rows = (CONTROL / "inputs" / "n1-UnicodeData-17.0.0.txt").read_text(encoding="utf-8").splitlines()
    assert next(s for s in unicode_rows if s.startswith("2F0E;")).split(";")[5] == "<compat> 51AB"
    stroke = {"revision": tree["sha"], "input": str(svg_path), "gitBlob": blob,
              "sourceUrl": "https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/kanji/051b4.svg",
              "bytes": len(svg), "sha256": digest(svg), "dictionaryStrokeCount": 7,
              "sourceStrokePaths": 7, "converted": False, "nativeDrawingAccepted": False,
              "converterNormalizedSha256": converter,
              "limits": "Whole pinned SVG inspected; geometric group names do not establish historical derivation."}
    save(OUT / "batch-080-stroke-evidence.json", stroke)
    han = sorted({c for c in data["proposedHanText"] if 0x2E80 <= ord(c) <= 0x2FDF
                  or 0x3400 <= ord(c) <= 0x9FFF or 0xF900 <= ord(c) <= 0xFAFF
                  or 0x20000 <= ord(c) <= 0x2FFFF})
    fonts = []
    for old in load(OUT / "batch-079-font-preparation.json")["fonts"]:
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
        "rareHanRangeCharacters": [c for c in han if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x4DBF
                                   or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF],
        "mechanism": "Actual unchanged RareHan.kt/RareHanTest.kt read; all three actual bundled cmaps inspected.",
        "limits": "Only proposed draft terms inventoried, not a nonexistent final draft. Reinventory every actual runtime Han after authoring; main cmap absence is not native glyph failure. No native/phone evidence."
    }
    save(OUT / "batch-080-font-preparation.json", font_record)
    public_bytes = []
    for name in ["batch-080-daijisen-saeru.html", "batch-080-jitsu-sae.html"]:
        path = CONTROL / "inputs" / name
        public_bytes.append({"path": str(path), "bytes": path.stat().st_size, "sha256": digest(path.read_bytes()),
                             "limits": "Actual downloaded page bytes; semantic inspection is the bounded tool return recorded in source evidence, not a claim every page byte was read."})
    current_counts = {"kanji": len(all_meta), "words": len(list((ROOT / "words").glob("*.md"))),
                      "n1Labelled": sum(m.get("jlpt") == 1 for m in all_meta),
                      "namedSourceMembersPresent": len(current_kanji & set(named))}
    assert current_counts == {"kanji": 1091, "words": 5047, "n1Labelled": 111, "namedSourceMembersPresent": 110}
    result = {
        "schemaVersion": 1, "execution": EXECUTION, "batch": BATCH, "stage": "source-prepared-not-drafted",
        "baseCommit": BASE, "membership": [CHAR], "sourceRow": 89,
        "frozenInputHashesVerified": 5, "decompressedDictionaryHashesVerified": 2,
        "exactFrozenNamedMembershipAndRowVerified": True, "packets": packets,
        "freshExactDictionaryExtractions": 3, "dictionaryFamilyOccurrences": 36,
        "distinctCompleteFamilies": 35, "allExtractedEntryIdsAccountedFor": True,
        "rawCharacterPacket": {"characters": 4, "sha256": digest(raw_bytes), "allRecordsAndHeaderVerified": True},
        "authorInspection": data["authorInspection"],
        "inspectedArticleHashes": {n: digest((ROOT / n).read_bytes()) for n in data["authorInspection"]["completeExistingArticlesRead"]},
        "publicSourceByteReceipts": public_bytes, "pinnedSvg": stroke, "fontPreparation": font_record,
        "allFiveReadingDispositionsVerified": True, "proposedOnKeys": [], "proposedKunKeys": ["さえる"],
        "originalBaselineMetadataAndStrokesPreserved": counts, "baselineMetadataExceptions": exceptions,
        "baselineKanjiDistractorException": {"kanji/山.md": ["川", "出", "木"]},
        "runtimeManifestEqualToPublishedBase": True, "manifestBytesUnchanged": True,
        "allRuntimePayloadHashesVerified": checked, "contentVersion": manifest["contentVersion"],
        "exactPublishedAdditionMembershipVerified": len(additions), "currentCounts": current_counts,
        "allMappedCurrentlyCardableReciprocalPairsEnumerated": 1, "requiredDirectedLinks": 2,
        "activatedBaselinePairs": 0, "proposedNewWordArticles": 1, "runtimeChanges": 0,
        "reviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 106, "remainingAdditions": 1122,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [], "limits": data["limits"],
    }
    save(OUT / "batch-080-preparation-audit.json", result)
    print(json.dumps({"families": 35, "occurrences": 36, "runtimeHashesUnchanged": checked,
                      "currentCounts": current_counts, "proposedHan": len(han),
                      "cmapAbsences": [f["allProposedMissing"] for f in fonts]}, ensure_ascii=True, indent=2))


def record():
    receipts = {}
    for name in ["extract-tests-537.txt", "freeze-tests-537.txt", "validate-537.txt", "manifest-537.txt", "budget-537.txt"]:
        path = LOG / name
        text = path.read_text(encoding="utf-8-sig")
        if name.startswith(("extract-tests", "freeze-tests")):
            expected = 5 if name.startswith("extract-tests") else 4
            assert f"Ran {expected} tests" in text and "OK" in text and "FAILED" not in text and "skipped" not in text
        elif name.startswith("validate"):
            assert "0 error(s)" in text
        elif name.startswith("manifest"):
            assert "8363" in text and "a01eb85b17601ac0" in text
        else:
            assert "ERROR" not in text and "8385" in text
        receipts[name] = {"path": str(path), "sha256": digest(path.read_bytes())}
    audit_data = load(OUT / "batch-080-preparation-audit.json")
    recipe = OUT / "batch-080-source-recipe.py"
    recipe.write_bytes(Path(__file__).read_bytes())
    save(OUT / "execution-537.json", {
        "schemaVersion": 1, "execution": EXECUTION, "batch": BATCH, "baseCommit": BASE,
        "stage": "source-prepared-not-drafted",
        "startingState": load(CONTROL / "progress.json")["execution537StartingState"],
        "sourceAudit": "batch-080-preparation-audit.json", "sourcePacket": "batch-080-progress.json",
        "sourceEvidence": "batch-080-source-evidence.json",
        "preparationRecipe": {"durableControlPath": str(Path(__file__)), "archive": recipe.name,
                              "sha256": digest(recipe.read_bytes()),
                              "limits": "Later coordinators use committed packets/approved workspace inputs, not optional historical session recipes."},
        "checks": receipts, "runtimeChanges": 0, "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "runtimePublished": False, "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 106, "remainingAdditions": 1122,
        "nextAction": load(OUT / "batch-080-progress.json")["nextAction"], "limits": audit_data["limits"],
    })
    print("Source recipe and execution evidence archived for a normal signed local source checkpoint.")


def seal():
    original = load(LOG / "execution-537-start-progress.json")
    progress = load(CONTROL / "progress.json")
    assert progress["checkpoint"] == 536 and progress["batch"] == BATCH
    assert not git("status", "--porcelain") and git("log", "-1", "--format=%G?") == "G"
    head = git("rev-parse", "HEAD")
    assert head != BASE and git("rev-parse", "origin/main") == BASE
    assert not git("diff", BASE, "HEAD", "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    allowed = {"checkpoint", "status", "stage", "batch", "nextAction", "blocker"}
    assert all(progress.get(k) == v for k, v in original.items() if k not in allowed)
    data = load(OUT / "batch-080-progress.json")
    progress["execution537CoordinatorCheckpoint"] = {
        "schemaVersion": 1, "execution": EXECUTION, "checkpoint": EXECUTION, "batch": BATCH,
        "savedCommit": head, "signature": "G", "sourcePacket": "docs/n1-sources/batch-080-progress.json",
        "sourceAudit": "docs/n1-sources/batch-080-preparation-audit.json", "evidence": "docs/n1-sources/execution-537.json",
        "membership": [CHAR], "sourceRow": 89, "distinctCompleteFamilies": 35, "completeRawCharacterRecords": 4,
        "completeExistingArticlesRead": 21, "fiveReadingDispositions": True,
        "pinnedSvgPaths": 7, "geometryConverted": False, "focusedTestsPassed": 9,
        "runtimeHashesUnchanged": 8363, "manifestBytesUnchanged": True,
        "runtimeDrafted": [], "reviewClosed": [], "published": [], "runtimePublished": False,
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 106, "remainingAdditions": 1122, "lastPublishedCommit": BASE,
        "allOriginalHistoricalRootValuesPreservedExactly": True, "originalRootKeysCompared": len(original),
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "nextAction": data["nextAction"], "status": "continue",
    }
    progress.update(checkpoint=EXECUTION, status="continue", stage="batch-080-source-prepared-not-drafted",
                    nextAction=data["nextAction"], blocker=None)
    save(CONTROL / "progress.json", progress)
    verified = load(CONTROL / "progress.json")
    assert all(verified.get(k) == v for k, v in original.items() if k not in allowed)
    save(LOG / "execution-537-final-checkpoint.json", verified["execution537CoordinatorCheckpoint"])
    print(json.dumps(verified["execution537CoordinatorCheckpoint"], ensure_ascii=True, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["start", "lexical", "comparison", "related", "raw", "audit", "record", "seal"])
    parser.add_argument("values", nargs="*")
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
        raw_records(args.values)
    else:
        packet(args.action, args.values)

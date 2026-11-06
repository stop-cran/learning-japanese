"""Prepare one source-only N1 checkpoint using approved durable inputs."""
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
LOGS = CONTROL / "logs" / "ea79aee6-273b-4535-b966-a6814f590146"
OUT = ROOT / "docs" / "n1-sources"
BASE = "2a6777503de6c23c2ac5582b0265dd68d224f44c"
BATCH = "079"
EXECUTION = 529
CHAR = "冠"
ROW = 88
sys.path.insert(0, str(ROOT / "tools"))
from audit_n1_pilot import metadata, offered_keys
from build_manifest import build_manifest, sha256
from extract_n1_jmdict import extract
from freeze_n1_sources import metadata_record


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def git(*args):
    return subprocess.check_output(
        ["git", "--no-pager", *args], cwd=ROOT, encoding="utf-8").strip()


def frozen():
    snapshot = load(ROOT / "docs" / "n1-source-snapshot.json")
    for name, info in snapshot["inputs"].items():
        assert digest((CONTROL / "inputs" / name).read_bytes()) == info["sha256"], name
    raw = (CONTROL / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    xml = gzip.decompress(raw)
    kd = gzip.decompress((CONTROL / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes())
    assert digest(xml) == snapshot["jmdict"]["xmlSha256"]
    assert digest(kd) == snapshot["kanjidic2"]["xmlSha256"]
    return snapshot, raw, ET.fromstring(xml), ET.fromstring(kd)


def start():
    progress = load(CONTROL / "progress.json")
    assert progress["checkpoint"] == 528 and progress["batch"] == "078"
    assert progress["lastPublishedCommit"] == BASE and progress["remainingAdditions"] == 1123
    assert git("rev-parse", "HEAD") == git("rev-parse", "origin/main") == BASE
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    backup = LOGS / "checkpoint-full-start.json"
    assert not backup.exists()
    save(backup, progress)
    request = (LOGS / "request.txt").read_bytes()
    text = request.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["checkpoint"] == 528
    progress["execution529StartingState"] = {
        "execution": EXECUTION, "batch": BATCH, "startingHead": BASE,
        "scope": "ONE source-preparation checkpoint for pending row88冠. No runtime draft, independent reviewer, Android/native, publication,080 or second runner.",
        "authorization": {
            "requestSha256": digest(request), "characters": len(text),
            "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded and checkpoint parsed; operative contract, final528 and complete approved issue inspected directly. Historical middle loaded/parsed, not freshly semantically re-reviewed.",
        },
        "worktrees": "Dedicated worktrees clean; normally signed contentG equals fresh origin/main2a677750; Android signedGf9b59a2. Canonical repositories not accessed.",
        "artifactPathPreflight": {
            "guide": str(CONTROL / "authoring-artifact-path-notes.txt"),
            "inputs": "Committed source packets and approved control inputs only.",
            "durableHelper": str(Path(__file__)),
            "optionalHistoricalHelpersAccessed": False, "newPermissionDenials": [],
        },
        "startedAt": datetime.now().astimezone().isoformat(),
    }
    progress.update(batch=BATCH, stage="batch-079-source-preparation-in-progress",
                    status="continue", blocker=None,
                    nextAction="SAME079 source preparation only for pending row88冠; preserve full history and every later gate.")
    save(CONTROL / "progress.json", progress)
    print("Starting scope saved; complete original live history preserved.")


def packet(kind, spellings):
    snapshot, raw, source, kd = frozen()
    row = next(r for r in load(OUT / "source-index.json") if r["sourceRow"] == ROW)
    assert row["kanji"] == CHAR and not (ROOT / row["article"]).exists()
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
        "selectionRule": (
            "Every complete frozen family containing 冠 in any keb; preserve all aliases, readings, restrictions and senses."
            if kind == "lexical" else
            "Every complete family matching an exact requested keb/reb; homographs retained."
        ),
        "limits": "Extraction alone is not author inspection, frequency evidence or independent review.",
    }
    if kind != "lexical":
        selection["requestedSpellings"] = spellings
    save(OUT / f"batch-{BATCH}-{kind}-selection.json", selection)
    suffix = "jmdict" if kind == "lexical" else f"{kind}-jmdict"
    path = OUT / f"batch-{BATCH}-{suffix}.xml"
    data = extract(raw, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
    if path.exists():
        assert path.read_bytes() == data
    else:
        path.write_bytes(data)
    if kind == "lexical":
        declared = []
        aliases = []
        for path in sorted((ROOT / "words").glob("*.md")):
            name = path.relative_to(ROOT).as_posix()
            meta = metadata(ROOT, name)
            if CHAR in meta.get("kanji", []):
                declared.append({"article": name, "metadata": meta})
            if meta["reading"] in {"かんむり", "おうかん", "かん", "かぶる"}:
                aliases.append({"article": name, "metadata": meta})
        save(CONTROL / "batch-079-source-navigation.json", {
            "sourceIndexRecord": row, "declared": declared, "sameReading": aliases,
            "baselinePairs": [r for r in load(OUT / "baseline-word-candidates.json") if r["kanji"] == CHAR],
        })
        print(json.dumps({"row": row, "declared": declared, "sameReading": aliases}, ensure_ascii=True, indent=2))
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
    (OUT / "batch-079-kanjidic2.xml").write_bytes(data)
    save(OUT / "batch-079-input-metadata.json", {
        "schemaVersion": 1, "batch": BATCH, "baseCommit": BASE,
        "sourceIndexRecord": next(r for r in load(OUT / "source-index.json") if r["sourceRow"] == ROW),
        "rawCharacterPacket": "batch-079-kanjidic2.xml", "rawCharacterPacketSha256": digest(data),
        "characters": chars, "provenance": "Complete frozen KANJIDIC2 records/header reserialized without dropping fields.",
        "dictionaryAttribution": "Copyright James William Breen and EDRDG; CC BY-SA 4.0; repository NOTICE.",
    })
    print(f"Raw characters: {len(chars)} / {len(data.splitlines())} XML lines.")


def canonical(node):
    return ET.canonicalize(ET.tostring(node, encoding="unicode"), strip_text=True)


def audit():
    from audit_n1_batch import lexical_pair
    from fontTools.ttLib import TTFont
    import yaml

    snapshot, raw, source, kd = frozen()
    data = load(OUT / "batch-079-progress.json")
    membership = load(OUT / "batch-079-membership.json")
    evidence = load(OUT / "batch-079-source-evidence.json")
    assert data["baseCommit"] == membership["baseCommit"] == BASE
    assert data["membership"] == membership["membership"] == [CHAR]
    assert data["drafted"] == data["reviewClosed"] == data["published"] == []
    assert data["status"] == "source-prepared-not-drafted"
    assert all(not (ROOT / p).exists() for p in ("kanji/冠.md", "strokes/冠.json", "words/王冠.md"))
    row = next(r for r in load(OUT / "source-index.json") if r["sourceRow"] == ROW)
    named = load(CONTROL / "inputs" / "n1-kanji-source-20261102.json")
    assert len(named) == len(set(named)) == 1232 and named[ROW - 1] == CHAR == row["kanji"]
    assert load(OUT / "community-list-20261102.json") == named
    records = {e.findtext("literal"): e for e in kd.findall("character")}
    assert metadata_record(records[CHAR], {14: "冖"}) == row["metadata"]
    assert data["sourceReadingOrder"] == {k: row["metadata"][k] for k in ("onyomi", "kunyomi")}
    assert [(d["kind"], d["reading"], d["proposedQuizSelection"], d["selected"])
            for d in data["readingDispositions"]] == [
                ("on", "カン", True, False), ("kun", "かんむり", True, False)]
    projection = data["proposedCuratedProjection"]
    for kind, field, keys in (("onyomi", "quizOnyomi", "onKeys"), ("kunyomi", "quizKunyomi", "kunKeys")):
        assert projection[field] == data["sourceReadingOrder"][kind]
        assert offered_keys(projection[field]) == projection[keys]
    families, packets, remaining = {}, [], {}
    for kind, decision_field in (("lexical", "lexicalDecisions"),
                                 ("comparison", "comparisonDecisions"), ("related", "relatedDecisions")):
        selection = load(OUT / f"batch-079-{kind}-selection.json")
        requested = set(selection.get("requestedSpellings", []))
        ids = [
            e.findtext("ent_seq") for e in source.findall("entry")
            if (any(CHAR in k.text for k in e.findall("k_ele/keb")) if kind == "lexical"
                else any(k.text in requested for k in e.findall("k_ele/keb"))
                or any(r.text in requested for r in e.findall("r_ele/reb")))
        ]
        assert ids == selection["entryIds"]
        suffix = "jmdict" if kind == "lexical" else f"{kind}-jmdict"
        path = OUT / f"batch-079-{suffix}.xml"
        packet_bytes = path.read_bytes()
        assert packet_bytes == extract(raw, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        described = [i for group in evidence[decision_field] for i in group["entryIds"]]
        assert len(described) == len(set(described)) and set(described) <= set(ids)
        remaining[kind] = [i for i in ids if i not in described]
        assert kind == "lexical" or not remaining[kind]
        entries = ET.fromstring(packet_bytes).findall("entry")
        families.update((e.findtext("ent_seq"), e) for e in entries)
        packets.append({"path": path.name, "families": len(entries),
                        "lines": len(packet_bytes.splitlines()), "sha256": digest(packet_bytes)})
    assert [p["families"] for p in packets] == [158, 18, 1]
    assert len(families) == data["authorInspection"]["distinctCompleteFamilies"] == 177
    raw_meta = load(OUT / "batch-079-input-metadata.json")
    raw_bytes = (OUT / "batch-079-kanjidic2.xml").read_bytes()
    selected = ET.fromstring(raw_bytes)
    assert raw_meta["sourceIndexRecord"] == row
    assert raw_meta["rawCharacterPacketSha256"] == digest(raw_bytes)
    assert [r.findtext("literal") for r in selected.findall("character")] == raw_meta["characters"]
    assert canonical(selected.find("header")) == canonical(kd.find("header"))
    assert all(canonical(r) == canonical(records[r.findtext("literal")]) for r in selected.findall("character"))
    for mapping in data["proposedSupportMapping"]:
        assert lexical_pair(families[mapping["entryId"]], mapping["word"], mapping["primaryReading"])
        if not mapping["newArticleNecessary"]:
            meta = metadata(ROOT, mapping["article"])
            assert meta["reading"] == mapping["primaryReading"] and meta["word"] == mapping["word"]
            assert meta["kanji"] == mapping["allWrittenKanji"] and meta["jlpt"] == mapping["preservedWordJlpt"] == 2
    assert [g.text for g in families["1181450"].findall("sense/gloss")] == ["crown", "diadem", "bottle cap"]
    assert families["1577620"].findall("sense")[4].findtext("stagr") == "かん"
    declared = [f"words/{p.name}" for p in sorted((ROOT / "words").glob("*.md"))
                if CHAR in metadata(ROOT, f"words/{p.name}").get("kanji", [])]
    assert declared == data["currentDeclaredWordPairs"] == ["words/冠.md"]
    baseline_pairs = [r for r in load(OUT / "baseline-word-candidates.json") if r["kanji"] == CHAR]
    assert len(baseline_pairs) == 1 and baseline_pairs[0]["article"] == declared[0]
    pairs = [tuple(p) for p in data["proposedReciprocalPairs"]]
    expected_pairs = {(c, m["article"]) for m in data["proposedSupportMapping"]
                      for c in m["allWrittenKanji"] if c == CHAR or (ROOT / "kanji" / f"{c}.md").exists()}
    assert set(pairs) == expected_pairs and len(pairs) == len(set(pairs)) == 3
    directed = data["proposedDirectedLinkPlan"]
    assert len(directed) == 6 and {(p["from"], p["to"]) for p in directed} == {
        (a, b) for c, article in pairs
        for a, b in [(f"kanji/{c}.md", article), (article, f"kanji/{c}.md")]}
    proposed_bodies = {}
    for change in data["proposedChangedReusedPassages"]:
        text = (ROOT / change["article"]).read_text(encoding="utf-8")
        assert text.count(change["before"]) == 1 and change["after"] not in text
        after = text.replace(change["before"], change["after"], 1)
        assert yaml.safe_load(after.split("---", 2)[1]) == metadata(ROOT, change["article"])
        proposed_bodies[change["article"]] = after
    for p in directed:
        if p["from"] in proposed_bodies:
            assert f"(../{p['to']})" in proposed_bodies[p["from"]]
    all_meta = [metadata(ROOT, f"kanji/{p.name}") for p in (ROOT / "kanji").glob("*.md")]
    quiz = data["proposedKanjiQuizAudit"]
    assert quiz["title"] not in [m["title"] for m in all_meta]
    assert len(quiz["distractors"]) == len({r["kanji"] for r in quiz["distractors"]}) == 3
    for choice in quiz["distractors"]:
        assert metadata(ROOT, f"kanji/{choice['kanji']}.md")["title"] == choice["title"]
    assert len(metadata(ROOT, "kanji/帽.md")["distractors"]) == 3
    assert all((ROOT / "words" / f"{w}.md").exists() for w in data["proposedWordQuizAudit"]["directExclusions"])
    baseline = load(OUT / "baseline-inventory.json")
    exceptions = {"words/虎.md": ["酔っ払い"], "words/猿.md": ["馬鹿"],
                  "words/丘.md": ["坂", "山"], "words/冗談.md": ["ユーモア"]}
    counts = {"kanji": 0, "words": 0, "strokes": 0}
    for name, item in baseline["files"].items():
        kind = name.split("/")[0]
        if kind in ("kanji", "words"):
            expected = dict(item["metadata"])
            if name in exceptions:
                expected["quiz_exclusions"] = exceptions[name]
            if name == "kanji/山.md":
                expected["distractors"] = ["川", "出", "木"]
            assert metadata(ROOT, name) == expected, name
            counts[kind] += 1
        elif kind == "strokes":
            assert digest((ROOT / name).read_bytes()) == item["sha256"]
            counts[kind] += 1
    assert counts == {"kanji": 985, "words": 4942, "strokes": 985}
    baseline_kanji = {Path(n).stem for n in baseline["files"] if n.startswith("kanji/")}
    actual_kanji = {p.stem for p in (ROOT / "kanji").glob("*.md")}
    additions = actual_kanji - baseline_kanji
    accepted = set("幹氏扱乃凹凸矛鷹彗漱栞莉")
    for path in OUT.glob("batch-*-progress.json"):
        accepted.update(load(path).get("published", []))
    assert additions == accepted and len(additions) == 105 and additions <= set(named)
    assert metadata(ROOT, "kanji/妖.md")["jlpt"] == 1
    assert not git("diff", BASE, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools",
                   "docs/n1-source-snapshot.json", "docs/n1-sources/source-index.json",
                   "docs/n1-sources/baseline-inventory.json", "docs/n1-sources/baseline-word-candidates.json")
    manifest = load(ROOT / "manifest.json")
    assert manifest == build_manifest(ROOT) == json.loads(git("show", f"{BASE}:manifest.json"))
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
    assert checked == 8360 and manifest["contentVersion"] == "8e06edf2b0857b26"
    tree = load(CONTROL / "inputs" / "n1-kanjivg-tree-70a0b7ae.json")
    assert tree["sha"] == snapshot["kanjivg"]["revision"] and not tree["truncated"]
    assert next(t for t in tree["tree"] if t["path"] == row["kanjivgInventory"]["path"]) == row["kanjivgInventory"]
    svg_path = CONTROL / "inputs" / "n1-051a0-70a0b7ae.svg"
    svg = svg_path.read_bytes()
    blob = hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest()
    assert blob == row["kanjivgInventory"]["sha"] and len(svg) == row["kanjivgInventory"]["size"]
    paths = ET.fromstring(svg).findall(".//{http://www.w3.org/2000/svg}path")
    assert len(paths) == row["metadata"]["strokes"] == 9
    assert [p.attrib["id"] for p in paths] == [f"kvg:051a0-s{i}" for i in range(1, 10)]
    converter_hash = digest((ROOT / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n"))
    assert converter_hash == snapshot["kanjivg"]["converter"]["normalizedSha256"]
    unicode_rows = (CONTROL / "inputs" / "n1-UnicodeData-17.0.0.txt").read_text(encoding="utf-8").splitlines()
    assert next(s for s in unicode_rows if s.startswith("2F0D;")).split(";")[5] == "<compat> 5196"
    stroke_record = {
        "revision": tree["sha"], "input": str(svg_path),
        "sourceUrl": "https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/kanji/051a0.svg",
        "gitBlob": blob, "sha256": digest(svg), "bytes": len(svg),
        "dictionaryStrokeCount": 9, "sourceStrokePaths": 9, "converted": False,
        "nativeDrawingAccepted": False, "converterNormalizedSha256": converter_hash,
        "limits": "Pinned whole SVG inspected; group/phon annotations are not historical-origin verification. Convert only with unchanged pinned converter later.",
    }
    save(OUT / "batch-079-stroke-evidence.json", stroke_record)
    text = data["proposedHanText"] + "".join(proposed_bodies.values())
    han = sorted({c for c in text if 0x2E80 <= ord(c) <= 0x2FDF
                  or 0x3400 <= ord(c) <= 0x9FFF or 0xF900 <= ord(c) <= 0xFAFF
                  or 0x20000 <= ord(c) <= 0x2FFFF})
    fonts = []
    for old in load(OUT / "batch-078-font-preparation.json")["fonts"]:
        path = Path(old["path"])
        assert digest(path.read_bytes()) == old["sha256"]
        with TTFont(path) as font:
            cmap = font.getBestCmap()
        fonts.append({"path": str(path), "sha256": old["sha256"],
                      "keyGlyphPresence": {c: ord(c) in cmap for c in "冠冖元寸冗完守王宀"},
                      "allProposedMissing": [c for c in han if ord(c) not in cmap]})
    rare = [c for c in han if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x4DBF
            or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF]
    font_record = {
        "schemaVersion": 1, "batch": BATCH, "inspectedArticleScope": list(proposed_bodies),
        "proposedTextInventory": data["proposedHanText"],
        "auditedHanCount": len(han), "auditedHan": han, "fonts": fonts,
        "rareHanRangeCharacters": rare,
        "mechanism": "Exact unchanged RareHan.kt and RareHanTest.kt read in dedicated f9b59a2; actual three bundled cmaps inspected.",
        "missingGlyphDispositions": {
            "冖": "Exact source radical14 U+5196; main cmaps absent and outside RareHan. Preserve exact glyph and inspect actual later supported-native fallback; no presumed failure.",
            "宀": "Exact contrasting radical40 U+5B80 in preserved existing冠 and王 text/完守 comparison. Main cmaps absent and outside RareHan; later native fallback inspection required, not a new unverified font claim.",
        },
        "limits": "Proposed terms plus complete affected-existing bodies only. Reinventory all actual runtime text after drafting. Cmap absence is not glyph failure. Native fallback/viewport/physical-phone acceptance remains pending.",
    }
    save(OUT / "batch-079-font-preparation.json", font_record)
    current_counts = {
        "kanji": len(all_meta), "words": len(list((ROOT / "words").glob("*.md"))),
        "n1Labelled": sum(m.get("jlpt") == 1 for m in all_meta),
        "namedSourceMembersPresent": len(actual_kanji & set(named)),
    }
    assert current_counts == {"kanji": 1090, "words": 5046, "n1Labelled": 110, "namedSourceMembersPresent": 109}
    result = {
        "schemaVersion": 1, "execution": EXECUTION, "batch": BATCH,
        "stage": "source-prepared-not-drafted", "baseCommit": BASE,
        "membership": [CHAR], "sourceRow": ROW, "frozenInputHashesVerified": 5,
        "decompressedDictionaryHashesVerified": 2, "exactFrozenNamedMembershipAndRowVerified": True,
        "packets": packets, "freshExactDictionaryExtractions": 3,
        "dictionaryFamilyOccurrences": 177, "distinctCompleteFamilies": len(families),
        "remainingLexicalDecisionEntryIds": remaining["lexical"],
        "remainingLexicalDecision": evidence["remainingLexicalDecision"],
        "allExtractedEntryIdsAccountedFor": True,
        "rawCharacterPacket": {"characters": 5, "sha256": digest(raw_bytes), "allRecordsAndHeaderVerified": True},
        "pinnedSvg": stroke_record, "fontPreparation": font_record,
        "authorInspection": data["authorInspection"],
        "inspectedArticleHashes": {n: digest((ROOT / n).read_bytes()) for n in data["authorInspection"]["completeExistingArticlesRead"]},
        "originalBaselineMetadataAndStrokesPreserved": counts,
        "baselineMetadataExceptions": exceptions, "baselineKanjiDistractorException": {"kanji/山.md": ["川", "出", "木"]},
        "runtimeManifestEqualToPublishedBase": True, "manifestBytesUnchanged": True,
        "allRuntimePayloadHashesVerified": checked, "contentVersion": manifest["contentVersion"],
        "exactPublishedAdditionMembershipVerified": len(additions),
        "allMappedCurrentlyCardableReciprocalPairsEnumerated": 3, "requiredDirectedLinks": 6,
        "activatedBaselinePairs": 1, "proposedNewWordArticles": 1,
        "currentCounts": current_counts, "runtimeChanges": 0, "reviewersLaunched": 0,
        "freshAndroidOrNativeClaimed": False, "publishedAdditions": 105, "remainingAdditions": 1123,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "limits": data["limits"],
    }
    save(OUT / "batch-079-preparation-audit.json", result)
    print(json.dumps({k: result[k] for k in ["membership", "distinctCompleteFamilies", "currentCounts",
                                            "allRuntimePayloadHashesVerified", "contentVersion", "runtimeChanges"]},
                     ensure_ascii=True, indent=2))
    print(json.dumps({"proposedHan": len(han), "cmapAbsences": [f["allProposedMissing"] for f in fonts],
                      "rareHan": rare}, ensure_ascii=True))


def record():
    data = load(OUT / "batch-079-preparation-audit.json")
    receipts = {}
    for name in ("source-tests-529.txt", "validate-529.txt", "manifest-529.txt", "budget-529.txt"):
        path = LOGS / name
        text = path.read_text(encoding="utf-8-sig")
        if name.startswith("source-tests"):
            assert "Ran 9 tests" in text and "OK" in text and "FAILED" not in text and "skipped" not in text
        elif name.startswith("validate"):
            assert "0 error(s)" in text
        elif name.startswith("manifest"):
            assert "8360" in text and "8e06edf2b0857b26" in text
        else:
            assert "ERROR" not in text and "8382" in text
        receipts[name] = {"path": str(path), "sha256": digest(path.read_bytes())}
    recipe = OUT / "batch-079-source-recipe.py"
    recipe.write_bytes(Path(__file__).read_bytes())
    starting = load(CONTROL / "progress.json")["execution529StartingState"]
    save(OUT / "execution-529.json", {
        "schemaVersion": 1, "execution": EXECUTION, "batch": BATCH, "baseCommit": BASE,
        "stage": "source-prepared-not-drafted", "startingState": starting,
        "sourceAudit": "batch-079-preparation-audit.json",
        "sourcePacket": "batch-079-progress.json", "sourceEvidence": "batch-079-source-evidence.json",
        "preparationRecipe": {"durableControlPath": str(Path(__file__)), "archive": recipe.name,
                              "sha256": digest(recipe.read_bytes()),
                              "limits": "Source checkpoint recipe only; later coordinators use committed packets/approved workspace inputs, not optional historical session recipes."},
        "checks": receipts, "runtimeChanges": 0, "runtimeDrafted": [],
        "reviewClosed": [], "published": [], "runtimePublished": False,
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 105, "remainingAdditions": 1123,
        "nextAction": "Same079 bounded runtime draft only, then signed LOCAL UNREVIEWED freeze and yield before reviewers or other later gates.",
        "limits": data["limits"],
    })
    print("Source recipe and execution evidence archived; ready for normal signed LOCAL source commit.")


def seal():
    progress = load(CONTROL / "progress.json")
    original = load(LOGS / "checkpoint-full-start.json")
    mutable = {"checkpoint", "status", "stage", "batch", "nextAction", "blocker"}
    assert all(progress[k] == v for k, v in original.items() if k not in mutable)
    assert progress["checkpoint"] == 528 and progress["batch"] == BATCH
    commit = git("rev-parse", "HEAD")
    assert commit != BASE and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    android = ROOT.parent / "kanji-cards-android"
    assert not subprocess.check_output(["git", "--no-pager", "status", "--porcelain"], cwd=android)
    changed = git("diff", BASE, "--name-only").splitlines()
    assert changed and all(p.startswith("docs/") for p in changed)
    assert git("rev-parse", "origin/main") == BASE
    assert (OUT / "batch-079-source-recipe.py").read_bytes() == Path(__file__).read_bytes()
    receipt = load(LOGS / "issue-receipt-529.json")
    body = (LOGS / "issue-update-529.txt").read_text(encoding="utf-8").strip()
    assert receipt["author"] == "stop-cran" and receipt["bodyVerified"]
    assert receipt["body"].replace("\r\n", "\n").strip() == body
    assert receipt["actualNewPermissionDenials"] == []
    audit_data = load(OUT / "batch-079-preparation-audit.json")
    next_action = (
        f"Batch079 source prepared at normally signed LOCAL {commit}; not pushed, drafted, reviewed or published. "
        "NEXT fresh coordinator: read entire request/final checkpoint/scoped live keys; preserve FULL history; verify dedicated clean signed heads and fresh main. "
        "Execute SAME079 bounded runtime draft ONLY: new冠 row88, preserve full/selectedカン andかんむり source order, linked existing冠かんむり N2 and ONE necessary new王冠おうかん with no inferred wordlevel. "
        "Use committed177completefamilies/5rawrecords/15existingarticles; own linked row per selectedreading, proposedかん/かんむり keys. "
        "Apply exact navigation-only reused冠 change and older王 reciprocal addition; preserve all metadata/examples/exclusions. "
        "Review actual王冠 royalcrown and crown-type bottlecap senses; proposed direct冠/帽子/蓋/栓 guards, not transitive cliques. "
        "Generate9strokes using unchanged pinnedconverter/canonical051a0SVG; audit baseline/membership/readings/threewrong冗完守choices/all3mappedpairs6directions/everyactualHan. "
        "Source35Han include冖/宀 absent allthree maincmaps outsideRareHan; later actualnativefallback required, not presumedfailure. "
        "Run validator/regeneratedmanifest and appropriate draft audits; normally signed LOCAL UNREVIEWED freeze, then checkpoint/yield. "
        "NO reviewers, Android/native, publication or080 in draft checkpoint. "
        "Use committed source packets/approved workspace inputs; durable helper control\\source-batch-079.py archived with packet. Optional historicalsession recipes NOT required; no deniedpath retry. "
        "Later gates unchanged: two serial blind different-family reviewers/serialinternaltools/boundedconfirmations/non-skippedAndroid/native/currentmain/normal signing/ownerfastforward/greenCI/EVERYimmutableZIPhash/originalbudgets. "
        "No unreviewedpush/authoragents/concurrentheavywork/secondrunner/signingretry/permissionworkaround. Preserve/report/yield on actualnewdenials. "
        "Published105/1228,remaining1123;1090kanji5046words110N1labels109namedmembers plus妖;104necessarysupports NOTN1vocabulary. "
        "Preserve accepted078 publication2a677750, all historical source/review/process/denial/OOM/lookup/readdepth/loadingtree limits and reviewed虎/猿/丘/山 plus冗談 exceptions; do not rerun acceptedheavywork absentnewconcern. "
        "HOST-only2GiBinit NEVER enters nativebuilds; no app/guestheap/archiveguard changes. CompatibleAndroidf9b59a2+ required; physicalphone/generalrelease/whole-set outstanding. Overallproject incomplete."
    )
    checkpoint = {
        "schemaVersion": 1, "execution": EXECUTION, "checkpoint": EXECUTION, "batch": BATCH,
        "savedCommit": commit, "signature": "G", "status": "continue",
        "stage": "source-prepared-not-drafted", "dedicatedWorktreesClean": True,
        "membership": [CHAR], "sourceRow": ROW, "distinctCompleteFamilies": 177,
        "dictionaryFamilyOccurrences": 177, "completeRawCharacterRecords": 5,
        "completeExistingArticlesRead": 15, "newNecessarySupportArticles": 1,
        "proposedAllMappedPairs": 3, "requiredDirectedLinks": 6,
        "pinnedSvgPaths": 9, "proposedHan": 35, "pendingNativeFallbackLabels": ["冖", "宀"],
        "focusedTestsPassed": 9, "validatorErrors": 0,
        "runtimeHashesUnchanged": audit_data["allRuntimePayloadHashesVerified"],
        "manifestBytesUnchanged": True, "contentVersion": audit_data["contentVersion"],
        "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "runtimeChanged": False, "runtimePublished": False,
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 105, "remainingAdditions": 1123, "lastPublishedCommit": BASE,
        "issueUpdate": receipt["url"], "ownerAuthorAndBodyVerified": True,
        "allOriginalHistoricalRootKeysPreservedExactly": True, "originalRootKeyCountCompared": len(original),
        "changedRootFields": [], "optionalHistoricalHelpersAccessed": False,
        "actualNewPermissionDenials": [], "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "nextBatchStarted": False, "nextAction": next_action,
        "verifiedAt": datetime.now().astimezone().isoformat(),
    }
    progress["execution529StartingState"]["status"] = "signed-local-source-preparation-checkpoint-complete"
    progress["execution529CoordinatorCheckpoint"] = checkpoint
    progress["execution529IssueReceipt"] = receipt
    progress["batch079Source"] = {
        "checkpoint": commit, "sourcePacket": "docs/n1-sources/batch-079-progress.json",
        "sourceAudit": "docs/n1-sources/batch-079-preparation-audit.json",
        "status": "source-prepared-not-drafted", "issueUpdate": receipt["url"],
        "runtimePublished": False,
    }
    progress.update(checkpoint=EXECUTION, status="continue", stage="batch-079-source-prepared-not-drafted",
                    batch=BATCH, nextAction=next_action, blocker=None)
    checkpoint["changedRootFields"] = sorted(k for k in mutable if progress[k] != original[k])
    assert all(progress[k] == v for k, v in original.items() if k not in mutable)
    save(CONTROL / "progress.json", progress)
    saved = load(CONTROL / "progress.json")
    assert all(saved[k] == v for k, v in original.items() if k not in mutable)
    save(LOGS / "checkpoint-529.json", checkpoint)
    print(json.dumps({"checkpoint": EXECUTION, "status": "continue", "batch": BATCH,
                      "savedCommit": commit, "signature": "G", "runtimeChanged": False,
                      "allOriginalHistoricalRootKeysPreserved": len(original),
                      "issueAuthorAndBodyVerified": receipt["url"]}, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    command = sys.argv[1]
    if command == "start":
        start()
    elif command == "packet":
        packet(sys.argv[2], sys.argv[3:])
    elif command == "raw":
        raw_records(sys.argv[2:])
    elif command == "audit":
        audit()
    elif command == "record":
        record()
    elif command == "seal":
        seal()
    else:
        raise ValueError(command)

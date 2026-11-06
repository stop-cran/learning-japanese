"""Prepare bounded batch078 source evidence without changing runtime content."""
import gzip
import hashlib
import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

ROOT = Path(r"C:\Users\stop-\n1-kanji-workspace\learning-japanese")
CONTROL = ROOT.parent / "control"
LOGS = CONTROL / "logs" / "1d7f840a-426f-4d3c-b5b8-f6f700dcaf6f"
OUT = ROOT / "docs" / "n1-sources"
BASE = "d7170f11e271a8de47bd2fd152e7196b96bff189"
sys.path.insert(0, str(ROOT / "tools"))
from extract_n1_jmdict import extract
from audit_n1_pilot import metadata
from audit_n1_pilot import offered_keys
from audit_n1_batch import lexical_pair
from build_manifest import build_manifest, sha256
from freeze_n1_sources import metadata_record
from fontTools.ttLib import TTFont


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def git(*args):
    return subprocess.check_output(
        ["git", "--no-pager", *args], cwd=ROOT, encoding="utf-8").strip()


def start():
    progress = load(CONTROL / "progress.json")
    assert progress["checkpoint"] == 520 and progress["batch"] == "077"
    assert progress["lastPublishedCommit"] == BASE and progress["remainingAdditions"] == 1124
    assert git("rev-parse", "HEAD") == git("rev-parse", "origin/main") == BASE
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    backup = LOGS / "checkpoint-full-start.json"
    assert not backup.exists()
    save(backup, progress)
    request = (LOGS / "request.txt").read_bytes()
    text = request.decode("utf-8-sig")
    marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
    request_checkpoint = json.loads(text.split(marker, 1)[1])
    assert request_checkpoint["execution520CoordinatorCheckpoint"]["checkpoint"] == 520
    progress["execution521StartingState"] = {
        "execution": 521, "batch": "078", "startingHead": BASE,
        "scope": "ONE source-preparation checkpoint for pending row87冗. No runtime draft, independent reviewer, Android/native, publication,079 or second runner.",
        "authorization": {
            "requestSha256": digest(request),
            "characters": len(text), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded and checkpoint parsed; operative contract, final520 and complete approved issue inspected directly. Historical middle loaded/parsed, not freshly semantically re-reviewed.",
        },
        "worktrees": "Dedicated worktrees clean; normally signed contentG equals fresh origin/main d7170f11; Android signedG f9b59a2. Canonical repositories not accessed.",
        "artifactPathPreflight": {
            "guide": str(CONTROL / "authoring-artifact-path-notes.txt"),
            "inputs": "Committed source packets and approved control inputs only.",
            "durableHelper": str(Path(__file__)),
            "optionalHistoricalHelpersAccessed": False,
            "newPermissionDenials": [],
        },
        "startedAt": datetime.now().astimezone().isoformat(),
    }
    progress.update(batch="078", stage="batch-078-source-preparation-in-progress",
                    status="continue", blocker=None,
                    nextAction="SAME078 source preparation only for pending row87冗; preserve full history and every later gate.")
    save(CONTROL / "progress.json", progress)
    print("Execution521 starting scope persisted; original full progress saved.")


def frozen():
    snapshot = load(ROOT / "docs" / "n1-source-snapshot.json")
    for name, info in snapshot["inputs"].items():
        assert digest((CONTROL / "inputs" / name).read_bytes()) == info["sha256"], name
    raw = (CONTROL / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    xml = gzip.decompress(raw)
    kd_xml = gzip.decompress((CONTROL / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes())
    assert digest(xml) == snapshot["jmdict"]["xmlSha256"]
    assert digest(kd_xml) == snapshot["kanjidic2"]["xmlSha256"]
    return snapshot, raw, ET.fromstring(xml), ET.fromstring(kd_xml)


def packet(kind, spellings=None):
    snapshot, raw, source, kd = frozen()
    row = next(r for r in load(OUT / "source-index.json") if r["sourceRow"] == 87)
    assert row["kanji"] == "冗" and not (ROOT / row["article"]).exists()
    requested = set(spellings or [])
    entries = [
        e for e in source.findall("entry")
        if (any("冗" in k.text for k in e.findall("k_ele/keb")) if kind == "lexical"
            else any(k.text in requested for k in e.findall("k_ele/keb"))
            or any(r.text in requested for r in e.findall("r_ele/reb")))
    ]
    ids = [e.findtext("ent_seq") for e in entries]
    selection = {
        "schemaVersion": 1, "batch": "078", "entryIds": ids,
        "sourceSnapshot": "docs/n1-source-snapshot.json",
        "selectionRule": (
            "Every complete frozen family containing 冗 in any keb; preserve all aliases, readings, restrictions and senses."
            if kind == "lexical" else
            "Every complete family matching an exact requested keb/reb; homographs retained, not substring or first-sense matching."
        ),
        "limits": "Extraction alone is not author inspection, frequency evidence or independent review.",
    }
    if kind != "lexical":
        selection["requestedSpellings"] = spellings
    save(OUT / f"batch-078-{kind}-selection.json", selection)
    suffix = "jmdict" if kind == "lexical" else f"{kind}-jmdict"
    path = OUT / f"batch-078-{suffix}.xml"
    data = extract(raw, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
    if path.exists():
        assert path.read_bytes() == data
    else:
        path.write_bytes(data)
    print(f"{kind}: {len(ids)} complete families / {len(data.splitlines())} XML lines.")
    if kind == "lexical":
        declared, aliases = [], []
        for path in sorted((ROOT / "words").glob("*.md")):
            name = path.relative_to(ROOT).as_posix()
            meta = metadata(ROOT, name)
            if "冗" in meta.get("kanji", []):
                declared.append({"article": name, "metadata": meta})
            if meta["reading"] in {"じょう", "じょうだん", "じょうちょう", "むだ", "よけい"}:
                aliases.append({"article": name, "metadata": meta})
        save(CONTROL / "batch-078-source-navigation.json", {
            "sourceIndexRecord": row, "declared": declared, "sameReading": aliases,
            "baselinePairs": [r for r in load(OUT / "baseline-word-candidates.json") if r["kanji"] == "冗"],
        })
        print(json.dumps({"row": row, "declared": declared, "sameReading": aliases}, ensure_ascii=False, indent=2))


def raw_records():
    snapshot, raw, source, kd = frozen()
    chars = ["冗", "談", "元", "兄", "見", "余"]
    records = {e.findtext("literal"): e for e in kd.findall("character")}
    selected = ET.Element("kanjidic2")
    selected.append(kd.find("header"))
    for char in chars:
        selected.append(records[char])
    ET.indent(selected, space="  ")
    data = ET.tostring(selected, encoding="utf-8", xml_declaration=True) + b"\n"
    (OUT / "batch-078-kanjidic2.xml").write_bytes(data)
    save(OUT / "batch-078-input-metadata.json", {
        "schemaVersion": 1, "batch": "078", "baseCommit": BASE,
        "sourceIndexRecord": next(r for r in load(OUT / "source-index.json") if r["sourceRow"] == 87),
        "rawCharacterPacket": "batch-078-kanjidic2.xml",
        "rawCharacterPacketSha256": digest(data), "characters": chars,
        "provenance": "Complete frozen KANJIDIC2 records/header reserialized without dropping fields.",
        "dictionaryAttribution": "Copyright James William Breen and EDRDG; CC BY-SA 4.0; repository NOTICE.",
    })
    print(f"Raw characters: {len(chars)} / {len(data.splitlines())} XML lines.")


def canonical(node):
    return ET.canonicalize(ET.tostring(node, encoding="unicode"), strip_text=True)


def audit():
    snapshot, raw, source, kd = frozen()
    data = load(OUT / "batch-078-progress.json")
    membership = load(OUT / "batch-078-membership.json")
    evidence = load(OUT / "batch-078-source-evidence.json")
    assert data["baseCommit"] == membership["baseCommit"] == BASE
    assert data["membership"] == membership["membership"] == ["冗"]
    assert data["drafted"] == data["reviewClosed"] == data["published"] == []
    assert data["status"] == "source-prepared-not-drafted"
    for name in ("kanji/冗.md", "strokes/冗.json", "words/冗長.md", "words/ジョーク.md"):
        assert not (ROOT / name).exists(), name
    row = next(r for r in load(OUT / "source-index.json") if r["sourceRow"] == 87)
    named = load(CONTROL / "inputs" / "n1-kanji-source-20261102.json")
    assert len(named) == len(set(named)) == 1232 and named[86] == row["kanji"] == "冗"
    assert load(OUT / "community-list-20261102.json") == named
    raw_meta = load(OUT / "batch-078-input-metadata.json")
    assert raw_meta["sourceIndexRecord"] == row
    assert data["sourceReadingOrder"] == {k: row["metadata"][k] for k in ("onyomi", "kunyomi")}
    assert row["metadata"]["radical"] == "冖" and row["metadata"]["radicalNumber"] == 14
    unicode_lines = (CONTROL / "inputs" / "n1-UnicodeData-17.0.0.txt").read_text(encoding="utf-8").splitlines()
    radical_line = next(line for line in unicode_lines if line.startswith("2F0D;")).split(";")
    assert radical_line[5] == "<compat> 5196"
    assert [(r["kind"], r["reading"], r["proposedQuizSelection"], r["selected"])
            for r in data["readingDispositions"]] == [("on", "ジョウ", True, False)]
    projection = data["proposedCuratedProjection"]
    assert projection["quizOnyomi"] == ["ジョウ"] and projection["quizKunyomi"] == []
    assert offered_keys(projection["quizOnyomi"]) == projection["onKeys"] == ["じょう"]
    assert offered_keys(projection["quizKunyomi"]) == projection["kunKeys"] == []
    families, packets = {}, []
    decisions = dict(lexical="lexicalDecisions", comparison="comparisonDecisions", related="relatedDecisions")
    for kind in decisions:
        selection = load(OUT / f"batch-078-{kind}-selection.json")
        requested = set(selection.get("requestedSpellings", []))
        expected = [
            e.findtext("ent_seq") for e in source.findall("entry")
            if (any("冗" in k.text for k in e.findall("k_ele/keb")) if kind == "lexical"
                else any(k.text in requested for k in e.findall("k_ele/keb"))
                or any(r.text in requested for r in e.findall("r_ele/reb")))
        ]
        assert selection["entryIds"] == expected
        suffix = "jmdict" if kind == "lexical" else f"{kind}-jmdict"
        path = OUT / f"batch-078-{suffix}.xml"
        packet_bytes = path.read_bytes()
        assert packet_bytes == extract(raw, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], expected)
        accounted = [i for group in evidence[decisions[kind]] for i in group["entryIds"]]
        assert len(accounted) == len(set(accounted)) and set(accounted) == set(expected), kind
        entries = ET.fromstring(packet_bytes).findall("entry")
        families.update((e.findtext("ent_seq"), e) for e in entries)
        packets.append({"path": path.name, "families": len(entries),
                        "lines": len(packet_bytes.splitlines()), "sha256": digest(packet_bytes)})
    assert [p["families"] for p in packets] == [47, 26, 6]
    assert len(families) == data["authorInspection"]["distinctCompleteFamilies"] == 78
    assert sum(p["families"] for p in packets) == 79
    for mapping in data["proposedSupportMapping"]:
        assert lexical_pair(families[mapping["entryId"]], mapping["word"], mapping["primaryReading"])
        assert not mapping["newArticleNecessary"]
        meta = metadata(ROOT, mapping["article"])
        assert meta["reading"] == mapping["primaryReading"] and meta["word"] == mapping["word"]
        assert meta["kanji"] == mapping["allWrittenKanji"] and meta["jlpt"] == mapping["preservedWordJlpt"] == 3
    jodan = families["1355540"]
    assert [e.findtext("keb") for e in jodan.findall("k_ele")] == ["冗談", "戯談", "串戯"]
    assert all(e.findtext("ke_inf") == "search-only kanji form" for e in jodan.findall("k_ele")[1:])
    assert "joke" in [g.text for g in families["1136850"].findall("sense/gloss")]
    assert metadata(ROOT, "words/ユーモア.md")["title"] == "humor"
    assert "冗談" in metadata(ROOT, "words/洒落.md")["quiz_exclusions"]
    assert "冗談" in metadata(ROOT, "words/ふざける.md")["quiz_exclusions"]
    assert "ユーモア" in metadata(ROOT, "words/洒落.md")["quiz_exclusions"]
    assert "ユーモア" not in metadata(ROOT, "words/冗談.md").get("quiz_exclusions", [])
    assert "冗談" not in metadata(ROOT, "words/ユーモア.md").get("quiz_exclusions", [])
    raw_records_by_char = {e.findtext("literal"): e for e in kd.findall("character")}
    assert metadata_record(raw_records_by_char["冗"], {14: "冖"}) == row["metadata"]
    kd_bytes = (OUT / "batch-078-kanjidic2.xml").read_bytes()
    selected = ET.fromstring(kd_bytes)
    assert [e.findtext("literal") for e in selected.findall("character")] == raw_meta["characters"]
    assert canonical(selected.find("header")) == canonical(kd.find("header"))
    assert all(canonical(e) == canonical(raw_records_by_char[e.findtext("literal")])
               for e in selected.findall("character"))
    assert raw_meta["rawCharacterPacketSha256"] == digest(kd_bytes)
    raw_readings = raw_records_by_char["冗"].findall("reading_meaning/rmgroup/reading")
    assert [r.text for r in raw_readings if r.get("r_type") == "ja_on"] == ["ジョウ"]
    assert not [r for r in raw_readings if r.get("r_type") == "ja_kun"]
    assert [r.text for r in raw_records_by_char["談"].findall("reading_meaning/rmgroup/reading")
            if r.get("r_type") == "ja_on"] == ["ダン"]
    declared = [f"words/{p.name}" for p in sorted((ROOT / "words").glob("*.md"))
                if "冗" in metadata(ROOT, f"words/{p.name}").get("kanji", [])]
    assert declared == data["currentDeclaredWordPairs"] == ["words/冗談.md"]
    baseline_pairs = [r for r in load(OUT / "baseline-word-candidates.json") if r["kanji"] == "冗"]
    assert len(baseline_pairs) == 1 and baseline_pairs[0]["article"] == declared[0]
    pairs = [tuple(p) for p in data["proposedReciprocalPairs"]]
    available = {(c, m["article"]) for m in data["proposedSupportMapping"]
                 for c in m["allWrittenKanji"] if c == "冗" or (ROOT / "kanji" / f"{c}.md").exists()}
    assert set(pairs) == available and len(pairs) == len(set(pairs)) == 2
    directed = data["proposedDirectedLinkPlan"]
    assert len(directed) == 4
    assert {(p["from"], p["to"]) for p in directed} == {
        (a, b) for c, article in pairs
        for a, b in [(f"kanji/{c}.md", article), (article, f"kanji/{c}.md")]}
    proposed_bodies = {}
    for change in data["proposedChangedReusedPassages"]:
        text = proposed_bodies.get(change["article"], (ROOT / change["article"]).read_text(encoding="utf-8"))
        assert text.count(change["before"]) == 1 and change["after"] not in text, change["article"]
        proposed_bodies[change["article"]] = text.replace(change["before"], change["after"], 1)
    for direction in directed:
        if (ROOT / direction["from"]).exists():
            text = (ROOT / direction["from"]).read_text(encoding="utf-8")
            assert (f"(../{direction['to']})" in text) == (direction["status"] == "already-present")
            if direction["status"] != "already-present":
                assert f"(../{direction['to']})" in proposed_bodies[direction["from"]]
    import yaml
    for name, text in proposed_bodies.items():
        before = metadata(ROOT, name)
        after = yaml.safe_load(text.split("---", 2)[1])
        if name == "words/冗談.md":
            before["quiz_exclusions"] = ["ユーモア"]
        assert before == after, name
    all_meta = [metadata(ROOT, f"kanji/{p.name}") for p in (ROOT / "kanji").glob("*.md")]
    quiz = data["proposedKanjiQuizAudit"]
    assert quiz["title"] not in [m["title"] for m in all_meta]
    assert len(quiz["distractors"]) == len({r["kanji"] for r in quiz["distractors"]}) == 3
    for choice in quiz["distractors"]:
        assert metadata(ROOT, f"kanji/{choice['kanji']}.md")["title"] == choice["title"]
    assert len(set(metadata(ROOT, "kanji/余.md")["distractors"])) == 3
    exceptions = {"words/虎.md": ["酔っ払い"], "words/猿.md": ["馬鹿"], "words/丘.md": ["坂", "山"]}
    counts = {"kanji": 0, "words": 0, "strokes": 0}
    baseline = load(OUT / "baseline-inventory.json")
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
            assert digest((ROOT / name).read_bytes()) == item["sha256"], name
            counts[kind] += 1
    assert counts == {"kanji": 985, "words": 4942, "strokes": 985}
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
    assert checked == 8358 and manifest["contentVersion"] == "2944928c13e2165a"
    baseline_kanji = {Path(n).stem for n in baseline["files"] if n.startswith("kanji/")}
    actual_kanji = {p.stem for p in (ROOT / "kanji").glob("*.md")}
    additions = actual_kanji - baseline_kanji
    accepted = set("幹氏扱乃凹凸矛鷹彗漱栞莉")
    for path in OUT.glob("batch-*-progress.json"):
        accepted.update(load(path).get("published", []))
    assert additions == accepted and len(additions) == 104 and additions <= set(named)
    assert metadata(ROOT, "kanji/妖.md")["jlpt"] == 1
    tree = load(CONTROL / "inputs" / "n1-kanjivg-tree-70a0b7ae.json")
    assert tree["sha"] == snapshot["kanjivg"]["revision"] and not tree["truncated"]
    assert next(t for t in tree["tree"] if t["path"] == row["kanjivgInventory"]["path"]) == row["kanjivgInventory"]
    svg_path = CONTROL / "inputs" / "n1-05197-70a0b7ae.svg"
    svg = svg_path.read_bytes()
    blob = hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest()
    assert blob == row["kanjivgInventory"]["sha"] and len(svg) == row["kanjivgInventory"]["size"]
    paths = ET.fromstring(svg).findall(".//{http://www.w3.org/2000/svg}path")
    assert len(paths) == row["metadata"]["strokes"] == 4
    assert [p.attrib["id"] for p in paths] == [f"kvg:05197-s{i}" for i in range(1, 5)]
    converter_hash = digest((ROOT / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n"))
    assert converter_hash == snapshot["kanjivg"]["converter"]["normalizedSha256"]
    stroke_record = {
        "revision": snapshot["kanjivg"]["revision"], "input": str(svg_path),
        "sourceUrl": "https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/kanji/05197.svg",
        "gitBlob": blob, "sha256": digest(svg), "bytes": len(svg),
        "dictionaryStrokeCount": 4, "sourceStrokePaths": 4,
        "converted": False, "nativeDrawingAccepted": False,
        "limits": "Whole source SVG inspected. Geometric group annotations are not historical-origin or phonetic evidence. Convert later only with pinned existing tools/generate_strokes.py.",
    }
    save(OUT / "batch-078-stroke-evidence.json", stroke_record)
    text = data["proposedHanText"] + "".join(proposed_bodies.values())
    han = sorted({c for c in text if 0x2E80 <= ord(c) <= 0x2FDF
                  or 0x3400 <= ord(c) <= 0x9FFF or 0xF900 <= ord(c) <= 0xFAFF
                  or 0x20000 <= ord(c) <= 0x2FFFF})
    fonts = []
    for old in load(OUT / "batch-077-font-preparation.json")["fonts"]:
        path = Path(old["path"])
        assert digest(path.read_bytes()) == old["sha256"]
        with TTFont(path) as font:
            cmap = font.getBestCmap()
        fonts.append({"path": str(path), "sha256": old["sha256"],
                      "keyGlyphPresence": {c: ord(c) in cmap for c in "冗冖几元兄見談"},
                      "allProposedMissing": [c for c in han if ord(c) not in cmap]})
    rare_han = [c for c in han if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x4DBF
                or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF]
    assert all(f["allProposedMissing"] == ["冖", "几"] for f in fonts)
    assert rare_han == []
    font_record = {
        "schemaVersion": 1, "batch": "078", "inspectedArticleScope": list(proposed_bodies),
        "proposedTextInventory": data["proposedHanText"],
        "auditedHanCount": len(han), "auditedHan": han, "fonts": fonts,
        "rareHanRangeCharacters": rare_han,
        "mechanism": "Exact unchanged RareHan.kt and RareHanTest.kt read in dedicated Android f9b59a2; all three actual bundled cmaps inspected, not inferred.",
        "missingGlyphDispositions": {
            "冖": "Exact source classical radical14 U+5196. Main cmaps absent and outside RareHan ranges; inspect actual later supported-native fallback. Not 宀 or a compatibility radical replacement; absence is not failure.",
            "几": "Exact visible lower-shape label U+51E0. Main cmaps absent and outside RareHan ranges; inspect actual later article fallback. No source-origin claim or presumed glyph failure.",
        },
        "limits": "Proposed-text and complete affected-existing-text inventory only. Reinventory every Han in the eventual complete runtime draft; no native glyph/typeface/viewport or physical-phone acceptance.",
    }
    save(OUT / "batch-078-font-preparation.json", font_record)
    current_counts = {
        "kanji": len(all_meta), "words": len(list((ROOT / "words").glob("*.md"))),
        "n1Labelled": sum(m.get("jlpt") == 1 for m in all_meta),
        "namedSourceMembersPresent": len(actual_kanji & set(named)),
    }
    assert current_counts == {"kanji": 1089, "words": 5046, "n1Labelled": 109, "namedSourceMembersPresent": 108}
    result = {
        "schemaVersion": 1, "execution": 521, "batch": "078", "stage": "source-prepared-not-drafted",
        "baseCommit": BASE, "membership": ["冗"], "sourceRow": 87,
        "frozenInputHashesVerified": 5, "decompressedDictionaryHashesVerified": 2,
        "exactFrozenNamedMembershipAndRowVerified": True, "exactFrozenKanjiVGInventoryRecordVerified": True,
        "freshExactDictionaryExtractions": 3, "packets": packets,
        "dictionaryFamilyOccurrences": 79, "distinctCompleteFamilies": len(families),
        "rawCharacterPacket": {"path": "batch-078-kanjidic2.xml", "characters": 6, "sha256": digest(kd_bytes)},
        "pinnedSvg": stroke_record, "converterNormalizedSha256": converter_hash,
        "fontPreparation": font_record, "authorInspection": data["authorInspection"],
        "inspectedArticleHashes": {n: digest((ROOT / n).read_bytes()) for n in data["authorInspection"]["completeExistingArticlesRead"]},
        "originalBaselineMetadataAndStrokesPreserved": counts,
        "baselineMetadataExceptions": exceptions, "baselineKanjiDistractorException": {"kanji/山.md": ["川", "出", "木"]},
        "runtimeManifestEqualToPublishedBase": True, "manifestFresh": True,
        "allRuntimePayloadHashesVerified": checked, "contentVersion": manifest["contentVersion"],
        "exactPublishedAdditionMembershipVerified": len(additions),
        "allMappedCurrentlyCardableReciprocalPairsEnumerated": 2, "requiredDirectedLinks": 4,
        "alreadyPresentDirectedLinks": 1, "proposedNewDirectedLinks": 3,
        "proposedNewWordArticles": 0, "proposedAdditiveDirectWordGuards": [["冗談", "ユーモア"]],
        "currentCounts": current_counts, "runtimeChanges": 0, "reviewersLaunched": 0,
        "freshAndroidOrNativeClaimed": False, "publishedAdditions": 104, "remainingAdditions": 1124,
        "limits": data["limits"],
    }
    save(OUT / "batch-078-preparation-audit.json", result)
    print(json.dumps({k: result[k] for k in ["membership", "distinctCompleteFamilies", "currentCounts",
                                            "allRuntimePayloadHashesVerified", "contentVersion", "runtimeChanges"]},
                     ensure_ascii=False, indent=2))
    print(f"Font preparation: {len(han)} Han; two missing main-cmap labels: 冖/几; rare-range inventory {rare_han}")


def record():
    audit_data = load(OUT / "batch-078-preparation-audit.json")
    receipts = {}
    for name in ("source-tests-521.txt", "validate-521.txt", "manifest-521.txt", "budget-521.txt"):
        path = LOGS / name
        text = path.read_text(encoding="utf-8-sig")
        if name.startswith("source-tests"):
            assert "Ran 9 tests" in text and "OK" in text and "FAILED" not in text and "skipped" not in text
        elif name.startswith("validate"):
            assert "0 error(s)" in text
        elif name.startswith("manifest"):
            assert "8358" in text and "2944928c13e2165a" in text
        else:
            assert all(str(n) in text for n in (8380, 44134674, 44403012))
            assert "ERROR" not in text
        receipts[name] = {"path": str(path), "sha256": digest(path.read_bytes())}
    recipe = OUT / "batch-078-source-recipe.py"
    recipe.write_bytes(Path(__file__).read_bytes())
    progress = load(CONTROL / "progress.json")
    start_state = progress["execution521StartingState"]
    execution = {
        "schemaVersion": 1, "execution": 521, "batch": "078",
        "stage": "source-prepared-not-drafted", "baseCommit": BASE,
        "androidCommit": "f9b59a2bc5a203c6b4de26be50021a4c720dc22c",
        "startingWorktrees": start_state["worktrees"],
        "authorization": start_state["authorization"],
        "artifactPathPreflight": start_state["artifactPathPreflight"],
        "scope": start_state["scope"],
        "membership": ["冗"], "sourceRow": 87,
        "sourcePacket": "batch-078-progress.json", "sourceAudit": "batch-078-preparation-audit.json",
        "sourceEvidence": "batch-078-source-evidence.json",
        "preparationRecipe": {
            "durableControlPath": str(Path(__file__)),
            "archive": recipe.name, "sha256": digest(recipe.read_bytes()),
            "limits": "Checkpoint-specific generated-evidence recipe, not runtime tooling or linguistic certification. Subsequent coordinators use committed packets/approved inputs; no optional historical session helper is required.",
        },
        "sourcePreparation": {
            "fiveFrozenInputHashesVerified": True, "twoDecompressedDictionaryHashesVerified": True,
            "distinctCompleteFamilies": 78, "dictionaryFamilyOccurrences": 79,
            "completeRawCharacterRecords": 6, "completeExistingArticlesRead": 11,
            "reusedSupport": "冗談じょうだん, N3 word metadata and examples preserved",
            "newNecessarySupportArticles": 0, "sourceReadings": {"on": ["ジョウ"], "kun": []},
            "proposedOnKeys": ["じょう"], "proposedKunKeys": [],
            "allMappedPairs": 2, "directedLinks": 4, "alreadyPresentDirections": 1,
            "proposedAdditiveDirectGuard": ["冗談", "ユーモア"],
            "pinnedSvgPaths": 4, "geometryConverted": False,
            "proposedAffectedHan": audit_data["fontPreparation"]["auditedHanCount"],
            "mainCmapAbsences": ["冖", "几"],
            "fontAcceptance": "Pending native/visual inspection; cmap absence is not glyph failure.",
        },
        "checks": [
            "Exact source87 membership, all raw metadata/order, Unicode radical mapping and canonical SVG Git blob/hash/four paths verified.",
            "Three selected complete-family packets freshly reproduce byte-for-byte; every family has an explicit source decision.",
            "All original baseline kanji/word metadata and985 stroke hashes preserved, except unchanged previously reviewed 虎/猿/丘/山 safeguards.",
            "Actual current and immutable baseline declare one 冗 word pair; exact primaryじょうだん/restrictions/selected sense inspected. Zero new words are necessary.",
            "Sole reading disposition and proposed normalizedじょう key mirror the pinned production helper. Source-only kun additions are not invented.",
            "Both all-mapped pairs/four directions and exact two-article reuse plan checked; only one proposed additive direct quiz safeguard, no metadata/level rewrite.",
            "Complete affected reused text plus proposed Han inventory:29 Han; three actual font cmaps inspected; exact 冖/几 absence outside RareHan ranges remains pending native evidence.",
            "Nine focused source-tool unittest cases passed; zero failures/skips. Validator zero errors.",
            "Manifest regenerated and exactly equal to published base bytes/contentVersion; all8358 runtime hashes unchanged.",
            "Existing archive budget check passes:8380 entries,44134674 retained,44403012 inflated bytes. This is a local budget check, not a new immutable public ZIP verification.",
            "All changes confined to contributor documentation; no runtime/tool/app changes, review launch, native run or publication.",
        ],
        "receipts": receipts,
        "diagnosticsPreserved": [
            "Speculative direct views found absent 凡/穴/無/駄/剰 cards. Missing paths are not permission denials; none becomes a supposed existing distractor or required support.",
            "The Windows-style glob did not locate RareHanTest; a scoped content search located and returned the actual existing test. No policy/path workaround or broad filesystem search.",
            "Long mixed Weblio 冗長 extraction did not establish inspection of a Daijisen entry; excluded as such and preserved in the source evidence lookup limits.",
        ],
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "publishedAdditions": 104, "remainingAdditions": 1124,
        "compatibleClient": "Android f9b59a2 or later",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "nextAction": load(OUT / "batch-078-progress.json")["nextAction"],
        "limits": "Source proposals/coordinator inspection only. No078 runtime draft, independent review, rendering/drawing acceptance or delivery. Historical source/review/process/permission/OOM/phone limitations and all original guards remain unchanged.",
    }
    save(OUT / "execution-521.json", execution)
    print("Execution521 source record and exact durable-helper archive saved.")


def checkpoint(commit, issue_url):
    progress = load(CONTROL / "progress.json")
    original = load(LOGS / "checkpoint-full-start.json")
    assert progress["checkpoint"] == 520 and progress["batch"] == "078"
    assert git("rev-parse", "HEAD") == commit and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert git("rev-parse", "origin/main") == BASE
    assert load(OUT / "batch-078-progress.json")["drafted"] == []
    assert not git("diff", BASE, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    next_action = (
        f"Batch078 source prepared at normally signed LOCAL {commit}; not pushed, drafted, reviewed or published. "
        "NEXT fresh coordinator: read entire request/final checkpoint/scoped live keys and preserve FULL history; verify dedicated clean signed heads and fresh main. "
        "Execute SAME078 bounded runtime draft ONLY from committed packet: new冗 row87, sole full/selectedジョウ and emptykun, linked existing冗談じょうだん N3; ZERO new word articles. "
        "Apply exact 冗談 component link plus conservative additive directユーモア guard and older談 reciprocal link; preserve all other metadata/examples/exclusions. "
        "Generate four-stroke geometry using unchanged pinned converter/canonicalSVG; audit baseline/membership/oneofferedじょうkey/threewrong元兄見choices/twomappedpairsfourdirections/everyactualHan. "
        "Exact冖/几 absent allthree maincmaps outsideRareHan needs laternativefallback inspection, not presumedfailure. "
        "Run validator/regeneratedmanifest and appropriate source/draft checks; normal signed LOCAL UNREVIEWED freeze, then checkpoint/yield. "
        "NO reviewers, Android/native, publication or079 in that draft checkpoint. "
        "Use committed source packets and approved controlinputs; reusable helper is control\\source-batch-078.py and committed batch-078-source-recipe.py archive; optional historical session-state recipes are NOT required evidence. "
        "Later stages retain two serial blind different-family reviewers/serialinternaltools/boundedconfirmations/non-skippedAndroid/native/currentmain/normal signing/ownerfastforward/greenCI/EVERYimmutableZIPhash/originalbudgets. "
        "No unreviewedpush/authoragents/concurrentheavywork/secondrunner/signingretry/permissionworkaround. Preserve/report/yield on actualnewdenials. "
        "Published104/1228,remaining1124;1089kanji5046words109N1labels108namedmembers plus妖;104necessarysupports NOTN1vocabulary. "
        "077 published d7170f11 and all prior accepted evidence/limitations remain; no redundant heavy rechecks absent new concern. "
        "CompatibleAndroidf9b59a2+ required; physicalphone/generalrelease/whole-set outstanding. Overallproject incomplete."
    )
    progress.update(checkpoint=521, status="continue", stage="batch-078-source-prepared-not-drafted",
                    batch="078", nextAction=next_action, blocker=None)
    progress["batch078Source"] = {
        "membership": ["冗"], "sourceRow": 87, "baseCommit": BASE, "sourceCommit": commit,
        "sourcePacket": "docs/n1-sources/batch-078-progress.json",
        "sourceAudit": "docs/n1-sources/batch-078-preparation-audit.json",
        "sourceEvidence": "docs/n1-sources/batch-078-source-evidence.json",
        "executionEvidence": "docs/n1-sources/execution-521.json",
        "status": "source-prepared-not-drafted", "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "durableHelper": str(Path(__file__)), "issueUpdate": issue_url,
    }
    mutable = {"checkpoint", "status", "stage", "batch", "nextAction", "blocker"}
    assert all(progress[k] == value for k, value in original.items() if k not in mutable)
    progress["execution521CoordinatorCheckpoint"] = {
        "schemaVersion": 1, "execution": 521, "checkpoint": 521, "batch": "078",
        "savedCommit": commit, "signature": "G", "status": "continue",
        "stage": "source-prepared-not-drafted", "dedicatedWorktreesClean": True,
        "membership": ["冗"], "sourceRow": 87, "distinctCompleteFamilies": 78,
        "dictionaryFamilyOccurrences": 79, "completeRawCharacterRecords": 6,
        "completeExistingArticlesRead": 11, "newNecessarySupportArticles": 0,
        "proposedAllMappedPairs": 2, "requiredDirectedLinks": 4,
        "pinnedSvgPaths": 4, "proposedHan": 29, "pendingNativeFallbackLabels": ["冖", "几"],
        "focusedTestsPassed": 9, "validatorErrors": 0,
        "runtimeHashesUnchanged": 8358, "manifestBytesUnchanged": True,
        "contentVersion": "2944928c13e2165a",
        "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "runtimeChanged": False, "runtimePublished": False,
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 104, "remainingAdditions": 1124, "lastPublishedCommit": BASE,
        "issueUpdate": issue_url, "ownerAuthorAndBodyVerified": True,
        "allOriginalHistoricalRootKeysPreservedExactly": True,
        "originalRootKeyCountCompared": len(original),
        "changedRootFields": sorted(mutable),
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "nextAction": next_action, "verifiedAt": datetime.now().astimezone().isoformat(),
    }
    save(CONTROL / "progress.json", progress)
    saved = load(CONTROL / "progress.json")
    assert all(saved[k] == value for k, value in original.items() if k not in mutable)
    save(LOGS / "checkpoint-521.json", saved["execution521CoordinatorCheckpoint"])
    print(f"Checkpoint521 persisted; {len(original)} original root keys compared; all historical values preserved.")


if __name__ == "__main__":
    if sys.argv[1] == "start":
        start()
    elif sys.argv[1] == "lexical":
        packet("lexical")
    elif sys.argv[1] == "comparison":
        packet("comparison", sys.argv[2:])
    elif sys.argv[1] == "related":
        packet("related", ["ふざける", "洒落", "ユーモア", "ジョーク"])
    elif sys.argv[1] == "raw":
        raw_records()
    elif sys.argv[1] == "audit":
        audit()
    elif sys.argv[1] == "record":
        record()
    elif sys.argv[1] == "checkpoint":
        checkpoint(sys.argv[2], sys.argv[3])
    else:
        raise ValueError(f"Unknown operation: {sys.argv[1]}")

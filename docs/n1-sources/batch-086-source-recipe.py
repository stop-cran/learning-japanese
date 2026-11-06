"""Prepare and checkpoint one frozen source member; never write runtime content."""
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
L = C / "logs" / "6a2f924a-5020-4d8d-b22b-dacfcc3b9042"
BASE = "f001846c194b20b13b9deb797d70e04a34025d93"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
CHAR = "\u51e1"
PREFIX = "batch-086-"
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata, offered_keys
from build_manifest import build_manifest
from extract_n1_jmdict import extract


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    temporary = path.with_suffix(path.suffix + ".600.tmp")
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
    assert (p["checkpoint"], p["batch"], p["status"]) == (599, "085", "continue")
    assert p["lastPublishedCommit"] == BASE and p["remainingAdditions"] == 1116
    assert not list(S.glob(PREFIX + "*"))
    before = L / "progress-before-600.json"
    assert not before.exists()
    shutil.copyfile(C / "progress.json", before)
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
    assert json.loads(text.split(marker, 1)[1])["checkpoint"] == 599
    runner = load(C / "runner.json")
    assert runner["pid"] == 19008 and runner["status"] == "running"
    assert runner["sessionId"] == L.name
    state = {
        "execution": 600, "batch": "086", "startingHead": BASE, "freshOriginMain": BASE,
        "androidHead": APP, "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "ONE bounded086 source-preparation checkpoint only; no runtime draft, reviewer, Android/native, publication,087 or second runner.",
        "request": {"sha256": sha(raw), "bytes": len(raw), "characters": len(text),
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded and embedded checkpoint decoded. Operative contract, approved issue and final599 inspected directly; historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": "Win32_Process verified current coordinator30448 parent19008 and child5900. runner.json identifies live parent19008 and exact session. Parent retains runner.lock; child never acquires/deletes/unlocks it.",
        "artifactPathPreflight": {"durableHelper": str(Path(__file__)),
                                  "priorArt": "Committed batch-085-source-recipe.py and extract/freeze/audit tools; approved frozen workspace inputs only.",
                                  "optionalHistoricalSessionHelpersAccessed": False},
        "actualNewPermissionDenials": [],
        "worktrees": "Wholly clean dedicated content and qualified TESTONLY Android; normal signatures G. Fresh origin/main equals content. Android1c1b7bf4 is atop unchanged productionf9b59a2, not latest app main. Canonical repositories not accessed.",
    }
    p["execution600StartingState"] = state
    p.update(batch="086", stage="batch-086-source-preparation-in-progress",
             nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    print("Starting scope persisted with full live history.")


def packet():
    assert load(C / "progress.json")["batch"] == "086"
    snapshot, inputs, jm, kd = frozen()
    row = next(r for r in load(S / "source-index.json") if r["kanji"] == CHAR)
    assert row["sourceRow"] == 95
    assert json.loads(inputs["n1-kanji-source-20261102.json"])[94] == CHAR
    assert not (R / row["article"]).exists() and not (R / row["strokeFile"]).exists()
    ids = [e.findtext("ent_seq") for e in jm.findall("entry")
           if any(CHAR in k.text for k in e.findall("k_ele/keb"))]
    selection = {
        "schemaVersion": 1, "batch": "086", "entryIds": ids,
        "sourceSnapshot": "docs/n1-source-snapshot.json",
        "selectionRule": "Every complete frozen family containing exact source member U+51E1 in any keb; preserve all aliases/readings/restrictions/senses.",
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
        "schemaVersion": 1, "batch": "086", "baseCommit": BASE, "sourceIndexRecord": row,
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
    save(C / "batch-086-source-navigation.json", {
        "sourceIndexRecord": row, "candidates": candidates,
        "baselinePairs": [r for r in load(S / "baseline-word-candidates.json") if r["kanji"] == CHAR],
    })
    print(json.dumps({"families": len(ids), "lines": len(raw.splitlines()),
                      "candidates": candidates}, ensure_ascii=True, indent=2))


def comparison():
    snapshot, inputs, jm, kd = frozen()
    words = ["\u4e38", "\u4e5d", "\u51f9", "\u4f8b", "\u8aac\u660e",
             "\u89e3\u8aac", "\u6ce8", "\u5224\u4f8b"]
    ids = [e.findtext("ent_seq") for e in jm.findall("entry")
           if any(k.text in words for k in e.findall("k_ele/keb"))]
    save(S / (PREFIX + "comparison-selection.json"), {
        "schemaVersion": 1, "batch": "086", "exactSpellings": words, "entryIds": ids,
        "rule": "Complete frozen families with any exact keb matching one of the recorded comparison spellings; no substring allocation.",
        "limits": "Bounded navigation packet, not an exhaustive quiz audit or linguistic acceptance.",
    })
    raw = extract(inputs["n1-implementation-JMdict_e.gz"],
                  snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
    (S / (PREFIX + "comparison-jmdict.xml")).write_bytes(raw)
    chars = "\u5e73\u4f8b\u4e38\u4e5d\u51f9\u5168"
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
    assert len(named) == len(set(named)) == 1232 and named[94] == CHAR
    canonical = lambda e: ET.canonicalize(ET.tostring(e, encoding="unicode"), strip_text=True)
    character = next(e for e in kd.findall("character") if e.findtext("literal") == CHAR)
    assert metadata_record(character, {16: "\u51e0"}) == row["metadata"]
    for name, chars in [("kanjidic2.xml", CHAR),
                        ("comparison-kanjidic2.xml", "\u5e73\u4f8b\u4e38\u4e5d\u51f9\u5168")]:
        packet = ET.parse(S / (PREFIX + name)).getroot()
        assert canonical(packet.find("header")) == canonical(kd.find("header"))
        assert [e.findtext("literal") for e in packet.findall("character")] == list(chars)
        for e in packet.findall("character"):
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
    assert len(exact_ids) == 49 and len(comparison_ids) == 12
    for stem, ids in [("", exact_ids), ("comparison-", comparison_ids)]:
        selected_ids = (comparison_selection["entryIds"] if stem
                        else load(S / (PREFIX + "lexical-selection.json"))["entryIds"])
        assert ids == selected_ids
        raw = (S / (PREFIX + stem + "jmdict.xml")).read_bytes()
        assert raw == extract(inputs["n1-implementation-JMdict_e.gz"],
                              snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
    groups = evidence["lexicalDecisions"][:5]
    explicit = [i for group in groups for i in group["entryIds"]]
    assert len(explicit) == len(set(explicit)) and set(explicit) <= set(exact_ids)
    remaining = [i for i in exact_ids if i not in explicit]
    evidence["lexicalDecisions"] = groups + [{
        "entryIds": remaining, "disposition": evidence["remainingFamilyDisposition"],
    }]
    all_ids = [i for group in evidence["lexicalDecisions"] for i in group["entryIds"]]
    assert len(all_ids) == len(set(all_ids)) == 49 and set(all_ids) == set(exact_ids)
    evidence["familyCounts"] = {"allExactMemberFamilies": 49, "individuallyGroupedFamilies": len(explicit),
                                "otherInspectedNotSelectedFamilies": len(remaining),
                                "comparisonFamilies": 12}
    evidence["actualPacketLineCounts"] = {
        name: len((S / (PREFIX + name)).read_text(encoding="utf-8").splitlines())
        for name in ["jmdict.xml", "kanjidic2.xml", "comparison-jmdict.xml", "comparison-kanjidic2.xml"]}
    assert not any(e.findtext("reb") == "\u304a\u3046\u3088\u305d" for e in jm.findall("entry/r_ele"))
    expected_readings = [(kind, reading) for kind, field in [("on", "onyomi"), ("kun", "kunyomi")]
                         for reading in row["metadata"][field]]
    assert [(d["kind"], d["reading"]) for d in progress["readingDispositions"]] == expected_readings
    assert progress["sourceReadingOrder"] == {k: row["metadata"][k] for k in ["onyomi", "kunyomi"]}
    assert len(progress["readingDispositions"]) == 5
    assert [d["reading"] for d in progress["readingDispositions"] if d["sourceOnly"]] == ["\u304a\u3046\u3088.\u305d"]
    for entry_id, word, reading in [
        ("1507910", "\u5e73\u51e1", "\u3078\u3044\u307c\u3093"),
        ("1523690", "\u51e1\u4f8b", "\u306f\u3093\u308c\u3044"),
        ("1523450", "\u51e1\u305d", "\u304a\u3088\u305d"),
        ("1595730", "\u51e1\u3066", "\u3059\u3079\u3066"),
        ("1595730", "\u5168\u3066", "\u3059\u3079\u3066"),
    ]:
        assert lexical_pair(families[entry_id], word, reading)
    rare_alias = next(k for k in families["1595730"].findall("k_ele")
                      if k.findtext("keb") == "\u51e1\u3066")
    assert rare_alias.findtext("ke_inf") == "rarely used kanji form"
    projection = progress["proposedCuratedProjection"]
    assert projection["onKeys"] == offered_keys(projection["quizOnyomi"]) == ["\u307c\u3093", "\u306f\u3093"]
    assert projection["kunKeys"] == offered_keys(projection["quizKunyomi"]) == []
    assert projection["legacyFullKunKeys"] == offered_keys(row["metadata"]["kunyomi"])
    mapping = progress["proposedSupportMapping"]
    assert len(mapping) == 4
    pairs = set()
    for m in mapping:
        assert m["entryId"] in exact_ids
        if m["status"] == "necessary-new-article-proposal":
            assert not (R / m["article"]).exists()
            assert lexical_pair(families[m["entryId"]], m["word"], m["primaryReading"])
        else:
            actual = metadata(R, m["article"])
            assert actual["word"] == m["word"] and actual["reading"] == m["primaryReading"]
            assert actual["kanji"] == m["allWrittenKanji"] and actual["jlpt"] == m["preservedWordJlpt"]
        chars = set(m["allWrittenKanji"])
        for alias in m.get("recognitionSpellings", []):
            assert lexical_pair(families[m["entryId"]], alias, m["primaryReading"])
            chars.update(c for c in alias if 0x4E00 <= ord(c) <= 0x9FFF)
        pairs.update((c, m["article"]) for c in chars
                     if c == CHAR or (R / "kanji" / f"{c}.md").exists())
    assert pairs == {tuple(p) for p in progress["proposedReciprocalPairs"]} and len(pairs) == 7
    directions = {(f"kanji/{c}.md", article) for c, article in pairs}
    directions |= {(article, f"kanji/{c}.md") for c, article in pairs}
    existing = []
    for source, target in sorted(directions):
        if (R / source).exists() and (R / target).exists():
            relative = ("../kanji/" if target.startswith("kanji/") else "../words/") + Path(target).name
            if f"]({relative})" in (R / source).read_text(encoding="utf-8"):
                existing.append({"from": source, "to": target})
    progress["proposedDirectedLinkPlan"] = [{"from": source, "to": target}
                                          for source, target in sorted(directions)]
    progress["alreadyExistingRequiredDirections"] = existing
    progress["requiredDirectionCount"] = 14
    progress["newOrChangedRequiredDirections"] = 14 - len(existing)
    save(S / (PREFIX + "progress.json"), progress)
    nav = load(C / "batch-086-source-navigation.json")
    assert [r["article"] for r in nav["candidates"]] == ["words/\u5e73\u51e1.md"]
    assert [r["article"] for r in nav["baselinePairs"]] == ["words/\u5e73\u51e1.md"]
    assert progress["membership"] == load(S / (PREFIX + "membership.json"))["membership"] == [CHAR]
    assert progress["drafted"] == progress["reviewClosed"] == progress["published"] == []
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json")
    checked = sum(len(v) for v in manifest.values() if isinstance(v, dict))
    assert checked == 8413 and manifest["contentVersion"] == "0c514711ae8d3212"
    assert not git("diff", BASE, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    baseline = load(S / "baseline-inventory.json")
    original = {Path(n).stem for n in baseline["files"] if n.startswith("kanji/")}
    current = {p.stem for p in (R / "kanji").glob("*.md")}
    accepted = set("\u5e79\u6c0f\u6271\u4e43\u51f9\u51f8\u77db\u9df9\u5f57\u6f31\u681e\u8389")
    for path in S.glob("batch-*-progress.json"):
        accepted.update(load(path).get("published", []))
    earlier = set("\u4fdd\u6848\u6d3e\u7b2c\u7b56\u7d50")
    assert len(accepted) == 112 and accepted <= current - original and accepted <= set(named)
    assert len(current) == 1108 and len(set(named) & current) == 122
    assert current & set(named) == (original & set(named)) | accepted | earlier
    assert len(set(named) - current) == 1110
    assert all(metadata(R, f"kanji/{c}.md")["jlpt"] == 2 for c in earlier)
    assert metadata(R, "kanji/\u5996.md")["jlpt"] == 1
    tree = json.loads(inputs["n1-kanjivg-tree-70a0b7ae.json"])
    assert not tree["truncated"] and tree["sha"] == snapshot["kanjivg"]["revision"]
    assert next(t for t in tree["tree"] if t["path"] == row["kanjivgInventory"]["path"]) == row["kanjivgInventory"]
    svg_path = C / "inputs" / "n1-051e1-70a0b7ae.svg"
    svg = svg_path.read_bytes()
    blob = hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest()
    assert blob == row["kanjivgInventory"]["sha"] and len(svg) == row["kanjivgInventory"]["size"]
    paths = ET.fromstring(svg).findall(".//{http://www.w3.org/2000/svg}path")
    assert len(paths) == row["metadata"]["strokes"] == 3
    assert [p.attrib["id"] for p in paths] == [f"kvg:051e1-s{i}" for i in range(1, 4)]
    converter = sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n"))
    assert converter == snapshot["kanjivg"]["converter"]["normalizedSha256"]
    stroke = {
        "schemaVersion": 1, "batch": "086", "revision": tree["sha"], "input": str(svg_path),
        "gitBlob": blob, "bytes": len(svg), "sha256": sha(svg),
        "sourceUrl": "https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/kanji/051e1.svg",
        "dictionaryStrokeCount": 3, "sourceStrokePaths": 3, "converted": False,
        "nativeDrawingAccepted": False, "converterNormalizedSha256": converter,
        "attribution": "Ulrich Apel and contributors, KanjiVG, CC BY-SA3.0; repositoryNOTICE.",
        "limits": "Pinned SVG available/inspected/verified; no converted runtime geometry or native drawing acceptance.",
    }
    save(S / (PREFIX + "stroke-evidence.json"), stroke)
    (S / (PREFIX + "kanjivg.svg")).write_bytes(svg)
    han = sorted({c for c in progress["proposedHanText"] if 0x2E80 <= ord(c) <= 0x2FDF
                  or 0x3400 <= ord(c) <= 0x9FFF or 0xF900 <= ord(c) <= 0xFAFF
                  or 0x20000 <= ord(c) <= 0x2FFFF})
    fonts = []
    for old in load(S / "batch-085-font-preparation.json")["fonts"]:
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
        "schemaVersion": 1, "batch": "086", "proposedTextInventory": progress["proposedHanText"],
        "auditedHan": han, "auditedHanCount": len(han), "fonts": fonts,
        "rareHanRangeCharacters": rare,
        "mechanism": "Unchanged RareHan.kt/RareHanTest.kt read; all three actual bundled font cmaps inspected.",
        "limits": "Proposed inventory only, not final runtimeHan. Native fourfont/allHan rendering and non-skipped RareHan test remain required. Cmap presence/absence is not glyph/fallback-face acceptance.",
    })
    public = []
    for item in evidence["publicSources"]:
        path = C / "inputs" / f"batch-086-{item['id']}.html"
        body = path.read_bytes()
        assert body and b"kotobank" in body and CHAR.encode("utf-8") in body
        archive = S / (path.stem + ".html.gz")
        archive.write_bytes(gzip.compress(body, mtime=0))
        assert gzip.decompress(archive.read_bytes()) == body
        public.append({"url": item["url"], "sourcePath": str(path), "archive": archive.name,
                       "sourceSha256": sha(body), "archiveSha256": sha(archive.read_bytes()),
                       "losslessGzip": True, "inspectionLimits": item["limits"]})
    save(evidence_path, evidence)
    result = {
        "schemaVersion": 1, "execution": 600, "batch": "086", "baseCommit": BASE,
        "stage": progress["status"], "membership": [CHAR], "sourceRow": 95,
        "frozenInputHashesVerified": 5, "decompressedDictionaryHashesVerified": 2,
        "exactFrozenNamedMembershipAndRowVerified": True, "completeLexicalFamilies": 49,
        "completeComparisonFamilies": 12, "allExtractedEntryIdsAccountedFor": True,
        "freshExactDictionaryExtractionsVerified": 2, "rawCharacterRecordsVerified": 7,
        "proposedMetadataReadingDispositionsVerified": 5,
        "sourceOnlyExactReadings": ["\u304a\u3046\u3088.\u305d"],
        "proposedOnKeys": projection["onKeys"], "proposedKunKeys": projection["kunKeys"],
        "proposedNewSupportArticles": 1, "proposedReusedSupportArticles": 3,
        "allMappedReciprocalPairs": 7, "requiredDirectedLinks": 14,
        "alreadyExistingRequiredDirections": len(existing),
        "newOrChangedRequiredDirections": 14 - len(existing),
        "activatedBaselinePairs": 1, "pinnedSvg": stroke,
        "proposedHanCount": len(han), "fontPreparation": PREFIX + "font-preparation.json",
        "publicSourceByteReceipts": public,
        "inspectedArticleHashes": {n: sha((R / n).read_bytes())
                                  for n in evidence["authorInspection"]["completeExistingArticlesRead"]},
        "runtimeManifestEqualToPublishedBase": True, "runtimeHashesUnchanged": checked,
        "contentVersion": manifest["contentVersion"], "publishedAdditions": 112,
        "remainingAcceptanceAdditions": 1116, "actuallyAbsentNamedMembers": 1110,
        "separateEarlierLevelSourceMembers": sorted(earlier),
        "separateEarlierPlacementsCountedAsIssue60AcceptedBatches": False,
        "baselinePreservation": "All runtime bytes unchanged from normally signed published base. No baseline metadata/readings/levels/exclusions/geometry changed.",
        "authorInspection": evidence["authorInspection"], "runtimeChanges": 0,
        "reviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "optionalHistoricalHelpersAccessed": False, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "limits": progress["limits"],
    }
    save(S / (PREFIX + "preparation-audit.json"), result)
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ["authorInspection", "limits", "publicSourceByteReceipts",
                                   "pinnedSvg", "inspectedArticleHashes"]}, ensure_ascii=True, indent=2))


def record():
    checks = {}
    for name in ["source-tests", "validate", "budget", "audit", "manifest"]:
        path = L / f"{name}-600.txt"
        text = path.read_text(encoding="utf-8-sig")
        assert "Traceback" not in text and "FAILED" not in text
        if name == "source-tests":
            assert "Ran 43 tests" in text and "OK" in text
        elif name == "validate":
            assert "0 error(s)" in text
        elif name == "audit":
            assert '"runtimeHashesUnchanged": 8413' in text
        raw = path.read_bytes()
        archive = S / f"batch-086-{name}-600.txt.gz"
        archive.write_bytes(gzip.compress(raw, mtime=0))
        assert gzip.decompress(archive.read_bytes()) == raw
        checks[name] = {"path": str(path), "sha256": sha(raw),
                        "archive": archive.name, "archiveSha256": sha(archive.read_bytes()),
                        "losslessGzip": True, "provenance": "Direct redirected subprocess stdout/stderr."}
    recipe = S / (PREFIX + "source-recipe.py")
    recipe.write_bytes(Path(__file__).read_bytes())
    save(S / "execution-600.json", {
        "schemaVersion": 1, "execution": 600, "batch": "086", "baseCommit": BASE,
        "startingState": load(C / "progress.json")["execution600StartingState"],
        "sourceAudit": PREFIX + "preparation-audit.json",
        "sourcePacket": PREFIX + "progress.json", "sourceEvidence": PREFIX + "source-evidence.json",
        "recipe": {"durableControlPath": str(Path(__file__)), "archive": recipe.name,
                   "sha256": sha(recipe.read_bytes())},
        "checks": checks, "runtimeChanged": False, "runtimePublished": False,
        "focusedTestCommand": {
            "cwd": str(R), "PYTHONPATH": str(R / "tools"),
            "argv": ["python", "-X", "utf8", "-B", "-m", "unittest",
                     "test_freeze_n1_sources", "test_extract_n1_jmdict",
                     "test_audit_n1_pilot", "test_audit_n1_batch"],
            "passed": 43,
        },
        "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 112, "remainingAdditions": 1116,
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
    assert changed and all(p.startswith("docs/n1-sources/batch-086-") or p == "docs/n1-sources/execution-600.json"
                           for p in changed)
    before = load(L / "progress-before-600.json")
    p = load(C / "progress.json")
    allowed = {"checkpoint", "status", "stage", "batch", "nextAction", "blocker"}
    assert (p["checkpoint"], p["batch"]) == (599, "086")
    assert all(p.get(k) == v for k, v in before.items() if k not in allowed)
    audit_record = load(S / (PREFIX + "preparation-audit.json"))
    issue = load(L / "issue-response-600.json")
    expected_body = (C / "execution600-issue.txt").read_text(encoding="utf-8").replace("\r\n", "\n")
    assert issue["user"]["login"] == "stop-cran"
    assert issue["body"].replace("\r\n", "\n") == expected_body
    assert issue["issue_url"].endswith("/issues/60")
    receipt = {"id": issue["id"], "url": issue["html_url"], "author": "stop-cran",
               "bodySha256": sha(expected_body.encode("utf-8")), "verified": True}
    state = {
        "schemaVersion": 1, "execution": 600, "checkpoint": 600, "batch": "086",
        "status": "continue", "stage": "source-prepared-not-drafted", "savedCommit": head,
        "signature": "G", "lastPublishedCommit": BASE,
        "sourcePacket": "docs/n1-sources/batch-086-progress.json",
        "sourceAudit": "docs/n1-sources/batch-086-preparation-audit.json",
        "evidence": "docs/n1-sources/execution-600.json",
        "membership": [CHAR], "sourceRow": 95, "completeDictionaryFamilies": 61,
        "lexicalFamilies": 49, "comparisonFamilies": 12, "completeRawCharacterRecords": 7,
        "metadataReadings": 5, "sourceOnlyExactReadings": ["\u304a\u3046\u3088.\u305d"],
        "proposedNewSupportArticles": 1, "proposedReusedSupportArticles": 3,
        "allMappedReciprocalPairs": 7, "proposedLinkDirections": 14,
        "alreadyExistingRequiredDirections": audit_record["alreadyExistingRequiredDirections"],
        "pinnedSvgPaths": 3, "geometryConverted": False,
        "dedicatedWorktreesClean": True, "runtimeChanged": False, "runtimePublished": False,
        "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 112, "remainingAdditions": 1116,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "runtimeHashesUnchanged": 8413, "originalHistoricalRootKeysCompared": len(before),
        "allOriginalHistoricalValuesPreserved": True,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [],
        "issueUpdate": receipt["url"], "ownerIssueAuthorAndBodyVerified": True,
        "nextAction": load(S / (PREFIX + "progress.json"))["nextAction"],
    }
    p["execution600CoordinatorCheckpoint"] = state
    p["batch086SourcePreparation"] = state
    p["batch086SourcePreparationIssueReceipt"] = receipt
    p.update(checkpoint=600, status="continue", stage="batch-086-source-prepared-not-drafted",
             blocker=None, nextAction=state["nextAction"])
    save(C / "progress.json", p)
    reread = load(C / "progress.json")
    assert all(reread.get(k) == v for k, v in before.items() if k not in allowed)
    save(L / "execution-600-final-checkpoint.json", state)
    print(json.dumps(state, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["start", "packet", "comparison", "audit", "record", "seal"])
    globals()[parser.parse_args().action]()

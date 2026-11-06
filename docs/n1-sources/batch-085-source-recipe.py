"""Batch 085 source preparation only; no runtime authoring or publication."""
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
L = C / "logs" / "fe689fe1-5055-4993-a768-f35a1524dadb"
BASE = "97a16b0027b05c0528d78971dd3b17cce17d8056"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
CHAR = "\u51dd"
PREFIX = "batch-085-"
BEFORE = L / "progress-before-591.json"
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata, offered_keys
from build_manifest import build_manifest
from extract_n1_jmdict import extract
from freeze_n1_sources import metadata_record


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    temporary = path.with_suffix(path.suffix + ".591.tmp")
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
    assert (p["checkpoint"], p["batch"], p["status"]) == (590, "084", "continue")
    assert p["lastPublishedCommit"] == BASE and p["remainingAdditions"] == 1117
    assert not BEFORE.exists() and not list(S.glob(PREFIX + "*"))
    shutil.copyfile(C / "progress.json", BEFORE)
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
    assert json.loads(text.split(marker, 1)[1])["checkpoint"] == 590
    state = {
        "execution": 591, "batch": "085", "startingHead": BASE, "freshOriginMain": BASE,
        "androidHead": APP, "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "ONE bounded085 source-preparation checkpoint only; no runtime, reviewer, Android/native, publication,086 or second runner.",
        "request": {"sha256": sha(raw), "bytes": len(raw), "characters": len(text),
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded and embedded checkpoint decoded; operative contract, complete approved issue and final590 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": "Live parent19008 runs control/runner.ps1; child12780 command matches this exact session, parent PID19008. Verified by Win32_Process. Parent retains lock; no child acquisition/deletion/unlock.",
        "artifactPathPreflight": {"durableHelper": str(Path(__file__)),
                                  "priorArt": "Committed batch-084-source-recipe.py and existing extract/freeze/audit tools; approved frozen workspace inputs.",
                                  "optionalHistoricalSessionHelpersAccessed": False},
        "actualNewPermissionDenials": [],
        "worktrees": "Dedicated content and qualified TESTONLY Android wholly clean with signatures G; content equals freshly fetched origin/main. Android1c1b7bf4 atop unchanged productionf9b59a2. Canonical repositories not accessed.",
    }
    p["execution591StartingState"] = state
    p.update(batch="085", stage="batch-085-source-preparation-in-progress", blocker=None,
             nextAction=state["scope"])
    save(C / "progress.json", p)
    print("Full-history starting scope persisted.")


def packet():
    assert load(C / "progress.json")["batch"] == "085"
    snapshot, inputs, jm, kd = frozen()
    row = next(r for r in load(S / "source-index.json") if r["kanji"] == CHAR)
    assert row["sourceRow"] == 94
    assert json.loads(inputs["n1-kanji-source-20261102.json"])[93] == CHAR
    assert not (R / row["article"]).exists() and not (R / row["strokeFile"]).exists()
    ids = [e.findtext("ent_seq") for e in jm.findall("entry")
           if any(CHAR in k.text for k in e.findall("k_ele/keb"))]
    save(S / (PREFIX + "lexical-selection.json"), {
        "schemaVersion": 1, "batch": "085", "entryIds": ids,
        "sourceSnapshot": "docs/n1-source-snapshot.json",
        "selectionRule": "Every complete frozen family containing exact source member U+51DD in any keb; preserve all aliases/readings/restrictions/senses.",
        "limits": "Extraction alone is not inspection, per-character allocation, frequency evidence or independent review.",
    })
    raw = extract(inputs["n1-implementation-JMdict_e.gz"],
                  snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
    (S / (PREFIX + "jmdict.xml")).write_bytes(raw)
    selected = ET.Element("kanjidic2")
    selected.append(copy.deepcopy(kd.find("header")))
    character = next(e for e in kd.findall("character") if e.findtext("literal") == CHAR)
    selected.append(copy.deepcopy(character))
    ET.indent(selected, space="  ")
    raw_kd = ET.tostring(selected, encoding="utf-8", xml_declaration=True) + b"\n"
    (S / (PREFIX + "kanjidic2.xml")).write_bytes(raw_kd)
    save(S / (PREFIX + "input-metadata.json"), {
        "schemaVersion": 1, "batch": "085", "baseCommit": BASE, "sourceIndexRecord": row,
        "characters": [CHAR], "rawCharacterPacket": PREFIX + "kanjidic2.xml",
        "rawCharacterPacketSha256": sha(raw_kd),
        "provenance": "Complete frozen character record/header, parsed and reserialized.",
        "dictionaryAttribution": "Copyright James William Breen and EDRDG; CC BY-SA 4.0; repository NOTICE.",
    })
    candidates = []
    for path in sorted((R / "words").glob("*.md")):
        name = path.relative_to(R).as_posix()
        m = metadata(R, name)
        if CHAR in m.get("kanji", []) or CHAR in m["word"]:
            candidates.append({"article": name, "metadata": m})
    save(C / "batch-085-source-navigation.json", {
        "sourceIndexRecord": row, "candidates": candidates,
        "baselinePairs": [r for r in load(S / "baseline-word-candidates.json") if r["kanji"] == CHAR],
    })
    print(json.dumps({"families": len(ids), "lines": len(raw.splitlines()),
                      "candidates": candidates}, ensure_ascii=True, indent=2))


def audit():
    from audit_n1_batch import lexical_pair
    from fontTools.ttLib import TTFont

    snapshot, inputs, jm, kd = frozen()
    progress = load(S / (PREFIX + "progress.json"))
    evidence_path = S / (PREFIX + "source-evidence.json")
    evidence = load(evidence_path)
    row = next(r for r in load(S / "source-index.json") if r["kanji"] == CHAR)
    named = json.loads(inputs["n1-kanji-source-20261102.json"])
    assert named == load(S / "community-list-20261102.json")
    assert len(named) == len(set(named)) == 1232 and named[93] == CHAR
    character = next(e for e in kd.findall("character") if e.findtext("literal") == CHAR)
    assert metadata_record(character, {15: "\u51ab"}) == row["metadata"]
    canonical = lambda e: ET.canonicalize(ET.tostring(e, encoding="unicode"), strip_text=True)
    raw_character = ET.parse(S / (PREFIX + "kanjidic2.xml")).getroot()
    assert canonical(raw_character.find("header")) == canonical(kd.find("header"))
    assert len(raw_character.findall("character")) == 1
    assert canonical(raw_character.find("character")) == canonical(character)
    ids = [e.findtext("ent_seq") for e in jm.findall("entry")
           if any(CHAR in k.text for k in e.findall("k_ele/keb"))]
    assert ids == load(S / (PREFIX + "lexical-selection.json"))["entryIds"] and len(ids) == 78
    raw = (S / (PREFIX + "jmdict.xml")).read_bytes()
    assert raw == extract(inputs["n1-implementation-JMdict_e.gz"],
                          snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
    explicit = evidence["lexicalDecisions"][:6]
    described = [i for d in explicit for i in d["entryIds"]]
    assert len(described) == len(set(described)) and set(described) <= set(ids)
    remaining = [i for i in ids if i not in described]
    evidence["lexicalDecisions"] = explicit + [{
        "entryIds": remaining, "disposition": evidence["remainingFamilyDisposition"],
    }]
    all_described = [i for d in evidence["lexicalDecisions"] for i in d["entryIds"]]
    assert len(all_described) == len(set(all_described)) == 78 and set(all_described) == set(ids)
    evidence["familyCounts"] = {"allExactMemberFamilies": 78,
                                "individuallyGroupedFamilies": len(described),
                                "otherInspectedNotSelectedFamilies": len(remaining)}
    save(evidence_path, evidence)
    families = {e.findtext("ent_seq"): e for e in ET.fromstring(raw).findall("entry")}
    expected_readings = [(kind, reading) for kind, field in [("on", "onyomi"), ("kun", "kunyomi")]
                         for reading in row["metadata"][field]]
    assert [(d["kind"], d["reading"]) for d in progress["readingDispositions"]] == expected_readings
    assert progress["sourceReadingOrder"] == {k: row["metadata"][k] for k in ["onyomi", "kunyomi"]}
    assert len(progress["readingDispositions"]) == 6
    assert not any(d["sourceOnly"] for d in progress["readingDispositions"])
    for entry_id, word, reading in [
        ("1239070", "\u51dd\u308b", "\u3053\u308b"),
        ("1239010", "\u51dd\u3089\u3059", "\u3053\u3089\u3059"),
        ("1239120", "\u51dd\u56fa", "\u304e\u3087\u3046\u3053"),
        ("1239000", "\u51dd\u3089\u3059", "\u3053\u3054\u3089\u3059"),
        ("1239020", "\u51dd\u3089\u305b\u308b", "\u3053\u3054\u3089\u305b\u308b"),
        ("1239060", "\u51dd\u308b", "\u3053\u3054\u308b"),
    ]:
        assert lexical_pair(families[entry_id], word, reading)
    assert families["1239060"].findtext("sense/misc") == "word usually written using kana alone"
    projection = progress["proposedCuratedProjection"]
    assert projection["onKeys"] == offered_keys(projection["quizOnyomi"]) == ["\u304e\u3087\u3046"]
    assert projection["kunKeys"] == offered_keys(projection["quizKunyomi"]) == ["\u3053\u308b"]
    assert projection["legacyFullKunKeys"] == offered_keys(row["metadata"]["kunyomi"]) == ["\u3053\u308b", "\u3053\u3054\u3089\u3059"]
    selected = [(d["kind"], d["reading"]) for d in progress["readingDispositions"]
                if d["proposedQuizSelection"]]
    assert selected == [("on", "\u30ae\u30e7\u30a6"), ("kun", "\u3053.\u308b"), ("kun", "\u3053.\u3089\u3059")]
    navigation = load(C / "batch-085-source-navigation.json")
    assert navigation["candidates"] == navigation["baselinePairs"] == []
    aliases = {k.findtext("keb") for i in ["1239070", "1239010", "1239120"]
               for k in families[i].findall("k_ele")}
    collisions = []
    for path in (R / "words").glob("*.md"):
        m = metadata(R, path.relative_to(R).as_posix())
        if m["word"] in aliases:
            collisions.append(path.name)
    assert not collisions
    mapping = progress["proposedSupportMapping"]
    assert len(mapping) == 3 and all(not (R / m["article"]).exists() for m in mapping)
    pairs = {(c, m["article"]) for m in mapping for c in m["allWrittenKanji"]
             if c == CHAR or (R / "kanji" / f"{c}.md").exists()}
    assert pairs == {tuple(p) for p in progress["proposedReciprocalPairs"]} and len(pairs) == 4
    directions = {(f"kanji/{c}.md", article) for c, article in pairs}
    directions |= {(article, f"kanji/{c}.md") for c, article in pairs}
    assert directions == {(d["from"], d["to"]) for d in progress["proposedDirectedLinkPlan"]}
    assert len(directions) == 8
    assert progress["membership"] == load(S / (PREFIX + "membership.json"))["membership"] == [CHAR]
    assert progress["drafted"] == progress["reviewClosed"] == progress["published"] == []
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json")
    assert manifest["contentVersion"] == "8c3fa3ee6f2b1ebc"
    checked = sum(len(v) for v in manifest.values() if isinstance(v, dict))
    assert checked == 8408
    assert not git("diff", BASE, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    baseline = load(S / "baseline-inventory.json")
    original = {Path(n).stem for n in baseline["files"] if n.startswith("kanji/")}
    current = {p.stem for p in (R / "kanji").glob("*.md")}
    accepted = set("\u5e79\u6c0f\u6271\u4e43\u51f9\u51f8\u77db\u9df9\u5f57\u6f31\u681e\u8389")
    for path in S.glob("batch-*-progress.json"):
        accepted.update(load(path).get("published", []))
    earlier = set("\u4fdd\u6848\u6d3e\u7b2c\u7b56\u7d50")
    assert len(accepted) == 111 and accepted <= current - original and accepted <= set(named)
    assert len(current) == 1107 and len(set(named) & current) == 121
    assert current & set(named) == (original & set(named)) | accepted | earlier
    assert len(set(named) - current) == 1111
    assert all(metadata(R, f"kanji/{c}.md")["jlpt"] == 2 for c in earlier)
    assert metadata(R, "kanji/\u5996.md")["jlpt"] == 1
    tree = json.loads(inputs["n1-kanjivg-tree-70a0b7ae.json"])
    assert not tree["truncated"] and tree["sha"] == snapshot["kanjivg"]["revision"]
    assert next(t for t in tree["tree"] if t["path"] == row["kanjivgInventory"]["path"]) == row["kanjivgInventory"]
    svg_path = C / "inputs" / "n1-051dd-70a0b7ae.svg"
    svg = svg_path.read_bytes()
    blob = hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest()
    assert blob == row["kanjivgInventory"]["sha"] and len(svg) == row["kanjivgInventory"]["size"]
    paths = ET.fromstring(svg).findall(".//{http://www.w3.org/2000/svg}path")
    assert len(paths) == row["metadata"]["strokes"] == 16
    assert [p.attrib["id"] for p in paths] == [f"kvg:051dd-s{i}" for i in range(1, 17)]
    converter = sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n"))
    assert converter == snapshot["kanjivg"]["converter"]["normalizedSha256"]
    stroke = {
        "schemaVersion": 1, "batch": "085", "revision": tree["sha"], "input": str(svg_path),
        "gitBlob": blob, "bytes": len(svg), "sha256": sha(svg),
        "sourceUrl": "https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/kanji/051dd.svg",
        "dictionaryStrokeCount": 16, "sourceStrokePaths": 16, "converted": False,
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
    for old in load(S / "batch-084-font-preparation.json")["fonts"]:
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
        "schemaVersion": 1, "batch": "085", "proposedTextInventory": progress["proposedHanText"],
        "auditedHan": han, "auditedHanCount": len(han), "fonts": fonts,
        "rareHanRangeCharacters": rare,
        "mechanism": "Unchanged RareHan.kt/RareHanTest.kt read; all three actual bundled font cmaps inspected.",
        "limits": "Proposed inventory only, not final runtime Han; native fourfont/allHan rendering and non-skipped RareHan test remain required. Cmap absence is not glyph failure/fallback-face evidence.",
    })
    public = []
    for item in evidence["publicSources"]:
        path = C / "inputs" / f"batch-085-{item['id']}.html"
        body = path.read_bytes()
        assert body and b"kotobank" in body and CHAR.encode("utf-8") in body
        archive = S / (path.stem + ".html.gz")
        archive.write_bytes(gzip.compress(body, mtime=0))
        assert gzip.decompress(archive.read_bytes()) == body
        public.append({"url": item["url"], "sourcePath": str(path), "archive": archive.name,
                       "sourceSha256": sha(body), "archiveSha256": sha(archive.read_bytes()),
                       "losslessGzip": True, "inspectionLimits": item["limits"]})
    result = {
        "schemaVersion": 1, "execution": 591, "batch": "085", "baseCommit": BASE,
        "stage": progress["status"], "membership": [CHAR], "sourceRow": 94,
        "frozenInputHashesVerified": 5, "decompressedDictionaryHashesVerified": 2,
        "exactFrozenNamedMembershipAndRowVerified": True, "completeLexicalFamilies": 78,
        "allExtractedEntryIdsAccountedFor": True, "freshExactDictionaryExtractionVerified": True,
        "lexicalPacketSha256": sha(raw), "rawCharacterRecordsVerified": 1,
        "proposedMetadataReadingDispositionsVerified": 6,
        "documentedUnselectedNotSourceOnlyReadings": 3,
        "proposedOnKeys": projection["onKeys"], "proposedKunKeys": projection["kunKeys"],
        "proposedNewSupportArticles": 3, "allMappedReciprocalPairs": 4,
        "requiredDirectedLinks": 8, "activatedBaselinePairs": 0, "pinnedSvg": stroke,
        "proposedHanCount": len(han), "fontPreparation": PREFIX + "font-preparation.json",
        "publicSourceByteReceipts": public,
        "inspectedArticleHashes": {n: sha((R / n).read_bytes())
                                  for n in evidence["authorInspection"]["completeExistingArticlesRead"]},
        "runtimeManifestEqualToPublishedBase": True, "runtimeHashesUnchanged": checked,
        "contentVersion": manifest["contentVersion"], "publishedAdditions": 111,
        "remainingAcceptanceAdditions": 1117, "actuallyAbsentNamedMembers": 1111,
        "separateEarlierLevelSourceMembers": sorted(earlier),
        "separateEarlierPlacementsCountedAsIssue60AcceptedBatches": False,
        "baselinePreservation": "All runtime bytes unchanged from normally signed published base; this checkpoint changes no baseline metadata, readings, levels, exclusions or geometry.",
        "authorInspection": evidence["authorInspection"], "runtimeChanges": 0,
        "reviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "optionalHistoricalHelpersAccessed": False, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "limits": progress["limits"],
    }
    save(S / (PREFIX + "preparation-audit.json"), result)
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ["authorInspection", "limits", "publicSourceByteReceipts", "pinnedSvg", "inspectedArticleHashes"]},
                     ensure_ascii=True, indent=2))


def record():
    checks = {}
    for name in ["source-tests", "validate", "budget", "audit", "manifest", "audit-initial", "source-tests-initial"]:
        path = L / f"{name}-591.txt"
        text = path.read_text(encoding="utf-8-sig")
        if name == "source-tests":
            assert "Ran 43 tests" in text and "OK" in text and "FAILED" not in text
        elif name == "validate":
            assert "0 error(s)" in text
        elif name == "audit":
            assert '"runtimeHashesUnchanged": 8408' in text
        elif name == "audit-initial":
            assert "AssertionError" in text
        elif name == "source-tests-initial":
            assert "ModuleNotFoundError" in text and "FAILED (errors=4)" in text
        else:
            assert "ERROR" not in text and "Traceback" not in text
        raw = path.read_bytes()
        archive = S / f"batch-085-{name}-591.txt.gz"
        archive.write_bytes(gzip.compress(raw, mtime=0))
        assert gzip.decompress(archive.read_bytes()) == raw
        checks[name] = {"path": str(path), "sha256": sha(raw),
                        "archive": archive.name, "archiveSha256": sha(archive.read_bytes()),
                        "losslessGzip": True, "provenance": "Direct redirected subprocess stdout/stderr."}
    recipe = S / (PREFIX + "source-recipe.py")
    recipe.write_bytes(Path(__file__).read_bytes())
    save(S / "execution-591.json", {
        "schemaVersion": 1, "execution": 591, "batch": "085", "baseCommit": BASE,
        "startingState": load(C / "progress.json")["execution591StartingState"],
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
            "diagnostic": "First invocation used tools.test_* from repo root without tools on sys.path, yielding four loader import errors and zero actual cases. Original output preserved. Corrected invocation sets process-only PYTHONPATH to existing tools; no dependencies installed or tests changed.",
        },
        "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 111, "remainingAdditions": 1117,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False,
        "nextAction": load(S / (PREFIX + "progress.json"))["nextAction"],
        "limits": load(S / (PREFIX + "progress.json"))["limits"],
    })
    print("Source evidence/checks and durable recipe archived; local signing next, no push.")


def seal():
    head = git("rev-parse", "HEAD")
    clean(R, head)
    clean(A, APP)
    assert head != BASE and git("rev-parse", "origin/main") == BASE
    assert not git("diff", BASE, "HEAD", "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    changed = git("diff", "--name-only", BASE, "HEAD").splitlines()
    assert changed and all(p.startswith("docs/n1-sources/batch-085-") or p == "docs/n1-sources/execution-591.json"
                           for p in changed)
    before = load(BEFORE)
    p = load(C / "progress.json")
    allowed = {"checkpoint", "status", "stage", "batch", "nextAction", "blocker"}
    assert (p["checkpoint"], p["batch"]) == (590, "085")
    assert all(p.get(k) == v for k, v in before.items() if k not in allowed)
    state = {
        "schemaVersion": 1, "execution": 591, "checkpoint": 591, "batch": "085",
        "status": "continue", "stage": "source-prepared-not-drafted", "savedCommit": head,
        "signature": "G", "lastPublishedCommit": BASE,
        "sourcePacket": "docs/n1-sources/batch-085-progress.json",
        "sourceAudit": "docs/n1-sources/batch-085-preparation-audit.json",
        "evidence": "docs/n1-sources/execution-591.json",
        "membership": [CHAR], "sourceRow": 94, "completeDictionaryFamilies": 78,
        "metadataReadings": 6, "proposedNewSupportArticles": 3,
        "allMappedReciprocalPairs": 4, "proposedLinkDirections": 8,
        "pinnedSvgPaths": 16, "geometryConverted": False,
        "dedicatedWorktreesClean": True, "runtimeChanged": False, "runtimePublished": False,
        "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 111, "remainingAdditions": 1117,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "runtimeHashesUnchanged": 8408, "originalHistoricalRootKeysCompared": len(before),
        "allOriginalHistoricalValuesPreserved": True,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [],
        "nextAction": load(S / (PREFIX + "progress.json"))["nextAction"],
    }
    p["execution591CoordinatorCheckpoint"] = state
    p["batch085SourcePreparation"] = state
    p.update(checkpoint=591, status="continue", stage="batch-085-source-prepared-not-drafted",
             blocker=None, nextAction=state["nextAction"])
    save(C / "progress.json", p)
    reread = load(C / "progress.json")
    assert all(reread.get(k) == v for k, v in before.items() if k not in allowed)
    save(L / "execution-591-final-checkpoint.json", state)
    print(json.dumps(state, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["start", "packet", "audit", "record", "seal"])
    globals()[parser.parse_args().action]()

"""Complete a bounded batch100 source plan; no runtime authoring."""
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
L = C / "logs" / "7af9c34a-0eb0-446e-a0c2-4e6b5aee3383"
HEAD = "961b94b6e9456a6f55585482c67b9cb8c4d0c2e7"
MAIN = "716c610153234e8d2240dcf528de3ef83b654b27"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata
from extract_n1_jmdict import extract


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, value):
    tmp = path.with_suffix(path.suffix + ".746.tmp")
    assert not tmp.exists(), tmp
    tmp.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(tmp) == value
    tmp.replace(path)


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
    clean(R, HEAD)
    clean(A, APP)
    assert git("rev-parse", "origin/main") == MAIN
    assert git("branch", "--show-current") == "content/n1-kanji"
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (745, "100", "continue")
    assert p["lastPublishedCommit"] == MAIN and p["remainingAdditions"] == 1102
    role = load(L / "preflight-746.json")
    assert role["liveParentPid"] == 5920 and role["sessionId"] == L.name
    assert role["lockTouched"] is False
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["execution745CoordinatorCheckpoint"] == p["execution745CoordinatorCheckpoint"]
    assert not (L / "progress-before-746.json").exists()
    shutil.copyfile(C / "progress.json", L / "progress-before-746.json")
    state = {
        "execution": 746, "batch": "100", "startingHead": HEAD, "freshOriginMain": MAIN,
        "androidHead": APP, "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME100 bounded source-completion checkpoint only; no runtime draft, reviewer, Android/native, publication,101 or second runner.",
        "request": {"sha256": sha(raw), "bytes": len(raw), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and checkpoint parsed; operative contract, approved issue and final745 inspected directly. Historical middle parsed, not freshly semantically re-reviewed. Initial console encoding failure happened after loading."},
        "runnerPreflight": role,
        "artifactPathPreflight": "Approved control helpers, committed source packets and frozen workspace inputs only; no optional historical-session recipes accessed.",
        "actualNewPermissionDenials": [],
    }
    p["execution746StartingState"] = state
    p.update(stage="batch-100-source-completion-in-progress", nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    print("Starting scope persisted with full live history.")


def navigate():
    _, _, jm, _ = frozen()
    selected = {"1597890", "1307550", "1580260", "1398420", "1345890"}
    for e in jm.findall("entry"):
        if e.findtext("ent_seq") in selected:
            print(ET.tostring(e, encoding="unicode"))
    print("KANJI LABEL CANDIDATES")
    for path in sorted((R / "kanji").glob("*.md")):
        m = metadata(R, path.relative_to(R).as_posix())
        import re
        if re.search(r"creat|origin|begin|start|wound|injur|scratch|make|produc|warehouse|inspect|sword|frugal", m["title"], re.I):
            print(path.name, json.dumps(m, ensure_ascii=False))


def comparisons():
    snapshot, inputs, jm, kd = frozen()
    spellings = ["剣", "真剣", "倹約", "倹しい", "試験", "作る", "始める",
                 "生産", "原因", "元", "本", "緒"]
    members = load(S / "batch-100-lexical-selection.json")["entryIds"]
    ids = [e.findtext("ent_seq") for e in jm.findall("entry")
           if any(k.text in spellings for k in e.findall("k_ele/keb"))
           and e.findtext("ent_seq") not in members]
    selection = {
        "schemaVersion": 1, "batch": "100", "entryIds": ids, "exactSpellings": spellings,
        "memberPacketAlsoApplicable": ["1597890", "1307550", "1580260", "1398420", "1345890"],
        "selectionRule": "Every complete frozen family with an exact selected keb, excluding families already retained in the member packet. All aliases/readings/restrictions/senses retained.",
        "scope": "Existing distractor and fallback-guard label checks plus actual reused spelling identity, not a review of every unchanged example or linked article.",
    }
    save(S / "batch-100-comparison-selection.json", selection)
    raw = extract(inputs["n1-implementation-JMdict_e.gz"],
                  snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
    (S / "batch-100-comparison-jmdict.xml").write_bytes(raw)
    compact = []
    for entry in ET.fromstring(raw):
        for node in entry.iter():
            if node.text and not node.text.strip():
                node.text = None
            node.tail = None
        compact.append(ET.tostring(entry, encoding="unicode"))
    text = ("\n".join(compact) + "\n").encode("utf-8")
    (C / "batch-100-comparison-full-family-reading.txt").write_bytes(text)
    (S / "batch-100-comparison-full-family-reading.txt.gz").write_bytes(gzip.compress(text, mtime=0))
    chars = "創剣倹験作造始元原本緒産刀"
    selected = ET.Element("kanjidic2")
    selected.append(copy.deepcopy(kd.find("header")))
    for char in chars:
        selected.append(copy.deepcopy(next(e for e in kd.findall("character")
                                          if e.findtext("literal") == char)))
    ET.indent(selected, space="  ")
    (S / "batch-100-comparison-kanjidic2.xml").write_bytes(
        ET.tostring(selected, encoding="utf-8", xml_declaration=True) + b"\n")
    print(json.dumps({"families": len(ids), "entryIds": ids, "characters": list(chars)}, ensure_ascii=False))


def canonical(element):
    return (element.tag, tuple(sorted(element.attrib.items())),
            (element.text or "").strip(), tuple(canonical(child) for child in element))


def prepare():
    from fontTools.ttLib import TTFont
    snapshot, inputs, _, _ = frozen()
    plan = load(S / "batch-100-authoring-plan.json")
    han = sorted({c for c in plan["proposedHanText"] if
                  0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                  or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF})
    fonts = []
    for old in load(S / "batch-099-font-preparation.json")["fonts"]:
        path = Path(old["path"])
        assert path.is_relative_to(A) and sha(path.read_bytes()) == old["sha256"]
        with TTFont(path) as font:
            cmap = font.getBestCmap()
        fonts.append({"path": str(path), "sha256": old["sha256"],
                      "keyGlyphPresence": {c: ord(c) in cmap for c in han},
                      "allProposedMissing": [c for c in han if ord(c) not in cmap]})
    rare = [c for c in han if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x4DBF
            or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF]
    radical = next(line for line in inputs["n1-UnicodeData-17.0.0.txt"].decode("utf-8").splitlines()
                   if line.startswith("2F11;"))
    assert radical.split(";")[5] == "<compat> 5200"
    save(S / "batch-100-font-preparation.json", {
        "schemaVersion": 1, "batch": "100", "proposedTextInventory": plan["proposedHanText"],
        "inventoryScope": plan["fontInventoryScope"], "auditedHan": han,
        "auditedHanCount": len(han), "fonts": fonts, "rareHanRangeCharacters": rare,
        "unicodeRadicalRecord": radical,
        "mechanism": "Unchanged RareHan.kt and RareHanTest.kt inspected; three actual bundled font cmaps checked. All proposed Han ordinary BMP.",
        "limits": "Cmap absence is not a glyph failure; this is proposed text only. Final actual Han, non-skipped RareHan test and fresh native four-font/all-Han rendering remain required. No font acceptance claimed.",
    })
    raw = (C / "batch-100-tsukuru.html").read_bytes()
    text = raw.decode("utf-8")
    assert "デジタル大辞泉" in text and "創る" in text and "つくる" in text
    target = S / "batch-100-tsukuru.html.gz"
    target.write_bytes(gzip.compress(raw, mtime=0))
    save(S / "batch-100-additional-public-sources.json", [{
        "url": "https://www.weblio.jp/content/%E5%89%B5%E3%82%8B",
        "downloadedAt": datetime.now(timezone.utc).isoformat(),
        "actualHeading": "Digital Daijisen: つく・る【作る／造る／創る】",
        "rawBytes": len(raw), "rawSha256": sha(raw), "archive": target.name,
        "archiveSha256": sha(target.read_bytes()), "losslessGzip": True,
        "inspection": plan["authorInspection"]["newPublicSource"],
        "claim": "Actual heading confirms exact spelling/reading. The supplement distinguishes creation-oriented 創る from production/manufacturing and usual broad 作る; no fabricated collocation or universal substitution rule is adopted.",
        "limits": "Actual web_fetch return inspected through the spelling supplement and into later usage notes; not a claim that every raw HTML section was read. JMdict family1597890 remains the frozen complete lexical base.",
    }])
    p = load(S / "batch-100-progress.json")
    p.update(status="source-prepared-not-drafted", sourcePreparationComplete=True,
             authoringPlan="batch-100-authoring-plan.json",
             preparationAudit="batch-100-preparation-audit.json",
             fullSourceObservationsRemainHistorical=True,
             proposedSupportArticles=plan["reusedSupportArticles"], proposedNewSupportArticles=[],
             proposedMetadata=plan["proposedMetadata"],
             allMappedReciprocalPairs=plan["allMappedReciprocalPairs"],
             nextAction=plan["nextAction"])
    save(S / "batch-100-progress.json", p)
    print(json.dumps({"proposedHan": len(han), "missingMainCmap": fonts[0]["allProposedMissing"],
                      "sourcePreparationComplete": True}, ensure_ascii=False))


def audit():
    from audit_n1_pilot import offered_keys
    from build_manifest import build_manifest
    snapshot, inputs, jm, kd = frozen()
    plan = load(S / "batch-100-authoring-plan.json")
    assert plan["membership"] == ["創"] and plan["sourceRows"] == [111]
    row = next(r for r in load(S / "source-index.json") if r["kanji"] == "創")
    assert row == load(S / "batch-100-input-metadata.json")["sourceIndexRecord"]
    assert json.loads(inputs["n1-kanji-source-20261102.json"])[110] == "創"
    member_ids = [e.findtext("ent_seq") for e in jm.findall("entry")
                  if any("創" in k.text for k in e.findall("k_ele/keb"))]
    assert len(member_ids) == 137
    assert member_ids == load(S / "batch-100-lexical-selection.json")["entryIds"]
    selection = load(S / "batch-100-comparison-selection.json")
    compare_ids = [e.findtext("ent_seq") for e in jm.findall("entry")
                   if any(k.text in selection["exactSpellings"] for k in e.findall("k_ele/keb"))
                   and e.findtext("ent_seq") not in member_ids]
    assert compare_ids == selection["entryIds"] and len(compare_ids) == 16
    families = {}
    for ids, xml, compact in [
        (member_ids, "batch-100-jmdict.xml", "batch-100-full-family-reading.txt.gz"),
        (compare_ids, "batch-100-comparison-jmdict.xml", "batch-100-comparison-full-family-reading.txt.gz"),
    ]:
        raw = (S / xml).read_bytes()
        assert raw == extract(inputs["n1-implementation-JMdict_e.gz"],
                              snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        entries = ET.fromstring(raw).findall("entry")
        lines = gzip.decompress((S / compact).read_bytes()).decode("utf-8").splitlines()
        assert len(entries) == len(lines) == len(ids)
        assert all(canonical(ET.fromstring(a)) == canonical(b) for a, b in zip(lines, entries))
        families.update({e.findtext("ent_seq"): e for e in entries})
    expected_characters = list("創剣倹験作造始元原本緒産刀")
    source_chars = {e.findtext("literal"): e for e in kd.findall("character")}
    records = ET.parse(S / "batch-100-comparison-kanjidic2.xml").getroot().findall("character")
    assert [e.findtext("literal") for e in records] == expected_characters
    assert all(canonical(e) == canonical(source_chars[e.findtext("literal")]) for e in records)
    assert canonical(ET.parse(S / "batch-100-kanjidic2.xml").getroot().find("character")) == canonical(source_chars["創"])
    assert not (R / row["article"]).exists() and not (R / row["strokeFile"]).exists()
    meta = plan["proposedMetadata"]
    assert plan["sourceReadingOrder"] == {k: row["metadata"][k] for k in ["onyomi", "kunyomi"]}
    assert all(meta[k] == row["metadata"][k] for k in ["kanji", "strokes", "radical", "radicalNumber", "onyomi", "kunyomi"])
    dispositions = plan["readingDispositions"]
    assert [(r["kind"], r["reading"]) for r in dispositions] == [
        (kind, reading) for kind, field in [("on", "onyomi"), ("kun", "kunyomi")]
        for reading in meta[field]]
    for kind, field in [("on", "onyomi"), ("kun", "kunyomi")]:
        selected = [r for r in dispositions if r["kind"] == kind and r["status"] == "selected"]
        assert meta["quiz" + field.capitalize()] == [r["reading"] for r in selected]
        for r in selected:
            assert r["reading"] in meta[field]
            article = metadata(R, r["article"])
            assert article["reading"] == r["exampleReading"]
            family = families[r["entryIds"][0]]
            assert r["example"] in [k.text for k in family.findall("k_ele/keb")]
            assert r["exampleReading"] in [k.text for k in family.findall("r_ele/reb")]
    assert offered_keys(meta["quizOnyomi"]) == ["そう"]
    assert offered_keys(meta["quizKunyomi"]) == ["つくる"]
    assert [r["reading"] for r in dispositions if r["status"] == "source-only-unselected"] == ["ショウ", "けず.しける"]
    assert len(meta["distractors"]) == 3 and len(set(meta["quiz_exclusions"])) == 8
    assert not set(meta["distractors"]) & set(meta["quiz_exclusions"])
    assert [r["kanji"] for r in plan["quizPlan"]["distractors"]] == meta["distractors"]
    assert [r["kanji"] for r in plan["quizPlan"]["directGuards"]] == meta["quiz_exclusions"]
    for r in plan["quizPlan"]["distractors"] + plan["quizPlan"]["directGuards"]:
        old = metadata(R, f"kanji/{r['kanji']}.md")
        assert r["label"] == old["title"]
        assert "創" not in old.get("quiz_exclusions", [])
    for p in (R / "kanji").glob("*.md"):
        assert metadata(R, p.relative_to(R).as_posix())["title"] != meta["title"]
    mappings = {(r["kanji"], r["article"]) for r in plan["supportMappings"]}
    assert mappings == {tuple(p) for p in plan["allMappedReciprocalPairs"]} and len(mappings) == 5
    for article in plan["reusedSupportArticles"]:
        assert {(c, article) for c in metadata(R, article)["kanji"]} <= mappings
    baseline = [r for r in load(S / "baseline-word-candidates.json") if r["kanji"] == "創"]
    assert [(r["kanji"], r["article"]) for r in baseline] == [tuple(p) for p in plan["activatedBaselinePairs"]]
    directions = {(f"kanji/{char}.md", article) for char, article in mappings}
    directions |= {(article, f"kanji/{char}.md") for char, article in mappings}
    existing = set()
    for source, target in directions:
        if (R / source).exists() and (R / target).exists():
            relative = ("../words/" if source.startswith("kanji/") else "../kanji/") + target.split("/")[-1]
            if f"]({relative})" in (R / source).read_text(encoding="utf-8"):
                existing.add((source, target))
    assert len(directions) == plan["requiredDirections"] == 10
    assert existing == {tuple(p) for p in plan["existingDirections"]} and len(existing) == 5
    assert len(directions - existing) == plan["newDirectionsRequired"] == 5
    assert len(metadata(R, "words/創作.md")["quiz_exclusions"]) == 13
    assert len(metadata(R, "words/作る.md")["quiz_exclusions"]) == 5
    assert metadata(R, "words/創作.md")["jlpt"] == 2
    assert metadata(R, "words/作る.md")["jlpt"] == 5
    svg = (S / "batch-100-kanjivg.svg").read_bytes()
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == row["kanjivgInventory"]["sha"]
    assert svg == (C / "inputs" / "n1-05275-70a0b7ae.svg").read_bytes()
    paths = ET.fromstring(svg).findall(".//{http://www.w3.org/2000/svg}path")
    assert [p.attrib["id"] for p in paths] == [f"kvg:05275-s{i}" for i in range(1, 13)]
    assert sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")) == snapshot["kanjivg"]["converter"]["normalizedSha256"]
    font = load(S / "batch-100-font-preparation.json")
    for receipt in load(S / "batch-100-additional-public-sources.json"):
        raw = (S / receipt["archive"]).read_bytes()
        assert sha(raw) == receipt["archiveSha256"] and sha(gzip.decompress(raw)) == receipt["rawSha256"]
    for r in font["fonts"]:
        assert sha(Path(r["path"]).read_bytes()) == r["sha256"]
    assert not git("diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert git("rev-parse", "HEAD") == HEAD and git("rev-parse", "origin/main") == MAIN
    clean(A, APP)
    manifest = load(R / "manifest.json")
    assert manifest == build_manifest(R)
    checked = 0
    text_maps = {"files", "scenes", "listening", "curriculum", "listeningTasks"}
    binary_maps = {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
    for category, entries in manifest.items():
        if not isinstance(entries, dict):
            continue
        assert category in text_maps | binary_maps, category
        for name, expected in entries.items():
            data = (R / name).read_bytes()
            if category in text_maps:
                data = data.replace(b"\r\n", b"\n")
            assert sha(data) == expected, (category, name)
            checked += 1
    before, now = load(L / "progress-before-746.json"), load(C / "progress.json")
    mutable = {"stage", "nextAction", "blocker"}
    assert all(now[k] == v for k, v in before.items() if k not in mutable)
    result = {
        "schemaVersion": 1, "execution": 746, "batch": "100", "baseCommit": HEAD,
        "stage": "source-prepared-not-drafted", "membership": ["創"], "sourceRow": 111,
        "frozenInputHashesVerified": len(inputs), "decompressedDictionaryHashesVerified": 2,
        "completeMemberFamilies": len(member_ids), "completeComparisonFamilies": len(compare_ids),
        "distinctCompleteFamilies": len(families), "freshExactExtractionsVerified": 2,
        "compactFullFamilySemanticEquality": True, "completeRawCharacterRecords": len(records),
        "rawCharacterSemanticEquality": True, "metadataReadingDispositions": len(dispositions),
        "sourceOnlyReadingCount": 2, "verifiedRecognitionUnselectedCount": 2,
        "proposedOnKeys": ["そう"], "proposedKunKeys": ["つくる"],
        "proposedNewSupportArticles": 0, "proposedReusedSupportArticles": 2,
        "allMappedReciprocalPairs": len(mappings), "requiredDirectedLinks": len(directions),
        "alreadyExistingDirections": len(existing), "newDirectionsRequired": len(directions - existing),
        "activatedBaselinePairs": len(baseline), "proposedNewDirectKanjiGuards": 8,
        "proposedNewDirectWordGuards": 0, "pinnedSvgPaths": len(paths), "geometryConverted": False,
        "proposedHanCount": font["auditedHanCount"], "mainFontCmapAbsences": font["fonts"][0]["allProposedMissing"],
        "inspectedArticleHashes": {name: sha((R / name).read_bytes()) for name in plan["authorInspection"]["completeExistingArticlesRead"]},
        "runtimeBytesUnchanged": True, "runtimeHashesVerified": checked,
        "manifestSha256": sha((R / "manifest.json").read_bytes()), "contentVersion": manifest["contentVersion"],
        "originalHistoricalRootValuesPreserved": True,
        "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "runtimeChanged": False, "runtimePublished": False, "independentReviewersLaunched": 0,
        "freshAndroidOrNativeClaimed": False, "publishedAdditions": 126, "remainingAdditions": 1102,
        "limits": "Source plan and mechanical provenance only; source-only lexical validity remains explicitly unverified/excluded from quiz teaching. No runtime authored, independent review, fresh app/native/phone acceptance or publication.",
    }
    save(S / "batch-100-preparation-audit.json", result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("step", choices=["start", "navigate", "comparisons", "prepare", "audit"])
    globals()[parser.parse_args().step]()

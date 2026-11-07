"""Complete batch101's source plan without changing runtime content."""
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
L = C / "logs" / "4e67593f-d049-419a-bffc-99f4ebf29f79"
BASE = "1a25e38563f59f91b50cfaa3a8d8329ef2acd6f2"
MAIN = "ba1a7f467a2431523e3131d4f259c1d3260c93af"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata
from build_manifest import build_manifest, sha256 as manifest_sha256
from extract_n1_jmdict import extract


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, value):
    temporary = path.with_suffix(path.suffix + ".763.tmp")
    assert not temporary.exists(), temporary
    temporary.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temporary) == value
    temporary.replace(path)


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
    assert git("rev-parse", "origin/main") == MAIN
    assert git("branch", "--show-current") == "content/n1-kanji"
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (762, "101", "continue")
    assert p["lastPublishedCommit"] == MAIN and p["remainingAdditions"] == 1101
    role = load(L / "preflight-763.json")
    assert role["liveParentPid"] == 5920 and role["sessionId"] == L.name and not role["lockTouched"]
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["checkpoint"] == 762
    assert checkpoint["execution762CoordinatorCheckpoint"] == p["execution762CoordinatorCheckpoint"]
    assert not (L / "progress-before-763.json").exists()
    shutil.copyfile(C / "progress.json", L / "progress-before-763.json")
    state = {
        "execution": 763, "batch": "101", "startingHead": BASE, "freshOriginMain": MAIN,
        "androidHead": APP, "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME101 source completion only; no runtime draft, reviewer, Android/native, publication,102 or second runner.",
        "request": {"sha256": sha(raw), "bytes": len(raw), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and complete checkpoint parsed before acting. Operative contract, approved issue and final762 inspected directly; historical middle parsed, not freshly semantically re-reviewed. Initial output encoding failure occurred after full loading."},
        "runnerPreflight": role,
        "artifactPathPreflight": "Approved control helpers, committed source packets and frozen workspace inputs only; no optional historical-session recipes accessed.",
        "worktrees": "Wholly clean dedicated signed content and qualified Android heads; fresh main unchanged. Canonical repositories not accessed.",
        "actualNewPermissionDenials": [],
    }
    p["execution763StartingState"] = state
    p.update(stage="batch-101-source-completion-in-progress", nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    print("Starting scope persisted with full live history.")


def comparisons():
    snapshot, inputs, jm, kd = frozen()
    spellings = [
        "\u52a0\u3048\u308b", "\u5e7c\u3044", "\u5200",
        "\u6210\u7e3e", "\u5b9f\u7e3e", "\u52b9\u679c", "\u52b9\u304f",
        "\u679c\u305f\u3059", "\u6210\u308b", "\u9054\u3059\u308b", "\u52dd\u3064",
        "\u51f1\u6b4c", "\u6804\u3048\u308b", "\u656c\u3046", "\u50cd\u304f",
        "\u696d", "\u6280", "\u5de5",
    ]
    member_ids = set(load(S / "batch-101-lexical-selection.json")["entryIds"])
    ids = [e.findtext("ent_seq") for e in jm.findall("entry")
           if any(k.text in spellings for k in e.findall("k_ele/keb"))
           and e.findtext("ent_seq") not in member_ids]
    selection = {
        "schemaVersion": 1, "batch": "101", "entryIds": ids, "exactSpellings": spellings,
        "memberPacketAlsoApplicable": ["1275070", "1375690", "1275080", "2411570", "2411590"],
        "selectionRule": "Every complete frozen family with an exact selected keb, excluding member-packet families. Preserve all aliases, readings, restrictions and senses.",
        "scope": "Actual distractor and possible fallback-overlap labels; source extraction is not independent review or an assertion that all matches are teaching examples.",
    }
    save(S / "batch-101-comparison-selection.json", selection)
    raw = extract(inputs["n1-implementation-JMdict_e.gz"],
                  snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
    (S / "batch-101-comparison-jmdict.xml").write_bytes(raw)
    compact = []
    for entry in ET.fromstring(raw):
        for node in entry.iter():
            if node.text and not node.text.strip():
                node.text = None
            node.tail = None
        compact.append(ET.tostring(entry, encoding="unicode"))
    text = ("\n".join(compact) + "\n").encode("utf-8")
    (C / "batch-101-comparison-full-family-reading.txt").write_bytes(text)
    (S / "batch-101-comparison-full-family-reading.txt.gz").write_bytes(gzip.compress(text, mtime=0))
    chars = "\u529f\u52a0\u5e7c\u5200\u7e3e\u52b9\u679c\u6210\u9054\u52dd\u51f1\u6804\u656c\u50cd\u696d\u6280\u5de5\u529b"
    selected = ET.Element("kanjidic2")
    selected.append(copy.deepcopy(kd.find("header")))
    for char in chars:
        selected.append(copy.deepcopy(next(e for e in kd.findall("character")
                                          if e.findtext("literal") == char)))
    ET.indent(selected, space="  ")
    (S / "batch-101-comparison-kanjidic2.xml").write_bytes(
        ET.tostring(selected, encoding="utf-8", xml_declaration=True) + b"\n")
    print(json.dumps({"families": len(ids), "entryIds": ids, "characters": list(chars)}))


def canonical(element):
    return (element.tag, tuple(sorted(element.attrib.items())),
            (element.text or "").strip(), tuple(canonical(child) for child in element))


def prepare():
    from fontTools.ttLib import TTFont
    import yaml

    snapshot, inputs, _, _ = frozen()
    plan = load(S / "batch-101-authoring-plan.json")
    baselines = []
    for name in plan["authorInspection"]["completeExistingArticlesRead"]:
        path = R / name
        raw = path.read_bytes()
        baselines.append({"article": name, "rawSha256": sha(raw),
                          "metadata": metadata(R, name),
                          "scope": "Full existing article freshly read; preserved except exact planned navigation replacement, if assigned."})
    simulations = []
    for change in plan["reusedPassageChanges"]:
        original = (R / change["article"]).read_text(encoding="utf-8")
        assert original.count(change["old"]) == 1, change["article"]
        assert change["new"] not in original, change["article"]
        proposed = original.replace(change["old"], change["new"], 1)
        assert proposed.replace(change["new"], change["old"], 1) == original
        assert yaml.safe_load(proposed.split("---", 2)[1]) == metadata(R, change["article"])
        simulations.append({**change, "oldTextSha256": sha(original.encode()),
                            "proposedTextSha256": sha(proposed.encode()),
                            "metadataPreservedExactly": True, "runtimeEdited": False})
    save(S / "batch-101-baseline-plan.json", {
        "schemaVersion": 1, "batch": "101", "baseCommit": BASE,
        "completeExistingArticles": baselines, "exactNavigationSimulations": simulations,
        "noNewWordOrTitle": True, "existingWordExclusionsUnchanged": True,
        "limits": "In-memory source-plan simulation only, not a runtime diff or independent review.",
    })
    han = sorted({c for c in plan["proposedHanText"] if
                  0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                  or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF})
    fonts = []
    for old in load(S / "batch-100-font-preparation.json")["fonts"]:
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
                   if line.startswith("2F12;"))
    assert radical.split(";")[5] == "<compat> 529B"
    save(S / "batch-101-font-preparation.json", {
        "schemaVersion": 1, "batch": "101", "proposedTextInventory": plan["proposedHanText"],
        "inventoryScope": plan["fontInventoryScope"], "auditedHan": han,
        "auditedHanCount": len(han), "fonts": fonts, "rareHanRangeCharacters": rare,
        "unicodeRadicalRecord": radical,
        "mechanism": "Unchanged RareHan.kt and RareHanTest.kt inspected. Actual three bundled font cmaps checked against proposed text. Canonical力 is ordinary U+529B, not compatibility-radical U+2F12.",
        "limits": "Proposed text only; cmap absence is not a glyph failure and cmap presence is not native rendered acceptance. Final actual-Han audit, non-skipped RareHan test and fresh native four-font/all-Han rendering remain mandatory.",
    })
    progress = load(S / "batch-101-progress.json")
    progress.update(status="source-prepared-not-drafted", sourcePreparationComplete=True,
                    authoringPlan="batch-101-authoring-plan.json",
                    preparationAudit="batch-101-preparation-audit.json",
                    fullSourceObservationsRemainHistorical=True,
                    nextAction=plan["nextAction"])
    save(S / "batch-101-progress.json", progress)
    print(json.dumps({"articlesPreserved": len(baselines),
                      "navigationSimulations": len(simulations), "proposedHan": len(han),
                      "fontAbsences": [f["allProposedMissing"] for f in fonts]}))


def audit():
    import re
    snapshot, inputs, jm, kd = frozen()
    plan = load(S / "batch-101-authoring-plan.json")
    progress = load(S / "batch-101-progress.json")
    assert plan["sourcePreparationComplete"] and progress["sourcePreparationComplete"]
    row = load(S / "batch-101-input-metadata.json")["sourceIndexRecord"]
    assert row == next(r for r in load(S / "source-index.json") if r["sourceRow"] == 112)
    assert json.loads(inputs["n1-kanji-source-20261102.json"])[111] == row["kanji"] == "\u529f"
    assert not (R / row["article"]).exists() and not (R / row["strokeFile"]).exists()
    assert plan["sourceReadingOrder"] == {k: row["metadata"][k] for k in ("onyomi", "kunyomi")}
    proposed = plan["proposedMetadata"]
    for field in ("kanji", "strokes", "radical", "radicalNumber", "onyomi", "kunyomi"):
        assert proposed[field] == row["metadata"][field], field
    assert proposed["quizOnyomi"] == ["\u30b3\u30a6"] and proposed["quizKunyomi"] == []
    expected = [(kind, reading) for kind, field in [("on", "onyomi"), ("kun", "kunyomi")]
                for reading in row["metadata"][field]]
    assert [(r["kind"], r["reading"]) for r in plan["readingDispositions"]] == expected
    members = load(S / "batch-101-lexical-selection.json")["entryIds"]
    fresh_members = [e.findtext("ent_seq") for e in jm.findall("entry")
                     if any("\u529f" in k.text for k in e.findall("k_ele/keb"))]
    assert members == fresh_members and len(members) == 99
    for prefix, selection in [
        ("batch-101-", {"entryIds": members}),
        ("batch-101-comparison-", load(S / "batch-101-comparison-selection.json")),
    ]:
        raw = (S / (prefix + "jmdict.xml")).read_bytes()
        assert raw == extract(inputs["n1-implementation-JMdict_e.gz"],
                              snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"],
                              selection["entryIds"])
        entries = ET.fromstring(raw).findall("entry")
        compact = gzip.decompress((S / (prefix + "full-family-reading.txt.gz")).read_bytes())
        lines = compact.decode("utf-8").splitlines()
        assert len(entries) == len(lines) == len(selection["entryIds"])
        assert all(canonical(ET.fromstring(a)) == canonical(b) for a, b in zip(lines, entries))
    comparison = load(S / "batch-101-comparison-selection.json")
    expected_ids = [e.findtext("ent_seq") for e in jm.findall("entry")
                    if any(k.text in comparison["exactSpellings"] for k in e.findall("k_ele/keb"))
                    and e.findtext("ent_seq") not in members]
    assert comparison["entryIds"] == expected_ids and len(expected_ids) == 23
    records = ET.parse(S / "batch-101-comparison-kanjidic2.xml").getroot().findall("character")
    for record in records:
        original = next(e for e in kd.findall("character")
                        if e.findtext("literal") == record.findtext("literal"))
        assert canonical(record) == canonical(original)
    assert len(records) == 18
    all_ids = set(members + expected_ids)
    for disposition in plan["readingDispositions"]:
        assert set(disposition["entryIds"]) <= all_ids
    for item in [*plan["quizPlan"]["distractors"], *plan["quizPlan"]["directGuards"]]:
        assert metadata(R, "kanji/" + item["kanji"] + ".md")["title"] == item["label"]
        assert set(item["entryIds"]) <= all_ids
    assert proposed["distractors"] == [x["kanji"] for x in plan["quizPlan"]["distractors"]]
    assert proposed["quiz_exclusions"] == [x["kanji"] for x in plan["quizPlan"]["directGuards"]]
    assert len(set(proposed["distractors"])) == 3 and len(set(proposed["quiz_exclusions"])) == 13
    assert not set(proposed["distractors"]) & set(proposed["quiz_exclusions"])
    for path in (R / "kanji").glob("*.md"):
        assert metadata(R, path.relative_to(R).as_posix())["title"] != proposed["title"]
    baseline = load(S / "batch-101-baseline-plan.json")
    for old in baseline["completeExistingArticles"]:
        assert sha((R / old["article"]).read_bytes()) == old["rawSha256"]
        assert metadata(R, old["article"]) == old["metadata"]
    pairs = {(x["kanji"], x["article"]) for x in plan["supportMappings"]}
    assert pairs == {tuple(x) for x in plan["allMappedReciprocalPairs"]} and len(pairs) == 4
    supports = set(plan["reusedSupportArticles"])
    actual_pairs = {(c, name) for name in supports for c in metadata(R, name)["kanji"]}
    assert actual_pairs == pairs
    actual_baseline = {(r["kanji"], r["article"])
                       for r in load(S / "baseline-word-candidates.json") if r["kanji"] == "\u529f"}
    assert actual_baseline == {tuple(x) for x in plan["activatedBaselinePairs"]} and len(actual_baseline) == 2
    directions = set()
    for char, word in pairs:
        card = "kanji/" + char + ".md"
        for src, dst in [(word, card), (card, word)]:
            path = R / src
            if path.exists():
                links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", path.read_text(encoding="utf-8"))
                if any((path.parent / link).resolve() == (R / dst).resolve()
                       for link in links if not link.startswith("https:")):
                    directions.add((src, dst))
    assert directions == {tuple(x) for x in plan["existingDirections"]} and len(directions) == 3
    for mapping in plan["supportMappings"]:
        meta = metadata(R, mapping["article"])
        assert meta["reading"] == mapping["reading"] and meta["word"] == mapping["word"]
    for simulation in baseline["exactNavigationSimulations"]:
        text = (R / simulation["article"]).read_text(encoding="utf-8")
        assert sha(text.encode()) == simulation["oldTextSha256"]
        assert text.count(simulation["old"]) == 1
        assert sha(text.replace(simulation["old"], simulation["new"], 1).encode()) == simulation["proposedTextSha256"]
    for receipt in load(S / "batch-101-public-source-receipts.json"):
        raw = (S / receipt["archive"]).read_bytes()
        assert sha(raw) == receipt["archiveSha256"]
        assert sha(gzip.decompress(raw)) == receipt["rawSha256"]
        assert sha((S / receipt["extractedText"]).read_bytes()) == receipt["extractedTextSha256"]
    stroke = load(S / "batch-101-stroke-evidence.json")
    svg = (S / "batch-101-kanjivg.svg").read_bytes()
    assert sha(svg) == stroke["sha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == row["kanjivgInventory"]["sha"]
    paths = ET.fromstring(svg).findall(".//{http://www.w3.org/2000/svg}path")
    assert [p.attrib["id"] for p in paths] == [f"kvg:0529f-s{i}" for i in range(1, 6)]
    assert len(paths) == proposed["strokes"] == 5 and not stroke["converted"]
    converter = sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n"))
    assert converter == snapshot["kanjivg"]["converter"]["normalizedSha256"]
    assert converter == plan["shapeAndStrokePlan"]["converterNormalizedSha256"]
    font = load(S / "batch-101-font-preparation.json")
    assert len(font["fonts"]) == 3 and not font["rareHanRangeCharacters"]
    for f in font["fonts"]:
        assert sha(Path(f["path"]).read_bytes()) == f["sha256"] and not f["allProposedMissing"]
    manifest = load(R / "manifest.json")
    assert build_manifest(R) == manifest
    count = 0
    for section in ("files", "images", "scenes", "audio", "listening", "curriculum", "listeningTasks",
                    "listeningTaskAudio", "listeningTaskImages"):
        for name, digest in manifest.get(section, {}).items():
            path = R.joinpath(*name.split("/"))
            actual = (sha(path.read_bytes()) if section in
                      {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
                      else manifest_sha256(path))
            assert actual == digest, name
            count += 1
    assert count == 8453 and manifest["contentVersion"] == "606c836e4be33ba9"
    assert not git("diff", BASE, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert git("rev-parse", "HEAD") == BASE and git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "origin/main") == MAIN
    clean(A, APP)
    before = load(L / "progress-before-763.json")
    now = load(C / "progress.json")
    mutable = {"stage", "nextAction", "blocker"}
    assert all(now[k] == value for k, value in before.items() if k not in mutable)
    result = {
        "schemaVersion": 1, "execution": 763, "batch": "101", "baseCommit": BASE,
        "frozenInputHashesVerified": len(inputs), "decompressedDictionaryHashesVerified": 2,
        "completeMemberFamiliesRetained": 99, "freshApplicableMemberFamiliesRead": 7,
        "completeComparisonFamilies": 23, "exactFreshExtractionsMatch": True,
        "compactFullFamilySemanticEquality": True, "completeRawCharacterRecords": 18,
        "rawCharacterSemanticEquality": True, "sourceRow": 112, "kanji": "\u529f",
        "metadataReadingsPreservedInSourceOrder": 3,
        "curatedOnKeys": ["\u3053\u3046"], "curatedKunKeys": [],
        "sourcePreparationComplete": True, "completeExistingArticlesRead": 19,
        "allMappedPairs": 4, "requiredDirections": 8, "existingDirections": 3,
        "newDirectionsPlanned": 5, "activatedBaselinePairs": 2,
        "exactNavigationSimulations": 3, "newSupportArticles": 0,
        "curatedDistractors": 3, "directSymmetricNontransitiveGuards": 13,
        "proposedHan": font["auditedHanCount"], "bundledFonts": 3,
        "proposedCmapAbsences": [], "newRareHan": [], "pinnedSvgPaths": 5,
        "geometryConverted": False, "runtimeBytesUnchanged": True,
        "runtimeManifestHashesVerified": count, "contentVersion": manifest["contentVersion"],
        "originalHistoricalRootValuesPreserved": True,
        "limits": "Source-plan mechanical audit, not independent linguistic review or runtime/native/rendered acceptance. Thirteen conservative guards require later actual-builder/default fallback checks and independent review. No fresh phone/general-release acceptance.",
    }
    save(S / "batch-101-preparation-audit.json", result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("step", choices=["start", "comparisons", "prepare", "audit"])
    globals()[parser.parse_args().step]()

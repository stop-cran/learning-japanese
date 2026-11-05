import gzip
import hashlib
import json
import math
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

CONTROL = Path(__file__).resolve().parent
ROOT = CONTROL.parent / "learning-japanese"
FOLDER = ROOT / "docs" / "n1-sources"
BASE = "af7bae60d24ee20fe6eea1c31100eca5f09459df"
CHAR = "俳"
COMPARISONS = ["非", "悲", "借", "優", "句", "詩", "詩人", "役者", "女優", "主役", "川柳", "演技"]
RAW_CHARACTERS = {CHAR, "人", "非", "悲", "借", "優", "句"}
sys.path.insert(0, str(ROOT / "tools"))
from audit_n1_pilot import metadata
from audit_n1_batch import base_file, lexical_pair, reused_changes, runtime_delta
from audit_n1_pilot import offered_keys, quiz_readings
from build_manifest import build_manifest, sha256
from check_content_budget import archive_names, check
from extract_n1_jmdict import extract
from fontTools.ttLib import TTFont
from generate_strokes import convert


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def git(*args):
    return subprocess.check_output(
        ["git", "--no-pager", *args], cwd=ROOT, text=True, encoding="utf-8"
    ).strip()


def start():
    request = CONTROL / "logs" / "6f53135d-12ad-49ab-93cd-e94359f83468" / "request.txt"
    raw = request.read_bytes()
    text = raw.decode("utf-8-sig")
    marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
    embedded = json.loads(text.split(marker, 1)[1])
    progress = load(CONTROL / "progress.json")
    assert progress["checkpoint"] == embedded["checkpoint"] == 369
    assert progress["status"] == "continue"
    assert progress["lastPublishedCommit"] == git("rev-parse", "HEAD") == git("rev-parse", "origin/main") == BASE
    assert not git("status", "--porcelain")
    assert "execution370StartingState" not in progress
    record = {
        "execution": 370, "batch": "061", "startingHead": BASE,
        "startedAt": datetime.now().astimezone().isoformat(),
        "scope": "ONE evidence-bounded061 source inspection and normally signed local source checkpoint; draft only if complete evidence fits. No reviewer, Android/native, runtime publication,062 or second runner.",
        "status": "inspecting-frozen-source-and-current-support",
        "authorization": {
            "requestSha256": digest(raw), "lines": len(text.splitlines()), "characters": len(text),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request acquired into memory and complete embedded checkpoint parsed; operative contract, complete final369 checkpoint and complete approved issue inspected directly. Historical middle acquired and parsed, not freshly semantically re-reviewed.",
        },
        "worktrees": "Dedicated content clean signedGaf7bae60 and dedicated Android clean signedGf9b59a2. Fresh main fetch equals content HEAD. No canonical worktree accessed; accepted060 retained without rerun.",
    }
    save(CONTROL / "execution-370-starting-progress.json", progress)
    save(CONTROL / "execution-370-start.json", record)
    progress["stage"] = "batch-061-source-inspection"
    progress["batch"] = "061"
    progress["execution370StartingState"] = record
    progress["nextAction"] = "Prepare ONE bounded061俳 from exact remaining source row54. Inspect complete applicable families and actual reused articles, preserve all history; no062/reviewer/Android/native/publication in this checkpoint."
    save(CONTROL / "progress.json", progress)
    print(json.dumps(record, ensure_ascii=False, indent=2))


def inputs():
    snapshot = load(ROOT / "docs" / "n1-source-snapshot.json")
    for name, row in snapshot["inputs"].items():
        assert digest((CONTROL / "inputs" / name).read_bytes()) == row["sha256"], name
    for name, section in [
        ("n1-planning-kanjidic2.xml.gz", "kanjidic2"),
        ("n1-implementation-JMdict_e.gz", "jmdict"),
    ]:
        assert digest(gzip.decompress((CONTROL / "inputs" / name).read_bytes())) == snapshot[section]["xmlSha256"]
    return snapshot


def groups(dictionary):
    result = {"lexical": [], "comparison": []}
    for entry in ET.fromstring(gzip.decompress(dictionary)).findall("entry"):
        forms = {e.text for e in entry.findall("k_ele/keb") + entry.findall("r_ele/reb")}
        kind = "lexical" if any(CHAR in form for form in forms) else "comparison" if forms & set(COMPARISONS) else None
        if kind:
            result[kind].append(entry.findtext("ent_seq"))
    return result


def raw_metadata():
    source = ET.fromstring(gzip.decompress((CONTROL / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes()))
    selected = ET.Element("kanjidic2")
    selected.append(source.find("header"))
    for element in source.findall("character"):
        if element.findtext("literal") in RAW_CHARACTERS:
            selected.append(element)
    ET.indent(selected, space="  ")
    return ET.tostring(selected, encoding="utf-8", xml_declaration=True) + b"\n"


def prepare():
    snapshot = inputs()
    dictionary = (CONTROL / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    row = next(r for r in load(FOLDER / "source-index.json") if r["kanji"] == CHAR)
    assert git("rev-parse", "HEAD") == BASE and not git("status", "--porcelain")
    assert not (ROOT / row["article"]).exists() and not (ROOT / row["strokeFile"]).exists()
    for kind, ids in groups(dictionary).items():
        selection = FOLDER / f"batch-061-{kind}-selection.json"
        packet = FOLDER / ("batch-061-jmdict.xml" if kind == "lexical" else "batch-061-comparison-jmdict.xml")
        assert not selection.exists() and not packet.exists()
        save(selection, {
            "schemaVersion": 1, "batch": "061", "entryIds": ids,
            "selectionSpellings": [CHAR] if kind == "lexical" else COMPARISONS,
            "provenance": "Complete frozen JMdict families in all spelling/reading positions; comparisons disjoint from lexical matches.",
            "limits": "Recognition does not establish frequency, per-character allocation, etymology or unrestricted substitution.",
        })
        raw = extract(dictionary, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        packet.write_bytes(raw)
        print(kind, len(ids), "families", len(raw.splitlines()), "lines")
        for entry in ET.fromstring(raw).findall("entry"):
            print(entry.findtext("ent_seq"), "/".join(e.text for e in entry.findall("k_ele/keb")), "/".join(e.text for e in entry.findall("r_ele/reb")))
    target = FOLDER / "batch-061-kanjidic2.xml"
    assert not target.exists()
    target.write_bytes(raw_metadata())
    save(FOLDER / "batch-061-input-metadata.json", {
        "schemaVersion": 1, "batch": "061", "baseCommit": BASE,
        "sourceIndexRecord": row, "rawCharacterPacket": target.name,
        "rawCharacterPacketSha256": digest(target.read_bytes()),
        "provenance": "Complete seven frozen KANJIDIC2 character elements plus header; raw fields retained separately from future teaching choices.",
    })
    print("RAW CHARACTERS", len(RAW_CHARACTERS), "LINES", len(target.read_bytes().splitlines()))
    baseline = [r for r in load(FOLDER / "baseline-word-candidates.json") if r["kanji"] == CHAR]
    print("BASELINE CANDIDATES", json.dumps(baseline, ensure_ascii=False))


def strokes():
    snapshot = inputs()
    row = next(r for r in load(FOLDER / "source-index.json") if r["kanji"] == CHAR)
    svg = (CONTROL / "inputs" / "n1-04ff3-70a0b7ae.svg").read_bytes()
    blob = hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest()
    assert len(svg) == row["kanjivgInventory"]["size"] == 3787
    assert blob == row["kanjivgInventory"]["sha"]
    converter_hash = digest((ROOT / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n"))
    assert converter_hash == snapshot["kanjivg"]["converter"]["normalizedSha256"]
    data = convert(CHAR, svg.decode("utf-8"))
    assert data["strokeCount"] == row["metadata"]["strokes"] == 10
    target = ROOT / "strokes" / f"{CHAR}.json"
    assert not target.exists()
    target.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    record = {
        "schemaVersion": 1, "batch": "061", "character": CHAR,
        "sourceUrl": "https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/kanji/04ff3.svg",
        "sourceRevision": data["sourceRevision"], "sourceBytes": len(svg),
        "gitBlob": blob, "sourceSha256": digest(svg),
        "sourceLocalPath": "control/inputs/n1-04ff3-70a0b7ae.svg",
        "converter": "tools/generate_strokes.py:convert; unchanged pinned converter",
        "converterNormalizedSha256": converter_hash,
        "target": "strokes/俳.json", "targetSha256": digest(target.read_bytes()),
        "strokeCount": 10, "pointsPerStroke": 16,
        "dictionaryAndSvgCountAgreement": True,
        "license": "KanjiVG CC BY-SA 3.0; generated file retains attribution.",
        "limits": "Pinned SVG conversion only, not native drawing recognition, readable glyphs or phone evidence. No historical/phonetic analysis inferred from SVG annotations.",
    }
    save(FOLDER / "batch-061-stroke-evidence.json", record)
    print(json.dumps(record, ensure_ascii=False, indent=2))


def audit():
    snapshot = inputs()
    ledger = load(FOLDER / "batch-061-progress.json")
    membership = load(FOLDER / "batch-061-membership.json")
    assert ledger["baseCommit"] == membership["baseCommit"] == BASE
    assert ledger["membership"] == ledger["drafted"] == membership["membership"] == [CHAR]
    assert ledger["reviewClosed"] == ledger["published"] == []
    assert git("rev-parse", "HEAD") == BASE
    row = next(r for r in load(FOLDER / "source-index.json") if r["kanji"] == CHAR)
    named = load(CONTROL / "inputs" / "n1-kanji-source-20261102.json")
    assert len(named) == len(set(named)) == 1232 and named[row["sourceRow"] - 1] == CHAR
    assert row["sourceRow"] == membership["members"][0]["sourceRow"] == 54
    tree = load(CONTROL / "inputs" / "n1-kanjivg-tree-70a0b7ae.json")
    assert next(r for r in tree["tree"] if r["path"] == row["kanjivgInventory"]["path"]) == row["kanjivgInventory"]
    assert load(FOLDER / "batch-061-input-metadata.json")["sourceIndexRecord"] == row
    assert (FOLDER / "batch-061-kanjidic2.xml").read_bytes() == raw_metadata()
    dictionary = (CONTROL / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    families, packets = {}, []
    for kind, ids in groups(dictionary).items():
        name = "batch-061-jmdict.xml" if kind == "lexical" else "batch-061-comparison-jmdict.xml"
        raw = (FOLDER / name).read_bytes()
        assert load(FOLDER / f"batch-061-{kind}-selection.json")["entryIds"] == ids
        assert raw == extract(dictionary, digest(dictionary), ids)
        dispositions = [entry for group in ledger[f"{kind}Dispositions"] for entry in group["entries"]]
        assert len(dispositions) == len(set(dispositions)) and set(dispositions) == set(ids)
        entries = ET.fromstring(raw).findall("entry")
        assert [e.findtext("ent_seq") for e in entries] == ids
        assert not families.keys() & set(ids)
        families.update(zip(ids, entries))
        packets.append({"path": name, "families": len(ids), "lines": len(raw.splitlines()), "sha256": digest(raw)})
    assert len(families) == 45
    assert families["1600580"].findall("k_ele")[1].findtext("ke_inf") == "search-only kanji form"
    immutable = [
        "docs/n1-source-snapshot.json", "docs/n1-sources/source-index.json",
        "docs/n1-sources/baseline-inventory.json", "docs/n1-sources/baseline-word-candidates.json",
    ]
    for name in immutable:
        assert (ROOT / name).read_text(encoding="utf-8") == base_file(ROOT, BASE, name)
    manifest = load(ROOT / "manifest.json")
    assert manifest == build_manifest(ROOT)
    before = json.loads(base_file(ROOT, BASE, "manifest.json"))
    additions = {"kanji/俳.md", "strokes/俳.json"}
    changes = {r["article"] for r in ledger["changedReusedPassages"]}
    assert changes == {"words/俳句.md", "words/俳優.md", "kanji/優.md"}
    runtime_delta(before, manifest, additions, changes)
    for name in changes:
        edits = [r for r in ledger["changedReusedPassages"] if r["article"] == name]
        reused_changes(base_file(ROOT, BASE, name), (ROOT / name).read_text(encoding="utf-8"), edits)
    checked = 0
    for section, entries in manifest.items():
        if isinstance(entries, dict):
            for name, expected in entries.items():
                path = ROOT / name
                actual = digest(path.read_bytes()) if section in {
                    "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(path)
                assert actual == expected, name
                checked += 1
    assert checked == 8311
    counts = {"kanji": 0, "words": 0, "strokes": 0}
    exceptions = {
        "words/虎.md": {"quiz_exclusions": ["酔っ払い"]},
        "words/猿.md": {"quiz_exclusions": ["馬鹿"]},
        "words/丘.md": {"quiz_exclusions": ["坂", "山"]},
        "kanji/山.md": {"distractors": ["川", "出", "木"]},
    }
    for name, record in load(FOLDER / "baseline-inventory.json")["files"].items():
        kind = name.split("/")[0]
        if kind in {"kanji", "words"}:
            expected = dict(record["metadata"])
            expected.update(exceptions.get(name, {}))
            assert metadata(ROOT, name) == expected, name
            counts[kind] += 1
        elif kind == "strokes":
            assert digest((ROOT / name).read_bytes()) == record["sha256"], name
            counts[kind] += 1
    assert counts == {"kanji": 985, "words": 4942, "strokes": 985}
    pairs = {(r["kanji"], r["article"]) for r in ledger["supportMappings"]}
    assert len(pairs) == len(ledger["supportMappings"]) == 3
    assert pairs == set(map(tuple, ledger["requiredReciprocalPairs"])) == {
        ("俳", "words/俳句.md"), ("俳", "words/俳優.md"), ("優", "words/俳優.md")}
    for mapping in ledger["supportMappings"]:
        char, name = mapping["kanji"], mapping["article"]
        m = metadata(ROOT, name)
        assert char in m["kanji"] and m["reading"] == mapping["primaryReading"]
        assert not mapping["newArticle"] and name in changes
        assert any(lexical_pair(families[i], m["word"], m["reading"]) for i in mapping["entryIds"])
        assert f"(../kanji/{char}.md)" in (ROOT / name).read_text(encoding="utf-8")
        assert f"(../{name})" in (ROOT / f"kanji/{char}.md").read_text(encoding="utf-8")
    assert not (ROOT / "kanji" / "句.md").exists()
    assert [r for r in load(FOLDER / "baseline-word-candidates.json") if r["kanji"] == CHAR] == ledger["baselineCandidatePairs"]
    current_pairs = []
    for path in sorted((ROOT / "words").glob("*.md")):
        relative = path.relative_to(ROOT).as_posix()
        m = metadata(ROOT, relative)
        if CHAR in m.get("kanji", []):
            current_pairs.append({"article": relative, "word": m["word"], "primaryReading": m["reading"]})
    assert current_pairs == ledger["currentDeclaredWordPairs"]
    all_mapped = {(char, mapping["article"]) for mapping in ledger["supportMappings"]
                  for char in metadata(ROOT, mapping["article"])["kanji"]
                  if (ROOT / "kanji" / f"{char}.md").exists()}
    assert all_mapped == pairs
    m = metadata(ROOT, "kanji/俳.md")
    for key in ("kanji", "strokes", "radical", "radicalNumber", "onyomi", "kunyomi"):
        assert m[key] == row["metadata"][key]
    assert m["jlpt"] == 1 and {"jlpt-n1", "grade-6", "structure-unclassified"} <= set(m["tags"])
    assert "phonetic" not in m
    assert ledger["sourceReadingOrder"] == {key: m[key] for key in ("onyomi", "kunyomi")}
    assert len(ledger["readingDispositions"]) == 1
    decision = ledger["readingDispositions"][0]
    assert decision["kanji"] == CHAR and decision["reading"] == "ハイ" and decision["selected"] and not decision["sourceOnly"]
    table = (ROOT / "kanji" / "俳.md").read_text(encoding="utf-8").split("## Readings\n", 1)[1].split("## Common words", 1)[0]
    lines = [line for line in table.splitlines() if line.startswith("| ハイ |")]
    assert len(lines) == 1 and "(../words/俳句.md)" in lines[0] and "(../words/俳優.md)" in lines[0]
    projection = ledger["curatedProjection"][0]
    for field, key in (("onyomi", "onKeys"), ("kunyomi", "kunKeys")):
        selected = quiz_readings(m, field)
        assert selected == projection["quiz" + field[0].upper() + field[1:]]
        assert offered_keys(selected) == projection[key]
    quiz = ledger["quizAudit"][CHAR]
    assert m["title"] == quiz["title"] and m["distractors"] == quiz["distractors"] == ["非", "悲", "借"]
    assert quiz["labels"] == [metadata(ROOT, f"kanji/{c}.md")["title"] for c in m["distractors"]]
    assert sum(metadata(ROOT, p.relative_to(ROOT).as_posix())["title"] == m["title"] for p in (ROOT / "kanji").glob("*.md")) == 1
    assert metadata(ROOT, "words/俳句.md")["jlpt"] == 2 and metadata(ROOT, "words/俳優.md")["jlpt"] == 3
    assert metadata(ROOT, "words/役者.md")["title"] == metadata(ROOT, "words/俳優.md")["title"]
    for left, right in [("俳句", "句"), ("俳句", "詩"), ("川柳", "俳句"), ("女優", "俳優"), ("主役", "俳優")]:
        assert right in metadata(ROOT, f"words/{left}.md").get("quiz_exclusions", [])
    svg = (CONTROL / "inputs" / "n1-04ff3-70a0b7ae.svg").read_bytes()
    geometry = load(FOLDER / "batch-061-stroke-evidence.json")
    assert len(svg) == row["kanjivgInventory"]["size"] == 3787
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == row["kanjivgInventory"]["sha"]
    assert digest(svg) == geometry["sourceSha256"]
    data = load(ROOT / "strokes" / "俳.json")
    assert data == convert(CHAR, svg.decode("utf-8"))
    assert data["strokeCount"] == len(data["strokes"]) == 10
    for stroke in data["strokes"]:
        assert len(stroke["points"]) == 16
        assert all(len(p) == 2 and all(math.isfinite(v) and 0 <= v <= 109 for v in p) for p in stroke["points"])
    assert digest((ROOT / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")) == snapshot["kanjivg"]["converter"]["normalizedSha256"]
    authored = sorted(changes | {"kanji/俳.md"})
    authored_text = "\n".join((ROOT / name).read_text(encoding="utf-8") for name in authored)
    han = sorted(set(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]", authored_text)))
    assert "亻" in han and CHAR in han
    android = CONTROL.parent / "kanji-cards-android"
    assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=android, text=True).strip() == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
    assert not subprocess.check_output(["git", "status", "--porcelain"], cwd=android).strip()
    fonts = []
    for record in load(FOLDER / "font-coverage.json")["fonts"]:
        path = android / record["path"]
        assert digest(path.read_bytes()) == record["sha256"]
        with TTFont(path) as font:
            missing = [c for c in han if ord(c) not in font.getBestCmap()]
        fonts.append({"path": record["path"], "sha256": record["sha256"], "missing": missing})
    legacy = []
    for path in sorted((ROOT / "kanji").glob("*.md")):
        item = metadata(ROOT, path.relative_to(ROOT).as_posix())
        if len(item.get("distractors", [])) < 3:
            legacy.append({key: item[key] for key in ("kanji", "title", "distractors")})
    assert [r["kanji"] for r in legacy] == ["人", "休", "何", "入", "出", "口", "女", "日", "月", "男", "買"]
    actual_counts = {
        "kanji": len(list((ROOT / "kanji").glob("*.md"))),
        "words": len(list((ROOT / "words").glob("*.md"))),
        "n1Labelled": sum(metadata(ROOT, p.relative_to(ROOT).as_posix())["jlpt"] == 1 for p in (ROOT / "kanji").glob("*.md")),
        "namedSourceMembersPresent": sum((ROOT / "kanji" / f"{c}.md").exists() for c in named),
    }
    assert actual_counts == {"kanji": 1073, "words": 5031, "n1Labelled": 93, "namedSourceMembersPresent": 92}
    source_members = {r["kanji"] for r in load(FOLDER / "source-index.json")}
    original_cards = {Path(n).stem for n in load(FOLDER / "baseline-inventory.json")["files"] if n.startswith("kanji/")}
    local_additions = {p.stem for p in (ROOT / "kanji").glob("*.md")} - original_cards
    assert len(local_additions) == 88 and local_additions <= source_members
    assert metadata(ROOT, "kanji/妖.md")["jlpt"] == 1
    result = {
        "schemaVersion": 1, "execution": 370, "batch": "061",
        "status": "local-unreviewed-runtime-draft", "baseCommit": BASE,
        "namedSourceRow": 54, "exactFrozenNamedMembershipAndKanjiVGRecordVerified": True,
        "frozenInputHashesVerified": 5, "decompressedDictionaryHashesVerified": 2,
        "exactFrozenFamilyExtractions": 45, "dictionaryPackets": packets,
        "rawCharacterPacket": {"path": "batch-061-kanjidic2.xml", "characters": 7, "sha256": digest(raw_metadata())},
        "coordinatorInspection": ledger["authorInspection"],
        "immutableEvidenceUnchanged": immutable, "baselineMetadataAndStrokesChecked": counts,
        "explicitBaselineMetadataExceptions": exceptions, "newBaselineMetadataExceptions": [],
        "runtimePayloadHashesVerified": checked, "baseRuntimeHashesUnchanged": checked - len(additions) - len(changes),
        "runtimeAdditions": sorted(additions), "changedReusedRuntimePayloads": sorted(changes),
        "manifestFresh": True, "contentVersion": manifest["contentVersion"], "actualDraftCounts": actual_counts,
        "localDraftAdditions": 88, "requiredReciprocalPairs": 3, "directedLinks": 6,
        "activatedBaselinePairs": 2, "unavailableMappedPairs": ledger["unavailableMappedPairs"],
        "fullReadingDispositions": 1, "offeredKeys": ["はい"], "sourceOnlyOfferedKeys": [],
        "newWords": 0, "changedWordTitles": 0, "newDirectWordExclusions": 0,
        "originalWordGuardsPreserved": True,
        "legacyFallbackCandidatesWithFewerThanThree": legacy,
        "legacyFallbackDisposition": "All eleven labels inspected. Haiku/actor is not the general person, gender or everyday action/object meaning of these cards; mere performer/person relationship does not establish a general synonym. No new default four-choice collision established. Larger/random/live pools unverified.",
        "geometry": geometry,
        "actualAuthoredHanFonts": {
            "articles": authored, "characters": han, "count": len(han), "fonts": fonts,
            "missingUnion": sorted({c for r in fonts for c in r["missing"]}),
            "limits": "All new and changed reused articles included, including actual 亻. Cmap presence is not native readability, fallback-face or phone evidence.",
        },
        "budget": check(ROOT, archive_names(ROOT)),
        "publishedAdditions": 87, "remainingAdditions": 1141, "limits": ledger["limits"],
    }
    save(FOLDER / "batch-061-draft-audit.json", result)
    print(json.dumps({key: result[key] for key in (
        "actualDraftCounts", "contentVersion", "runtimePayloadHashesVerified",
        "requiredReciprocalPairs", "actualAuthoredHanFonts", "budget")}, ensure_ascii=False, indent=2))


def evidence():
    assert git("rev-parse", "HEAD") == BASE
    test_source = CONTROL / "execution-370-python-tests.txt"
    test_raw = test_source.read_bytes()
    test_text = test_raw.decode("utf-8-sig")
    assert "Ran 368 tests" in test_text and test_text.rstrip().endswith("OK")
    target = FOLDER / "execution-370-python-tests.txt"
    assert not target.exists()
    target.write_bytes(test_raw)
    audit_record = load(FOLDER / "batch-061-draft-audit.json")
    ledger = load(FOLDER / "batch-061-progress.json")
    paths = sorted(
        p for p in (ROOT / "docs" / "n1-sources").glob("batch-061-*") if p.is_file()
    )
    record = {
        "schemaVersion": 1, "execution": 370, "batch": "061",
        "startingHead": BASE, "stage": "validated-unreviewed-draft-awaiting-signed-snapshot",
        "recordedAt": datetime.now().astimezone().isoformat(),
        "authorization": load(CONTROL / "execution-370-start.json")["authorization"],
        "membership": ["俳"], "sourceRow": 54,
        "actualDraftCounts": audit_record["actualDraftCounts"],
        "teachingScope": {
            "newCards": ["kanji/俳.md"], "generatedStrokes": ["strokes/俳.json"],
            "changedReusedPassages": ledger["changedReusedPassages"],
            "newWords": [], "changedMetadataOnExistingCardsOrWords": [],
            "requiredReciprocalPairs": ledger["requiredReciprocalPairs"],
            "unavailableMappedPairs": ledger["unavailableMappedPairs"],
            "fullOn": ["ハイ"], "fullKun": [], "offeredOnKeys": ["はい"], "offeredKunKeys": [],
        },
        "coordinatorInspection": ledger["authorInspection"],
        "sourcePacketHashes": {p.relative_to(ROOT).as_posix(): digest(p.read_bytes()) for p in paths},
        "checks": {
            "validatorErrors": 0, "manifestFresh": True,
            "runtimeHashesVerified": 8311, "contentVersion": "d01d660cc41262fe",
            "baselinePreserved": audit_record["baselineMetadataAndStrokesChecked"],
            "newBaselineMetadataExceptions": [],
            "pythonTests": 368, "pythonTestFailures": 0, "pythonTestErrors": 0,
            "pythonTestLog": target.relative_to(ROOT).as_posix(), "pythonTestLogSha256": digest(test_raw),
            "testOutputQualification": "Generated-media and429 messages are synthetic test-fixture output, not authorized media generation or an upstream failure; exact runtime delta was checked separately.",
            "grammarVocabularyConsistency": "passed; unchanged pilot coverage2122/2431, not a claim that missing baseline coverage is fixed",
            "exactFrozenDictionaryReextraction": 45, "frozenInputHashes": 5,
            "decompressedDictionaryHashes": 2, "allMappedReciprocalPairs": 3,
            "generatedStrokeCount": 10, "unchangedArchiveBudgets": audit_record["budget"],
            "actualAuthoredHan": 33, "bundledFontMissingUnion": ["亻"],
            "dedicatedAndroidHead": "f9b59a2bc5a203c6b4de26be50021a4c720dc22c",
            "dedicatedAndroidClean": True,
        },
        "independentReview": "not-started; two serial blind different-family initial reviewers pending on the commit containing this record",
        "androidNativePhoneAcceptance": "not-performed for061; original accepted060 retained, not substituted for061 evidence",
        "publishedAdditions": 87, "remainingAdditions": 1141,
        "necessarySupportingWordAdditionsPublished": 89, "pushed": False,
        "nextAction": "Two serial blind initial reviews on one normally signed draft snapshot; current actual model catalog and identities, one active reviewer and serial internaltools. Reconcile all facets and exact reused diffs, then applicable fresh Android/native/font/combinedmain/signing/ownerpush/CI/publicZIP gates. No062 before061 publication.",
        "limits": ledger["limits"],
    }
    save(FOLDER / "execution-370.json", record)
    print("Durable execution370 draft evidence and complete368-test output archived.")


def checkpoint():
    progress_path = CONTROL / "progress.json"
    progress = load(progress_path)
    original = load(CONTROL / "execution-370-starting-progress.json")
    assert progress["checkpoint"] == original["checkpoint"] == 369
    assert progress["status"] == "continue" and progress["batch"] == "061"
    assert progress["lastPublishedCommit"] == BASE and progress["remainingAdditions"] == 1141
    head = git("rev-parse", "HEAD")
    assert head != BASE and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert git("rev-parse", "origin/main") == BASE
    assert load(ROOT / "manifest.json") == build_manifest(ROOT)
    receipt = load(CONTROL / "execution-370-issue-receipt.json")
    assert receipt["user"]["login"] == "stop-cran" and receipt["html_url"].startswith(
        "https://github.com/stop-cran/learning-japanese/issues/60#issuecomment-")
    assert head in receipt["body"]
    allowed = {"stage", "batch", "nextAction"}
    for key, value in original.items():
        if key not in allowed:
            assert progress[key] == value, key
    assert set(progress) - set(original) == {"execution370StartingState"}
    save(CONTROL / "execution-370-precheckpoint-progress.json", progress)
    record = {
        "execution": 370, "checkpoint": 370, "batch": "061",
        "status": "signed-validated-unreviewed-draft",
        "startingHead": BASE, "savedCommit": head, "signature": "G",
        "recordedAt": datetime.now().astimezone().isoformat(),
        "sourceRow": 54, "membership": ["俳"],
        "draftAudit": "docs/n1-sources/batch-061-draft-audit.json",
        "durableExecutionEvidence": "docs/n1-sources/execution-370.json",
        "independentInitialReviews": "not-started",
        "freshAndroid": "not-started", "native": "not-started",
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "runtimeHashesVerified": 8311, "pythonTestsPassed": 368,
        "localDraftAdditions": 88, "publishedAdditions": 87,
        "remainingAdditions": 1141, "necessarySupportingWordAdditionsPublished": 89,
        "contentWorktreeClean": True, "dedicatedAndroidClean": True,
        "pushed": False, "nextBatchStarted": False,
        "limits": load(FOLDER / "batch-061-progress.json")["limits"],
    }
    progress["checkpoint"] = 370
    progress["status"] = "continue"
    progress["stage"] = "batch-061-signed-unreviewed-draft-awaiting-two-family-initials"
    progress["batch"] = "061"
    progress["blocker"] = None
    progress["nextAction"] = (
        f"SAME061 signedG draft {head}; published main remains{BASE}. "
        "Read complete request/finalcheckpoint and scoped live keys; preserve FULL history. "
        "Review complete俳 card, exact俳句/俳優/優 reused diffs and all source/reading/quiz/link decisions "
        "on ONE frozen snapshot via TWO serialblind different actual model families, at mostONE active reviewer "
        "and strictly serial internaltool calls; obtain current CLIcatalog/actualidentities and retain completeoriginalreports/"
        "executionaudits before next launch. No authoragents.45full frozenfamilies,7rawcharacters,17olderarticles "
        "coordinator-inspected; sourceinspection NOT independentreview. Solefull/curatedハイ;noKun. "
        "No newwordarticles; preserve俳句N2/俳優N3/allmetadata/exclusions. "
        "Two activatedbaselinepairs plus優/俳優 =3reciprocalpairs/6links;句cardabsent disposition explicit. "
        "Pinned10strokes/16points;8311runtimehashes;368Pythontests/validator/manifest/vocabularyconsistency/"
        "baseline985/4942/985/originalbudgets passed.33authoredHan cmaps missing亻only; "
        "nativeglyphreadability NOT yettested. Newwrongchoices非/悲/借;優actor and芸/演performance not used. "
        "Reconcile allfacets with justified originalsessions, then applicable fresh non-skippedAndroid3+1/native/"
        "visual/font/currentmain/normalsigning/ownerfastforward/greenCI/everyimmutablepublicZIPhash gates. "
        "Public87/1228;1141remaining;89necessarysupportwords;local88draftadditions NOT delivered. "
        "Androidf9b59a2+ required;physical-phone/general-release/whole-set outstanding. "
        "Original060accepted evidence/historicalprocesslimits unchanged; no repeatabsentanewconcern. "
        "No unreviewedpush/062/concurrentheavywork/secondrunner/signingretry/permissionworkaround. Overalltaskincomplete."
    )
    progress["execution370StartingState"]["status"] = "signed-draft-checkpoint-complete"
    progress["batch061DraftCheckpoint"] = record
    progress["execution370CoordinatorCheckpoint"] = dict(record)
    save(progress_path, progress)
    restored = load(progress_path)
    exceptions = allowed | {"checkpoint", "status", "blocker"}
    for key, value in original.items():
        if key not in exceptions:
            assert restored[key] == value, key
    verification = {
        "schemaVersion": 1, "checkpoint": 370, "savedCommit": head, "signature": "G",
        "allOriginalHistoricalKeysPreservedExactly": True,
        "originalTopLevelKeys": len(original), "currentTopLevelKeys": len(restored),
        "cleanLocalSignedDraft": True, "publishedMainUnchanged": BASE,
        "projectCompleted": False, "status": "continue", "issueUpdate": receipt["html_url"],
    }
    save(CONTROL / "execution-370-final-verification.json", verification)
    print(json.dumps(verification, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    {"start": start, "prepare": prepare, "strokes": strokes, "audit": audit,
     "evidence": evidence, "checkpoint": checkpoint}[sys.argv[1]]()

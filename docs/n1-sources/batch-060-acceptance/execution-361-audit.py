import gzip
import hashlib
import json
import math
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

CONTROL = Path(__file__).resolve().parent
ROOT = CONTROL.parent / "learning-japanese"
FOLDER = ROOT / "docs" / "n1-sources"
BASE = "48d7110f893a2700dce2f73c5f14653b19b1a14d"
SOURCE = "38cf5e64ac41b65d194fd4137193ef0996c941f0"
sys.path.insert(0, str(ROOT / "tools"))
from audit_n1_batch import base_file, lexical_pair, reused_changes, runtime_delta
from audit_n1_pilot import metadata, offered_keys, quiz_readings
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


def text(name):
    return (ROOT / name).read_text(encoding="utf-8")


def strokes():
    row = load(FOLDER / "batch-060-input-metadata.json")["sourceIndexRecord"]
    svg = (CONTROL / "inputs" / "n1-04ead-70a0b7ae.svg").read_bytes()
    blob = hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest()
    assert len(svg) == row["kanjivgInventory"]["size"] == 3780
    assert blob == row["kanjivgInventory"]["sha"]
    snapshot = load(ROOT / "docs" / "n1-source-snapshot.json")
    converter_hash = digest((ROOT / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n"))
    assert converter_hash == snapshot["kanjivg"]["converter"]["normalizedSha256"]
    data = convert("亭", svg.decode("utf-8"))
    assert data["strokeCount"] == row["metadata"]["strokes"] == 9
    target = ROOT / "strokes" / "亭.json"
    assert not target.exists()
    target.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    record = {
        "schemaVersion": 1, "batch": "060", "character": "亭",
        "sourceUrl": "https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/kanji/04ead.svg",
        "sourceRevision": data["sourceRevision"], "sourceBytes": len(svg),
        "gitBlob": blob, "sourceSha256": digest(svg),
        "sourceLocalPath": "control/inputs/n1-04ead-70a0b7ae.svg",
        "converter": "tools/generate_strokes.py:convert; unchanged pinned converter",
        "converterNormalizedSha256": converter_hash,
        "target": "strokes/亭.json", "targetSha256": digest(target.read_bytes()),
        "strokeCount": 9, "pointsPerStroke": 16,
        "dictionaryAndSvgCountAgreement": True,
        "license": "KanjiVG CC BY-SA 3.0; generated file retains attribution.",
        "limits": "Actual pinned SVG conversion, not native drawing recognition, glyph inspection or phone evidence. SVG component annotations are not adopted historical/phonetic teaching.",
    }
    save(FOLDER / "batch-060-stroke-evidence.json", record)
    print(json.dumps(record, ensure_ascii=False, indent=2))


def audit():
    ledger = load(FOLDER / "batch-060-progress.json")
    frozen = load(FOLDER / "batch-060-membership.json")
    assert ledger["baseCommit"] == frozen["baseCommit"] == BASE
    assert ledger["membership"] == ledger["drafted"] == frozen["membership"] == ["亭"]
    assert ledger["reviewClosed"] == ledger["published"] == []
    snapshot = load(ROOT / "docs" / "n1-source-snapshot.json")
    for name, row in snapshot["inputs"].items():
        assert digest((CONTROL / "inputs" / name).read_bytes()) == row["sha256"]
    dictionary = (CONTROL / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    kd = gzip.decompress((CONTROL / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes())
    assert digest(kd) == snapshot["kanjidic2"]["xmlSha256"]
    assert digest(gzip.decompress(dictionary)) == snapshot["jmdict"]["xmlSha256"]
    families, packets = {}, []
    for packet in ledger["dictionaryPackets"]:
        ids = load(FOLDER / packet["selection"])["entryIds"]
        raw = (FOLDER / packet["xml"]).read_bytes()
        assert raw == extract(dictionary, digest(dictionary), ids)
        entries = ET.fromstring(raw).findall("entry")
        assert [e.findtext("ent_seq") for e in entries] == ids
        assert not families.keys() & set(ids)
        families.update(zip(ids, entries))
        packets.append({"path": packet["xml"], "families": len(entries), "sha256": digest(raw)})
    assert len(families) == 51
    immutable = [
        "docs/n1-source-snapshot.json", "docs/n1-sources/source-index.json",
        "docs/n1-sources/baseline-inventory.json", "docs/n1-sources/baseline-word-candidates.json",
        *[f"docs/n1-sources/batch-060-{suffix}" for suffix in (
            "membership.json", "input-metadata.json", "preparation-audit.json",
            "kanjidic2.xml", "lexical-selection.json", "comparison-selection.json",
            "jmdict.xml", "comparison-jmdict.xml", "source-evidence.json")],
    ]
    for name in immutable:
        assert (ROOT / name).read_bytes() == subprocess.check_output(
            ["git", "--no-pager", "show", f"{SOURCE}:{name}"], cwd=ROOT), name
    row = load(FOLDER / "batch-060-input-metadata.json")["sourceIndexRecord"]
    assert row == next(r for r in load(FOLDER / "source-index.json") if r["kanji"] == "亭")
    named = load(CONTROL / "inputs" / "n1-kanji-source-20261102.json")
    assert len(named) == len(set(named)) == 1232 and named[row["sourceRow"] - 1] == "亭"
    raw_source = ET.fromstring(kd)
    packet = ET.parse(FOLDER / "batch-060-kanjidic2.xml").getroot()
    chars = {e.findtext("literal") for e in packet.findall("character")}
    expected = ET.Element("kanjidic2")
    expected.append(raw_source.find("header"))
    for element in raw_source.findall("character"):
        if element.findtext("literal") in chars:
            expected.append(element)
    ET.indent(expected, space="  ")
    assert len(chars) == 6
    assert (FOLDER / "batch-060-kanjidic2.xml").read_bytes() == ET.tostring(expected, encoding="utf-8", xml_declaration=True) + b"\n"
    manifest = load(ROOT / "manifest.json")
    assert manifest == build_manifest(ROOT)
    before = json.loads(base_file(ROOT, BASE, "manifest.json"))
    additions = {"kanji/亭.md", "strokes/亭.json", "words/料亭.md"}
    changes = {"kanji/料.md", "kanji/停.md"}
    runtime_delta(before, manifest, additions, changes)
    all_hashes = 0
    for section, entries in manifest.items():
        if isinstance(entries, dict):
            for name, expected_hash in entries.items():
                path = ROOT / name
                actual = digest(path.read_bytes()) if section in {
                    "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(path)
                assert actual == expected_hash, name
                all_hashes += 1
    assert all_hashes == 8309
    for name in changes:
        edits = [r for r in ledger["changedReusedPassages"] if r["article"] == name]
        reused_changes(base_file(ROOT, BASE, name).replace("\r\n", "\n"), text(name), edits)
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
            expected_meta = dict(record["metadata"])
            expected_meta.update(exceptions.get(name, {}))
            assert metadata(ROOT, name) == expected_meta, name
            counts[kind] += 1
        elif kind == "strokes":
            assert digest((ROOT / name).read_bytes()) == record["sha256"], name
            counts[kind] += 1
    assert counts == {"kanji": 985, "words": 4942, "strokes": 985}
    pairs = {(r["kanji"], r["article"]) for r in ledger["supportMappings"]}
    assert len(pairs) == len(ledger["supportMappings"]) == 2
    assert pairs == set(map(tuple, ledger["requiredReciprocalPairs"])) == {
        ("亭", "words/料亭.md"), ("料", "words/料亭.md")}
    for mapping in ledger["supportMappings"]:
        char, name = mapping["kanji"], mapping["article"]
        m = metadata(ROOT, name)
        assert char in m["kanji"] and m["reading"] == mapping["primaryReading"]
        assert mapping["newArticle"] and name in additions
        assert any(lexical_pair(families[i], m["word"], m["reading"]) for i in mapping["entryIds"])
        assert f"(../kanji/{char}.md)" in text(name) and f"(../{name})" in text(f"kanji/{char}.md")
    assert [r for r in load(FOLDER / "baseline-word-candidates.json") if r["kanji"] == "亭"] == ledger["baselineCandidatePairs"] == []
    current_pairs = {("亭", p.relative_to(ROOT).as_posix()) for p in (ROOT / "words").glob("*.md")
                     if "亭" in metadata(ROOT, p.relative_to(ROOT).as_posix()).get("kanji", [])}
    assert current_pairs == {("亭", "words/料亭.md")}
    meta = metadata(ROOT, "kanji/亭.md")
    for key in ("kanji", "strokes", "radical", "radicalNumber", "onyomi", "kunyomi"):
        assert meta[key] == row["metadata"][key]
    assert meta["jlpt"] == 1 and {"jlpt-n1", "grade-8", "structure-unclassified"} <= set(meta["tags"])
    assert "phonetic" not in meta
    assert [(r["kind"], r["reading"]) for r in ledger["readingDispositions"]] == [("on", "テイ"), ("on", "チン")]
    table = text("kanji/亭.md").split("## Readings\n", 1)[1].split("## Common words", 1)[0]
    projection = ledger["curatedProjection"][0]
    for kind, field, keys in (("on", "onyomi", "onKeys"), ("kun", "kunyomi", "kunKeys")):
        selected = [r["reading"] for r in ledger["readingDispositions"] if r["kind"] == kind and r["selected"]]
        assert quiz_readings(meta, field) == selected == projection["quiz" + field[0].upper() + field[1:]]
        assert offered_keys(selected) == projection[keys]
    for decision in ledger["readingDispositions"]:
        assert decision["reason"].strip() and set(decision["entryIds"]) <= families.keys()
        lines = [line for line in table.splitlines() if line.startswith(f"| {decision['reading']} |")]
        assert len(lines) == 1 and not decision["sourceOnly"]
        if decision["selected"]:
            assert (decision["kanji"], decision["article"]) in pairs and f"(../{decision['article']})" in lines[0]
        else:
            assert decision["recognitionOnly"] and "亭 ちん" in lines[0] and "recognition" in lines[0]
    quiz = ledger["quizAudit"]["亭"]
    assert meta["title"] == quiz["title"] and meta["distractors"] == quiz["distractors"]
    assert len(set(meta["distractors"])) == 3
    assert quiz["labels"] == [metadata(ROOT, f"kanji/{c}.md")["title"] for c in meta["distractors"]]
    word = metadata(ROOT, "words/料亭.md")
    assert "jlpt" not in word and not any(t.startswith("jlpt-") for t in word["tags"])
    assert word["title"] == ledger["wordQuizAudit"]["title"] and word["reading"] == "りょうてい"
    assert word["quiz_exclusions"] == ledger["wordQuizAudit"]["directExclusions"][0]["exclude"] == ["レストラン", "食堂"]
    for guard in ledger["wordQuizAudit"]["pairEvidence"]:
        m = metadata(ROOT, f"words/{guard['neighbor']}.md")
        entry = families[guard["entry"]]
        assert m["reading"] in [r.findtext("reb") for r in entry.findall("r_ele")]
        assert entry.findall("sense")[guard["sense"] - 1] is not None
    svg = (CONTROL / "inputs" / "n1-04ead-70a0b7ae.svg").read_bytes()
    geometry = load(FOLDER / "batch-060-stroke-evidence.json")
    assert len(svg) == row["kanjivgInventory"]["size"] == 3780
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == row["kanjivgInventory"]["sha"]
    assert digest(svg) == geometry["sourceSha256"]
    strokes = load(ROOT / "strokes" / "亭.json")
    assert strokes == convert("亭", svg.decode("utf-8"))
    assert strokes["strokeCount"] == len(strokes["strokes"]) == 9
    for stroke in strokes["strokes"]:
        assert len(stroke["points"]) == 16
        assert all(len(p) == 2 and all(math.isfinite(v) and 0 <= v <= 109 for v in p) for p in stroke["points"])
    assert digest((ROOT / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")) == snapshot["kanjivg"]["converter"]["normalizedSha256"]
    authored = sorted(changes | {"kanji/亭.md", "words/料亭.md"})
    han = sorted(set(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]", "\n".join(text(n) for n in authored))))
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
        m = metadata(ROOT, path.relative_to(ROOT).as_posix())
        if len(m.get("distractors", [])) < 3:
            legacy.append({key: m[key] for key in ("kanji", "title", "distractors")})
    assert [r["kanji"] for r in legacy] == ["人", "休", "何", "入", "出", "口", "女", "日", "月", "男", "買"]
    current = {
        "kanji": len(list((ROOT / "kanji").glob("*.md"))),
        "words": len(list((ROOT / "words").glob("*.md"))),
        "n1Labelled": sum(metadata(ROOT, p.relative_to(ROOT).as_posix())["jlpt"] == 1 for p in (ROOT / "kanji").glob("*.md")),
        "namedSourceMembersPresent": sum((ROOT / "kanji" / f"{c}.md").exists() for c in named),
    }
    assert current == {"kanji": 1072, "words": 5031, "n1Labelled": 92, "namedSourceMembersPresent": 91}
    assert metadata(ROOT, "kanji/妖.md")["jlpt"] == 1
    result = {
        "schemaVersion": 1, "execution": 361, "batch": "060",
        "status": "local-unreviewed-runtime-draft", "baseCommit": BASE, "sourceCheckpoint": SOURCE,
        "frozenInputHashesVerified": 5, "decompressedDictionaryHashesVerified": 2,
        "exactFrozenFamilyExtractions": 51, "dictionaryPackets": packets,
        "coordinatorInspection": ledger["draftInspection"], "namedSourceRow": row["sourceRow"],
        "immutableEvidenceUnchanged": immutable, "baselineMetadataAndStrokesChecked": counts,
        "explicitBaselineMetadataExceptions": exceptions, "newBaselineMetadataExceptions": [],
        "runtimePayloadHashesVerified": all_hashes, "baseRuntimeHashesUnchanged": 8304,
        "runtimeAdditions": sorted(additions), "changedReusedRuntimePayloads": sorted(changes),
        "manifestFresh": True, "contentVersion": manifest["contentVersion"], "actualDraftCounts": current,
        "requiredReciprocalPairs": 2, "directedLinks": 4, "activatedBaselinePairs": 0,
        "fullReadingDispositions": 2, "offeredKeys": ["てい"], "sourceOnlyOfferedKeys": [],
        "directWordExclusions": 2, "originalWordGuardsPreserved": True,
        "legacyFallbackCandidatesWithFewerThanThree": legacy,
        "legacyFallbackDisposition": "All eleven titles inspected: person/rest/what/enter/go-out/mouth/woman/sun/moon/man/buy are not the pavilion or restaurant-building meanings. Rest is an action/state, not the resting structure. No new default four-choice repair established; larger/live pools unverified.",
        "geometry": geometry,
        "actualAuthoredHanFonts": {
            "articles": authored, "characters": han, "count": len(han), "fonts": fonts,
            "missingUnion": sorted({c for r in fonts for c in r["missing"]}),
            "limits": "Complete new and changed reused articles included. Cmap presence is not native readability, fallback-face or phone evidence.",
        },
        "budget": check(ROOT, archive_names(ROOT)),
        "publishedAdditions": 86, "remainingAdditions": 1142, "limits": ledger["limits"],
    }
    save(FOLDER / "batch-060-draft-audit.json", result)
    print(json.dumps({k: result[k] for k in (
        "actualDraftCounts", "contentVersion", "actualAuthoredHanFonts",
        "legacyFallbackCandidatesWithFewerThanThree", "budget")}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    {"strokes": strokes, "audit": audit}[sys.argv[1]]()

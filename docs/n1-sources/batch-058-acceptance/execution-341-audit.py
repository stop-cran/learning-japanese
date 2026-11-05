import gzip
import hashlib
import json
import math
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

CONTROL = Path(__file__).resolve().parent
ROOT = CONTROL.parent / "learning-japanese"
FOLDER = ROOT / "docs" / "n1-sources"
BASE = "c064f0c749bdc93bc1f86dbd01cec19212991bd7"
SOURCE = "c7a204576667efb63e8cd3e1b4c55773f174b406"
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


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def text(name):
    return (ROOT / name).read_text(encoding="utf-8")


ledger = load(FOLDER / "batch-058-progress.json")
membership = load(FOLDER / "batch-058-membership.json")
assert ledger["membership"] == ledger["drafted"] == membership["membership"] == ["丘"]
assert ledger["reviewClosed"] == ledger["published"] == []
assert ledger["baseCommit"] == membership["baseCommit"] == BASE
snapshot = load(ROOT / "docs" / "n1-source-snapshot.json")
for name, record in snapshot["inputs"].items():
    assert digest((CONTROL / "inputs" / name).read_bytes()) == record["sha256"], name
dictionary = (CONTROL / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
raw_kd = gzip.decompress((CONTROL / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes())
assert digest(raw_kd) == snapshot["kanjidic2"]["xmlSha256"]
assert digest(gzip.decompress(dictionary)) == snapshot["jmdict"]["xmlSha256"]
families = {}
packets = []
for packet in ledger["dictionaryPackets"]:
    selection = load(FOLDER / packet["selection"])
    raw = (FOLDER / packet["xml"]).read_bytes()
    assert raw == extract(dictionary, digest(dictionary), selection["entryIds"])
    entries = ET.fromstring(raw).findall("entry")
    assert [entry.findtext("ent_seq") for entry in entries] == selection["entryIds"]
    assert not families.keys() & set(selection["entryIds"])
    families.update(zip(selection["entryIds"], entries))
    packets.append({"path": packet["xml"], "families": len(entries), "sha256": digest(raw)})
assert len(families) == 68
assert set(ledger["draftInspection"]["freshCompleteFamilies"]) <= families.keys()
raw_source = ET.fromstring(raw_kd)
for packet_name in ("batch-058-kanjidic2.xml", "batch-058-draft-kanjidic2.xml"):
    packet = ET.parse(FOLDER / packet_name).getroot()
    chars = {entry.findtext("literal"): entry for entry in packet.findall("character")}
    expected = ET.Element("kanjidic2")
    expected.append(raw_source.find("header"))
    for entry in raw_source.findall("character"):
        if entry.findtext("literal") in chars:
            expected.append(entry)
    ET.indent(expected, space="  ")
    assert (FOLDER / packet_name).read_bytes() == ET.tostring(expected, encoding="utf-8", xml_declaration=True) + b"\n"
source_row = next(row for row in load(FOLDER / "source-index.json") if row["kanji"] == "丘")
named = load(CONTROL / "inputs" / "n1-kanji-source-20261102.json")
assert len(named) == len(set(named)) == 1232 and named[source_row["sourceRow"] - 1] == "丘"
assert source_row["sourceRow"] == 4
assert source_row == load(FOLDER / "batch-058-input-metadata.json")["sourceIndexRecord"]
immutable = [
    "docs/n1-source-snapshot.json", "docs/n1-sources/source-index.json",
    "docs/n1-sources/baseline-inventory.json", "docs/n1-sources/baseline-word-candidates.json",
    *[f"docs/n1-sources/batch-058-{suffix}" for suffix in (
        "membership.json", "input-metadata.json", "preparation-audit.json", "kanjidic2.xml",
        "lexical-selection.json", "comparison-selection.json", "jmdict.xml", "comparison-jmdict.xml",
        "source-evidence.json", "execution-340-source-checkpoint.json")],
]
for name in immutable:
    expected = subprocess.check_output(["git", "--no-pager", "show", f"{SOURCE}:{name}"], cwd=ROOT)
    assert (ROOT / name).read_bytes() == expected, name
manifest = load(ROOT / "manifest.json")
assert manifest == build_manifest(ROOT)
before = json.loads(base_file(ROOT, BASE, "manifest.json"))
additions = {"kanji/丘.md", "words/砂丘.md", "strokes/丘.json"}
changes = {"words/丘.md", "kanji/砂.md", "kanji/山.md"}
runtime_delta(before, manifest, additions, changes)
all_hashes = 0
for section, entries in manifest.items():
    if isinstance(entries, dict):
        for name, expected in entries.items():
            path = ROOT / name
            actual = digest(path.read_bytes()) if section in {
                "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(path)
            assert actual == expected, name
            all_hashes += 1
assert all_hashes == 8303
for name in changes:
    old, new = base_file(ROOT, BASE, name).replace("\r\n", "\n"), text(name)
    rows = [r for r in ledger["changedReusedPassages"] if r["article"] == name]
    if name == "kanji/山.md":
        assert len(rows) == 1
        assert old.count(rows[0]["before"]) == 1 and old.replace(rows[0]["before"], rows[0]["after"], 1) == new
        old_meta = metadata(ROOT, name).copy()
        assert old_meta["distractors"] == ["川", "出", "木"]
        old_meta["distractors"] = ["川", "出"]
        assert old_meta == yaml.safe_load(old.split("---", 2)[1])
    else:
        exclusions = ["坂", "山"] if name == "words/丘.md" else None
        reused_changes(old, new, rows, exclusions)
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
    ("丘", "words/丘.md"), ("丘", "words/砂丘.md"), ("砂", "words/砂丘.md")}
for mapping in ledger["supportMappings"]:
    char, name = mapping["kanji"], mapping["article"]
    meta = metadata(ROOT, name)
    assert char in meta["kanji"] and meta["reading"] == mapping["primaryReading"]
    assert bool(mapping["newArticle"]) == (name in additions)
    assert any(lexical_pair(families[entry], meta["word"], meta["reading"]) for entry in mapping["entryIds"])
    assert f"(../kanji/{char}.md)" in text(name)
    assert f"(../{name})" in text(f"kanji/{char}.md")
activated = {(row["kanji"], row["article"]) for row in load(FOLDER / "baseline-word-candidates.json") if row["kanji"] == "丘"}
assert activated == {("丘", "words/丘.md")} <= pairs
meta = metadata(ROOT, "kanji/丘.md")
for key in ("kanji", "strokes", "radical", "radicalNumber", "onyomi", "kunyomi"):
    assert meta[key] == source_row["metadata"][key]
assert meta["jlpt"] == 1 and {"jlpt-n1", "grade-8", "structure-unclassified"} <= set(meta["tags"])
assert "phonetic" not in meta
table = text("kanji/丘.md").split("## Readings\n", 1)[1].split("## Common words", 1)[0]
assert [(r["kind"], r["reading"]) for r in ledger["readingDispositions"]] == [("on", "キュウ"), ("kun", "おか")]
projection = ledger["curatedProjection"][0]
for kind, field, keys in (("on", "onyomi", "onKeys"), ("kun", "kunyomi", "kunKeys")):
    assert quiz_readings(meta, field) == meta[field] == projection["quiz" + field[0].upper() + field[1:]]
    assert offered_keys(meta[field]) == projection[keys]
for row in ledger["readingDispositions"]:
    assert row["selected"] and not row["sourceOnly"] and row["reason"].strip()
    assert (row["kanji"], row["article"]) in pairs and set(row["entryIds"]) <= families.keys()
    lines = [line for line in table.splitlines() if line.startswith(f"| {row['reading']} |")]
    assert len(lines) == 1 and f"(../{row['article']})" in lines[0]
quiz = ledger["quizAudit"]["丘"]
assert meta["title"] == quiz["title"] and meta["distractors"] == quiz["distractors"]
assert len(set(meta["distractors"])) == 3
assert quiz["labels"] == [metadata(ROOT, f"kanji/{char}.md")["title"] for char in meta["distractors"]]
word_pairs = set()
for row in ledger["wordQuizAudit"]["directExclusions"]:
    assert metadata(ROOT, f"words/{row['word']}.md")["quiz_exclusions"] == row["exclude"]
    word_pairs.update(frozenset((row["word"], excluded)) for excluded in row["exclude"])
assert len(word_pairs) == 5
assert metadata(ROOT, "words/丘.md")["reading"] == "おか" and metadata(ROOT, "words/丘.md")["jlpt"] == 3
assert "jlpt" not in metadata(ROOT, "words/砂丘.md")
stroke_evidence = load(FOLDER / "batch-058-stroke-evidence.json")
svg = (CONTROL / "inputs" / "batch-058-04e18.svg").read_bytes()
assert len(svg) == source_row["kanjivgInventory"]["size"] == 2786
assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == source_row["kanjivgInventory"]["sha"]
assert digest(svg) == stroke_evidence["sourceSha256"]
strokes = load(ROOT / "strokes" / "丘.json")
assert strokes == convert("丘", svg.decode("utf-8"))
assert strokes["strokeCount"] == len(strokes["strokes"]) == 5
for row in strokes["strokes"]:
    assert len(row["points"]) == 16
    assert all(len(point) == 2 and all(math.isfinite(value) and 0 <= value <= 109 for value in point) for point in row["points"])
assert digest((ROOT / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")) == snapshot["kanjivg"]["converter"]["normalizedSha256"]
authored = ["kanji/丘.md", "words/砂丘.md", "words/丘.md", "kanji/砂.md", "kanji/山.md"]
han = sorted(set(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]", "\n".join(text(name) for name in authored))))
android = CONTROL.parent / "kanji-cards-android"
assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=android, text=True).strip() == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
assert not subprocess.check_output(["git", "status", "--porcelain"], cwd=android).strip()
fonts = []
for record in load(FOLDER / "font-coverage.json")["fonts"]:
    path = android / record["path"]
    assert digest(path.read_bytes()) == record["sha256"]
    with TTFont(path) as font:
        cmap = font.getBestCmap()
        missing = [char for char in han if ord(char) not in cmap]
    fonts.append({"path": record["path"], "sha256": record["sha256"], "missing": missing})
legacy = []
for path in sorted((ROOT / "kanji").glob("*.md")):
    m = metadata(ROOT, path.relative_to(ROOT).as_posix())
    if len(m.get("distractors", [])) < 3:
        legacy.append({key: m[key] for key in ("kanji", "title", "distractors")})
assert [row["kanji"] for row in legacy] == ["人", "休", "何", "入", "出", "口", "女", "日", "月", "男", "買"]
current_counts = {
    "kanji": len(list((ROOT / "kanji").glob("*.md"))),
    "words": len(list((ROOT / "words").glob("*.md"))),
    "n1Labelled": sum(metadata(ROOT, p.relative_to(ROOT).as_posix())["jlpt"] == 1 for p in (ROOT / "kanji").glob("*.md")),
    "namedSourceMembersPresent": sum((ROOT / "kanji" / f"{char}.md").exists() for char in named),
}
assert current_counts == {"kanji": 1070, "words": 5029, "n1Labelled": 90, "namedSourceMembersPresent": 89}
assert metadata(ROOT, "kanji/妖.md")["jlpt"] == 1
result = {
    "schemaVersion": 1, "execution": 341, "batch": "058", "status": "local-unreviewed-runtime-draft",
    "baseCommit": BASE, "sourceCheckpoint": SOURCE, "frozenInputHashesVerified": 5, "decompressedDictionaryHashesVerified": 2,
    "freshExactFrozenFamilyExtraction": len(families), "dictionaryPackets": packets,
    "freshLinguisticReviewOfAllFamiliesClaimed": False, "inspectionScope": ledger["draftInspection"],
    "namedSourceRow": 4, "immutableEvidenceUnchanged": immutable,
    "originalBaselineMetadataAndStrokesChecked": counts, "explicitBaselineMetadataExceptions": exceptions,
    "runtimePayloadHashesVerified": all_hashes, "baseRuntimeHashesUnchanged": 8297,
    "runtimeAdditions": sorted(additions), "changedReusedRuntimePayloads": sorted(changes),
    "manifestFresh": True, "contentVersion": manifest["contentVersion"], "actualDraftCounts": current_counts,
    "selectedReciprocalPairs": 3, "directedSelectedLinks": 6, "activatedBaselinePairs": 1,
    "fullReadingDispositions": 2, "curatedOfferedKeys": ["きゅう", "おか"], "sourceOnlyOfferedKeys": [],
    "directWordExclusions": len(word_pairs), "originalWordGuardsPreserved": True,
    "legacyFallbackCandidatesWithFewerThanThree": legacy,
    "legacyFallbackDisposition": ledger["quizAudit"]["丘"]["remainingLegacyFallbackDisposition"],
    "geometry": stroke_evidence,
    "actualAuthoredHanFonts": {"characters": han, "count": len(han), "fonts": fonts,
        "missingUnion": sorted({char for row in fonts for char in row["missing"]}),
        "limits": "Includes full changed reused articles, not just inserted passages. Cmap presence/absence is not native readability/fallback-face or phone evidence."},
    "budget": check(ROOT, archive_names(ROOT)),
    "publishedAdditions": 84, "remainingAdditions": 1144, "limits": ledger["limits"],
}
(FOLDER / "batch-058-draft-audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({key: result[key] for key in (
    "actualDraftCounts", "contentVersion", "actualAuthoredHanFonts", "legacyFallbackCandidatesWithFewerThanThree", "budget")}, ensure_ascii=False, indent=2))

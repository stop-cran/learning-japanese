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
BASE = "633f60022b4c42d5f3a6fa83f85465c39729cedd"
SOURCE = "8f8d2e25e3c33c9b09f642500752459b5fd934ca"
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


ledger = load(FOLDER / "batch-059-progress.json")
membership = load(FOLDER / "batch-059-membership.json")
assert ledger["membership"] == ledger["drafted"] == membership["membership"] == ["享"]
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
    ids = load(FOLDER / packet["selection"])["entryIds"]
    raw = (FOLDER / packet["xml"]).read_bytes()
    assert raw == extract(dictionary, digest(dictionary), ids)
    entries = ET.fromstring(raw).findall("entry")
    assert [entry.findtext("ent_seq") for entry in entries] == ids
    assert not families.keys() & set(ids)
    families.update(zip(ids, entries))
    packets.append({"path": packet["xml"], "families": len(entries), "sha256": digest(raw)})
assert len(families) == ledger["draftInspection"]["freshCompleteFamilies"] == 54
raw_source = ET.fromstring(raw_kd)
packet = ET.parse(FOLDER / "batch-059-kanjidic2.xml").getroot()
chars = {entry.findtext("literal") for entry in packet.findall("character")}
expected = ET.Element("kanjidic2")
expected.append(raw_source.find("header"))
for entry in raw_source.findall("character"):
    if entry.findtext("literal") in chars:
        expected.append(entry)
ET.indent(expected, space="  ")
assert (FOLDER / "batch-059-kanjidic2.xml").read_bytes() == ET.tostring(expected, encoding="utf-8", xml_declaration=True) + b"\n"
row = next(r for r in load(FOLDER / "source-index.json") if r["kanji"] == "享")
named = load(CONTROL / "inputs" / "n1-kanji-source-20261102.json")
assert len(named) == len(set(named)) == 1232 and named[row["sourceRow"] - 1] == "享"
assert row["sourceRow"] == 20
assert row == load(FOLDER / "batch-059-input-metadata.json")["sourceIndexRecord"]
immutable = [
    "docs/n1-source-snapshot.json", "docs/n1-sources/source-index.json",
    "docs/n1-sources/baseline-inventory.json", "docs/n1-sources/baseline-word-candidates.json",
    *[f"docs/n1-sources/batch-059-{suffix}" for suffix in (
        "membership.json", "input-metadata.json", "preparation-audit.json", "kanjidic2.xml",
        "lexical-selection.json", "comparison-selection.json", "supportComparison-selection.json",
        "jmdict.xml", "comparison-jmdict.xml", "support-comparison-jmdict.xml",
        "source-evidence.json", "execution-350-source-checkpoint.json")],
]
for name in immutable:
    assert (ROOT / name).read_bytes() == subprocess.check_output(
        ["git", "--no-pager", "show", f"{SOURCE}:{name}"], cwd=ROOT), name
manifest = load(ROOT / "manifest.json")
assert manifest == build_manifest(ROOT)
before = json.loads(base_file(ROOT, BASE, "manifest.json"))
additions = {"kanji/享.md", "words/享受.md", "strokes/享.json"}
changes = {"kanji/受.md"}
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
assert all_hashes == 8306
reused_changes(base_file(ROOT, BASE, "kanji/受.md").replace("\r\n", "\n"),
               text("kanji/受.md"), ledger["changedReusedPassages"])
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
    ("享", "words/享受.md"), ("受", "words/享受.md")}
for mapping in ledger["supportMappings"]:
    char, name = mapping["kanji"], mapping["article"]
    meta = metadata(ROOT, name)
    assert char in meta["kanji"] and meta["reading"] == mapping["primaryReading"]
    assert mapping["newArticle"] and name in additions
    assert any(lexical_pair(families[i], meta["word"], meta["reading"]) for i in mapping["entryIds"])
    assert f"(../kanji/{char}.md)" in text(name) and f"(../{name})" in text(f"kanji/{char}.md")
activated = [p for p in load(FOLDER / "baseline-word-candidates.json") if p["kanji"] == "享"]
assert activated == ledger["baselineCandidatePairs"] == []
current_pairs = {("享", p.relative_to(ROOT).as_posix()) for p in (ROOT / "words").glob("*.md")
                 if "享" in metadata(ROOT, p.relative_to(ROOT).as_posix()).get("kanji", [])}
assert current_pairs == {("享", "words/享受.md")}
meta = metadata(ROOT, "kanji/享.md")
for key in ("kanji", "strokes", "radical", "radicalNumber", "onyomi", "kunyomi"):
    assert meta[key] == row["metadata"][key]
assert meta["jlpt"] == 1 and {"jlpt-n1", "grade-8", "structure-unclassified"} <= set(meta["tags"])
assert "phonetic" not in meta
table = text("kanji/享.md").split("## Readings\n", 1)[1].split("## Common words", 1)[0]
assert [(r["kind"], r["reading"]) for r in ledger["readingDispositions"]] == [
    ("on", "キョウ"), ("on", "コウ"), ("kun", "う.ける")]
projection = ledger["curatedProjection"][0]
for kind, field, keys in (("on", "onyomi", "onKeys"), ("kun", "kunyomi", "kunKeys")):
    selected = [r["reading"] for r in ledger["readingDispositions"] if r["kind"] == kind and r["selected"]]
    assert quiz_readings(meta, field) == selected == projection["quiz" + field[0].upper() + field[1:]]
    assert offered_keys(selected) == projection[keys]
for decision in ledger["readingDispositions"]:
    assert decision["reason"].strip() and set(decision["entryIds"]) <= families.keys()
    lines = [line for line in table.splitlines() if line.startswith(f"| {decision['reading']} |")]
    assert len(lines) == 1
    if decision["selected"]:
        assert (decision["kanji"], decision["article"]) in pairs and f"(../{decision['article']})" in lines[0]
    elif decision["sourceOnly"]:
        assert "source-only" in lines[0].lower()
    else:
        assert decision["recognitionOnly"] and "生を享ける" in lines[0]
quiz = ledger["quizAudit"]["享"]
assert meta["title"] == quiz["title"] and meta["distractors"] == quiz["distractors"]
assert len(set(meta["distractors"])) == 3
assert quiz["labels"] == [metadata(ROOT, f"kanji/{c}.md")["title"] for c in meta["distractors"]]
word_meta = metadata(ROOT, "words/享受.md")
assert "jlpt" not in word_meta and not any(t.startswith("jlpt-") for t in word_meta["tags"])
assert word_meta["title"] == ledger["wordQuizAudit"]["title"] and word_meta["reading"] == "きょうじゅ"
guards = ledger["wordQuizAudit"]["directExclusions"][0]["exclude"]
assert word_meta["quiz_exclusions"] == guards and len(set(guards)) == 11
assert {r["neighbor"] for r in ledger["wordQuizAudit"]["pairEvidence"]} == set(guards)
for guard in ledger["wordQuizAudit"]["pairEvidence"]:
    m = metadata(ROOT, f"words/{guard['neighbor']}.md")
    entry = families[guard["entry"]]
    if guard["neighbor"] == "もらう":
        assert entry.findtext("r_ele/reb") == m["reading"]
    elif guard["neighbor"] == "いただく":
        assert entry.findtext("r_ele/reb") == m["reading"]
    else:
        assert lexical_pair(entry, m["word"], m["reading"]), guard["neighbor"]
    assert entry.findall("sense")[guard["sense"] - 1] is not None
svg = (CONTROL / "inputs" / "n1-04eab-70a0b7ae.svg").read_bytes()
geometry = load(FOLDER / "batch-059-stroke-evidence.json")
assert len(svg) == row["kanjivgInventory"]["size"] == 3511
assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == row["kanjivgInventory"]["sha"]
assert digest(svg) == geometry["sourceSha256"]
strokes = load(ROOT / "strokes" / "享.json")
assert strokes == convert("享", svg.decode("utf-8"))
assert strokes["strokeCount"] == len(strokes["strokes"]) == 8
for stroke in strokes["strokes"]:
    assert len(stroke["points"]) == 16
    assert all(len(p) == 2 and all(math.isfinite(v) and 0 <= v <= 109 for v in p) for p in stroke["points"])
assert digest((ROOT / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")) == snapshot["kanjivg"]["converter"]["normalizedSha256"]
authored = ["kanji/享.md", "words/享受.md", "kanji/受.md"]
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
current_counts = {
    "kanji": len(list((ROOT / "kanji").glob("*.md"))),
    "words": len(list((ROOT / "words").glob("*.md"))),
    "n1Labelled": sum(metadata(ROOT, p.relative_to(ROOT).as_posix())["jlpt"] == 1 for p in (ROOT / "kanji").glob("*.md")),
    "namedSourceMembersPresent": sum((ROOT / "kanji" / f"{c}.md").exists() for c in named),
}
assert current_counts == {"kanji": 1071, "words": 5030, "n1Labelled": 91, "namedSourceMembersPresent": 90}
assert metadata(ROOT, "kanji/妖.md")["jlpt"] == 1
result = {
    "schemaVersion": 1, "execution": 351, "batch": "059", "status": "local-unreviewed-runtime-draft",
    "baseCommit": BASE, "sourceCheckpoint": SOURCE,
    "frozenInputHashesVerified": 5, "decompressedDictionaryHashesVerified": 2,
    "exactFrozenFamilyExtractions": len(families), "dictionaryPackets": packets,
    "coordinatorInspection": ledger["draftInspection"], "namedSourceRow": 20,
    "immutableEvidenceUnchanged": immutable, "baselineMetadataAndStrokesChecked": counts,
    "explicitBaselineMetadataExceptions": exceptions, "newBaselineMetadataExceptions": [],
    "runtimePayloadHashesVerified": all_hashes, "baseRuntimeHashesUnchanged": 8302,
    "runtimeAdditions": sorted(additions), "changedReusedRuntimePayloads": sorted(changes),
    "manifestFresh": True, "contentVersion": manifest["contentVersion"], "actualDraftCounts": current_counts,
    "requiredReciprocalPairs": 2, "directedLinks": 4, "activatedBaselinePairs": 0,
    "fullReadingDispositions": 3, "offeredKeys": ["きょう"], "sourceOnlyOfferedKeys": [],
    "directWordExclusions": 11, "originalWordGuardsPreserved": True,
    "legacyFallbackCandidatesWithFewerThanThree": legacy,
    "legacyFallbackDisposition": "All eleven titles inspected: person/rest/what/enter/go-out/mouth/woman/sun/moon/man/buy are not receiving or enjoyment meanings. No new default four-choice repair established; larger/live pools unverified.",
    "geometry": geometry,
    "actualAuthoredHanFonts": {"characters": han, "count": len(han), "fonts": fonts,
        "missingUnion": sorted({c for r in fonts for c in r["missing"]}),
        "limits": "Includes complete new and changed reused articles. Cmap presence is not native readability, fallback-face or phone evidence."},
    "budget": check(ROOT, archive_names(ROOT)),
    "publishedAdditions": 85, "remainingAdditions": 1143, "limits": ledger["limits"],
}
(FOLDER / "batch-059-draft-audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: result[k] for k in (
    "actualDraftCounts", "contentVersion", "actualAuthoredHanFonts", "legacyFallbackCandidatesWithFewerThanThree", "budget")}, ensure_ascii=False, indent=2))

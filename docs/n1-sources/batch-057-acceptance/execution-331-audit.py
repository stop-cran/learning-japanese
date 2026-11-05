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
BASE = "e8dc74eba6a783552f069593c6fc1d3849986293"
SOURCE = "a3edef2d787e35180fd482946c2429b259d42d04"
sys.path.insert(0, str(ROOT / "tools"))
from audit_n1_batch import audit
from audit_n1_pilot import metadata
from build_manifest import build_manifest, sha256
from check_content_budget import archive_names, check
from extract_n1_jmdict import extract
from fontTools.ttLib import TTFont
from generate_strokes import convert


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def git(*args):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=ROOT, encoding="utf-8").strip()


ledger = load(FOLDER / "batch-057-progress.json")
mechanical = audit(ROOT, "057")
snapshot = load(ROOT / "docs" / "n1-source-snapshot.json")
for name, record in snapshot["inputs"].items():
    assert digest((CONTROL / "inputs" / name).read_bytes()) == record["sha256"], name
for name, key in [
    ("n1-planning-kanjidic2.xml.gz", "kanjidic2"),
    ("n1-implementation-JMdict_e.gz", "jmdict"),
]:
    assert digest(gzip.decompress((CONTROL / "inputs" / name).read_bytes())) == snapshot[key]["xmlSha256"]
dictionary = (CONTROL / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
families = set()
packets = []
for packet in ledger["dictionaryPackets"]:
    selection = load(FOLDER / packet["selection"])
    raw = (FOLDER / packet["xml"]).read_bytes()
    assert raw == extract(dictionary, digest(dictionary), selection["entryIds"])
    assert not families.intersection(selection["entryIds"])
    families.update(selection["entryIds"])
    packets.append({"path": packet["xml"], "families": len(selection["entryIds"]), "sha256": digest(raw)})
assert len(families) == 194
assert set(ledger["draftInspection"]["freshCompleteFamilies"]) <= families
source_row = next(row for row in load(FOLDER / "source-index.json") if row["kanji"] == "企")
named = load(CONTROL / "inputs" / "n1-kanji-source-20261102.json")
assert len(named) == len(set(named)) == 1232 and named[source_row["sourceRow"] - 1] == "企"
assert source_row["sourceRow"] == 27
raw_characters = ET.parse(FOLDER / "batch-057-kanjidic2.xml").getroot()
raw_character = next(row for row in raw_characters.findall("character") if row.findtext("literal") == "企")
assert [row.text for row in raw_character.findall("reading_meaning/rmgroup/reading[@r_type='ja_on']")] == ["キ"]
assert [row.text for row in raw_character.findall("reading_meaning/rmgroup/reading[@r_type='ja_kun']")] == ["くわだ.てる", "たくら.む"]
assert [row.text for row in raw_character.findall("misc/stroke_count")] == ["6"]
immutable = [
    "docs/n1-source-snapshot.json", "docs/n1-sources/source-index.json",
    "docs/n1-sources/baseline-inventory.json", "docs/n1-sources/baseline-word-candidates.json",
    *[f"docs/n1-sources/batch-057-{name}" for name in (
        "membership.json", "input-metadata.json", "preparation-audit.json", "kanjidic2.xml",
        "lexical-selection.json", "comparison-selection.json", "jmdict.xml", "comparison-jmdict.xml")],
]
for name in immutable:
    actual = (ROOT / name).read_bytes().replace(b"\r\n", b"\n")
    expected = subprocess.check_output(["git", "show", f"{SOURCE}:{name}"], cwd=ROOT).replace(b"\r\n", b"\n")
    assert actual == expected, name
counts = {"kanji": 0, "words": 0, "strokes": 0}
exceptions = {"words/虎.md": ["酔っ払い"], "words/猿.md": ["馬鹿"]}
for name, row in load(FOLDER / "baseline-inventory.json")["files"].items():
    kind = name.split("/")[0]
    if kind in {"kanji", "words"}:
        expected = dict(row["metadata"])
        if name in exceptions:
            expected["quiz_exclusions"] = exceptions[name]
        assert metadata(ROOT, name) == expected, name
        counts[kind] += 1
    elif kind == "strokes":
        assert digest((ROOT / name).read_bytes()) == row["sha256"], name
        counts[kind] += 1
assert counts == {"kanji": 985, "words": 4942, "strokes": 985}
manifest = load(ROOT / "manifest.json")
assert manifest == build_manifest(ROOT)
before = json.loads(git("show", f"{BASE}:manifest.json"))
payloads = {name: value for entries in manifest.values() if isinstance(entries, dict) for name, value in entries.items()}
previous = {name: value for entries in before.values() if isinstance(entries, dict) for name, value in entries.items()}
additions = {"kanji/企.md", "words/企てる.md", "strokes/企.json"}
assert set(payloads) - set(previous) == additions and not set(previous) - set(payloads)
changed = {name for name in previous if previous[name] != payloads[name]}
assert changed == {"words/企業.md"}
for section, entries in manifest.items():
    if isinstance(entries, dict):
        for name, expected in entries.items():
            actual = digest((ROOT / name).read_bytes()) if section in {
                "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(ROOT / name)
            assert actual == expected, name
assert len(previous) == 8297 and len(payloads) == 8300
evidence = load(FOLDER / "batch-057-dictionary-evidence.json")
for record in evidence["sources"]:
    path = CONTROL.parent / record["rawArtifact"]
    assert path.stat().st_size == record["rawBytes"] and digest(path.read_bytes()) == record["rawSha256"]
svg = (CONTROL / "inputs" / "batch-057" / "04f01.svg").read_bytes()
blob = hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest()
assert blob == source_row["kanjivgInventory"]["sha"] == evidence["strokeSource"]["gitBlob"]
assert digest(svg) == evidence["strokeSource"]["sha256"]
strokes_raw = (ROOT / "strokes" / "企.json").read_bytes()
strokes = json.loads(strokes_raw)
assert strokes == convert("企", svg.decode("utf-8"))
assert strokes["strokeCount"] == 6 and len(strokes["strokes"]) == 6
for stroke in strokes["strokes"]:
    assert len(stroke["points"]) == 16
    assert all(len(point) == 2 and all(math.isfinite(value) and 0 <= value <= 109 for value in point) for point in stroke["points"])
assert digest((ROOT / "tools" / "generate_strokes.py").read_bytes()) == snapshot["kanjivg"]["converter"]["sha256"]
authored = ["kanji/企.md", "words/企てる.md", "words/企業.md"]
han = sorted(set(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]", "\n".join(
    (ROOT / name).read_text(encoding="utf-8") for name in authored))))
android = CONTROL.parent / "kanji-cards-android"
android_sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=android, text=True).strip()
assert android_sha == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
assert not subprocess.check_output(["git", "status", "--porcelain"], cwd=android).strip()
fonts = []
for font_record in load(FOLDER / "font-coverage.json")["fonts"]:
    path = android / font_record["path"]
    assert digest(path.read_bytes()) == font_record["sha256"]
    with TTFont(path) as font:
        cmap = font.getBestCmap()
        missing = [ch for ch in han if ord(ch) not in cmap]
    fonts.append({"path": font_record["path"], "sha256": font_record["sha256"], "missing": missing})
legacy = []
for path in sorted((ROOT / "kanji").glob("*.md")):
    meta = metadata(ROOT, path.relative_to(ROOT).as_posix())
    if len(meta.get("distractors", [])) < 3:
        legacy.append({key: meta[key] for key in ("kanji", "title", "distractors")})
assert len(legacy) == 12
assert metadata(ROOT, "words/企業.md")["jlpt"] == 3
assert metadata(ROOT, "words/企業.md")["quiz_exclusions"] == ["会社"]
assert metadata(ROOT, "words/商社.md")["quiz_exclusions"] == ["会社", "企業"]
assert "jlpt" not in metadata(ROOT, "words/企てる.md")
assert metadata(ROOT, "words/企てる.md")["kanji"] == ["企"]
word_pairs = {frozenset((row["word"], target)) for row in ledger["wordQuizAudit"]["directExclusions"] for target in row["exclude"]}
assert len(word_pairs) == 11
current_counts = {
    "kanji": len(list((ROOT / "kanji").glob("*.md"))),
    "words": len(list((ROOT / "words").glob("*.md"))),
    "n1Labels": sum(metadata(ROOT, path.relative_to(ROOT).as_posix())["jlpt"] == 1 for path in (ROOT / "kanji").glob("*.md")),
    "unpublishedBatchAdditions": 1,
}
assert current_counts == {"kanji": 1069, "words": 5028, "n1Labels": 89, "unpublishedBatchAdditions": 1}
result = {
    "schemaVersion": 1, "execution": 331, "batch": "057", "status": "local-unreviewed-runtime-draft",
    "mechanicalBatchAudit": mechanical, "frozenInputHashesVerified": 5, "decompressedDictionaryHashesVerified": 2,
    "freshExactFrozenFamilyExtraction": len(families), "dictionaryPackets": packets,
    "freshLinguisticReviewOfAllFamiliesClaimed": False, "inspectionScope": ledger["draftInspection"],
    "namedSourceRow": 27, "originalBaselineMetadataAndStrokesPreserved": counts,
    "baselineMetadataExceptions": exceptions, "runtimePayloadHashesVerified": len(payloads),
    "baseRuntimePayloadHashesPreserved": len(previous) - len(changed),
    "runtimeAdditions": sorted(additions), "changedReusedRuntimePayloads": sorted(changed),
    "immutableEvidenceUnchanged": immutable, "actualDraftCounts": current_counts,
    "actualAuthoredHanFonts": {"characters": han, "count": len(han), "fonts": fonts,
        "missingUnion": sorted({char for row in fonts for char in row["missing"]}),
        "limits": "Actual final authored/reused article Han and current bundled font cmaps only; not a native readability/fallback-face/phone acceptance claim."},
    "legacyFallbackCandidatesWithFewerThanThree": legacy,
    "legacyFallbackDisposition": "All12 actual labels inspected: person/rest/what/enter/exit/mouth/woman/mountain/sun-day/moon-month/man/buy do not denote planning, undertaking or attempts. Close semantic neighbors計/図/承/意/試 already have three choices. No baseline kanji metadata changed; no larger/random/live-pool certification.",
    "selectedReciprocalPairs": 2, "directedSelectedLinks": 4, "activatedBaselinePairs": 1,
    "existingComponentLinksPreserved": ["words/企業.md -> kanji/業.md"],
    "directWordExclusions": len(word_pairs), "noTransitiveClique": True,
    "geometry": {"rawRuntimeSha256": digest(strokes_raw), "normalizedSha256": digest(strokes_raw.replace(b"\r\n", b"\n")),
        "rawSvgSha256": digest(svg), "gitBlob": blob, "strokes": 6, "pointsPerStroke": 16,
        "unchangedConverter": True, "equalToVerifiedPinnedSvgConversion": True},
    "budget": check(ROOT, archive_names(ROOT)),
    "publishedAdditions": 83, "remainingAdditions": 1145, "limits": ledger["limits"],
}
(FOLDER / "batch-057-draft-audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({key: result[key] for key in ("mechanicalBatchAudit", "actualDraftCounts", "actualAuthoredHanFonts", "geometry", "budget")}, ensure_ascii=False, indent=2))

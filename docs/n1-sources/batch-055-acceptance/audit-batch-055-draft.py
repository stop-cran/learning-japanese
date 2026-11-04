import gzip
import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
F = R / "docs" / "n1-sources"
A = C.parent / "kanji-cards-android"
BASE = "c2004b726e5086f811a8ef238d78da3c0285dd54"
UPSTREAM = "998eca51e8d6620a4e60f7b66fdb8c1ff515a545"
QUALIFIED = "e5446a76dec02e49fb4acd148d7f71b1d5787dbc"
sys.path.insert(0, str(R / "tools"))
from audit_n1_batch import audit
from audit_n1_pilot import metadata
from build_manifest import build_manifest, sha256
from extract_n1_jmdict import extract
from fontTools.ttLib import TTFont
from generate_strokes import convert


def load(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def committed(sha, name):
    return subprocess.check_output(["git", "--no-pager", "show", f"{sha}:{name}"], cwd=R)


batch = audit(R, "055")
ledger = load(F / "batch-055-progress.json")
snapshot = load(R / "docs" / "n1-source-snapshot.json")
for name, row in snapshot["inputs"].items():
    assert digest((C / "inputs" / name).read_bytes()) == row["sha256"], name
for name, section in [
    ("n1-planning-kanjidic2.xml.gz", "kanjidic2"),
    ("n1-implementation-JMdict_e.gz", "jmdict"),
]:
    assert digest(gzip.decompress((C / "inputs" / name).read_bytes())) == snapshot[section]["xmlSha256"]
dictionary = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
families = []
for packet in ledger["dictionaryPackets"]:
    selection = load(F / packet["selection"])
    assert (F / packet["xml"]).read_bytes() == extract(
        dictionary, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"],
        selection["entryIds"],
    )
    families.extend(selection["entryIds"])
assert len(families) == len(set(families)) == 14
counts = {"kanji": 0, "words": 0, "strokes": 0}
exceptions = {"words/虎.md": ["酔っ払い"], "words/猿.md": ["馬鹿"]}
inventory = load(F / "baseline-inventory.json")["files"]
for name, row in inventory.items():
    kind = name.split("/")[0]
    if kind in ["kanji", "words"]:
        expected = dict(row["metadata"])
        if name in exceptions:
            expected["quiz_exclusions"] = exceptions[name]
        assert metadata(R, name) == expected, name
        counts[kind] += 1
    elif kind == "strokes":
        assert digest((R / name).read_bytes()) == row["sha256"], name
        counts[kind] += 1
assert counts == {"kanji": 985, "words": 4942, "strokes": 985}
unchanged = [
    "docs/n1-source-snapshot.json", "docs/n1-sources/source-index.json",
    "docs/n1-sources/baseline-inventory.json", "docs/n1-sources/baseline-word-candidates.json",
    "docs/n1-sources/batch-055-input-metadata.json",
    "docs/n1-sources/batch-055-dictionary-evidence.json",
    "docs/n1-sources/batch-055-qualification-audit.json",
    "docs/n1-sources/batch-055-preparation-audit.json",
    "docs/n1-sources/batch-055-jmdict.xml",
    "docs/n1-sources/batch-055-comparison-jmdict.xml",
    "docs/n1-sources/batch-055-lexical-selection.json",
    "docs/n1-sources/batch-055-comparison-selection.json",
]
for name in unchanged:
    assert (R / name).read_bytes() == committed(QUALIFIED, name), name
upstream_preserved = ["kanji/号.md", "kanji/番.md", "kanji/目.md"]
for name in upstream_preserved:
    assert (R / name).read_bytes() == committed(UPSTREAM, name) == committed(BASE, name), name
membership = load(F / "batch-055-membership.json")
prepared = json.loads(committed(QUALIFIED, "docs/n1-sources/batch-055-membership.json"))
assert membership["sourcePreparationBaseCommit"] == ledger["sourcePreparationBaseCommit"] == prepared["baseCommit"]
assert membership["membership"] == prepared["membership"] == ["丞"]
assert membership["members"] == prepared["members"]
named = load(C / "inputs" / "n1-kanji-source-20261102.json")
assert len(named) == len(set(named)) == 1232 and named[5] == "丞"
source = load(F / "batch-055-input-metadata.json")["sourceIndexRecord"]
assert source["sourceRow"] == 6
assert source == next(row for row in load(F / "source-index.json") if row["kanji"] == "丞")
e = load(F / "batch-055-dictionary-evidence.json")
g = e["geometryQualification"]
svg = (C.parent / g["rawArtifact"]).read_bytes()
assert digest(svg) == g["rawSha256"]
assert hashlib.sha1(b"blob " + str(len(svg)).encode() + b"\0" + svg).hexdigest() == g["verifiedGitBlob"]
geometry = convert("丞", svg.decode("utf-8"))
generated = (json.dumps(geometry, ensure_ascii=False, separators=(",", ":")) + "\n").encode()
runtime_geometry = (R / "strokes" / "丞.json").read_bytes()
assert runtime_geometry.replace(b"\r\n", b"\n") == generated == (C / "artifacts" / "batch-055-stroke-candidate.json").read_bytes()
assert digest(generated) == g["converterCandidate"]["sha256"]
assert digest((R / "tools" / "generate_strokes.py").read_bytes()) == g["converterCandidate"]["converterSha256"]
assert geometry["viewBox"] == [0, 0, 109, 109]
assert [s["id"] for s in geometry["strokes"]] == list(range(1, 7))
for stroke in geometry["strokes"]:
    assert len(stroke["points"]) == 16
    assert all(len(p) == 2 and all(math.isfinite(v) and 0 <= v <= 109 for v in p) for p in stroke["points"])
for row in e["sources"]:
    assert digest((C.parent / row["rawArtifact"]).read_bytes()) == row["rawSha256"]
manifest = load(R / "manifest.json")
assert manifest == build_manifest(R)
runtime = 0
for section, entries in manifest.items():
    if isinstance(entries, dict):
        for name, expected in entries.items():
            path = R / name
            actual = digest(path.read_bytes()) if section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(path)
            assert actual == expected, name
            runtime += 1
assert runtime == 8293
before = json.loads(committed(BASE, "manifest.json"))
preserved = 0
for section, entries in before.items():
    if isinstance(entries, dict):
        for name, expected in entries.items():
            assert manifest[section][name] == expected, name
            preserved += 1
assert preserved == 8290
articles = ["kanji/丞.md", "words/丞相.md"]
han = sorted({ch for name in articles for ch in (R / name).read_text(encoding="utf-8")
              if "\u3400" <= ch <= "\u9fff" or "\U00020000" <= ch <= "\U000323af"})
font_rows = []
for row in load(F / "font-coverage.json")["fonts"]:
    path = A / row["path"]
    assert digest(path.read_bytes()) == row["sha256"]
    with TTFont(path) as font:
        cmap = font.getBestCmap()
        missing = [ch for ch in han if ord(ch) not in cmap]
    font_rows.append({"path": row["path"], "sha256": row["sha256"], "missing": missing})
missing = sorted({ch for row in font_rows for ch in row["missing"]})
assert not missing, missing
short = []
for path in sorted((R / "kanji").glob("*.md")):
    m = metadata(R, f"kanji/{path.name}")
    labels = {metadata(R, f"kanji/{d}.md")["title"] for d in m.get("distractors", [])}
    if len(labels) < 3:
        short.append({"kanji": path.stem, "title": m["title"], "distractors": m.get("distractors", [])})
assert len(short) == 12
assert [row["title"] for row in short] == [
    "person", "rest", "what", "enter, put in", "go out, exit", "mouth",
    "woman, female", "mountain", "sun, day", "moon, month", "man, male", "buy",
]
assert metadata(R, "kanji/助.md")["distractors"] == ["加", "男", "動"]
word = metadata(R, "words/丞相.md")
assert "jlpt" not in word
assert word["reading"] == "じょうしょう" and word["type"] == "kango" and word["kanji"] == ["丞", "相"]
assert word["quiz_exclusions"] == ["大臣", "首相", "総理大臣"]
assert "(../kanji/相.md)" in (R / "words" / "丞相.md").read_text(encoding="utf-8")
assert not [p for p in load(F / "baseline-word-candidates.json") if p["kanji"] == "丞"]
all_cards = [metadata(R, f"kanji/{p.name}") for p in (R / "kanji").glob("*.md")]
actual_members = {m["kanji"] for m in all_cards if m["jlpt"] == 1}
baseline_kanji = {name.split("/")[1][:-3] for name in inventory if name.startswith("kanji/")}
assert len({m["kanji"] for m in all_cards} - baseline_kanji) == 82
assert {m["kanji"] for m in all_cards} - baseline_kanji <= set(named)
assert actual_members - set(named) == {"妖"}
assert len(actual_members & set(named)) == 86 and len(actual_members) == 87
assert len(all_cards) == 1067 and len(list((R / "words").glob("*.md"))) == 5025
assert all((R / f"strokes/{m['kanji']}.json").exists() for m in all_cards)
result = {
    "schemaVersion": 1, "execution": 308, "batch": "055", "status": "local-unreviewed-runtime-draft",
    "mechanicalBatchAudit": batch,
    "frozenInputHashesVerified": len(snapshot["inputs"]), "decompressedDictionaryHashesVerified": 2,
    "freshExactFrozenFamilyExtraction": 14, "freshLinguisticReviewOfAllFamiliesClaimed": True,
    "inspectionScope": ledger["draftInspection"],
    "namedSourceRow": 6, "originalBaselineMetadataAndStrokesPreserved": counts,
    "baselineMetadataExceptions": exceptions, "runtimePayloadHashesVerified": runtime,
    "baseRuntimePayloadHashesPreserved": preserved,
    "runtimeAdditions": articles + ["strokes/丞.json"], "changedReusedRuntimePayloads": [],
    "immutableEvidenceUnchanged": unchanged, "upstreamArticlesPreservedByteForByte": upstream_preserved,
    "draftBaseIntegration": ledger["draftBaseIntegration"],
    "actualDraftCounts": {"kanji": 1067, "words": 5025, "n1Labels": 87, "namedSourceMembers": 86,
                          "separateException": "妖", "unpublishedBatchAdditions": 1},
    "actualAuthoredHanFonts": {"characters": han, "count": len(han), "fonts": font_rows,
                              "missing": missing, "requiredNativeFallback": [],
                              "limits": "Every final authored Han checked in all three actual bundled cmaps; no missing glyph. Not native readability or phone acceptance."},
    "legacyFallbackCandidatesWithFewerThanThree": short,
    "legacyFallbackDisposition": "All12 actual labels inspected; none denotes assistance or historical assisting office. Overlapping 助 has three existing distinct wrong labels 加/男/動 and needs no default four-choice fallback fill. New curated 蒸/乗/水 labels wrong against inspected secondary senses. No newly established default fallback ambiguity; not larger/random/session certification.",
    "selectedReciprocalPairs": 1, "directedSelectedLinks": 2, "activatedBaselinePairs": 0,
    "existingComponentLinks": 1, "directWordExclusions": 3, "noTransitiveClique": True,
    "geometry": {"sha256": digest(generated), "rawRuntimeSha256": digest(runtime_geometry),
                 "strokes": 6, "pointsPerStroke": 16,
                 "unchangedConverter": True, "equalToQualifiedCandidateAfterLfNormalization": True,
                 "serialization": "Unchanged generator main writes Windows CRLF; qualified external candidate is LF. Exact LF-normalized serialization and parsed geometry agree. No generated path edited; manifest text hashing normalizes LF.",
                 "limits": "Not native drawing recognition or visual acceptance."},
    "publishedAdditions": 81, "remainingAdditions": 1147,
    "limits": "Mechanical LOCAL UNREVIEWED draft audit with separate coordinator source inspections, not independent linguistic certification. Two-family review, reconciliation, fresh Android/native/visual/current-main/publication gates pending. No phone/general-release/whole-set acceptance.",
}
(F / "batch-055-draft-audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))

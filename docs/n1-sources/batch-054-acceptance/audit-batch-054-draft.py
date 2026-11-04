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


batch = audit(R, "054")
base = "672266d5fffae425e608cdfa5a631ac147d1d08c"
qualified = "73f84e43fd710987366b85a5cb9155fccba1e9b1"
snapshot = load(R / "docs" / "n1-source-snapshot.json")
for name, row in snapshot["inputs"].items():
    assert digest((C / "inputs" / name).read_bytes()) == row["sha256"], name
for name, section in [("n1-planning-kanjidic2.xml.gz", "kanjidic2"),
                      ("n1-implementation-JMdict_e.gz", "jmdict")]:
    assert digest(gzip.decompress((C / "inputs" / name).read_bytes())) == snapshot[section]["xmlSha256"]
dictionary = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
families = []
for kind in ["lexical", "comparison", "additive", "additive-followup"]:
    selection = load(F / f"batch-054-{kind}-selection.json")
    packet = F / ("batch-054-jmdict.xml" if kind == "lexical" else f"batch-054-{kind}-jmdict.xml")
    assert packet.read_bytes() == extract(dictionary, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"],
                                          selection["entryIds"])
    families.extend(selection["entryIds"])
assert len(families) == len(set(families)) == 31
counts = {"kanji": 0, "words": 0, "strokes": 0}
exceptions = {"words/虎.md": ["酔っ払い"], "words/猿.md": ["馬鹿"]}
for name, row in load(F / "baseline-inventory.json")["files"].items():
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
    "docs/n1-sources/batch-054-membership.json", "docs/n1-sources/batch-054-input-metadata.json",
    "docs/n1-sources/batch-054-dictionary-evidence.json",
    "docs/n1-sources/batch-054-qualified-source-audit.json",
    "docs/n1-sources/batch-054-preparation-audit.json",
]
for name in unchanged:
    assert (R / name).read_bytes() == committed(qualified, name), name
named = load(C / "inputs" / "n1-kanji-source-20261102.json")
assert len(named) == len(set(named)) == 1232 and named[2] == "且"
source = load(F / "batch-054-input-metadata.json")["sourceIndexRecord"]
assert source["sourceRow"] == 3
assert source == next(row for row in load(F / "source-index.json") if row["kanji"] == "且")
e = load(F / "batch-054-dictionary-evidence.json")
g = e["geometryQualification"]
svg = (C.parent / g["rawArtifact"]).read_bytes()
assert digest(svg) == g["rawSha256"]
assert hashlib.sha1(b"blob " + str(len(svg)).encode() + b"\0" + svg).hexdigest() == g["verifiedGitBlob"]
geometry = convert("且", svg.decode("utf-8"))
generated = (json.dumps(geometry, ensure_ascii=False, separators=(",", ":")) + "\n").encode()
assert (R / "strokes" / "且.json").read_bytes() == generated == (C / "artifacts" / "batch-054-stroke-candidate.json").read_bytes()
assert digest(generated) == g["converterCandidate"]["sha256"]
assert digest((R / "tools" / "generate_strokes.py").read_bytes()) == g["converterCandidate"]["converterSha256"]
assert geometry["viewBox"] == [0, 0, 109, 109]
assert [s["id"] for s in geometry["strokes"]] == list(range(1, 6))
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
assert runtime == 8290
before = json.loads(committed(base, "manifest.json"))
preserved = 0
for section, entries in before.items():
    if isinstance(entries, dict):
        for name, expected in entries.items():
            assert manifest[section][name] == expected, name
            preserved += 1
assert preserved == 8287
articles = ["kanji/且.md", "words/且つ.md"]
han = sorted({ch for name in articles for ch in (R / name).read_text(encoding="utf-8")
              if "\u3400" <= ch <= "\u9fff" or "\U00020000" <= ch <= "\U000323af"})
font_rows = []
for row in load(F / "font-coverage.json")["fonts"]:
    p = A / row["path"]
    assert digest(p.read_bytes()) == row["sha256"]
    with TTFont(p) as font:
        cmap = font.getBestCmap()
        missing = [ch for ch in han if ord(ch) not in cmap]
    assert missing == ["苟"], missing
    font_rows.append({"path": row["path"], "sha256": row["sha256"], "missing": missing})
short = []
for p in sorted((R / "kanji").glob("*.md")):
    m = metadata(R, f"kanji/{p.name}")
    if len(set(m.get("distractors", []))) < 3:
        short.append({"kanji": p.stem, "title": m["title"], "distractors": m.get("distractors", [])})
assert len(short) == 12
word = metadata(R, "words/且つ.md")
assert "jlpt" not in word
assert word["reading"] == "かつ" and word["type"] == "wago" and word["kanji"] == ["且"]
assert word["quiz_exclusions"] == [row["word"] for row in e["proposedDirectWordExclusions"]]
ledger = load(F / "batch-054-progress.json")
for row in e["proposedDirectWordExclusions"]:
    assert metadata(R, f"words/{row['word']}.md")["title"] == row["label"]
assert len(ledger["wordQuizAudit"]["directExclusions"]) == 1
all_cards = [metadata(R, f"kanji/{p.name}") for p in (R / "kanji").glob("*.md")]
actual_members = {m["kanji"] for m in all_cards if m["jlpt"] == 1}
baseline_kanji = {name.split("/")[1][:-3] for name in load(F / "baseline-inventory.json")["files"]
                 if name.startswith("kanji/")}
assert len({m["kanji"] for m in all_cards} - baseline_kanji) == 81
assert {m["kanji"] for m in all_cards} - baseline_kanji <= set(named)
assert actual_members - set(named) == {"妖"}
assert len(actual_members & set(named)) == 85 and len(actual_members) == 86
assert len(all_cards) == 1066 and len(list((R / "words").glob("*.md"))) == 5024
assert all((R / f"strokes/{m['kanji']}.json").exists() for m in all_cards)
result = {
    "schemaVersion": 1, "execution": 299, "batch": "054", "status": "local-unreviewed-runtime-draft",
    "mechanicalBatchAudit": batch,
    "frozenInputHashesVerified": len(snapshot["inputs"]), "decompressedDictionaryHashesVerified": 2,
    "freshExactFrozenFamilyExtraction": 31, "freshLinguisticReviewOfAllFamiliesClaimed": False,
    "namedSourceRow": 3, "originalBaselineMetadataAndStrokesPreserved": counts,
    "baselineMetadataExceptions": exceptions, "runtimePayloadHashesVerified": runtime,
    "baseRuntimePayloadHashesPreserved": preserved,
    "runtimeAdditions": articles + ["strokes/且.json"], "changedReusedRuntimePayloads": [],
    "immutableEvidenceUnchanged": unchanged,
    "actualDraftCounts": {"kanji": 1066, "words": 5024, "n1Labels": 86, "namedSourceMembers": 85,
                          "separateException": "妖", "unpublishedBatchAdditions": 1},
    "actualAuthoredHanFonts": {"characters": han, "count": len(han), "fonts": font_rows,
                              "missing": ["苟"], "requiredNativeFallback": ["苟"],
                              "limits": "All final authored Han audited in all three actual bundled cmaps. 苟 missing: actual supported-native fallback/readability remains mandatory. Cmap presence is not visual/phone acceptance."},
    "legacyFallbackCandidatesWithFewerThanThree": short,
    "legacyFallbackDisposition": "All12 actual labels inspected: person/rest/what/enter/goout/mouth/woman/mountain/sun-day/moon-month/man/buy; none denotes additive moreover/also. New curated目/日/助 labels also wrong against inspected secondary senses. No newly established default fallback ambiguity; not larger/random/session certification.",
    "selectedReciprocalPairs": 1, "directedSelectedLinks": 2, "activatedBaselinePairs": 0,
    "directWordExclusions": 9, "noTransitiveClique": True,
    "registerDisposition": ledger["registerDisposition"],
    "geometry": {"sha256": digest(generated), "strokes": 5, "pointsPerStroke": 16,
                 "unchangedConverter": True, "equalToQualifiedCandidate": True,
                 "limits": "Not native drawing recognition or visual acceptance."},
    "publishedAdditions": 80, "remainingAdditions": 1148,
    "limits": "Mechanical LOCAL UNREVIEWED draft audit. Two-family review, reconciliation, fresh Android/native/visual/current-main/publication gates pending. No phone/general-release/whole-set acceptance.",
}
(F / "batch-054-draft-audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))

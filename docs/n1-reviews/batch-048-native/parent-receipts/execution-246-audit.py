import hashlib
import json
import math
import runpy
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

CONTROL = Path(__file__).resolve().parent
ROOT = CONTROL.parent / "learning-japanese"
FOLDER = ROOT / "docs" / "n1-sources"
ANDROID = CONTROL.parent / "kanji-cards-android"


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


mode = sys.argv[1]
assert mode in {"record", "audit"}
path = FOLDER / "batch-048-dictionary-evidence.json"
evidence = load(path)
markers = {
    "daijisen-in": ["デジタル大辞泉", "読み方：いん", "［音］", "イン", "甲寅", "こういん", "きのえとら"],
    "daijisen-tora": ["デジタル大辞泉", "読み方：とら", "その後", "前後", "東北東", "30", "陰暦", "1月"],
    "daijisen-toradoshi": ["デジタル大辞泉", "読み方：とらどし", "生まれた"],
    "nikkoku-koin": ["精選版 日本国語大辞典", "こう‐いん", "【甲寅】", "第五一番目", "きのえとら", "1477"],
    "daijisen-ushitora": ["デジタル大辞泉", "読み方：うしとら", "中間の", "北東", "艮"],
    "daijisen-ukanmuri": ["デジタル大辞泉", "読み方：うかんむり", "ウ冠", "宀", "片仮名"],
    "kanjipedia-character": ['id="kanjiOyaji">寅', "画数：(11)", "/bushu/16/39.png", 'class="onkunYomi">イン', "とら・つつし", "角川新字源"],
    "kanjipedia-word": ['class="kotobaYomi">とら', "①十二支の三番目", "②昔の時刻", "③昔の方角", "東北東"],
}
assert len(evidence["sources"]) == len(markers) == 8
assert len({s["id"] for s in evidence["sources"]}) == 8
assert len({s["rawArtifact"] for s in evidence["sources"]}) == 7
for source in evidence["sources"]:
    raw = (CONTROL.parent / source["rawArtifact"]).read_bytes()
    lines = raw.decode("utf-8").splitlines()
    sections = []
    for start, end in source["inspectedRanges"]:
        assert 1 <= start <= end <= len(lines), (source["id"], start, end, len(lines))
        sections.extend(lines[start - 1:end])
    for marker in markers[source["id"]]:
        assert marker in "\n".join(sections), (source["id"], marker)
    receipts = {"rawBytes": len(raw), "rawSha256": digest(raw), "rawLines": len(lines)}
    if mode == "record":
        source.update(receipts)
    else:
        assert all(source[k] == value for k, value in receipts.items()), source["id"]

geometry = evidence["geometryQualification"]
raw = (CONTROL.parent / geometry["rawArtifact"]).read_bytes()
blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
assert blob == geometry["expectedGitBlob"] and len(raw) == geometry["expectedBytes"]
if mode == "record":
    geometry["inspectedRanges"] = [[1, len(raw.splitlines())]]
assert geometry["inspectedRanges"] == [[1, len(raw.splitlines())]]
svg = ET.fromstring(raw.decode("utf-8").split("]>", 1)[1])
ns = "{http://www.w3.org/2000/svg}"
kns = "{https://kanjivg.tagaini.net/}"
paths = svg.findall(f".//{ns}path")
assert [p.attrib["id"] for p in paths] == [f"kvg:05bc5-s{i}" for i in range(1, 12)]
radical = next(g for g in svg.iter(ns + "g") if g.attrib.get("id") == "kvg:05bc5-g1")
assert radical.attrib[kns + "element"] == "宀"
assert radical.attrib[kns + "radical"] == "general" and radical.attrib[kns + "position"] == "top"
assert [p.attrib["id"] for p in radical.iter(ns + "path")] == [f"kvg:05bc5-s{i}" for i in range(1, 4)]
receipts = {"rawSha256": digest(raw), "verifiedGitBlob": blob, "actualBytes": len(raw), "actualPaths": len(paths), "actualLines": len(raw.splitlines())}
if mode == "record":
    geometry.update(receipts)
else:
    assert all(geometry[k] == value for k, value in receipts.items())

sys.path.insert(0, str(ROOT / "tools"))
from generate_strokes import KANJIVG_REVISION, POINTS_PER_STROKE, convert
from fontTools.ttLib import TTFont

assert KANJIVG_REVISION == geometry["revision"] and POINTS_PER_STROKE == 16
candidate = convert("寅", raw.decode("utf-8"))
assert candidate["strokeCount"] == geometry["expectedPaths"] == 11
assert candidate["viewBox"] == [0, 0, 109, 109]
assert candidate["sourceRevision"] == geometry["revision"] and "CC BY-SA 3.0" in candidate["source"]
assert [s["id"] for s in candidate["strokes"]] == list(range(1, 12))
for stroke in candidate["strokes"]:
    assert len(stroke["points"]) == 16
    assert all(len(p) == 2 and all(math.isfinite(v) and 0 <= v <= 109 for v in p) for p in stroke["points"])
candidate_path = CONTROL / "artifacts" / "batch-048-stroke-candidate.json"
candidate_raw = (json.dumps(candidate, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
converter_hash = digest((ROOT / "tools" / "generate_strokes.py").read_bytes())
assert converter_hash == "6993834d66221d23399547e5a17771d2d638dc68b2d08d47e9875ddc2c932081"
candidate_receipt = {
    "path": "control/artifacts/batch-048-stroke-candidate.json",
    "sha256": digest(candidate_raw), "bytes": len(candidate_raw),
    "converter": "tools/generate_strokes.py", "converterSha256": converter_hash,
    "strokeCount": 11, "pointsPerStroke": 16, "runtimeFileCreated": False,
    "limits": "Mechanical source reconciliation only; no font readability, native, visual, physical-phone or independent teaching acceptance.",
}
font_checks = []
assert not subprocess.check_output(["git", "status", "--porcelain"], cwd=ANDROID)
android_head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ANDROID, text=True).strip()
assert android_head == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
characters = sorted(set("寅宀由八演黄申虎甲"))
for row in load(FOLDER / "font-coverage.json")["fonts"]:
    font_path = ANDROID / row["path"]
    assert digest(font_path.read_bytes()) == row["sha256"]
    with TTFont(font_path) as font:
        cmap = font.getBestCmap()
        checks = {char: ord(char) in cmap for char in characters}
    font_checks.append({"path": row["path"], "sha256": row["sha256"], "glyphs": checks})
font_receipt = {
    "androidHead": android_head, "characters": characters, "fonts": font_checks,
    "missing": sorted({char for f in font_checks for char, present in f["glyphs"].items() if not present}),
    "scope": "Nine source/candidate component/comparison characters only; not a whole future draft or every glyph in Japanese source pages.",
    "limits": "Cmap presence is not readability or native visual acceptance. No Android build/device launched or font/runtime edits.",
}
if mode == "record":
    assert not candidate_path.exists()
    candidate_path.write_bytes(candidate_raw)
    geometry["converterCandidate"] = candidate_receipt
    evidence["candidateFontChecks"] = font_receipt
    evidence["retrievedOn"] = datetime.now().astimezone().date().isoformat()
    save(path, evidence)
else:
    assert candidate_path.read_bytes() == candidate_raw
    assert geometry["converterCandidate"] == candidate_receipt
    assert evidence["candidateFontChecks"] == font_receipt

preparation_path = FOLDER / "batch-048-preparation-audit.json"
original = preparation_path.read_bytes()
old_argv = sys.argv[:]
sys.argv = [str(CONTROL / "execution-245-source.py"), "audit"]
try:
    runpy.run_path(str(CONTROL / "execution-245-source.py"), run_name="__main__")
    preparation = load(preparation_path)
finally:
    preparation_path.write_bytes(original)
    sys.argv = old_argv
assert preparation_path.read_bytes() == original
ledger = load(FOLDER / "batch-048-progress.json")
assert evidence["proposedQuizSelection"] == ledger["qualifiedReadingSelectionCandidates"] == {"quizOnyomi": [], "quizKunyomi": ["とら"]}
assert ledger["nextAction"] == evidence["nextAction"] and ledger["limits"] == evidence["limits"]
assert ledger["sourceReadingOrder"] == {"onyomi": ["イン"], "kunyomi": ["とら"]}
assert not (ROOT / "words" / "寅.md").exists()
assert preparation["allRuntimePayloadHashesVerified"] == 8269
assert preparation["contentVersion"] == "4ca64c255449dba4"
inherited = subprocess.check_output(
    ["git", "--no-pager", "show", "3b2f689972f009604f8f2950d6588a760a2b740f:kanji/安.md"], cwd=ROOT,
).decode("utf-8")
assert "radical: 宀" in inherited and "宀 (roof, no. 40)" in inherited
assert font_receipt["missing"] == ["宀"]
result = dict(preparation)
result.update(
    execution=246, stage="qualified-source-not-drafted",
    sourcePreparationSnapshot=evidence["sourcePreparationSnapshot"],
    exactNamedJapaneseSectionsVerified=8, distinctAuthoritativeRawPages=7,
    externalDictionaryReceipts=evidence["sources"], geometryQualification=geometry,
    candidateFontChecks=font_receipt, fontFallbackBoundary=evidence["fontFallbackBoundary"],
    inheritedRadicalOccurrence={"article": "kanji/安.md", "commit": "3b2f689972f009604f8f2950d6588a760a2b740f", "sourceSha256": digest(inherited.encode("utf-8")), "scope": "Exact inherited radical/facts occurrence; not a new linguistic review or native result."},
    readingDispositions=evidence["readingDispositions"],
    radicalNameReconciliation=evidence["radicalNameReconciliation"],
    historicalSenseBoundary=evidence["historicalSenseBoundary"],
    proposedQuizSelection=evidence["proposedQuizSelection"],
    proposedNecessarySupport=evidence["proposedNecessarySupport"],
    historicalPreparationAuditPreservedSha256=digest(original), limits=evidence["limits"],
)
save(FOLDER / "batch-048-qualified-source-audit.json", result)
print(json.dumps({"sections": 8, "rawPages": 7, "paths": 11, "frozenFamilies": 26, "runtimeHashesVerified": 8269, "candidateFontCharacters": len(characters), "missingCandidateFontGlyphs": font_receipt["missing"], "runtimeChanges": 0, "historicalPreparationAuditPreserved": True}))

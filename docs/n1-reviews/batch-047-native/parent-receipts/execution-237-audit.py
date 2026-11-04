import hashlib
import json
import math
import runpy
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

CONTROL = Path(__file__).resolve().parent
ROOT = CONTROL.parent / "learning-japanese"
FOLDER = ROOT / "docs" / "n1-sources"


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


mode = sys.argv[1]
assert mode in {"record", "audit"}
path = FOLDER / "batch-047-dictionary-evidence.json"
evidence = load(path)
markers = {
    "daijisen-u": ["デジタル大辞泉", "読み方：う", "その後", "前後", "陰暦", "2月"],
    "daijisen-bo": ["デジタル大辞泉", "読み方：ぼう", "ボウ", "バウ", "己卯", "きぼう", "丁卯", "ていぼう"],
    "daijisen-udoshi": ["デジタル大辞泉", "読み方：うどし", "生まれた"],
    "daijisen-uzuki": ["デジタル大辞泉", "読み方：うづき", "陰暦", "4月", "植月"],
    "daijisen-shinbo": ["デジタル大辞泉", "読み方：しんぼう", "かのとう"],
    "daijisen-fushizukuri": ["デジタル大辞泉", "読み方：ふしづくり", "卩", "㔾"],
    "kanjipedia-character": ['id="kanjiOyaji">卯', "画数：(5)", "/bushu/16/26a.png", 'class="onkunYomi">ボウ', 'class="onkunYomi">う', "角川新字源"],
    "kanjipedia-word": ['class="kotobaYomi">う', "①十二支の四番目", "②昔の時刻", "③昔の方角"],
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
assert geometry["inspectedRanges"] == [[1, len(raw.splitlines())]]
svg = ET.fromstring(raw.decode("utf-8").split("]>", 1)[1])
ns = "{http://www.w3.org/2000/svg}"
kns = "{https://kanjivg.tagaini.net/}"
paths = svg.findall(f".//{ns}path")
assert [p.attrib["id"] for p in paths] == [f"kvg:0536f-s{i}" for i in range(1, 6)]
radical = next(g for g in svg.iter(ns + "g") if g.attrib.get("id") == "kvg:0536f-g3")
assert radical.attrib[kns + "element"] == "卩"
assert radical.attrib[kns + "radical"] == "general" and radical.attrib[kns + "position"] == "right"
assert [p.attrib["id"] for p in radical] == ["kvg:0536f-s4", "kvg:0536f-s5"]
receipts = {"rawSha256": digest(raw), "verifiedGitBlob": blob, "actualBytes": len(raw), "actualPaths": len(paths), "actualLines": len(raw.splitlines())}
if mode == "record":
    geometry.update(receipts)
else:
    assert all(geometry[k] == value for k, value in receipts.items())

sys.path.insert(0, str(ROOT / "tools"))
from generate_strokes import KANJIVG_REVISION, POINTS_PER_STROKE, convert

assert KANJIVG_REVISION == geometry["revision"] and POINTS_PER_STROKE == 16
candidate = convert("卯", raw.decode("utf-8"))
assert candidate["strokeCount"] == geometry["expectedPaths"] == 5
assert candidate["viewBox"] == [0, 0, 109, 109]
assert candidate["sourceRevision"] == geometry["revision"] and "CC BY-SA 3.0" in candidate["source"]
assert [s["id"] for s in candidate["strokes"]] == list(range(1, 6))
for stroke in candidate["strokes"]:
    assert len(stroke["points"]) == 16
    assert all(len(p) == 2 and all(math.isfinite(v) and 0 <= v <= 109 for v in p) for p in stroke["points"])
candidate_path = CONTROL / "artifacts" / "batch-047-stroke-candidate.json"
candidate_raw = (json.dumps(candidate, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
converter_hash = digest((ROOT / "tools" / "generate_strokes.py").read_bytes())
assert converter_hash == "6993834d66221d23399547e5a17771d2d638dc68b2d08d47e9875ddc2c932081"
if mode == "record":
    assert not candidate_path.exists()
    candidate_path.write_bytes(candidate_raw)
    geometry["converterCandidate"] = {
        "path": "control/artifacts/batch-047-stroke-candidate.json",
        "sha256": digest(candidate_raw), "bytes": len(candidate_raw),
        "converter": "tools/generate_strokes.py", "converterSha256": converter_hash,
        "strokeCount": 5, "pointsPerStroke": 16, "runtimeFileCreated": False,
        "limits": "Mechanical source reconciliation only; no font, native, visual, physical-phone or independent teaching acceptance.",
    }
    evidence["retrievedOn"] = datetime.now().astimezone().date().isoformat()
    save(path, evidence)
else:
    assert candidate_path.read_bytes() == candidate_raw
    assert geometry["converterCandidate"]["sha256"] == digest(candidate_raw)
    assert geometry["converterCandidate"]["bytes"] == len(candidate_raw)
    assert geometry["converterCandidate"]["converterSha256"] == converter_hash

preparation_path = FOLDER / "batch-047-preparation-audit.json"
original = preparation_path.read_bytes()
old_argv = sys.argv[:]
sys.argv = [str(CONTROL / "execution-236-source.py"), "audit"]
try:
    runpy.run_path(str(CONTROL / "execution-236-source.py"), run_name="__main__")
    preparation = load(preparation_path)
finally:
    preparation_path.write_bytes(original)
    sys.argv = old_argv
assert preparation_path.read_bytes() == original
ledger = load(FOLDER / "batch-047-progress.json")
assert evidence["proposedQuizSelection"] == ledger["qualifiedReadingSelectionCandidates"] == {"quizOnyomi": [], "quizKunyomi": ["う"]}
assert ledger["nextAction"] == evidence["nextAction"] and ledger["limits"] == evidence["limits"]
assert ledger["sourceReadingOrder"] == {"onyomi": ["ボウ", "モウ"], "kunyomi": ["う"]}
assert not (ROOT / "words" / "卯.md").exists()
assert preparation["allRuntimePayloadHashesVerified"] == 8266
assert preparation["contentVersion"] == "4a05b1fff8b65ff6"
result = dict(preparation)
result.update(
    execution=237, stage="qualified-source-not-drafted",
    sourcePreparationSnapshot=evidence["sourcePreparationSnapshot"],
    exactNamedJapaneseSectionsVerified=8, dictionaryEntries=8, distinctAuthoritativeRawPages=7,
    externalDictionaryReceipts=evidence["sources"], geometryQualification=geometry,
    readingDispositions=evidence["readingDispositions"],
    radicalNameReconciliation=evidence["radicalNameReconciliation"],
    proposedQuizSelection=evidence["proposedQuizSelection"],
    proposedNecessarySupport=evidence["proposedNecessarySupport"],
    historicalPreparationAuditPreservedSha256=digest(original), limits=evidence["limits"],
)
save(FOLDER / "batch-047-qualified-source-audit.json", result)
print(json.dumps({"sections": 8, "rawPages": 7, "paths": 5, "frozenFamilies": 39, "runtimeHashesVerified": 8266, "runtimeChanges": 0, "historicalPreparationAuditPreserved": True}))

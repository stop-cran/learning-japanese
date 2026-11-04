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
evidence_path = FOLDER / "batch-046-dictionary-evidence.json"
evidence = load(evidence_path)
markers = {
    "daijisen-tori": ["デジタル大辞泉", "読み方：とり", "十二支", "その後", "前後", "陰暦", "8月"],
    "daijisen-yu": ["読み方：ゆう", "ユウ", "イウ", "辛酉", "丁酉"],
    "daijisen-shinyu": ["デジタル大辞泉", "読み方：しんゆう", "かのととり"],
    "daijisen-toridoshi": ["デジタル大辞泉", "読み方：とりどし", "生まれた"],
    "daijisen-hiyomi": ["デジタル大辞泉", "読み方：ひよみのとり", "鳥", "ふるとり", "酒"],
    "daijisen-torihen": ["デジタル大辞泉", "読み方：とりへん", "酔", "酸"],
    "kanjipedia-character": ['id="kanjiOyaji">酉', "画数：(7)", "/bushu/16/164a.png", 'class="onkunYomi">ユウ', "とり・ひよみのとり", "角川新字源", "象形"],
    "kanjipedia-word": ['class="kotobaYomi">とり', "①十二支の一〇番目", "②昔の時刻", "③昔の方角", "ニワトリ"],
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
        assert all(source[k] == v for k, v in receipts.items()), source["id"]

geometry = evidence["geometryQualification"]
namespace = "{http://www.w3.org/2000/svg}"
kns = "{https://kanjivg.tagaini.net/}"
roots = {}
for item in [geometry, *evidence["visualComparisonGeometry"]]:
    raw = (CONTROL.parent / item["rawArtifact"]).read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    assert blob == item["expectedGitBlob"] and len(raw) == item["expectedBytes"]
    assert item["inspectedRanges"] == [[1, len(raw.splitlines())]]
    text = raw.decode("utf-8")
    svg = ET.fromstring(text.split("]>", 1)[1] if "]>" in text else text)
    paths = svg.findall(f".//{namespace}path")
    char = item.get("character", "酉")
    code = f"{ord(char):05x}"
    assert [p.attrib["id"] for p in paths] == [
        f"kvg:{code}-s{i}" for i in range(1, item["expectedPaths"] + 1)
    ]
    roots[char] = svg
    receipts = {
        "rawSha256": digest(raw), "verifiedGitBlob": blob,
        "actualBytes": len(raw), "actualPaths": len(paths), "actualLines": len(raw.splitlines()),
    }
    if mode == "record":
        item.update(receipts)
    else:
        assert all(item[k] == v for k, v in receipts.items()), char
group = next(g for g in roots["酉"].iter(namespace + "g") if g.attrib.get("id") == "kvg:09149")
assert group.attrib[kns + "element"] == "酉" and group.attrib[kns + "radical"] == "general"
parts = list(group)
assert [g.attrib[kns + "element"] for g in parts] == ["西", "一", "西"]
assert parts[1].find(namespace + "path").attrib["id"] == "kvg:09149-s6"
assert parts[2].find(namespace + "path").attrib["id"] == "kvg:09149-s7"

sys.path.insert(0, str(ROOT / "tools"))
from generate_strokes import KANJIVG_REVISION, POINTS_PER_STROKE, convert

assert KANJIVG_REVISION == geometry["revision"] and POINTS_PER_STROKE == 16
candidate = convert("酉", (CONTROL.parent / geometry["rawArtifact"]).read_text(encoding="utf-8"))
assert candidate["strokeCount"] == geometry["expectedPaths"] == 7
assert candidate["viewBox"] == [0, 0, 109, 109]
assert candidate["sourceRevision"] == geometry["revision"] and "CC BY-SA 3.0" in candidate["source"]
assert [s["id"] for s in candidate["strokes"]] == list(range(1, 8))
for stroke in candidate["strokes"]:
    assert len(stroke["points"]) == 16
    assert all(len(p) == 2 and all(math.isfinite(v) and 0 <= v <= 109 for v in p) for p in stroke["points"])
candidate_path = CONTROL / "artifacts" / "batch-046-stroke-candidate.json"
candidate_raw = (json.dumps(candidate, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
converter_hash = digest((ROOT / "tools" / "generate_strokes.py").read_bytes())
assert converter_hash == "6993834d66221d23399547e5a17771d2d638dc68b2d08d47e9875ddc2c932081"
if mode == "record":
    assert not candidate_path.exists()
    candidate_path.write_bytes(candidate_raw)
    geometry["converterCandidate"] = {
        "path": "control/artifacts/batch-046-stroke-candidate.json",
        "sha256": digest(candidate_raw), "bytes": len(candidate_raw),
        "converter": "tools/generate_strokes.py", "converterSha256": converter_hash,
        "strokeCount": 7, "pointsPerStroke": 16, "runtimeFileCreated": False,
        "limits": "Mechanical source reconciliation only; no native, visual, physical-phone or independent teaching acceptance.",
    }
    evidence["retrievedOn"] = datetime.now().astimezone().date().isoformat()
    save(evidence_path, evidence)
else:
    assert candidate_path.read_bytes() == candidate_raw
    assert geometry["converterCandidate"]["sha256"] == digest(candidate_raw)
    assert geometry["converterCandidate"]["bytes"] == len(candidate_raw)
    assert geometry["converterCandidate"]["converterSha256"] == converter_hash

preparation_path = FOLDER / "batch-046-preparation-audit.json"
original_preparation = preparation_path.read_bytes()
sys.argv = [str(CONTROL / "execution-227-source.py"), "audit"]
try:
    runpy.run_path(str(CONTROL / "execution-227-source.py"), run_name="__main__")
    preparation = load(preparation_path)
finally:
    preparation_path.write_bytes(original_preparation)
assert preparation_path.read_bytes() == original_preparation
ledger = load(FOLDER / "batch-046-progress.json")
assert evidence["proposedQuizSelection"] == ledger["qualifiedReadingSelectionCandidates"] == {"quizOnyomi": [], "quizKunyomi": ["とり"]}
assert ledger["nextAction"] == evidence["nextAction"] and ledger["limits"] == evidence["limits"]
assert ledger["sourceReadingOrder"] == {"onyomi": ["ユウ"], "kunyomi": ["とり"]}
assert not (ROOT / "words" / "酉.md").exists()
assert preparation["allRuntimePayloadHashesVerified"] == 8263
assert preparation["contentVersion"] == "c0c51142ac779ed8"
result = dict(preparation)
result.update(
    execution=228, stage="qualified-source-not-drafted",
    sourcePreparationSnapshot=evidence["sourcePreparationSnapshot"],
    exactNamedJapaneseSectionsVerified=8, dictionaryEntries=8, distinctAuthoritativeRawPages=7,
    externalDictionaryReceipts=evidence["sources"],
    geometryQualification=geometry, visualComparisonGeometry=evidence["visualComparisonGeometry"],
    readingDispositions=evidence["readingDispositions"],
    radicalNameReconciliation=evidence["radicalNameReconciliation"],
    proposedQuizSelection=evidence["proposedQuizSelection"],
    proposedNecessarySupport=evidence["proposedNecessarySupport"],
    historicalPreparationAuditPreservedSha256=digest(original_preparation),
    limits=evidence["limits"],
)
save(FOLDER / "batch-046-qualified-source-audit.json", result)
print(json.dumps({
    "sections": 8, "dictionaryEntries": 8, "distinctAuthoritativeRawPages": 7,
    "paths": 7, "comparisonGlyphs": 1, "candidateOnlyNotRuntime": True,
    "frozenFamilies": 33, "runtimeChanges": 0, "runtimeHashesVerified": 8263,
    "historicalPreparationAuditPreserved": True,
}))

"""Reuse complete inspected baseline audit with explicit batch046 identities."""
import hashlib
import json
import sys
from pathlib import Path

control = Path(__file__).resolve().parent
original = control / "audit-batch-040-draft.py"
raw = original.read_bytes()
source = raw.decode("utf-8")
assert sys.argv[1:] == ["audit"]
replacements = [
    ("batch-040", "batch-046"), ('"040"', '"046"'),
    ('execution": 175', 'execution": 229'), ("execution=175", "execution=229"),
    ("execution-175-", "execution-229-"), ("鵬", "酉"),
    ("range(2, 41)", "range(2, 47)"),
    ("len(expected_members) == 67", "len(expected_members) == 73"),
    ("== 1220", "== 1105"), ('== "ほう"', '== "とり"'),
    ("09d6c.svg", "09149.svg"),
    ("b4b30a4007689ef1316dc5b3f8584ce75dc6dc08", "38024c2354b40835626066d5733a6fa1156d31d1"),
    ("== 19", "== 7"), ('"strokeCount": 19', '"strokeCount": 7'),
    ('{"酉", "鳥", "朋", "月", "鳳", "鴻", "翼", "巨"}',
     '{"酉", "鶏", "鳥", "西", "酒", "酔", "配"}'),
    ("publishedAdditions=66, remainingAdditions=1162",
     "publishedAdditions=72, remainingAdditions=1156"),
]
for before, after in replacements:
    assert before in source, before
    source = source.replace(before, after)
scope = {"__file__": str(__file__), "__name__": "__main__"}
exec(compile(source, str(__file__), "exec"), scope)
result = scope["result"]
assert result["pythonTests"] == {"passed": 361, "failures": 0, "errors": 0}
assert len(scope["ids"]) == 33 and result["manifestFresh"]
assert result["currentKanjiIncludingDrafts"] == 1058
assert result["currentWordsIncludingDrafts"] == 5016
assert result["n1LabelledIncludingDrafts"] == 78
assert result["sourceMembersPresentIncludingDrafts"] == 77
assert result["readingDispositions"] == 2 and result["curatedOfferedKeys"] == 1
assert result["requiredReciprocalPairs"] == 1 and result["activatedBaselinePairs"] == 0
assert result["exactWordChoiceLabels"] == [
    {"word": "酉", "label": "Rooster zodiac sign", "excludedWord": c, "excludedLabel": label}
    for c, label in (("鳥", "bird"), ("鶏", "chicken"), ("西", "west"))
]
assert scope["load"](scope["root"] / "strokes" / "酉.json") == scope["load"](
    control / "artifacts" / "batch-046-stroke-candidate.json")
assert (scope["root"] / "strokes" / "酉.json").read_bytes() == (
    control / "artifacts" / "batch-046-stroke-candidate.json").read_bytes()
baseline = scope["load"](scope["folder"] / "baseline-inventory.json")["files"]
assert not any("酉" in row.get("metadata", {}).get("kanji", [])
               for name, row in baseline.items() if name.startswith("words/"))
declared = {
    ("酉", f"words/{path.name}") for path in (scope["root"] / "words").glob("*.md")
    if "酉" in scope["metadata"](scope["root"], f"words/{path.name}").get("kanji", [])
}
assert declared == {("酉", "words/酉.md")}
assert len(scope["ledger"]["wordQuizAudit"]["comparisonArticles"]) + len(
    scope["ledger"]["wordQuizAudit"]["comparisonKanji"]) == 18
for c, label in scope["ledger"]["wordQuizAudit"]["actualLabels"].items():
    assert scope["metadata"](scope["root"], f"words/{c}.md")["title"] == label
assert not any(c in (scope["root"] / "docs" / "confusable-words.md").read_text(
    encoding="utf-8") for c in ("酉", "鳥", "鶏", "西"))
historical = {}
for name in ("batch-046-preparation-audit.json", "batch-046-qualified-source-audit.json",
             "batch-046-dictionary-evidence.json", "batch-046-input-metadata.json"):
    path = scope["folder"] / name
    base = scope["git"]("show", f"d8bd58d646581930293c14aae70b1e6d01ad5a11:docs/n1-sources/{name}")
    assert path.read_bytes().replace(b"\r\n", b"\n") == base.replace(b"\r\n", b"\n")
    historical[name] = hashlib.sha256(path.read_bytes()).hexdigest()
qualification = control / "execution-228-audit.py"
qualification_source = qualification.read_text(encoding="utf-8").split("preparation_path =", 1)[0]
qualification_scope = {"__file__": str(qualification), "__name__": "__main__"}
exec(compile(qualification_source, str(qualification), "exec"), qualification_scope)
assert qualification_scope["mode"] == "audit"
manifest = scope["load"](scope["root"] / "manifest.json")
runtime = {}
for section, values in manifest.items():
    if not isinstance(values, dict):
        continue
    for name, value in values.items():
        path = scope["root"] / name
        actual = scope["sha256"](path) if path.suffix not in {".webp", ".ogg"} else scope["digest"](path.read_bytes())
        assert actual == value, (section, name)
        runtime[name] = value
assert len(runtime) == 8266
result["allRuntimePayloadHashesVerified"] = len(runtime)
result["declaredCurrentPairs"] = sorted(declared)
result["nativeFontDisposition"] = {
    "authoredHan": result["authoredTextHan"],
    "authoredHanInAllThreeBundledFonts": result["authoredTextHanInAllThreeFonts"],
    "authoredMissingGlyphs": sorted(scope["authored_missing"]),
    "newMissingGlyphsAcrossAuthoredAndComparisons": result["newFallbackNativePending"],
    "requiredGate": "Supported-native酉/西/鳥 and radical164 distinctions, actual fullarchiveContentSyncONCE/article/reciprocal/SystemBack/offline routes and bounded independent visual acceptance remain required before publication. Cmap presence and inherited occurrences are not native acceptance; fonts/heaps/guards unchanged.",
}
result["historicalSourceReceiptsPreserved"] = historical
result["qualifiedSourceSectionsReverified"] = {
    "sections": 8, "distinctRawPages": 7, "geometryPaths": 7, "comparisonPaths": 6,
    "boundary": "Reused inspected audit prefix verifies exact section ranges/markers, raw hashes, geometry and converter candidate. Does not execute old preparation audit or change historical records; not fresh whole-page linguistic review.",
    "implementationSha256": hashlib.sha256(qualification.read_bytes()).hexdigest(),
}
result["runtimePayloadAdditions"] = ["kanji/酉.md", "words/酉.md", "strokes/酉.json"]
result["runtimePayloadChanges"] = []
result["auditImplementation"] = {
    "adapter": str(__file__), "reusedCompleteAudit": str(original),
    "reusedAuditSha256": hashlib.sha256(raw).hexdigest(),
    "scope": "Explicit046 identities/counts; preserves complete frozen inputs and exact dictionary re-extraction, baseline, membership, reading/link, stroke/font, log checks plus all runtime hashes and complete current declared-pair audit.",
}
scope["save"](scope["folder"] / "batch-046-draft-audit.json", result)
print(json.dumps({
    "runtimeHashesVerified": len(runtime), "contentVersion": manifest["contentVersion"],
    "historicalReceiptsPreserved": True,
    "authoredMissingGlyphs": sorted(scope["authored_missing"]),
}, ensure_ascii=False))

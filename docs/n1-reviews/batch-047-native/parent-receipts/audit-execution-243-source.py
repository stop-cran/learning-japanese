"""Reuse the inspected full baseline audit with explicit batch047 identities."""
import hashlib
import json
import sys
from pathlib import Path

control = Path(__file__).resolve().parent
original = control / "audit-batch-040-draft.py"
raw = original.read_bytes()
source = raw.decode("utf-8").replace("save(folder /", "save(control /")
assert sys.argv[1:] == ["audit"]
replacements = [
    ("batch-040", "batch-047"), ('"040"', '"047"'),
    ('execution": 175', 'execution": 243'), ("execution=175", "execution=243"),
    ("execution-175-", "execution-243-"), ("鵬", "卯"),
    ("range(2, 41)", "range(2, 48)"),
    ("len(expected_members) == 67", "len(expected_members) == 74"),
    ("== 1220", "== 130"), ('== "ほう"', '== "う"'),
    ("09d6c.svg", "0536f.svg"),
    ("b4b30a4007689ef1316dc5b3f8584ce75dc6dc08", "fffb1fd0a0b20accf36fe3d58162d94eabb528db"),
    ("== 19", "== 5"), ('"strokeCount": 19', '"strokeCount": 5'),
    ('{"卯", "鳥", "朋", "月", "鳳", "鴻", "翼", "巨"}',
     '{"印", "卯", "兎", "酉", "柳", "卵", "卩"}'),
    ("publishedAdditions=66, remainingAdditions=1162",
     "publishedAdditions=73, remainingAdditions=1155"),
]
for before, after in replacements:
    assert before in source, before
    source = source.replace(before, after)
scope = {"__file__": str(__file__), "__name__": "__main__"}
exec(compile(source, str(__file__), "exec"), scope)
result = scope["result"]
assert result["pythonTests"] == {"passed": 361, "failures": 0, "errors": 0}
assert len(scope["ids"]) == 39 and result["manifestFresh"]
assert result["currentKanjiIncludingDrafts"] == 1059
assert result["currentWordsIncludingDrafts"] == 5017
assert result["n1LabelledIncludingDrafts"] == 79
assert result["sourceMembersPresentIncludingDrafts"] == 78
assert result["readingDispositions"] == 3 and result["curatedOfferedKeys"] == 1
assert result["requiredReciprocalPairs"] == 1 and result["activatedBaselinePairs"] == 0
assert result["exactWordChoiceLabels"] == [
    {"word": "卯", "label": "Rabbit zodiac sign", "excludedWord": c, "excludedLabel": label}
    for c, label in (("兎", "rabbit; hare"), ("東", "east"))
]
stroke = scope["root"] / "strokes" / "卯.json"
assert stroke.read_bytes() == (control / "artifacts" / "batch-047-stroke-candidate.json").read_bytes()
baseline = scope["load"](scope["folder"] / "baseline-inventory.json")["files"]
assert not any("卯" in row.get("metadata", {}).get("kanji", [])
               for name, row in baseline.items() if name.startswith("words/"))
declared = {
    ("卯", f"words/{path.name}") for path in (scope["root"] / "words").glob("*.md")
    if "卯" in scope["metadata"](scope["root"], f"words/{path.name}").get("kanji", [])
}
assert declared == {("卯", "words/卯.md")}
assert len(scope["ledger"]["wordQuizAudit"]["comparisonArticles"]) + len(
    scope["ledger"]["wordQuizAudit"]["comparisonKanji"]) == 14
for c, label in scope["ledger"]["wordQuizAudit"]["actualLabels"].items():
    assert scope["metadata"](scope["root"], f"words/{c}.md")["title"] == label
assert not any(term.lower() in (scope["root"] / "docs" / "confusable-words.md").read_text(
    encoding="utf-8").lower() for term in ("卯", "兎", "rabbit", "east", "zodiac"))
historical = {}
for name in (
    "batch-047-preparation-audit.json", "batch-047-qualified-source-audit.json",
    "batch-047-dictionary-evidence.json", "batch-047-input-metadata.json",
    "batch-047-membership.json", "batch-047-jmdict.xml", "batch-047-comparison-jmdict.xml",
    "batch-047-lexical-selection.json", "batch-047-comparison-selection.json",
):
    path = scope["folder"] / name
    before = scope["git"]("show", f"35dad5619ebd93cedc7367cdb5222696aa1016a3:docs/n1-sources/{name}")
    assert path.read_bytes().replace(b"\r\n", b"\n") == before.replace(b"\r\n", b"\n")
    historical[name] = hashlib.sha256(path.read_bytes()).hexdigest()
qualification = control / "execution-237-audit.py"
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
assert len(runtime) == 8269
result["allRuntimePayloadHashesVerified"] = len(runtime)
result["declaredCurrentPairs"] = sorted(declared)
result["nativeFontDisposition"] = {
    "authoredHan": result["authoredTextHan"],
    "authoredHanInAllThreeBundledFonts": result["authoredTextHanInAllThreeFonts"],
    "authoredMissingGlyphs": sorted(scope["authored_missing"]),
    "newMissingGlyphsAcrossAuthoredAndComparisons": result["newFallbackNativePending"],
    "requiredGate": "Supported-native卯/卵/印/柳/right卩 distinction, actual fullarchiveContentSyncONCE/article/reciprocal/SystemBack/offline routes and bounded independent visual acceptance remain required before publication. Cmap presence is not readability; productionfonts/heaps/guards unchanged.",
}
result["historicalSourceReceiptsPreserved"] = historical
result["qualifiedSourceSectionsReverified"] = {
    "sections": 8, "distinctRawPages": 7, "geometryPaths": 5,
    "boundary": "Fresh bounded coordinator reads of all recorded sections and fullSVG; reused inspected audit prefix verifies exact section ranges/markers, raw hashes, geometry and converter candidate without old preparation audit side effects. No fresh retrieval or wholepage linguistic/native review.",
    "implementationSha256": hashlib.sha256(qualification.read_bytes()).hexdigest(),
}
result["runtimePayloadAdditions"] = ["kanji/卯.md", "words/卯.md", "strokes/卯.json"]
result["runtimePayloadChanges"] = []
result["auditImplementation"] = {
    "adapter": str(__file__), "reusedCompleteAudit": str(original),
    "reusedAuditSha256": hashlib.sha256(raw).hexdigest(),
    "scope": "Explicit047 identities/counts; preserves complete frozen inputs and exact dictionary re-extraction, fullbaseline, membership, reading/link, stroke/font, log checks plus all runtime hashes/current declared-pair audit.",
}
scope["save"](control / "execution-243-source-audit.json", result)
print(json.dumps({
    "runtimeHashesVerified": len(runtime), "contentVersion": manifest["contentVersion"],
    "historicalReceiptsPreserved": True,
    "authoredMissingGlyphs": sorted(scope["authored_missing"]),
}, ensure_ascii=False))

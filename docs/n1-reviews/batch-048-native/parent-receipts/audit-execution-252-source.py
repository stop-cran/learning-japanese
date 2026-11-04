"""Reuse the complete baseline audit with explicit batch048 identities/delta."""
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
    ("batch-040", "batch-048"), ('"040"', '"048"'),
    ('execution": 175', 'execution": 252'), ("execution=175", "execution=252"),
    ("execution-175-", "execution-252-"), ("鵬", "寅"),
    ("range(2, 41)", "range(2, 49)"),
    ("len(expected_members) == 67", "len(expected_members) == 75"),
    ("== 1220", "== 256"), ('== "ほう"', '== "とら"'),
    ("09d6c.svg", "05bc5.svg"),
    ("b4b30a4007689ef1316dc5b3f8584ce75dc6dc08", "2588dd3be664744172436567fd08ab87a8d4df1b"),
    ("== 19", "== 11"), ('"strokeCount": 19', '"strokeCount": 11'),
    ('{"寅", "鳥", "朋", "月", "鳳", "鴻", "翼", "巨"}',
     '{"演", "黄", "虎", "申", "辰", "寅", "宀"}'),
    ("publishedAdditions=66, remainingAdditions=1162",
     "publishedAdditions=74, remainingAdditions=1154"),
    ('authored = ["kanji/寅.md", "words/寅.md"]',
     'authored = ["kanji/寅.md", "words/寅.md", "kanji/演.md"]'),
    ('    assert texts[name].encode().replace(b"\\r\\n", b"\\n") == git("show", f"{ledger[\'baseCommit\']}:{name}").replace(b"\\r\\n", b"\\n"), name',
     '''    before = git("show", f"{ledger['baseCommit']}:{name}").decode("utf-8")
    rows = [r for r in ledger["changedReusedPassages"] if r["article"] == name]
    if rows:
        from audit_n1_batch import reused_changes
        reused_changes(before, texts[name], rows)
    else:
        assert texts[name].replace("\\r\\n", "\\n") == before.replace("\\r\\n", "\\n"), name'''),
]
for before, after in replacements:
    assert before in source, before
    source = source.replace(before, after)
scope = {"__file__": str(__file__), "__name__": "__main__"}
exec(compile(source, str(__file__), "exec"), scope)
result = scope["result"]
assert result["pythonTests"] == {"passed": 361, "failures": 0, "errors": 0}
assert len(scope["ids"]) == 26 and result["manifestFresh"]
assert result["currentKanjiIncludingDrafts"] == 1060
assert result["currentWordsIncludingDrafts"] == 5018
assert result["n1LabelledIncludingDrafts"] == 80
assert result["sourceMembersPresentIncludingDrafts"] == 79
assert result["readingDispositions"] == 2 and result["curatedOfferedKeys"] == 1
assert result["requiredReciprocalPairs"] == 1 and result["activatedBaselinePairs"] == 0
assert result["changedReusedArticles"] == 1
assert result["exactWordChoiceLabels"] == [
    {"word": "寅", "label": "Tiger zodiac sign", "excludedWord": "虎", "excludedLabel": "tiger"}
]
assert (scope["root"] / "strokes" / "寅.json").read_bytes() == (
    control / "artifacts" / "batch-048-stroke-candidate.json").read_bytes()
baseline = scope["load"](scope["folder"] / "baseline-inventory.json")["files"]
assert not any("寅" in row.get("metadata", {}).get("kanji", [])
               for name, row in baseline.items() if name.startswith("words/"))
declared = {
    ("寅", f"words/{path.name}") for path in (scope["root"] / "words").glob("*.md")
    if "寅" in scope["metadata"](scope["root"], f"words/{path.name}").get("kanji", [])
}
assert declared == {("寅", "words/寅.md")}
for c, label in scope["ledger"]["wordQuizAudit"]["actualLabels"].items():
    assert scope["metadata"](scope["root"], f"words/{c}.md")["title"] == label
assert not any(term.lower() in (scope["root"] / "docs" / "confusable-words.md").read_text(
    encoding="utf-8").lower() for term in ("寅", "tiger", "zodiac"))
historical = {}
for name in (
    "batch-048-preparation-audit.json", "batch-048-qualified-source-audit.json",
    "batch-048-dictionary-evidence.json", "batch-048-input-metadata.json",
    "batch-048-membership.json", "batch-048-jmdict.xml", "batch-048-comparison-jmdict.xml",
    "batch-048-lexical-selection.json", "batch-048-comparison-selection.json",
):
    path = scope["folder"] / name
    before = scope["git"]("show", f"ec87c6dc9f69ed00f196d18e1433ccba21284127:docs/n1-sources/{name}")
    assert path.read_bytes().replace(b"\r\n", b"\n") == before.replace(b"\r\n", b"\n")
    historical[name] = hashlib.sha256(path.read_bytes()).hexdigest()
qualification = control / "execution-246-audit.py"
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
assert len(runtime) == 8272
assert sorted(scope["authored_missing"]) == ["宀", "氵"]
assert result["newFallbackNativePending"] == []
result["allRuntimePayloadHashesVerified"] = len(runtime)
result["declaredCurrentPairs"] = sorted(declared)
result["nativeFontDisposition"] = {
    "authoredHan": result["authoredTextHan"],
    "authoredHanInAllThreeBundledFonts": result["authoredTextHanInAllThreeFonts"],
    "authoredMissingGlyphs": sorted(scope["authored_missing"]),
    "newMissingGlyphsAcrossAuthoredAndComparisons": result["newFallbackNativePending"],
    "comparisonMissingGlyphs": sorted(scope["missing"]),
    "requiredGate": "Supported-native寅/演/黄/申 shape distinctions, explicit authored宀/氵systemfallback and compared虍/黃glyphs, actual fullarchiveContentSyncONCE/article/reciprocal/SystemBack/offline routes and bounded independent visual acceptance remain required before publication. Cmap/inheritedoccurrence is not readability; productionfonts/heaps/guards unchanged.",
}
result["historicalSourceReceiptsPreserved"] = historical
result["qualifiedSourceSectionsReverified"] = {
    "sections": 8, "distinctRawPages": 7, "geometryPaths": 11,
    "boundary": "Fresh bounded coordinator reads of all recorded sections and fullSVG; reused inspected audit prefix verifies exact section ranges/markers, raw hashes, geometry and converter candidate without old preparation audit side effects. No fresh retrieval or wholepage linguistic/native review.",
    "implementationSha256": hashlib.sha256(qualification.read_bytes()).hexdigest(),
}
result["runtimePayloadAdditions"] = ["kanji/寅.md", "words/寅.md", "strokes/寅.json"]
result["runtimePayloadChanges"] = ["kanji/演.md"]
result["auditImplementation"] = {
    "adapter": str(__file__), "reusedCompleteAudit": str(original),
    "reusedAuditSha256": hashlib.sha256(raw).hexdigest(),
    "scope": "Explicit048identities/counts and exact演linkdelta; preserves complete frozen inputs/exactdictionary re-extraction, fullbaseline, membership, reading/link, stroke/font, log checks plus allruntimehashes/currentdeclaredpair audit. Entire changed演article included in font checks, only exact recorded link passage authorized.",
}
scope["save"](control / "execution-252-source-audit.json", result)
print(json.dumps({
    "runtimeHashesVerified": len(runtime), "contentVersion": manifest["contentVersion"],
    "historicalReceiptsPreserved": True,
    "authoredMissingGlyphs": sorted(scope["authored_missing"]),
}, ensure_ascii=False))

result.update(execution=252, stage="mechanical-source-audit-at-native-visual-checkpoint",
    limits="Mechanical re-verification on unchanged teaching, not fresh linguistic/source-page/native acceptance. Original textual and bounded visual reviews retained separately; latest-main/publication and physical-phone/general-release pending.")
result["qualifiedSourceSectionsReverified"]["boundary"] = "Mechanical source hashes/ranges/markers and pinned geometry/converter candidate reverified using the inspected original qualification audit prefix. No fresh source-page/SVG comprehension or retrieval claimed in execution252; earlier author inspection remains historical."
scope["save"](control / "execution-252-source-audit.json", result)

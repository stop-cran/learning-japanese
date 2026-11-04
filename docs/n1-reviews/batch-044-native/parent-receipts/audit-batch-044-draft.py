"""Use the inspected baseline audit with explicit batch044 identities."""
import hashlib
import sys
from pathlib import Path

control = Path(__file__).resolve().parent
original = control / "audit-batch-040-draft.py"
raw = original.read_bytes()
source = raw.decode("utf-8")
assert sys.argv[1:] == ["audit"]
replacements = [
    ("batch-040", "batch-044"),
    ('"040"', '"044"'),
    ('execution": 175', 'execution": 211'),
    ("execution=175", "execution=211"),
    ("execution-175-", "execution-211-"),
    ("鵬", "亥"),
    ("range(2, 41)", "range(2, 45)"),
    ("len(expected_members) == 67", "len(expected_members) == 71"),
    ("== 1220", "== 17"),
    ('== "ほう"', '== "い"'),
    ("09d6c.svg", "04ea5.svg"),
    ("b4b30a4007689ef1316dc5b3f8584ce75dc6dc08", "9b11963ee7bf47b33e585046928fd281fe7fbead"),
    ("== 19", "== 6"),
    ('"strokeCount": 19', '"strokeCount": 6'),
    ('{"亥", "鳥", "朋", "月", "鳳", "鴻", "翼", "巨"}',
     '{"亥", "骸", "核", "刻", "猪", "豚", "亠"}'),
    ("publishedAdditions=66, remainingAdditions=1162",
     "publishedAdditions=70, remainingAdditions=1158"),
]
for before, after in replacements:
    assert before in source, before
    source = source.replace(before, after)
scope = {"__file__": str(__file__), "__name__": "__main__"}
exec(compile(source, str(__file__), "exec"), scope)
result = scope["result"]
assert result["pythonTests"] == {"passed": 361, "failures": 0, "errors": 0}
assert len(scope["ids"]) == 36 and result["manifestFresh"]
assert result["currentKanjiIncludingDrafts"] == 1056
assert result["currentWordsIncludingDrafts"] == 5014
assert result["n1LabelledIncludingDrafts"] == 76
assert result["sourceMembersPresentIncludingDrafts"] == 75
assert result["readingDispositions"] == 3 and result["curatedOfferedKeys"] == 1
assert result["requiredReciprocalPairs"] == 1 and result["activatedBaselinePairs"] == 0
assert not result["exactWordChoiceLabels"]
assert scope["load"](scope["root"] / "strokes" / "亥.json") == scope["load"](
    control / "artifacts" / "batch-044-stroke-candidate.json")
result["nativeFontDisposition"] = {
    "authoredHan": result["authoredTextHan"],
    "authoredHanInAllThreeBundledFonts": result["authoredTextHanInAllThreeFonts"],
    "authoredMissingGlyphs": sorted(scope["authored_missing"]),
    "newMissingGlyphsAcrossAuthoredAndComparisons": result["newFallbackNativePending"],
    "requiredGate": "Fresh supported-native content, fallback/readability and visual acceptance remain required before publication. Cmap presence and inherited occurrences are not native/phone evidence. Fonts and app guards unchanged.",
}
result["auditImplementation"] = {
    "adapter": str(__file__),
    "reusedCompleteAudit": str(original),
    "reusedAuditSha256": hashlib.sha256(raw).hexdigest(),
    "scope": "Explicit044 identity/count substitutions; source-stage extraction mode not executed. Full frozen inputs, complete dictionary re-extraction, baseline, exact membership, reading/link, stroke/font and validation-log checks retained.",
}
scope["save"](scope["folder"] / "batch-044-draft-audit.json", result)

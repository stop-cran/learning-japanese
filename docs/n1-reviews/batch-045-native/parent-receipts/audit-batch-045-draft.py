"""Use the inspected baseline audit with explicit batch045 identities."""
import hashlib
import sys
from pathlib import Path

control = Path(__file__).resolve().parent
original = control / "audit-batch-040-draft.py"
raw = original.read_bytes()
source = raw.decode("utf-8")
assert sys.argv[1:] == ["audit"]
replacements = [
    ("batch-040", "batch-045"),
    ('"040"', '"045"'),
    ('execution": 175', 'execution": 220'),
    ("execution=175", "execution=220"),
    ("execution-175-", "execution-220-"),
    ("鵬", "巳"),
    ("range(2, 41)", "range(2, 46)"),
    ("len(expected_members) == 67", "len(expected_members) == 72"),
    ("== 1220", "== 300"),
    ('== "ほう"', '== "み"'),
    ("09d6c.svg", "05df3.svg"),
    ("b4b30a4007689ef1316dc5b3f8584ce75dc6dc08", "a1786fec005c3fad7ae402595262face43019f45"),
    ("== 19", "== 3"),
    ('"strokeCount": 19', '"strokeCount": 3'),
    ('{"巳", "鳥", "朋", "月", "鳳", "鴻", "翼", "巨"}',
     '{"巳", "蛇", "己", "已", "亥", "年"}'),
    ("publishedAdditions=66, remainingAdditions=1162",
     "publishedAdditions=71, remainingAdditions=1157"),
]
for before, after in replacements:
    assert before in source, before
    source = source.replace(before, after)
scope = {"__file__": str(__file__), "__name__": "__main__"}
exec(compile(source, str(__file__), "exec"), scope)
result = scope["result"]
assert result["pythonTests"] == {"passed": 361, "failures": 0, "errors": 0}
assert len(scope["ids"]) == 32 and result["manifestFresh"]
assert result["currentKanjiIncludingDrafts"] == 1057
assert result["currentWordsIncludingDrafts"] == 5015
assert result["n1LabelledIncludingDrafts"] == 77
assert result["sourceMembersPresentIncludingDrafts"] == 76
assert result["readingDispositions"] == 2 and result["curatedOfferedKeys"] == 1
assert result["requiredReciprocalPairs"] == 1 and result["activatedBaselinePairs"] == 0
assert result["exactWordChoiceLabels"] == [{
    "word": "巳", "label": "Snake zodiac sign",
    "excludedWord": "蛇", "excludedLabel": "snake; serpent",
}]
assert scope["load"](scope["root"] / "strokes" / "巳.json") == scope["load"](
    control / "artifacts" / "batch-045-stroke-candidate.json")
assert scope["metadata"](scope["root"], "kanji/蛇.md")["distractors"] == ["虫", "蚊", "蛍"]
baseline = scope["load"](scope["folder"] / "baseline-inventory.json")["files"]
assert not any("巳" in row.get("metadata", {}).get("kanji", [])
               for name, row in baseline.items() if name.startswith("words/"))
historical = {}
for name in ("batch-045-preparation-audit.json", "batch-045-qualified-source-audit.json"):
    path = scope["folder"] / name
    base = scope["git"]("show", f"56f225b052792ad29aa922bdd67280062bd4e86f:docs/n1-sources/{name}")
    assert path.read_bytes().replace(b"\r\n", b"\n") == base.replace(b"\r\n", b"\n")
    historical[name] = hashlib.sha256(path.read_bytes()).hexdigest()
result["nativeFontDisposition"] = {
    "authoredHan": result["authoredTextHan"],
    "authoredHanInAllThreeBundledFonts": result["authoredTextHanInAllThreeFonts"],
    "authoredMissingGlyphs": sorted(scope["authored_missing"]),
    "newMissingGlyphsAcrossAuthoredAndComparisons": result["newFallbackNativePending"],
    "requiredGate": "Supported-native巳/己/已 distinctions and canonical-radical readability, actual article/reciprocal/SystemBack/offline routes and bounded independent visual acceptance remain required before publication. Inherited occurrences and cmap presence are not new native evidence. Production fonts, heaps and guards unchanged.",
}
result["historicalSourceReceiptsPreserved"] = historical
result["runtimePayloadAdditions"] = ["kanji/巳.md", "words/巳.md", "strokes/巳.json"]
result["runtimePayloadChanges"] = []
result["auditImplementation"] = {
    "adapter": str(__file__),
    "reusedCompleteAudit": str(original),
    "reusedAuditSha256": hashlib.sha256(raw).hexdigest(),
    "scope": "Explicit045 identity/count substitutions; source-stage extraction mode not executed. Full frozen inputs, complete dictionary re-extraction, baseline, exact membership, reading/link, stroke/font and validation-log checks retained.",
}
scope["save"](scope["folder"] / "batch-045-draft-audit.json", result)

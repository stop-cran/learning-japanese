"""Bounded adapter of the inspected batch040 audit; no repository tool changes."""
import hashlib
import sys
from pathlib import Path

control = Path(__file__).resolve().parent
original = control / "audit-batch-040-draft.py"
raw = original.read_bytes()
source = raw.decode("utf-8")
assert sys.argv[1:] == ["audit"]
replacements = [
    ("batch-040", "batch-043"),
    ('"040"', '"043"'),
    ('execution": 175', 'execution": 202'),
    ("execution=175", "execution=202"),
    ("execution-175-", "execution-202-"),
    ("鵬", "麟"),
    ("range(2, 41)", "range(2, 44)"),
    ("len(expected_members) == 67", "len(expected_members) == 70"),
    ("== 1220", "== 1226"),
    ('"words/麟.md"', '"words/麒麟.md"'),
    ('== "ほう"', '== "きりん"'),
    ("09d6c.svg", "09e9f.svg"),
    ("b4b30a4007689ef1316dc5b3f8584ce75dc6dc08", "b9111b32021522c426032f851b7477c167d1ffdf"),
    ("== 19", "== 24"),
    ('"strokeCount": 19', '"strokeCount": 24'),
    ('{"麟", "鳥", "朋", "月", "鳳", "鴻", "翼", "巨"}',
     '{"麟", "鹿", "麒", "粦", "燐", "隣"}'),
    ('{"word": "麟", "label":', '{"word": "麒麟", "label":'),
    ("publishedAdditions=66, remainingAdditions=1162",
     "publishedAdditions=69, remainingAdditions=1159"),
]
for before, after in replacements:
    assert before in source, before
    source = source.replace(before, after)
scope = {"__file__": str(__file__), "__name__": "__main__"}
exec(compile(source, str(__file__), "exec"), scope)
result = scope["result"]
assert result["pythonTests"] == {"passed": 361, "failures": 0, "errors": 0}
assert len(scope["ids"]) == 50 and result["manifestFresh"]
assert result["currentKanjiIncludingDrafts"] == 1055
assert result["currentWordsIncludingDrafts"] == 5013
assert result["n1LabelledIncludingDrafts"] == 75
assert result["sourceMembersPresentIncludingDrafts"] == 74
assert result["readingDispositions"] == result["curatedOfferedKeys"] == 1
assert len(result["exactWordChoiceLabels"]) == 11
assert result["newFallbackNativePending"] == ["粦", "騏", "驎", "麒"]
assert scope["authored_missing"] == {"凰", "粦", "騏", "驎", "麒"}
result["nativeFontDisposition"] = {
    "authoredHan": 28,
    "authoredHanInAllThreeBundledFonts": 23,
    "inheritedAuthoredMissingGlyphs": ["凰"],
    "newAuthoredMissingGlyphs": ["粦", "騏", "驎", "麒"],
    "requiredGate": "Fresh supported-native fallback/readability and visual evidence for all authored missing glyphs, plus applicable comparison广, before publication. No font changes or acceptance inferred from inherited occurrences.",
    "initialAuditAssertion": "The reused previous-batch zero-new-missing assertion failed on the exact four new glyphs. Preserve this discovery; the bounded draft records pending native gates, not a font pass or deletion of necessary teaching.",
}
result["auditImplementation"] = {
    "adapter": str(__file__),
    "reusedCompleteAudit": str(original),
    "reusedAuditSha256": hashlib.sha256(raw).hexdigest(),
    "scope": "Same frozen source/baseline/guard/geometry/font/log checks with explicit043 identities/counts; no source-stage extraction mode executed.",
}
scope["save"](scope["folder"] / "batch-043-draft-audit.json", result)

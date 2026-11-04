import gzip
import hashlib
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

control = Path(__file__).resolve().parent
root = control.parent / "learning-japanese"
android = control.parent / "kanji-cards-android"
folder = root / "docs" / "n1-sources"
sys.path.insert(0, str(root / "tools"))
from audit_n1_batch import audit
from audit_n1_pilot import metadata
from build_manifest import sha256
from check_content_budget import archive_names, check
from extract_n1_jmdict import extract
from fontTools.ttLib import TTFont
from generate_strokes import KANJIVG_REVISION, convert


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def git(*args, tree=root):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=tree)


snapshot = load(root / "docs" / "n1-source-snapshot.json")
for name, row in snapshot["inputs"].items():
    assert digest((control / "inputs" / name).read_bytes()) == row["sha256"], name
dictionary = (control / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
entries = ET.fromstring(gzip.decompress(dictionary)).findall("entry")
assert digest(gzip.decompress(dictionary)) == snapshot["jmdict"]["xmlSha256"]
characters_raw = gzip.decompress((control / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes())
assert digest(characters_raw) == snapshot["kanjidic2"]["xmlSha256"]
ledger = load(folder / "batch-040-progress.json")

if sys.argv[1] == "extract":
    excluded = {value for packet in ledger["dictionaryPackets"][:2]
                for value in load(folder / packet["selection"])["entryIds"]}
    forms = {"動物", "生き物", "生物"}
    ids = [entry.findtext("ent_seq") for entry in entries
           if {value.text for value in entry.findall("k_ele/keb") + entry.findall("r_ele/reb")} & forms
           and entry.findtext("ent_seq") not in excluded]
    selection_path = folder / "batch-040-support-comparison-selection.json"
    xml_path = folder / "batch-040-support-comparison-jmdict.xml"
    assert not selection_path.exists() and not xml_path.exists()
    save(selection_path, {"schemaVersion": 1, "batch": "040", "entryIds": ids,
                          "selectionSpellings": sorted(forms),
                          "provenance": "Complete frozen exact spelling/reading families, excluding the original two packets.",
                          "limits": "Recognition and restrictions, not frequency or unrestricted synonymy."})
    raw = extract(dictionary, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
    xml_path.write_bytes(raw)
    print(json.dumps({"families": len(ids), "lines": len(raw.splitlines()), "sha256": digest(raw)}))
    sys.exit(0)

assert sys.argv[1] == "audit"
result = audit(root, "040")
ids, packets = set(), []
for packet in ledger["dictionaryPackets"]:
    selection = load(folder / packet["selection"])
    raw = (folder / packet["xml"]).read_bytes()
    assert raw == extract(dictionary, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], selection["entryIds"])
    assert not ids & set(selection["entryIds"])
    if "lexical-selection" in packet["selection"]:
        expected_ids = [entry.findtext("ent_seq") for entry in entries
                        if any("鵬" in (value.text or "") for value in entry.findall("k_ele/keb") + entry.findall("r_ele/reb"))]
    else:
        forms = set(selection["selectionSpellings"])
        expected_ids = [entry.findtext("ent_seq") for entry in entries
                        if {value.text for value in entry.findall("k_ele/keb") + entry.findall("r_ele/reb")} & forms
                        and entry.findtext("ent_seq") not in ids]
    assert selection["entryIds"] == expected_ids, packet
    ids.update(selection["entryIds"])
    packets.append({"path": packet["xml"], "families": len(selection["entryIds"]),
                    "lines": len(raw.splitlines()), "sha256": digest(raw)})
assert len(ids) == ledger["extractedDistinctFamilies"]
raw_meta = load(folder / "batch-040-input-metadata.json")["rawCharacterElements"]
assert raw_meta == {entry.findtext("literal"): ET.tostring(entry, encoding="unicode")
                    for entry in ET.fromstring(characters_raw).findall("character")
                    if entry.findtext("literal") in {"鵬", "鳥", "朋", "月", "鳳", "鴻", "翼", "巨"}}
baseline = load(folder / "baseline-inventory.json")
exceptions = {"words/虎.md": ["酔っ払い"], "words/猿.md": ["馬鹿"]}
counts = {"kanji": 0, "words": 0, "strokes": 0}
for name, row in baseline["files"].items():
    kind = name.split("/")[0]
    if kind in ("kanji", "words"):
        expected = dict(row["metadata"])
        if name in exceptions:
            expected["quiz_exclusions"] = exceptions[name]
        assert metadata(root, name) == expected, name
        counts[kind] += 1
    elif kind == "strokes":
        assert digest((root / name).read_bytes()) == row["sha256"], name
        counts[kind] += 1
assert counts == {"kanji": 985, "words": 4942, "strokes": 985}
expected_members = {row["kanji"] for row in load(folder / "pilot-membership.json")["members"]}
for number in range(2, 41):
    expected_members.update(load(folder / f"batch-{number:03}-membership.json")["membership"])
original = {Path(name).stem for name in baseline["files"] if name.startswith("kanji/")}
current = {path.stem for path in (root / "kanji").glob("*.md")}
assert current - original == expected_members and not original - current and len(expected_members) == 67
assert {path.stem for path in (root / "strokes").glob("*.json")} == current
community = set(load(folder / "community-list-20261102.json"))
assert community & current == {"士", "奇", "怪", "訳"} | expected_members
assert "妖" in current and "妖" not in community
index = {row["kanji"]: row for row in load(folder / "source-index.json")}
for char in expected_members:
    meta = metadata(root, f"kanji/{char}.md")
    for field in ("kanji", "strokes", "radical", "radicalNumber", "onyomi", "kunyomi"):
        assert meta[field] == index[char]["metadata"][field], (char, field)
    assert meta["jlpt"] == 1
assert index["鵬"]["sourceRow"] == 1220
assert metadata(root, "words/鵬.md")["reading"] == "ほう"
assert "jlpt" not in metadata(root, "words/鵬.md")
svg = (control / "artifacts" / "batch-040-09d6c.svg").read_bytes()
blob = hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest()
assert blob == index["鵬"]["kanjivgInventory"]["sha"] == "b4b30a4007689ef1316dc5b3f8584ce75dc6dc08"
stroke_path = root / "strokes" / "鵬.json"
assert convert("鵬", svg.decode("utf-8")) == load(stroke_path)
assert load(stroke_path)["strokeCount"] == 19
authored = ["kanji/鵬.md", "words/鵬.md"]
comparisons = ledger["wordQuizAudit"]["comparisonArticles"] + ledger["wordQuizAudit"]["comparisonKanji"]
texts = {name: (root / name).read_text(encoding="utf-8") for name in authored + comparisons}
for name in comparisons:
    assert texts[name].encode().replace(b"\r\n", b"\n") == git("show", f"{ledger['baseCommit']}:{name}").replace(b"\r\n", b"\n"), name


def han(text):
    return {char for char in text if "\u3400" <= char <= "\u9fff" or "\U00020000" <= char <= "\U000323af"}


authored_han = han("".join(texts[name] for name in authored))
all_han = han("".join(texts.values()))
fonts, missing, authored_missing = [], set(), set()
for row in load(folder / "font-coverage.json")["fonts"]:
    path = android / row["path"]
    assert digest(path.read_bytes()) == row["sha256"]
    with TTFont(path) as font:
        checks = {char: ord(char) in font.getBestCmap() for char in sorted(all_han)}
    missing.update(char for char, present in checks.items() if not present)
    authored_missing.update(char for char in authored_han if not checks[char])
    fonts.append({"path": row["path"], "sha256": row["sha256"], "glyphs": checks})
inherited_occurrences = {}
for char in sorted(missing):
    process = subprocess.run(["git", "--no-pager", "-c", "core.quotepath=false", "grep", "-l", "-F",
                              char, ledger["baseCommit"], "--", "kanji", "words", "articles"],
                             cwd=root, capture_output=True)
    assert process.returncode in (0, 1)
    inherited_occurrences[char] = [line.split(":", 1)[1] for line in process.stdout.decode().splitlines()]
new_missing = {char for char in missing if not inherited_occurrences[char]}
stroke_record = {
    "schemaVersion": 1, "execution": 175, "batch": "040", "revision": KANJIVG_REVISION,
    "converter": "tools/generate_strokes.py",
    "cards": [{"kanji": "鵬", "svgGitBlob": blob, "svgSha256": digest(svg),
               "svgLines": len(svg.splitlines()), "strokeCount": 19,
               "strokeSha256": digest(stroke_path.read_bytes()), "exactPinnedReconversionEqual": True}],
    "runtimeStrokeManifestSha256": sha256(stroke_path),
    "authoredFilesAuditedWhole": authored, "comparisonFilesAuditedWhole": comparisons,
    "authoredTextHan": len(authored_han), "allAuthoredAndComparisonHan": len(all_han),
    "fontCmapChecks": fonts, "missingBundledGlyphs": sorted(missing),
    "authoredMissingBundledGlyphs": sorted(authored_missing),
    "inheritedExactBaseOccurrences": inherited_occurrences, "newMissingBundledGlyphs": sorted(new_missing),
    "limits": "Exact pinned conversion and cmap checks, not supported-native readability or visual acceptance. Inherited occurrences are not fresh native evidence. Production fonts unchanged; applicable native/visual acceptance remains pending."
}
save(folder / "batch-040-stroke-audit.json", stroke_record)
external = load(folder / "batch-040-dictionary-evidence.json")
for row in external["sources"]:
    raw = (control.parent / row["rawArtifact"]).read_bytes()
    assert digest(raw) == row["rawSha256"] and len(raw) == row["rawBytes"]
logs = {}
for name in ("python-tests", "validate", "vocabulary", "manifest", "budget"):
    path = control / "logs" / f"execution-175-{name}.txt"
    text = path.read_text(encoding="utf-8-sig")
    if name == "python-tests":
        match = re.search(r"Ran (\d+) tests", text)
        assert match and re.search(r"(?m)^OK\s*$", text) and "FAILED (" not in text
        test_count = int(match[1])
    if name == "validate":
        assert "0 error(s)" in text
    logs[name] = {"path": str(path), "sha256": digest(path.read_bytes()), "exitCode": 0}
assert not git("status", "--porcelain", tree=android)
assert git("rev-parse", "HEAD", tree=android).decode().strip() == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
result.update(
    schemaVersion=1, execution=175, stage="validated-local-draft-not-independently-reviewed",
    frozenInputHashesVerified=len(snapshot["inputs"]), decompressedDictionaryHashesVerified=2,
    freshExactDictionaryExtractions=len(packets), dictionaryPackets=packets, rawCharacterRecords=len(raw_meta),
    originalBaselineMetadataAndStrokesPreserved=counts, baselineMetadataExceptions=exceptions,
    exactLocalAdditionMembership=sorted(expected_members), currentKanjiIncludingDrafts=len(current),
    currentWordsIncludingDrafts=len(list((root / "words").glob("*.md"))),
    n1LabelledIncludingDrafts=sum(metadata(root, f"kanji/{c}.md")["jlpt"] == 1 for c in current),
    sourceMembersPresentIncludingDrafts=len(current & community),
    authoredTextHan=len(authored_han), authoredTextHanInAllThreeFonts=len(authored_han) - len(authored_missing),
    newFallbackNativePending=sorted(new_missing), externalNamedEntryReceiptsVerified=len(external["sources"]),
    exactWordChoiceLabels=[{"word": "鵬", "label": metadata(root, "words/鵬.md")["title"],
                           "excludedWord": name, "excludedLabel": metadata(root, f"words/{name}.md")["title"]}
                          for name in metadata(root, "words/鵬.md")["quiz_exclusions"]],
    budget=check(root, archive_names(root)), pythonTests={"passed": test_count, "failures": 0, "errors": 0},
    validationLogs=logs, publishedAdditions=66, remainingAdditions=1162,
    reviewersLaunched=0, freshAndroidOrNativeClaimed=False, limits=ledger["limits"])
save(folder / "batch-040-draft-audit.json", result)
print(json.dumps({key: result[key] for key in ("dictionaryFamilies", "authoredTextHan",
                 "authoredTextHanInAllThreeFonts", "newFallbackNativePending", "pythonTests", "budget")}, ensure_ascii=False))

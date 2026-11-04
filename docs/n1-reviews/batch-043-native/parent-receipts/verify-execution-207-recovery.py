import hashlib
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

control = Path(__file__).resolve().parent
root = control.parent / "learning-japanese"
snapshot = "f4e7d506c9f6cdacd1d1a406eebe891fe283ac87"


def text(path):
    raw = path.read_bytes()
    return raw.decode("utf-16" if raw.startswith((b"\xff\xfe", b"\xfe\xff")) else "utf-8-sig").replace("\r\n", "\n")


def load(path):
    return json.loads(text(path))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


provenance = load(control / "batch-043-parent-native-provenance.json")
index = load(control / "batch-043-parent-native-artifact-index.json")
android_provenance = load(control / "batch-043-parent-android-provenance.json")
for row in provenance + index + android_provenance:
    assert digest(Path(row["path"])) == row["sha256"], row["path"]
log = text(control / "logs" / "batch-043-parent-native-attempt-2.txt")
assert re.findall(r"INSTRUMENTATION_STATUS_CODE: (-?\d+)", log) == ["1", "0", "1", "0"]
assert "OK (2 tests)" in log
for name in ("fullSingleImportOfflineQilinArticleAndSystemBack", "qilinAndFallbacksAcrossFourProductionFamilies"):
    assert log.count("INSTRUMENTATION_STATUS: test=" + name) == 2
failed = text(control / "logs" / "batch-043-parent-native-attempt-1.txt")
assert re.findall(r"INSTRUMENTATION_STATUS_CODE: (-?\d+)", failed) == ["1", "-2", "1", "0"]
artifacts = control / "artifacts" / "batch-043-parent-native-attempt-2"
route = load(artifacts / "n1-043-article-route.json")
assert route["contentSnapshot"] == snapshot and route["contentVersion"] == "e86891b100028fa9"
assert [route[k] for k in ("archiveRequests", "importedKanji", "importedWords", "n1Cards", "problems", "acceptedReadingParserEpoch")] == [1, 1055, 5013, 75, 0, 1]
assert route["fullOnyomi"] == ["リン"] and route["fullKunyomi"] == []
assert route["quizOnKeys"] == ["りん"] and route["quizKunKeys"] == []
assert route["passed"] and route["offline"] and route["reciprocalLinkAndSystemBack"]
assert not route["phoneEvidence"] and not route["sessionOrDrawingRetest"]
fixture = root / "docs" / "n1-reviews" / "batch-043-native" / "N1Batch043NativeTest.kt"
assert fixture.read_bytes() == (artifacts / fixture.name).read_bytes()
assert digest(fixture) == "913bcaf95ffb85d2e601f9cc6a52d28d59bf4f3a03d6d615892fc95f7648aeff"
original = control / "artifacts" / "batch-043-parent-native-attempt-1" / fixture.name
assert digest(original) == "2e550b60e997beef4d981931daf6eec33dd289528a535e631d71efb5c80e3a9a"
before = 'assertEquals(listOf("リン"), qilin.toReadingCard().quizKeys(ReadingKind.On))'
after = 'assertEquals(listOf("りん"), qilin.toReadingCard().quizKeys(ReadingKind.On))'
assert text(original).count(before) == 1
assert text(fixture) == text(original).replace(before, after)
raster = load(artifacts / "n1-043-font-raster.json")
assert len(raster["rows"]) == 32 and all(r["hasGlyph"] for r in raster["rows"])
styles = {}
for character in ("麟", "鹿", "凰", "广", "粦", "騏", "驎", "麒"):
    rows = [r for r in raster["rows"] if r["character"] == character]
    assert len(rows) == 4 and {r["font"] for r in rows} == {"Gothic", "Mincho", "Textbook", "Brush"}
    styles[character] = len({r["nativePaintRasterSha256"] for r in rows})
    assert styles[character] == (4 if character in "麟鹿" else 1)
for left, right in (("word-qilin-example", "word-giraffe-example"), ("backlink-kanji", "kanji-mnemonic"),
                    ("system-back-word", "word-components"), ("word-person-sense", "word-rare-spelling")):
    assert digest(artifacts / f"n1-043-{left}.png") == digest(artifacts / f"n1-043-{right}.png")
android = load(control / "batch-043-parent-android-recovery.json")
assert [row["tests"] for row in android["tests"]] == [3, 1]
for row in android["tests"]:
    assert digest(Path(row["sourcePath"])) == digest(Path(row["artifactPath"])) == row["sha256"]
    suite = ET.parse(row["artifactPath"]).getroot()
    assert suite.attrib["name"] == row["name"] and suite.attrib["timestamp"] == row["timestamp"]
    for key in ("tests", "errors", "failures", "skipped"):
        assert int(suite.attrib[key]) == row[key]
    assert row["errors"] == row["failures"] == row["skipped"] == 0
    assert sorted(c.attrib["name"] for c in suite.findall("testcase")) == sorted(row["caseNames"])
    assert row["fixtureRoot"] == str(root)
cleanup = load(control / "batch-043-parent-native-cleanup.json")
assert cleanup["ownedProcessesStopped"] == [22568, 12668]
assert cleanup["exactTemporaryAndroidFilesRemoved"] and cleanup["androidClean"] and cleanup["contentTrackedUnchanged"]
android_root = control.parent / "kanji-cards-android"
for path in (android_root / "app" / "src" / "androidTest" / "java" / "io" / "github" / "stopcran" / "kanji" / "ui" / fixture.name,
             android_root / "app" / "src" / "androidTest" / "assets" / "n1-batch-043-f4e7d50-envelope.zip"):
    assert not path.exists()
assert not subprocess.check_output(["git", "status", "--porcelain"], cwd=android_root)
assert not subprocess.check_output(["git", "diff", snapshot, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools"], cwd=root)
audit = load(root / "docs" / "n1-sources" / "batch-043-review-audit.json")
for row in audit["reviewProcesses"]:
    assert digest(root / "docs" / "n1-reviews" / f'batch-043-{row["label"]}.md') == row["reportSha256"]
    assert digest(control / f'batch-043-{row["label"]}.jsonl') == row["rawExecutionSha256"]
result = {
    "schemaVersion": 1, "execution": 207, "batch": "043",
    "verifiedParentProvenanceAndArtifactHashes": len(provenance) + len(index) + len(android_provenance),
    "acceptedNativeAttempt": 2, "terminalCodes": [1, 0, 1, 0],
    "failedAttemptPreserved": 1, "exactNormalizedKeyExpectationCorrectionVerified": True,
    "glyphProbes": 32, "distinctRasterStylesPerCharacter": styles,
    "freshAndroidTests": [3, 1], "failuresErrorsSkips": 0,
    "originalReportsAndRawExecutionsVerified": 2, "runtimeUnchanged": True,
    "limits": "Mechanical verification only; independent original-reviewer visual pending. Six fallback characters share one style; no claim of four designs or identified fallback face. No build/native/Android rerun or publication. Original normalized-key failure retained; raw/curated katakana assertions unchanged.",
}
(control / "execution-207-recovery-verification.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Verified SAME043 attempt2 terminal0/0, exact key-only fixture fix, all recovery hashes,32probes and fresh204Android3+1.")

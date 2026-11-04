import hashlib
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

control = Path(__file__).resolve().parent
root = control.parent / "learning-japanese"
snapshot = "01b3d3b2f0fc0fceca382d0ce54d91c13ab464a1"


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


provenance = load(control / "batch-045-parent-native-provenance.json")
index = load(control / "batch-045-parent-native-artifact-index.json")
android_provenance = load(control / "batch-045-parent-android-provenance.json")
for row in provenance + index + android_provenance:
    assert digest(Path(row["path"])) == row["sha256"], row["path"]
log = (control / "logs" / "batch-045-parent-native-attempt-1.txt").read_text(encoding="utf-8-sig")
assert re.findall(r"INSTRUMENTATION_STATUS_CODE: (-?\d+)", log) == ["1", "0", "1", "0"]
assert "OK (2 tests)" in log
for name in ("fullSingleImportOfflineSnakeSignArticleAndSystemBack", "snakeSignRadicalAndLookalikesAcrossFourProductionFamilies"):
    assert log.count("INSTRUMENTATION_STATUS: test=" + name) == 2
artifacts = control / "artifacts" / "batch-045-parent-native-attempt-1"
route = load(artifacts / "n1-045-article-route.json")
assert route["contentSnapshot"] == snapshot and route["contentVersion"] == "c0c51142ac779ed8"
assert [route[k] for k in ("archiveRequests", "importedKanji", "importedWords", "n1Cards", "problems", "acceptedReadingParserEpoch")] == [1, 1057, 5015, 77, 0, 1]
assert route["fullOnyomi"] == ["シ"] and route["fullKunyomi"] == ["み"]
assert route["quizOnKeys"] == [] and route["quizKunKeys"] == ["み"]
assert route["passed"] and route["offline"] and route["reciprocalLinkAndSystemBack"]
assert not route["phoneEvidence"] and not route["sessionOrDrawingRetest"]
fixture = root / "docs" / "n1-reviews" / "batch-045-native" / "N1Batch045NativeTest.kt"
assert fixture.read_bytes() == (artifacts / fixture.name).read_bytes()
assert digest(fixture) == "8fea7eaa7dbc8e4db7814e168c2462ad748565cca6041b7e593fa711ab9cbc70"
raster = load(artifacts / "n1-045-font-raster.json")
assert len(raster["rows"]) == 28 and all(r["hasGlyph"] for r in raster["rows"])
styles = {}
for character in "包己已巳巻蛇記":
    rows = [r for r in raster["rows"] if r["character"] == character]
    assert len(rows) == 4 and {r["font"] for r in rows} == {"Gothic", "Mincho", "Textbook", "Brush"}
    styles[character] = len({r["nativePaintRasterSha256"] for r in rows})
    assert styles[character] == (1 if character == "已" else 4)
for left, right in load(control / "batch-045-parent-native-recovery.json")["visual"]["additionalHashEquivalentViewports"]:
    assert digest(artifacts / f"n1-045-{left}.png") == digest(artifacts / f"n1-045-{right}.png")
android = load(control / "batch-045-parent-android-recovery.json")
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
cleanup = load(control / "batch-045-parent-native-cleanup.json")
assert cleanup["ownedProcessStopped"] == 14844
assert cleanup["exactTemporaryAndroidFilesRemoved"] and cleanup["androidClean"] and cleanup["contentTrackedUnchanged"]
android_root = control.parent / "kanji-cards-android"
for path in (android_root / "app" / "src" / "androidTest" / "java" / "io" / "github" / "stopcran" / "kanji" / "ui" / fixture.name,
             android_root / "app" / "src" / "androidTest" / "assets" / "n1-batch-045-01b3d3b-envelope.zip"):
    assert not path.exists()
assert not subprocess.check_output(["git", "status", "--porcelain"], cwd=android_root)
assert not subprocess.check_output(["git", "diff", snapshot, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools"], cwd=root)
audit = load(root / "docs" / "n1-sources" / "batch-045-review-audit.json")
for row in audit["reviewProcesses"]:
    assert digest(root / "docs" / "n1-reviews" / f'batch-045-{row["label"]}.md') == row["reportSha256"]
    assert digest(control / f'batch-045-{row["label"]}.jsonl') == row["rawExecutionSha256"]
result = {
    "schemaVersion": 1, "execution": 225, "batch": "045",
    "verifiedParentProvenanceAndArtifactHashes": len(provenance) + len(index) + len(android_provenance),
    "acceptedNativeAttempt": 1, "terminalCodes": [1, 0, 1, 0],
    "fixtureUnchanged": True, "glyphProbes": 28, "distinctRasterStylesPerCharacter": styles,
    "freshAndroidTests": [3, 1], "failuresErrorsSkips": 0,
    "originalReportsAndRawExecutionsVerified": 2, "runtimeUnchanged": True,
    "limits": "Mechanical verification only; original-reviewer visual pending. 已 shares one fallback style, exact face unidentified. No Android/native rerun or publication.",
}
(control / "execution-225-recovery-verification.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Verified SAME045 original attempt1 terminal0/0,28probes, two original reports and fresh222Android3+1.")

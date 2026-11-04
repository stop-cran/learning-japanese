import difflib
import hashlib
import json
import re
import subprocess
import xml.etree.ElementTree as ET
import zipfile
from datetime import datetime, timezone
from pathlib import Path

c = Path(__file__).parent
r = c.parent / "learning-japanese"
head = "cec76575d6e2b15560144ff118cc4261ba1881de"
teaching = "ca54f1e910522d76f42732fa10ee1a8a6ef1359f"
load = lambda p: json.loads(Path(p).read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()


def save(path, value):
    assert not path.exists(), path
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=r, text=True).strip() == head
assert not subprocess.check_output(["git", "diff", teaching, "--", "kanji", "words", "articles", "strokes", "manifest.json"], cwd=r)
verified = []
for kind in ["native", "android"]:
    for row in load(c / f"batch-051-parent-{kind}-provenance.json"):
        assert sha(row["path"]) == row["sha256"], row["path"]
        verified.append(row)
n = load(c / "batch-051-parent-native-recovery.json")
a = load(c / "batch-051-parent-android-recovery.json")
attempts = []
for attempt in n["attempts"]:
    index = load(attempt["artifactIndex"])
    assert len(index) == attempt["artifactCount"]
    for row in index:
        assert sha(row["path"]) == row["sha256"], row["path"]
    log = Path(attempt["log"]).read_text(encoding="utf-8-sig")
    codes = [int(x) for x in re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)$", log, re.M)]
    assert codes == ([1, -2, 1, 0] if attempt["attempt"] < 3 else [1, 0, 1, 0]), codes
    route = load(next(x["path"] for x in index if x["path"].endswith("article-route.json")))
    assert route == attempt["route"]
    assert route["archiveRequests"] == 1 and route["problems"] == 0
    assert (route["importedKanji"], route["importedWords"], route["n1Cards"]) == (1063, 5021, 83)
    assert route["contentVersion"] == "a90e66e16d24c25d"
    assert route["fullOnyomi"] == [] and route["fullKunyomi"] == ["もんめ", "め"]
    assert route["quizOnKeys"] == [] and route["quizKunKeys"] == ["もんめ"]
    assert route["acceptedReadingParserEpoch"] == 1
    assert f'Time: {attempt["durationSeconds"]}' in log
    if attempt["attempt"] >= 3:
        assert "OK (2 tests)" in log
        assert all(route[k] for k in [
            "passed", "offline", "reciprocalLinkAndSystemBack", "meaningQuestionAndFeedback",
            "curatedKunQuestionAndPersistedGrade", "drawingTraceThenRecall", "drawingGradeRecordedOnNext",
        ])
        assert route["touchInjectedReferenceStrokes"] == 4
    attempts.append({**attempt, "verifiedArtifactHashes": len(index), "actualStatusCodes": codes})
original = Path(n["fixture"]["originalUnchanged"])
variant = Path(n["fixture"]["separateAcceptedVariant"])
assert sha(original) == n["fixture"]["originalSha256"]
assert sha(variant) == n["fixture"]["acceptedSha256"]
old = original.read_text(encoding="utf-8")
new = variant.read_text(encoding="utf-8")
expected = old.replace(
    'await("匁 もんめ — monme", substring = true)',
    'await("匁 もんめ — monme, a traditional mass unit", substring = true)',
).replace(
    "    private fun click(node: SemanticsNodeInteraction) {\n",
    "    private fun click(node: SemanticsNodeInteraction) {\n"
    "        rule.waitUntil(30_000) { !node.fetchSemanticsNode().config.contains(SemanticsProperties.Disabled) }\n",
).replace(
    "        automation.waitForIdle(500, 5_000)\n",
    "        automation.waitForIdle(500, 5_000)\n"
    "        android.os.SystemClock.sleep(1_000)\n        rule.waitForIdle()\n",
)
assert new == expected
diff = "".join(difflib.unified_diff(old.splitlines(True), new.splitlines(True), fromfile=original.name, tofile=variant.name))
(c / "batch-051-visual-fixture.diff").write_text(diff, encoding="utf-8")
for test in a["tests"]:
    assert sha(test["sourcePath"]) == sha(test["artifactPath"]) == test["sha256"]
    xml = ET.parse(test["artifactPath"]).getroot()
    assert xml.attrib["name"] == test["name"] and xml.attrib["timestamp"] == test["timestamp"]
    for key in ["tests", "failures", "errors", "skipped"]:
        assert int(xml.attrib[key]) == test[key]
    assert sorted(x.attrib["name"] for x in xml.findall("testcase")) == sorted(test["caseNames"])
archive = n["archive"]
assert sha(archive["path"]) == archive["sha256"]
with zipfile.ZipFile(archive["path"]) as z:
    assert len(z.infolist()) == archive["entries"] == 8303
    manifests = [x for x in z.namelist() if x.endswith("/manifest.json") or x == "manifest.json"]
    assert len(manifests) == 1
    prefix = manifests[0][:-len("manifest.json")]
    assert z.read(manifests[0]) == (r / "manifest.json").read_bytes()
    manifest = json.loads(z.read(manifests[0]))
    count = 0
    for kind, section in manifest.items():
        if not isinstance(section, dict):
            continue
        for name, digest in section.items():
            archived = z.read(prefix + name)
            current = (r / name).read_bytes()
            if kind not in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}:
                archived = archived.replace(b"\r\n", b"\n")
                current = current.replace(b"\r\n", b"\n")
            assert hashlib.sha256(archived).hexdigest() == hashlib.sha256(current).hexdigest() == digest, name
            count += 1
    assert count == archive["verifiedRuntimeHashes"] == 8281
artifact_dir = c / "artifacts" / "batch-051-parent-native-attempt-4"
glyphs = load(artifact_dir / "n1-051-font-raster.json")["rows"]
assert len(glyphs) == 24 and all(x["hasGlyph"] for x in glyphs)
rasters = {}
for char in "匁久文包勹丿":
    rows = [x for x in glyphs if x["character"] == char]
    assert len(rows) == 4 and len({x["font"] for x in rows}) == 4
    rasters[char] = len({x["nativePaintRasterSha256"] for x in rows})
assert rasters == {"匁": 4, "久": 4, "文": 4, "包": 4, "勹": 1, "丿": 1}
screens = n["visual"]["parentDirectAcceptedPngReads"]
assert len(screens) == 16
pngs = [artifact_dir / f"n1-051-{s}.png" for s in screens]
save(c / "batch-051-recovered-evidence-verification.json", {
    "execution": 277, "verifiedAt": datetime.now(timezone.utc).isoformat(),
    "contentHead": head, "reviewedTeachingSnapshot": teaching,
    "runtimeAndTeachingUnchanged": True, "provenanceHashesVerified": len(verified),
    "provenance": verified, "attempts": attempts, "freshAndroid": a,
    "archiveRuntimeHashesVerified": count, "nativePaintProbes": 24, "distinctRasters": rasters,
    "fixtureDiff": diff, "sameVisualScope": [{"path": str(p), "sha256": sha(p)} for p in pngs],
    "cleanup": load(c / "batch-051-parent-native-cleanup.json"),
    "limits": "Byte/terminal-result re-verification, not new execution or fresh visual inspection. Failed1/2 and functionally passed3/stale drawing captures retained. Drawing geometry fallback only. Parent cleanup historical; current app Git cleanliness separately checked. No publication/052.",
})
common = f"""SAME051 bounded ORIGINAL-session dependent visual confirmation, not a new blind initial.
Current HEAD {head}; teaching unchanged from revised reviewed {teaching}.
Native envelope ceb79db1221d139629c60aa703a87a3b66923c93 differs only in contributor evidence.
Use ONLY SERIAL view calls: ONE tool call per response, await completion. Never parallelize even text reads.
Read this task, YOUR complete initial report and YOUR complete textual confirmation report (paths below); do NOT read the other reviewer's report.
Read complete current kanji and word in separate responses:
{r}\\kanji\\匁.md
{r}\\words\\匁.md
Read accepted disposable native fixture lines180-335 in one call:
{variant}
Actual teaching diff {teaching}..{head} for kanji/words/articles/strokes/manifest is EMPTY, verified by coordinator.
Exact disposable harness diff, no teaching/production/acceptance-assertion changes:
{diff}
Actually view EACH of these SIXTEEN accepted attempt4 PNGs singly, ONE PER RESPONSE:
""" + "\n".join(str(p) for p in pngs) + """
Check visible readability and distinction of 匁久文包勹丿 in four actual production rows. 匁久文包 each four rasters; 勹丿 one Gothic-like fallback across families, exact face unknown. Readability matters, not four fallback designs.
Check radical勹20/fourstrokes/hooked-outline and crossing strokes as explicitly modern mnemonic, not etymology; mass3.75g/current pearl specialty versus historical silver money/no modern conversion.
Check full emptyon/orderedもんめ,め versus sole selectedkunもんめ; qualified 百匁ひゃくめ irregular-kana/archaic whole expression, shortened目unit noteye and not free numeral paradigm. Exact Japanese 百匁 whole heading remains unverified, not claimed.
Check reciprocal article/word/SystemBack, conversion/reading and visible meaning/curated reading feedback, trace geometry feedback and recall-miss UI. Distinguish your visible observations from supplied operational results.
Preserve original initials38/40calls, one Claude internalguidanceoverlap and partial1876HTMLgap/false self-report, later originalsession recovery/correction; GPT truncated1888 recovered initially. Both textual confirmations9/9 strictly serial. Minor omitted irregular-kana/目 clarification resolved, unsupported usually withdrawn, six optional groups not adopted; not a new blind review or model benchmark.
Operational evidence supplied by coordinator, NOT tests run by you: original nativecompile permission denial retained, parent EXACT command passed1m2s56tasks9executed47uptodate. Genuine attempt1 Article-2/Glyph0/25.656s reading-table/Commonwords ambiguity; attempt2 Article-2/Glyph0/56.36s transientLoading/disabledStart. Attempt3 two terminalcase0/56.536s/functionallypassed but drawingPNGs staleLoading/Checking; preserve, not accepted visual evidence. Acceptedattempt4 two terminalcase0/no skips75.175s. Variant only precise link selector, boundedwaitenabled before unchangedassert and1000ms compositor settle/Composeidle. No production/teaching/assertion/heap/guard change.
Full exact Gitenvelope through productionContentSync ONCE perarticleattempt imported1063kanji/5021words/N183/contentVersiona90e66e16d24c25d/problems0/acceptedepoch1/fullrawemptyon/fullkunもんめ,め/emptyquizOn/solequizKunもんめ. Unique disposable source/duefixtures/twohistoricalmeaninglogs unlockdrawing; no drawingstate seeded/notownerprogress. Actual meaningcorrectfeedback, curatedもんめ question/noめoption and persistedkungrade3; fourtouch-injected exactreference strokes; ungradedtraceWellDrawn; recall I don't remember/persistedDrawgrade onNext; offlinereciprocalBack. 24Paintprobes. Actual drawing ONLY offline geometry fallback, modelunavailable, NOT MLKit recognition/realcorrectrecall/negativegeometry/reverse-order testing.
Freshsame051275Android3+1 exactnames/source-copyhashes/UTC/dedicatedroot reverified, not rerun or050reuse. Original275denial and parent exact275obsolete274assertion failure retained; separatelyapprovedcurrent275recovery accepted. Original049default512MiBHOSTTestOOM/bounded1GiBHOSTcoreTestheadroom retained, NOT used for native. Guestappheaps192m576m/archiveguards unchanged.
All ownedhelpersstopped/exacttempsremoved/appclean; otherownerdevices untouched. API35fingerprint google/sdk_gphone64_x86_64/emu64xa:15/AE3A.240806.036/12592187:user/release-keys/read-only2048MiB2cores/hostGPU/Vulkan-disabled.
Parent16directPNGreads/eightadditionalhash-equivalentviewports NOT extra independentreads. Readingtable rightedge clipped in initialview/firstcolumn afterhorizontal scroll; do not certify hidden columns/fullarticle. Trace retains first-use downloading-model message; subsequent feedback says modelunavailable/strokeshapesonly. Actual returned image tool may resize; do not claim original byte identity/dimensions/hashes without evidence.
Return complete Snapshot/Scope/Verdicts/Findings/Optional/Limits report; enumerate actual PNG reads/text ranges, distinguish inherited textualCLEAN from boundedvisual. No finding quota. No edits, shell, delegation, retries, source search or tools beyond view. Physicalphone/native-speaker/generalrelease/currentmain/publication/whole-set remain unperformed. Return final report, not task_complete. ONE tool call per response.
"""
for label, model, session in [
    ("claude", "claude-opus-5.5", "b90bb59d-8135-4296-afb4-60732512ce23"),
    ("gpt", "gpt-6.1-sol", "b16b7291-287d-4f89-8090-57a326320478"),
]:
    path = c / f"batch-051-visual-{label}-prompt.txt"
    assert not path.exists()
    path.write_text(
        f"You are original {model} reviewer, same session {session}.\n"
        f"Your initial report: {r}\\docs\\n1-reviews\\batch-051-initial-{label}.md\n"
        f"Your textual confirmation: {r}\\docs\\n1-reviews\\batch-051-confirmation-{label}.md\n" + common,
        encoding="utf-8",
    )
print(f"Verified {len(verified)} provenance hashes,93 attempt artifacts,8281 runtime hashes,24 probes,fresh Android3+1; prepared common16PNG scope.")

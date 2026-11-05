import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).parent
R = C.parent / "learning-japanese"
V = R / "docs" / "n1-reviews"
HEAD = "18c87f8ac27f3bd0eb59f4320130bfdfd34a755f"
TEACHING = "45c275e7c041d8486705ab860a31f34e51ac7a70"
load = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def save(path, value):
    assert not path.exists(), path
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=R, text=True).strip() == HEAD
assert not subprocess.check_output(["git", "status", "--porcelain"], cwd=R)
assert not subprocess.check_output(["git", "diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json"], cwd=R)
request = C / r"logs\0f527758-3db9-463f-87c5-5d71f442775d\request.txt"
text = request.read_text(encoding="utf-8-sig")
embedded = json.loads(text.split("Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
state = load(C / "progress.json")
assert state["checkpoint"] == embedded["checkpoint"] == 419
assert state["batch"] == "065" and state["status"] == "continue"
backup = C / "execution-420-before-progress.json"
assert not backup.exists()
backup.write_bytes((C / "progress.json").read_bytes())
start = {
    "execution": 420, "batch": "065", "startingHead": HEAD,
    "scope": "SAME065 two serial ORIGINAL-session dependent visual confirmations, exact returned-payload/range/process archival, evidence reconciliation and normally signed local checkpoint only. No native/Android rerun, runtime publication,066 or second runner.",
    "authorization": {
        "requestSha256": sha(request), "characters": len(text), "lines": len(text.splitlines()),
        "completeFileLoadedAndCheckpointParsed": True,
        "limits": "Complete request acquired and complete embedded checkpoint parsed; operative contract, final419 and complete approved issue inspected directly. Historical middle acquired/parsed, not freshly semantically re-reviewed.",
    },
    "recordedAt": datetime.now(timezone.utc).isoformat(),
}
save(C / "execution-420-start.json", start)
state["execution420StartingState"] = start
state["stage"] = "batch-065-dependent-visual-confirmation-starting"
temporary = C / "execution-420-progress.tmp"
temporary.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
temporary.replace(C / "progress.json")
assert all(load(backup)[k] == state[k] for k in load(backup) if k != "stage")

native = load(R / r"docs\n1-sources\execution-419.json")
index = R / native["artifactIndex"]
assert sha(index) == native["artifactIndexSha256"]
groups = {}
for item in load(index)["files"]:
    path = R / item["path"]
    assert sha(path) == item["sha256"] and path.stat().st_size == item["bytes"], path
    if path.suffix == ".png":
        groups.setdefault(item["sha256"], []).append(path.name)
names = [names[0] for names in groups.values()]
folder = V / "batch-065-native" / "attempt-1"
fixture = folder / "N1Batch065NativeTest.kt"
count = len(fixture.read_text(encoding="utf-8").splitlines())
fixture_ranges = [(a, min(a + 139, count)) for a in range(1, count + 1, 140)]
task_path = C / "batch-065-visual-task.txt"
task = f"""SAME065 dependent ORIGINAL-session native visual confirmation, execution420.
NOT a new blind initial review, dictionary audit or native rerun.
Frozen evidence HEAD {HEAD}; teaching unchanged from {TEACHING}.
Native full archive source ee672744235275d321b4bfb33a6efe0286444594.

ONLY SERIAL view calls: exactly ONE tool call per response; await its result.
Never parallelize even text reads. No shell, edits, search, delegation, task_complete.
Read YOUR complete original initial report and YOUR complete textual confirmation
(exact paths appended to prompt). Do not read another reviewer report or coordinator
adjudication. Inherit original lexical conclusions with their source/lookup limits.
Read this COMPLETE shared task itself: {task_path}

Freshly read complete teaching files separately:
{R / 'kanji' / '倹.md'}
{R / 'words' / '倹約.md'}
{R / 'words' / '倹しい.md'}
{R / 'kanji' / '約.md'}
Only the added 倹約 Common words line in reused 約 is changed scope;
unchanged context is not a fresh review of easier teaching. No subsequent runtime diff.

Read COMPLETE native fixture in these separate inclusive ranges: {fixture_ranges}.
{fixture}
Also read COMPLETE terminal log and route receipt separately:
{folder / 'instrumentation.txt'}
{folder / 'n1-065-article-route.json'}

Actually VIEW EACH sourcePNG below singly, ONE PER RESPONSE, under:
{folder}\\
"""
task += "\n".join(names)
task += f"""

These are {len(names)} DISTINCT source hashes selected from60capture names.
Byte-identical aliases are not independent scenes. Names/selectors/assertIsDisplayed
are NOT proof a named sentence or whole cell is visible. Inspect actual pixels;
do not certify unseen prose or first-column labels. Source1080x2400 may be resized
by view: record actual transport/dimensions and viewport limits honestly.
Clipped/horizontally shifted table labels alone do not establish inaccessible content.
Any consequential unsupported visual conclusion stays UNVERIFIED.

Inspect 倹/儉/険/験/値/人/亻/阝/馬/約/糸/勺 and 倹約/倹しい across FOUR
production font rows: readable/distinguishable, no blank/replacement boxes.
Typeface change alone is not a defect; wrapped 勺 is not absence. Same fallback
styles may coincide.48single-glyph/8whole-word Paint probes establish nonblankness/
distinct rasters, not fallback-face identity or every-phone readability.
Full on[ケン], ordered kun[つま.しい,つづまやか]; curated on[ケン]/kun[つま.しい],
normalizedけん/つましい only. Check both ACTUAL question/options/feedback pixels;
feedback's dictionary list alone does not establish which key was asked.
Source-only つづまやか is retained, not offered. Inspect curation distinction,
modern10strokes/radical人9 with亻, mnemonic not etymology, older儉 not another
modern spelling example. Meaning frugal/thrifty versus ACTUAL displayed wrong options:
live fallback choices may differ from authored 険/験/値.
Check 倹約けんやく/ケン+ヤク, noun/transitiveする/な attachment and を examples;
倹しいつましい/い adjective ending and kana-oriented spelling/register guidance,
living-context modesty not humble attitude. Pronunciation つましい versusつつましい
and rare/source-only spelling boundaries; no rigid semantic compartments or
frequency conclusion from spellings alone. Check examples/translations actually
visible, source-only tables/scroll cues, attachment and comparison passages.
THREE component reciprocal pairs倹/倹約,約/倹約,倹/倹しい in SIX directions;
倹約/倹しい comparison both directions and SystemBack. Actual whole-word reading,
not invented source-only compound. Quiz exclusion judgments inherited, no whole-pool
or fresh dictionary certification.

SUPPLIED operational results, NOT reviewer-executed:419both namedcases terminal0,
no skips148.883s. Full archive productionContentSyncONCE:1077kanji5036words97N1,
problems0/contentVersion6a940651167e0e94/parserEpoch1. Read actual fixture assertions
and terminal log. Synthetic disposable source/HEAD, otherN1 postponed, two historical
Goodmeaninglogs unlock drawing, no drawing state seeded. Not owner progress or
learning efficacy. Meaning feedback exits Back before Next: do NOT claim a new
persisted meaning grade. Both reading Good grades persisted/no source-only logs.
10generated-reference touchstrokes/ungraded trace/model-unavailable geometry feedback/
recall miss/persistedDrawAgain are NOT MLKit recognition, human successful recall or
negative geometry/reverse-order testing. Downloading status alone is not successful
model download. Offline/SystemBack asserted API35fontscale1/fingerprint
google/sdk_gphone64_x86_64/emu64xa:15/AE3A.240806.036/12592187:user/release-keys.
Native heapgrowth192m/heapsize576m unchanged; accepted417 freshAndroid3+1 retained,
not rerun. Owned helpers stopped; shared preexisting emulator5556 preserved.
No new device/process operation or upstream observation by reviewer.
Historical416denial/actual1GiBOOM/prior049512MiBfailure remain historical;
qualifiedHOST-only2GiB memory init NEVER applies to native builds.

Return COMPLETE Snapshot/Scope/Verdicts(EACH of four articles correctness/
scopedcoverage/comprehensibility CLEAN,NEEDS FIX,UNVERIFIED)/Findings/Optional/Limits.
Enumerate ACTUAL image reads and text ranges/deviations. Separate inherited lexical
conclusions, new pixels, supplied operational assertions. Actionable findings need
severity/facet/exact PNG location or filelines/impact/remedy/evidence/confidence.
No quota; optional polish is not an acceptance blocker. Original reports and source/
read-depth/citation limits preserved. Unseen article/table parts, fallback face,
physical phone/general release/whole-set/currentmain/publication remain explicit.
CompatibleAndroidf9b59a2+ required. FINAL COMPLETE REPORT then EXIT.
"""
assert not task_path.exists()
task_path.write_text(task, encoding="utf-8")
for family in ("claude", "gpt"):
    prompt = C / f"batch-065-visual-{family}-prompt.txt"
    assert not prompt.exists()
    prompt.write_text(task + f"\nRead YOUR complete initial report: {V / f'batch-065-initial-{family}.md'}\n"
                      f"Read YOUR complete textual confirmation: {V / f'batch-065-confirmation-{family}.md'}\n", encoding="utf-8")
freeze = {
    "schemaVersion": 1, "execution": 420, "batch": "065",
    "evidenceHead": HEAD, "teachingSnapshot": TEACHING,
    "nativeArtifactIndexSha256": sha(index), "indexedArtifactsVerified": len(load(index)["files"]),
    "sourceCaptureNames": 60, "assignedDistinctSourceImages": len(names),
    "imageAliasGroups": groups, "fixtureRanges": fixture_ranges,
    "sharedTaskSha256": sha(task_path),
    "teachingHashes": {str(p.relative_to(R)): sha(p) for p in [
        R / "kanji" / "倹.md", R / "words" / "倹約.md", R / "words" / "倹しい.md",
        R / "kanji" / "約.md", R / "manifest.json"]},
    "originalReportHashes": {str(p.relative_to(R)): sha(p) for p in [
        V / f"batch-065-{kind}-{family}.md" for kind in ("initial", "confirmation")
        for family in ("claude", "gpt")]},
}
save(C / "batch-065-visual-freeze.json", freeze)
print(f"Starting state persisted preserving history; verified {freeze['indexedArtifactsVerified']} artifacts; assigned {len(names)} distinct images and complete fixture.")

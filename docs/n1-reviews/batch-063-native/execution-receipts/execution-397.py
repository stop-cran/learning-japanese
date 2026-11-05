import copy
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
C = Path(__file__).parent
R = C.parent / "learning-japanese"
V = R / "docs" / "n1-reviews"
S = R / "docs" / "n1-sources"
HEAD = "6d616d75cb15a0d574e28545c89ef45e3bcd85cb"
TEACHING = "ddad655f71c06e7cb2c749de18596863a800a73d"
MODELS = {"claude": "claude-opus-5.5", "gpt": "gpt-6.1-sol"}
SESSIONS = {"claude": "80bc3198-c572-419d-b7a1-2df6ec8475c5", "gpt": "65373d23-fce9-455e-a51f-5bd7c89b5d17"}
NATIVE = V / "batch-063-native" / "attempt-1"
IMAGES = [
    "font-pairs", "selection", "kanji-radical", "kanji-meaning",
    "kanji-on-reading", "kanji-model-boundary", "kanji-lookalikes",
    "imitation-components", "imitation-work-example", "imitation-speech-example",
    "imitation-particle-contrast", "imitation-copy-boundary",
    "follow-model-particle", "follow-learning-contrast", "follow-spelling-boundary",
    "follow-backlink", "meaning-question", "meaning-feedback",
    "curated-On-question", "curated-On-feedback", "curated-Kun-question",
    "curated-Kun-feedback", "drawing-trace", "drawing-feedback", "drawing-recall-feedback",
]


def load(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def save(p, data):
    assert not p.exists(), p
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def git(*args):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=R, text=True, encoding="utf-8").strip()


def unchanged():
    assert git("rev-parse", "HEAD") == HEAD
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    index = load(V / "batch-063-native" / "execution-396-artifact-index.json")
    for row in index["files"]:
        assert sha(R / row["path"]) == row["sha256"], row["path"]


def prepare():
    assert not git("status", "--porcelain")
    unchanged()
    request = C / "logs" / "92471855-9893-4429-8ffe-35a7cf499e38" / "request.txt"
    text = request.read_text(encoding="utf-8-sig")
    embedded = json.loads(text.split("Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert embedded["checkpoint"] == 396
    progress = load(C / "progress.json")
    assert progress["checkpoint"] == 396 and progress["batch"] == "063"
    save(C / "execution-397-original-progress.json", progress)
    record = {
        "execution": 397, "batch": "063", "startingHead": HEAD,
        "startedAt": datetime.now().astimezone().isoformat(),
        "scope": "SAME063 original-session two-family serial dependent native visual confirmation, evidence reconciliation and normally signed local checkpoint only. No runtime edits, Android/native rerun, publication,064 or second runner.",
        "status": "preparing-dependent-visual-review",
        "authorization": {
            "requestSha256": sha(request), "characters": len(text), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request acquired into memory and complete embedded checkpoint parsed; operative contract, final396 checkpoint and complete approved issue inspected directly. Historical middle acquired and parsed, not freshly semantically re-reviewed.",
        },
    }
    assert "execution397StartingState" not in progress
    progress["execution397StartingState"] = record
    (C / "progress.json").write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for args, name in [(["copilot", "--help"], "help"), (["copilot", "help", "config"], "model-catalog")]:
        result = subprocess.run(args, shell=True, check=True, capture_output=True, text=True, encoding="utf-8")
        target = V / f"batch-063-copilot-{name}-execution-397.txt"
        assert not target.exists()
        target.write_text(result.stdout, encoding="utf-8")
        if name == "model-catalog":
            assert all(m in result.stdout for m in MODELS.values())
    task = f"""SAME063 dependent native visual confirmation, execution397.
NOT a new blind initial review, dictionary audit or native rerun.
Frozen evidence HEAD {HEAD}; teaching unchanged from {TEACHING}.
Exact native archive source53ecd11711804be900ca95f9f1018942910aecec.

Use ONLY SERIAL view calls: exactly ONE tool call per response; await result.
NEVER parallelize even text reads. No shell, edits, search, delegation or task_complete.
Do not read another reviewer's report or coordinator adjudication.
Read YOUR original report and YOUR OWN dependent confirmations specified below.
Inherit prior lexical/source conclusions only with their original limitations.

Freshly read each complete teaching file separately:
{R / 'kanji' / '倣.md'}
{R / 'words' / '模倣.md'}
{R / 'words' / '倣う.md'}
Only the added kanji link at physical line29 of 倣う and tightly coupled behavior
are new scope; remainder is context, not a fresh review of easier teaching.
No teaching changes since your textual review; actual subsequent teaching diff empty.

Read FOUR native fixture ranges, FOUR separate calls:54-142,150-285,286-359,360-419.
{NATIVE / 'N1Batch063NativeTest.kt'}
Also separately read COMPLETE actual terminal log and route receipt:
{NATIVE / 'instrumentation.txt'}
{NATIVE / 'n1-063-article-route.json'}

Actually VIEW EACH of these25sourcePNGnames singly, ONE PER RESPONSE:
""" + "\n".join(str(NATIVE / f"n1-063-{name}.png") for name in IMAGES) + """

Capture names are selectors, NOT proof target fully visible. Inspect actual pixels.
Some captures are byte-identical; enumerate actual distinct returned images honestly.
Source1080x2400 mayreturn900x2000; report transport/viewport limits.
Horizontal reading table scrolling may clip labels; partial viewport is not proof
of inaccessible content. Do not certify unseen cells or whole article rendering.
If an important visual conclusion lacks evidence mark it UNVERIFIED.

Check actual倣/放/方/付/人/亻/模/木/傚/習/攵 and模倣/倣う across FOUR production
font rows: readable/distinguishable, no blank/replacement boxes. Typeface change
alone is not a defect; fallback styles may coincide. Paint/raster probes do not
identify actual fallback faces or prove every phone. Actual reused傚 and radical亻
need pixel inspection, not bundled cmap inference.
Preserve full on[ホウ],kun[なら.う], both explicit same-value practice subsets,
normalizedほう/ならう. Check full visible reading questions/options/feedback,
not just intended key. Feedback lookup lists alone do not prove practice selection.
Meaningimitation/emulation versus放release/方direction,method/付attach;
actual live options may be fallbacks rather than authored three, report pixels.
模倣もほう and transitiveを; 倣うならう/modelに; distinguish習うlearning and
copying/resemblance without asserting fraud-only or obligatory teacher.
Usually-kana/rare傚う/慣らう qualifiers inherit source review, not fresh frequency.
Check actual sentences, kana, translations and qualifiers. Mnemonic is modern
shape not etymology; radical人9 visible亻. Two reciprocal pairs倣/模倣 and倣/倣う
in FOUR directions with actual SystemBack; retain source/dictionary/8exclusions/
35families judgments separately from new pixels, no fresh dictionary certification.

Operational results SUPPLIED, not reviewer-executed: native396 BOTH named cases
terminal0/no skips114.805s. Exact full archive through productionContentSyncONCE
1075kanji5033words95N1/problems0/versionc19b742b7e6320a7/acceptedparserEpoch1.
Read actual assertions and terminal log. Syntheticdisposablesource/HEAD; otherN1
postponed/twohistoricalGoodmeaninglogs unlockdrawing/no drawingstate seeded.
NOT ownerprogress or learningefficacy. Meaningfeedback exitsBack BEFORENext:
do not claim a new persisted meaninggrade. BOTH sole curatedOn/KunGood and
drawingNext persistence asserted. Ten generated-reference touchstrokes/ungraded
trace/modelunavailablegeometry-onlyfeedback/recallmiss/persistedDrawAgain:
NOT MLKit recognition, successfulhumanrecall, negativegeometry/reverseorder.
Firstuse downloading status is NOT downloadsuccess. Offline/SystemBack asserted
API35/fontscale1/fingerprintgoogle/sdk_gphone64_x86_64/emu64xa:15/AE3A.240806.036/12592187:user/release-keys.
Ownedemulator26180/QEMU4200 stopped; unrelatedemulator5556 untouched.
Nativeheapgrowth192m/heapsize576m unchanged; accepted394Android3+1 NOT rerun.

HistoricalClaude063-P1 one response/two overlappingviews remains noncompliant.
Two separately exiting dependent confirmations freshly reread11lexical families
serially; other24families/sixcharacterrecords inherited. This remediates forward
operation, never retroactively strictinitial acceptance. Originalreports unchanged.
Sourceattribution-only headings/incompletewrappers/historicalgaiji limits remain.
No new upstream retrieval or35family rereview. Do not force agreement.

Return complete Snapshot/Scope/Verdicts(each article correctness/scopedcoverage/
comprehensibility separately)/Findings/Optional/Limits. Enumerate actualPNGreads,
textranges and processdeviations honestly. Separate inheritedtext/newpixels/
suppliedoperationalresults. Any consequential defect:severity/facet/exact filelines
orPNG location/learningimpact/remedy/evidence/confidence. No findingquota.
Unseenarticle/tableportions, actualfallbackface, physicalphone/generalrelease/
whole-set/currentmain/publication stayexplicit. FINALREPORT then EXIT;
do not call task_complete. ONE toolcallperresponse.
"""
    target = C / "batch-063-visual-task.txt"
    assert not target.exists()
    target.write_text(task, encoding="utf-8")
    (V / target.name).write_text(task, encoding="utf-8")
    for family in MODELS:
        own = f"\nYOUR original report: {V / f'batch-063-initial-{family}.md'}\n"
        if family == "claude":
            for turn in [1, 2]:
                own += f"YOUR dependent confirmation: {V / f'batch-063-dependent-claude-turn{turn}.md'}\n"
        prompt = task + own
        p = C / f"batch-063-visual-{family}-prompt.txt"
        assert not p.exists()
        p.write_text(prompt, encoding="utf-8")
        (V / p.name).write_text(prompt, encoding="utf-8")
    save(C / "batch-063-visual-freeze.json", {
        "head": HEAD, "teaching": TEACHING, "images": [
            {"path": str(NATIVE / f"n1-063-{name}.png"), "sha256": sha(NATIVE / f"n1-063-{name}.png")}
            for name in IMAGES
        ], "nativeIndexSha256": sha(V / "batch-063-native" / "execution-396-artifact-index.json"),
    })
    print(json.dumps(record, ensure_ascii=False))


def archive(family):
    unchanged()
    prefix = f"batch-063-visual-{family}"
    process = load(C / f"{prefix}-process.json")
    usage = load(C / f"{prefix}-usage.json")
    raw = C / f"{prefix}.jsonl"
    events = [json.loads(line) for line in raw.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    assert process["exitCode"] == 0 and process["sessionId"] == SESSIONS[family]
    assert usage["currentModel"] == MODELS[family]
    messages = [e for e in events if e["type"] == "assistant.message"]
    actual_models = sorted({e["data"]["model"] for e in messages})
    assert actual_models == [MODELS[family]]
    multi = [e["id"] for e in messages if len(e["data"].get("toolRequests", [])) > 1]
    active = {}
    overlaps, calls = [], []
    for e in events:
        data = e.get("data", {})
        if e["type"] == "tool.execution_start":
            if active:
                overlaps.append({"id": data["toolCallId"], "active": list(active)})
            assert data["toolName"] == "view"
            active[data["toolCallId"]] = e
        elif e["type"] == "tool.execution_complete":
            start = active.pop(data["toolCallId"])
            result = data.get("result", {}).get("content", "")
            args = start["data"]["arguments"]
            path = Path(args["path"])
            call = {
                "name": "view", "arguments": args, "startedAt": start["timestamp"],
                "completedAt": e["timestamp"], "success": data["success"],
                "returnedCharacters": len(result),
                "returnedSha256": hashlib.sha256(result.encode("utf-8")).hexdigest(),
                "sourceSha256": sha(path),
                "truncationOrLimitMarker": any(m in result for m in ["[Output truncated", "File too large", "Invalid view_range"]),
            }
            if path.suffix != ".png" and data["success"]:
                bounds = args.get("view_range", [1, -1])
                lines = path.read_text(encoding="utf-8-sig").splitlines(keepends=True)
                end = len(lines) if bounds[1] == -1 else bounds[1]
                expected = "".join(lines[bounds[0]-1:end])
                normalize = lambda s: s.replace("\r\n", "\n").rstrip()
                call["exactRequestedTextContainedInResult"] = normalize(expected) in normalize(result)
            calls.append(call)
    report = messages[-1]["data"]["content"]
    assert report and not messages[-1]["data"].get("toolRequests")
    target = V / f"{prefix}.md"
    assert not target.exists()
    target.write_text(report + "\n", encoding="utf-8")
    returned_images = {c["arguments"]["path"] for c in calls if c["success"] and c["arguments"]["path"].endswith(".png")}
    expected_images = {str(NATIVE / f"n1-063-{n}.png") for n in IMAGES}
    record = {
        **process, "teachingSnapshot": TEACHING, "dependentNotBlind": True,
        "actualModels": actual_models, "usageCurrentModel": usage["currentModel"],
        "availableTools": ["view"], "toolCalls": calls,
        "multiToolResponses": multi, "observedToolOverlaps": overlaps, "unfinishedTools": list(active),
        "assignedImageNames": len(expected_images), "successfulAssignedImageNames": len(returned_images & expected_images),
        "missingAssignedImages": sorted(expected_images - returned_images),
        "distinctAssignedSourceImageHashes": len({sha(Path(p)) for p in returned_images & expected_images}),
        "reportSha256": sha(target), "rawExecutionSha256": sha(raw),
        "rawExecutionLocation": f"Sibling control/{prefix}.jsonl",
        "promptSha256": sha(C / f"{prefix}-prompt.txt"),
        "configurationEvidence": [e["data"] for e in events if e["type"] in ["session.info", "session.tools_updated"]],
        "usage": usage,
        "limits": "Original returned report unchanged; image tool results, source hashes and report observations are distinct evidence. Supplied native operations not reviewer-executed. Original historical063-P1 unchanged.",
    }
    if family == "gpt":
        prior = load(V / "batch-063-visual-claude-execution.json")
        assert datetime.fromisoformat(prior["completedAt"]) < datetime.fromisoformat(record["startedAt"])
        for suffix in [".md", "-execution.json"]:
            assert (V / f"batch-063-visual-claude{suffix}").stat().st_mtime < datetime.fromisoformat(record["startedAt"]).timestamp()
        record["priorProcessExitAndCompleteArchiveBeforeLaunch"] = True
    save(V / f"{prefix}-execution.json", record)
    print(json.dumps({k: record[k] for k in [
        "actualModels", "exitCode", "assignedImageNames", "successfulAssignedImageNames",
        "distinctAssignedSourceImageHashes", "multiToolResponses", "observedToolOverlaps", "missingAssignedImages",
    ]}, ensure_ascii=False))
    print(report)


def stage():
    unchanged()
    before = load(C / "execution-397-original-progress.json")
    progress = load(C / "progress.json")
    assert progress["checkpoint"] == 396
    assert all(progress[k] == v for k, v in before.items())
    assert set(progress) - set(before) == {"execution397StartingState"}
    reviews = {}
    for family in MODELS:
        prefix = f"batch-063-visual-{family}"
        record = load(V / f"{prefix}-execution.json")
        assert record["exitCode"] == 0 and record["actualModels"] == [MODELS[family]]
        assert record["sessionId"] == SESSIONS[family] and record["availableTools"] == ["view"]
        assert record["reportSha256"] == sha(V / f"{prefix}.md")
        assert record["rawExecutionSha256"] == sha(C / f"{prefix}.jsonl")
        assert record["promptSha256"] == sha(C / f"{prefix}-prompt.txt") == sha(V / f"{prefix}-prompt.txt")
        assert not record["multiToolResponses"] and not record["observedToolOverlaps"] and not record["unfinishedTools"]
        assert not record["missingAssignedImages"] and record["successfulAssignedImageNames"] == 25
        assert record["distinctAssignedSourceImageHashes"] == 20
        for call in record["toolCalls"]:
            assert call["success"] and not call["truncationOrLimitMarker"]
            assert call.get("exactRequestedTextContainedInResult", True)
            assert call["sourceSha256"] == sha(Path(call["arguments"]["path"]))
        reviews[family] = record
    assert reviews["gpt"]["priorProcessExitAndCompleteArchiveBeforeLaunch"]
    assert datetime.fromisoformat(reviews["claude"]["completedAt"]) < datetime.fromisoformat(reviews["gpt"]["startedAt"])
    android = C.parent / "kanji-cards-android"
    assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=android, text=True).strip() == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
    assert not subprocess.check_output(["git", "status", "--porcelain"], cwd=android, text=True).strip()
    next_action = (
        "SAME063 bounded current-main integration and publication gate. Signed local397 native/visual "
        "closure follows unchanged ddad655f teaching: originalClaude80bc3198/GPT65373d23 dependent "
        "visual processes BOTHexit0, actualclaude-opus-5.5/gpt-6.1-sol, view-only, onecallperresponse, "
        "zerooverlaps/failedtools/truncations. Each25PNGnames/20distinctsourcehashes, full3teachingfiles/"
        "fourfixture ranges/terminal log/route. Exact reports and audits docs/n1-reviews/batch-063-visual-*. "
        "No actionable content defect; inheritedtext/newpixels/supplied396native distinct. Fullreadingtable "
        "visible in kanji-meaning; shiftedonreading clipsleftlabels. Fourfontrows actual亻/傚 and倣/放 "
        "readable. Original063-P1 remains historical noncompliance, NOTretroactive strictinitialacceptance. "
        "Accepted394Android3+1/native396two terminal0 cases NOT rerun absent new concern. "
        "NEXT fetch latestorigin/main, normalnonrewriting merge if needed, regenerate derivedoutput and "
        "revalidate ACTUALcombinedtree: source/baseline/membership/readings/reciprocallinks/font/stroke/"
        "fullPython/vocab/validator/freshmanifest/18000entries42MiBcompressed80MiBinflated56MiBretained. "
        "Substantive merged teaching needs originalreviewer confirmation. Normal signing then authorized "
        "owner fastforwardpush/publicSHA/terminalgreenCI/EVERYimmutablepublicZIP runtimeentryhash/budgets/"
        "ownerissue60 and durable receipts BEFOREdelivery or064. Do not equate local closure with delivery. "
        "No new blindinitials,062rerun,064,secondrunner,supervisorchanges or concurrentheavywork. Actual "
        "permissiondenial/signingwait: preserveexactcommand/error, report/yield; no retry/workaround. "
        "PreserveFULLlivehistory and393denial/049hostheapqualification. Published89/1228,1139remain; "
        "localdraft90 NOTdelivered. CompatibleAndroidf9b59a2+ required; physicalphone/generalrelease/"
        "whole-set outstanding. Overallproject incomplete."
    )
    limits = (
        "Bounded emulator native/visual acceptance only; integration and public delivery remain pending. "
        "25 PNG names per reviewer have20 distinct source byte hashes, not25 independent scenes; both "
        "reports estimated19 visually distinct returned states without hashing. Retain reports verbatim; "
        "exact20 source hashes take precedence for byte counts, visual sameness is separate. Source1080x2400 "
        "returned900x2000. Readingtable fully visible in kanji-meaning screenshot, shifted viewport clips "
        "left labels in kanji-on-reading; no whole-article/allfontscale certification. Source/35family/"
        "sixcharacter/8exclusion judgments inherited, no fresh dictionary retrieval. No persisted new "
        "meaning grade; both curatedOn/KunGood and DrawAgain persistence supplied from396fixture. "
        "Reference-touch trace/modelunavailable/recallmiss notMLKit or humanrecall. Actualfallbackfaces/"
        "physicalphone/generalrelease/whole-set/currentmain/publication unverified. Historical063-P1 "
        "and393permissiondenial retained; later serial confirmation is not retroactive strictacceptance."
    )
    optional = [
        {"id": "063-V1", "status": "optional", "origin": "visual-claude",
         "claim": "Rare 傚う wraps between 傚 andう in one viewport.",
         "disposition": "No text loss or learning defect established; natural small-screen wrapping, not adopted."},
        {"id": "063-V2", "status": "optional", "origin": "visual-claude",
         "claim": "Extra visual space before comma after亻.",
         "disposition": "Rendered inline spacing, no content defect; not adopted."},
        {"id": "063-V3", "status": "optional", "origin": "visual-claude",
         "claim": "Rightmost chip clipped in selection row.",
         "disposition": "App viewport surface, no demonstrated inaccessible selection or content defect; no app edit in scope."},
        {"id": "063-V4", "status": "optional", "origin": "visual-claude",
         "claim": "Drawing feedback uses both not-graded and graded-by-stroke-shapes-only wording.",
         "disposition": "App wording outside content scope. Practice-only/model-unavailable limits retained; not claimed as MLKit or graded human recall."},
    ]
    groups = {}
    for name in IMAGES:
        p = NATIVE / f"n1-063-{name}.png"
        groups.setdefault(sha(p), []).append(p.name)
    supplement = {
        "schemaVersion": 1, "execution": 397, "batch": "063",
        "status": "bounded-native-visual-accepted-awaiting-integration",
        "evidenceHead": HEAD, "reviewedTeachingSnapshot": TEACHING,
        "teachingChanged": False, "dependentNotBlind": True,
        "reviewRecords": [
            {"family": fam, "model": MODELS[fam], "sessionId": SESSIONS[fam],
             "report": f"batch-063-visual-{fam}.md",
             "reportSha256": reviews[fam]["reportSha256"],
             "executionRecord": f"batch-063-visual-{fam}-execution.json",
             "toolCalls": len(reviews[fam]["toolCalls"]),
             "assignedPngNamesReturned": 25, "distinctSourceImageHashes": 20,
             "failedTools": 0, "overlaps": 0, "multiToolResponses": 0}
            for fam in MODELS
        ],
        "serialProcessExitAndCompleteArchiveBeforeNextLaunch": True,
        "verdicts": {
            "kanji/倣.md:complete": {"correctness": "CLEAN", "scopedCoverage": "CLEAN", "boundedComprehensibility": "CLEAN"},
            "words/模倣.md:complete": {"correctness": "CLEAN", "scopedCoverage": "CLEAN", "boundedComprehensibility": "CLEAN"},
            "words/倣う.md:line29 and tightly coupled context": {"correctness": "CLEAN", "scopedCoverage": "CLEAN", "boundedComprehensibility": "CLEAN"},
        },
        "findings": [], "optional": optional,
        "duplicateAssignedSourceGroups": [names for names in groups.values() if len(names) > 1],
        "imageCountQualification": "25 individually successful view calls/20distinctsourcehashes per reviewer; both described approximately19 visually distinct returned states. Byte counts verified by coordinator, not reviewer. Reports preserved unchanged.",
        "coordinatorFreshDirectImages": [
            {"path": str(NATIVE / f"n1-063-{name}.png"), "sha256": sha(NATIVE / f"n1-063-{name}.png")}
            for name in ["font-pairs", "kanji-meaning", "kanji-on-reading"]
        ],
        "coordinatorObservation": "Four rows show readable distinct targets including actual亻/傚 and倣/放. Newly inspected kanji-meaning shows complete two reading rows includingホウ/なら.う and both linked examples; shifted kanji-on-reading clips leftlabels. Prior396 limited direct-image description stays historical, not silently rewritten.",
        "nativeExecutionEvidence": "docs/n1-sources/execution-396.json",
        "nativeTerminalCases": 2, "nativeTerminalStatus": 0,
        "nativeRerun": False, "accepted394AndroidRerun": False,
        "nativeAcceptance": True, "independentVisualAcceptance": True,
        "strictInitialProcessContractAccepted": False,
        "runtimePublished": False, "integrationAccepted": False,
        "nextAction": next_action, "limits": limits,
    }
    save(V / "batch-063-native-acceptance.json", supplement)
    recon_path = V / "batch-063-reconciliation.json"
    recon = load(recon_path)
    recon["textualCheckpointStatus"] = recon["status"]
    recon["textualCheckpointNextAction"] = recon["nextAction"]
    recon["textualCheckpointLimits"] = recon["limits"]
    recon["status"] = supplement["status"]
    recon["nativeVisualSupplement"] = "batch-063-native-acceptance.json"
    recon["nativeAcceptance"] = True
    recon["independentVisualAcceptance"] = True
    recon["runtimeAccepted"] = False
    recon["runtimePublished"] = False
    recon["nextAction"] = next_action
    recon["limits"] = limits
    recon_path.write_text(json.dumps(recon, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ledger_path = S / "batch-063-progress.json"
    ledger = load(ledger_path)
    ledger["textualCheckpointLimits"] = ledger["limits"]
    ledger["textualCheckpointPending"] = ledger["pending"]
    ledger["status"] = supplement["status"]
    ledger["independentVisualAcceptance"] = True
    ledger["nativeAcceptance"] = True
    ledger["nativeVisualCheckpoint"] = "execution-397.json"
    ledger["nativeVisualEvidence"] = "docs/n1-reviews/batch-063-native-acceptance.json"
    ledger["independentReview"] += " Original-session dependent native visual confirmations397 both exit0/view-only/fully serial, no actionable defect; bounded emulator acceptance only."
    ledger["pending"] = [
        "Latest-main normal nonrewriting integration, combined-tree validation, normal signing and authorized owner fast-forward push.",
        "Exact publicSHA/terminal greenCI/every immutable publicZIP runtimehash/budgets and issue60 publication receipts.",
        "Physical-phone/general-release and whole-set acceptance outstanding.",
    ]
    ledger["fontDisposition"]["historicalPendingBefore397"] = ledger["fontDisposition"]["pending"]
    ledger["fontDisposition"]["pending"] = "Physical-phone/general-release and other device/fontscale combinations outstanding; fresh063API35/fontscale1 native and serial two-family visual inspection accepted."
    ledger["fontDisposition"]["nativeEvidence"] = "docs/n1-reviews/batch-063-native-acceptance.json"
    ledger["nextAction"] = next_action
    ledger["limits"] = limits
    ledger_path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    record = {
        **progress["execution397StartingState"],
        "status": supplement["status"],
        "reviewedTeachingSnapshot": TEACHING,
        "nativeVisualEvidence": "docs/n1-reviews/batch-063-native-acceptance.json",
        "reviewRecords": supplement["reviewRecords"],
        "serialProcessExitAndCompleteArchiveBeforeNextLaunch": True,
        "nativeAcceptance": True, "independentVisualAcceptance": True,
        "runtimeEditsMade": False, "runtimePublished": False,
        "publishedAdditions": 89, "remainingAdditions": 1139,
        "nextAction": next_action, "limits": limits,
        "operationalObservations": [
            "Complete request parsed; initial display hit cp1252 UnicodeEncodeError, subsequently UTF8. Historical middle acquired and parsed, not freshly semantically re-reviewed.",
            "Initial generic JSONL audit assumed every event has data; usage event lacks data. Corrected parser to use empty data for unrelated event types before preserving report. Raw execution untouched.",
            "One coordinator display used default cp1252 read_text and failed on UTF8; subsequent explicit UTF8 reads succeeded. No permission failure or data change.",
        ],
        "recordedAt": datetime.now().astimezone().isoformat(),
    }
    save(S / "execution-397.json", record)
    progress["checkpoint"] = 397
    progress["status"] = "continue"
    progress["stage"] = "batch-063-native-visual-accepted-awaiting-integration"
    progress["nextAction"] = next_action
    progress["blocker"] = None
    progress["execution397StartingState"]["status"] = "native-visual-closed-preparing-signed-checkpoint"
    progress["batch063NativeVisualCheckpoint"] = {
        "execution": 397, "checkpoint": 397, "batch": "063",
        "status": supplement["status"], "record": "docs/n1-sources/execution-397.json",
        "nativeAcceptance": True, "independentVisualAcceptance": True,
        "runtimePublished": False, "publishedAdditions": 89, "remainingAdditions": 1139,
        "nextAction": next_action,
    }
    assert all(progress[k] == v for k, v in before.items() if k not in ["checkpoint", "status", "stage", "nextAction", "blocker"])
    (C / "progress.json").write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"checkpoint": 397, "status": "continue", "nativeVisualAccepted": True, "runtimePublished": False}, ensure_ascii=False))


def prepare_commit():
    unchanged()
    logs = V / "batch-063-native" / "execution-receipts"
    checks = []
    for label in ["validate", "manifest", "budget"]:
        p = logs / f"execution-397-{label}.txt"
        assert p.is_file()
        checks.append({"check": label, "exitCode": 0, "log": str(p.relative_to(R)), "sha256": sha(p)})
    assert "0 error(s)" in (logs / "execution-397-validate.txt").read_text(encoding="utf-8-sig")
    assert "c19b742b7e6320a7" in (logs / "execution-397-manifest.txt").read_text(encoding="utf-8-sig")
    for source in [Path(__file__), C / "run-batch-063-visual-397.ps1", C / "post-execution-397.ps1"]:
        target = logs / source.name
        shutil.copy2(source, target)
    record_path = S / "execution-397.json"
    record = load(record_path)
    record["validation"] = checks
    record["runtimeUnchangedAfterValidation"] = True
    record["inheritedNotRerun"] = ["Execution390 full Python/source/baseline/link/reading/font/stroke audits", "Execution394 Android3+1", "Execution396 native2"]
    record["fullHistoryCompared"] = True
    record["rawLogWhitespacePreserved"] = ["docs/n1-reviews/batch-063-copilot-model-catalog-execution-397.txt"]
    record["operationalObservations"].append(
        "Staged whitespace check identified one extra EOF blank line in actual CLI model catalog. "
        "Preserved raw output unchanged; nonraw evidence whitespace checked separately."
    )
    record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    paths = [
        "docs/n1-authoring-notes.md", "docs/n1-reviews/batch-063-reconciliation.json",
        "docs/n1-sources/batch-063-progress.json", "docs/n1-sources/execution-397.json",
        "docs/n1-reviews/batch-063-native-acceptance.json",
        "docs/n1-reviews/batch-063-visual-task.txt",
        "docs/n1-reviews/batch-063-copilot-help-execution-397.txt",
        "docs/n1-reviews/batch-063-copilot-model-catalog-execution-397.txt",
    ]
    for family in MODELS:
        for suffix in [".md", "-execution.json", "-prompt.txt"]:
            paths.append(f"docs/n1-reviews/batch-063-visual-{family}{suffix}")
    paths += [p.relative_to(R).as_posix() for p in logs.iterdir() if "397" in p.name]
    subprocess.run(["git", "add", "--", *paths], cwd=R, check=True)
    changed = git("diff", "--cached", "--name-only").splitlines()
    assert set(changed) == set(paths)
    subprocess.run([
        "git", "diff", "--cached", "--check", "--", ".",
        ":(exclude)docs/n1-reviews/batch-063-copilot-model-catalog-execution-397.txt",
    ], cwd=R, check=True)
    save(C / "execution-397-staged-inventory.json", {
        "startingHead": HEAD, "files": [
            {"path": p, "sha256": sha(R / p)} for p in changed
        ], "runtimeUnchanged": True,
    })
    print("Staged", len(changed), "accounted evidence-only paths; runtime unchanged.")


def finish():
    head = git("rev-parse", "HEAD")
    assert head != HEAD and git("rev-parse", "HEAD^") == HEAD
    assert git("show", "-s", "--format=%G?", "HEAD") == "G"
    assert not git("status", "--porcelain")
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    inventory = load(C / "execution-397-staged-inventory.json")
    for row in inventory["files"]:
        p = R / row["path"]
        assert sha(p) == row["sha256"]
        committed = subprocess.check_output(["git", "show", f"{head}:{row['path']}"], cwd=R)
        assert hashlib.sha256(committed).hexdigest() == row["sha256"]
    progress = load(C / "progress.json")
    before = load(C / "execution-397-original-progress.json")
    assert progress["checkpoint"] == 397 and progress["status"] == "continue"
    assert all(progress[k] == v for k, v in before.items() if k not in ["checkpoint", "status", "stage", "nextAction", "blocker"])
    receipt = load(C / "execution-397-issue-receipt.json")
    assert receipt["localCommit"] == head and receipt["author"] == "stop-cran" and receipt["bodyVerified"]
    final = {
        "execution": 397, "checkpoint": 397, "batch": "063",
        "savedCommit": head, "signature": "G", "contentClean": True,
        "runtimeUnchanged": True, "committedEvidenceFilesVerified": len(inventory["files"]),
        "reviewersExitedSuccessfully": 2, "nativeVisualAccepted": True,
        "reviewerAssignedImagesEach": 25, "distinctSourceHashesEach": 20,
        "failedReviewerTools": 0, "overlaps": 0, "multiToolResponses": 0,
        "runtimePublished": False, "wholeProjectComplete": False,
        "fullHistoricalProgressPreserved": True,
        "issueUpdate": receipt["url"], "ownerAuthorAndBodyVerified": True,
        "recordedAt": datetime.now().astimezone().isoformat(),
    }
    save(C / "execution-397-final-verification.json", final)
    progress["execution397StartingState"]["status"] = "signed-native-visual-checkpoint-complete"
    progress["batch063NativeVisualCheckpoint"].update({
        "savedCommit": head, "signature": "G", "verification": final, "issueUpdate": receipt["url"],
    })
    progress["batch063NativeVisualIssueReceipt"] = receipt
    progress["nextAction"] = f"SAME063 signed local397 at {head}. " + progress["nextAction"]
    (C / "progress.json").write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(final, ensure_ascii=False))


if __name__ == "__main__":
    if sys.argv[1] == "prepare":
        prepare()
    elif sys.argv[1] == "archive":
        archive(sys.argv[2])
    elif sys.argv[1] == "stage":
        stage()
    elif sys.argv[1] == "prepare-commit":
        prepare_commit()
    elif sys.argv[1] == "finish":
        finish()

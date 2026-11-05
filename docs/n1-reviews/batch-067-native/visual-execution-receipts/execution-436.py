import base64
import hashlib
import json
import struct
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).parent
R = C.parent / "learning-japanese"
V = R / "docs" / "n1-reviews"
HEAD = "a6c57b57f7c90f5a9c78e5bdf953bd2df768d5ed"
TEACHING = "5cb2ea4bc804ac218b17d5c583d4fba95e60971c"
FOLDER = V / "batch-067-native" / "attempt-1"
load = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    assert load(path) == json.loads(json.dumps(value, ensure_ascii=False))


def git(*args):
    return subprocess.check_output(["git", "--no-pager", "-C", str(R), *args], encoding="utf-8").strip()


def prepare():
    assert git("rev-parse", "HEAD") == HEAD and not git("status", "--porcelain")
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    request = C / r"logs\a614f9d8-4604-413a-88a5-866fcbeafa2a\request.txt"
    text = request.read_text(encoding="utf-8-sig")
    embedded = json.loads(text.split("Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    state = load(C / "progress.json")
    assert state["checkpoint"] == embedded["checkpoint"] == 435 and state["batch"] == "067"
    backup = C / "execution-436-before-progress.json"
    assert not backup.exists()
    backup.write_bytes((C / "progress.json").read_bytes())
    start = {
        "execution": 436, "batch": "067", "startingHead": HEAD,
        "scope": "SAME067 two serial ORIGINAL-session dependent visual confirmations, exact returned-image/range/process archival, evidence reconciliation and normally signed local checkpoint only. No native/Android rerun, runtime publication,068 or second runner.",
        "authorization": {
            "requestSha256": sha(request), "characters": len(text), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request acquired and complete embedded checkpoint parsed; operative contract, final435 and approved issue inspected directly. Historical middle acquired/parsed, not freshly semantically re-reviewed.",
        },
        "recordedAt": datetime.now(timezone.utc).isoformat(),
    }
    save(C / "execution-436-start.json", start)
    state["execution436StartingState"] = start
    state["stage"] = "batch-067-dependent-visual-confirmation-starting"
    save(C / "progress.json", state)
    index = V / "batch-067-native" / "execution-435-artifact-index.json"
    groups = {}
    for row in load(index)["files"]:
        path = R / row["path"]
        assert sha(path) == row["sha256"] and path.stat().st_size == row["bytes"]
        if path.suffix == ".png":
            groups.setdefault(row["sha256"], []).append(path.name)
    names = [g[0] for g in groups.values()]
    fixture = FOLDER / "N1Batch067NativeTest.kt"
    count = len(fixture.read_text(encoding="utf-8").splitlines())
    ranges = [(a, min(a + 139, count)) for a in range(1, count + 1, 140)]
    task = f"""SAME067 dependent ORIGINAL-session native visual confirmation, execution436.
NOT a new blind initial review, dictionary audit or native rerun.
Frozen evidence HEAD {HEAD}; teaching unchanged from {TEACHING}.
Native full git envelope source a45ce3014661487bf16977260daa5ca23e001663.

STRICT SERIAL: exactly ONE view tool call per response, then WAIT for its result.
Never multiple tool calls or parallel wrappers even for text. No shell, edits,
search, delegation, task_complete or new device operations. Only view available.
Read this COMPLETE shared task: {C / 'batch-067-visual-task.txt'}
Read YOUR complete original initial report (exact path appended to prompt).
Do not read another report or coordinator adjudication. Inherit your original
lexical conclusions with all original source/lookup limits.

Freshly read COMPLETE three teaching files separately:
{R / 'kanji' / '僧.md'}
{R / 'words' / '僧侶.md'}
{R / 'words' / '坊さん.md'}
Complete new 僧 and 僧侶 are in scope. Only words\\坊さん.md:30 comparison link
is changed reused scope. Complete reused article is context, not a fresh easier-
deck review. No subsequent runtime diff or new evidence-based teaching fix.

Read COMPLETE native fixture in separate inclusive ranges {ranges}:
{fixture}
Read COMPLETE terminal log and route receipt separately:
{FOLDER / 'instrumentation.txt'}
{FOLDER / 'n1-067-article-route.json'}

Actually VIEW EACH PNG singly, ONE PER RESPONSE, under:
{FOLDER}\\
""" + "\n".join(names) + f"""

These are {len(names)} DISTINCT source hashes selected from37capture names.
Byte-identical aliases are not independent scenes. Filenames/selectors/
assertIsDisplayed are NOT proof a named sentence or whole cell is visible.
Inspect actual pixels and disclose unseen/clipped prose/first-column labels.
Source1080x2400 may be resized by view; record actual transport/dimensions and
viewport limits honestly. Horizontally shifted labels alone do not establish
inaccessible content; there is a sideways-scroll hint. Consequential unsupported
visual conclusions remain UNVERIFIED, not CLEAN by a screenshot's filename.

Inspect 僧/増/値/倍/人/亻/曽/侶 and 僧侶/坊さん in FOUR production font rows:
readable/distinguishable, no blank/replacement boxes, especially 僧 versus増
(left亻 versus土), differing right components値/倍 and 人 versus亻.
Typeface change alone is not a defect; fallback styles may coincide.
32single-Paint+8word-raster probes support nonblankness/distinct rasters, not
fallback-face identity or every-phone readability.
Full+curated on[ソウ], full+curated kun[]; sole normalizedそう key.
Check actual question/options/feedback pixels, not feedback dictionary list alone.
Modern13strokes/canonicalradical人9/visible亻; labelled mnemonic not etymology.
Check Buddhist clergy rather than all believers, individual/community/sangha,
小僧こぞう and高僧こうそう without mechanical reading substitution.
僧侶そうりょ/ソウ+リョ; noun/individual versus collective, 寺 boundary,
temple/person examples and translations, formal/familiar-respectful坊さん
register distinction not different occupations, 神父Catholic distinction,
unlinked侶 and lexical boundaries where ACTUALLY visible.
Meaning option labels may differ from authored distractors増/値/倍:
inspect actual displayed choices, no whole-pool certification.
ONE mapped component pair僧-僧侶, BOTH directions; TWO comparison directions
僧侶-坊さん, SystemBack. No other incidental backlink requirement.

SUPPLIED operational results, NOT reviewer-executed:435 both namedcases terminal0,
no skips138.141s. Exact full archive productionContentSyncONCE:1079kanji5037words99N1,
problems0/contentVersion68c767f176e68882/parserEpoch1.
Read actual fixture assertions and terminal log. Synthetic disposable source/HEAD,
otherN1 postponed, two historicalGoodmeaninglogs unlock drawing, no drawing state
seeded. Not owner progress/learning efficacy. Meaning feedback exits Back before
Next: do NOT claim a new persisted meaning grade. SoleOnGood persisted/noKunLog.
13generated-reference touchstrokes/ungradedtrace/model-unavailablegeometryfeedback/
recallmiss/persistedDrawAgain are NOT MLKit recognition/human successful recall or
negative geometry/reverse-order testing. Downloading label is not successful model
download. Offline/SystemBack API35fontscale1/fingerprint
google/sdk_gphone64_x86_64/emu64xa:15/AE3A.240806.036/12592187:user/release-keys.
Native heapgrowth192m/heapsize576m unchanged; accepted433 freshAndroid3+1 inherited,
not rerun. Owned helpers stopped; preexisting emulator5556 preserved.
No fresh upstream retrieval or reviewer native execution. Historical denials/HOST
OOMs remain historical; qualifiedHOST-only2GiB init NEVER applies to native.

Return COMPLETE Snapshot/Scope/Verdicts(EACH of THREE teaching files correctness/
scopedcoverage/comprehensibility CLEAN,NEEDS FIX,UNVERIFIED)/Findings/Optional/Limits.
Enumerate actual image reads/text ranges/deviations. Separate inherited lexical
conclusions, new pixels, supplied operational assertions. Findings need severity/
facet/exactPNG location or filelines/impact/remedy/evidence/confidence. No quota.
Optional polish is not a blocker. Unseen parts/fallbackface/physicalphone/general
release/whole-set/latestmain/publication limits explicit. CompatibleAndroidf9b59a2+
required. FINAL COMPLETE REPORT then EXIT.
"""
    task_path = C / "batch-067-visual-task.txt"
    assert not task_path.exists()
    task_path.write_text(task, encoding="utf-8")
    for family in ("claude", "gpt"):
        (C / f"batch-067-visual-{family}-prompt.txt").write_text(
            task + f"\nRead YOUR complete original initial report: {V / f'batch-067-initial-{family}.md'}\n", encoding="utf-8")
    freeze = {
        "schemaVersion": 1, "execution": 436, "batch": "067", "evidenceHead": HEAD,
        "teachingSnapshot": TEACHING, "nativeArtifactIndexSha256": sha(index),
        "indexedArtifactsVerified": len(load(index)["files"]), "sourceCaptureNames": 37,
        "assignedDistinctSourceImages": len(names), "imageAliasGroups": groups,
        "fixtureRanges": ranges, "sharedTaskSha256": sha(task_path),
        "teachingHashes": {str(p.relative_to(R)): sha(p) for p in [
            R / "kanji" / "僧.md", R / "words" / "僧侶.md", R / "words" / "坊さん.md", R / "manifest.json"]},
        "originalReportHashes": {str(p.relative_to(R)): sha(p) for p in [
            V / f"batch-067-initial-{family}.md" for family in ("claude", "gpt")]},
    }
    save(C / "batch-067-visual-freeze.json", freeze)
    print("Starting state persisted; artifacts verified; assigned", len(names), "distinct images.")


def archive(family):
    prefix = f"batch-067-visual-{family}"
    process = load(C / f"{prefix}-process.json")
    usage = load(C / f"{prefix}-usage.json")
    freeze = load(C / "batch-067-visual-freeze.json")
    raw = C / f"{prefix}.jsonl"
    events = [json.loads(s) for s in raw.read_text(encoding="utf-8-sig").splitlines() if s.strip()]
    messages = [e["data"] for e in events if e["type"] == "assistant.message"]
    models = sorted({m["model"] for m in messages if m.get("model")})
    report = V / f"{prefix}.md"
    audit = V / f"{prefix}-execution.json"
    assert not report.exists() and not audit.exists()
    report.write_text([m["content"] for m in messages if m.get("content")][-1] + "\n", encoding="utf-8")
    calls, active, overlaps = {}, set(), []
    for e in events:
        d = e.get("data", {})
        if e["type"] == "tool.execution_start":
            key = d["toolCallId"]
            if active:
                overlaps.append({"starting": key, "active": sorted(active)})
            active.add(key)
            calls[key] = {"name": d["toolName"], "arguments": d["arguments"], "startedAt": e["timestamp"]}
        elif e["type"] == "tool.execution_complete":
            key = d["toolCallId"]
            active.remove(key)
            row = calls[key]
            row.update(success=d["success"], completedAt=e["timestamp"])
            if not d["success"]:
                row["error"] = d.get("error")
                continue
            result = d["result"]
            text = result.get("content", "")
            row.update(returnedCharacters=len(text), returnedTextSha256=hashlib.sha256(text.encode("utf-8")).hexdigest(),
                       truncationOrLimitMarker=any(s in text for s in ("[Output truncated", "File too large to read", "Invalid view_range", "<note>Content truncated")))
            source = Path(row["arguments"]["path"])
            if source.suffix == ".png":
                images = result.get("binaryResultsForLlm", [])
                assert len(images) == 1 and images[0]["type"] == "image"
                image = base64.b64decode(images[0]["data"], validate=True)
                assert image.startswith(b"\x89PNG\r\n\x1a\n")
                returned = V / "batch-067-native" / f"visual-{family}-returned" / source.name
                returned.parent.mkdir(exist_ok=True)
                assert not returned.exists()
                returned.write_bytes(image)
                row["imagePayload"] = {
                    "bytes": len(image), "sha256": sha(returned), "sourceSha256": sha(source),
                    "sourceDimensions": struct.unpack(">II", source.read_bytes()[16:24]),
                    "returnedDimensions": struct.unpack(">II", image[16:24]),
                    "exactFileBytesReturnedToModel": image == source.read_bytes(),
                    "returnedPayloadCopy": str(returned.relative_to(R)),
                }
            else:
                lines = source.read_text(encoding="utf-8-sig").splitlines()
                a, b = row["arguments"].get("view_range", [1, len(lines)])
                if b == -1:
                    b = len(lines)
                requested = "\n".join(lines[a-1:b])
                row["requestedRange"] = [a, b]
                row["exactRequestedTextContainedInResult"] = requested in text.replace("\r\n", "\n")
    expected_images = {g[0] for g in freeze["imageAliasGroups"].values()}
    actual_images = {Path(r["arguments"]["path"]).name for r in calls.values() if "imagePayload" in r}
    required = {
        str(C / "batch-067-visual-task.txt"): None,
        str(V / f"batch-067-initial-{family}.md"): None,
        str(R / "kanji" / "僧.md"): None,
        str(R / "words" / "僧侶.md"): None,
        str(R / "words" / "坊さん.md"): None,
        str(FOLDER / "N1Batch067NativeTest.kt"): freeze["fixtureRanges"],
        str(FOLDER / "instrumentation.txt"): None,
        str(FOLDER / "n1-067-article-route.json"): None,
    }
    missing = []
    for path in required:
        count = len(Path(path).read_text(encoding="utf-8-sig").splitlines())
        covered = set()
        for row in calls.values():
            if row["arguments"]["path"] == path and row.get("exactRequestedTextContainedInResult"):
                a, b = row["requestedRange"]
                covered.update(range(a, b + 1))
        if covered != set(range(1, count + 1)):
            missing.append(path)
    multi = [m for m in messages if len(m.get("toolRequests", [])) > 1]
    allowed = set(required) | {str(FOLDER / name) for name in expected_images}
    unexpected = [r["arguments"]["path"] for r in calls.values() if r["arguments"]["path"] not in allowed]
    accepted = (process["exitCode"] == 0 and models == [process["requestedModel"]]
                and usage["currentModel"] == process["requestedModel"] and not active
                and not overlaps and not multi and not missing and not unexpected
                and actual_images == expected_images and all(r["success"] and r["name"] == "view" for r in calls.values()))
    record = {
        **process, "actualModels": models, "availableTools": ["view"],
        "dependentFollowupNotBlindInitial": True, "reportSha256": sha(report),
        "rawExecutionLocation": str(raw), "rawExecutionSha256": sha(raw),
        "sharedTaskSha256": freeze["sharedTaskSha256"],
        "configurationEvidence": [e["data"] for e in events if e["type"] == "session.info"],
        "usage": usage, "toolCalls": list(calls.values()), "observedToolOverlaps": overlaps,
        "multiToolResponses": len(multi), "unfinishedTools": sorted(active),
        "missingRequiredText": missing, "unexpectedReadPaths": unexpected,
        "imagePayloadsVerified": len(actual_images), "expectedPngMembershipReturned": actual_images == expected_images,
        "priorExitAndArchiveVerifiedBeforeLaunch": family == "gpt",
        "processAndCoverageAccepted": accepted,
        "limits": "Dependent original-session confirmation. Exact returned bytes/ranges establish access, not comprehension. No reviewer native execution, fresh dictionary retrieval or physical-phone evidence.",
    }
    save(audit, record)
    print(json.dumps({k: record[k] for k in ("actualModels", "processAndCoverageAccepted", "imagePayloadsVerified", "missingRequiredText", "observedToolOverlaps", "multiToolResponses")}))
    assert accepted


def repair():
    prefix = "batch-067-visual-claude-serial-repair"
    process = load(C / f"{prefix}-process.json")
    usage = load(C / f"{prefix}-usage.json")
    raw = C / f"{prefix}.jsonl"
    events = [json.loads(s) for s in raw.read_text(encoding="utf-8-sig").splitlines() if s.strip()]
    messages = [e["data"] for e in events if e["type"] == "assistant.message"]
    models = sorted({m["model"] for m in messages if m.get("model")})
    calls, active, overlaps = {}, set(), []
    for event in events:
        d = event.get("data", {})
        if event["type"] == "tool.execution_start":
            key = d["toolCallId"]
            if active:
                overlaps.append(key)
            active.add(key)
            calls[key] = {"name": d["toolName"], "arguments": d["arguments"], "startedAt": event["timestamp"]}
        elif event["type"] == "tool.execution_complete":
            key = d["toolCallId"]
            active.remove(key)
            row = calls[key]
            row.update(success=d["success"], completedAt=event["timestamp"])
            text = d.get("result", {}).get("content", "")
            source = Path(row["arguments"]["path"])
            row["exactCompleteTextReturned"] = source.read_text(encoding="utf-8-sig").strip() in text.replace("\r\n", "\n")
            row["returnedTextSha256"] = hashlib.sha256(text.encode("utf-8")).hexdigest()
    report = V / f"{prefix}.md"
    assert not report.exists()
    report.write_text([m["content"] for m in messages if m.get("content")][-1] + "\n", encoding="utf-8")
    expected = [str(FOLDER / "instrumentation.txt"), str(FOLDER / "n1-067-article-route.json")]
    accepted = (process["exitCode"] == 0 and models == ["claude-opus-5.5"] == [usage["currentModel"]]
                and len(calls) == 2 and not active and not overlaps
                and [r["arguments"]["path"] for r in calls.values()] == expected
                and all(r["name"] == "view" and r["success"] and r["exactCompleteTextReturned"] for r in calls.values())
                and all(len(m.get("toolRequests", [])) <= 1 for m in messages))
    record = {
        **process, "actualModels": models, "serialRepairAccepted": accepted, "toolCalls": list(calls.values()),
        "observedToolOverlaps": overlaps, "reportSha256": sha(report), "rawExecutionLocation": str(raw),
        "rawExecutionSha256": sha(raw), "usage": usage,
        "limits": "Two small operational receipts reread serially in original session. Original overlap/report preserved, not reclassified as compliant. No image/teaching/native rerun or new independent initial review.",
    }
    save(V / f"{prefix}-execution.json", record)
    print(json.dumps({"serialRepairAccepted": accepted, "calls": len(calls), "actualModels": models}))
    assert accepted


if __name__ == "__main__":
    if sys.argv[1] == "prepare":
        prepare()
    elif sys.argv[1] == "archive":
        archive(sys.argv[2])
    elif sys.argv[1] == "repair":
        repair()

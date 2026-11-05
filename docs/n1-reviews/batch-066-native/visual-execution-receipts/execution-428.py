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
HEAD = "b37c5ad6ffb5ab62cf4525b50afe4e2a6cdd011b"
TEACHING = "6c23db00d2d14ec6d0a3537a1ef72b273e3d55e7"
FOLDER = V / "batch-066-native" / "attempt-1"
load = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def git(*args):
    return subprocess.check_output(["git", "-C", str(R), *args], encoding="utf-8").strip()


def prepare():
    assert git("rev-parse", "HEAD") == HEAD and not git("status", "--porcelain")
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    request = C / r"logs\024c50c5-a1b6-4337-b6d0-1aacbdd89d16\request.txt"
    text = request.read_text(encoding="utf-8-sig")
    embedded = json.loads(text.split("Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    state = load(C / "progress.json")
    assert state["checkpoint"] == embedded["checkpoint"] == 427 and state["batch"] == "066"
    backup = C / "execution-428-before-progress.json"
    assert not backup.exists()
    backup.write_bytes((C / "progress.json").read_bytes())
    start = {
        "execution": 428, "batch": "066", "startingHead": HEAD,
        "scope": "SAME066 two serial ORIGINAL-session dependent visual confirmations, exact returned-image/range/process archival, reconciliation and normally signed local checkpoint only. No native/Android rerun, runtime publication,067 or second runner.",
        "authorization": {
            "requestSha256": sha(request), "characters": len(text), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request acquired and complete embedded checkpoint parsed; operative contract, final427 and approved issue inspected directly. Historical middle acquired/parsed, not freshly semantically re-reviewed.",
        },
        "recordedAt": datetime.now(timezone.utc).isoformat(),
    }
    save(C / "execution-428-start.json", start)
    state["execution428StartingState"] = start
    state["stage"] = "batch-066-dependent-visual-confirmation-starting"
    save(C / "progress.json", state)
    index = V / "batch-066-native" / "execution-427-artifact-index.json"
    groups = {}
    for row in load(index)["files"]:
        path = R / row["path"]
        assert sha(path) == row["sha256"] and path.stat().st_size == row["bytes"]
        if path.suffix == ".png":
            groups.setdefault(row["sha256"], []).append(path.name)
    names = [g[0] for g in groups.values()]
    fixture = FOLDER / "N1Batch066NativeTest.kt"
    count = len(fixture.read_text(encoding="utf-8").splitlines())
    ranges = [(a, min(a + 139, count)) for a in range(1, count + 1, 140)]
    task = f"""SAME066 dependent ORIGINAL-session native visual confirmation, execution428.
NOT a new blind initial review, dictionary audit or native rerun.
Frozen evidence HEAD {HEAD}; teaching unchanged from {TEACHING}.
Native full git envelope source 175fdf3f1605f231e27a9de19a7c18c4a02cb20d.

STRICT SERIAL: exactly ONE view tool call per response, then WAIT for its result.
Never multiple tool calls or parallel wrappers even for text. No shell, edits,
search, delegation, task_complete or new device operations. Only view available.
Read this COMPLETE shared task: {C / 'batch-066-visual-task.txt'}
Read YOUR complete original initial report (exact path appended to prompt).
Do not read another report or coordinator adjudication. Inherit your original
lexical conclusions with all original source/lookup limits.

Freshly read COMPLETE three teaching files separately:
{R / 'kanji' / '僚.md'}
{R / 'words' / '同僚.md'}
{R / 'kanji' / '同.md'}
Only words\\同僚.md:28 component link and kanji\\同.md:36 common-word line
are changed reused scope. Complete new 僚 is in scope. No subsequent runtime diff.
Unchanged reused teaching is context, not a fresh easier-deck review.

Read COMPLETE native fixture in separate inclusive ranges {ranges}:
{fixture}
Read COMPLETE terminal log and route receipt separately:
{FOLDER / 'instrumentation.txt'}
{FOLDER / 'n1-066-article-route.json'}

Actually VIEW EACH PNG singly, ONE PER RESPONSE, under:
{FOLDER}\\
""" + "\n".join(names) + f"""

These are {len(names)} DISTINCT source hashes selected from41capture names.
Byte-identical aliases are not independent scenes. Filenames/selectors/
assertIsDisplayed are NOT proof a named sentence or whole cell is visible.
Inspect actual pixels and disclose unseen/clipped prose/first-column labels.
Source1080x2400 may be resized by view; record actual transport/dimensions and
viewport limits honestly. Horizontally shifted labels alone do not establish
inaccessible content; there is a sideways-scroll hint. Consequential unsupported
visual conclusions remain UNVERIFIED, not CLEAN by a screenshot's filename.

Inspect 僚/療/像/値/人/亻/疒/同/口 and 同僚 in FOUR production font rows:
readable/distinguishable, no blank/replacement boxes, especially 僚 versus療,
person亻 versusillness疒 and different right components of像/値.
Typeface change alone is not a defect; fallback styles may coincide.
36single-Paint+4word-raster probes support nonblankness/distinct rasters, not
fallback-face identity or every-phone readability.
Full+curated on[リョウ], full+curated kun[]; sole normalizedりょう key.
Check actual question/options/feedback pixels, not feedback dictionary list alone.
Modern14strokes/canonicalradical人9/visible亻; labelled mnemonic not etymology.
Check colleague/associate versus official sense/官僚かんりょう and work role not
rigid equal rank/friendship. 同僚どうりょう/ドウ+リョウ; noun examples withと,
consulted-personに/plural context, 仲間/友人/上司 distinction and rank boundary
where ACTUALLY visible. Meaning option labels may differ from authored distractors
療/像/値; inspect displayed choices, no whole-pool certification.
TWO mapped component pairs僚-同僚 and同-同僚, FOUR directions, SystemBack.
同じ direct ordinary-noun attachment note is unchanged context, not a new edit.
No new word title/exclusion or support article.

SUPPLIED operational results, NOT reviewer-executed:427 both namedcases terminal0,
no skips93.971s. Exact full archive productionContentSyncONCE:1078kanji5036words98N1,
problems0/contentVersiona9ecc100b6c1335c/parserEpoch1.
Read actual fixture assertions and terminal log. Synthetic disposable source/HEAD,
otherN1 postponed, two historicalGoodmeaninglogs unlock drawing, no drawing state
seeded. Not owner progress/learning efficacy. Meaning feedback exits Back before
Next: do NOT claim a new persisted meaning grade. SoleOnGood persisted/noKunLog.
14generated-reference touchstrokes/ungradedtrace/model-unavailablegeometryfeedback/
recallmiss/persistedDrawAgain are NOT MLKit recognition/human successful recall or
negative geometry/reverse-order testing. Downloading label is not successful model
download. Offline/SystemBack API35fontscale1/fingerprint
google/sdk_gphone64_x86_64/emu64xa:15/AE3A.240806.036/12592187:user/release-keys.
Native heapgrowth192m/heapsize576m unchanged; accepted425 freshAndroid3+1 inherited,
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
    task_path = C / "batch-066-visual-task.txt"
    assert not task_path.exists()
    task_path.write_text(task, encoding="utf-8")
    for family in ("claude", "gpt"):
        (C / f"batch-066-visual-{family}-prompt.txt").write_text(
            task + f"\nRead YOUR complete original initial report: {V / f'batch-066-initial-{family}.md'}\n", encoding="utf-8")
    freeze = {
        "schemaVersion": 1, "execution": 428, "batch": "066", "evidenceHead": HEAD,
        "teachingSnapshot": TEACHING, "nativeArtifactIndexSha256": sha(index),
        "indexedArtifactsVerified": len(load(index)["files"]), "sourceCaptureNames": 41,
        "assignedDistinctSourceImages": len(names), "imageAliasGroups": groups,
        "fixtureRanges": ranges, "sharedTaskSha256": sha(task_path),
        "teachingHashes": {str(p.relative_to(R)): sha(p) for p in [
            R / "kanji" / "僚.md", R / "words" / "同僚.md", R / "kanji" / "同.md", R / "manifest.json"]},
        "originalReportHashes": {str(p.relative_to(R)): sha(p) for p in [
            V / f"batch-066-initial-{family}.md" for family in ("claude", "gpt")]},
    }
    save(C / "batch-066-visual-freeze.json", freeze)
    print("Starting state persisted; artifacts verified; assigned", len(names), "distinct images.")


def archive(family):
    prefix = f"batch-066-visual-{family}"
    process = load(C / f"{prefix}-process.json")
    usage = load(C / f"{prefix}-usage.json")
    freeze = load(C / "batch-066-visual-freeze.json")
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
                returned = V / "batch-066-native" / f"visual-{family}-returned" / source.name
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
                lines = source.read_text(encoding="utf-8-sig").splitlines(keepends=True)
                a, b = row["arguments"].get("view_range", [1, -1])
                expected = "".join(lines[a - 1:None if b == -1 else b])
                norm = lambda s: s.replace("\r\n", "\n").rstrip()
                row["exactRequestedTextContainedInResult"] = norm(expected) in norm(text)
                row["requestedRange"] = [a, len(lines) if b == -1 else b]
    required = [
        C / "batch-066-visual-task.txt", V / f"batch-066-initial-{family}.md",
        R / "kanji" / "僚.md", R / "words" / "同僚.md", R / "kanji" / "同.md",
        FOLDER / "N1Batch066NativeTest.kt", FOLDER / "instrumentation.txt", FOLDER / "n1-066-article-route.json",
    ]
    missing = []
    for path in required:
        covered = {i for x in calls.values() if x.get("exactRequestedTextContainedInResult")
                   and Path(x["arguments"]["path"]) == path
                   for i in range(x["requestedRange"][0], x["requestedRange"][1] + 1)}
        if not set(range(1, len(path.read_text(encoding="utf-8-sig").splitlines()) + 1)) <= covered:
            missing.append(str(path))
    expected_names = {g[0] for g in freeze["imageAliasGroups"].values()}
    images = [x for x in calls.values() if "imagePayload" in x]
    multi = [m.get("messageId") for m in messages if len(m.get("toolRequests", [])) > 1]
    allowed = {str(p) for p in required} | {str(FOLDER / n) for n in expected_names} | {str(C / f"{prefix}-prompt.txt")}
    unexpected = [x["arguments"]["path"] for x in calls.values() if x["arguments"]["path"] not in allowed]
    prior_ok = True
    if family == "gpt":
        prior_path = V / "batch-066-visual-claude-execution.json"
        prior = load(prior_path)
        began = datetime.fromisoformat(process["startedAt"])
        prior_ok = prior["processAndCoverageAccepted"] and datetime.fromisoformat(prior["completedAt"]) < began and prior_path.stat().st_mtime < began.timestamp()
    terminal = [e for e in events if e["type"] == "result"]
    accepted = (
        process["exitCode"] == 0 and models == [process["requestedModel"]] == [usage["currentModel"]]
        and not active and not overlaps and not multi and not missing and not unexpected and prior_ok
        and all(x["name"] == "view" and x["success"] and not x.get("truncationOrLimitMarker", False)
                and x.get("exactRequestedTextContainedInResult", True) for x in calls.values())
        and len(images) == len(expected_names) == 19
        and {Path(x["arguments"]["path"]).name for x in images} == expected_names
        and len(terminal) == 1 and terminal[0]["exitCode"] == 0
        and terminal[0]["sessionId"] == process["sessionId"]
        and not terminal[0]["usage"]["codeChanges"]["filesModified"]
    )
    record = {
        **process, "actualModels": models, "availableTools": ["view"], "dependentFollowupNotBlindInitial": True,
        "reportSha256": sha(report), "rawExecutionLocation": str(raw), "rawExecutionSha256": sha(raw),
        "sharedTaskSha256": freeze["sharedTaskSha256"],
        "configurationEvidence": [e["data"] for e in events if e["type"] in ("session.info", "session.tools_updated")],
        "controlArtifactHashes": {s: sha(C / (prefix + s)) for s in ("-process.json", "-usage.json", "-prompt.txt", "-stderr.txt", "-preflight.json")},
        "toolCalls": list(calls.values()), "observedToolOverlaps": overlaps, "multiToolResponses": multi,
        "unfinishedTools": sorted(active), "missingRequiredText": missing, "unexpectedReadPaths": unexpected,
        "imagePayloadsVerified": len(images), "expectedPngMembershipReturned": {Path(x["arguments"]["path"]).name for x in images} == expected_names,
        "priorExitAndArchiveVerifiedBeforeLaunch": prior_ok, "processAndCoverageAccepted": accepted,
        "usage": usage, "usageBoundary": "Resumed-session usage cumulative, not this turn's cost.",
        "terminalResults": [{"sessionId": e["sessionId"], "exitCode": e["exitCode"]} for e in terminal],
        "limits": "Dependent original-session visual confirmation, not blind initial or reviewer-executed native tests. Actual returned bytes are not comprehension. Raw execution retained in sibling control; no private instructions/provider reasoning exported into Git.",
    }
    save(audit, record)
    print(json.dumps({"family": family, "models": models, "calls": len(calls), "images": len(images), "overlaps": overlaps,
                      "multi": multi, "missing": missing, "unexpected": unexpected, "accepted": accepted}, ensure_ascii=True, indent=2))
    assert accepted, "Original report preserved; process or coverage requires bounded reconciliation."


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if sys.argv[1] == "prepare":
        prepare()
    elif sys.argv[1] == "archive":
        archive(sys.argv[2])

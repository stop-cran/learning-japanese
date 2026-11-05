import base64
import gzip
import hashlib
import json
import os
import shutil
import struct
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).parent
R = C.parent / "learning-japanese"
V = R / "docs" / "n1-reviews"
F = V / "batch-068-native"
LOG = C / r"logs\87b53f2e-5022-411c-b2cc-e1949c27d1dd"
HEAD = "8b55a36712029349fe66c084ae0588efb49b8001"
TEACHING = "80f5f424729d8832cdc9ecb8491b59559d921cd3"
IMAGES = [
    "font-pairs", "kanji-01", "kanji-11", "kanji-19",
    "word1-06", "word2-07", "word3-07", "word4-07",
    "component1-16", "component2-20", "component3-30", "component4-19",
    "curated-On-question", "curated-On-feedback", "meaning-question", "meaning-feedback",
    "drawing-trace", "drawing-feedback", "drawing-recall-feedback", "selection",
]
FILES = [R / "kanji" / "儀.md"] + [
    R / "words" / (name + ".md") for name in ("儀式", "礼儀", "行儀", "お辞儀")
] + [R / "kanji" / (name + ".md") for name in ("式", "礼", "行", "辞")]
SESSIONS = {
    "claude": ("claude-opus-5.5", "79971d7f-dd53-46bf-8249-df9d0c122c12"),
    "gpt": ("gpt-6.1-sol", "4b8ed210-be92-4627-8679-44e8622067dd"),
}
NEXT = (
    "SAME068 signed bounded visual checkpoint445: original Claude79971d7f and GPT4b8ed210 "
    "dependent visual confirmations complete; both processes exited serially, each41single "
    "view calls/20assignedPNG/complete9teachingfiles/696linefixture/ownoriginal+confirmation/"
    "terminal-log/route. All40actual returned900x2000payloads archived separately from "
    "1080x2400sources;20/127capture scope, not full-PNG acceptance. Read "
    "docs\\n1-sources\\execution-445.json and docs\\n1-reviews\\batch-068-visual-reconciliation.json. "
    "All8changedreusedpassages/revised私儀note/fontglyphs/soleギ/actualmeaningoptions/"
    "drawingtrace+recallmiss covered. No actionable teaching/rendering defect established; "
    "no teaching/app edits. All445reviewer internal calls serial, no overlaps; original441 "
    "Claude13ms textual-confirmation overlap remains historical with its serial repair, "
    "not erased. No fresh native/dictionary/HOST rerun. Inherit444native2terminal0/272.859s "
    "and442freshAndroid3+1; no redundant heavy work absentnewconcern. Viewport clipping with "
    "sideways hint does not establish inaccessible content. Fallbackface/MLKit/humanrecall/"
    "physicalphone/generalrelease/whole-set remain unverified. Next bounded checkpoint: "
    "freshfetchlatestorigin/main, nonrewritingintegration as needed, actualcombined "
    "source-membership/baseline/reading/link/font/stroke/Python/vocab/validator/freshmanifest/"
    "original18000entries42MiBcompressed80MiBinflated56MiBretainedbudgets, normal signing/"
    "ownerfastforward/publicSHA/terminalgreenCI/EVERYimmutablepublicZIP runtimehash/budgets/"
    "ownerissue60 BEFOREdelivery or069. Preserve precise permissiondenials/signingwait and "
    "yield; no workaround/secondrunner/concurrentheavywork/supervisorchanges. QualifiedHOST-"
    "only2GiBinit NEVER nativebuilds; historicaldenials/OOMs/full livehistory retained. "
    "Published94/1228,remaining1134/latest06772f99d82; local068 NOTdelivered. Compatible "
    "Androidf9b59a2+ required; wholeproject incomplete."
)


def load(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def save(p, value):
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    assert load(p) == json.loads(json.dumps(value, ensure_ascii=False))


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def git(*args):
    return subprocess.check_output(["git", "--no-pager", "-C", str(R), *args], encoding="utf-8").strip()


def verify_freeze():
    freeze = load(C / "batch-068-visual-freeze.json")
    assert git("rev-parse", "HEAD") == HEAD
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    for path, digest in freeze["resourceHashes"].items():
        assert sha(Path(path)) == digest, path
    return freeze


def prepare():
    assert git("rev-parse", "HEAD") == HEAD and not git("status", "--porcelain")
    request = LOG / "request.txt"
    text = request.read_text(encoding="utf-8-sig")
    embedded = json.loads(text.split("Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    p = load(C / "progress.json")
    assert p["checkpoint"] == embedded["checkpoint"] == 444 and p["batch"] == "068"
    backup = LOG / "execution-445-before-progress.json"
    assert not backup.exists()
    backup.write_bytes((C / "progress.json").read_bytes())
    start = {
        "execution": 445, "batch": "068", "startingHead": HEAD, "recordedAt": now(),
        "scope": "SAME068 two serial original-session dependent bounded visual confirmations, exact payload/range/process archival, reconciliation and normally signed local evidence checkpoint only. No native/Android rerun, publication,069 or second runner.",
        "authorization": {
            "requestSha256": sha(request), "characters": len(text), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request acquired and complete embedded checkpoint parsed; operative contract, final444 checkpoint and complete approved issue inspected directly. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "status": "dependent-visual-confirmation-preparing",
    }
    save(LOG / "execution-445-start.json", start)
    p["execution445StartingState"] = start
    p["stage"] = "batch-068-dependent-visual-confirmation-preparing"
    p["nextAction"] = start["scope"]
    save(C / "progress.json", p)
    index = F / "execution-444-artifact-index.json"
    for row in load(index)["artifacts"]:
        assert sha(R / row["path"]) == row["sha256"]
        assert (R / row["path"]).stat().st_size == row["bytes"]
        if "rawGzipPath" in row:
            assert sha(R / row["rawGzipPath"]) == row["rawGzipSha256"]
            original = gzip.decompress((R / row["rawGzipPath"]).read_bytes())
            assert hashlib.sha256(original).hexdigest() == row["originalSha256"]
    fixture = F / "N1Batch068NativeTest.kt"
    n = len(fixture.read_text(encoding="utf-8").splitlines())
    ranges = [[a, min(a + 119, n)] for a in range(1, n + 1, 120)]
    images = [F / ("n1-068-" + name + ".png") for name in IMAGES]
    task = f"""SAME068 original-session DEPENDENT native visual confirmation, execution445.
NOT a fresh blind initial review, fresh dictionary audit or native rerun.
Frozen evidence HEAD {HEAD}; teaching unchanged from {TEACHING}.
Native full Git envelope source7ca40a695d8e01f4176f4afcca91b1e4d2d6c0b0.

STRICT SERIAL TOOLS: exactly ONE view call per response, WAIT for its result.
Never multiple tool calls or a parallel wrapper, even for small text.
Only view available. No shell/edit/search/delegation/device operations.
Read this COMPLETE shared task: {C / 'batch-068-visual-task.txt'}
Read YOUR complete original initial report and YOUR latest textual confirmation
(exact two paths appended to the launch prompt). Do not read another report
or coordinator adjudication. Inherit original lexical conclusions and original
source/lookup limits; do not pretend fresh upstream retrieval.

Read each COMPLETE teaching file, ONE view call at a time:
""" + "\n".join(str(path) for path in FILES) + f"""

Only new 儀 is whole-card teaching scope. Eight changed reused passages are:
words\\儀式.md: the formation paragraph links 儀; counterpart kanji\\式.md:
Common words 儀式ぎしき. words\\礼儀.md: formation links 儀; counterpart
kanji\\礼.md: Common words 礼儀れいぎ. words\\行儀.md: formation links 儀;
counterpart kanji\\行.md: Common words 行儀ぎょうぎ. words\\お辞儀.md:
formation links 儀; counterpart kanji\\辞.md: Common words お辞儀おじぎ.
Complete reused bodies are context, NOT renewed full easier-deck review.
No new words; no teaching diff after your textual confirmation.

Read COMPLETE native fixture in separate inclusive ranges {ranges}:
{fixture}
Read COMPLETE each small operational receipt in SEPARATE calls:
{F / 'instrumentation.txt'}
{F / 'n1-068-article-route.json'}

Actually VIEW each of these TWENTY PNGs singly, ONE PER RESPONSE:
""" + "\n".join(str(path) for path in images) + """

This is a bounded20/127 capture packet, not all127PNG coverage. Assignments:
word1=儀式,word2=礼儀,word3=行儀,word4=お辞儀;
component1=式,component2=礼,component3=行,component4=辞.
The eight listed word/component images assign ALL eight changed reused passages.
kanji19 assigns revised formal suffix 私儀 note; kanji11 reading table,
kanji01 heading/shape context. Names/selectors/assertions do NOT prove visibility;
inspect actual pixels. Report if a named sentence/label is absent or clipped.
Source1080x2400 may be resized by view; disclose returned transport/viewport
limits. Sideways-scroll hint means a horizontally shifted clipped label alone
is NOT proof the content is inaccessible. Do not equate clipping at one scroll
offset with an established defect; consequential unsupported conclusions remain
UNVERIFIED. Distinguish whole-file text review from bounded visible viewport.

Inspect 儀/義/億/優/倍/人/亻/式/礼/辞/行/亍/弋/彳/礻 and
儀式/礼儀/行儀/お辞儀 across FOUR production font rows.
Readable/distinguishable, no blank/replacement boxes, 儀 versus義 left亻,
different right halves億優倍, standalone人/亻, components亍弋彳礻.
Typeface changes and coinciding fallback styles alone are not defects.
60single-Paint+16word-raster probes support nonblankness/distinct rasters,
NOT fallback-face identity/every-phone readability.
Full+curated on[ギ], full+curated kun[], normalized soleぎ key.
Check actual question/options/feedback pixels; feedback dictionary alone is not
proof of actual offered key. Authored distractors億優倍; actual meaning choices
can differ: inspect displayed labels, do not claim whole-pool certification.
15strokes/canonical radical人9/visible亻; labelled mnemonic not etymology.
Ceremony/formal conduct rather than every儀 means ceremony; suffix self/own-side,
humble/formal correspondence 私儀わたくしぎ; matter/affair branch and 地球儀
counterexample. Complete notes may not all be visible in selected PNGs.
Eight mapped reciprocal pairs, sixteen directions: 儀 with each of four words,
plus式/儀式,礼/礼儀,行/行儀,辞/お辞儀. No incidental backlink requirement.

SUPPLIED operational results, NOT reviewer-executed:444 two named native cases
terminal0/no skips272.859s. Exact full envelope productionContentSyncONCE:
1080kanji5037words100N1/problems0/versionddef65b637fe2f85/epoch1.
Read actual fixture and terminal log. Synthetic disposable source/HEAD;
other N1 postponed; two historicalGood meaning logs unlock drawing.
No drawing state seeded; not owner progress or measured learning efficacy.
Meaning feedback exits Back before Next: do NOT claim new persisted meaning
grade. SoleOnGood persisted/noKunLog. Fifteen generated-reference touch strokes,
ungradedtrace/model-unavailablegeometryfeedback/recallmiss/persistedDrawAgain
are NOT MLKit recognition, human successful recall or negative/reverse-order
geometry testing. Downloading label is not successful model download.
Offline/SystemBack API35fontscale1/fingerprint
google/sdk_gphone64_x86_64/emu64xa:15/AE3A.240806.036/12592187:user/release-keys.
Native heapgrowth192m/heapsize576m unchanged;442freshAndroid3+1 inherited,
not rerun. Owned helpers stopped; preexistingemulator5556 preserved.
No fresh source retrieval/native execution by reviewer. Historical denials/HOST
OOMs preserved; qualifiedHOST-only2GiB init NEVER applies to native.

Return COMPLETE Snapshot/Scope/Verdicts/Findings/Optional/Limits report.
Verdicts separately for 儀 and EACH of EIGHT changed reused article passages:
correctness/scopedcoverage/comprehensibility CLEAN,NEEDS FIX,UNVERIFIED.
Separate inherited lexical conclusions, new pixels, supplied runtime assertions.
Enumerate actual20image reads/text ranges/deviations. Findings need severity,
facet,exactPNG location or filelines,impact,remedy,evidence,confidence. No quota.
Optional polish not a blocker. Unseen parts/fallbackface/physicalphone/general
release/whole-set/latestmain/publication limits explicit. Androidf9b59a2+ required.
Finish COMPLETE report then EXIT; no questions/fixes/next batch.
"""
    task_path = C / "batch-068-visual-task.txt"
    assert not task_path.exists()
    task_path.write_text(task, encoding="utf-8")
    resources = FILES + images + [fixture, F / "instrumentation.txt", F / "n1-068-article-route.json", index, task_path]
    for family in SESSIONS:
        initial = V / f"batch-068-initial-{family}.md"
        confirm = V / ("batch-068-confirm-serial-repair-claude.md" if family == "claude" else "batch-068-confirm-gpt.md")
        resources.extend([initial, confirm])
        prompt = task + f"\nYOUR original report: {initial}\nYOUR latest textual confirmation: {confirm}\n"
        (C / f"batch-068-visual-{family}-prompt.txt").write_text(prompt, encoding="utf-8")
    save(C / "batch-068-visual-freeze.json", {
        "execution": 445, "batch": "068", "evidenceHead": HEAD, "teachingSnapshot": TEACHING,
        "images": [str(path) for path in images], "assignedCaptures": 20,
        "archivedCaptures": 127, "fixtureRanges": ranges,
        "resourceHashes": {str(path): sha(path) for path in resources},
    })
    for args, name in [(["--help"], "help"), (["help", "config"], "models")]:
        result = subprocess.run([shutil.which("copilot"), *args], check=True, capture_output=True, encoding="utf-8")
        (C / f"batch-068-visual-{name}-execution-445.txt").write_text(result.stdout, encoding="utf-8")
    print("Starting scope saved; exact native evidence verified; bounded20image packet prepared.")


def run(family):
    verify_freeze()
    if family == "gpt":
        prior = load(V / "batch-068-visual-claude-execution.json")
        assert prior["exitCode"] == 0 and not prior["unfinishedTools"]
    model, session = SESSIONS[family]
    prefix = "batch-068-visual-" + family
    raw = C / f"{prefix}.jsonl"
    assert not raw.exists(), "Never overwrite original execution"
    command = [
        shutil.which("copilot"), "-C", str(R), "--add-dir", str(C),
        "--model", model, "--session-id", session, "--no-ask-user",
        "--allow-all-tools", "--disable-builtin-mcps", "--available-tools=view",
        "--output-format", "json", "--log-dir", str(C / "review-logs" / prefix),
        "--usage-output-file", str(C / f"{prefix}-usage.json"),
        "-p", "Read the entire bounded dependent visual task at " + str(C / f"{prefix}-prompt.txt")
        + ". Execute it with exactly ONE view tool call per response; WAIT before each next call. Never parallel tools.",
    ]
    env = os.environ.copy()
    env.pop("GH_TOKEN", None)
    env.pop("GITHUB_TOKEN", None)
    started = now()
    with raw.open("wb") as out, (C / f"{prefix}-stderr.txt").open("wb") as err:
        process = subprocess.Popen(command, stdout=out, stderr=err, env=env)
        save(C / f"{prefix}-active.json", {"pid": process.pid, "sessionId": session, "startedAt": started})
        print(f"Running original {family}: PID{process.pid} model{model}", flush=True)
        code = process.wait()
    save(C / f"{prefix}-process.json", {
        "launcherPid": process.pid, "startedAt": started, "completedAt": now(),
        "exitCode": code, "requestedModel": model, "sessionId": session, "snapshot": HEAD,
        "command": command, "priorProcessExitedBeforeLaunch": family == "gpt",
    })
    assert code == 0, f"Reviewer exit {code}; original output preserved"
    archive(family)


def archive(family):
    freeze = verify_freeze()
    prefix = "batch-068-visual-" + family
    raw = C / f"{prefix}.jsonl"
    process = load(C / f"{prefix}-process.json")
    usage = load(C / f"{prefix}-usage.json")
    events = [json.loads(line) for line in raw.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    messages = [event["data"] for event in events if event["type"] == "assistant.message"]
    models = sorted({m["model"] for m in messages if m.get("model")})
    report = V / f"{prefix}.md"
    assert not report.exists()
    report.write_text([m["content"] for m in messages if m.get("content")][-1] + "\n", encoding="utf-8")
    calls, active, overlaps = {}, set(), []
    for event in events:
        data = event.get("data", {})
        key = data.get("toolCallId")
        if event["type"] == "tool.execution_start":
            if active:
                overlaps.append({"starting": key, "active": sorted(active)})
            active.add(key)
            calls[key] = {"name": data["toolName"], "arguments": data["arguments"], "startedAt": event["timestamp"]}
        elif event["type"] == "tool.execution_complete":
            active.remove(key)
            row = calls[key]
            row.update(success=data["success"], completedAt=event["timestamp"])
            if not data["success"]:
                row["error"] = data.get("error")
                continue
            result = data["result"]
            text = result.get("content", "")
            row["returnedTextSha256"] = hashlib.sha256(text.encode("utf-8")).hexdigest()
            source = Path(row["arguments"]["path"])
            if source.suffix == ".png":
                images = result.get("binaryResultsForLlm", [])
                assert len(images) == 1 and images[0]["type"] == "image"
                payload = base64.b64decode(images[0]["data"], validate=True)
                assert payload[:8] == b"\x89PNG\r\n\x1a\n"
                target = F / f"visual-{family}-returned" / source.name
                target.parent.mkdir(exist_ok=True)
                assert not target.exists()
                target.write_bytes(payload)
                row["imagePayload"] = {
                    "bytes": len(payload), "sha256": sha(target), "sourceSha256": sha(source),
                    "sourceDimensions": struct.unpack(">II", source.read_bytes()[16:24]),
                    "returnedDimensions": struct.unpack(">II", payload[16:24]),
                    "exactSourceBytesReturned": payload == source.read_bytes(),
                    "returnedPayloadCopy": str(target.relative_to(R)),
                }
            else:
                lines = source.read_text(encoding="utf-8-sig").splitlines()
                a, b = row["arguments"].get("view_range", [1, len(lines)])
                b = len(lines) if b == -1 else b
                row["requestedRange"] = [a, b]
                row["exactRequestedTextContainedInResult"] = "\n".join(lines[a-1:b]) in text.replace("\r\n", "\n")
    initial = V / f"batch-068-initial-{family}.md"
    confirm = V / ("batch-068-confirm-serial-repair-claude.md" if family == "claude" else "batch-068-confirm-gpt.md")
    required = FILES + [C / "batch-068-visual-task.txt", initial, confirm, F / "N1Batch068NativeTest.kt",
                        F / "instrumentation.txt", F / "n1-068-article-route.json"]
    missing = []
    for path in required:
        covered = set()
        for row in calls.values():
            if row["arguments"]["path"] == str(path) and row.get("exactRequestedTextContainedInResult"):
                a, b = row["requestedRange"]
                covered.update(range(a, b + 1))
        if covered != set(range(1, len(path.read_text(encoding="utf-8-sig").splitlines()) + 1)):
            missing.append(str(path))
    actual_images = {row["arguments"]["path"] for row in calls.values() if "imagePayload" in row}
    allowed = {str(path) for path in required} | set(freeze["images"]) | {str(C / f"{prefix}-prompt.txt")}
    unexpected = [row["arguments"]["path"] for row in calls.values() if row["arguments"]["path"] not in allowed]
    multi = sum(len(m.get("toolRequests", [])) > 1 for m in messages)
    accepted = (process["exitCode"] == 0 and models == [process["requestedModel"]] == [usage["currentModel"]]
                and not active and not overlaps and not multi and not missing and not unexpected
                and actual_images == set(freeze["images"])
                and all(row["success"] and row["name"] == "view" for row in calls.values()))
    record = {
        **process, "actualModels": models, "availableTools": ["view"],
        "dependentOriginalSessionNotBlindInitial": True, "reportSha256": sha(report),
        "rawExecutionLocation": str(raw), "rawExecutionSha256": sha(raw),
        "configurationEvidence": [event["data"] for event in events if event["type"] == "session.info"],
        "usage": usage, "toolCalls": list(calls.values()), "observedToolOverlaps": overlaps,
        "multiToolResponses": multi, "unfinishedTools": sorted(active), "missingRequiredText": missing,
        "unexpectedReadPaths": unexpected, "imagePayloadsVerified": len(actual_images),
        "expectedPngMembershipReturned": actual_images == set(freeze["images"]),
        "processAndCoverageAccepted": accepted,
        "limits": "Dependent original-session confirmation;20/127captures. Exact bytes/ranges establish access, not comprehension. No reviewer native execution, fresh upstream dictionary retrieval, physical-phone or final publication acceptance.",
    }
    save(V / f"{prefix}-execution.json", record)
    print(json.dumps({key: record[key] for key in ("actualModels", "processAndCoverageAccepted", "imagePayloadsVerified",
                                                   "missingRequiredText", "observedToolOverlaps", "multiToolResponses")}))
    assert accepted


def verify_reviews():
    freeze = verify_freeze()
    records = {}
    for family, (model, session) in SESSIONS.items():
        prefix = "batch-068-visual-" + family
        record = load(V / f"{prefix}-execution.json")
        assert record["processAndCoverageAccepted"] and record["exitCode"] == 0
        assert record["actualModels"] == [model] == [record["usage"]["currentModel"]]
        assert record["sessionId"] == session and not record["unfinishedTools"]
        assert not record["observedToolOverlaps"] and not record["multiToolResponses"]
        assert record["imagePayloadsVerified"] == 20
        assert sha(V / f"{prefix}.md") == record["reportSha256"]
        assert sha(Path(record["rawExecutionLocation"])) == record["rawExecutionSha256"]
        for row in record["toolCalls"]:
            assert row["name"] == "view" and row["success"]
            if "imagePayload" in row:
                payload = row["imagePayload"]
                assert sha(R / payload["returnedPayloadCopy"]) == payload["sha256"]
                assert sha(Path(row["arguments"]["path"])) == payload["sourceSha256"]
                assert payload["sourceDimensions"] == [1080, 2400]
                assert payload["returnedDimensions"] == [900, 2000]
            else:
                assert row["exactRequestedTextContainedInResult"]
        records[family] = record
    assert datetime.fromisoformat(records["claude"]["completedAt"]) < datetime.fromisoformat(records["gpt"]["startedAt"])
    return freeze, records


def record():
    freeze, records = verify_reviews()
    counts = {family: len(item["toolCalls"]) for family, item in records.items()}
    assert set(counts.values()) == {41}, counts
    checks = {}
    for name in ("validate", "manifest", "budget"):
        source = C / f"execution-445-{name}.txt"
        target = V / f"batch-068-visual-{name}-execution-445.txt"
        assert not target.exists()
        shutil.copyfile(source, target)
        checks[name] = {"path": str(target.relative_to(R)), "sha256": sha(target)}
    for name in ("task", "help-execution-445", "models-execution-445"):
        source = C / f"batch-068-visual-{name}.txt"
        target = V / source.name
        assert not target.exists()
        target.write_text(source.read_text(encoding="utf-8-sig"), encoding="utf-8")
    save(V / "batch-068-visual-freeze.json", freeze)
    limits = (
        "Bounded20/127capture confirmation, not all screenshots/viewports or full easier-deck review. "
        "Exact returned text/image bytes establish access, not comprehension. Source1080x2400 rendered "
        "to900x2000 by view, not native-pixel physical viewing size. Sideways-scroll hint and complementary "
        "views do not certify every offset. No fallback-face identity/every-phone readability/MLKit/"
        "human recall/negative geometry/successful model download/native-language certification. "
        "Original frozen-XML/public-source retrieval limitations retained; no fresh dictionary fetch "
        "or reviewer native execution. Physical-phone/general-release/current-main/whole-set/publication "
        "acceptance outstanding; Androidf9b59a2+ required. Historical441 textual overlap/repair preserved."
    )
    reviews = {
        family: {
            "report": str((V / f"batch-068-visual-{family}.md").relative_to(R)),
            "reportSha256": item["reportSha256"],
            "execution": str((V / f"batch-068-visual-{family}-execution.json").relative_to(R)),
            "executionSha256": sha(V / f"batch-068-visual-{family}-execution.json"),
            "actualModel": item["actualModels"][0], "sessionId": item["sessionId"],
            "startedAt": item["startedAt"], "completedAt": item["completedAt"],
            "exitCode": item["exitCode"], "toolCalls": len(item["toolCalls"]),
            "verifiedReturnedImages": 20, "allInternalCallsSerial": True,
            "processAndCoverageAccepted": True,
        } for family, item in records.items()
    }
    reconciliation = {
        "schemaVersion": 1, "execution": 445, "batch": "068",
        "status": "bounded-visual-confirmation-closed-awaiting-integration",
        "evidenceHead": HEAD, "reviewedTeachingSnapshot": TEACHING,
        "dependentNotBlind": True, "models": [item[0] for item in SESSIONS.values()],
        "scope": "Whole new 儀 and eight changed reused passages in context; complete nine teaching files read. Same20assigned native screenshots per model; own original report and textual confirmation, complete696line fixture/log/route.",
        "allReviewerProcessesSerialAndExited": True, "allInternalCallsSerial": True,
        "allImageCallsSerial": True, "findings": [],
        "verdicts": {
            str(path.relative_to(R)): {
                "correctness": "CLEAN", "scopedCoverage": "CLEAN",
                "boundedVisualComprehensibility": "CLEAN",
                "scope": "Whole new card" if path.name == "儀.md" else "Changed passage in complete article context only",
            } for path in FILES
        },
        "changedReusedPassageAssignments": [
            {"article": str(path.relative_to(R)), "image": "n1-068-" + image + ".png"}
            for path, image in zip(FILES[1:], [
                "word1-06", "word2-07", "word3-07", "word4-07",
                "component1-16", "component2-20", "component3-30", "component4-19",
            ])
        ],
        "originalFinding": {
            "status": "resolved", "originalSeverity": "Minor", "facet": "scoped coverage",
            "claim": "Formal suffix attachment/humble scope was implicit.",
            "resolution": "Textually resolved at80f5f424; now visible in kanji19: self/own-side, humble nuance, 私儀わたくしぎ, formal-written restriction. No regression.",
            "evidence": "Original textual reports and confirmations retained; both dependent visual reports confirm actual revised note pixels.",
        },
        "observations": [
            "All eight assigned changed reused paragraphs/backlinks and revised 私儀 note are visible/readable in the bounded packet.",
            "Four production font rows render15characters/fourwords without blank/replacement boxes. 儀 versus義 left亻, differing億優倍 right halves and 人/亻/亍/弋/彳/礻 identifiable. Textbook wraps 礻 without losing it.",
            "Actual On optionsヨウ/ギ/ジュ/ヘイ; correctギ feedback. Meaning optionschicken/chrysanthemum/crane(bird)/ceremony;formalconduct, correct last. Not authored億優倍 native presentation or whole-pool certification.",
            "Sideways reading tables clip left reading-column edges at captured offset; explicit scroll hint and complementary views. Not demonstrated inaccessible content or simultaneous whole-table certification.",
            "15numbered generated-reference strokes injected; practice/noSRS trace then recallmiss/Again persistence per fixture. No MLKit or human handwriting certification.",
            "Runtime assertions supplied: production ContentSyncONCE1080kanji5037words100N1/problems0/versionddef65b637fe2f85/epoch1;16directedreciprocalroutes/SystemBack/offline/N1selection/meaning/soleOnGood/noKunLog. Meaning feedback exits Back before Next, not a new persisted meaning grade.",
        ],
        "reportQualifications": [
            "Reviewers have no Git tools; supplied SHA/signature/unchanged-teaching claims are not independently reviewer-verified. Coordinator freeze/diff/hash checks provide that provenance.",
            "Claude calls a heavier Textbook component appearance a fallback face; only visible style difference is adopted. Neither model nor coordinator identifies the actual font face.",
            "Reviewer no-defect verdicts apply to bounded visual/textual scope, not native-language certification or exhaustive device acceptance.",
        ],
        "optional": [
            {"status": "optional", "source": "Claude", "claim": "'In this suffix use' could be clearer than 'this suffix'.",
             "decision": "No actionable defect; existing full note explicitly states typical attachment/humble/formal scope. Do not expand teaching just for polish."}
        ],
        "payloadAccounting": {
            "archivedSourceCaptures": 127, "assignedSourceCaptures": 20,
            "claudePayloads": 20, "gptPayloads": 20, "totalReturnedPayloads": 40,
            "sourceDimensions": [1080, 2400], "returnedDimensions": [900, 2000],
            "actualImagePaths": freeze["images"],
            "limit": "40payloads are two model views of the same20captures, not40independent scenes.",
        },
        "modelContributionComparison": {
            "matchedScope": "Same snapshot/all9boundedarticlefacets/20identicalimages/completefixtureandreceipts; dependent confirmations.",
            "shared": "No new actionable defect; glyphs, eight reused passages, suffix note and actual question/feedback scope accepted with viewport/phone limits.",
            "uniqueVerifiedClaudeDefects": [], "uniqueVerifiedGPTDefects": [],
            "limit": "No manufactured finding quota or general model ranking; initial reviews remain the two-family independent evidence.",
        },
        "inheritedEvidence": {
            "textual": "batch-068-reconciliation.json / execution441, unchanged",
            "android": "execution-442.json freshRealContentTest3+RareHanTest1, not rerun",
            "native": "execution-444.json bothterminal0/no skips272.859s, not rerun",
            "historicalProcessException": "441Claude13ms two-text-call overlap remains with exact original report/audit and one-call original-session repair. This445execution is entirely serial; no historical relabeling.",
            "historicalFailures": "Permission denials and HOST OOMs retained. Qualified HOST-only2GiBinit NEVER nativebuilds.",
        },
        "reviews": reviews, "checks": checks, "boundedIndependentVisualConfirmation": True,
        "runtimeAccepted": False, "runtimePublished": False, "limits": limits, "nextAction": NEXT,
    }
    save(V / "batch-068-visual-reconciliation.json", reconciliation)
    start = load(LOG / "execution-445-start.json")
    result = {
        "schemaVersion": 1, "execution": 445, "checkpoint": 445, "batch": "068",
        "status": reconciliation["status"], "startingHead": HEAD,
        "reviewedTeachingSnapshot": TEACHING, "authorization": start["authorization"],
        "scope": start["scope"], "reviews": reviews,
        "reconciliation": r"docs\n1-reviews\batch-068-visual-reconciliation.json",
        "reconciliationSha256": sha(V / "batch-068-visual-reconciliation.json"),
        "boundedIndependentVisualConfirmation": True, "allReviewerProcessesSerialAndExited": True,
        "allInternalCallsSerial": True, "allOriginalReportsAndTeachingUnmodified": True,
        "runtimeEditsMade": False, "nativeOrAndroidRerun": False, "publicationAttempted": False,
        "runtimePublished": False, "publishedAdditions": 94, "remainingAdditions": 1134,
        "phoneEvidence": False, "wholeProjectComplete": False, "nextAction": NEXT,
        "blocker": None, "limits": limits, "checks": checks, "recordedAt": now(),
        "coordinatorDirectImageChecks": ["n1-068-font-pairs.png", "n1-068-kanji-11.png", "n1-068-kanji-19.png"],
        "diagnostics": [
            "Initial whole-request PowerShell projection command had a syntax error before executing; corrected read acquired complete request and parsed checkpoint.",
            "A first generic checkpoint projection returned too much historical output; narrowed to active final444 ranges/live fields.",
            "Issue file has129lines; attempted161start was invalid, recovered missing123-129 directly. No authorization omitted.",
        ],
    }
    save(R / r"docs\n1-sources\execution-445.json", result)
    batch_path = R / r"docs\n1-sources\batch-068-progress.json"
    batch = load(batch_path)
    batch.update(status=result["status"], nextAction=NEXT, limits=limits)
    batch["nativeVisualCheckpoint"] = {
        "execution": 445, "record": "execution-445.json",
        "reconciliation": "../n1-reviews/batch-068-visual-reconciliation.json",
        "boundedIndependentVisualConfirmation": True, "allInternalCallsSerial": True,
        "allReviewerProcessesSerialAndExited": True, "runtimePublished": False, "limits": limits,
    }
    save(batch_path, batch)
    receipts = F / "visual-execution-receipts"
    receipts.mkdir()
    for source in [Path(__file__), LOG / "execution-445-start.json"] + [
        C / f"batch-068-visual-{family}-process.json" for family in SESSIONS
    ]:
        shutil.copyfile(source, receipts / source.name)
    print("Bounded visual closure written;40actual returned PNGs; no runtime edit/publication.")


def checkpoint():
    result = load(R / r"docs\n1-sources\execution-445.json")
    assert sha(R / result["reconciliation"]) == result["reconciliationSha256"]
    signed = git("rev-parse", "HEAD")
    assert signed != HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    before = load(LOG / "execution-445-before-progress.json")
    p = load(C / "progress.json")
    assert p["checkpoint"] == 444 and p["batch"] == "068"
    summary = {
        "execution": 445, "checkpoint": 445, "batch": "068", "savedCommit": signed, "signature": "G",
        "record": r"docs\n1-sources\execution-445.json",
        "recordSha256": sha(R / r"docs\n1-sources\execution-445.json"), "status": "continue",
        "boundedIndependentVisualConfirmation": True, "allReviewerProcessesSerialAndExited": True,
        "allInternalCallsSerial": True, "runtimePublished": False,
        "allOriginalHistoricalRootKeysPreservedExactly": True, "nextAction": NEXT,
    }
    p.update(checkpoint=445, status="continue", stage="batch-068-bounded-visual-confirmation-closed-awaiting-integration",
             nextAction=NEXT, blocker=None)
    p["execution445StartingState"]["status"] = "signed-bounded-visual-checkpoint-complete"
    p["batch068VisualConfirmationCheckpoint"] = dict(summary)
    p["execution445CoordinatorCheckpoint"] = dict(summary)
    for key in before.keys() - {"checkpoint", "status", "stage", "nextAction", "blocker"}:
        assert p[key] == before[key], key
    save(C / "progress.json", p)
    save(LOG / "execution-445-final-checkpoint.json", summary)
    body = (
        f"Batch 068 (儀) bounded visual checkpoint **445** saved locally in normally signed `{signed}`; "
        "**not pushed or counted as delivered**.\n\n"
        "The original Claude Opus 5.5 and GPT-6.1 Sol sessions ran serially and exited. Each made "
        "41 strictly serial view calls: complete nine teaching files, own original/textual reports, "
        "696-line native fixture/log/route and the same **20/127 native captures**. All forty actual "
        "900×2000 returned image payloads are archived separately from 1080×2400 sources. Both "
        "confirmations cover all eight changed reused passages, revised 私儀 note, four font rows, "
        "sole ギ question/feedback, actual meaning options and drawing trace/recall miss. No actionable "
        "teaching/rendering defect established; no teaching/app changes. Historical textual-confirmation "
        "overlap and its repair remain preserved, not reclassified.\n\n"
        "Validator: zero errors; regenerated manifest unchanged, version `ddef65b637fe2f85`, 8,331 runtime "
        "files. Original local budgets pass (8,353 entries; 30,123,317 compressed / 44,329,433 inflated / "
        "44,061,095 retained bytes). Passed native 444 and Android 442 checks inherited without rerun. "
        "Captured horizontal-table clipping has a visible scroll hint; no fallback-face identity, MLKit, "
        "human recall, physical-phone or all-127-image acceptance is claimed. Complete reports and "
        "scope/limits: `docs/n1-sources/execution-445.json` and "
        "`docs/n1-reviews/batch-068-visual-reconciliation.json`.\n\n"
        "**94/1,228 additions published; 1,134 remain.** Next bounded checkpoint: fresh latest-main "
        "nonrewriting integration/combined validation, normal signing/owner fast-forward push, green CI "
        "and exact immutable public ZIP/runtime-hash/budget verification before counting 068 delivered "
        "or starting 069. Compatible Android `f9b59a2`+ required; physical-phone/general-release/whole-set "
        "acceptance outstanding. Full control history preserved; `progress.json` is `continue` at445."
    )
    (C / "execution-445-issue-body.txt").write_text(body + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


def issue_receipt():
    response = load(C / "execution-445-issue-api.json")
    body = (C / "execution-445-issue-body.txt").read_text(encoding="utf-8")
    assert response["user"]["login"] == "stop-cran"
    assert response["body"].replace("\r\n", "\n").rstrip("\n") == body.replace("\r\n", "\n").rstrip("\n")
    p = load(C / "progress.json")
    assert p["checkpoint"] == 445 and p["status"] == "continue"
    assert git("rev-parse", "HEAD") == p["execution445CoordinatorCheckpoint"]["savedCommit"]
    assert not git("status", "--porcelain") and git("log", "-1", "--format=%G?") == "G"
    issue = {
        "url": response["html_url"], "author": "stop-cran", "commentId": response["id"],
        "bodyVerified": True, "bodyComparison": "Exact after CRLF/final-newline normalization only.",
    }
    p["batch068VisualIssueReceipt"] = issue
    for key in ("batch068VisualConfirmationCheckpoint", "execution445CoordinatorCheckpoint"):
        p[key]["issueUpdate"] = issue["url"]
        p[key]["ownerAuthorAndBodyVerified"] = True
    before = load(LOG / "execution-445-before-progress.json")
    for key in before.keys() - {"checkpoint", "status", "stage", "nextAction", "blocker"}:
        assert p[key] == before[key], key
    save(C / "progress.json", p)
    save(LOG / "execution-445-final-verification.json", {
        "checkpoint": 445, "status": "continue", "savedCommit": git("rev-parse", "HEAD"),
        "signature": "G", "worktreeClean": True, "allPriorHistoryPreserved": True,
        "issue": issue, "runtimePublished": False, "publishedAdditions": 94, "remainingAdditions": 1134,
    })
    print(json.dumps(issue, indent=2))


if __name__ == "__main__":
    if sys.argv[1] == "prepare":
        prepare()
    elif sys.argv[1] == "run":
        run(sys.argv[2])
    elif sys.argv[1] == "archive":
        archive(sys.argv[2])
    elif sys.argv[1] == "record":
        record()
    elif sys.argv[1] == "checkpoint":
        checkpoint()
    elif sys.argv[1] == "issue-receipt":
        issue_receipt()

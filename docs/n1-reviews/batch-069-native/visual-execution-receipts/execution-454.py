import base64
import gzip
import hashlib
import json
import os
from pathlib import Path
import shutil
import struct
import subprocess
import sys
from datetime import datetime, timezone

C = Path(__file__).parent
R = C.parent / "learning-japanese"
V = R / "docs" / "n1-reviews"
F = V / "batch-069-native"
L = C / r"logs\23e04e4c-900c-4888-8da3-113d52b9d318"
HEAD = "41390d7019b58dd8be521388865164d706b2b34d"
TEACHING = "f5061bcdf101f8eba5729b21f222b57821df9a38"
SESSIONS = {
    "claude": ("claude-opus-5.5", "78cf2390-1187-4593-ba60-ebe562f1a49a"),
    "gpt": ("gpt-6.1-sol", "e683a0f6-66de-4049-ae70-eb508e0866ee"),
}
FILES = [R / "kanji" / "儒.md", R / "words" / "儒教.md", R / "kanji" / "教.md"]
IMAGES = [
    "font-pairs", "kanji-01", "kanji-11", "word1-02", "word1-07",
    "word1-new-kanji-backlink", "word1-legacy-backlink", "component1-19",
    "curated-On-question", "curated-On-feedback", "meaning-question", "meaning-feedback",
    "drawing-trace", "drawing-feedback", "drawing-recall-feedback", "selection",
]
NEXT = (
    "SAME069 signed bounded visual checkpoint454: original Claude78cf2390 and GPTe683a0f6 "
    "dependent visual confirmations complete; both processes exited serially, each28single "
    "view calls/16assignedPNG/complete3teachingfiles/529line retry1fixture/ownoriginalreport/"
    "terminal-log/route. All32actual returned900x2000payloads archived separately from "
    "1080x2400sources;16/46successfulcapture scope, not full-PNG acceptance. Read "
    "docs\\n1-sources\\execution-454.json and "
    "docs\\n1-reviews\\batch-069-visual-reconciliation.json. New儒/儒教 and exact changed教 "
    "backlink covered; unchanged教body rendering/context, NOT renewed full linguistic review. "
    "No actionable teaching/rendering defect established; no teaching/app changes. "
    "Inherited450textual,451freshAndroid3+1 and453native2terminal0/158.188s retained without "
    "rerun. All454reviewer calls serial; original reports/failedattempts/history preserved. "
    "Horizontal clipping with sideways hint does not establish inaccessible content. "
    "Unseen儒source-note pixels/fallbackface/MLKit/humanrecall/physicalphone/generalrelease/"
    "whole-set remain unverified; optional dense drawing numbers are existing app polish, "
    "not an established content defect. NEXT BOUNDED CHECKPOINT: freshfetchlatestorigin/main, "
    "nonrewritingintegration as needed, actualcombined source-membership/baseline/reading/"
    "link/font/stroke/Python/vocab/validator/freshmanifest/original18000entries42MiBcompressed"
    "80MiBinflated56MiBretainedbudgets, normal signing/ownerfastforward/publicSHA/"
    "terminalgreenCI/EVERYimmutablepublicZIP runtimehash/budgets/ownerissue60 BEFOREdelivery "
    "or070. Preserve precise permissiondenials/signingwait and yield; no workaround/second"
    "runner/concurrentheavywork/supervisorchanges. HOST-only heapinit NEVER nativebuilds. "
    "Published95/1228,remaining1133/latest068f9e0511f; local069 NOTdelivered. Compatible "
    "Androidf9b59a2+ required; wholeproject incomplete."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    assert load(path) == json.loads(json.dumps(value))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def git(*args):
    return subprocess.check_output(["git", "--no-pager", "-C", str(R), *args], encoding="utf-8").strip()


def verify_freeze():
    freeze = load(C / "batch-069-visual-freeze.json")
    assert git("rev-parse", "HEAD") == HEAD
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    for path, digest in freeze["resourceHashes"].items():
        assert sha(Path(path)) == digest, path
    return freeze


def prepare():
    assert git("rev-parse", "HEAD") == HEAD and not git("status", "--porcelain")
    request = L / "request.txt"
    text = request.read_text(encoding="utf-8-sig")
    embedded = json.loads(text.split("Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    p = load(C / "progress.json")
    assert p["checkpoint"] == embedded["checkpoint"] == 453 and p["batch"] == "069"
    backup = L / "execution-454-before-progress.json"
    assert not backup.exists()
    backup.write_bytes((C / "progress.json").read_bytes())
    start = {
        "execution": 454, "batch": "069", "startingHead": HEAD, "recordedAt": now(),
        "scope": "SAME069 two serial original-session dependent bounded visual confirmations, exact payload/range/process archival, reconciliation and normally signed local evidence checkpoint only. No native/Android rerun, publication,070 or second runner.",
        "authorization": {
            "requestSha256": sha(request), "bytes": request.stat().st_size,
            "characters": len(text), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request acquired and complete embedded checkpoint parsed; operative contract, final453 checkpoint and complete approved issue inspected directly. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "originMainFreshFetch": git("rev-parse", "origin/main"),
        "status": "dependent-visual-confirmation-preparing",
    }
    save(L / "execution-454-start.json", start)
    p["execution454StartingState"] = start
    p.update(stage="batch-069-dependent-visual-confirmation-preparing", nextAction=start["scope"])
    save(C / "progress.json", p)
    index = F / "execution-453-artifact-index.json"
    for row in load(index)["artifacts"]:
        assert sha(R / row["path"]) == row["sha256"]
        assert (R / row["path"]).stat().st_size == row["bytes"]
        if "rawGzipPath" in row:
            assert sha(R / row["rawGzipPath"]) == row["rawGzipSha256"]
            original = gzip.decompress((R / row["rawGzipPath"]).read_bytes())
            assert hashlib.sha256(original).hexdigest() == row["originalSha256"]
    resources = FILES + [F / ("n1-069-" + name + ".png") for name in IMAGES]
    resources += [F / name for name in ("N1Batch069NativeRetry1Test.kt", "instrumentation.txt", "n1-069-article-route.json")]
    resources += [C / "batch-069-visual-task.txt", index]
    resources += [V / f"batch-069-initial-{family}.md" for family in SESSIONS]
    freeze = {
        "execution": 454, "batch": "069", "evidenceHead": HEAD, "teachingSnapshot": TEACHING,
        "images": [str(F / ("n1-069-" + name + ".png")) for name in IMAGES],
        "assignedCaptures": 16, "archivedSuccessfulCaptures": 46,
        "fixtureRanges": [[1, 120], [121, 240], [241, 360], [361, 480], [481, 529]],
        "resourceHashes": {str(path): sha(path) for path in resources},
    }
    assert len((F / "N1Batch069NativeRetry1Test.kt").read_text(encoding="utf-8").splitlines()) == 529
    save(C / "batch-069-visual-freeze.json", freeze)
    print("Starting scope saved; exact native evidence verified; bounded16image packet frozen.")


def run(family):
    verify_freeze()
    if family == "gpt":
        prior = load(V / "batch-069-visual-claude-execution.json")
        assert prior["exitCode"] == 0 and prior["processAndCoverageAccepted"]
    model, session = SESSIONS[family]
    prefix = "batch-069-visual-" + family
    raw = C / f"{prefix}.jsonl"
    assert not raw.exists(), "Never overwrite original execution"
    command = [
        shutil.which("copilot"), "-C", str(R), "--add-dir", str(C),
        "--model", model, "--session-id", session, "--no-ask-user",
        "--allow-all-tools", "--disable-builtin-mcps", "--available-tools=view",
        "--output-format", "json", "--log-dir", str(C / "review-logs" / prefix),
        "--usage-output-file", str(C / f"{prefix}-usage.json"),
        "-p", "Read the ENTIRE shared bounded dependent visual task at "
        + str(C / "batch-069-visual-task.txt") + ". YOUR original initial report is "
        + str(V / f"batch-069-initial-{family}.md")
        + ". Execute task with exactly ONE view tool call per response, WAIT before next. Never parallel tools.",
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
    prefix = "batch-069-visual-" + family
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
    required = FILES + [C / "batch-069-visual-task.txt", V / f"batch-069-initial-{family}.md"]
    required += [F / name for name in ("N1Batch069NativeRetry1Test.kt", "instrumentation.txt", "n1-069-article-route.json")]
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
    allowed = {str(path) for path in required} | set(freeze["images"])
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
        "limits": "Dependent original-session confirmation;16/46successful captures. Exact bytes/ranges establish access, not comprehension. No reviewer native execution, fresh upstream dictionary retrieval, physical-phone or final publication acceptance.",
    }
    save(V / f"{prefix}-execution.json", record)
    print(json.dumps({key: record[key] for key in ("actualModels", "processAndCoverageAccepted", "imagePayloadsVerified",
                                                   "missingRequiredText", "observedToolOverlaps", "multiToolResponses")}))
    assert accepted


def record():
    freeze = verify_freeze()
    reviews = {}
    for family, (model, session) in SESSIONS.items():
        path = V / f"batch-069-visual-{family}-execution.json"
        item = load(path)
        assert item["processAndCoverageAccepted"] and item["exitCode"] == 0
        assert item["actualModels"] == [model] == [item["usage"]["currentModel"]]
        assert item["sessionId"] == session and not item["unfinishedTools"]
        assert not item["observedToolOverlaps"] and not item["multiToolResponses"]
        assert len(item["toolCalls"]) == 28 and item["imagePayloadsVerified"] == 16
        assert sha(V / f"batch-069-visual-{family}.md") == item["reportSha256"]
        assert sha(Path(item["rawExecutionLocation"])) == item["rawExecutionSha256"]
        for row in item["toolCalls"]:
            assert row["name"] == "view" and row["success"]
            if "imagePayload" in row:
                payload = row["imagePayload"]
                assert sha(R / payload["returnedPayloadCopy"]) == payload["sha256"]
                assert sha(Path(row["arguments"]["path"])) == payload["sourceSha256"]
                assert payload["sourceDimensions"] == [1080, 2400]
                assert payload["returnedDimensions"] == [900, 2000]
            else:
                assert row["exactRequestedTextContainedInResult"]
        reviews[family] = {
            "report": str((V / f"batch-069-visual-{family}.md").relative_to(R)),
            "reportSha256": item["reportSha256"],
            "execution": str(path.relative_to(R)), "executionSha256": sha(path),
            "actualModel": model, "sessionId": session,
            "startedAt": item["startedAt"], "completedAt": item["completedAt"],
            "exitCode": 0, "toolCalls": 28, "verifiedReturnedImages": 16,
            "allInternalCallsSerial": True, "processAndCoverageAccepted": True,
        }
    assert datetime.fromisoformat(reviews["claude"]["completedAt"]) < datetime.fromisoformat(reviews["gpt"]["startedAt"])
    checks = {}
    for name in ("validate", "manifest", "budget"):
        source = C / f"execution-454-{name}.txt"
        target = V / f"batch-069-visual-{name}-execution-454.txt"
        assert not target.exists()
        shutil.copyfile(source, target)
        checks[name] = {"path": str(target.relative_to(R)), "sha256": sha(target)}
    for name in ("task", "help-execution-454", "models-execution-454"):
        source = C / f"batch-069-visual-{name}.txt"
        target = V / source.name
        assert not target.exists()
        target.write_text(source.read_text(encoding="utf-8-sig").rstrip() + "\n", encoding="utf-8")
    save(V / "batch-069-visual-freeze.json", freeze)
    limits = (
        "Dependent16/46successfulcapture confirmation, not all screenshots/viewports or full easier-deck review. "
        "Exact bytes/ranges establish access, not comprehension. Source1080x2400 returned900x2000, not physical "
        "viewing size. Sideways-scroll hint/complementary offsets do not certify every gesture. 儒 final source-note "
        "line is not fully visible in assigned images. No fallback-face identity/every-phone readability/MLKit/"
        "human recall/negative geometry/successful model download/native-language certification. Original "
        "frozen-XML/public-source retrieval limitations retained; no fresh dictionary fetch or reviewer native "
        "execution. Physical-phone/general-release/current-main/whole-set/publication acceptance outstanding; "
        "Androidf9b59a2+ required. Original native failures and all historical keys preserved."
    )
    reconciliation = {
        "schemaVersion": 1, "execution": 454, "batch": "069",
        "status": "bounded-visual-confirmation-closed-awaiting-integration",
        "evidenceHead": HEAD, "reviewedTeachingSnapshot": TEACHING,
        "dependentNotBlind": True, "models": [item[0] for item in SESSIONS.values()],
        "scope": "Whole new 儒 and 儒教 plus only added 教 Common words backlink. Complete3teachingfiles read; unchanged教 body rendering/context, not renewed full linguistic review. Same16assigned native screenshots per model; own complete original report, complete529line retry1fixture/log/route.",
        "allReviewerProcessesSerialAndExited": True, "allInternalCallsSerial": True,
        "allImageCallsSerial": True, "findings": [],
        "verdicts": {
            str(path.relative_to(R)): {
                "correctness": "CLEAN", "scopedCoverage": "CLEAN",
                "boundedVisualComprehensibility": "CLEAN",
                "scope": "Only added 儒教 backlink, in complete rendering/context" if path.name == "教.md" else "Whole new teaching file",
            } for path in FILES
        },
        "changedReusedPassageAssignments": [{"article": "kanji\\教.md", "image": "n1-069-component1-19.png"}],
        "observations": [
            "No new actionable defect. Both new teaching files and exact changed 教 backlink remain correct/scoped/readable within assigned viewports and inherited lexical limits.",
            "Four production rows render14characters/儒教 without blank/replacement boxes. 儒 versus需 left亻, differing儀僧優 right shapes, 人/亻 and 教/攴/攵/子/考/校/木 identifiable. Some wholeword samples wrap without losing a character.",
            "Actual On optionsジュ/ソウ/ジョウ/ギ, correctジュ feedback. Actual meaning choicesceremony;formalconduct/frugal;thrifty/Confucian;Confucianscholar/Buddhistmonk;priest. Not the authored儀僧優 trio or whole-pool certification.",
            "Reading tables clip opposite edges at selected horizontal offsets, with explicit scroll hint and complementary views. No established inaccessible content; 儒 final source-note line remains unseen in full.",
            "Supplied runtime: one productionContentSync1081kanji5038words101N1/problems0/version83ed94552dd1a9ce/epoch1; fourdirectedreciprocalroutes/SystemBack/offline/N1selection/meaning/soleOnGood/noKunLog. Meaning feedback exits Back before Next, not a new persisted meaning grade.",
            "16numbered generated-reference strokes injected; practice/noSRS trace, model-unavailable geometry feedback, recallmiss/Again persistence per fixture. No MLKit or human handwriting certification.",
        ],
        "reportQualifications": [
            "Reviewers have no Git tools; coordinator freeze/diff/hash checks, not reviewer assertions, establish SHAs and unchanged teaching.",
            "Claude calls a heavier component appearance a fallback face; only visible style difference is adopted. Neither model nor coordinator identifies actual font face.",
            "Claude notes component1-19 selector names 教える rather than the changed backlink; actual pixels include full 儒教 line. File naming/selector alone was not treated as visibility.",
            "Two models viewing16samecaptures yields32payloads, not32independent scenes. Byte access is not linguistic comprehension or native-speaker certification.",
        ],
        "optional": [
            {"status": "optional", "source": "Claude", "claim": "Dense stroke numbers overlap in the small Correct strokes panel.",
             "decision": "Existing app presentation polish; no blank/misleading content or consequential teaching defect established. No unrelated app change authorized or made."},
            {"status": "optional", "source": "Claude, carried from original review",
             "claim": "儒者 or 儒学者 could illustrate the scholar half of the title.",
             "decision": "Original optional disposition retained: sole ジュ already has useful exact linked 儒教, and qualified learned-person note supplies scope. Not a missing reading or necessary support addition."},
        ],
        "modelContributionComparison": {
            "matchedScope": "Same snapshot/all3boundedarticlefacets/16identicalimages/complete529linefixtureandreceipts; dependent confirmations.",
            "shared": "No actionable defect; glyphs, new teaching and changed backlink/actual questions accepted within shared viewport and phone limits.",
            "uniqueVerifiedClaudeDefects": [], "uniqueVerifiedGPTDefects": [],
            "limit": "Compared optional and limits too; no finding quota or general model ranking. Initial reviews remain independent evidence.",
        },
        "payloadAccounting": {
            "archivedSuccessfulSourceCaptures": 46, "assignedSourceCaptures": 16,
            "claudePayloads": 16, "gptPayloads": 16, "totalReturnedPayloads": 32,
            "sourceDimensions": [1080, 2400], "returnedDimensions": [900, 2000],
            "actualImagePaths": freeze["images"],
        },
        "inheritedEvidence": {
            "textual": "batch-069-reconciliation.json / execution450, unchanged",
            "android": "execution-451.json freshRealContentTest3+RareHanTest1, not rerun",
            "native": "execution-453.json bothterminal0/no skips158.188s, not rerun",
            "historicalFailures": "Original native attempt1timeout and attempt2ownershipabort preserved; retry1 adds only destination await. Historical permission denials/HOST OOMs retained; HOST-only heapinit NEVER nativebuilds.",
        },
        "reviews": reviews, "checks": checks, "boundedIndependentVisualConfirmation": True,
        "runtimeAccepted": False, "runtimePublished": False, "limits": limits, "nextAction": NEXT,
    }
    save(V / "batch-069-visual-reconciliation.json", reconciliation)
    start = load(L / "execution-454-start.json")
    result = {
        "schemaVersion": 1, "execution": 454, "checkpoint": 454, "batch": "069",
        "status": reconciliation["status"], "startingHead": HEAD,
        "reviewedTeachingSnapshot": TEACHING, "authorization": start["authorization"],
        "scope": start["scope"], "originMainFreshFetch": start["originMainFreshFetch"],
        "reviews": reviews, "reconciliation": r"docs\n1-reviews\batch-069-visual-reconciliation.json",
        "reconciliationSha256": sha(V / "batch-069-visual-reconciliation.json"),
        "boundedIndependentVisualConfirmation": True, "allReviewerProcessesSerialAndExited": True,
        "allInternalCallsSerial": True, "allOriginalReportsAndTeachingUnmodified": True,
        "runtimeEditsMade": False, "nativeOrAndroidRerun": False, "publicationAttempted": False,
        "runtimePublished": False, "publishedAdditions": 95, "remainingAdditions": 1133,
        "phoneEvidence": False, "wholeProjectComplete": False, "nextAction": NEXT,
        "blocker": None, "limits": limits, "checks": checks, "recordedAt": now(),
        "coordinatorDirectImageChecks": ["n1-069-font-pairs.png", "n1-069-kanji-11.png", "n1-069-component1-19.png", "n1-069-word1-07.png"],
        "diagnostics": [
            "First broad request projection exceeded tool-output limit and hit Windows cp1252 UnicodeEncodeError; complete request had been loaded/parsed. Narrowed UTF-8 output recovered operative scalar/final checkpoint.",
            "Initial guessed native-index path under docs/n1-sources was absent; glob located actual docs/n1-reviews/batch-069-native path. No missing evidence waived.",
            "Initial --help config and config --help captures showed command help, not catalog; actual copilot help config returned model IDs and is the archived catalog. No model inferred from failed probes.",
        ],
    }
    save(R / r"docs\n1-sources\execution-454.json", result)
    batch_path = R / r"docs\n1-sources\batch-069-progress.json"
    batch = load(batch_path)
    batch.update(status=result["status"], nextAction=NEXT, limits=limits)
    batch["nativeVisualCheckpoint"] = {
        "execution": 454, "record": "execution-454.json",
        "reconciliation": "../n1-reviews/batch-069-visual-reconciliation.json",
        "boundedIndependentVisualConfirmation": True, "allInternalCallsSerial": True,
        "allReviewerProcessesSerialAndExited": True, "runtimePublished": False, "limits": limits,
    }
    save(batch_path, batch)
    receipts = F / "visual-execution-receipts"
    receipts.mkdir()
    for source in [Path(__file__), L / "execution-454-start.json"] + [
        C / f"batch-069-visual-{family}-process.json" for family in SESSIONS
    ]:
        shutil.copyfile(source, receipts / source.name)
    print("Bounded visual closure written;32actual returned PNGs; no runtime edit/publication.")


def checkpoint():
    result = load(R / r"docs\n1-sources\execution-454.json")
    assert sha(R / result["reconciliation"]) == result["reconciliationSha256"]
    signed = git("rev-parse", "HEAD")
    assert signed != HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    before = load(L / "execution-454-before-progress.json")
    p = load(C / "progress.json")
    assert p["checkpoint"] == 453 and p["batch"] == "069"
    summary = {
        "execution": 454, "checkpoint": 454, "batch": "069", "savedCommit": signed, "signature": "G",
        "record": r"docs\n1-sources\execution-454.json",
        "recordSha256": sha(R / r"docs\n1-sources\execution-454.json"), "status": "continue",
        "boundedIndependentVisualConfirmation": True, "allReviewerProcessesSerialAndExited": True,
        "allInternalCallsSerial": True, "runtimePublished": False,
        "publishedAdditions": 95, "remainingAdditions": 1133,
        "allOriginalHistoricalRootKeysPreservedExactly": True, "nextAction": NEXT,
    }
    p.update(checkpoint=454, status="continue", stage="batch-069-bounded-visual-confirmation-closed-awaiting-integration",
             nextAction=NEXT, blocker=None)
    p["execution454StartingState"]["status"] = "signed-bounded-visual-checkpoint-complete"
    p["batch069VisualConfirmationCheckpoint"] = dict(summary)
    p["execution454CoordinatorCheckpoint"] = dict(summary)
    for key in before.keys() - {"checkpoint", "status", "stage", "nextAction", "blocker"}:
        assert p[key] == before[key], key
    save(C / "progress.json", p)
    save(L / "execution-454-final-checkpoint.json", summary)
    body = (
        f"Batch 069 (儒/儒教) bounded visual checkpoint **454** saved locally in normally signed `{signed}`; "
        "**not pushed or counted as delivered**.\n\n"
        "Original Claude Opus 5.5 and GPT-6.1 Sol sessions ran serially and exited. Each made "
        "28 strictly serial view calls: complete three teaching files, own original report, "
        "529-line retry1 native fixture/log/route and the same **16/46 successful native captures**. "
        "All 32 actual 900×2000 returned image payloads are archived separately from 1080×2400 sources. "
        "Both confirmations cover new 儒/儒教 and only 教's added 儒教 backlink; unchanged 教 is "
        "rendering/context, not renewed full linguistic review. No actionable teaching/rendering "
        "defect established; no teaching/app changes. Original reports, failed native attempts "
        "and all checkpoint history remain intact.\n\n"
        "Validator: zero errors; regenerated manifest unchanged, version `83ed94552dd1a9ce`, "
        "8,334 runtime files. Original local budgets pass: 8,356 entries; 30,127,683 compressed / "
        "44,338,064 inflated / 44,069,726 retained bytes. Passed native 453 and Android 451 "
        "checks inherited without rerun. Horizontal-table clipping has a visible scroll hint; "
        "no inaccessible content established. Final 儒 source-note pixels are incompletely visible; "
        "no fallback-face identity, MLKit, human recall, physical-phone or all-46-image acceptance "
        "claimed. Dense reference stroke numbers and extra scholar examples remain nonblocking "
        "polish/expansion, not content defects. Reports and dispositions: "
        "`docs/n1-sources/execution-454.json` and "
        "`docs/n1-reviews/batch-069-visual-reconciliation.json`.\n\n"
        "**95/1,228 additions published; 1,133 remain.** Next bounded checkpoint: fresh latest-main "
        "nonrewriting integration/combined validation, normal signing/owner fast-forward push, green CI "
        "and exact immutable public ZIP/runtime-hash/budget verification before counting 069 delivered "
        "or starting 070. Compatible Android `f9b59a2`+ required; physical-phone/general-release/whole-set "
        "acceptance outstanding. Full control history preserved; `progress.json` is `continue` at454."
    )
    (C / "execution-454-issue-body.txt").write_text(body + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


def issue_receipt():
    response = load(C / "execution-454-issue-api.json")
    body = (C / "execution-454-issue-body.txt").read_text(encoding="utf-8")
    assert response["user"]["login"] == "stop-cran"
    assert response["body"].replace("\r\n", "\n").rstrip("\n") == body.replace("\r\n", "\n").rstrip("\n")
    p = load(C / "progress.json")
    assert p["checkpoint"] == 454 and p["status"] == "continue"
    assert git("rev-parse", "HEAD") == p["execution454CoordinatorCheckpoint"]["savedCommit"]
    assert not git("status", "--porcelain") and git("log", "-1", "--format=%G?") == "G"
    issue = {
        "url": response["html_url"], "author": "stop-cran", "commentId": response["id"],
        "bodyVerified": True, "bodyComparison": "Exact after CRLF/final-newline normalization only.",
    }
    p["batch069VisualIssueReceipt"] = issue
    for key in ("batch069VisualConfirmationCheckpoint", "execution454CoordinatorCheckpoint"):
        p[key]["issueUpdate"] = issue["url"]
        p[key]["ownerAuthorAndBodyVerified"] = True
    before = load(L / "execution-454-before-progress.json")
    for key in before.keys() - {"checkpoint", "status", "stage", "nextAction", "blocker"}:
        assert p[key] == before[key], key
    save(C / "progress.json", p)
    save(L / "execution-454-final-verification.json", {
        "checkpoint": 454, "status": "continue", "savedCommit": git("rev-parse", "HEAD"),
        "signature": "G", "worktreeClean": True, "allPriorHistoryPreserved": True,
        "issue": issue, "runtimePublished": False, "publishedAdditions": 95, "remainingAdditions": 1133,
    })
    print(json.dumps(issue, indent=2))


if __name__ == "__main__":
    if sys.argv[1] == "prepare":
        prepare()
    elif sys.argv[1] == "run":
        run(sys.argv[2])
    elif sys.argv[1] == "record":
        record()
    elif sys.argv[1] == "checkpoint":
        checkpoint()
    elif sys.argv[1] == "issue-receipt":
        issue_receipt()

import base64
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
F = V / "batch-070-native" / "attempt-1"
L = C / "logs" / "db68b74a-716d-445e-96fe-17bc698d6214"
HEAD = "f05c73d26f1091e03cfcbaaba33d7dab41eca461"
TEACHING = "174ee1d82ddf8bd67dd72c14b411adf3d82e4aef"
SESSIONS = {
    "claude": ("claude-opus-5.5", "5ace375a-4747-4cb8-be76-486c1a778e45"),
    "gpt": ("gpt-6.1-sol", "5424a79d-80be-4124-ba8b-fb09e2be95c2"),
}
FILES = [R / "kanji" / "償.md", R / "words" / "償う.md",
         R / "words" / "補償.md", R / "kanji" / "補.md", R / "words" / "補う.md"]
FIXTURE = V / "batch-070-native" / "N1Batch070NativeTest.kt"
IMAGES = [
    "font-pairs", "kanji-01", "kanji-11", "kanji-23",
    "word1-04", "word1-09", "word1-new-kanji-backlink",
    "word2-04", "word2-09", "word2-new-kanji-backlink", "word2-legacy-backlink",
    "component1-19", "comparison-11",
    "curated-On-question", "curated-On-feedback", "curated-Kun-question", "curated-Kun-feedback",
    "meaning-question", "meaning-feedback", "drawing-trace", "drawing-feedback",
    "drawing-recall-feedback", "selection",
]
NEXT = (
    "SAME070 bounded visual checkpoint462 closed: original Claude5ace375a and GPT5424a79d "
    "dependent confirmations complete, processes exited serially; each37singleviewcalls/"
    "23assignedPNG/complete5teachingfiles/596linefixture/ownoriginalreport/terminal-log/route. "
    "All46 actual returned900x2000 payloads archived separately from1080x2400sources; "
    "23/75sourcecapture scope, not full-PNG acceptance. Read docs\\n1-sources\\execution-462.json "
    "and docs\\n1-reviews\\batch-070-visual-reconciliation.json. New償/償う/補償 and exact "
    "changed補backlink/補うcomparison covered; unchanged reused bodies rendering/context, "
    "NOT renewed full linguistic review. No actionable teaching/rendering defect established; "
    "no teaching/app changes. Inherit458textual,459freshAndroid3+1 and461native2terminal0/"
    "178.905s without rerun. Claude cannot confidently distinguish isolated衤/礻 at resized "
    "transport; GPT distinguishes them; original100nativePaintprobes and coordinator views "
    "preserved, no claim of unanimous fine-glyph certainty or fallbackface identification. "
    "Scroll-hinted table clipping not established inaccessibility. Dense drawing numbers/"
    "practice-versus-geometry wording are existing app presentation observations, not new "
    "content defects or successful MLKit/recall. NEXT BOUNDED CHECKPOINT: freshfetchlatest"
    "origin/main/nonrewritingintegration as needed; actualcombined source-membership/"
    "baseline/reading/link/font/stroke/Python/vocab/validator/freshmanifest/"
    "original18000entries42MiBcompressed80MiBinflated56MiBretainedbudgets; normal signing/"
    "ownerfastforward/publicSHA/terminalgreenCI/EVERYimmutablepublicZIP runtimehash/budgets/"
    "ownerissue60 BEFOREdelivery or071. Preserve exact permissiondenials/signingwait and "
    "yield; no workaround/secondrunner/concurrentheavywork/supervisoredits. HOST-only "
    "heapinit NEVER nativebuilds. Published96/1228,remaining1132/latest069caf2eebf; local070 "
    "NOTdelivered. CompatibleAndroidf9b59a2+ required; physicalphone/generalrelease/whole-set "
    "acceptance outstanding."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    assert load(path) == json.loads(json.dumps(data))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def git(*args):
    return subprocess.check_output(["git", "--no-pager", "-C", str(R), *args], encoding="utf-8").strip()


def verify_freeze():
    freeze = load(C / "batch-070-visual-freeze.json")
    assert git("rev-parse", "HEAD") == HEAD
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    for path, digest in freeze["resourceHashes"].items():
        assert sha(Path(path)) == digest, path
    return freeze


def prepare():
    assert git("rev-parse", "HEAD") == HEAD and not git("status", "--porcelain")
    assert git("log", "-1", "--format=%G?") == "G"
    text = (L / "request.txt").read_text(encoding="utf-8-sig")
    embedded = json.loads(text.split("Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    p = load(C / "progress.json")
    assert embedded["checkpoint"] == p["checkpoint"] == 461 and p["batch"] == "070"
    backup = L / "execution-462-before-progress.json"
    assert not backup.exists()
    shutil.copyfile(C / "progress.json", backup)
    start = {
        "execution": 462, "batch": "070", "startingHead": HEAD, "recordedAt": now(),
        "scope": "SAME070 two serial original-session dependent bounded visual confirmations, actual returned payload/range/process archival, reconciliation and normally signed local evidence checkpoint only. No Android/native rerun, publication,071 or second runner.",
        "authorization": {
            "requestSha256": sha(L / "request.txt"), "characters": len(text), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request acquired and complete embedded checkpoint parsed. Operative contract, complete approved issue and final461 checkpoint inspected directly; historical middle parsed, not freshly semantically re-reviewed.",
        },
        "originMainFreshFetch": git("rev-parse", "origin/main"),
        "status": "dependent-visual-confirmation-preparing",
    }
    save(L / "execution-462-start.json", start)
    p["execution462StartingState"] = start
    p.update(stage="batch-070-dependent-visual-confirmation-preparing", nextAction=start["scope"])
    save(C / "progress.json", p)
    index = V / "batch-070-native" / "execution-461-artifact-index.json"
    for row in load(index)["files"]:
        assert sha(R / row["path"]) == row["sha256"], row["path"]
        assert (R / row["path"]).stat().st_size == row["bytes"]
    resources = FILES + [F / ("n1-070-" + name + ".png") for name in IMAGES]
    resources += [FIXTURE, F / "instrumentation.txt", F / "n1-070-article-route.json", index]
    resources += [C / "batch-070-visual-task.txt"]
    resources += [V / f"batch-070-initial-{family}.md" for family in SESSIONS]
    assert len(FIXTURE.read_text(encoding="utf-8").splitlines()) == 596
    save(C / "batch-070-visual-freeze.json", {
        "execution": 462, "batch": "070", "evidenceHead": HEAD, "teachingSnapshot": TEACHING,
        "images": [str(F / ("n1-070-" + name + ".png")) for name in IMAGES],
        "assignedCaptures": len(IMAGES), "archivedSourceCaptures": 75,
        "fixtureRanges": [[1, 120], [121, 240], [241, 360], [361, 480], [481, 596]],
        "resourceHashes": {str(path): sha(path) for path in resources},
    })
    print("Early scope saved; exact native evidence verified; bounded23image packet frozen.")


def run(family):
    verify_freeze()
    if family == "gpt":
        prior = load(V / "batch-070-visual-claude-execution.json")
        assert prior["exitCode"] == 0 and prior["processAndCoverageAccepted"]
    model, session = SESSIONS[family]
    prefix = "batch-070-visual-" + family
    raw = C / f"{prefix}.jsonl"
    assert not raw.exists(), "Never overwrite original execution"
    command = [
        shutil.which("copilot"), "-C", str(R), "--add-dir", str(C),
        "--model", model, "--session-id", session, "--no-ask-user",
        "--allow-all-tools", "--disable-builtin-mcps", "--available-tools=view",
        "--output-format", "json", "--log-dir", str(C / "review-logs" / prefix),
        "--usage-output-file", str(C / f"{prefix}-usage.json"),
        "-p", "Read the ENTIRE shared bounded dependent visual task at "
        + str(C / "batch-070-visual-task.txt") + ". YOUR complete original initial report is "
        + str(V / f"batch-070-initial-{family}.md")
        + ". Execute task with exactly ONE view tool call per response; WAIT before next. Never parallel tools.",
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
    prefix = "batch-070-visual-" + family
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
                target = F.parent / f"visual-{family}-returned" / source.name
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
    required = FILES + [C / "batch-070-visual-task.txt", V / f"batch-070-initial-{family}.md",
                        FIXTURE, F / "instrumentation.txt", F / "n1-070-article-route.json"]
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
        "limits": "Dependent original-session confirmation;23/75source captures. Exact returned bytes/ranges establish access, not comprehension. No reviewer native execution, fresh upstream retrieval, physical-phone or final publication acceptance.",
    }
    save(V / f"{prefix}-execution.json", record)
    print(json.dumps({key: record[key] for key in ("actualModels", "processAndCoverageAccepted",
                     "imagePayloadsVerified", "missingRequiredText", "observedToolOverlaps", "multiToolResponses")}))
    assert accepted


def record():
    freeze = verify_freeze()
    reviews = {}
    for family, (model, session) in SESSIONS.items():
        path = V / f"batch-070-visual-{family}-execution.json"
        item = load(path)
        assert item["processAndCoverageAccepted"] and item["exitCode"] == 0
        assert item["actualModels"] == [model] == [item["usage"]["currentModel"]]
        assert item["sessionId"] == session and not item["unfinishedTools"]
        assert not item["observedToolOverlaps"] and not item["multiToolResponses"]
        assert len(item["toolCalls"]) == 37 and item["imagePayloadsVerified"] == 23
        assert sha(V / f"batch-070-visual-{family}.md") == item["reportSha256"]
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
            "report": str((V / f"batch-070-visual-{family}.md").relative_to(R)),
            "reportSha256": item["reportSha256"], "execution": str(path.relative_to(R)),
            "executionSha256": sha(path), "actualModel": model, "sessionId": session,
            "startedAt": item["startedAt"], "completedAt": item["completedAt"],
            "exitCode": 0, "toolCalls": len(item["toolCalls"]), "verifiedReturnedImages": 23,
            "allInternalCallsSerial": True, "processAndCoverageAccepted": True,
        }
    assert datetime.fromisoformat(reviews["claude"]["completedAt"]) < datetime.fromisoformat(reviews["gpt"]["startedAt"])
    checks = {}
    for name in ("validate", "manifest", "budget"):
        source = C / f"execution-462-{name}.txt"
        target = V / f"batch-070-visual-{name}-execution-462.txt"
        assert not target.exists()
        shutil.copyfile(source, target)
        checks[name] = {"path": str(target.relative_to(R)), "sha256": sha(target)}
    for name in ("task", "help-execution-462", "models-execution-462"):
        source = C / f"batch-070-visual-{name}.txt"
        target = V / source.name
        assert not target.exists()
        target.write_text(source.read_text(encoding="utf-8-sig").rstrip() + "\n", encoding="utf-8")
    save(V / "batch-070-visual-freeze.json", freeze)
    limits = (
        "Dependent23/75sourcecapture confirmation, not all screenshots/viewports or full easier-deck review. "
        "Returned bytes/ranges establish access, not comprehension. Source1080x2400 returned900x2000, "
        "not physical viewing size. Claude cannot confidently distinguish isolated衤/礻 at transport size; "
        "GPT reports distinguishing them, with original distinct nonblank native rasters retained. "
        "No unanimous fine-glyph certainty or actual fallback-face identity claimed. Scroll-hinted table "
        "clipping does not establish inaccessibility or prove every offset/gesture. No MLKit/human recall/"
        "negative geometry/successful model download/native-speaker/every-phone certification. Original "
        "source retrieval and initial process limits retained; no fresh dictionary fetch or reviewer "
        "native execution. Physical-phone/general-release/current-main/whole-set/publication acceptance "
        "outstanding; compatibleAndroidf9b59a2+ required. Historical denials/HOST OOMs retained; HOST-only "
        "heapinit NEVER native authorization."
    )
    reconciliation = {
        "schemaVersion": 1, "execution": 462, "batch": "070",
        "status": "bounded-visual-confirmation-closed-awaiting-integration",
        "evidenceHead": HEAD, "reviewedTeachingSnapshot": TEACHING,
        "dependentNotBlind": True, "models": [item[0] for item in SESSIONS.values()],
        "scope": "Whole new 償/償う/補償 and ONLY added 補 Common words backlink and newly linked 補償 comparison in 補う. Complete five teaching files read; unchanged reused bodies rendering/context, not renewed full linguistic review. Same23assigned native screenshots per model; own complete original report, complete596linefixture/log/route.",
        "allReviewerProcessesSerialAndExited": True, "allInternalCallsSerial": True,
        "allImageCallsSerial": True, "findings": [],
        "verdicts": {
            str(path.relative_to(R)): {
                "correctness": "CLEAN", "scopedCoverage": "CLEAN",
                "boundedVisualComprehensibility": "CLEAN",
                "scope": ("Only added Common words backlink" if path.name == "補.md" else
                          "Only newly linked compensation comparison" if path.name == "補う.md" else
                          "Whole new teaching file"),
            } for path in FILES
        },
        "changedReusedPassageAssignments": [
            {"article": "kanji\\補.md", "image": "n1-070-component1-19.png"},
            {"article": "words\\補う.md", "image": "n1-070-comparison-11.png"},
        ],
        "observations": [
            "No new actionable teaching/rendering defect established; inherited lexical conclusions unchanged. Exact new backlink and linked comparison visibly present in assigned screenshots.",
            "Four production rows show22individual characters and3words without blank/replacement boxes. Extra亻 in償, differing儀僧億 right shapes, 人/亻 and relevant clothing/hand comparisons visible. Claude retains isolated衤/礻 fine-detail uncertainty at resized size; GPT distinguishes them. Native88single/12wholeword rasters support nonblankness/distinctness, not actual fallback-face identity.",
            "Actual On optionsギ/ソウ/ショウ/ヨウ with correctショウ; Kunつぐなう/つましい/つばき/あつかう with correctつぐなう. Meaning choicesceremony;formalconduct/Japanesecedar/Buddhistmonk;priest/recompense;makeamends. Not complete authored儀僧億 trio or whole-pool certification.",
            "Four illustrative examples/kana/translations and godan/attempt/seeking-versus-paid guidance remain legible. Near-synonymous補+償 ホ+ショウ allocation and qualified compensation/legal scope retained.",
            "Reading tables clip at selected horizontal offsets, with explicit scroll hint/complementary views. No established inaccessible content; not every viewport/gesture certified.",
            "Supplied461native: exact full productionContentSyncONCE1082kanji5040words102N1/problems0/versiona9867cc4b455639a/epoch1; sixdirectedreciprocalroutes plus補↔補う and補う→補償/SystemBack/offline/N1selection/meaning/bothreadingGoodpersisted. Meaning exits Back before Next: no new persisted meaning grade.",
            "17numbered generated-reference strokes injected; practice/noSRS trace, model-unavailable geometry feedback, recallmiss and persistedDrawAgain. No successful human recall/MLKit or successful model download claimed.",
        ],
        "reportQualifications": [
            "Reviewers have no Git tools; coordinator freeze/diff/hash verification establishes snapshot identity and unchanged teaching.",
            "Both family reports establish bounded CLEAN findings, not unanimous certainty about every isolated small glyph. Claude's fine-detail uncertainty is preserved, not reclassified as a missing-glyph finding. GPT's direct visible distinction and original native evidence do not certify every device.",
            "Claude's 'each question exactly one correct option' is adopted only for actual pictured choices. It is not complete/random/live pool certification.",
            "Two reviewers viewing23samecaptures yields46payloads, not46independent scenes. Byte access is not linguistic comprehension/native-speaker certification.",
        ],
        "optional": [
            {
                "status": "optional", "reportedBy": "Claude",
                "claim": "Original suggestions: soften existing 補う legal-damages wording/mention償う; add1514650 to補 source line; add弁償/賠償.",
                "decision": "Retain original458 evidence-based optional dispositions unchanged. New link reaches explicit broad/narrow legal qualification; source line remains historical; all selected readings have useful exact linked examples. No new consequential omission established.",
            },
            {
                "status": "optional", "reportedBy": "Claude",
                "claim": "Dense reference stroke numbers overlap; ungraded-practice screen also mentions grading by geometry with model unavailable.",
                "decision": "Existing app presentation observations retained, not new teaching defects. Fixture explicitly verifies no tracing SRS log and later separate recall-miss Again log. No production app change or handwriting-recognition claim made.",
            },
        ],
        "modelContributionComparison": {
            "matchedScope": "Same snapshot/fiveboundedteachingfacets/23identicalimages/complete596linefixtureandreceipts; dependent confirmations.",
            "shared": "No actionable new teaching/rendering defect; changed reused passages and actual choices visible within shared viewport/phone limits.",
            "uniqueVerifiedClaudeDefects": [], "uniqueVerifiedGPTDefects": [],
            "limit": "Optional and limits compared too; no finding quota or general model ranking. Fine-glyph confidence differs explicitly; original initial independence preserved.",
        },
        "payloadAccounting": {
            "archivedSourceCaptures": 75, "assignedSourceCaptures": 23,
            "claudePayloads": 23, "gptPayloads": 23, "totalReturnedPayloads": 46,
            "sourceDimensions": [1080, 2400], "returnedDimensions": [900, 2000],
            "actualImagePaths": freeze["images"],
        },
        "inheritedEvidence": {
            "textual": "batch-070-reconciliation.json/execution458 unchanged, original initial two-read overlap and corrective serial reread retained.",
            "android": "execution-459.json freshRealContentTest3+RareHanTest1, not rerun.",
            "native": "execution-461.json two named terminal0/no skips178.905s, not rerun.",
        },
        "reviews": reviews, "checks": checks, "boundedIndependentVisualConfirmation": True,
        "runtimeAccepted": False, "runtimePublished": False, "limits": limits, "nextAction": NEXT,
    }
    save(V / "batch-070-visual-reconciliation.json", reconciliation)
    start = load(L / "execution-462-start.json")
    result = {
        "schemaVersion": 1, "execution": 462, "checkpoint": 462, "batch": "070",
        "status": reconciliation["status"], "startingHead": HEAD, "reviewedTeachingSnapshot": TEACHING,
        "authorization": start["authorization"], "scope": start["scope"],
        "originMainFreshFetch": start["originMainFreshFetch"], "reviews": reviews,
        "reconciliation": r"docs\n1-reviews\batch-070-visual-reconciliation.json",
        "reconciliationSha256": sha(V / "batch-070-visual-reconciliation.json"),
        "boundedIndependentVisualConfirmation": True, "allReviewerProcessesSerialAndExited": True,
        "allInternalCallsSerial": True, "allOriginalReportsAndTeachingUnmodified": True,
        "runtimeEditsMade": False, "nativeOrAndroidRerun": False, "publicationAttempted": False,
        "runtimePublished": False, "publishedAdditions": 96, "remainingAdditions": 1132,
        "phoneEvidence": False, "wholeProjectComplete": False, "nextAction": NEXT,
        "blocker": None, "limits": limits, "checks": checks, "recordedAt": now(),
        "coordinatorDirectImageChecks": ["n1-070-font-pairs.png", "n1-070-kanji-23.png",
                                         "n1-070-component1-19.png", "n1-070-comparison-11.png"],
    }
    save(R / r"docs\n1-sources\execution-462.json", result)
    path = R / r"docs\n1-sources\batch-070-progress.json"
    batch = load(path)
    batch.update(status=result["status"], nextAction=NEXT, limits=limits)
    batch["nativeVisualCheckpoint"] = {
        "execution": 462, "record": "execution-462.json",
        "reconciliation": "../n1-reviews/batch-070-visual-reconciliation.json",
        "boundedIndependentVisualConfirmation": True, "allInternalCallsSerial": True,
        "allReviewerProcessesSerialAndExited": True, "runtimePublished": False, "limits": limits,
    }
    save(path, batch)
    receipts = F.parent / "visual-execution-receipts"
    receipts.mkdir()
    for source in [Path(__file__), L / "execution-462-start.json"] + [
        C / f"batch-070-visual-{family}-process.json" for family in SESSIONS
    ]:
        shutil.copyfile(source, receipts / source.name)
    print("Bounded visual closure written;46actual returned PNGs; no runtime edit/publication.")


def checkpoint():
    result = load(R / r"docs\n1-sources\execution-462.json")
    assert sha(R / result["reconciliation"]) == result["reconciliationSha256"]
    signed = git("rev-parse", "HEAD")
    assert signed != HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    before = load(L / "execution-462-before-progress.json")
    p = load(C / "progress.json")
    assert p["checkpoint"] == 461 and p["batch"] == "070"
    summary = {
        "execution": 462, "checkpoint": 462, "batch": "070", "savedCommit": signed, "signature": "G",
        "record": r"docs\n1-sources\execution-462.json",
        "recordSha256": sha(R / r"docs\n1-sources\execution-462.json"), "status": "continue",
        "boundedIndependentVisualConfirmation": True, "allReviewerProcessesSerialAndExited": True,
        "allInternalCallsSerial": True, "runtimePublished": False,
        "publishedAdditions": 96, "remainingAdditions": 1132,
        "allOriginalHistoricalRootKeysPreservedExactly": True, "nextAction": NEXT,
    }
    p.update(checkpoint=462, status="continue", stage="batch-070-bounded-visual-confirmation-closed-awaiting-integration",
             nextAction=NEXT, blocker=None)
    p["execution462StartingState"]["status"] = "signed-bounded-visual-checkpoint-complete"
    p["batch070VisualConfirmationCheckpoint"] = dict(summary)
    p["execution462CoordinatorCheckpoint"] = dict(summary)
    for key in before.keys() - {"checkpoint", "status", "stage", "nextAction", "blocker"}:
        assert p[key] == before[key], key
    save(C / "progress.json", p)
    save(L / "execution-462-final-checkpoint.json", summary)
    body = (
        f"Batch 070 (償/償う/補償) bounded visual checkpoint **462** saved locally in normally signed `{signed}`; "
        "**not pushed or counted as delivered**.\n\n"
        "Original Claude Opus 5.5 and GPT-6.1 Sol sessions ran serially and exited. Each made "
        "37 strictly serial view calls: complete five teaching files, own original report, "
        "596-line native fixture/log/route and the same **23/75 source captures**. All46actual "
        "900×2000 returned image payloads are archived separately from1080×2400sources. "
        "New償/償う/補償 and exact changed補backlink/補うcomparison covered; unchanged reused bodies "
        "are rendering/context, not renewed full linguistic review. No actionable teaching/rendering "
        "defect established; no teaching/app changes. Original reports, source/process limits and "
        "all checkpoint history preserved.\n\n"
        "Validator zero errors; manifest unchanged, version`a9867cc4b455639a`,8338runtimefiles. "
        "Original local budgets pass:8360entries;30133596compressed/44349680inflated/"
        "44081342retained bytes. Passed461native(two terminal0/no skips178.905s) and459Android3+1 "
        "inherited without rerun. Both actual reading questions and correct feedback inspected; "
        "both Good grades persisted per fixture. No new persisted meaning grade, MLKit or successful "
        "human recall claimed. Scroll-hinted horizontal clipping is not established inaccessibility. "
        "Claude could not confidently distinguish isolated衤/礻 at resized transport; GPT distinguished "
        "them. Original native rasters and coordinator views retained, without unanimous fine-glyph/"
        "fallback-face/every-phone certification. Dense drawing numbers/practice-versus-geometry wording "
        "remain existing app presentation observations, not new teaching defects. Reports/dispositions: "
        "`docs/n1-sources/execution-462.json` and`docs/n1-reviews/batch-070-visual-reconciliation.json`.\n\n"
        "**96/1228 additions published;1132remain.** Next bounded checkpoint: fresh latest-main "
        "nonrewriting integration/combined validation, normal signing/owner fast-forward push, greenCI "
        "and exact immutable publicZIP/runtime-hash/original-budget verification before counting070 "
        "delivered or starting071. CompatibleAndroid`f9b59a2`+ required; physical-phone/general-release/"
        "whole-set acceptance outstanding. Full control history preserved;`progress.json`continue at462."
    )
    (C / "execution-462-issue-body.txt").write_text(body + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


def issue_receipt():
    response = load(C / "execution-462-issue-api.json")
    body = (C / "execution-462-issue-body.txt").read_text(encoding="utf-8")
    assert response["user"]["login"] == "stop-cran"
    assert response["body"].replace("\r\n", "\n").rstrip("\n") == body.replace("\r\n", "\n").rstrip("\n")
    p = load(C / "progress.json")
    assert p["checkpoint"] == 462 and p["status"] == "continue"
    assert git("rev-parse", "HEAD") == p["execution462CoordinatorCheckpoint"]["savedCommit"]
    assert not git("status", "--porcelain") and git("log", "-1", "--format=%G?") == "G"
    issue = {
        "url": response["html_url"], "author": "stop-cran", "commentId": response["id"],
        "bodyVerified": True, "bodyComparison": "Exact after CRLF/final-newline normalization only.",
    }
    p["batch070VisualIssueReceipt"] = issue
    for key in ("batch070VisualConfirmationCheckpoint", "execution462CoordinatorCheckpoint"):
        p[key]["issueUpdate"] = issue["url"]
        p[key]["ownerAuthorAndBodyVerified"] = True
    before = load(L / "execution-462-before-progress.json")
    for key in before.keys() - {"checkpoint", "status", "stage", "nextAction", "blocker"}:
        assert p[key] == before[key], key
    save(C / "progress.json", p)
    save(L / "execution-462-final-verification.json", {
        "checkpoint": 462, "status": "continue", "savedCommit": git("rev-parse", "HEAD"),
        "signature": "G", "worktreeClean": True, "allPriorHistoryPreserved": True,
        "issue": issue, "runtimePublished": False, "publishedAdditions": 96, "remainingAdditions": 1132,
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

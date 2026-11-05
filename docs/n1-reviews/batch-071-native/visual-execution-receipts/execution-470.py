import base64
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import struct
import subprocess
import sys

C = Path(__file__).parent
R = C.parent / "learning-japanese"
V = R / "docs" / "n1-reviews"
F = V / "batch-071-native" / "attempt-1"
L = C / "logs" / "439f9d14-dac5-41a5-ae84-b32d61040269"
HEAD = "43016306901a1111e309e7081e90db258cbc5f2d"
TEACHING = "1dc352148065c47d6d3a33206c62f3b877e678f6"
SESSIONS = {
    "claude": ("claude-opus-5.5", "43cc8b39-2d2e-4d29-a274-d582d2ac4e02"),
    "gpt": ("gpt-6.1-sol", "08e79180-ae38-4be2-bc8c-cd2f83041ab0"),
}
NEXT = (
    "SAME071 bounded dependent visual checkpoint470 closed: original Claude43cc8b39 and "
    "GPT08e79180 processes exited SERIAL; each33singleviewcalls/22assignedPNG/complete "
    "允+允可/ownoriginalreport/completefixture+terminal-log+route. All44actual returned "
    "900x2000payloads archived separately from1080x2400sources. All22unique source "
    "byte-streams represented;18otherfiles are duplicates, not fresh visual reads. "
    "GPT reported word-03 as status-bar strip but read construction in word-02; archived "
    "word-03 payload is full900x2000/844812bytes and identical to Claude's; coordinator "
    "direct returned-payload view shows complete passage. Do not equate complete returned "
    "bytes with every pixel actually perceived. No actionable teaching/rendering defect "
    "established; no teaching/app changes. Read docs\\n1-sources\\execution-470.json and "
    "docs\\n1-reviews\\batch-071-visual-reconciliation.json. Four production rows show "
    "27distinctHan+允可 including isolated儿/厶/口/土 readable/distinct; actual fallback "
    "face/every-phone unverified. Complementary left/right table captures jointly expose "
    "all4readinglabels/explanations with horizontal clipping/scrollhint; not all gestures "
    "or bodyH1 visually certified. SoleOnイン/いん question+feedback/Done1correct; explicit "
    "noKun is intended, fullkun retained. Actual meaning choices camphortree/chestnut/"
    "hawkfalcon, NOT authored元兄去 trio or whole-pool certification. Inherit466textual, "
    "467freshAndroid3+1 and469native2terminal0/no skips112.22s without rerun. No new "
    "persisted meaning grade, MLKit/human recall or successful modeldownload. NEXT "
    "BOUNDED CHECKPOINT: freshfetchlatestorigin/main/nonrewritingintegration as needed; "
    "actualcombined membership/baseline/readings/links/font/stroke/Python/vocab/validator/"
    "freshmanifest/original18000entries42MiBcompressed80MiBinflated56MiBretainedbudgets; "
    "normal signing/ownerfastforward/publicSHA/terminalgreenCI/EVERYimmutablepublicZIP "
    "runtimehash+budgets/ownerissue60 BEFOREdelivery or072. No redundant Android/native "
    "absent new concern. Preserve actual denials/signingwait and yield; no workaround/"
    "secondrunner/supervisoredits/concurrentheavywork. HOST-only2GiBinit NEVER native. "
    "Published97/1228,remaining1131/latest070e8874e68; local071 NOTdelivered. Compatible "
    "Androidf9b59a2+ required; physicalphone/generalrelease/whole-set acceptance outstanding."
)
FILES = [R / "kanji" / "允.md", R / "words" / "允可.md"]
FIXTURE = F / "N1Batch071NativeTest.kt"
TASK = C / "batch-071-visual-task.txt"


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


def freeze():
    record = load(C / "batch-071-visual-freeze.json")
    assert git("rev-parse", "HEAD") == HEAD
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    for path, digest in record["resourceHashes"].items():
        assert sha(Path(path)) == digest, path
    return record


def prepare():
    assert git("rev-parse", "HEAD") == HEAD and not git("status", "--porcelain")
    assert git("log", "-1", "--format=%G?") == "G"
    text = (L / "request.txt").read_text(encoding="utf-8-sig")
    embedded = json.loads(text.split("Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    progress = load(C / "progress.json")
    assert embedded["checkpoint"] == progress["checkpoint"] == 469
    assert progress["batch"] == "071"
    backup = L / "execution-470-before-progress.json"
    assert not backup.exists()
    shutil.copyfile(C / "progress.json", backup)
    start = {
        "execution": 470, "batch": "071", "startingHead": HEAD, "recordedAt": now(),
        "scope": "SAME071 two serial original-session dependent visual confirmations, exact returned payload/range/process archival, reconciliation and normally signed local evidence checkpoint only. No Android/native rerun, publication,072 or second runner.",
        "authorization": {
            "requestSha256": sha(L / "request.txt"), "characters": len(text), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request acquired and complete embedded checkpoint parsed; operative contract, approved issue and complete final469 checkpoint inspected directly. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "status": "dependent-visual-confirmation-preparing",
    }
    save(L / "execution-470-start.json", start)
    progress["execution470StartingState"] = start
    progress.update(stage="batch-071-dependent-visual-confirmation-preparing", nextAction=start["scope"])
    save(C / "progress.json", progress)
    index = V / "batch-071-native" / "execution-469-artifact-index.json"
    native = load(index)
    for row in native["files"]:
        assert sha(R / row["path"]) == row["sha256"], row["path"]
        assert (R / row["path"]).stat().st_size == row["bytes"]
    images = [F / name for name in native["directCoordinatorImageRequests"]]
    assert len(images) == 22 and len({sha(path) for path in images}) == 22
    resources = FILES + images + [FIXTURE, F / "instrumentation.txt", F / "n1-071-article-route.json", index, TASK]
    resources += [V / f"batch-071-initial-{family}.md" for family in SESSIONS]
    save(C / "batch-071-visual-freeze.json", {
        "execution": 470, "batch": "071", "evidenceHead": HEAD, "teachingSnapshot": TEACHING,
        "images": [str(path) for path in images], "assignedCaptures": 22, "archivedSourceCaptures": 40,
        "fixtureLines": len(FIXTURE.read_text(encoding="utf-8").splitlines()),
        "fixtureRanges": [[1, 120], [121, 240], [241, 360], [361, 480], [481, -1]],
        "resourceHashes": {str(path): sha(path) for path in resources},
    })
    print("Early scope saved; exact native evidence verified; all22 unique image streams frozen.")


def run(family):
    freeze()
    if family == "gpt":
        prior = load(V / "batch-071-visual-claude-execution.json")
        assert prior["exitCode"] == 0 and prior["processAndCoverageAccepted"]
    model, session = SESSIONS[family]
    prefix = "batch-071-visual-" + family
    raw = C / f"{prefix}.jsonl"
    assert not raw.exists(), "Never overwrite original execution"
    command = [
        shutil.which("copilot"), "-C", str(R), "--add-dir", str(C),
        "--model", model, "--session-id", session, "--no-ask-user",
        "--allow-all-tools", "--disable-builtin-mcps", "--available-tools=view",
        "--output-format", "json", "--log-dir", str(C / "review-logs" / prefix),
        "--usage-output-file", str(C / f"{prefix}-usage.json"),
        "-p", "Read the ENTIRE shared bounded dependent visual task at " + str(TASK)
        + ". YOUR complete original initial report is " + str(V / f"batch-071-initial-{family}.md")
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
    frozen = freeze()
    prefix = "batch-071-visual-" + family
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
    required = FILES + [TASK, V / f"batch-071-initial-{family}.md", FIXTURE,
                        F / "instrumentation.txt", F / "n1-071-article-route.json"]
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
    allowed = {str(path) for path in required} | set(frozen["images"])
    unexpected = [row["arguments"]["path"] for row in calls.values() if row["arguments"]["path"] not in allowed]
    multi = sum(len(m.get("toolRequests", [])) > 1 for m in messages)
    accepted = (process["exitCode"] == 0 and models == [process["requestedModel"]] == [usage["currentModel"]]
                and not active and not overlaps and not multi and not missing and not unexpected
                and actual_images == set(frozen["images"])
                and all(row["success"] and row["name"] == "view" for row in calls.values()))
    record = {
        **process, "actualModels": models, "availableTools": ["view"],
        "dependentOriginalSessionNotBlindInitial": True, "reportSha256": sha(report),
        "rawExecutionLocation": str(raw), "rawExecutionSha256": sha(raw),
        "configurationEvidence": [event["data"] for event in events if event["type"] == "session.info"],
        "usage": usage, "toolCalls": list(calls.values()), "observedToolOverlaps": overlaps,
        "multiToolResponses": multi, "unfinishedTools": sorted(active), "missingRequiredText": missing,
        "unexpectedReadPaths": unexpected, "imagePayloadsVerified": len(actual_images),
        "expectedPngMembershipReturned": actual_images == set(frozen["images"]),
        "processAndCoverageAccepted": accepted,
        "limits": "Dependent original-session confirmation;22 unique source captures/40 archived files. Exact returned bytes/ranges establish access, not comprehension. No reviewer native execution, fresh upstream retrieval, physical-phone or final publication acceptance.",
    }
    save(V / f"{prefix}-execution.json", record)
    print(json.dumps({key: record[key] for key in ("actualModels", "processAndCoverageAccepted",
                     "imagePayloadsVerified", "missingRequiredText", "observedToolOverlaps", "multiToolResponses")}))
    assert accepted


def record():
    frozen = freeze()
    reviews = {}
    for family, (model, session) in SESSIONS.items():
        path = V / f"batch-071-visual-{family}-execution.json"
        item = load(path)
        assert item["processAndCoverageAccepted"] and item["exitCode"] == 0
        assert item["actualModels"] == [model] == [item["usage"]["currentModel"]]
        assert item["sessionId"] == session and not item["unfinishedTools"]
        assert not item["observedToolOverlaps"] and not item["multiToolResponses"]
        assert len(item["toolCalls"]) == 33 and item["imagePayloadsVerified"] == 22
        assert sha(V / f"batch-071-visual-{family}.md") == item["reportSha256"]
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
            "report": str((V / f"batch-071-visual-{family}.md").relative_to(R)),
            "reportSha256": item["reportSha256"], "execution": str(path.relative_to(R)),
            "executionSha256": sha(path), "actualModel": model, "sessionId": session,
            "startedAt": item["startedAt"], "completedAt": item["completedAt"],
            "exitCode": 0, "toolCalls": len(item["toolCalls"]), "verifiedReturnedImages": 22,
            "allInternalCallsSerial": True, "processAndCoverageAccepted": True,
        }
    assert datetime.fromisoformat(reviews["claude"]["completedAt"]) < datetime.fromisoformat(reviews["gpt"]["startedAt"])
    for name in frozen["images"]:
        a = F.parent / "visual-claude-returned" / Path(name).name
        b = F.parent / "visual-gpt-returned" / Path(name).name
        assert sha(a) == sha(b)
    checks = {}
    for name in ("validate", "manifest", "budget"):
        source = C / f"execution-470-{name}.txt"
        target = V / f"batch-071-visual-{name}-execution-470.txt"
        assert not target.exists()
        shutil.copyfile(source, target)
        checks[name] = {"path": str(target.relative_to(R)), "sha256": sha(target)}
    for name in ("task", "help-execution-470", "models-execution-470"):
        source = C / f"batch-071-visual-{name}.txt"
        target = V / source.name
        assert not target.exists()
        target.write_text(source.read_text(encoding="utf-8-sig").rstrip() + "\n", encoding="utf-8")
    save(V / "batch-071-visual-freeze.json", frozen)
    limits = (
        "Dependent22unique-sourcecapture confirmation/40archivedfiles;18duplicates are not fresh "
        "visual reads. Both received22full900x2000payloads, not physical viewing size. GPT reported "
        "word-03 as a narrow strip and used word-02 for the same construction. Raw full-sized "
        "word-03 payload equals Claude's and coordinator directly saw the complete passage; "
        "do not claim every returned pixel was perceived by GPT. Source1080x2400; no every-viewport/"
        "gesture/bodyH1 certificate. Horizontal clipping with scrollhint/complementary views "
        "does not establish inaccessibility. No fallback-face identification, whole-pool safety, "
        "fresh upstream/Git review, native-speaker/every-phone certification, MLKit, human recall, "
        "successful model download, reverse/negative geometry or new persisted meaning grade. "
        "Original initial lexical/process/source limits and optional dispositions inherited. "
        "Native469/Android467 not rerun. Physical-phone/general-release/current-main/whole-set/"
        "publication acceptance outstanding; compatibleAndroidf9b59a2+ required. Historical "
        "denials/HOST OOMs retained; HOST-only heapinit NEVER native authorization."
    )
    reconciliation = {
        "schemaVersion": 1, "execution": 470, "batch": "071",
        "status": "bounded-visual-confirmation-closed-awaiting-integration",
        "evidenceHead": HEAD, "reviewedTeachingSnapshot": TEACHING,
        "dependentNotBlind": True, "models": [item[0] for item in SESSIONS.values()],
        "scope": "Whole new kanji/允.md and words/允可.md; no reused teaching edits. Both complete files, own complete initial report, complete native fixture/log/route and same22nativePNG per family. Initial independent textual conclusions inherited, not fresh dictionary review.",
        "allReviewerProcessesSerialAndExited": True, "allInternalCallsSerial": True,
        "allImageCallsSerial": True, "findings": [],
        "verdicts": {
            str(path.relative_to(R)): {
                "correctness": "CLEAN", "scopedCoverage": "CLEAN",
                "boundedVisualComprehensibility": "CLEAN", "scope": "Whole new teaching file",
            } for path in FILES
        },
        "observations": [
            "Both retain whole-text CLEAN verdicts; no new actionable teaching/rendering defect established. No teaching/app changes.",
            "Four production font rows show27distinctHan and whole word允可 without observed blank/replacement boxes. 允厶-above儿, 元bars, 兄口, 去土-above厶, 公/先, isolated儿/厶 and口/土 distinguishable. Textbook isolated radicals visibly heavier; actual fallback face unidentified. Native108singlePaint+4word probes corroborate nonblankness/distinct rasters, not every-phone readability.",
            "Complementary left/right table captures show all four labels and explanations, with clipped left beginnings/right explanations at different offsets and explicit scrollhint. Historical雅楽允うたのじょう, classicalまこと.に, dictionary-onlyゆるす and linked selectedイン remain qualified. No every-offset/gesture certificate.",
            "Visible允可を得るいんかをえる means obtain, not give permission;1868dictionary-form adaptation, compliance limitation, near-synonymous允+可イン+カ, ordinary写真を撮ってもいいですか kana/translation and formal/older register qualifications remain readable.",
            "Actual On optionsイン/ハン/ケン/リン with correctイン and Done1of1correct; intentional noKun with Full+Lite full readings retained. Actual meaning choicescamphortree/chestnut/hawkfalcon are distinct from permit;sincerity, NOT the authored元兄去 trio or whole-pool certification.",
            "Mapped允↔允可 two directions and SystemBack screens consistent with actual supplied native route;可 remains declared but unlinked without card. Pixels alone are not reviewer-executed navigation.",
            "Supplied469native: exact full productionContentSyncONCE1083kanji5041words103N1/problems0/version05002d6e68a4eb89/epoch1; terminal0two named cases/no skips112.22s. Synthetic source/HEAD, otherN1postponed/twohistoricalGoodmeaninglogs/no drawingstateseeded. SoleOnGood/noKunLog/Done1correct persisted; meaning exited Back before Next, no new meaning grade.",
            "Four generated-reference touch strokes; ungradedtrace/noDrawLog/model-unavailablegeometryfeedback/recallmiss/persistedDrawAgain. Not MLKit, human handwriting/successful recall, successful model download or reverse/negative geometry evidence.",
        ],
        "reportQualifications": [
            "Both have no Git tools; coordinator freeze/diff/hash checks establish snapshot identity and unchanged teaching. Read/byte evidence establishes access, not comprehension.",
            "GPT reports word-03 as a narrow strip but explicitly reads full example in word-02. Archived word-03 is900x2000/844812bytes, matches Claude's full payload; coordinator directly viewed it and saw full example/explanation. Preserve GPT's perceived-viewport limit rather than rewriting the original report or assuming full perception.",
            "Claude's screenshot list groups21names but actual audited33calls include selection and22images. GPT explicitly lists22. All actual paths/payloads retained.",
            "Claude's 'top heading never appears' interpreted as bodyH1, not appbar, which visibly shows允可 permission;assent. Complete source H1 text read; no standalone bodyH1 pixel acceptance claimed.",
            "Claude's reading-feedback line omits the source dot inまこと.に as expected for normalized display; raw source reading/own row preserve dot. Not metadata loss.",
            "NoKun absence/navigation/persistedgrades rely on fixture/terminal receipt, not observation of every transition. Claude's drawing-geometry language does not make practice graded; no tracingSRSlog and separateRecallAgain are explicit.",
        ],
        "optional": [
            {
                "status": "optional", "reportedBy": "Claude",
                "claim": "Initial雅楽允allocation, Osaka-prefecture provenance, 允文允武citation and emperor wording suggestions retained;従う comment does not allege missing exclusion.",
                "decision": "Keep original466 evidence-based optional dispositions unchanged. No consequential omission or erroneous scope newly established; do not broaden historical/name/idiom teaching.",
            },
            {
                "status": "optional", "reportedBy": "Claude",
                "claim": "character-dictionary wraps mid-word without a hyphen.",
                "decision": "Existing renderer/table-width presentation, not incorrect content or established inaccessibility. Whole term legible across wrapped lines; retain explicit sideways-scroll guidance, no app/algorithm work.",
            },
        ],
        "modelContributionComparison": {
            "matchedScope": "Same snapshot/two whole new teaching files/22identicalimages/completefixture+receipts; dependent confirmations.",
            "shared": "No actionable new teaching/rendering defect; scoped glyph/reading/example/route acceptance with original source and phone limits.",
            "uniqueVerifiedClaudeDefects": [], "uniqueVerifiedGPTDefects": [],
            "limit": "Optional and limits compared too; no finding quota or general model ranking. GPT's perceived word-03 strip retained; equivalent example visible in word-02. Initial independent review not relabelled.",
        },
        "payloadAccounting": {
            "archivedSourceCaptures": 40, "assignedUniqueSourceCaptures": 22,
            "otherByteIdenticalSourceFiles": 18, "claudePayloads": 22, "gptPayloads": 22,
            "totalReturnedPayloads": 44, "sourceDimensions": [1080, 2400],
            "returnedDimensions": [900, 2000], "sameReturnedBytesForBoth": True,
            "actualImagePaths": frozen["images"],
            "gptPerceivedViewportLimit": "word-03 reported strip; full example seen in word-02. Payload full-sized and coordinator independently views complete passage.",
        },
        "coordinatorArchiveError": {
            "reviewerFailed": False, "reviewerExitCode": 0,
            "cause": "After complete Claude report/execution/payload archival, helper save roundtrip asserted tuple image dimensions equal JSON lists. Record had already saved correctly.",
            "fix": "Compare JSON-normalized in-memory value to loaded JSON; no content/reviewer evidence rewritten or rerun. GPT launch gated on re-read successful Claude processAndCoverageAccepted record and process exit.",
        },
        "inheritedEvidence": {
            "textual": "batch-071-reconciliation.json/execution466 unchanged; initial Claude overlapping guidance read and original-session serial reread retained.",
            "android": "execution-467.json freshRealContentTest3+RareHanTest1, not rerun.",
            "native": "execution-469.json two named terminal0/no skips112.22s, not rerun.",
        },
        "reviews": reviews, "checks": checks, "boundedIndependentVisualConfirmation": True,
        "runtimeAccepted": False, "runtimePublished": False, "limits": limits, "nextAction": NEXT,
    }
    save(V / "batch-071-visual-reconciliation.json", reconciliation)
    start = load(L / "execution-470-start.json")
    result = {
        "schemaVersion": 1, "execution": 470, "checkpoint": 470, "batch": "071",
        "status": reconciliation["status"], "startingHead": HEAD, "reviewedTeachingSnapshot": TEACHING,
        "authorization": start["authorization"], "scope": start["scope"],
        "originMainFreshFetch": git("rev-parse", "origin/main"), "reviews": reviews,
        "reconciliation": r"docs\n1-reviews\batch-071-visual-reconciliation.json",
        "reconciliationSha256": sha(V / "batch-071-visual-reconciliation.json"),
        "boundedIndependentVisualConfirmation": True, "allReviewerProcessesSerialAndExited": True,
        "allInternalCallsSerial": True, "allOriginalReportsAndTeachingUnmodified": True,
        "runtimeEditsMade": False, "nativeOrAndroidRerun": False, "publicationAttempted": False,
        "runtimePublished": False, "publishedAdditions": 97, "remainingAdditions": 1131,
        "phoneEvidence": False, "wholeProjectComplete": False, "nextAction": NEXT,
        "blocker": None, "limits": limits, "checks": checks, "recordedAt": now(),
        "coordinatorDirectImageChecks": ["n1-071-font-pairs.png", "n1-071-kanji-20.png",
                                         "n1-071-kanji-09.png", "visual-gpt-returned/n1-071-word-03.png",
                                         "n1-071-word-02.png"],
        "checksSummary": {
            "validatorErrors": 0, "manifestFresh": True, "runtimeHashesVerified": 8341,
            "contentVersion": "05002d6e68a4eb89",
            "budget": {"entries": 8363, "localZipBytes": 30137644, "inflatedBytes": 44356753,
                       "retainedBytes": 44088415},
            "originalLimitsUnchanged": True,
        },
    }
    save(R / r"docs\n1-sources\execution-470.json", result)
    path = R / r"docs\n1-sources\batch-071-progress.json"
    batch = load(path)
    batch.update(status=result["status"], nextAction=NEXT, limits=limits)
    batch["nativeVisualCheckpoint"] = {
        "execution": 470, "record": "execution-470.json",
        "reconciliation": "../n1-reviews/batch-071-visual-reconciliation.json",
        "boundedIndependentVisualConfirmation": True, "allInternalCallsSerial": True,
        "allReviewerProcessesSerialAndExited": True, "runtimePublished": False, "limits": limits,
    }
    save(path, batch)
    receipts = F.parent / "visual-execution-receipts"
    receipts.mkdir()
    for source in [Path(__file__), L / "execution-470-start.json"] + [
        C / f"batch-071-visual-{family}-process.json" for family in SESSIONS
    ]:
        shutil.copyfile(source, receipts / source.name)
    preflight = load(C / "batch-071-visual-preflight-470.json")
    processes = preflight if isinstance(preflight, list) else [preflight]
    matches = [
        row["ProcessId"] for row in processes
        if any(session in (row.get("CommandLine") or "") for _, session in SESSIONS.values())
    ]
    assert not matches
    save(receipts / "batch-071-visual-preflight-470.json", {
        "originalReviewerSessionsActive": matches,
        "checkedSessionIds": [session for _, session in SESSIONS.values()],
        "rawControlReceiptSha256": sha(C / "batch-071-visual-preflight-470.json"),
        "scope": "Process inspection immediately before first launch; unrelated process command lines excluded from contributor evidence.",
    })
    print("Bounded visual closure written;44actual returned PNGs; no runtime edit/publication.")


def checkpoint():
    result = load(R / r"docs\n1-sources\execution-470.json")
    assert sha(R / result["reconciliation"]) == result["reconciliationSha256"]
    signed = git("rev-parse", "HEAD")
    assert signed != HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    before = load(L / "execution-470-before-progress.json")
    progress = load(C / "progress.json")
    assert progress["checkpoint"] == 469 and progress["batch"] == "071"
    summary = {
        "execution": 470, "checkpoint": 470, "batch": "071", "savedCommit": signed, "signature": "G",
        "record": r"docs\n1-sources\execution-470.json",
        "recordSha256": sha(R / r"docs\n1-sources\execution-470.json"), "status": "continue",
        "boundedIndependentVisualConfirmation": True, "allReviewerProcessesSerialAndExited": True,
        "allInternalCallsSerial": True, "runtimePublished": False,
        "publishedAdditions": 97, "remainingAdditions": 1131,
        "allOriginalHistoricalRootKeysPreservedExactly": True, "nextAction": NEXT,
    }
    progress.update(checkpoint=470, status="continue", stage="batch-071-bounded-visual-confirmation-closed-awaiting-integration",
                    nextAction=NEXT, blocker=None)
    progress["execution470StartingState"]["status"] = "signed-bounded-visual-checkpoint-complete"
    progress["batch071VisualConfirmationCheckpoint"] = dict(summary)
    progress["execution470CoordinatorCheckpoint"] = dict(summary)
    for key in before.keys() - {"checkpoint", "status", "stage", "nextAction", "blocker"}:
        assert progress[key] == before[key], key
    save(C / "progress.json", progress)
    save(L / "execution-470-final-checkpoint.json", summary)
    body = (
        f"Batch 071 (允/允可) bounded visual checkpoint **470** saved locally in normally signed `{signed}`; "
        "**not pushed or counted as delivered**.\n\n"
        "Original Claude Opus 5.5 and GPT-6.1 Sol sessions ran serially and exited. Each made "
        "33 strictly serial view calls: complete two new teaching files, own original report, "
        "complete native fixture/log/route and the same **22 unique source captures** out of40files. "
        "All44actual900×2000returned image payloads archived separately from1080×2400sources; "
        "18otherfiles are byte-identical duplicates, not fresh visual reads. Both retain scoped "
        "CLEAN verdicts; no actionable teaching/rendering defect or teaching/app change. Original "
        "reports/source/process limits and all historical progress preserved.\n\n"
        "All27Han+允可 visible across four production rows, including isolated儿/厶/口/土; actual "
        "fallback face/every-phone unverified. Complementary left/right table views expose all4 "
        "reading labels/explanations with scroll-hinted clipping; not every viewport/gesture/bodyH1. "
        "GPT reported word-03 as a narrow strip but saw the construction in word-02; raw word-03 "
        "is full900×2000 and identical to Claude's, independently viewed by coordinator. Complete "
        "returned bytes are not proof every pixel was perceived. SoleOnイン/いん correct, Done1of1; "
        "explicit noKun intentional/fullsourcekun retained. Actual meaning distractors arecamphor "
        "tree/chestnut/hawk;falcon, not the authored元兄去 trio or full-pool certification.\n\n"
        "Validator zero errors; manifest unchanged, version`05002d6e68a4eb89`,8341runtimefiles. "
        "Original local budgets pass:8363entries;30137644compressed/44356753inflated/"
        "44088415retained bytes. Passed469native(two terminal0/no skips112.22s) and467Android3+1 "
        "inherited without rerun. No new persisted meaning grade, MLKit, human successful recall "
        "or successful model download claimed. Reports/dispositions: "
        "`docs/n1-sources/execution-470.json` and`docs/n1-reviews/batch-071-visual-reconciliation.json`.\n\n"
        "**97/1228 additions published;1131remain.** Next bounded checkpoint: fresh latest-main "
        "nonrewriting integration/combined validation, normal signing/owner fast-forward push, greenCI "
        "and exact immutable publicZIP/runtime-hash/original-budget verification before counting071 "
        "delivered or starting072. CompatibleAndroid`f9b59a2`+ required; physical-phone/general-release/"
        "whole-set acceptance outstanding. Full control history preserved;`progress.json`continue at470."
    )
    (C / "execution-470-issue-body.txt").write_text(body + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


def issue_receipt():
    response = load(C / "execution-470-issue-api.json")
    body = (C / "execution-470-issue-body.txt").read_text(encoding="utf-8")
    assert response["user"]["login"] == "stop-cran"
    assert response["body"].replace("\r\n", "\n").rstrip("\n") == body.replace("\r\n", "\n").rstrip("\n")
    progress = load(C / "progress.json")
    assert progress["checkpoint"] == 470 and progress["status"] == "continue"
    assert git("rev-parse", "HEAD") == progress["execution470CoordinatorCheckpoint"]["savedCommit"]
    assert not git("status", "--porcelain") and git("log", "-1", "--format=%G?") == "G"
    issue = {
        "url": response["html_url"], "author": "stop-cran", "commentId": response["id"],
        "bodyVerified": True, "bodyComparison": "Exact after CRLF/final-newline normalization only.",
    }
    progress["batch071VisualIssueReceipt"] = issue
    for key in ("batch071VisualConfirmationCheckpoint", "execution470CoordinatorCheckpoint"):
        progress[key]["issueUpdate"] = issue["url"]
        progress[key]["ownerAuthorAndBodyVerified"] = True
    before = load(L / "execution-470-before-progress.json")
    for key in before.keys() - {"checkpoint", "status", "stage", "nextAction", "blocker"}:
        assert progress[key] == before[key], key
    save(C / "progress.json", progress)
    save(L / "execution-470-final-verification.json", {
        "checkpoint": 470, "status": "continue", "savedCommit": git("rev-parse", "HEAD"),
        "signature": "G", "worktreeClean": True, "allPriorHistoryPreserved": True,
        "issue": issue, "runtimePublished": False, "publishedAdditions": 97, "remainingAdditions": 1131,
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
    else:
        raise ValueError(sys.argv[1])

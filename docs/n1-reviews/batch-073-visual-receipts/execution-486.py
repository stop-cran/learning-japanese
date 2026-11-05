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

L = Path(__file__).parent
C = L.parent.parent
R = C.parent / "learning-japanese"
V = R / "docs" / "n1-reviews"
F = V / "batch-073-native" / "attempt-1"
HEAD = "27813d5ed5478935b7256a54f81f0c91d7e297f9"
TEACHING = "c8c2a0ba7dfc794feac5362fcfefa41e8d33ee5a"
TASK = V / "batch-073-visual-task.txt"
FIXTURE = F / "N1Batch073NativeTest.kt"
FILES = [R / "kanji" / "克.md", R / "words" / "克服.md", R / "kanji" / "服.md"]
SESSIONS = {
    "claude": ("claude-opus-5.5", "482a74cb-d8a4-47d5-8e7d-1451bbdfc13b"),
    "gpt": ("gpt-6.1-sol", "427eb11f-e4a8-43eb-9677-eb03d1065cfe"),
}
NEXT = (
    "SAME073 dependent visual confirmations486 complete: original Claude482a74cb THEN "
    "GPT427eb11f processes exited serially; actual claude-opus-5.5/gpt-6.1-sol; "
    "both full task/own original report/three teaching context files/complete native fixture/"
    "terminal instrumentation/route and18uniquePNG returned with exact payload archival. "
    "Read docs\\n1-sources\\execution-486.json and batch-073-visual-reconciliation.json "
    "for verdicts, actual read coverage and limits. No teaching/app changes or new blind "
    "initial reviews. Inherit482textual/483HOST3+1/485native2terminal0noskips; no rerun "
    "absent new concern. NEXT freshfetchorigin/main/nonrewritingintegration if needed; "
    "validate actual combined membership/baseline/readings/links/font/stroke/Python/vocab/"
    "validator/freshmanifest/original18000entries42MiBcompressed80MiBinflated56MiBretained; "
    "normal signing/owner fastforward/publicSHA/terminalgreenCI/EVERYimmutablepublicZIP"
    "runtimehash+budgets/ownerissue60 BEFOREdelivery or074. No signingretry/permissionworkaround/"
    "secondrunner/supervisoredits/concurrentheavywork. Published99/1228,remaining1129;"
    "local073NOTdelivered;100publishednecessarysupportsNOTN1vocabulary. CompatibleAndroid"
    "f9b59a2+ required; physicalphone/generalrelease/whole-setacceptanceoutstanding."
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


def freeze():
    frozen = load(L / "visual-freeze.json")
    assert git("rev-parse", "HEAD") == HEAD
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    for path, digest in frozen["resourceHashes"].items():
        assert sha(Path(path)) == digest, path
    return frozen


def prepare():
    assert git("rev-parse", "HEAD") == HEAD and not git("status", "--porcelain")
    assert git("log", "-1", "--format=%G?") == "G"
    request = (L / "request.txt").read_text(encoding="utf-8-sig")
    embedded = json.loads(request.split("Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    progress = load(C / "progress.json")
    assert embedded["checkpoint"] == progress["checkpoint"] == 485 and progress["batch"] == "073"
    shutil.copyfile(C / "progress.json", L / "before-progress.json")
    start = {
        "execution": 486, "batch": "073", "startingHead": HEAD, "recordedAt": now(),
        "scope": "SAME073 two serial original-session dependent visual confirmations, exact returned payload/range/process archival, reconciliation and normally signed local evidence checkpoint only. No Android/native rerun, publication,074 or second runner.",
        "authorization": {
            "requestSha256": sha(L / "request.txt"), "characters": len(request), "lines": len(request.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request acquired and complete embedded checkpoint parsed; operative contract, complete approved issue and complete final485 inspected directly. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "status": "preparing-dependent-visual-confirmation",
    }
    save(L / "starting-state.json", start)
    progress["execution486StartingState"] = start
    progress.update(stage="batch-073-dependent-visual-confirmation-preparing", nextAction=start["scope"])
    save(C / "progress.json", progress)
    index = V / "batch-073-native" / "execution-485-artifact-index.json"
    native = load(index)
    for row in native["files"]:
        path = R / row["path"]
        assert sha(path) == row["sha256"] and path.stat().st_size == row["bytes"], path
    images = [F / name for name in native["directCoordinatorImageRequests"]]
    assert len(images) == len({sha(path) for path in images}) == 18
    for args, label in [(["--help"], "help"), (["help", "config"], "models")]:
        result = subprocess.run([shutil.which("copilot"), *args], capture_output=True, encoding="utf-8", check=True)
        (L / f"copilot-{label}.txt").write_text(result.stdout, encoding="utf-8")
    catalog = (L / "copilot-models.txt").read_text(encoding="utf-8")
    assert all(model in catalog for model, _ in SESSIONS.values())
    task = f"""SAME073 DEPENDENT original-session native visual confirmation, execution486.
NOT a fresh blind initial review, fresh dictionary audit or native rerun.
Evidence HEAD {HEAD}; teaching unchanged from {TEACHING}.
Exact full native Git envelope5d322346c0c8bccdc36769d85f3fb23f4b5cbbee.

STRICT SERIAL TOOLS: exactly ONE view call per response; WAIT for result.
Never multiple tool calls/parallel wrappers. Only view is available.
No shell/edit/search/delegation/device operations. Read this COMPLETE task
and YOUR complete original initial report supplied at launch. Do not read
other reports or coordinator adjudication. Inherit original lexical
conclusions/optional dispositions/source and process limits. No fresh
upstream retrieval is requested; do not reopen full dictionary dossiers.

Read each COMPLETE teaching file singly:
"""
    task += "\n".join(str(path) for path in FILES)
    task += f"""
Review complete NEW克. Reused克服 ONLY line24 link addition and服 ONLY line21
new sentence are assigned; full files are context, NOT fresh whole reused-article
certification. Historical enemy-submission wording outside those changed
passages is not a new unconditional modern substitution claim.
Read COMPLETE native fixture in separate inclusive ranges <=120lines:
{FIXTURE}
Use [1,120],[121,240],... through EOF; do not skip middle ranges.
Actual fixture has {len(FIXTURE.read_text(encoding="utf-8").splitlines())} lines.
Read COMPLETE these small operational receipts separately:
{F / "instrumentation.txt"}
{F / "n1-073-article-route.json"}

Actually VIEW each of these EIGHTEEN PNGs singly, ONE PER RESPONSE:
"""
    task += "\n".join(str(path) for path in images)
    task += """

Bounded18/30 source captures: other12 are exact byte duplicates mapped by
artifact index, NOT extra fresh views. Do not infer visibility from selectors
or names. State missing/clipped parts. Source1080x2400 may be resized by
view; disclose transport/viewport limits. Whole text is not whole-viewport
visual acceptance. Horizontal reading-table offsets may clip cells.
Check labels in left capture and explanations in complementary right views;
an explicit sideways-scroll hint does not prove every gesture/offset worked.
Final source-link line may be partly below notes frame; distinguish complete
projection assertions from actual pixels. Do not demand redundant device
work for an incidental external-source footer if substantive teaching is shown.

Inspect actual27distinctHan and克服 in FOUR production font rows:
人 儿 元 兄 克 制 前 勝 口 古 困 女 己 彼 怖 恐 月 服 朝 決 洋 用 着 紙 解 話 難
Check readable/distinguishable, no blank/replacement boxes,克/古/兄/元,
isolated儿 and己/勝/服. Typeface changes/coinciding styles alone not defects.
108singlePaint+4wholeword probes support nonblankness/distinct rasters,
NOT actual fallback-face identity/every-phone readability.
Seven strokes/indexing radical儿10; labelled modern-shape mnemonic not origin.

Full+Lite raw on[コク],kun[か.つ] retained. Curated on[コク]/kun[],
normalizedこく/[]; no kun question or log. Both visible reading labels/
explanations need inspection. Rare SPELLING克つ not rare pronunciationかつ;
己に克つおのれにかつ is self-control, not an absolute克/勝 semantic partition.
Linked克服こくふく is usefulコク example;服 brings under control HERE, not
clothes in this compound. Match actual shown quiz/options/feedback,
not solely authored distractors古兄元 or dictionary text.
Check克↔克服 and服↔克服 FOUR directions/SystemBack via supplied fixture/
route and bounded representative screenshots. Duplicate Back frames
not separately assigned fresh views. No new support word/article title/
exclusion; do not expand scope to unchanged easier articles.

SUPPLIED operational results, NOT reviewer-executed:485 BOTH named cases
terminal0/no skips82.165s. Exact full envelope productionContentSync ONCE:
1085kanji5042words105N1/problems0/version1d8a4ee1a97c6bb5/epoch1.
Synthetic disposable source/HEAD, otherN1postponed/twohistoricalGoodmeaning
logs unlock drawing/no drawingstateseeded. Not ownerprogress/effectiveness.
Sole curated On persistedGood/Done1correct, no kun question/log.
Meaning feedback exits Back before Next: do not infer new persistedmeaninggrade.
Seven generated-reference touch strokes; ungradedtrace/model-unavailable
geometryfeedback/recallmiss/persistedDrawAgain are NOT MLKit recognition,
human successful handwriting/recall, reverse/negative geometry evidence.
Downloading label is not successful model download.
Offline/SystemBack API35/fontscale1/fingerprint
google/sdk_gphone64_x86_64/emu64xa:15/AE3A.240806.036/12592187:user/release-keys.
Native heapgrowth192m/heapsize576m unchanged. FreshAndroid483RealContent3+
RareHan1 inherited, not rerun. Owned helpers stopped; preexisting5556preserved.
Historical denials/HOST OOMs retained; HOST-onlyheapinit NEVER nativeauthorization.

Return COMPLETE Snapshot/Scope/Verdicts/Findings/Optional/Limits report.
Separate correctness/scopedcoverage/comprehensibility CLEAN/NEEDS FIX/
UNVERIFIED verdicts for whole克,exact reused克服line24,exact服line21.
Separate inherited lexical conclusions, new pixels, supplied runtimeassertions.
Enumerate actual18images and complete text ranges/deviations. Findings need
severity/facet/exactPNG location or filelines/impact/remedy/evidence/confidence.
No quota; optional polish not blocker. Unseen parts/fallbackface/physicalphone/
generalrelease/whole-set/latestmain/publication limits explicit.
CompatibleAndroidf9b59a2+ required. Finish COMPLETE report then EXIT.
No edits/questions/nextbatch/repeatedfull-dossierreads/nestedtasks.
"""
    TASK.write_text(task, encoding="utf-8")
    resources = FILES + images + [FIXTURE, F / "instrumentation.txt", F / "n1-073-article-route.json", index, TASK]
    resources += [V / f"batch-073-initial-{family}.md" for family in SESSIONS]
    save(L / "visual-freeze.json", {
        "execution": 486, "batch": "073", "evidenceHead": HEAD, "teachingSnapshot": TEACHING,
        "images": [str(path) for path in images], "assignedCaptures": 18, "archivedSourceCaptures": 30,
        "fixtureLines": len(FIXTURE.read_text(encoding="utf-8").splitlines()),
        "resourceHashes": {str(path): sha(path) for path in resources},
    })
    print("Early scope saved; exact native evidence verified; all18 unique image streams frozen.")


def run(family, repair=False):
    freeze()
    if family == "gpt":
        prior = load(V / "batch-073-visual-claude-execution.json")
        repair_record = load(V / "batch-073-visual-claude-serial-repair-execution.json")
        assert prior["exitCode"] == 0 and repair_record["processAndCoverageAccepted"]
        assert not subprocess.run(
            ["pwsh", "-NoProfile", "-Command", f"Get-Process -Id {prior['launcherPid']} -ErrorAction SilentlyContinue"],
            capture_output=True,
        ).stdout.strip(), "Prior reviewer must have exited"
    model, session = SESSIONS[family]
    prefix = "batch-073-visual-" + family
    if repair:
        assert family == "claude"
        prefix += "-serial-repair"
    raw = L / f"{prefix}.jsonl"
    assert not raw.exists(), "Never overwrite original execution"
    command = [
        shutil.which("copilot"), "-C", str(R), "--add-dir", str(C),
        "--model", model, "--session-id", session, "--no-ask-user",
        "--allow-all-tools", "--disable-builtin-mcps", "--available-tools=view",
        "--output-format", "json", "--log-dir", str(L / f"review-{family}"),
        "--usage-output-file", str(L / f"{prefix}-usage.json"),
        "-p", (
            "Read the entire bounded corrective task at " + str(L / "claude-serial-repair-task.txt")
            if repair else
            "These reads are DEPENDENT: after EVERY returned view, inspect its contents and identify one "
            "specific observation before selecting the next view. Parallel reads cannot satisfy this task. "
            "Read the ENTIRE shared bounded dependent visual task at " + str(TASK)
            + ". YOUR complete original initial report is " + str(V / f"batch-073-initial-{family}.md")
            + ". Exactly ONE view call per response; WAIT for result, inspect it, then select next. Never batch tools."
        ),
    ]
    env = os.environ.copy()
    env.pop("GH_TOKEN", None)
    env.pop("GITHUB_TOKEN", None)
    started = now()
    with raw.open("wb") as out, (L / f"{prefix}-stderr.txt").open("wb") as err:
        process = subprocess.Popen(command, stdout=out, stderr=err, env=env)
        save(L / f"{prefix}-active.json", {"pid": process.pid, "sessionId": session, "startedAt": started})
        print(f"Running original {family}: PID{process.pid} model{model}", flush=True)
        code = process.wait()
    save(L / f"{prefix}-process.json", {
        "launcherPid": process.pid, "startedAt": started, "completedAt": now(),
        "exitCode": code, "requestedModel": model, "sessionId": session, "snapshot": HEAD,
        "command": command, "priorProcessExitedBeforeLaunch": family == "gpt",
    })
    assert code == 0, f"Reviewer exit {code}; original output preserved"
    archive(family, repair)


def archive(family, repair=False):
    frozen = freeze()
    prefix = "batch-073-visual-" + family
    if repair:
        prefix += "-serial-repair"
    raw = L / f"{prefix}.jsonl"
    process = load(L / f"{prefix}-process.json")
    usage = load(L / f"{prefix}-usage.json")
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
                target = F.parent / f"visual-{family}{'-serial-repair' if repair else ''}-returned" / source.name
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
                b = len(lines) if b == -1 else min(b, len(lines))
                row["requestedRange"] = [a, b]
                row["exactRequestedTextContainedInResult"] = "\n".join(lines[a-1:b]) in text.replace("\r\n", "\n")
    required = FILES + [TASK, V / f"batch-073-initial-{family}.md", FIXTURE,
                        F / "instrumentation.txt", F / "n1-073-article-route.json"]
    if repair:
        required = [L / "claude-serial-repair-task.txt", FIXTURE, F / "instrumentation.txt",
                    F / "n1-073-article-route.json"]
    missing = []
    for path in required:
        covered = set()
        for row in calls.values():
            if Path(row["arguments"]["path"]) == path and row.get("exactRequestedTextContainedInResult"):
                a, b = row["requestedRange"]
                covered.update(range(a, b + 1))
        if covered != set(range(1, len(path.read_text(encoding="utf-8-sig").splitlines()) + 1)):
            missing.append(str(path))
    actual_images = {str(Path(row["arguments"]["path"])) for row in calls.values() if "imagePayload" in row}
    allowed = {str(path) for path in required} | set(frozen["images"])
    unexpected = [row["arguments"]["path"] for row in calls.values() if str(Path(row["arguments"]["path"])) not in allowed]
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
        "limits": "Dependent original-session confirmation;18unique source captures/30archived files. Exact returned bytes/ranges establish access, not comprehension. No reviewer native execution, fresh upstream retrieval, physical-phone or final publication acceptance.",
    }
    save(V / f"{prefix}-execution.json", record)
    print(json.dumps({key: record[key] for key in ("actualModels", "processAndCoverageAccepted",
                     "imagePayloadsVerified", "missingRequiredText", "observedToolOverlaps", "multiToolResponses")}))
    assert accepted


def prepare_repair():
    frozen = freeze()
    original = load(V / "batch-073-visual-claude-execution.json")
    assert original["exitCode"] == 0 and not original["missingRequiredText"]
    assert original["imagePayloadsVerified"] == 18 and original["multiToolResponses"] == 2
    task = """DEPENDENT corrective confirmation in SAME original Claude session.
Execution486; same frozen teaching and native evidence, NO edits.
Your report falsely claimed 'one view call at a time'. Actual execution shows
the five fixture ranges plus two operational files launched as one group of7,
then ALL18 PNG calls as one group of18. Original complete report/execution/
images are preserved. All bytes returned, but serial process contract FAILED.
No other reviewer report is supplied.

Perform ONE bounded repair ONLY of those overlapping reads. Do NOT re-read
the original task, original report, articles, dictionaries or other dossier.
These operations are DEPENDENT: inspect and explain each returned result
before deciding whether the next expected step is safe. In every response
use at most ONE view call. WAIT for the result. In the FOLLOWING response
give one concrete observation about that result BEFORE the next call.
Do not pre-issue any next call alongside the current call. No parallel wrapper.
This result-before-next decision is essential; reads are NOT independent.

First inspect native fixture as this dependent chain, five separate calls:
"""
    for a in range(1, frozen["fixtureLines"] + 1, 120):
        task += f"{FIXTURE} range[{a},{min(a+119, frozen['fixtureLines'])}]\n"
    task += f"""Then, each as a separate dependent result-before-next operation:
{F / "instrumentation.txt"}
{F / "n1-073-article-route.json"}

Then view these18PNGs IN ORDER, each only after the previous result has
returned and you have stated a concrete visual observation. Compare each to
the cumulative source/route evidence already inspected; do not infer pixels
from selectors or filenames:
"""
    task += "\n".join(frozen["images"])
    task += """

The original scope, inherited lexical conclusions and limitations remain.
Review complete new克, exact克服line24 link and服line21 sentence only.
Check both reading labels/explanations across complementary clipped table
views, isolated儿 and all27Han/克服 across4fontrows, actual meaning and sole
curatedOn choices/feedback/1of1Done, drawing/reference/recall, backlink,
selection. Some source footer may be below frame. Native is supplied API35
emulator evidence, not phone/MLKit/humanrecall/fallback-face identity.

Return COMPLETE Snapshot/Scope/Verdicts/Findings/Optional/Limits report.
Explicitly correct the false serial-execution statement in original report.
Record exact newly inspected ranges/images; no fresh blind initial review.
Reassess optional stroke-number observation using actual new pixels; if it is
a consequential established defect report severity/evidence/remedy, otherwise
keep it optional or qualify/withdraw. Do not invent a finding quota.
Finish and EXIT. No source/device work, delegation, edits or batch074.
"""
    save(L / "claude-serial-deviation.json", {
        "originalExecutionSha256": sha(V / "batch-073-visual-claude-execution.json"),
        "originalReportSha256": sha(V / "batch-073-visual-claude.md"),
        "allAssignedBytesReturned": True, "serialProcessAccepted": False,
        "multiToolResponses": 2, "overlapStarts": len(original["observedToolOverlaps"]),
        "repair": "One bounded same-session result-before-next dependent repair of overlapping fixture/receipts/18PNG only.",
    })
    (L / "claude-serial-repair-task.txt").write_text(task, encoding="utf-8")
    print("Original deviation preserved; bounded dependent serial repair prepared.")


def record():
    frozen = freeze()
    reviews = {}
    ordered = []
    for family in ("claude", "claude-serial-repair", "gpt"):
        path = V / f"batch-073-visual-{family}-execution.json"
        item = load(path)
        assert item["exitCode"] == 0
        expected = SESSIONS["gpt" if family == "gpt" else "claude"]
        assert item["actualModels"] == [expected[0]] == [item["usage"]["currentModel"]]
        assert item["sessionId"] == expected[1]
        assert not item["missingRequiredText"] and not item["unfinishedTools"] and not item["unexpectedReadPaths"]
        assert item["imagePayloadsVerified"] == 18 and item["expectedPngMembershipReturned"]
        assert item["processAndCoverageAccepted"] == (family != "claude")
        if family != "claude":
            assert not item["observedToolOverlaps"] and not item["multiToolResponses"]
        assert sha(Path(item["rawExecutionLocation"])) == item["rawExecutionSha256"]
        report = V / f"batch-073-visual-{family}.md"
        assert sha(report) == item["reportSha256"]
        assert not subprocess.run(
            ["pwsh", "-NoProfile", "-Command", f"Get-Process -Id {item['launcherPid']} -ErrorAction SilentlyContinue"],
            capture_output=True,
        ).stdout.strip(), "Reviewer must have exited"
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
            "report": str(report.relative_to(R)), "reportSha256": sha(report),
            "execution": str(path.relative_to(R)), "executionSha256": sha(path),
            "actualModel": expected[0], "sessionId": expected[1],
            "startedAt": item["startedAt"], "completedAt": item["completedAt"],
            "exitCode": 0, "toolCalls": len(item["toolCalls"]), "verifiedReturnedImages": 18,
            "processAndCoverageAccepted": item["processAndCoverageAccepted"],
            "toolOverlapStarts": len(item["observedToolOverlaps"]), "multiToolResponses": item["multiToolResponses"],
        }
        ordered.append(item)
    for first, second in zip(ordered, ordered[1:]):
        assert datetime.fromisoformat(first["completedAt"]) < datetime.fromisoformat(second["startedAt"])
    for source in frozen["images"]:
        copies = [F.parent / f"visual-{name}-returned" / Path(source).name for name in reviews]
        assert len({sha(path) for path in copies}) == 1
    checks = {}
    for name in ("validate", "manifest", "budget"):
        source = L / f"{name}.txt"
        target = V / f"batch-073-visual-{name}-execution-486.txt"
        shutil.copyfile(source, target)
        checks[name] = {"path": str(target.relative_to(R)), "sha256": sha(target), "exitCode": 0}
    for name in ("help", "models"):
        shutil.copyfile(L / f"copilot-{name}.txt", V / f"batch-073-visual-{name}-execution-486.txt")
    save(V / "batch-073-visual-freeze.json", frozen)
    shutil.copyfile(L / "claude-serial-repair-task.txt", V / "batch-073-visual-claude-serial-repair-task.txt")
    shutil.copyfile(L / "claude-serial-deviation.json", V / "batch-073-visual-claude-serial-deviation.json")
    limits = (
        "Dependent original-session confirmation, not new blind initial review or upstream retrieval. "
        "Original Claude visual pass violated internal serial contract:7text and18PNG batched; "
        "its false serial claim is corrected in same-session bounded serial repair. All original "
        "reports/executions/payloads preserved. Reviewer processes never overlapped. Repair and "
        "GPT each internally serial, zero overlaps. Returned bytes/ranges establish access, not "
        "comprehension.18unique source captures/30originalfiles;12duplicates not freshly inspected. "
        "All54returned payloads900x2000 from1080x2400, identical per source across three executions; "
        "not everypixel/viewport/gesture/physicalviewingsize proof. Complementary tables clip "
        "different columns; source footer at lower edge. No fallback-face identity/every-phone "
        "certificate. Initial lexical/source/optional limits inherited. Native485/Android483 "
        "not rerun. No reviewer device execution, new persisted meaning grade, MLKit/human "
        "handwriting/successful recall/model download/reverse or negative geometry evidence. "
        "Current-main/CI/public ZIP/physical-phone/general-release/whole-set acceptance remains "
        "outstanding. CompatibleAndroidf9b59a2+ required. No runtime edits/publication/guard/heap changes."
    )
    reconciliation = {
        "schemaVersion": 1, "execution": 486, "batch": "073",
        "status": "bounded-visual-confirmation-closed-awaiting-integration",
        "evidenceHead": HEAD, "reviewedTeachingSnapshot": TEACHING, "dependentNotBlind": True,
        "models": [pair[0] for pair in SESSIONS.values()],
        "scope": "Whole new kanji/克.md; exact reused words/克服.md:24 link-only passage and kanji/服.md:21 sentence. Whole reused files as context only. Each family received complete521line fixture, terminal log/route and18uniquePNG. Original lexical conclusions inherited.",
        "allReviewerProcessesSerialAndExited": True,
        "allHistoricalInternalCallsSerial": False,
        "acceptedRepairAndGPTInternalCallsSerial": True,
        "findings": [],
        "verdicts": {
            path: {"correctness": "CLEAN", "scopedCoverage": "CLEAN", "boundedVisualComprehensibility": "CLEAN"}
            for path in ("kanji/克.md", "words/克服.md:24 link-only passage", "kanji/服.md:21 sentence")
        },
        "observations": [
            "No new actionable teaching/rendering defect established by either family. Initial bounded lexical verdicts retained; no teaching/app changes.",
            "Four production rows show all27Han and克服 readable, including isolated儿 and克/古/兄/元/己/勝/服 contrasts. Textbook isolated儿 visibly heavier, but actual fallback face unidentified.108singlePaint+4word probes do not prove all-phone readability.",
            "Complementary table views show both labels and complete examples/explanations, with differing horizontal clipping and explicit scroll hint. Rare spelling克つ, ordinary pronunciationかつ, attested己に克つ and nonabsolute克/勝 distinction remain legible. Rawコク/か.つ retained; selectedコク only normalizedこく.",
            "Complete new mnemonic and substantive notes, exact克服line24 links and服line21 sentence visible. Four reciprocal directions/SystemBack supported by supplied fixture/receipts and representative static destinations, not independently performed gestures. No new support word/title/exclusion.",
            "Actual meaning choices chrysanthemum/strange;extraordinary/overcome/vertebra;chinquapin are distinct, NOT authored古兄元 or whole-pool certification. Actual Onコウ/キク/ヤク/コク with correctコク feedback/Done1of1. Full feedback retainsかつ, but no kun question/log within supplied bounded fixture.",
            "Inherited485native both named terminal0/no skips82.165s; full productionContentSyncONCE1085kanji5042words105N1/problems0/version1d8a4ee1a97c6bb5/epoch1. Disposable synthetic source, otherN1postponed/twohistoricalGoodmeaninglogs/no drawingstateseeded. SolecuratedOnGood persisted; meaning exits before Next. Sevenreference touch strokes/ungradedtrace/model-unavailablegeometry/recallmiss/persistedDrawAgain not human handwriting/MLKit.",
        ],
        "processDeviation": {
            "status": "resolved",
            "originalPassAcceptedAsSerial": False,
            "actual": "Original Claude30calls: one batch7fixture/receipt reads and one batch18PNG;23overlap starts,2multi-tool responses. All assigned bytes returned. Original claim 'one view call at a time' false.",
            "remedy": "One bounded SAME-session dependent result-before-next repair26singleviewcalls covering only overlapping5fixture ranges+2receipts+18PNG and corrective task. Zero overlaps/multi-tool responses. Original report/execution/payloads retained and repair explicitly corrects claim. GPT30calls then serial with zero overlaps.",
            "firstOriginalProcessExitBeforeRepair": True,
            "repairCompleteArchiveBeforeGPT": True,
            "originalEvidence": "batch-073-visual-claude-serial-deviation.json",
        },
        "optional": [
            {
                "status": "optional", "reportedBy": ["Claude"],
                "claim": "Clarify十 above兄-like shape and mention克明.",
                "decision": "Retain482 nonblocking dispositions; no new content defect, source claim or support requirement.",
            },
            {
                "status": "optional", "reportedBy": ["Claude original visual and serial repair"],
                "claim": "Stroke-number labels6/7 sit between lower strokes or inside mouth-like box in trace/recall; app-side placement may be clearer.",
                "evidence": "n1-073-drawing-trace.png, drawing-feedback.png and drawing-recall-feedback.png directly inspected by coordinator.6 lies between lower stroke starts;7 is higher near lower horizontal. Correct seven generated reference paths retained and injected in order.",
                "decision": "Localized label proximity is observed, not an established wrong stroke/path/order or unreadable glyph. Preserve as nonblocking app-side polish, moderate-confidence learning-impact hypothesis; no app/geometry change authorized or made. Proposed placement heuristic cause not independently verified. GPT reports no finding; no forced agreement.",
            },
        ],
        "hypothesisDispositions": [
            {
                "status": "withdrawn",
                "claim": "Claude repair inherits earlier tension between historical enemy-submission sense and unchanged modern克服 distinction.",
                "decision": "Keep482 precise reconciliation: unchanged text says 'not a general word', not 'never'; historically sourced1930 usage does not establish unrestricted modern substitution. No changed teaching claim or new lexical evidence. Original reports retained; no reopened full dossier or extra review.",
                "evidence": "batch-073-reconciliation.json hypothesisDispositions and its preserved source records.",
            }
        ],
        "reportQualifications": [
            "Reviewers lack Git/shell. Coordinator verified exact freeze/no teaching diff and report hashes; initial reports unmodified.",
            "Fallback-looking style does not establish actual typeface identity. Seven-stroke reference inspection is not independent historical standardization/recognition.",
            "Claude calls source footer complete; GPT notes lower-edge visibility. Coordinator's direct kanji-17 view shows link text near lower edge. Preserve conservative viewport limitation, not universal footer visibility.",
            "Original Claude serial claim explicitly superseded by raw execution and corrective report; do not erase original deviation or describe all historical tool execution as serial.",
        ],
        "modelContributionComparison": {
            "matchedScope": "Same frozen teaching/native fixture/receipts/18identical returned PNG payloads, dependent confirmations.",
            "shared": "No actionable teaching/rendering defect; scoped glyph/reading/route acceptance with phone/source limits.",
            "uniqueVerifiedClaudeDefects": [], "uniqueVerifiedGPTDefects": [],
            "qualification": "Claude optional label proximity retained as optional hypothesis, not unique established defect. Compare findings/optional/limits together; no model benchmark or finding quota.",
        },
        "payloadAccounting": {
            "archivedSourceCaptures": 30, "assignedUniqueSourceCaptures": 18,
            "otherByteIdenticalSourceFiles": 12, "claudeOriginalPayloads": 18,
            "claudeSerialRepairPayloads": 18, "gptPayloads": 18, "totalReturnedPayloads": 54,
            "sourceDimensions": [1080, 2400], "returnedDimensions": [900, 2000],
            "sameReturnedBytesAcrossAllThree": True, "actualImagePaths": frozen["images"],
        },
        "inheritedEvidence": {
            "textual": "batch-073-reconciliation.json/execution482 unchanged; original reports/range receipts retained.",
            "android": "execution-483.json freshRealContentTest3+RareHanTest1, not rerun.",
            "native": "execution-485.json two named terminal0/no skips82.165s, not rerun.",
        },
        "reviews": reviews, "checks": checks, "boundedIndependentVisualConfirmation": True,
        "runtimeAccepted": False, "runtimePublished": False, "limits": limits, "nextAction": NEXT,
    }
    save(V / "batch-073-visual-reconciliation.json", reconciliation)
    manifest = load(R / "manifest.json")
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest
    assert manifest == build_manifest(R)
    count = sum(len(section) for section in manifest.values() if isinstance(section, dict))
    assert count == 8346
    result = {
        "schemaVersion": 1, "execution": 486, "checkpoint": 486, "batch": "073",
        "status": reconciliation["status"], "startingHead": HEAD, "reviewedTeachingSnapshot": TEACHING,
        "authorization": load(L / "starting-state.json")["authorization"],
        "scope": load(L / "starting-state.json")["scope"], "reviews": reviews,
        "reconciliation": r"docs\n1-reviews\batch-073-visual-reconciliation.json",
        "reconciliationSha256": sha(V / "batch-073-visual-reconciliation.json"),
        "boundedIndependentVisualConfirmation": True, "allReviewerProcessesSerialAndExited": True,
        "allHistoricalInternalCallsSerial": False, "acceptedRepairAndGPTInternalCallsSerial": True,
        "allOriginalReportsAndTeachingUnmodified": True, "runtimeEditsMade": False,
        "nativeOrAndroidRerun": False, "publicationAttempted": False, "runtimePublished": False,
        "publishedAdditions": 99, "remainingAdditions": 1129, "phoneEvidence": False,
        "wholeProjectComplete": False, "nextAction": NEXT, "blocker": None, "limits": limits,
        "checks": checks, "recordedAt": now(),
        "evidenceWhitespace": {
            "initialCachedDiffCheckExitCode": 2,
            "affectedFile": "docs/n1-reviews/batch-073-visual-models-execution-486.txt",
            "disposition": "Raw current CLI catalog ends with a blank line. Preserve actual output bytes/hash; check every other staged file separately. Initial check chain stopped before any signing command.",
        },
        "coordinatorDirectImageChecks": ["n1-073-kanji-17.png", "n1-073-drawing-trace.png",
                                       "n1-073-drawing-feedback.png", "n1-073-drawing-recall-feedback.png"],
        "checksSummary": {
            "validatorErrors": 0, "manifestFresh": True, "runtimeHashesVerified": count,
            "contentVersion": "1d8a4ee1a97c6bb5",
            "budget": {"entries": 8368, "localZipBytes": 30144262, "inflatedBytes": 44368710,
                       "retainedBytes": 44100372}, "originalLimitsUnchanged": True,
        },
    }
    save(R / "docs" / "n1-sources" / "execution-486.json", result)
    batch = load(R / "docs" / "n1-sources" / "batch-073-progress.json")
    batch.update(status=reconciliation["status"], nextAction=NEXT, limits=limits)
    batch["visualReviewCheckpoint"] = {
        "execution": 486, "evidenceHead": HEAD, "reviewedSnapshot": TEACHING,
        "reconciliation": str((V / "batch-073-visual-reconciliation.json").relative_to(R)),
        "reconciliationSha256": result["reconciliationSha256"],
        "boundedIndependentVisualConfirmation": True, "runtimePublished": False,
        "originalClaudeSerialDeviationPreservedAndRepaired": True,
    }
    save(R / "docs" / "n1-sources" / "batch-073-progress.json", batch)
    receipts = V / "batch-073-visual-receipts"
    receipts.mkdir(exist_ok=True)
    shutil.copyfile(Path(__file__), receipts / "execution-486.py")
    print("Three original reports/executions,54returned payloads and qualified reconciliation preserved.")


def checkpoint():
    progress = load(C / "progress.json")
    before = load(L / "before-progress.json")
    assert progress["checkpoint"] == 485
    for key, value in before.items():
        if key not in {"stage", "nextAction"}:
            assert progress[key] == value, key
    head = git("rev-parse", "HEAD")
    assert head != HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    record_path = R / "docs" / "n1-sources" / "execution-486.json"
    receipt = {
        "execution": 486, "checkpoint": 486, "batch": "073", "status": "continue",
        "savedCommit": head, "signature": "G", "record": str(record_path.relative_to(R)),
        "recordSha256": sha(record_path), "runtimePublished": False,
        "boundedIndependentVisualAcceptance": True,
        "originalClaudeSerialDeviationPreservedAndRepaired": True, "nextAction": NEXT,
        "publishedAdditions": 99, "remainingAdditions": 1129,
        "allOriginalHistoricalRootKeysPreserved": True,
    }
    progress.update(checkpoint=486, status="continue", stage="batch-073-visual-closed-awaiting-integration",
                    nextAction=NEXT, blocker=None)
    progress["execution486StartingState"]["status"] = "signed-dependent-visual-checkpoint-complete"
    progress["execution486CoordinatorCheckpoint"] = receipt
    progress["batch073VisualCheckpoint"] = receipt.copy()
    save(C / "progress.json", progress)
    save(L / "checkpoint-full.json", progress)
    save(L / "execution-486-checkpoint.json", receipt)
    body = f"""N1 kanji batch 073: bounded visual confirmation checkpoint 486 saved locally at signed `{head}`; **not published**.

Original reviewers Claude Opus 5.5 and GPT-6.1 Sol confirmed complete new 克 and exact reused 克服 link/服 sentence against the same frozen teaching and native evidence. All three scoped facets CLEAN; no actionable content defect established. Complete reports, actual model/session/process/range evidence and 54 returned image payloads are preserved. Claude's first visual pass batched 7 text reads and 18 images despite the serial requirement and falsely claimed serial reads; original evidence is retained. One bounded same-session serial repair corrected that claim and reread only affected evidence before GPT started. Repair and GPT each have zero internal overlaps. No new blind initial review or native rerun is claimed.

Both families inspected 18 unique source PNGs (12 other captures are byte duplicates), complete 521-line fixture and terminal/route receipts. Four font rows, isolated 儿, both raw reading dispositions, sole curated コク/Done 1 of 1, reciprocal links, meaning, reference tracing/recall and offline/System Back evidence accepted within the bounded emulator scope. Source/right-offset table clipping, unidentified fallback face, label6/7 proximity as optional app-side polish and other original evidence limits remain explicit. No app/content/geometry changes. Fresh content validation, unchanged manifest (8,346 runtime hashes, version `1d8a4ee1a97c6bb5`) and original budgets pass.

Next: fresh-main nonrewriting integration and combined validation, normal signing, authorized owner fast-forward publication, terminal green CI and every immutable public ZIP runtime hash/budget before delivery or batch074. No batch074 started. Published additions remain **99/1,228**, remaining **1,129**; 100 published necessary supports are not an N1 vocabulary deck. Compatible Android `f9b59a2+` required. Physical-phone, general-release and whole-set acceptance remain outstanding.
"""
    (L / "issue-486-body.txt").write_text(body, encoding="utf-8")
    print(json.dumps({key: receipt[key] for key in ("checkpoint", "savedCommit", "signature", "status", "runtimePublished")}))


def finalize():
    progress = load(C / "progress.json")
    before = load(L / "before-progress.json")
    assert progress["checkpoint"] == 486 and progress["status"] == "continue"
    for key, value in before.items():
        if key not in {"checkpoint", "stage", "nextAction"}:
            assert progress[key] == value, key
    head = git("rev-parse", "HEAD")
    assert head == progress["execution486CoordinatorCheckpoint"]["savedCommit"]
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    android = C.parent / "kanji-cards-android"
    assert not subprocess.check_output(["git", "-C", str(android), "status", "--porcelain"], encoding="utf-8").strip()
    for path, digest in load(L / "visual-freeze.json")["resourceHashes"].items():
        assert sha(Path(path)) == digest, path
    record_path = R / "docs" / "n1-sources" / "execution-486.json"
    assert sha(record_path) == progress["execution486CoordinatorCheckpoint"]["recordSha256"]
    result = load(record_path)
    assert sha(R / result["reconciliation"]) == result["reconciliationSha256"]
    for review in result["reviews"].values():
        assert sha(R / review["report"]) == review["reportSha256"]
        assert sha(R / review["execution"]) == review["executionSha256"]
        item = load(R / review["execution"])
        assert sha(Path(item["rawExecutionLocation"])) == item["rawExecutionSha256"]
        for row in item["toolCalls"]:
            if "imagePayload" in row:
                payload = row["imagePayload"]
                assert sha(R / payload["returnedPayloadCopy"]) == payload["sha256"]
    api = load(L / "issue-486-api.json")
    receipt = load(L / "issue-486-verified.json")
    assert receipt["author"] == api["user"]["login"] == "stop-cran" and receipt["bodyVerified"]
    assert api["body"].replace("\r\n", "\n").rstrip() == (L / "issue-486-body.txt").read_text(encoding="utf-8").rstrip()
    progress["batch073VisualIssueReceipt"] = receipt
    for key in ("execution486CoordinatorCheckpoint", "batch073VisualCheckpoint"):
        progress[key]["issueUpdate"] = receipt["url"]
        progress[key]["ownerAuthorAndBodyVerified"] = True
    save(C / "progress.json", progress)
    save(L / "checkpoint-full.json", progress)
    save(L / "execution-486-checkpoint.json", progress["execution486CoordinatorCheckpoint"])
    save(L / "execution-486-final-verification.json", {
        "execution": 486, "checkpoint": 486, "status": "continue", "batch": "073",
        "savedCommit": head, "signature": "G", "contentAndAndroidClean": True,
        "historicalRootValuesPreserved": True, "reviewerProcessesExitedSerially": True,
        "acceptedRepairAndGPTInternallySerial": True, "originalDeviationPreserved": True,
        "returnedPayloadsVerified": 54, "runtimePublished": False,
        "issueReceipt": receipt, "verifiedAt": now(),
    })
    print("Checkpoint486 verified: signed local evidence, complete historical values preserved, owner issue receipt; status continue.")


if __name__ == "__main__":
    if sys.argv[1] == "prepare":
        prepare()
    elif sys.argv[1] == "run":
        run(sys.argv[2])
    elif sys.argv[1] == "repair":
        run("claude", True)
    elif sys.argv[1] == "prepare-repair":
        prepare_repair()
    elif sys.argv[1] == "record":
        record()
    elif sys.argv[1] == "checkpoint":
        checkpoint()
    elif sys.argv[1] == "finalize":
        finalize()
    else:
        raise ValueError(sys.argv[1])

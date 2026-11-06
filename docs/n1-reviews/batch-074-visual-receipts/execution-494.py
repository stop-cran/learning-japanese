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
F = V / "batch-074-native" / "attempt-3"
HEAD = "564561b6ef566d6117fd9c70e41f12158589fc7e"
TEACHING = "75fbfc7dc734c7ff5d9771fbd5103afd3f3fdc1c"
TASK = V / "batch-074-visual-task.txt"
FIXTURE = F / "N1Batch074NativeTest.kt"
FILES = [R / "kanji" / "免.md", R / "words" / "免れる.md",
         R / "words" / "免許.md", R / "words" / "免税.md", R / "kanji" / "許.md"]
SESSIONS = {
    "claude": ("claude-opus-5.5", "af76d4d5-df98-409c-a302-d8d9fd63f45d"),
    "gpt": ("gpt-6.1-sol", "c7f3d66f-c4ff-479b-82cb-957c2f7913ec"),
}


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


def prepare():
    assert git("rev-parse", "HEAD") == HEAD and not git("status", "--porcelain")
    assert git("log", "-1", "--format=%G?") == "G"
    text = (L / "request.txt").read_text(encoding="utf-8-sig")
    embedded = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    progress = load(C / "progress.json")
    assert embedded["checkpoint"] == progress["checkpoint"] == 493
    assert progress["batch"] == "074"
    shutil.copyfile(C / "progress.json", L / "before-progress.json")
    start = {
        "execution": 494, "batch": "074", "startingHead": HEAD, "recordedAt": now(),
        "scope": "SAME074 two serial original-session dependent visual confirmations, exact payload/range/process archival, reconciliation and normally signed local evidence checkpoint only. No native/HOST rerun, publication,075 or second runner.",
        "authorization": {
            "requestSha256": sha(L / "request.txt"), "characters": len(text),
            "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request acquired and embedded checkpoint parsed; operative contract, entire approved issue and final493 inspected directly. Historical middle parsed, not freshly semantically re-reviewed. First console enumeration failed cp1252 after successful parse; diagnostic retained.",
        },
        "status": "preparing-dependent-visual-confirmation",
    }
    save(L / "starting-state.json", start)
    progress["execution494StartingState"] = start
    progress.update(stage="batch-074-dependent-visual-confirmation-preparing", nextAction=start["scope"])
    save(C / "progress.json", progress)
    index = V / "batch-074-native" / "execution-493-artifact-index.json"
    native = load(index)
    for row in native["files"]:
        path = R / row["path"]
        assert sha(path) == row["sha256"] and path.stat().st_size == row["bytes"], path
    images = []
    seen = set()
    for path in sorted(F.glob("*.png")):
        digest = sha(path)
        if digest not in seen:
            images.append(path)
            seen.add(digest)
    assert len(images) == 32 and len(list(F.glob("*.png"))) == 57
    for args, label in [(["--help"], "help"), (["help", "config"], "models")]:
        result = subprocess.run([shutil.which("copilot"), *args], capture_output=True, encoding="utf-8", check=True)
        (L / f"copilot-{label}.txt").write_text(result.stdout, encoding="utf-8")
    catalog = (L / "copilot-models.txt").read_text(encoding="utf-8")
    assert all(model in catalog for model, _ in SESSIONS.values())
    task = f"""SAME074 DEPENDENT original-session visual confirmation, execution494.
NOT a new blind initial review, fresh dictionary audit or native rerun.
Evidence HEAD {HEAD}; teaching unchanged from {TEACHING}.
Exact full native Git envelope4078c7d42e6bc2173c555e73d0bd39fb5d69eb08.

STRICT DEPENDENT SERIAL TOOL CONTRACT:
Exactly ONE view call in each response. WAIT for its result. In your NEXT
response, state ONE concrete observation from that returned resource BEFORE
deciding the next view. Every next step depends on the preceding result.
Never multiple tool calls, batches or parallel wrappers. Only view available.
No shell/edit/search/delegation/device operations. Read this COMPLETE task
and YOUR complete original initial and textual confirmation reports identified
at launch. Do not read the other reviewer's reports or author adjudication.
Inherit lexical conclusions and original optional/source/process limits.
Initial Claude ONE concurrent兄/元 read remains historical, not erased here.
No fresh upstream retrieval or rereading of complete dictionary dossiers.

Read each COMPLETE teaching file singly:
"""
    task += "\n".join(str(path) for path in FILES)
    task += f"""
Review complete NEW免 and NEW免れる; reused免許 ONLY line25 link,
免税 ONLY line26 link, 許 ONLY line38 new example. Complete reused files
are context, NOT fresh whole-article certification.
Read COMPLETE native fixture in separate inclusive ranges <=120lines:
{FIXTURE}
Use [1,120],[121,240],... through EOF, including middle ranges.
Actual fixture has {len(FIXTURE.read_text(encoding="utf-8").splitlines())} lines.
Then read COMPLETE each small operational receipt separately:
{F / "instrumentation.txt"}
{F / "n1-074-article-route.json"}

Actually VIEW each of these32 UNIQUE PNGs IN ORDER, ONE PER RESPONSE,
only after the preceding result has returned and been inspected:
"""
    task += "\n".join(str(path) for path in images)
    task += """

These are32/57 source PNGs; remaining25 exact-byte duplicates are hash-mapped,
NOT additional fresh visual reads. Do not infer visibility from selectors,
filenames or assertions. State unseen/clipped parts. Source1080x2400 may be
resized by view; disclose transport/viewport limitations. Full projection is
not every-character viewport evidence. Left/right table views complement:
inspect actual labels AND linked examples/qualified alternate explanation,
not solely one column. Explicit horizontal-scroll hint is not proof every
gesture/offset worked. New word final external source-link line below notes
frame is a viewport limit, not necessarily a substantive teaching defect.

Inspect all43 authoredHan plus免れる/免許/免税 across FOUR production rows:
任 使 儿 元 兄 先 免 助 午 去 取 口 可 品 商 年 幸 店 持 救 方 書 格 無 物
税 舌 見 言 訪 許 証 話 課 責 買 資 転 辞 逃 運 避 金
Check readable/distinguishable, no blank/replacement boxes,免/兄/元/先,
isolated儿 and許/税. Typeface changes/coinciding styles alone not defects.
172singlePaint+12wholeword rasters support nonblankness/distinct rasters,
NOT actual fallback-face identity/every-phone readability. Eight strokes;
indexing radical儿10, explicitly labelled modern-shape mnemonic not origin.

Full+Lite raw on[メン],kun[まぬか.れる,まぬが.れる] source order.
Curated on[メン],kun[まぬが.れる]; normalizedめん/まぬがれる.
Both pronunciations valid; excluded alternate is NOT rare or wrong.
Avoid duplicate variant questions. Dot is written ending boundary.
Both actual offered kinds must be checked in question/feedback/2of2Done.
Match actual shown options, not solely authored distractors兄元先.
免れる ichidan, adverse eventを免れる, both voiced/unvoiced conjugations,
not passiveれる; lexicographic transitive/intransitive difference qualified.
No new JLPT word level from constituent kanji. Reused免許N3/免税N2 preserved.
Five reciprocalpairs10directions:
免↔免れる,免↔免許,免↔免税,許↔免許,税↔免税.
Supplied fixture/route and representative images support SystemBack/offline;
static screenshots do NOT prove reviewer independently performed gestures.

SUPPLIED operational results, NOT reviewer-executed:493attempt3 BOTH named
cases terminal0/no skips128.836s. Full productionContentSync ONCE:
1086kanji5043words106N1/problems0/versionc507eceeb764bc3f/epoch1.
Disposable synthetic source/HEAD, otherN1postponed/twohistoricalGoodmeaning
logs unlock drawing/no drawingstateseeded. Not ownerprogress/effectiveness.
Both actual curated kinds persistedGood/Done2correct; no alternate key/log.
Meaning feedback exits Back before Next: no newly persistedmeaninggrade.
Eight generated-reference touch strokes; ungradedtrace/model-unavailable
geometryfeedback/recallmiss/persistedDrawAgain are NOT MLKit recognition,
human successful handwriting/recall or reverse/negative geometry evidence.
Downloading label is not successful model download.
Offline/SystemBack API35/fontscale1/fingerprint
google/sdk_gphone64_x86_64/emu64xa:15/AE3A.240806.036/12592187:user/release-keys.
Nativeheapgrowth192m/heapsize576m unchanged. FreshAndroid491HOST3+1 inherited,
not rerun. Owned helpers stopped; preexisting5556preserved. Historical
denials/HOST OOMs retained; HOST-onlyheapinit NEVER nativeauthorization.
Attempt1 passed but ASCII filename filter lost27Unicode-named captures;
attempt2 ownership gate refused own shutdownTIME_WAIT/sharedADB SynSent;
attempt3 natural release/unchanged gate+ports+fixture+heaps+guards, all57PNGs.
Original attempts preserved, not denied permissions or weakened checks.

Return COMPLETE Snapshot/Scope/Verdicts/Findings/Optional/Limits report.
Separate correctness/scopedcoverage/comprehensibility CLEAN/NEEDS FIX/
UNVERIFIED verdicts for whole免,whole免れる,exact免許line25link,
exact免税line26link,exact許line38example. Inherit original lexical conclusions
separately from newly viewed pixels and supplied runtime assertions.
Enumerate actual32images and complete text ranges/deviations. Findings need
severity/facet/exactPNG location or filelines/impact/remedy/evidence/confidence.
No quota; optional polish is not a blocker. Actual glyph fallback face,
unseen parts, physicalphone/generalrelease/whole-set/latestmain/publication
limits explicit. CompatibleAndroidf9b59a2+ required.
Finish COMPLETE report and EXIT. No edits/questions/nextbatch/nestedtasks.
"""
    TASK.write_text(task, encoding="utf-8")
    resources = FILES + images + [FIXTURE, F / "instrumentation.txt",
                                F / "n1-074-article-route.json", index, TASK]
    resources += [V / f"batch-074-{kind}-{family}.md"
                  for family in SESSIONS for kind in ("initial", "confirmation")]
    save(L / "visual-freeze.json", {
        "execution": 494, "batch": "074", "evidenceHead": HEAD, "teachingSnapshot": TEACHING,
        "images": [str(path) for path in images], "assignedCaptures": 32, "archivedSourceCaptures": 57,
        "fixtureLines": len(FIXTURE.read_text(encoding="utf-8").splitlines()),
        "resourceHashes": {str(path): sha(path) for path in resources},
    })
    print("Early scope saved; exact native evidence verified; all32 unique source PNGs frozen.")


def freeze():
    frozen = load(L / "visual-freeze.json")
    assert git("rev-parse", "HEAD") == HEAD
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    for path, digest in frozen["resourceHashes"].items():
        assert sha(Path(path)) == digest, path
    return frozen


def run(family):
    freeze()
    if family == "gpt":
        prior = load(V / "batch-074-visual-claude-execution.json")
        assert prior["processAndCoverageAccepted"]
        assert not subprocess.run(
            ["pwsh", "-NoProfile", "-Command",
             f"Get-Process -Id {prior['launcherPid']} -ErrorAction SilentlyContinue"],
            capture_output=True).stdout.strip(), "Prior reviewer must have exited"
    model, session = SESSIONS[family]
    prefix = "batch-074-visual-" + family
    raw = L / f"{prefix}.jsonl"
    assert not raw.exists(), "Never overwrite original execution"
    prompt = (
        "Perform this DEPENDENT original-session confirmation. Every next read is contingent on "
        "your concrete observation of the previous result. Exactly ONE view call per response; "
        "WAIT for its result and state one observation before the next call. Never batch tools. "
        "Read ENTIRE task " + str(TASK)
        + ". YOUR complete original initial report: " + str(V / f"batch-074-initial-{family}.md")
        + "; YOUR complete textual confirmation: " + str(V / f"batch-074-confirmation-{family}.md")
        + ". Read both completely, singly. Then follow the task's dependent resource chain."
    )
    command = [
        shutil.which("copilot"), "-C", str(R), "--add-dir", str(C),
        "--model", model, "--session-id", session, "--no-ask-user",
        "--allow-all-tools", "--disable-builtin-mcps", "--available-tools=view",
        "--output-format", "json", "--log-dir", str(L / f"review-{family}"),
        "--usage-output-file", str(L / f"{prefix}-usage.json"), "-p", prompt,
    ]
    env = os.environ.copy()
    env.pop("GH_TOKEN", None)
    env.pop("GITHUB_TOKEN", None)
    started = now()
    with raw.open("wb") as out, (L / f"{prefix}-stderr.txt").open("wb") as err:
        process = subprocess.Popen(command, stdout=out, stderr=err, env=env)
        save(L / f"{prefix}-active.json", {
            "pid": process.pid, "sessionId": session, "startedAt": started})
        print(f"Running original {family}: PID{process.pid} model{model}", flush=True)
        code = process.wait()
    save(L / f"{prefix}-process.json", {
        "launcherPid": process.pid, "startedAt": started, "completedAt": now(),
        "exitCode": code, "requestedModel": model, "sessionId": session, "snapshot": HEAD,
        "command": command, "priorProcessExitedBeforeLaunch": family == "gpt",
    })
    assert code == 0, f"Reviewer exit {code}; original output preserved"
    archive(family)


def archive(family):
    frozen = freeze()
    prefix = "batch-074-visual-" + family
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
            calls[key] = {"name": data["toolName"], "arguments": data["arguments"],
                          "startedAt": event["timestamp"]}
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
                b = len(lines) if b == -1 else min(b, len(lines))
                row["requestedRange"] = [a, b]
                row["exactRequestedTextContainedInResult"] = "\n".join(lines[a-1:b]) in text.replace("\r\n", "\n")
    required = FILES + [TASK, FIXTURE, F / "instrumentation.txt", F / "n1-074-article-route.json"]
    required += [V / f"batch-074-{kind}-{family}.md" for kind in ("initial", "confirmation")]
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
    unexpected = [row["arguments"]["path"] for row in calls.values()
                  if str(Path(row["arguments"]["path"])) not in allowed]
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
        "limits": "Dependent original-session confirmation;32unique source captures/57archived files. Exact returned bytes/ranges establish access, not comprehension. No reviewer native execution, fresh upstream retrieval, physical-phone or final publication acceptance.",
    }
    save(V / f"{prefix}-execution.json", record)
    print(json.dumps({key: record[key] for key in ("actualModels", "processAndCoverageAccepted",
                     "imagePayloadsVerified", "missingRequiredText", "observedToolOverlaps", "multiToolResponses")}))
    assert accepted


if __name__ == "__main__":
    if sys.argv[1] == "prepare":
        prepare()
    elif sys.argv[1] == "run":
        run(sys.argv[2])

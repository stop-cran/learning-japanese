import ast
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
import uuid

L = Path(__file__).parent
C = L.parent.parent
R = C.parent / "learning-japanese"
V = R / "docs" / "n1-reviews"
F = V / "batch-075-native" / "attempt-1"
HEAD = "c42c80e2044ad0acebab8c1daf442d851e582c06"
TEACHING = "f5b70805d4a4a99d27036c71701277f1b8fc8b00"
TASK = V / "batch-075-visual-task.txt"
FIXTURE = F / "N1Batch075NativeTest.kt"
FILES = [R / "kanji" / "典.md", R / "words" / "香典.md"]
FILES += [R / "words" / (name + ".md") for name in ("典型", "古典", "百科事典", "辞典")]
FILES += [R / "kanji" / (name + ".md") for name in ("古", "辞", "百", "科", "事", "香", "型")]
SESSIONS = {
    "claude": ("claude-opus-5.5", "9fa0573b-2a16-4020-95ca-b6db67263344"),
    "gpt": ("gpt-6.1-sol", "f8bb1a1f-8f2e-469d-a486-7874e1b6f3da"),
}
PRIOR = C / "logs" / "df5c6afa-28bf-4236-a0a9-180cb2c31223" / "execution-494.py"


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


# Reuse the previously verified exact-range, returned-image and overlap archiver.
source = PRIOR.read_text(encoding="utf-8")
for node in ast.parse(source).body:
    if isinstance(node, ast.FunctionDef) and node.name == "archive":
        recipe = ast.get_source_segment(source, node).replace("074", "075")
        recipe = recipe.replace(
            'for kind in ("initial", "confirmation")]',
            'for kind in ("initial", "confirmation") if (V / f"batch-075-{kind}-{family}.md").exists()]',
        )
        recipe = recipe.replace("32unique source captures/57archived files", "51unique source captures/111archived files")
        exec(compile(recipe, str(PRIOR), "exec"))


def prepare():
    assert git("rev-parse", "HEAD") == HEAD and not git("status", "--porcelain")
    assert git("log", "-1", "--format=%G?") == "G"
    text = (L / "request.txt").read_text(encoding="utf-8-sig")
    embedded = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    progress = load(C / "progress.json")
    assert embedded["checkpoint"] == progress["checkpoint"] == 501 and progress["batch"] == "075"
    shutil.copyfile(C / "progress.json", L / "starting-progress.json")
    start = progress["execution502StartingState"]
    start["authorization"] = {
        "requestSha256": sha(L / "request.txt"), "characters": len(text),
        "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
        "limits": "Entire request loaded and checkpoint parsed; operative contract, final501 and complete approved issue inspected directly. Historical middle loaded/parsed, not freshly semantically re-reviewed.",
    }
    start["recordedAt"] = now()
    start["freshOriginMain"] = git("rev-parse", "origin/main")
    save(L / "starting-state.json", start)
    progress.update(stage="batch-075-dependent-visual-confirmation-preparing", nextAction=start["scope"])
    save(C / "progress.json", progress)
    native = load(R / "docs" / "n1-sources" / "execution-501.json")
    for row in native["artifacts"]:
        path = R / row["path"]
        assert sha(path) == row["sha256"] and path.stat().st_size == row["bytes"], path
    captures = sorted(F.glob("*.png"))
    groups = {}
    for path in captures:
        groups.setdefault(sha(path), []).append(path)
    images = [paths[0] for paths in groups.values()]
    assert len(images) == 51 and len(captures) == 111
    catalog = (L / "copilot-model-catalog.txt").read_text(encoding="utf-8-sig")
    assert all(model in catalog for model, _ in SESSIONS.values())
    task = f"""SAME075 DEPENDENT original-session visual confirmation, execution502.
NOT a new blind initial review, fresh dictionary audit or native rerun.
Evidence HEAD {HEAD}; teaching unchanged from {TEACHING}.
Exact full native Git envelope fba1a8868b82cd93d7bfaeae1080f5642bd92730.

STRICT DEPENDENT SERIAL TOOL CONTRACT:
Exactly ONE view call in each response. WAIT for its result. In your NEXT
response state ONE concrete observation from that returned resource BEFORE
deciding the next view. Every next step depends on the preceding result.
Never multiple tool calls, batches or parallel wrappers. Only view available.
No shell/edit/search/delegation/device operations. Read this COMPLETE task
and YOUR complete original initial report; Claude also reads its complete
textual confirmation identified at launch. GPT had no textual follow-up.
Do not read the other reviewer's reports or author adjudication.
Inherit lexical conclusions and original optional/source/process limits.
Initial Claude EIGHT multi-tool responses/THIRTY overlapping starts and false
serial claim remain historical, not erased by its later serial confirmation
or this pass. No fresh upstream retrieval or full dictionary reread required.

Read each COMPLETE teaching/context file singly:
"""
    task += "\n".join(str(path) for path in FILES)
    task += f"""
Review complete NEW典 and NEW香典; reused scope ONLY:
words/典型.md:24 link, words/古典.md:31 link,
words/百科事典.md:29 link, words/辞典.md:23 link;
kanji/古.md:38 example, kanji/辞.md:37 example,
kanji/百.md:22 link ONLY, kanji/科.md:41 example,
kanji/事.md:36 example, kanji/香.md:42 example.
Complete reused files and unchanged型 are CONTEXT, not fresh whole-article
certification. Do not reopen unchanged historical etymology claims.
Read COMPLETE native fixture in separate inclusive ranges <=120lines:
{FIXTURE}
Use [1,120],[121,240],... through EOF, including middle ranges.
Actual fixture has {len(FIXTURE.read_text(encoding="utf-8").splitlines())} lines.
Then read COMPLETE each small operational receipt separately:
{F / "instrumentation.txt"}
{F / "n1-075-article-route.json"}

Actually VIEW each of these51 UNIQUE PNGs IN ORDER, ONE PER RESPONSE,
only after preceding result has returned and been inspected:
"""
    task += "\n".join(str(path) for path in images)
    task += """

These are51/111 source PNGs; remaining60 exact-byte duplicates are hash-mapped,
NOT additional fresh visual reads. Do not infer visibility from selectors,
filenames or assertions. State unseen/clipped parts. Source1080x2400 may be
resized by view; disclose transport/viewport limitations. Full projection is
not every-character viewport evidence. Left/right table views complement:
inspect actual labels AND linked examples/source-only qualifications,
not solely one column. Horizontal-scroll hint is not proof every gesture
worked. Judge actual target passage, not unrelated adjacent screen clipping.

Inspect all117 scopedHan across FOUR production rows in panels1-5 and focused
panel6: 典/具/曲/共, isolated奠/亅/厂/艹/八 and sixwholewords
典型/古典/百科事典/辞典/香典/香奠. All117Han are enumerated in
fixture lines63-86. Check readable/distinguishable, no blank/replacement boxes.
Typeface changes/coinciding styles alone not defects.468singlePaint+24word
rasters support nonblankness/distinct rasters, NOT actual fallback-face
identity/every-phone readability. Eight strokes; indexing radical八12,
explicit modern-shape mnemonic not historical origin.

Full+Lite raw on[テン,デン],kun[ふみ,のり] source order.
Curated on[テン,デン],kun[]; normalizedてん/でん offered, no kun.
Source-only does NOT mean nonexistent/incorrect/names-only. Both selected
readings need actual words: テン in辞典/典型/古典, デン in香典.
No unrestricted voicing rule. Both actual on keys checked in question/
feedback/2of2Done, no kun log. Match actual shown options, not solely
authored distractors具/曲/共 or unspecified live/random pools.
New香典 no inferred wordJLPT; reused wordN3/N2/N2/N4 preserved.
Distinguish funeraloffering from funeral/incense; usuallymoney allowsgoods;
香奠 rarity attaches to spelling, not reading; コウ+デン and objectを.
辞典/事典 contrast includes wholeword百科辞典 alias qualification.

Twelve reciprocalpairs/24directions:
典-典型,型-典型;典-古典,古-古典;
百-百科事典,科-百科事典,事-百科事典,典-百科事典;
辞-辞典,典-辞典;香-香典,典-香典.
Supplied fixture/route and representative images support SystemBack/offline;
static screenshots do NOT prove reviewer independently performed gestures.

SUPPLIED operational results, NOT reviewer-executed:501attempt1 BOTH named
cases terminal0/no skips234.957s. Full productionContentSync ONCE:
1087kanji5044words107N1/problems0/version2759d7b13c89eb8f/epoch1.
Disposable synthetic source/HEAD, otherN1postponed/twohistoricalGoodmeaning
logs unlock drawing/no drawingstateseeded. Not ownerprogress/effectiveness.
Both actual curated onkeys persistedGood/Done2correct; no kun key/log.
Meaning feedback exits Back before Next: no newly persistedmeaninggrade.
Eight generated-reference touch strokes; ungradedtrace/model-unavailable
geometryfeedback/recallmiss/persistedDrawAgain are NOT MLKit recognition,
human successful handwriting/recall or reverse/negative geometry evidence.
Downloading label is not successful model download.
Offline/SystemBack API35/fontscale1/fingerprint
google/sdk_gphone64_x86_64/emu64xa:15/AE3A.240806.036/12592187:user/release-keys.
Nativeheapgrowth192m/heapsize576m unchanged. FreshAndroid499HOST3+1 inherited,
not rerun. Owned5580parent24028/QEMU30848 stopped; shared5556/10668/18200
preserved. Residual post-stopTCP states preserved, no blanket absentTCP claim.
HOST-only2GiBinit NEVER nativeauthorization. No guard/heap/app changes.
Inherited accepted074/all40font160probes/sevenvisual inspections are historical
evidence, not fresh review here. Preserve baseline虎/猿/丘/山exceptions.

Return COMPLETE Snapshot/Scope/Verdicts/Findings/Optional/Limits report.
Separate correctness/scopedcoverage/comprehensibility CLEAN/NEEDS FIX/
UNVERIFIED verdicts for the TWO whole new articles and TEN exact reused
changed passages. Inherit original lexical conclusions separately from newly
viewed pixels and supplied runtime assertions. Enumerate actual51images
and complete text ranges/deviations. Findings need severity/facet/exactPNG
location or filelines/impact/remedy/evidence/confidence. No finding quota.
Optional polish is not blocker. Actual glyphfallbackface, unseenparts,
physicalphone/generalrelease/whole-set/latestmain/publication limits explicit.
CompatibleAndroidf9b59a2+ required.
Finish COMPLETE report and EXIT. No edits/questions/nextbatch/nestedtasks.
"""
    TASK.write_text(task, encoding="utf-8")
    resources = FILES + images + [FIXTURE, F / "instrumentation.txt",
                                F / "n1-075-article-route.json", TASK]
    resources += [V / f"batch-075-initial-{family}.md" for family in SESSIONS]
    resources.append(V / "batch-075-confirmation-claude.md")
    save(V / "batch-075-visual-freeze.json", {
        "execution": 502, "batch": "075", "evidenceHead": HEAD, "teachingSnapshot": TEACHING,
        "images": [str(path) for path in images], "assignedCaptures": 51, "archivedSourceCaptures": 111,
        "fixtureLines": len(FIXTURE.read_text(encoding="utf-8").splitlines()),
        "duplicateGroups": [{"sha256": key, "representative": str(paths[0]),
                             "paths": [str(path) for path in paths]} for key, paths in groups.items()],
        "resourceHashes": {str(path): sha(path) for path in resources},
        "archiverRecipe": {"path": str(PRIOR), "sha256": sha(PRIOR),
                           "adaptation": "Reused archive function with batch075 filenames, optional own confirmation report and corrected51/111 limit string only."},
    })
    print("Frozen 51 unique actual captures /111 originals,13 teaching/context files,",
          len(FIXTURE.read_text(encoding="utf-8").splitlines()), "fixture lines.")


def freeze():
    frozen = load(V / "batch-075-visual-freeze.json")
    assert git("rev-parse", "HEAD") == HEAD
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    for path, digest in frozen["resourceHashes"].items():
        assert sha(Path(path)) == digest, path
    return frozen


def exited(pid, completed_at=None):
    result = subprocess.run(
        ["pwsh", "-NoProfile", "-Command",
         f"$p=Get-Process -Id {pid} -ErrorAction SilentlyContinue; "
         "if($p){@{id=$p.Id;name=$p.ProcessName;startedAt=$p.StartTime.ToUniversalTime().ToString('o')}|ConvertTo-Json -Compress}"],
        capture_output=True, encoding="utf-8")
    if result.stdout.strip():
        process = json.loads(result.stdout)
        assert completed_at is not None, f"Reviewer PID{pid} still exists"
        assert datetime.fromisoformat(process["startedAt"]) > datetime.fromisoformat(completed_at), process
        save(L / f"pid-{pid}-reused-after-review.json", {
            "previousReviewerCompletedAt": completed_at, "currentProcess": process,
            "observedAt": now(), "action": "No process modified; later PID incarnation is not exited reviewer.",
        })


def run(family):
    freeze()
    if family == "gpt":
        prior = load(V / "batch-075-visual-claude-execution.json")
        correction = load(V / "batch-075-visual-claude-confirmation-execution.json")
        assert prior["exitCode"] == 0 and correction["processAndCoverageAccepted"]
        assert prior["imagePayloadsVerified"] == 51 and not prior["missingRequiredText"]
        assert not prior["unexpectedReadPaths"] and not prior["unfinishedTools"]
        exited(prior["launcherPid"])
        exited(correction["launcherPid"])
    model, session = SESSIONS[family]
    prefix = "batch-075-visual-" + family
    raw = L / f"{prefix}.jsonl"
    assert not raw.exists(), "Never overwrite original execution"
    prompt = (
        "Perform this DEPENDENT original-session visual confirmation. Every next read is contingent on "
        "your concrete observation of the previous result. Exactly ONE view call per response; "
        "WAIT for its result and state one observation before the next call. Never batch tools. "
        "Read ENTIRE task " + str(TASK)
        + ". YOUR complete original initial report: " + str(V / f"batch-075-initial-{family}.md") + ". "
    )
    if family == "claude":
        prompt += "YOUR complete textual confirmation: " + str(V / "batch-075-confirmation-claude.md") + ". "
    prompt += "Read your own report(s) completely, singly. Then follow the task's dependent resource chain."
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
        save(L / f"{prefix}-active.json", {"pid": process.pid, "sessionId": session, "startedAt": started})
        print(f"Running original {family}: PID{process.pid} model{model}", flush=True)
        code = process.wait()
    save(L / f"{prefix}-process.json", {
        "launcherPid": process.pid, "startedAt": started, "completedAt": now(),
        "exitCode": code, "requestedModel": model, "sessionId": session, "snapshot": HEAD,
        "command": command, "priorProcessExitedBeforeLaunch": family == "gpt",
    })
    assert code == 0, f"Reviewer exit {code}; original output preserved"
    exited(process.pid)
    archive(family)


def prepare_claude_confirmation():
    freeze()
    original = load(V / "batch-075-visual-claude-execution.json")
    exited(original["launcherPid"])
    assert original["exitCode"] == 0 and original["imagePayloadsVerified"] == 51
    assert original["multiToolResponses"] == 1 and len(original["observedToolOverlaps"]) == 2
    packet = V / "batch-075-visual-claude-confirmation-packet.txt"
    assert not packet.exists()
    lines = FIXTURE.read_text(encoding="utf-8").splitlines()
    report = V / "batch-075-visual-claude.md"
    parts = [
        "BOUND ORIGINAL-SESSION CORRECTION; NO TEACHING CHANGES; NOT A NEW INITIAL REVIEW.",
        "Teaching " + TEACHING + "; native evidence " + HEAD + ".",
        "Your original visual report and execution are preserved unchanged. Exact execution audit: ONE assistant response requested THREE concurrent fixture ranges [121,240], [241,360], [361,480], causing TWO overlapping starts. Your report says TWO calls; correct it. All743 fixture lines, all13 context files,51uniquePNG and required operational receipts were returned; image calls themselves were serial. Returned bytes do not prove comprehension. The original processAndCoverageAccepted flag remains FALSE; a serial follow-up cannot change that history. Initial498 EIGHT multi-toolresponses/THIRTYoverlaps and original false serial claim also remain historical.",
        "Your own complete visual report:\n" + report.read_text(encoding="utf-8"),
        "EXACT PREVIOUSLY READ FIXTURE LINES121-480, reproduced without changes:\n"
        + "\n".join(f"{i + 1}: {lines[i]}" for i in range(120, 480)),
        "COMPLETE UNCHANGED NEW TEACHING:\n" + (R / "kanji" / "典.md").read_text(encoding="utf-8")
        + "\n" + (R / "words" / "香典.md").read_text(encoding="utf-8"),
        "Exact operational distinction: disposable source and mocked HTTP/HEAD, but real complete signed Git archive through production ContentSync ONCE. NOT synthetic/reduced content. Supplied actual API35 instrumentation has BOTH named case terminal0/no skips234.957s; you did NOT execute it. The drawing path first injects eight reference touch strokes, checks ungraded trace, then separate recall 'I don't remember'/Again. It is not solely recall or human handwriting/MLKit evidence. Bounded emulator visual acceptance is distinct from physical-phone/generalrelease acceptance, which remain outstanding.",
        "No new images or dictionary evidence. Inherit your own51actual viewedPNGs and original lexical/source/optional limits, not other reviewer conclusions.",
    ]
    packet.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    save(V / "batch-075-visual-claude-confirmation-provenance.json", {
        "sourceFixture": str(FIXTURE), "sourceFixtureSha256": sha(FIXTURE),
        "exactFixtureRange": [121, 480], "originalReportSha256": sha(report),
        "packetSha256": sha(packet), "bytes": packet.stat().st_size,
        "teachingDiff": [], "newImages": 0, "freshDictionaryClaimed": False,
    })
    print("Prepared one bounded source-provenanced correction packet", packet.stat().st_size, "bytes.")


def confirm_claude():
    freeze()
    packet = V / "batch-075-visual-claude-confirmation-packet.txt"
    provenance = load(V / "batch-075-visual-claude-confirmation-provenance.json")
    assert sha(packet) == provenance["packetSha256"]
    prefix = "batch-075-visual-claude-confirmation"
    raw = L / f"{prefix}.jsonl"
    assert not raw.exists()
    model, session = SESSIONS["claude"]
    prompt = (
        "Bounded correction of YOUR OWN original-session visual review. Only ONE resource exists: "
        + str(packet) + ". Make exactly ONE view call for that path with forceReadLargeFiles=true, "
        "then no other tools. Read its complete bounded content. It includes your complete own report, "
        "exact unchanged previously batched fixture range and complete unchanged new teaching; "
        "no independent resources to parallelize. Correct your inaccurate TWO-call process count "
        "to actual THREE concurrent fixture reads/ONE multi-toolresponse/TWO overlaps. Preserve "
        "the original false processAndCoverageAccepted flag and all historical deviations. "
        "Confirm operational ContentSync/native/drawing distinctions precisely. "
        "Return COMPLETE Snapshot/Scope/Verdicts/Findings/Optional/Limits report; a separate "
        "three-facet verdict row for EACH of TWO whole new files and TEN exact reused scoped "
        "passages specified in your prior task; inherit previously viewed pixels/lexical conclusions "
        "explicitly, not fresh image or upstream review. Reassess own optional source-list "
        "observations, retaining them optional if no teaching defect. Report all consequential "
        "unresolved issues accurately; no finding quota or whole-project/phone/publication claim. "
        "A single-resource serial follow-up does not retroactively fix original concurrency."
    )
    command = [
        shutil.which("copilot"), "-C", str(R), "--add-dir", str(C), "--model", model,
        "--session-id", session, "--no-ask-user", "--allow-all-tools",
        "--disable-builtin-mcps", "--available-tools=view", "--output-format", "json",
        "--log-dir", str(L / f"review-{prefix}"),
        "--usage-output-file", str(L / f"{prefix}-usage.json"), "-p", prompt,
    ]
    env = os.environ.copy()
    env.pop("GH_TOKEN", None)
    env.pop("GITHUB_TOKEN", None)
    started = now()
    with raw.open("wb") as out, (L / f"{prefix}-stderr.txt").open("wb") as err:
        process = subprocess.Popen(command, stdout=out, stderr=err, env=env)
        print("Running bounded original Claude correction:", process.pid, flush=True)
        code = process.wait()
    exited(process.pid)
    events = [json.loads(line) for line in raw.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    messages = [e["data"] for e in events if e["type"] == "assistant.message"]
    models = sorted({m["model"] for m in messages if m.get("model")})
    starts = [e for e in events if e["type"] == "tool.execution_start"]
    ends = [e for e in events if e["type"] == "tool.execution_complete"]
    text = ends[0]["data"]["result"]["content"] if len(ends) == 1 else ""
    expected = packet.read_text(encoding="utf-8").strip()
    accepted = (code == 0 and models == [model] and len(starts) == len(ends) == 1
                and starts[0]["data"]["toolName"] == "view"
                and Path(starts[0]["data"]["arguments"]["path"]) == packet
                and ends[0]["data"]["success"] and expected in text.replace("\r\n", "\n"))
    report = V / f"{prefix}.md"
    assert not report.exists()
    report.write_text([m["content"] for m in messages if m.get("content")][-1] + "\n", encoding="utf-8")
    save(V / f"{prefix}-execution.json", {
        "launcherPid": process.pid, "startedAt": started, "completedAt": now(), "exitCode": code,
        "requestedModel": model, "actualModels": models, "sessionId": session,
        "command": command, "availableTools": ["view"], "toolCalls": len(starts),
        "returnedPacketComplete": expected in text.replace("\r\n", "\n"),
        "returnedTextSha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "packetSha256": sha(packet), "reportSha256": sha(report),
        "rawExecutionLocation": str(raw), "rawExecutionSha256": sha(raw),
        "configurationEvidence": [e["data"] for e in events if e["type"] == "session.info"],
        "usage": load(L / f"{prefix}-usage.json"),
        "processAndCoverageAccepted": accepted, "originalVisualProcessCompliant": False,
        "limits": "One-resource dependent correction, no fresh images/dictionary. Original51image reads and exact scope inherited. Original three concurrent fixture reads/twooverlaps remain noncompliant, not erased.",
    })
    print("Bounded confirmation process/range accepted:", accepted)
    assert accepted


def archive_pass(prefix, process, required, images, transport_limit=False):
    frozen = freeze()
    raw = L / f"{prefix}.jsonl"
    events = [json.loads(line) for line in raw.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    messages = [e["data"] for e in events if e["type"] == "assistant.message"]
    models = sorted({m["model"] for m in messages if m.get("model")})
    content = [m["content"] for m in messages if m.get("content")][-1] + "\n"
    report = V / f"{prefix}.md"
    if report.exists():
        assert report.read_text(encoding="utf-8") == content
    else:
        report.write_text(content, encoding="utf-8")
    calls, active, overlaps = {}, set(), []
    image_count = 0
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
                binary = result.get("binaryResultsForLlm", [])
                assert len(binary) == 1 and binary[0]["type"] == "image"
                payload = base64.b64decode(binary[0]["data"], validate=True)
                assert payload[:8] == b"\x89PNG\r\n\x1a\n"
                image_count += 1
                target = F.parent / f"{prefix}-returned" / source.name
                target.parent.mkdir(exist_ok=True)
                if target.exists() and target.read_bytes() != payload:
                    target = target.with_name(f"{image_count:03d}-" + source.name)
                if target.exists():
                    assert target.read_bytes() == payload
                else:
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
    allowed = {str(path) for path in required} | {str(path) for path in images}
    unexpected = [row["arguments"]["path"] for row in calls.values()
                  if str(Path(row["arguments"]["path"])) not in allowed]
    multi = sum(len(m.get("toolRequests", [])) > 1 for m in messages)
    usage = load(L / f"{prefix}-usage.json")
    mechanical = (process["exitCode"] == 0 and models == [process["requestedModel"]] == [usage["currentModel"]]
                  and not active and not overlaps and not multi and not missing and not unexpected
                  and actual_images == {str(path) for path in images}
                  and all(row["success"] and row["name"] == "view" for row in calls.values()))
    record = {
        **process, "actualModels": models, "availableTools": ["view"],
        "dependentNotBlindInitial": True, "reportSha256": sha(report),
        "rawExecutionLocation": str(raw), "rawExecutionSha256": sha(raw),
        "configurationEvidence": [e["data"] for e in events if e["type"] == "session.info"],
        "usage": usage, "toolCalls": list(calls.values()), "observedToolOverlaps": overlaps,
        "multiToolResponses": multi, "unfinishedTools": sorted(active), "missingRequiredText": missing,
        "unexpectedReadPaths": unexpected, "imagePayloadCalls": image_count,
        "imagePayloadsVerified": len(actual_images), "mechanicalTransportCoverageComplete": mechanical,
        "modelReportedImageLimit": transport_limit,
        "processAndCoverageAccepted": mechanical and not transport_limit,
        "returnedBytesAreNotComprehensionOrVisibility": True,
        "warnings": [{"type": e["type"], "data": e["data"]} for e in events
                     if e["type"] in ("session.warning", "system.notification", "session.compaction_start")],
        "limits": "Raw image payloads establish transport bytes, not actual model access/comprehension. InitialGPT50 repeated recovery reads and withdrawn unsupported image observations preserved. Fresh bounded retry must not repeat missing-image loops.",
    }
    output = V / f"{prefix}-execution.json"
    assert not output.exists()
    save(output, record)
    print(prefix, "mechanical transport:", mechanical, "accepted:", record["processAndCoverageAccepted"],
          "image calls:", image_count, "distinct:", len(actual_images))
    return record


def recover_archive():
    frozen = freeze()
    prefix = "batch-075-visual-gpt"
    process = load(L / f"{prefix}-process.json")
    exited(process["launcherPid"])
    required = FILES + [TASK, FIXTURE, F / "instrumentation.txt", F / "n1-075-article-route.json",
                        V / "batch-075-initial-gpt.md"]
    record = archive_pass(prefix, process, required, [Path(p) for p in frozen["images"]], True)
    assert record["mechanicalTransportCoverageComplete"]
    assert len(record["toolCalls"]) == 125 and record["imagePayloadCalls"] == 101
    save(L / "gpt-archive-diagnostic.json", {
        "originalControllerExitCode": 1,
        "reviewerExitCode": 0,
        "failure": "Previously verified archiver refused an already existing source-named returned-payload copy on GPT's repeated image call.",
        "disposition": "Original report and all events retained. Recovered archive verifies duplicates without overwrite and records all101image calls. Model certifies only27/51, notwithstanding101successful binary tool results. Original flag remains false.",
    })


def prepare_gpt_recovery():
    freeze()
    prior = load(V / "batch-075-visual-gpt-execution.json")
    exited(prior["launcherPid"])
    assert prior["modelReportedImageLimit"] and not prior["processAndCoverageAccepted"]
    images = [Path(p) for p in load(V / "batch-075-visual-freeze.json")["images"][:24]]
    packet = V / "batch-075-visual-gpt-recovery-task.txt"
    assert not packet.exists()
    text = f"""BOUND DEPENDENT GPT VISUAL RECOVERY, SAME075, execution502.
Fresh session because original GPT context reported image limits and made50
unproductive repeated recovery reads. That original execution/report stays
partial, not retrospectively approved. Original51sourceimage calls+50repeats
all returned binaryPNG to CLI; returned bytes do NOT establish model vision.
Fresh context is a recovery of24 missing pixel inspections, NOT a new blind
initial review or dictionary audit. Do NOT repeat a read or start recovery
loops. If any image cannot be seen, STOP and report precisely what is missing.

Exactly ONE view call PER RESPONSE. Wait for result, state one actual visible
observation from it in NEXT response before deciding nextcall. No parallel/
batch/nested/shell/edit tools. Only view is available. Read this task once,
then your own complete partial report once:
{V / "batch-075-visual-gpt.md"}
Do NOT read another family's report or author adjudication.

Frozen teaching{TEACHING}; evidenceHEAD{HEAD};
native fullGit envelopefba1a8868b82cd93d7bfaeae1080f5642bd92730.
Original family reviewed complete典/香典 + tenexactreusedpassages and
743linefixture/instrumentation/route; inherited source/context conclusions,
not fresh upstream review in this recovery. No teaching changes.
The27 certified images of reusedpassages/new香典 remain in originalreport;
do NOT reread them. Inspect ONLY these24 missing PNGs in listed order:
"""
    text += "\n".join(str(path) for path in images)
    text += """

Assess: all117scopedHan in panels1-5 across Gothic/Mincho/Textbook/Brush;
panel6 focused典/具/曲/共, 奠/亅/厂/艹/八, and sixwholewords
典型/古典/百科事典/辞典/香典/香奠. Distinguish readableglyphs from
unknownfallbackface; paint/cmap/hash evidence is not readability.
Complementary left/right table captures must expose allfour readinglabels
and selected examples/source-only qualifications; offscreenadjacent text
doesnotprove targetclipping. Some adjacent columns clip and のり wraps.
Actual onkeyquestions/feedback/Done2of2 and meaningchoices need pixelcheck,
not authored具/曲/共 substitutes or whole-livepool certification.
Full+Lite rawonテン/デン,kunふみ/のり in sourceorder; curatedonboth,
kunempty. Offeredてん/でん eachGood/Done2correct/noKunLog supplied.
Eightreference-touchstrokes/ungradedtrace/model-unavailablegeometry/
separaterecallmiss/Again are NOT MLKit or successfulhumanhandwriting.
Supplied actual two named API35 cases terminal0/noskips234.957s;
productionContentSync fullsignedGitarchive ONCE1087kanji5044words107N1/
problems0/version2759d7b13c89eb8f/epoch1. Synthetic source/HTTP, NOT
synthetic/reducedcontent. Staticpixels NOT reviewerperformedgestures.
All12mappedpairs24directions/Back/offline and originallexicalconclusions
inherited, not rerun. No newpersistedmeaninggrade; meaningexitsbeforeNext.
Nativeheapgrowth192m/heapsize576m unchanged; noheap/guard/appchanges.
Source1080x2400 mayresize; nophysicalphone/nativespeaker/generalrelease/
whole-set/latestmain/publication acceptance. CompatibleAndroidf9b59a2+.

Return COMPLETE Snapshot/Scope/Verdicts/Findings/Optional/Limits report.
State ACTUAL24pixels inspected/anymissing/transport limits. Give separate
correctness/scopedcoverage/comprehensibility verdicts for full典/full香典
and ten reusedchanges (words典型24,古典31,百科事典29,辞典23;
kanji古38,辞37,百22linkonly,科41,事36,香42).
Explicitly inherit previouslyreviewed lexical/context/27pixels separately
from NEW24pixelchecks. Use CLEAN/NEEDS FIX/UNVERIFIED, nofindingquota.
Retain originalpartialreport and withdrawnunsupportedobservations, plus
initialClaude8multitool/30overlaps and visualClaude3reads/2overlaps as
processhistory supplied here, NOT otherfamilycontent evidence.
Findings require severity/facet/exactPNG/impact/remedy/evidence/confidence.
No morethan ONE call for ANYresource; stopatfirsttransportfailure.
Finish COMPLETE report and EXIT. No unrelatedscope,nextbatch,questions.
"""
    packet.write_text(text, encoding="utf-8")
    save(V / "batch-075-visual-gpt-recovery-freeze.json", {
        "sessionId": str(uuid.uuid4()), "model": "gpt-6.1-sol",
        "reasonFreshContext": "Original session's image-limit/50 repeated reads do not certify24missingPNG.",
        "images": [str(path) for path in images],
        "resourceHashes": {str(path): sha(path) for path in
                           [packet, V / "batch-075-visual-gpt.md"] + images},
    })
    print("Prepared fresh bounded GPT recovery for24missingimages; zero repeatedread policy.")


def run_gpt_recovery():
    freeze()
    frozen = load(V / "batch-075-visual-gpt-recovery-freeze.json")
    for path, digest in frozen["resourceHashes"].items():
        assert sha(Path(path)) == digest
    prior = load(V / "batch-075-visual-gpt-execution.json")
    exited(prior["launcherPid"])
    prefix = "batch-075-visual-gpt-recovery"
    raw = L / f"{prefix}.jsonl"
    assert not raw.exists()
    task = V / "batch-075-visual-gpt-recovery-task.txt"
    command = [
        shutil.which("copilot"), "-C", str(R), "--add-dir", str(C),
        "--model", frozen["model"], "--session-id", frozen["sessionId"],
        "--no-ask-user", "--allow-all-tools", "--disable-builtin-mcps",
        "--available-tools=view", "--output-format", "json",
        "--log-dir", str(L / "review-gpt-recovery"),
        "--usage-output-file", str(L / f"{prefix}-usage.json"),
        "-p", "Exactly ONE view call per response, no repeats. Read complete bounded recovery task "
        + str(task) + " then follow its dependent chain. Stop on first unavailable image; no recovery loops.",
    ]
    env = os.environ.copy()
    env.pop("GH_TOKEN", None)
    env.pop("GITHUB_TOKEN", None)
    started = now()
    with raw.open("wb") as out, (L / f"{prefix}-stderr.txt").open("wb") as err:
        process = subprocess.Popen(command, stdout=out, stderr=err, env=env)
        print("Running fresh bounded GPT24image recovery:", process.pid, flush=True)
        code = process.wait()
    exited(process.pid)
    record = {
        "launcherPid": process.pid, "startedAt": started, "completedAt": now(),
        "exitCode": code, "requestedModel": frozen["model"], "sessionId": frozen["sessionId"],
        "snapshot": HEAD, "command": command, "priorProcessExitedBeforeLaunch": True,
    }
    save(L / f"{prefix}-process.json", record)
    result = archive_pass(prefix, record, [task, V / "batch-075-visual-gpt.md"],
                          [Path(path) for path in frozen["images"]])
    assert result["processAndCoverageAccepted"]
    assert len(result["toolCalls"]) == 26 and result["imagePayloadCalls"] == 24


if __name__ == "__main__":
    if sys.argv[1] == "prepare":
        prepare()
    elif sys.argv[1] == "run":
        run(sys.argv[2])
    elif sys.argv[1] == "prepare-confirmation":
        prepare_claude_confirmation()
    elif sys.argv[1] == "confirm-claude":
        confirm_claude()
    elif sys.argv[1] == "recover-archive":
        recover_archive()
    elif sys.argv[1] == "prepare-gpt-recovery":
        prepare_gpt_recovery()
    elif sys.argv[1] == "gpt-recovery":
        run_gpt_recovery()

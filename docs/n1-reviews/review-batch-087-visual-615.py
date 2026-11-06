import hashlib
import gzip
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

C = Path(__file__).parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
V = R / "docs" / "n1-reviews"
N = V / "batch-087-native" / "execution-614"
HEAD = "dbf9201eb2c70fd0e5819a14ef6b1e74b7cbc396"
ANDROID = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
SESSIONS = {
    "claude": ("claude-opus-5.5", "2308e256-e5c9-494d-8e53-805f94ff6314"),
    "gpt": ("gpt-6.1-sol", "d08a2c70-c89c-4b1f-a38c-311b6245ad29"),
}
PACKET = C / "batch-087-visual-615-packet.txt"
IMAGES = [N / "inspection" / f"contact-{i:02d}.png" for i in range(1, 11)]
IMAGES += [N / f"n1-087-font-panel-{i}.png" for i in (1, 2)]
NEXT = (
    "SAME087 bounded review-closed acceptance/current-main integration preparation, not088. "
    "Read docs/n1-sources/execution-615.json and docs/n1-reviews/batch-087-visual-reconciliation-615.json. "
    "Original Claude2308e256 and GPTd08a2c70 serial dependent visual confirmations returned complete "
    "14 serial view calls each, all12 actual PNGs decoded; allthree articles renderedCLEAN, no actionable defects. "
    "Teachingf6391022 unchanged; both initial textual reviews remain separate historical blind credit. "
    "Actual defaultN1 yuzu citrus pictured; seed613 chestnut/Allwind are production JSON receipt only, "
    "NOT separately pictured nor allfuturefallback safety. Existing native two terminalcase0/no skips and "
    "fullarchive404f507d productionContentSyncONCE1110kanji5066words119N1zeroProblems/versioneb3a9413cccd4f57epoch1 "
    "inherited; no fresh native/Android/phone claim615. All21Han visible across fourCompose families; "
    "Paint84+8 recycled hashes NOT92exportedPNGs. Injectedtrace/giveup not humanhandwriting/MLKit/phone. "
    "QualifiedTESTONLYAndroid1c1b7bf4 retains productionf9b59a2, not latestappmain. "
    "Recheck freshmain/exactsignedheads/cleanworktrees/source-membership/fullbaseline-preservation/links/readings/"
    "wordguards/stroke/font dispositions; run required contenttests/vocabularyconsistency/manifestfreshness/"
    "budget/audits/applicableAndroid on actual combinedtree. Normal nonrewriting mainmerge; "
    "independent review of substantive teaching changes; no publication until all acceptance prerequisites. "
    "Then normal signing/ownerfastforward/terminalCI/EVERYimmutablepublicZIP runtime entryhash/"
    "18000entries42MiBcompressed80MiBinflated56MiBretained/perfile-media-safepath/ownerissue gates. "
    "No forcepush/amend/guardincrease/productionappchange/088. Parent19008 ownsrunner.lock; verify live "
    "ancestry/current runner session, no child acquisition/delete/unlock. Approvedcontrol/committedsources "
    "only, no optional historical-session recipes. Preserve/report/yield actualnewdenial/signinghang/"
    "uncertainownership. Published113/1228,1115remaining unchanged; "
    "phone/generalrelease/whole-set outstanding; projectincomplete."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def now():
    return datetime.now().astimezone().isoformat()


def git(*args, repo=R):
    return subprocess.check_output(
        ["git", "--no-pager", "-C", str(repo), *args], encoding="utf-8"
    ).strip()


def frozen():
    assert git("rev-parse", "HEAD") == HEAD
    assert git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert git("rev-parse", "HEAD", repo=A) == ANDROID
    assert git("log", "-1", "--format=%G?", repo=A) == "G"
    assert not git("status", "--porcelain", repo=A)
    p = load(C / "progress.json")
    assert p["checkpoint"] == 614 and p["batch"] == "087"
    runner = load(C / "runner.json")
    assert runner["pid"] == 19008
    assert runner["sessionId"] == "3a624779-90df-4d36-a6d6-446b83883e98"
    command = (
        "$p=Get-CimInstance Win32_Process -Filter \"ProcessId=$PID\";"
        "$found=$false; while($p){if($p.ProcessId -eq 19008){$found=$true;break};"
        "$p=Get-CimInstance Win32_Process -Filter \"ProcessId=$($p.ParentProcessId)\"};"
        "if(-not $found){exit 1}"
    )
    assert subprocess.run(["pwsh", "-NoProfile", "-Command", command],
                          capture_output=True).returncode == 0
    for path, expected in load(V / "batch-087-reconciliation.json")["reviewedRuntimeHashes"].items():
        assert sha(R / path) == expected


def prepare():
    frozen()
    assert not PACKET.exists()
    log = C / "logs" / "3a624779-90df-4d36-a6d6-446b83883e98"
    request = log / "request.txt"
    data = request.read_bytes()
    text = data.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1
    )[1])
    assert checkpoint["execution614CoordinatorCheckpoint"]["savedCommit"] == HEAD
    shutil.copyfile(C / "progress.json", log / "progress-before-615.json")
    p = load(C / "progress.json")
    p["execution615StartingState"] = {
        "execution": 615, "batch": "087", "startedAt": now(),
        "startingHead": HEAD, "androidHead": ANDROID,
        "freshOriginMain": git("rev-parse", "origin/main"),
        "scope": "SAME087 original-session serial dependent visual confirmations; local signed evidence checkpoint only, no publication or088.",
        "request": {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data),
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Complete request loaded/decoded; operative contract, approved issue and final614 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": "Live parent19008 verified through child ancestry and exact runner session. No child lock acquisition/delete/unlock.",
        "artifactPathPreflight": "Committed packets and approved control artifacts only; no optional historical session helpers accessed.",
        "diagnostics": ["Preparation preflight caught a copied historical runner session ID before state mutation/reviewer launch. Read-only verification found live parent19008 assigned this current execution session; corrected exact-session assertion. No lock touched or new denial."],
        "actualNewPermissionDenials": [],
    }
    p["stage"] = "batch-087-dependent-visual-confirmations"
    p["nextAction"] = "SAME087 original Claude then original GPT serial visual follow-ups; preserve actual reports/read/model/process limits before local checkpoint."
    save(C / "progress.json", p)
    parts = [
        f"DEPENDENT VISUAL EVIDENCE; frozen signed HEAD {HEAD}; unchanged teaching f6391022356073dd3e53437be30885f9a09857d9.",
        "Not a new blind review. Initial textual source findings remain historical. Native receipt is supplied coordinator evidence, not reviewer-executed testing. All production app/native/phone limitations remain explicit.",
    ]
    for path in [R / "kanji" / "\u51ea.md", R / "words" / "\u51ea.md",
                 R / "words" / "\u51ea\u3050.md", V / "batch-087-reconciliation.json",
                 N / "visual-inspection.json", N / "execution.json",
                 N / "n1-087-article-route.json", N / "inspection" / "contact-map.json"]:
        parts.append(f"RESOURCE {path}; SHA256 {sha(path)}\n{path.read_text(encoding='utf-8-sig')}")
    parts.append("EXACT TEACHING DIFF FROM INITIAL REVIEW SNAPSHOT TO CURRENT HEAD:\n" +
                 git("diff", "f6391022356073dd3e53437be30885f9a09857d9", HEAD,
                     "--", "kanji", "words", "articles", "strokes", "manifest.json"))
    parts.append("ACTUAL PNGS TO VIEW SERIALLY:\n" + "\n".join(map(str, IMAGES)))
    PACKET.write_text("\n\n".join(parts), encoding="utf-8")
    save(C / "batch-087-visual-615-inputs.json", {
        "packet": {"path": str(PACKET), "sha256": sha(PACKET)},
        "images": [{"path": str(path), "sha256": sha(path)} for path in IMAGES],
        "head": HEAD, "teachingSnapshot": "f6391022356073dd3e53437be30885f9a09857d9",
    })
    print("Prepared bounded visual packet:", PACKET.stat().st_size, "bytes,", len(IMAGES), "images")


def run(label):
    frozen()
    model, session = SESSIONS[label]
    if label == "gpt":
        prior = load(C / "batch-087-visual-615-claude-execution.json")
        assert prior["exitCode"] == 0 and not prior["unfinishedTools"]
        assert not prior["observedToolOverlaps"]
        assert prior["allAssignedResourcesSuccessfullyReturned"]
        assert subprocess.run(["pwsh", "-NoProfile", "-Command",
                               f"if(Get-Process -Id {prior['launcherPid']} -ErrorAction SilentlyContinue){{exit 1}}"],
                              capture_output=True).returncode == 0
    prefix = C / f"batch-087-visual-615-{label}"
    raw = prefix.with_suffix(".jsonl")
    assert not raw.exists()
    catalog = (C / "copilot-config-execution-615.txt").read_text(encoding="utf-8-sig")
    assert f'"{model}"' in catalog
    prompt = f"""DEPENDENT VISUAL FOLLOW-UP in your ORIGINAL session {session}, model {model}.
Frozen signed evidence HEAD {HEAD}; original teaching f6391022356073dd3e53437be30885f9a09857d9 UNCHANGED (exact diff supplied). This is NOT another blind initial review.
Read your own original report {V / ('batch-087-initial-' + label + '.md')} and the ENTIRE {PACKET} with forceReadLargeFiles=true. Then view ALL TWELVE actual PNG paths listed at its end, one tool call at a time, serially. All55 screenshots are mapped in ten whole-frame contact sheets, with two font panels also separately full-size. If image decoding/vision is unavailable or a response truncated, say precisely so; do not replace visual inspection with hashes/cmap/hasGlyph/author opinion. Only view exposed; no shell, edit, delegation, parallel calls or other reviewer's report. Recover missing text ranges serially if necessary.

Assess independent rendered comprehensibility of EACH new kanji\\凪.md, words\\凪.md, words\\凪ぐ.md; all21 Han across Gothic/Mincho/Textbook/Brush production selections, especially 几 U+51E0 versus 凡/凪/風/凹. Native Paint84+8 were recycled hash probes, NOT92 exported PNGs. Actual evidence is Compose panels and session/article captures. Inspect morning/evening words and gu-ending paradigm/readings, allthree full article projections, left/right horizontally scrollable reading table, reciprocal routes/restored SystemBack, N1 selection/meaning, BOTHkunkeysなぎ/なぐ and done, sixstroke injectedtrace/recall feedback. Explain any actual clipping/readability defect rather than demanding cosmetic uniformity.
Adjudicate actual N1 displayed fallback labels: default yuzu citrus(柚) and seeded613 chestnut(栗), beside凹 concave;sunken/凡 commonplace;mediocre versus凪 calmseas;lull. N4風 excluded in N1; All contains風 wind;style. Scope is actual witnessed choices, not every future random pool. Check actual reading alternatives too.
Reconcile your original native/fallback-unverified limits ONLY where new evidence suffices. Textual correctness/scoped coverage is inherited unless actual screenshots establish a new defect; preserve qualifications weather凪ぐ vs feelings和ぐ/classicalforms. No new upstream/source or blind-review credit.
Return COMPLETE compact report Snapshot;Scope(actualmodel/resources);Verdicts(separate correctness/scopedcoverage/renderedcomprehensibility for EACH article, label inherited textual conclusions);Findings(severity/facet/file or PNG:location/claim+impact/remedy/evidence/confidence, ornone);Optional;Limits. Explicitly distinguish supplied successful native receipt from your visual inspection. API35 emulator not phone/native-speaker. Injected stroke/giveup not humanhandwriting or offline MLKit. Qualified TESTONLY Android1c1b7bf4 retains productionf9b59a2, NOT latestappmain. Currentmain integration/publicZIP/CI/phone/generalrelease/wholeproject outstanding. Disclose exact incomplete reads/images. No edits, publication, nextbatch, questions.
"""
    prompt_path = prefix.with_suffix(".prompt.txt")
    prompt_path.write_text(prompt, encoding="utf-8")
    cmd = [shutil.which("copilot"), "-C", str(R), "--add-dir", str(C),
           "--resume=" + session, "--model", model, "--no-ask-user",
           "--allow-tool=view", "--available-tools=view", "--disable-builtin-mcps",
           "--no-custom-instructions", "--output-format", "json",
           "--log-dir", str(C / "review-logs" / prefix.name),
           "--usage-output-file", str(prefix.with_suffix(".usage.json")), "-p", prompt]
    env = os.environ.copy()
    env.pop("GH_TOKEN", None)
    env.pop("GITHUB_TOKEN", None)
    started = now()
    with raw.open("wb") as out, prefix.with_suffix(".stderr.txt").open("wb") as err:
        process = subprocess.Popen(cmd, stdout=out, stderr=err, env=env)
        save(prefix.with_suffix(".active.json"), {
            "pid": process.pid, "sessionId": session, "model": model, "command": cmd, "startedAt": started,
        })
        print("Started original-session reviewer", label, process.pid, session, flush=True)
        code = process.wait()
    events = [json.loads(line) for line in raw.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    messages = [event["data"] for event in events if event["type"] == "assistant.message"]
    prefix.with_suffix(".md").write_text(
        messages[-1].get("content", "") + "\n" if messages else "No completed report.\n", encoding="utf-8")
    active, calls, overlaps = set(), {}, []
    required = {str(path) for path in IMAGES} | {str(PACKET), str(V / f"batch-087-initial-{label}.md")}
    returned = set()
    for event in events:
        data = event.get("data", {})
        if event["type"] == "tool.execution_start":
            key = data["toolCallId"]
            if active:
                overlaps.append({"starting": key, "active": sorted(active)})
            active.add(key)
            calls[key] = {"name": data["toolName"], "arguments": data["arguments"],
                          "startedAt": event["timestamp"]}
        elif event["type"] == "tool.execution_complete":
            key = data["toolCallId"]
            active.discard(key)
            result = data.get("result", {}).get("content", "")
            result = result if isinstance(result, str) else json.dumps(result, ensure_ascii=False)
            call = calls[key]
            call.update({"completedAt": event["timestamp"], "success": data["success"],
                         "returnedCharacters": len(result),
                         "returnedSha256": hashlib.sha256(result.encode("utf-8")).hexdigest(),
                         "truncationMarker": any(x in result for x in [
                             "[Output truncated", "File too large to read", "<note>Content truncated",
                             "Invalid view_range"])})
            path = call["arguments"].get("path")
            if path in required and data["success"] and not call["truncationMarker"]:
                if path.endswith(".png"):
                    returned.add(path)
                else:
                    norm = lambda value: value.replace("\r\n", "\n").rstrip()
                    exact = norm(Path(path).read_text(encoding="utf-8-sig")) in norm(result)
                    call["entireRequestedTextContained"] = exact
                    if exact:
                        returned.add(path)
    usage_path = prefix.with_suffix(".usage.json")
    usage = load(usage_path) if usage_path.exists() else None
    record = {
        "execution": 615, "batch": "087", "snapshot": HEAD,
        "originalTeachingSnapshot": "f6391022356073dd3e53437be30885f9a09857d9",
        "dependentOriginalSession": True, "newBlindReviewCredit": False,
        "sessionId": session, "requestedModel": model,
        "actualModels": sorted({message.get("model", "") for message in messages}),
        "usageCurrentModel": usage.get("currentModel") if usage else None,
        "launcherPid": process.pid, "startedAt": started, "completedAt": now(), "exitCode": code,
        "toolCalls": list(calls.values()), "observedToolOverlaps": overlaps,
        "unfinishedTools": sorted(active), "requiredResources": sorted(required),
        "successfullyReturnedResources": sorted(returned), "missingResources": sorted(required - returned),
        "allAssignedResourcesSuccessfullyReturned": not (required - returned),
        "rawSha256": sha(raw), "reportSha256": sha(prefix.with_suffix(".md")),
        "availableTools": ["view"], "usage": usage,
        "limits": "Successful PNG tool returns establish resource delivery, not comprehension. Actual report determines whether model vision/inspection was available.",
    }
    save(C / (prefix.name + "-execution.json"), record)
    print(json.dumps({key: record[key] for key in [
        "exitCode", "actualModels", "missingResources", "observedToolOverlaps"]}, ensure_ascii=True))
    assert code == 0 and record["actualModels"] == [model]
    assert usage and usage["currentModel"] == model
    assert not active and not overlaps and not (required - returned)
    frozen()


def runtime():
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest, sha256

    manifest = load(R / "manifest.json")
    assert build_manifest(R) == manifest
    checked = {}
    for kind, section in manifest.items():
        if isinstance(section, dict):
            for path, expected in section.items():
                if isinstance(expected, str) and len(expected) == 64:
                    file = R.joinpath(*path.split("/"))
                    actual = sha(file) if kind in {
                        "images", "audio", "listeningTaskAudio", "listeningTaskImages"
                    } else sha256(file)
                    assert actual == expected, path
                    checked[path] = expected
    assert len(checked) == 8420
    assert manifest["contentVersion"] == "eb3a9413cccd4f57"
    return {"runtimeHashesVerified": len(checked), "contentVersion": manifest["contentVersion"],
            "manifestSha256": sha(R / "manifest.json")}


def archive():
    frozen()
    records = {label: load(C / f"batch-087-visual-615-{label}-execution.json") for label in SESSIONS}
    assert records["claude"]["completedAt"] < records["gpt"]["startedAt"]
    for label, record in records.items():
        assert record["exitCode"] == 0 and record["actualModels"] == [SESSIONS[label][0]]
        assert record["allAssignedResourcesSuccessfullyReturned"]
        assert not record["unfinishedTools"] and not record["observedToolOverlaps"]
        assert len(record["toolCalls"]) == 14
        assert subprocess.run(["pwsh", "-NoProfile", "-Command",
                               f"if(Get-Process -Id {record['launcherPid']} -ErrorAction SilentlyContinue){{exit 1}}"],
                              capture_output=True).returncode == 0
    verified = runtime()
    reconciliation = {
        "schemaVersion": 1, "execution": 615, "batch": "087",
        "evidenceSnapshot": HEAD, "teachingSnapshot": "f6391022356073dd3e53437be30885f9a09857d9",
        "status": "dependent-visual-review-closed-awaiting-combined-acceptance",
        "teachingChanged": False, "originalInitialReviewsPreserved": True,
        "newBlindInitialReviewCredit": False, "processes": records,
        "serialProcessesExited": True, "eachReportPreservedBeforeNextLaunch": True,
        "allAssignedResourcesReturned": True, "eachReviewerImagesDecoded": 12,
        "eachReviewerSerialViewCalls": 14, "findings": [],
        "verdicts": {path: {"correctness": "CLEAN-inherited-textual",
                            "scopedCoverage": "CLEAN-inherited-textual",
                            "renderedComprehensibility": "CLEAN"}
                     for path in ["kanji/\u51ea.md", "words/\u51ea.md", "words/\u51ea\u3050.md"]},
        "dispositions": [
            {"claim": "Actual glyph and article rendering unverified in original textual reviews",
             "status": "resolved", "evidence": "Both original reviewers actually decoded twelve PNGs serially: ten mapped contact sheets/all55 captures and two full-size Compose panels. Each found all21 scopedHan visible in allfour production selections, including U+51E0 distinguishable from related forms; allthree article bodies readable.",
             "limits": "Not physicalphone, identifiedfallbackfont, native-speaker or92PaintPNG evidence."},
            {"claim": "N1 filtered-pool fallback could overlap calm/lull",
             "status": "resolved", "scope": "bounded tested configurations only",
             "evidence": "Both independently inspected pictured defaultyuzucitrus alongside concave/sunken and commonplace/mediocre. Seed613chestnut and Allwind/style are supplied productionbuilderJSON, not separately pictured. No competing answer established.",
             "limits": "No universalfuturefallback oroldclient certification."},
            {"claim": "Wrapping, side-scrolled reading-table clipping or leading toolbar cropping",
             "status": "optional",
             "evidence": "Both reviewers find fullbody readable in adjoining captures; table explicitly scrollable and separate left/right cells visible. Later route/restored screenshots show title/Back. No established persistent article defect.",
             "decision": "No content/app edit; keep reported screenshot/transition uncertainty."},
            {"claim": "Practice feedback combines ungraded attempt with shape-only grading label",
             "status": "optional", "reportedBy": ["Claude"],
             "evidence": "contact01#6 visibly labels practiceonly/notgraded and shapeonly fallback. No article defect established; unrelated productionapp wording outside this task.",
             "decision": "No productionapp change; retain original report."},
            {"claim": "Again persistence, seeded fallback, no onquestion and native import success",
             "status": "resolved", "scope": "supplied native terminal/route receipts",
             "evidence": "Both distinguish visually inspected two-keydone/reference screens from native supplied DB/parser/test assertions. Again is not a separately pictured grade.",
             "limits": "Not reviewer-executed test, humanhandwriting, MLKit or phone."},
        ],
        "modelContributionComparison": {
            "sharedVerifiedFindings": "Both observed readable fonts/articles, bounded unambiguous choices and no actionable defect.",
            "claudeUniqueVerifiedDefect": None, "gptUniqueVerifiedDefect": None,
            "unsupportedOrOptional": "Claude practice-label wording optional; toolbar/wrapping/viewport observations are shared across reports/limits, not unique discoveries.",
            "limits": "Dependent same-snapshot visual sample, not modelbenchmark or newblind review.",
        },
        "limits": [
            "Inherited source/textual initial reviews, not new upstream retrieval or repeated full lexical review.",
            "API35 screenshots; contact sheets downscaled, only fontpanels separately fullsize.",
            "Paint84+8 recycled probes are hashes, not exported individually viewed PNGs.",
            "No fresh Android/native615 execution; qualified TESTONLY app not latestappmain.",
            "Currentmain combined acceptance/publicZIP/terminalCI/publication/phone/generalrelease/whole-set remain outstanding.",
        ],
        "runtime": verified, "runtimeAcceptedForPublication": False,
        "runtimePublished": False, "nextAction": NEXT,
    }
    receipts = []
    sources = [Path(__file__), PACKET, C / "batch-087-visual-615-inputs.json",
               C / "copilot-help-execution-615.txt", C / "copilot-config-execution-615.txt"]
    for label in SESSIONS:
        prefix = C / f"batch-087-visual-615-{label}"
        sources += [prefix.with_suffix(suffix) for suffix in [".md", ".prompt.txt", ".stderr.txt", ".usage.json"]]
        sources += [C / (prefix.name + "-execution.json")]
        raw = prefix.with_suffix(".jsonl")
        target = V / (raw.name + ".gz")
        assert not target.exists()
        with gzip.open(target, "wb") as output:
            output.write(raw.read_bytes())
        assert gzip.decompress(target.read_bytes()) == raw.read_bytes()
        receipts.append({"source": str(raw), "archive": str(target.relative_to(R)).replace("\\", "/"),
                         "sourceSha256": sha(raw), "archiveSha256": sha(target), "losslessGzip": True})
    for source in sources:
        target = V / source.name
        assert not target.exists()
        shutil.copyfile(source, target)
        receipts.append({"source": str(source), "archive": str(target.relative_to(R)).replace("\\", "/"),
                         "sourceSha256": sha(source), "archiveSha256": sha(target)})
    save(V / "batch-087-visual-reconciliation-615.json", reconciliation)
    save(R / "docs" / "n1-sources" / "execution-615.json", {
        "schemaVersion": 1, "execution": 615, "batch": "087",
        "startingState": load(C / "progress.json")["execution615StartingState"],
        "snapshot": HEAD, "status": reconciliation["status"], "runtime": verified,
        "reconciliation": "docs/n1-reviews/batch-087-visual-reconciliation-615.json",
        "receipts": receipts, "runtimeChanged": False, "runtimePublished": False,
        "newNativeOrPhoneClaimed": False, "actualNewPermissionDenials": [],
        "diagnostics": ["First archive preflight used raw bytes for text and caught curriculum/grammar.json CRLF normalization before any archive writes. Reused repository build_manifest/sha256 canonical text hashing; no content, manifest or acceptance rule changed."],
        "publishedAdditions": 113, "remainingAdditions": 1115,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
    })
    print("Archived both complete reports and lossless execution streams; runtime unchanged")


def finalize():
    saved = git("rev-parse", "HEAD")
    assert git("rev-parse", "HEAD^") == HEAD
    assert git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert git("rev-parse", "HEAD", repo=A) == ANDROID
    assert not git("status", "--porcelain", repo=A)
    verified = runtime()
    evidence = load(R / "docs" / "n1-sources" / "execution-615.json")
    for receipt in evidence["receipts"]:
        assert sha(R.joinpath(*receipt["archive"].split("/"))) == receipt["archiveSha256"]
    body = (C / "batch-087-visual-615-issue-body.txt").read_bytes().decode("utf-8")
    posted = load(C / "batch-087-visual-615-issue-posted.json")
    receipt = load(C / "batch-087-visual-615-issue-receipt.json")
    assert posted["id"] == receipt["id"]
    assert posted["body"] == receipt["body"] == body
    assert posted["user"]["login"] == receipt["user"]["login"] == "stop-cran"
    state = load(C / "progress.json")
    before = load(C / "logs" / "3a624779-90df-4d36-a6d6-446b83883e98" / "progress-before-615.json")
    assert state["checkpoint"] == 614 and state["stage"] == "batch-087-dependent-visual-confirmations"
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    for key, value in before.items():
        if key not in allowed:
            assert state[key] == value, key
    checkpoint = {
        "schemaVersion": 1, "execution": 615, "checkpoint": 615, "batch": "087",
        "savedCommit": saved, "signature": "G", "status": "continue",
        "stage": "visual-review-closed-awaiting-combined-acceptance",
        "evidence": "docs/n1-sources/execution-615.json",
        "reconciliation": "docs/n1-reviews/batch-087-visual-reconciliation-615.json",
        "runtime": verified, "independentVisualConfirmationsComplete": True,
        "originalSessionsReused": {label: session for label, (_, session) in SESSIONS.items()},
        "actualModels": [model for model, _ in SESSIONS.values()],
        "eachReviewerPngsDecoded": 12, "eachReviewerSerialViewCalls": 14,
        "serialReviewerProcessesExited": True, "actionableFindings": [],
        "runtimeChanged": False, "runtimeAcceptedForPublication": False, "runtimePublished": False,
        "newNativeOrPhoneClaimed": False, "dedicatedWorktreesClean": True,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "publishedAdditions": 113, "remainingAdditions": 1115,
        "lastPublishedCommit": state["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "issueBodySha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
        "originalRootKeysCompared": len(before), "allOriginalHistoricalRootValuesPreservedExactly": True,
    }
    state.update({"checkpoint": 615, "status": "continue", "stage": checkpoint["stage"],
                  "nextAction": NEXT, "blocker": None})
    state["execution615CoordinatorCheckpoint"] = checkpoint
    state["batch087VisualReviewCheckpoint"] = checkpoint.copy()
    temporary = C / "progress-execution-615.tmp"
    save(temporary, state)
    temporary.replace(C / "progress.json")
    final = load(C / "progress.json")
    for key, value in before.items():
        if key not in allowed:
            assert final[key] == value, key
    save(C / "logs" / "3a624779-90df-4d36-a6d6-446b83883e98" / "checkpoint-final-615.json", checkpoint)
    print(json.dumps(checkpoint, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    if sys.argv[1] == "prepare":
        prepare()
    elif sys.argv[1] == "run":
        run(sys.argv[2])
    elif sys.argv[1] == "archive":
        archive()
    elif sys.argv[1] == "finalize":
        finalize()
    else:
        raise ValueError("Unsupported operation")

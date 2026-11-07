import gzip
import hashlib
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
N = V / "batch-088-native" / "execution-623"
L = C / "logs" / "9b3d9e2b-9e0c-4510-b579-2bd1c5dcb8aa"
HEAD = "7e514fe5161da7ff046f3c20ae4ffead201b4bd9"
TEACHING = "42077c31b4462081eb6b2c171a907c7cae47192d"
ANDROID = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
SESSIONS = {
    "claude": ("claude-opus-5.5", "915d0745-fc54-49b0-99cf-49762fb5e16f"),
    "gpt": ("gpt-6.1-sol", "11925f67-211b-497f-9d75-3d2802c178ab"),
}
PACKET = C / "batch-088-visual-624-packet.txt"
IMAGES = [N / "inspection" / f"contact-{i:02d}.png" for i in range(1, 9)]
IMAGES += [N / f"n1-088-font-panel-{i}.png" for i in (1, 2, 3)]


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
    state = load(C / "progress.json")
    assert state["checkpoint"] == 623 and state["batch"] == "088"
    runner = load(C / "runner.json")
    assert runner["pid"] == 19008 and runner["sessionId"] == L.name
    command = (
        '$p=Get-CimInstance Win32_Process -Filter "ProcessId=$PID";'
        "$found=$false; while($p){if($p.ProcessId -eq 19008){$found=$true;break};"
        '$p=Get-CimInstance Win32_Process -Filter "ProcessId=$($p.ParentProcessId)"};'
        "if(-not $found){exit 1}"
    )
    assert subprocess.run(["pwsh", "-NoProfile", "-Command", command],
                          capture_output=True).returncode == 0
    for path, expected in load(V / "batch-088-reconciliation.json")["reviewedRuntimeHashes"].items():
        assert sha(R.joinpath(*path.split("/"))) == expected


def prepare():
    frozen()
    assert not PACKET.exists()
    text = (L / "request.txt").read_text(encoding="utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1
    )[1])
    assert checkpoint["batch088NativeExecutionCheckpoint"]["savedCommit"] == HEAD
    shutil.copyfile(C / "progress.json", L / "progress-before-624.json")
    state = load(C / "progress.json")
    state["execution624StartingState"] = {
        "execution": 624, "batch": "088", "startedAt": now(),
        "startingHead": HEAD, "androidHead": ANDROID,
        "scope": "SAME088 original-session serial dependent visual confirmations and normally signed LOCAL evidence checkpoint; no publication or089.",
        "request": {"sha256": sha(L / "request.txt"), "characters": len(text),
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded; operative contract, approved issue and final623 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": "Live parent19008 verified through current child ancestry and exact runner session; no child lock acquisition/delete/unlock.",
        "artifactPathPreflight": "Committed sources and approved control helpers/inputs only; no optional historical session recipes accessed.",
        "actualNewPermissionDenials": [],
    }
    state["stage"] = "batch-088-dependent-visual-confirmations"
    state["nextAction"] = "SAME088 original Claude then original GPT serial dependent visual confirmations; preserve complete reports and actual model/read/process limits, then local checkpoint."
    save(C / "progress.json", state)
    parts = [
        f"DEPENDENT VISUAL EVIDENCE: signed frozen HEAD {HEAD}; unchanged teaching {TEACHING}.",
        "Not a new blind initial review. Native assertions are supplied coordinator evidence, not reviewer-executed tests. No other reviewer's report or adjudication is supplied.",
    ]
    for path in [R / "kanji" / "\u51f1.md", R / "words" / "\u51f1\u65cb.md",
                 N / "execution.json", N / "n1-088-article-route.json",
                 N / "inspection" / "contact-map.json"]:
        parts.append(f"RESOURCE {path}; SHA256 {sha(path)}\n{path.read_text(encoding='utf-8-sig')}")
    parts.append("EXACT TEACHING DIFF FROM INITIAL REVIEW SNAPSHOT TO CURRENT HEAD:\n" +
                 git("diff", TEACHING, HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json"))
    parts.append("ACTUAL PNGS TO VIEW SERIALLY:\n" + "\n".join(map(str, IMAGES)))
    PACKET.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    save(C / "batch-088-visual-624-inputs.json", {
        "packet": {"path": str(PACKET), "sha256": sha(PACKET)},
        "images": [{"path": str(path), "sha256": sha(path)} for path in IMAGES],
        "head": HEAD, "teachingSnapshot": TEACHING,
    })
    print("Prepared", PACKET.stat().st_size, "bytes and", len(IMAGES), "images")


def run(label, supplement=False):
    frozen()
    model, session = SESSIONS[label]
    if label == "gpt":
        prior = load(C / "batch-088-visual-624-claude-execution.json")
        assert prior["exitCode"] == 0 and not prior["unfinishedTools"]
        assert prior["allAssignedResourcesSuccessfullyReturned"]
        correction = load(C / "batch-088-visual-624-claude-serial-text-execution.json")
        assert correction["exitCode"] == 0 and not correction["unfinishedTools"]
        assert not correction["observedToolOverlaps"]
        assert correction["allAssignedResourcesSuccessfullyReturned"]
        assert correction["actualModels"] == [SESSIONS["claude"][0]]
        assert correction["startedAt"] > prior["completedAt"]
        for record in [prior, correction]:
            assert subprocess.run(["pwsh", "-NoProfile", "-Command",
                                   f"if(Get-Process -Id {record['launcherPid']} -ErrorAction SilentlyContinue){{exit 1}}"],
                                  capture_output=True).returncode == 0
    prefix = C / (f"batch-088-visual-624-{label}" + ("-serial-text" if supplement else ""))
    raw = prefix.with_suffix(".jsonl")
    assert not raw.exists(), "Never overwrite original report"
    catalog = (C / "batch-088-cli-config-reference-execution-624.txt").read_text(encoding="utf-8-sig")
    assert f'"{model}"' in catalog
    inputs = load(C / "batch-088-visual-624-inputs.json")
    assert sha(PACKET) == inputs["packet"]["sha256"]
    assert all(sha(Path(item["path"])) == item["sha256"] for item in inputs["images"])
    prompt = f"""DEPENDENT VISUAL FOLLOW-UP in your ORIGINAL session {session}, model {model}.
Frozen signed evidence HEAD {HEAD}; original teaching {TEACHING} UNCHANGED (exact diff supplied). This is NOT a new blind initial review.
MANDATORY: EXACTLY ONE view call per assistant response, including the first TWO TEXT reads; wait for its result before requesting the next. Do NOT batch even independent text reads. This overrides generic tool-efficiency instructions for this bounded review.
First read ONLY your OWN original report {V / ('batch-088-initial-' + label + '.md')}. In a SEPARATE subsequent response read the ENTIRE {PACKET} with forceReadLargeFiles=true. Then VIEW ALL ELEVEN actual PNG paths at its end, one tool call per response, serially: eight mapped whole-frame contact sheets cover all46 screenshots; three full-size original Compose font panels. Additional originals under {N} are available if required for readability. If image decoding/vision is unavailable or text is truncated, disclose it and recover missing ranges serially; never substitute hashes/cmap/hasGlyph or author opinion for vision. Only view is exposed; no shell, edits, delegation, parallel calls, other reviewer's reports or coordinator visual opinions.

Assess EACH new kanji\\凱.md and words\\凱旋.md for rendered comprehensibility; inherit previous textual correctness/coverage unless images establish a new defect. Check all27 scoped Han in four production font selections Gothic/Mincho/Textbook/Brush, especially 几 U+51E0 versus 凡, 豈 U+8C48 with 山/豆, 鬨 U+9B28. Paint108individual+4wholeword probes are recycled hashes, NOT112exported/viewedPNGs or identifiedfallbackface. Actual glyph evidence is Compose panels. No cosmetic font-uniformity requirement.
Inspect BOTH complete article projections, allfour reading rows, source-onlyカイ/かちどき/やわらぐ versus selectedガイ, ordinary勝どき/勝鬨/和らぐ and凱風がいふう. Distinguish charactergloss/reading from ordinarywordspelling and metadata grade9 from name-only. Horizontal table can scroll: complementary left/right captures expose explanations; assess actual readability, not static clipping alone.
Inspect victorious-return examples/readings/translations, noun/intransitivesuru/subjectが/destinationにへ versus nominalを祝う, military/sports/performance and compound-specific旋return, one reciprocalpair/twodirections/restoredSystemBack/offline navigation.
Check actual pictured and supplied production N1 AND All four meaning options: victorysong;triumph versus 凡 commonplace;mediocre, 凸 convex;protruding, 凹 concave;sunken; allthree curatedwrongcards available, zero fallback. Actual question reading alternatives too; singleonがい Good and1of1done, explicitkun[], fullrawonガイ/カイ andkunかちどき/やわらぐ/order unchanged. Confirm original fallback-unverified limit ONLY for these tested configurations, not everyfuturecustompool/oldclient.
Inspect N1selection120cards, twelvestroke injectedtrace/practicefeedback/recallgiveup. Supplied native fullarchivee445d826 productionContentSyncONCE imported1111kanji5067words120N1zeroproblems/acceptedVersionafff40af0e155dbe/epoch1; both terminalcase0/no skips. These are supplied receipts, NOT your executed tests. Trace/giveup is not humanhandwriting or offlineMLKit; unavailablemodel/shape-only feedback explicit. Qualified TESTONLY Android1c1b7bf4 retains productionf9b59a2, NOT latestappmain. No new nativephone acceptance.

Return COMPLETE report: Snapshot;Scope(actualmodel, actualtext/image reads);Verdicts(separate correctness/scopedcoverage/renderedcomprehensibility for EACH article, identify inheritedtextual conclusions);Findings(severity;facet;file/PNG:location;claim+impact;remedy;evidence;confidence, ornone);Optional;Limits. Reconcile your own prior limitations to evidence, preserve remaining uncertainty. Disclose exact incomplete reads/images; API35 emulator not physicalphone/native-speaker, contactsheet scaling versus originalpanels, not identifiedfallbackface or112PaintPNGs. Currentmain integration/combinedchecks/CI/publicZIP/publication/phone/generalrelease/whole-set remain later gates. No edits/questions/nextbatch.
"""
    if supplement:
        assert label == "claude"
        prior = load(C / "batch-088-visual-624-claude-execution.json")
        assert prior["exitCode"] == 0 and prior["allAssignedResourcesSuccessfullyReturned"]
        assert len(prior["observedToolOverlaps"]) == 1
        prompt = f"""Bounded PROCESS CORRECTION in the SAME original Claude session {session}. No new blind review or image-reread credit.
Your prior visual follow-up returned complete, but execution evidence detected overlapping first TWO TEXT reads (own original report and visual packet). ALL ELEVEN image reads were actually serial and decoded; preserve that original report and all original process evidence. Do not claim the entire prior run was serial. Frozen HEAD {HEAD}, unchanged teaching {TEACHING}; no edits have occurred.
Correct only the missed serial text-reading operation now. EXACTLY ONE view call PER assistant response: FIRST read ONLY {V / 'batch-088-initial-claude.md'} in full. WAIT for the tool result. In a separate subsequent response read ONLY {PACKET} in full with forceReadLargeFiles=true. WAIT for the result. Do not batch these calls or view images/other resources; the original eleven serial image observations remain available in this same session. Only view exposed, no shell/edit/delegation.
Then provide a compact COMPLETE dependent confirmation report Snapshot;Scope;Verdicts(EACHarticle correctness/scopedcoverage inherited and renderedcomprehensibility from your prior actual eleven serial image reads);Findings;Optional;Limits. State whether sequential fresh text reads change any prior conclusion. Preserve original optional suggestions and evidence limitations without manufacturing findings. Explicitly acknowledge original two-text overlap versus serial images and this corrective two-text read. No new native/source/phone/whole-project claim.
"""
    prefix.with_suffix(".prompt.txt").write_text(prompt, encoding="utf-8")
    command = [shutil.which("copilot"), "-C", str(R), "--add-dir", str(C),
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
        process = subprocess.Popen(command, stdout=out, stderr=err, env=env)
        save(prefix.with_suffix(".active.json"), {
            "pid": process.pid, "sessionId": session, "model": model,
            "command": command, "startedAt": started,
        })
        print("Started original-session reviewer", label, process.pid, session, flush=True)
        code = process.wait()
    events = [json.loads(line) for line in raw.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    messages = [event["data"] for event in events if event["type"] == "assistant.message"]
    prefix.with_suffix(".md").write_text(
        messages[-1].get("content", "") + "\n" if messages else "No completed report.\n", encoding="utf-8")
    active, calls, overlaps = set(), {}, []
    required = {str(PACKET), str(V / f"batch-088-initial-{label}.md")}
    if not supplement:
        required.update(str(path) for path in IMAGES)
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
                         "truncationMarker": any(marker in result for marker in [
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
        "execution": 624, "batch": "088", "snapshot": HEAD,
        "originalTeachingSnapshot": TEACHING,
        "dependentOriginalSession": True, "newBlindReviewCredit": False,
        "serialTextCorrectionOnly": supplement,
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
        "configurationEvidence": [event["data"] for event in events
                                  if event["type"] == "session.info" and
                                  event["data"].get("infoType") == "configuration"],
        "limits": "Successful PNG returns prove resource delivery, not comprehension. Original report determines actual visual capability/inspection.",
    }
    save(C / (prefix.name + "-execution.json"), record)
    print(json.dumps({key: record[key] for key in [
        "exitCode", "actualModels", "missingResources", "observedToolOverlaps"]}, ensure_ascii=True))
    assert code == 0 and record["actualModels"] == [model]
    assert usage and usage["currentModel"] == model
    assert not active and not overlaps and not (required - returned)
    frozen()


if __name__ == "__main__":
    if sys.argv[1] == "prepare":
        prepare()
    elif sys.argv[1] in SESSIONS:
        run(sys.argv[1])
    elif sys.argv[1] == "claude-serial-text":
        run("claude", supplement=True)
    else:
        raise ValueError(sys.argv[1])

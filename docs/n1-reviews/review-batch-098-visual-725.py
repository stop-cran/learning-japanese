import base64
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
V = R / "docs" / "n1-reviews"
N = V / "batch-098-native" / "execution-724"
L = C / "logs" / "55343788-f20f-4a3c-b000-c3e5bbd06cc5"
HEAD = "7e03dede82cd517518b7debb8918ff0390477b78"
TEACHING = "233d3add2b90fcb98f9706b8901aa936fc6e56e7"
ANDROID = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
PACKET = C / "batch-098-visual-725-packet.txt"
SESSIONS = {
    "claude": ("claude-opus-5.5", "d41cdccb-18bc-4302-803f-803d7bd4a007"),
    "gpt": ("gpt-6.1-sol", "33216339-ddd8-411a-8aca-b73da1a3bae7"),
}
IMAGES = [N / f"n1-098-font-panel-{i}.png" for i in range(1, 4)]
IMAGES += [N / "contact-sheets" / f"sheet-{i:02d}.png" for i in range(1, 13)]
IMAGES += [N / name for name in [
    "n1-098-meaning-question.png", "n1-098-selection.png",
    "n1-098-kanji-11.png", "n1-098-kanji-20.png", "n1-098-kanji-36.png",
    "n1-098-curated-\u3056\u3044-question.png", "n1-098-curated-\u3056\u3044-feedback.png",
    "n1-098-drawing-feedback.png",
]]


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def git(*args, root=R):
    return subprocess.check_output(
        ["git", "--no-pager", "-C", str(root), *args], encoding="utf-8"
    ).rstrip("\r\n")


def ownership():
    subprocess.run(["pwsh", "-NoProfile", "-File", str(C / "preflight-725.ps1")], check=True)


def frozen():
    ownership()
    for root, expected in ((R, HEAD), (A, ANDROID)):
        assert git("rev-parse", "HEAD", root=root) == expected
        assert git("log", "-1", "--format=%G?", root=root) == "G"
        assert not git("status", "--porcelain=v1", "--untracked-files=all", root=root)
    state = load(C / "progress.json")
    assert state["checkpoint"] == 724 and state["batch"] == "098"
    assert not git("diff", TEACHING, HEAD, "--",
                   "kanji", "words", "articles", "strokes", "manifest.json", "tools")


def prepare():
    frozen()
    assert not PACKET.exists() and not (L / "progress-before-725.json").exists()
    state = load(C / "progress.json")
    request = L / "request.txt"
    text = request.read_text(encoding="utf-8-sig")
    embedded = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1
    )[1])
    assert embedded["execution724CoordinatorCheckpoint"] == state["execution724CoordinatorCheckpoint"]
    shutil.copyfile(C / "progress.json", L / "progress-before-725.json")
    state["execution725StartingState"] = {
        "execution": 725, "batch": "098", "startingHead": HEAD, "androidHead": ANDROID,
        "startedAt": now(), "runnerLockRole": load(L / "preflight-725.json"),
        "scope": "SAME098 original Claude then original GPT serial dependent rendered confirmations and signed LOCAL evidence checkpoint; no publication/099/Android/native rerun.",
        "request": {
            "sha256": sha(request), "bytes": request.stat().st_size,
            "characters": len(text), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded/decoded; operative contract, complete issue and final724 inspected directly. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "artifactPathPreflight": "Approved control and committed source/review packets only; no optional historical-session helper access.",
        "actualNewPermissionDenials": [],
    }
    state.update(stage="batch-098-original-session-dependent-rendered-confirmations",
                 nextAction="SAME098 serial original Claude then original GPT rendered confirmations; preserve reports, actual model/image/process evidence and reconcile before signed local checkpoint. No publication/099.")
    save(C / "progress.json", state)
    for name, args in (("help", ["--help"]), ("config", ["help", "config"])):
        result = subprocess.run([shutil.which("copilot"), *args], capture_output=True, check=True)
        (C / f"batch-098-visual-cli-{name}-725.txt").write_bytes(result.stdout)
    catalog = (C / "batch-098-visual-cli-config-725.txt").read_text(encoding="utf-8-sig")
    assert all(f'"{model}"' in catalog for model, _ in SESSIONS.values())
    for item in load(N / "artifact-index.json"):
        assert sha(R.joinpath(*item["path"].split("/"))) == item["sha256"]
    parts = [
        f"DEPENDENT RENDERED FOLLOW-UP: signed evidence HEAD {HEAD}; unchanged teaching {TEACHING}.",
        "Not new blind initial review. No other reviewer's report or coordinator visual opinions included. Native assertions below are supplied receipts, NOT reviewer-executed tests.",
    ]
    for path in [
        R / "kanji" / "\u5264.md", R / "words" / "\u6d17\u5264.md",
        R / "kanji" / "\u6d17.md", N / "n1-098-article-route.json",
        N / "contact-sheets" / "index.json",
    ]:
        parts.append(f"RESOURCE {path}; SHA256 {sha(path)}\n{path.read_text(encoding='utf-8-sig')}")
    native = load(R / "docs" / "n1-sources" / "execution-724.json")
    parts.append("SUPPLIED NATIVE EXECUTION RECEIPT:\n" +
                 json.dumps(native["nativeExecution"], ensure_ascii=True, indent=2))
    parts.append("EXACT ORIGINAL TEACHING DIFF:\n" + git(
        "-c", "core.quotepath=false", "diff",
        "0ccfbcc2ee066534a28414d428d6fc3a6240ef67", TEACHING, "--", "kanji", "words"))
    parts.append("TEACHING DIFF FROM INITIAL REVIEW TO CURRENT HEAD (empty):\n" +
                 git("diff", TEACHING, HEAD, "--", "kanji", "words", "strokes", "articles", "manifest.json"))
    parts.append("VIEW ALL 23 PNGS IN ORDER, ONE CALL PER ASSISTANT MESSAGE:\n" +
                 "\n".join(map(str, IMAGES)))
    PACKET.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    save(C / "batch-098-visual-725-inputs.json", {
        "packet": {"path": str(PACKET), "sha256": sha(PACKET)},
        "images": [{"path": str(path), "sha256": sha(path)} for path in IMAGES],
        "originalCaptures": 48, "contactSheets": 12, "fontPanels": 3,
        "additionalOriginalResolutionRouteReads": 8, "assignedPngViews": len(IMAGES),
        "snapshot": HEAD, "teachingSnapshot": TEACHING,
    })
    print("Prepared", PACKET.stat().st_size, "bytes and", len(IMAGES), "PNG views", flush=True)


def prompt(label, model, session):
    return f"""DEPENDENT rendered confirmation in your ORIGINAL reviewer session {session}, requested actual model {model}.
Evidence signed HEAD {HEAD}; teaching remains {TEACHING}. This is NOT a new blind initial review.
Resource constraint: EXACTLY ONE view call per assistant message, including texts. Interpret each returned resource before deciding the next call; never batch or use a parallel wrapper. Only view is exposed; no shell, edits, delegation, other reports or coordinator visual opinions.
FIRST read ONLY your own original report {V / ('batch-098-initial-' + label + '.md')}.
In a SEPARATE assistant message read ENTIRE {PACKET} using forceReadLargeFiles=true, no range. Then view ALL23 PNGs listed at its end IN ORDER, ONE call per message: THREE original font panels, TWELVE mapped contact sheets covering45route captures, EIGHT additional original-resolution route images. These represent48original captures, not23independent renderings or48separate original-resolution views. Additional originals at {N} available only if legibility needs them. Disclose resizing/incomplete evidence; never infer legibility from hashes/hasGlyph/cmap.

Assess COMPLETE new kanji\\剤.md, and EXACT reused words\\洗剤.md:28 component-link and kanji\\洗.md:38 linked-word changes. Full reused articles are context, NOT a new full linguistic review. Inherit OWN initial textual correctness/coverage unless captures establish a defect. Reconcile own original runtime/fallback limits with ACTUAL evidence; no author verdict supplied.
All19scopedHan across FOUR production fonts Gothic/Mincho/Textbook/Brush in THREEpanels; especially剤/済/剛/則 and刀/刂/氵, fallbackU+5202/U+6C35. Distinguishability/readability rather than cosmetic uniformity.76individual+8wholewordPaint probes NOT84viewedPNGs or identifiedfallbackface. Complete剤 projection with Japanese/examples/translations and FIVErawreadingrows plus qualifying paragraphs; horizontal reading-table scroll is intended, judge complementary captures rather than static clipped column alone. Identify gaps not established by captures rather than claiming unseen text visible.
Raw onザイ/スイ/セイ andkunかる/けず.る retained in source order; ONLYquizOnyomi[ザイ], quizKunyomi[] selected. Onlyonざい offered/persistedGood/Done1of1, NOkun. Full reference readings in feedback NOT additional offered keys. Four separate source-only entries remain lookup data, not invalid/obsolete labels or modern spelling examples; no invented剤る. Reused洗剤せんざい N2metadata/title/primaryreading/originalせっけん guard unchanged; no new word/title/guard. Medicine/chemical preparation compound element is not all substances/only oral medicine; 洗剤 detergent/cleaningagent and soap category preserve nuance.
ACTUAL pictured N1 choices: 剤 medicinalpreparation/chemicalagent, 剛 sturdy/unyieldingstrength, 冶 smelt/workmetals, 刑 criminalpunishment. ONLYONE curatedwrongcard剛 available; TWOproductionfallbacks冶/刑. Curated済N3/則N2 are NOT the actual N1screen. Assess actual64kanjibuilder records/16seeds/N1+All+boundedcustom+randomN1subset in routeJSON, including every distinct displayedlabel/ordinarysecondarymeaning; 35unique samplelabels plus pictured冶. Close own unverified fallback limit ONLY tested samples; no whole-pool certification. 薬/剤 overlap concern is not resolved universally by absence from samples.
128preserved DIRECTwordguard checks for 洗剤/せっけん, All+custom/bothdirections/bothtargetorientations; check every completed four-option record in its visible operation for alternate defensible answer, not merely excludedpairabsence. Sample safety NOT universal pool proof; directexclusions NOT synonymclique.
N1selection130cards, meaning/reading feedback, TEN supplied pinned strokes/injectedtrace/recallgiveup/persistence. Actualshape-only/modelunavailable drawing is NOThumanhandwriting/successfulMLKit/phone. TWOallmappedpairs剤-洗剤 AND洗-洗剤/FOURdirections/ONEactivatedbaseline剤-洗剤pair; links/SystemBack/offline. Supplied fullarchivecefedeb6 through productionContentSyncONCE imported1121kanji5073words130N1zeroProblems/contentVersion0cbdc2723b0433f2/RoomreadingEpoch1. TWOcases terminalpercase0/noskips; own helper5580 stopped. These are supplied receipts NOT your tests. QualifiedTESTONLYAndroid1c1b7bf4 retains productionf9b59a2, NOTlatestappmain. API35/defaultfontscale1 NOTphysicalphone.

Return COMPLETE report: Snapshot;Scope(actual model/resources/images/provenance);Verdicts(correctness/scopedcoverage/renderedcomprehensibility EACH new article/exactreusedpassage, mark inheritedtextual conclusions);Findings(severity;facet;file/PNG:location;preciseclaim+impact;minimalremedy;evidence;confidence ornone);Optional;Limits.
Reconcile OWN previous concerns with actual sampledoptions; preserve consequentialunresolvedclaims asUNVERIFIED rather than CLEAN. Explain if evidence only closes bounded testedconfigs. No mandatory finding quota. No edits/questions/nextbatch. Combinedcurrentmainchecks/CI/publicZIP/publication/phone/generalrelease/whole-set gates remain.
"""


def run(label):
    frozen()
    if label == "gpt":
        prior = load(C / "batch-098-visual-725-claude-execution.json")
        assert prior["exitCode"] == 0
        subprocess.run(["pwsh", "-NoProfile", "-Command",
                        f"if(Get-Process -Id {prior['launcherPid']} -ErrorAction SilentlyContinue){{exit 1}}"], check=True)
    model, session = SESSIONS[label]
    prefix = C / f"batch-098-visual-725-{label}"
    raw = prefix.with_suffix(".jsonl")
    assert not raw.exists()
    task = prompt(label, model, session)
    prefix.with_suffix(".prompt.txt").write_text(task, encoding="utf-8")
    command = [shutil.which("copilot"), "-C", str(R), "--add-dir", str(C),
               "--resume=" + session, "--model", model, "--no-ask-user",
               "--allow-tool=view", "--available-tools=view", "--disable-builtin-mcps",
               "--no-custom-instructions", "--output-format", "json",
               "--log-dir", str(C / "review-logs" / prefix.name),
               "--usage-output-file", str(prefix.with_suffix(".usage.json")), "-p", task]
    env = os.environ.copy()
    env.pop("GH_TOKEN", None)
    env.pop("GITHUB_TOKEN", None)
    started = now()
    with raw.open("wb") as out, prefix.with_suffix(".stderr.txt").open("wb") as err:
        process = subprocess.Popen(command, stdout=out, stderr=err, env=env)
        save(prefix.with_suffix(".active.json"),
             {"pid": process.pid, "sessionId": session, "model": model, "startedAt": started})
        print("Started", label, process.pid, session, flush=True)
        code = process.wait()
    events = [json.loads(line) for line in raw.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    messages = [event["data"] for event in events if event["type"] == "assistant.message"]
    prefix.with_suffix(".md").write_text(
        (messages[-1].get("content", "") if messages else "No completed report.") + "\n", encoding="utf-8")
    required = {str(PACKET), str(V / f"batch-098-initial-{label}.md"), *map(str, IMAGES)}
    active, calls, overlaps, returned, images = set(), {}, [], set(), []
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
            call = calls[key]
            result = data.get("result", {}).get("content", "")
            result = result if isinstance(result, str) else json.dumps(result)
            call.update(completedAt=event["timestamp"], success=data["success"],
                        returnedCharacters=len(result),
                        returnedSha256=hashlib.sha256(result.encode()).hexdigest(),
                        truncationMarker=any(s in result for s in [
                            "[Output truncated", "File too large to read", "<note>Content truncated",
                            "Invalid view_range"]))
            path = call["arguments"].get("path")
            if path in required and data["success"] and not call["truncationMarker"]:
                if path.endswith(".png"):
                    payloads = data.get("result", {}).get("binaryResultsForLlm", [])
                    assert len(payloads) == 1 and payloads[0]["mimeType"] == "image/png"
                    payload = base64.b64decode(payloads[0]["data"], validate=True)
                    with Image.open(io.BytesIO(payload)) as image:
                        image.load()
                        dimensions = list(image.size)
                    with Image.open(path) as image:
                        source_dimensions = list(image.size)
                    images.append({"path": path, "sourceSha256": sha(Path(path)),
                                   "sourceDimensions": source_dimensions,
                                   "returnedSha256": hashlib.sha256(payload).hexdigest(),
                                   "returnedDimensions": dimensions, "returnedBytes": len(payload)})
                    returned.add(path)
                else:
                    norm = lambda text: text.replace("\r\n", "\n").rstrip()
                    exact = norm(Path(path).read_text(encoding="utf-8-sig")) in norm(result)
                    call["entireRequestedTextContained"] = exact
                    if exact:
                        returned.add(path)
    usage = load(prefix.with_suffix(".usage.json")) if prefix.with_suffix(".usage.json").exists() else None
    groupings = [len(message["toolRequests"]) for message in messages if message.get("toolRequests")]
    record = {
        "execution": 725, "batch": "098", "snapshot": HEAD, "teachingSnapshot": TEACHING,
        "dependentOriginalSession": True, "newBlindReviewCredit": False,
        "sessionId": session, "requestedModel": model,
        "actualModels": sorted({message.get("model", "") for message in messages}),
        "usageCurrentModel": usage.get("currentModel") if usage else None,
        "launcherPid": process.pid, "startedAt": started, "completedAt": now(), "exitCode": code,
        "toolCalls": list(calls.values()), "observedToolOverlaps": overlaps,
        "unfinishedTools": sorted(active), "requiredResources": sorted(required),
        "successfullyReturnedResources": sorted(returned), "missingResources": sorted(required - returned),
        "allAssignedResourcesSuccessfullyReturned": not (required - returned),
        "exactlyOneViewPerToolBearingMessage": bool(groupings) and set(groupings) == {1},
        "actualDecodedImageReturns": images, "rawSha256": sha(raw),
        "reportSha256": sha(prefix.with_suffix(".md")), "usage": usage,
        "availableTools": ["view"], "command": command,
        "configurationEvidence": [event["data"] for event in events if event["type"] == "session.info"
                                  and event["data"].get("infoType") == "configuration"],
        "limits": "Payload/range audit establishes delivery, not comprehension. Actual report records visual observations and limitations.",
    }
    save(C / (prefix.name + "-execution.json"), record)
    print(json.dumps({key: record[key] for key in [
        "exitCode", "actualModels", "missingResources", "observedToolOverlaps"]}), flush=True)
    assert code == 0 and record["actualModels"] == [model] and usage["currentModel"] == model
    assert not active and not overlaps and not (required - returned)
    assert record["exactlyOneViewPerToolBearingMessage"]
    assert [image["path"] for image in images] == list(map(str, IMAGES))
    frozen()


if __name__ == "__main__":
    if sys.argv[1] == "prepare":
        prepare()
    elif sys.argv[1] in SESSIONS:
        run(sys.argv[1])
    else:
        raise ValueError(sys.argv[1])

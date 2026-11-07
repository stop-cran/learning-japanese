import base64
import hashlib
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

C = Path(__file__).parent
spec = importlib.util.spec_from_file_location("visual_base", C / "review-batch-089-visual-633.py")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
R, A, V = base.R, base.A, base.V
N = V / "batch-091-native" / "execution-650"
L = C / "logs" / "68d723d9-1e18-462d-92ff-95446914bd69"
HEAD = "99d11124a5eab51850be91b15c0ebd224af7f8ce"
TEACHING = "c2a59d5c1cd4ac8040156a6c067bd9d565d59116"
ANDROID = base.ANDROID
SESSIONS = {
    "claude": ("claude-opus-5.5", "075924f2-f60b-4ae0-bf3f-341db3dfbd74"),
    "gpt": ("gpt-6.1-sol", "8da57d75-100b-4996-acf7-f52b0b446472"),
}
PACKET = C / "batch-091-visual-651-packet.txt"
INSPECTION = C / "batch-091-visual-651-inspection"
load, save, sha, git, now = base.load, base.save, base.sha, base.git, base.now


def ownership():
    command = rf"""
$ErrorActionPreference='Stop'
$runner=Get-Content '{C}\runner.json' -Raw | ConvertFrom-Json
if($runner.pid -ne 19008 -or $runner.sessionId -ne '{L.name}'){{throw 'Runner identity uncertain'}}
$p=Get-CimInstance Win32_Process -Filter "ProcessId=$PID"
while($p -and $p.ProcessId -ne 19008){{$p=Get-CimInstance Win32_Process -Filter "ProcessId=$($p.ParentProcessId)"}}
if(-not $p){{throw 'Expected live parent ancestry not established'}}
$command=$p.CommandLine
if($command -match '(?i)-EncodedCommand\s+([A-Za-z0-9+/=]+)'){{
 $command=[Text.Encoding]::Unicode.GetString([Convert]::FromBase64String($Matches[1]))
}}
if(-not $command.Contains('{C}\runner.ps1')){{throw 'Parent launcher command uncertain'}}
"""
    subprocess.run(["pwsh", "-NoProfile", "-Command", command], check=True, capture_output=True)


def frozen():
    ownership()
    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert git("rev-parse", "HEAD", repo=A) == ANDROID
    assert git("log", "-1", "--format=%G?", repo=A) == "G"
    assert not git("status", "--porcelain", repo=A)
    state = load(C / "progress.json")
    assert state["checkpoint"] == 650 and state["batch"] == "091"
    assert not git("diff", TEACHING, HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json")


def prepare():
    frozen()
    assert not PACKET.exists() and not INSPECTION.exists()
    request = L / "request.txt"
    text = request.read_text(encoding="utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1
    )[1])
    assert checkpoint["execution650CoordinatorCheckpoint"]["savedCommit"] == HEAD
    shutil.copyfile(C / "progress.json", L / "progress-before-651.json")
    state = load(C / "progress.json")
    state["execution651StartingState"] = {
        "execution": 651, "batch": "091", "startedAt": now(),
        "startingHead": HEAD, "androidHead": ANDROID,
        "freshOriginMain": git("rev-parse", "origin/main"),
        "scope": "SAME091 original-session serial dependent visual confirmations and normally signed LOCAL evidence only; no publication/092.",
        "request": {"sha256": sha(request), "bytes": request.stat().st_size,
                    "characters": len(text), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request read/decoded; operative contract, complete issue and final650 inspected directly. Historical middle parsed, not freshly semantically re-reviewed. Initial root-state print encountered cp1252 output encoding; request read and JSON parse had already completed."},
        "runnerLockRole": "Live parent19008 ancestry, exact session and decoded launcher command verified; no child lock acquisition/delete/unlock.",
        "artifactPathPreflight": "Approved control helpers/inputs and committed source/evidence only; no optional historical session recipes accessed.",
        "actualNewPermissionDenials": [],
    }
    state.update(stage="batch-091-dependent-visual-confirmations",
                 nextAction="SAME091 original Claude then original GPT serial dependent visual confirmations; preserve complete reports and process/read limits, normally signed local evidence checkpoint only.")
    save(C / "progress.json", state)
    for kind, args in [("help", ["--help"]), ("config", ["help", "config"])]:
        result = subprocess.run([shutil.which("copilot"), *args], capture_output=True, check=True)
        (C / f"batch-091-visual-cli-{kind}-651.txt").write_bytes(result.stdout)
    native = load(R / "docs" / "n1-sources" / "execution-650.json")
    for artifact in native["artifacts"]:
        assert sha(R.joinpath(*artifact["path"].split("/"))) == artifact["sha256"]
    groups = {}
    for path in sorted(N.glob("*.png")):
        groups.setdefault(sha(path), []).append(path)
    assert sum(map(len, groups.values())) == 50 and len(groups) == 26
    INSPECTION.mkdir()
    representatives = [paths[0] for paths in groups.values() if "-font-panel-" not in paths[0].name]
    assert len(representatives) == 23
    sheets, mapping = [], []
    for offset in range(0, len(representatives), 2):
        pair = representatives[offset:offset + 2]
        sheet = Image.new("RGB", (1400, 1596), "white")
        draw = ImageDraw.Draw(sheet)
        sheet_path = INSPECTION / f"contact-{offset // 2 + 1:02d}.png"
        for column, path in enumerate(pair):
            with Image.open(path) as image:
                assert image.size == (1080, 2400)
                frame = image.convert("RGB").resize((700, 1556), Image.Resampling.LANCZOS)
            sheet.paste(frame, (column * 700, 40))
            draw.text((column * 700 + 5, 5), path.name, fill="black")
            mapping.append({
                "sheet": str(sheet_path), "column": column,
                "representative": str(path), "sha256": sha(path),
                "identicalOriginals": [str(p) for p in groups[sha(path)]],
                "sourceDimensions": [1080, 2400], "frameDimensions": [700, 1556],
            })
        sheet.save(sheet_path)
        sheets.append(sheet_path)
    images = sheets + [N / f"n1-091-font-panel-{i}.png" for i in (1, 2, 3)]
    contact_map = {
        "allCaptureCount": 50, "distinctByteIdentities": 26,
        "nonfontRepresentatives": 23, "sheets": 12,
        "mapping": mapping,
        "separateOriginalFontPanels": [str(p) for p in images[-3:]],
        "limits": "Whole frames resized, not cropped. Exact SHA equality accounts for duplicate captures, not separate fresh semantic inspections.",
    }
    save(INSPECTION / "contact-map.json", contact_map)
    parts = [
        f"DEPENDENT VISUAL EVIDENCE: frozen signed HEAD {HEAD}; unchanged reviewed teaching {TEACHING}.",
        "Not new blind review. Native assertions below are supplied receipts, NOT reviewer-executed tests. No other reviewer's report or coordinator visual opinions are included.",
    ]
    for path in [R / "kanji" / "\u5203.md", R / "words" / "\u5203.md",
                 N / "n1-091-article-route.json", INSPECTION / "contact-map.json"]:
        parts.append(f"RESOURCE {path}; SHA256 {sha(path)}\n{path.read_text(encoding='utf-8-sig')}")
    parts.append("NATIVE EXECUTION RECEIPT ONLY (not coordinator visual opinions):\n" +
                 json.dumps(native["executionReceipt"], ensure_ascii=False, indent=2))
    parts.append("EXACT TEACHING DIFF FROM TEXTUALLY CONFIRMED SNAPSHOT TO CURRENT HEAD:\n" +
                 git("diff", TEACHING, HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json"))
    parts.append("VIEW ALL ACTUAL PNGS SERIALLY:\n" + "\n".join(map(str, images)))
    PACKET.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    save(C / "batch-091-visual-651-inputs.json", {
        "packet": {"path": str(PACKET), "sha256": sha(PACKET)},
        "images": [{"path": str(p), "sha256": sha(p)} for p in images],
        "contactMap": {"path": str(INSPECTION / "contact-map.json"), "sha256": sha(INSPECTION / "contact-map.json")},
        "head": HEAD, "teachingSnapshot": TEACHING,
    })
    print("Prepared", PACKET.stat().st_size, "bytes;", len(images), "images; all50captures mapped.")


def make_prompt(label, model, session):
    return f"""DEPENDENT visual follow-up in your ORIGINAL session {session}, actual model {model}.
Frozen signed HEAD {HEAD}; unchanged textually confirmed teaching {TEACHING}. NOT new blind initial review.
MANDATORY: EXACTLY ONE view call PER assistant response, starting with THREE TEXT reads. Never batch text or image reads; wait for each result before requesting the next.
FIRST read ONLY your own original report {V / ('batch-091-initial-' + label + '.md')}.
SECOND read ONLY your own changed-passage confirmation {V / ('batch-091-confirmation-' + label + '.md')}.
THIRD read the ENTIRE {PACKET} with forceReadLargeFiles=true.
Then view ALL FIFTEEN PNG paths at its end, ONE call per response, SERIALLY: twelve mapped whole-frame contact sheets cover23distinct nonfontframes including all47nonfontcaptures by exactduplicate identities; three separate original Compose font panels cover remaining3captures. All50captures mapped. Additional original PNGs under {N} are available if legibility requires.
Only view exposed. No other reports/opinions, shell, edits, delegation or parallel calls. If vision unavailable/text truncated disclose and recover serially; never substitute hashes/cmap/hasGlyph for viewing.

Assess EACH new kanji\\刃.md and new words\\刃.md. No changed reused passages. Inherit original textual correctness/coverage and your own correction confirmation unless images establish a defect; no fresh dictionary-retrieval claim.
Inspect all21scopedHan in FOUR production font selections Gothic/Mincho/Textbook/Brush, especially 丶 U+4E36 and distinction 刃/刀/乃/凹/凸, 先/端 and 刃物. 84individual+4wholewordPaint probes are recycled hashes, NOT88exported/viewedPNGs or identifiedfallbackface. Actual glyph evidence is THREE Compose panels. No cosmetic font-uniformity requirement.
Inspect BOTH complete new article projections; reading table horizontally scrollable, complementary captures expose rows. Raw onジン/ニン and kunは/やいば/き.る kept in sourceorder; onlyは selected with own linkedrow and quizOnyomi[]. Recognizedジン/ニン/やいば NOTsourceonly/uniformlyrare; sourceonlyき.る without fabricated刃る. Full/Lite agreement/persistence supplied receipt, not extra offeredkeys from fullrawreferencefeedback.
Physical blade/cutting-edge PART noun は versus wholetools刀/日本刀/ナイフ/包丁. Neutral kitchen-tool/photograph sentences/readings/translations/の/が. Modernshape mnemonic NOT historicalorigin. Explicit figurativeEnglish cuttingedge/forefront contrast with先端せんたん. FIVE directwordguards 刃/刀,日本刀,端,縁,先端 not transitiveclique/physicalsynonymclaim. ONE mappedreciprocalpair/TWOdirections and extra先端forward/SystemBack/offline.
Inspect picturedN1 and supplied productionN1 AND All options: blade;cuttingedge versus乃thereupon;possessiveno/凹concave;sunken/凸convex;protruding; allthreecuratedwrongcards available/zerofallback. Close own prior fallbackunverifiedlimit ONLY for testedconfigurations, not everyfuturecustompool/oldclients; All is suppliedreceipt unless separatelypictured.
Inspect exactly ONEkunはquestion/feedback/Good/1of1Done and NOonkeys. N1selection123cards. THREEpinnedstrokes injectedtrace/practicefeedback/recallgiveup/persistence; modelunavailable/shapeonlygrading explicit. Supplied fullarchivef6b2ee39 through productionContentSyncONCE imported1114kanji5070words123N1zeroProblems/acceptedVersioncb3c857f3614485d/Roomreadingepoch1; BOTHnative terminalcase0/noskips. Receipts NOT your tests. Injectedtrace/giveup NOT humanhandwriting/successfulofflineMLKit/phone. QualifiedTESTONLYAndroid1c1b7bf4 retains productionf9b59a2, NOTlatestappmain. No new nativephone acceptance.

Return COMPLETE report: Snapshot;Scope(actual model, actual text/image reads);Verdicts(correctness/scopedcoverage/renderedcomprehensibility EACH of2newarticles, identify inheritedtextual conclusions);Findings(severity;facet;file/PNG:location;claim+impact;remedy;evidence;confidence ornone);Optional;Limits.
Reconcile OWN prior findings/limits, preserve optional suggestions/nonactionablehypotheses and uncertainty. Rawfile hashes differ from manifestnormalizedhashes whereCRLF; coordinatorverified productionLFnormalization and every8432payloadhash, not yourindependentverification.
Disclose resizedcontactsheets/originalfontpanels/incompletereads, no identifiedfallbackface/88PaintPNGs, API35 emulator not physicalphone/native-speaker. Preserve original reports/provenance/readlimits; dependentfollowup not replacementblindinitialreview. Currentmain/combinedchecks/CI/publicZIP/publication/phone/generalrelease/whole-set remain later gates. No edits/questions/nextbatch.
"""


def run(label):
    frozen()
    model, session = SESSIONS[label]
    if label == "gpt":
        prior = load(C / "batch-091-visual-651-claude-execution.json")
        assert prior["exitCode"] == 0 and prior["allAssignedResourcesSuccessfullyReturned"]
        assert not prior["unfinishedTools"] and not prior["observedToolOverlaps"]
        subprocess.run(["pwsh", "-NoProfile", "-Command",
                        f"if(Get-Process -Id {prior['launcherPid']} -ErrorAction SilentlyContinue){{exit 1}}"],
                       check=True, capture_output=True)
    prefix = C / f"batch-091-visual-651-{label}"
    raw = prefix.with_suffix(".jsonl")
    assert not raw.exists(), "Never overwrite original reviewer evidence"
    assert f'"{model}"' in (C / "batch-091-visual-cli-config-651.txt").read_text(encoding="utf-8-sig")
    inputs = load(C / "batch-091-visual-651-inputs.json")
    images = [Path(i["path"]) for i in inputs["images"]]
    assert sha(PACKET) == inputs["packet"]["sha256"]
    assert all(sha(Path(i["path"])) == i["sha256"] for i in inputs["images"])
    prompt = make_prompt(label, model, session)
    prefix.with_suffix(".prompt.txt").write_text(prompt, encoding="utf-8")
    command = [shutil.which("copilot"), "-C", str(R), "--add-dir", str(C), "--resume=" + session,
               "--model", model, "--no-ask-user", "--allow-tool=view", "--available-tools=view",
               "--disable-builtin-mcps", "--no-custom-instructions", "--output-format", "json",
               "--log-dir", str(C / "review-logs" / prefix.name),
               "--usage-output-file", str(prefix.with_suffix(".usage.json")), "-p", prompt]
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
    messages = [e["data"] for e in events if e["type"] == "assistant.message"]
    prefix.with_suffix(".md").write_text(
        (messages[-1].get("content", "") if messages else "No completed report.") + "\n", encoding="utf-8")
    required = {str(PACKET), str(V / f"batch-091-initial-{label}.md"),
                str(V / f"batch-091-confirmation-{label}.md"), *map(str, images)}
    active, calls, overlaps, returned, decoded = set(), {}, [], set(), []
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
            call.update({"completedAt": event["timestamp"], "success": data["success"],
                         "returnedCharacters": len(result),
                         "returnedSha256": hashlib.sha256(result.encode()).hexdigest(),
                         "truncationMarker": any(s in result for s in [
                             "[Output truncated", "File too large to read", "<note>Content truncated",
                             "Invalid view_range"])})
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
                    decoded.append({"path": path, "sourceSha256": sha(Path(path)),
                                    "sourceDimensions": source_dimensions,
                                    "returnedSha256": hashlib.sha256(payload).hexdigest(),
                                    "returnedDimensions": dimensions, "returnedBytes": len(payload)})
                    returned.add(path)
                else:
                    norm = lambda s: s.replace("\r\n", "\n").rstrip()
                    exact = norm(Path(path).read_text(encoding="utf-8-sig")) in norm(result)
                    call["entireRequestedTextContained"] = exact
                    if exact:
                        returned.add(path)
    usage = load(prefix.with_suffix(".usage.json")) if prefix.with_suffix(".usage.json").exists() else None
    record = {
        "execution": 651, "batch": "091", "snapshot": HEAD, "teachingSnapshot": TEACHING,
        "dependentOriginalSession": True, "newBlindReviewCredit": False,
        "sessionId": session, "requestedModel": model,
        "actualModels": sorted({m.get("model", "") for m in messages}),
        "usageCurrentModel": usage.get("currentModel") if usage else None,
        "launcherPid": process.pid, "startedAt": started, "completedAt": now(), "exitCode": code,
        "command": command, "toolCalls": list(calls.values()), "observedToolOverlaps": overlaps,
        "unfinishedTools": sorted(active), "requiredResources": sorted(required),
        "successfullyReturnedResources": sorted(returned), "missingResources": sorted(required - returned),
        "allAssignedResourcesSuccessfullyReturned": not (required - returned),
        "actualDecodedImageReturns": decoded, "rawSha256": sha(raw),
        "reportSha256": sha(prefix.with_suffix(".md")), "usage": usage,
        "availableTools": ["view"],
        "configurationEvidence": [e["data"] for e in events if e["type"] == "session.info"
                                  and e["data"].get("infoType") == "configuration"],
        "limits": "Payload/range audit establishes delivery, not comprehension. Actual report records visual observations and limitations.",
    }
    save(C / (prefix.name + "-execution.json"), record)
    print(json.dumps({k: record[k] for k in [
        "exitCode", "actualModels", "missingResources", "observedToolOverlaps"]}))
    assert code == 0 and record["actualModels"] == [model] and usage["currentModel"] == model
    assert not active and not overlaps and not (required - returned)
    assert [i["path"] for i in decoded] == list(map(str, images))
    frozen()


if __name__ == "__main__":
    if sys.argv[1] == "prepare":
        prepare()
    elif sys.argv[1] in SESSIONS:
        run(sys.argv[1])
    else:
        raise ValueError(sys.argv[1])

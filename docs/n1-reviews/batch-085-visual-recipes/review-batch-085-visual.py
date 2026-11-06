import base64
import gzip
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from PIL import Image

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
V = R / "docs" / "n1-reviews"
N = V / "batch-085-native" / "attempt-596"
L = C / "logs" / "49d7da9a-f013-459b-b094-bb8f50eebfe0"
HEAD = "6921ddbd75e93e43974d2e9340f41c7f8848e626"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
SESSIONS = {
    "claude": ("claude-opus-5.5", "58040cfc-7f07-4bd0-bb1e-18ba6bf9c793"),
    "gpt": ("gpt-6.1-sol", "7e74aba9-d92a-4615-b858-c68100c7dfdb"),
}
PREFIX = "batch-085-visual"


def load(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def save(p, data):
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def now():
    return datetime.now().astimezone().isoformat()


def git(root, *args):
    return subprocess.check_output(
        ["git", "--no-pager", "-C", str(root), *args], encoding="utf-8"
    ).strip()


def persist(p):
    temp = C / "progress.597.tmp"
    assert not temp.exists()
    save(temp, p)
    assert load(temp) == p
    temp.replace(C / "progress.json")


def ancestry():
    rows = json.loads(subprocess.check_output([
        "pwsh", "-NoProfile", "-Command",
        "$i=$PID;$rows=@();while($i){$p=Get-CimInstance Win32_Process -Filter \"ProcessId=$i\";"
        "if(!$p){break};$rows+=($p|Select-Object ProcessId,ParentProcessId,CommandLine);"
        "$i=$p.ParentProcessId};ConvertTo-Json -InputObject $rows -Depth 4"
    ], encoding="utf-8"))
    parent = [x for x in rows if x["ProcessId"] == 19008]
    assert len(parent) == 1, "Uncertain launcher ancestry"
    command = parent[0]["CommandLine"]
    if "-EncodedCommand " in command:
        command = base64.b64decode(command.split("-EncodedCommand ", 1)[1]).decode("utf-16-le")
    assert str(C / "runner.ps1").lower() in command.lower()
    runner = load(C / "runner.json")
    assert runner["pid"] == 19008 and runner["sessionId"] == L.name
    assert runner["status"] == "running"
    return rows


def heads():
    for root, expected in [(R, HEAD), (A, APP)]:
        assert git(root, "rev-parse", "HEAD") == expected
        assert git(root, "log", "-1", "--format=%G?") == "G"
    assert not git(A, "status", "--porcelain")
    changes = git(R, "status", "--porcelain", "--untracked-files=all").splitlines()
    assert all(x.startswith("?? docs/n1-reviews/batch-085-visual-") for x in changes), changes
    p = load(C / "progress.json")
    assert p["checkpoint"] == 596 and p["batch"] == "085" and p["status"] == "continue"
    assert load(C / "runner.json")["pid"] == 19008


def frozen():
    heads()
    f = load(V / (PREFIX + "-freeze.json"))
    for row in f["sources"] + f["resources"]:
        assert sha(Path(row["path"])) == row["sha256"], row["path"]
    assert sha(V / (PREFIX + "-task.txt")) == f["taskSha256"]
    return f


def prepare():
    heads()
    assert not git(R, "status", "--porcelain")
    backup = L / "progress-before-597.json"
    assert not backup.exists()
    shutil.copyfile(C / "progress.json", backup)
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    state = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1
    )[1])
    assert state["execution596CoordinatorCheckpoint"]["savedCommit"] == HEAD
    rows = ancestry()
    save(L / "runner-ancestry-597.json", rows)
    p = load(C / "progress.json")
    p["execution597StartingState"] = {
        "execution": 597, "batch": "085", "startedAt": now(),
        "startingHead": HEAD, "androidHead": APP,
        "freshOriginMain": git(R, "rev-parse", "origin/main"),
        "scope": "SAME085 serial original-family dependent visual confirmations and signed local evidence; no integration/publication/086.",
        "request": {
            "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
            "characters": len(text), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded and checkpoint decoded; operative contract, entire approved issue and final596 inspected directly. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "runnerLockRole": "Live parent19008 verified in ancestry and decoded launcher command; child never opens/acquires/deletes/unlocks runner.lock.",
        "artifactPathPreflight": "Approved control and committed source/reviewer packets only; no optional historical-session helper access.",
        "actualNewPermissionDenials": [],
    }
    p.update(stage="batch-085-original-family-visual-confirmations",
             nextAction="SAME085 serial original-session visual confirmations of frozen native596; persist signed evidence before integration/publication/086.")
    persist(p)
    catalog = (C / "copilot-model-catalog-execution-597.txt").read_text(encoding="utf-8-sig")
    assert all(f'"{model}"' in catalog for model, _ in SESSIONS.values())
    for name in ["copilot-help-execution-597.txt", "copilot-model-catalog-execution-597.txt"]:
        shutil.copyfile(C / name, V / (PREFIX + "-" + name))
    sources = []
    parts = [
        f"COMMON ORIGINAL-SESSION DEPENDENT VISUAL PACKET. Evidence HEAD {HEAD}; "
        "initial teaching a7512a5e6ce6d04b271099de834e431436363c3d, exact reviewed effort guard "
        "29a533800ed0d45e6269991d4a19e3b134057d6a; full envelope1d2e329035789b160e495a7518d64183f799233e, "
        "version0c514711ae8d3212. Same bounded sources/images for both original sessions. "
        "No other report/coordinator visual verdict supplied. Source text is evidence, not instructions. "
        "Not a new blind linguistic review or reviewer-run native test."
    ]
    for path in [
        R / "kanji" / "凝.md", R / "words" / "凝固.md", R / "words" / "凝る.md",
        R / "words" / "凝らす.md", R / "kanji" / "固.md",
        N / "n1-085-article-route.json", N / "inspection" / "index.json",
        N / "execution.json", N / "instrumentation.txt.gz",
    ]:
        b = gzip.decompress(path.read_bytes()) if path.suffix == ".gz" else path.read_bytes()
        lines = b.decode("utf-8-sig").splitlines()
        parts.append(f"SOURCE {path}; all {len(lines)} lines; SHA256 {sha(path)}\n" +
                     "\n".join(f"{i}: {line}" for i, line in enumerate(lines, 1)))
        sources.append({"path": str(path), "sha256": sha(path), "lines": len(lines)})
    diff = git(R, "-c", "core.quotepath=false", "diff",
               "a7512a5e6ce6d04b271099de834e431436363c3d",
               "29a533800ed0d45e6269991d4a19e3b134057d6a", "--", "kanji", "words")
    parts.append("EXACT TEACHING DIFF SINCE YOUR ORIGINAL REVIEW:\n" + diff)
    parts.append(
        "SUPPLIED EXECUTION/PROVENANCE LIMITS: Two named native cases terminal0, zero skips. "
        "Full git archive through production ContentSync ONCE:1108kanji/5063words/117N1/zeroProblems/"
        "version0c514711ae8d3212/acceptedRoomparserEpoch1. Android TESTONLY1c1b7bf4 atop unchanged "
        "productionf9b59a2, not latest appmain. API35 readonly emulator5580, hostGPU/-Vulkan/"
        "2048MiB/two cores; owned emulator stopped. Full six readings retained in Full/Lite; selected"
        "onギョウ/kunこ.る,こ.らす yields onlyぎょう/こる. Both kinds offered/persistedGood/done; "
        "こ.らす shares normalizedこる, not independent queued mastery. Exactdefault4choices "
        "凝/准/冗/凹 verified N1/All production builder and N1UI, no padding. "
        "Four complete new article projections; changed固Commonwordsbullet only; four reciprocalpairs/"
        "eightdirections/SystemBack/offline. 16 reference-INJECTED touchstrokes/trace/recallgiveup/"
        "gradepersistence NOT humanhandwriting or MLKit; offline handwritingmodel unavailable. "
        "39actualHan (37original plus努力 for Q1), four productionfamilies Gothic/Mincho/Textbook/Brush, "
        "156individual/12wholewordrasterprobes and three Composepanels. Probe counts are not PNGreadcounts "
        "or fallbackfaceidentity. All39 displayed in firsttwo panels; thirdfocused "
        "凝/疑/准/冗/凹/冫/隹/凍/固/硬 plus凝固/凝る/凝らす. "
        "Check actual glyph distinction especially冫/隹. Cmapabsence is not glyphfailure; stylechange alone "
        "notdefect. Initial all40 fallbackinspection inherited, not repeated. Originalsixreadings/"
        "sourcefamilies/optionaldispositions remain; Q1effortguard alreadytextuallyresolved. "
        "15 labelled full-frame aspect-preserving sheets represent all87 originals, no crop, "
        "thumbnail<=600x1320; tool may resize AGAIN. Eight focused originalpaths also supplied, "
        "which tool may resize. Disclose real readdepth, not87fullresolutionreads. "
        "Horizontaltables signposted/autoscrolled targetcells; not allcolumns simultaneous. "
        "Natural viewportedges not automatically contentloss. Physicalphone/generalrelease/whole-set/"
        "currentmainintegration/publication/CI/immutableZIP remain outstanding. Notownerprogress, "
        "native-speaker/corpus/randompool/learningeffectiveness certification."
    )
    packet = V / (PREFIX + "-source-packet.txt")
    assert not packet.exists()
    packet.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    images = [N / "inspection" / f"sheet-{i:02d}.png" for i in range(1, 16)]
    images += [N / ("n1-085-" + name + ".png") for name in [
        "font-panel-1", "font-panel-2", "font-panel-3", "drawing-feedback",
        "kanji-20", "effort-13", "curated-Kun-feedback", "absorbed-14",
    ]]
    task = f"""SAME085 ORIGINAL-SESSION dependent visual confirmation, evidenceHEAD {HEAD}.
Reuse YOUR OWN initial and textual-confirmation findings; no other review/coordinator visual verdict supplied. Not new blind lexical review.
Host dispatches exactly ONE resource per CLI process/turn: complete common packet, then15 full-frame labelled sheets covering all87originals, then8 focused originalpaths, thenzero-tool complete report. ExactlyONEviewcall per resource turn, tools SERIAL. No shell/edit/delegation/parallelcalls/unassignedreads or overallverdict before final. Stop/report actual denial or missing evidence; do not circumvent.
Review all FOUR new articles kanji凝,words凝固/凝る/凝らす and ONLYchanged固Commonwordsbullet: correctness/scopedcoverage/boundednativecomprehensibility separately. Inspect actual rendered Japanese/English/kana/examples/translations and scroll states collectively. Tables horizontallyscrollable/signposted; targetcells shifted, notsimultaneousallcolumns. Distinguish genuine learner-impact from ordinaryviewportedges.
Inspect39Han across FOURproductionfamilies in THREEComposepanels, particularly凝/疑/准/冗/凹/冫/隹/凍/固/硬 and wholewords凝固/凝る/凝らす. Blank/tofu/materiallymisleadingcollapsedlookalike isdefect; meretypefacechange isnot. Cmap/hasGlyph/rasterassertions cannotidentifyfallbackface or replacepixels. All40historical fallbackinspection inherited, notfresh.
Check actualdefaultmeaningchoices凝congeal;becomeabsorbed versus准quasi-;associate rank/冗superfluous;redundant/凹concave;sunken; N1selection/readingquestion+feedback/done/drawing/article/back/offline evidence versuspixels. Fullsourceonギョウ/kunこ.る,こ.らす,こご.らす,こご.らせる,こご.る unchanged; curatedonギョウ/kunこ.る,こ.らす yieldsぎょう/こる, BOTHkindspersistedGood/done; こ.らす sharesnormalizedこる NOT independentqueuedmastery.
Q1direct努力exclusion resolved byboth originaltextualconfirmations; exactdiffsupplied. Preserve originaloptional and unresolvedlimits; nofreshcompletefamily/corpusclaim. Sourcepacket supplies terminalcase0 BOTHnativecases, fullproductionContentSyncONCE1108kanji5063words117N1/zeroProblems/version/epoch1 and fourreciprocalpairs/eightdirections. 16referenceinjectedstrokes/recallgiveup isNOThumanhandwriting/MLKit/phone; offline model unavailable. QualifiedTESTONLYAndroid1c1b7bf4 atop unchangedproductionf9b59a2, NOTlatestappmain. Physicalphone/generalrelease/currentmainintegration/publication/CI/ZIP/whole-set remainoutstanding.
FINALcomplete report: Snapshot;Scope(actualmodel/resumedsession, actualsource/imagecoverage and toolresizing/readlimits);Verdicts(EACHfournewarticles correctness/scopedcoverage/boundednativecomprehensibility CLEAN/NEEDS FIX/UNVERIFIED; changed固bulletseparately);Findings(severity/facet/file:lines/claimimpact/remedy/evidence/confidence ornone);Optional;Limits. Reconcile own earlier render/runtimeunknowns asresolved/partiallyresolved/unresolved separately from publication/physicalphoneunknowns. CLEAN means noactionabledefect established in scoped observedtask, notexhaustivecertification. No manufacturedfinding/edits/questions/newbatch.
"""
    taskpath = V / (PREFIX + "-task.txt")
    taskpath.write_text(task, encoding="utf-8")
    save(V / (PREFIX + "-freeze.json"), {
        "execution": 597, "batch": "085", "evidenceHead": HEAD, "androidHead": APP,
        "sources": sources, "taskSha256": sha(taskpath),
        "resources": [{"path": str(path), "sha256": sha(path)} for path in [packet] + images],
        "originalPngs": 87, "contactSheets": 15, "focusedOriginalPaths": 8,
        "limits": "Hashes establish consistency, not comprehension. Sheets and view payloads are resized full frames, not87 full-resolution reads.",
    })
    frozen()
    print("Prepared early597 state, common source packet and23 image resources.", flush=True)


def run(family):
    f = frozen()
    ancestry()
    model, session = SESSIONS[family]
    prefix = PREFIX + "-" + family
    if family == "gpt":
        prior = load(V / (PREFIX + "-claude-execution.json"))
        assert prior["processAndCoverageAccepted"]
        check = subprocess.run(["pwsh", "-NoProfile", "-Command",
                                f"if(Get-Process -Id {prior['turns'][-1]['launcherPid']} -ErrorAction SilentlyContinue){{exit 1}}"])
        assert check.returncode == 0, "Previous reviewer process still present"
    folder = C / (prefix + "-turns")
    folder.mkdir(exist_ok=False)
    returned_folder = V / (prefix + "-returned")
    returned_folder.mkdir(exist_ok=False)
    task = (V / (PREFIX + "-task.txt")).read_text(encoding="utf-8")
    own = "\n\n".join((V / f"batch-085-{kind}-{family}.md").read_text(encoding="utf-8")
                       for kind in ["initial", "confirmation"])
    env = os.environ.copy()
    env.pop("GH_TOKEN", None)
    env.pop("GITHUB_TOKEN", None)
    started = now()
    rows, observations = [], []
    for i in range(len(f["resources"]) + 1):
        frozen()
        final = i == len(f["resources"])
        resource = None if final else Path(f["resources"][i]["path"])
        prompt = (
            "FINAL SAME085 dependent visual confirmation. All24resource turns exited; complete packet "
            "and23imagepayloads verified by host. NOtools/rereads. Return FULL report:\n" + task
            if final else
            f"SAME085 strict host-dispatched original-session visual resource{i+1}/24.\n"
            f"Read ONLY {resource}\nEXACTLY ONE viewcall then brief resource-specific observation andSTOP. "
            "No other reads/paralleltools/edits/shell/delegation/questions/overallverdict. Host sendsnext AFTERexit. "
            + ("Use forceReadLargeFiles=true, no view_range for ENTIRE packet.\n" + task +
               "\nYOUR OWN ORIGINAL REPORTS:\n" + own if i == 0 else
               "Inspect actual PNG pixels; disclose unreadable detail. Source and returned full-frame "
               "payload may differ due to tool resizing. Not87fullresolutionreads.")
        )
        (folder / f"turn-{i+1:02d}-prompt.txt").write_text(prompt, encoding="utf-8")
        raw = folder / f"turn-{i+1:02d}.jsonl"
        err = folder / f"turn-{i+1:02d}-stderr.txt"
        usage = folder / f"turn-{i+1:02d}-usage.json"
        cmd = [
            shutil.which("copilot"), "-C", str(R), "--add-dir", str(C),
            "--model", model, "--session-id", session, "--no-ask-user",
            "--allow-tool=view", "--disable-builtin-mcps", "--available-tools=view",
            "--no-custom-instructions", "--output-format", "json",
            "--log-dir", str(C / "review-logs" / prefix),
            "--usage-output-file", str(usage), "-p", prompt,
        ]
        begin = now()
        with raw.open("wb") as out, err.open("wb") as stderr:
            proc = subprocess.Popen(cmd, stdout=out, stderr=stderr, env=env)
            save(C / (prefix + "-active.json"), {
                "pid": proc.pid, "sessionId": session, "turn": i + 1,
                "resource": str(resource) if resource else None, "startedAt": begin,
            })
            print(f"{family} turn{i+1}/25 pid{proc.pid}", flush=True)
            code = proc.wait()
        events = [json.loads(x) for x in raw.read_text(encoding="utf-8-sig").splitlines() if x.strip()]
        messages = [e["data"] for e in events if e.get("type") == "assistant.message"]
        actual = sorted({m.get("model", "") for m in messages})
        starts = [e for e in events if e.get("type") == "tool.execution_start"]
        ends = [e for e in events if e.get("type") == "tool.execution_complete"]
        terminal = [e for e in events if e.get("type") == "result"]
        row = {
            "turn": i + 1, "launcherPid": proc.pid, "startedAt": begin,
            "completedAt": now(), "exitCode": code,
            "resource": str(resource) if resource else None,
            "requestedModel": model, "actualModels": actual, "sessionId": session,
            "rawSha256": sha(raw), "toolCalls": len(starts),
        }
        save(folder / f"turn-{i+1:02d}-process.json", row)
        assert code == 0 and actual == [model] and load(usage)["currentModel"] == model
        assert len(terminal) == 1 and terminal[0]["exitCode"] == 0
        assert terminal[0]["sessionId"] == session
        assert not terminal[0]["usage"]["codeChanges"]["filesModified"]
        assert len(starts) == len(ends) == (0 if final else 1), "Strict single-resource tool count"
        if not final:
            assert starts[0]["data"]["toolName"] == "view"
            assert starts[0]["data"]["arguments"]["path"] == str(resource)
            assert ends[0]["data"]["success"], "New failed/denied evidence; preserve and yield"
            result = ends[0]["data"]["result"]
            content = result.get("content", "")
            assert not any(x in content for x in [
                "[Output truncated", "File too large to read", "Invalid view_range", "<note>Content truncated"
            ]), "Truncated required resource"
            if i == 0:
                norm = lambda s: s.replace("\r\n", "\n").rstrip()
                assert isinstance(content, str)
                assert norm(resource.read_text(encoding="utf-8")) in norm(content), "Incomplete packet"
                row["completePacketReturned"] = True
            else:
                images = result.get("binaryResultsForLlm", [])
                assert len(images) == 1 and images[0]["type"] == "image", "Missing image payload"
                payload = base64.b64decode(images[0]["data"], validate=True)
                returned = returned_folder / resource.name
                assert not returned.exists()
                returned.write_bytes(payload)
                row["imagePayload"] = {
                    "bytes": len(payload), "sha256": sha(returned),
                    "sourceSha256": sha(resource),
                    "sourceDimensions": list(Image.open(resource).size),
                    "returnedDimensions": list(Image.open(io.BytesIO(payload)).size),
                    "exactFileBytesReturnedToModel": payload == resource.read_bytes(),
                    "returnedPayloadCopy": str(returned.relative_to(R)),
                }
                sw, sh = Image.open(resource).size
                rw, rh = Image.open(io.BytesIO(payload)).size
                assert 0 < rw <= sw and 0 < rh <= sh and abs(sw/sh - rw/rh) < 0.001
            row["singleResourceAccepted"] = True
        observation = messages[-1]["content"] if messages else "No completed report."
        observations.append(f"TURN{i+1}; {resource}\n{observation}")
        rows.append(row)
        save(folder / f"turn-{i+1:02d}-process.json", row)
        if final:
            (V / (prefix + ".md")).write_text(observation + "\n", encoding="utf-8")
        save(C / (prefix + "-partial.json"), rows)
        frozen()
    (V / (prefix + "-observations.md")).write_text("\n\n".join(observations) + "\n", encoding="utf-8")
    with gzip.open(V / (prefix + "-turns.jsonl.gz"), "wb") as combined:
        for raw in sorted(folder.glob("turn-*.jsonl")):
            combined.write(raw.read_bytes())
    for path in sorted(folder.glob("*")):
        if path.suffix != ".jsonl":
            shutil.copyfile(path, returned_folder / path.name)
    save(V / (prefix + "-execution.json"), {
        "execution": 597, "requestedModel": model, "actualModels": [model],
        "sessionId": session, "startedAt": started, "completedAt": now(),
        "exitCode": 0, "evidenceHead": HEAD, "dependentOriginalSessionConfirmation": True,
        "availableTools": ["view"], "hostSingleResourceTurns": True, "turns": rows,
        "sourcePacketComplete": True, "acceptedImagePayloads": 23,
        "processAndCoverageAccepted": True,
        "limits": "15full-frame resized sheets cover87originals plus8focusedoriginalpaths; returned dimensions archived, NOT87fullresolutionreads or comprehension certification.",
    })
    print(f"{family} original-session visual report archived; process exited.", flush=True)


if __name__ == "__main__":
    if sys.argv[1] == "prepare":
        prepare()
    elif sys.argv[1] == "run":
        run(sys.argv[2])

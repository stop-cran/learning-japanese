"""Bounded original-session confirmation of the frozen direct quiz guard."""
import gzip
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

C = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("prior683", C / "confirm-batch-094-rendered-683.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
m.SESSION = "7bece5b8-823a-4293-be99-46acd8a55ed0"
m.HEAD = "b85d7a4d40225ad829891c1c7fe3b31f8cd31afe"
R, V = m.R, m.V
L = C / "logs" / m.SESSION
HEAD = m.HEAD
VERSION = "74b7e886a1afbd46"


def frozen(final=False):
    proof = m.ownership()
    assert m.git("rev-parse", "HEAD^" if final else "HEAD") == HEAD
    for repo in [R, m.A]:
        assert m.git("log", "-1", "--format=%G?", repo=repo) == "G"
        assert not m.git("status", "--porcelain", "--untracked-files=all", repo=repo)
    assert m.git("rev-parse", "HEAD", repo=m.A) == m.APP
    p = m.load(C / "progress.json")
    assert (p["checkpoint"], p["batch"]) == (684, "094")
    return proof


def runtime():
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest, sha256
    manifest = m.load(R / "manifest.json")
    assert build_manifest(R) == manifest
    count = 0
    for kind, entries in manifest.items():
        if isinstance(entries, dict):
            for name, digest in entries.items():
                actual = m.sha(R / name) if kind in {
                    "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(R / name)
                assert actual == digest, name
                count += 1
    assert count == 8438 and manifest["contentVersion"] == VERSION
    assert not m.git("diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    return {"runtimeHashesVerified": count, "contentVersion": VERSION,
            "manifestFresh": True, "runtimeChangedThisExecution": False}


def stopped(pid):
    subprocess.run(["pwsh", "-NoProfile", "-NonInteractive", "-Command",
                    f"if(Get-Process -Id {int(pid)} -ErrorAction SilentlyContinue){{exit 1}}"],
                   capture_output=True, check=True)


def prepare():
    proof = frozen()
    before = L / "progress-before-685.json"
    assert not before.exists()
    shutil.copyfile(C / "progress.json", before)
    request = (L / "request.txt").read_text(encoding="utf-8-sig")
    checkpoint = json.loads(request.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    p = m.load(C / "progress.json")
    assert p["execution684CoordinatorCheckpoint"] == checkpoint["execution684CoordinatorCheckpoint"]
    p["execution685StartingState"] = {
        "execution": 685, "batch": "094", "startedAt": m.now(),
        "startingHead": HEAD, "androidHead": m.APP,
        "freshOriginMain": m.git("rev-parse", "origin/main"),
        "scope": "SAME094 bounded original-session correction confirmations only; signed LOCAL evidence checkpoint; no native, publication,095 or second runner.",
        "request": {"sha256": m.sha(L / "request.txt"), "characters": len(request),
                    "lines": len(request.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded and embedded checkpoint decoded. Operative contract, complete issue and final684 inspected directly; historical middle parsed, not freshly semantically re-reviewed. Initial console summary encountered cp1252 encoding error after successful complete parse; no source or checkpoint loss."},
        "runnerLockRole": proof,
        "artifactPathPreflight": "Approved control and committed packets only; no optional historical-session helper accessed.",
        "actualNewPermissionDenials": [],
    }
    p.update(stage="batch-094-original-session-correction-confirmations-in-progress",
             nextAction=p["execution685StartingState"]["scope"], blocker=None)
    m.save(C / "progress.json", p)
    m.save(L / "runtime-preflight-685.json", runtime())
    for kind, args in [("help", ["--help"]), ("config", ["help", "config"])]:
        result = subprocess.run([shutil.which("copilot"), *args], capture_output=True, check=True)
        (C / f"batch-094-correction-cli-{kind}-685.txt").write_bytes(result.stdout)
    parts = [
        f"COMMON BOUNDED CORRECTION EVIDENCE\nFrozen signed HEAD {HEAD}; contentVersion {VERSION}.\n"
        "This is dependent confirmation, NOT new blind review or corrected native/import acceptance.\n"
        "Correction base da2905cd8eee44011d02582076101d47ec97daa9.\n"
        "Only runtime payload edit: append one direct exclusion to words/削る.md; generated manifest changes.\n"
        "No title, identity, reading, level, body, link, geometry or other exclusion changed.\n"
        "Original Claude683 overlap remains rejected; accepted serial repair never retroactively changes it.",
        "EXACT RUNTIME DIFF\n" + m.git("diff", HEAD + "^", HEAD, "--", "words", "kanji", "articles", "strokes", "manifest.json"),
    ]
    for name in ["words/削る.md", "words/縮める.md"]:
        text = (R / name).read_text(encoding="utf-8-sig")
        parts.append(f"COMPLETE CURRENT {name}; SHA256 {m.sha(R / name)}\n" +
                     "\n".join(f"{i}: {s}" for i, s in enumerate(text.splitlines(), 1)))
    packet = C / "batch-094-rendered-observed-pair-683.xml"
    assert m.sha(packet) == "5bb1f9aec869ecce6a61c8cfafa761aa0ad39f2002c898559bb43d270fef3ce4"
    parts.append("COMPLETE FROZEN JMDICT FAMILIES 1298090 AND 1337570\n"
                 "Coordinator-supplied extraction from pinned implementation JMdict, not fresh upstream retrieval.\n"
                 "EDRDG CC BY-SA4.0; exact provenance in committed batch-094-rendered-packet-provenance-683.json.\n" +
                 packet.read_text(encoding="utf-8"))
    contract = (R / "docs" / "content-format.md").read_text(encoding="utf-8").splitlines()
    parts.append("PAIRWISE QUIZ CONTRACT docs/content-format.md:155-177\n" + "\n".join(contract[154:177]))
    parts.append("SUPPLIED CORRECTION AUDIT (mechanical, NOT reviewer-run or native evidence)\n" +
                 (R / "docs" / "n1-sources" / "batch-094-correction-audit-684.json").read_text(encoding="utf-8"))
    common = C / "batch-094-correction-common-685.txt"
    assert not common.exists()
    common.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    assert common.stat().st_size < 20000
    for label in m.MODELS:
        resources = [str(V / f"batch-094-rendered-683-{label}.md")]
        if label == "claude":
            resources.append(str(V / "batch-094-rendered-683-claude-serial-repair.md"))
        resources.append(str(common))
        m.save(C / f"batch-094-correction-{label}-resources-685.json", resources)
    print("Starting state persisted; exact bounded common packet prepared.", flush=True)


def review(label):
    frozen()
    runtime()
    if label == "gpt":
        prior = m.load(C / "batch-094-correction-685-claude-execution.json")
        assert prior["acceptedExecution"]
        stopped(prior["launcherPid"])
    model, session = m.MODELS[label]
    assert f'"{model}"' in (C / "batch-094-correction-cli-config-685.txt").read_text(encoding="utf-8-sig")
    resources = m.load(C / f"batch-094-correction-{label}-resources-685.json")
    prefix = C / f"batch-094-correction-685-{label}"
    raw = prefix.with_suffix(".jsonl")
    assert not raw.exists(), "Preserve original evidence; never overwrite"
    prompt = f"""DEPENDENT CORRECTION CONFIRMATION in YOUR ORIGINAL session {session}, requested model {model}.
Same frozen signed snapshot for both original models: {HEAD}, contentVersion {VERSION}.
This is NOT a fresh blind initial review. No edits while reviewers run. Only read-only view is available.
Read EXACTLY these resources IN ORDER, ONE view call per response; WAIT for result before next.
Read each complete text file without ranges (all below20KB); no parallel calls, shell, delegation or other reports.
{chr(10).join(resources)}
First resource is YOUR OWN complete683 report. Claude additionally has YOUR OWN serial repair report.
The common packet gives the exact runtime diff, both complete current articles, both complete frozen JMdict
families1298090/1337570, direct-pair quiz contract and supplied684 mechanical audit.
Your own prior finding was the actual All-stack 削る/縮める ordinary reduction-sense overlap. Appending ONLY
縮める on 削る is intended to address it. Verify the precise change, existing exclusions/order, unchanged
titles/identities/levels/readings/bodies and semantic justification, not shared-third-party transitive closure.
Assess correctness, scoped coverage and comprehensibility of this narrow metadata correction and any regression.
Distinguish source-backed textual/direct-declaration closure from NOT-YET-RUN corrected native ContentSync
and production builder checks. Supplied audit is not independent test execution. Do not claim runtime acceptance.
The original Claude683 overlapping panel reads remain rejected; serial repair does not relabel that execution.
Earlier85unchanged visual captures and682native evidence remain inherited, not corrected-archive evidence.
No need to re-read121families or images; no new native, physicalphone, handwriting/MLKit, latestappmain,
generalrelease, whole-set or publication claim. No new blind-review/discovery/model-comparison credit.
Return compact complete Snapshot; Scope(actual model/session, actual resources/limits);
Verdicts separately correctness/scopedcoverage/comprehensibility CLEAN/NEEDS FIX/UNVERIFIED for narrow
correction; Findings(severity/facet/file:lines,impact/remedy/evidence/confidence or none);
Reconciliation(resolved/partially resolved/unresolved/withdrawn/optional, separating textual from runtime);
Optional; Limits. Preserve your prior findings/optional/history; no questions or edits.
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
    started = m.now()
    with raw.open("wb") as out, prefix.with_suffix(".stderr.txt").open("wb") as err:
        process = subprocess.Popen(command, stdout=out, stderr=err, env=env)
        m.save(prefix.with_suffix(".active.json"),
               {"pid": process.pid, "sessionId": session, "model": model, "startedAt": started})
        print("Started original", label, process.pid, session, flush=True)
        code = process.wait()
    events = [json.loads(line) for line in raw.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    messages = [e["data"] for e in events if e["type"] == "assistant.message"]
    prefix.with_suffix(".md").write_text(
        (messages[-1].get("content", "") if messages else "No completed report.") + "\n", encoding="utf-8")
    active, calls, overlaps, returned = set(), {}, [], []
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
                        returnedCharacters=len(result), returnedSha256=hashlib.sha256(result.encode()).hexdigest())
            path = call["arguments"].get("path", "")
            if data["success"] and path:
                norm = lambda s: s.replace("\r\n", "\n").rstrip()
                call["entireRequestedTextContained"] = norm(Path(path).read_text(encoding="utf-8-sig")) in norm(result)
                if call["entireRequestedTextContained"]:
                    returned.append(path)
    usage = m.load(prefix.with_suffix(".usage.json")) if prefix.with_suffix(".usage.json").exists() else {}
    models = sorted({item.get("model", "") for item in messages})
    accepted = (code == 0 and models == [model] and usage.get("currentModel") == model
                and not active and not overlaps and len(calls) == len(resources)
                and all(call["name"] == "view" for call in calls.values())
                and returned == resources)
    stopped(process.pid)
    record = {
        "execution": 685, "batch": "094", "snapshot": HEAD, "sessionId": session,
        "dependentOriginalSession": True, "newBlindInitialReviewCredit": False,
        "requestedModel": model, "actualModels": models, "usageCurrentModel": usage.get("currentModel"),
        "launcherPid": process.pid, "startedAt": started, "completedAt": m.now(), "exitCode": code,
        "processExitVerified": True, "command": command, "toolCalls": list(calls.values()),
        "observedToolOverlaps": overlaps, "unfinishedTools": sorted(active),
        "requiredResources": resources, "successfullyReturnedResources": returned,
        "acceptedExecution": accepted, "rawSha256": m.sha(raw),
        "reportSha256": m.sha(prefix.with_suffix(".md")), "usage": usage,
        "availableTools": ["view"],
        "configurationEvidence": [e["data"] for e in events if e["type"] == "session.info"
                                  and e["data"].get("infoType") == "configuration"],
        "limits": "Complete returned text and strict serial process verified; not proof of comprehension or reviewer-run tests.",
    }
    m.save(C / (prefix.name + "-execution.json"), record)
    print(json.dumps({key: record[key] for key in [
        "exitCode", "actualModels", "acceptedExecution", "observedToolOverlaps"]}), flush=True)
    frozen()
    assert accepted, "Preserve evidence and yield on actual denial, incomplete or nonserial execution"


if __name__ == "__main__":
    if sys.argv[1] == "prepare":
        prepare()
    elif sys.argv[1] == "review":
        review(sys.argv[2])

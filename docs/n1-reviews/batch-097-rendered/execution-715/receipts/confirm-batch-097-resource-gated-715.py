"""Recover a nonconforming batched-tool read using one resource per CLI turn."""
import base64
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

from PIL import Image

C = Path(__file__).parent
spec = importlib.util.spec_from_file_location("confirmation715", C / "confirm-batch-097-rendered-715.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
load, save, sha, now = m.load, m.save, m.sha, m.now
ROOT = C / "batch-097-resource-gated-715"


def prepare():
    m.frozen()
    failed = load(C / "batch-097-rendered-715-claude-execution.json")
    assert not failed["acceptedExecution"] and len(failed["observedToolOverlaps"]) == 29
    m.stopped(failed)
    assert not ROOT.exists()
    ROOT.mkdir()
    resources = load(C / "batch-097-rendered-claude-resources-715.json")
    original = "".join(Path(p).read_text(encoding="utf-8") for p in resources if p.endswith(".txt"))
    common = original.split("COMMON EVIDENCE\n", 1)[1]
    start = common.index("COMPLETE SOURCE " + str(m.R / "docs" / "n1-sources" / "batch-097-jmdict.xml"))
    end = common.index("QUIZ CONTRACT docs\\content-format.md:152-177")
    common = common[:start] + (
        "Original complete dictionary evidence remains in YOUR original initial session and committed "
        "batch-097-initial-packet.txt, unchanged. No fresh full-family review claimed here.\n\n"
    ) + common[end:]
    for label in m.MODELS:
        own = (m.V / f"batch-097-initial-{label}.md").read_text(encoding="utf-8")
        packet = ROOT / f"{label}-bounded-text.txt"
        packet.write_text("YOUR OWN ORIGINAL REPORT\n" + own + "\n\nCOMMON EVIDENCE\n" + common, encoding="utf-8")
        save(ROOT / f"{label}-resources.json", [str(packet)] + [p for p in resources if p.endswith(".png")])
    save(ROOT / "recovery-disposition.json", {
        "execution": 715, "batch": "097", "failedExecution": failed,
        "reason": "Claude issued overlapping view calls despite serial prompt. All resources returned, but execution is NOT accepted.",
        "reportCorrection": "Original report says in-order reads; actual execution shows 29 overlaps. Preserve report verbatim, not as serial evidence.",
        "gptLaunchedBeforeRecovery": False, "runtimeAcceptance": False,
        "remedy": "One resource exposed in each successive original-session CLI prompt; verify actual single tool call, full returned bytes/image, process exit before next turn. No batch tool opportunity.",
        "scope": "Bounded native/choice confirmation only; unchanged independent initial dictionary/teaching reviews retained, not repeated or newly credited.",
    })
    print("Resource-gated recovery prepared; 17 one-resource turns per original reviewer.", flush=True)


def one_turn(label, index, resource, prompt):
    model, session = m.MODELS[label]
    prefix = ROOT / f"{label}-{index:02d}"
    raw = prefix.with_suffix(".jsonl")
    assert not raw.exists(), "Never overwrite an attempted reviewer turn"
    prefix.with_suffix(".prompt.txt").write_text(prompt, encoding="utf-8")
    command = [shutil.which("copilot"), "-C", str(m.R), "--add-dir", str(C),
               "--resume=" + session, "--model", model, "--no-ask-user",
               "--allow-tool=view", "--available-tools=view", "--disable-builtin-mcps",
               "--no-custom-instructions", "--output-format", "json",
               "--log-dir", str(C / "review-logs" / f"batch-097-resource-gated-715-{label}-{index:02d}"),
               "--usage-output-file", str(prefix.with_suffix(".usage.json")), "-p", prompt]
    env = os.environ.copy()
    env.pop("GH_TOKEN", None)
    env.pop("GITHUB_TOKEN", None)
    started = now()
    with raw.open("wb") as out, prefix.with_suffix(".stderr.txt").open("wb") as err:
        process = subprocess.Popen(command, stdout=out, stderr=err, env=env)
        save(prefix.with_suffix(".active.json"),
             {"pid": process.pid, "session": session, "model": model, "startedAt": started})
        code = process.wait()
    events = [json.loads(line) for line in raw.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    messages = [e["data"] for e in events if e["type"] == "assistant.message"]
    report = messages[-1].get("content", "") if messages else "No completed report."
    prefix.with_suffix(".md").write_text(report + "\n", encoding="utf-8")
    active, calls, overlaps = set(), {}, []
    for event in events:
        d = event.get("data", {})
        if event["type"] == "tool.execution_start":
            key = d["toolCallId"]
            if active:
                overlaps.append({"starting": key, "active": sorted(active)})
            active.add(key)
            calls[key] = {"name": d["toolName"], "arguments": d["arguments"], "startedAt": event["timestamp"]}
        elif event["type"] == "tool.execution_complete":
            key = d["toolCallId"]
            active.discard(key)
            call = calls[key]
            result = d.get("result", {}).get("content", "")
            result = result if isinstance(result, str) else json.dumps(result)
            call.update(success=d["success"], completedAt=event["timestamp"],
                        returnedCharacters=len(result), returnedSha256=hashlib.sha256(result.encode()).hexdigest())
            if resource and d["success"] and call["arguments"].get("path") == resource:
                path = Path(resource)
                if path.suffix == ".png":
                    payloads = d.get("result", {}).get("binaryResultsForLlm", [])
                    if len(payloads) == 1 and payloads[0]["mimeType"] == "image/png":
                        payload = base64.b64decode(payloads[0]["data"], validate=True)
                        with Image.open(io.BytesIO(payload)) as image:
                            image.load()
                            call["decodedImageDimensions"] = list(image.size)
                        call["decodedImageSha256"] = hashlib.sha256(payload).hexdigest()
                        call["sourceSha256"] = sha(path)
                        call["fullRequestedResourceReturned"] = True
                else:
                    norm = lambda s: s.replace("\r\n", "\n").rstrip()
                    call["fullRequestedResourceReturned"] = norm(path.read_text(encoding="utf-8")) in norm(result)
    usage = load(prefix.with_suffix(".usage.json")) if prefix.with_suffix(".usage.json").exists() else {}
    models = sorted({d.get("model", "") for d in messages})
    tool_ok = not calls if resource is None else (
        len(calls) == 1 and all(t["name"] == "view" and t.get("fullRequestedResourceReturned") for t in calls.values()))
    accepted = bool(code == 0 and models == [model] and usage.get("currentModel") == model
                    and not active and not overlaps and tool_ok)
    record = {
        "execution": 715, "batch": "097", "snapshot": m.HEAD, "sessionId": session,
        "dependentOriginalSession": True, "newBlindInitialReviewCredit": False,
        "requestedModel": model, "actualModels": models, "usageCurrentModel": usage.get("currentModel"),
        "launcherPid": process.pid, "startedAt": started, "completedAt": now(), "exitCode": code,
        "command": command, "resource": resource, "toolCalls": list(calls.values()),
        "observedToolOverlaps": overlaps, "unfinishedTools": sorted(active),
        "acceptedExecution": accepted, "rawSha256": sha(raw), "reportSha256": sha(prefix.with_suffix(".md")),
        "availableTools": ["view"], "usage": usage,
        "configurationEvidence": [e["data"] for e in events if e["type"] == "session.info"
                                  and e["data"].get("infoType") == "configuration"],
    }
    save(prefix.with_suffix(".execution.json"), record)
    m.stopped(record)
    m.frozen()
    print(label, index, "accepted" if accepted else "NOT ACCEPTED", "calls", len(calls), flush=True)
    assert accepted, "Preserve actual failure and yield; do not retry an identical failed turn"
    return record


def run(label):
    m.frozen()
    if label == "gpt":
        first = load(ROOT / "claude-summary.json")
        assert first["acceptedExecution"]
        m.stopped(first["turns"][-1])
    resources = load(ROOT / f"{label}-resources.json")
    turns = []
    for i, resource in enumerate(resources):
        instruction = (
            "Read the entire text once with forceReadLargeFiles=true, no ranges. It contains YOUR own "
            "initial report, unchanged four articles/exact reused diff, native receipts, ALL64 kanji choices "
            "and ALL512 losslessly encoded wordguard records. Inspect actual labels/senses; four guards "
            "are not universal semantic safety. Prior independent dictionary evidence remains inherited."
            if i == 0 else
            "Decode and inspect this PNG. Do not infer legibility from hashes/hasGlyph. Identify actual "
            "glyphs, wording, layout or route evidence visible here; distinguish clipping from missing "
            "content using previous captures retained in your context. Contact sheets are reduced scale."
        )
        prompt = (
            f"DEPENDENT resource-gated native confirmation, batch097, original {label} session. "
            f"Frozen signed HEAD {m.HEAD}, unchanged teaching1fa1ac69/versiona066afceaf1f447a. "
            "Only ONE resource is assigned to this turn. Make EXACTLY ONE view call for it and no other "
            "tool call. Do NOT revisit earlier resources or anticipate later resources. No parallel calls, "
            "edits, shell, delegation, other reports or new blind credit. "
            f"RESOURCE: {resource}\n{instruction}\n"
            "Store the observation for a final report in this SAME session after all resources. "
            "Reply with a brief exact observation and any established defect, not final acceptance. "
            "Native714 supplied receipt is API35 emulator only, not reviewer-run tests/physical phone/"
            "human handwriting/MLKit/general release. Full import once, two terminalcase0/no skips. "
            "Do not claim seriality of the earlier715 batched attempt: it had29 overlaps despite its report."
        )
        turns.append(one_turn(label, i, resource, prompt))
    final = (
        f"FINAL dependent rendered confirmation in YOUR ORIGINAL {label} session, batch097. "
        "NO TOOL CALLS now; use only the resources already returned in the17 resource-gated turns. "
        "Do not re-read, edit, delegate or ask questions. Signed contentHEAD e75b4bb1, nativearchive83e5c090, "
        "unchanged reviewedteaching1fa1ac69/versiona066afceaf1f447a. Not a fresh blind review. "
        "Preserve original findings/hypotheses/optional history. EarlierClaude715 batched attempt had29 "
        "tool overlaps; it is NOT serial acceptance, irrespective of its report. These gated turns "
        "supply bounded corrected process evidence, not retroactive independence. "
        "You received one boundedtext and THREEfontpanels(all20Han/fourfonts/especially刂) plus13contactsheets"
        "(52routecaptures, reducedscale). Use actual supplied labels and ALL64 kanjichoices/512wordguardrecords. "
        "ActualUIfallback蚊mosquito differs from builderseed0; 則N2 isn't available inN1. "
        "矛spear/polearm is relatedweapondomain, assess answer-equivalence. "
        "Both rawケン/[つるぎ] and exact curation retained; bothnormalizedkeysGood/Done2of2. "
        "TWOcomplete newarticles剣kanji/剣つるぎ and EXACTTWOreusedchanges(words真剣line27,kanji真line37); "
        "THREEreciprocalpairs/SIXdirections/ONEactivatedbaselinepair/Back/offline/N1selection/meaning/"
        "bothreadings/drawingtrace+giveuprecall. Teninjectedstrokes NOT humanhandwriting/MLKit. "
        "Supplied714native: fullarchive productionContentSyncONCE;1120kanji5073words129N1/zeroProblems/"
        "Roomepoch1/two terminalcase0/noskips. QualifiedTESTONLYAndroid1c1b7bf4 retainsproductionf9b59a2, "
        "NOT latestappmain. No new reviewer-run native, physicalphone/generalrelease/whole-set/publication claim. "
        "Original initial full dictionaries/18comparisonbodies/rawmetadata inherited, not freshly re-reviewed. "
        "Return COMPLETE Snapshot;Scope(actual model/session, actual text resources, decoded images, omissions/"
        "scale);Verdicts correctness/scopedcoverage/comprehensibility CLEAN/NEEDS FIX/UNVERIFIED separately "
        "for EACHofTWOnewarticles and EACHboundedchangedreusedpassage, plus boundedrendered/quizscope; "
        "Findings(severity/facet/file:lines,claim+impact,remedy,evidence,confidence ornone);Reconciliation"
        "(resolved/partiallyresolved/unresolved/withdrawn/optional);Optional;Limits. CLEAN means no demonstrated "
        "defect in actual bounded sample; never certify every wider custom/random/legacy pool or label a "
        "consequential unresolved claim CLEAN. No manufactured findings or expansion quota."
    )
    turns.append(one_turn(label, len(resources), None, final))
    save(ROOT / f"{label}-summary.json", {
        "execution": 715, "batch": "097", "snapshot": m.HEAD,
        "sessionId": m.MODELS[label][1], "model": m.MODELS[label][0],
        "dependentOriginalSession": True, "newBlindInitialReviewCredit": False,
        "acceptedExecution": all(t["acceptedExecution"] for t in turns),
        "turns": turns, "resources": resources, "textReads": 1, "decodedImageReads": 16,
        "finalReport": str(ROOT / f"{label}-{len(resources):02d}.md"),
        "earlierNonconformingAttemptPreserved": True,
    })
    print(label, "resource-gated confirmation complete", flush=True)


if __name__ == "__main__":
    if sys.argv[1] == "prepare":
        prepare()
    elif sys.argv[1] == "review":
        run(sys.argv[2])

import base64
import importlib.util
import json
import os
import shutil
import struct
import subprocess
import sys
from pathlib import Path

from PIL import Image

C = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("visual084", C / "review-batch-084-visual.py")
x = importlib.util.module_from_spec(spec)
spec.loader.exec_module(x)
V, N = x.V, x.N
CROP = V / "batch-084-visual-detail-crop.png"
PROVENANCE = V / "batch-084-visual-detail-provenance.json"


def prepare():
    x.frozen()
    assert all((V / f"batch-084-visual-{family}-execution.json").exists() for family in x.SESSIONS)
    assert not CROP.exists() and not PROVENANCE.exists()
    source = N / "n1-084-font-panel-3.png"
    box = (48, 300, 680, 1060)
    with Image.open(source) as image:
        assert image.size == (1080, 2400)
        crop = image.crop(box)
        crop.save(CROP)
        with Image.open(CROP) as check:
            assert check.tobytes() == crop.tobytes()
    x.save(PROVENANCE, {
        "source": str(source.relative_to(x.R)), "sourceSha256": x.sha(source),
        "sourceDimensions": [1080, 2400], "cropBox": box,
        "crop": str(CROP.relative_to(x.R)), "cropSha256": x.sha(CROP),
        "cropDimensions": [632, 760], "losslessOriginalPixelExtraction": True,
        "resampling": False, "enlargement": False, "newNativeRun": False,
        "reason": "Resolve consequential fine-bottom distinguishability uncertainty from downscaled full-frame review, without changing teaching or rerunning native.",
    })
    print("Lossless original-pixel focused panel crop prepared.", flush=True)


def run(family):
    x.frozen()
    model, session = x.SESSIONS[family]
    original = x.load(V / f"batch-084-visual-{family}-execution.json")
    assert original["processAndCoverageAccepted"]
    prefix = f"batch-084-visual-detail-{family}"
    if family == "gpt":
        prior = x.load(V / "batch-084-visual-detail-claude-execution.json")
        assert prior["processAndCoverageAccepted"]
    provenance = x.load(PROVENANCE)
    assert x.sha(CROP) == provenance["cropSha256"]
    source = x.R / provenance["source"]
    assert x.sha(source) == provenance["sourceSha256"]
    own = (V / f"batch-084-visual-{family}.md").read_text(encoding="utf-8")
    prompt = f"""SAME084 original-session bounded fine-detail addendum, not new blind review.
Unchanged teaching{x.TEACHING}, evidenceHEAD{x.HEAD}, runtime{x.CONTENT}/version74b87b47347b78c1.
Your own complete visual report below is preserved unchanged. No other report or coordinator verdict supplied.
One issue merits precise closure: actual small-panel 凜 versus 凛 bottom distinguishability, especially whether
the earlier whole-frame auto-resize left a consequential uncertainty. Do not equate every fine-stroke certification
with readable/distinguishable glyphs. Do not force agreement or invent a defect; preserve real uncertainty.

Read ONLY {CROP} with EXACTLY ONE view, then final addendum and stop. No extra reads/rereads/paralleltools/shell/edit/delegation.
This is lossless crop of ORIGINAL n1-084-font-panel-3.png, NOT enlarged/new rendering:
{json.dumps(provenance, ensure_ascii=False)}
It isolates left portions of allfour productionfamily rows at native screenshot pixels, without resampling;
labels/otherportions cropped out remain in your previous complete-frame review. The crop is not a new scale/device test
and cannot certify unseen bodytext/everyfine stroke or identify fallbackface.

State actualmodel/session, exactread/resizing limits; Snapshot/Scope/Verdicts(botharticle correctness/
scopedcoverage/renderedcomprehensibility separately)/Findings/Optional/Limits. Explain whether recognition/
distinguishability uncertainty is resolved, partlyresolved or unresolved from actual pixels with confidence/evidence.
Do not silently rewrite originalreport. Keep phone/MLKit/largerpools/publication outstanding.
YOUR OWN ORIGINAL VISUAL REPORT:\n{own}
"""
    prompt_path = C / (prefix + "-prompt.txt")
    assert not prompt_path.exists()
    prompt_path.write_text(prompt, encoding="utf-8")
    raw = C / (prefix + ".jsonl")
    usage = C / (prefix + "-usage.json")
    stderr = C / (prefix + "-stderr.txt")
    assert not raw.exists()
    command = [
        shutil.which("copilot"), "-C", str(x.R), "--add-dir", str(C),
        "--model", model, "--session-id", session, "--no-ask-user",
        "--allow-tool=view", "--disable-builtin-mcps", "--available-tools=view",
        "--no-custom-instructions", "--output-format", "json",
        "--log-dir", str(C / "review-logs" / prefix),
        "--usage-output-file", str(usage), "-p", prompt,
    ]
    env = os.environ.copy()
    env.pop("GH_TOKEN", None)
    env.pop("GITHUB_TOKEN", None)
    started = x.now()
    with raw.open("wb") as out, stderr.open("wb") as err:
        proc = subprocess.Popen(command, stdout=out, stderr=err, env=env)
        print(f"{family} detail PID{proc.pid}", flush=True)
        code = proc.wait()
    events = [json.loads(line) for line in raw.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    calls = [e["data"] for e in events if e["type"] == "tool.execution_start"]
    ends = [e["data"] for e in events if e["type"] == "tool.execution_complete"]
    messages = [e["data"] for e in events if e["type"] == "assistant.message"]
    terminal = [e for e in events if e["type"] == "result"]
    models = sorted({m["model"] for m in messages if m.get("model")})
    assert code == 0 and len(calls) == len(ends) == 1
    assert calls[0]["toolName"] == "view" and calls[0]["arguments"]["path"] == str(CROP)
    assert ends[0]["success"] and models == [model] and x.load(usage)["currentModel"] == model
    assert len(terminal) == 1 and terminal[0]["sessionId"] == session and terminal[0]["exitCode"] == 0
    assert not terminal[0]["usage"]["codeChanges"]["filesModified"]
    images = ends[0]["result"]["binaryResultsForLlm"]
    assert len(images) == 1 and images[0]["type"] == "image"
    payload = base64.b64decode(images[0]["data"], validate=True)
    target = V / (prefix + "-returned.png")
    assert not target.exists()
    target.write_bytes(payload)
    dimensions = struct.unpack(">II", payload[16:24])
    assert dimensions == (632, 760)
    with Image.open(CROP) as source_image, Image.open(target) as returned:
        assert source_image.convert("RGBA").tobytes() == returned.convert("RGBA").tobytes()
    report = V / (prefix + ".md")
    content = [m["content"] for m in messages if m.get("content")][-1]
    report.write_text(content + "\n", encoding="utf-8")
    x.save(V / (prefix + "-execution.json"), {
        "execution": 588, "launcherPid": proc.pid, "startedAt": started, "completedAt": x.now(),
        "exitCode": code, "actualModels": models, "sessionId": session,
        "availableTools": ["view"], "toolCalls": calls, "observedToolOverlaps": [],
        "unfinishedTools": [], "originalPixelEquivalentReturned": True,
        "returnedDimensions": dimensions, "returnedPayloadSha256": x.sha(target),
        "originalReportSha256": original["reportSha256"], "reportSha256": x.sha(report),
        "rawExecutionLocation": str(raw), "rawExecutionSha256": x.sha(raw),
        "processAndCoverageAccepted": True,
        "limits": "Dependent original-session pixel-detail addendum, not a new native/scale/device/dictionary review.",
    })
    x.frozen()
    print(f"{family} detail exited0; native crop pixels and complete addendum archived.", flush=True)


if __name__ == "__main__":
    if sys.argv[1] == "prepare":
        prepare()
    else:
        run(sys.argv[1])

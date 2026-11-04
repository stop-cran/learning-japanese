import base64
import hashlib
import io
import json
import shutil
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageChops, ImageStat

control = Path(__file__).resolve().parent
root = control.parent / "learning-japanese"
reviews = root / "docs" / "n1-reviews"
native_dir = reviews / "batch-044-native"
prefix = "batch-044-visual-claude"
snapshot = "bb63b6182784ddc318574ef77490c2c9c672fe70"


def text(path):
    raw = path.read_bytes()
    return raw.decode("utf-16" if raw.startswith((b"\xff\xfe", b"\xfe\xff")) else "utf-8-sig").replace("\r\n", "\n")


def load(path):
    return json.loads(text(path))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, data):
    assert not path.exists(), path
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


process = load(control / (prefix + "-process.json"))
usage = load(control / (prefix + "-usage.json"))
events = [json.loads(line) for line in text(control / (prefix + ".jsonl")).splitlines() if line.strip()]
messages = [e["data"] for e in events if e["type"] == "assistant.message"]
models = sorted({m.get("model", "") for m in messages})
assert process["exitCode"] == 0 and process["snapshot"] == snapshot
assert process["sessionId"] == "80caf75e-72b4-46da-a623-a2b89219e51f"
assert usage["currentModel"] == "claude-opus-5.5" and models == ["claude-opus-5.5"]
terminal = [e for e in events if e["type"] == "result"]
assert len(terminal) == 1 and terminal[0]["exitCode"] == 0
assert terminal[0]["usage"]["codeChanges"]["filesModified"] == []
names = ("font-pairs", "selection", "kanji-mnemonic", "kanji-reading-disposition",
         "kanji-lookalikes", "word-sign-example", "word-components", "word-animal-comparison")
expected_images = {f"n1-044-{name}.png" for name in names}
calls, active, overlaps, returned, payloads = {}, set(), [], [], []
for event in events:
    data = event.get("data", {})
    if event["type"] == "tool.execution_start":
        key = data["toolCallId"]
        if active:
            overlaps.append({"starting": key, "alreadyActive": sorted(active)})
        active.add(key)
        assert data["toolName"] == "view"
        calls[key] = {"name": "view", "arguments": data["arguments"], "startedAt": event["timestamp"],
                      "turnId": data["turnId"]}
    elif event["type"] == "tool.execution_complete":
        key = data["toolCallId"]
        active.remove(key)
        assert data["success"]
        result = data["result"]
        source = Path(calls[key]["arguments"]["path"])
        calls[key].update(completedAt=event["timestamp"], success=True)
        if source.suffix == ".png":
            assert source.parent == control / "artifacts" / "batch-044-parent-native-attempt-1"
            binaries = result["binaryResultsForLlm"]
            assert len(binaries) == 1 and binaries[0]["type"] == "image" and binaries[0]["mimeType"] == "image/png"
            binary = base64.b64decode(binaries[0]["data"], validate=True)
            original = Image.open(source).convert("RGB")
            shown = Image.open(io.BytesIO(binary)).convert("RGB")
            rms = ImageStat.Stat(ImageChops.difference(original.resize(shown.size, Image.Resampling.LANCZOS), shown)).rms
            assert max(rms) < 1.0, (source, rms)
            target = native_dir / "reviewer-returned" / source.name
            returned.append({
                "source": str(source), "sourceSha256": digest(source),
                "returnedPath": target.relative_to(root).as_posix(),
                "returnedSha256": hashlib.sha256(binary).hexdigest(), "bytes": len(binary),
                "sourceDimensions": list(original.size), "returnedDimensions": list(shown.size),
                "binaryExactlyMatchesArchivedSource": binary == source.read_bytes(),
                "fullImageLanczosResampleRgbRms": rms,
                "transformation": "Exact returned bytes retained separately. Full-image RGB Lanczos RMS below1/255channel verifies correspondence, not comprehension or source-byte identity.",
            })
            payloads.append((target, binary))
        else:
            arguments = calls[key]["arguments"]
            expected = text(source).strip()
            if "view_range" in arguments:
                assert source == native_dir / "N1Batch044NativeTest.kt"
                assert arguments["view_range"] == [150, 245]
                expected = "\n".join(text(source).splitlines()[149:245]).strip()
            assert expected in result["content"].replace("\r\n", "\n"), source
assert not active and len(calls) == 13 and not overlaps
assert len({c["turnId"] for c in calls.values()}) == 13
assert len(returned) == 8 and {Path(r["source"]).name for r in returned} == expected_images
report_content = messages[-1]["content"]
assert "None blocking or consequential." in report_content
assert all(label in report_content for label in ("Snapshot:", "Scope:", "Verdicts:", "Findings:", "Optional:", "Limits:"))
provenance = load(control / "batch-044-parent-native-provenance.json")
index = load(control / "batch-044-parent-native-artifact-index.json")
android_provenance = load(control / "batch-044-parent-android-provenance.json")
native = load(control / "batch-044-parent-native-recovery.json")
android = load(control / "batch-044-parent-android-recovery.json")
mechanical = load(control / "execution-216-recovery-verification.json")
copied = []


def copy(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        assert source.read_bytes() == target.read_bytes(), "Never overwrite evidence"
    else:
        shutil.copyfile(source, target)
    copied.append({"path": target.relative_to(root).as_posix(), "sha256": digest(target),
                   "bytes": target.stat().st_size, "source": str(source)})


for row in provenance + android_provenance:
    source = Path(row["path"])
    assert digest(source) == row["sha256"]
    copy(source, native_dir / "parent-receipts" / source.name)
for row in index:
    source = Path(row["path"])
    assert digest(source) == row["sha256"]
    assert source.parent.name == "batch-044-parent-native-attempt-1"
    copy(source, native_dir / "attempt-1" / source.name)
for row in android["tests"]:
    copy(Path(row["artifactPath"]), native_dir / "parent-receipts" / Path(row["artifactPath"]).name)
for name in (
    "batch-044-parent-native-provenance.json", "execution-216-recovery-verification.json",
    prefix + "-process.json", prefix + "-usage.json", prefix + "-stderr.txt",
):
    copy(control / name, native_dir / "parent-receipts" / name)
copy(control / "batch-044-visual-prompt.txt", reviews / "batch-044-visual-task.txt")
for target, binary in payloads:
    target.parent.mkdir(parents=True, exist_ok=True)
    assert not target.exists()
    target.write_bytes(binary)
    copied.append({"path": target.relative_to(root).as_posix(), "sha256": digest(target),
                   "bytes": len(binary), "source": "Exact recorded binaryResultsForLlm payload"})
report = reviews / (prefix + ".md")
assert not report.exists()
report.write_bytes((report_content + "\n").encode("utf-8"))
visual = {
    **process, "actualModels": models, "usageCurrentModel": usage["currentModel"],
    "reportSha256": digest(report), "rawExecutionSha256": digest(control / (prefix + ".jsonl")),
    "rawExecutionLocation": "Sibling control/" + prefix + ".jsonl",
    "availableTools": ["view", "glob", "rg", "web_fetch"], "actualTools": ["view"],
    "toolCalls": list(calls.values()), "observedToolOverlaps": overlaps, "unfinishedTools": [],
    "binaryImageReturnsVerified": returned, "usage": usage,
    "usageScope": "Cumulative reused original session, not isolated followup billing.",
    "serialDisposition": "All13 calls in13distinctturns, no overlapping start or unfinished tool. Eight PNG returns individually verified. One original reviewer process actually exited0.",
    "limits": "Dependent ORIGINAL-session confirmation, not new blind/full-source/full-article/native-speaker/phone certification. Five original reports and process limits unchanged. Coordinator separately verifies hashes/dimensions/resampling.",
}
save(reviews / (prefix + "-execution.json"), visual)
record = {
    "schemaVersion": 1, "execution": 216, "batch": "044",
    "status": "native-and-freshAndroid-verified-pending-local-validation",
    "recordedAt": datetime.now().astimezone().isoformat(),
    "contentSnapshot": snapshot, "reviewedTeachingSnapshot": "3a7e268c758220fc06d6fecd4b29302da1bab69b",
    "native": native, "artifactIndex": index, "provenance": provenance,
    "android": android, "androidProvenance": android_provenance, "copiedEvidence": copied,
    "mechanicalVerification": mechanical, "independentVisual": visual,
    "coordinatorDirectImages": [str(control / "artifacts" / "batch-044-parent-native-attempt-1" / f"n1-044-{p}.png")
                                for p in ("font-pairs", "kanji-reading-disposition")],
    "coordinatorAdjudication": {
        "findings": [], "unresolvedConsequentialClaimsWithinBoundedVisualScope": [],
        "result": "Bounded visual accepted; no teaching edit or lexical rereview needed. Coordinator directly inspected two PNGs this execution; remaining six inspected by original reviewer, not claimed as current coordinator reads. Parent eight reads retained distinctly.",
        "originalFindings": "C1 exact documented animal-name zodiac spelling resolved; conservative direct亥/猪guard accepted. Unsupported optional compound kana removed. All five original textual reports and30/34/10/8/9calls0/0/4/0/6overlaps/twofailedlookups remain unchanged.",
        "processDeviation": "None this visual pass; not a claim about inherited confirmation overlaps.",
        "reportQualification": "Original report preserved verbatim. Snapshot/untracked claims are supplied, not reviewer Git verification. Chip horizontal scrolling is not exercised by these PNGs; optional observation only, no interaction certification. Seven hash-equivalent viewports not separately viewed. No invented extra image.",
        "optional": [
            {"status": "optional", "claim": "Right table column clipping", "disposition": "Visible sideways-scroll hint and repeated Common words preserve scope; unseen columns/full articles not certified."},
            {"status": "optional", "claim": "N1 chip-row clipping", "disposition": "No demonstrated learning defect; scrolling not exercised in this visual pass."},
        ],
        "fallbackDisposition": "亥刻交亡 each four distinct raster styles;亠刂犭豕 each one shared Gothic-like fallback across four requested families. All readable/distinguishable in bounded API35 sheet. Exact fallback face unidentified; not four bundled designs for these four components.",
    },
    "limits": "Bounded API35 emulator only. Original unchangedfixture accepted1terminal0/0/32glyphs/fullContentSyncONCEoffline. Parent source/artifact and fresh213Android3+1exactXML verified, not rerun. Actual5580/requested2048MiB automatic2560MiB/appheap192m576m unchanged. OriginalClaude13views/8PNGserial/0overlaps; resizedreturned/source bytes separate. Clipped/offscreen/fullarticles not certified. No freshquizdrawing/phone/native-speaker/generalrelease/currentmain/CI/publicZIP acceptance. CompatibleAndroidf9b59a2+ required. Public70/1158remaining unchanged; no045/publication.",
}
save(reviews / "batch-044-native-acceptance.json", record)
print("Archived accepted1 and verified originalClaude13serialviews/8PNG/0overlaps with exact returned payloads.")

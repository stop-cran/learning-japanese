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
native_dir = reviews / "batch-043-native"
prefix = "batch-043-visual-claude"
snapshot = "f4e7d506c9f6cdacd1d1a406eebe891fe283ac87"


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
assert process["sessionId"] == "54bc51a8-88e8-4869-98bc-2db0fc6cb7cb"
assert usage["currentModel"] == "claude-opus-5.5" and models == ["claude-opus-5.5"]
terminal = [e for e in events if e["type"] == "result"]
assert len(terminal) == 1 and terminal[0]["exitCode"] == 0
assert terminal[0]["usage"]["codeChanges"]["filesModified"] == []
names = ("font-pairs", "selection", "kanji-mnemonic", "kanji-reading-disposition",
         "kanji-lookalikes", "word-giraffe-example", "word-components",
         "word-phoenix-comparison", "word-rare-spelling")
expected_images = {f"n1-043-{name}.png" for name in names}
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
            assert source.parent == control / "artifacts" / "batch-043-parent-native-attempt-2"
            binaries = result["binaryResultsForLlm"]
            assert len(binaries) == 1 and binaries[0]["type"] == "image" and binaries[0]["mimeType"] == "image/png"
            binary = base64.b64decode(binaries[0]["data"], validate=True)
            original = Image.open(source).convert("RGB")
            shown = Image.open(io.BytesIO(binary)).convert("RGB")
            rms = ImageStat.Stat(ImageChops.difference(
                original.resize(shown.size, Image.Resampling.LANCZOS), shown)).rms
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
                assert source == native_dir / "N1Batch043NativeTest.kt"
                assert arguments["view_range"] == [150, 245]
                expected = "\n".join(text(source).splitlines()[149:245]).strip()
            assert expected in result["content"].replace("\r\n", "\n"), source
assert not active and len(calls) == 14 and len(overlaps) == 2
overlap_paths = {Path(calls[k]["arguments"]["path"]).name for row in overlaps
                 for k in [row["starting"], *row["alreadyActive"]]}
assert overlap_paths == {"麟.md", "麒麟.md", "N1Batch043NativeTest.kt"}
image_calls = [c for c in calls.values() if c["arguments"]["path"].endswith(".png")]
assert len({c["turnId"] for c in image_calls}) == 9
assert len(returned) == 9 and {Path(r["source"]).name for r in returned} == expected_images
assert len({c["arguments"]["path"] for c in calls.values()}) == 14
report_content = messages[-1]["content"]
assert "**Findings:** None blocking." in report_content
assert all(label in report_content for label in ("Snapshot:", "Scope:", "Verdicts:", "Findings:", "Optional:", "Limits:"))
provenance = load(control / "batch-043-parent-native-provenance.json")
index = load(control / "batch-043-parent-native-artifact-index.json")
android_provenance = load(control / "batch-043-parent-android-provenance.json")
native = load(control / "batch-043-parent-native-recovery.json")
android = load(control / "batch-043-parent-android-recovery.json")
mechanical = load(control / "execution-207-recovery-verification.json")
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
    attempt = source.parent.name.rsplit("-", 1)[1]
    assert attempt in {"1", "2"}
    copy(source, native_dir / f"attempt-{attempt}" / source.name)
for row in android["tests"]:
    copy(Path(row["artifactPath"]), native_dir / "parent-receipts" / Path(row["artifactPath"]).name)
for source in (
    control / "batch-043-parent-native-provenance.json", control / "execution-207-recovery-verification.json",
    control / (prefix + "-process.json"), control / (prefix + "-usage.json"), control / (prefix + "-stderr.txt"),
):
    copy(source, native_dir / "parent-receipts" / source.name)
copy(control / "batch-043-visual-prompt.txt", reviews / "batch-043-visual-task.txt")
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
    "serialDisposition": "One three-text-call response produced TWO overlapping starts: teaching files and fixture range. Self-disclosed, no retry to conceal deviation. All NINE PNG calls were in distinct subsequent turns, serial with no image overlap. Full reads and returned payloads verified. Not perfect serial compliance.",
    "limits": "Dependent ORIGINAL-session confirmation; inherited50/54initialcalls,0/0overlaps,0XMLviolations and supplied-source limits unchanged. No new blind/full-source/full-article/native-speaker/phone certification. Coordinator separately verifies hashes/dimensions/resampling.",
}
save(reviews / (prefix + "-execution.json"), visual)
record = {
    "schemaVersion": 1, "execution": 207, "batch": "043",
    "status": "native-and-freshAndroid-verified-pending-local-validation",
    "recordedAt": datetime.now().astimezone().isoformat(),
    "contentSnapshot": snapshot, "reviewedTeachingSnapshot": "0fa7a534d58bb625b838eb664775293fa2460757",
    "native": native, "artifactIndex": index, "provenance": provenance,
    "android": android, "androidProvenance": android_provenance, "copiedEvidence": copied,
    "mechanicalVerification": mechanical, "independentVisual": visual,
    "coordinatorDirectImages": [str(control / "artifacts" / "batch-043-parent-native-attempt-2" / f"n1-043-{p}.png")
                                for p in ("font-pairs", "kanji-reading-disposition")],
    "coordinatorAdjudication": {
        "findings": [], "unresolvedConsequentialClaimsWithinBoundedVisualScope": [],
        "result": "Bounded visual accepted; no teaching edit or lexical rereview needed. Coordinator directly inspected two PNGs this execution; other seven inspected by original reviewer, not claimed as current coordinator reads. Prior parent nine reads retained distinctly.",
        "originalFindings": "No actionable initial textual findings; three optional groups unchanged. Seven supplied dictionary entry sections, not original report's eight pages; correction accepted, teaching unchanged.",
        "processDeviation": visual["serialDisposition"],
        "reportCorrection": "Original report preserved verbatim. Its Limits invents a fifth unseen capture 'reading-quiz keys'; fixture captures FOUR additional hash-equivalent viewports only, no reading-quiz-key screenshot. Key arrays are route JSON/assertion evidence, not visual quiz evidence. The nine actual PNG reads are verified; no task rerun or fabricated artifact.",
        "optional": [
            {"status": "optional", "claim": "Right table column clipping", "disposition": "Sideways-scroll hint and visible gloss preserve distinction; unseen columns/full articles not certified."},
        ],
        "fallbackDisposition": "麟 and 鹿 each four distinct raster styles; 凰广粦騏驎麒 each one shared Gothic-like fallback across four requested families. All readable/distinguishable in bounded API35 sheet. Exact fallback face not identified; not four bundled designs for six fallback characters.",
    },
    "limits": "Bounded API35 emulator only. Original failed1article-2/glyph0 and exact normalized-key expectation correction preserved; accepted2terminal0/0/32glyphs/fullContentSyncONCEoffline. Parent source/artifact and fresh204Android3+1 exactXML verified, not rerun. Actual5580/requested2048MiB automatic2560MiB/appheap192m unchanged;TimeWaitPID0collision preserved/wait90s unchanged guard then passed. OriginalClaude14views/9PNGserial/one3textresponse-TWOoverlappingstarts disclosed; resized returned/source bytes separate. Clipped/offscreen/fullarticles not certified. No freshquizdrawing/phone/native-speaker/generalrelease/currentmain/CI/publicZIP acceptance. CompatibleAndroidf9b59a2+ required. Public69/1159remaining unchanged; no044/publication.",
}
save(reviews / "batch-043-native-acceptance.json", record)
print("Archived failed1/accepted2 and verified actual originalClaude14views/9serialPNG/TWOtextoverlap starts with report correction.")

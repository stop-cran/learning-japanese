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
native_dir = reviews / "batch-048-native"
prefix = "batch-048-visual-claude"
snapshot = "66211c0f70abdc92f565bebb095e6c18344bde52"


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
assert process["sessionId"] == "80a82572-cc26-4d43-b490-52fbc401e296"
assert usage["currentModel"] == "claude-opus-5.5" and models == ["claude-opus-5.5"]
terminal = [e for e in events if e["type"] == "result"]
assert len(terminal) == 1 and terminal[0]["exitCode"] == 0
assert terminal[0]["usage"]["codeChanges"]["filesModified"] == []
names = ("font-pairs", "selection", "kanji-radical", "kanji-mnemonic", "kanji-reading-disposition",
         "kanji-lookalikes", "reused-en-mnemonic", "word-sign-example", "word-components", "word-sign-boundary")
expected_images = {f"n1-048-{name}.png" for name in names}
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
            assert source.parent == control / "artifacts" / "batch-048-parent-native-attempt-1"
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
                assert source == native_dir / "N1Batch048NativeTest.kt"
                assert arguments["view_range"] == [140, 275]
                expected = "\n".join(text(source).splitlines()[139:275]).strip()
            assert expected in result["content"].replace("\r\n", "\n"), source
assert not active and len(calls) == 17 and len(overlaps) == 3
assert len({c["turnId"] for c in calls.values()}) == 14
image_calls = [c for c in calls.values() if Path(c["arguments"]["path"]).suffix == ".png"]
assert len({c["turnId"] for c in image_calls}) == 10
assert all(c["turnId"] != "3" for c in image_calls)
assert {c["turnId"] for c in calls.values() if c["arguments"]["path"].endswith((".md", ".kt"))} == {"1", "2", "3"}
assert all(row["starting"] not in {
    key for key, call in calls.items() if Path(call["arguments"]["path"]).suffix == ".png"
} for row in overlaps)
assert len(returned) == 10 and {Path(r["source"]).name for r in returned} == expected_images
report_content = messages[-1]["content"]
assert "Findings:" in report_content
assert all(label in report_content for label in ("Snapshot:", "Scope:", "Verdicts:", "Findings:", "Optional:", "Limits:"))
provenance = load(control / "batch-048-parent-native-provenance.json")
index = load(control / "batch-048-parent-native-artifact-index.json")
android_provenance = load(control / "batch-048-parent-android-provenance.json")
native = load(control / "batch-048-parent-native-recovery.json")
android = load(control / "batch-048-parent-android-recovery.json")
mechanical = load(control / "execution-252-recovery-verification.json")
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
    assert source.parent.name == "batch-048-parent-native-attempt-1"
    copy(source, native_dir / "attempt-1" / source.name)
for row in android["tests"]:
    copy(Path(row["artifactPath"]), native_dir / "parent-receipts" / Path(row["artifactPath"]).name)
for name in (
    "batch-048-parent-native-provenance.json", "execution-252-recovery-verification.json",
    prefix + "-process.json", prefix + "-usage.json", prefix + "-stderr.txt",
):
    copy(control / name, native_dir / "parent-receipts" / name)
copy(control / "batch-048-visual-prompt.txt", reviews / "batch-048-visual-task.txt")
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
    "serialDisposition": "One original reviewer process actually exited0. Actual17views in14distinctturns; one four-text-read batch produced3overlappingstarts/max4active. This violated one-call-per-response despite explicit prompt. All10PNGviews in10laterdistinctturns were serial without overlaps; allreturns verified,0unfinished. Report's15response count is corrected to actual14distincttoolturns, not erased.",
    "limits": "Dependent ORIGINAL-session confirmation, not new blind/full-source/full-article/native-speaker/phone certification. Two original reports and process limits unchanged. Coordinator separately verifies hashes/dimensions/resampling.",
}
save(reviews / (prefix + "-execution.json"), visual)



record = {
    "schemaVersion": 1, "execution": 252, "batch": "048",
    "status": "native-and-freshAndroid-verified-pending-local-validation",
    "recordedAt": datetime.now().astimezone().isoformat(),
    "contentSnapshot": snapshot,
    "reviewedTeachingSnapshot": "ac944d9e66a6aeb4f8272f89a6fe1b40d87b47c9",
    "native": native, "artifactIndex": index, "provenance": provenance,
    "android": android, "androidProvenance": android_provenance,
    "copiedEvidence": copied, "mechanicalVerification": mechanical,
    "independentVisual": visual,
    "coordinatorDirectImages": [
        str(control / "artifacts" / "batch-048-parent-native-attempt-1" / f"n1-048-{p}.png")
        for p in ("font-pairs", "kanji-reading-disposition")
    ],
    "coordinatorAdjudication": {
        "findings": [], "unresolvedConsequentialClaimsWithinBoundedVisualScope": [],
        "result": "Bounded visual acceptance, no teaching change. Coordinator directly viewed font-pairs and kanji-reading-disposition; other eight actual PNG reads belong to original reviewer, not current coordinator. Parent ten operational reads retained separately.",
        "originalFindings": "Two blind textual initials34/33calls plus bounded original-session supplements3/3calls, zero internaloverlaps/XMLrangeviolations preserved. Initial common task incorrectly called演unchanged and omitted exactdelta; supplements closed演line24componentlink on unchanged teaching snapshot, not retroactive blind coverage. Two nonblocking optional Claude groups retained. Eight supplied Japanese sections across seven pages, not fresh upstream retrieval. Coordinator alone freshly inspected pinned86lineSVG geometry at earlier authoring checkpoint.",
        "processDeviation": "One four-text-read batch on turn3 produced3overlappingstarts/max4active despite explicit serial prompt. Preserve deviation; no repeated run to manufacture compliance. All10PNGreads were individually serial in10subsequentturns. Actual17calls/14distincttoolturns, not report's15responses;0unfinished/exit0. This is bounded visual evidence, not strict-all-tool serialization.",
        "reportQualification": "Original report preserved verbatim. Snapshot and operational facts supplied, not reviewer Git/hash/native test verification. Ten hash-equivalent viewports not separate independent reads. Clipped columns, keyboard-covered content and full articles not certified; no phone/quiz/drawing screenshot or interaction inferred. The report's claim that 甲寅's second reading is recoverable as きの|とら is not accepted: clipped え is unseen and cannot be visually reconstructed as a complete reading. Current text has correct completeきのえとら, while visible prose explains two complete readings without actually spelling both. This overstatement does not change correct text or bounded visible selection-rule acceptance. Earlier coordinator SVG inspection is distinct from current returned-image dimension/resampling checks.",
        "optional": [
            {
                "status": "optional",
                "claim": "Right edge of Typical words is clipped in captured viewport.",
                "disposition": "Visible sideways-scroll hint and readable post-table paragraph preserve selectedとら/verifiedインcalendar recognition distinction. No demonstrated blocking defect; horizontal interaction and unseen columns not certified."
            }
        ],
        "fallbackDisposition": "寅演黄申 each have four distinct raster styles across Gothic/Mincho/Textbook/Brush. 宀氵虍黃 each share one Gothic-like system fallback across families, not four bundled designs; exact face unidentified. Bounded API35 readability and shape distinctions accepted, not physical-phone or exact-face provenance certification.",
    },
    "limits": "Bounded API35 emulator only. Original unchangedfixture accepted1terminal0/0/32glyphs/fullContentSyncONCEoffline, including changed演link/SystemBack. Parent source/artifact and fresh249Android3+1 exactXML verified, not rerun. Actual5580owned20980stopped/requested2048MiB automatic2560MiB/appheap192m576m unchanged. OriginalClaude17views/14distincttoolturns/onefour-textbatch3overlappingstarts/max4active;10PNGindividuallyserial/0imageoverlaps/0unfinished/exit0. Explicit serial instruction violated in text batch, not retrospectively certified. Original and actual resized returned bytes separately archived. Ten hash-equivalent viewports not independently viewed. Clipped second甲寅reading not whollyvisible; reportoverclaim qualified. Clipped/offscreen/fullarticles/keyboard-coveredcontent not certified. No freshquizdrawing/phone/native-speaker/generalrelease/currentmain/CI/publicZIP acceptance. CompatibleAndroidf9b59a2+ required; oldclients ignore curation and8000entry clients reject collection. Public74/1154remaining unchanged; no049/publication.",
}
save(reviews / "batch-048-native-acceptance.json", record)
print("Archived batch048 original report/17views/3textoverlaps/10serialPNG returns; deviation preserved.")

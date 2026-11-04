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
native_dir = reviews / "batch-045-native"
snapshot = "01b3d3b2f0fc0fceca382d0ce54d91c13ab464a1"
session = "945744ea-501d-43bd-b966-a1a8ca98177b"


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


copied = []


def copy(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        assert source.read_bytes() == target.read_bytes(), "Never overwrite evidence"
    else:
        shutil.copyfile(source, target)
    copied.append({"path": target.relative_to(root).as_posix(), "sha256": digest(target),
                   "bytes": target.stat().st_size, "source": str(source)})


names = ("font-pairs", "selection", "kanji-radical", "kanji-mnemonic",
         "kanji-reading-disposition", "kanji-lookalikes", "word-sign-example",
         "word-components", "word-animal-comparison", "word-sign-boundary")
expected = {str(control / "artifacts" / "batch-045-parent-native-attempt-1" / f"n1-045-{name}.png")
            for name in names}


def review(prefix, image_paths, expected_calls):
    process = load(control / (prefix + "-process.json"))
    usage = load(control / (prefix + "-usage.json"))
    events = [json.loads(line) for line in text(control / (prefix + ".jsonl")).splitlines() if line.strip()]
    messages = [e["data"] for e in events if e["type"] == "assistant.message"]
    models = sorted({m.get("model", "") for m in messages})
    assert process["exitCode"] == 0 and process["snapshot"] == snapshot
    assert process["sessionId"] == session
    assert usage["currentModel"] == "claude-opus-5.5" and models == ["claude-opus-5.5"]
    terminal = [e for e in events if e["type"] == "result"]
    assert len(terminal) == 1 and terminal[0]["exitCode"] == 0
    assert terminal[0]["usage"]["codeChanges"]["filesModified"] == []
    calls, active, overlaps, returned = {}, set(), [], []
    for event in events:
        data = event.get("data", {})
        if event["type"] == "tool.execution_start":
            key = data["toolCallId"]
            if active:
                overlaps.append({"starting": key, "alreadyActive": sorted(active)})
            active.add(key)
            assert data["toolName"] == "view"
            calls[key] = {"name": "view", "arguments": data["arguments"],
                          "startedAt": event["timestamp"], "turnId": data["turnId"]}
        elif event["type"] == "tool.execution_complete":
            key = data["toolCallId"]
            active.remove(key)
            assert data["success"]
            result = data["result"]
            source = Path(calls[key]["arguments"]["path"])
            calls[key].update(completedAt=event["timestamp"], success=True)
            if source.suffix == ".png":
                assert str(source) in image_paths
                binaries = result["binaryResultsForLlm"]
                assert len(binaries) == 1 and binaries[0]["type"] == "image"
                assert binaries[0]["mimeType"] == "image/png"
                binary = base64.b64decode(binaries[0]["data"], validate=True)
                original, shown = Image.open(source).convert("RGB"), Image.open(io.BytesIO(binary)).convert("RGB")
                rms = ImageStat.Stat(ImageChops.difference(
                    original.resize(shown.size, Image.Resampling.LANCZOS), shown)).rms
                assert max(rms) < 1.0, (source, rms)
                target = native_dir / "reviewer-returned" / source.name
                target.parent.mkdir(parents=True, exist_ok=True)
                assert not target.exists()
                target.write_bytes(binary)
                returned.append({
                    "source": str(source), "sourceSha256": digest(source),
                    "returnedPath": target.relative_to(root).as_posix(),
                    "returnedSha256": digest(target), "bytes": len(binary),
                    "sourceDimensions": list(original.size), "returnedDimensions": list(shown.size),
                    "binaryExactlyMatchesArchivedSource": binary == source.read_bytes(),
                    "fullImageLanczosResampleRgbRms": rms,
                    "transformation": "Exact returned bytes retained separately; source correspondence verified, not comprehension.",
                })
                copied.append({"path": target.relative_to(root).as_posix(), "sha256": digest(target),
                               "bytes": len(binary), "source": "Exact recorded binaryResultsForLlm payload"})
            else:
                arguments = calls[key]["arguments"]
                expected_text = text(source).strip()
                if "view_range" in arguments:
                    assert source == native_dir / "N1Batch045NativeTest.kt"
                    assert arguments["view_range"] == [150, 245]
                    expected_text = "\n".join(text(source).splitlines()[149:245]).strip()
                assert expected_text in result["content"].replace("\r\n", "\n"), source
    assert not active and len(calls) == expected_calls and not overlaps
    assert len({c["turnId"] for c in calls.values()}) == expected_calls
    assert {r["source"] for r in returned} == image_paths
    assert len(returned) == len(image_paths)
    report_content = messages[-1]["content"]
    assert all(label in report_content for label in ("Snapshot:", "Scope:", "Verdicts:", "Findings:", "Optional:", "Limits:"))
    report = reviews / (prefix + ".md")
    assert not report.exists()
    report.write_bytes((report_content + "\n").encode("utf-8"))
    record = {
        **process, "actualModels": models, "usageCurrentModel": usage["currentModel"],
        "reportSha256": digest(report), "rawExecutionSha256": digest(control / (prefix + ".jsonl")),
        "rawExecutionLocation": "Sibling control/" + prefix + ".jsonl",
        "availableTools": ["view", "glob", "rg", "web_fetch"], "actualTools": ["view"],
        "toolCalls": list(calls.values()), "observedToolOverlaps": overlaps, "unfinishedTools": [],
        "binaryImageReturnsVerified": returned, "usage": usage,
        "usageScope": "Cumulative reused original session, not isolated followup billing.",
        "serialDisposition": f"All{expected_calls}calls in distinctturns, no overlappingstart or unfinishedtool; {len(returned)}PNG returns independently verified. Sole original reviewer process actually exited0.",
        "limits": "Dependent ORIGINAL-session confirmation, not new blind/full-source/full-article/native-speaker/phone certification. Coordinator separately verifies hashes/dimensions/resampling.",
    }
    save(reviews / (prefix + "-execution.json"), record)
    for suffix in ("-process.json", "-usage.json", "-stderr.txt"):
        copy(control / (prefix + suffix), native_dir / "parent-receipts" / (prefix + suffix))
    return record


visual = review("batch-045-visual-claude", expected, 15)
detail = review("batch-045-visual-detail-claude",
                {str(control / "artifacts" / "batch-045-visual-detail.png")}, 2)
assert visual["completedAt"] <= detail["startedAt"]
provenance = load(control / "batch-045-parent-native-provenance.json")
index = load(control / "batch-045-parent-native-artifact-index.json")
android_provenance = load(control / "batch-045-parent-android-provenance.json")
native = load(control / "batch-045-parent-native-recovery.json")
android = load(control / "batch-045-parent-android-recovery.json")
for row in provenance + android_provenance:
    source = Path(row["path"])
    assert digest(source) == row["sha256"]
    copy(source, native_dir / "parent-receipts" / source.name)
for row in index:
    source = Path(row["path"])
    assert digest(source) == row["sha256"]
    copy(source, native_dir / "attempt-1" / source.name)
for row in android["tests"]:
    copy(Path(row["artifactPath"]), native_dir / "parent-receipts" / Path(row["artifactPath"]).name)
for name in ("batch-045-parent-native-provenance.json", "execution-225-recovery-verification.json",
             "batch-045-visual-detail-derivation.json"):
    copy(control / name, native_dir / "parent-receipts" / name)
copy(control / "artifacts" / "batch-045-visual-detail.png", native_dir / "derived" / "batch-045-visual-detail.png")
for suffix in ("visual", "visual-detail"):
    copy(control / f"batch-045-{suffix}-prompt.txt", reviews / f"batch-045-{suffix}-task.txt")
record = {
    "schemaVersion": 1, "execution": 225, "batch": "045",
    "status": "native-and-freshAndroid-verified-pending-local-validation",
    "recordedAt": datetime.now().astimezone().isoformat(),
    "contentSnapshot": snapshot, "reviewedTeachingSnapshot": "1bff321d279bdc187b3569b710a50913fdbf5f0d",
    "native": native, "artifactIndex": index, "provenance": provenance,
    "android": android, "androidProvenance": android_provenance, "copiedEvidence": copied,
    "mechanicalVerification": load(control / "execution-225-recovery-verification.json"),
    "independentVisual": visual, "independentVisualDetail": detail,
    "detailDerivation": load(control / "batch-045-visual-detail-derivation.json"),
    "coordinatorDirectImages": [str(control / "artifacts" / "batch-045-parent-native-attempt-1" / f"n1-045-{name}.png")
                                for name in ("font-pairs", "kanji-reading-disposition")] +
                               [str(control / "artifacts" / "batch-045-visual-detail.png")],
    "coordinatorAdjudication": {
        "findings": [], "unresolvedConsequentialClaimsWithinBoundedVisualScope": [],
        "result": "Bounded emulator visual accepted; no teaching edit. Current coordinator directly inspected two full PNGs plus one source-pixel crop; parent ten accepted reads distinct.",
        "originalFindings": "Two blind textual initials37/38calls1/0internaloverlaps0XMLrangeviolations/all28assignedresources returned; four Claude optional items and supplied-source/quizfallback limits unchanged. No actionable textual findings.",
        "reportQualification": "First visual report preserved verbatim: self-count14 excludes launcher prompt; actual15calls/15turns/10PNG. Its downscaled巳/已visibility limit is resolved only for enlarged source pixels by narrow same-original-session2call/1crop followup. Not a normal-size phone guarantee. All remaining limits retained. Six hash-equivalent viewports not separately viewed.",
        "optional": [
            {"status": "optional", "claim": "Right table column clipping", "disposition": "Visible sideways-scroll hint and repeated Common words; unseen columns/full articles not certified."},
            {"status": "optional", "claim": "Section ends clipped", "disposition": "Other supplied viewports show continuation; no demonstrated teaching defect or full-article certification."},
        ],
        "fallbackDisposition": "巳己蛇包巻記 each four distinct raster styles;已 one shared Gothic-like fallback across all four production families, exact face unidentified. Enlarged captured Gothic pixels distinguish top/middle/intermediate left-return heights for巳/己/已. Not four bundled已designs or physical-phone/normal-size certification.",
    },
    "limits": "Bounded API35 emulator only. Original unchangedfixture accepted1terminal0/0/28probes/fullContentSyncONCEoffline. Parent source/artifact and fresh222Android3+1exactXML verified, not rerun. Actual5580/requested2048MiB automatic2560MiB/appheap192m576m unchanged. OriginalClaude15views/10PNG then2views/1derivedcrop, bothserial0overlaps/0unfinished/actualexit0. Source/returned bytes separately retained. Clipped/offscreen/fullarticles/fallbackquiz/phone/native-speaker/generalrelease/currentmain/CI/publicZIP not accepted. CompatibleAndroidf9b59a2+ required. Public71/1157remaining unchanged; no046/publication.",
}
save(reviews / "batch-045-native-acceptance.json", record)
print("Archived unchanged native and original-reviewer15/2serial views; actual report scope/counts reconciled.")

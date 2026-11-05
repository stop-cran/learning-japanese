import base64
import hashlib
import json
import re
import struct
import sys
from datetime import datetime
from pathlib import Path

C = Path(__file__).parent
R = C.parent / "learning-japanese"
V = R / "docs" / "n1-reviews"
family = sys.argv[1]
assert family in ("claude", "gpt")
verification = len(sys.argv) > 2
if verification:
    assert sys.argv[2] == "verify-first-read" and family == "gpt"
prefix = f"batch-064-visual-411-{family}"
load = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda b: hashlib.sha256(b).hexdigest()
process = load(C / f"{prefix}-process.json")
usage = load(C / f"{prefix}-usage.json")
raw_path = C / f"{prefix}.jsonl"
raw = raw_path.read_bytes()
events = [json.loads(s) for s in raw.decode("utf-8-sig").splitlines() if s.strip()]
messages = [e["data"] for e in events if e["type"] == "assistant.message"]
models = sorted({m["model"] for m in messages if m.get("model")})
report_path = V / f"{prefix}.md"
audit_path = V / f"{prefix}-execution.json"
report_text = [m["content"] for m in messages if m.get("content")][-1] + "\n"
if verification:
    original = load(audit_path)
    assert not original["processAndCoverageAccepted"] and not original["failedTools"]
    assert report_path.read_text(encoding="utf-8") == report_text
    audit_path = V / f"{prefix}-execution-verified.json"
    assert not audit_path.exists()
else:
    assert not report_path.exists() and not audit_path.exists()
    report_path.write_text(report_text, encoding="utf-8")
calls, active, overlaps = {}, set(), []
for event in events:
    data = event.get("data", {})
    if event["type"] == "tool.execution_start":
        key = data["toolCallId"]
        if active:
            overlaps.append({"starting": key, "alreadyActive": sorted(active)})
        active.add(key)
        calls[key] = {"name": data["toolName"], "arguments": data["arguments"],
                      "startedAt": event["timestamp"]}
    elif event["type"] == "tool.execution_complete":
        key = data["toolCallId"]
        active.remove(key)
        row = calls[key]
        row.update(completedAt=event["timestamp"], success=data["success"])
        if not data["success"]:
            row.update(error=data.get("error"), returnedCharacters=0)
            continue
        result = data["result"]
        text = result.get("content", "")
        row.update(returnedCharacters=len(text), returnedTextSha256=sha(text.encode("utf-8")),
                   truncationOrLimitMarker=any(s in text for s in (
                       "[Output truncated", "File too large to read", "Invalid view_range", "<note>Content truncated")))
        source = Path(row["arguments"]["path"])
        if source.suffix == ".png":
            images = result.get("binaryResultsForLlm", [])
            assert len(images) == 1 and images[0]["type"] == "image"
            image = base64.b64decode(images[0]["data"], validate=True)
            source_bytes = source.read_bytes()
            assert image.startswith(b"\x89PNG\r\n\x1a\n")
            returned = V / "batch-064-native" / f"visual-411-{family}-returned" / source.name
            returned.parent.mkdir(exist_ok=True)
            if verification:
                assert returned.read_bytes() == image
            else:
                assert not returned.exists()
                returned.write_bytes(image)
            row["imagePayload"] = {
                "bytes": len(image), "sha256": sha(image), "sourceSha256": sha(source_bytes),
                "sourceDimensions": struct.unpack(">II", source_bytes[16:24]),
                "returnedDimensions": struct.unpack(">II", image[16:24]),
                "exactFileBytesReturnedToModel": image == source_bytes,
                "returnedPayloadCopy": str(returned.relative_to(R)),
                "boundary": "Actual source/model-visible bytes retained; hashes do not establish comprehension.",
            }
        else:
            lines = source.read_text(encoding="utf-8-sig").splitlines(keepends=True)
            start, end = row["arguments"].get("view_range", [1, -1])
            expected = "".join(lines[start - 1:None if end == -1 else end])
            normalize = lambda s: s.replace("\r\n", "\n").rstrip()
            row["exactRequestedTextContainedInResult"] = normalize(expected) in normalize(text)
            row["requestedRange"] = [start, len(lines) if end == -1 else end]
task = C / "batch-064-visual-task.txt"
native = V / "batch-064-native" / "attempt-1"
names = set(re.findall(r"^n1-064-[\w-]+\.png$", task.read_text(encoding="utf-8"), re.M))
required_text = {
    str(task): None, str(R / "kanji" / "偵.md"): None, str(R / "words" / "探偵.md"): None,
}
if family == "claude":
    names = {f"n1-064-{s}.png" for s in ("kanji-compound-boundary", "kanji-no-kun",
             "kanji-detective-story", "detective-fiction-example", "detective-components", "detective-role-summary")}
    required_text[str(V / "batch-064-visual-claude.md")] = None
else:
    required_text.update({
        str(V / "batch-064-initial-gpt.md"): None,
        str(V / "batch-064-confirmation-gpt.md"): None,
        str(R / "kanji" / "探.md"): None, str(R / "words" / "刑事.md"): None,
        str(native / "N1Batch064NativeTest.kt"): [(54, 143), (150, 285), (286, 453), (499, 550)],
        str(native / "instrumentation.txt"): None, str(native / "n1-064-article-route.json"): None,
    })
missing_text = []
for path, ranges in required_text.items():
    actual = [x for x in calls.values() if x.get("success") and x["arguments"]["path"] == path]
    required = ranges or [(1, len(Path(path).read_text(encoding="utf-8-sig").splitlines()))]
    covered = {i for x in actual for i in range(x["requestedRange"][0], x["requestedRange"][1] + 1)}
    for start, end in required:
        if not set(range(start, end + 1)) <= covered:
            missing_text.append({"path": path, "range": [start, end]})
allowed = set(required_text) | {str(native / name) for name in names}
unexpected = [x["arguments"] for x in calls.values() if x["arguments"].get("path") not in allowed]
images = [x for x in calls.values() if "imagePayload" in x]
terminal = [e for e in events if e["type"] == "result"]
multi = [len(m["toolRequests"]) for m in messages if len(m.get("toolRequests", [])) > 1]
serial_before = True
if family == "gpt":
    prior_path = V / "batch-064-visual-411-claude-execution.json"
    prior = load(prior_path)
    began = datetime.fromisoformat(process["startedAt"])
    serial_before = (prior["processAndCoverageAccepted"]
                     and datetime.fromisoformat(prior["completedAt"]) < began
                     and prior_path.stat().st_mtime < began.timestamp()
                     and (V / "batch-064-visual-411-claude.md").stat().st_mtime < began.timestamp())
first = next(iter(calls.values()), {})
path_recovered = (first.get("name") == "view"
                  and first.get("arguments", {}).get("path") == str(task)
                  and first.get("success") and first.get("exactRequestedTextContainedInResult")
                  and first.get("requestedRange", [0, 0])[0] == 1
                  and first.get("requestedRange", [0, 0])[1] >= len(task.read_text(encoding="utf-8").splitlines()))
accepted = (
    process["exitCode"] == 0 and models == [process["requestedModel"]] == [usage["currentModel"]]
    and path_recovered and not active and not overlaps and not multi and not missing_text
    and serial_before and not unexpected
    and all(x["name"] == "view" and x["success"] and not x["truncationOrLimitMarker"]
            and x.get("exactRequestedTextContainedInResult", True) for x in calls.values())
    and len(images) == len(names)
    and {Path(x["arguments"]["path"]).name for x in images} == names
    and len({x["imagePayload"]["sourceSha256"] for x in images}) == len(names)
    and len(terminal) == 1 and terminal[0]["exitCode"] == 0
    and terminal[0]["sessionId"] == process["sessionId"]
    and not terminal[0]["usage"]["codeChanges"]["filesModified"]
)
record = {
    **process, "actualModels": models, "dependentFollowupNotBlindInitial": True,
    "reportSha256": sha(report_path.read_bytes()), "sharedTaskSha256": sha(task.read_bytes()),
    "rawExecutionLocation": str(raw_path), "rawExecutionSha256": sha(raw),
    "requestsPerAssistantResponse": [len(m.get("toolRequests", [])) for m in messages],
    "toolCalls": list(calls.values()), "observedToolOverlaps": overlaps,
    "multiToolResponses": multi, "unfinishedTools": sorted(active),
    "failedTools": [x for x in calls.values() if not x["success"]],
    "imagePayloadsVerified": len(images), "missingRequiredText": missing_text,
    "unexpectedReadPaths": unexpected, "exactFirstSharedTaskReadRecovered": bool(path_recovered),
    "priorExitAndArchiveVerifiedBeforeLaunch": serial_before,
    "usage": usage, "usageBoundary": "Cumulative original-session usage, not incremental411 effort.",
    "terminalResults": [{"sessionId": e["sessionId"], "exitCode": e["exitCode"]} for e in terminal],
    "processAndCoverageAccepted": bool(accepted),
    "limits": "Dependent visual confirmation only. Original408/409/410 strict acceptance remains FALSE. No new upstream dictionary, reviewer-executed native/device, phone, fallback-face or publication certification. Raw execution remains in control; private instructions/reasoning are not exported to Git.",
}
if verification:
    record["auditCorrection"] = {
        "originalAudit": str((V / f"{prefix}-execution.json").relative_to(R)),
        "originalAuditSha256": sha((V / f"{prefix}-execution.json").read_bytes()),
        "reason": "Initial auditor incorrectly required arguments to contain only path. Explicit view_range [1,140] returns the complete exact shared task, with returned UTF-8 hash identical to its frozen source. No reviewer rerun, substitution or gate waiver.",
        "exactReturnedTaskHashMatchesSource": first["returnedTextSha256"] == sha(task.read_bytes()),
    }
    assert record["auditCorrection"]["exactReturnedTaskHashMatchesSource"]
audit_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"family": family, "models": models, "calls": len(calls), "images": len(images),
                  "pathRecovered": bool(path_recovered), "accepted": bool(accepted),
                  "missingText": missing_text, "overlaps": overlaps, "multi": multi,
                  "unexpected": unexpected}, ensure_ascii=False, indent=2))
if not accepted:
    sys.exit(1)

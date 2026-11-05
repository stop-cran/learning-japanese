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
prefix = f"batch-064-visual-{family}"
load = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda b: hashlib.sha256(b).hexdigest()
process = load(C / f"{prefix}-process.json")
usage = load(C / f"{prefix}-usage.json")
raw_path = C / f"{prefix}.jsonl"
raw = raw_path.read_bytes()
events = [json.loads(s) for s in raw.decode("utf-8-sig").splitlines() if s.strip()]
messages = [e["data"] for e in events if e["type"] == "assistant.message"]
models = sorted({m["model"] for m in messages if m.get("model")})
reports = [m for m in messages if m.get("content")]
report_path = V / f"{prefix}.md"
audit_path = V / f"{prefix}-execution.json"
assert not audit_path.exists()
report_bytes = (reports[-1]["content"] + "\n").encode("utf-8")
if report_path.exists():
    assert report_path.read_text(encoding="utf-8").replace("\r\n", "\n") == report_bytes.decode("utf-8")
else:
    report_path.write_bytes(report_bytes)
calls, active, overlaps = {}, set(), []
for event in events:
    data = event.get("data", {})
    if event["type"] == "tool.execution_start":
        key = data["toolCallId"]
        if active:
            overlaps.append({"starting": key, "alreadyActive": sorted(active)})
        active.add(key)
        calls[key] = {"name": data["toolName"], "arguments": data["arguments"],
                      "startedAt": event["timestamp"], "model": data.get("model")}
    elif event["type"] == "tool.execution_complete":
        key = data["toolCallId"]
        active.remove(key)
        row = calls[key]
        if not data["success"]:
            row.update(completedAt=event["timestamp"], success=False,
                       error=data.get("error"), returnedCharacters=0,
                       truncationOrLimitMarker=False)
            continue
        result = data["result"]
        text = result.get("content", "")
        row.update(completedAt=event["timestamp"], success=data["success"],
                   returnedCharacters=len(text), returnedTextSha256=sha(text.encode("utf-8")),
                   truncationOrLimitMarker=any(s in text for s in (
                       "[Output truncated", "File too large to read", "Invalid view_range", "<note>Content truncated")))
        source = Path(row["arguments"]["path"])
        if source.suffix == ".png":
            images = result.get("binaryResultsForLlm", [])
            assert len(images) == 1 and images[0]["type"] == "image"
            image = base64.b64decode(images[0]["data"], validate=True)
            source_bytes = source.read_bytes()
            assert image.startswith(b"\x89PNG\r\n\x1a\n")
            returned = V / "batch-064-native" / f"visual-{family}-returned" / source.name
            returned.parent.mkdir(exist_ok=True)
            assert not returned.exists()
            returned.write_bytes(image)
            row["imagePayload"] = {
                "bytes": len(image), "sha256": sha(image), "sourceSha256": sha(source_bytes),
                "sourceDimensions": struct.unpack(">II", source_bytes[16:24]),
                "returnedDimensions": struct.unpack(">II", image[16:24]),
                "exactFileBytesReturnedToModel": image == source_bytes,
                "returnedPayloadCopy": str(returned.relative_to(R)),
                "boundary": "Exact source and actual model-visible payload preserved separately; hashes do not establish comprehension.",
            }
        else:
            lines = source.read_text(encoding="utf-8-sig").splitlines(keepends=True)
            start, end = row["arguments"].get("view_range", [1, -1])
            expected = "".join(lines[start - 1:None if end == -1 else end])
            normalize = lambda s: s.replace("\r\n", "\n").rstrip()
            row["exactRequestedTextContainedInResult"] = normalize(expected) in normalize(text)
            row["sourceLineCount"] = len(lines)
            row["requestedRange"] = [start, len(lines) if end == -1 else end]
task = C / "batch-064-visual-task.txt"
expected_names = set(re.findall(r"^n1-064-[\w-]+\.png$", task.read_text(encoding="utf-8"), re.M))
images = [x for x in calls.values() if "imagePayload" in x]
terminal = [e for e in events if e["type"] == "result"]
multi = [{"messageId": m.get("messageId"), "requests": len(m["toolRequests"])}
         for m in messages if len(m.get("toolRequests", [])) > 1]
required_text = {
    str(task): None,
    str(V / f"batch-064-initial-{family}.md"): None,
    str(V / f"batch-064-confirmation-{family}.md"): None,
    str(R / "kanji" / "偵.md"): None,
    str(R / "words" / "探偵.md"): None,
    str(R / "kanji" / "探.md"): None,
    str(R / "words" / "刑事.md"): None,
    str(V / "batch-064-native" / "attempt-1" / "N1Batch064NativeTest.kt"): [(54, 143), (150, 285), (286, 453), (499, 550)],
    str(V / "batch-064-native" / "attempt-1" / "instrumentation.txt"): None,
    str(V / "batch-064-native" / "attempt-1" / "n1-064-article-route.json"): None,
}
missing_text = []
for path, ranges in required_text.items():
    actual = [x for x in calls.values() if x.get("success")
              and str(Path(x["arguments"]["path"])) == path]
    required = ranges or [(1, len(Path(path).read_text(encoding="utf-8-sig").splitlines()))]
    covered = {i for x in actual for i in range(x["requestedRange"][0], x["requestedRange"][1] + 1)}
    for start, end in required:
        if not set(range(start, end + 1)) <= covered:
            missing_text.append({"path": path, "range": [start, end]})
serial_before = True
if family == "gpt":
    prior_path = V / "batch-064-visual-claude-execution.json"
    prior = load(prior_path)
    began = datetime.fromisoformat(process["startedAt"])
    serial_before = (prior["processAndCoverageAccepted"]
                     and datetime.fromisoformat(prior["completedAt"]) < began
                     and prior_path.stat().st_mtime < began.timestamp()
                     and (V / "batch-064-visual-claude.md").stat().st_mtime < began.timestamp())
allowed_paths = set(required_text) | {
    str(V / "batch-064-native" / "attempt-1" / name) for name in expected_names
}
allowed_paths.add(str(C / f"{prefix}-prompt.txt"))
unexpected_paths = [x["arguments"]["path"] for x in calls.values()
                    if x["arguments"]["path"] not in allowed_paths]
accepted = (
    process["exitCode"] == 0 and models == [process["requestedModel"]] == [usage["currentModel"]]
    and not active and not overlaps and not multi and not missing_text and serial_before
    and not unexpected_paths
    and all(x["name"] == "view" and x["success"] and not x["truncationOrLimitMarker"]
            and x.get("exactRequestedTextContainedInResult", True) for x in calls.values())
    and len(images) == len(expected_names) == 28
    and {Path(x["arguments"]["path"]).name for x in images} == expected_names
    and len({x["imagePayload"]["sourceSha256"] for x in images}) == 28
    and len(terminal) == 1 and terminal[0]["exitCode"] == 0
    and terminal[0]["sessionId"] == process["sessionId"]
    and not terminal[0]["usage"]["codeChanges"]["filesModified"]
)
record = {
    **process, "actualModels": models, "availableTools": ["view"],
    "dependentFollowupNotBlindInitial": True, "reportSha256": sha(report_path.read_bytes()),
    "sharedTaskSha256": sha(task.read_bytes()),
    "rawExecutionLocation": str(raw_path), "rawExecutionSha256": sha(raw),
    "controlArtifactHashes": {suffix: sha((C / (prefix + suffix)).read_bytes())
                              for suffix in ("-process.json", "-usage.json", "-prompt.txt", "-stderr.txt")},
    "requestsPerAssistantResponse": [len(m.get("toolRequests", [])) for m in messages],
    "multiToolResponses": multi, "toolCalls": list(calls.values()),
    "observedToolOverlaps": overlaps, "unfinishedTools": sorted(active),
    "failedTools": [x for x in calls.values() if not x["success"]],
    "imagePayloadsVerified": len(images), "missingRequiredText": missing_text,
    "unexpectedReadPaths": unexpected_paths,
    "distinctSourceImageHashes": len({x["imagePayload"]["sourceSha256"] for x in images}),
    "expectedPngMembershipReturned": {Path(x["arguments"]["path"]).name for x in images} == expected_names,
    "priorExitAndArchiveVerifiedBeforeLaunch": serial_before,
    "usage": usage, "usageBoundary": "Resumed-session usage is cumulative, not this turn's measured cost.",
    "terminalResults": [{"sessionId": e["sessionId"], "exitCode": e["exitCode"]} for e in terminal],
    "processAndCoverageAccepted": accepted,
    "limits": "Dependent original-session visual confirmation, not blind initial or reviewer-executed native tests. Actual returned bytes are not comprehension. Raw execution retained in sibling control; provider reasoning and private instructions not exported into Git. Original source/process limits remain historical.",
}
audit_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({
    "family": family, "models": models, "calls": len(calls), "overlaps": overlaps,
    "multiToolResponses": multi, "images": len(images), "missingText": missing_text,
    "unexpectedPaths": unexpected_paths, "accepted": accepted,
}, ensure_ascii=False, indent=2))
assert accepted, "Report and execution preserved; bounded process/coverage failure needs reconciliation."

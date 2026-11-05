import base64
import hashlib
import json
import re
import struct
import sys
from pathlib import Path

c = Path(__file__).resolve().parent
r = c.parent / "learning-japanese"
out = r / "docs" / "n1-reviews"
label = sys.argv[1]
assert label in ("claude", "gpt", "claude-clarification")
prefix = f"batch-057-visual-{label}"
load = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda b: hashlib.sha256(b).hexdigest()
process = load(c / f"{prefix}-process.json")
usage = load(c / f"{prefix}-usage.json")
raw_path = c / f"{prefix}.jsonl"
raw = raw_path.read_bytes()
events = [json.loads(s) for s in raw.decode("utf-8-sig").splitlines() if s.strip()]
messages = [e["data"] for e in events if e["type"] == "assistant.message"]
models = sorted({m["model"] for m in messages if m.get("model")})
reports = [m for m in messages if m.get("content")]
report_path = out / f"{prefix}.md"
audit_path = out / f"{prefix}-execution.json"
assert not report_path.exists() and not audit_path.exists()
report_path.write_text(reports[-1]["content"] + "\n", encoding="utf-8")
calls, active, overlaps = {}, set(), []
for event in events:
    data = event.get("data", {})
    if event["type"] == "tool.execution_start":
        key = data["toolCallId"]
        if active:
            overlaps.append({"starting": key, "alreadyActive": sorted(active)})
        active.add(key)
        calls[key] = {
            "name": data["toolName"], "arguments": data["arguments"],
            "startedAt": event["timestamp"], "model": data.get("model"),
        }
    elif event["type"] == "tool.execution_complete":
        key = data["toolCallId"]
        active.remove(key)
        row = calls[key]
        result = data["result"]
        text = result.get("content", "")
        row.update(
            completedAt=event["timestamp"], success=data["success"],
            returnedCharacters=len(text), returnedTextSha256=sha(text.encode("utf-8")),
            truncationOrLimitMarker=any(s in text for s in (
                "[Output truncated", "File too large to read", "Invalid view_range", "<note>Content truncated",
            )),
        )
        source = Path(row["arguments"]["path"])
        if source.suffix == ".png":
            images = result.get("binaryResultsForLlm", [])
            assert len(images) == 1 and images[0]["type"] == "image"
            image = base64.b64decode(images[0]["data"], validate=True)
            source_bytes = source.read_bytes()
            assert image.startswith(b"\x89PNG\r\n\x1a\n")
            returned = out / "batch-057-native" / f"visual-{label}-returned" / source.name
            returned.parent.mkdir(exist_ok=True)
            assert not returned.exists()
            returned.write_bytes(image)
            row["imagePayload"] = {
                "bytes": len(image), "sha256": sha(image),
                "sourceSha256": sha(source_bytes),
                "sourceDimensions": struct.unpack(">II", source_bytes[16:24]),
                "returnedDimensions": struct.unpack(">II", image[16:24]),
                "exactFileBytesReturnedToModel": image == source_bytes,
                "returnedPayloadCopy": str(returned.relative_to(r)),
                "boundary": "Source and actual model-visible payload preserved separately; byte consistency is not comprehension.",
            }
        else:
            lines = source.read_text(encoding="utf-8-sig").splitlines(keepends=True)
            start, end = row["arguments"].get("view_range", [1, -1])
            expected = "".join(lines[start - 1:None if end == -1 else end])
            normalize = lambda s: s.replace("\r\n", "\n").rstrip()
            row["exactRequestedTextContainedInResult"] = normalize(expected) in normalize(text)
            row["sourceLineCount"] = len(lines)
            row["requestedRange"] = [start, len(lines) if end == -1 else end]
expected_names = set(re.findall(r"^n1-057-[\w-]+\.png$", (c / "batch-057-visual-task.txt").read_text(encoding="utf-8"), re.M))
if label == "claude-clarification":
    expected_names = {"n1-057-enterprise-backlink-kanji.png", "n1-057-selection.png"}
images = [x for x in calls.values() if "imagePayload" in x]
terminal = [e for e in events if e["type"] == "result"]
record = {
    **process, "actualModels": models, "availableTools": ["view"],
    "dependentFollowupNotBlindInitial": True,
    "reportSha256": sha(report_path.read_bytes()),
    "sharedTaskSha256": sha((c / "batch-057-visual-task.txt").read_bytes()),
    "rawExecutionLocation": str(raw_path), "rawExecutionSha256": sha(raw),
    "configurationEvidence": [e["data"] for e in events if e["type"] == "system.message"
                              and e["data"].get("infoType") == "configuration"],
    "toolCalls": list(calls.values()), "observedToolOverlaps": overlaps,
    "unfinishedTools": sorted(active), "imagePayloadsVerified": len(images),
    "expectedPngMembershipReturned": {Path(x["arguments"]["path"]).name for x in images} == expected_names,
    "usage": usage,
    "usageBoundary": "Resumed-session usage is cumulative, not the measured cost of this followup.",
    "terminalResults": [{"sessionId": e["sessionId"], "exitCode": e["exitCode"]} for e in terminal],
    "limits": "Original complete final report unchanged. Process/byte-return audit not comprehension certification. Dependent visual confirmation, not blind initial or reviewer-executed native tests. Raw execution retained in sibling control; provider reasoning not exported into Git.",
}
audit_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
assert process["exitCode"] == 0
assert models == [process["requestedModel"]] == [usage["currentModel"]]
assert not active
assert all(x["name"] == "view" and x["success"] and not x["truncationOrLimitMarker"] for x in calls.values())
assert all(x.get("exactRequestedTextContainedInResult", True) for x in calls.values())
assert len(images) == len(expected_names) and record["expectedPngMembershipReturned"]
assert len({x["imagePayload"]["sourceSha256"] for x in images}) == len(expected_names)
assert len(terminal) == 1 and terminal[0]["exitCode"] == 0 and terminal[0]["sessionId"] == process["sessionId"]
assert not terminal[0]["usage"]["codeChanges"]["filesModified"]
print(f"Archived {prefix}: {models}, {len(calls)} calls, {len(overlaps)} overlaps, {len(images)} actual image payloads.")

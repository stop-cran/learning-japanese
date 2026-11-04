import base64
import hashlib
import json
import struct
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
control = Path(__file__).resolve().parent
root = control.parent / "learning-japanese"
out = root / "docs" / "n1-reviews"
label = sys.argv[1]
assert label in ["claude", "gpt"]
prefix = f"batch-050-visual-{label}"
raw_path = control / f"{prefix}.jsonl"
raw = raw_path.read_bytes()
events = [json.loads(s) for s in raw.decode("utf-8-sig").splitlines() if s.strip()]
load = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
process = load(control / f"{prefix}-process.json")
usage = load(control / f"{prefix}-usage.json")
assert process["exitCode"] == 0
messages = [e["data"] for e in events if e["type"] == "assistant.message"]
models = sorted({m["model"] for m in messages if m.get("model")})
assert models == [process["requestedModel"]] == [usage["currentModel"]]
calls, active, overlaps = {}, set(), []
for event in events:
    data = event.get("data", {})
    if event["type"] == "tool.execution_start":
        key = data["toolCallId"]
        if active:
            overlaps.append({"starting": key, "alreadyActive": sorted(active)})
        active.add(key)
        assert data["toolName"] == "view", data
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
            returnedCharacters=len(text),
            returnedTextSha256=hashlib.sha256(text.encode("utf-8")).hexdigest(),
            truncationOrLimitMarker=any(s in text for s in [
                "[Output truncated", "File too large to read", "Invalid view_range", "<note>Content truncated",
            ]),
        )
        path = Path(row["arguments"]["path"])
        if path.suffix == ".png":
            images = result.get("binaryResultsForLlm", [])
            assert len(images) == 1 and images[0]["type"] == "image", path
            image = base64.b64decode(images[0]["data"], validate=True)
            source = path.read_bytes()
            assert image.startswith(b"\x89PNG\r\n\x1a\n") and source.startswith(b"\x89PNG\r\n\x1a\n")
            source_size = struct.unpack(">II", source[16:24])
            returned_size = struct.unpack(">II", image[16:24])
            assert source_size == (1080, 2400) and returned_size == (900, 2000)
            returned_path = out / "batch-050-native" / "view-returned" / path.name
            returned_path.parent.mkdir(exist_ok=True)
            if returned_path.exists():
                assert returned_path.read_bytes() == image
            else:
                returned_path.write_bytes(image)
            row["imagePayload"] = {
                "bytes": len(image), "sha256": hashlib.sha256(image).hexdigest(),
                "mimeType": images[0].get("mimeType"),
                "description": images[0].get("description"),
                "sourceSha256": hashlib.sha256(source).hexdigest(),
                "sourceDimensions": source_size, "returnedDimensions": returned_size,
                "exactFileBytesReturnedToModel": image == source,
                "returnedPayloadCopy": str(returned_path.relative_to(root)),
                "boundary": "view tool returned a resized PNG, not original bytes; source hash and actual payload hash/dimensions recorded separately. No independent proof of tool resampling algorithm.",
            }
        else:
            lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
            start, end = row["arguments"].get("view_range", [1, -1])
            expected = "".join(lines[start - 1:None if end == -1 else end])
            normalize = lambda s: s.replace("\r\n", "\n").rstrip()
            row["exactRequestedTextContainedInResult"] = normalize(expected) in normalize(text)
            assert row["exactRequestedTextContainedInResult"], path
        assert row["success"] and not row["truncationOrLimitMarker"], row
assert not active and not overlaps
expected_pngs = load(control / "batch-050-recovered-evidence-verification.json")["sameVisualScope"]
observed_pngs = [x for x in calls.values() if "imagePayload" in x]
assert {x["arguments"]["path"] for x in observed_pngs} == {x["path"] for x in expected_pngs}
assert len(observed_pngs) == 12
report = messages[-1]["content"] + "\n"
report_path = out / f"{prefix}.md"
audit_path = out / f"{prefix}-execution.json"
assert not report_path.exists() and not audit_path.exists()
report_path.write_text(report, encoding="utf-8")
record = {
    **process, "actualModels": models, "availableTools": ["view"],
    "dependentFollowupNotBlindInitial": True,
    "reportSha256": hashlib.sha256(report_path.read_bytes()).hexdigest(),
    "rawExecutionLocation": str(raw_path), "rawExecutionSha256": hashlib.sha256(raw).hexdigest(),
    "toolCalls": list(calls.values()), "observedToolOverlaps": overlaps, "unfinishedTools": [],
    "imagePayloadsVerified": 12, "usage": usage,
    "usageBoundary": "Resumed-session usage is cumulative, not a measured cost of this followup alone.",
    "limits": "Complete final report preserved without editorial changes. Byte-return and serial-tool audit, not comprehension certification. Initial review stays independent; this supplied-evidence visual followup is not blind or reviewer-executed native testing. Raw execution retained in sibling control; provider reasoning not exported into Git.",
}
audit_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Archived {prefix}: actual {models}, {len(calls)} calls,0 overlaps,12 actual resized PNG payloads preserved,0 truncations.")
print(report)

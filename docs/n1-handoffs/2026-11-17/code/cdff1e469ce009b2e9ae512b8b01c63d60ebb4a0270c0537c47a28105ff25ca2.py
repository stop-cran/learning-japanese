"""Read-only progress poll of a reviewer session: python poll_reviewer.py SESSION_ID SINCE_ISO [REPORT_PATH]"""
import json
import os
import sys
from collections import Counter

sid, since = sys.argv[1], sys.argv[2]
report = sys.argv[3] if len(sys.argv) > 3 else None
path = os.path.join(r"C:\Users\stop-\.copilot\session-state", sid, "events.jsonl")
rows = []
with open(path, encoding="utf-8") as fh:
    for line in fh:
        line = line.strip()
        if not line:
            continue
        try:
            e = json.loads(line)
        except ValueError:
            continue
        if e.get("timestamp", "") >= since:
            rows.append(e)

starts, completes, names, order = {}, {}, {}, []
for e in rows:
    d = e.get("data") or {}
    if e["type"] == "tool.execution_start":
        starts[d["toolCallId"]] = e["timestamp"]
        names[d["toolCallId"]] = d.get("toolName")
        order.append(d["toolCallId"])
    elif e["type"] == "tool.execution_complete":
        completes[d["toolCallId"]] = e["timestamp"]

marks = []
for cid, s in starts.items():
    marks.append((s, 1, cid))
    marks.append((completes.get(cid, s), 0, cid))
marks.sort(key=lambda m: (m[0], m[1]))
cur = peak = 0
overlaps = 0
for _, kind, _cid in marks:
    if kind == 1:
        cur += 1
        if cur > 1:
            overlaps += 1
        peak = max(peak, cur)
    else:
        cur -= 1

assistant = sum(1 for e in rows if e["type"] == "assistant.message")
done = [e for e in rows if e["type"] == "session.task_complete" or (e["type"] == "tool.execution_start" and (e.get("data") or {}).get("toolName") == "task_complete")]
print("events", len(rows), "first", rows[0]["timestamp"] if rows else None, "last", rows[-1]["timestamp"] if rows else None)
print("tool starts", len(starts), "completes", len(completes), "in flight now", len(starts) - len(completes), "max in flight", peak, "overlapping starts", overlaps)
print("by tool", dict(Counter(names.values())))
print("last tools", [names[c] for c in order[-6:]])
print("assistant messages", assistant, "task_complete seen", bool(done))
if report:
    print("report exists", os.path.exists(report), os.path.getsize(report) if os.path.exists(report) else "")

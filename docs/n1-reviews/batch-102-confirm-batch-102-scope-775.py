"""Clarify an original review's scope without changing its preserved report."""
import importlib.util
import json
import os
import shutil
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

C = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("batch102", C / "review-batch-102-775.py")
batch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(batch)
r = batch.review
batch.frozen()
original = r.load(r.V / "batch-102-initial-claude-execution.json")
other = r.load(r.V / "batch-102-initial-gpt-execution.json")
assert r.absent(original["launcherPid"]) and r.absent(other["launcherPid"])
inventory = []
for name in ["jmdict", "comparison-jmdict"]:
    entries = ET.parse(r.S / f"batch-102-{name}.xml").getroot().findall("entry")
    inventory.append({"packet": name, "count": len(entries),
                      "entryIds": [e.findtext("ent_seq") for e in entries]})
provenance = r.load(r.V / "batch-102-review-dictionary-provenance.json")
articles = [s for s in provenance["sources"]
            if str(Path(s["path"]).parent) in [str(r.R / "words"), str(r.R / "kanji")]]
assert len(articles) == 32
prompt = f"""Original-session read-only SCOPE CLARIFICATION only, same unchanged signed snapshot {r.SNAPSHOT}.
Your original report is preserved unchanged. No other reviewer's report or author adjudication is supplied.
The execution audit verified your one view call returned the exact full272741-byte/6196-line packet, without truncation. This proves byte access, NOT comprehension. A parser independently enumerated69+43=112 complete families and32 article bodies (two new, two reused,28 further comparison articles). Your report instead counted68+42=110 and23 comparison articles. Resolve this precise scope discrepancy, not by accepting the requested totals as proof of comprehension. Inventory below.

State whether those were counting/reporting mistakes, or identify any entries/articles actually uninspected. If any were not inspected, inspect them now from the original common packet at {r.PACKET}, with view only and strictly SERIAL calls. Do not invent full semantic review from byte counts. If you cannot establish complete scope, explicitly preserve that limit and identify the remaining records. The same packet is still available; no teaching has changed. No need to reread all112 families if this was merely a reporting count error. Do not change the original report.

After resolving scope, report any resulting changed-article correctness/scoped-coverage/text-comprehensibility finding, or none; preserve native/runtime/phone/upstream limits. Do not expand optional teaching or review unrelated articles. State actual model, exact reads this turn, whether prior semantic inspection or new inspection supports clarification, and limits.
MECHANICAL FAMILY INVENTORY:
{json.dumps(inventory, ensure_ascii=True)}
ARTICLE INVENTORY:
{json.dumps(articles, ensure_ascii=True)}
"""
prefix = "batch-102-scope-claude"
raw, stderr = C / (prefix + ".jsonl"), C / (prefix + "-stderr.txt")
assert not raw.exists()
session = original["sessionId"]
cmd = [shutil.which("copilot"), "-C", str(r.R), "--add-dir", str(C),
       "--model", "claude-opus-5.5", "--session-id", session, "--no-ask-user",
       "--allow-tool=view", "--disable-builtin-mcps", "--available-tools=view",
       "--no-custom-instructions", "--output-format", "json",
       "--log-dir", str(C / "review-logs" / prefix),
       "--usage-output-file", str(C / (prefix + "-usage.json")), "-p", prompt]
r.save(C / (prefix + "-prompt.json"), {"prompt": prompt})
(r.V / (prefix + "-task.txt")).write_text(prompt, encoding="utf-8")
env = os.environ.copy()
env.pop("GH_TOKEN", None)
env.pop("GITHUB_TOKEN", None)
started = r.now()
with raw.open("wb") as out, stderr.open("wb") as err:
    proc = subprocess.Popen(cmd, stdout=out, stderr=err, env=env)
    r.save(C / (prefix + "-active.json"), {"pid": proc.pid, "sessionId": session, "startedAt": started})
    print("Scope clarification running", proc.pid, flush=True)
    code = proc.wait()
events = [json.loads(line) for line in raw.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
messages = [e["data"] for e in events if e.get("type") == "assistant.message"]
models = sorted({m.get("model", "") for m in messages})
report = r.V / (prefix + ".md")
report.write_text(messages[-1]["content"] + "\n" if messages else "No completed report.\n", encoding="utf-8")
active, overlaps, calls = set(), [], []
for event in events:
    data = event.get("data", {})
    if event.get("type") == "tool.execution_start":
        if active:
            overlaps.append(sorted(active))
        active.add(data["toolCallId"])
        calls.append(data)
    elif event.get("type") == "tool.execution_complete":
        active.discard(data["toolCallId"])
usage = r.load(C / (prefix + "-usage.json"))
r.save(r.V / (prefix + "-execution.json"), {
    "snapshot": r.SNAPSHOT, "originalSessionId": session, "launcherPid": proc.pid,
    "startedAt": started, "completedAt": r.now(), "exitCode": code,
    "actualModels": models, "usageCurrentModel": usage["currentModel"],
    "availableTools": ["view"], "toolCalls": calls, "observedToolOverlaps": overlaps,
    "unfinishedTools": sorted(active), "reportSha256": r.sha(report),
    "rawExecutionSha256": r.sha(raw),
    "limits": "Dependent original-session scope clarification, not a third blind review. Counts/byte access are not comprehension.",
})
shutil.copyfile(raw, r.V / raw.name)
shutil.copyfile(stderr, r.V / stderr.name)
assert code == 0 and models == ["claude-opus-5.5"] and usage["currentModel"] == "claude-opus-5.5"
assert not active and not overlaps and r.absent(proc.pid)
batch.frozen()
print("Scope clarification preserved; actual process exited.")

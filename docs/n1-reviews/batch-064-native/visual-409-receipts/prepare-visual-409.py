import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).parent
R = C.parent / "learning-japanese"
V = R / "docs" / "n1-reviews"
load = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
p = C / "progress.json"
data = load(p)
assert data["checkpoint"] == 408 and data["batch"] == "064"
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=R, text=True).strip()
assert head == "c111a1b7d2f6148c2ca87a5c4386c46ccf739879"
assert not subprocess.check_output(["git", "status", "--porcelain"], cwd=R)
request = C / "logs" / "16ebcc3f-151d-4a85-9965-b259d33e26a4" / "request.txt"
raw = request.read_bytes()
text = raw.decode("utf-8-sig")
marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
assert json.loads(text.split(marker, 1)[1])["checkpoint"] == 408
recovery = load(C / "batch-064-parent-shared-task-read-recovery.json")
assert hashlib.sha256((C / "batch-064-visual-task.txt").read_bytes()).hexdigest() == recovery["taskSha256"]
data["execution409StartingState"] = {
    "execution": 409, "batch": "064", "startingHead": head,
    "status": "preparing-bounded-original-claude-recovery-confirmation",
    "scope": "SAME064 original Claude dependent missing-task/consequential-pixel confirmation, then original GPT visual confirmation strictly serial after complete first archive; signed local evidence checkpoint only. No native/Android rerun, publication,065 or second runner.",
    "authorization": {
        "requestSha256": hashlib.sha256(raw).hexdigest(),
        "characters": len(text), "lines": len(text.splitlines()),
        "completeFileLoadedAndCheckpointParsed": True,
        "limits": "Entire request acquired into memory and parsed; operative contract, final408/parent recovery and approved issue directly inspected. Historical middle not freshly semantically re-reviewed.",
    },
    "worktrees": "Clean dedicated content signedG c111a1b7 and Android f9b59a2. No headless reviewer active. Runner lock read returned Windows sharing violation, consistent with parent's exclusive lock; not a new permission denial. No canonical checkout accessed.",
    "recordedAt": datetime.now(timezone.utc).isoformat(),
}
p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
native = V / "batch-064-native" / "attempt-1"
names = [
    "n1-064-kanji-compound-boundary.png",
    "n1-064-kanji-no-kun.png",
    "n1-064-kanji-detective-story.png",
    "n1-064-detective-fiction-example.png",
    "n1-064-detective-components.png",
    "n1-064-detective-role-summary.png",
]
claude = f"""SAME064 execution409 BOUNDED DEPENDENT recovery confirmation in YOUR ORIGINAL Claude session.
Not a fresh blind initial, dictionary review, native rerun or retroactive acceptance.
Frozen teaching ff6eb7893344b806bf517ebd41bf19089bed5021 unchanged; evidence HEAD {head}.
Historical408 required shared task view failed. Parent has resolved ONLY that exact read,
successfully reading its original7294bytes/hash57b9eaef18761da17477704b6eab37216d6f5c6cd3f0985d25b13a5d0aaf12cf.
Parent read is NOT your read. Original408 report/process and failed call remain immutable;
historical strict process/coverage stays FALSE regardless of this follow-up.

Exactly ONE view call per response; wait before next. No parallel calls, shell, delegation,
edits, search or task_complete. If any call is denied, STOP and report it; no alternatives/retry.
FIRST freshly view the COMPLETE original task at this EXACT path:
{C / 'batch-064-visual-task.txt'}
Then view YOUR complete original408 visual report:
{V / 'batch-064-visual-claude.md'}
Do not repeat all408 reads; use their returned evidence with its documented limits.
This recovery task overrides its larger reread scope: fresh evidence is limited to the
shared task, your408report, these TWO complete current articles and SIX images:
{R / 'kanji' / '偵.md'}
{R / 'words' / '探偵.md'}
"""
claude += "\n".join(str(native / n) for n in names)
claude += """

Reassess specifically your408 claims that the kun cell is a dash visible after sideways
scrolling and that every in-scope paragraph/full footer was visible. Compare actual pixels
with complete source. Describe any clipped portion without inventing offscreen rows or
certifying unseen prose. Correct or withdraw unsupported report claims explicitly; distinguish
source knowledge from fresh pixels and retained408 pixels. No manufactured content defect
if report wording rather than teaching is wrong. Consequential unresolved claims UNVERIFIED.
Keep original lexical/source/lookup/process limits and accepted404Android/406native supplied
results unchanged. No dictionary, actual fallback-face, physical-phone/general-release,
whole-set, latest-main or publication certification.
Return full Snapshot/Scope/Verdicts(all4original files, inherited versus fresh facets)/
Findings/Optional/Limits. Explicitly reconcile old claims as resolved/withdrawn/unresolved/
optional, enumerate new reads and inherited28images, and historical failed-task-read.
Final report then EXIT; no task_complete.
"""
gpt = (C / "batch-064-visual-gpt-prompt.txt").read_text(encoding="utf-8")
gpt += f"""

Execution409 dependent original-session follow-up; evidence-only HEAD now {head}.
The frozen teaching and all supplied native evidence remain unchanged. You have NOT yet
performed your native visual turn. Do the complete assigned task and all28single PNG reads.
Do not read any Claude report, coordinator adjudication or recovery report. Only own initial/
textual reports are allowed. Exactly one view call per response. If denied STOP immediately;
do not continue using supplied prompt text or substitute a path/tool. Report missing evidence.
"""
for family, prompt in [("claude", claude), ("gpt", gpt)]:
    target = C / f"batch-064-visual-409-{family}-prompt.txt"
    assert not target.exists()
    target.write_text(prompt, encoding="utf-8")
print("Execution409 starting scope and bounded prompts saved; full live history preserved.")

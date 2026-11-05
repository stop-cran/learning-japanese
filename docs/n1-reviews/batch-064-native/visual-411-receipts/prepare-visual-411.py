import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).parent
R = C.parent / "learning-japanese"
load = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
git = lambda *args: subprocess.check_output(["git", *args], cwd=R, text=True).strip()
P = C / "progress.json"
data = load(P)
assert data["checkpoint"] == 410 and data["batch"] == "064"
assert data["status"] == "continue"
authorization = load(C / "batch-064-authorized-scoped-path-recovery.json")
head = git("rev-parse", "HEAD")
assert head == authorization["savedContentHead"]
assert not git("status", "--porcelain")
assert not git("diff", "ff6eb7893344b806bf517ebd41bf19089bed5021", "--",
               "kanji", "words", "articles", "strokes", "manifest.json")
assert not (C / ".github").exists(), "Inspect unexpected trusted configuration"
assert sha(Path(authorization["notesPath"])) == authorization["notesSha256"]
freeze = load(C / "batch-064-visual-freeze.json")
for path, expected in (freeze["teachingHashes"] | freeze["originalReportHashes"]).items():
    assert sha(R / path) == expected, path
assert sha(C / "batch-064-visual-task.txt") == freeze["sharedTaskSha256"]
request = C / "logs" / "dc77bb34-e440-4b03-bba6-985f310b5819" / "request.txt"
raw = request.read_bytes()
text = raw.decode("utf-8-sig")
marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
assert json.loads(text.split(marker, 1)[1])["checkpoint"] == 410
for family in ("claude", "gpt"):
    old = C / f"batch-064-visual-410-{family}-prompt.txt"
    prompt = old.read_text(encoding="utf-8").split("\n\nExecution410 NEW", 1)[0]
    if family == "gpt":
        prompt = prompt.split("\n\nExecution409 dependent", 1)[0]
    prompt += f"""

Execution411 CURRENT authorization and evidence, superseding historical launch
and access descriptions above. User2026-11-05T12:46:10.432+01:00 authorized
the scoped CLI path grant --add-dir {C}. Historical denials were CLI path
approval, not OS sharing locks. This grant is now in YOUR launch; recovery
remains unverified until YOUR EXACT first shared-task view succeeds.
Current evidence HEAD {head}; teaching unchanged at
ff6eb7893344b806bf517ebd41bf19089bed5021. Original408/409/410 logs immutable,
strict coverage FALSE. No retroactive acceptance. First read EXACT shared task:
{C / 'batch-064-visual-task.txt'}
If denied STOP immediately, no retries/substitutions. Otherwise do only the
assigned scope: Claude own408 report/two articles/SIX images and BOTH old
claim reconciliations; GPT own initial/confirmation/four teaching files/four
fixture ranges/terminal log/route receipt and all28images. Do NOT follow the
larger shared-task reread instructions in Claude's bounded assignment.
One view per response, serially; no other tools, opposite report or author
adjudication. Distinguish inherited source evidence, new pixels and supplied
operational results. Claims about hidden kun cells or every paragraph/footer
must be withdrawn/qualified unless supported by actual returned pixels.
Do not manufacture a content defect from an inaccurate previous report.
Full contract report then EXIT; no task_complete.
"""
    target = C / f"batch-064-visual-411-{family}-prompt.txt"
    assert not target.exists()
    target.write_text(prompt, encoding="utf-8")
data["execution411StartingState"] = {
    "execution": 411, "batch": "064", "startingHead": head,
    "status": "authorized-scoped-path-grant-prepared",
    "scope": "SAME064 scoped path recovery, bounded original Claude confirmation then original GPT full dependent visual, strictly serial; signed local evidence checkpoint only. No native/Android rerun, runtime publication,065 or second runner.",
    "authorization": authorization,
    "request": {"sha256": sha(request), "characters": len(text),
                "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                "limits": "Entire request acquired and complete checkpoint parsed; operative contract, approved issue, final checkpoint and scoped authorization directly inspected. Historical middle not freshly semantically re-reviewed."},
    "configurationPreflight": "No control .github directory; scoped trust inspected. No global permissions, ACL or configuration changed.",
    "recordedAt": datetime.now(timezone.utc).isoformat(),
}
data["stage"] = "batch-064-scoped-reviewer-path-recovery-and-visual-running"
P.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Execution411 starting state and new prompts persisted; full live history preserved.")

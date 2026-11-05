import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).parent
R = C.parent / "learning-japanese"
load = lambda path: json.loads(path.read_text(encoding="utf-8-sig"))
p = C / "progress.json"
data = load(p)
assert data["checkpoint"] == 409 and data["batch"] == "064"
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=R, text=True).strip()
assert head == "1effd21f78c2c86e215b463f9857ab123d90d266"
assert not subprocess.check_output(["git", "status", "--porcelain"], cwd=R)
request = C / "logs" / "9d6c4f04-cb0f-438f-906a-2298f8dc6739" / "request.txt"
raw = request.read_bytes()
text = raw.decode("utf-8-sig")
marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
assert json.loads(text.split(marker, 1)[1])["checkpoint"] == 409
authorization = load(C / "batch-064-user-authorized-reviewer-retry.json")
assert authorization["userAuthorization"] == "Ok, I see, try now"
assert not authorization["permissionResolved"]
data["execution410StartingState"] = {
    "execution": 410, "batch": "064", "startingHead": head,
    "status": "one-user-authorized-original-reviewer-retry-prepared",
    "scope": "ONE original Claude exact shared-task view retry; bounded missing-task/pixel confirmation only after success; original GPT strictly serial only after complete first archive. Durable local checkpoint, no native/Android rerun, publication,065 or second runner.",
    "authorization": authorization,
    "request": {
        "sha256": hashlib.sha256(raw).hexdigest(),
        "characters": len(text), "lines": len(text.splitlines()),
        "completeFileLoadedAndCheckpointParsed": True,
        "limits": "Entire file acquired and complete embedded checkpoint parsed. Operative contract, approved issue, final checkpoint and new authorization directly inspected; historical middle not freshly semantically re-reviewed.",
    },
    "recordedAt": datetime.now(timezone.utc).isoformat(),
}
data["stage"] = "batch-064-one-user-authorized-reviewer-retry-running"
p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
for family in ("claude", "gpt"):
    prompt = (C / f"batch-064-visual-409-{family}-prompt.txt").read_text(encoding="utf-8")
    prompt += f"""

Execution410 NEW explicit user authorization2026-11-05T12:17:22.316+01:00:
"Ok, I see, try now". Evidence HEAD now {head}; teaching unchanged.
Historical409 failed EXACT shared-task view and stopped; parent coordinator-only
success did NOT establish reviewer permission. All historical reports/denials stay
immutable; no retroactive strict408/409 acceptance. No claim permission resolved.
This is ONE expressly user-authorized attempt, NOT an autonomous denial retry.
FIRST make EXACT view call path
{C / 'batch-064-visual-task.txt'}
If denied, STOP immediately and final-report actual failure: no substitute path/tool,
supplied-prompt proxy, policy changes or further attempt. If successful, complete
only your assigned bounded scope above (Claude six-image claim reconciliation;
GPT full dependent visual with28images). One call per response, no task_complete.
For Claude reconcile BOTH old consequential claims explicitly against actual
pixels, including kun-dash and every-paragraph/full-footer visibility. Retained
408pixels and fresh410pixels are distinct. Source text is not unseen-pixel proof.
No opposite report or author adjudication. Final report then EXIT.
"""
    target = C / f"batch-064-visual-410-{family}-prompt.txt"
    assert not target.exists()
    target.write_text(prompt, encoding="utf-8")
print("Execution410 starting scope and prompts persisted; full live history preserved.")

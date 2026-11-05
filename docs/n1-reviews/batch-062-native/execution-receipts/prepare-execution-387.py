import hashlib
import json
import subprocess
from datetime import datetime
from pathlib import Path

C = Path(__file__).parent
R = C.parent / "learning-japanese"
REQUEST = C / "logs" / "2e8fe088-e894-4d3c-8a78-624ccd240ea3" / "request.txt"
HEAD = "da3a602a8eaf12190c7baf4048d02d86fe20a048"
TEACHING = "38ab6072d2041325142c54cf54be5d126928eb31"


def git(*args, cwd=R):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=cwd, text=True, encoding="utf-8").strip()


text = REQUEST.read_text(encoding="utf-8-sig")
marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
checkpoint = json.loads(text.split(marker, 1)[1])
assert checkpoint["checkpoint"] == 386
assert git("rev-parse", "HEAD") == HEAD and not git("status", "--porcelain")
assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json")
A = C.parent / "kanji-cards-android"
assert git("rev-parse", "HEAD", cwd=A) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
assert not git("status", "--porcelain", cwd=A)
p = C / "progress.json"
progress = json.loads(p.read_text(encoding="utf-8-sig"))
assert progress["checkpoint"] == 386 and progress["batch"] == "062"
backup = C / "execution-387-precheckpoint-progress.json"
assert not backup.exists() and "execution387StartingState" not in progress
backup.write_bytes(p.read_bytes())
progress["execution387StartingState"] = {
    "execution": 387, "batch": "062", "startingHead": HEAD,
    "startedAt": datetime.now().astimezone().isoformat(),
    "scope": "SAME062 serial dependent visual confirmation in the two original reviewer sessions; reconcile and normally signed local evidence checkpoint only. No teaching edits, accepted Android/native rerun, publication,063 or second runner.",
    "status": "starting-bounded-dependent-visual-confirmation",
    "authorization": {
        "requestSha256": hashlib.sha256(REQUEST.read_bytes()).hexdigest(),
        "characters": len(text), "lines": len(text.splitlines()),
        "completeFileLoadedAndCheckpointParsed": True,
        "limits": "Entire request acquired into memory and complete embedded checkpoint parsed; operative contract, complete final386 native checkpoint and complete approved issue inspected directly. Historical middle acquired and parsed, not freshly semantically re-reviewed.",
    },
    "worktrees": "Dedicated content clean signedGda3a602a; Android clean f9b59a2. Fresh fetch origin/main42f144c7. Runtime teaching unchanged38ab6072.",
    "cliProbe": "copilot --help succeeded. copilot --model help without prompt returned no-prompt error, not a catalog or permission denial; supported copilot help config confirmed original claude-opus-5.5 and gpt-6.1-sol.",
}
p.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Execution387 starting scope persisted; complete live history preserved.")

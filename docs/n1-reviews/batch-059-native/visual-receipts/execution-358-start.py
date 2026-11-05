import hashlib
import json
import subprocess
from datetime import datetime
from pathlib import Path

c = Path(__file__).resolve().parent
r = c.parent / "learning-japanese"
load = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
p = load(c / "progress.json")
assert p["checkpoint"] == 357 and p["batch"] == "059"
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=r, text=True).strip()
assert head == "b4173065b2b78d697e41279777c177a8d92e58c5"
request = c / "logs" / "3a6fa6c0-d831-4aa6-b379-818636ef5dab" / "request.txt"
text = request.read_text(encoding="utf-8-sig")
marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
checkpoint = json.loads(text.split(marker, 1)[1])
assert checkpoint["checkpoint"] == 357
assert not (c / "execution-358-starting-progress.json").exists()
(c / "execution-358-starting-progress.json").write_bytes((c / "progress.json").read_bytes())
p["execution358StartingState"] = {
    "execution": 358, "batch": "059", "startingHead": head,
    "scope": "SAME059 original-session serial dependent native visual confirmation and signed durable checkpoint only. No native/Android rerun, publication,060 or second runner.",
    "status": "preparing-bounded-dependent-visual-review",
    "recordedAt": datetime.now().astimezone().isoformat(),
    "authorization": {
        "requestSha256": sha(request), "characters": len(text), "lines": len(text.splitlines()),
        "completeFileLoadedAndCheckpointParsed": True,
        "limits": "Entire request acquired and complete embedded checkpoint parsed; operative contract, complete final357 checkpoint and approved issue inspected directly. Historical middle acquired and parsed, not freshly semantically re-reviewed.",
    },
}
temporary = c / "progress.execution358.tmp"
temporary.write_text(json.dumps(p, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
temporary.replace(c / "progress.json")
native = r / "docs" / "n1-reviews" / "batch-059-native" / "attempt-1"
groups = {}
for path in sorted(native.glob("*.png")):
    groups.setdefault(sha(path), []).append(path.name)
assert sum(map(len, groups.values())) == 35 and len(groups) == 20
freeze = {
    "schemaVersion": 1, "execution": 358, "snapshot": head,
    "teachingSnapshot": "769293c824dc41abb9386e76c4dd5f8c676e48e0",
    "files": {str(path.relative_to(r)): sha(path) for path in native.iterdir() if path.is_file()},
    "teachingFiles": {name: sha(r / name) for name in ("kanji\\享.md", "kanji\\受.md", "words\\享受.md", "strokes\\享.json", "manifest.json")},
    "originalReports": {name: sha(r / "docs" / "n1-reviews" / name) for name in (
        "batch-059-initial-claude.md", "batch-059-initial-gpt.md",
        "batch-059-confirmation-claude.md", "batch-059-confirmation-claude-serial-followup.md",
        "batch-059-confirmation-gpt.md")},
    "pngGroups": [{"sha256": h, "representative": names[0], "equivalentFiles": names} for h, names in groups.items()],
}
(c / "batch-059-visual-freeze.json").write_text(json.dumps(freeze, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Starting scope persisted preserving full history; 35 PNGs / 20 distinct frozen payloads.")

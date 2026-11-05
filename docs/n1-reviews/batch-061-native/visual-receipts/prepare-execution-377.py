import hashlib
import json
import re
import subprocess
from pathlib import Path
from datetime import datetime

C = Path(__file__).parent
R = C.parent / "learning-japanese"
V = R / "docs" / "n1-reviews"
N = V / "batch-061-native"
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
load = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
assert not subprocess.check_output(
    ["git", "diff", "2567f5e7b3888f2df3ed560f618341266b471902", "--",
     "kanji", "words", "articles", "strokes", "manifest.json"], cwd=R, text=True
).strip()
index = N / "execution-376-artifact-index.json"
for row in load(index)["files"]:
    assert sha(R / row["path"]) == row["sha256"]
raw = (N / "attempt-1" / "instrumentation.txt").read_text(encoding="utf-8-sig")
assert re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)$", raw, re.M) == ["1", "0", "1", "0"]
assert "OK (2 tests)" in raw and "Time: 108.92" in raw
groups = {}
for path in sorted((N / "attempt-1").glob("*.png")):
    groups.setdefault(sha(path), []).append(path.name)
assert len(groups) == 20 and sum(map(len, groups.values())) == 40
task = C / "batch-061-visual-task.txt"
names = re.findall(r"^n1-061-[\w-]+\.png$", task.read_text(encoding="utf-8"), re.M)
assert len(names) == 20
assert {sha(N / "attempt-1" / name) for name in names} == set(groups)
paths = [
    V / "batch-061-initial-claude.md", V / "batch-061-initial-gpt.md",
    V / "batch-061-initial-review-checkpoint.json", V / "batch-061-reconciliation.json",
    V / "batch-061-dependent-claude-turn-4.md", index, task,
]
paths.extend(R / p for p in ("kanji\\俳.md", "words\\俳句.md", "words\\俳優.md", "kanji\\優.md"))
record = {
    "execution": 377, "batch": "061", "snapshot": "f2267727d982589890b2f4ae0b17e82666337956",
    "teachingSnapshot": "2567f5e7b3888f2df3ed560f618341266b471902",
    "recordedAt": datetime.now().astimezone().isoformat(),
    "artifactIndexSha256": sha(index),
    "nativeArtifactHashesVerified": len(load(index)["files"]),
    "sourcePngCount": 40, "distinctPngCount": 20,
    "pngGroups": [{"sha256": key, "equivalentNames": value} for key, value in groups.items()],
    "files": [{"path": str(path), "sha256": sha(path)} for path in paths],
    "runtimeUnchanged": True, "nativeRerun": False, "androidRerun": False,
    "catalogProbeNote": "copilot --model help without prompt returned no-prompt/exit1, not catalog. Actual copilot help config and --help were captured successfully; actual selected models are listed.",
}
target = C / "batch-061-visual-freeze.json"
assert not target.exists()
target.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Frozen unchanged runtime and twenty distinct images; native2case0 reverified without rerun.")

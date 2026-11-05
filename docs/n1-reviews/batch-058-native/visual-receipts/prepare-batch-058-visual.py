import hashlib
import json
import subprocess
from pathlib import Path

c = Path(__file__).resolve().parent
r = c.parent / "learning-japanese"
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
load = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=r, text=True).strip() == "9468bac2169909be53ef87bda5cffdbb79646040"
assert not subprocess.check_output(["git", "diff", "58b53fd31b6d55baba32c049fba62ac739feb004", "--", "kanji", "words", "articles", "strokes", "manifest.json"], cwd=r)
index = r / "docs/n1-reviews/batch-058-native/execution-347-artifact-index.json"
for row in load(index)["files"]:
    assert sha(r / row["path"]) == row["sha256"]
groups = {}
for p in sorted((index.parent / "attempt-1").glob("*.png")):
    groups.setdefault(sha(p), []).append(p.name)
assert sum(map(len, groups.values())) == 43 and len(groups) == 25
files = ["kanji/丘.md", "words/砂丘.md", "words/丘.md", "kanji/砂.md", "kanji/山.md", "manifest.json", "strokes/丘.json"]
freeze = {
    "schemaVersion": 1, "execution": 348, "batch": "058",
    "snapshot": "9468bac2169909be53ef87bda5cffdbb79646040",
    "teachingSnapshot": "58b53fd31b6d55baba32c049fba62ac739feb004",
    "files": {f: sha(r / f) for f in files},
    "originalReports": {p.name: sha(p) for p in (r / "docs/n1-reviews").glob("batch-058-*.md")},
    "nativeArtifactIndex": str(index.relative_to(r)),
    "nativeArtifactIndexSha256": sha(index),
    "sourcePngCount": 43, "distinctSourcePngCount": 25, "pngHashGroups": groups,
    "sharedTaskSha256": sha(c / "batch-058-visual-task.txt"),
    "limits": "Byte consistency and fresh Git checks, not comprehension. Dependent original-session visual review; initial process history unchanged.",
}
dest = c / "batch-058-visual-freeze.json"
assert not dest.exists()
dest.write_text(json.dumps(freeze, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Frozen unchanged teaching, all 55 native artifacts, 43 source PNGs / 25 distinct viewports.")

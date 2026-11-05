import hashlib
import json
import shutil
import subprocess
from pathlib import Path

c = Path(__file__).parent
r = c.parent / "learning-japanese"
v = r / "docs" / "n1-reviews"
digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
load = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
assert load(c / "progress.json")["checkpoint"] == 407
assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=r, text=True).strip() == "e2c49895daee2bbf0019388c0333e3d0e245fd4a"
assert not subprocess.check_output(["git", "diff", "ff6eb7893344b806bf517ebd41bf19089bed5021", "--",
                                    "kanji", "words", "articles", "strokes", "manifest.json"], cwd=r)
index = v / "batch-064-native" / "execution-406-artifact-index.json"
assert digest(index) == "83638bf17311ae74742ab9f2a12e4c95cb5938d9035f7767ac0531dc9af4bc8d"
for row in load(index)["files"]:
    path = r / row["path"]
    assert digest(path) == row["sha256"] and path.stat().st_size == row["bytes"], row["path"]
task = c / "batch-064-visual-task.txt"
for family in ("claude", "gpt"):
    target = c / f"batch-064-visual-{family}-prompt.txt"
    assert not target.exists()
    target.write_text(
        task.read_text(encoding="utf-8") +
        f"\nRead the complete shared task itself with view: {task}\n"
        f"Read YOUR complete original report: {v / f'batch-064-initial-{family}.md'}\n"
        f"Read YOUR complete textual confirmation: {v / f'batch-064-confirmation-{family}.md'}\n",
        encoding="utf-8")
freeze = {
    "schemaVersion": 1, "execution": 408, "batch": "064",
    "evidenceHead": "e2c49895daee2bbf0019388c0333e3d0e245fd4a",
    "teachingSnapshot": "ff6eb7893344b806bf517ebd41bf19089bed5021",
    "nativeArtifactIndexSha256": digest(index),
    "verifiedIndexedArtifacts": 68,
    "sharedTaskSha256": digest(task),
    "teachingHashes": {str(p.relative_to(r)): digest(p) for p in [
        r / "kanji" / "偵.md", r / "words" / "探偵.md",
        r / "kanji" / "探.md", r / "words" / "刑事.md", r / "manifest.json"]},
    "originalReportHashes": {str(p.relative_to(r)): digest(p) for p in [
        v / f"batch-064-{kind}-{family}.md"
        for kind in ("initial", "confirmation") for family in ("claude", "gpt")]},
}
target = c / "batch-064-visual-freeze.json"
assert not target.exists()
target.write_text(json.dumps(freeze, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
catalog = v / "batch-064-copilot-model-catalog-execution-408.txt"
assert not catalog.exists()
shutil.copyfile(Path(r"C:\Users\stop-\AppData\Local\Temp\1793868222914-copilot-tool-output-25880-35c2d554-48be-4d23-bfa9-73114f325eb1.txt"), catalog)
print("Verified68indexed artifacts; frozen unchanged teaching and all4original reports; two own-report prompts prepared.")

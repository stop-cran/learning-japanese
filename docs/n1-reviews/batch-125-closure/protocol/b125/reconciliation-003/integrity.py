import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

repo = Path(os.environ["N1_REPO"])
root = repo.parent
parent = "dbca5192a4308dc6e8d954af37775e0fcd1986ea"
def git(*args):
    return subprocess.check_output(["git", "-c", "core.quotepath=false", *args], cwd=repo)
def digest(b):
    return hashlib.sha256(b).hexdigest()
def fields(data):
    text = data.decode("utf-8").replace("\r\n", "\n")
    front = text.split("---", 2)[1]
    result = {}
    for key in ("quiz_exclusions", "distractors", "onyomi", "kunyomi", "quizOnyomi", "quizKunyomi"):
        match = re.search(rf"^{key}:\s*\[([^\]]*)\]\s*$", front, re.M)
        result[key] = [v.strip() for v in match.group(1).split(",") if v.strip()] if match else []
    return result
before = fields(git("show", f"{parent}:kanji/侵.md"))
after = fields((repo / "kanji" / "侵.md").read_bytes())
for key in ("distractors", "onyomi", "kunyomi", "quizOnyomi", "quizKunyomi"):
    assert before[key] == after[key], key
assert len(before["quiz_exclusions"]) == 21
assert after["quiz_exclusions"] == before["quiz_exclusions"] + ["低", "短", "小", "容"]
for path in ("words/侵入.md", "strokes/侵.json"):
    assert git("show", f"{parent}:{path}") == (repo / path).read_bytes(), path
old = json.loads(git("show", f"{parent}:manifest.json"))
new = json.loads((repo / "manifest.json").read_bytes())
old_paths = {path: value for v in old.values() if isinstance(v, dict) for path, value in v.items()}
new_paths = {path: value for v in new.values() if isinstance(v, dict) for path, value in v.items()}
assert set(old_paths) == set(new_paths)
changed = {p for p in old_paths if old_paths[p] != new_paths[p]}
assert changed == {"kanji/侵.md"}, changed
assert digest((repo / "kanji" / "侵.md").read_bytes().replace(b"\r\n", b"\n")) == new_paths["kanji/侵.md"]
packet = repo / "docs" / "n1-sources" / "batch-125-reconciliation-003"
prior = repo / "docs" / "n1-sources" / "batch-125-reconciliation-002"
receipt = json.loads((packet / "source-receipt.json").read_text(encoding="utf-8"))
assert digest((prior / "source-receipt.json").read_bytes()) == receipt["priorSourceReceiptSha256"]
assert digest((prior / "dispositions.json").read_bytes()) == receipt["priorDispositionSha256"]
for name in ("kanjidic2-records.xml", "jmdict-records.xml"):
    assert digest((packet / name).read_bytes()) == receipt["selectedRecords"][name]
assert digest((root / "scratch-125" / "reconciliation-003-sources-001" / "source-receipt.json").read_bytes()) == receipt["selectedRecords"]["selectorReceiptSha256"]
assert digest((root / "scratch-125" / "reconciliation-003-reading-001" / "reading.log").read_bytes()) == receipt["readingModelLogSha256"]
assert digest((root / "scratch-125" / "reconciliation-003-author-gates-001" / "quiz-safety.log").read_bytes()) == receipt["meaningModelLogSha256"]
assert digest((root / "scratch-125" / "reconciliation-002-source-captures-001" / "shin.html").read_bytes()) == receipt["kanjiPedia"]["localCaptureSha256"]
inventory_path = root / receipt["parentInventory"]["localPath"]
assert digest(inventory_path.read_bytes()) == receipt["parentInventory"]["sha256"]
inventory = json.loads(inventory_path.read_bytes())
assert inventory["parent"] == parent and len(inventory["cards"]) == inventory["count"] == receipt["parentInventory"]["cards"]
for item in inventory["cards"]:
    assert digest(git("show", f"{parent}:kanji/{item['kanji']}.md")) == item["sha256"]
prior_dispositions = json.loads((prior / "dispositions.json").read_text(encoding="utf-8"))
rows = prior_dispositions["unchanged"] + prior_dispositions["revisions"]
expected_ids = {f"Q{i}" for i in range(1, 14)} | {"F1-討", "F1-痛"}
assert len(rows) == 15 and {r["id"] for r in rows} == expected_ids
for row in rows:
    assert row["status"] == "direct_guard" and row["other"] in after["quiz_exclusions"]
for other in ("低", "短", "小", "容"):
    assert "侵" not in fields(git("show", f"{parent}:kanji/{other}.md"))["quiz_exclusions"]
claude = (packet / "claude-response-003.md").read_text(encoding="utf-8")
gpt = (packet / "gpt-response-003.md").read_text(encoding="utf-8")
assert "GPT" not in claude and "UNVERIFIED" not in claude and "Claude" not in gpt
assert digest((root / "reports-125" / "N1-B125-CLAUDE-CONFIRM-001.md").read_bytes()) == "ce0cbf16a6b0c4248faedbe5df78f119296ca49cb055606ff5950602883c7679"
assert digest((root / "reports-125" / "N1-B125-GPT-CONFIRM-001.md").read_bytes()) == "0415392277549cc1f6a0592b6f2047ae659d6bb6ea370dd78d39206efa3e856d"
expected = {
    "kanji/侵.md", "manifest.json", "docs/n1-sources/batch-125-progress-004.json",
    "docs/n1-sources/batch-125/selection-004.json", "docs/n1-sources/batch-125/author-audit-004.md",
    *(f"docs/n1-sources/batch-125-reconciliation-003/{name}" for name in (
        "source-receipt.json", "disposition.md", "claude-response-003.md", "gpt-response-003.md", "kanjidic2-records.xml", "jmdict-records.xml")),
}
head = git("rev-parse", "HEAD").decode().strip()
if head == parent:
    paths = set(git("diff", "--name-only", parent).decode().splitlines()) | set(git("ls-files", "--others", "--exclude-standard").decode().splitlines())
else:
    assert git("rev-parse", "HEAD^@").decode().split() == [parent]
    assert not git("status", "--porcelain=v1", "--untracked-files=all")
    paths = set(git("diff", "--name-only", parent, "HEAD").decode().splitlines())
assert paths == expected, (paths, expected)
print(json.dumps({"parent": parent, "head": head, "changedFiles": sorted(paths), "baselineRuntimeCount": len(old_paths), "runtimeChangedSinceParent": sorted(changed), "wordAndStrokeByteIdenticalToParent": True, "previousTrackedArtifactsUnchanged": True, "parentInventoryCardsVerified": len(inventory["cards"]), "priorDispositionIds": sorted(expected_ids), "additionalGuards": ["低", "短", "小", "容"], "manifestSha256": digest((repo / "manifest.json").read_bytes()), "contentVersion": new["contentVersion"]}, ensure_ascii=False))

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

root = Path(r"C:\Users\stop-\n1-kanji-workspace")
repo = root / "b125-worktree"
assert os.environ["N1_REPO"] == str(repo)
assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo).decode().strip() == "dbca5192a4308dc6e8d954af37775e0fcd1986ea"
sys.path.insert(0, str(root / "lean"))
from n1lib import parse, read
import reading_options as ro

rows = []
for p in sorted((repo / "kanji").glob("*.md")):
    fm, _ = parse(read(p))
    if not fm:
        raise ValueError(f"Missing front matter: {p}")
    rows.append({
        "kanji": p.stem,
        "title": fm["title"],
        "onyomi": fm.get("onyomi", []),
        "kunyomi": fm.get("kunyomi", []),
        "quizOnyomi": fm.get("quizOnyomi"),
        "quizKunyomi": fm.get("quizKunyomi"),
        "tags": fm.get("tags", []),
        "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
    })
assert len({r["kanji"] for r in rows}) == len(rows)
assert next(r for r in rows if r["kanji"] == "侵")["title"] == "invade; encroach"
result = {
    "schemaVersion": 1,
    "parent": "dbca5192a4308dc6e8d954af37775e0fcd1986ea",
    "scope": "Every kanji/*.md at parent. Null quiz lists mean the explicit key is absent; the bounded reading model falls back to the corresponding metadata list.",
    "count": len(rows),
    "cards": rows,
}
out = Path(sys.argv[1])
out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
terms = ("ugly", "unattractive", "shabby", "appearance", "appear", "beaut", "look", "face", "short", "small", "little", "poor", "low", "mean", "plain", "deform", "unseem", "homely", "hideous", "unsightly", "dirty", "filth", "dirt", "squal", "wretched", "miser", "inferior", "unsight", "醜", "みにく")
matches = [(r["kanji"], r["title"]) for r in rows if any(t in r["title"].lower() for t in terms)]
offered = {}
raw_matches = {}
for kind, base, practice in (("on", "onyomi", "quizOnyomi"), ("kun", "kunyomi", "quizKunyomi")):
    offered[kind] = [(r["kanji"], x) for r in rows for x in (r[practice] if r[practice] is not None else r[base]) if ro.key(x) == "みにくい"]
    raw_matches[kind] = [(r["kanji"], x) for r in rows for x in r[base] if ro.key(x) == "みにくい"]
print(json.dumps({"count": len(rows), "inventoryPath": str(out), "sha256": hashlib.sha256(out.read_bytes()).hexdigest(), "literalTitleCandidates": matches, "readingKey": "みにくい", "practiceOffered": offered, "metadataMatches": raw_matches, "terms": terms}, ensure_ascii=False, indent=2))

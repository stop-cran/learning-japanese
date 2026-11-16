import json
import re
from collections import defaultdict
from b128_common import BASE, HERE, REPO, git, start_guard, write

guard = start_guard()
try:
    assert git("rev-parse", "HEAD").decode().strip() == BASE
    assert not git("status", "--porcelain=v1", "--untracked-files=all")
    assert git("remote", "get-url", "origin").decode().strip() == "https://github.com/stop-cran/learning-japanese.git"
    index = json.loads((REPO / "docs/n1-sources/source-index.json").read_text(encoding="utf-8"))
    cards = {p.stem for p in (REPO / "kanji").glob("*.md")}
    support = defaultdict(list)
    for path in (REPO / "words").glob("*.md"):
        guard.check()
        text = path.read_text(encoding="utf-8")
        match = re.search(r"^kanji: \[([^\]]*)\]", text, re.M)
        if match:
            for char in match.group(1).split(","):
                support[char.strip()].append(path.stem)
    rows = []
    for row in index:
        char, meta = row["kanji"], row["metadata"]
        if row["statusAtFreeze"] == "pending" and char not in cards and len(meta["onyomi"]) == 1 and not meta["kunyomi"] and 0 < len(support[char]) <= 2:
            rows.append({"row": row["sourceRow"], "kanji": char, "onyomi": meta["onyomi"], "meanings": meta["meanings"], "words": support[char]})
    write(HERE / "candidate-survey-001.json", {"base": BASE, "rows": rows})
    print(json.dumps(rows, ensure_ascii=False, indent=2))
finally:
    write(HERE / "survey-memory-001.json", guard.finish())

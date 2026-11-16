import json
from collections import defaultdict
from b126_common import BASE, HERE, REPO, git, start_guard, write

guard = start_guard()
try:
    assert git("rev-parse", "HEAD").decode().strip() == BASE
    assert not git("status", "--porcelain")
    index = json.loads((REPO / "docs" / "n1-sources" / "source-index.json").read_text(encoding="utf-8"))
    cards = {p.stem for p in (REPO / "kanji").glob("*.md")}
    support = defaultdict(list)
    for path in (REPO / "words").glob("*.md"):
        guard.check()
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("kanji: ["):
                for ch in line.split("[", 1)[1].split("]", 1)[0].split(","):
                    support[ch.strip()].append(path.stem)
                break
    rows = []
    for row in index:
        ch, meta = row["kanji"], row["metadata"]
        if row["statusAtFreeze"] == "pending" and ch not in cards and len(meta["onyomi"]) == 1 and not meta["kunyomi"] and 0 < len(support[ch]) <= 2:
            rows.append({"row": row["sourceRow"], "kanji": ch, "metadata": meta, "words": support[ch]})
    write(HERE / "candidate-inventory-001.json", rows)
    print(json.dumps(rows, ensure_ascii=False, indent=2))
finally:
    write(HERE / "candidate-inventory-memory-001.json", guard.finish())

import json
from b126_common import HERE, REPO, start_guard, write

guard = start_guard()
try:
    rows = json.loads((REPO / "docs" / "n1-sources" / "source-index.json").read_text(encoding="utf-8"))
    missing = {r["kanji"]: r for r in rows if r["statusAtFreeze"] == "pending" and not (REPO / r["article"]).exists()}
    support = {ch: [] for ch in missing}
    for path in (REPO / "words").glob("*.md"):
        guard.check()
        text = path.read_text(encoding="utf-8")
        for line in text.splitlines():
            if line.startswith("kanji: ["):
                for ch in line.split("[", 1)[1].split("]", 1)[0].split(","):
                    if ch.strip() in support:
                        support[ch.strip()].append(path.stem)
                break
    result = [
        {"kanji": ch, "row": r["sourceRow"], "on": r["metadata"]["onyomi"], "kun": r["metadata"]["kunyomi"], "meanings": r["metadata"]["meanings"], "words": support[ch]}
        for ch, r in missing.items() if 0 < len(support[ch]) <= 2
    ]
    write(HERE / "broader-inventory-001.json", result)
    for row in result:
        print(json.dumps(row, ensure_ascii=False))
finally:
    write(HERE / "broader-inventory-memory-001.json", guard.finish())

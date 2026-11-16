import json
from b130_common import HERE, write

for path in sorted(HERE.glob("semantic-readback-*.jsonl")):
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        row = f'{r["kanji"]} | {r["title"]}\n{r["actualMeaning"]}\nNOTES: {r["actualNotes"]}\n'
        for fam in r["completeExactSpellingFamilySemantics"]:
            row += f'{fam["id"]} '
            row += json.dumps({key: [{k: v for k, v in el.items() if v} for el in fam[key]] for key in ("k", "r")}, ensure_ascii=False, separators=(",", ":"))
            row += "\n"
            for sense in fam["s"]:
                row += json.dumps({k: v for k, v in sense.items() if v}, ensure_ascii=False, separators=(",", ":")) + "\n"
        rows.append(row)
    for i in range(0, len(rows), 4):
        write(HERE / f"compact-{path.stem[-2:]}-{i//4+1}.txt", "\n".join(rows[i:i+4]).encode())

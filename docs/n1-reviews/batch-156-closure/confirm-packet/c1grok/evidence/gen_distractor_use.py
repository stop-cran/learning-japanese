"""Generate distractor-use.tsv and distractor-senses.txt for the B156 confirm packet.

Run from the lean directory: python -X utf8 gen_distractor_use.py <repo> <outdir>
"""
import pathlib
import re
import subprocess
import sys

sys.path.insert(0, ".")
import n1lib  # noqa: E402

repo = pathlib.Path(sys.argv[1])
out = pathlib.Path(sys.argv[2])
BATCH = "丹乙亜仁仙伎伏伐伯伴"
NEW = "王硬粗下供生食自起座伸保耕育迎離他"
REJECTED = {
    "末": "乙 (draft before 2c206d8f, never in a commit on this branch): sense \"youngest child\" matches the 児 exclusion (乙子 おとご)",
    "初": "乙 (considered, never committed): reading うぶ \"inexperienced; green\" is close to the 稚 and 幼 exclusions",
    "父": "仙 (in 7eaf5c24): sense \"God; Father\" is close to the 神 exclusion (godlike being)",
    "敵": "伴 (draft before 2c206d8f, never in a commit on this branch): reading かたき, archaic sense \"spouse\", is close to 伴 \"consort\" and 伴侶 \"spouse\"",
    "達": "伎 (in 7eaf5c24): the 達 card teaches \"attain skill\" (上達), the reason 伎 excludes 熟",
    "行": "伎 (in 7eaf5c24): no sense clash found (JMdict 行 こう sense 2 is \"act; action\", a deed); replaced by 供 so that the set holds a 亻 card, as one initial review suggested",
}

sha = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()


def front_matter(path):
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    data = {}
    for line in m.group(1).split("\n"):
        key, _, value = line.partition(":")
        data[key.strip()] = value.strip()
    return data


def as_list(value):
    value = (value or "").strip()
    if not value.startswith("["):
        return []
    return [x.strip() for x in value[1:-1].split(",") if x.strip()]


cards = {p.stem: front_matter(p) for p in (repo / "kanji").glob("*.md")}
users = {}
for name, data in cards.items():
    for d in as_list(data.get("distractors")):
        users.setdefault(d, []).append(name)


def is_n1(name):
    return "jlpt-n1" in as_list(cards[name].get("tags"))


lines = [
    "# Curated meaning distractors in the revision: the distractor card's own front matter and every card that lists it",
    f"# generated from kanji\\*.md at {sha} ({len(cards)} kanji cards); 'starter' = the card carries the starter tag (the Starter stack); N1 users = users tagged jlpt-n1",
    "# columns: distractor, title, jlpt, starter, radicalNumber, onyomi, kunyomi, used by (all cards), count all/N1, used by batch cards",
]
for d in NEW:
    data = cards[d]
    us = sorted(users.get(d, []))
    lines.append("\t".join([
        d,
        data.get("title", ""),
        data.get("jlpt", ""),
        "starter" if "starter" in as_list(data.get("tags")) else "-",
        data.get("radicalNumber", ""),
        " ".join(as_list(data.get("onyomi"))),
        " ".join(as_list(data.get("kunyomi"))),
        " ".join(us),
        f"{len(us)}/{sum(1 for u in us if is_n1(u))}",
        " ".join(u for u in us if u in BATCH),
    ]))
lines += ["", f"# Batch cards: curated distractors at {sha[:8]}"]
for k in BATCH:
    lines.append(f"{k}\t{cards[k].get('title', '')}\tdistractors {' '.join(as_list(cards[k].get('distractors')))}")
lines += ["", "# Distractor candidates replaced or rejected during the fix (not in the revision)"]
for d, why in REJECTED.items():
    lines.append(f"{d}\t{cards[d].get('title', '')}\t{why}")
(out / "distractor-use.tsv").write_text("\n".join(lines) + "\n", encoding="utf-8")

jm = n1lib.build_jmdict_cache()["entries"]
single = {}
for eid, entry in jm.items():
    for k in entry["k"]:
        if len(k[0]) == 1:
            single.setdefault(k[0], []).append(eid)
senses = [
    "# JMdict entries whose kanji spelling is the single distractor character, for every new and rejected distractor",
    f"# repo {sha}; JMdict from the lean cache; sense numbers are JMdict order; [stagr]/[misc] shown when present",
]
for d in list(NEW) + list(REJECTED):
    tag = "replaced or rejected" if d in REJECTED else "in revision"
    senses.append(f"===== {d} ({cards[d].get('title', '')}; {tag})")
    ids = single.get(d, [])
    if not ids:
        senses.append("   (no JMdict entry spelled with this character alone)")
    for eid in sorted(ids, key=int):
        entry = jm[eid]
        senses.append(f"   {eid} {[k[0] for k in entry['k']]} {[r[0] for r in entry['r']]}")
        for n, s in enumerate(entry["s"], 1):
            extra = ""
            if s.get("stagr"):
                extra += f" [stagr {s['stagr']}]"
            if s.get("misc"):
                extra += f" [misc {s['misc']}]"
            senses.append(f"      {n} {'; '.join(s['gloss'])}{extra}")
(out / "distractor-senses.txt").write_text("\n".join(senses) + "\n", encoding="utf-8")
print("wrote", out / "distractor-use.tsv", out / "distractor-senses.txt")

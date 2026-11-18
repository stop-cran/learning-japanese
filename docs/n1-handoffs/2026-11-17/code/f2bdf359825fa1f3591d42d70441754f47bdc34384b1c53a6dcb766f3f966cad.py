# -*- coding: utf-8 -*-
import sys
from collections import Counter
sys.path.insert(0, r"C:\Users\stop-\n1-kanji-workspace\lean")
from n1lib import *

kc, wc = load_cards()
idx = source_index()
n1 = {k: v for k, v in kc.items() if v[0] and "jlpt-n1" in v[0].get("tags", [])}
print("kanji cards", len(kc), "jlpt-n1 tagged", len(n1))
src_n1 = [k for k in n1 if k in idx]
print("in source index", len(src_n1), "not in source", [k for k in n1 if k not in idx])
tagpat = Counter()
keypat = Counter()
jl = Counter()
for k, (fm, body) in n1.items():
    tags = fm["tags"]
    tagpat[tuple(t if not t.startswith("grade-") else "grade-*" for t in tags)] += 1
    keypat[tuple(fm.keys())] += 1
    jl[fm.get("jlpt")] += 1
print("tags:", dict(tagpat))
for kp, n in keypat.items():
    print(n, kp)
print("jlpt", dict(jl))
# grade None cases
nog = [k for k in src_n1 if idx[k]["metadata"].get("grade") in (None, "")]
print("source rows with no grade:", len(nog), nog[:10])
for k in nog[:5]:
    if k in kc:
        print(k, kc[k][0]["tags"])
# distinct sections
secs = Counter()
for k, (fm, body) in n1.items():
    secs[tuple(sections(body).keys())] += 1
print("section patterns:", dict(secs))
# facts line
facts = Counter()
for k, (fm, body) in n1.items():
    for line in body.split("\n"):
        if line.startswith("**Strokes:**"):
            facts[re.sub(r"\d+", "#", re.sub(r"\(no\. \d+[^)]*\)", "(no. #)", line))[:60]] += 1
            break
print("facts lines:", facts.most_common(8))

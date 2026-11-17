# -*- coding: utf-8 -*-
import sys, subprocess
from collections import Counter
sys.path.insert(0, r"C:\Users\stop-\n1-kanji-workspace\lean")
from n1lib import *

kc, wc = load_cards()
idx = source_index()
main_cards = set(git("ls-tree", "--name-only", "origin/main", "kanji/").split("\n"))
main_cards = {Path(p).stem for p in main_cards if p.endswith(".md")}
print("cards on origin/main:", len(main_cards), "cards in tree:", len(kc))
status = Counter()
rows = []
for k, r in idx.items():
    st = r["statusAtFreeze"]
    has_main = k in main_cards
    has_tree = k in kc
    lvl = kc[k][0].get("jlpt") if has_tree and kc[k][0] else None
    tags = [t for t in (kc[k][0].get("tags", []) if has_tree and kc[k][0] else []) if t.startswith("jlpt-")]
    status[(st, has_main, has_tree, lvl)] += 1
for key, n in sorted(status.items(), key=lambda x: str(x[0])):
    print(n, key)
pending = [k for k, r in idx.items() if r["statusAtFreeze"] == "pending"]
done_main = [k for k in pending if k in main_cards]
print("pending:", len(pending), "with card on main:", len(done_main))
print("pending with card in tree but not main:", [k for k in pending if k in kc and k not in main_cards])
nlvl = Counter(kc[k][0].get("jlpt") for k in done_main)
print("levels among done:", dict(nlvl))
print("non-N1 done:", [k for k in done_main if kc[k][0].get("jlpt") != "1"])
print("N1 tagged cards on main not in pending:", [k for k, (fm, b) in kc.items() if k in main_cards and fm and "jlpt-n1" in fm.get("tags", []) and k not in pending])
first_missing = [(r["sourceRow"], k) for k, r in idx.items() if r["statusAtFreeze"] == "pending" and k not in kc]
first_missing.sort()
print("next missing rows:", first_missing[:25])
print("total remaining (not in tree):", len(first_missing))

# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r"C:\Users\stop-\n1-kanji-workspace\lean")
from n1lib import *
kc, wc = load_cards()
idx = source_index()
rows_done = sorted(r["sourceRow"] for k, r in idx.items() if r["statusAtFreeze"] == "pending" and k in kc)
rows_all = sorted(r["sourceRow"] for k, r in idx.items() if r["statusAtFreeze"] == "pending")
print("done rows:", rows_done)
print("pending rows min/max:", rows_all[0], rows_all[-1], len(rows_all))
# batch assignment at freeze
from collections import Counter
b = Counter(r["assignedBatchAtFreeze"] for r in idx.values())
print("assignedBatchAtFreeze distribution (first 20):", sorted(b.items(), key=lambda x: str(x[0]))[:20])
sample = [(r["sourceRow"], k, r["assignedBatchAtFreeze"]) for k, r in idx.items()][:12]
print(sample)

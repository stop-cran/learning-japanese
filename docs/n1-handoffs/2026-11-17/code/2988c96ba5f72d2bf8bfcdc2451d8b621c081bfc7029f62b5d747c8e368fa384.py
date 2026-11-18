"""Which KANJIDIC2 readings of still-absent N1 kanji are already exemplified by existing word cards?"""
import sys
sys.path.insert(0, r"C:\Users\stop-\n1-kanji-workspace\lean")
import n1lib
from collections import defaultdict

kc, wc = n1lib.load_cards()
kd = n1lib.build_kanjidic_cache()["chars"]
si = n1lib.source_index()
absent = [k for k, r in si.items() if r["statusAtFreeze"] == "pending" and k not in kc]
decl = defaultdict(list)
for w, (fm, body) in wc.items():
    if not fm:
        continue
    for k in fm.get("kanji", []):
        decl[k].append(w)

rows = []
for k in absent:
    d = kd.get(k)
    if not d:
        continue
    words = decl.get(k, [])
    cov = defaultdict(set)
    for w in words:
        fm = wc[w][0]
        written = fm.get("word", w)
        reading = fm.get("reading", "")
        segs = n1lib.align(kd, written, reading)
        if not segs:
            continue
        per = None
        for seg in segs:
            labs = {lab for ch, s, lab in seg if ch == k}
            per = labs if per is None else (per & labs)
        for lab in per or ():
            cov[lab].add(w)
    on_all = ["on:" + o for o in d["on"]]
    kun_all = ["kun:" + o for o in d["kun"]]
    on_missing = [x for x in on_all if x not in cov]
    kun_missing = [x for x in kun_all if x not in cov]
    rows.append((si[k]["sourceRow"], k, d["grade"], d["strokes"], len(words),
                 len(on_all) - len(on_missing), len(on_all), len(kun_all) - len(kun_missing), len(kun_all),
                 [x[4:] for x in on_missing], [x[4:] for x in kun_missing], sorted({w for s in cov.values() for w in s})))

mode = sys.argv[1] if len(sys.argv) > 1 else "good"
n = 0
for r in sorted(rows):
    row, k, g, st, nw, onc, ont, kc_, kt, onm, kunm, ws = r
    if nw == 0:
        continue
    onlykun_ok = (kt == 0 or kc_ >= 1)
    on_ok = onc >= 1
    if mode == "good" and not (on_ok and onlykun_ok):
        continue
    n += 1
    print(f"{row:4d} {k} g{g} {st}s decl={nw} on {onc}/{ont} kun {kc_}/{kt} | miss on={','.join(onm)} kun={','.join(kunm)} | {' '.join(ws)}")
print("count", n)

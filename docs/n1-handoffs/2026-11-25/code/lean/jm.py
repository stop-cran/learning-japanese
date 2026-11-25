"""Quick JMdict lookup against the pinned compact cache.

usage: python jm.py WORD [WORD ...]     exact writing or reading matches
       python jm.py --chars 摩 擦        entries whose writings contain ALL given chars (top by priority)
       set JM_ALL=1 to print every sense and gloss (default: 6 senses, 6 glosses each)
"""
import os
import sys
sys.path.insert(0, r"C:\Users\romanko\n1-kanji-workspace\lean")
import n1lib

D = n1lib.build_jmdict_cache()
E = D["entries"]
CI = D["char_index"]
try:
    import jm_extra
    X = jm_extra.build()["entries"]
except Exception as ex:  # sense details are optional
    print("(sense details unavailable:", ex, ")", file=sys.stderr)
    X = {}


def sense_extra(eid, i):
    senses = X.get(eid) or []
    if i >= len(senses):
        return ""
    d = senses[i]
    parts = []
    for k, label in (("dial", "dialect"), ("field", "field"), ("s_inf", "note"), ("xref", "see also"), ("lsource", "from")):
        if d.get(k):
            parts.append(label + ": " + "; ".join(d[k]))
    return (" [" + " | ".join(parts) + "]") if parts else ""


def fmt(eid, e, maxs=6):
    full = os.environ.get("JM_ALL") == "1"  # JM_ALL=1 prints every sense and gloss
    if full:
        maxs = 10 ** 6
    ks = ", ".join(k[0] + ("[" + "/".join(k[1]) + "]" if k[1] else "") + ("{" + "/".join(k[2]) + "}" if k[2] else "")
                   for k in e["k"]) or "-"
    rs = ", ".join(r[0] + ("[" + "/".join(r[1]) + "]" if r[1] else "") + ("<restr:" + "/".join(r[2]) + ">" if r[2] else "")
                   + ("{" + "/".join(r[4]) + "}" if r[4] else "") for r in e["r"])
    print(f"{eid}  K: {ks}  R: {rs}")
    for i, s in enumerate(e["s"][:maxs], 1):
        extra = ""
        if s["stagk"]:
            extra += " stagk=" + "/".join(s["stagk"])
        if s["stagr"]:
            extra += " stagr=" + "/".join(s["stagr"])
        misc = ("/".join(s["misc"]) + " ") if s["misc"] else ""
        print(f"   {i}. ({','.join(p[:24] for p in s['pos'][:3])}) {misc}{'; '.join(s['gloss'] if full else s['gloss'][:6])}{extra}{sense_extra(eid, i - 1)}")
    if len(e["s"]) > maxs:
        print(f"   ... {len(e['s']) - maxs} more senses")


def by_word(w):
    hits = []
    cjk = [c for c in w if n1lib.CJK.match(c)]
    if cjk:
        pool = CI.get(cjk[0], [])
    else:
        pool = E.keys()
    for eid in pool:
        e = E[eid]
        if any(k[0] == w for k in e["k"]) or any(r[0] == w for r in e["r"]):
            hits.append(eid)
    return hits


def by_chars(chars, top=25):
    pool = None
    for c in chars:
        s = set(CI.get(c, []))
        pool = s if pool is None else pool & s
    ranked = sorted(pool or [], key=lambda i: -(sum(n1lib.pri_score(k[1]) for k in E[i]["k"])))
    return ranked[:top]


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--chars":
        for eid in by_chars(args[1:]):
            fmt(eid, E[eid], 3)
    else:
        for w in args:
            print("=" * 8, w)
            hits = by_word(w)
            if not hits:
                print("  (no entry)")
            for eid in hits:
                fmt(eid, E[eid])

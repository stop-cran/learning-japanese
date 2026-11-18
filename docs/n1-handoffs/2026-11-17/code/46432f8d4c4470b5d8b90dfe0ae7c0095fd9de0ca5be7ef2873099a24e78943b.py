# -*- coding: utf-8 -*-
"""Plan and verify the one-line word->kanji link edits that new kanji cards require (read-only).

usage: python n1_linkplan.py plan K [K ...]            suggested unique old/new snippets per declared word
       python n1_linkplan.py verify BASE [--remarks FILE] K [K ...]
                                                       working tree vs BASE: only link wrapping, exactly the expected pairs;
                                                       --remarks FILE is a JSON list of {"file","old","new"} stale-remark
                                                       edits that may additionally differ, each applying exactly once
"""
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, r"C:\Users\stop-\n1-kanji-workspace\lean")
import n1lib

FM = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.S)
LINKSPAN = re.compile(r"\[[^\]\n]*\]\([^)\n]*\)")
WRAPPED = re.compile(r"\[(.)\]\(\.\./kanji/\1\.md\)")


def declared(ch):
    out = []
    for p in sorted((n1lib.REPO / "words").glob("*.md")):
        t = p.read_bytes().decode("utf-8")
        m = FM.match(t)
        if not m:
            continue
        km = re.search(r"^kanji:\s*\[(.*?)\]", m.group(1), re.M)
        if km and ch in [x.strip() for x in km.group(1).split(",")]:
            out.append(p)
    return out


def standalone(s, i):
    prev_c = s[i - 1] if i else " "
    next_c = s[i + 1] if i + 1 < len(s) else " "
    return not n1lib.CJK.match(prev_c) and not n1lib.CJK.match(next_c)


def candidates(t, ch):
    m = FM.match(t)
    body_off = m.end()
    pos = 0
    sec = ""
    found = []
    for ln, line in enumerate(t.split("\n"), 1):
        start = pos
        pos += len(line) + 1
        if start < body_off:
            continue
        s = line.rstrip("\r")
        if s.startswith("#"):
            sec = s
            continue
        spans = [(x.start(), x.end()) for x in LINKSPAN.finditer(s)]
        for i, c in enumerate(s):
            if c == ch and not any(a <= i < b for a, b in spans):
                found.append((ln, sec, i, s))
    return found


def snippet(t, s, i):
    for r in range(3, 80):
        lo, hi = max(0, i - r), min(len(s), i + 1 + r)
        snip = s[lo:hi]
        if t.count(snip) == 1:
            return snip, i - lo
    return None, None


def cmd_plan(chars):
    for ch in chars:
        words = declared(ch)
        print(f"##### {ch}: {len(words)} declared words")
        for p in words:
            t = p.read_bytes().decode("utf-8")
            if f"](../kanji/{ch}.md)" in t:
                print(f"--- {p.name}: already linked")
                continue
            cands = candidates(t, ch)
            if not cands:
                print(f"--- {p.name}: NO plain occurrence")
                continue
            def key(c):
                ln, sec, i, s = c
                return (0 if "kanji" in sec.lower() else 1, 0 if standalone(s, i) else 1, ln)
            best = sorted(cands, key=key)[0]
            ln, sec, i, s = best
            snip, rel = snippet(t, s, i)
            tag = "K" if "kanji" in sec.lower() else "o"
            sa = "s" if standalone(s, i) else "c"
            print(f"--- {p.name} L{ln}{tag}{sa} (plain occurrences: {len(cands)})")
            if snip is None:
                print("    NO UNIQUE SNIPPET; line = " + s)
                continue
            print("    OLD: " + snip)
            print("    NEW: " + snip[:rel] + f"[{ch}](../kanji/{ch}.md)" + snip[rel + 1:])


def git_show(base, rel):
    p = subprocess.run(["git", "-c", "core.quotepath=false", "show", f"{base}:{rel}"], cwd=n1lib.REPO, capture_output=True)
    return p.stdout.decode("utf-8") if p.returncode == 0 else None


def load_remarks(path):
    out = {}
    for it in json.loads(Path(path).read_text(encoding="utf-8")):
        out.setdefault(it["file"], []).append((it["old"], it["new"]))
    return out


def cmd_verify(base, chars, remarks=None):
    remarks = remarks or {}
    remark_edits = 0
    expected = {}
    for ch in chars:
        for p in declared(ch):
            old = git_show(base, "words/" + p.name)
            if old is not None and f"](../kanji/{ch}.md)" in old:
                continue
            expected[(p.name, ch)] = 1
    names = subprocess.run(["git", "-c", "core.quotepath=false", "diff", "--name-only", base, "--", "words"],
                           cwd=n1lib.REPO, capture_output=True).stdout.decode("utf-8").split("\n")
    names = [n.strip() for n in names if n.strip()]
    added = Counter()
    problems = 0
    for rel in names:
        old = git_show(base, rel)
        new = (n1lib.REPO / rel).read_bytes().decode("utf-8").replace("\r\n", "\n")
        if old is None:
            print(f"NEW FILE (not link-only): {rel}")
            problems += 1
            continue
        old = old.replace("\r\n", "\n")
        cmp_old = old
        for r_old, r_new in remarks.get(rel, []):
            if cmp_old.count(r_old) != 1 or r_old in new:
                print(f"REMARK NOT APPLICABLE: {rel}")
                problems += 1
            else:
                cmp_old = cmp_old.replace(r_old, r_new)
                remark_edits += 1
        if WRAPPED.sub(r"\1", cmp_old) != WRAPPED.sub(r"\1", new):
            print(f"NOT LINK-ONLY: {rel}")
            problems += 1
        gain = Counter(WRAPPED.findall(new)) - Counter(WRAPPED.findall(old))
        for ch, n in gain.items():
            added[(Path(rel).name, ch)] += n
    for pair in sorted(set(expected) | set(added)):
        want, got = expected.get(pair, 0), added.get(pair, 0)
        if want != got:
            print(f"MISMATCH {pair[0]} {pair[1]}: expected {want} added link(s), got {got}")
            problems += 1
    for rel in sorted(set(remarks) - set(names)):
        print(f"REMARK FILE UNCHANGED: {rel}")
        problems += 1
    print(f"changed word files: {len(names)}; expected pairs: {len(expected)}; added link pairs: {len(added)}; "
          f"total added links: {sum(added.values())}; declared remark edits: {remark_edits}; problems: {problems}")
    return 1 if problems else 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "plan":
        cmd_plan(a[1:])
    elif a and a[0] == "verify":
        rest, rem = a[2:], None
        if "--remarks" in rest:
            i = rest.index("--remarks")
            rem = load_remarks(rest[i + 1])
            rest = rest[:i] + rest[i + 2:]
        sys.exit(cmd_verify(a[1], rest, rem))
    else:
        print(__doc__)

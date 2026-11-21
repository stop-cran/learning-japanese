import os, sys, subprocess
sys.path.insert(0, r"C:\Users\romanko\n1-kanji-workspace\lean")
import n1lib
REPO = r"C:\Users\romanko\n1-kanji-workspace\b156-wt"
REV = sys.argv[1]
D = n1lib.build_jmdict_cache(); E = D["entries"]; CI = D["char_index"]
files = set(subprocess.run(["git", "-c", "core.quotepath=false", "ls-tree", "-r", "--name-only", REV, "--", "kanji", "words"],
                           cwd=REPO, capture_output=True, text=True, encoding="utf-8").stdout.split())
COMMON = {"news1", "ichi1", "spec1", "gai1"}
PRI = COMMON | {"news2", "ichi2", "spec2", "gai2"}
print("# Candidate words for the 乙, 仙 and 伯 rows\n")
print("Generated at `%s` from the pinned JMdict (`%s`, sha256 %s) and the repository tree at that commit." % (
    REV, n1lib.JMDICT_GZ.name, n1lib.sha256_file(n1lib.JMDICT_GZ)))
print("Rows: every JMdict entry with a kanji form that contains the kanji and carries any priority tag on that form, plus the")
print("untagged entries named in `RESPONSE.md`. `list` = the form has one of news1, ichi1, spec1 or gai1 (the proposal's list).")
print("`other kanji` = the other kanji of the form and whether each has a card (`kanji/<k>.md`) at that commit; `article` =")
print("whether `words/<form>.md` exists. Readings are JMdict's, with their tags and restrictions; senses abridged to the first gloss of each.\n")
extra = {"乙": ["乙種", "早乙女", "乙女"], "仙": [], "伯": ["伯父", "伯母"]}
for k in "乙仙伯":
    print("## %s\n" % k)
    print("| entry | form [tags] {info} | readings | list | other kanji | article | senses |")
    print("| --- | --- | --- | --- | --- | --- | --- |")
    rows = []
    for eid in CI.get(k, []):
        e = E[eid]
        for kf in e["k"]:
            if k not in kf[0]:
                continue
            tagged = set(kf[1]) & PRI
            if not tagged and kf[0] not in extra[k]:
                continue
            rows.append((0 if set(kf[1]) & COMMON else 1, kf[0], eid, kf, e))
    seen = set()
    for _, form, eid, kf, e in sorted(rows, key=lambda r: (r[0], r[1])):
        if (eid, form) in seen:
            continue
        seen.add((eid, form))
        rs = ", ".join(r[0] + ("[" + "/".join(r[1]) + "]" if r[1] else "") + ("<restr:" + "/".join(r[2]) + ">" if r[2] else "")
                       + ("{" + "/".join(r[4]) + "}" if r[4] else "") for r in e["r"] if not r[2] or form in r[2])
        others = [c for c in dict.fromkeys(form) if c != k and n1lib.CJK.match(c)]
        oth = ", ".join("%s %s" % (c, "card" if "kanji/%s.md" % c in files else "NO CARD") for c in others) or "-"
        senses = "; ".join(("(" + "/".join(s["misc"]) + ") " if s["misc"] else "") + s["gloss"][0] for s in e["s"][:4])
        print("| %s | %s%s%s | %s | %s | %s | %s | %s |" % (
            eid, form, "[" + "/".join(kf[1]) + "]" if kf[1] else "", "{" + "/".join(kf[2]) + "}" if kf[2] else "", rs,
            "yes" if set(kf[1]) & COMMON else "no", oth, "yes" if "words/%s.md" % form in files else "no", senses.replace("|", "/")))
    print()

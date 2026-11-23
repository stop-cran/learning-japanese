"""Scan the pinned JMdict for entries spelled 甲乙 (completeness check for the 甲乙 word article).
usage: python -X utf8 kouotsu_scan.py   (run from the lean directory)"""
import sys, re, gzip, hashlib, os
sys.path.insert(0, ".")
import n1lib
p = str(n1lib.JMDICT_GZ)
raw = open(p, "rb").read()
data = (gzip.decompress(raw) if p.endswith(".gz") else raw).decode("utf-8")
ents = re.findall(r"<entry>.*?</entry>", data, re.S)
seq = lambda e: re.search(r"<ent_seq>(\d+)", e).group(1)
kebs = lambda e: re.findall(r"<keb>(.*?)</keb>", e)
rebs = lambda e: re.findall(r"<reb>(.*?)</reb>", e)
print("# Pinned-JMdict scan: entries spelled 甲乙")
print("command: python -X utf8 kouotsu_scan.py (from the lean directory)")
print(f"file: {os.path.basename(p)}; sha256 {hashlib.sha256(raw).hexdigest()}; {len(ents)} entries")
exact = [e for e in ents if "甲乙" in kebs(e)]
print(f"entries with a written form (keb) exactly 甲乙: {len(exact)}")
for e in exact:
    print("  ", seq(e), "kebs", kebs(e), "readings", rebs(e))
    for i, s in enumerate(re.findall(r"<sense>(.*?)</sense>", e, re.S), 1):
        print(f"     sense {i}:", "; ".join(re.findall(r"<gloss[^>]*>(.*?)</gloss>", s)))
part = [e for e in ents if any("甲乙" in k and k != "甲乙" for k in kebs(e))]
print(f"entries with a longer written form containing 甲乙: {len(part)}")
for e in part:
    print("  ", seq(e), kebs(e), rebs(e))
rd = [e for e in ents if "こうおつ" in rebs(e)]
print(f"entries with a reading (reb) exactly こうおつ: {len(rd)}")
for e in rd:
    print("  ", seq(e), kebs(e))
km = [e for e in ents if "かるめる" in rebs(e)]
print(f"entries with a reading (reb) exactly かるめる: {len(km)}")
for e in km:
    print("  ", seq(e), kebs(e))

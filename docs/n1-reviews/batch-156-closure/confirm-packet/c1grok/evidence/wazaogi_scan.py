"""Scan the pinned JMdict for entries with a reading わざおぎ (absence check for the 伎 card).
usage: python -X utf8 wazaogi_scan.py   (run from the lean directory)"""
import sys, re, gzip, hashlib, os
sys.path.insert(0, ".")
import n1lib
p = str(n1lib.JMDICT_GZ)
raw = open(p, "rb").read()
data = (gzip.decompress(raw) if p.endswith(".gz") else raw).decode("utf-8")
ents = re.findall(r"<entry>.*?</entry>", data, re.S)
print("# Pinned-JMdict scan: entries read わざおぎ")
print("command: python -X utf8 wazaogi_scan.py (from the lean directory)")
print(f"file: {os.path.basename(p)}; sha256 {hashlib.sha256(raw).hexdigest()}; {len(ents)} entries")
exact = [e for e in ents if re.search(r"<reb>わざおぎ</reb>", e)]
print(f"entries with a reading (reb) exactly わざおぎ: {len(exact)}")
near = [e for e in ents if re.search(r"<reb>わざお[^<]*</reb>", e)]
print(f"entries with any reading starting わざお: {len(near)}")
for e in near:
    print("  ", re.search(r"<ent_seq>(\d+)", e).group(1), re.findall(r"<keb>(.*?)</keb>", e), re.findall(r"<reb>(.*?)</reb>", e))
gi = [e for e in ents if re.search(r"<keb>伎</keb>", e)]
print(f"entries spelled 伎 alone: {len(gi)}")
for e in gi:
    print("  ", re.search(r"<ent_seq>(\d+)", e).group(1), re.findall(r"<reb>(.*?)</reb>", e))

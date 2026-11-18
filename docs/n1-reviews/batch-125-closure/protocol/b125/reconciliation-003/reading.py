import hashlib
import os
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

root = Path(r"C:\Users\stop-\n1-kanji-workspace")
repo = root / "b125-worktree"
assert os.environ["N1_REPO"] == str(repo)
sys.path.insert(0, str(root / "lean"))
import reading_exposure as exposure

raw = (repo / "docs" / "n1-sources" / "batch-125" / "jmdict-selected-records.xml").read_bytes()
assert hashlib.sha256(raw).hexdigest() == "47b6ea523f2efa3526714606e09ac5518b3c714ce637405698cdc0d66b52e951"
entries, char_index = {}, defaultdict(list)
for element in ET.fromstring(raw).findall("entry"):
    eid = element.findtext("ent_seq")
    spellings = [[k.findtext("keb"), [p.text for p in k.findall("ke_pri")], [f.text for f in k.findall("ke_inf")]] for k in element.findall("k_ele")]
    readings = [[r.findtext("reb"), [p.text for p in r.findall("re_pri")], [v.text for v in r.findall("re_restr")], r.find("re_nokanji") is not None, [f.text for f in r.findall("re_inf")]] for r in element.findall("r_ele")]
    senses = [{"misc": [m.text for m in s.findall("misc")], "gloss": [g.text for g in s.findall("gloss")]} for s in element.findall("sense")]
    entries[eid] = {"k": spellings, "r": readings, "s": senses}
    for char in set("".join(k[0] for k in spellings)):
        char_index[char].append(eid)
assert {"1359800", "1359850"}.issubset(entries)
exposure.build_jmdict_cache = lambda: {"entries": entries, "char_index": dict(char_index)}
code = exposure.main(["--seeds", "100", "侵"])
if code:
    raise SystemExit(code)
print("Bounded host model only; no arbitrary-pool, multiple-borrow, Kotlin/native/device, or whole-set acceptance.")

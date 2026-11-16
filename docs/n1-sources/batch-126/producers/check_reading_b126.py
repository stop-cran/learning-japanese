import json
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from b126_common import PACKET, ROOT, sha

sys.path.insert(0, str(ROOT / "lean"))
import reading_exposure as exposure

receipt = json.loads((PACKET / "source-receipt.json").read_text(encoding="utf-8"))
raw = (PACKET / "jmdict-selected-records.xml").read_bytes()
assert sha(raw) == receipt["dictionaryInputs"]["jmdict"]["outputs"]["jmdict-selected-records.xml"]["sha256"]
entries, char_index = {}, defaultdict(list)
for element in ET.fromstring(raw).findall("entry"):
    eid = element.findtext("ent_seq")
    spellings = [[k.findtext("keb"), [p.text for p in k.findall("ke_pri")], [f.text for f in k.findall("ke_inf")]] for k in element.findall("k_ele")]
    readings = [[r.findtext("reb"), [p.text for p in r.findall("re_pri")], [v.text for v in r.findall("re_restr")], r.find("re_nokanji") is not None, [f.text for f in r.findall("re_inf")]] for r in element.findall("r_ele")]
    senses = [{"misc": [m.text for m in s.findall("misc")], "gloss": [g.text for g in s.findall("gloss")], "stagk": [g.text for g in s.findall("stagk")], "stagr": [g.text for g in s.findall("stagr")]} for s in element.findall("sense")]
    entries[eid] = {"k": spellings, "r": readings, "s": senses}
    for ch in set("".join(k[0] for k in spellings)):
        char_index[ch].append(eid)
assert len(entries) == 56 and {"1301940", "1774770"} <= entries.keys()
exposure.build_jmdict_cache = lambda: {"entries": entries, "char_index": dict(char_index)}
print("Explicit positive non-metadata reading: 傘=からかさ, full JMdict 1774770; no standard-list, priority or age dismissal.")
code = exposure.main(["--extra", "傘=からかさ", "--seeds", "100", "傘"])
if code:
    raise SystemExit(code)
print("The explicit alternative was included, not merely metadata-scanned. Bounded host model only; no arbitrary/custom-pool, multiple-borrow, Kotlin/native/device or whole-set acceptance.")

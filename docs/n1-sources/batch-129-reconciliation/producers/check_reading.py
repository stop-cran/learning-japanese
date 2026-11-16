import json
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from recon_common import *

sys.path.insert(0, str(ROOT / "lean"))
import reading_exposure as exposure

entries, char_index, canonical_hashes = {}, defaultdict(list), {}
sources = [(ORIGINAL_PACKET, name) for name in (
    "jmdict-complete-families.xml", "jmdict-supplemental-comparisons-002.xml",
    "jmdict-final-comparisons.xml", "jmdict-additional-families.xml")]
sources += [(PACKET, name) for name in (
    "jmdict-complete-records.xml", "jmdict-supplement-complete-records.xml",
    "jmdict-noose-complete-records.xml")]
for folder, filename in sources:
    for element in ET.parse(folder / filename).getroot():
        eid = element.findtext("ent_seq")
        digest = sha(ET.canonicalize(ET.tostring(element, encoding="unicode"), strip_text=True).encode())
        if eid in entries:
            assert canonical_hashes[eid] == digest, eid
            continue
        canonical_hashes[eid] = digest
        spellings = [[k.findtext("keb"), [p.text for p in k.findall("ke_pri")], [f.text for f in k.findall("ke_inf")]] for k in element.findall("k_ele")]
        readings = [[r.findtext("reb"), [p.text for p in r.findall("re_pri")], [v.text for v in r.findall("re_restr")], r.find("re_nokanji") is not None, [f.text for f in r.findall("re_inf")]] for r in element.findall("r_ele")]
        senses = [{"misc": [m.text for m in s.findall("misc")], "gloss": [g.text for g in s.findall("gloss")],
                   "stagk": [g.text for g in s.findall("stagk")], "stagr": [g.text for g in s.findall("stagr")]} for s in element.findall("sense")]
        entries[eid] = {"k": spellings, "r": readings, "s": senses}
        for ch in set("".join(k[0] for k in spellings)):
            char_index[ch].append(eid)
exposure.build_jmdict_cache = lambda: {"entries": entries, "char_index": dict(char_index)}
extras = {"茉": ["まつり", "まち", "み"],
          "絹": ["かとり", "かく", "わな", "わなをかける", "きぎぬ", "ぎぬ"],
          "虹": ["ぐ", "のじ", "ぬじ", "おにじ", "はし", "あぶらざら", "みだれる", "あらそう", "せめる"]}
assert len(extras["茉"]) == 3 and len(extras["絹"]) == 6 and len(extras["虹"]) == 9
print("Complete canonical-equality checked family union:", len(entries))
print("Explicit supplemental reading keys:", json.dumps(extras, ensure_ascii=False))
print("Positive Jitsu glosses are tested conservatively, not asserted as ordinary modern readings. Wiktionary グ is explicitly supplied as ぐ. Historical ヲニジ is supplied as おにじ; whole-word 羂索/括り readings are not assigned to 絹.")
print("The host helper's generic 'card text' source label for --extra means explicit external input, not a quotation from current card prose. Neither initial reviewer read the separate gu supplement.")
args = []
for ch, keys in extras.items():
    args.extend(["--extra", ch + "=" + ",".join(keys)])
code = exposure.main([*args, "--seeds", "100", *CHARS])
if code:
    raise SystemExit(code)
print("Bounded host N1/All/Starter + one borrowed target only. Preserve separately reported one-additional-holder risks for 橋/攻/責. Not arbitrary/custom pools, multiple borrowing, Kotlin/native/device, rendered font, whole-set, retrospective reviewer or publication acceptance.")

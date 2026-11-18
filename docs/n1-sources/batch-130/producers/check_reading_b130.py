import json
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from b130_common import CHARS, PACKET, ROOT, sha

sys.path.insert(0, str(ROOT / "lean"))
import reading_exposure as exposure

entries, char_index, canonical_hashes = {}, defaultdict(list), {}
for filename in ("jmdict-complete-families.xml", "jmdict-supplemental-families.xml", "jmdict-final-families.xml"):
    for element in ET.parse(PACKET / filename).getroot():
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
assert len(entries) == json.loads((PACKET / "final-source-audit.json").read_text(encoding="utf-8"))["completeJmdictUnion"]
exposure.build_jmdict_cache = lambda: {"entries": entries, "char_index": dict(char_index)}
extras = json.loads((PACKET / "reading-keys.json").read_text(encoding="utf-8"))["testedKeys"]
print("Complete canonical-equality checked family union:", len(entries))
print("Explicit supplemental reading keys:", json.dumps(extras, ensure_ascii=False))
print("Supplemental character forms, historical lookup strings and explicitly qualified modernized keys are tested conservatively, not asserted as ordinary modern readings. Compound-only かしわで/びんざさら/ひむささら are extra precautions, not bare-character claims.")
args = []
for ch, keys in extras.items():
    args.extend(["--extra", ch + "=" + ",".join(keys)])
code = exposure.main([*args, "--seeds", "100", *CHARS])
if code:
    raise SystemExit(code)
print("Bounded host N1/All/Starter + one borrowed target only. Not arbitrary/custom pools, multiple borrowing, Kotlin/native/device, rendered font, whole-set or publication acceptance.")

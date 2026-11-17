import contextlib
import io
import json
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from common_133 import PACKET, ROOT, sha

sys.path.insert(0, str(ROOT / "lean"))
import reading_exposure as exposure

entries, char_index, hashes = {}, defaultdict(list), {}
for filename in ("jmdict-complete-families.xml", "jmdict-supplemental-families.xml", "additional/jmdict-additional-families.xml"):
    for node in ET.parse(PACKET / filename).getroot():
        eid = node.findtext("ent_seq")
        digest = sha(ET.canonicalize(ET.tostring(node, encoding="unicode"), strip_text=True).encode())
        if eid in entries:
            assert hashes[eid] == digest, eid
            continue
        hashes[eid] = digest
        spellings = [[k.findtext("keb"), [v.text for v in k.findall("ke_pri")], [v.text for v in k.findall("ke_inf")]] for k in node.findall("k_ele")]
        readings = [[r.findtext("reb"), [v.text for v in r.findall("re_pri")], [v.text for v in r.findall("re_restr")],
                     r.find("re_nokanji") is not None, [v.text for v in r.findall("re_inf")]] for r in node.findall("r_ele")]
        senses = [{"misc": [v.text for v in s.findall("misc")], "gloss": [v.text for v in s.findall("gloss")],
                   "stagk": [v.text for v in s.findall("stagk")], "stagr": [v.text for v in s.findall("stagr")]} for s in node.findall("sense")]
        entries[eid] = {"k": spellings, "r": readings, "s": senses}
        for ch in set("".join(k[0] for k in spellings)):
            char_index[ch].append(eid)
exposure.build_jmdict_cache = lambda: {"entries": entries, "char_index": dict(char_index)}
extras = json.loads((PACKET / "reading-keys.json").read_bytes())["testedKeys"]
assert extras == {
    "琴": ["きん", "ごん", "こと", "ごむ", "きむ", "ことのを", "きのこと"],
    "鉛": ["えん", "なまり", "くろなまり"],
    "滝": ["ろう", "そう", "たき", "りょう", "さう", "らき", "はやせ", "ひたす", "うるおす", "たるみ", "たぎ"],
}
print("Canonical-equality checked complete JMdict family union:", len(entries))
print("Explicit supplemental reading keys:", json.dumps(extras, ensure_ascii=False))
print("Historical, supplemental, uncertain and name forms deliberately over-tested; not all ordinary independent modern readings.")
args = []
for ch, keys in extras.items():
    args.extend(["--extra", ch + "=" + ",".join(keys)])
buffer = io.StringIO()
with contextlib.redirect_stdout(buffer):
    code = exposure.main([*args, "--seeds", "100", "琴", "鉛", "滝"])
output = buffer.getvalue()
print(output, end="")
if code:
    raise SystemExit(code)
assert "0 production hit(s)" in output and "0 padded-session hit(s)" in output, "Positive reading collision; audit exit code alone is insufficient."
print("Bounded host N1/All/Starter + one borrowed target only. Not arbitrary/custom or multiple-borrow pools, Kotlin/native/device, rendered font, whole-set or publication acceptance.")

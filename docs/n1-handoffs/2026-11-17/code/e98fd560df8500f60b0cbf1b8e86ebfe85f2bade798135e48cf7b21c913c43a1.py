import contextlib
import io
import json
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict

from common_134 import HERE, ROOT, sha

sys.path.insert(0, str(ROOT / "lean"))
import reading_exposure as exposure

packet = HERE / "source-002"
entries, char_index, hashes = {}, defaultdict(list), {}
for node in ET.parse(packet / "jmdict-complete-families.xml").getroot():
    identifier = node.findtext("ent_seq")
    digest = sha(ET.canonicalize(ET.tostring(node, encoding="unicode"), strip_text=True).encode())
    assert identifier not in entries
    hashes[identifier] = digest
    spellings = [[k.findtext("keb"), [v.text for v in k.findall("ke_pri")],
                  [v.text for v in k.findall("ke_inf")]] for k in node.findall("k_ele")]
    readings = [[r.findtext("reb"), [v.text for v in r.findall("re_pri")],
                 [v.text for v in r.findall("re_restr")], r.find("re_nokanji") is not None,
                 [v.text for v in r.findall("re_inf")]] for r in node.findall("r_ele")]
    senses = [{"misc": [v.text for v in s.findall("misc")],
               "gloss": [v.text for v in s.findall("gloss")],
               "stagk": [v.text for v in s.findall("stagk")],
               "stagr": [v.text for v in s.findall("stagr")]} for s in node.findall("sense")]
    entries[identifier] = {"k": spellings, "r": readings, "s": senses}
    for ch in set("".join(k[0] for k in spellings)):
        char_index[ch].append(identifier)

exposure.build_jmdict_cache = lambda: {"entries": entries, "char_index": dict(char_index)}
extras = json.loads((packet / "reading-keys.json").read_bytes())["testedKeys"]
assert extras == {"紫": ["し", "むらさき", "ゆかり", "さい", "つつむ"]}
print("Complete verified JMdict family union:", len(entries))
print("Explicit supplemental reading keys:", json.dumps(extras, ensure_ascii=False))
print("Name and uncertain historical forms deliberately over-tested; not all ordinary independent modern readings.")
buffer = io.StringIO()
with contextlib.redirect_stdout(buffer):
    code = exposure.main(["--extra", "紫=" + ",".join(extras["紫"]), "--seeds", "100", "紫"])
output = buffer.getvalue()
print(output, end="")
if code:
    raise SystemExit(code)
assert "0 production hit(s)" in output and "0 padded-session hit(s)" in output, (
    "Positive reading collision; audit exit code alone is insufficient."
)
print("Bounded host N1/All/Starter + one borrowed target only. Not arbitrary/custom or "
      "multiple-borrow pools, Kotlin/native/device, rendered font, whole-set or publication acceptance.")

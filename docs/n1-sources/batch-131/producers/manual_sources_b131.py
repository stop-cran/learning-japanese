import copy
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from b131_common import HERE, PACKET, git, sha, start_guard, write
from candidate_b131 import BASE
from survey_b131 import INPUTS, records
from survey_b131_002 import xml_output

guard = start_guard()
try:
    ch = "川"
    raw = git("show", f"{BASE}:kanji/{ch}.md")
    write(PACKET / "comparison-cards" / (ch + ".md"), raw)
    kd = [copy.deepcopy(n) for n in records("kanjidic2", guard) if n.findtext("literal") == ch]
    jm = [copy.deepcopy(n) for n in records("jmdict", guard)
          if ch in {k.text for k in n.findall("k_ele/keb")}]
    outputs = {
        "kanjidic2-manual-comparisons.xml": xml_output(PACKET / "kanjidic2-manual-comparisons.xml", "kanjidic2", kd),
        "jmdict-manual-families.xml": xml_output(PACKET / "jmdict-manual-families.xml", "JMdict", jm)}
    write(PACKET / "manual-source-receipt.json", {
        "base": BASE, "allExactSpellings": [ch], "inputs": INPUTS, "outputs": outputs,
        "predicate": "Every complete JMdict family with exact 川 spelling and the complete KANJIDIC2 川 record; no sense/rarity/priority filtering.",
        "reason": "Actual Starter padded-session hits in author-gates-002 require a third Starter curated choice; source-check river independently.",
        "comparisonCardSha256": sha(raw), "producerSha256": sha(Path(__file__).read_bytes())})
    print(ET.tostring(kd[0], encoding="unicode"))
    for node in jm:
        print(ET.tostring(node, encoding="unicode"))
finally:
    write(HERE / "manual-source-memory-001.json", guard.finish())

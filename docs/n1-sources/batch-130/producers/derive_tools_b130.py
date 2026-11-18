from b130_common import HERE, ROOT, write

for name in ("generate", "run_b129_gates"):
    source_name = "generate_b129.py" if name == "generate" else name + ".py"
    text = (ROOT / "scratch-129" / source_name).read_text(encoding="utf-8").replace("b129", "b130").replace('"129"', '"130"')
    if name == "generate":
        text = text.replace("茉絹虹艸艹末未本古糸⺯糹口月虫工紅功石莉花木綿紙約級", "塀拍耗土尸并手扌白耒毛古右石未本末耕")
    write(HERE / source_name.replace("b129", "b130"), text.encode())

text = (ROOT / "scratch-129" / "check_reading_b129.py").read_text(encoding="utf-8").replace("b129", "b130")
start, end = text.index('for filename in ('), text.index('    for element in ET.parse')
text = text[:start] + 'for filename in ("jmdict-complete-families.xml", "jmdict-supplemental-families.xml", "jmdict-final-families.xml"):\n' + text[end:]
text = text.replace("assert len(entries) == 252", 'assert len(entries) == json.loads((PACKET / "final-source-audit.json").read_text(encoding="utf-8"))["completeJmdictUnion"]')
start, end = text.index("extras = {"), text.index('print("Complete canonical')
text = text[:start] + 'extras = json.loads((PACKET / "reading-keys.json").read_text(encoding="utf-8"))["testedKeys"]\n' + text[end:]
text = text.replace('print("Jitsu glosses are tested conservatively, not asserted as ordinary modern readings. Wiktionary discrepancy is tested, not silently trusted. Historical ヲニジ is supplied as おにじ.")',
                    'print("Supplemental character forms, historical lookup strings and explicitly qualified modernized keys are tested conservatively, not asserted as ordinary modern readings. Compound-only かしわで/びんざさら/ひむささら are extra precautions, not bare-character claims.")')
write(HERE / "check_reading_b130.py", text.encode())

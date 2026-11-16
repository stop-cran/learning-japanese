import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from html.parser import HTMLParser
from b127_common import HERE, PACKET, sha, start_guard, write


class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        if data.strip():
            self.parts.append(data.strip())


guard = start_guard()
try:
    pages = []
    for label, url in [
        ("kanjipedia", "https://www.kanjipedia.jp/kanji/0004231200"),
        ("kotobank", "https://kotobank.jp/word/%E5%80%89-56132"),
    ]:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = response.read()
        guard.check()
        write(HERE / "external-pages" / (label + ".html"), data)
        parser = Text()
        parser.feed(data.decode("utf-8"))
        text = "\n".join(parser.parts)
        write(HERE / "external-pages" / (label + ".txt"), text.encode())
        pages.append({"label": label, "url": url, "capturedAt": datetime.now(timezone.utc).isoformat(), "rawSha256": sha(data), "rawBytes": len(data), "textSha256": sha(text.encode()), "localCapture": str(HERE / "external-pages" / (label + ".html"))})
    write(HERE / "external-pages" / "receipt.json", pages)
    lines = []
    for entry in ET.parse(PACKET / "jmdict-selected-records.xml").findall("entry"):
        guard.check()
        lines.append({
            "id": entry.findtext("ent_seq"),
            "spellings": [{"text": k.findtext("keb"), "info": [v.text for v in k.findall("ke_inf")], "priority": [v.text for v in k.findall("ke_pri")]} for k in entry.findall("k_ele")],
            "readings": [{"text": r.findtext("reb"), "restrictions": [v.text for v in r.findall("re_restr")], "info": [v.text for v in r.findall("re_inf")], "noKanji": r.find("re_nokanji") is not None} for r in entry.findall("r_ele")],
            "senses": [{tag: [v.text for v in s.findall(tag)] for tag in ("gloss", "pos", "misc", "field", "stagk", "stagr", "s_inf")} for s in entry.findall("sense")],
        })
    write(PACKET / "jmdict-inspection.json", lines)
    for item in lines:
        print(json.dumps(item, ensure_ascii=False))
finally:
    write(HERE / "inspection-memory-001.json", guard.finish())

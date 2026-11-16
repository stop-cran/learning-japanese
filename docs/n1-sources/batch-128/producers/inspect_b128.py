import json
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from b128_common import BASE, HERE, PACKET, git, sha, start_guard, write
from extract_b128 import PageText

guard = start_guard()
try:
    pages = []
    for label, url in [
        ("kanjipedia-character", "https://www.kanjipedia.jp/kanji/0003613500"),
        ("kanjipedia-word", "https://www.kanjipedia.jp/kotoba/0003614100"),
        ("kotobank", "https://kotobank.jp/word/唇-55487"),
        ("weblio", "https://www.weblio.jp/content/唇"),
    ]:
        encoded = urllib.parse.quote(url, safe=":/%")
        try:
            with urllib.request.urlopen(encoded, timeout=30) as response:
                data = response.read()
                final_url = response.url
            guard.check()
            write(HERE / "external-pages" / (label + ".html"), data)
            parser = PageText()
            parser.feed(data.decode("utf-8"))
            text = "\n".join(parser.parts)
            write(HERE / "external-pages" / (label + ".txt"), text.encode())
            pages.append({"label": label, "url": url, "finalUrl": final_url, "capturedAt": datetime.now(timezone.utc).isoformat(), "rawSha256": sha(data), "rawBytes": len(data), "textSha256": sha(text.encode()), "localCapture": str(HERE / "external-pages" / (label + ".html"))})
        except urllib.error.URLError as error:
            pages.append({"label": label, "url": url, "error": str(error)})
            print(f"Capture failed: {label}: {error}")
    write(HERE / "external-pages" / "receipt.json", pages)
    lines = []
    for entry in ET.parse(PACKET / "jmdict-selected-records.xml").findall("entry"):
        guard.check()
        lines.append({
            "id": entry.findtext("ent_seq"),
            "spellings": [{"text": k.findtext("keb"), "info": [v.text for v in k.findall("ke_inf")], "priority": [v.text for v in k.findall("ke_pri")]} for k in entry.findall("k_ele")],
            "readings": [{"text": r.findtext("reb"), "restrictions": [v.text for v in r.findall("re_restr")], "info": [v.text for v in r.findall("re_inf")], "priority": [v.text for v in r.findall("re_pri")], "noKanji": r.find("re_nokanji") is not None} for r in entry.findall("r_ele")],
            "senses": [{tag: [v.text for v in s.findall(tag)] for tag in ("gloss", "pos", "misc", "field", "stagk", "stagr", "s_inf", "xref", "ant")} for s in entry.findall("sense")],
        })
    write(PACKET / "jmdict-inspection.json", lines)
    for item in lines:
        print(json.dumps(item, ensure_ascii=False))
    print(git("fetch", "origin", include_stderr=True).decode("utf-8", "replace"))
    write(HERE / "fetch-001.json", {"head": git("rev-parse", "HEAD").decode().strip(), "originMain": git("rev-parse", "origin/main").decode().strip(), "expectedBase": BASE})
finally:
    write(HERE / "inspection-memory-001.json", guard.finish())

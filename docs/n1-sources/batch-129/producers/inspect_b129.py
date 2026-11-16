import json
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from b129_common import CHARS, HERE, PACKET, sha, start_guard, write
from extract_b129 import PageText


guard = start_guard()
try:
    pages = []
    for ch in CHARS:
        for label, url in [
            ("weblio", f"https://www.weblio.jp/content/{ch}"),
            ("kotobank", f"https://kotobank.jp/word/{ch}"),
        ]:
            filename = f"{ch}-{label}"
            try:
                with urllib.request.urlopen(urllib.parse.quote(url, safe=":/%"), timeout=30) as response:
                    raw, final_url = response.read(), response.url
                guard.check()
                write(HERE / "external-pages" / (filename + ".html"), raw)
                parser = PageText()
                parser.feed(raw.decode("utf-8"))
                text = "\n".join(parser.parts).encode()
                write(HERE / "external-pages" / (filename + ".txt"), text)
                pages.append({"character": ch, "provider": label, "url": url, "finalUrl": final_url,
                              "capturedAt": datetime.now(timezone.utc).isoformat(), "rawSha256": sha(raw),
                              "rawBytes": len(raw), "textSha256": sha(text),
                              "localRawCapture": str(HERE / "external-pages" / (filename + ".html"))})
            except urllib.error.URLError as error:
                pages.append({"character": ch, "provider": label, "url": url, "error": str(error)})
                print(f"FAILED {url}: {error}")
    write(HERE / "external-pages" / "receipt-001.json", pages)
    membership = json.loads((PACKET / "query-membership.json").read_text(encoding="utf-8"))
    entries = []
    for el in ET.parse(PACKET / "jmdict-complete-families.xml").findall("entry"):
        entries.append({
            "id": el.findtext("ent_seq"),
            "queries": membership[el.findtext("ent_seq")],
            "spellings": [{"text": k.findtext("keb"), "info": [v.text for v in k.findall("ke_inf")]} for k in el.findall("k_ele")],
            "readings": [{"text": r.findtext("reb"), "restrictions": [v.text for v in r.findall("re_restr")],
                          "info": [v.text for v in r.findall("re_inf")], "noKanji": r.find("re_nokanji") is not None} for r in el.findall("r_ele")],
            "senses": [{tag: [v.text for v in s.findall(tag)] for tag in ("gloss", "pos", "misc", "field", "stagk", "stagr", "s_inf", "xref", "ant")} for s in el.findall("sense")],
        })
    write(PACKET / "jmdict-inspection.json", entries)
    for ch in CHARS:
        lines = [json.dumps(e, ensure_ascii=False) for e in entries if f"contains:{ch}" in e["queries"] or any(k["text"] == ch for k in e["spellings"])]
        write(HERE / f"{ch}-complete-family-readback.txt", ("\n".join(lines) + "\n").encode())
    comparison_lines = []
    for path in sorted((PACKET / "comparison-cards").glob("*.md")):
        comparison_lines += [f"===== {path.name} =====", path.read_text(encoding="utf-8")]
    write(HERE / "comparison-card-readback.txt", "\n".join(comparison_lines).encode())
    write(HERE / "inspection-summary-001.json", {"pages": pages, "completeFamilies": len(entries),
          "inspectionProducerSha256": sha(Path(__file__).read_bytes())})
    print(json.dumps({"pages": [{"character": p["character"], "provider": p["provider"], "bytes": p.get("rawBytes"), "error": p.get("error")} for p in pages],
                      "families": len(entries)}, ensure_ascii=False))
finally:
    write(HERE / "inspection-memory-001.json", guard.finish())

"""Sidecar cache of JMdict sense details that the compact cache omits.

Per entry id with any such detail: a list (one item per sense) of
{"dial": [...], "field": [...], "s_inf": [...], "xref": [...], "lsource": [...]}.
Built from the same pinned JMdict_e.gz and keyed to its sha256.
"""
import gzip
import json
import xml.etree.ElementTree as ET

import n1lib

OUT = n1lib.CACHE / "jmdict-extra.json.gz"
KEYS = ("dial", "field", "s_inf", "xref")


def build(force=False):
    stamp = n1lib.sha256_file(n1lib.JMDICT_GZ)
    if OUT.exists() and not force:
        with gzip.open(OUT, "rt", encoding="utf-8") as f:
            data = json.load(f)
        if data.get("source_sha256") == stamp:
            return data
    entries = {}
    with gzip.open(n1lib.JMDICT_GZ) as f:
        for _, el in ET.iterparse(f, events=("end",)):
            if el.tag != "entry":
                continue
            senses, any_extra = [], False
            for s in el.findall("sense"):
                d = {k: [t.text for t in s.findall(k)] for k in KEYS}
                d["lsource"] = [(t.text or "") + " (" + (t.get("{http://www.w3.org/XML/1998/namespace}lang") or "eng") + ")"
                                for t in s.findall("lsource")]
                d = {k: v for k, v in d.items() if v}
                any_extra = any_extra or bool(d)
                senses.append(d)
            if any_extra:
                entries[el.findtext("ent_seq")] = senses
            el.clear()
    data = {"source_sha256": stamp, "entries": entries}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(OUT, "wt", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    return data


if __name__ == "__main__":
    d = build(force=True)
    print(len(d["entries"]), "entries with sense details")

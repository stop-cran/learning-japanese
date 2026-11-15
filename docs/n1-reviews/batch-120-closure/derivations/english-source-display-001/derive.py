"""Coordinator derivation: readable English Noun/Verb sense text from the bound Wiktionary capture."""
import hashlib, html, json, re, sys
from pathlib import Path
SRC = Path(r"C:\Users\stop-\n1-kanji-workspace\scratch-120\english-arrest-source-001.html")
SHA = "ce09115325ba4cb916bc695509e6c16d3e475fad7c9d5ece65ec96ff82d265e9"
OUT = Path(__file__).resolve().parent
raw = SRC.read_bytes()
assert hashlib.sha256(raw).hexdigest() == SHA
s = raw.decode("utf-8")
def section(start_id, end_id):
    a = s.index(f'id="{start_id}"'); a = s.rindex("<", 0, a)
    b = s.index(f'id="{end_id}"'); b = s.rindex("<h", 0, b)
    while s[b-1:b] != "" and not s[b:].startswith("<h"): b -= 1
    return a, b
def text(fragment):
    fragment = re.sub(r"(?is)<(script|style)\b.*?</\1>", "", fragment)
    fragment = re.sub(r"(?i)<(br|/p|/li|/dd|/dt|/h[1-6]|/div|/dl|/ol|/ul)\b[^>]*>", "\n", fragment)
    fragment = re.sub(r"(?i)<li\b[^>]*>", "\n* ", fragment)
    fragment = re.sub(r"<[^>]+>", "", fragment)
    lines = [re.sub(r"[ \t\u00a0]+", " ", html.unescape(l)).strip() for l in fragment.split("\n")]
    out = []
    for l in lines:
        if l and l != "*" and l != "[edit]" and not (out and out[-1] == l): out.append(l)
    return "\n".join(out) + "\n"
ranges = {"Noun senses": section("Noun", "Derived_terms"), "Verb senses and synonyms": section("Verb", "Derived_terms_2")}
body = [f"Coordinator-derived text display of {SRC.name} (SHA-256 {SHA}), Wiktionary 'arrest', captured 2026-11-15T11:19:33Z.",
        "Only the English Noun and Verb sense sections are displayed; translation tables and other languages are omitted.",
        "Tags removed, entities decoded, whitespace collapsed; no wording added. The raw capture is the authority.", ""]
for name, (a, b) in ranges.items():
    body += [f"===== {name} (raw character offsets {a}-{b}) =====", text(s[a:b])]
data = "\n".join(body).encode("utf-8")
target = OUT / "wiktionary-arrest-english-senses.txt"
with target.open("xb") as f: f.write(data)
rec = {"source": {"path": str(SRC), "sha256": SHA, "bytes": len(raw)}, "ranges": {k: list(v) for k, v in ranges.items()},
       "output": {"path": str(target), "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)},
       "script": {"path": str(Path(__file__).resolve()), "sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}}
with (OUT / "derivation.json").open("x", encoding="utf-8") as f: f.write(json.dumps(rec, indent=2) + "\n")
print(json.dumps(rec, indent=1))

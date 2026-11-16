import copy
import gzip
import hashlib
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from html.parser import HTMLParser
from b131_common import BASE, HERE, REPO, ROOT, git, normalized, sha, start_guard, write

CHARS = list("皇衛桜羊霜")
OUT = HERE / "survey-001"
INPUTS = {
    "jmdict": ("n1-implementation-JMdict_e.gz", "2dbbfe0b1214911766bbc128a0935618b925be917e7d1c50f3536a89b0e8786d", "107079c692f2e49c08d45da1da227b7e021298f247d16578b44dfaa2ec9002c4", "entry"),
    "kanjidic2": ("n1-planning-kanjidic2.xml.gz", "af0a499d62ac4413c614adcca360e2306490c3f64fccb3510fc7caa15f901bed", "9a000ef112b4bad8f1e6e3ca1f8e9f73ed84c93a5eae93dadfa1513081dc5db8", "character"),
}


class HashReader:
    def __init__(self, stream, guard):
        self.stream, self.guard, self.digest = stream, guard, hashlib.sha256()

    def read(self, size=-1):
        self.guard.check()
        raw = self.stream.read(size)
        self.digest.update(raw)
        return raw


class PageText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts, self.ignore = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.ignore += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.ignore = max(0, self.ignore - 1)

    def handle_data(self, data):
        if not self.ignore and data.strip():
            self.parts.append(data.strip())


def canonical(node):
    return ET.canonicalize(ET.tostring(node, encoding="unicode"), strip_text=True)


def records(source, guard):
    filename, compressed, decompressed, tag = INPUTS[source]
    path = ROOT / "control" / "inputs" / filename
    assert sha(path.read_bytes()) == compressed
    with gzip.open(path, "rb") as stream:
        reader = HashReader(stream, guard)
        context = ET.iterparse(reader, events=("start", "end"))
        _, root = next(context)
        for event, node in context:
            if event == "end" and node.tag == tag:
                yield node
                node.clear()
                root.clear()
    assert reader.digest.hexdigest() == decompressed


def xml_output(path, tag, nodes):
    nodes = list(nodes)
    original = {n.findtext("ent_seq") or n.findtext("literal"): sha(canonical(n).encode()) for n in nodes}
    root = ET.Element(tag)
    root.extend(copy.deepcopy(nodes))
    ET.indent(root, space="  ")
    raw = ET.tostring(root, encoding="utf8", xml_declaration=True) + b"\n"
    write(path, raw)
    actual = {n.findtext("ent_seq") or n.findtext("literal"): sha(canonical(n).encode()) for n in ET.fromstring(raw)}
    assert original == actual
    return {"sha256": sha(raw), "bytes": len(raw), "canonicalRecordHashes": actual}


def main():
    guard = start_guard()
    try:
        assert git("rev-parse", "HEAD").decode().strip() == BASE
        assert not git("status", "--porcelain=v1", "--untracked-files=all")
        index_raw = git("show", f"{BASE}:docs/n1-sources/source-index.json")
        index = {r["kanji"]: r for r in json.loads(index_raw)}
        manifest = json.loads(git("show", f"{BASE}:manifest.json"))
        supports = {c: [] for c in CHARS}
        for c in CHARS:
            assert index[c]["statusAtFreeze"] == "pending"
            assert f"kanji/{c}.md" not in manifest["files"]
        for path in sorted((REPO / "words").glob("*.md")):
            match = re.search(r"^kanji: \[([^\]]*)\]$", normalized(path), re.M)
            if match:
                for c in CHARS:
                    if c in [p.strip() for p in match.group(1).split(",")]:
                        supports[c].append(path.stem)
        write(OUT / "membership.json", {"base": BASE, "indexSha256": sha(index_raw),
              "rows": [index[c] for c in CHARS], "supports": supports})
        kd = {n.findtext("literal"): copy.deepcopy(n) for n in records("kanjidic2", guard) if n.findtext("literal") in CHARS}
        xml_output(OUT / "kanjidic2-targets.xml", "kanjidic2", kd.values())
        families = []
        for node in records("jmdict", guard):
            spellings = [n.text for n in node.findall("k_ele/keb")]
            if any(c in spelling for spelling in spellings for c in CHARS + ["櫻", "衞"]):
                families.append(copy.deepcopy(node))
        receipt = xml_output(OUT / "jmdict-target-families.xml", "JMdict", families)
        write(OUT / "dictionary-receipt.json", {"inputs": INPUTS, "output": receipt,
              "predicate": "Any spelling contains 皇衛桜羊霜 or variant 櫻衞; complete parsed/reserialized families, no sense/priority filter, not raw slices."})
        captures = []
        for c in CHARS:
            for provider, url in (("kotobank", f"https://kotobank.jp/word/{c}"), ("weblio", f"https://www.weblio.jp/content/{c}")):
                path = OUT / "external" / f"{c}-{provider}.html"
                try:
                    with urllib.request.urlopen(url, timeout=30) as response:
                        raw, final = response.read(), response.url
                    write(path, raw)
                    parser = PageText()
                    parser.feed(raw.decode("utf8"))
                    text = ("\n".join(parser.parts) + "\n").encode()
                    write(path.with_suffix(".txt"), text)
                    captures.append({"character": c, "provider": provider, "url": url, "finalUrl": final,
                        "capturedAt": datetime.now(timezone.utc).isoformat(), "localRawCapture": str(path),
                        "rawSha256": sha(raw), "rawBytes": len(raw), "textSha256": sha(text)})
                except (OSError, UnicodeError) as error:
                    captures.append({"character": c, "provider": provider, "url": url, "error": repr(error)})
                guard.check()
        write(OUT / "external-bindings.json", {"captures": captures, "fullCapturesLocalOnly": True})
        for c in CHARS:
            lines = []
            for node in families:
                if any(c in n.text for n in node.findall("k_ele/keb")):
                    lines.append(ET.tostring(node, encoding="unicode"))
            write(OUT / f"{c}-families.txt", ("\n".join(lines) + "\n").encode())
        print(json.dumps({"supports": supports, "families": len(families), "captures": len(captures),
                          "rows": [{k: index[c][k] for k in ("kanji", "sourceRow", "metadata")} for c in CHARS]}, ensure_ascii=False))
    finally:
        write(OUT / "memory.json", guard.finish())


if __name__ == "__main__":
    main()

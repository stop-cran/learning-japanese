import copy
import gzip
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(r"C:\Users\stop-\n1-kanji-workspace")
REPO = ROOT / "b132-worktree"
HERE = Path(__file__).resolve().parent
OUT = HERE / "survey-001"
BASE = "2375ab9add0cc5d569c8ea35d229b82813fd8557"
CHARS = "墓嵐琴紫詩鉛矢滝"
INPUTS = {
    "jmdict": ("n1-implementation-JMdict_e.gz", "2dbbfe0b1214911766bbc128a0935618b925be917e7d1c50f3536a89b0e8786d", "107079c692f2e49c08d45da1da227b7e021298f247d16578b44dfaa2ec9002c4", "entry"),
    "kanjidic2": ("n1-planning-kanjidic2.xml.gz", "af0a499d62ac4413c614adcca360e2306490c3f64fccb3510fc7caa15f901bed", "9a000ef112b4bad8f1e6e3ca1f8e9f73ed84c93a5eae93dadfa1513081dc5db8", "character"),
}
GUARD = ROOT / "scratch-115" / "confirm" / "ram-guard" / "verify-zip-streaming.py"
GUARD_SHA = "46c721d63970e352a2c5c9d21c5d67b216e88a160b0966e65e2e407c0cb41c84"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not isinstance(data, bytes):
        data = (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode()
    with path.open("xb") as stream:
        stream.write(data)


class HashReader:
    def __init__(self, stream, guard):
        self.stream, self.guard, self.digest = stream, guard, hashlib.sha256()

    def read(self, size=-1):
        self.guard.check()
        data = self.stream.read(size)
        self.digest.update(data)
        return data


class Text(HTMLParser):
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


def records(source, guard):
    name, compressed, decompressed, tag = INPUTS[source]
    path = ROOT / "control" / "inputs" / name
    assert sha(path.read_bytes()) == compressed
    with gzip.open(path, "rb") as stream:
        reader = HashReader(stream, guard)
        parser = ET.iterparse(reader, events=("start", "end"))
        _, root = next(parser)
        for event, node in parser:
            if event == "end" and node.tag == tag:
                yield node
                node.clear()
                root.clear()
    assert reader.digest.hexdigest() == decompressed


def xml_output(path, tag, nodes):
    root = ET.Element(tag)
    root.extend(nodes)
    ET.indent(root, space="  ")
    data = ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"
    write(path, data)
    return {"sha256": sha(data), "bytes": len(data), "records": len(root)}


def main():
    assert os.environ["N1_REPO"] == str(REPO)
    assert sha(GUARD.read_bytes()) == GUARD_SHA
    spec = importlib.util.spec_from_file_location("ramguard_b132", GUARD)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.available_ram() > 2 * 1024**3
    guard = module.RamGuard()
    guard.start()
    OUT.mkdir()
    try:
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, check=True, capture_output=True, timeout=10).stdout.decode().strip()
        status = subprocess.run(["git", "status", "--porcelain=v1", "--untracked-files=all"], cwd=REPO, check=True, capture_output=True, timeout=10).stdout
        assert head == BASE and not status
        index_bytes = (REPO / "docs" / "n1-sources" / "source-index.json").read_bytes()
        index = {r["kanji"]: r for r in json.loads(index_bytes)}
        manifest = json.loads((REPO / "manifest.json").read_bytes())
        supports = {c: [] for c in CHARS}
        for c in CHARS:
            assert index[c]["statusAtFreeze"] == "pending"
            assert f"kanji/{c}.md" not in manifest["files"]
        for path in sorted((REPO / "words").glob("*.md")):
            text = path.read_bytes().replace(b"\r\n", b"\n").decode("utf-8")
            match = re.search(r"^kanji: \[([^\]]*)\]$", text, re.M)
            if match:
                for c in CHARS:
                    if c in [p.strip() for p in match.group(1).split(",")]:
                        supports[c].append(path.stem)
        write(OUT / "membership.json", {"base": BASE, "indexSha256": sha(index_bytes), "rows": [index[c] for c in CHARS], "supports": supports})
        kd = [copy.deepcopy(n) for n in records("kanjidic2", guard) if n.findtext("literal") in CHARS]
        assert {n.findtext("literal") for n in kd} == set(CHARS)
        kd_output = xml_output(OUT / "kanjidic2-targets.xml", "kanjidic2", kd)
        families = []
        membership = {}
        for node in records("jmdict", guard):
            spellings = [n.text for n in node.findall("k_ele/keb")]
            matched = [c for c in CHARS if any(c in s for s in spellings)]
            if matched:
                families.append(copy.deepcopy(node))
                membership[node.findtext("ent_seq")] = matched
        jm_output = xml_output(OUT / "jmdict-target-families.xml", "JMdict", families)
        write(OUT / "dictionary-receipt.json", {"base": BASE, "inputs": INPUTS, "outputs": {"kanjidic2-targets.xml": kd_output, "jmdict-target-families.xml": jm_output}, "predicate": "Union of complete families with any spelling containing one of 墓嵐琴紫詩鉛矢滝; complete target character records. No priority or sense filter. Parsed/reserialized XML, not raw source slices.", "membership": membership, "limits": "Planning survey only: variant-containing, exact-reading and exact-comparison queries are not included."})
        captures = []
        for c in CHARS:
            for provider, prefix in (("kotobank", "https://kotobank.jp/word/"), ("weblio", "https://www.weblio.jp/content/")):
                url = prefix + urllib.parse.quote(c)
                item = {"character": c, "provider": provider, "url": url}
                try:
                    with urllib.request.urlopen(url, timeout=30) as response:
                        raw, final = response.read(), response.url
                    path = OUT / "external" / f"{c}-{provider}.html"
                    write(path, raw)
                    parser = Text()
                    parser.feed(raw.decode("utf-8"))
                    text = ("\n".join(parser.parts) + "\n").encode()
                    write(path.with_suffix(".txt"), text)
                    item.update({"finalUrl": final, "capturedAt": datetime.now(timezone.utc).isoformat(), "localRawCapture": str(path), "rawSha256": sha(raw), "rawBytes": len(raw), "textSha256": sha(text)})
                except (OSError, UnicodeError) as error:
                    item["error"] = repr(error)
                captures.append(item)
                guard.check()
        write(OUT / "external-bindings.json", {"captures": captures, "fullCapturesLocalOnly": True})
        print(json.dumps({"supports": supports, "families": len(families), "captures": len(captures), "failures": [c for c in captures if "error" in c]}, ensure_ascii=False))
    finally:
        write(OUT / "memory.json", guard.finish())


if __name__ == "__main__":
    main()

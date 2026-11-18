"""Prepare complete, explicitly bounded publisher sections for B133 confirmations."""
import json
import xml.etree.ElementTree as ET
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, start_guard, write_frozen

ROOT = WS / "scratch-133"
SOURCE = ROOT / "source-reconciliation-001"
OUT = ROOT / "review" / "confirmation-sources-002"
INVENTORY_SHA = "771407a30005890503babae922f454e672f1d92ee504111bd83a7974960d4eb7"
D, N, J, W = ("デジタル大辞泉", "精選版 日本国語大辞典", "普及版 字通",
              "改訂新版　世界大百科事典")
SECTIONS = {
    "鉱": [D, N, J], "粗金": [D, N], "鉄": [D, N], "金": [N], "鉄砲": [N],
    "速": [D], "早い": [D], "似": [D, N], "似せる": [N], "具": [D, N],
    "岩": [D], "巌": [J], "機": [D], "糸": [D, N], "緒": [D],
    "線": [D, J], "索": [D], "遅": [D], "円": [N], "倣": [D],
    "声": [D], "険": [D], "激": [J], "液": [D], "急": [J], "器": [D],
    "琴": [D, N, J], "鉛": [D, N, J], "滝": [D, N, J, W],
}


def sections(raw, requested):
    lines = raw.decode("utf-8").splitlines(keepends=True)
    selected = []
    for publisher in requested:
        starts = [i for i, line in enumerate(lines) if line.strip() == publisher]
        require(len(starts) == 1, "Missing or ambiguous publisher: " + publisher)
        first = starts[0]
        last = next(i for i in range(first + 1, len(lines)) if lines[i].startswith("出典"))
        selected.append((first + 1, last + 1, publisher, "".join(lines[first:last + 1]).encode("utf-8")))
    return sorted(selected)


def canonical(node):
    return (node.tag, tuple(sorted(node.attrib.items())), (node.text or "").strip(),
            tuple(canonical(child) for child in node))


def main():
    require(not OUT.exists(), "Preserve existing source preparation")
    inventory = json.loads(frozen(SOURCE / "inventory.json", INVENTORY_SHA))
    by_name = {row["relativePath"]: row for row in inventory["files"]}
    guard, _ = start_guard("B133 bounded confirmation sources")
    refs, mappings = [], []
    try:
        for char, publishers in SECTIONS.items():
            folder = "reused-captures" if char in "琴鉛滝" else "captures"
            name = str(Path(folder) / (char + "-kotobank.txt"))
            original = by_name[name]
            raw = frozen(SOURCE / name, original["sha256"])
            body, spans = [], []
            for first, last, publisher, selected in sections(raw, publishers):
                header = (f"Complete publisher section: {publisher}\n"
                          f"Original capture: {name}; SHA256 {original['sha256']}; "
                          f"original lines {first}-{last}.\n").encode("utf-8")
                body.append(header + selected + b"\n")
                spans.append({"publisher": publisher, "firstLine": first, "lastLine": last,
                              "bytes": len(selected), "sha256": sha(selected)})
            output = OUT / "external" / (char + "-extract.txt")
            ref = write_frozen(output, b"".join(body))
            refs.append({"source": "evidence/external/" + output.name, **ref})
            mappings.append({"character": char, "original": original, "sections": spans, "output": ref})
            guard.check()
        entries = {}
        for name in ("jmdict-complete-families.xml", "jmdict-supplement-complete-families.xml"):
            raw = frozen(SOURCE / name, by_name[name]["sha256"])
            for entry in ET.fromstring(raw):
                key = entry.findtext("ent_seq")
                require(key not in entries or canonical(entries[key]) == canonical(entry),
                        "Overlapping source family differs")
                entries[key] = entry
        chosen = [node for key, node in entries.items()
                  if key == "1736440" or {"丸", "円"} <= {
                      element.text for element in node.findall("./k_ele/keb")}]
        require(len(chosen) == 2, "Expected lead-mine family and the complete money/round family")
        for entry in chosen:
            for node in entry.iter():
                if node.text is not None and not node.text.strip():
                    node.text = None
                if node.tail is not None and not node.tail.strip():
                    node.tail = None
        data = b"<JMdict>\n" + b"\n".join(ET.tostring(node, encoding="utf-8") for node in chosen) + b"\n</JMdict>\n"
        require([canonical(node) for node in ET.fromstring(data)] == [canonical(node) for node in chosen],
                "Complete selected family serialization differs")
        ref = write_frozen(OUT / "jmdict-families.xml", data)
        refs.append({"source": "evidence/jmdict-families.xml", **ref})
        record = {
            "batch": 133, "sourceInventorySha256": INVENTORY_SHA,
            "sources": refs, "publisherSelections": mappings,
            "jmdictFamilies": [node.findtext("ent_seq") for node in chosen],
            "scope": "Complete named publisher sections, not full Kotobank pages. Every sense/example "
                     "inside each selected section is retained. The complete regional waterfall "
                     "encyclopedia section is included. Two complete referenced JMdict families.",
            "limits": [
                "Other publishers/encyclopedias, HTML/layout and image glyphs are not supplied in this delta chain.",
                "Original captures, source verification and all failed attempts remain frozen locally.",
                "No fresh KANJIDIC2 or whole JMdict reread; unchanged metadata/readings are carried through "
                "the signed revision proof and original reviews, not newly accepted from these sections.",
                "Selected publisher sections support the finite 18 direct comparisons plus disclosed "
                "lead/implement cross-pair; no universal semantic-negative claim.",
            ],
        }
        freeze_json(OUT / "index.json", record)
        print(json.dumps({"path": str(OUT / "index.json"), "sha256": sha(frozen(OUT / "index.json")),
                          "sources": len(refs), "bytes": sum(row["bytes"] for row in refs),
                          "jmdictFamilies": record["jmdictFamilies"]}))
    finally:
        require(not guard.finish()["breach"], "Confirmation-source preparation RAM breach")


if __name__ == "__main__":
    main()

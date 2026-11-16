import copy
import gzip
import hashlib
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from recon_common import BASE, HERE, ORIGINAL, PACKET, PARENT, REPO, ROOT, SCRATCH, git, sha, start_guard, write

QUERIES = {
    "刃", "刃物", "声", "差", "差す", "差し", "房", "案", "案ずる", "横",
    "鋭", "鋭い", "鋭利", "響", "響く", "響き", "鳴", "鳴く", "鳴る", "鳴らす",
    "危", "危ない", "危うい", "危ぶむ", "危険", "在", "在る", "郊", "郊外", "近郊",
    "騒", "騒ぐ", "騒ぎ", "騒がしい", "騒々しい", "騒音", "物騒", "叫", "叫ぶ", "絶叫",
    "咲", "咲く", "巧笑", "巧咲", "花", "唇", "脣", "唇音", "驚く", "驚かす",
}
CHARACTERS = list("刃声差房案横鋭響鳴危在郊騒叫咲唇")


def canonical(node):
    return ET.canonicalize(ET.tostring(node, encoding="unicode"), strip_text=True)


class HashReader:
    def __init__(self, stream, guard):
        self.stream, self.guard, self.digest = stream, guard, hashlib.sha256()

    def read(self, size=-1):
        self.guard.check()
        raw = self.stream.read(size)
        self.digest.update(raw)
        return raw


def main():
    guard = start_guard()
    try:
        assert git("rev-parse", "HEAD").decode().strip() == PARENT
        assert not git("status", "--porcelain=v1", "--untracked-files=all")
        assert not PACKET.exists()
        receipt = json.loads((ORIGINAL / "source-receipt.json").read_text(encoding="utf-8"))
        proof = json.loads((ORIGINAL / "packet-files-002.json").read_text(encoding="utf-8"))
        for path, info in proof["files"].items():
            guard.check()
            assert sha((ORIGINAL / path).read_bytes()) == info["sha256"]
        records, source_bindings, memberships = {}, {}, {q: [] for q in sorted(QUERIES)}
        memberships["reading=ほとり"] = []
        for label, tag, identifier in (("jmdict", "entry", "ent_seq"), ("kanjidic2", "character", "literal")):
            info = receipt["dictionaryInputs"][label]
            path = ROOT / "control" / "inputs" / info["filename"]
            digest = hashlib.sha256()
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(65536), b""):
                    guard.check()
                    digest.update(chunk)
            assert digest.hexdigest() == info["compressedSha256"]
            selected, canonical_hashes = [], {}
            with gzip.open(path, "rb") as stream:
                reader = HashReader(stream, guard)
                context = ET.iterparse(reader, events=("start", "end"))
                _, root = next(context)
                for event, node in context:
                    if event != "end" or node.tag != tag:
                        continue
                    key = node.findtext(identifier)
                    if label == "jmdict":
                        matched = QUERIES & {k.text for k in node.findall("k_ele/keb")}
                        if "ほとり" in {r.text for r in node.findall("r_ele/reb")}:
                            matched.add("reading=ほとり")
                        for query in matched:
                            memberships[query].append(key)
                    else:
                        matched = key in CHARACTERS
                    if matched:
                        selected.append(copy.deepcopy(node))
                        canonical_hashes[key] = sha(canonical(node).encode("utf-8"))
                    node.clear()
                    root.clear()
            assert reader.digest.hexdigest() == info["decompressedXmlSha256"]
            root = ET.Element("JMdict" if label == "jmdict" else "kanjidic2")
            root.extend(selected)
            ET.indent(root, space="  ")
            raw = ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"
            filename = label + "-complete-records.xml"
            write(PACKET / filename, raw)
            assert {n.findtext(identifier): sha(canonical(n).encode("utf-8")) for n in ET.fromstring(raw).findall(tag)} == canonical_hashes
            source_bindings[label] = {
                "filename": info["filename"], "compressedSha256": digest.hexdigest(),
                "decompressedXmlSha256": reader.digest.hexdigest(), "records": len(selected),
                "output": filename, "outputSha256": sha(raw), "canonicalCompleteRecordHashes": canonical_hashes,
                "transformation": "Complete parsed/reserialized records, not raw compressed-file slices. No spelling, reading, priority, sense, restriction or metadata filtering.",
            }
            if label == "jmdict":
                records = {n.findtext("ent_seq"): n for n in selected}
        assert len(source_bindings["kanjidic2"]["canonicalCompleteRecordHashes"]) == 16
        for char in CHARACTERS:
            write(PACKET / "comparison-cards" / (char + ".md"), git("show", f"{PARENT}:kanji/{char}.md"))
        write(PACKET / "selector-membership.json", {
            "exactKebOrRebQueries": memberships, "kanjidic2LiteralSelectors": CHARACTERS,
            "allMatchingFamiliesIncluded": True, "selectorRule": "Any exact k_ele/keb match, or r_ele/reb=ほとり; include entire matching family without sense filtering.",
        })
        write(PACKET / "source-receipt.json", {
            "parentCommit": PARENT, "publishedBase": BASE, "membership": [{"kanji": "唇", "sourceRow": 159}],
            "dictionaryInputs": source_bindings,
            "existingSources": {name: {"path": "../batch-128/" + name, "sha256": sha((ORIGINAL / name).read_bytes())} for name in (
                "source-receipt.json", "complete-source-verification-002.json", "external-source-bindings.json",
                "baseline-gloss-scan.json", "baseline-gloss-scan-002.json", "pair-dispositions.json", "stroke-font-evidence.json")},
            "completeSelection": "selector-membership.json", "producerSha256": sha(Path(__file__).read_bytes()),
            "license": "JMdict and KANJIDIC2: EDRDG, CC BY-SA 4.0. https://www.edrdg.org/edrdg/licence.html",
        })
        for offset in range(0, len(records), 16):
            part = list(records.values())[offset:offset + 16]
            lines = [ET.tostring(n, encoding="unicode") for n in part]
            write(SCRATCH / f"reconciliation-record-readback-{offset // 16 + 1:02d}.txt", "\n".join(lines).encode("utf-8"))
        print(json.dumps({"records": {k: v["records"] for k, v in source_bindings.items()}, "queries": memberships}, ensure_ascii=False))
    finally:
        write(SCRATCH / "reconciliation-extraction-memory-001.json", guard.finish())


if __name__ == "__main__":
    main()

import copy
import gzip
import hashlib
import json
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from html.parser import HTMLParser
from b129_common import BASE, CHARS, HERE, PACKET, REPO, ROOT, git, sha, start_guard, write

INPUTS = {
    "jmdict": ("n1-implementation-JMdict_e.gz", "2dbbfe0b1214911766bbc128a0935618b925be917e7d1c50f3536a89b0e8786d", "107079c692f2e49c08d45da1da227b7e021298f247d16578b44dfaa2ec9002c4", "entry"),
    "kanjidic2": ("n1-planning-kanjidic2.xml.gz", "af0a499d62ac4413c614adcca360e2306490c3f64fccb3510fc7caa15f901bed", "9a000ef112b4bad8f1e6e3ca1f8e9f73ed84c93a5eae93dadfa1513081dc5db8", "character"),
}
KEYWORDS = {
    "茉": "jasmine jasmin flower flowers blossom blossoms bloom blooms plant plants shrub shrubs",
    "絹": "silk silks silken textile textiles cloth cloths fabric fabrics clothing clothes garment garments thread threads fiber fibre",
    "羊": "sheep ram rams ewe ewes lamb lambs flock flocks goat goats wool fleece zodiac sacrifice sacrifices animal animals",
    "虹": "rainbow rainbows iridescent arc arcs bridge bridges bow bows bride brides beauty beautiful dragon dragons snake snakes",
    "霜": "frost frosts ice icy freeze freezes freezing frozen cold chill chilly snow white whiteness grey gray hair hairs year years age aged autumn winter hardship hardships suffering adversity dew crystallize crystals crystalline powder powdered",
}
EXACT = {"茉莉花", "茉莉", "絹", "虹", "霓", "綿", "織", "布", "衣", "服", "橋", "弓", "蛇", "竜", "花", "咲", "莉"}
READINGS = {"まつり", "きぬ", "にじ"}


class HashReader:
    def __init__(self, stream, guard):
        self.stream, self.guard, self.digest = stream, guard, hashlib.sha256()

    def read(self, size=-1):
        self.guard.check()
        chunk = self.stream.read(size)
        self.digest.update(chunk)
        return chunk


def canonical(node):
    return ET.canonicalize(ET.tostring(node, encoding="unicode"), strip_text=True)


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


def main():
    guard = start_guard()
    try:
        assert git("rev-parse", "HEAD").decode().strip() == BASE
        assert not git("status", "--porcelain=v1", "--untracked-files=all")
        assert git("remote", "get-url", "origin").decode().strip() == "https://github.com/stop-cran/learning-japanese.git"
        assert git("config", "user.email").decode().strip() == "stop-cran@list.ru"
        assert git("config", "user.signingkey").decode().strip() == "D4C9A275A218AF747B787AFA9D94B9D311BD26A7"
        assert not PACKET.exists()
        index_raw = git("show", f"{BASE}:docs/n1-sources/source-index.json")
        community_raw = git("show", f"{BASE}:docs/n1-sources/community-list-20261102.json")
        assert sha(index_raw) == "0d517145b92c19ea4a17ba5aa9ca12c18f408001fdc01f0f7bb1a99659bbe1dd"
        assert sha(community_raw) == "889faaefbec573e806f298766d2eee1300674c7b229bd973a35169cd2652cd73"
        index = {r["kanji"]: r for r in json.loads(index_raw)}
        for ch in CHARS:
            row = index[ch]
            assert row["statusAtFreeze"] == "pending" and json.loads(community_raw)[row["sourceRow"] - 1] == ch
            assert not (REPO / row["article"]).exists() and not (REPO / row["strokeFile"]).exists()
        write(PACKET / "source-rows.json", [index[ch] for ch in CHARS])
        supports = {}
        for path in sorted((REPO / "words").glob("*.md")):
            text = path.read_text(encoding="utf-8")
            match = re.search(r"^kanji: \[([^\]]*)\]$", text, re.M)
            if not match:
                continue
            for ch in CHARS:
                if ch in [p.strip() for p in match.group(1).split(",")]:
                    supports.setdefault(ch, []).append(path.stem)
                    write(PACKET / "baseline-words" / path.name, git("show", f"{BASE}:words/{path.name}"))
        assert supports == {"絹": ["絹"], "茉": ["茉莉花"], "虹": ["虹"]}
        write(PACKET / "selection.json", {
            "batch": "129", "base": BASE, "members": [{"kanji": ch, "row": index[ch]["sourceRow"]} for ch in CHARS],
            "allDeclaredSupportArticles": supports, "requiredReciprocalPairs": [[ch, w] for ch in CHARS for w in supports[ch]],
            "selectionReason": "Three missing members with one verified existing support each. A complete five-member survey reached 153 comparison cards; split 羊 and 霜 before teaching authoring because their standalone/historical senses exceeded one bounded review packet. Preserve that survey under scratch-129/planning-001; no claim it closes those rows.",
            "deferred": [{"kanji": "伯", "row": 33, "reason": "伯母さん does not establish ハク."}, {"kanji": "憶", "row": 395, "reason": "Remember/think comparison evidence remains unresolved."}, {"kanji": "撲", "row": 461, "reason": "相撲 does not establish ボク."}],
            "notSelected": ["皇", "耗", "衛", "塀", "拍", "桜", "羊", "霜"],
            "deliveredAtBase": 258, "undeliveredAtBase": 970,
        })
        records, inputs, memberships = {}, {}, {}
        for name, (filename, compressed_sha, xml_sha, tag) in INPUTS.items():
            path = ROOT / "control" / "inputs" / filename
            digest = hashlib.sha256()
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(65536), b""):
                    guard.check()
                    digest.update(chunk)
            assert digest.hexdigest() == compressed_sha
            selected = {}
            with gzip.open(path, "rb") as stream:
                reader = HashReader(stream, guard)
                context = ET.iterparse(reader, events=("start", "end"))
                _, root = next(context)
                for event, node in context:
                    if event != "end" or node.tag != tag:
                        continue
                    if name == "jmdict":
                        eid = node.findtext("ent_seq")
                        kebs = {k.text for k in node.findall("k_ele/keb")}
                        rebs = {r.text for r in node.findall("r_ele/reb")}
                        predicates = [f"contains:{ch}" for ch in [*CHARS, "霓"] if any(ch in k for k in kebs)]
                        predicates += [f"exact-spelling:{k}" for k in sorted(EXACT & kebs)]
                        predicates += [f"exact-reading:{r}" for r in sorted(READINGS & rebs)]
                        if predicates:
                            selected[eid] = copy.deepcopy(node)
                            memberships[eid] = predicates
                    else:
                        selected[node.findtext("literal")] = copy.deepcopy(node)
                    node.clear()
                    root.clear()
            assert reader.digest.hexdigest() == xml_sha
            records[name] = selected
            inputs[name] = {"filename": filename, "compressedSha256": compressed_sha, "decompressedSha256": xml_sha}
        kd = records["kanjidic2"]
        scans, comparisons = {}, set("古右石")
        old_manifest = json.loads(git("show", f"{BASE}:manifest.json"))
        baseline_paths = [p for p in old_manifest["files"] if p.startswith("kanji/")]
        assert len(baseline_paths) == 1248
        for ch in CHARS:
            row, keywords = index[ch], set(KEYWORDS[ch].split())
            meanings = [m.text for m in kd[ch].findall("reading_meaning/rmgroup/meaning") if m.get("m_lang") in (None, "en")]
            assert meanings == row["metadata"]["meanings"]
            for kind in ("on", "kun"):
                assert [r.text for r in kd[ch].findall(f"reading_meaning/rmgroup/reading[@r_type='ja_{kind}']")] == row["metadata"][kind + "yomi"]
            literal = set(re.findall("[a-z]+", " ".join(meanings).lower()))
            keywords |= literal
            scan_rows = []
            for path in sorted(baseline_paths):
                char = path.split("/")[-1][:-3]
                raw = git("show", f"{BASE}:{path}")
                title = re.search(r"^title: (.+)$", raw.decode().replace("\r\n", "\n"), re.M).group(1)
                full = [m.text for m in kd[char].findall("reading_meaning/rmgroup/meaning") if m.get("m_lang") in (None, "en")]
                hits = sorted(keywords & set(re.findall("[a-z]+", " ".join([title, *full]).lower())))
                scan_rows.append({"kanji": char, "path": path, "baselineBytesSha256": sha(raw), "title": title, "completeMeanings": full, "matchedKeywords": hits})
                if hits:
                    comparisons.add(char)
            scans[ch] = {"base": BASE, "kanji": ch, "literalKeywords": sorted(literal), "expandedKeywords": sorted(keywords), "tokenRegex": "[a-z]+", "rows": scan_rows, "matches": [r["kanji"] for r in scan_rows if r["matchedKeywords"]], "limits": "Complete displayed-title and KANJIDIC2 English-meaning token scan; not exhaustive synonym discovery. External positive senses motivate expanded terms."}
            write(PACKET / "scans" / (ch + ".json"), scans[ch])
        for ch in sorted(comparisons):
            write(PACKET / "comparison-cards" / (ch + ".md"), git("show", f"{BASE}:kanji/{ch}.md"))
        verification = {}
        for filename, source, chosen in [
            ("jmdict-complete-families.xml", "jmdict", list(records["jmdict"].values())),
            ("kanjidic2-target-records.xml", "kanjidic2", [kd[ch] for ch in CHARS]),
            ("kanjidic2-comparison-records.xml", "kanjidic2", [kd[ch] for ch in sorted(comparisons)]),
        ]:
            root = ET.Element("JMdict" if source == "jmdict" else "kanjidic2")
            root.extend(copy.deepcopy(chosen))
            ET.indent(root, space="  ")
            raw = ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"
            write(PACKET / filename, raw)
            originals = {n.findtext("ent_seq") or n.findtext("literal"): sha(canonical(n).encode()) for n in chosen}
            actual = {n.findtext("ent_seq") or n.findtext("literal"): sha(canonical(n).encode()) for n in ET.fromstring(raw)}
            assert originals == actual
            verification[filename] = {"source": source, "sha256": sha(raw), "bytes": len(raw), "completeCanonicalEquality": True, "canonicalRecordHashes": actual}
        write(PACKET / "query-membership.json", memberships)
        write(PACKET / "complete-source-verification.json", verification)
        svgs = {}
        for ch in CHARS:
            row = index[ch]
            url = "https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/" + row["kanjivgInventory"]["path"]
            with urllib.request.urlopen(url, timeout=30) as response:
                raw = response.read()
            guard.check()
            blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
            assert blob == row["kanjivgInventory"]["sha"] and len(raw) == row["kanjivgInventory"]["size"]
            filename = f"{ord(ch):05x}.svg"
            write(PACKET / "kanjivg" / filename, raw)
            svgs[ch] = {"url": url, "file": "kanjivg/" + filename, "gitBlob": blob, "sha256": sha(raw)}
        write(PACKET / "source-receipt.json", {
            "batch": "129", "base": BASE, "createdAt": datetime.now(timezone.utc).isoformat(),
            "indexSha256": sha(index_raw), "communitySha256": sha(community_raw), "dictionaryInputs": inputs,
            "predicate": "Union of every complete JMdict family whose any k_ele/keb contains 茉, 絹, 虹 or variant 霓; complete exact-spelling and exact-reading families explicitly listed by entry in query-membership.json. No priority/sense/rarity filtering.",
            "transformation": "Complete parsed/reserialized XML records, not raw source slices; canonical field equality checked against original decompressed stream.",
            "outputs": verification, "kanjivg": svgs, "kanjivgRevision": "70a0b7ae0c18ceb5cb358274b029cce0234a43bc",
            "dictionaryAttribution": "Copyright James William Breen and EDRDG, CC BY-SA 4.0.",
            "kanjivgAttribution": "Copyright Ulrich Apel and contributors, CC BY-SA 3.0.",
            "producerSha256": sha(__import__("pathlib").Path(__file__).read_bytes()),
        })
        print(json.dumps({"families": len(records["jmdict"]), "comparisons": len(comparisons), "scans": {ch: [{"kanji": r["kanji"], "title": r["title"], "meanings": r["completeMeanings"], "matched": r["matchedKeywords"]} for r in scan["rows"] if r["matchedKeywords"]] for ch, scan in scans.items()}}, ensure_ascii=False, indent=2))
    finally:
        write(HERE / "extraction-memory-002.json", guard.finish())


if __name__ == "__main__":
    main()

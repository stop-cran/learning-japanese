"""Build projected-successor-011: the 008 core with dictionary XML encoded and canonical JSON minified, losslessly."""
import json
import sys
from pathlib import Path

from common import WS, json_bytes, require, sha, start_guard, write_frozen
import compact_xml_v1 as codec

ROOT = WS / "scratch-134" / "review" / "fresh-independent-002"
PRED = ROOT / "projected-successor-008"
OUT = ROOT / "projected-successor-011"
PRED_PACKET_SHA = "6f774ec7906cbe8279e972959507d8ccbbea8541273f8cfa51a405dc34fcc5f6"
PRED_CORE_SHA = "b6e49cbbcb6ebab5886dc87b9cf9557a4b213fda5d3c3b0c7c6ff3f7c18c76b8"
CODEC_INDEX_SHA = "274bedd21e6d2fa754b90f9cd350dbacb651f52ebe6e283434420d7e15f977b8"
sys.path.insert(0, str(PRED / "protocol-003"))
from review_chain_with_optional import build_chain  # noqa: E402

GUIDE = "evidence/lossless-core-representation-guide.md"
ENCODED = {
    "evidence/jmdict-families.xml": (
        "evidence/jmdict-families.compact-xml-v1.txt",
        dict(root="JMdict", record="entry", separator=1,
             aliases=["#=ent_seq", "K=k_ele", "R=r_ele", "S=sense", "g=gloss[xml:lang=eng]",
                      "kp=ke_pri", "rp=re_pri", "ki=ke_inf", "ri=re_inf"],
             bare={"k_ele": "keb", "r_ele": "reb"})),
    "evidence/kanjidic2-review-projection.xml": (
        "evidence/kanjidic2-review-projection.compact-xml-v1.txt",
        dict(root="kanjidic2", record="character", separator=2,
             aliases=["rad=rad_value[rad_type=classical]", "on=reading[r_type=ja_on]",
                      "kun=reading[r_type=ja_kun]", "m=meaning"],
             bare={"character": "literal"})),
}
EXAMPLE_SOURCE = "evidence/jmdict-families.xml"


def real_example(original, encoded):
    """Pick the shortest real record showing aliases, a bare child and an explicit attribute tag."""
    xml_lines = original.decode("utf-8").split("\n")[1:-2]
    lines = encoded.decode("utf-8").split("%end\n", 1)[1].split("\n")[:-1]
    require(len(xml_lines) == len(lines), "Encoded records do not align with original record lines")
    _, index = min((len(line), i) for i, line in enumerate(lines) if "gloss[" in line and "| rp=" in line)
    return index + 1, lines[index], xml_lines[index]


def minified(raw):
    """Return the minified form of canonical 2-space JSON, or None when the file is not canonical."""
    value = json.loads(raw)
    if json_bytes(value) != raw:
        return None
    small = (json.dumps(value, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
    require(json_bytes(json.loads(small)) == raw and len(small) < len(raw), "Minified JSON is not invertible")
    return small


def minified_name(name):
    return name[:-len(".json")] + ".min.json"


def guide(json_count, original, encoded):
    number, example_line, example_xml = real_example(original, encoded)
    rows = "\n".join(f"- `{new}` encodes `{old}` (original bytes remain in this packet)."
                     for old, (new, _) in ENCODED.items())
    return f"""# Lossless core representation guide

Some sources of this review core are presented in a shorter but exactly invertible form, used
only to fit the complete sources into the review context. Nothing was selected, removed,
reordered, normalized or summarized, and every original file remains in this packet with its
SHA-256 in `SHA256SUMS.json`. Two representations are used.

## 1. Minified JSON (`*.min.json`)

`X.min.json` is the JSON value of the packet file `X.json` written without insignificant
whitespace. All {json_count} core JSON files that were stored as canonical 2-space-indented
JSON are presented this way; any other JSON file appears unchanged. Keys, key order, strings and
numbers are identical: the original bytes are exactly
`json.dumps(value, ensure_ascii=False, indent=2) + "\\n"`, which was checked for every file
before this core was frozen.

## 2. compact-xml-v1 dictionary records

{rows}

Each encoded file's header states the SHA-256 and byte length of its original XML file. Before
this core was frozen, the mechanical decoder (`codec/compact_xml_v1.py` in this packet)
rebuilt both original files byte-for-byte from the encoded files alone.

### Header (lines up to `%end`)

- `%root` / `%record`: the XML root element and the per-line record element.
- `%separator N`: records were separated by N newlines in the original file.
- `%alias SHORT=tag[attr=value,...]`: SHORT stands for exactly that tag with exactly those
  attributes in that order. An alias without brackets has no attributes.
- `%bare parent=child`: the first child of `parent` is written as plain text without its tag.

### Body

- One record per line, in original order. The record's child elements are separated by ` ¦ `.
- `name=value` is an element containing only text (`name=` is an empty element).
- `name a | b | c` (a space after the name) is a record-level element whose child elements
  are a, b and c, separated by ` | `.
- `name{{a | b}}` is a deeper element whose child elements are a and b.
- A tag written as `tag[k=v,...]` carries those attributes in that order; it is not an alias.
- Values are literal text: no escaping is used, and spaces, `;`, parentheses and quotes are
  part of the value.

### Example (a real record, repeated here verbatim from both files)

Record {number} (line {number} after `%end`) of `{ENCODED[EXAMPLE_SOURCE][0]}`:

`{example_line}`

is exactly XML line {number + 1} of `{EXAMPLE_SOURCE}`:

`{example_xml}`
"""


def main():
    require(not OUT.exists(), "projected-successor-011 already exists; preserve it")
    index_raw = (WS / "scratch-134" / "review" / "continuation-tools-004" / "index.json").read_bytes()
    require(sha(index_raw) == CODEC_INDEX_SHA, "Codec freeze index changed")
    index = json.loads(index_raw)
    codec_raw = Path(codec.__file__).read_bytes()
    require(sha(codec_raw) == index["files"]["compact_xml_v1.py"]["sha256"], "Codec differs from its freeze")
    sums_raw = (PRED / "packet" / "SHA256SUMS.json").read_bytes()
    require(sha(sums_raw) == PRED_PACKET_SHA, "Predecessor packet inventory changed")
    sums = json.loads(sums_raw)
    core_raw = (PRED / "fresh-independent-core-001.json").read_bytes()
    require(sha(core_raw) == PRED_CORE_SHA, "Predecessor core manifest changed")
    pred_names = [row["source"] for row in json.loads(core_raw)["sources"]]
    require(len(pred_names) == 89 and all(name in pred_names for name in ENCODED), "Unexpected predecessor core")
    guard, _ = start_guard("B134 successor-011 lossless core construction")
    try:
        packet = {}
        for name, digest in sums.items():
            raw = (PRED / "packet" / name).read_bytes()
            require(sha(raw) == digest, "Predecessor packet file differs: " + name)
            packet[name] = raw
            guard.check()
        on_disk = {p.relative_to(PRED / "packet").as_posix() for p in (PRED / "packet").rglob("*") if p.is_file()}
        require(on_disk == set(sums) | {"SHA256SUMS.json"}, "Unlisted predecessor packet file")
        added = {"codec/compact_xml_v1.py": codec_raw}
        conversions = {}
        for old, (new, config) in ENCODED.items():
            encoded = codec.encode(packet[old], **config)
            require(codec.decode(encoded) == packet[old], "Encoded source does not decode exactly: " + old)
            added[new] = encoded
            conversions[old] = {"representation": "compact-xml-v1", "converted": new, "config": config,
                                "originalSha256": sha(packet[old]), "originalBytes": len(packet[old]),
                                "convertedSha256": sha(encoded), "convertedBytes": len(encoded)}
        unchanged_json = []
        for old in pred_names:
            if not old.endswith(".json"):
                continue
            small = minified(packet[old])
            if small is None:
                unchanged_json.append(old)
                continue
            added[minified_name(old)] = small
            conversions[old] = {"representation": "minified-canonical-json", "converted": minified_name(old),
                                "originalSha256": sha(packet[old]), "originalBytes": len(packet[old]),
                                "convertedSha256": sha(small), "convertedBytes": len(small)}
        json_count = len(conversions) - len(ENCODED)
        require(json_count == 42 and unchanged_json == ["snapshot/strokes/紫.json"],
                "Canonical JSON population differs from the measured predecessor")
        added[GUIDE] = guide(json_count, packet[EXAMPLE_SOURCE],
                             added[ENCODED[EXAMPLE_SOURCE][0]]).encode("utf-8")
        require(not set(added) & set(packet), "New packet file would replace a predecessor file")
        new_sums = dict(sums)
        for name, raw in {**packet, **added}.items():
            write_frozen(OUT / "packet" / name, raw)
            guard.check()
        for name, raw in added.items():
            new_sums[name] = sha(raw)
        sums_ref = write_frozen(OUT / "packet" / "SHA256SUMS.json", json_bytes(new_sums))
        names = []
        for name in pred_names:
            names.append(conversions[name]["converted"] if name in conversions else name)
            if name == "REVIEW.md":
                names.append(GUIDE)
        require(names[:2] == ["REVIEW.md", GUIDE] and len(names) == 90 and len(set(names)) == 90,
                "Successor source list is malformed")
        sources_ref = write_frozen(OUT / "core-sources-011.json", json_bytes(
            {"predecessorCoreSha256": PRED_CORE_SHA, "sources": names}))
        core_path = OUT / "fresh-independent-core-001.json"
        core = build_chain([(name, (packet | added)[name], None) for name in names],
                           OUT / "chains" / "fresh-independent-core-001", core_path, guard,
                           "B134 fresh independent core successor 011")
        require([row["source"] for row in core["sources"]] == names, "Chain source order differs")
        payload = sum(len((packet | added)[name]) for name in names)
        chain = sum(row["bytes"] for row in core["segments"])
        write_frozen(OUT / "tools" / "build_b134_successor_011.py", Path(__file__).read_bytes())
        result = {
            "status": "FROZEN_LOSSLESS_SUCCESSOR_CORE_NOT_REVIEW_ADMISSION",
            "predecessor": {"root": str(PRED), "packetSha256": PRED_PACKET_SHA, "coreSha256": PRED_CORE_SHA},
            "codecFreezeIndexSha256": CODEC_INDEX_SHA, "codecSha256": sha(codec_raw),
            "conversions": conversions, "unchangedJsonSources": unchanged_json,
            "addedPacketFiles": {k: sha(v) for k, v in added.items()},
            "packetInventory": {**sums_ref, "files": len(new_sums)},
            "sourceList": sources_ref,
            "coreManifest": {"path": str(core_path), "sha256": sha(core_path.read_bytes())},
            "sourceCount": len(core["sources"]), "segmentCount": len(core["segments"]),
            "payloadBytes": payload, "chainBytes": chain,
            "producerSha256": sha(Path(__file__).read_bytes()),
            "limits": "Lossless representation change only; every predecessor packet file retained byte-exactly. "
                      "No tokenizer measurement, capacity admission, semantic review, lifecycle or reviewer launch.",
        }
    finally:
        memory = guard.finish()
        require(not memory["breach"], "Successor construction RAM breach")
    result["memory"] = memory
    print(json.dumps(write_frozen(OUT / "frozen-core-011.json", json_bytes(result)), ensure_ascii=False))
    print(json.dumps({k: result[k] for k in ("sourceCount", "segmentCount", "payloadBytes", "chainBytes")}))


if __name__ == "__main__":
    main()

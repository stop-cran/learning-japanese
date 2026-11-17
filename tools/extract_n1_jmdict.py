#!/usr/bin/env python3
"""Extract complete selected families from the pinned N1 implementation JMdict.

``--pin frozen`` (default) checks the 2026-11-02 file in docs/n1-source-snapshot.json;
``--pin continuation`` checks the later file in docs/n1-sources/continuation-inputs.json.
"""
import argparse
import gzip
import hashlib
import json
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PINS = {
    "frozen": (Path("docs") / "n1-source-snapshot.json", "n1-implementation-JMdict_e.gz"),
    "continuation": (Path("docs") / "n1-sources" / "continuation-inputs.json", "n1-continuation-JMdict_e.gz"),
}


def pinned_hash(pin, root=ROOT):
    if pin not in PINS:
        raise ValueError(f"Unknown JMdict pin: {pin}")
    path, key = PINS[pin]
    return json.loads((root / path).read_text(encoding="utf-8"))["inputs"][key]["sha256"]


def extract(raw, expected_hash, entry_ids):
    if hashlib.sha256(raw).hexdigest() != expected_hash:
        raise ValueError("Pinned JMdict compressed hash mismatch")
    if not entry_ids or len(entry_ids) != len(set(entry_ids)):
        raise ValueError("Select nonempty distinct JMdict entry IDs")
    source = ET.fromstring(gzip.decompress(raw))
    families = {e.findtext("ent_seq"): e for e in source.findall("entry")}
    missing = set(entry_ids) - families.keys()
    if missing:
        raise ValueError(f"Missing JMdict entries: {sorted(missing)}")
    selected = ET.Element("JMdict")
    for entry_id in entry_ids:
        selected.append(families[entry_id])
    ET.indent(selected, space="  ")
    return ET.tostring(selected, encoding="utf-8", xml_declaration=True) + b"\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--selection", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--pin", choices=sorted(PINS), default="frozen")
    args = parser.parse_args()
    selection = json.loads(args.selection.read_text(encoding="utf-8"))
    result = extract(args.input.read_bytes(), pinned_hash(args.pin), selection["entryIds"])
    if args.output.exists():
        if args.output.read_bytes() != result:
            raise ValueError(f"Different evidence already exists: {args.output}")
    elif args.check:
        raise ValueError(f"Missing evidence: {args.output}")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(result)
    print(f"Verified {len(selection['entryIds'])} complete JMdict families"
          + (" (check only)." if args.check else "."))


if __name__ == "__main__":
    main()

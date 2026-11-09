#!/usr/bin/env python3
"""Extract complete payment-comparison families from the already pinned JMdict."""
import argparse
import gzip
import hashlib
import json
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCE_NAME = "n1-implementation-JMdict_e.gz"
SOURCE_SHA256 = "2dbbfe0b1214911766bbc128a0935618b925be917e7d1c50f3536a89b0e8786d"
ENTRY_IDS = ("1230350", "1594480")


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def extract(source):
    snapshot = json.loads((ROOT / "docs" / "n1-source-snapshot.json").read_text(encoding="utf-8-sig"))
    record = snapshot["inputs"][SOURCE_NAME]
    raw_hash = digest(source.read_bytes())
    if raw_hash != SOURCE_SHA256 or raw_hash != record["sha256"] or source.stat().st_size != record["bytes"]:
        raise ValueError("Frozen JMdict source differs from the signed snapshot")
    found = {}
    with gzip.open(source, "rb") as stream:
        for _, element in ET.iterparse(stream, events=("end",)):
            if element.tag == "entry":
                identity = element.findtext("ent_seq")
                if identity in ENTRY_IDS:
                    if identity in found:
                        raise ValueError(f"Duplicate dictionary family: {identity}")
                    found[identity] = ET.tostring(element, encoding="utf-8")
                element.clear()
    if set(found) != set(ENTRY_IDS):
        raise ValueError("Required complete dictionary families are missing")
    output = (b'<?xml version="1.0" encoding="UTF-8"?>\n<JMdict>\n'
              + b"\n".join(found[identity] for identity in ENTRY_IDS) + b"\n</JMdict>\n")
    return output, snapshot


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists() or args.receipt.exists():
        raise FileExistsError("Refusing to overwrite supplemental evidence")
    output, snapshot = extract(args.source)
    receipt = {
        "batch": "107",
        "source": "JMdict, Electronic Dictionary Research and Development Group",
        "sourceSnapshot": "dfed2c150d7fe921aacdb1d616ff527df1935f3b",
        "sourceGzipSha256": SOURCE_SHA256,
        "sourceXmlSha256FromSignedSnapshot": snapshot["jmdict"]["xmlSha256"],
        "entryIds": list(ENTRY_IDS),
        "output": args.output.name,
        "outputSha256": digest(output),
        "outputBytes": len(output),
        "representation": "Complete parsed entry elements, serialized as XML; entity expansion and insignificant whitespace may differ from the original source bytes.",
        "limits": "The original full-source audit verified the decompressed XML hash. This streaming extraction rechecks the full compressed source hash and parses the full dictionary, but does not independently recompute the decompressed hash or retrieve a new upstream source.",
    }
    with args.output.open("xb") as stream:
        stream.write(output)
    with args.receipt.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(receipt, ensure_ascii=True, indent=2) + "\n")
    print(json.dumps(receipt, ensure_ascii=True))

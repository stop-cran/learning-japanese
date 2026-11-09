#!/usr/bin/env python3
"""Reproduce the additional payment-comparison families from the frozen source."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

REVIEW = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("extract107", REVIEW / "extract-supplemental-jmdict.py")
extractor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(extractor)
extractor.ENTRY_IDS = ("1501620", "1411790", "1554280")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    args = parser.parse_args()
    output = REVIEW / "followup-payment-jmdict.xml"
    provenance = REVIEW / "followup-payment-jmdict-provenance.json"
    if output.exists() or provenance.exists():
        raise FileExistsError("Refusing to overwrite additional review evidence")
    raw, snapshot = extractor.extract(args.source)
    receipt = {
        "batch": "107",
        "source": "JMdict, Electronic Dictionary Research and Development Group",
        "sourceSnapshot": "dfed2c150d7fe921aacdb1d616ff527df1935f3b",
        "compressedSourceSha256": extractor.SOURCE_SHA256,
        "decompressedSourceSha256FromSignedSnapshot": snapshot["jmdict"]["xmlSha256"],
        "entryIds": list(extractor.ENTRY_IDS),
        "output": output.name,
        "outputSha256": hashlib.sha256(raw).hexdigest(),
        "outputBytes": len(raw),
        "representation": "Complete parsed entry elements, serialized as XML; entity expansion and insignificant whitespace may differ from original source bytes.",
        "limits": "Pinned compressed hash rechecked; full XML is parsed by streaming. The decompressed hash was established in the separately preserved original source audit, not independently recomputed here.",
    }
    with output.open("xb") as stream:
        stream.write(raw)
    with provenance.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(receipt, ensure_ascii=True, indent=2) + "\n")
    print(json.dumps(receipt, ensure_ascii=True))


if __name__ == "__main__":
    main()

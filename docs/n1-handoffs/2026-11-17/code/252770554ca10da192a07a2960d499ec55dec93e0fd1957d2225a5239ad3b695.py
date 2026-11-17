"""Correct the packet's serialization description for explicit source contracts."""
import hashlib
import json
import stat
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "build-packet-v3.py"
TARGET = ROOT / "build-packet-v4.py"
RECEIPT = ROOT.parent / "scratch-120" / "review" / "packet-builder-derivation.json"
EXPECTED = "48ebd9a122ca90d901c2d7127c7eb87d26a4f60587a87520c434d1179d4b0c0d"


def main():
    raw = SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != EXPECTED:
        raise ValueError("Pinned packet builder changed")
    if TARGET.exists() or RECEIPT.exists():
        raise FileExistsError("Preserve the existing packet-builder derivation")
    before = (
        '"serialization": "Complete JMdict families copied byte for byte from the committed batch evidence. "\n'
        '                             "Not byte-identical compressed-source slices. No author observations or adjudication.",'
    )
    after = (
        '"serialization": (source_contract["method"] if source_contract is not None else\n'
        '                              "Complete JMdict families copied byte for byte from committed batch evidence. "\n'
        '                              "Not byte-identical compressed-source slices. No author observations or adjudication."),'
    )
    newline = "\r\n" if b"\r\n" in raw else "\n"
    before, after = before.replace("\n", newline), after.replace("\n", newline)
    pairs = [(before, after), ("build-packet-v3.py", "build-packet-v4.py")]
    text, counts = raw.decode("utf-8"), []
    for old, new in pairs:
        count = text.count(old)
        if not count or new in text:
            raise ValueError("Ambiguous packet-builder derivation")
        text = text.replace(old, new)
        counts.append({"before": old, "after": new, "count": count})
    reverse = text
    for item in reversed(counts):
        if reverse.count(item["after"]) != item["count"]:
            raise ValueError("Packet-builder reverse count mismatch")
        reverse = reverse.replace(item["after"], item["before"])
    if reverse.encode("utf-8") != raw:
        raise ValueError("Packet-builder reverse proof failed")
    result = text.encode("utf-8")
    compile(result, str(TARGET), "exec")
    proof = {
        "source": str(SOURCE), "sourceSha256": EXPECTED,
        "target": str(TARGET), "targetSha256": hashlib.sha256(result).hexdigest(),
        "reverseExact": True, "substitutions": counts,
        "deriverSha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "scope": "Only the serialization description and builder self-identifiers changed. The explicit source contract now supplies its actual merge/reserialization method rather than claiming byte-copying of committed XML.",
    }
    for path, content in (
        (TARGET, result),
        (RECEIPT, (json.dumps(proof, ensure_ascii=False, indent=2) + "\n").encode("utf-8")),
    ):
        with path.open("xb") as stream:
            stream.write(content)
        path.chmod(stat.S_IREAD)
    print(json.dumps({"builderSha256": proof["targetSha256"],
                      "derivationSha256": hashlib.sha256(RECEIPT.read_bytes()).hexdigest()}))


if __name__ == "__main__":
    main()

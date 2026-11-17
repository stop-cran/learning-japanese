"""Preserve the unlaunched packet, then derive a correct cross-source extractor."""
from pathlib import Path

from common import WS, freeze_json, frozen, load_batch, packet_dir, require, sha, verify_packet, write_frozen

HERE = Path(__file__).parent
REVIEW = WS / "scratch-129" / "review"


def main():
    raw = frozen(HERE / "build-packet-b128-v2.py",
                 "6ac96f15ef967b8464af8a441ce47035a94e19e2aab07ea4f379778a02d2d715")
    text = raw.decode()
    before_call = ('extract_sections(raw, result["finalUrl"], sorted({PurePosixPath(item["card"]).stem '
                   'for item in result["citedBy"]} | ({result["memberPage"]} if result.get("memberPage") else set())))')
    rules = [
        ("build-packet-b128-v2.py", "build-packet-b129.py"),
        ("from b128_external_sources import METHOD as SECTION_METHOD, extract as extract_sections",
         "from b129_external_sources import METHOD as SECTION_METHOD, extract_capture as extract_sections"),
        (before_call, "extract_sections(raw, result)"),
        ('TOOLS / "b128_external_sources.py"', 'TOOLS / "b129_external_sources.py"'),
    ]
    changes = []
    for before, after in rules:
        count = text.count(before)
        require(count > 0 and after not in text, "Ambiguous packet derivation")
        text = text.replace(before, after)
        changes.append({"before": before, "after": after, "count": count})
    reverse = text
    for change in reversed(changes):
        require(reverse.count(change["after"]) == change["count"], "Packet reverse count differs")
        reverse = reverse.replace(change["after"], change["before"])
    require(reverse.encode() == raw, "Packet derivation is not byte-reversible")
    target = HERE / "build-packet-b129.py"
    compile(text, str(target), "exec")
    require(not target.exists() and not (REVIEW / "prompts").exists()
            and not (REVIEW / "core-chain.json").exists(), "Packet is already in use")
    config = load_batch(129)
    root, sums, digest = verify_packet(config)
    require(digest == "d27a3b14203d12a0a551f3e3c2103aa28f26d79d2fc610b03ba02c9846c47c77",
            "Original packet changed")
    preserved = root.with_name(root.name + "-initial-cross-source-limitation")
    record = REVIEW / "packet-build.json"
    preserved_record = REVIEW / "packet-build-initial-cross-source-limitation.json"
    require(not preserved.exists() and not preserved_record.exists(), "Preserve existing packet history")
    record_raw = frozen(record)
    binding = write_frozen(target, text.encode())
    root.rename(preserved)
    record.rename(preserved_record)
    require(sha(frozen(preserved / "SHA256SUMS.json")) == digest
            and frozen(preserved_record) == record_raw, "Relocated evidence differs")
    for relative, expected in sums.items():
        frozen(preserved / relative, expected)
    print(freeze_json(REVIEW / "packet-v2-preparation.json", {
        "derivation": changes, "reverseExact": True, "builder": binding,
        "sourceBuilderSha256": sha(raw),
        "relocatedPacket": {"originalPath": str(root), "preservedPath": str(preserved),
                            "manifestSha256": digest, "verifiedFiles": len(sums)},
        "relocatedBuildRecord": {"originalPath": str(record), "preservedPath": str(preserved_record),
                                 "sha256": sha(record_raw)},
        "reason": "The original generic extractor expected the citing card's character for a cited "
                  "comparison page. It incorrectly classified the complete cotton source cited by "
                  "the silk card as AMBIGUOUS. The successor checks the actual captured URL headword.",
        "scope": "No reviewer was launched, no source response was re-fetched, and all initial bytes "
                 "remain preserved at the explicit relocation paths. Canonical packet paths are reusable.",
    }))


if __name__ == "__main__":
    main()

"""Freeze the complete 89-source B134 review core without making a capacity claim."""
import json
import sys
from pathlib import Path

WS = Path(r"C:\Users\stop-\n1-kanji-workspace")
ROOT = WS / "scratch-134" / "review" / "fresh-independent-002"
OUT = ROOT / "projected-successor-008"
PACKET = OUT / "packet"
sys.path.insert(0, str(WS / "review-tools"))
sys.path.insert(0, str(OUT / "protocol-003"))

from common import require, sha, start_guard, write_frozen
from review_chain_with_optional import build_chain


def main():
    seed = json.loads((ROOT / "projected-successor-007" / "core-sources-001.json")
                      .read_text(encoding="utf-8"))
    names = ["parent/kanji/紫.md" if name == "baseline/kanji/紫.md" else name
             for name in seed["sources"]]
    require(len(names) == 89 and len(set(names)) == 89
            and "baseline/words/紫.md" in names and "snapshot/words/紫.md" in names
            and "parent/kanji/紫.md" in names and "baseline/kanji/紫.md" not in names,
            "Source list is not the accepted 89-source core with correctly labeled parent card")
    sums_path = PACKET / "SHA256SUMS.json"
    sums_raw = sums_path.read_bytes()
    sums = json.loads(sums_raw)
    packet_files = {path.relative_to(PACKET).as_posix(): path.read_bytes()
                    for path in PACKET.rglob("*")
                    if path.is_file() and path.name != "SHA256SUMS.json"}
    require(set(packet_files) == set(sums)
            and all(sha(packet_files[name]) == sums[name] for name in sums),
            "Packet inventory differs before core construction")
    require(names == [name for name in names if name in packet_files],
            "Accepted core includes a missing packet source")
    source_rows = [(name, packet_files[name], None) for name in names]
    core_path = OUT / "fresh-independent-core-001.json"
    chain_dir = OUT / "chains" / "fresh-independent-core-001"
    require(not core_path.exists() and not chain_dir.exists(),
            "A successor core already exists; preserve it and use a new name")
    guard, _ = start_guard("B134 frozen source-core construction")
    try:
        core = build_chain(source_rows, chain_dir, core_path, guard, "B134 fresh independent core")
        require(len(core["sources"]) == 89 and len(core["segments"]) == 77,
                "Frozen core source/segment counts differ from the accepted predecessor")
        result = {
            "status": "FROZEN_COMPLETE_SOURCE_CORE_NOT_REVIEW_ADMISSION",
            "candidate": seed["candidate"], "base": seed["base"],
            "publishedBaseline": "e17cb97c53ca4e3193dae5e11b52ba517fe86e76",
            "sourceCount": len(core["sources"]), "segmentCount": len(core["segments"]),
            "coreManifest": {"path": str(core_path), "sha256": sha(core_path.read_bytes())},
            "packetInventory": {"path": str(sums_path), "sha256": sha(sums_raw),
                                "files": len(sums)},
            "sourceList": {"path": str(OUT / "core-sources-003.json"),
                           "sha256": sha((OUT / "core-sources-003.json").read_bytes())},
            "limits": "Complete source reconstruction only; no tokenizer measurement, capacity admission, semantic review, or reviewer launch.",
        }
        out = OUT / "frozen-core-003.json"
        write_frozen(out, (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
        print(json.dumps(result, ensure_ascii=False))
    finally:
        require(not guard.finish()["breach"], "Frozen source-core construction RAM breach")


if __name__ == "__main__":
    main()

"""Verify added recurrence entries, literal quiz labels and component cmap coverage."""
import gzip
import hashlib
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from fontTools.ttLib import TTFont

from common import WS, freeze_json, frozen, git, load_batch, require, sha, start_guard
from verify_b119_revision import parse
from verify_reconciliation_sources import element_value


def verify(candidate, output):
    config = load_batch(119)
    directory = WS / "scratch-119" / "review" / "reconciliation-002"
    receipt = json.loads(frozen(directory / "source-extraction.json"))
    extra = receipt["additionalJmdict"]
    guard, _ = start_guard("B119 recurrence, labels and font verification")
    try:
        source = WS / "control" / "inputs" / "n1-implementation-JMdict_e.gz"
        hasher = hashlib.sha256()
        with source.open("rb") as stream:
            while chunk := stream.read(1024 * 1024):
                hasher.update(chunk)
                guard.check()
        require(hasher.hexdigest() == extra["inputSha256"]
                == "2dbbfe0b1214911766bbc128a0935618b925be917e7d1c50f3536a89b0e8786d",
                "JMdict pin mismatch")
        raw = frozen(directory / extra["file"], extra["xmlSha256"])
        entries = ET.fromstring(raw).findall("entry")
        expected = {entry.findtext("ent_seq"): element_value(entry) for entry in entries}
        require(len(entries) == len(expected) == len(extra["entryIds"])
                and set(expected) == set(extra["entryIds"]), "Extra membership mismatch")
        found = set()
        with gzip.open(source, "rb") as stream:
            for _, node in ET.iterparse(stream, events=("end",)):
                if node.tag != "entry":
                    continue
                key = node.findtext("ent_seq")
                if key in expected:
                    require(key not in found and element_value(node) == expected[key],
                            f"Incomplete recurrence entry {key}")
                    found.add(key)
                node.clear()
                guard.check()
        require(found == set(expected), "Missing recurrence entry")
        prefix = f"{candidate}:docs/n1-sources/batch-119/reconciliation-002/"
        require(raw == git(config, "show", prefix + extra["file"]), "Committed recurrence bytes differ")
        rows = json.loads(frozen(directory / "pair-dispositions.json"))["pairs"]
        outcomes = {c: set() for c in config["members"]}
        seen = set()
        for row in rows:
            target, other = row["target"], row["comparison"]
            pair = (target, other)
            require(pair not in seen, "Duplicate pair")
            seen.add(pair)
            target_meta, _ = parse(git(config, "show", f"{candidate}:kanji/{target}.md")
                                   .decode("utf-8").replace("\r\n", "\n"))
            comparison_meta, _ = parse(frozen(directory / "comparison-cards" / f"{other}.md")
                                       .decode("utf-8").replace("\r\n", "\n"))
            require(target_meta and comparison_meta, f"Cannot parse frontmatter: {pair}")
            require(row["targetDisplayedTitle"] == target_meta["title"]
                    and row["comparisonDisplayedTitle"] == comparison_meta["title"],
                    f"Invented displayed label: {pair}")
            for prompt, option, title in ((target, other, comparison_meta["title"]),
                                          (other, target, target_meta["title"])):
                require(row["directions"][f"{prompt} prompt, {option} meaning option"]
                        .startswith(f"Displayed option: {title}."),
                        f"Direction does not use actual title: {pair}")
            if row["outcome"] == "direct exclusion appended":
                outcomes[target].add(other)
            guard.check()
        for character in config["members"]:
            before, _ = parse(git(config, "show", f"{config['candidate']}:kanji/{character}.md").decode("utf-8"))
            after, _ = parse(git(config, "show", f"{candidate}:kanji/{character}.md").decode("utf-8"))
            require(set(after["quiz_exclusions"]) - set(before["quiz_exclusions"]) == outcomes[character],
                    "Guard disposition inventory differs")
        fonts = json.loads(frozen(directory / "font-audit.json"))
        verified = []
        for font in fonts["fonts"]:
            path = WS / "kanji-cards-android" / Path(font["path"])
            require(sha(path.read_bytes()) == font["sha256"], "Bundled font bytes differ")
            with TTFont(path) as opened:
                cmap = opened.getBestCmap()
            require(all(ord(c) in cmap and font["coverage"][c] is True for c in ("爪", "盾")),
                    "Component glyph absent")
            verified.append(font["sha256"])
            guard.check()
        result = {
            "batch": 119, "candidate": candidate, "status": "PASS",
            "sourceExtractionSha256": sha(frozen(directory / "source-extraction.json")),
            "recurrenceXmlSha256": sha(raw), "completeAdditionalEntriesVerified": len(found),
            "pairDispositionsSha256": sha(frozen(directory / "pair-dispositions.json")),
            "exactDisplayedPairs": len(rows), "exactPromptDirections": 2 * len(rows),
            "newGuardInventoryMatches": True, "fontSha256": verified,
            "componentCodePoints": ["U+722A", "U+76FE"],
            "toolSha256": sha(Path(__file__).read_bytes()),
            "limits": "Mechanical provenance, literal labels and cmap coverage only; semantic confirmation "
                      "and native rendering remain separate. No publication approval.",
        }
    finally:
        memory = guard.finish()
    require(not memory["breach"], "RAM guard breach")
    result["memory"] = memory
    print(json.dumps(freeze_json(output, result)))


if __name__ == "__main__":
    verify(sys.argv[1], Path(sys.argv[2]))

"""Verify B131's signed inventory, finite pair coverage and bounded external/font evidence."""
import itertools
import json
import re
import sys
import unicodedata
from pathlib import Path, PurePosixPath

from common import WS, freeze_json, frozen, require, sha, start_guard, write_frozen
from prepare_b131_source_facts import CANDIDATE, CANDIDATE_BASE, HERE, MEMBERS, PREFIX, REPO, RUNNER, SOURCE_BASE
from verify_b131_sources import Git

SCRATCH = HERE.parent
SOURCE_SHA = "99a7a9a11c213280ddae0110fceec9599a7d4d47451e1b3fb1ae6a9e2ab6ac33"
PAYLOAD_SHA = "dc3f1068362350bd81fdc8ec94e20b32589b0fdcdb25248a911e4817ffb068d6"
UNION_SHA = "1735390e50f8768da2cdf264b8157dc19a31e690970cd689b4fc9077e97677f5"
DECISIONS = {"guard", "curated", "distinct", "rejected"}
FONTS = {"kanji_brush.ttf", "kanji_mincho.ttf", "kanji_textbook.ttf"}


def safe_relative(name):
    path = PurePosixPath(name)
    return bool(name) and "\\" not in name and not path.is_absolute() and ".." not in path.parts


def pair_coverage(disposition, cards, scans, comparisons):
    require(disposition["base"] == CANDIDATE_BASE, "Pair base differs")
    items = disposition["members"]
    members = [item for item in items if "kanji" in item]
    new = [item for item in items if "newMemberPair" in item]
    require(len(members) + len(new) == len(items) and [item["kanji"] for item in members] == MEMBERS
            and [item["newMemberPair"] for item in new] == [list(pair) for pair in itertools.combinations(MEMBERS, 2)],
            "Finite member-pair inventory differs")
    guards, curated = ({char: set() for char in MEMBERS} for _ in range(2))
    for item in new:
        require(item["decision"] in DECISIONS and item["bothDirections"].strip(), "Missing new-pair disposition")
        target = {"guard": guards, "curated": curated}.get(item["decision"])
        if target is not None:
            left, right = item["newMemberPair"]
            target[left].add(right)
            target[right].add(left)
    for item in members:
        char = item["kanji"]
        first, final, final_sha = scans[char]
        rows = item["pairs"]
        others = [row["pair"][1] for row in rows]
        require(item["targetTitle"] == cards[char]["title"] and len(set(others)) == len(others)
                and all(row["pair"][0] == char and row["pair"][1] not in MEMBERS for row in rows)
                and item["scanFile"] == f"scans-002/{char}.json" and item["scanSha256"] == final_sha
                and item["scanRows"] == 1254 and item["originalScanBase"] == SOURCE_BASE
                and item["candidateBase"] == CANDIDATE_BASE, "Pair-to-scan or title binding differs")
        require(set(first["matches"]) | set(final["matches"]) <= set(others),
                "A baseline scan match has no pair disposition")
        for row in rows:
            other = row["pair"][1]
            require(other in comparisons and row["decision"] in DECISIONS, "Unbound comparison pair")
            title, digest = comparisons[other]
            require(row["comparisonTitle"] == title and row["baselineCardSha256"] == digest
                    and row["scanMatch"] is (other in final["matches"])
                    and row["targetLabelOnComparison"].strip() and row["comparisonLabelOnTarget"].strip(),
                    "Pair snapshot or bidirectional coverage differs")
        require({row["pair"][1] for row in rows if row["decision"] == "guard"} | guards[char]
                == set(cards[char].get("quiz_exclusions", []))
                and {row["pair"][1] for row in rows if row["decision"] == "curated"} | curated[char]
                == set(cards[char]["distractors"]), "Direct guards or curated choices differ")
    return sum(len(item["pairs"]) for item in members), len(new)


def main():
    output = HERE / "packet-verification-002"
    require(not output.exists(), "Preserve packet verification")
    source = json.loads(frozen(HERE / "source-verification-001.json", SOURCE_SHA))
    payload = json.loads(frozen(HERE / "payload-verification-001.json", PAYLOAD_SHA))
    union = json.loads(frozen(HERE / "source-union-verification-001.json", UNION_SHA))
    require(all(p["candidate"] == CANDIDATE and p["base"] == CANDIDATE_BASE and p["status"] == "PASS"
                for p in (source, payload, union)), "Verified proofs bind different snapshots")
    guard, _ = start_guard("B131 finite packet evidence verification")
    git = Git(REPO, RUNNER, guard)
    signed, captures, local_history = {}, {}, {}
    sys.path.insert(0, str(WS / "lean"))
    from n1lib import parse
    from fontTools.ttLib import TTFont

    def blob(name):
        raw = git("show", CANDIDATE + ":" + PREFIX + name)
        signed[PREFIX + name] = sha(raw)
        return raw

    def clean():
        require(git("rev-parse", "HEAD").decode().strip() == CANDIDATE
                and not git("status", "--porcelain=v1", "--untracked-files=all"),
                "Signed candidate checkout differs")

    try:
        clean()
        inventory = json.loads(blob("evidence-inventory-002.json"))
        paths = {name.removeprefix(PREFIX) for name in
                 git("ls-tree", "-r", "--name-only", CANDIDATE, "--", PREFIX).decode().splitlines()}
        require(inventory["selfExcluded"] is True
                and paths == set(inventory["files"]) | {"evidence-inventory-002.json"},
                "Signed evidence inventory is incomplete")
        for name, digest in inventory["files"].items():
            require(safe_relative(name) and sha(blob(name)) == digest, "Changed packet file: " + name)
            guard.check()
        old = json.loads(blob("evidence-inventory.json"))
        require(old["selfExcluded"] is True
                and all(inventory["files"].get(name) == digest for name, digest in old["files"].items()),
                "Preserved inventory is not an unchanged subset")
        history = json.loads(blob("local-history-bindings.json"))
        require(Path(history["directory"]).resolve() == SCRATCH.resolve(), "Wrong local history root")
        for name, record in history["files"].items():
            path = SCRATCH / name
            require(safe_relative(name) and path.resolve().is_relative_to(SCRATCH.resolve()),
                    "Unsafe local history path")
            raw = path.read_bytes()
            require(sha(raw) == record["sha256"] and len(raw) == record["bytes"],
                    "Historical evidence changed: " + name)
            local_history[name] = record
            guard.check()
        disposition = json.loads(blob("pair-dispositions-002.json"))
        for name, digest in disposition["readbackBindings"].items():
            require(Path(name).name == name and sha((SCRATCH / name).read_bytes()) == digest,
                    "Finite comparison readback changed")
        comparisons, teaching = {}, []
        for char in source["packetComparisonCards"]:
            raw = blob(f"comparison-cards/{char}.md")
            metadata, _ = parse(raw.decode("utf-8").replace("\r\n", "\n"))
            comparisons[char] = (metadata["title"], sha(raw))
        cards = {member["kanji"]: member["metadata"] for member in payload["members"]}
        scans = {}
        for char in MEMBERS:
            teaching.append(git("show", CANDIDATE + f":kanji/{char}.md").decode("utf-8"))
            raw = blob(f"scans-002/{char}.json")
            first, final = json.loads(blob(f"scans/{char}.json")), json.loads(raw)
            require(first["base"] == final["base"] == SOURCE_BASE
                    and first["kanji"] == final["kanji"] == char
                    and len(first["rows"]) == len(final["rows"]) == 1254, "Scan binding differs")
            scans[char] = first, final, sha(raw)
        pair_count, new_pair_count = pair_coverage(disposition, cards, scans, comparisons)
        require(pair_count == 195 and new_pair_count == 3, "Observed finite pair counts differ")
        analysis = json.loads(blob("authored-source-analysis.json"))
        require(analysis["base"] == CANDIDATE_BASE and analysis["originalSourceBase"] == SOURCE_BASE,
                "Authored analysis base differs")
        external = json.loads(blob("external-capture-bindings.json"))
        require(len(external["captures"]) == 6 and external["fullCapturesLocalOnly"] is True
                and {(item["character"], item["provider"]) for item in external["captures"]}
                == {(char, provider) for char in MEMBERS for provider in ("kotobank", "weblio")},
                "External capture coverage differs")
        excerpts = 0
        for item in external["captures"]:
            path = Path(item["localRawCapture"])
            require(path.parent == SCRATCH / "external-003" and path.suffix == ".html"
                    and path.name == item["character"] + "-" + item["provider"] + ".html",
                    "Capture path differs")
            raw, text = path.read_bytes(), path.with_suffix(".txt").read_bytes()
            require(sha(raw) == item["rawSha256"] and len(raw) == item["rawBytes"]
                    and sha(text) == item["textSha256"], "External capture bytes changed")
            captures["external/" + path.name] = raw
            captures["external/" + path.with_suffix(".txt").name] = text
            if item["provider"] == "kotobank":
                quote = analysis["members"][item["character"]]["boundedQuote"]["text"]
                require("".join(quote.split()) in "".join(text.decode("utf-8").split()),
                        "Attributed excerpt is absent from capture")
                excerpts += 1
            guard.check()
        fonts = json.loads(blob("stroke-font-evidence-002.json"))
        require(fonts["producerSha256"] == signed[PREFIX + "producers/font_final_b131.py"]
                and fonts["initialGenerationEvidenceSha256"] == signed[PREFIX + "stroke-font-evidence.json"],
                "Font producer or initial generation binding differs")
        points = fonts["codePoints"]
        chars = {point["character"] for point in points}
        require(len(chars) == len(points)
                and all(point["codePoint"] == f"U+{ord(point['character']):04X}"
                        and point["unicodeName"] == unicodedata.name(point["character"]) for point in points)
                and (set(re.findall("[\u3400-\u9fff]", "\n".join(teaching)))
                     | set(comparisons) | set("\u5f73\u4e8d\u97cb\u884c\u7f8a\u96e8\u76f8\u6728\u76ee")) == chars,
                "Finite taught/comparison Han or code-point inventory differs")
        require(len(fonts["fonts"]) == 3 and {item["filename"] for item in fonts["fonts"]} == FONTS,
                "Bundled font inventory differs")
        missing = {}
        for item in fonts["fonts"]:
            path = WS / "kanji-cards-android" / "app" / "src" / "main" / "res" / "font" / item["filename"]
            require(sha(path.read_bytes()) == item["sha256"], "Actual bundled font bytes differ")
            with TTFont(path) as font:
                cmap = font.getBestCmap()
                coverage = {point["codePoint"]: ord(point["character"]) in cmap for point in points}
            require(coverage == item["coverage"], "Actual font cmap differs")
            missing[item["filename"]] = sorted(key for key, present in coverage.items() if not present)
            guard.check()
        progress = json.loads(git("show", CANDIDATE + ":docs/n1-sources/batch-131-progress.json"))
        require(progress["batch"] == 131 and progress["status"] == "local-unreviewed-author-candidate"
                and progress["base"] == CANDIDATE_BASE and progress["originalSourceBase"] == SOURCE_BASE
                and progress["members"] == MEMBERS and progress["sourceRows"] == [977, 870, 1174]
                and progress["publishedDelivered"] == 264 and progress["undelivered"] == 964
                and progress["deliveryNotIncremented"] is True and progress["localUnpublishedDrafts"] == 3
                and progress["manifestSha256"] == payload["manifestSha256"]
                and progress["activePairTable"] == "batch-131/pair-dispositions-002.json",
                "Progress record expands scope or prematurely credits delivery")
        clean()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "RAM breach")
    captured = {name: write_frozen(output / name, raw) for name, raw in captures.items()}
    print(json.dumps(freeze_json(output / "verification.json", {
        "batch": 131, "status": "PASS", "candidate": CANDIDATE, "base": CANDIDATE_BASE,
        "sourceProofSha256": SOURCE_SHA, "payloadProofSha256": PAYLOAD_SHA, "sourceUnionProofSha256": UNION_SHA,
        "signedInputs": signed, "localHistoryBindings": local_history, "capturedInputs": captured,
        "finiteBaselinePairs": pair_count, "finiteNewPairs": new_pair_count, "verifiedExcerpts": excerpts,
        "fontMissingCodePoints": missing,
        "fontScope": "All Han in the three new cards, all comparison identifiers and explicit "
                     "mnemonic/radical components; not every legacy comparison article body.",
        "memory": memory, "verifierSha256": sha(frozen(Path(__file__))),
        "limits": "Mechanical signed-inventory, finite pair/scan coverage, retained local bytes, "
                  "attributed excerpt and actual bounded font-cmap verification. Does not certify "
                  "pair judgments, historical execution/manual reading depth, rendered fallback, "
                  "native/device, independent review, whole-set or publication acceptance.",
    })))


if __name__ == "__main__":
    main()

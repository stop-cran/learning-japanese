"""Reproduce compact002 core coverage and conservative capacity arithmetic independently."""
import hashlib
import json
import math
import stat
import sys
from pathlib import Path

from verify_b131_compact002_data_coordinator_002 import WS, NEW, frozen, require

HERE = WS / "scratch-131" / "review" / "preparation-002"
REVIEW = HERE.parent
PINS = {
    HERE / "core-chain-compact-002.json": "c6ce97ff03a25a08029689fe0e0cb26af83c97853892cd1bee135094956c8bdb",
    HERE / "capacity-forecast-compact-002.json": "1d524f25ed065fb5a2c9f4ecfbad1e28a25b4b54d0b058c6bbcd1619283ca3bb",
    NEW / "SHA256SUMS.json": "7a8308db2ca5f912afbb61151afff31f98ee5b35c5b357957e9c80835010305c",
    REVIEW / "capacity" / "claude001-calibration-001.json": "aca593742a9191eec34aa7b8774b4042789bdf7d0025fcfe0d06896b0a3041da",
    REVIEW / "preparation-001" / "core-chain-compact-001.json": "1226ce87e7d7a92685de6845406678dac668ece7508002f4389b4f8ab97df32b",
}


def rate(name):
    if name.endswith("/kanjidic2-review-projection.xml"):
        return .65
    if name.endswith("/jmdict-review-core.xml"):
        return .543
    if name == "repo/docs/jlpt-levels.md":
        return .374
    if name.endswith("-extract.txt"):
        return .446
    if name.endswith(("/title-index.txt", "/title-index-delta.txt")):
        return .531
    if name.endswith(".md") and name.startswith(("snapshot/", "baseline/", "repo/kanji/", "repo/words/")):
        return .502
    if name.startswith(("evidence/", "snapshot/strokes/")):
        return .522
    return .354


def extension_cost(rows):
    article_bytes = sum(row["articleBytes"] for row in rows)
    dictionary_bytes = sum(row["supplementalDictionaryBytes"] for row in rows)
    records = sum(row["supplementalRecords"] for row in rows)
    return math.ceil((article_bytes + dictionary_bytes) * .55) + 1024 + len(rows) * 512 + records * 128


def main(output):
    output = Path(output)
    require(output.parent == REVIEW and not output.exists(), "Use a new review output")
    values = {path: json.loads(frozen(path, digest)) for path, digest in PINS.items()}
    chain = values[HERE / "core-chain-compact-002.json"]
    forecast = values[HERE / "capacity-forecast-compact-002.json"]
    sums = values[NEW / "SHA256SUMS.json"]
    calibration = values[REVIEW / "capacity" / "claude001-calibration-001.json"]
    old = values[REVIEW / "preparation-001" / "core-chain-compact-001.json"]
    dropped = {"evidence/xml-presentation.json", "evidence/font-cmap.json",
               "evidence/baseline-title-index.txt", "evidence/dictionary-index.json"}
    replacements = {"evidence/kanjidic2-records.xml": "evidence/kanjidic2-review-projection.xml",
                    "evidence/jmdict-families.xml": "evidence/jmdict-review-core.xml"}
    names = []
    for row in old["sources"]:
        name = row["source"]
        if name not in dropped:
            names.append(replacements.get(name, name))
            if name == "evidence/title-index.txt":
                names.append("evidence/title-index-delta.txt")
    require([row["source"] for row in chain["sources"]] == names and len(names) == len(set(names)),
            "Core source order or membership changed")
    sources = {name: frozen(NEW.joinpath(*name.split("/")), sums[name]) for name in names}
    rebuilt = {name: b"" for name in names}
    positions = dict.fromkeys(names, 1)
    measured = {row["sha256"]: row["measuredInputTokenDelta"] for row in calibration["segments"]
                if type(row["measuredInputTokenDelta"]) is int}
    per_segment = []
    for i, segment in enumerate(chain["segments"]):
        require(segment["index"] == i + 1, "Segment order changed")
        raw = frozen(Path(segment["path"]), segment["sha256"])
        lines = raw.splitlines(keepends=True)
        require(len(raw) == segment["bytes"] and len(raw) < 16000 and len(lines) == segment["lines"],
                "Segment size/line limit changed")
        ending = ("NEXT SEGMENT: " + chain["segments"][i + 1]["path"] + "\n"
                  if i + 1 < len(chain["segments"]) else
                  "END OF CHAIN. Follow the run instruction's phase boundary.\n").encode()
        require(raw.endswith(ending), "Chain successor changed")
        token_cost, payload_lines = 0.0, set()
        for part in segment["parts"]:
            name = part["source"]
            require(name in sources and part["a"] == positions[name] and part["sha256"] == sums[name],
                    "Source continuity or binding changed")
            source_lines = sources[name].splitlines(keepends=True)
            require(1 <= part["a"] <= part["b"] <= len(source_lines), "Invalid source range")
            expected = b"".join(source_lines[part["a"] - 1:part["b"]])
            actual = b"".join(lines[part["segmentStart"] - 1:part["segmentEnd"]])
            require(actual == expected, "Source bytes changed within segment")
            selected = set(range(part["segmentStart"], part["segmentEnd"] + 1))
            require(not selected & payload_lines, "Overlapping segment payloads")
            payload_lines.update(selected)
            rebuilt[name] += actual
            positions[name] = part["b"] + 1
            token_cost += len(actual) * rate(name) * 1.10
        expected_tokens = (math.ceil(measured[segment["sha256"]] * 1.05)
                           if segment["sha256"] in measured else math.ceil(token_cost))
        claimed = forecast["segments"][i]
        require(claimed["index"] == segment["index"] and claimed["sha256"] == segment["sha256"]
                and claimed["tokens"] == expected_tokens, "Per-segment forecast differs")
        per_segment.append(expected_tokens)
    require(rebuilt == sources, "Core does not contain every source byte exactly once")
    require(len(sources["repo/docs/content-format.md"].splitlines()) == 1419,
            "Content-format coverage changed")
    for row in chain["sources"]:
        require(row["sha256"] == row["selectedSha256"] == sums[row["source"]]
                and row["selectedLines"] == row["sourceLines"] == len(sources[row["source"]].splitlines()),
                "Source manifest declares partial coverage")
    core_tokens = sum(per_segment)
    require(core_tokens == forecast["coreTokens"], "Core total differs")
    reference = json.loads(frozen(NEW / "eligibility-reference.json"))
    catalog = json.loads(frozen(NEW / "evidence" / "jmdict-extension-index.json"))["characters"]
    articles = {Path(name).stem: len(frozen(NEW.joinpath(*name.split("/")), digest))
                for name, digest in sums.items() if name.startswith("repo/kanji/") and name.endswith(".md")}
    blocked = set(reference["newCards"]) | set(reference["otherRequiredCards"])
    blocked.update(c for row in reference["cards"] for c in row["distractors"])
    guards = {c for row in reference["cards"] for c in row["quiz_exclusions"]}
    universe = set(articles) | {c for c in catalog if len(c) == 1 and "\u4e00" <= c <= "\u9fff"}
    eligible = {"D": [], "E": []}
    for character in sorted(universe - blocked):
        ids = catalog.get(character, {}).get("matchingRemainderIds", [])
        extra = sum(len(frozen(NEW / "evidence" / "jmdict-extension-records" / f"{i}.xml")) for i in ids)
        row = {"character": character, "articleBytes": articles.get(character, 0),
               "supplementalDictionaryBytes": extra, "supplementalRecords": len(ids),
               "dictionaryIds": ids}
        row["score"] = (row["articleBytes"] + extra) * .55 + 512 + len(ids) * 128
        eligible["E" if character in guards else "D"].append(row)
    trials = []
    for dcap, claimed in zip((40, 35, 30, 25, 20), forecast["trials"]):
        chosen = sorted(eligible["D"], key=lambda r: (-r["score"], r["character"]))[:dcap]
        chosen += sorted(eligible["E"], key=lambda r: (-r["score"], r["character"]))[:10]
        extension = extension_cost(chosen)
        peak = 80000 + core_tokens + extension + 30000
        require(claimed["D"] == dcap and claimed["E"] == 10
                and claimed["selectionIndependentUpperBound"] == chosen
                and claimed["worstCaseExtension"]["tokens"] == extension
                and claimed["projectedWorstCasePeak"] == peak
                and claimed["passes"] == (peak <= 700000), "Worst-case cap trial differs")
        trials.append({"D": dcap, "E": 10, "peak": peak, "passes": peak <= 700000})
    require(len(trials) == len(forecast["trials"]) == 5, "Cap options omitted")
    passed = next((t for t in trials if t["passes"]), None)
    require(passed is not None and forecast["chosenCaps"] == {"D": passed["D"], "E": 10}
            and forecast["projectedWorstCasePeak"] == passed["peak"], "Largest passing cap differs")
    require(forecast["startupGate"] == 700000 and forecast["prePhase2Gate"] == 740000
            and forecast["reportMessageAllowance"] == 30000 and forecast["currentTokenOffset"] == 7000,
            "Capacity limits changed")
    result = {
        "status": "PASS_CHAIN_AND_FORECAST_ONLY", "packetManifestSha256": PINS[NEW / "SHA256SUMS.json"],
        "chainManifestSha256": PINS[HERE / "core-chain-compact-002.json"],
        "forecastSha256": PINS[HERE / "capacity-forecast-compact-002.json"],
        "sources": len(sources), "segments": len(chain["segments"]),
        "coreBytes": sum(s["bytes"] for s in chain["segments"]), "coreTokens": core_tokens,
        "chosenCaps": forecast["chosenCaps"], "trials": trials,
        "limits": "Independent source-byte coverage and specified arithmetic reproduced. Statistical rates and "
                  "header allowances remain estimates, not context guarantees. Runtime gates, final prompts, "
                  "actual reviewer execution and semantic acceptance remain unverified.",
    }
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(result, indent=2) + "\n")
    output.chmod(stat.S_IREAD)
    print(json.dumps(result))
    print("Record SHA256: " + hashlib.sha256(output.read_bytes()).hexdigest())


if __name__ == "__main__":
    main(sys.argv[1])

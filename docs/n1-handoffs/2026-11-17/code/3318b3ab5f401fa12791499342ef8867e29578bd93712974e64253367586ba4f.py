"""Independently verify B134's frozen source chains and capacity arithmetic."""
import argparse
import json
import math
import xml.etree.ElementTree as ET
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, start_guard

ROOT = WS / "scratch-134" / "review"
PREPARATION = ROOT / "neutral-preparation-001"
HERE = PREPARATION / "projected-successor-001"
FULL = PREPARATION / "complete-record-trial-003"
CAPS = ((25, 10), (20, 10), (15, 10), (10, 10), (10, 5))


def load(path, digest=None):
    return json.loads(frozen(path, digest))


def packet(root, guard):
    manifest = load(root / "packet" / "SHA256SUMS.json")
    files = {}
    for name, digest in manifest.items():
        path = root / "packet" / name
        require(path.resolve().is_relative_to((root / "packet").resolve()), "Unsafe packet path")
        files[name] = frozen(path, digest)
        guard.check()
    actual = {p.relative_to(root / "packet").as_posix()
              for p in (root / "packet").rglob("*") if p.is_file()}
    require(actual == set(files) | {"SHA256SUMS.json"}, "Packet inventory differs")
    return files


def verify_chain(files, chain, root):
    sources = chain["sources"]
    names = [row["source"] for row in sources]
    require(len(names) == len(set(names)), "Duplicate core source")
    recovered = {name: bytearray() for name in names}
    next_line = dict.fromkeys(names, 1)
    observed_order = []
    for index, segment in enumerate(chain["segments"], 1):
        path = Path(segment["path"])
        require(path.resolve().is_relative_to(root.resolve()) and segment["index"] == index,
                "Chain path or order differs")
        raw = frozen(path, segment["sha256"])
        lines = raw.splitlines(keepends=True)
        require(len(raw) == segment["bytes"] < 16000 and len(lines) == segment["lines"],
                "Segment size or line count differs")
        last_end = 0
        for part in segment["parts"]:
            name = part["source"]
            require(name in recovered, "Unexpected source in chain")
            original = files[name].splitlines(keepends=True)
            a, b = part["a"], part["b"]
            start, end = part["segmentStart"], part["segmentEnd"]
            require(a == next_line[name] and a <= b <= len(original)
                    and last_end < start <= end <= len(lines), "Partial, reordered or overlapping source")
            selected = b"".join(lines[start - 1:end])
            require(selected == b"".join(original[a - 1:b])
                    and part["sha256"] == part["selectedSha256"] == sha(files[name])
                    and part["sourceLines"] == part["selectedLines"] == len(original),
                    "Source bytes or source identity differ")
            recovered[name].extend(selected)
            next_line[name] = b + 1
            last_end = end
            if not observed_order or observed_order[-1] != name:
                observed_order.append(name)
    require(observed_order == names, "Core source order differs")
    for row in sources:
        name, raw = row["source"], files[row["source"]]
        require(bytes(recovered[name]) == raw and row["sha256"] == row["selectedSha256"] == sha(raw)
                and row["sourceLines"] == row["selectedLines"] == len(raw.splitlines()),
                "Incomplete core source")
    return [(name, files[name]) for name in names]


def rate(name):
    if name.startswith("evidence/kanjidic2-full-records/"):
        return .60
    if name == "evidence/kanjidic2-review-projection.xml":
        return .715
    if name == "evidence/kanjidic2-records.xml":
        return 1.0
    if name == "evidence/jmdict-families.xml":
        return .543 * 1.10
    if name == "evidence/title-index.txt":
        return .531 * 1.10
    if name.startswith("evidence/") and name.endswith("-extract.txt"):
        return .446 * 1.10
    if name.endswith(".json") or name.startswith(("diffs/", "checks/", "evidence/")):
        return .522 * 1.10
    if name == "repo/docs/jlpt-levels.md":
        return .374 * 1.10
    if name.endswith(".md") and name.startswith(("repo/kanji/", "snapshot/", "baseline/")):
        return .502 * 1.10
    return .354 * 1.10


def envelope(raw):
    require(raw.endswith(b"\n"), "Unframed source")
    parts, occupied = 1, 0
    for line in raw.splitlines(keepends=True):
        require(len(line) <= 13900, "Oversized source line")
        if occupied + len(line) > 13900:
            parts += 1
            occupied = 0
        occupied += len(line)
    return 2100 * (parts + (len(raw) > 13900))


def upper(sources):
    framed = 2100 + sum(envelope(raw) for _, raw in sources)
    return {
        "payloadBytes": sum(len(raw) for _, raw in sources),
        "envelopeBytesUpper": framed,
        "tokens": sum(math.ceil(len(raw) * rate(name)) for name, raw in sources)
        + math.ceil(framed * .574),
    }


def shape(node):
    return node.tag, tuple(sorted(node.attrib.items())), node.text, tuple(map(shape, node))


def verify_projection(full, projected):
    original = ET.fromstring(full)
    for node in original:
        for child in list(node):
            if child.tag in ("codepoint", "dic_number", "query_code"):
                node.remove(child)
        for group in node.findall("reading_meaning/rmgroup"):
            for child in list(group):
                if ((child.tag == "meaning" and child.get("m_lang", "en") != "en")
                        or (child.tag == "reading" and child.get("r_type") in
                            ("pinyin", "korean_r", "korean_h", "vietnam"))):
                    group.remove(child)
    require(shape(original) == shape(ET.fromstring(projected)), "Unauthorized projection")


def verify_capacity(files, chain, forecast, root, projected):
    sources = verify_chain(files, chain, root)
    payload = sum(len(raw) for _, raw in sources)
    total = sum(row["bytes"] for row in chain["segments"])
    cost = {
        "payloadBytes": payload, "chainBytes": total, "envelopeBytes": total - payload,
        "tokens": sum(math.ceil(len(raw) * rate(name)) for name, raw in sources)
        + math.ceil((total - payload) * .574),
    }
    require(cost == forecast["coreCost"] and cost["tokens"] == forecast["coreTokens"],
            "Independent core forecast differs")
    reference = json.loads(files["eligibility-reference.json"])
    excluded = set(reference["newCards"]) | set(reference["otherRequiredCards"])
    excluded.update(c for row in reference["cards"] for c in row["distractors"])
    guards = {c for row in reference["cards"] for c in row["quiz_exclusions"]}
    groups = {"D": [], "E": []}
    for name, raw in files.items():
        if name.startswith("repo/kanji/") and name.endswith(".md") and Path(name).stem not in excluded:
            group = "E" if Path(name).stem in guards else "D"
            groups[group].append((upper([(name, raw)])["tokens"], name, raw))
    require({k: len(v) for k, v in groups.items()} == forecast["eligibleArticleCounts"]
            and len(forecast["trials"]) == len(CAPS), "Eligibility or capacity trials differ")
    chosen = None
    for caps, trial in zip(CAPS, forecast["trials"]):
        pairs = sorted(groups["D"], reverse=True)[:caps[0]] + sorted(groups["E"], reverse=True)[:caps[1]]
        article = upper([(name, raw) for _, name, raw in pairs])
        peak = cost["tokens"] + article["tokens"] + 20000 + 80000 + 30000
        cap = dict(zip(("D", "E"), caps))
        require(trial["caps"] == cap and trial["articleUpper"] == article
                and trial["startupPeak"] == peak and trial["passes"] == (peak <= 700000)
                and trial["excess"] == max(0, peak - 700000), "Worst-case forecast differs")
        if chosen is None and peak <= 700000:
            chosen = trial
    if projected:
        require(chosen and forecast["chosenCaps"] == forecast["caps"] == chosen["caps"],
                "Not the first prescribed passing capacity")
        optional_names = {name for name in files if name.startswith("evidence/kanjidic2-full-records/")}
        optional_names.update(("evidence/xml-presentation.json", "evidence/font-cmap.json",
                               "evidence/dictionary-index.json"))
        require(len(optional_names) == 62
                and {r["source"] for r in forecast["optionalUnits"]} == optional_names,
                "Optional inventory differs")
        maximum = 0
        for row in forecast["optionalUnits"]:
            name = row["source"]
            measured = upper([(name, files[name])])
            require(row["sha256"] == sha(files[name]) and all(row[k] == v for k, v in measured.items()),
                    "Optional unit cost differs")
            maximum = max(maximum, measured["tokens"])
        require(maximum == forecast["largestOptionalUnitTokens"] <= forecast["optionalUnitAllowance"] == 20000
                and forecast["maximumExtensionTokens"] == chosen["articleUpper"]["tokens"] + 20000,
                "Optional or combined extension allowance differs")
    return {"coreTokens": cost["tokens"], "firstPassingTrial": chosen,
            "coreSources": len(sources), "segments": len(chain["segments"])}


def main(output):
    guard, _ = start_guard("B134 independent neutral capacity verification")
    try:
        selected = load(PREPARATION / "selected-packet-001.json")
        require(Path(selected["root"]) == HERE, "Selected packet root differs")
        files, full_files = packet(HERE, guard), packet(FULL, guard)
        require(set(full_files) <= set(files)
                and {name for name in full_files if full_files[name] != files[name]}
                == {"REVIEW.md", "packet.json"}, "Unexpected original source modification")
        full_kd = files["evidence/kanjidic2-records.xml"]
        require(len(ET.fromstring(full_kd)) == 59
                and len(ET.fromstring(files["evidence/jmdict-families.xml"])) == 399,
                "Dictionary union count differs")
        verify_projection(full_kd, files["evidence/kanjidic2-review-projection.xml"])
        lines = full_kd.splitlines(keepends=True)[1:-1]
        require(len(lines) == 59, "Full KD framing differs")
        for line in lines:
            char = ET.fromstring(line).findtext("literal")
            require(files[f"evidence/kanjidic2-full-records/{char}.xml"] == line, "Full KD unit changed")
        forecast = load(selected["forecast"]["path"], selected["forecast"]["sha256"])
        full_forecast = load(selected["completeRecordTrial"]["path"], selected["completeRecordTrial"]["sha256"])
        complete = verify_capacity(full_files, load(FULL / "core-chain-001.json"), full_forecast, FULL, False)
        require(not full_forecast["trials"][0]["passes"], "Projection was unnecessary at original D25/E10 gate")
        measured = verify_capacity(files, load(HERE / "core-chain-001.json"), forecast, HERE, True)
        require(selected["caps"] == measured["firstPassingTrial"]["caps"], "Selected caps differ")
        result = {
            "status": "PASS_INDEPENDENT_BYTE_CHAIN_PROJECTION_CAPACITY_NOT_REVIEW_ADMISSION",
            "candidate": "ba80afffc20a72d31be68b355b6f90aab36a5726",
            "packetManifestSha256": sha(frozen(HERE / "packet" / "SHA256SUMS.json")),
            "capacitySha256": selected["forecast"]["sha256"],
            "packetFiles": len(files), "completeRecordTrial": complete, "selected": measured,
            "limits": "Forecasts, not measured tokens. Final protocol, source derivation and actual reviews still require verification.",
        }
    finally:
        memory = guard.finish()
        require(not memory["breach"], "Capacity verifier RAM breach")
    result["memory"] = memory
    print(json.dumps(freeze_json(output, result)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    main(parser.parse_args().output)

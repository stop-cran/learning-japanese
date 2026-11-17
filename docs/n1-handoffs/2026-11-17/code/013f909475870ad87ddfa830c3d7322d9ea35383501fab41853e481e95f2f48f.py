"""Reproduce the complete byte proof and independently check 004 capacity arithmetic."""
import argparse
import json
import math
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

WS = Path(r"C:\Users\stop-\n1-kanji-workspace")
ROOT = WS / "scratch-133" / "review"
HERE = ROOT / "neutral-preparation-004" / "successor-002"
OLD = ROOT / "neutral-preparation-003"
sys.path.insert(0, str(WS / "review-tools"))
from common import freeze_json, frozen, require, sha, start_guard


def load(path, digest=None):
    return json.loads(frozen(path, digest))


def rate(name):
    if name.startswith("evidence/kanjidic2-full-records/"):
        return .60
    if name == "evidence/kanjidic2-review-projection.xml":
        return .715
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


def check_projection(files):
    full = files["evidence/kanjidic2-records.xml"]
    original = ET.fromstring(full)
    projected = ET.fromstring(files["evidence/kanjidic2-review-projection.xml"])
    require(len(original) == len(projected) == 83, "KD membership differs")
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
    require(shape(original) == shape(projected), "Unauthorized projection")
    lines = full.splitlines(keepends=True)[1:-1]
    require(len(lines) == 83, "Original KD record framing differs")
    for line in lines:
        literal = ET.fromstring(line).findtext("literal")
        require(files[f"evidence/kanjidic2-full-records/{literal}.xml"] == line,
                "Optional complete record changed")


def check_capacity(files, chain, forecast):
    sources = [(row["source"], files[row["source"]]) for row in chain["sources"]]
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
    targets = {c for row in reference["cards"] for c in row["quiz_exclusions"]}
    groups = {"D": [], "E": []}
    for name, raw in files.items():
        if name.startswith("repo/kanji/") and name.endswith(".md") and Path(name).stem not in excluded:
            group = "E" if Path(name).stem in targets else "D"
            groups[group].append((upper([(name, raw)])["tokens"], name, raw))
    require(len(forecast["trials"]) == 5, "Missing capacity trials")
    chosen = None
    for caps, trial in zip(((25, 10), (20, 10), (15, 10), (10, 10), (10, 5)), forecast["trials"]):
        pairs = sorted(groups["D"], reverse=True)[:caps[0]] + sorted(groups["E"], reverse=True)[:caps[1]]
        article = upper([(name, raw) for _, name, raw in pairs])
        peak = cost["tokens"] + article["tokens"] + 20000 + 80000 + 30000
        cap = dict(zip(("D", "E"), caps))
        require(trial["caps"] == cap and trial["articleUpper"] == article
                and trial["startupPeak"] == peak and trial["passes"] == (peak <= 700000),
                "Independent worst-case trial differs")
        if chosen is None and peak <= 700000:
            chosen = cap
    require(chosen == forecast["chosenCaps"] == forecast["caps"] == {"D": 10, "E": 5},
            "Not the first prescribed passing capacity")
    optional_names = {name for name in files if name.startswith("evidence/kanjidic2-full-records/")}
    optional_names.update(("evidence/xml-presentation.json", "evidence/font-cmap.json",
                           "evidence/dictionary-index.json"))
    require(len(optional_names) == 86 and {r["source"] for r in forecast["optionalUnits"]} == optional_names,
            "Optional inventory differs")
    maximum = 0
    for row in forecast["optionalUnits"]:
        name, raw = row["source"], files[row["source"]]
        measured = upper([(name, raw)])
        require(row["sha256"] == sha(raw) and all(row[k] == v for k, v in measured.items()),
                "Optional whole-unit cost differs")
        maximum = max(maximum, measured["tokens"])
    require(maximum == forecast["largestOptionalUnitTokens"] <= forecast["optionalUnitAllowance"] == 20000,
            "An individual optional unit cannot fit")
    require(forecast["maximumExtensionTokens"] == forecast["trials"][-1]["articleUpper"]["tokens"] + 20000,
            "Combined extension allowance differs")
    return {"coreTokens": cost["tokens"], "startupUpper": forecast["trials"][-1]["startupPeak"],
            "caps": chosen, "optionalUnits": len(optional_names), "largestOptionalUnitTokens": maximum}


def reproduce(producer, output):
    expected = load(output)
    namespace = {"__name__": "coordinator_reproduction", "__file__": str(producer)}
    exec(compile(frozen(producer).decode(), str(producer), "exec"), namespace)
    results = []

    def compare_only(path, result):
        require(path == output and result == expected, "Complete byte proof did not reproduce")
        results.append(result)
        return {"reproducedExactly": True}

    namespace["freeze_json"] = compare_only
    namespace["main"]()
    require(len(results) == 1, "Missing reproduced proof")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-sha", required=True)
    parser.add_argument("--handoff-sha", required=True)
    parser.add_argument("--final-sha", required=True)
    parser.add_argument("--preflight", type=Path, default=HERE / "audit-configs-003" / "preflight.json")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    guard, _ = start_guard("B133 coordinator final preparation verification")
    try:
        manifest_path = HERE / "PREPARATION-SHA256SUMS-001.json"
        manifest = load(manifest_path, args.manifest_sha)
        frozen(HERE / "COORDINATOR-HANDOFF-001.txt", args.handoff_sha)
        final = load(HERE / "final-static-verification-001.json", args.final_sha)
        require(final["candidate"] == "ad047ace020579f81bde250ac948b9a4cb597887"
                and final["base"] == "6858fcfb069cc56a195c3f6ed938f92f657fe96b"
                and final["status"].startswith("PASS_") and final["actualReviewersLaunched"] == 0,
                "Final preparation identity/status differs")
        actual = {p.relative_to(HERE).as_posix() for p in HERE.rglob("*") if p.is_file()}
        require(actual == set(manifest) | {manifest_path.name, "final-static-verification-001.json"},
                "Final inventory changed")
        for name, digest in manifest.items():
            path = HERE / name
            require(path.resolve().is_relative_to(HERE), "Unsafe static path")
            frozen(path, digest)
            guard.check()
        sums = load(HERE / "packet" / "SHA256SUMS.json")
        files = {name: frozen(HERE / "packet" / name, digest) for name, digest in sums.items()}
        old_sums = load(OLD / "packet" / "SHA256SUMS.json")
        require(set(old_sums) <= set(files), "Original source removed")
        require({name for name, digest in old_sums.items() if sha(files[name]) != digest}
                == {"REVIEW.md", "packet.json"}, "Unapproved original source modification")
        check_projection(files)
        chain = load(HERE / "core-chain-001.json")
        forecast = load(HERE / "capacity-measurement-001.json")
        measured = check_capacity(files, chain, forecast)
        reproduce(HERE / "tools" / "verify004-full-derived.py", HERE / "complete-verification-001.json")
        disclosure = frozen(HERE / "DISCLOSURE-001.txt")
        require(args.preflight.resolve().is_relative_to(HERE), "Preflight outside preparation")
        preflight = load(args.preflight, manifest[args.preflight.relative_to(HERE).as_posix()])
        for family, spec in preflight["runs"].items():
            prompt = frozen(spec["prompt"]["path"], spec["prompt"]["sha256"])
            require(prompt.count(disclosure) == files["REVIEW.md"].count(disclosure) == 1,
                    "Paired disclosure mismatch")
            require(spec["startupEstimate"]["estimatedUpper"] == measured["startupUpper"]
                    and spec["startupEstimate"]["status"] == "PASS_ESTIMATE", "Prompt forecast mismatch")
            require(not Path(spec["report"]).exists() and not any(Path(spec["report"]).parent.iterdir()),
                    "Report destination not empty")
        result = {
            "status": "PASS_REPRODUCED_004_PREPARATION_NOT_REVIEW_ACCEPTANCE",
            "candidate": final["candidate"], "staticFilesVerified": len(manifest), "packetFiles": len(sums),
            "completeByteProofReproducedExactly": True, "capacityIndependentRecomputation": measured,
            "manifestSha256": args.manifest_sha, "handoffSha256": args.handoff_sha,
            "finalStaticVerificationSha256": args.final_sha,
            "limits": "Mechanical preparation only. Actual serial admission, two-family reviews, reconciliation and publication remain required.",
        }
        print(json.dumps(freeze_json(args.output, result)))
    finally:
        require(not guard.finish()["breach"], "Coordinator verification RAM breach")


if __name__ == "__main__":
    main()

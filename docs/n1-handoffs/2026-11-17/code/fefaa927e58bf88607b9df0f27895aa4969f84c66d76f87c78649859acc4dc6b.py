"""Verify exact packet derivations, full source coverage and reproducible capacity bindings."""
import json
import re
from pathlib import Path

from b131_review_v2_common import (
    CALIBRATION, CALIBRATION_SHA, FORECAST, HERE, PACKET, frozen, json_bytes,
    load_batch, require, sha, verify_inputs, verify_packet)
from b131_review_v2_derivations import (
    supplement_catalog, verify_delta, verify_jm, verify_kd)
from b131_capacity_002 import compute_forecast
from prepare_chain_b131_002 import core_sources


def verify_chain(chain, sources):
    require([row["source"] for row in chain["sources"]] == [row[0] for row in sources],
            "Chain source order/coverage differs")
    expected = {name: raw for name, raw, _ in sources}
    require(len(expected) == len(sources), "Duplicate source")
    rebuilt = {name: b"" for name in expected}
    next_line = dict.fromkeys(expected, 1)
    for index, segment in enumerate(chain["segments"], 1):
        require(segment["index"] == index, "Chain indices differ")
        raw = frozen(segment["path"], segment["sha256"])
        require(len(raw) == segment["bytes"] and len(raw) < 16000
                and raw.count(b"\n") == segment["lines"], "Chain byte/line bound changed")
        lines = raw.splitlines(keepends=True)
        final = ("NEXT SEGMENT: " + chain["segments"][index]["path"] + "\n"
                 if index < len(chain["segments"]) else
                 "END OF CHAIN. Follow the run instruction's phase boundary.\n").encode()
        require(raw.endswith(final), "Chain successor/terminator changed")
        for part in segment["parts"]:
            name = part["source"]
            require(name in expected and part["sha256"] == sha(expected[name])
                    and part["a"] == next_line[name], "Chain source hash or contiguous range changed")
            source_lines = expected[name].splitlines(keepends=True)
            payload = b"".join(lines[part["segmentStart"] - 1:part["segmentEnd"]])
            require(1 <= part["a"] <= part["b"] <= len(source_lines)
                    and payload == b"".join(source_lines[part["a"] - 1:part["b"]]),
                    "Chain payload range changed")
            rebuilt[name] += payload
            next_line[name] = part["b"] + 1
    require(rebuilt == expected, "Chain omits/changes complete source bytes")
    for row in chain["sources"]:
        data = expected[row["source"]]
        require(row["sha256"] == row["selectedSha256"] == sha(data)
                and row["sourceLines"] == row["selectedLines"] == len(data.splitlines()),
                "Chain source manifest selects incomplete source")
    return {"sources": len(sources), "segments": len(chain["segments"]),
            "bytes": sum(row["bytes"] for row in chain["segments"]),
            "maxBytes": max(row["bytes"] for row in chain["segments"])}


def verify_subset(guard, initial=False):
    if initial:
        verify_inputs(guard)
    _, sums, packet_sha = verify_packet(load_batch(131), guard)
    proof = json.loads(frozen(HERE / "derivation-verification-002.json"))
    reference = json.loads(frozen(PACKET / "eligibility-reference.json"))
    full_jm = frozen(PACKET / "evidence/jmdict-families.xml")
    kd = verify_kd(frozen(PACKET / "evidence/kanjidic2-records.xml"),
                   frozen(PACKET / "evidence/kanjidic2-review-projection.xml"))
    require(kd == proof["kanjidicRecords"], "Per-record removed classes proof changed")
    partition = verify_jm(full_jm, frozen(PACKET / "evidence/jmdict-review-core.xml"), reference,
                          json.loads(frozen(PACKET / "evidence/dictionary-index.json")),
                          proof["jmdictPartition"])
    delta = verify_delta(frozen(PACKET / "evidence/baseline-title-index.txt"),
                         frozen(PACKET / "evidence/title-index.txt"),
                         frozen(PACKET / "evidence/title-index-delta.txt"))
    require(delta == proof["titleDelta"], "Title delta proof changed")
    records, catalog = supplement_catalog(full_jm, partition)
    for identity, raw in records.items():
        require(frozen(PACKET / f"evidence/jmdict-extension-records/{identity}.xml") == raw,
                "Complete supplemental record derivation changed")
    index = json.loads(frozen(PACKET / "evidence/jmdict-extension-index.json"))
    require(index["characters"] == catalog and index["recordOrder"] == partition["remainderIds"],
            "Supplemental exact-keb catalog changed")
    calibration = json.loads(frozen(CALIBRATION, CALIBRATION_SHA))
    old = json.loads(frozen(calibration["coreChain"], calibration["coreChainSha256"]))
    chain = json.loads(frozen(HERE / "core-chain-compact-002.json"))
    sources = [(name, frozen(PACKET / name, sums[name]), None) for name in core_sources(old)]
    coverage = verify_chain(chain, sources)
    forecast = json.loads(frozen(FORECAST))
    computed = compute_forecast(chain, calibration, sums, reference, catalog)
    require(all(forecast.get(key) == value for key, value in computed.items()),
            "Forecast not reproducible, or selected dictionary cost omitted")
    require(forecast["packetManifestSha256"] == packet_sha
            and forecast["chainManifestSha256"] == sha(frozen(HERE / "core-chain-compact-002.json")),
            "Forecast packet/chain binding changed")
    require(forecast["status"] == "PASS_CAPACITY_FORECAST", "No permitted capacity cap passes")
    guard.check()
    return {"status": "VERIFIED_IMMUTABLE_SUBSET_ONLY", "packetManifestSha256": packet_sha,
            "kanjidicRecords": len(kd), "jmdictCoreRecords": partition["core"],
            "jmdictRemainderRecords": partition["remainder"], "completeSupplementalRecordFiles": len(records),
            "chain": coverage, "chosenCaps": forecast["chosenCaps"],
            "projectedPeak": forecast["projectedWorstCasePeak"], "forecastIsNotAGuarantee": True}


def normalize_prompt(raw):
    return raw.replace(b"CLAUDE", b"FAMILY").replace(b"GPT", b"FAMILY").replace(
        b"-claude-", b"-family-").replace(b"-gpt-", b"-family-")


def verify_protocol(preflight):
    runs = preflight["runs"]
    require(list(runs) == ["claude", "gpt"], "Paired family order differs")
    prompts = []
    for family, spec in runs.items():
        config = json.loads(frozen(spec["auditConfig"]))
        for binding in config["files"]:
            frozen(binding["path"], binding["sha256"])
        prompts.append(frozen(spec["prompt"], spec["promptSha256"]))
        require(frozen(spec["kickoff"]).decode("ascii") == spec["kickoffText"],
                "Kickoff text binding differs")
        require(config["capacityForecastSha256"] == sha(frozen(FORECAST))
                and config["run"] == spec["run"] and config["expectedFamily"] == family
                and config["maxWebFetches"] == 0 and not Path(spec["report"]).exists(),
                "Fresh protocol identity, capacity or report absence differs")
    require(normalize_prompt(prompts[0]) == normalize_prompt(prompts[1]), "Prompt pair differs beyond identity")
    return {"status": "PASS_PAIRED_PROTOCOL", "runs": [spec["run"] for spec in runs.values()]}

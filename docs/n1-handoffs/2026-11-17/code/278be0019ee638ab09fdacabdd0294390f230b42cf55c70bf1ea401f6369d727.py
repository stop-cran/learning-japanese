"""Recompute B134 comparison extension and runtime checks."""
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from b134_common import HERE, PACKET, frozen, require, sha, verify_packet
from b134_capacity import OPTIONAL_ALLOWANCE, load_forecast, phase2_gate, telemetry, validate_capacity_config
from review_chain_with_optional import optional_unit_map, validate_selection


def context_telemetry(events, forecast, family, session=None):
    return telemetry(events, forecast, family, session)


def extension_sources(reply_text, sums):
    reference = json.loads(frozen(PACKET / "eligibility-reference.json", sums["eligibility-reference.json"]))
    index_name = "evidence/kanjidic2-full-unit-index.json"
    index = json.loads(frozen(PACKET / index_name, sums[index_name]))
    units = optional_unit_map(index)
    selection = validate_selection(reply_text, reference, units)
    require(selection["valid"], "Invalid independent D/E list: " + repr(selection["errors"]))
    entries = ET.fromstring(frozen(PACKET / "evidence/jmdict-families.xml", sums["evidence/jmdict-families.xml"]))
    sources, missing, matches = [], [], {}
    for entry in selection["entries"]:
        char = entry["character"]
        name = f"repo/kanji/{char}.md"
        if name in sums:
            sources.append((name + f" [{entry['label']}]", frozen(PACKET / name, sums[name]), None))
        else:
            missing.append(entry["requestLine"])
        matches[char] = [node.findtext("ent_seq") for node in entries
                         if char in [k.text for k in node.findall("k_ele/keb")]]
    for item in selection["optional"]:
        name = item["source"]
        require(name in sums and (item.get("sha256") is None or item["sha256"] == sums[name]),
                "Optional unit differs from the frozen unit index")
        sources.append((name + " [" + item["label"] + "]", frozen(PACKET / name, sums[name]), None))
    from b134_capacity import extension_upper
    optional_sources = [s for s in sources if " [O" in s[0]]
    require(extension_upper(optional_sources)["tokens"] <= OPTIONAL_ALLOWANCE,
            "HOLD/UNVERIFIED: optional evidence allowance exceeded; no truncation or reselection")
    return sources, missing, matches


def expected_message(chain, missing, matches):
    message = chain["segments"][0]["path"] + "\n"
    message += ("Missing entries:\n" + "\n".join(missing) if missing else "Missing entries: none")
    message += "\nDictionary matches in fully read core: " + json.dumps(matches, ensure_ascii=False, separators=(",", ":"))
    message += "\nNo exact-keb match in frozen union: " + (" ".join(k for k, v in matches.items() if not v) or "none")
    optional = [r["source"] for r in chain["sources"] if " [O" in r["source"]]
    message += "\nOptional evidence units: " + json.dumps(optional, ensure_ascii=False)
    return message


def verify_chain(chain, sources):
    require([row["source"] for row in chain["sources"]] == [row[0] for row in sources],
            "Extension source order differs")
    expected = {name: raw for name, raw, _ in sources}
    require(len(expected) == len(sources), "Duplicate extension source")
    rebuilt = {name: b"" for name in expected}
    next_line = dict.fromkeys(expected, 1)
    for index, segment in enumerate(chain["segments"], 1):
        data = frozen(segment["path"], segment["sha256"])
        require(segment["index"] == index and len(data) == segment["bytes"] < 16000, "Segment bound differs")
        tail = ("NEXT SEGMENT: " + chain["segments"][index]["path"] + "\n"
                if index < len(chain["segments"]) else
                "END OF CHAIN. Follow the run instruction's phase boundary.\n").encode()
        require(data.endswith(tail), "Extension successor differs")
        lines = data.splitlines(keepends=True)
        for part in segment["parts"]:
            name = part["source"]
            require(name in expected and part["sha256"] == sha(expected[name])
                    and part["a"] == next_line[name], "Extension source binding differs")
            value = b"".join(lines[part["segmentStart"] - 1:part["segmentEnd"]])
            require(value == b"".join(expected[name].splitlines(keepends=True)[part["a"] - 1:part["b"]]),
                    "Extension payload differs")
            rebuilt[name] += value
            next_line[name] = part["b"] + 1
    require(rebuilt == expected, "Extension incomplete")
    from b134_capacity import chain_cost
    cost = chain_cost(chain, sources)
    return {"sources": len(sources), "segments": len(chain["segments"]),
            "bytes": cost["chainBytes"], "tokens": cost["tokens"]}


def validate_prepared_extension(config, chain, reply_text, phase2_text, phase1_audit_path,
                                require_fresh_report=True):
    if require_fresh_report:
        from b134_common import validate_report_destination
        validate_report_destination(config)
    validate_capacity_config(config)
    forecast = load_forecast()
    sums = verify_packet()
    sources, missing, matches = extension_sources(reply_text, sums)
    coverage = verify_chain(chain, sources)
    require(phase2_text == expected_message(chain, missing, matches), "Incomplete phase-2 message")
    audit_raw = frozen(phase1_audit_path)
    audit = json.loads(audit_raw)
    require(audit["status"] == "PHASE1_READY" and audit["run"] == config["run"]
            and audit["bootstrapVerified"] and audit["bootstrapReplyVerified"]
            and audit["coreReleaseVerified"]
            and not audit["breaches"] and audit["phase1ListSha256"] == sha(reply_text.encode("utf-8")),
            "Phase-1 audit/list mismatch")
    event_bytes = frozen(Path(phase1_audit_path).parent / "events.jsonl", audit["eventsSha256"])
    events = [json.loads(line) for line in event_bytes.decode("utf-8").splitlines()]
    gate = phase2_gate(events, forecast, coverage["tokens"], config["expectedFamily"], audit["session"])
    require(gate["sendPhase2Message"], "Actual pre-phase-2 capacity gate failed")
    record = json.loads(frozen(HERE / f"{config['run']}-extension-preflight.json"))
    require(record["chainManifestSha256"] == sha(frozen(HERE / f"{config['run']}-extension.json"))
            and record["phase1AuditSha256"] == sha(audit_raw)
            and record["phase1ListSha256"] == sha(reply_text.encode("utf-8"))
            and record["phase2MessageSha256"] == sha(phase2_text.encode("utf-8"))
            and record["capacity"] == gate, "Extension preflight differs")
    return {"status": "PASS", "capacity": gate, "coverage": coverage, "dictionaryMatches": matches}

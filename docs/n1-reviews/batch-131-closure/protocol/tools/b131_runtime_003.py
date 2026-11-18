"""Verify capacity and exact independent comparison evidence before any phase-2 delivery."""
import json
import sys
from pathlib import Path

from b131_review_v3_common import FORECAST, HERE, PACKET, frozen, load_batch, require, sha, verify_packet
from b131_capacity_002 import load_forecast, phase2_gate, telemetry
from b131_preflight_002 import verify_chain
from prepare_chain_b131_003 import extension_sources

sys.path.insert(0, str(HERE))


def context_telemetry(events, forecast):
    observed = telemetry(events, forecast)
    starts = [event.get("data") or {} for event in events if event.get("type") == "session.start"]
    if len(starts) != 1 or starts[0].get("contextTier") != "long_context":
        observed["errors"].append("Expected one actual long_context session.start")
        observed["status"] = "HOLD"
    return observed


def expected_message(chain, missing, matches):
    text = chain["segments"][0]["path"] + "\n" + (
        "Missing entries:\n" + "\n".join(missing) if missing else "Missing entries: none")
    text += "\nDictionary matches: " + json.dumps(matches, ensure_ascii=False, separators=(",", ":"))
    text += "\nNo exact-keb match in frozen union: " + (
        " ".join(char for char, row in matches.items()
                 if not row["matchingCoreIds"] and not row["matchingRemainderIds"]) or "none")
    return text


def validate_prepared_extension(config, chain, reply_text, phase2_text, phase1_audit_path,
                                require_fresh_report=True):
    from b131_preflight_003 import validate_report_destination
    if require_fresh_report:
        validate_report_destination(config)
    from review_chain import validate_selection
    require(config["capacityForecastSha256"] == sha(frozen(FORECAST)), "Capacity forecast binding changed")
    forecast = load_forecast()
    _, sums, _ = verify_packet(load_batch(131))
    reference = json.loads(frozen(config["reference"]))
    selection = validate_selection(reply_text, reference)
    require(selection["valid"], "Invalid independent D/E selection")
    partition = json.loads(frozen(HERE / "derivation-verification-002.json"))["jmdictPartition"]
    sources, missing, matches, cost = extension_sources(selection, sums, partition)
    coverage = verify_chain(chain, sources)
    require(phase2_text == expected_message(chain, missing, matches),
            "Phase2 message is not the complete exact mechanical article/dictionary disclosure")
    audit_raw = frozen(phase1_audit_path)
    audit = json.loads(audit_raw)
    require(audit["status"] == "PHASE1_READY" and audit["run"] == config["run"]
            and audit["phase1ListSha256"] == sha(reply_text.encode("utf-8"))
            and not audit["breaches"], "Phase1 audit/list/run binding differs")
    event_bytes = frozen(Path(phase1_audit_path).parent / "events.jsonl", audit["eventsSha256"])
    events = [json.loads(line) for line in event_bytes.decode("utf-8").splitlines()]
    require(context_telemetry(events, forecast)["status"] == "PASS", "Invalid/compacted phase1 context")
    gate = phase2_gate(events, forecast, cost)
    require(gate["sendPhase2Message"] is True, "HOLD: actual pre-phase2 capacity gate exceeded")
    preflight = json.loads(frozen(HERE / f"{config['run']}-extension-preflight.json"))
    capacity = json.loads(frozen(preflight["capacity"]["path"], preflight["capacity"]["sha256"]))
    require(preflight["chainManifestSha256"] == sha(frozen(HERE / f"{config['run']}-extension.json"))
            and all(capacity.get(key) == value for key, value in gate.items())
            and capacity["dictionaryMatches"] == matches
            and capacity["phase1AuditSha256"] == sha(audit_raw)
            and capacity["selectionSha256"] == sha(reply_text.encode("utf-8"))
            and capacity["forecastSha256"] == sha(frozen(FORECAST)),
            "Selected dictionary cost, records or runtime-capacity proof omitted/changed")
    return {"status": "PASS", "capacity": gate, "coverage": coverage,
            "independentlyRecomputedSupplementalDictionaryBytes": cost["supplementalDictionaryBytes"],
            "dictionaryMatches": matches}

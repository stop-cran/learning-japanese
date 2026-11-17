"""Build a phase-1-audited, actual-telemetry-gated B134 extension."""
import argparse
import json
from pathlib import Path
from b134_common import HERE, frozen, freeze_json, require, sha, start_guard, verify_packet, write_frozen
from b134_capacity import load_forecast, phase2_gate, extension_upper
from b134_runtime import expected_message, extension_sources, verify_chain
from review_chain_with_optional import build_chain


def article_upper(raw):
    lines = raw.splitlines(keepends=True)
    require(raw.endswith(b"\n") and all(len(line) <= 13900 for line in lines), "Invalid article line")
    segments, size = 1, 0
    for line in lines:
        if size + len(line) > 13900:
            segments += 1
            size = 0
        size += len(line)
    return len(raw) + 2100 * (segments + 1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--reply", type=Path, required=True)
    parser.add_argument("--phase1-audit", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(frozen(args.config))
    run = config["run"]
    require(run in ("N1-B134-CLAUDE-FRESH-002", "N1-B134-GPT-FRESH-002"), "Invalid run")
    require(run in args.phase1_audit.parts, "Audit path is not inside run directory")
    output = HERE / f"{run}-extension.json"
    message = HERE / f"{run}-phase2-message.txt"
    preflight = HERE / f"{run}-extension-preflight.json"
    directory = HERE / "chains" / (run + "-extension-001")
    require(not any(p.exists() for p in (output, message, preflight, directory)), "Preserve existing outputs")
    guard, _ = start_guard("B134 selected extension")
    try:
        reply_raw = frozen(args.reply)
        audit_raw = frozen(args.phase1_audit)
        audit = json.loads(audit_raw)
        require(audit["status"] == "PHASE1_READY" and audit["run"] == run and not audit["breaches"]
                and audit["bootstrapVerified"] and audit["bootstrapReplyVerified"]
                and audit["coreReleaseVerified"]
                and audit["phase1ListSha256"] == sha(reply_raw)
                and audit["capacityTelemetry"]["status"] == "PASS", "Phase 1 is not bound and ready")
        event_raw = frozen(args.phase1_audit.parent / "events.jsonl", audit["eventsSha256"])
        events = [json.loads(line) for line in event_raw.decode("utf-8").splitlines()]
        sums = verify_packet(guard)
        sources, missing, matches = extension_sources(reply_raw.decode("utf-8"), sums)
        forecast = load_forecast()
        upper = extension_upper(sources)["tokens"]
        require(phase2_gate(events, forecast, upper, config["expectedFamily"], audit["session"])["sendPhase2Message"],
                "HOLD: pre-phase-2 capacity gate")
        chain = build_chain(sources, directory, output, guard, "B134 " + run + " extension")
        coverage = verify_chain(chain, sources)
        gate = phase2_gate(events, forecast, coverage["tokens"], config["expectedFamily"], audit["session"])
        require(gate["sendPhase2Message"], "HOLD: actual extension capacity gate")
        message_text = expected_message(chain, missing, matches)
        message_binding = write_frozen(message, message_text.encode("utf-8"))
        record = {"status": "PREPARED_CAPACITY_GATED_EXTENSION", "run": run,
                  "chainManifestSha256": sha(frozen(output)), "phase1AuditSha256": sha(audit_raw),
                  "phase1ListSha256": sha(reply_raw), "phase2MessageSha256": message_binding["sha256"],
                  "capacity": gate, "coverage": coverage}
        print(json.dumps(freeze_json(preflight, record)))
    finally:
        require(not guard.finish()["breach"], "Extension RAM breach")


if __name__ == "__main__":
    main()

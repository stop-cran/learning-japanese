"""Build compact-002 core or a gated independent article-plus-dictionary extension."""
import argparse
import json
import sys
from pathlib import Path

from b131_review_v2_common import (
    CALIBRATION, CALIBRATION_SHA, FORECAST, HERE, OLD_HERE, PACKET, RUNS,
    freeze_json, frozen, load_batch, require, sha, start_guard, verify_packet, write_frozen)
from b131_review_v2_derivations import selected_supplements, verify_supplements
from b131_capacity_002 import extension_tokens, load_forecast, phase2_gate


def core_sources(old_chain):
    drop = {"evidence/xml-presentation.json", "evidence/baseline-title-index.txt",
            "evidence/font-cmap.json", "evidence/dictionary-index.json"}
    replace = {"evidence/kanjidic2-records.xml": "evidence/kanjidic2-review-projection.xml",
               "evidence/jmdict-families.xml": "evidence/jmdict-review-core.xml"}
    output = []
    for row in old_chain["sources"]:
        name = row["source"]
        if name in drop:
            continue
        output.append(replace.get(name, name))
        if name == "evidence/title-index.txt":
            output.append("evidence/title-index-delta.txt")
    return output


def extension_sources(selection, sums, partition):
    source_rows, missing = [], []
    for entry in selection["entries"]:
        name = f"repo/kanji/{entry['character']}.md"
        if name in sums:
            source_rows.append((name + f" [{entry['label']}]", frozen(PACKET / name, sums[name]), None))
        else:
            missing.append(entry["requestLine"])
    selected, matches = selected_supplements(
        frozen(PACKET / "evidence/jmdict-families.xml"), partition,
        [entry["character"] for entry in selection["entries"]])
    verify_supplements(frozen(PACKET / "evidence/jmdict-families.xml"), partition,
                       [entry["character"] for entry in selection["entries"]], selected)
    for identity, raw in selected:
        name = f"evidence/jmdict-extension-records/{identity}.xml"
        require(frozen(PACKET / name, sums[name]) == raw, "Supplemental complete record changed")
        source_rows.append((name, raw, None))
    article_rows = [row for row in source_rows if row[0].startswith("repo/kanji/")]
    cost = extension_tokens(sum(len(row[1]) for row in article_rows),
                            sum(len(raw) for _, raw in selected),
                            len(selection["entries"]), len(selected))
    return source_rows, missing, matches, cost


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("batch", type=int)
    parser.add_argument("--run", choices=RUNS)
    parser.add_argument("--reply", type=Path)
    parser.add_argument("--phase1-audit", type=Path)
    args = parser.parse_args(argv)
    require(bool(args.run) == bool(args.reply) == bool(args.phase1_audit), "Extension requires all three arguments")
    sys.path.insert(0, str(HERE))
    from review_chain import build_chain, validate_selection
    guard, _ = start_guard("B131 compact-002 ordered chain preparation")
    try:
        root, sums, packet_sha = verify_packet(load_batch(args.batch), guard)
        if not args.run:
            calibration = json.loads(frozen(CALIBRATION, CALIBRATION_SHA))
            old_chain = json.loads(frozen(calibration["coreChain"], calibration["coreChainSha256"]))
            names = core_sources(old_chain)
            sources = [(name, frozen(root / name, sums[name]), None) for name in names]
            require(len(frozen(root / "repo/docs/content-format.md").splitlines()) == 1419,
                    "Content-format complete1419-line contract changed")
            directory = HERE / "chains" / "b131-initial-compact-002"
            manifest_path = HERE / "core-chain-compact-002.json"
            preflight = HERE / "core-chain-compact-002-preflight.json"
            chain = build_chain(sources, directory, manifest_path, guard, "B131 compact-002 required core")
            record = {"status": "PREPARED_CORE_ONLY", "packetManifestSha256": packet_sha,
                      "chainManifestSha256": sha(frozen(manifest_path)),
                      "sources": len(sources), "segments": len(chain["segments"]),
                      "bytes": sum(s["bytes"] for s in chain["segments"]),
                      "maxSegmentBytes": max(s["bytes"] for s in chain["segments"])}
        else:
            forecast = load_forecast()
            audit_raw = frozen(args.phase1_audit)
            audit = json.loads(audit_raw)
            reply = frozen(args.reply)
            require(args.run in args.phase1_audit.parts and audit["run"] == args.run
                    and audit["status"] == "PHASE1_READY" and not audit["breaches"]
                    and audit["capacityTelemetry"]["status"] == "PASS"
                    and audit["phase1ListSha256"] == sha(reply), "Phase1 is not ready/bound to this run")
            reference = json.loads(frozen(PACKET / "eligibility-reference.json"))
            selection = validate_selection(reply.decode("utf-8"), reference)
            require(selection["valid"], "Invalid or over-cap list: " + str(selection["errors"]))
            partition = json.loads(frozen(HERE / "derivation-verification-002.json"))["jmdictPartition"]
            sources, missing, matches, cost = extension_sources(selection, sums, partition)
            events_raw = frozen(args.phase1_audit.parent / "events.jsonl", audit["eventsSha256"])
            events = [json.loads(line) for line in events_raw.decode("utf-8").splitlines()]
            capacity = phase2_gate(events, forecast, cost)
            capacity_record = freeze_json(HERE / f"{args.run}-pre-phase2-capacity.json", {
                **capacity, "forecastSha256": sha(frozen(FORECAST)), "phase1AuditSha256": sha(audit_raw),
                "selectionSha256": sha(reply), "dictionaryMatches": matches,
                "absentExactKebCharacters": [char for char, row in matches.items()
                                             if not row["matchingCoreIds"] and not row["matchingRemainderIds"]]})
            if not capacity["sendPhase2Message"]:
                print(json.dumps({"status": "HOLD_PRE_PHASE2_CAPACITY", "capacity": capacity_record,
                                  "phase2MessageCreated": False}))
                return 1
            directory = HERE / "chains" / f"b131-{args.run}-extension-002"
            manifest_path = HERE / f"{args.run}-extension.json"
            chain = build_chain(sources, directory, manifest_path, guard, "B131 " + args.run + " extension")
            message = chain["segments"][0]["path"] + "\n" + (
                "Missing entries:\n" + "\n".join(missing) if missing else "Missing entries: none")
            message += "\nDictionary matches: " + json.dumps(matches, ensure_ascii=False, separators=(",", ":"))
            message += "\nNo exact-keb match in frozen union: " + (
                " ".join(char for char, row in matches.items()
                         if not row["matchingCoreIds"] and not row["matchingRemainderIds"]) or "none")
            message_binding = write_frozen(HERE / f"{args.run}-phase2-message.txt", message.encode("utf-8"))
            preflight = HERE / f"{args.run}-extension-preflight.json"
            record = {"status": "PREPARED_CAPACITY_GATED_EXTENSION", "run": args.run,
                      "packetManifestSha256": packet_sha, "chainManifestSha256": sha(frozen(manifest_path)),
                      "capacity": capacity_record, "phase2Message": message_binding,
                      "dictionaryMatches": matches, "sources": len(sources), "segments": len(chain["segments"])}
        record["memory"] = guard.finish()
        require(not record["memory"]["breach"], "Chain RAM breach")
        result = freeze_json(preflight, record)
        print(json.dumps({"record": result, **{k: record[k] for k in ("status", "sources", "segments")}}))
        return 0
    except (Exception, KeyboardInterrupt):
        guard.finish()
        raise


if __name__ == "__main__":
    sys.exit(main())

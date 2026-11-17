"""Collect immutable original B134 reviews for the later replacement closure.

The output is a local closure fragment, not publication approval. Full event
payloads, admissions and source-capture chain segments remain local.
"""
import json
import sys
from pathlib import Path

from archive_b129_chains import prepare
from b132_closure_records import archive_path
from b134_initial_records import INITIALS, P, PREFLIGHT, actual_initial, disposition_ids
from b134_review_history import CAPACITY_SHA, FAILED_SESSION, REJECTION_SHA
from common import WS, freeze_json, frozen, json_bytes, require, sha, start_guard, write_frozen

ROOT = WS / "scratch-134" / "review"


def put(files, name, raw):
    archive_path(name)
    require(not name.endswith((".jsonl", ".html", ".htm")), "Raw event/HTML payload must remain local")
    require(name not in files or files[name] == raw, "Conflicting archive bytes: " + name)
    files[name] = raw
    return {"path": name, "sha256": sha(raw)}


def read_ref(path, digest=None):
    path = Path(path).resolve()
    require(path.is_relative_to(ROOT), "Original review evidence escaped its root")
    raw = frozen(path, digest)
    return raw, {"path": str(path), "sha256": sha(raw), "bytes": len(raw)}


def add_chain(files, label, path, digest, guard):
    raw, _ = read_ref(path, digest)
    manifest = json.loads(raw)
    segments = {}
    for row in manifest["segments"]:
        part = Path(row["path"]).resolve()
        require(part.is_relative_to(P / "chains"), "Original chain segment escaped its root")
        segments[row["path"]], _ = read_ref(part, row["sha256"])
        guard.check()
    archived, retention = prepare(raw, segments)
    for name, value in archived.items():
        put(files, "chains/" + label + "/" + name, value)
    return retention


def collect_originals(guard):
    files, entries, local, chains, obligations = {}, [], [], {}, {}
    preflight_raw, _ = read_ref(PREFLIGHT["path"], PREFLIGHT["sha256"])
    preflight = json.loads(preflight_raw)
    put(files, "protocol/original-preflight.json", preflight_raw)
    for family in INITIALS:
        spec, refs, derivatives, claims = actual_initial(family)
        run = spec["run"]
        prefix = "reviews/" + run + "/"
        entry = {**spec, **claims, "reviewAccepted": True}
        for field in ("report", "final", "acceptance", "adjudication", "auditConfig"):
            ref = refs[field]
            raw, _ = read_ref(ref["path"], ref["sha256"])
            entry[field] = put(files, prefix + field + (".md" if field == "report" else ".json"), raw)
        for name, raw in derivatives.items():
            entry[name] = put(files, prefix + name + ".json", raw)
        report = files[prefix + "report.md"]
        obligations[run] = disposition_ids(report, claims)
        final = json.loads(files[prefix + "final.json"])
        config = json.loads(files[prefix + "auditConfig.json"])
        audit_raw, audit_ref = read_ref(refs["audit"]["path"], refs["audit"]["sha256"])
        audit = json.loads(audit_raw)
        events, events_ref = read_ref(Path(refs["audit"]["path"]).parent / "events.jsonl",
                                      audit["eventsSha256"])
        require(len(events) == audit["eventsBytes"] and len(events.splitlines()) == audit["eventsCount"],
                "Frozen original event snapshot differs")
        local.extend((audit_ref, events_ref))
        launch_raw, _ = read_ref(P / (run + "-launch.json"))
        launch = json.loads(launch_raw)
        require(launch["run"] == run and launch["session"] == spec["session"]
                and launch["candidate"] == spec["snapshot"]
                and launch["start"]["selectedModel"] == config["contextProfile"]["selectedModel"]
                and launch["start"]["contextTier"] == "long_context", "Original launch differs")
        entry["launch"] = put(files, prefix + "launch.json", launch_raw)
        admission_raw, admission_ref = read_ref(launch["admission"]["path"],
                                              launch["admission"]["sha256"])
        admission = json.loads(admission_raw)
        require(admission["admitted"] is True and admission["candidate"] == spec["snapshot"]
                and admission["run"] == run, "Original admission differs")
        local.append(admission_ref)
        for ref in admission["snapshots"].values():
            _, checked = read_ref(ref["path"], ref["sha256"])
            local.append(checked)
        for name in ("prompt", "kickoff"):
            ref = preflight["runs"][family][name]
            raw, _ = read_ref(ref["path"], ref["sha256"])
            require(config[name] == ref["path"], "Original prompt configuration differs")
            if name == "kickoff":
                require(ref["sha256"] == launch["kickoffSha256"], "Original kickoff differs")
            put(files, prefix + name + ".txt", raw)
        phase_raw, _ = read_ref(P / (run + "-phase1.json"))
        phase = json.loads(phase_raw)
        require(phase["readyForPhase2"] is True and phase["run"] == run
                and phase["session"] == spec["session"], "Original phase one differs")
        put(files, prefix + "phase1.json", phase_raw)
        phase_audit, phase_audit_ref = read_ref(Path(phase["auditDir"]) / "audit.json",
                                              phase["auditSha256"])
        require(json.loads(phase_audit)["session"] == spec["session"], "Phase audit session differs")
        local.append(phase_audit_ref)
        raw, _ = read_ref(Path(phase["auditDir"]) / "phase1-list.txt")
        put(files, prefix + "phase1-list.txt", raw)
        for name in ("phase2-message.txt", "extension-preflight.json"):
            raw, _ = read_ref(P / (run + "-" + name))
            put(files, prefix + name, raw)
        for folder in (final["auditReceipt"], final["structureReceipt"],
                       phase["auditReceipt"], phase["extensionReceipt"]):
            receipt_raw, receipt_ref = read_ref(Path(folder) / "receipt.json")
            receipt = json.loads(receipt_raw)
            require(receipt["exitCode"] == 0 and not receipt["memory"]["breach"]
                    and receipt["cleanupError"] is None, "Original lifecycle gate failed")
            _, log_ref = read_ref(Path(folder) / "output.log", receipt["logSha256"])
            local.extend((receipt_ref, log_ref))
            guard.check()
        extension = P / (run + "-extension.json")
        extension_raw, _ = read_ref(extension)
        require(len(json.loads(extension_raw)["segments"]) == audit["extensionRequired"],
                "Original extension read count differs")
        chains[run] = add_chain(files, run, extension, sha(extension_raw), guard)
        if "core" not in chains:
            core = config["coreManifest"]
            chains["core"] = add_chain(files, "core", core, preflight["coreManifestSha256"], guard)
        require(chains["core"]["originalSegments"] == audit["coreRequired"],
                "Original core read count differs")
        entry["originalAuditSha256"] = refs["audit"]["sha256"]
        entry["actualResponseModels"] = audit["actualResponseModels"]
        entries.append(entry)
        guard.check()
    return files, entries, local, chains, obligations


def collect_attempt_history(files):
    capacity_raw, _ = read_ref(ROOT / "confirmation-capacity-fallback-001" / "measurement.json",
                              CAPACITY_SHA)
    capacity = json.loads(capacity_raw)
    require(capacity["status"] == "HOLD" and capacity["startupGate"] == 700000
            and capacity["projectedPeak"] > capacity["startupGate"], "Historical capacity hold differs")
    rejected_raw, _ = read_ref(ROOT / "fresh-independent-001-rejection" / "rejection.json", REJECTION_SHA)
    rejected = json.loads(rejected_raw)
    require(rejected["status"] == "REJECTED_PREPARATION_AND_LAUNCH_NOT_CARD_VERDICT"
            and rejected["session"] == FAILED_SESSION and rejected["reportExists"] is False,
            "Rejected preparation cannot be accepted as a review")
    ref = rejected["eventSnapshot"]
    events, event_ref = read_ref(ref["path"], ref["sha256"])
    require(len(events) == ref["bytes"], "Rejected event snapshot differs")
    return {
        "replacementBasis": {
            "reason": "original-reviewer-context-capacity", "status": "HOLD", "reviewAccepted": False,
            "measurement": put(files, "history/original-reviewer-capacity-hold.json", capacity_raw),
        },
        "nonAcceptedReviews": [{
            "session": FAILED_SESSION, "status": rejected["status"],
            "reviewAccepted": False, "reportPresent": False,
            "rejection": put(files, "history/rejected-fresh-001.json", rejected_raw),
        }],
    }, event_ref


def main(output):
    require(output.parent == ROOT and not output.exists(), "Use a new direct review output directory")
    guard, _ = start_guard("B134 original review archive collection")
    try:
        files, entries, local, chains, obligations = collect_originals(guard)
        attempts, event_ref = collect_attempt_history(files)
        local.append(event_ref)
        put(files, "verification/original-local-retention.json", json_bytes({
            "files": local,
            "policy": "Full events, audits, admissions and rosters remain local; hashes retain bindings.",
        }))
        for name, raw in sorted(files.items()):
            write_frozen(output / name, raw)
            guard.check()
    finally:
        memory = guard.finish()
        require(not memory["breach"], "Original archive RAM breach")
    result = {
        "status": "COLLECTED_ORIGINALS_NOT_REVIEW_CLOSURE", "batch": 134,
        "reviewLineage": entries, **attempts, "chainRetention": chains,
        "obligations": obligations, "recordedFileSha256": {name: sha(raw) for name, raw in files.items()},
        "producerSha256": sha(Path(__file__).read_bytes()), "memory": memory,
        "limits": "Immutable local closure fragment only. No replacement review or claim closure. "
                  "Publication privacy/copyright window scans still required on the assembled archive.",
    }
    print(json.dumps(freeze_json(output / "index.json", result)))


if __name__ == "__main__":
    require(len(sys.argv) == 2, "b134_original_archive.py NEW_OUTPUT_DIRECTORY")
    main(Path(sys.argv[1]).resolve())

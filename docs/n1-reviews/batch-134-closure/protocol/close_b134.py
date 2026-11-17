"""Assemble B134 closure only from accepted fresh reviews and complete claim dispositions.

Usage: close_b134.py dry|real REQUEST_JSON OUTPUT
REQUEST_JSON binds reviews (spec, preflight, final, launch, phase1, extension),
resolution, evidence (archivePath, path, sha256), protectedSources and limits.
All review inputs stay below scratch-134/review. Full native extracts and raw
events remain local; prompt-only bootstrap and core-release records are bound
to the final event stream. No publication credit is granted by this assembler.
"""
import copy
import json
import sys
from pathlib import Path

from archive_b129_chains import is_local_only_source, prepare
from b133_closure_retention import retain_overlapping_chains
from b134_closure_progress import closed_progress
from b134_initial_records import INITIALS, actual_initial, disposition_ids
from b134_original_archive import put
from b134_replacement_records import collect_replacement_record
from b134_review_history import FAILED_SESSION, MODE, validate_resolution
from close_b131 import add_protected
from close_b132 import publication_findings
from common import COORDINATOR, WS, freeze_json, frozen, json_bytes, require, sha, start_guard, write_frozen
from run_b134_closure_checks import BASE, BATCH, CANDIDATE, CLOSURE, HERE, MEMBERS, PROGRESS, REPO, lineage
from verify_b134_packet import RUNNER
from verify_b134_sources import Git

ROOT = HERE / "review"
REVIEWED = "355cccb840d22e7313e79f234eb93d1367e00352"
CORE_ROOT = ROOT / "fresh-independent-002" / "projected-successor-011"
CORE_SHA = "49db3ba57325e7913a533b3b11b7ad810e6085123474327b037a6de7c7c31719"
PACKET_SHA = "adeac0009e52039a57fd3121a45f0e91eb697a6f35b131db0517922f3d1b540c"
ORIGINAL = ROOT / "original-archive-001"
ORIGINAL_SHA = "91d55a27716a227e6fd8fbe1668f50bc1b96cbedcc32a953525294d2299102c1"
AUTHOR = "c222bfef-4874-456d-b830-1b09165b1f40"
METER_SESSIONS = {"439ba40b-5cb0-4669-a3c8-de1e385dc321", "00039869-7c08-4e94-8224-a5d4fd673a60"}
HELD_SESSION = "adb64370-2aa5-4eb8-9e28-c5cf3111bf2b"
HELD_RUN = "N1-B134-CLAUDE-FRESH-002"
HOLD_PATH = ROOT / "fresh-002-launch-hold-001" / "quarantine.json"
HOLD_SHA = "4b8eea0869cd6aaa64b3f7ec7b0418054e4c764459c1ae30b488887f5c340576"
PROOFS = {
    "reconciliation-sources": ("reconciliation-verification-001/verification.json",
                               "7ea9e7dde1989b5d1eb71bed3b5789ab77f4e3713277591b4841eeb2b0295da1"),
    "reconciliation-gates": ("reconciliation-gate-verification-001/verification.json",
                             "7b0e846ede88b4a5350df16b58df0c4461e4ba83fc0208f006d65c3951170787"),
    "lossless-core": ("successor-011-verification-001/verification.json",
                      "7ad06c861b4af2b2f722e54e6e200531919fb6cad6f8cd81541ea2d291571577"),
    "measured-capacity": ("meter-011-capacity-001/capacity.json",
                         "3aec7dc4d2701303145c8bfddbb698e2c180065c2298d115ae5b23b249a020d9"),
}


def read_review(path, digest=None):
    path = Path(path).resolve()
    require(path.is_relative_to(ROOT), "Review input escaped scratch-134/review")
    return frozen(path, digest)


def ref_bytes(ref):
    return read_review(ref["path"], ref["sha256"])


def protected_source(name):
    return (is_local_only_source(name)
            or (name.startswith("reconciliation/evidence/native-") and name.endswith(".txt")))


def retained_chain(manifest_raw, segments):
    files, retention = prepare(manifest_raw, segments)
    manifest = json.loads(manifest_raw)
    for row in manifest["segments"]:
        if row["index"] not in retention["archivedSegmentIndices"]:
            continue
        protected = [part for part in row["parts"] if protected_source(part["source"])]
        if not protected:
            continue
        del files[Path(row["path"]).name + ".gz"]
        retention["archivedSegmentIndices"].remove(row["index"])
        retention["localOnlySegments"].append({
            "index": row["index"], "sha256": row["sha256"], "bytes": len(segments[row["path"]]),
            "sources": [{"source": part["source"], "sha256": part["sha256"],
                         "firstLine": part["a"], "lastLine": part["b"]} for part in protected],
        })
    retention["localOnlySegments"].sort(key=lambda row: row["index"])
    files["retention.json"] = json_bytes(retention)
    return files, retention


def add_chain(files, label, ref, guard):
    raw = ref_bytes(ref)
    manifest = json.loads(raw)
    segments = {}
    for row in manifest["segments"]:
        segments[row["path"]] = read_review(row["path"], row["sha256"])
        guard.check()
    archived, retention = retained_chain(raw, segments)
    for name, value in archived.items():
        put(files, "chains/" + label + "/" + name, value)
    return retention


def require_fresh_inventory(report, claims):
    tracked = {value for values in claims.values() for value in values}
    require(set(disposition_ids(report, claims)) <= tracked,
            "A fresh report claim is missing from the explicit adjudication inventory")


def verify_audited_chain(manifest, audit, events, role):
    rows = manifest["segments"]
    calls = [call for call in audit["calls"] if call.get("role", "").startswith(role + "-")]
    require(rows and len(rows) == len(calls)
            and [call["role"] for call in calls] == [f"{role}-{i}" for i in range(1, len(rows) + 1)]
            and [call["path"] for call in calls] == [row["path"] for row in rows],
            "Archived chain differs from the exact audited read sequence")
    for row, call in zip(rows, calls, strict=True):
        returned = [event["data"] for event in events if event["type"] == "tool.execution_complete"
                    and event["data"].get("toolCallId") == call["id"]]
        require(call["success"] is True and len(returned) == 1 and returned[0]["success"] is True,
                "Chain read did not complete exactly once")
        raw = returned[0]["result"]["content"].encode("utf-8")
        require(len(raw) == row["bytes"] and sha(raw) == row["sha256"],
                "Archived chain bytes differ from the actual tool response")


def retain_bootstrap(files, prefix, spec, config, config_ref, launch, final_events):
    authorization_raw = read_review(config["coreAuthorizationPath"])
    authorization = json.loads(authorization_raw)
    require(authorization["bootstrapRecordPath"] == config["bootstrapRecordPath"],
            "Core authorization names another bootstrap record")
    bootstrap_raw = read_review(config["bootstrapRecordPath"], authorization["bootstrapRecordSha256"])
    bootstrap = json.loads(bootstrap_raw)
    require(bootstrap["status"] == "PROMPT_ONLY_BOOTSTRAP_PASS"
            and authorization["status"] == "CORE_RELEASE_AUTHORIZED",
            "Bootstrap or core release did not pass")
    profile = config["contextProfile"]
    for record in (bootstrap, authorization):
        require(record["run"] == spec["run"] and record["sessionId"] == spec["session"]
                and record["candidate"] == spec["snapshot"] and record["base"] == config["base"] == CANDIDATE
                and record["configSha256"] == config_ref["sha256"]
                and record["selectedModel"] == profile["selectedModel"]
                and record["contextTier"] == "long_context"
                and record["maxPromptTokens"] == profile["maxPromptTokens"]
                and record["compactionEvents"] == [],
                "Bootstrap or core authorization belongs to another review/context")
    require(bootstrap["kickoffSha256"] == launch["kickoffSha256"]
            and bootstrap["promptSha256"] == sha(read_review(config["prompt"]))
            and authorization["eventSnapshotPath"] == bootstrap["eventSnapshotPath"]
            and authorization["eventSnapshotSha256"] == bootstrap["eventSnapshotSha256"],
            "Bootstrap prompt or authorized event snapshot differs")
    snapshot = read_review(bootstrap["eventSnapshotPath"], bootstrap["eventSnapshotSha256"])
    events = [json.loads(line) for line in snapshot.decode("utf-8").splitlines()]
    final_messages = [(index, event["data"].get("content")) for index, event in enumerate(events)
                      if event["type"] == "assistant.message"
                      and not event["data"].get("toolRequests")]
    require(len(final_messages) == 1
            and final_messages[0][1] == config["bootstrapResponseText"]
            and any(event["type"] == "assistant.turn_end"
                    for event in events[final_messages[0][0] + 1:]),
            "Bootstrap does not contain the completed prompt-only response")
    require(len(snapshot) == bootstrap["eventSnapshotBytes"] and events
            and len(events) == bootstrap["eventCount"]
            and events[-1]["type"] == bootstrap["eventSnapshotLastType"]
            and final_events.startswith(snapshot),
            "Final execution does not retain the complete authorized bootstrap prefix")
    entries = {
        "bootstrap": put(files, prefix + "bootstrap.json", bootstrap_raw),
        "coreAuthorization": put(files, prefix + "core-authorization.json", authorization_raw),
    }
    return entries, {"path": bootstrap["eventSnapshotPath"],
                     "sha256": sha(snapshot), "bytes": len(snapshot)}


def retain_launch_hold(files):
    raw = read_review(HOLD_PATH, HOLD_SHA)
    hold = json.loads(raw)
    require(hold["status"] == "QUARANTINED_PROMPT_ONLY_AUTOPILOT_LAUNCH_NOT_REVIEW"
            and hold["run"] == HELD_RUN and hold["session"] == HELD_SESSION
            and hold["candidate"] == REVIEWED and hold["promptReads"] == 1
            and hold["coreReads"] == 0 and hold["extraAutopilotUserTurns"] == 5
            and hold["reportCreated"] is False and hold["reviewAccepted"] is False,
            "Prompt-only failed launch was changed or promoted to review evidence")
    events = ref_bytes(hold["events"])
    require(len(events) == hold["events"]["bytes"], "Failed-launch snapshot length differs")
    receipt_raw = ref_bytes(hold["failureReceipt"])
    receipt = json.loads(receipt_raw)
    require(receipt["exitCode"] != 0 and receipt["cleanupError"] is None
            and not receipt["memory"]["breach"], "Launch failure receipt differs")
    ref = put(files, "history/fresh-002-launch-hold.json", raw)
    entry = {
        "run": HELD_RUN, "session": HELD_SESSION, "status": hold["status"],
        "reviewAccepted": False, "reportPresent": False, "quarantine": ref,
    }
    return entry, [hold["events"], hold["failureReceipt"]]


def add_replacement(files, item, guard):
    spec = item["spec"]
    require(spec["snapshot"] == REVIEWED and spec["session"] != HELD_SESSION
            and spec["run"] != HELD_RUN, "Fresh review reuses a failed launch or another snapshot")
    refs, derivatives, claims = collect_replacement_record(
        spec, item["preflight"], item["final"], read_review)
    require_fresh_inventory(ref_bytes(refs["report"]), claims)
    preflight, final = (json.loads(ref_bytes(item[key])) for key in ("preflight", "final"))
    require(preflight["coreManifestSha256"] == CORE_SHA, "Fresh review used another core")
    config = json.loads(ref_bytes(refs["auditConfig"]))
    audit = json.loads(ref_bytes(refs["audit"]))
    prefix = "reviews/" + spec["run"] + "/"
    entry = {
        **spec, **claims, "reviewAccepted": True,
        "replacesInitialRun": "N1-B134-" + spec["family"].upper() + "-001",
    }
    for key in ("report", "final", "acceptance", "adjudication", "preflight", "auditConfig"):
        entry[key] = put(files, prefix + key + (".md" if key == "report" else ".json"),
                         ref_bytes(refs[key]))
    for key, raw in derivatives.items():
        entry[key] = put(files, prefix + key + ".json", raw)
    local = [refs["audit"]]
    events_path = Path(refs["audit"]["path"]).parent / "events.jsonl"
    events = read_review(events_path, audit["eventsSha256"])
    require(len(events) == audit["eventsBytes"], "Final execution snapshot length differs")
    local.append({"path": str(events_path), "sha256": sha(events), "bytes": len(events)})
    event_rows = [json.loads(line) for line in events.decode("utf-8").splitlines()]
    core = json.loads(read_review(config["coreManifest"], CORE_SHA))
    verify_audited_chain(core, audit, event_rows, "core")
    launch_raw, phase_raw = ref_bytes(item["launch"]), ref_bytes(item["phase1"])
    launch, phase = json.loads(launch_raw), json.loads(phase_raw)
    require(launch["run"] == phase["run"] == spec["run"]
            and launch["session"] == phase["session"] == spec["session"]
            and launch["candidate"] == REVIEWED and phase["readyForPhase2"] is True,
            "Fresh launch or phase-one binding differs")
    require(launch["start"]["selectedModel"] == config["contextProfile"]["selectedModel"]
            and launch["start"]["contextTier"] == "long_context", "Fresh launch context differs")
    bootstrap_entries, bootstrap_events = retain_bootstrap(
        files, prefix, spec, config, refs["auditConfig"], launch, events)
    entry.update(bootstrap_entries)
    local.append(bootstrap_events)
    entry["launch"] = put(files, prefix + "launch.json", launch_raw)
    put(files, prefix + "phase1.json", phase_raw)
    admission_raw = ref_bytes(launch["admission"])
    admission = json.loads(admission_raw)
    require(admission["run"] == spec["run"] and admission["candidate"] == REVIEWED
            and admission["admitted"] is True, "Fresh admission differs")
    local.append(launch["admission"])
    for ref in admission["snapshots"].values():
        ref_bytes(ref)
        local.append(ref)
    for key in ("prompt", "kickoff"):
        raw = read_review(config[key])
        put(files, prefix + key + ".txt", raw)
        if key == "kickoff":
            require(sha(raw) == launch["kickoffSha256"], "Fresh kickoff hash differs")
    phase_audit_path = Path(phase["auditDir"]) / "audit.json"
    phase_audit_raw = read_review(phase_audit_path, phase["auditSha256"])
    require(json.loads(phase_audit_raw)["session"] == spec["session"], "Phase audit session differs")
    local.append({"path": str(phase_audit_path), "sha256": sha(phase_audit_raw)})
    put(files, prefix + "phase1-list.txt", read_review(Path(phase["auditDir"]) / "phase1-list.txt"))
    for folder in (final["auditReceipt"], final["structureReceipt"],
                   phase["auditReceipt"], phase["extensionReceipt"]):
        path = Path(folder)
        receipt_raw = read_review(path / "receipt.json")
        receipt = json.loads(receipt_raw)
        require(receipt["exitCode"] == 0 and not receipt["memory"]["breach"]
                and receipt["cleanupError"] is None, "Fresh lifecycle command failed")
        log = read_review(path / "output.log", receipt["logSha256"])
        local.extend(({"path": str(path / "receipt.json"), "sha256": sha(receipt_raw)},
                      {"path": str(path / "output.log"), "sha256": sha(log)}))
    extension = json.loads(ref_bytes(item["extension"]))
    require(len(extension["segments"]) == audit["extensionRequired"], "Extension coverage differs")
    verify_audited_chain(extension, audit, event_rows, "extension")
    retention = add_chain(files, spec["run"], item["extension"], guard)
    entry["originalAuditSha256"] = refs["audit"]["sha256"]
    return entry, local, retention


def load_originals():
    raw = read_review(ORIGINAL / "index.json", ORIGINAL_SHA)
    original = json.loads(raw)
    require(original["status"] == "COLLECTED_ORIGINALS_NOT_REVIEW_CLOSURE",
            "Original history fragment status differs")
    files = {name: read_review(ORIGINAL / name, digest)
             for name, digest in original["recordedFileSha256"].items()}
    return original, files


def history(original, entries, files, resolution_ref, limits):
    require(len(entries) == 2 and [entry["family"] for entry in entries] == ["claude", "gpt"],
            "Two serial family reviews are required")
    require(isinstance(limits, list) and limits
            and all(isinstance(value, str) and value.strip() for value in limits),
            "Explicit current scope limitations are required")
    return {
        "schemaVersion": 1, "batch": BATCH, "base": BASE, "initialSnapshot": CANDIDATE,
        "reviewedSnapshot": REVIEWED, "members": MEMBERS, "publication": "PENDING",
        "reviewMode": MODE, "originalReviewerConfirmation": False,
        "reviewLineage": copy.deepcopy(original["reviewLineage"]) + entries,
        "finalRuns": [entry["run"] for entry in entries],
        "replacementBasis": original["replacementBasis"],
        "nonAcceptedReviews": original["nonAcceptedReviews"],
        "resolution": resolution_ref,
        "recordedFileSha256": {name: sha(raw) for name, raw in sorted(files.items())},
        "packetManifestSha256": PACKET_SHA, "limits": limits,
    }


def main(mode, request_path, output):
    report_path = (HERE / "closure-real-report-001.json" if mode == "real"
                   else output.with_name(output.name + "-report.json"))
    require(mode in ("dry", "real") and not output.exists() and not report_path.exists(),
            "Preserve existing closure attempts")
    require((mode == "dry" and output.parent == HERE)
            or (mode == "real" and output == REPO / CLOSURE), "Unexpected closure destination")
    request_raw = read_review(request_path)
    request = json.loads(request_raw)
    require(set(request) == {"reviews", "resolution", "evidence", "protectedSources", "limits"},
            "Unexpected closure request fields")
    require(isinstance(request["reviews"], list) and len(request["reviews"]) == 2
            and [item["spec"]["family"] for item in request["reviews"]] == ["claude", "gpt"],
            "Both serial fresh reviews are required before assembling a closure")
    guard, _ = start_guard("B134 complete fresh-review closure")
    try:
        git = Git(REPO, RUNNER, guard)

        def clean():
            require(git("rev-parse", "HEAD").decode().strip() == REVIEWED
                    and not git("status", "--porcelain=v1", "--untracked-files=all"),
                    "Closure requires the clean reviewed snapshot")
            require(lineage(git, REVIEWED) > 0, "Missing signed reconciliation lineage")

        clean()
        manifest = git("show", REVIEWED + ":manifest.json")
        progress_raw = git("show", CANDIDATE + ":" + PROGRESS)
        require(git("show", REVIEWED + ":" + PROGRESS) == progress_raw
                and (REPO / PROGRESS).read_bytes() == progress_raw
                and (REPO / "manifest.json").read_bytes() == manifest,
                "Reviewed manifest or original progress changed")
        original, files = load_originals()
        retentions = copy.deepcopy(original["chainRetention"])
        launch_hold, local = retain_launch_hold(files)
        entries, original_claims = [], {}
        for item in request["reviews"]:
            entry, retained, retention = add_replacement(files, item, guard)
            entries.append(entry)
            local.extend(retained)
            retentions[entry["run"]] = retention
        for family in INITIALS:
            _, refs, _, claims = actual_initial(family)
            original_claims[family] = {
                "report": ref_bytes(refs["report"]), "reportSha256": refs["report"]["sha256"],
                "claims": claims,
            }
        core_ref = {"path": str(CORE_ROOT / "fresh-independent-core-001.json"), "sha256": CORE_SHA}
        retentions["fresh-core"] = add_chain(files, "fresh-core", core_ref, guard)
        put(files, ".gitattributes", b"* -text\n")
        put(files, "verification/original-progress.json", progress_raw)
        for label, (relative, digest) in PROOFS.items():
            put(files, "verification/" + label + ".json", read_review(ROOT / relative, digest))
        for ref in request["evidence"]:
            put(files, ref["archivePath"], ref_bytes(ref))
        put(files, "protocol/close_b134.py", Path(__file__).read_bytes())
        put(files, "verification/fresh-local-retention.json", json_bytes({
            "files": local, "policy": "Raw audits, events, admissions, rosters and execution logs remain local.",
        }))
        windows = set()
        sums_raw = read_review(CORE_ROOT / "packet" / "SHA256SUMS.json", PACKET_SHA)
        for name, digest in json.loads(sums_raw).items():
            raw = read_review(CORE_ROOT / "packet" / name, digest)
            if protected_source(name):
                add_protected(windows, raw, name.endswith((".html", ".htm")))
            guard.check()
        for ref in request["protectedSources"]:
            path = Path(ref["path"]).resolve()
            require(path.is_relative_to(WS), "Protected source escaped N1 workspace")
            add_protected(windows, frozen(path, ref["sha256"]), path.suffix in (".html", ".htm"))
        require(windows, "Missing protected-source scan windows")
        put(files, "packet/SHA256SUMS.json", sums_raw)
        resolution_raw = ref_bytes(request["resolution"])
        resolution_ref = put(files, "resolution.json", resolution_raw)
        allowed = {COORDINATOR, AUTHOR, FAILED_SESSION, HELD_SESSION, *METER_SESSIONS,
                   *(entry["session"] for entry in original["reviewLineage"] + entries)}
        adjustments = retain_overlapping_chains(files, windows, allowed, guard, retentions)
        put(files, "verification/chain-retention-adjustments.json", json_bytes(adjustments))
        uuids, leaks = publication_findings(files, windows, allowed, guard)
        checks = {"uuidFindings": len(uuids), "externalWindowFindings": len(leaks)}
        report = {"batch": BATCH, "mode": mode, "files": len(files) + 1,
                  "assemblyRequestSha256": sha(request_raw),
                  "publicationChecks": checks, "uuidFindings": uuids, "externalWindowFindings": leaks}
        freeze_json(report_path, report)
        require(not uuids and not leaks, "Publication retention failed; report preserved")
        closure = history(original, entries, files, resolution_ref, request["limits"])
        closure["nonAcceptedLaunches"] = [launch_hold]
        closure.update(publicationChecks=checks, chainRetention=retentions,
                       assemblyRequestSha256=sha(request_raw))
        resolution = json.loads(resolution_raw)
        validate_resolution(resolution, closure, REVIEWED, original_claims)
        closure_raw = json_bytes(closure)
        progress = closed_progress(json.loads(progress_raw), closure_raw, manifest, resolution, original_claims)
        clean()
        for name, raw in sorted(files.items()):
            write_frozen(output / name, raw)
            guard.check()
        write_frozen(output / "provenance.json", closure_raw)
        if mode == "real":
            path = REPO / PROGRESS
            require(path.read_bytes() == progress_raw, "Progress changed before replacement")
            path.chmod(0o644)
            path.write_bytes(json_bytes(progress))
            path.chmod(0o444)
            require(frozen(path) == json_bytes(progress), "Progress readback failed")
        print(json.dumps({**report, "status": "PASS", "closureSha256": sha(closure_raw),
                          "progressUpdated": mode == "real"}))
    finally:
        require(not guard.finish()["breach"], "Closure RAM breach")


if __name__ == "__main__":
    require(len(sys.argv) == 4, __doc__)
    main(sys.argv[1], Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve())

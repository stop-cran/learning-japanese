"""Close B132 only after both original reviewers accept the signed reconciliation."""
import gzip
import json
import sys
from pathlib import Path

from b132_closure_records import closed_progress, validate_resolution
from b132_closure_records_v2 import collect_initial_record
from b132_confirmation_records import collect_confirmation
from close_b132 import (CORE_SHA, PACKET_SHA, PREFLIGHT, PREFLIGHT_SHA, PREP, PROOFS, LIMITS,
                        add_chain, publication_findings, put, read_review, source_ref)
from close_b131 import add_protected
from common import COORDINATOR, TOOLS, WS, freeze_json, frozen, json_bytes, require, sha, start_guard, write_frozen
from confirm_b132 import INITIALS, OUT as CONFIRM, clean, preflight
from record_b132_publication import validate_reviews
from run_b132_closure_checks import BASE, BATCH, CANDIDATE, CLOSURE, HERE, MEMBERS, PROGRESS, REPO
from verify_b132_packet import RUNNER
from verify_b132_sources import Git
from verify_b132_teaching_revision import REVISION

ROOT = HERE / "review"
REVISION_PROOF = ROOT / "teaching-revision-verification-001" / "verification.json"
REVISION_PROOF_SHA = "899c61fff8616c48a3de52d15ca9b44cb0646b3c02c2935768b37b2a766d02e5"


def keep_confirmation_chain(files, run, manifest_path):
    raw = frozen(manifest_path)
    chain = json.loads(raw)
    prefix = "chains/" + run + "/"
    put(files, prefix + "manifest.json", raw)
    local, archived = [], []
    for row in chain["segments"]:
        data = frozen(row["path"], row["sha256"])
        protected = [part for part in row["parts"] if "/external/" in part["source"]]
        if protected:
            local.append({"index": row["index"], "sha256": row["sha256"], "bytes": len(data),
                          "sources": [{"source": part["source"], "sha256": part["sha256"],
                                       "firstLine": part["a"], "lastLine": part["b"]} for part in protected]})
        else:
            packed = gzip.compress(data, mtime=0)
            require(gzip.decompress(packed) == data, "Chain compression differs")
            put(files, prefix + Path(row["path"]).name + ".gz", packed)
            archived.append(row["index"])
    retention = {
        "originalManifestSha256": sha(raw), "originalSegments": len(chain["segments"]),
        "archivedSegmentIndices": archived, "localOnlySegments": local,
        "policy": "Every segment containing any complete external extract remains local in full, "
                  "including other sources sharing that segment. This is not the complete local read chain.",
    }
    put(files, prefix + "retention.json", json_bytes(retention))
    return retention


def initial_entry(files, family, guard):
    known = INITIALS[family]
    run = "N1-B132-" + family.upper() + "-001"
    spec = {
        "family": family, "role": "initial", "run": run, "session": known["session"],
        "snapshot": CANDIDATE, "verdict": known["verdict"],
        "acceptance": source_ref(PREP / (run + "-acceptance.json"), known["acceptanceSha256"]),
    }
    refs, derivatives, claims = collect_initial_record(
        spec, source_ref(PREFLIGHT, PREFLIGHT_SHA),
        source_ref(PREP / (run + "-final.json"), known["finalSha256"]), read_review)
    prefix = "reviews/" + run + "/"
    entry = {**spec, **claims, "reviewAccepted": True}
    for field in ("report", "final", "acceptance", "adjudication", "auditConfig"):
        ref = refs[field]
        entry[field] = put(files, prefix + field + (".md" if field == "report" else ".json"),
                           read_review(ref["path"], ref["sha256"]))
    for name, raw in derivatives.items():
        entry[name] = put(files, prefix + name + ".json", raw)
    audit = json.loads(read_review(refs["audit"]["path"], refs["audit"]["sha256"]))
    events_path = Path(refs["audit"]["path"]).parent / "events.jsonl"
    raw_events = read_review(events_path, audit["eventsSha256"])
    require(len(raw_events) == audit["eventsBytes"], "Initial event bytes differ")
    local = [source_ref(events_path, audit["eventsSha256"]), refs["audit"]]
    launch_path = PREP / (run + "-launch.json")
    launch_raw = read_review(launch_path)
    launch = json.loads(launch_raw)
    require(launch["candidate"] == CANDIDATE and launch["run"] == run
            and launch["session"] == known["session"], "Original launch differs")
    put(files, prefix + "launch.json", launch_raw)
    admission = json.loads(read_review(launch["admission"]["path"], launch["admission"]["sha256"]))
    require(admission["admitted"] is True and admission["candidate"] == CANDIDATE, "Initial not admitted")
    local.extend([launch["admission"], *admission["snapshots"].values()])
    for ref in local:
        read_review(ref["path"], ref["sha256"])
    for suffix in ("phase1.json", "phase2-message.txt"):
        put(files, prefix + suffix, read_review(PREP / (run + "-" + suffix)))
    config = json.loads(read_review(refs["auditConfig"]["path"], refs["auditConfig"]["sha256"]))
    for field in ("prompt", "kickoff"):
        raw = read_review(config[field])
        put(files, prefix + field + ".txt", raw)
        if field == "kickoff":
            require(sha(raw) == launch["kickoffSha256"], "Original kickoff differs")
    retained = add_chain(files, run, PREP / (run + "-extension.json"),
                         sha(read_review(PREP / (run + "-extension.json"))), guard)
    return entry, local, retained


def confirmation_entry(files, family):
    run = "N1-B132-" + family.upper() + "-CONFIRM-002"
    preflight_path = CONFIRM / (run + "-preflight.json")
    record, config, _ = preflight(preflight_path)
    accepted_path = CONFIRM / (run + "-acceptance.json")
    accepted = json.loads(frozen(accepted_path))
    final = json.loads(frozen(accepted["final"]["path"], accepted["final"]["sha256"]))
    events_path = Path(final["audit"]["path"]).parent / "events.jsonl"
    audit = json.loads(frozen(final["audit"]["path"], final["audit"]["sha256"]))
    spec = {
        "family": family, "role": "confirmation", "run": run, "session": INITIALS[family]["session"],
        "snapshot": REVISION, "confirmation": "CONFIRMED", "acceptance": source_ref(accepted_path),
        "preflight": source_ref(preflight_path),
        "admission": source_ref(CONFIRM / (run + "-admission.json")),
        "events": source_ref(events_path, audit["eventsSha256"]),
    }
    refs, derivatives, _ = collect_confirmation(spec, frozen)
    prefix = "reviews/" + run + "/"
    entry = {key: spec[key] for key in ("family", "role", "run", "session", "snapshot", "confirmation")}
    entry["reviewAccepted"] = True
    for field in ("report", "final", "acceptance", "adjudication", "context", "structure", "preflight"):
        ref = refs[field]
        entry[field] = put(files, prefix + field + (".md" if field == "report" else ".json"),
                           frozen(ref["path"], ref["sha256"]))
    for name, raw in derivatives.items():
        entry[name] = put(files, prefix + name + ".json", raw)
    for key in ("prompt", "kickoff"):
        put(files, prefix + key + ".txt", frozen(config[key]))
    put(files, prefix + "config.json", frozen(record["config"]["path"], record["config"]["sha256"]))
    local = [spec["events"], spec["admission"], refs["audit"]]
    admission = json.loads(frozen(spec["admission"]["path"], spec["admission"]["sha256"]))
    for key in ("prefix", "status", "roster", "request"):
        ref = admission[key]
        frozen(ref["path"], ref["sha256"])
        local.append(ref)
    retained = keep_confirmation_chain(files, run, config["chainManifest"])
    return entry, local, retained


def main(mode, output):
    require(mode in ("dry", "real") and not output.exists()
            and not output.with_name(output.name + "-report.json").exists(), "Preserve closure attempt")
    require((mode == "dry" and output.parent == HERE) or (mode == "real" and output == REPO / CLOSURE),
            "Unexpected closure destination")
    guard, _ = start_guard("B132 reconciled review closure")
    try:
        git = Git(REPO, RUNNER, guard)
        clean(git, REVISION)
        proof_raw = frozen(REVISION_PROOF, REVISION_PROOF_SHA)
        proof = json.loads(proof_raw)
        require(proof["candidate"] == REVISION and proof["status"] == "PASS_SIGNED_RECONCILIATION_BINDINGS_ONLY",
                "Revision proof differs")
        manifest = git("show", REVISION + ":manifest.json")
        require(sha(manifest) == proof["manifestSha256"], "Reviewed manifest differs")
        original = git("show", CANDIDATE + ":" + PROGRESS)
        require((REPO / PROGRESS).read_bytes() == original, "Original progress changed")
        files, local, retention, entries = {}, [], {}, []
        put(files, ".gitattributes", b"* -text\n")
        put(files, "verification/original-progress.json", original)
        for family in INITIALS:
            entry, retained, chain = initial_entry(files, family, guard)
            entries.append(entry)
            local.extend(retained)
            retention[entry["run"]] = chain
        for family in INITIALS:
            entry, retained, chain = confirmation_entry(files, family)
            entries.append(entry)
            local.extend(retained)
            retention[entry["run"]] = chain
        retention["core"] = add_chain(files, "core", PREP / "core-chain-001.json", CORE_SHA, guard)
        put(files, "protocol/preflight.json", frozen(PREFLIGHT, PREFLIGHT_SHA))
        sums_raw = frozen(PREP / "packet" / "SHA256SUMS.json", PACKET_SHA)
        sums = json.loads(sums_raw)
        windows = set()
        from archive_b129_chains import is_local_only_source
        for name, digest in sums.items():
            raw = frozen(PREP / "packet" / name, digest)
            if is_local_only_source(name):
                add_protected(windows, raw, name.endswith((".html", ".htm")))
            guard.check()
        put(files, "packet/SHA256SUMS.json", sums_raw)
        for path in (WS / "scratch-132" / "source-reconciliation-001" / "external").iterdir():
            if path.suffix in (".html", ".txt"):
                add_protected(windows, frozen(path), path.suffix == ".html")
                guard.check()
        for suffix in ("html", "txt"):
            add_protected(windows, frozen(WS / "scratch-132" / "survey-001" / "external" /
                                         ("墓-kotobank." + suffix)), suffix == "html")
        revision_ref = put(files, "verification/signed-reconciliation.json", proof_raw)
        for name, digest in PROOFS.items():
            put(files, "verification/" + name, read_review(ROOT / name, digest))
        source_ref_record = put(files, "verification/reconciliation-sources.json",
                                frozen(ROOT / "source-reconciliation-verification-001.json",
                                       "4f64783f8810d41b778a7ccb2048ca1fc54bcff7c3ed009b20541ddd23b9bc77"))
        for name in ("source-reconciliation-freeze-001.json", "source-reconciliation-adjudication-001.json"):
            put(files, "verification/" + name, frozen(ROOT / name))
        for name in ("close_b132_reconciled.py", "b132_confirmation_records.py", "confirm_b132.py",
                     "b132_closure_records.py", "b132_closure_records_v2.py", "run_b132_closure_checks.py",
                     "record_b132_publication.py", "verify_b132_teaching_revision.py"):
            put(files, "protocol/tools/" + name, frozen(TOOLS / name))
        for name in ("audit-confirm.py", "check-confirm-structure.py", "renderer.py"):
            put(files, "protocol/confirmation/" + name, frozen(CONFIRM / name))
        put(files, "verification/local-retention.json", json_bytes({
            "files": local, "policy": "Raw audits, event histories, full rosters and external captures remain "
                                     "local. Original failed preparations and unlaunched001 chains are preserved "
                                     "locally, not successful reviews or additional review attempts.",
        }))
        finals = entries[2:]
        resolution = {
            "batch": BATCH, "initialSnapshot": CANDIDATE, "reviewedSnapshot": REVISION,
            "remainingActionableFindings": [], "remainingConsequentialClaims": [],
            "adjudicationSha256": {entry["run"]: entry["adjudication"]["sha256"] for entry in entries},
            "dispositions": [
                {"run": "N1-B132-GPT-001", "id": claim, "status": "fixed",
                 "reason": "Complete independent sources and the narrow qualified direct precaution were "
                           "checked on the owner-signed revision and accepted by both original reviewers. "
                           "The initial UNVERIFIED evidence gap is preserved, not reclassified as a defect.",
                 "evidence": [revision_ref, source_ref_record, *(entry["adjudication"] for entry in finals)]}
                for claim in ("Q1", "Q2")
            ],
        }
        resolution_ref = put(files, "resolution.json", json_bytes(resolution))
        allowed = {COORDINATOR, "271cf1ff-b4ef-4145-9ea8-ab3674276ac5",
                   "42fe7f24-889c-4a9f-bfc9-8e2a2a1b5ecd", *(entry["session"] for entry in entries)}
        uuids, leaks = publication_findings(files, windows, allowed, guard)
        checks = {"uuidFindings": len(uuids), "externalWindowFindings": len(leaks)}
        report = {"batch": BATCH, "mode": mode, "files": len(files) + 1,
                  "bytes": sum(map(len, files.values())), "publicationChecks": checks,
                  "uuidFindings": uuids, "externalWindowFindings": leaks}
        freeze_json(output.with_name(output.name + "-report.json"), report)
        require(not uuids and not leaks, "Publication retention failed; inspect preserved report")
        limits = [LIMITS[0].replace("Two independent same-snapshot initial textual reviews",
                                   "Two independent same-snapshot initials plus both original-reviewer delta confirmations"),
                  *LIMITS[1:]]
        limits.append("Initial CLEAN and UNVERIFIED reports remain unchanged. Two source-backed direct guards "
                      "resolve the original Q1/Q2 evidence gaps only in the signed revised snapshot. The full "
                      "external extracts were supplied locally and are not redistributed. The source packet's "
                      "initially writable64 files were verified and later frozen; no retroactive immutability.")
        closure = {
            "schemaVersion": 1, "batch": BATCH, "base": BASE, "initialSnapshot": CANDIDATE,
            "reviewedSnapshot": REVISION, "members": MEMBERS, "publication": "PENDING",
            "reviewLineage": entries, "finalRuns": [entry["run"] for entry in finals],
            "resolution": resolution_ref, "recordedFileSha256": {name: sha(raw) for name, raw in sorted(files.items())},
            "publicationChecks": checks, "chainRetention": retention,
            "packetManifestSha256": PACKET_SHA, "limits": limits,
        }
        validate_reviews(closure, REVISION)
        validate_resolution(resolution, entries, REVISION, closure["recordedFileSha256"])
        closure_raw = json_bytes(closure)
        progress = closed_progress(json.loads(original), closure_raw, manifest, resolution)
        clean(git, REVISION)
        for name, raw in sorted(files.items()):
            write_frozen(output / name, raw)
            guard.check()
        write_frozen(output / "provenance.json", closure_raw)
        if mode == "real":
            path = REPO / PROGRESS
            require(path.read_bytes() == original, "Progress changed before replacement")
            path.chmod(0o644)
            path.write_bytes(json_bytes(progress))
            path.chmod(0o444)
            require(frozen(path) == json_bytes(progress), "Progress readback failed")
        print(json.dumps({**report, "status": "PASS", "closureSha256": sha(closure_raw),
                          "progressUpdated": mode == "real"}))
    finally:
        require(not guard.finish()["breach"], "Closure RAM breach")


if __name__ == "__main__":
    main(sys.argv[1], Path(sys.argv[2]).resolve())

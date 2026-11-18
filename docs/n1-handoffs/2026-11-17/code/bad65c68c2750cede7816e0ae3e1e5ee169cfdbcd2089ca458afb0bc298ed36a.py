"""Close unchanged B132 teaching only after two accepted, claim-adjudicated CLEAN reviews.

Usage: close_b132.py dry|real OUT RESOLUTION
This initial-review builder deliberately rejects a changed snapshot or unresolved claims.
"""
import gzip
import json
import re
import sys
from pathlib import Path

from archive_b129_chains import is_local_only_source, prepare
from b132_closure_records import archive_path, closed_progress, validate_resolution
from b132_closure_records_v2 import collect_initial_record
from close_b131 import WINDOW, add_protected, normalize, texts
from common import COORDINATOR, TOOLS, freeze_json, frozen, json_bytes, require, sha, start_guard, write_frozen
from record_b132_publication import validate_reviews
from run_b132_closure_checks import BASE, BATCH, CANDIDATE, CLOSURE, HERE, MEMBERS, PROGRESS, REPO
from verify_b132_packet import RUNNER
from verify_b132_sources import FINGERPRINT, OWNER, TRAILER, Git

REVIEW = HERE / "review"
PREP = REVIEW / "neutral-preparation-002"
PREFLIGHT = PREP / "audit-configs-001" / "preflight.json"
PREFLIGHT_SHA = "c790a53590a8b6691c87a9d1290b5d0c914eb99c24e49eca2c1f394f9016e18f"
PACKET_SHA = "b563c909467add3541b3f849cbcc93fdfc155157cf77f13a26662b688967a973"
CORE_SHA = "2fb4092299b47a7a2808965c6e4f58dba716367b4ac403123285bb5f8aaf9bcd"
UUID = re.compile(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}")
PROOFS = {
    "source-verification-001.json": "da96caae19030d3facd5d8c91ef196d857ddfff4d723ebd6e4b514acfbbac078",
    "payload-verification-001.json": "d4a77b1abdd90b547fddb5efbe449641b218846fd3e6f7bfe3a136003d96e482",
    "gate-verification-001/verification.json": "d51652ee878d4462ea7fa418ec903e7a2db709bcacb1b9d95ede80fdb0c11ecc",
    "packet-verification-001/verification.json": "558e1eeacdc0a69aa9ec69924698c20b74c3e37e3df65f63e7cf40c7b4f0640a",
}
LIMITS = [
    "Two independent same-snapshot initial textual reviews, not exhaustive linguistic certification.",
    "The source packet and every original review input remain immutable locally. Complete external "
    "extracts, raw HTML, raw execution events, raw audits and private session rosters are not redistributed.",
    "Chain segments containing any complete external extract remain local in full; retention indices "
    "and original hashes are published. This archive is not the full local review environment.",
    "The reading audit covers finite N1/All/Starter and single-borrow pools only. Three latent "
    "smaller-pool collisions and the positive Starter-plus-束 case remain disclosed; arbitrary, "
    "custom and multiple-borrow pools, Kotlin/native/device behavior are not established.",
    "Finite font cmap coverage and stroke metadata are not rendered, native or phone acceptance. "
    "Missing historical glyph images were not reconstructed.",
    "The author survey's earlier noncompliant child waits remain disclosed in original progress.",
    "No delivery or whole-set credit until owner-signed publication, matching CI and exact served ZIP "
    "verification; delivered remains 267/1228 and remaining remains 961.",
]


def put(files, name, raw):
    archive_path(name)
    require(not name.endswith((".jsonl", ".html", ".htm")), "Raw events/HTML must remain local")
    require(name not in files or files[name] == raw, "Conflicting archive bytes: " + name)
    files[name] = raw
    return {"path": name, "sha256": sha(raw)}


def read_review(path, digest=None):
    path = Path(path).resolve()
    require(path.is_relative_to(REVIEW), "Review input escaped its root")
    return frozen(path, digest)


def source_ref(path, digest=None):
    raw = read_review(path, digest)
    return {"path": str(path), "sha256": sha(raw), "bytes": len(raw)}


def add_chain(files, label, path, digest, guard):
    raw = read_review(path, digest)
    manifest = json.loads(raw)
    segments = {}
    for row in manifest["segments"]:
        guard.check()
        segment_path = Path(row["path"]).resolve()
        require(segment_path.is_relative_to(PREP / "chains"), "Chain segment escaped the frozen chains")
        segments[row["path"]] = frozen(segment_path, row["sha256"])
    archived, retention = prepare(raw, segments)
    for name, value in archived.items():
        put(files, f"chains/{label}/{name}", value)
    return retention


def add_review(files, family, preflight_ref, guard):
    run = "N1-B132-" + family.upper() + "-001"
    acceptance_ref = source_ref(PREP / (run + "-acceptance.json"))
    final_ref = source_ref(PREP / (run + "-final.json"))
    final = json.loads(read_review(final_ref["path"], final_ref["sha256"]))
    spec = {
        "family": family, "run": run, "role": "initial", "session": final["session"],
        "snapshot": CANDIDATE, "verdict": "CLEAN", "acceptance": acceptance_ref,
    }
    refs, derivatives, claims = collect_initial_record(spec, preflight_ref, final_ref, read_review)
    require(not any(claims.values()), "Initial-only closure requires no outstanding consequential claims")
    prefix = f"reviews/{run}/"
    entry = {**spec, **claims, "reviewAccepted": True}
    for field in ("report", "final", "acceptance", "adjudication", "auditConfig"):
        ref = refs[field]
        suffix = ".md" if field == "report" else ".json"
        entry[field] = put(files, prefix + field + suffix, read_review(ref["path"], ref["sha256"]))
    for name, raw in derivatives.items():
        entry[name] = put(files, prefix + name + ".json", raw)
    audit = json.loads(read_review(refs["audit"]["path"], refs["audit"]["sha256"]))
    events_path = Path(refs["audit"]["path"]).parent / "events.jsonl"
    events = read_review(events_path, audit["eventsSha256"])
    require(len(events) == audit["eventsBytes"]
            and len(events.splitlines()) == audit["eventsCount"], "Frozen event snapshot differs")
    local = [source_ref(events_path, audit["eventsSha256"]), refs["audit"]]
    launch_path = PREP / (run + "-launch.json")
    launch_raw = read_review(launch_path)
    launch = json.loads(launch_raw)
    config = json.loads(read_review(refs["auditConfig"]["path"], refs["auditConfig"]["sha256"]))
    require(launch["candidate"] == CANDIDATE and launch["run"] == run
            and launch["session"] == spec["session"]
            and launch["start"]["selectedModel"] == config["contextProfile"]["selectedModel"]
            and launch["start"]["contextTier"] == "long_context", "Launch identity differs")
    entry["launch"] = put(files, prefix + "launch.json", launch_raw)
    admission_ref = launch["admission"]
    admission = json.loads(read_review(admission_ref["path"], admission_ref["sha256"]))
    require(admission["admitted"] is True and admission["candidate"] == CANDIDATE
            and admission["run"] == run, "Launch admission differs")
    local.append(admission_ref)
    for ref in admission["snapshots"].values():
        read_review(ref["path"], ref["sha256"])
        local.append(ref)
    phase_path = PREP / (run + "-phase1.json")
    phase_raw = read_review(phase_path)
    phase = json.loads(phase_raw)
    require(phase["readyForPhase2"] is True and phase["session"] == spec["session"], "Phase one differs")
    put(files, prefix + "phase1.json", phase_raw)
    extension_path = PREP / (run + "-extension.json")
    retention = add_chain(files, run, extension_path, sha(read_review(extension_path)), guard)
    message = read_review(PREP / (run + "-phase2-message.txt"))
    put(files, prefix + "phase2-message.txt", message)
    phase_list = Path(phase["auditDir"]) / "phase1-list.txt"
    put(files, prefix + "phase1-list.txt", read_review(phase_list))
    for key in ("auditReceipt", "structureReceipt"):
        root = Path(final[key])
        receipt_raw = read_review(root / "receipt.json")
        receipt = json.loads(receipt_raw)
        require(receipt["exitCode"] == 0 and not receipt["memory"]["breach"], "Final child gate failed")
        read_review(root / "output.log", receipt["logSha256"])
        local.extend([source_ref(root / "receipt.json"), source_ref(root / "output.log")])
    for key in ("prompt", "kickoff"):
        raw = read_review(config[key])
        put(files, prefix + key + ".txt", raw)
        if key == "kickoff":
            require(sha(raw) == launch["kickoffSha256"], "Kickoff bytes differ from launch")
    entry["originalAuditSha256"] = refs["audit"]["sha256"]
    entry["actualResponseModels"] = audit["actualResponseModels"]
    return entry, local, retention


def publication_findings(files, windows, allowed_uuids, guard):
    uuids, leaks = [], []
    for name, raw in sorted(files.items()):
        guard.check()
        for text in texts(name, raw):
            unknown = {value.lower() for value in UUID.findall(text)} - allowed_uuids
            uuids.extend({"file": name, "uuid": value} for value in sorted(unknown))
            value = normalize(text)
            hits = sum(value[i:i + WINDOW] in windows for i in range(max(0, len(value) - WINDOW + 1)))
            if hits:
                leaks.append({"file": name, "windows": hits})
    return uuids, leaks


def main(mode, out, resolution_path):
    require(mode in ("dry", "real"), "Use dry or real")
    require(not out.exists() and not out.with_name(out.name + "-report.json").exists(), "Preserve prior attempt")
    require((mode == "dry" and out.parent == HERE)
            or (mode == "real" and out == REPO / CLOSURE), "Unexpected closure output")
    resolution_raw = frozen(resolution_path)
    resolution = json.loads(resolution_raw)
    guard, _ = start_guard("B132 unchanged-candidate closure")
    try:
        git = Git(REPO, RUNNER, guard)
        require(git("rev-parse", "HEAD").decode().strip() == CANDIDATE
                and not git("status", "--porcelain=v1", "--untracked-files=all"),
                "Initial-only closure needs the clean unchanged candidate")
        require(git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", CANDIDATE).decode().strip()
                == f"{BASE}|G|{FINGERPRINT}|{OWNER}|{OWNER}"
                and TRAILER in git("show", "-s", "--format=%B", CANDIDATE), "Candidate signature differs")
        manifest = git("show", f"{CANDIDATE}:manifest.json")
        original_raw = git("show", f"{CANDIDATE}:{PROGRESS}")
        require((REPO / "manifest.json").read_bytes() == manifest
                and (REPO / PROGRESS).read_bytes() == original_raw, "Working manifest/progress differ")
        files = {}
        put(files, ".gitattributes", b"* -text\n")
        put(files, "verification/original-progress.json", original_raw)
        preflight_raw = frozen(PREFLIGHT, PREFLIGHT_SHA)
        put(files, "protocol/preflight.json", preflight_raw)
        preflight_ref = {"path": str(PREFLIGHT), "sha256": PREFLIGHT_SHA}
        lineage, local, retentions = [], [], {}
        for family in ("claude", "gpt"):
            entry, retained, retention = add_review(files, family, preflight_ref, guard)
            lineage.append(entry)
            local.extend(retained)
            retentions[entry["run"]] = retention
        retentions["core"] = add_chain(files, "core", PREP / "core-chain-001.json", CORE_SHA, guard)
        packet = PREP / "packet"
        sums_raw = frozen(packet / "SHA256SUMS.json", PACKET_SHA)
        sums = json.loads(sums_raw)
        windows = set()
        for name, digest in sums.items():
            archive_path(name)
            guard.check()
            raw = frozen(packet / name, digest)
            if is_local_only_source(name):
                add_protected(windows, raw, name.endswith((".html", ".htm")))
        require(sorted(p.relative_to(packet).as_posix() for p in packet.rglob("*") if p.is_file())
                == sorted([*sums, "SHA256SUMS.json"]), "Packet inventory differs")
        put(files, "packet/SHA256SUMS.json", sums_raw)
        put(files, "packet/packet.json", frozen(packet / "packet.json", sums["packet.json"]))
        for name, digest in PROOFS.items():
            raw = read_review(REVIEW / name, digest)
            proof = json.loads(raw)
            require(proof["candidate"] == CANDIDATE and proof["base"] == BASE
                    and proof["status"] == "PASS", "Candidate proof differs")
            put(files, "verification/" + name, raw)
        for name in ("close_b132.py", "b132_closure_records.py", "b132_closure_records_v2.py",
                     "run_b132_closure_checks.py", "record_b132_publication.py",
                     "archive_b129_chains.py", "common.py"):
            put(files, "protocol/tools/" + name, frozen(TOOLS / name))
        put(files, "verification/local-retention.json", json_bytes({
            "files": local, "policy": "Exact originals retained locally; never evidence of new review.",
            "historicalPreparation": "Failed coordinator preparations and all original source captures "
            "remain local unchanged, outside the accepted-review lineage.",
        }))
        resolution_ref = put(files, "resolution.json", resolution_raw)
        allowed = {COORDINATOR, "271cf1ff-b4ef-4145-9ea8-ab3674276ac5",
                   "42fe7f24-889c-4a9f-bfc9-8e2a2a1b5ecd", *(entry["session"] for entry in lineage)}
        uuids, leaks = publication_findings(files, windows, allowed, guard)
        checks = {"uuidFindings": len(uuids), "externalWindowFindings": len(leaks)}
        report = {"batch": BATCH, "mode": mode, "files": len(files) + 1,
                  "bytes": sum(len(raw) for raw in files.values()), "publicationChecks": checks,
                  "uuidFindings": uuids, "externalWindowFindings": leaks}
        freeze_json(out.with_name(out.name + "-report.json"), report)
        require(not uuids and not leaks, "Publication retention check failed; inspect preserved report")
        inventory = {name: sha(raw) for name, raw in sorted(files.items())}
        closure = {
            "schemaVersion": 1, "batch": BATCH, "base": BASE, "initialSnapshot": CANDIDATE,
            "reviewedSnapshot": CANDIDATE, "members": MEMBERS, "publication": "PENDING",
            "reviewLineage": lineage, "finalRuns": [entry["run"] for entry in lineage],
            "resolution": resolution_ref, "recordedFileSha256": inventory, "publicationChecks": checks,
            "chainRetention": retentions, "packetManifestSha256": PACKET_SHA, "limits": LIMITS,
        }
        validate_reviews(closure, CANDIDATE)
        validate_resolution(resolution, lineage, CANDIDATE, inventory)
        closure_raw = json_bytes(closure)
        progress = closed_progress(json.loads(original_raw), closure_raw, manifest, resolution)
        require(git("rev-parse", "HEAD").decode().strip() == CANDIDATE
                and not git("status", "--porcelain=v1", "--untracked-files=all"), "Candidate changed")
        for name, raw in sorted(files.items()):
            guard.check()
            write_frozen(out / name, raw)
        write_frozen(out / "provenance.json", closure_raw)
        if mode == "real":
            progress_path = REPO / PROGRESS
            require(progress_path.read_bytes() == original_raw, "Progress changed before replacement")
            progress_path.chmod(0o644)
            progress_path.write_bytes(json_bytes(progress))
            progress_path.chmod(0o444)
            require(frozen(progress_path) == json_bytes(progress), "Progress readback failed")
        print(json.dumps({**report, "status": "PASS", "closureSha256": sha(closure_raw),
                          "progressUpdated": mode == "real"}))
    finally:
        require(not guard.finish()["breach"], "Closure RAM breach")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)
    main(sys.argv[1], Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve())

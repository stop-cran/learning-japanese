"""Close B133 only after both original reviewers accept the owner-signed reconciliation.

Usage: close_b133.py dry|real OUT
Dry output must be a new direct child of scratch-133; real output is the repository closure.
"""
import gzip
import json
import sys
from pathlib import Path

from accept_b133_confirmation import initial_binding
from admit_b133_source_reconciliation import AUTHOR, INITIALS, P as PREP, PREFLIGHT as PREFLIGHT_REF
from archive_b129_chains import is_local_only_source, prepare
from b132_closure_records import archive_path
from b133_closure_records_v2 import closed_progress, collect_initial_record, validate_resolution
from b133_confirmation_records import collect_confirmation
from b133_fresh_confirmation_records_v2 import collect_confirmation as collect_fresh_confirmation
from b133_closure_history import unaccepted_entry
from close_b131 import add_protected
from close_b132 import publication_findings
from common import COORDINATOR, TOOLS, WS, freeze_json, frozen, json_bytes, require, sha, start_guard, write_frozen
from confirm_b133_v2 import OUT as CONFIRM, clean, preflight
from record_b133_publication_v2 import validate_reviews
from run_b133_closure_checks import BASE, BATCH, CANDIDATE, CLOSURE, HERE, MEMBERS, PROGRESS, REPO
from verify_b133_packet import RUNNER
from verify_b133_sources import Git

REVIEW = HERE / "review"
REVISION = "b1acf155fb8c7e1066a5c3baf88ae98ab92c29ac"
PREFLIGHT, PREFLIGHT_SHA = Path(PREFLIGHT_REF["path"]), PREFLIGHT_REF["sha256"]
PACKET_SHA = "dee789f5d8d6f547c9bd8616a5f9b28bd584028703ac05b9ddec63d9fe6f82e4"
CORE_SHA = "f54ea59e3c10ba539ab110df523740bf9c58da108a7f5e4e990688ed98554146"
REVISION_PROOF = REVIEW / "teaching-revision-verification-004" / "verification.json"
REVISION_PROOF_SHA = "8a88b67f4e609885fd14b739442ae72ecad9476d2f19040c535c9f468ab6a90e"
SOURCE_PROOF = REVIEW / "source-reconciliation-verification-001.json"
SOURCE_PROOF_SHA = "d6c01b0501e4c3d23c8ab250a5cd674a32270058e5f7a3252b39bf5d185443fb"
ADJUDICATION = REVIEW / "coordinator-adjudication-001.json"
ADJUDICATION_SHA = "cc04c27c12c3fd9fcced0075acfb817f8f0427049c1cfdcc18db146ac1d4f549"
PROOFS = {
    "source-verification-001.json": "5d8c9aee7a31a35e5eeae047d35ff3a79aedb4ecc81cb7f72358d9515974cd12",
    "payload-verification-001.json": "692ecc9d3af90157b97733ff29c2b11ebe4d271893308a2c6eb2cf4e9b61c2cb",
    "gate-verification-001/verification.json": "65e292b34893b15862d70f37a9dfdb94bc22972bbc70044bc6431716349181fb",
    "packet-verification-001/verification.json": "9ecbdbb9d2c0f90c1de9c1a4088a78655bb531f715e74ae07002ad797dcf9ebd",
}
SOURCE_ROOT = HERE / "source-reconciliation-001"
PROTECTED_DIRS = (
    (REVIEW / "confirmation-sources-002" / "external", (".txt", ".html")),
    (SOURCE_ROOT / "captures", (".txt", ".html")),
    (SOURCE_ROOT / "reused-captures", (".txt", ".html")),
    (SOURCE_ROOT / "readback", (".txt",)),
    (HERE / "teaching-reconciliation-002" / "source-sections", (".txt",)),
    (HERE / "teaching-reconciliation-003" / "source-sections", (".txt",)),
    (REVIEW / "claude-confirm-002-adjudication-sources-001", (".txt", ".html")),
)
TOOL_NAMES = (
    "close_b133.py", "close_b133_v2.py", "test_b133_closure_v2.py",
    "b133_closure_records.py", "b133_closure_records_v2.py", "b133_confirmation_records.py",
    "b133_closure_history.py", "b133_closure_origins.py", "record_b133_publication_v2.py",
    "b133_fresh_confirmation_records_v2.py", "b133_fresh_confirmation_v2.py",
    "confirm_b133_fresh_v2.py", "accept_b133_fresh_confirmation_v2.py",
    "confirm_b133.py", "confirm_b133_v2.py", "accept_b133_confirmation.py",
    "admit_b133_source_reconciliation.py", "run_b133_closure_checks.py", "record_b133_publication.py",
    "verify_b133_teaching_revision_v2.py", "verify_b133_teaching_revision_v3.py",
    "verify_b133_teaching_revision_v4.py", "archive_b129_chains.py", "common.py",
)
CONFIRMATION_TOOLS = ("audit-confirm.py", "check-confirm-structure.py", "renderer.py")
LIMITS = [
    "Two independent same-snapshot initial textual reviews, original GPT final confirmation and "
    "disclosed same-family fresh-context Claude final confirmation. Original Claude context "
    "could not fit the unchanged gate; its initial and first confirmation remain historical. "
    "This is not equal fresh-read depth or exhaustive linguistic certification.",
    "The source packet and every original review input remain immutable locally. Complete external "
    "extracts, raw HTML, raw execution events, raw audits and private session rosters are not redistributed.",
    "Chain segments containing any complete external extract remain local in full; retention indices "
    "and original hashes are published. This archive is not the full local review environment.",
    "The reading audit covers finite N1/All/Starter and single-borrow pools only: 0 production and "
    "0 padded-session hits. One latent smaller-pool 滝/湿 collision for うるおす remains disclosed and "
    "not drawable in the checked pools; arbitrary, custom and multiple-borrow pools, Kotlin/native/device "
    "behavior are not established.",
    "Finite font cmap coverage (all three target glyphs present; eight component/variant/supplemental "
    "code points absent from each bundled font) and stroke metadata are not rendered, native or phone "
    "acceptance. Missing historical glyph images were not reconstructed.",
    "琴 ことのを keeps an explicitly unresolved historical scope and is not taught as cord; the regional "
    "タキ cliff sense is not taught as unrestricted 滝. The 鉛-具 pigment/white-lead cross-pair remains a "
    "separately disclosed retained distinction, outside the nineteen direct pair decisions.",
    "All initial and intermediate reports remain unchanged, including both UNVERIFIED confirmations. "
    "Thirteen qualified direct precautions, six retained distinctions and the corrected historical "
    "sake-name abbreviation apply only to the final signed snapshot. Earlier waterfall-water "
    "interpretations in GPT CONFIRM-002 and coordinator adjudications are withdrawn, not erased.",
    "Five JMdict identities cited only by the reconciliation (1396980, 1404975, 1380440, 1244950, "
    "1343610) are in the committed complete reconciliation families, not the original review packet.",
    "No delivery or whole-set credit until owner-signed publication, matching CI and exact served ZIP "
    "verification; delivered remains 268/1228 and remaining remains 960.",
]
RESOLUTION = (
    ("claude", "C1", "fixed", "鉛-鉱: qualified direct precaution added for the ore/unrefined-metal label."),
    ("claude", "C2", "source-backed-no-change",
     "鉛-鉄: retained distinction between two specific metal labels; confirmed by the final original GPT and disclosed fresh Claude reviewers."),
    ("claude", "C3", "fixed", "滝-速: qualified direct precaution added for fast river flow (shared with GPT Q3)."),
    ("gpt", "Q1", "source-backed-no-change",
     "鉛-似: retained noun-versus-action distinction; complete sources establish no bare counterfeit-money "
     "sense for 似. The initial UNVERIFIED evidence gap is preserved, not reclassified as a defect."),
    ("gpt", "Q2", "fixed", "琴-具: qualified direct precaution added for the broad implement label."),
    ("gpt", "Q3", "fixed", "滝-速: qualified direct precaution added for fast river flow (shared with Claude C3)."),
    ("gpt", "Q4", "fixed", "滝-岩: qualified direct precaution added for the regional タキ cliff sense, "
                           "which is not taught as unrestricted 滝."),
    ("gpt", "C4", "fixed", "琴 instrument/string family: 糸 and 緒 precautions added; 機, 線 and 索 retained "
                           "as source-backed distinctions."),
    ("gpt", "C5", "fixed", "鉛 dull/money family: 遅 and 円 precautions added; 倣 retained as a "
                           "source-backed action distinction."),
    ("gpt", "C6", "fixed", "滝 sound/terrain/water family: 声, 激, 険 and 液 precautions added. The liquid "
                           "precaution has direct flow/drink grounds, not a third-card argument; "
                           "the erroneous historical abbreviation gloss was corrected."),
)


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
    binding = initial_binding(family)
    spec = binding["spec"]
    run = spec["run"]
    refs, derivatives, claims = collect_initial_record(spec, binding["preflight"], binding["final"], read_review)
    require(claims == known["claims"], "Initial consequential claims differ")
    final = json.loads(read_review(refs["final"]["path"], refs["final"]["sha256"]))
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
    admission = json.loads(read_review(launch["admission"]["path"], launch["admission"]["sha256"]))
    require(admission["admitted"] is True and admission["candidate"] == CANDIDATE
            and admission["run"] == run, "Launch admission differs")
    local.append(launch["admission"])
    for ref in admission["snapshots"].values():
        read_review(ref["path"], ref["sha256"])
        local.append(ref)
    phase_raw = read_review(PREP / (run + "-phase1.json"))
    phase = json.loads(phase_raw)
    require(phase["readyForPhase2"] is True and phase["session"] == spec["session"]
            and phase["run"] == run, "Phase one differs")
    put(files, prefix + "phase1.json", phase_raw)
    put(files, prefix + "phase1-list.txt", read_review(Path(phase["auditDir"]) / "phase1-list.txt"))
    for name in ("phase2-message.txt", "extension-preflight.json"):
        put(files, prefix + name, read_review(PREP / (run + "-" + name)))
    receipts = [Path(final["auditReceipt"]), Path(final["structureReceipt"]),
                Path(phase["auditReceipt"]), Path(phase["extensionReceipt"])]
    for root in receipts:
        receipt_raw = read_review(root / "receipt.json")
        receipt = json.loads(receipt_raw)
        require(receipt["exitCode"] == 0 and not receipt["memory"]["breach"], "Lifecycle child gate failed")
        read_review(root / "output.log", receipt["logSha256"])
        local.extend([source_ref(root / "receipt.json"), source_ref(root / "output.log")])
    for key in ("prompt", "kickoff"):
        raw = read_review(config[key])
        put(files, prefix + key + ".txt", raw)
        if key == "kickoff":
            require(sha(raw) == launch["kickoffSha256"], "Kickoff bytes differ from launch")
    entry["originalAuditSha256"] = refs["audit"]["sha256"]
    entry["actualResponseModels"] = audit["actualResponseModels"]
    extension_path = PREP / (run + "-extension.json")
    retention = add_chain(files, run, extension_path, sha(read_review(extension_path)), guard)
    return entry, local, retention


def confirmation_entry(files, family, run=None, candidate=REVISION):
    run = run or "N1-B133-" + family.upper() + "-CONFIRM-003"
    preflight_path = CONFIRM / (run + "-preflight.json")
    record, config, _ = preflight(preflight_path)
    require(record["candidate"] == candidate and record["teachingChange"] is True, "Confirmation snapshot differs")
    accepted_path = CONFIRM / (run + "-acceptance.json")
    accepted = json.loads(frozen(accepted_path))
    final = json.loads(frozen(accepted["final"]["path"], accepted["final"]["sha256"]))
    events_path = Path(final["audit"]["path"]).parent / "events.jsonl"
    audit = json.loads(frozen(final["audit"]["path"], final["audit"]["sha256"]))
    spec = {
        "family": family, "role": "confirmation", "run": run, "session": record["session"],
        "snapshot": candidate, "confirmation": "CONFIRMED",
        "acceptance": {"path": str(accepted_path), "sha256": sha(frozen(accepted_path))},
        "preflight": {"path": str(preflight_path), "sha256": sha(frozen(preflight_path))},
        "admission": {"path": str(CONFIRM / (run + "-admission.json")),
                      "sha256": sha(frozen(CONFIRM / (run + "-admission.json")))},
        "events": {"path": str(events_path), "sha256": audit["eventsSha256"]},
    }
    if "originalSession" in record:
        spec.update(reviewerOrigin="fresh-context-replacement", originalSession=record["originalSession"])
        refs, derivatives, _ = collect_fresh_confirmation(spec, initial_binding(family), frozen)
    else:
        refs, derivatives, _ = collect_confirmation(spec, initial_binding(family), frozen)
    prefix = "reviews/" + run + "/"
    entry = {key: spec[key] for key in ("family", "role", "run", "session", "snapshot", "confirmation")}
    entry["reviewAccepted"] = True

    if "originalSession" in record:
        entry.update(
            reviewerOrigin="fresh-context-replacement", originalSession=record["originalSession"],
            replacementReason=record["replacementReason"],
        )
        ref = record["contextObservation"]
        entry["contextObservation"] = put(
            files, prefix + "origin-observation.json", frozen(ref["path"], ref["sha256"]))
        prior_prefix = "reviews/N1-B133-CLAUDE-CONFIRM-002/"
        entry["priorFinal"] = {"path": prior_prefix + "final.json",
                               "sha256": sha(files[prior_prefix + "final.json"])}
        name = prior_prefix + "adjudication-summary.json"
        entry["priorAdjudication"] = {
            "path": name, "sha256": sha(files[name]),
            "originalSha256": json.loads(files[name])["originalAdjudicationSha256"],
        }
    for field in ("report", "final", "acceptance", "adjudication", "context", "structure", "preflight"):
        ref = refs[field]
        entry[field] = put(files, prefix + field + (".md" if field == "report" else ".json"),
                           frozen(ref["path"], ref["sha256"]))
    for name, raw in derivatives.items():
        entry[name] = put(files, prefix + name + ".json", raw)
    for key in ("prompt", "kickoff"):
        put(files, prefix + key + ".txt", frozen(config[key]))
    put(files, prefix + "config.json", frozen(record["config"]["path"], record["config"]["sha256"]))
    local = [spec["events"], spec["admission"], refs["audit"],
             {"path": str(CONFIRM / (run + "-spec.json")), "sha256": sha(frozen(CONFIRM / (run + "-spec.json")))}]
    admission = json.loads(frozen(spec["admission"]["path"], spec["admission"]["sha256"]))
    for key in ("prefix", "status", "roster", "request"):
        ref = admission[key]
        frozen(ref["path"], ref["sha256"])
        local.append(ref)
    retained = keep_confirmation_chain(files, run, config["chainManifest"])
    return entry, local, retained


def protected_windows(guard):
    windows = set()
    sums_raw = frozen(PREP / "packet" / "SHA256SUMS.json", PACKET_SHA)
    sums = json.loads(sums_raw)
    for name, digest in sums.items():
        raw = frozen(PREP / "packet" / name, digest)
        if is_local_only_source(name):
            add_protected(windows, raw, name.endswith((".html", ".htm")))
        guard.check()
    counts = {}
    for directory, suffixes in PROTECTED_DIRS:
        paths = sorted(path for path in directory.iterdir() if path.suffix in suffixes)
        require(paths, "Missing protected extracts: " + str(directory))
        for path in paths:
            add_protected(windows, frozen(path), path.suffix == ".html")
            guard.check()
        counts[directory.relative_to(HERE).as_posix()] = len(paths)
    return windows, sums_raw, counts


def resolution_record(entries, evidence):
    adjudications = {entry["family"]: entry["adjudication"] for entry in entries if entry["role"] == "confirmation"}
    return {
        "batch": BATCH, "initialSnapshot": CANDIDATE, "reviewedSnapshot": REVISION,
        "remainingActionableFindings": [], "remainingConsequentialClaims": [],
        "adjudicationSha256": {entry["run"]: entry["adjudication"]["sha256"] for entry in entries},
        "dispositions": [
            {"run": "N1-B133-" + family.upper() + "-001", "id": claim, "status": status,
             "reason": reason + " Checked against complete independent sources on the owner-signed revision "
                                "and confirmed by the final original GPT and disclosed fresh Claude reviewers.",
             "evidence": [*evidence, adjudications["claude"], adjudications["gpt"]]}
            for family, claim, status, reason in RESOLUTION
        ],
    }


def closure_report_path(mode, output):
    return (HERE / "closure-real-report-002.json" if mode == "real"
            else output.with_name(output.name + "-report.json"))


def main(mode, output):
    report_path = closure_report_path(mode, output)
    require(mode in ("dry", "real") and not output.exists() and not report_path.exists(),
            "Preserve closure attempt")
    require((mode == "dry" and output.parent == HERE) or (mode == "real" and output == REPO / CLOSURE),
            "Unexpected closure destination")
    guard, _ = start_guard("B133 reconciled review closure")
    try:
        git = Git(REPO, RUNNER, guard)
        clean(git, REVISION, True)
        proof_raw = frozen(REVISION_PROOF, REVISION_PROOF_SHA)
        proof = json.loads(proof_raw)
        require(proof["candidate"] == REVISION and proof["status"] == "PASS_SIGNED_RECONCILIATION_BINDINGS_ONLY",
                "Revision proof differs")
        manifest = git("show", REVISION + ":manifest.json")
        require(sha(manifest) == proof["manifestSha256"] and (REPO / "manifest.json").read_bytes() == manifest,
                "Reviewed manifest differs")
        original = git("show", CANDIDATE + ":" + PROGRESS)
        require(git("show", REVISION + ":" + PROGRESS) == original
                and (REPO / PROGRESS).read_bytes() == original, "Original progress changed")
        files, local, retention, entries = {}, [], {}, []
        put(files, ".gitattributes", b"* -text\n")
        put(files, "verification/original-progress.json", original)
        for family in INITIALS:
            entry, retained, chain = initial_entry(files, family, guard)
            entries.append(entry)
            local.extend(retained)
            retention[entry["run"]] = chain

        for family, run, snapshot in (
            ("claude", "N1-B133-CLAUDE-CONFIRM-001", "110b4ffb6af078eb2adb00645db4c9e0bd6db188"),
            ("gpt", "N1-B133-GPT-CONFIRM-002", "d7d6cff92afe8220c16a5daa76f1c3f00a2bef30"),
        ):
            entry, retained, chain = confirmation_entry(files, family, run, snapshot)
            entries.append(entry)
            local.extend(retained)
            retention[run] = chain
        nonaccepted = []
        for run, name, digest in (
            ("N1-B133-GPT-CONFIRM-001", "gpt-confirm-001-adjudication-001.json",
             "987fb5f9fc5c793992b2d1d70d0ccf56086f8257656aa6837cfbcc0bc5b60adc"),
            ("N1-B133-CLAUDE-CONFIRM-002", "claude-confirm-002-adjudication-001.json",
             "8bba057dd162f4e32c8fa6e0c9243692643dc312fd2e4d2d8548ae1fe2ccf326"),
        ):
            entry, retained, chain = unaccepted_entry(files, run, REVIEW / name, digest)
            nonaccepted.append(entry)
            local.extend(retained)
            retention[run] = chain

        for family in INITIALS:
            entry, retained, chain = confirmation_entry(files, family)
            entries.append(entry)
            local.extend(retained)
            retention[entry["run"]] = chain
        retention["core"] = add_chain(files, "core", PREP / "core-chain-001.json", CORE_SHA, guard)
        put(files, "protocol/preflight.json", frozen(PREFLIGHT, PREFLIGHT_SHA))
        windows, sums_raw, protected_counts = protected_windows(guard)
        put(files, "packet/SHA256SUMS.json", sums_raw)
        revision_ref = put(files, "verification/signed-reconciliation.json", proof_raw)
        for name, digest in PROOFS.items():
            raw = read_review(REVIEW / name, digest)
            item = json.loads(raw)
            require(item["candidate"] == CANDIDATE and item["base"] == BASE and item["status"] == "PASS",
                    "Candidate proof differs")
            put(files, "verification/" + name, raw)
        source_proof = read_review(SOURCE_PROOF, SOURCE_PROOF_SHA)
        require(json.loads(source_proof)["status"] == "PASS", "Source reconciliation proof differs")
        source_proof_ref = put(files, "verification/reconciliation-sources.json", source_proof)
        adjudication_raw = read_review(ADJUDICATION, ADJUDICATION_SHA)
        adjudication = json.loads(adjudication_raw)
        require(adjudication["candidate"] == CANDIDATE and adjudication["openClaimIds"] == ["Q1", "Q2", "Q3", "Q4"]
                and adjudication["coordinatorClaimIds"] == ["C1", "C2", "C3", "C4", "C5", "C6"],
                "Coordinator adjudication differs")
        adjudication_ref = put(files, "verification/coordinator-adjudication.json", adjudication_raw)
        for name in TOOL_NAMES:
            put(files, "protocol/tools/" + name, frozen(TOOLS / name))
        for name in CONFIRMATION_TOOLS:
            put(files, "protocol/confirmation/" + name, frozen(CONFIRM / name))
        put(files, "verification/local-retention.json", json_bytes({
            "files": local, "protectedExtractFiles": protected_counts,
            "policy": "Raw audits, event histories, full rosters, confirmation specs and external captures "
                      "remain local. Failed preparations and unused drafts are preserved locally, not "
                      "successful reviews or additional review attempts.",
        }))
        resolution = resolution_record(entries, [revision_ref, source_proof_ref, adjudication_ref])
        resolution_ref = put(files, "resolution.json", json_bytes(resolution))
        allowed = {COORDINATOR, AUTHOR, *(entry["session"] for entry in entries)}
        uuids, leaks = publication_findings(files, windows, allowed, guard)
        checks = {"uuidFindings": len(uuids), "externalWindowFindings": len(leaks)}
        report = {"batch": BATCH, "mode": mode, "files": len(files) + 1,
                  "bytes": sum(map(len, files.values())), "publicationChecks": checks,
                  "uuidFindings": uuids, "externalWindowFindings": leaks}
        freeze_json(report_path, report)
        require(not uuids and not leaks, "Publication retention failed; inspect preserved report")
        closure = {
            "schemaVersion": 1, "batch": BATCH, "base": BASE, "initialSnapshot": CANDIDATE,
            "reviewedSnapshot": REVISION, "members": MEMBERS, "publication": "PENDING",
            "reviewLineage": entries, "finalRuns": ["N1-B133-CLAUDE-CONFIRM-003", "N1-B133-GPT-CONFIRM-003"],
            "intermediateRuns": ["N1-B133-CLAUDE-CONFIRM-001", "N1-B133-GPT-CONFIRM-002"],
            "nonAcceptedReviews": nonaccepted,
            "resolution": resolution_ref, "recordedFileSha256": {name: sha(raw) for name, raw in sorted(files.items())},
            "publicationChecks": checks, "chainRetention": retention,
            "packetManifestSha256": PACKET_SHA, "limits": LIMITS,
        }
        validate_reviews(closure, REVISION)
        validate_resolution(resolution, entries, REVISION, closure["recordedFileSha256"])
        closure_raw = json_bytes(closure)
        progress = closed_progress(json.loads(original), closure_raw, manifest, resolution)
        clean(git, REVISION, True)
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
    require(len(sys.argv) == 3, __doc__)
    main(sys.argv[1], Path(sys.argv[2]).resolve())

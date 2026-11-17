"""Assemble the B131 review-closure archive.

Usage: close_b131.py dry|real OUT
  dry   OUT is a new direct child of scratch-131. UUID and external-text window findings are
        reported in OUT-report.json; the batch progress ledger is untouched.
  real  OUT is b131-worktree/docs/n1-reviews/batch-131-closure. Findings fail closed and the
        batch progress ledger is rewritten after the archive is frozen.
"""
import gzip
import html
import json
import re
import sys
from pathlib import Path

from common import (COORDINATOR, TOOLS, WS, freeze_json, frozen, git, json_bytes, load_module,
                    readonly, require, sha, start_guard, write_frozen)

REPO = WS / "b131-worktree"
CONFIG = {"repo": str(REPO)}
SCRATCH = WS / "scratch-131"
REVIEW = SCRATCH / "review"
REPORTS = WS / "reports-131"
REVIEW_CHAINS = WS / "review-chains"
LEDGER = Path(r"C:\Users\stop-\.copilot\session-state") / COORDINATOR / "files" / "b131-authoring-assignment.json"
BOUNDED = WS / "scratch-115" / "assemble-closure.py"
CLOSURE_REL = "docs/n1-reviews/batch-131-closure"
PROGRESS_REL = "docs/n1-sources/batch-131-progress.json"
BASE = "cb0f5581bdda84f7e673225c19126c85e242e57b"
INITIAL = "1359b467e0edee8822c665614d6ca57e42785c4d"
REVIEWED = "88a9dfab6a783b082659b742a24242342bb2e461"
SOURCE_BASE = "6da1184b82b60553f9b65c57f53289c779f96f7c"
FINGERPRINT = "D4C9A275A218AF747B787AFA9D94B9D311BD26A7"
MEMBERS = ["衛", "羊", "霜"]
SOURCE_ROWS = [977, 870, 1174]
MANIFEST_SHA = "37368d2baab4fc70d5e6696f44c38caa3f4adb2017298652d7f8b418ffcb6329"
CONTENT_VERSION = "51b44905cb6b6a81"
RUNTIME_ENTRIES = 8737
PACKETS = {
    "compact-001": (WS / "review-packets" / "batch-131-1359b467-compact-001",
                    "454c924ce460d050d31eedca225b9553d42790a0060df474088e38c7ca049b39"),
    "compact-002": (WS / "review-packets" / "batch-131-1359b467-compact-002",
                    "7a8308db2ca5f912afbb61151afff31f98ee5b35c5b357957e9c80835010305c"),
}
CLAUDE = "95cb8d22-f976-4ed5-bb62-0a3a52ff2931"
GPT = "ebb78462-3199-4b4f-9afc-18103f010fc9"
AUTHOR = "868aa8d9-f7fe-41f5-91b1-38fed99fa6f5"
TOP_CHAT = "e1ee36b6-cb53-4c64-854e-cec8a61c1dfb"
EXCLUDED_SESSIONS = {"94a1b0ae-e1c1-462a-ba0f-9a23171211b7", "91c7afbb-aae4-4d63-9af7-e71e48b68b83",
                     "aa87b029-4a2d-42cd-b321-12caefc89b2a"}
ALLOWED_UUIDS = {COORDINATOR, CLAUDE, GPT, AUTHOR, TOP_CHAT, *EXCLUDED_SESSIONS}
ACCEPTED = {
    "N1-B131-CLAUDE-003": {"family": "claude", "role": "initial", "dir": "preparation-003",
                           "snapshot": INITIAL, "session": CLAUDE, "key": "verdict",
                           "verdict": "NEEDS FIX", "reads": ("core", "extension")},
    "N1-B131-GPT-004": {"family": "gpt", "role": "initial", "dir": "preparation-004",
                        "snapshot": INITIAL, "session": GPT, "key": "verdict",
                        "verdict": "UNVERIFIED", "reads": ("core", "extension")},
    "N1-B131-CLAUDE-CONFIRM-003": {"family": "claude", "role": "confirmation", "dir": "confirm-003",
                                   "snapshot": REVIEWED, "session": CLAUDE, "key": "confirmation",
                                   "verdict": "CONFIRMED", "reads": ("chain",)},
    "N1-B131-GPT-CONFIRM-003": {"family": "gpt", "role": "confirmation", "dir": "confirm-003",
                                "snapshot": REVIEWED, "session": GPT, "key": "confirmation",
                                "verdict": "CONFIRMED", "reads": ("chain",)},
}
FINAL_RUNS = ["N1-B131-CLAUDE-CONFIRM-003", "N1-B131-GPT-CONFIRM-003"]
EXCLUDED = {
    "N1-B131-CLAUDE-001": ("claude", "reviewClaude001", ("status",)),
    "N1-B131-CLAUDE-002": ("claude", "reviewClaude002", ("status",)),
    "N1-B131-GPT-003": ("gpt", "reviewGpt003", None),
}
PREPARED_ONLY = {
    "N1-B131-CLAUDE-CONFIRM-001": ("claude", "PREPARED_NOT_ADMITTED"),
    "N1-B131-CLAUDE-CONFIRM-002": ("claude", "PREPARED_ADMISSION_FAILED_NOT_LAUNCHED"),
    "N1-B131-GPT-CONFIRM-002": ("gpt", "PREPARED_NOT_ADMITTED"),
}
DEPENDENCIES = ("common.py", "run_b127_tool.py", "archive_b129_chains.py", "b130_source_schema.py",
                "test_b130_source_schema.py", "build-prompts-b130-attempt004.py", "confirm_b130_compact.py",
                "prepare-chain-b130-compact.py", "step_b130_compact.py", "source_query_union.py",
                "verify_b126_sources.py", "verify_b127_sources.py", "verify_b130_payload.py",
                "test_verify_b130_payload.py", "verify_b130_sources.py")
AGGREGATES = ("preparation-002/validation-001", "preparation-003/validation-001",
              "preparation-003/validation-002", "preparation-004/validation-004",
              "compact002-protocol-coordinator-tests-001", "preparation004-coordinator-controls-001")
PRIVATE_EXACT = {"reconciliation-001-author-status.json", "reconciliation-001-author-admission.json",
                 "capacity-telemetry-shape-001/output.log"}
EXTERNAL_DIRS = {"external-snapshots", "external-reconciliation", "original-source-sections", "community",
                 "external"}
PROTECTED_EXCERPTS = {"confirmation-003-membership/membership.json", "coordinator-packet-verification-002.json",
                      "coordinator-packet-verification-003.json",
                      "preparation-003/N1-B131-CLAUDE-003-evidence-check.json",
                      "preparation-004/N1-B131-GPT-004-evidence-check.json"}
MAX_PUBLISHED = 256 * 1024
WINDOW, STRIDE, MIN_NON_ASCII = 32, 16, 8
UUID = re.compile(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}")
STATUS = "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION"
FILES = {}


def put(name, raw):
    require(not name.endswith(".jsonl"), "Raw event logs stay local: " + name)
    require(name not in FILES or FILES[name] == raw, "Conflicting archive file: " + name)
    FILES[name] = raw
    return {"path": name, "sha256": sha(raw)}


def dump(name, value):
    return put(name, json_bytes(value))


def arch(path):
    path = Path(path)
    for root, prefix in ((REVIEW, "review/"), (REPORTS, "reports/"), (TOOLS, "protocol/tools/")):
        try:
            return prefix + path.relative_to(root).as_posix()
        except ValueError:
            continue
    raise ValueError(f"No archive location for {path}")


def bound(path, digest):
    name = arch(path)
    require(name in FILES and sha(FILES[name]) == digest, "Bound file is not published unchanged: " + name)
    return {"path": name, "sha256": digest}


def is_local_only_source(source):
    source = source.removeprefix("original-packet/")
    return ((source.startswith("evidence/external-snapshots/")
             and source != "evidence/external-snapshots/manifest.json")
            or source.startswith(("external-reconciliation/", "original-source-sections/",
                                  "evidence/community/", "community/")))


def prepare(manifest_raw, segment_bytes):
    """archive_b129_chains.prepare with the B131 community-membership extension."""
    manifest = json.loads(manifest_raw)
    segments = manifest["segments"]
    require(set(segment_bytes) == {s["path"] for s in segments}, "Chain segment set differs")
    files = {"manifest.json": manifest_raw}
    archived, local_only = [], []
    for segment in segments:
        raw = segment_bytes[segment["path"]]
        require(sha(raw) == segment["sha256"], "Original chain segment hash differs")
        protected = [part for part in segment["parts"] if is_local_only_source(part["source"])]
        if protected:
            local_only.append({
                "index": segment["index"], "sha256": segment["sha256"], "bytes": len(raw),
                "sources": [{"source": p["source"], "sha256": p["sha256"], "firstLine": p["a"],
                             "lastLine": p["b"]} for p in protected]})
            continue
        name = Path(segment["path"]).name + ".gz"
        require(name not in files, "Duplicate archive segment name")
        packed = gzip.compress(raw, mtime=0)
        require(gzip.decompress(packed) == raw, "Chain compression differs")
        files[name] = packed
        archived.append(segment["index"])
    retention = {
        "schemaVersion": 1,
        "originalManifestSha256": sha(manifest_raw),
        "originalSegments": len(segments),
        "archivedSegmentIndices": archived,
        "localOnlySegments": local_only,
        "policy": "Segments containing complete external source extracts or the pinned community "
                  "membership array remain local in full, including any other material sharing those "
                  "segments. The original manifest, source ranges and hashes are retained without "
                  "altering review inputs. This publication archive is not a complete copy of the "
                  "local read chains.",
    }
    files["retention.json"] = json_bytes(retention)
    return files, retention


def aggregate_root(rel):
    for root in AGGREGATES:
        if rel.startswith(root + "/") and "/" in rel[len(root) + 1:]:
            return root
    parts = rel.split("/")
    if "fixtures" in parts[:-1]:
        return "/".join(parts[:parts.index("fixtures") + 1])
    return None


def classify(rel, path, size):
    parts = rel.split("/")
    name = parts[-1]
    if parts[0].startswith("closure-"):
        return "closure-execution"
    if aggregate_root(rel):
        return "aggregate"
    if "chains" in parts[:-1]:
        return "chain"
    if "__pycache__" in parts or name.endswith(".pyc"):
        return "cache"
    if name.endswith(".jsonl"):
        return "raw-events"
    if name == "audit.json" and len(parts) > 1 and parts[-2].startswith("audit-"):
        return "raw-audit"
    if (rel in PRIVATE_EXACT or rel.startswith("claude-admission-snapshots-001/")
            or name.endswith(("admission-roster.txt", "admission-status.json"))
            or "observed" in name or name.startswith("review-preparation-full-")):
        return "private-session-roster"
    if (name.lower().endswith((".html", ".htm")) or re.match(r"external-\d", name)
            or name.startswith("n1-kanji-source-") or "community" in name
            or EXTERNAL_DIRS.intersection(parts[:-1])):
        return "external-source"
    if rel in PROTECTED_EXCERPTS:
        return "protected-source-excerpt"
    if not readonly(path):
        return "writable"
    if size > MAX_PUBLISHED:
        return "oversize"
    return "publish"


def tree_sha(entries):
    return sha(json.dumps(sorted(entries), ensure_ascii=False).encode("utf-8"))


def normalize(text):
    return re.sub(r"\s+", "", text)


def add_protected(windows, raw, is_html):
    text = raw.decode("utf-8", "replace")
    if is_html:
        text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    text = normalize(text)
    for index in range(0, max(len(text) - WINDOW + 1, 0), STRIDE):
        window = text[index:index + WINDOW]
        if sum(ord(c) > 127 for c in window) >= MIN_NON_ASCII:
            windows.add(window)


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, item in value.items():
            yield key
            yield from strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)


def texts(name, raw):
    if name.endswith(".gz"):
        raw = gzip.decompress(raw)
    text = raw.decode("utf-8", "replace")
    result = [text]
    if name.endswith(".json"):
        try:
            result.append("\n".join(strings(json.loads(text))))
        except ValueError:
            pass
    return result


def references(value):
    if isinstance(value, dict):
        path, digest = value.get("path"), value.get("sha256")
        if isinstance(path, str) and isinstance(digest, str) and re.fullmatch(r"[0-9a-f]{64}", digest):
            yield path, digest
        for item in value.values():
            yield from references(item)
    elif isinstance(value, list):
        for item in value:
            yield from references(item)


def check_git():
    require(git(CONFIG, "rev-parse", "HEAD").decode().strip() == REVIEWED, "HEAD is not signed 88a9dfab")
    require(git(CONFIG, "rev-parse", "HEAD^@").decode().split() == [INITIAL], "Reviewed parent differs")
    require(git(CONFIG, "rev-parse", f"{INITIAL}^@").decode().split() == [BASE], "Initial parent differs")
    require(git(CONFIG, "log", "-1", "--format=%G?|%GF", REVIEWED).decode().strip() == "G|" + FINGERPRINT,
            "Reviewed snapshot signature differs")
    require(sha(git(CONFIG, "show", f"{REVIEWED}:manifest.json")) == MANIFEST_SHA, "Reviewed manifest differs")
    return git(CONFIG, "status", "--porcelain=v1", "--untracked-files=all")


def packets(guard, windows):
    result = {}
    for name, (root, expected) in PACKETS.items():
        raw = frozen(root / "SHA256SUMS.json", expected)
        sums = json.loads(raw)
        require(isinstance(sums, dict) and sums, "Packet sums must be a non-empty mapping")
        protected = 0
        for count, (rel, digest) in enumerate(sums.items()):
            if count % 50 == 0:
                guard.check()
            data = frozen(root / Path(rel), digest)
            if is_local_only_source(rel):
                add_protected(windows, data, rel.lower().endswith((".html", ".htm")))
                protected += 1
        on_disk = sorted(p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file())
        require(on_disk == sorted([*sums, "SHA256SUMS.json"]), "Packet contains unlisted files: " + name)
        put(f"packet/{name}/SHA256SUMS.json", raw)
        put(f"packet/{name}/packet.json", frozen(root / "packet.json", sums.get("packet.json")))
        result[name] = {"root": str(root), "sha256SumsSha256": expected, "listedFiles": len(sums),
                        "localOnlyExternalFiles": protected,
                        "archived": [f"packet/{name}/SHA256SUMS.json", f"packet/{name}/packet.json"]}
    return result


def chain_name(manifest_path):
    stem = manifest_path.stem
    if stem.startswith("core-chain-"):
        return "core-" + stem.removeprefix("core-chain-")
    return stem.removesuffix("-chain")


def chains(guard, windows):
    found = {}
    for path in sorted(REVIEW.rglob("*.json")):
        rel = path.relative_to(REVIEW).as_posix()
        if aggregate_root(rel) or rel.startswith("closure-") or path.stat().st_size > 4_000_000:
            continue
        try:
            value = json.loads(path.read_bytes())
        except ValueError:
            continue
        segments = value.get("segments") if isinstance(value, dict) else None
        if (isinstance(segments, list) and segments and isinstance(segments[0], dict)
                and "path" in segments[0] and "parts" in segments[0]):
            found.setdefault(sha(path.read_bytes()), []).append(path)
    records, segment_paths = [], {}
    for digest, paths in found.items():
        name = chain_name(paths[0])
        require(all(chain_name(p) == name for p in paths), "Duplicate manifests disagree on name")
        raw = frozen(paths[0], digest)
        manifest = json.loads(raw)
        segment_bytes = {}
        for count, segment in enumerate(manifest["segments"]):
            if count % 25 == 0:
                guard.check()
            segment_bytes[segment["path"]] = frozen(segment["path"], segment["sha256"])
            segment_paths[Path(segment["path"])] = segment["sha256"]
        files, retention = prepare(raw, segment_bytes)
        by_index = {s["index"]: s["path"] for s in manifest["segments"]}
        for local in retention["localOnlySegments"]:
            add_protected(windows, segment_bytes[by_index[local["index"]]], False)
        for file_name, data in files.items():
            put(f"chains/{name}/{file_name}", data)
        records.append({
            "name": name, "path": f"chains/{name}", "manifestSha256": digest,
            "manifestCopies": [arch(p) for p in paths], "segments": len(manifest["segments"]),
            "archivedSegmentIndices": retention["archivedSegmentIndices"],
            "localOnlySegmentIndices": [s["index"] for s in retention["localOnlySegments"]],
            "retentionSha256": sha(files["retention.json"])})
    return sorted(records, key=lambda r: r["name"]), segment_paths


def mirror(guard, windows, segment_paths):
    local, aggregates, unbound = [], {}, []
    for count, path in enumerate(sorted(REVIEW.rglob("*"))):
        if not path.is_file():
            continue
        if count % 100 == 0:
            guard.check()
        rel = path.relative_to(REVIEW).as_posix()
        raw = path.read_bytes()
        kind = classify(rel, path, len(raw))
        if kind == "closure-execution":
            continue
        if kind == "aggregate":
            root = aggregate_root(rel)
            aggregates.setdefault(root, []).append([rel[len(root) + 1:], sha(raw), len(raw)])
        elif kind == "chain":
            if segment_paths.get(path) != sha(raw):
                unbound.append({"path": "scratch-131/review/" + rel, "sha256": sha(raw), "bytes": len(raw)})
        elif kind == "publish":
            put("review/" + rel, frozen(path))
        else:
            if kind == "external-source":
                add_protected(windows, raw, path.suffix.lower() in (".html", ".htm"))
            local.append({"path": "scratch-131/review/" + rel, "sha256": sha(raw), "bytes": len(raw),
                          "reason": kind})
    for directory in sorted(REVIEW_CHAINS.glob("n1-b131-*")):
        for path in sorted(directory.rglob("*")):
            if path.is_file() and segment_paths.get(path) != sha(path.read_bytes()):
                unbound.append({"path": path.relative_to(WS).as_posix(), "sha256": sha(path.read_bytes()),
                                "bytes": path.stat().st_size})
    groups = [{"root": "scratch-131/review/" + root, "files": len(entries),
               "bytes": sum(e[2] for e in entries), "treeSha256": tree_sha(entries),
               "reason": "synthetic-test-fixtures"} for root, entries in sorted(aggregates.items())]
    return local, groups, unbound


def void_summary(path, raw, audit, status):
    fields = ("session", "eventsSha256", "eventsBytes", "eventsCount", "sliceSha256", "sliceBytes",
              "offset", "prefixSha256", "status", "breaches", "bootstrapVerified", "actualResponseModels",
              "reviewerIdle", "recordIncomplete", "unexpectedUserMessages", "coreRead", "coreRequired",
              "extensionRead", "extensionRequired", "writes", "readbacks", "readbackVerified",
              "reportBinding", "fetches")
    result = {key: audit[key] for key in fields if key in audit}
    messages, notes, calls = audit.get("messages", []), audit.get("notes", []), audit.get("calls", [])
    result.update({
        "originalAuditSha256": sha(raw), "rawExecutionPayloadsRemainLocal": True,
        "reviewAccepted": False, "finalAcceptance": False, "excludedStatus": status,
        "rawCompletionMessageCount": len(messages),
        "rawCompletionMessagesSha256": sha(json.dumps(messages, ensure_ascii=False).encode("utf-8")),
        "notesCount": len(notes), "notesSha256": sha(json.dumps(notes, ensure_ascii=False).encode("utf-8")),
        "callCount": len(calls),
        "rawCallsSha256": sha(json.dumps(calls, ensure_ascii=False, sort_keys=True).encode("utf-8")),
        "representation": "Non-accepting audit with recorded breaches. Bounded mechanical fields only; "
                          "completion messages, notes and calls are represented by counts and hashes "
                          "and remain local with the raw audit and events."})
    return result


def audits(guard, accepted_audits, excluded_status):
    bounded_audit = load_module("n1_bounded_archive", BOUNDED).bounded_audit
    roles, by_run = {}, {}
    for path in sorted(REVIEW.rglob("audit.json")):
        rel = path.relative_to(REVIEW).as_posix()
        parts = rel.split("/")
        if aggregate_root(rel) or parts[0].startswith("closure-") or not parts[-2].startswith("audit-"):
            continue
        guard.check()
        raw = frozen(path)
        audit = json.loads(raw)
        run = parts[-3]
        if not audit.get("breaches") and audit.get("reviewerIdle"):
            summary = bounded_audit(path)
        else:
            require(run in excluded_status, "Breached audit outside an excluded run: " + rel)
            summary = void_summary(path, raw, audit, excluded_status[run])
        name = "review/" + "/".join(parts[:-1]) + "/audit-summary.json"
        dump(name, summary)
        if path in accepted_audits:
            role = "accepted-final"
        elif run in excluded_status:
            role = f"excluded-initial:{audit.get('status')}"
        elif audit.get("status") == "PHASE1_READY":
            role = "phase1-of-accepted-run"
        else:
            role = f"superseded-not-accepted:{audit.get('status')}"
        roles[name] = {"run": run, "role": role, "status": audit.get("status"),
                       "breaches": len(audit.get("breaches") or []), "originalAuditSha256": sha(raw),
                       "session": audit.get("session")}
        by_run.setdefault(run, []).append(name)
    require(all(p in [Path(REVIEW / "/".join(n.split("/")[1:-1]) / "audit.json") for n in roles]
                for p in accepted_audits), "Accepted audit lacks a summary")
    return roles, by_run


def record(run, spec):
    root = REVIEW / spec["dir"]
    acceptance_raw = frozen(root / f"{run}-acceptance.json")
    acceptance = json.loads(acceptance_raw)
    require(acceptance["run"] == run and acceptance["candidate"] == spec["snapshot"]
            and acceptance["reviewAccepted"] is True and acceptance[spec["key"]] == spec["verdict"],
            "Acceptance differs: " + run)
    final_raw = frozen(acceptance["final"]["path"], acceptance["final"]["sha256"])
    final = json.loads(final_raw)
    require(final["run"] == run and final["candidate"] == spec["snapshot"] and final["status"] == STATUS
            and final["session"] == spec["session"], "Mechanical final differs: " + run)
    audit_ref = final["finalAudit"] if spec["role"] == "initial" else final["audit"]
    audit = json.loads(frozen(audit_ref["path"], audit_ref["sha256"]))
    require(audit["final"] is True and audit["reviewerIdle"] is True and audit["recordIncomplete"] is False
            and audit["breaches"] == [] and not audit["unexpectedUserMessages"] and audit["fetches"] == 0
            and audit["writes"] == audit["readbacks"] == 1 and audit["readbackVerified"] is True
            and audit["session"] == spec["session"]
            and all(audit[f"{r}Read"] == audit[f"{r}Required"] for r in spec["reads"]),
            "Final audit differs: " + run)
    context = json.loads(frozen(final["context"]["path"], final["context"]["sha256"]))
    require(context["status"] == "PASS" and context["compactions"] == []
            and context["eventsSha256"] == audit["eventsSha256"], "Context audit differs: " + run)
    structure = json.loads(frozen(final["structure"]["path"], final["structure"]["sha256"]))
    require(structure["status"] == "PASS"
            and structure["overall" if spec["role"] == "initial" else "confirmation"] == spec["verdict"],
            "Structure audit differs: " + run)
    report = acceptance["report"]
    frozen(report["path"], report["sha256"])
    adjudication_raw = frozen(acceptance["adjudication"]["path"], acceptance["adjudication"]["sha256"])
    adjudication = json.loads(adjudication_raw)
    entry = {"run": run, "family": spec["family"], "role": spec["role"], "session": spec["session"],
             "snapshot": spec["snapshot"], spec["key"]: spec["verdict"], "reviewAccepted": True,
             "acceptance": bound(root / f"{run}-acceptance.json", sha(acceptance_raw)),
             "adjudication": bound(acceptance["adjudication"]["path"], acceptance["adjudication"]["sha256"]),
             "final": bound(acceptance["final"]["path"], acceptance["final"]["sha256"]),
             "report": bound(report["path"], report["sha256"]),
             "context": bound(final["context"]["path"], final["context"]["sha256"]),
             "structure": bound(final["structure"]["path"], final["structure"]["sha256"]),
             "auditSummary": "review/" + Path(audit_ref["path"]).parent.relative_to(REVIEW).as_posix()
                             + "/audit-summary.json",
             "originalAuditSha256": audit_ref["sha256"]}
    if spec["role"] == "initial":
        require(final["preflightSha256"] == sha(frozen(final["preflight"])), "Preflight differs: " + run)
        entry["preflight"] = bound(final["preflight"], final["preflightSha256"])
        entry["acceptedFindings"] = acceptance["acceptedFindings"]
        entry["openClaimIds"] = adjudication.get("openClaimIds", [])
        entry["publicationAccepted"] = False
    else:
        require(final["confirmation"] == spec["verdict"] and final["report"]["sha256"] == report["sha256"],
                "Confirmation final differs: " + run)
        entry["preflight"] = bound(root / f"{run}-preflight.json", sha(frozen(root / f"{run}-preflight.json")))
        entry["dispositions"] = adjudication.get("dispositions", {})
    return entry, Path(audit_ref["path"]), adjudication


def hold(run, family, key, ledger, ledger_sha, summaries, roles):
    entry = ledger[key]
    status = ledger["reviewGpt003Status"] if run == "N1-B131-GPT-003" else entry["status"]
    require("not-accepted" in status, "Excluded run status must be non-accepting: " + run)
    sessions = {roles[name]["session"] for name in summaries}
    require(len(sessions) == 1 and sessions <= ALLOWED_UUIDS, "Excluded run session differs: " + run)
    reasons = {k: entry[k] for k in ("rootCause", "quarantine", "next") if k in entry}
    if run == "N1-B131-GPT-003":
        reasons.update({k: entry["phase1"][k] for k in ("preservation", "disposition")})
    lists = sorted(n for n in FILES if n.startswith("review/") and n.endswith("/phase1-list.txt")
                   and f"/{run}/" in n)
    runfiles = sorted(n for n in FILES if n.startswith("review/") and Path(n).name.startswith(run + "-"))
    value = {"batch": 131, "run": run, "family": family, "session": sessions.pop(), "candidate": INITIAL,
             "status": status, "reviewAccepted": False, "finalAcceptance": False,
             "audits": [{"summary": n, "status": roles[n]["status"],
                         "originalAuditSha256": roles[n]["originalAuditSha256"]} for n in summaries],
             "quarantinedPhase1Lists": lists, "runFiles": runfiles, **reasons,
             "ledger": {"key": key, "sha256": ledger_sha},
             "evidenceStatus": "Preserved for audit only. Quarantined lists, messages and observations are "
                               "not review evidence and were not shared with the author, preparer or later "
                               "reviewers."}
    dump(f"excluded-initials/{run}/hold.json", value)
    return {"run": run, "family": family, "session": value["session"], "status": status,
            "reviewAccepted": False, "finalAcceptance": False,
            "holdSha256": sha(FILES[f"excluded-initials/{run}/hold.json"])}


def prepared_only(ledger, ledger_sha):
    preparation = json.loads(frozen(REVIEW / "confirmation-003-preparation.json"))
    failures = ledger["signedReconciliationVerification001"]["confirmationPreparation"]["preservedFailures"]
    result = []
    for run, (family, status) in PREPARED_ONLY.items():
        published = sorted(n for n in FILES if n.startswith("review/confirm-003/" + run + "-"))
        require(published, "Prepared-only run lacks published files: " + run)
        reason = (ledger["confirmationPreparation004"]["reason"] if run == "N1-B131-CLAUDE-CONFIRM-002"
                  else failures)
        result.append({"run": run, "family": family, "session": CLAUDE if family == "claude" else GPT,
                       "status": status, "reason": reason, "files": published,
                       "preparationRecord": "review/confirmation-003-preparation.json",
                       "preparationStatus": preparation["status"], "ledgerSha256": ledger_sha,
                       "confirmationAccepted": False, "reviewEvidenceAccepted": False})
    return result


def protocol(guard):
    names = sorted({p.name for p in TOOLS.iterdir() if p.is_file() and "b131" in p.name} | set(DEPENDENCIES))
    for name in names:
        guard.check()
        put("protocol/tools/" + name, frozen(TOOLS / name))
    return names


def resolve_references(segment_paths, local):
    local_sha = {entry["path"]: entry["sha256"] for entry in local}
    added, historical, mismatched, other = [], [], [], {}
    packet_sums = {root: json.loads((root / "SHA256SUMS.json").read_bytes()) for root, _ in PACKETS.values()}
    for name in sorted(n for n in list(FILES) if n.endswith(".json")):
        try:
            value = json.loads(FILES[name])
        except ValueError:
            continue
        for raw_path, digest in references(value):
            path = Path(raw_path)
            if not path.is_absolute():
                path = WS / path
            if segment_paths.get(path) == digest:
                continue
            packet = next((r for r in packet_sums if _under(path, r)), None)
            if packet:
                rel = path.relative_to(packet).as_posix()
                if packet_sums[packet].get(rel) != digest and rel != "SHA256SUMS.json":
                    mismatched.append({"path": str(path), "sha256": digest, "in": name})
                continue
            if _under(path, TOOLS):
                target = "protocol/tools/" + path.relative_to(TOOLS).as_posix()
                if target in FILES and sha(FILES[target]) == digest:
                    continue
                if path.is_file() and readonly(path) and sha(path.read_bytes()) == digest and target not in FILES:
                    put(target, path.read_bytes())
                    added.append(target)
                else:
                    historical.append({"path": str(path), "sha256": digest, "in": name})
                continue
            if _under(path, REVIEW) or _under(path, REPORTS):
                target = arch(path)
                local_name = "scratch-131/review/" + path.relative_to(REVIEW).as_posix() if _under(path, REVIEW) else None
                if (target in FILES and sha(FILES[target]) == digest) or local_sha.get(local_name) == digest:
                    continue
                if (path.is_file() and sha(path.read_bytes()) == digest
                        and (_under(path, REVIEW) and path.relative_to(REVIEW).parts[0].startswith("closure-")
                             or aggregate_root(path.relative_to(REVIEW).as_posix() if _under(path, REVIEW) else ""))):
                    continue
                mismatched.append({"path": str(path), "sha256": digest, "in": name})
                continue
            other.setdefault(str(path), set()).add(digest)
    return added, historical, mismatched, {k: sorted(v) for k, v in sorted(other.items())}


def _under(path, root):
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def publication_checks(guard, windows):
    uuids, leaks = [], []
    for count, (name, raw) in enumerate(sorted(FILES.items())):
        if count % 50 == 0:
            guard.check()
        for text in texts(name, raw):
            for match in sorted({m.group(0).lower() for m in UUID.finditer(text)} - ALLOWED_UUIDS):
                uuids.append({"file": name, "uuid": match})
            normalized = normalize(text)
            if not windows or not any(ord(c) > 127 for c in normalized):
                continue
            hits = [i for i in range(len(normalized) - WINDOW + 1) if normalized[i:i + WINDOW] in windows]
            if hits:
                leaks.append({"file": name, "windows": len(hits),
                              "sample": normalized[hits[0]:hits[0] + WINDOW * 3]})
    return uuids, leaks


def progress(provenance_sha, lineage, excluded, prepared, runtime_open):
    original = git(CONFIG, "show", f"{REVIEWED}:{PROGRESS_REL}")
    old = json.loads(original)
    require(old["status"] == "local-unreviewed-author-candidate" and old["members"] == MEMBERS,
            "Unexpected original progress")
    finals = {e["run"]: e for e in lineage}
    initial = {"claude": finals["N1-B131-CLAUDE-003"], "gpt": finals["N1-B131-GPT-004"]}
    return {
        "batch": 131, "base": BASE, "originalSourceBase": SOURCE_BASE, "governingIssue": 60,
        "status": "textual-review-closed-publication-pending",
        "membership": MEMBERS, "sourceRows": SOURCE_ROWS, "supports": old["supports"],
        "initialSnapshot": INITIAL, "reviewedSnapshot": REVIEWED,
        "reviewClosed": MEMBERS, "published": [], "runtimePublished": False,
        "accounting": {"frozenPendingRecords": 1228, "publishedPendingRecordsWithCards": 264,
                       "publishedN1Additions": 258, "n2Placements": 6, "undelivered": 964,
                       "reviewClosedPendingRecordsWithCards": 267, "localUnreviewedDrafts": 0,
                       "notStarted": 961, "overallN1TaskComplete": False},
        "runtimeCandidate": {"manifestSha256": MANIFEST_SHA, "contentVersion": CONTENT_VERSION,
                             "runtimeEntries": RUNTIME_ENTRIES},
        "review": {
            "status": "closed-with-disclosed-limits",
            "finalRuns": FINAL_RUNS,
            "finalConfirmations": [{"run": r, "family": finals[r]["family"], "session": finals[r]["session"],
                                    "candidate": REVIEWED, "confirmation": "CONFIRMED",
                                    "confirmationAccepted": True,
                                    "acceptanceSha256": finals[r]["acceptance"]["sha256"],
                                    "adjudicationSha256": finals[r]["adjudication"]["sha256"],
                                    "dispositions": sorted(finals[r]["dispositions"])} for r in FINAL_RUNS],
            "closure": "../n1-reviews/batch-131-closure/provenance.json",
            "closureProvenanceSha256": provenance_sha,
            "remainingActionableFindings": [], "remainingConsequentialClaims": [],
            "historicalReportsPreserved": True,
            "initialHistory": {family: {"run": e["run"], "verdict": e["verdict"],
                                        "acceptanceSha256": e["acceptance"]["sha256"],
                                        "adjudicationSha256": e["adjudication"]["sha256"],
                                        "acceptedFindings": e["acceptedFindings"],
                                        "openClaimIds": runtime_open[family]}
                               for family, e in initial.items()},
            "excludedInitialRuns": [{"run": e["run"], "status": e["status"], "holdSha256": e["holdSha256"]}
                                    for e in excluded],
            "retiredUnlaunchedRuns": [{"run": "N1-B131-GPT-002",
                                       "status": "retired-unlaunched: same missing report parent; "
                                                 "replaced by fresh pair"}],
            "preparedOnlyConfirmationRuns": [{"run": e["run"], "status": e["status"],
                                              "confirmationAccepted": False} for e in prepared],
            "identity": "Claude003 remains NEEDS FIX (F1/F2 accepted) and GPT004 remains UNVERIFIED with "
                        "Q1-Q13 open on unchanged 1359b467, attributed to their original sessions. The signed "
                        "reconciliation 88a9dfab addressed F1/F2/C1 and Q1-Q13; the same sessions separately "
                        "CONFIRMED it. Excluded, retired and prepared-only runs are not review evidence.",
        },
        "publicationGates": ["Owner-signed publication", "CI", "Exact served ZIP/runtime equality"],
        "correctionSources": ["batch-131-reconciliation/"],
        "reconciliationProgress": "batch-131-progress-reconciliation-001.json",
        "originalAuthorProgress": "../n1-reviews/batch-131-closure/verification/original-progress.json",
        "originalAuthorWarnings": old["warnings"],
        "limits": LIMITS,
    }


LIMITS = [
    "Bounded textual/host review, not exhaustive linguistic or arbitrary/custom-pool acceptance.",
    "No new native/device, installed-APK, image, font-rendering or stroke-geometry acceptance; five "
    "taught/comparison code points lack bundled-font cmap coverage.",
    "Six latent smaller-pool reading collisions and multiple-borrow-pool risks remain outside tested-pool "
    "acceptance.",
    "Modern-level membership of 衛/羊/霜 rests on the named community array, not an official JLPT syllabus.",
    "衛 historical founder/date discrepancies, missing historical glyph images and broad-family sense "
    "allocations remain qualified.",
    "Non-selected dictionary records were not reread; every initial and confirmation report's recorded "
    "limits remain applicable.",
    "Complete external captures, the pinned community array and co-located chain material remain local.",
    "No delivery or whole-set credit before owner-signed publication, CI and served ZIP/runtime equality.",
]


def main(mode, out):
    require(mode in ("dry", "real"), "Mode must be dry or real")
    closure = REPO / Path(CLOSURE_REL)
    if mode == "real":
        require(out == closure and not out.exists(), "Real output must be the absent worktree closure")
    else:
        require(out.parent == SCRATCH and not out.exists(), "Dry output must be a new scratch-131 child")
    guard, _ = start_guard("B131 closure")
    try:
        status = check_git()
        require(not status, "Worktree must be clean before closure")
        ledger_raw = LEDGER.read_bytes()
        ledger = json.loads(ledger_raw)
        ledger_sha = sha(ledger_raw)
        windows = set()
        packet_records = packets(guard, windows)
        chain_records, segment_paths = chains(guard, windows)
        local, groups, unbound = mirror(guard, windows, segment_paths)
        reports = sorted(p.name for p in REPORTS.iterdir())
        require(reports == ["N1-B131-CLAUDE-CONFIRM-003.md", "N1-B131-GPT-CONFIRM-003.md"],
                "Unexpected reports-131 content")
        for name in reports:
            put("reports/" + name, frozen(REPORTS / name))
        lineage, accepted_audits, adjudications = [], set(), {}
        excluded_status = {}
        for run, (_, key, _) in EXCLUDED.items():
            excluded_status[run] = (ledger["reviewGpt003Status"] if run == "N1-B131-GPT-003"
                                    else ledger[key]["status"])
        accepted_paths = {}
        for run, spec in ACCEPTED.items():
            acceptance = json.loads(frozen(REVIEW / spec["dir"] / f"{run}-acceptance.json"))
            final = json.loads(frozen(acceptance["final"]["path"], acceptance["final"]["sha256"]))
            ref = final["finalAudit"] if spec["role"] == "initial" else final["audit"]
            accepted_paths[run] = Path(ref["path"])
        roles, by_run = audits(guard, set(accepted_paths.values()), excluded_status)
        for run, spec in ACCEPTED.items():
            entry, audit_path, adjudication = record(run, spec)
            require(entry["auditSummary"] in roles and roles[entry["auditSummary"]]["role"] == "accepted-final",
                    "Accepted audit summary missing: " + run)
            lineage.append(entry)
            adjudications[run] = adjudication
        runtime = json.loads(frozen(REVIEW / "revision-runtime-proof-001.json"))
        require(runtime["candidate"] == REVIEWED and runtime["manifestSha256"] == MANIFEST_SHA
                and runtime["contentVersion"] == CONTENT_VERSION and runtime["runtimeEntries"] == RUNTIME_ENTRIES,
                "Runtime proof differs")
        runtime_open = runtime["initialOpenClaimIds"]
        require(runtime_open["gpt"] == adjudications["N1-B131-GPT-004"]["openClaimIds"],
                "GPT open claims differ")
        excluded = [hold(run, family, key, ledger, ledger_sha, by_run.get(run, []), roles)
                    for run, (family, key, _) in EXCLUDED.items()]
        prepared = prepared_only(ledger, ledger_sha)
        tools = protocol(guard)
        original_progress = git(CONFIG, "show", f"{REVIEWED}:{PROGRESS_REL}")
        put("verification/original-progress.json", original_progress)
        added, historical, mismatched, other = resolve_references(segment_paths, local)
        bindings = {
            "schemaVersion": 1, "batch": 131,
            "policy": "Files kept local: raw events and audits (bounded summaries published), session "
                      "rosters/status snapshots, complete external captures and community arrays, mechanical "
                      "records quoting protected source passages or the community array, writable or "
                      "oversize records, and synthetic test fixtures (aggregated by tree hash).",
            "localFiles": local, "aggregatedFixtureTrees": groups, "unboundChainFiles": unbound,
            "referencedToolsAdded": added, "historicalToolReferences": historical,
            "mismatchedReviewReferences": mismatched, "otherReferences": other,
            "ledger": {"path": "coordinator session files/b131-authoring-assignment.json", "sha256": ledger_sha},
            "boundedAuditHelper": {"path": str(BOUNDED), "sha256": sha(BOUNDED.read_bytes())},
        }
        dump("local-bindings.json", bindings)
        put(".gitattributes", b"* -text\n*.gz binary\n")
        uuids, leaks = publication_checks(guard, windows)
        provenance = {
            "schemaVersion": 1, "batch": 131, "members": MEMBERS, "base": BASE,
            "originalSourceBase": SOURCE_BASE, "initialSnapshot": INITIAL, "reviewedSnapshot": REVIEWED,
            "publication": "PENDING", "finalRuns": FINAL_RUNS, "reviewLineage": lineage,
            "excludedInitialRuns": excluded,
            "retiredUnlaunchedRuns": [{"run": "N1-B131-GPT-002", "status": ledger["reviewGpt002Status"]}],
            "preparedOnlyConfirmationRuns": prepared, "packets": packet_records, "chains": chain_records,
            "auditRoles": roles, "protocolTools": len(tools) + len(added),
            "runtimeProof": {"path": "review/revision-runtime-proof-001.json",
                             "sha256": sha(FILES["review/revision-runtime-proof-001.json"])},
            "publicationChecks": {"uuidAllowlist": sorted(ALLOWED_UUIDS), "uuidFindings": len(uuids),
                                  "externalWindowFindings": len(leaks), "protectedWindows": len(windows),
                                  "window": WINDOW, "stride": STRIDE, "minimumNonAscii": MIN_NON_ASCII},
            "representation": "Reports, prompts, receipts and review records are byte-exact. Published chain "
                              "segments are losslessly gzipped. Complete external captures, the pinned "
                              "community array and segments containing them remain local; original hashes "
                              "and ranges are preserved. Raw execution payloads remain local; audit summaries "
                              "are explicit bounded derivatives. local-bindings.json hashes every local file.",
            "independence": "Claude003 and GPT004 were fresh independent initial sessions on unchanged 1359b467 "
                            "with neutral compact packets; neither received the other's findings before both "
                            "were accepted. The author reconciled accepted findings and open questions in "
                            "signed 88a9dfab. The same sessions then confirmed using only their own family's "
                            "report, the author's response and frozen chains. Excluded Claude001/Claude002/"
                            "GPT003 material was quarantined and is not review evidence.",
            "limits": LIMITS,
        }
        provenance["recordedFileSha256"] = {name: sha(raw) for name, raw in sorted(FILES.items())}
        provenance_bytes = json_bytes(provenance)
        uuids += [{"file": "provenance.json", "uuid": u} for u in
                  sorted({m.group(0).lower() for m in UUID.finditer(provenance_bytes.decode())} - ALLOWED_UUIDS)]
        if mode == "real":
            require(not uuids and not leaks and not unbound and not mismatched,
                    "Publication checks failed; run dry mode for details")
        for count, (name, raw) in enumerate(sorted(FILES.items())):
            if count % 50 == 0:
                guard.check()
            write_frozen(out / Path(name), raw)
        write_frozen(out / "provenance.json", provenance_bytes)
        on_disk = sorted(p.relative_to(out).as_posix() for p in out.rglob("*") if p.is_file())
        require(on_disk == sorted([*FILES, "provenance.json"]), "Archive tree differs")
        sizes = {}
        for name, raw in FILES.items():
            top = name.split("/")[0]
            sizes.setdefault(top, [0, 0])
            sizes[top][0] += 1
            sizes[top][1] += len(raw)
        summary = {"mode": mode, "out": str(out), "files": len(FILES) + 1,
                   "bytes": sum(map(len, FILES.values())) + len(provenance_bytes), "byTop": sizes,
                   "provenanceSha256": sha(provenance_bytes),
                   "chains": {c["name"]: c["localOnlySegmentIndices"] for c in chain_records},
                   "localFiles": len(local), "localReasons": _count(e["reason"] for e in local),
                   "aggregatedTrees": len(groups), "unbound": len(unbound),
                   "referencedToolsAdded": added, "historicalToolReferences": len(historical),
                   "mismatchedReviewReferences": len(mismatched), "otherReferences": len(other),
                   "uuidFindings": len(uuids), "externalWindowFindings": len(leaks),
                   "protectedWindows": len(windows), "auditRoles": {k: v["role"] for k, v in roles.items()}}
        if mode == "real":
            value = progress(sha(provenance_bytes), lineage, excluded, prepared, runtime_open)
            path = REPO / Path(PROGRESS_REL)
            require(path.read_bytes() == original_progress, "Progress differs from signed blob")
            data = json_bytes(value)
            path.chmod(0o644)
            path.write_bytes(data)
            require(path.read_bytes() == data, "Progress readback differs")
            path.chmod(0o444)
            summary["progressSha256"] = sha(data)
        else:
            freeze_json(Path(str(out) + "-report.json"),
                        {**summary, "uuids": uuids, "leaks": leaks, "unboundChainFiles": unbound,
                         "mismatchedReviewReferences": mismatched, "historicalToolReferences": historical,
                         "otherReferences": other})
        print(json.dumps(summary, ensure_ascii=False, indent=1))
    finally:
        require(not guard.finish()["breach"], "B131 closure RAM breach")


def _count(values):
    result = {}
    for value in values:
        result[value] = result.get(value, 0) + 1
    return result


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: close_b131.py dry|real OUT")
    main(sys.argv[1], Path(sys.argv[2]).resolve())

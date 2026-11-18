"""Archive accepted B115 evidence; raw execution payloads and void reports stay local."""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\stop-\n1-kanji-workspace")
SCRATCH = ROOT / "scratch-115"
CONFIRM = SCRATCH / "confirm"
REPO = ROOT / "rollout-recovered" / "learning-japanese"
OUT = REPO / "docs" / "n1-reviews" / "batch-115-closure"
STATE = Path(r"C:\Users\stop-\.copilot\session-state\2451b10d-02a9-46ab-82d5-d90993f0cb8b\files\b115-freeze-result.json")
sys.path.insert(0, str(ROOT / "lean"))
import n1_closure


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    return json.loads(path.read_bytes())


def write_json(path, value):
    n1_closure.put(path, (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))


def copy(source, destination, digest=None, compress=False):
    data = Path(source).read_bytes()
    if digest is not None:
        assert sha(data) == digest, source
    stored = n1_closure.gz(data) if compress else data
    n1_closure.put(OUT / destination, stored)
    return {"sourceSha256": sha(data), "storedSha256": sha(stored),
            "sourceBytes": len(data), "storedBytes": len(stored)}


def chain(source, name):
    manifest = read_json(source)
    copy(source, f"chains/{name}/manifest.json")
    files = {}
    for segment in manifest["segments"]:
        path = Path(segment["path"])
        files[path.name + ".gz"] = copy(path, f"chains/{name}/{path.name}.gz",
                                       segment["sha256"], compress=True)
    return {"manifestSha256": sha(source.read_bytes()), "segments": len(files), "files": files}


def bounded_audit(path):
    original = read_json(path)
    assert not original["breaches"] and original["reviewerIdle"]
    fields = ("session", "eventsSha256", "eventsBytes", "eventsCount", "sliceSha256",
              "sliceBytes", "offset", "prefixSha256", "status", "breaches", "notes",
              "bootstrapVerified", "actualResponseModels", "reviewerIdle", "recordIncomplete",
              "coreRead", "coreRequired", "extensionRead", "extensionRequired", "chainRead",
              "chainRequired", "writes", "readbacks", "readbackVerified", "reportBinding", "fetches")
    result = {key: original[key] for key in fields if key in original}
    result["originalAuditSha256"] = sha(path.read_bytes())
    result["rawExecutionPayloadsRemainLocal"] = True
    result["calls"] = []
    for call in original["calls"]:
        item = {key: call[key] for key in ("id", "name", "event", "phase", "timestamp", "role", "success")
                if key in call}
        arguments = call.get("arguments", {})
        item["auditArgumentRepresentationSha256"] = sha(json.dumps(arguments, ensure_ascii=False, sort_keys=True).encode("utf-8"))
        if isinstance(arguments, dict):
            item["requestedPath"] = arguments.get("path")
            item["requestedViewRange"] = arguments.get("view_range")
            item["forceReadLargeFiles"] = arguments.get("forceReadLargeFiles")
        else:
            assert arguments == "<report write>", "Unexpected audit argument representation"
            item["argumentsRedactedInOriginalAudit"] = True
        if call["name"] == "web_fetch":
            item["url"] = call["url"]
        result["calls"].append(item)
    return result


def main():
    assert not OUT.exists(), f"Refusing to overwrite {OUT}"
    state = read_json(STATE)
    initial = [
        ("initial-claude", state["claude004"], SCRATCH / "N1-B115-CLAUDE-004-final-adjudication.json"),
        ("initial-gpt", state["gpt"], SCRATCH / "N1-B115-GPT-001-final-adjudication.json"),
    ]
    confirmations = [
        ("confirm-claude-002", "N1-B115-CLAUDE-CONFIRM-002", "claude-115-002"),
        ("confirm-gpt", "N1-B115-GPT-CONFIRM-001", "gpt-115-001"),
    ]
    for _, _, path in initial:
        assert read_json(path)["reviewAccepted"]
    for _, run, _ in confirmations:
        assert read_json(CONFIRM / f"{run}-final-adjudication.json")["reviewAccepted"]
    packet = ROOT / "review-packets" / "batch-115-f36cd819"
    packet_metadata, raw_manifest = n1_closure.load_initial_packet(packet)
    assert sha(raw_manifest) == "36931780d7bc4c416b697686453d910a9b7972ec62028531f52f19129d445542"
    OUT.mkdir(parents=True)
    n1_closure.put(OUT / ".gitattributes", b"* -text\n*.gz binary\n")
    n1_closure.record_flat_packet(packet, OUT / "packet", packet_metadata["files"], raw_manifest)
    n1_closure.record_confirm(OUT, [
        f"claude={ROOT / 'review-packets' / 'confirm-115-206f9893-claude'}",
        f"gpt={ROOT / 'review-packets' / 'confirm-115-206f9893-gpt'}",
    ])
    confirm_provenance_path = OUT / "confirm-packet" / "provenance.json"
    confirm_provenance = read_json(confirm_provenance_path)
    confirm_provenance["note"] = (
        "Identical non-snapshot files are stored under common/. Snapshot hashes describe captured "
        "checkout bytes, which may use CRLF; snapshotBlobs separately identifies Git blobs. These "
        "representations are not claimed byte-equal. All delivered snapshot text also appears in the "
        "hashed source chains. The original packet manifests remain byte-exact."
    )
    write_json(confirm_provenance_path, confirm_provenance)
    chains = {"core": chain(SCRATCH / "core-chain.json", "core")}
    runs = []
    for label, info, adjudication_path in initial:
        adjudication = read_json(adjudication_path)
        run = adjudication["run"]
        raw = adjudication["originalReport"]
        accepted = adjudication["acceptedDerivative"]
        copy(raw["path"], f"reports/{label}-raw.md", raw["sha256"])
        copy(accepted["path"], f"reports/{label}-coordinator-normalized.md", accepted["sha256"])
        copy(info["prompt"], f"prompts/{label}.txt", info["promptSha256"])
        copy(info["kickoff"], f"prompts/{label}-kickoff.txt", info["kickoffSha256"])
        for field in ("auditConfig", "preflight", "phase1List", "phase1Adjudication", "phase2Message", "preDeliveryReceipt"):
            copy(info[field], f"protocol/{label}/{Path(info[field]).name}")
        for suffix in ("final-adjudication.json", "source-claims.json", "normalization.json",
                       "normalization.diff", "report-structure.json", "normalized-report-structure.json"):
            copy(SCRATCH / f"{run}-{suffix}", f"adjudications/{run}-{suffix}")
        audit_path = Path(adjudication["mechanicalAudit"]["path"])
        assert sha(audit_path.read_bytes()) == adjudication["mechanicalAudit"]["sha256"]
        audit = bounded_audit(audit_path)
        write_json(OUT / "audits" / f"{label}.json", audit)
        chains[label + "-extension"] = chain(Path(info["extensionManifest"]), label + "-extension")
        runs.append({"label": label, "run": run, "snapshot": adjudication["candidate"],
                     "actualModels": audit["actualResponseModels"],
                     "toolWindow": [audit["calls"][0]["timestamp"], audit["calls"][-1]["timestamp"]],
                     "calls": len(audit["calls"]), "fetches": audit["fetches"],
                     "rawReportSha256": raw["sha256"], "acceptedReportSha256": accepted["sha256"],
                     "originalStructureStatus": "FAIL", "acceptedStructureStatus": "PASS"})
    for label, run, suffix in confirmations:
        adjudication_path = CONFIRM / f"{run}-final-adjudication.json"
        adjudication = read_json(adjudication_path)
        copy(adjudication["report"], f"reports/{label}.md", adjudication["reportSha256"])
        for name in ("final-adjudication.json", "source-claims.json", "report-structure.json"):
            copy(CONFIRM / f"{run}-{name}", f"adjudications/{run}-{name}")
        copy(CONFIRM / "prompts" / f"confirm-{suffix}.txt", f"prompts/{label}.txt")
        copy(CONFIRM / "prompts" / f"kickoff-{suffix}.txt", f"prompts/{label}-kickoff.txt")
        copy(CONFIRM / "prompts" / f"audit-config-{run}.json", f"protocol/{label}/audit-config.json")
        copy(CONFIRM / f"predelivery-{run}.json", f"protocol/{label}/predelivery.json")
        audit_path = Path(adjudication["audit"])
        assert sha(audit_path.read_bytes()) == adjudication["auditSha256"]
        audit = bounded_audit(audit_path)
        write_json(OUT / "audits" / f"{label}.json", audit)
        family = "claude" if label.startswith("confirm-claude") else "gpt"
        chains[label] = chain(CONFIRM / f"{family}-chain.json", label)
        runs.append({"label": label, "run": run, "snapshot": adjudication["candidate"],
                     "actualModels": audit["actualResponseModels"],
                     "toolWindow": [audit["calls"][0]["timestamp"], audit["calls"][-1]["timestamp"]],
                     "calls": len(audit["calls"]), "fetches": audit["fetches"],
                     "acceptedReportSha256": adjudication["reportSha256"],
                     "acceptedWithLocatorErrors": family == "claude", "reportUnchanged": True})
    copy(CONFIRM / "N1-B115-CLAUDE-CONFIRM-002-claim-hold.json", "adjudications/claude-confirm-002-historical-hold.json")
    for name in ("confirm-002-fabricated-tests.txt", "confirm-002-prompt.diff"):
        copy(CONFIRM / name, f"protocol/{name}")
    for name in ("authoring-inventory.json", "design.json", "source-inspection.json",
                 "comparison-inspection.json", "selection.json", "evidence-index.json"):
        copy(SCRATCH / name, f"author-evidence/{name}")
    for folder in ("checks-r1", "checks-prepublication-206f9893"):
        for path in (SCRATCH / folder).rglob("*"):
            if path.is_file():
                copy(path, f"gates/{folder}/{path.relative_to(SCRATCH / folder).as_posix()}")
    for name in ("lint-frozen-f36cd819.txt", "lint-fix-206f9893.txt", "lint-warning-basis.txt",
                 "quiz-safety-r1.txt", "linkplan-r1.txt", "reading-exposure-r1.txt", "reading-options-r1.txt"):
        copy(SCRATCH / name, f"gates/{name}")
    for name in ("audit-review-v2.py", "check-report-structure.py", "review_chain.py",
                 "test-review-audit-v3.py", "test-review-audit-v3.txt",
                 "test-report-structure.py", "test-report-structure.txt",
                 "normalize-claude-004-report.py", "normalize-gpt-001-report.py"):
        copy(SCRATCH / name, f"protocol/initial-tools/{name}")
    for name in ("audit-confirm.py", "test-audit-confirm.py", "check-confirm-structure.py",
                 "test-confirm-structure.py", "prepare-claude-confirm-002.py"):
        copy(CONFIRM / name, f"protocol/confirmation-tools/{name}")
    quarantine = []
    classifications = [
        ("N1-B115-CLAUDE-001", "VOID", SCRATCH / "N1-B115-CLAUDE-001-final-adjudication.json"),
        ("N1-B115-CLAUDE-002", "VOID", SCRATCH / "N1-B115-CLAUDE-002-final-adjudication.json"),
        ("N1-B115-CLAUDE-003", "UNACCEPTED", SCRATCH / "N1-B115-CLAUDE-003-report-contract-hold.json"),
        ("N1-B115-CLAUDE-CONFIRM-001", "VOID", CONFIRM / "N1-B115-CLAUDE-CONFIRM-001-final-adjudication.json"),
    ]
    for run, classification, path in classifications:
        quarantine.append({"run": run, "classification": classification,
                           "localClassificationArtifactSha256": sha(path.read_bytes()),
                           "reportOrObservationsIncluded": False, "observationsUsed": False})
    write_json(OUT / "quarantine.json", quarantine)
    provenance = {
        "schemaVersion": 2, "batch": 115, "members": state["members"],
        "base": state["base"], "initialSnapshot": state["freeze"],
        "reviewedSnapshot": state["reconciliation"]["commit"], "publication": "PENDING",
        "runsInChronologicalOrder": runs, "chains": chains,
        "initialPacketChecksumManifestSha256": sha(raw_manifest),
        "representation": "Raw reports, prompts, source manifests and adjudications are byte-exact. Gzip mtime is zero. Source chains preserve original uncompressed hashes. Audit summaries are explicit bounded derivatives; original audit and event hashes identify local originals.",
        "excluded": ["Raw execution payloads", "Void or unaccepted reports and observations", "B113 void material"],
        "recordedFileSha256": {p.relative_to(OUT).as_posix(): sha(p.read_bytes())
                              for p in sorted(OUT.rglob("*")) if p.is_file()},
        "hashScope": "All assembled evidence files; excludes this provenance object and the subsequently authored README.",
    }
    write_json(OUT / "provenance.json", provenance)
    for name, digest in provenance["recordedFileSha256"].items():
        assert sha((OUT / name).read_bytes()) == digest, name
    for value in chains.values():
        assert value["segments"] == len(value["files"])
    print(json.dumps({"closure": str(OUT), "files": len(provenance["recordedFileSha256"]) + 1,
                      "provenanceSha256": sha((OUT / "provenance.json").read_bytes()),
                      "runs": runs}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    specification = importlib.util.spec_from_file_location("closure_ram_guard", CONFIRM / "ram-guard" / "verify-zip-streaming.py")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    assert module.available_ram() > 2 * 1024 ** 3
    guard = module.RamGuard()
    guard.start()
    try:
        main()
        guard.check()
    finally:
        memory = guard.finish()
        write_json(SCRATCH / "closure-build-memory.json", memory)
        assert memory["breach"] is None

"""Archive B126's two CLEAN initials without inventing correction or confirmation runs."""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from archive_b124_chains_v2 import prepare as prepare_chain
from common import (TOOLS, WS, freeze_json, frozen, json_bytes, load_batch, load_module,
                    require, sha, start_guard, verify_packet, write_frozen)
from scoped_admission import assess_status
from verify_b124_archive_v2 import verify_chain

CANDIDATE = "246a1319ef30414d73e4518b52ae99c1d700c57e"
BASE = "ea9e1e364da4f3421a05d2a9706e5dcf44f0d797"
MEMBER = "\u5098"
SIGNER = "D4C9A275A218AF747B787AFA9D94B9D311BD26A7"
REVIEW = WS / "scratch-126" / "review"
REPO = WS / "b126-worktree"
OUT = REPO / "docs" / "n1-reviews" / "batch-126-closure"
GIT_HELPER = REPO / "docs" / "n1-sources" / "batch-126" / "producers" / "b126_common.py"
GIT_HELPER_SHA = "7e968e53af0e3c0cb12463067ea64bb575fa81c805f8ce9da1220ef9f1cd5483"
ASSEMBLER = WS / "scratch-115" / "assemble-closure.py"
ASSEMBLER_SHA = "32f5b353bf7c1030dd494074ed0598c3594b438a752cee9aabb6448a73ce0a6a"
PINS = {
    "common.py": "9e181d1ae59b786e691d8efce453c3f9a4a3f61765b46b5a29a868dfaeacde1d",
    "archive_b124_chains_v2.py": "ab34fc350a5062af5c3ee3b6e6041d28da13819a9ab67d908f4137f3df0558d6",
    "verify_b124_archive_v2.py": "5a782206eef96c614383fccd42d614d04e6af3e3492b4450663d246993b5f6f2",
    "scoped_admission.py": "e40e5107ef31e3040c0b212786dbce0f680b1d718b3cdbb7bb9a086aeaea7df8",
}
RUNS = {
    "claude": ("N1-B126-CLAUDE-001", "9061f4e3-6f2e-4713-a645-d4ac9c096b44",
               "claude-opus-5-5", "cab7357d0bf6f26daa800304e06758e609289fc03216a70ae0214858ce524061"),
    "gpt": ("N1-B126-GPT-001", "655acc5f-64c3-4842-813e-7be830558e3e",
            "gpt-6.1-sol", "febe4e9bc5debe4c1b5a9963e3100d032e8884940d63ab2232afd69ac49b3ddc"),
}
PROOFS = {
    "coordinator-candidate-verification.json": "0d3be59a7cf6f2f95e9d5b049c608e2e9b0152aca031012a57d2892420c5f8a6",
    "source-selection-verification-001.json": "0d65e40047536eb850ae57af542206ceeb5c24560b8cfc824220419b329be9a9",
    "handoff-verification-001.json": "171f22a65f87535186a9fda1fcb7b976c2da7f3fed44b86c00f943c442cdb2fa",
}


def read(path, digest=None):
    return json.loads(frozen(path, digest))


def bound(item):
    return read(item["path"], item["sha256"])


def bounded_git(guard):
    require(sha(GIT_HELPER.read_bytes()) == GIT_HELPER_SHA, "Bounded Git helper changed")
    helper = load_module("b126_closure_git", GIT_HELPER)
    require(helper.REPO == REPO, "Git helper targets another repository")
    helper.ACTIVE_GUARD = guard
    return lambda *args: helper.git("-c", "core.quotepath=false", "-c", "core.autocrlf=false", *args)


def check_review(accepted, final, audit, context, structure, adjudication, family):
    run, session, model, _ = RUNS[family]
    require(accepted["run"] == final["run"] == adjudication["run"] == run
            and accepted["candidate"] == final["candidate"] == CANDIDATE
            and final["session"] == audit["session"] == session, "Run or snapshot identity differs")
    require(accepted["reviewAccepted"] is True
            and accepted["verdict"] == adjudication["verdict"] == structure["overall"] == "CLEAN"
            and accepted["acceptedFindings"] == adjudication["acceptedFindings"] == []
            and adjudication["openClaimIds"] == []
            and accepted["report"] == adjudication["report"], "Initial review is not closed CLEAN evidence")
    require(final["status"] == "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION"
            and not final["problems"] and audit["final"] and audit["reviewerIdle"]
            and not audit["recordIncomplete"] and not audit["breaches"]
            and not audit["unexpectedUserMessages"] and audit["fetches"] == 0
            and audit["writes"] == audit["readbacks"] == 1 and audit["readbackVerified"]
            and len(audit["messages"]) == 2 and audit["messages"][-1].strip() == "CLEAN"
            and audit["actualResponseModels"] == [model], "Execution audit failed")
    for stem in ("core", "extension"):
        require(audit[stem + "Read"] == audit[stem + "Required"] > 0, "Incomplete read chain")
    require(context["status"] == structure["status"] == "PASS" and not context["compactions"]
            and context["contextTiers"] == ["long_context"]
            and context["eventsSha256"] == audit["eventsSha256"]
            and structure["findings"] == 0
            and set(structure["facets"].values()) == {"CLEAN"}, "Context or facet evidence failed")


def check_history(provenance):
    rows = provenance["reviewLineage"]
    require(provenance["batch"] == 126 and provenance["members"] == [MEMBER]
            and provenance["base"] == BASE
            and provenance["initialSnapshot"] == provenance["reviewedSnapshot"] == CANDIDATE
            and provenance["publication"] == "PENDING"
            and not provenance["intermediateRuns"] and not provenance["excludedInitialRuns"]
            and len(rows) == 2
            and provenance["finalRuns"] == [RUNS[key][0] for key in RUNS],
            "Unexpected clean-initial closure history")
    for row, (family, (run, session, model, _)) in zip(rows, RUNS.items()):
        require(row["run"] == run and row["family"] == family and row["session"] == session
                and row["snapshot"] == CANDIDATE and row["role"] == "initial"
                and row["rawVerdict"] == "CLEAN" and row["finalAcceptance"] is True
                and row["confirmationAcceptedOnSnapshot"] is False
                and row["priorRun"] is None and row["actualModels"] == [model]
                and len(row["chains"]) == 2, "Initial evidence was substituted or relabelled")


def verify_archive():
    provenance_raw = frozen(OUT / "provenance.json")
    provenance = json.loads(provenance_raw)
    check_history(provenance)
    validation = read(OUT / "validation-provenance.json")
    require(validation["candidate"] == CANDIDATE
            and validation["reviewClosureSha256"] == sha(provenance_raw), "Validation binding differs")
    expected = {"provenance.json", "validation-provenance.json"}
    for record in (provenance, validation):
        for name, digest in record["recordedFileSha256"].items():
            frozen(OUT / name, digest)
            expected.add(name)
    actual = {path.relative_to(OUT).as_posix() for path in OUT.rglob("*") if path.is_file()}
    require(actual == expected, "Closure has missing or unlisted files")
    chains = []
    for row in provenance["reviewLineage"]:
        for binding in row["chains"]:
            directory = OUT / binding["path"]
            files = {p.relative_to(directory).as_posix(): frozen(p)
                     for p in directory.rglob("*") if p.is_file()}
            chains.append({"run": row["run"], "path": binding["path"],
                           **verify_chain(files, binding)})
    return {"status": "PASS", "batch": 126, "candidate": CANDIDATE,
            "provenanceSha256": sha(provenance_raw), "files": len(actual), "chains": chains,
            "limits": "Exact retained review/archive bytes, not native/device or publication acceptance."}


def build(snapshot):
    config = load_batch(126)
    require(config["candidate"] == CANDIDATE and config["base"] == BASE
            and config["members"] == [MEMBER] and Path(config["repo"]) == REPO, "Batch differs")
    require(not OUT.exists(), "Preserve existing closure")
    for name, digest in PINS.items():
        frozen(TOOLS / name, digest)
    frozen(ASSEMBLER, ASSEMBLER_SHA)
    audit_support = load_module("b126_bounded_audit", ASSEMBLER)
    guard, resource = start_guard("B126 clean-initial closure")
    try:
        git = bounded_git(guard)
        require(git("rev-parse", "HEAD").decode().strip() == CANDIDATE
                and not git("status", "--porcelain=v1", "--untracked-files=all"), "Candidate changed")
        require(git("show", "-s", "--format=%P", CANDIDATE).decode().strip() == BASE
                and git("show", "-s", "--format=%G?|%GF|%ae|%ce", CANDIDATE).decode().strip()
                == f"G|{SIGNER}|stop-cran@list.ru|stop-cran@list.ru", "Owner signature or parent differs")
        age = datetime.now(timezone.utc).timestamp() - snapshot.stat().st_mtime
        require(0 <= age < 180, "Admission snapshot is stale")
        status_raw = snapshot.read_bytes()
        assessment = assess_status(json.loads(status_raw), "B126 closure writer", resource.available_ram())
        require(assessment["statusAllowsAdmission"], "A scoped writer/reviewer is still active")
        contents, lineage, audits, launches = {}, [], {}, {}

        def put(name, raw):
            require(not name.endswith(".jsonl") and ".." not in name.split("/")
                    and name not in contents, "Unsafe or duplicate archive path")
            contents[name] = raw
            return {"path": name, "sha256": sha(raw)}

        def copy(path, name, digest=None):
            return put(name, frozen(path, digest))

        def binding(item, name):
            return copy(Path(item["path"]), name, item["sha256"])

        def chain(path, prefix):
            raw = frozen(path)
            manifest = json.loads(raw)
            files, retention = prepare_chain(raw, {
                s["path"]: frozen(s["path"], s["sha256"]) for s in manifest["segments"]})
            result = {"path": prefix, "manifestSha256": sha(raw), "segments": len(manifest["segments"]),
                      "retentionSha256": sha(files["retention.json"]),
                      "archivedSegmentIndices": retention["archivedSegmentIndices"],
                      "localOnlySegmentIndices": [s["index"] for s in retention["localOnlySegments"]]}
            verify_chain(files, result)
            for name, data in files.items():
                put(f"{prefix}/{name}", data)
            return result

        packet, _, _ = verify_packet(config, guard)
        copy(packet / "SHA256SUMS.json", "packet/SHA256SUMS.json")
        copy(packet / "packet.json", "packet/packet.json")
        preflight = read(REVIEW / "prompts" / "preflight.json")
        for family, (run, session, _, digest) in RUNS.items():
            accepted = read(REVIEW / f"{run}-acceptance.json", digest)
            final = bound(accepted["final"])
            audit = bound(final["finalAudit"])
            context, structure = bound(final["context"]), bound(final["structure"])
            adjudication = bound(accepted["adjudication"])
            check_review(accepted, final, audit, context, structure, adjudication, family)
            prefix = f"runs/{run}"
            report = binding(accepted["report"], f"{prefix}/report.md")
            copy(REVIEW / f"{run}-acceptance.json", f"{prefix}/acceptance.json", digest)
            for field in ("final", "adjudication"):
                binding(accepted[field], f"{prefix}/{field}.json")
            for field in ("context", "structure", "evidenceCheck"):
                binding(final[field], f"{prefix}/{field}.json")
            put(f"{prefix}/audit-summary.json", json_bytes(audit_support.bounded_audit(Path(final["finalAudit"]["path"]))))
            for suffix in ("phase1", "launch", "admission"):
                copy(REVIEW / f"{run}-{suffix}.json", f"{prefix}/{suffix}.json")
            phase = read(REVIEW / f"{run}-phase1.json")
            frozen(Path(phase["auditDir"]) / "audit.json", phase["auditSha256"])
            final_events = frozen(Path(context["events"]), audit["eventsSha256"])
            prior_events = frozen(Path(phase["auditDir"]) / "events.jsonl", phase["eventsSha256"])
            require(final_events.startswith(prior_events), "Final execution changed the phase-one prefix")
            spec = preflight["runs"][family]
            audit_config = read(spec["auditConfig"])
            launch = read(REVIEW / f"{run}-launch.json")
            require(launch["session"] == session and spec["run"] == run
                    and audit_config["run"] == run and audit_config["maxWebFetches"] == 0
                    and launch["model"] == spec["launch"]["model"]
                    and launch["contextTier"] == "long_context", "Reviewer launch differs")
            require(accepted["preflightSha256"] == final["preflightSha256"]
                    == launch["preflightSha256"] == sha(frozen(REVIEW / "prompts" / "preflight.json")),
                    "Review lifecycle binds another preflight")
            bound(launch["admission"])
            for item in audit_config["files"]:
                frozen(item["path"], item["sha256"])
                guard.check()
            copy(Path(spec["auditConfig"]), f"{prefix}/config.json")
            for field in ("prompt", "kickoff"):
                copy(Path(audit_config[field]), f"{prefix}/{field}.txt")
            chains = [chain(Path(audit_config["coreManifest"]), f"{prefix}/chain"),
                      chain(REVIEW / f"{run}-extension.json", f"{prefix}/extension")]
            copy(REVIEW / f"{run}-phase2-message.txt", f"{prefix}/phase2-message.txt")
            lineage.append({"run": run, "family": family, "session": session, "snapshot": CANDIDATE,
                            "rawVerdict": "CLEAN", "role": "initial", "priorRun": None,
                            "confirmationAcceptedOnSnapshot": False, "finalAcceptance": True,
                            "report": report, "chains": chains, "actualModels": audit["actualResponseModels"],
                            "originalAuditSha256": final["finalAudit"]["sha256"],
                            "eventsSha256": audit["eventsSha256"]})
            audits[family], launches[family] = audit, launch
        last_claude = max(datetime.fromisoformat(c["timestamp"]) for c in audits["claude"]["calls"])
        require(last_claude <= datetime.fromisoformat(launches["gpt"]["runtimeStartedAt"]),
                "Independent initial executions overlap")
        reconciliation = read(REVIEW / "coordinator-reconciliation-001.json")
        require(reconciliation["candidate"] == CANDIDATE and reconciliation["members"] == [MEMBER]
                and reconciliation["acceptedInitials"] == {r[0]: r[3] for r in RUNS.values()}
                and not reconciliation["remainingActionableFindings"]
                and not reconciliation["remainingConsequentialClaims"]
                and not reconciliation["teachingChanges"], "Reconciliation is not closed")
        copy(REVIEW / "coordinator-reconciliation-001.json", "reconciliation.json")
        for name, digest in PROOFS.items():
            copy(REVIEW / name, f"verification/{name}", digest)
        proof = read(REVIEW / "coordinator-candidate-verification.json", PROOFS["coordinator-candidate-verification.json"])
        require(proof["status"] == "PASS" and proof["candidate"] == CANDIDATE
                and proof["sourceMembersPublishedBeforeBatch"] == 255
                and proof["sourceMembersInCandidate"] == 256
                and proof["runtimeEntries"] == 8714
                and proof["baselineRuntimePreservedExceptRequiredWrappers"]
                and sha(git("show", f"{CANDIDATE}:manifest.json")) == proof["manifestSha256"],
                "Candidate preservation proof differs")
        for relative, item in proof["capturedGateInputs"].items():
            binding(item, f"gates/{relative}")
        for name in ("batch.json", "source-contract.json", "coordinator-tooling-readiness-001.json",
                     "audit-review.py", "check-report-structure.py", "check-run-context.py",
                     "review_chain.py", "tooling-derivation.json", "guarded-test-v2.py",
                     "test-review-chain.py", "test-review-audit.py", "test-report-structure.py"):
            copy(REVIEW / name, f"protocol/{name}")
        copy(REVIEW / "prompts" / "preflight.json", "protocol/prompts-preflight.json")
        for name in (*PINS, "step_v2.py", "prepare-chain.py", "verify_b126_sources.py",
                     "test_verify_b126_sources.py", "prepare_b126_candidate.py",
                     "test_prepare_b126_candidate.py", "close_b126.py", "test_close_b126.py"):
            copy(TOOLS / name, f"protocol/tools/{name}")
        copy(ASSEMBLER, "protocol/assemble-closure.py", ASSEMBLER_SHA)
        put("protocol/b126_common.py", GIT_HELPER.read_bytes())
        execution = []
        for directory in sorted(REVIEW.iterdir()):
            receipt = directory / "receipt.json"
            if not directory.is_dir() or not receipt.exists():
                continue
            raw, log = receipt.read_bytes(), (directory / "output.log").read_bytes()
            value = json.loads(raw)
            require(value["exitCode"] is not None
                    and value["exitCode"] == value["childExitCodeAfterCleanup"]
                    and sha(log) == value["logSha256"] and value["waitTimeoutSeconds"] == 0.1
                    and not value["memory"]["breach"], "Incomplete historical outer execution")
            put(f"verification/executions/{directory.name}/receipt.json", raw)
            if value["exitCode"] != 0 or directory.name.startswith(("test-", "closure-tests-")):
                put(f"verification/executions/{directory.name}/output.log", log)
            execution.append({"directory": directory.name, "exitCode": value["exitCode"],
                              "receiptSha256": sha(raw), "logSha256": sha(log)})
        put("verification/execution-capture.json", json_bytes({
            "completedExecutions": execution,
            "scope": "Post-execution capture, not retrospective immutability. Failed exits stay failed. "
                     "Successful outer logs, raw execution streams and full app status remain local."}))
        admission = {
            **assessment, "createdAt": datetime.now(timezone.utc).isoformat(),
            "snapshotAgeSeconds": age, "fullStatusSha256": sha(status_raw),
            "candidate": CANDIDATE, "operation": "coordinator contributor-only closure"}
        put("verification/closure-admission.json", json_bytes(admission))
        put(".gitattributes", b"* -text\n*.gz binary\n")
        progress_path = REPO / "docs" / "n1-sources" / "batch-126-progress.json"
        previous = git("show", f"{CANDIDATE}:docs/n1-sources/batch-126-progress.json")
        require(progress_path.read_bytes().replace(b"\r\n", b"\n") == previous.replace(b"\r\n", b"\n"),
                "Progress file changed")
        ledger = json.loads(previous)
        require(not ledger["published"] and not ledger["reviewClosed"] and not ledger["runtimePublished"]
                and ledger["accounting"]["publishedPendingRecordsWithCards"] == 255, "Premature delivery")
        put("verification/original-progress.json", previous)
        provenance = {"schemaVersion": 1, "batch": 126, "members": [MEMBER], "base": BASE,
                      "initialSnapshot": CANDIDATE, "reviewedSnapshot": CANDIDATE, "publication": "PENDING",
                      "finalRuns": [r[0] for r in RUNS.values()], "intermediateRuns": [],
                      "excludedInitialRuns": [], "reviewLineage": lineage,
                      "representation": "Byte-exact reports and audit bindings. Safe chain segments are "
                                        "losslessly gzipped; complete external captures and entire mixed "
                                        "segments containing them remain local under explicit retention manifests.",
                      "independence": "Two serial independent model-family CLEAN initial passes on one "
                                      "unchanged signed snapshot; no corrections or confirmations were necessary.",
                      "limits": "Bounded textual/host evidence, not exhaustive or native/device acceptance.",
                      "recordedFileSha256": {name: sha(raw) for name, raw in sorted(contents.items())}}
        check_history(provenance)
        provenance_raw = json_bytes(provenance)
        ledger.update(status="textual-review-closed-publication-pending", initialSnapshot=CANDIDATE,
                      reviewedSnapshot=CANDIDATE, reviewClosed=[MEMBER])
        ledger["accounting"].update(reviewClosedPendingRecordsWithCards=256, notStarted=972,
                                    localUnreviewedDrafts=0)
        ledger["review"] = {"status": "closed-with-disclosed-limits", "finalRuns": provenance["finalRuns"],
                            "intermediateRuns": [], "excludedInitialRuns": [],
                            "closure": "../n1-reviews/batch-126-closure/provenance.json",
                            "closureProvenanceSha256": sha(provenance_raw),
                            "remainingActionableFindings": [], "remainingConsequentialClaims": [],
                            "historicalReportsPreserved": True,
                            "identity": provenance["independence"]}
        ledger["limits"] = [
            "Bounded textual/host evidence, not exhaustive linguistic or arbitrary/custom/multiple-borrow acceptance.",
            "No fresh Kotlin, native, phone, installed-APK or fallback-rendering acceptance.",
            "Claude O1 is optional; its source-line qualification and both complete reports remain preserved.",
            "Complete external captures and mixed containing segments remain local; no source rarity is inferred.",
            "Publication, CI and exact served ZIP are still pending; review closure is not delivery."]
        require(not git("status", "--porcelain=v1", "--untracked-files=all"), "Worktree changed before persistence")
        require(datetime.now(timezone.utc).timestamp() - snapshot.stat().st_mtime < 180,
                "Admission expired before persistence")
        write_frozen(REVIEW / "closure-admission-status.json", status_raw)
        freeze_json(REVIEW / "closure-admission.json", admission)
        for name, raw in contents.items():
            write_frozen(OUT / name, raw)
            guard.check()
        write_frozen(OUT / "provenance.json", provenance_raw)
        freeze_json(OUT / "validation-provenance.json", {
            "candidate": CANDIDATE, "reviewClosureSha256": sha(provenance_raw), "publication": "PENDING",
            "recordedFileSha256": {name: sha(raw) for name, raw in contents.items()
                                  if name.startswith(("verification/", "gates/"))}})
        progress_path.chmod(0o644)
        progress_path.write_bytes(json_bytes(ledger))
        require(progress_path.read_bytes() == json_bytes(ledger), "Progress readback differs")
        progress_path.chmod(0o444)
        result = verify_archive()
        freeze_json(REVIEW / "closure-verification-001.json", result)
        print(json.dumps(result))
    finally:
        require(not guard.finish()["breach"], "Closure RAM guard breached")


if __name__ == "__main__":
    require(len(sys.argv) == 3 and sys.argv[1] in ("build", "verify"), "Use build STATUS or verify NEW_OUTPUT")
    if sys.argv[1] == "build":
        build(Path(sys.argv[2]))
    else:
        print(freeze_json(Path(sys.argv[2]), verify_archive()))

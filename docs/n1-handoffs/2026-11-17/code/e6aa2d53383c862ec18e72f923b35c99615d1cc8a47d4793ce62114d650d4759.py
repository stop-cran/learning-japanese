"""Independently verify the signed integration closure, retained reviews and actual gate receipts."""
import json
import re
from pathlib import Path

import record_b130_integration_publication as publication
from b129_revision_gates import memory_ok
from b130_delta_gates import commands
from common import WS, freeze_json, frozen, git, json_bytes, load_batch, load_module, require, sha, start_guard
from verify_b129_evidence_v2 import ORDER, verify_execution
from verify_b130_archive_v2 import verify_chain
from verify_b130_integration_evidence import COMMON, IMPLEMENTATION
from verify_b130_payload import LINK_HELPER, LINK_HELPER_SHA, REPO, runtime_entries

CANDIDATE = "98f3a8160c00431a01833f48a8f7a3240b5d2fcd"
TREE = "f52c8ad530b88e733f531b9d74c853b5518df098"
PARENT = publication.ACTIVE
ROOT = WS / "scratch-130" / "review"
AUTHOR = WS / "scratch-130" / "integration-closure-001-author"
BUNDLE = AUTHOR / "handoff-001"
ENVELOPE = "7e833202c9c13ea15703b9bb69fac1b0422f30cb6325c07c6584594e7969153c"
HELPER = "da0c9f98251af255c00a85e2a36026c1fa1c6df5e578835d53518ec5ef172020"
RECORDER = "1030d51405b16ea92a620f27dcfc0a012d0c595b477737926b2b17e5ff62b2d7"
HANDOFF = "f65186065aa1573ed079f9ba6a74d9e1f7224d3599f52c8157bf659629829adc"
INVENTORY = "a42dafc9a2bde807a04205a310506407647953e0a61883512eb1b374f4c9d1cb"


def check_context(summary, admission, mode):
    head = PARENT if mode == "author" else CANDIDATE
    require(mode in ("author", "committed") and summary["status"] == "PASS"
            and summary["mode"] == admission["mode"] == mode
            and summary["head"] == admission["head"] == head
            and summary["tree"] == admission["tree"] == TREE
            and summary["parent"] == admission["parent"] == PARENT
            and summary["publishedBaseScope"] == "f237a8d590a4cb91029bc0b8485163933f44b403"
            and summary["checks"] == list(ORDER) and summary["commandsUnchanged"] is True
            and summary["serial"] is True and summary["manifestSha256"] == publication.RUNTIME["manifestSha256"]
            and summary["runnerSha256"] == ENVELOPE and summary["closureHelperSha256"] == HELPER
            and summary["gateImplementationSha256"] == IMPLEMENTATION
            and summary["commonHelperSha256"] == COMMON and set(summary["logs"]) == set(ORDER)
            and memory_ok(admission["memory"]) and memory_ok(summary["finalMemory"]),
            "Closure gate context differs")


def review_archive(config, blobs):
    presenter_path = WS / "scratch-115" / "assemble-closure.py"
    frozen(presenter_path, "32f5b353bf7c1030dd494074ed0598c3594b438a752cee9aabb6448a73ce0a6a")
    presenter = load_module("integration_closure_bounded_audit", presenter_path)
    provenance = json.loads(blobs["provenance.json"])
    require(provenance["reviewedSnapshot"] == PARENT
            and provenance["previousReviewedSnapshot"] == publication.PREVIOUS
            and provenance["parents"] == publication.PARENTS
            and provenance["runtimeCandidate"] == publication.RUNTIME
            and provenance["finalRuns"] == publication.FINAL_RUNS
            and provenance["publication"] == "PENDING" and provenance["deliveryCredit"] == 0,
            "Archived integration lineage differs")
    require(len(provenance["reviewLineage"]) == 2, "Expected two independent integration reviews")
    result = []
    for row in provenance["reviewLineage"]:
        run = row["run"]
        require(run in publication.ACCEPTANCES, "Unaccepted integration run archived")
        prefix = "runs/" + run + "/"
        accepted = json.loads(frozen(ROOT / "confirm" / f"{run}-acceptance.json",
                                     publication.ACCEPTANCES[run]))
        require(blobs[prefix + "acceptance.json"] == json_bytes(accepted)
                and row["session"] == accepted["session"] and row["family"] == accepted["family"]
                and row["snapshot"] == PARENT and row["priorSnapshot"] == publication.PREVIOUS
                and row["rawVerdict"] == "CONFIRMED" and row["rawAuditWasClean"]
                and row["controlMessageAdjudicationApplied"] is False,
                "Archived acceptance or identity differs")
        final = json.loads(blobs[prefix + "final.json"])
        for field, filename in (("report", "report.md"), ("final", "final.json"),
                                ("adjudication", "adjudication.json")):
            require(blobs[prefix + filename] == frozen(accepted[field]["path"], accepted[field]["sha256"]),
                    "Archived accepted evidence differs")
        for field in ("context", "structure"):
            require(blobs[prefix + field + ".json"] == frozen(final[field]["path"], final[field]["sha256"]),
                    "Archived context/structure differs")
        audit_path = Path(final["audit"]["path"])
        audit = json.loads(frozen(audit_path, final["audit"]["sha256"]))
        require(blobs[prefix + "audit-summary.json"] == json_bytes(presenter.bounded_audit(audit_path))
                and row["originalAuditSha256"] == final["audit"]["sha256"]
                and row["actualResponseModels"] == audit["actualResponseModels"],
                "Bounded audit differs from the accepted actual audit")
        local = json.loads(blobs[prefix + "lineage-and-local-inputs.json"])
        require(local["priorReviewedSnapshot"] == publication.PREVIOUS
                and row["priorRun"] == local["priorRun"], "Prior lineage differs")
        for item in local["priorEvidenceInPreservedClosure"].values():
            require(sha(git(config, "show", f"{CANDIDATE}:{item['repositoryPath']}")) == item["sha256"],
                    "Preserved prior evidence differs")
        for item in local["localOnly"]:
            require(item["sha256"] not in {sha(raw) for raw in blobs.values()},
                    "A full local-only input was included in the public archive")
        chain_prefix = prefix + "chain/"
        chain = {name[len(chain_prefix):]: raw for name, raw in blobs.items() if name.startswith(chain_prefix)}
        retention = json.loads(chain["retention.json"])
        chain_config = json.loads(frozen(ROOT / "confirm" / f"{run}-config.json"))
        require(chain["manifest.json"] == frozen(chain_config["chainManifest"]), "Reviewed chain changed")
        binding = {
            "manifestSha256": sha(chain["manifest.json"]), "retentionSha256": sha(chain["retention.json"]),
            "segments": retention["originalSegments"],
            "archivedSegmentIndices": retention["archivedSegmentIndices"],
            "localOnlySegmentIndices": [item["index"] for item in retention["localOnlySegments"]],
        }
        result.append({"run": run, **verify_chain(chain, binding)})
    require({item["run"] for item in result} == set(publication.FINAL_RUNS)
            and not any(name.endswith(".jsonl") for name in blobs), "Review archive scope differs")
    return result


def main():
    frozen(Path(publication.__file__), RECORDER)
    handoff = json.loads(frozen(BUNDLE / "handoff.json", HANDOFF))
    inventory = json.loads(frozen(BUNDLE / "evidence-inventory.json", INVENTORY))
    config = load_batch(130)
    config["reviewDir"] = str(ROOT)
    frozen(LINK_HELPER, LINK_HELPER_SHA)
    receipts_helper = load_module("integration_closure_gate_bindings", LINK_HELPER)
    guard, _ = start_guard("B130 signed integration closure verification")
    try:
        require(inventory["selfExcluded"] and
                {p.relative_to(BUNDLE).as_posix() for p in BUNDLE.rglob("*") if p.is_file()}
                == set(inventory["files"]) | {"evidence-inventory.json"}, "Handoff inventory incomplete")
        for name, digest in inventory["files"].items():
            path = BUNDLE / name
            require(path.resolve().is_relative_to(BUNDLE), "Bundle path escapes")
            frozen(path, digest)
            if name.startswith("evidence/"):
                require(sha((AUTHOR / name.removeprefix("evidence/")).read_bytes()) == digest,
                        "Original receipt differs from captured bytes")
            guard.check()
        require(handoff["candidate"] == CANDIDATE and handoff["parent"] == PARENT
                and handoff["tree"] == TREE and handoff["runtimeCandidate"] == publication.RUNTIME
                and handoff["accounting"] == {"publishedDelivered": 261, "frozenTotal": 1228,
                                             "undelivered": 967, "deliveryCredit": 0,
                                             "oldLedgerAccountingPreservedExactly": True},
                "Handoff candidate or accounting differs")
        require(git(config, "rev-parse", "HEAD").decode().strip() == CANDIDATE
                and git(config, "rev-parse", f"{CANDIDATE}^{{tree}}").decode().strip() == TREE
                and not git(config, "status", "--porcelain=v1", "--untracked-files=all"),
                "Closure checkout is not clean at the claimed commit")
        manifest_raw = git(config, "show", f"{CANDIDATE}:manifest.json")
        ledger_raw = git(config, "show", f"{CANDIDATE}:{publication.LEDGER}")
        context = publication.select_reviewed_snapshot(config, CANDIDATE, json.loads(ledger_raw), manifest_raw)
        blobs = publication.archive_blobs(config, CANDIDATE, publication.INTEGRATION_CLOSURE)
        require(len(blobs) == 133, "Unexpected integration archive size")
        chains = review_archive(config, blobs)
        changed = json.loads(frozen(BUNDLE / "new-and-changed-committed-files.json",
                                    handoff["contributorFileInventorySha256"]))
        expected = {publication.INTEGRATION_CLOSURE + "/" + name: raw for name, raw in blobs.items()}
        expected[publication.LEDGER] = ledger_raw
        actual_tree = publication.tracked_tree(config, CANDIDATE)
        require(set(changed) == set(expected), "Contributor handoff membership differs")
        for path, raw in expected.items():
            item = changed[path]
            require(actual_tree[path] == (item["mode"], item["kind"], item["blob"])
                    and sha(raw) == item["sha256"] and len(raw) == item["bytes"]
                    and frozen(BUNDLE / "contributor-files" / path) == raw == (REPO / path).read_bytes(),
                    "Contributor blob/working/bundle bytes differ")
        baseline = json.loads(frozen(WS / "scratch-130" / "integration-001-author" / "handoff-001" /
                                     "evidence/committed-preserve-001/runtime-hashes.json",
                                     "3deede7ae09f478353d93c2fbb246fa83b05aec04e4d844c18995231652e5363"))
        runtime = runtime_entries(json.loads(manifest_raw))
        require(runtime.keys() == baseline.keys() and len(runtime) == 8730, "Runtime membership differs")
        for path, (digest, binary) in runtime.items():
            raw = (REPO / path).read_bytes()
            require(sha(raw) == baseline[path]["rawSha256"]
                    and sha(raw if binary else raw.replace(b"\r\n", b"\n")) == digest
                    and digest == baseline[path]["integrated"], "Actual runtime bytes changed: " + path)
            guard.check()
        for name, digest in (("run_closure_gates.py", ENVELOPE), ("closure_common.py", HELPER),
                             ("reused/run_b130_gates.py", IMPLEMENTATION), ("reused/b130_common.py", COMMON)):
            frozen(BUNDLE / "tooling" / name, digest)
        gate_sets = {}
        warnings = json.loads(git(config, "show", f"{PARENT}:{publication.LEDGER}"))[
            "originalAuthorWarnings"]["quizSafetyWarnings"]
        for mode, attempt in (("author", "author-gates-001"), ("committed", "committed-gates-002")):
            directory = BUNDLE / "evidence" / attempt
            summary_raw = frozen(directory / "summary.json", handoff["closureGateSets"][mode]["summarySha256"])
            summary = json.loads(summary_raw)
            check_context(summary, json.loads(frozen(directory / "admission.json")), mode)
            rows = receipts_helper.gate_bindings(
                directory, config, publication.RUNTIME["manifestSha256"], IMPLEMENTATION, guard)
            receipts = {}
            for row in rows:
                name = row["gate"]
                require(summary["logs"][name] == {key: row[key] for key in ("receiptSha256", "logSha256")},
                        "Gate summary differs from actual receipt/log")
                receipt = json.loads(frozen(directory / f"{name}.json", row["receiptSha256"]))
                require(receipt["cleanupScope"] == "Own immediate child PID only." and memory_ok(receipt["memory"]),
                        "Gate cleanup/RAM differs")
                receipts[name] = receipt
            verify_execution(receipts, commands(), COMMON)
            tests = frozen(directory / "unittest.log").decode().replace("\r\n", "\n")
            require(re.search(r"Ran 431 tests in [^\n]+\n\nOK(?:\n|$)", tests), "Actual431-test output absent")
            require([line for line in frozen(directory / "quiz-safety.log").decode().splitlines()
                     if line.startswith("WARN  ")] == warnings and len(warnings) == 83,
                    "Actual retained warnings differ")
            gate_sets[mode] = {"summarySha256": sha(summary_raw), "gates": rows,
                               "started": receipts[ORDER[0]]["startedAt"],
                               "completed": receipts[ORDER[-1]]["completedAt"]}
        require(gate_sets["author"]["completed"] <= gate_sets["committed"]["started"], "Gate sets overlap")
        for attempt in ("author-preserve-002", "committed-preserve-001"):
            preserved = json.loads(frozen(BUNDLE / "evidence" / attempt / "summary.json"))
            require(preserved["tree"] == TREE and preserved["parent"] == PARENT
                    and preserved["parentTrackedEntries"] == 40297
                    and preserved["preservedOtherParentBlobsAndModes"] == 40296
                    and preserved["oldClosureFilesByteAndModePreserved"] == 1212
                    and preserved["trackedInventorySha256"] == handoff["trackedInventorySha256"]
                    and preserved["runtimeInventorySha256"] == handoff["runtimeInventorySha256"]
                    and preserved["patchSha256"] == handoff["patchSha256"],
                    "Author preservation contradicts actual signed scope")
            for filename, key in (("all-tracked-identities.json", "trackedInventorySha256"),
                                  ("runtime-hashes.json", "runtimeInventorySha256"),
                                  ("closure.patch", "patchSha256")):
                frozen(BUNDLE / "evidence" / attempt / filename, preserved[key])
        for path in (BUNDLE / "evidence").glob("*/memory.json"):
            require(memory_ok(json.loads(frozen(path))), "Other closure operation breached RAM")
        require(memory_ok(json.loads(frozen(BUNDLE / "memory.json"))), "Handoff collection breached RAM")
        signing = json.loads(frozen(BUNDLE / "evidence/signing-001/command.json"))
        require(signing["exitCode"] == 0 and not signing["timedOut"] and signing["childWaitSeconds"] == 0.1
                and signing["cleanupTimeoutSecondsPerStage"] == 10
                and sha(frozen(BUNDLE / "evidence/signing-001/stdout.log")) == signing["stdoutSha256"]
                and sha(frozen(BUNDLE / "evidence/signing-001/stderr.log")) == signing["stderrSha256"],
                "Signing execution differs")
        aborted = json.loads(frozen(BUNDLE / "committed-gates-001-observed-abort.json"))
        require(aborted["status"] == "ABORTED-NOT-A-PASS" and aborted["candidate"] == CANDIDATE
                and not (BUNDLE / "evidence/committed-gates-001/validate.json").exists()
                and not (BUNDLE / "evidence/committed-gates-001/summary.json").exists(),
                "Interrupted gate was relabelled as a success")
        require(not git(config, "status", "--porcelain=v1", "--untracked-files=all")
                and git(config, "rev-parse", "HEAD").decode().strip() == CANDIDATE,
                "Checkout changed during independent verification")
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Closure verification breached RAM")
    print(json.dumps(freeze_json(ROOT / "integration-closure-verification-001.json", {
        "status": "PASS_SIGNED_INTEGRATION_CLOSURE_ONLY", "candidate": CANDIDATE, "parent": PARENT,
        "tree": TREE, "worktreeClean": True, "context": context, "runtimeEntries": 8730,
        "unchangedOtherParentEntries": 40296, "newArchiveFiles": 133, "bundleFiles": len(inventory["files"]),
        "handoffSha256": HANDOFF, "bundleInventorySha256": INVENTORY, "gateSets": gate_sets,
        "chains": chains, "actualTestsPerGateSet": 431, "retainedWarnings": len(warnings),
        "preservedFailures": ["author-preserve-001 dependency-path failure",
                              "committed-gates-001 RAM abort with incomplete cleanup receipt"],
        "publicationRecorderSha256": RECORDER, "producerSha256": sha(frozen(Path(__file__))),
        "memory": memory, "publicationAccepted": False,
        "limits": "Exact signed contributor closure and successful unchanged receipts verified. "
                  "The earlier abort retains its observational limitation; no missing cleanup record "
                  "is inferred. No CI, served-ZIP, native/device, arbitrary-pool or whole-N1 delivery acceptance.",
    })))


if __name__ == "__main__":
    main()

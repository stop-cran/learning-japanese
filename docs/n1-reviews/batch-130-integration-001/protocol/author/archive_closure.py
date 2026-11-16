import importlib.util
import json
import stat
import sys
from pathlib import Path
from closure_common import *

sys.path.insert(0, str(TOOLS))
from archive_b129_chains import prepare
from b130_integration_lineage import require_followup_identity


def module(path):
    spec = importlib.util.spec_from_file_location("bounded_closure_audit", path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def main():
    output = HERE / "archive-001"
    require(not output.exists() and not (REPO / ARCHIVE).exists(), "Preserve existing attempt/archive")
    output.mkdir()
    guard = start_guard()
    try:
        inputs = admitted_inputs()
        require(git("rev-parse", "HEAD").decode().strip() == PARENT
                and git("rev-parse", "HEAD^@").decode().split() == PARENTS
                and not git("status", "--porcelain=v1", "--untracked-files=all"), "Starting snapshot changed")
        owner = signature(PARENT)
        previous_raw = raw(REPO / LEDGER)
        require(previous_raw == git("show", PARENT + ":" + LEDGER), "Ledger working bytes differ")
        previous = json.loads(previous_raw)
        old_provenance = frozen(REPO / OLD / "provenance.json")
        require(sha(old_provenance) == previous["review"]["closureProvenanceSha256"], "Old closure binding differs")
        files, lineage = {}, []
        audit_producer = ROOT / "scratch-115" / "assemble-closure.py"
        presenter = module(audit_producer)

        def put(name, value):
            require(name not in files and not name.endswith(".jsonl"), "Duplicate/raw archive path")
            files[name] = value if isinstance(value, bytes) else (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()

        def copy(item, name):
            put(name, frozen(Path(item["path"]), item["sha256"]))

        put(".gitattributes", b"* -text\n*.gz binary\n")
        put("original-primary-progress.json", previous_raw)
        for family, run in RUNS.items():
            path = REVIEW / "confirm" / (run + "-acceptance.json")
            accepted = json.loads(frozen(path, ACCEPTANCE[family]))
            require(accepted["candidate"] == PARENT and accepted["family"] == family
                    and accepted["run"] == run and accepted["confirmationAccepted"]
                    and accepted["reviewEvidenceAccepted"] and accepted["verdict"] == "CONFIRMED"
                    and not accepted["openClaimIds"] and not accepted["acceptedNewFindings"], "Unaccepted integration review")
            final_raw = frozen(Path(accepted["final"]["path"]), accepted["final"]["sha256"])
            final = json.loads(final_raw)
            adjudication = json.loads(frozen(Path(accepted["adjudication"]["path"]), accepted["adjudication"]["sha256"]))
            audit_path = Path(final["audit"]["path"])
            audit = json.loads(frozen(audit_path, final["audit"]["sha256"]))
            spec = load(REVIEW / "confirm" / (run + "-spec.json"))
            initial = json.loads(frozen(Path(spec["acceptance"]["path"]), spec["acceptance"]["sha256"]))
            launch = load(REVIEW / (initial["run"] + "-launch.json"))
            require_followup_identity(spec, initial, launch, REVIEW)
            prior = json.loads(frozen(Path(spec["prior"]["path"]), spec["prior"]["sha256"]))
            require(all(final[key] == accepted[key] for key in ("run", "candidate", "session", "report"))
                    and final["confirmation"] == "CONFIRMED"
                    and final["status"] == "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION"
                    and adjudication["rawAuditWasClean"] and not adjudication["controlAdjudicationApplied"]
                    and adjudication["decision"] == "ACCEPT_CONFIRMATION_ON_THIS_SNAPSHOT_ONLY",
                    "Current confirmation/audit decision differs")
            require(audit["final"] and audit["reviewerIdle"] and not audit["recordIncomplete"]
                    and not audit["breaches"] and not audit["unexpectedUserMessages"]
                    and audit["fetches"] == 0 and audit["writes"] == audit["readbacks"] == 1
                    and audit["readbackVerified"] and audit["messages"] == ["CONFIRMED"]
                    and audit["chainRead"] == audit["chainRequired"] == (10 if family == "claude" else 12),
                    "Raw current audit is not clean/complete")
            prefix = "runs/" + run
            put(prefix + "/acceptance.json", frozen(path, ACCEPTANCE[family]))
            put(prefix + "/final.json", final_raw)
            for field in ("report", "adjudication"):
                copy(accepted[field], prefix + ("/report.md" if field == "report" else "/adjudication.json"))
            for field in ("context", "structure"):
                copy(final[field], prefix + "/" + field + ".json")
            context, structure = (json.loads(files[prefix + "/" + field + ".json"]) for field in ("context", "structure"))
            require(context["status"] == structure["status"] == "PASS" and not context["compactions"]
                    and context["eventsSha256"] == audit["eventsSha256"]
                    and structure["limits"] == (6 if family == "claude" else 8), "Context/structure differs")
            copy(adjudication["citationCheck"], prefix + "/citation-check.json")
            put(prefix + "/audit-summary.json", presenter.bounded_audit(audit_path))
            config_path = REVIEW / "confirm" / (run + "-config.json")
            config = load(config_path)
            require(config["run"] == run and config["expectedFamily"] == family and config["maxWebFetches"] == 0,
                    "Wrong admitted config")
            for item in config["files"]:
                guard.check()
                frozen(Path(item["path"]), item["sha256"])
            chain_path = Path(config["chainManifest"])
            chain_raw = frozen(chain_path)
            chain = json.loads(chain_raw)
            archived, retention = prepare(chain_raw, {
                row["path"]: frozen(Path(row["path"]), row["sha256"]) for row in chain["segments"]})
            for name, value in archived.items():
                put(prefix + "/chain/" + name, value)
            prior_references = {}
            for name in ("report.md", "acceptance.json", "final.json", "adjudication.json"):
                relative = OLD + "/runs/" + prior["run"] + "/" + name
                data = frozen(REPO / relative)
                require(data == git("show", PARENT + ":" + relative), "Old predecessor artifact changed")
                if name == "report.md":
                    require(sha(data) == prior["report"]["sha256"], "Prior report differs")
                if name == "acceptance.json":
                    require(sha(data) == spec["prior"]["sha256"], "Prior acceptance differs")
                prior_references[name] = {"repositoryPath": relative, "sha256": sha(data)}
            local = [binding(REVIEW / "confirm" / (run + "-" + suffix))
                     for suffix in ("spec.json", "config.json", "preflight.json", "admission.json",
                                    "admission-status.json", "pre-delivery-events.jsonl", "prompt.txt", "kickoff.txt")]
            local += [binding(audit_path), binding(audit_path.parent / "events.jsonl")]
            put(prefix + "/lineage-and-local-inputs.json", {
                "run": run, "family": family, "reviewedSnapshot": PARENT,
                "session": accepted["session"], "originalSession": accepted["originalSession"],
                "priorRun": prior["run"], "priorReviewedSnapshot": prior["candidate"],
                "priorEvidenceInPreservedClosure": prior_references,
                "initialAcceptance": spec["acceptance"], "reviewerOrigin": spec["reviewerOrigin"],
                "sourceChain": {"manifestSha256": sha(chain_raw), "retention": retention},
                "configInputHashesVerified": config["files"], "localOnly": local,
                "rawAuditWasClean": True, "controlMessageAdjudicationApplied": False,
                "omittedInputs": "Raw events/pre-delivery logs, full session snapshots, full usage records, execution calls/messages and coordinator brief remain local. These are hash references, not published payloads.",
            })
            lineage.append({"run": run, "family": family, "session": accepted["session"],
                            "snapshot": PARENT, "priorRun": prior["run"], "priorSnapshot": prior["candidate"],
                            "reportSha256": accepted["report"]["sha256"], "rawVerdict": accepted["verdict"],
                            "actualResponseModels": audit["actualResponseModels"],
                            "originalAuditSha256": final["audit"]["sha256"],
                            "rawAuditWasClean": True, "controlMessageAdjudicationApplied": False})
        put("scope-and-lineage.md", (
            "# B130 integration-impact closure\n\n"
            "This distinct contributor-only archive records two independently accepted integration-impact "
            "confirmations on `" + PARENT + "`, not automatic transfer of prior acceptance. "
            "The normal merge has ordered parents `" + PARENTS[0] + "` and `" + PARENTS[1] + "`.\n\n"
            "Each reader continued only its own accepted report from `" + PREVIOUS + "`. The old "
            "`../batch-130-closure/` is the byte/mode-preserved referenced predecessor, not replaced or "
            "re-certified here. Original initial, excluded, prepared-only, D18/UNVERIFIED and older control "
            "adjudication histories are unchanged. Both current raw audits were clean; neither needed a "
            "control-message adjudication. Their substantive acceptance decisions are separate from audit mechanics.\n\n"
            "Reports and chain manifests preserve original bytes; permitted source-chain segments are losslessly "
            "gzipped by the existing retention helper. Each retention.json records omissions. No raw execution "
            "or pre-delivery logs, full119-session snapshots, full usage records, raw calls/messages, unrelated "
            "session data or raw coordinator briefing is published. Bounded attestations retain their hashes.\n\n"
            "The earlier integration gates/proofs in validation provenance were actually executed on the merge. "
            "The new contributor closure gates are deliberately scratch-only and are NOT claimed by this archive "
            "before execution. This separation avoids a commit/hash cycle.\n\n"
            + "\n".join("- " + item for item in LIMITS)
            + "\n\nPublished accounting remains261/1228,967 remaining; no delivery credit or publication acceptance.\n"
        ).encode())
        for path in (TOOLS / "archive_b129_chains.py", audit_producer,
                     TOOLS / "b130_integration_lineage.py", TOOLS / "accept_b130_integration_confirmation.py"):
            put("protocol/" + path.name, frozen(path))
        for name in ("closure_common.py", "archive_closure.py", "verify_closure.py", "test_closure.py",
                     "run_closure_gates.py", "sign_closure.py", "review_staged.py"):
            put("protocol/author/" + name, raw(HERE / name))
        provenance = {
            "schemaVersion": 1, "batch": 130, "reviewedSnapshot": PARENT, "parents": PARENTS,
            "previousReviewedSnapshot": PREVIOUS, "runtimeCandidate": RUNTIME,
            "finalRuns": list(RUNS.values()), "reviewLineage": lineage,
            "predecessor": {"path": OLD, "provenanceSha256": sha(old_provenance),
                            "validationProvenanceSha256": sha(frozen(REPO / OLD / "validation-provenance.json")),
                            "preservedNotRecertified": True},
            "scope": LIMITS, "publication": "PENDING", "deliveryCredit": 0,
            "recordedFileSha256": {name: sha(value) for name, value in sorted(files.items())},
        }
        validation_files = {}
        handoff = SCRATCH / "integration-001-author" / "handoff-001"
        independent = {
            "integration-runtime.json": ("integration-runtime-001/verification.json", "5a8aacbd6e0303acc9794a1689f4f329b9b4f4a556b9a91f94f24af1db31a08a"),
            "integration-evidence.json": ("integration-evidence-001.json", "ea21d87422c1af22703ae09d39c1a51747fe127db12a52293538e55a42836ffa"),
            "predecessor-signed-closure.json": ("signed-closure-verification-001/verification.json", "a86768afa7010cab36541e872a42e8d6f0ff6f3469f5a8fedb309582b91bf3da"),
        }
        for name, (source, digest) in independent.items():
            validation_files["verification/" + name] = frozen(REVIEW / source, digest)
        for directory in ("author-gates-001", "committed-gates-001", "author-preserve-001", "committed-preserve-001", "signing-001"):
            for path in sorted((handoff / "evidence" / directory).rglob("*")):
                if path.is_file():
                    if directory == "author-preserve-001" and path.name in ("tracked-blob-comparison.json", "runtime-hashes.json", "integration.patch"):
                        continue
                    validation_files["verification/integration/" + directory + "/" + path.name] = frozen(path)
        for path in (TOOLS / "verify_b130_integration_evidence.py", TOOLS / "verify_b130_integration_runtime.py"):
            validation_files["verification/producers/" + path.name] = frozen(path)
        for path in sorted((handoff / "tooling").rglob("*")):
            if path.is_file():
                validation_files["verification/producers/author/" + path.relative_to(handoff / "tooling").as_posix()] = frozen(path)
        integration_inventory = load(handoff / "evidence-inventory.json")["files"]
        for mode in ("author", "committed"):
            directory = handoff / "evidence" / (mode + "-gates-001")
            summary = load(directory / "summary.json")
            require(summary["status"] == "PASS" and len(summary["checks"]) == 10
                    and summary["manifestSha256"] == MANIFEST_SHA, "Integration gates differ")
            for name in summary["checks"]:
                receipt = load(directory / (name + ".json"))
                require(receipt["exitCode"] == 0 and not receipt["memory"]["breach"]
                        and not receipt["activeError"] and not receipt["cleanupError"], "Integration receipt failed")
                for suffix in (".log", ".json"):
                    frozen(directory / (name + suffix), integration_inventory["evidence/" + directory.name + "/" + name + suffix])
        validation_files["verification/local-input-bindings.json"] = (json.dumps({
            "inputs": inputs, "authorHandoff": binding(handoff / "handoff.json"),
            "authorBundleInventory": binding(handoff / "evidence-inventory.json"),
            "integrationInputArtifactsAlreadyVerifiedByCoordinator": True,
            "rawCoordinatorBriefAndAdmissionSnapshotsRemainLocal": True,
        }, ensure_ascii=False, indent=2) + "\n").encode()
        provenance_bytes = (json.dumps(provenance, ensure_ascii=False, indent=2) + "\n").encode()
        validation = {
            "batch": 130, "candidate": PARENT, "reviewClosureSha256": sha(provenance_bytes),
            "runtimeCandidate": RUNTIME, "publication": "PENDING",
            "gateScope": "Actual successful integration author/committed gates on37a53e75 only. New contributor-closure gates remain scratch-only, not future-execution claims.",
            "sharedProofBytes": "Author and committed full comparisons were byte-identical; committed comparison/runtime/patch bytes are archived once, with both original preservation summaries retained.",
            "recordedFileSha256": {name: sha(value) for name, value in sorted(validation_files.items())},
        }
        validation_bytes = (json.dumps(validation, ensure_ascii=False, indent=2) + "\n").encode()
        ledger = make_ledger(previous, sha(provenance_bytes), sha(validation_bytes))
        require(not files.keys() & validation_files.keys(), "Archive inventory collision")
        for name, value in {**files, **validation_files, "provenance.json": provenance_bytes,
                            "validation-provenance.json": validation_bytes}.items():
            guard.check()
            freeze(REPO / ARCHIVE / name, value)
        path = REPO / LEDGER
        attributes = {"path": LEDGER, "priorSha256": sha(previous_raw),
                      "priorReadOnly": not bool(path.stat().st_mode & stat.S_IWRITE)}
        write(output / "ledger-before.json", attributes)
        require(raw(path) == previous_raw, "Ledger changed before extension")
        if attributes["priorReadOnly"]:
            path.chmod(stat.S_IREAD | stat.S_IWRITE)
        with path.open("wb") as stream:
            stream.write((json.dumps(ledger, ensure_ascii=False, indent=2) + "\n").encode())
        path.chmod(stat.S_IREAD)
        require(load(path) == ledger and not path.stat().st_mode & stat.S_IWRITE, "Ledger extension/freeze differs")
        check_archive(guard)
        git("add", "--", ARCHIVE, LEDGER)
        write(output / "summary.json", {
            "status": "AUTHORED-STAGED-NOT-YET-GATED-OR-SIGNED", "parent": PARENT,
            "tree": git("write-tree").decode().strip(), "owner": owner,
            "provenanceSha256": sha(provenance_bytes), "validationProvenanceSha256": sha(validation_bytes),
            "newArchiveFiles": len(files) + len(validation_files) + 2,
            "priorLedger": attributes, "currentLedgerSha256": sha(raw(path)),
            "currentLedgerReadOnly": True, "inputs": inputs, "producerSha256": sha(raw(Path(__file__))),
        })
        print(json.dumps({"status": "STAGED", "archiveFiles": len(files) + len(validation_files) + 2}))
    finally:
        write(output / "memory.json", guard.finish())


if __name__ == "__main__":
    main()

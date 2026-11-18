"""Archive B127 review evidence with complete external-snapshot segments retained locally."""
import gzip
import json
import sys
from pathlib import Path

from common import (WS, freeze_json, frozen, git, load_batch, load_module, require,
                    review_dir, sha, start_guard, verify_packet, write_frozen)
from confirm_v2 import clean
from confirm_v3 import run_number
from closure_initials import archive_excluded
from close_v4 import require_historical_confirmation
from archive_b124_chains_v2 import prepare as prepare_public_chain


def read(path, expected=None):
    return json.loads(frozen(path, expected))


def require_confirmation(accepted, candidate):
    require(accepted.get("confirmationAccepted") is True
            and accepted.get("verdict") == "CONFIRMED"
            and accepted.get("openClaimIds") == []
            and accepted.get("candidate") == candidate,
            "Confirmation is not accepted on this candidate")


def require_intermediate(accepted, candidate):
    require(accepted.get("reviewEvidenceAccepted") is True
            and accepted.get("confirmationAccepted") is False
            and accepted.get("verdict") in ("CONFIRMED", "NEEDS FIX", "UNVERIFIED")
            and accepted.get("openClaimIds")
            and accepted.get("candidate") != candidate,
            "Intermediate confirmation is not adjudicated, unaccepted evidence on an earlier revision")


def archive(batch, candidate, final_runs, intermediate_runs=(), *, preflight_path,
            excluded_initials=(), confirmation_protocol=()):
    require(batch == 127, "This closure adapter is limited to B127")
    config = load_batch(batch)
    clean(config, candidate)
    records = review_dir(batch)
    out = Path(config["repo"]) / "docs" / "n1-reviews" / f"batch-{batch}-closure"
    require(not out.exists(), "Preserve the existing closure")
    require(len(final_runs) == len(set(final_runs)) == 2, "Two distinct final runs required")
    require(len(intermediate_runs) == len(set(intermediate_runs))
            and not set(intermediate_runs) & set(final_runs), "Duplicate intermediate run")
    finals = [read(records / "confirm" / f"{run}-acceptance.json") for run in final_runs]
    for accepted in finals:
        require_confirmation(accepted, candidate)
    require({item["family"] for item in finals} == {"claude", "gpt"}, "Two families required")
    require({item["run"] for item in finals} == set(final_runs), "Run mismatch")
    intermediates = sorted((read(records / "confirm" / f"{run}-acceptance.json") for run in intermediate_runs),
                           key=lambda item: run_number(batch, item["run"]))
    for accepted in intermediates:
        require_historical_confirmation(accepted, candidate)
        require(accepted["family"] in ("claude", "gpt"), "Unknown intermediate family")
        git(config, "merge-base", "--is-ancestor", accepted["candidate"], candidate)
    require({item["run"] for item in intermediates} == set(intermediate_runs), "Intermediate run mismatch")
    originals = read(preflight_path)["runs"]
    require(set(originals) == {"claude", "gpt"}, "Exactly two initial families required")
    audit_support = load_module("n1_bounded_archive", WS / "scratch-115" / "assemble-closure.py")
    contents, lineage = {}, []

    def put(name, raw):
        require(name not in contents or contents[name] == raw, f"Conflicting archive path: {name}")
        require(not name.endswith(".jsonl"), "Raw execution payloads must remain local")
        contents[name] = raw
        return {"path": name, "sha256": sha(raw)}

    def copy(path, name, expected=None):
        return put(name, frozen(path, expected))

    def binding(item, name):
        return copy(Path(item["path"]), name, item["sha256"])

    def dump(name, item):
        return put(name, (json.dumps(item, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))

    def chain(path, name):
        manifest_raw = frozen(path)
        manifest = json.loads(manifest_raw)
        files, retention = prepare_public_chain(manifest_raw, {
            segment["path"]: frozen(Path(segment["path"]), segment["sha256"])
            for segment in manifest["segments"]
        })
        for relative, raw in files.items():
            put(f"{name}/{relative}", raw)
        return {"path": name, "segments": retention["originalSegments"],
                "manifestSha256": sha(manifest_raw),
                "archivedSegmentIndices": retention["archivedSegmentIndices"],
                "localOnlySegmentIndices": [item["index"] for item in retention["localOnlySegments"]],
                "retentionSha256": sha(files["retention.json"])}

    def record(acceptance_path, family, kind="initial", previous=None):
        accepted = read(acceptance_path)
        run = accepted["run"]
        confirmation = kind != "initial"
        if kind == "final":
            require_confirmation(accepted, candidate)
        elif kind == "intermediate":
            require_historical_confirmation(accepted, candidate)
        else:
            require(accepted["reviewAccepted"] and accepted["candidate"] == config["candidate"],
                    "Initial review not accepted on the original freeze")
        mechanics = read(Path(accepted["final"]["path"]), accepted["final"]["sha256"])
        require(mechanics["status"] == "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION",
                "Mechanical final did not pass")
        require(mechanics["candidate"] == accepted["candidate"] and mechanics["run"] == run,
                "Mechanical result describes another revision or run")
        if confirmation:
            require(mechanics["confirmation"] == accepted["verdict"]
                    and mechanics["report"] == accepted["report"],
                    "Acceptance contradicts the audited confirmation")
        audit_ref = mechanics["audit" if confirmation else "finalAudit"]
        audit = read(Path(audit_ref["path"]), audit_ref["sha256"])
        require(audit["final"] and audit["reviewerIdle"] and not audit["recordIncomplete"]
                and not audit["breaches"] and not audit["unexpectedUserMessages"]
                and audit["fetches"] == 0 and audit["writes"] == audit["readbacks"] == 1
                and audit["readbackVerified"], "Execution audit failed")
        for stem in (("chain",) if confirmation else ("core", "extension")):
            require(audit[stem + "Read"] == audit[stem + "Required"], "Incomplete chain")
        context = read(Path(mechanics["context"]["path"]), mechanics["context"]["sha256"])
        structure = read(Path(mechanics["structure"]["path"]), mechanics["structure"]["sha256"])
        require(context["status"] == structure["status"] == "PASS" and not context["compactions"]
                and context["eventsSha256"] == audit["eventsSha256"], "Context/structure failed")
        prefix = f"runs/{run}"
        report = binding(accepted["report"], f"{prefix}/report.md")
        copy(acceptance_path, f"{prefix}/acceptance.json")
        binding(accepted["final"], f"{prefix}/final.json")
        binding(accepted["adjudication"], f"{prefix}/adjudication.json")
        for field in ("context", "structure"):
            binding(mechanics[field], f"{prefix}/{field}.json")
        dump(f"{prefix}/audit-summary.json", audit_support.bounded_audit(Path(audit_ref["path"])))
        if confirmation:
            spec_path = records / "confirm" / f"{run}-spec.json"
            spec = read(spec_path)
            original = read(Path(spec["acceptance"]["path"]), spec["acceptance"]["sha256"])
            require(original["run"] == originals[family]["run"], "Wrong original review")
            launch = read(records / f"{original['run']}-launch.json")
            require(spec["session"] == mechanics["session"] == launch["session"],
                    "Confirmation changed reviewer")
            prior_run = read(Path(spec["prior"]["path"]), spec["prior"]["sha256"])["run"] if "prior" in spec else None
            require(prior_run == previous, "Confirmation lineage skips or reorders a recorded run")
            config_path = records / "confirm" / f"{run}-config.json"
            copy(spec_path, f"{prefix}/spec.json")
            for suffix in ("preflight", "admission"):
                copy(records / "confirm" / f"{run}-{suffix}.json", f"{prefix}/{suffix}.json")
        else:
            require(run == originals[family]["run"], "Initial family mismatch")
            config_path = Path(originals[family]["auditConfig"])
            for suffix in ("phase1", "launch", "admission"):
                copy(records / f"{run}-{suffix}.json", f"{prefix}/{suffix}.json")
            if mechanics["evidenceCheck"]:
                binding(mechanics["evidenceCheck"], f"{prefix}/evidence-check.json")
        audit_config = read(config_path)
        require(audit_config["run"] == run and audit_config["maxWebFetches"] == 0, "Config mismatch")
        for item in audit_config["files"]:
            frozen(Path(item["path"]), item["sha256"])
        copy(config_path, f"{prefix}/config.json")
        for field in ("prompt", "kickoff"):
            copy(Path(audit_config[field]), f"{prefix}/{field}.txt")
        chains = [chain(Path(audit_config["chainManifest" if confirmation else "coreManifest"]),
                        f"{prefix}/chain")]
        if not confirmation:
            chains.append(chain(records / f"{run}-extension.json", f"{prefix}/extension"))
            copy(records / f"{run}-phase2-message.txt", f"{prefix}/phase2-message.txt")
        lineage.append({"run": run, "family": family, "session": mechanics["session"],
                        "snapshot": accepted["candidate"], "rawVerdict": accepted["verdict"],
                        "role": kind, "priorRun": previous if confirmation else None,
                        "confirmationAcceptedOnSnapshot": accepted.get("confirmationAccepted", False),
                        "finalAcceptance": kind == "final", "report": report, "chains": chains,
                        "actualModels": audit["actualResponseModels"],
                        "originalAuditSha256": audit_ref["sha256"],
                        "eventsSha256": audit["eventsSha256"]})
        return run

    guard, _ = start_guard(f"B{batch} closure")
    try:
        packet, _, _ = verify_packet(config, guard)
        copy(packet / "SHA256SUMS.json", "packet/SHA256SUMS.json")
        copy(packet / "packet.json", "packet/packet.json")
        for family in ("claude", "gpt"):
            record(records / f"{originals[family]['run']}-acceptance.json", family)
            previous = None
            for item in (item for item in intermediates if item["family"] == family):
                previous = record(records / "confirm" / f"{item['run']}-acceptance.json", family,
                                  "intermediate", previous)
            final = next(item for item in finals if item["family"] == family)
            record(records / "confirm" / f"{final['run']}-acceptance.json", family, "final", previous)
            guard.check()
        excluded = archive_excluded(excluded_initials, batch, config["candidate"],
                                    {item["run"] for item in lineage}, copy, binding, dump,
                                    chain, audit_support, records)
        copy(preflight_path, "protocol/selected-initial-preflight.json")
        for path in sorted((records / "confirm").glob("*-superseded.json")):
            copy(path, f"superseded/{path.name}")
        for name in ("audit-review.py", "check-report-structure.py", "check-run-context.py",
                     "review_chain.py", "tooling-derivation.json", "protocol-tooling-readiness-001.json"):
            copy(records / name, f"protocol/{name}")
        for name in ("audit-confirm.py", "check-confirm-structure.py", "renderer.py",
                     "tooling-preflight.json", "tooling-tests.txt", *confirmation_protocol):
            copy(records / "confirm" / name, f"protocol/confirmation/{name}")
        for name in ("common.py", "step.py", "confirm.py", "confirm_v2.py", "test_confirm.py",
                     "confirm_v3.py", "test_confirm_v3.py", "close.py", "test_close.py",
                     "close_selected.py", "closure_initials.py", "test_closure_initials.py",
                     "derive_close_selected.py", "close-selected-derivation.json",
                     "confirm_v5.py", "confirm_followup.py", "replacement_lineage.py",
                     "confirm_replacement.py", "close_v4.py", "close_selected_v2.py",
                     "derive_selected_followups.py", "selected-followups-derivation.json",
                     "test_selected_followups.py", "close_b124.py",
                     "archive_b124_chains.py", "test_archive_b124_chains.py",
                     "test_close_b124.py", "prepare_b124_closure.py",
                     "b124-closure-derivation.json", "close_b124_v2.py",
                     "archive_b124_chains_v2.py", "test_archive_b124_chains_v2.py",
                     "verify_b124_archive.py", "test_verify_b124_archive.py",
                     "verify_b124_archive_v2.py", "test_verify_b124_archive_v2.py",
                     "test_close_b124_v2.py", "prepare_b124_retention_v2.py",
                     "b124-retention-v2-derivation.json", "close_b127.py", "close_b127_v2.py", "prepare_b127_closure_inputs.py", "verify_b127_archive.py", "test_close_b127.py", "test_verify_b127_archive.py", "prepare_b127_closure_tools.py", "record_b127_confirmation_decision.py", "confirm_b127.py", "prepare_b127_confirmation_tools.py", "verify_b127_confirmation_tools.py", "run_b127_tool.py", "b127_lifecycle_process.py", "verify_b127_sources.py"):
            copy(Path(__file__).parent / name, f"protocol/tools/{name}")
        put(".gitattributes", b"* -text\n*.gz binary\n")
        provenance = {
            "schemaVersion": 1, "batch": batch, "members": config["members"], "base": config["base"],
            "initialSnapshot": config["candidate"], "reviewedSnapshot": candidate,
            "publication": "PENDING", "finalRuns": final_runs, "intermediateRuns": list(intermediate_runs),
            "reviewLineage": lineage, "excludedInitialRuns": excluded,
            "representation": "Reports, prompts and receipts are byte-exact. Published chain "
                              "segments are losslessly gzipped. Complete external-snapshot "
                              "sections and co-located source material remain local; original "
                              "hashes and ranges are preserved. Per-chain retention.json states "
                              "the archived and local-only segments. Raw execution payloads remain "
                              "local; audit summaries are explicit bounded derivatives.",
            "independence": "Independent initials share the frozen source packet. Confirmations use "
                            "the original reviewer, its own report, the actual runtime delta and "
                            "explicitly selected author responses and source evidence. Intermediate "
                            "confirmations retain their raw verdicts and snapshot-specific acceptance; "
                            "neither accepted nor unaccepted earlier snapshots are final acceptance of this revision.",
            "limits": "Bounded textual and host evidence, not native/device or arbitrary-pool acceptance.",
            "recordedFileSha256": {name: sha(raw) for name, raw in sorted(contents.items())},
        }
        for name, raw in contents.items():
            write_frozen(out / name, raw)
            guard.check()
        result = freeze_json(out / "provenance.json", provenance)
        print(json.dumps(result))
    finally:
        memory = guard.finish()
        require(not memory["breach"], "Closure RAM guard breached")


if __name__ == "__main__":
    spec = read(Path(sys.argv[1]))
    archive(spec["batch"], spec["candidate"], spec["finalRuns"],
            tuple(spec.get("intermediateRuns", [])), preflight_path=Path(spec["preflight"]),
            excluded_initials=tuple(Path(p) for p in spec.get("excludedInitials", [])),
            confirmation_protocol=tuple(spec.get("confirmationProtocol", [])))

"""Archive B117 while preserving accepted historical snapshots and replacement identity."""
import gzip
import json
import sys
from pathlib import Path

from common import (WS, freeze_json, frozen, git, load_batch, load_module, require,
                    review_dir, sha, start_guard, verify_packet, write_frozen)
from close import read, require_confirmation, require_intermediate
from confirm_replacement import require_replacement
from confirm_v2 import clean
from confirm_v3 import run_number
from replacement_lineage import require_followup_identity
from replay_lineage import verify_replay


def require_historical_confirmation(accepted, candidate):
    if accepted.get("confirmationAccepted") is True:
        require_confirmation(accepted, accepted.get("candidate"))
        require(accepted.get("reviewEvidenceAccepted") is True
                and accepted.get("acceptedNewFindings") == []
                and accepted.get("candidate") and accepted["candidate"] != candidate,
                "Historical acceptance is not closed evidence on an earlier snapshot")
    else:
        require_intermediate(accepted, candidate)


def require_context_hold(held, mechanics, context):
    require(held["status"] == "HELD_CONTEXT_COMPACTION"
            and held["reviewEvidenceAccepted"] is False and held["confirmationAccepted"] is False
            and mechanics["status"] == "HOLD"
            and held["run"] == mechanics["run"] and held["candidate"] == mechanics["candidate"]
            and held["session"] == mechanics["session"] and held["verdict"] == mechanics["confirmation"]
            and held["report"] == mechanics["report"] and held["context"] == mechanics["context"]
            and context["status"] == "FAIL" and context["compactions"],
            "Excluded run is not the recorded context-held confirmation")


def require_identity(spec, session, original, launch, held=None, context=None, prior=None, records=None):
    require(spec["session"] == session, "Audited reviewer differs from the spec")
    if "replayedFrom" in spec:
        verify_replay(spec, load_batch(spec["batch"]), records)
        require(held is not None and held["session"] != session,
                "Fresh replay has no quarantined predecessor")
    elif "unavailable" in spec:
        require(held is not None and context is not None and prior is not None,
                "Replacement identity lacks its unavailable-context evidence")
        require_replacement(spec, original, launch, held, context, prior)
    elif "reviewerOrigin" in spec:
        require(records is not None, "Continuing replacement lacks archived records")
        require_followup_identity(spec, original, launch, records)
    else:
        require(spec["session"] == launch["session"], "Confirmation changed reviewer without provenance")


def archive(batch, candidate, final_runs, intermediate_runs=()):
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
    originals = read(records / "prompts" / "preflight.json")["runs"]
    audit_support = load_module("n1_bounded_archive", WS / "scratch-115" / "assemble-closure.py")
    contents, lineage, excluded = {}, [], []

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
        manifest = read(path)
        copy(path, f"{name}/manifest.json")
        for segment in manifest["segments"]:
            raw = frozen(Path(segment["path"]), segment["sha256"])
            packed = gzip.compress(raw, mtime=0)
            require(gzip.decompress(packed) == raw, "Chain compression mismatch")
            put(f"{name}/{Path(segment['path']).name}.gz", packed)
        return {"path": name, "segments": len(manifest["segments"]),
                "manifestSha256": sha(frozen(path))}

    def quarantine(item):
        held = read(Path(item["path"]), item["sha256"])
        mechanics = read(Path(held["final"]["path"]), held["final"]["sha256"])
        context = read(Path(held["context"]["path"]), held["context"]["sha256"])
        require_context_hold(held, mechanics, context)
        run, prefix = held["run"], f"held-runs/{held['run']}"
        binding(item, f"{prefix}/hold.json")
        for field in ("report", "final", "context", "structure"):
            binding(held[field], f"{prefix}/{field}.{'md' if field == 'report' else 'json'}")
        audit = read(Path(held["audit"]["path"]), held["audit"]["sha256"])
        require(audit["eventsSha256"] == context["eventsSha256"], "Held audit/context log differs")
        dump(f"{prefix}/audit-summary.json", audit_support.bounded_audit(Path(held["audit"]["path"])))
        for suffix in ("spec", "config", "preflight", "admission"):
            copy(records / "confirm" / f"{run}-{suffix}.json", f"{prefix}/{suffix}.json")
        audit_config = read(records / "confirm" / f"{run}-config.json")
        for entry in audit_config["files"]:
            frozen(Path(entry["path"]), entry["sha256"])
        for field in ("prompt", "kickoff"):
            copy(Path(audit_config[field]), f"{prefix}/{field}.txt")
        source_chain = chain(Path(audit_config["chainManifest"]), f"{prefix}/chain")
        excluded.append({"run": run, "family": held["family"], "session": held["session"],
                         "snapshot": held["candidate"], "rawVerdict": held["verdict"],
                         "status": held["status"], "reviewEvidenceAccepted": False,
                         "finalAcceptance": False, "chain": source_chain,
                         "eventsSha256": context["eventsSha256"]})
        return held, context

    def record(acceptance_path, family, kind="initial", previous=None):
        accepted = read(acceptance_path)
        run, confirmation = accepted["run"], kind != "initial"
        if kind == "final":
            require_confirmation(accepted, candidate)
        elif kind == "intermediate":
            require_historical_confirmation(accepted, candidate)
        else:
            require(accepted["reviewAccepted"] and accepted["candidate"] == config["candidate"],
                    "Initial review not accepted on the original freeze")
        mechanics = read(Path(accepted["final"]["path"]), accepted["final"]["sha256"])
        require(mechanics["status"] == "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION"
                and mechanics["candidate"] == accepted["candidate"] and mechanics["run"] == run,
                "Mechanical final failed or describes another revision/run")
        if confirmation:
            require(mechanics["confirmation"] == accepted["verdict"] and mechanics["report"] == accepted["report"],
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
        prefix, replacement_for = f"runs/{run}", None
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
            prior = read(Path(spec["prior"]["path"]), spec["prior"]["sha256"]) if "prior" in spec else None
            require((prior["run"] if prior else None) == previous,
                    "Confirmation lineage skips or reorders a recorded run")
            if "unavailable" in spec:
                held, held_context = quarantine(spec["unavailable"])
                require_identity(spec, mechanics["session"], original, launch, held, held_context, prior, records)
                replacement_for = held["run"]
            else:
                require_identity(spec, mechanics["session"], original, launch, records=records)
            config_path = records / "confirm" / f"{run}-config.json"
            copy(spec_path, f"{prefix}/spec.json")
            if "replayedFrom" in spec:
                binding(spec["replayedFrom"], f"{prefix}/replayed-from-spec.json")
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
                        "replacementFor": replacement_for,
                        "reviewerOrigin": spec.get("reviewerOrigin") if confirmation else None,
                        "replayedFrom": spec.get("replayedFrom") if confirmation else None,
                        "priorReviewerOrigin": spec.get("priorReviewerOrigin") if confirmation else None,
                        "finalAcceptance": kind == "final",
                        "report": report, "chains": chains, "actualModels": audit["actualResponseModels"],
                        "originalAuditSha256": audit_ref["sha256"], "eventsSha256": audit["eventsSha256"]})
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
        for path in sorted((records / "confirm").glob("*-superseded.json")):
            copy(path, f"superseded/{path.name}")
        for name in ("audit-review.py", "check-report-structure.py", "check-run-context.py",
                     "review_chain.py", "tooling-derivation.json", "coordinator-gate-tests.json"):
            copy(records / name, f"protocol/{name}")
        for name in ("audit-confirm.py", "check-confirm-structure.py", "renderer.py",
                     "tooling-preflight.json", "tooling-tests.txt", "tooling-v2-derivation.json",
                     "tooling-v2.patch", "tooling-v2-tests.txt", "tooling-v3-freeze.json",
                     "replacement-tooling-derivation.json", "replacement-tooling-tests.txt",
                     "closure-v2-derivation.json", "closure-v2-tests.txt",
                     "replacement-continuation-derivation.json", "replacement-continuation-tests.txt"):
            copy(records / "confirm" / name, f"protocol/confirmation/{name}")
        for name in ("common.py", "step.py", "confirm.py", "confirm_v2.py", "test_confirm.py",
                     "confirm_v3.py", "test_confirm_v3.py", "close.py", "test_close.py",
                     "confirm_replacement.py", "test_confirm_replacement.py", "close_v2.py", "test_close_v2.py",
                     "confirm_v4.py", "close_v3.py", "replacement_lineage.py",
                     "test_replacement_lineage.py", "derive_replacement_continuation.py",
                     "confirm_v5.py", "close_v4.py", "test_accepted_followup.py",
                     "confirm_replay.py", "close_v5.py", "replay_lineage.py", "test_replay_lineage.py"):
            copy(Path(__file__).parent / name, f"protocol/tools/{name}")
        copy(records / "confirm" / "replay-006-tooling-proof.json",
             "protocol/confirmation/replay-006-tooling-proof.json")
        put(".gitattributes", b"* -text\n*.gz binary\n")
        provenance = {
            "schemaVersion": 1, "batch": batch, "members": config["members"], "base": config["base"],
            "initialSnapshot": config["candidate"], "reviewedSnapshot": candidate,
            "publication": "PENDING", "finalRuns": final_runs, "intermediateRuns": list(intermediate_runs),
            "reviewLineage": lineage, "excludedRuns": excluded,
            "representation": "Reports, prompts and receipts are byte-exact. Complete delivered sources "
                              "are in losslessly gzipped chains. Raw execution payloads remain local; "
                              "audit summaries are explicit bounded derivatives.",
            "independence": "Independent initials share the frozen source packet. Original-reviewer "
                            "confirmations retain their identity. A replacement is explicitly attributed "
                            "to a fresh same-family reviewer re-reading reconstructed source evidence, "
                            "not retained original context. Context-held conclusions are excluded from "
                            "the replacement inputs and from acceptance, but preserved under held-runs.",
            "limits": "Bounded textual and host evidence, not native/device or arbitrary-pool acceptance.",
            "recordedFileSha256": {name: sha(raw) for name, raw in sorted(contents.items())},
        }
        for name, raw in contents.items():
            write_frozen(out / name, raw)
            guard.check()
        print(json.dumps(freeze_json(out / "provenance.json", provenance)))
    finally:
        require(not guard.finish()["breach"], "Closure RAM guard breached")


if __name__ == "__main__":
    batch, candidate, *runs = sys.argv[1:]
    archive(int(batch), candidate, [run for run in runs if not run.startswith("+")],
            tuple(run[1:] for run in runs if run.startswith("+")))

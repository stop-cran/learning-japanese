"""Archive B123 with an explicitly attributed fresh-context Claude replacement final.

Derived from close_selected_v2.py. The only identity change: a final confirmation whose
spec replays an unlaunched assignment after proven context exhaustion is verified with
b123_unavailable_context.verify_replacement and recorded as a replacement, never as the
original reviewer. All other audit, context, structure and lineage checks are unchanged.
"""
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
from b123_unavailable_context import verify_replacement

REPLACEMENT_ORIGIN = "fresh-context-replacement"
ORIGINAL = {"reviewerOrigin": "original", "replacementFor": None, "replayedFrom": None,
            "originalSession": None}


def confirmation_origin(spec, mechanics, launch, accepted, original_run, *, kind, family, batch,
                        previous, verify, load, prefix):
    """Return lineage attribution; only a proven B123 Claude final may be a fresh replacement."""
    require(spec["session"] == mechanics["session"], "Audited reviewer differs from the spec")
    if "replayedFrom" not in spec and "unavailable" not in spec:
        require(spec["session"] == launch["session"]
                and accepted.get("reviewerOrigin", "original") == "original",
                "Confirmation changed reviewer")
        return dict(ORIGINAL)
    require(kind == "final" and family == "claude" and batch == 123
            and "replayedFrom" in spec and "unavailable" in spec,
            "Only B123's final Claude confirmation may be a fresh-context replacement")
    initial_seen, prior_seen, _ = verify(spec)
    source = load(spec["replayedFrom"])
    require(initial_seen["run"] == original_run and prior_seen["run"] == previous
            and spec["session"] != launch["session"] == source["session"]
            and accepted.get("reviewerOrigin") == REPLACEMENT_ORIGIN
            and accepted.get("replacesUnavailable") == source["run"],
            "Replacement lineage, attribution or acceptance differs")
    return {"reviewerOrigin": REPLACEMENT_ORIGIN, "replacementFor": source["run"],
            "replayedFrom": f"{prefix}/replayed-from-spec.json", "originalSession": launch["session"]}


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
        manifest = read(path)
        copy(path, f"{name}/manifest.json")
        for segment in manifest["segments"]:
            raw = frozen(Path(segment["path"]), segment["sha256"])
            packed = gzip.compress(raw, mtime=0)
            require(gzip.decompress(packed) == raw, "Chain compression mismatch")
            put(f"{name}/{Path(segment['path']).name}.gz", packed)
        return {"path": name, "segments": len(manifest["segments"]),
                "manifestSha256": sha(frozen(path))}

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
        origin = dict(ORIGINAL)
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
            origin = confirmation_origin(
                spec, mechanics, launch, accepted, original["run"], kind=kind, family=family,
                batch=batch, previous=previous,
                verify=lambda item: verify_replacement(item, config, records),
                load=lambda item: read(Path(item["path"]), item["sha256"]), prefix=prefix)
            if origin["reviewerOrigin"] == REPLACEMENT_ORIGIN:
                unavailable = read(Path(spec["unavailable"]["path"]), spec["unavailable"]["sha256"])
                binding(spec["replayedFrom"], f"{prefix}/replayed-from-spec.json")
                binding(spec["unavailable"], f"{prefix}/unavailable.json")
                for key in ("context", "voidExecution", "admissionRefusal", "admissionLog"):
                    binding(unavailable[key], f"{prefix}/unavailable/{key}-{Path(unavailable[key]['path']).name}")
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
                        "eventsSha256": audit["eventsSha256"], **origin})
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
            item = read(path)
            if "archivalCopy" in item:
                binding(item["archivalCopy"], f"superseded/{Path(item['archivalCopy']['path']).name}")
        for pattern in ("*-unavailable.json", "*-context-diagnosis.json"):
            for path in sorted((records / "confirm").glob(pattern)):
                copy(path, f"superseded/{path.name}")
        for name in ("audit-review.py", "check-report-structure.py", "check-run-context.py",
                     "review_chain.py", "tooling-derivation.json", "coordinator-gate-tests.json"):
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
                     "test_selected_followups.py", "b123_unavailable_context.py",
                     "test_b123_unavailable_context.py", "prepare_b123_context_replacement.py",
                     "confirm_b123_context_replacement.py", "close_b123_v3.py",
                     "test_close_b123_v3.py"):
            copy(Path(__file__).parent / name, f"protocol/tools/{name}")
        put(".gitattributes", b"* -text\n*.gz binary\n")
        provenance = {
            "schemaVersion": 1, "batch": batch, "members": config["members"], "base": config["base"],
            "initialSnapshot": config["candidate"], "reviewedSnapshot": candidate,
            "publication": "PENDING", "finalRuns": final_runs, "intermediateRuns": list(intermediate_runs),
            "reviewLineage": lineage, "excludedInitialRuns": excluded,
            "representation": "Reports, prompts and receipts are byte-exact. Complete delivered sources "
                              "are in losslessly gzipped chains. Raw execution payloads remain local; "
                              "audit summaries are explicit bounded derivatives.",
            "independence": "Independent initials share the frozen source packet. Confirmations use "
                            "the original reviewer, its own report, the actual runtime delta and "
                            "explicitly selected author responses and source evidence, except where "
                            "reviewerOrigin is fresh-context-replacement: that same-family reviewer "
                            "received the original reviewer's attributed reports after proven context "
                            "exhaustion, and is never identified as the original. Void, unlaunched and "
                            "incomplete attempts are preserved under superseded/ and never accepted. "
                            "Intermediate confirmations retain their raw verdicts and snapshot-specific "
                            "acceptance; neither accepted nor unaccepted earlier snapshots are final "
                            "acceptance of this revision.",
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

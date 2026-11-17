"""Close the later signed snapshot without relabelling either historical002 outcome."""
import json
import re
import sys
from pathlib import Path

from b130_followup_closure_history import FINALS, PREVIOUS
from b130_followup_ledger import BASE, make_ledger
from prepare_b130_followup_ready import ledger_acceptance
from common import (CHECKS, TOOLS, freeze_json, frozen, git, json_bytes, load_batch,
                    require, sha, start_guard, write_frozen)
from confirm_b130_fresh_context import preflight
from finalize_b130 import (PROOF_SHA, ROOT, RUNTIME_SHA, SIGNER, SOURCES_SHA,
                          execution_files, read_binding)

PRIOR_PROOFS = {
    "reconciliation-001.json": ("revision-evidence-001/verification.json", PROOF_SHA),
    "runtime-proof-001.json": ("revision-runtime-proof-001.json", RUNTIME_SHA),
    "source-proof-001.json": ("revision-source-proof-001.json", SOURCES_SHA),
}


def check_proofs(candidate, proof, runtime, sources, runtime_binding, source_binding):
    require(re.fullmatch(r"[0-9a-f]{40}", candidate) and candidate != PREVIOUS,
            "Finalizer needs the new signed candidate")
    for item, status in (
        (proof, "PASS_SECOND_RECONCILIATION_BINDINGS_ONLY"),
        (runtime, "PASS_RUNTIME_ONLY"), (sources, "PASS_SOURCE_REUSE_ONLY"),
    ):
        require(item["batch"] == 130 and item["status"] == status
                and item["candidate"] == candidate and item["parent"] == PREVIOUS
                and item["base"] == BASE and item["reviewAccepted"] is False
                and item["publicationAccepted"] is False and not item["memory"]["breach"],
                "Follow-up proof or its semantic boundary differs")
    require(proof["proofs"] == {"runtime": runtime_binding, "sourceReuse": source_binding}
            and runtime["signature"] == {"fingerprint": SIGNER, "ownerVerified": True}
            and runtime["worktreeClean"] and runtime["runtimeEntries"] == 8730
            and runtime["runtimeChanged"] == ["kanji/拍.md"]
            and set(runtime["cardMetadata"]) == {"拍"}
            and runtime["cardMetadata"]["拍"]["addedGuards"] == ["響"]
            and runtime["claimResolutionAccepted"] is False
            and proof["pairBindings"]["pairCount"] == 28
            and proof["pairBindings"]["counts"] == {"guard": 8, "precaution": 17, "bounded-noncollision": 3}
            and proof["pairBindings"]["authorOpenQuizHolds"] == []
            and proof["priorEvidencePreserved"] is True
            and len(proof["retainedQuizSafetyWarnings"]) == 83,
            "Verified follow-up scope differs")
    require(sources["previousSourceProof"] == {
                "path": str(ROOT / "revision-source-proof-001.json"), "sha256": SOURCES_SHA}
            and sources["newDictionaryScanPerformed"] is False
            and sources["comparisonCardsVerified"] == 28
            and sources["previousVerifiedCounts"] == {"jmdict": 99, "kanjidic2": 31},
            "Source reuse was confused with a new complete scan")
    require(set(proof["gateSets"]) == {"author", "committed"}, "Missing host gate set")
    for gates in proof["gateSets"].values():
        require(len(gates["gates"]) == len(CHECKS)
                and {row["gate"] for row in gates["gates"]} == set(CHECKS),
                "Host gate set differs")


def check_archive(candidate, archive, provenance, provenance_raw):
    expected = {(review["run"], chain["path"])
                for review in provenance["reviewLineage"] + provenance["excludedInitialRuns"]
                for chain in review["chains"]}
    actual = [(row["run"], row["path"]) for row in archive["chains"]]
    require(archive["status"] == "PASS" and archive["candidate"] == candidate
            and archive["provenanceSha256"] == sha(provenance_raw)
            and len(actual) == len(set(actual)) and set(actual) == expected,
            "Actual, historical and excluded archive chains were not all verified")


def finalize(spec_path):
    spec_raw = frozen(spec_path)
    spec = json.loads(spec_raw)
    candidate = spec["candidate"]
    require(spec["batch"] == 130 and spec["parent"] == PREVIOUS,
            "Finalizer spec describes another lineage")
    proof_raw, proof = read_binding(spec["evidenceProof"])
    runtime_raw, runtime = read_binding(spec["runtimeProof"])
    source_raw, sources = read_binding(spec["sourceReuseProof"])
    check_proofs(candidate, proof, runtime, sources, spec["runtimeProof"], spec["sourceReuseProof"])
    prior = {name: frozen(ROOT / path, digest) for name, (path, digest) in PRIOR_PROOFS.items()}
    config = load_batch(130)
    repo = Path(config["repo"])
    closure = repo / "docs" / "n1-reviews" / "batch-130-closure"
    provenance_raw = frozen(closure / "provenance.json")
    provenance = json.loads(provenance_raw)
    archive_raw, archive = read_binding(spec["archiveVerification"])
    check_archive(candidate, archive, provenance, provenance_raw)
    finals = []
    for run in FINALS.values():
        accepted = json.loads(frozen(ROOT / "confirm" / f"{run}-acceptance.json"))
        record, _ = preflight(ROOT / "confirm" / f"{run}-preflight.json")
        finals.append(ledger_acceptance(accepted, record))
    guard, _ = start_guard("B130 follow-up closure finalization")
    try:
        require(git(config, "rev-parse", "HEAD").decode().strip() == candidate
                and git(config, "show", "-s", "--format=%P%n%G?|%GF|%ae|%ce", candidate)
                .decode().strip() == f"{PREVIOUS}\nG|{SIGNER}|stop-cran@list.ru|stop-cran@list.ru"
                and not git(config, "diff", "--name-only")
                and not git(config, "diff", "--cached", "--name-only"), "Signed candidate changed")
        untracked = git(config, "ls-files", "--others", "--exclude-standard", "-z").decode().split("\0")
        require(all(not name or name.startswith("docs/n1-reviews/batch-130-closure/")
                    for name in untracked), "Unrelated untracked paths")
        require(sha(git(config, "show", f"{candidate}:manifest.json")) == runtime["manifestSha256"],
                "Reviewed manifest differs")
        for path, digest in provenance["recordedFileSha256"].items():
            frozen(closure / path, digest)
            guard.check()
        progress = repo / "docs" / "n1-sources" / "batch-130-progress.json"
        previous = git(config, "show", f"{candidate}:docs/n1-sources/batch-130-progress.json")
        require(progress.read_bytes() == previous, "Author progress changed")
        ledger = make_ledger(json.loads(previous), config, provenance, sha(provenance_raw), runtime, finals)
        artifacts = {
            "verification/original-progress.json": previous,
            "verification/reconciliation-002.json": proof_raw,
            "verification/runtime-proof.json": runtime_raw,
            "verification/source-reuse-proof.json": source_raw,
            "verification/actual-archive.json": archive_raw,
            "verification/finalizer-spec.json": spec_raw,
            **{"verification/previous/" + name: raw for name, raw in prior.items()},
        }
        for relative, item in proof["capturedExecutionFiles"].items():
            artifacts["verification/captured/" + relative] = frozen(item["path"], item["sha256"])
        for name, item in spec["tooling"].items():
            require(Path(name).name == name and Path(name).suffix in (".json", ".py"),
                    "Only named tooling and metadata may be retained")
            artifacts["verification/tooling/" + name] = frozen(item["path"], item["sha256"])
        for name, code in spec["executions"].items():
            require(Path(name).name == name and code in (0, 1, 5), "Invalid execution record")
            for filename, raw in execution_files(ROOT / name, code).items():
                artifacts[f"verification/executions/{name}/{filename}"] = raw
        for name in ("finalize_b130_followup.py", "test_finalize_b130_followup.py",
                     "finalize_b130_followup_v2.py", "prepare_b130_followup_ready.py",
                     "test_b130_followup_ready.py"):
            artifacts["protocol/b130/" + name] = frozen(TOOLS / name)
        require(not set(artifacts) & set(provenance["recordedFileSha256"]),
                "Validation artifacts conflict with review archive")
        require(not (closure / "validation-provenance.json").exists(), "Already finalized")
        for name, raw in artifacts.items():
            write_frozen(closure / name, raw)
            guard.check()
        freeze_json(closure / "validation-provenance.json", {
            "batch": 130, "candidate": candidate, "reviewClosureSha256": sha(provenance_raw),
            "recordedFileSha256": {name: sha(raw) for name, raw in artifacts.items()},
            "publication": "PENDING",
            "acceptanceSchema": "Acceptance batch derives from each bound003 preflight; all original "
                                "acceptance bytes and the old002 snapshot outcomes remain unchanged.",
            "sourceReuse": "Previous complete-source verification reused byte-exactly, not rerun.",
        })
        require(progress.read_bytes() == previous, "Progress changed during finalization")
        progress.chmod(0o644)
        progress.write_bytes(json_bytes(ledger))
        require(progress.read_bytes() == json_bytes(ledger), "Progress readback differs")
        progress.chmod(0o444)
        print(json.dumps({"candidate": candidate, "status": ledger["status"], "published": False}))
    finally:
        require(not guard.finish()["breach"], "Closure RAM breach")


if __name__ == "__main__":
    finalize(Path(sys.argv[1]))

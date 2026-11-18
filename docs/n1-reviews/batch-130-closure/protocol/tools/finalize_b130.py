"""Finalize B130's accepted textual review; publication remains a separate gate."""
import json
import sys
from pathlib import Path

from b130_closure_ledger_v2 import BASE, PARENT, make_ledger
from b130_fresh_archive import ledger_acceptance
from common import (CHECKS, TOOLS, WS, freeze_json, frozen, git, json_bytes, load_batch,
                    require, sha, start_guard, write_frozen)
from confirm_b130_fresh_context import preflight

ROOT = WS / "scratch-130" / "review"
CANDIDATE = "d440617274eef6ea7611e60f147d6483f29ca710"
SIGNER = "D4C9A275A218AF747B787AFA9D94B9D311BD26A7"
PROOF_SHA = "3b05ee5d043bdf081ef30ec818cc46a4e16f9bacd472e5266b6a69b048871df1"
RUNTIME_SHA = "4bcc85598f49936f731fb184f16e5614d6f2bd77ff910361852abbcb9bf345a2"
SOURCES_SHA = "6b8fc5bbfc0b8a6dacff71ae5ac677e57466e3680d1db4bb125e684434aa3995"


def read_binding(item):
    raw = frozen(item["path"], item["sha256"])
    return raw, json.loads(raw)


def check_proofs(proof, runtime, sources):
    for item, status in (
        (proof, "PASS_SIGNED_RECONCILIATION_BINDINGS_ONLY"),
        (runtime, "PASS_RUNTIME_ONLY"), (sources, "PASS_COMPLETE_SOURCES_ONLY"),
    ):
        require(item["batch"] == 130 and item["status"] == status
                and item["candidate"] == CANDIDATE and item["parent"] == PARENT
                and item["base"] == BASE and item["reviewAccepted"] is False
                and item["publicationAccepted"] is False and not item["memory"]["breach"],
                "Signed mechanical proof or its semantic boundary differs")
    require(proof["proofs"]["runtime"]["sha256"] == RUNTIME_SHA
            and proof["proofs"]["sources"]["sha256"] == SOURCES_SHA
            and runtime["signature"] == {"fingerprint": SIGNER, "ownerVerified": True}
            and runtime["worktreeClean"] and runtime["runtimeEntries"] == 8730
            and runtime["claimResolutionAccepted"] is False
            and proof["changedFileCount"] == 111 and proof["originalPacketFiles"] == 307
            and proof["pairBindings"]["pairCount"] == 28
            and len(proof["retainedQuizSafetyWarnings"]) == 83
            and len(sources["results"]["jmdict"]["identities"]) == 99
            and len(sources["results"]["kanjidic2"]["identities"]) == 31,
            "Verified B130 scope differs")
    require(set(proof["gateSets"]) == {"author", "committed"}, "Missing host gate set")
    for gates in proof["gateSets"].values():
        require(len(gates["gates"]) == len(CHECKS)
                and {row["gate"] for row in gates["gates"]} == set(CHECKS),
                "Host gate set differs")


def execution_files(directory, expected_exit):
    raw = frozen(directory / "receipt.json")
    receipt = json.loads(raw)
    log = frozen(directory / "output.log")
    require(sha(log) == receipt["logSha256"]
            and receipt["exitCode"] == receipt["childExitCodeAfterCleanup"] == expected_exit
            and not receipt["cleanupError"] and not receipt["memory"]["breach"],
            "Execution receipt differs: " + directory.name)
    return {"receipt.json": raw, "output.log": log}


def check_archive(archive, provenance, provenance_raw):
    expected = {(review["run"], chain["path"])
                for review in provenance["reviewLineage"] + provenance["excludedInitialRuns"]
                for chain in review["chains"]}
    actual = [(row["run"], row["path"]) for row in archive["chains"]]
    require(archive["status"] == "PASS" and archive["candidate"] == CANDIDATE
            and archive["provenanceSha256"] == sha(provenance_raw)
            and len(actual) == len(set(actual)) and set(actual) == expected,
            "Accepted and excluded archive chains were not all verified")


def finalize(spec_path):
    spec_raw = frozen(spec_path)
    spec = json.loads(spec_raw)
    require(spec["batch"] == 130 and spec["candidate"] == CANDIDATE,
            "Finalizer spec describes another candidate")
    config = load_batch(130)
    repo = Path(config["repo"])
    closure = repo / "docs" / "n1-reviews" / "batch-130-closure"
    provenance_raw = frozen(closure / "provenance.json")
    provenance = json.loads(provenance_raw)
    proof_raw = frozen(ROOT / "revision-evidence-001" / "verification.json", PROOF_SHA)
    proof = json.loads(proof_raw)
    runtime_raw, runtime = read_binding(proof["proofs"]["runtime"])
    sources_raw, sources = read_binding(proof["proofs"]["sources"])
    check_proofs(proof, runtime, sources)
    archive_raw, archive = read_binding(spec["archiveVerification"])
    check_archive(archive, provenance, provenance_raw)
    finals = []
    for family in ("claude", "gpt"):
        run = f"N1-B130-{family.upper()}-CONFIRM-002"
        accepted = json.loads(frozen(ROOT / "confirm" / f"{run}-acceptance.json"))
        record, _ = preflight(ROOT / "confirm" / f"{run}-preflight.json")
        finals.append(ledger_acceptance(accepted, record))
    guard, _ = start_guard("B130 closure finalization")
    try:
        require(git(config, "rev-parse", "HEAD").decode().strip() == CANDIDATE
                and git(config, "show", "-s", "--format=%P%n%G?|%GF|%ae|%ce", CANDIDATE)
                .decode().strip() == f"{PARENT}\nG|{SIGNER}|stop-cran@list.ru|stop-cran@list.ru"
                and not git(config, "diff", "--name-only")
                and not git(config, "diff", "--cached", "--name-only"), "Signed candidate changed")
        untracked = git(config, "ls-files", "--others", "--exclude-standard", "-z").decode().split("\0")
        require(all(not name or name.startswith("docs/n1-reviews/batch-130-closure/")
                    for name in untracked), "Unrelated untracked paths")
        require(sha(git(config, "show", f"{CANDIDATE}:manifest.json")) == runtime["manifestSha256"],
                "Reviewed manifest differs")
        for path, digest in provenance["recordedFileSha256"].items():
            frozen(closure / path, digest)
            guard.check()
        progress = repo / "docs" / "n1-sources" / "batch-130-progress.json"
        previous = git(config, "show", f"{CANDIDATE}:docs/n1-sources/batch-130-progress.json")
        require(progress.read_bytes() == previous, "Author progress changed")
        ledger = make_ledger(json.loads(previous), config, provenance, sha(provenance_raw),
                             runtime, finals)
        artifacts = {
            "verification/original-progress.json": previous,
            "verification/reconciliation-001.json": proof_raw,
            "verification/runtime-proof.json": runtime_raw,
            "verification/source-proof.json": sources_raw,
            "verification/actual-archive.json": archive_raw,
            "verification/finalizer-spec.json": spec_raw,
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
        for name in ("finalize_b130.py", "test_finalize_b130.py"):
            artifacts["protocol/b130/" + name] = frozen(TOOLS / name)
        require(not set(artifacts) & set(provenance["recordedFileSha256"]),
                "Validation artifacts conflict with review archive")
        require(not (closure / "validation-provenance.json").exists(), "Already finalized")
        for name, raw in artifacts.items():
            write_frozen(closure / name, raw)
            guard.check()
        freeze_json(closure / "validation-provenance.json", {
            "batch": 130, "candidate": CANDIDATE, "reviewClosureSha256": sha(provenance_raw),
            "recordedFileSha256": {name: sha(raw) for name, raw in artifacts.items()},
            "publication": "PENDING",
            "acceptanceSchema": "Acceptance batch is derived from each bound fresh preflight; "
                                "the original acceptance bytes remain unchanged.",
        })
        require(progress.read_bytes() == previous, "Progress changed during finalization")
        progress.chmod(0o644)
        progress.write_bytes(json_bytes(ledger))
        require(progress.read_bytes() == json_bytes(ledger), "Progress readback differs")
        progress.chmod(0o444)
        print(json.dumps({"candidate": CANDIDATE, "status": ledger["status"], "published": False}))
    finally:
        require(not guard.finish()["breach"], "Closure RAM breach")


if __name__ == "__main__":
    finalize(Path(sys.argv[1]))

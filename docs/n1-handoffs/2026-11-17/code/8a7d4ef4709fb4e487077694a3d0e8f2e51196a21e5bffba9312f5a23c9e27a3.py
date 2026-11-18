"""Finalize B124 only from six preserved runs and two verified correction snapshots."""
import json
import sys
from pathlib import Path

from common import (CHECKS, WS, freeze_json, frozen, git, json_bytes, load_batch,
                    load_module, require, sha, start_guard, write_frozen)
from verify_b124_reconciliation import CANDIDATE as PARENT, CONTRACT_TOOL_SHA, SIGNER

INITIALS = {family: f"N1-B124-{family.upper()}-001" for family in ("claude", "gpt")}
HELD = {family: f"N1-B124-{family.upper()}-CONFIRM-001" for family in INITIALS}
FINALS = {family: f"N1-B124-{family.upper()}-CONFIRM-002" for family in INITIALS}
FIRST_PROOF_SHA = "4a2622178667f86cb0c6a80b4e1e2cedde2846d2d34511b84c828f09c24edcc0"
RUNTIME_PROOF_SHA = "d914e5e63ab5e576aae26104276b8bb7b1fad1b81656923d48b510a522594dc2"
RESPONSE_PATHS = {
    "docs/n1-sources/batch-124-reconciliation-002/claude-response-002.md",
    "docs/n1-sources/batch-124-reconciliation-002/response-correction-001.json",
}


def check_history(provenance, candidate, config):
    require(candidate != PARENT and provenance["reviewedSnapshot"] == candidate
            and provenance["initialSnapshot"] == config["candidate"]
            and provenance["base"] == config["base"] and provenance["publication"] == "PENDING"
            and provenance["members"] == config["members"] == ["\u88d5"]
            and not provenance["excludedInitialRuns"], "Closure scope or snapshot differs")
    lineage = provenance["reviewLineage"]
    require(len(lineage) == len({row["run"] for row in lineage}) == 6
            and len(provenance["finalRuns"]) == len(provenance["intermediateRuns"]) == 2
            and set(provenance["finalRuns"]) == set(FINALS.values())
            and set(provenance["intermediateRuns"]) == set(HELD.values()),
            "Expected two initials, two held confirmations and two exact-snapshot finals")
    for family in INITIALS:
        rows = [row for row in lineage if row["family"] == family]
        require([row["run"] for row in rows] == [INITIALS[family], HELD[family], FINALS[family]],
                "Reviewer lineage skips, substitutes or reorders a run")
        initial, held, final = rows
        require(initial["role"] == "initial" and initial["snapshot"] == config["candidate"]
                and initial["rawVerdict"] == "NEEDS FIX" and not initial["finalAcceptance"]
                and not initial["confirmationAcceptedOnSnapshot"]
                and initial["priorRun"] is None, "Initial evidence was relabeled")
        require(held["role"] == "intermediate" and held["snapshot"] == PARENT
                and held["rawVerdict"] == ("CONFIRMED" if family == "claude" else "UNVERIFIED")
                and held["confirmationAcceptedOnSnapshot"] is False
                and not held["finalAcceptance"] and held["priorRun"] is None,
                "Held evidence was accepted, relabeled or moved")
        require(final["role"] == "final" and final["snapshot"] == candidate
                and final["rawVerdict"] == "CONFIRMED" and final["finalAcceptance"]
                and final["confirmationAcceptedOnSnapshot"] and final["priorRun"] == held["run"]
                and final["session"] == held["session"] == initial["session"],
                "Final confirmation changed the original reviewer or exact snapshot")


def check_proofs(first, current, candidate, config):
    require(first["candidate"] == PARENT and current["parent"] == PARENT
            and current["candidate"] == candidate, "Correction lineage differs")
    for proof in (first, current):
        require(proof["status"] == "PASS" and proof["initial"] == config["candidate"]
                and proof["base"] == config["base"]
                and proof["metadataStrokesSupportAndHistoricalEvidencePreserved"]
                and proof["sourceMembersPublishedBeforeBatch"] == 253
                and proof["sourceMembersInCandidate"] == 254 and proof["runtimeEntries"] == 8710
                and proof["signature"] == {"fingerprint": SIGNER, "ownerVerified": True}
                and proof["worktreeClean"] and not proof["memory"]["breach"],
                "Mechanical proof scope, identity or accounting differs")
        require(set(proof["gateSets"]) == {"author", "committed"}, "Both gate sets are required")
        for gates in proof["gateSets"].values():
            require([item["gate"] for item in gates["gates"]] == list(CHECKS),
                    "Incomplete or reordered gate bindings")


def check_documentation(proof, candidate, runtime_proof, config):
    require(proof["status"] == "PASS" and proof["candidate"] == candidate
            and proof["parent"] == runtime_proof["candidate"]
            and proof["initial"] == config["candidate"] and proof["base"] == config["base"]
            and proof["runtimeAndPriorEvidenceUnchanged"] is True
            and proof["runtimeProofSha256"] == RUNTIME_PROOF_SHA
            and proof["manifestSha256"] == runtime_proof["manifestSha256"]
            and set(proof["signedArtifacts"]) == RESPONSE_PATHS
            and proof["signature"] == {"fingerprint": SIGNER, "ownerVerified": True}
            and proof["worktreeClean"] and not proof["memory"]["breach"],
            "Documentation-only correction lineage or preserved runtime differs")


def make_ledger(config, candidate, provenance, provenance_sha, first, current, documentation):
    return {
        "schemaVersion": 1, "batch": "124", "baseCommit": config["base"],
        "initialSnapshot": config["candidate"], "reviewedSnapshot": candidate,
        "membership": ["\u88d5"], "sourceRows": [986],
        "status": "textual-review-closed-publication-pending",
        "drafted": ["\u88d5"], "reviewClosed": ["\u88d5"], "published": [],
        "runtimePublished": False,
        "accounting": {
            "frozenPendingRecords": 1228, "publishedPendingRecordsWithCards": 253,
            "reviewClosedPendingRecordsWithCards": 254, "n2Placements": 6,
            "publishedN1Additions": 247, "undelivered": 975, "notStarted": 974,
            "overallN1TaskComplete": False,
        },
        "declaringWords": {"\u88d5": ["\u4f59\u88d5"]}, "requiredLinkPairs": 1, "newWordArticles": 0,
        "runtimeCandidate": {key: current[key] for key in
                             ("contentVersion", "manifestSha256", "runtimeEntries")},
        "review": {
            "status": "closed-with-disclosed-limits", "finalRuns": provenance["finalRuns"],
            "intermediateRuns": provenance["intermediateRuns"],
            "closure": "../n1-reviews/batch-124-closure/provenance.json",
            "closureProvenanceSha256": provenance_sha, "remainingActionableFindings": [],
            "remainingConsequentialClaims": [], "historicalReportsPreserved": True,
            "excludedInitialRuns": [],
            "identity": "Independent original Claude and GPT NEEDS FIX initials. The first Claude "
                        "CONFIRMED and GPT UNVERIFIED remain held, usable evidence, not snapshot "
                        "acceptance. Both original reviewers subsequently confirmed the second "
                        "runtime correction and its additive response-attribution successor in "
                        "isolated serial followups.",
        },
        "sourceEvidence": {
            "initial": "batch-124/source-receipt.json",
            "reconciliations": ["batch-124-reconciliation/", "batch-124-reconciliation-002/"],
            "responseCorrection": "batch-124-reconciliation-002/response-correction-001.json",
            "runtimeGateSnapshot": current["candidate"],
            "signedArtifactSha256": {**first["signedArtifacts"], **current["signedArtifacts"],
                                     **documentation["signedArtifacts"]},
        },
        "limits": [
            "Bounded textual and host review, not exhaustive linguistic or arbitrary-pool acceptance.",
            "The nine added exclusions conservatively protect broad-English choices; they do not "
            "establish universal Japanese synonymy, equal frequency or transitive exclusions.",
            "No new Kotlin, native, phone, installed-APK or fallback-rendering acceptance.",
            "Publication, CI and exact served ZIP remain pending; review closure is not delivery.",
            "Earlier reports, optional judgments, source qualifications and failed attempts are preserved.",
            "Complete external captures and mixed segments containing them remain local.",
        ],
    }


def finalize(spec_path):
    spec = json.loads(frozen(spec_path))
    candidate = spec["candidate"]
    config = load_batch(124)
    repo, records = Path(config["repo"]), WS / "scratch-124" / "review"
    closure = repo / "docs" / "n1-reviews" / "batch-124-closure"
    provenance_raw = frozen(closure / "provenance.json")
    provenance = json.loads(provenance_raw)
    first_raw = frozen(records / "coordinator-reconciliation-verification-001.json", FIRST_PROOF_SHA)
    require(spec["verification"]["sha256"] == RUNTIME_PROOF_SHA, "Unexpected runtime proof")
    current_raw = frozen(spec["verification"]["path"], RUNTIME_PROOF_SHA)
    first, current = json.loads(first_raw), json.loads(current_raw)
    doc_raw = frozen(spec["documentationVerification"]["path"], spec["documentationVerification"]["sha256"])
    documentation = json.loads(doc_raw)
    check_history(provenance, candidate, config)
    check_proofs(first, current, current["candidate"], config)
    check_documentation(documentation, candidate, current, config)
    archive_raw = frozen(spec["archiveVerification"]["path"], spec["archiveVerification"]["sha256"])
    archive = json.loads(archive_raw)
    require(archive["status"] == "PASS" and archive["candidate"] == candidate
            and archive["provenanceSha256"] == sha(provenance_raw)
            and len(archive["chains"]) == 8, "Actual six-run/eight-chain archive was not verified")
    require(git(config, "rev-parse", "HEAD").decode().strip() == candidate
            and git(config, "show", "-s", "--format=%P", candidate).decode().strip() == current["candidate"]
            and git(config, "show", "-s", "--format=%G?|%GF|%ae|%ce", candidate).decode().strip()
            == f"G|{SIGNER}|stop-cran@list.ru|stop-cran@list.ru", "Signed successor changed")
    require(not git(config, "diff", "--name-only") and not git(config, "diff", "--cached", "--name-only"),
            "Tracked revision changed")
    untracked = git(config, "ls-files", "--others", "--exclude-standard", "-z").decode("utf-8").split("\0")
    require(all(not path or path.startswith("docs/n1-reviews/batch-124-closure/") for path in untracked),
            "Unrelated untracked files")
    ledger_path = repo / "docs" / "n1-sources" / "batch-124-progress.json"
    previous = git(config, "show", f"{candidate}:docs/n1-sources/batch-124-progress.json")
    old = json.loads(previous)
    require(ledger_path.read_bytes() == previous and old["status"] == "local-authoring-candidate-unreviewed"
            and old["published"] == old["reviewClosed"] == [] and old["runtimePublished"] is False
            and old["membership"] == ["\u88d5"]
            and old["accounting"]["publishedPendingRecordsWithCards"] == 253,
            "Unexpected prior progress state")
    artifacts = {
        "verification/original-progress.json": previous,
        "verification/reconciliation-001.json": first_raw,
        "verification/reconciliation-002.json": current_raw,
        "verification/response-correction-001.json": doc_raw,
        "verification/actual-archive.json": archive_raw,
        "protocol/finalizer-spec.json": frozen(spec_path),
    }
    guard, _ = start_guard("B124 six-run closure finalization")
    try:
        for path, digest in provenance["recordedFileSha256"].items():
            frozen(closure / path, digest)
            guard.check()
        require(sha(git(config, "show", f"{candidate}:manifest.json")) == current["manifestSha256"],
                "Confirmed manifest changed")
        for proof in (first, current, documentation):
            for path, digest in proof["signedArtifacts"].items():
                require(sha(git(config, "show", f"{candidate}:{path}")) == digest,
                        f"Signed evidence changed: {path}")
                guard.check()
        contract_path = records / "prepare-source-contract.py"
        frozen(contract_path, CONTRACT_TOOL_SHA)
        contract = load_module("b124_final_gate_contract", contract_path)
        for revision, proof in enumerate((first, current), 1):
            frozen(proof["runner"]["path"], proof["runner"]["sha256"])
            for mode, gates in proof["gateSets"].items():
                directory = Path(gates["directory"])
                require(contract.gate_bindings(directory, config, proof["manifestSha256"],
                                               proof["runner"]["sha256"], guard) == gates["gates"],
                        "Archived author/committed gate evidence differs")
                prefix = f"gates/reconciliation-{revision:03}/{mode}"
                artifacts[f"{prefix}/summary.json"] = frozen(directory / "summary.json", gates["summarySha256"])
                for item in gates["gates"]:
                    name = item["gate"]
                    artifacts[f"{prefix}/{name}.json"] = frozen(directory / f"{name}.json", item["receiptSha256"])
                    artifacts[f"{prefix}/{name}.log"] = frozen(directory / f"{name}.log", item["logSha256"])
        for item in spec["supportingArtifacts"]:
            name = item["archivePath"]
            require(name.startswith(("verification/", "protocol/")) and "\\" not in name
                    and ".." not in name.split("/") and not name.endswith(".jsonl")
                    and name not in artifacts and name not in provenance["recordedFileSha256"],
                    "Unsafe or duplicate supporting archive path")
            artifacts[name] = frozen(item["path"], item["sha256"])
        for name, raw in artifacts.items():
            write_frozen(closure / name, raw)
            guard.check()
        freeze_json(closure / "validation-provenance.json", {
            "batch": 124, "candidate": candidate, "reviewClosureSha256": sha(provenance_raw),
            "recordedFileSha256": {name: sha(raw) for name, raw in artifacts.items()},
            "publication": "PENDING",
        })
        ledger = make_ledger(config, candidate, provenance, sha(provenance_raw), first, current, documentation)
        require(ledger_path.read_bytes() == previous, "Progress changed during finalization")
        ledger_path.chmod(0o644)
        ledger_path.write_bytes(json_bytes(ledger))
        require(ledger_path.read_bytes() == json_bytes(ledger), "Progress readback mismatch")
        ledger_path.chmod(0o444)
        print(json.dumps({"path": str(ledger_path), "sha256": sha(json_bytes(ledger)),
                          "status": ledger["status"], "publicationAccepted": False}))
    finally:
        require(not guard.finish()["breach"], "Finalization RAM guard breached")


if __name__ == "__main__":
    finalize(Path(sys.argv[1]))

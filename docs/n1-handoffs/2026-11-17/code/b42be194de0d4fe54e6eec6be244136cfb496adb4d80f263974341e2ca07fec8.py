"""Finalize B127's four-run closure without counting an unpublished card as delivered."""
import copy
import json
import sys
from pathlib import Path

from common import (CHECKS, TOOLS, WS, freeze_json, frozen, git, json_bytes,
                    load_batch, require, sha, start_guard, write_frozen)

SIGNER = "D4C9A275A218AF747B787AFA9D94B9D311BD26A7"
INITIALS = {family: f"N1-B127-{family.upper()}-001" for family in ("claude", "gpt")}
FINALS = {family: f"N1-B127-{family.upper()}-CONFIRM-001" for family in INITIALS}
REVIEWERS = {
    "claude": "b1e90345-f8f3-4c8d-b776-09eb8d299ba9",
    "gpt": "3d1c4b40-90b0-466d-a565-32a96db5281c",
}


def check_history(provenance, candidate, config):
    require(provenance["batch"] == 127 and provenance["reviewedSnapshot"] == candidate
            and candidate != config["candidate"]
            and provenance["initialSnapshot"] == config["candidate"]
            and provenance["base"] == config["base"]
            and provenance["members"] == config["members"] == ["\u5009"]
            and provenance["publication"] == "PENDING"
            and provenance["excludedInitialRuns"] == []
            and provenance["intermediateRuns"] == []
            and len(provenance["finalRuns"]) == 2
            and set(provenance["finalRuns"]) == set(FINALS.values()),
            "Unexpected closure scope or selected runs")
    rows = provenance["reviewLineage"]
    require(len(rows) == len({row["run"] for row in rows}) == 4,
            "Exactly two initials and two confirmations are required")
    for family in INITIALS:
        selected = [row for row in rows if row["family"] == family]
        require([row["run"] for row in selected] == [INITIALS[family], FINALS[family]],
                "Original-family lineage differs")
        initial, final = selected
        require(initial["role"] == "initial" and initial["snapshot"] == config["candidate"]
                and initial["rawVerdict"] == ("CLEAN" if family == "claude" else "NEEDS FIX")
                and initial["priorRun"] is None and not initial["finalAcceptance"]
                and not initial["confirmationAcceptedOnSnapshot"], "Initial evidence was relabeled")
        require(final["role"] == "final" and final["snapshot"] == candidate
                and final["rawVerdict"] == "CONFIRMED" and final["priorRun"] is None
                and final["finalAcceptance"] and final["confirmationAcceptedOnSnapshot"]
                and final["session"] == initial["session"] == REVIEWERS[family],
                "Final acceptance is not from the original reviewer on the exact candidate")


def check_proof(proof, candidate, config):
    require(proof["batch"] == 127 and proof["status"] == "PASS"
            and proof["candidate"] == candidate and proof["parent"] == config["candidate"]
            and proof["base"] == config["base"]
            and proof["signature"] == {"fingerprint": SIGNER, "ownerVerified": True}
            and proof["worktreeClean"] is True
            and proof["runtimeChanged"] == ["kanji/\u5009.md"]
            and proof["runtimeEntries"] == 8716
            and proof["preservedRuntimeAndHistory"] is True
            and proof["reviewAccepted"] is False and proof["confirmationAccepted"] is False
            and not proof["memory"]["breach"], "Correction verification is not applicable")
    require(set(proof["gateSets"]) == {"author", "committed"}, "Both gate sets are required")
    for mode, gates in proof["gateSets"].items():
        require(gates["head"] == (proof["parent"] if mode == "author" else candidate)
                and len(gates["gates"]) == len(CHECKS)
                and {row["gate"] for row in gates["gates"]} == set(CHECKS),
                "Incomplete gate inventory or wrong snapshot")


def make_ledger(old, config, candidate, provenance, provenance_sha, proof):
    require(old["status"] == "local-unreviewed-authoring-candidate"
            and old["membership"] == ["\u5009"] and old["sourceRows"] == [57]
            and old["reviewClosed"] == old["published"] == []
            and old["runtimePublished"] is False
            and old["accounting"]["frozenPendingRecords"] == 1228
            and old["accounting"]["publishedPendingRecordsWithCards"] == 256
            and old["accounting"]["publishedN1Additions"] == 250
            and old["accounting"]["n2Placements"] == 6
            and old["accounting"]["undelivered"] == 972,
            "Unexpected author ledger or published accounting")
    ledger = copy.deepcopy(old)
    ledger.update(initialSnapshot=config["candidate"], reviewedSnapshot=candidate,
                  status="textual-review-closed-publication-pending", reviewClosed=["\u5009"])
    ledger["accounting"].update(reviewClosedPendingRecordsWithCards=257, localUnreviewedDrafts=0,
                                notStarted=971, overallN1TaskComplete=False)
    ledger["runtimeCandidate"] = {key: proof[key] for key in
                                  ("manifestSha256", "contentVersion", "runtimeEntries")}
    ledger["review"] = {
        "status": "closed-with-disclosed-limits",
        "finalRuns": provenance["finalRuns"], "intermediateRuns": [],
        "closure": "../n1-reviews/batch-127-closure/provenance.json",
        "closureProvenanceSha256": provenance_sha,
        "remainingActionableFindings": [], "remainingConsequentialClaims": [],
        "historicalReportsPreserved": True, "excludedInitialRuns": [],
        "identity": "Independent Claude CLEAN and GPT NEEDS FIX initials remain unchanged. "
                    "Both original reviewers confirmed the signed correction in isolated serial "
                    "followups on the same exact snapshot.",
    }
    ledger["correctionSources"] = ["batch-127-reconciliation/"]
    ledger["limits"] = [
        "Bounded textual and host review, not exhaustive linguistic or arbitrary/custom-pool acceptance.",
        "No new Kotlin, native, phone, installed-APK or fallback-rendering acceptance.",
        "Direct guards prevent bounded broad-English ambiguity; they do not assert universal "
        "Japanese synonymy, equal frequency or transitive exclusions.",
        "Publication, CI and exact served ZIP remain pending; review closure is not delivery.",
        "Original reports, optional judgments, qualified sources and failed attempts are preserved.",
        "Complete external captures and mixed segments containing them remain local.",
    ]
    return ledger


def finalize(spec_path):
    spec_raw = frozen(spec_path)
    spec = json.loads(spec_raw)
    candidate = spec["candidate"]
    config = load_batch(127)
    repo = Path(config["repo"])
    closure = repo / "docs" / "n1-reviews" / "batch-127-closure"
    provenance_raw = frozen(closure / "provenance.json")
    provenance = json.loads(provenance_raw)
    proof_raw = frozen(spec["verification"]["path"], spec["verification"]["sha256"])
    proof = json.loads(proof_raw)
    check_history(provenance, candidate, config)
    check_proof(proof, candidate, config)
    archive_raw = frozen(spec["archiveVerification"]["path"], spec["archiveVerification"]["sha256"])
    archive = json.loads(archive_raw)
    require(archive["status"] == "PASS" and archive["candidate"] == candidate
            and archive["provenanceSha256"] == sha(provenance_raw)
            and len(archive["chains"]) == 6, "Actual six-chain archive was not verified")
    guard, _ = start_guard("B127 four-run closure finalization")
    try:
        require(git(config, "rev-parse", "HEAD").decode().strip() == candidate
                and git(config, "show", "-s", "--format=%P%n%G?|%GF|%ae|%ce", candidate).decode().strip()
                == f"{config['candidate']}\nG|{SIGNER}|stop-cran@list.ru|stop-cran@list.ru"
                and not git(config, "diff", "--name-only")
                and not git(config, "diff", "--cached", "--name-only"), "Signed candidate changed")
        untracked = git(config, "ls-files", "--others", "--exclude-standard", "-z").decode().split("\0")
        require(all(not path or path.startswith("docs/n1-reviews/batch-127-closure/")
                    for path in untracked), "Unrelated untracked files")
        manifest = git(config, "show", f"{candidate}:manifest.json")
        require(sha(manifest) == proof["manifestSha256"], "Confirmed manifest changed")
        for path, digest in proof["signedArtifacts"].items():
            require(sha(git(config, "show", f"{candidate}:{path}")) == digest,
                    f"Verified signed evidence changed: {path}")
            guard.check()
        for path, digest in provenance["recordedFileSha256"].items():
            frozen(closure / path, digest)
            guard.check()
        ledger_path = repo / "docs" / "n1-sources" / "batch-127-progress.json"
        previous = git(config, "show", f"{candidate}:docs/n1-sources/batch-127-progress.json")
        require(ledger_path.read_bytes() == previous, "Author progress changed")
        ledger = make_ledger(json.loads(previous), config, candidate, provenance,
                             sha(provenance_raw), proof)
        artifacts = {
            "verification/original-progress.json": previous,
            "verification/reconciliation-001.json": proof_raw,
            "verification/actual-archive.json": archive_raw,
            "protocol/finalizer-spec.json": spec_raw,
        }
        for mode, gates in proof["gateSets"].items():
            directory = Path(gates["directory"])
            prefix = f"gates/reconciliation-001/{mode}"
            artifacts[f"{prefix}/summary.json"] = frozen(directory / "summary.json", gates["summarySha256"])
            for row in gates["gates"]:
                name = row["gate"]
                artifacts[f"{prefix}/{name}.json"] = frozen(directory / f"{name}.json", row["receiptSha256"])
                artifacts[f"{prefix}/{name}.log"] = frozen(directory / f"{name}.log", row["logSha256"])
        for name in ("finalize_b127.py", "test_finalize_b127.py", "verify_b127_reconciliation.py",
                     "prepare_b127_confirmations.py"):
            artifacts[f"protocol/b127/{name}"] = frozen(TOOLS / name)
        for item in spec.get("supportingArtifacts", []):
            name = item["archivePath"]
            require(name.startswith(("verification/", "protocol/")) and "\\" not in name
                    and ".." not in name.split("/") and not name.endswith(".jsonl")
                    and name not in artifacts, "Unsafe or duplicate supporting artifact")
            artifacts[name] = frozen(item["path"], item["sha256"])
        require(not set(artifacts) & set(provenance["recordedFileSha256"]), "Duplicate closure artifact")
        for name, raw in artifacts.items():
            write_frozen(closure / name, raw)
            guard.check()
        freeze_json(closure / "validation-provenance.json", {
            "batch": 127, "candidate": candidate, "reviewClosureSha256": sha(provenance_raw),
            "recordedFileSha256": {name: sha(raw) for name, raw in artifacts.items()},
            "publication": "PENDING",
        })
        require(ledger_path.read_bytes() == previous, "Progress changed during finalization")
        ledger_path.chmod(0o644)
        ledger_path.write_bytes(json_bytes(ledger))
        require(ledger_path.read_bytes() == json_bytes(ledger), "Progress readback differs")
        ledger_path.chmod(0o444)
        print(json.dumps({"candidate": candidate, "status": ledger["status"],
                          "ledgerSha256": sha(json_bytes(ledger)), "published": False}))
    finally:
        require(not guard.finish()["breach"], "Finalization RAM guard breached")


if __name__ == "__main__":
    finalize(Path(sys.argv[1]))

"""Bind both actual revision-002 gate runs to the verified signed correction."""
import json
import sys
from pathlib import Path

from common import freeze_json, frozen, load_module, require, sha, start_guard, write_frozen
from run_b134_closure_checks import BASE, CANDIDATE, HELPERS, HERE, ORDER, REPO, lineage
from verify_b134_gates import (
    LINK_HELPER, LINK_HELPER_SHA, READING_KEYS, commands, memory_ok,
    verify_execution, verify_launcher, verify_quiz, verify_reading,
)
from verify_b134_packet import RUNNER
from verify_b134_sources import Git

ROOT = HERE / "review"
REVIEWED = "355cccb840d22e7313e79f234eb93d1367e00352"
SCOPE_VERIFIER_SHA = "328b5281659b6dd9f049cf05cc8219fe56843aa952f315c1e7bb4d331ba17b6b"
WRAPPER_SHA = "0d7dc53c3633075fc2d345e53c9609de3abfb864ca65668e66a287c67d47123f"


def verify_summary(summary, mode, head, depth, manifest_sha, signed):
    require(
        summary["batch"] == 134 and summary["status"] == "PASS"
        and summary["mode"] == mode and summary["base"] == BASE
        and summary["initialSnapshot"] == CANDIDATE and summary["head"] == head
        and summary["reconciliationCommits"] == depth
        and summary["checks"] == ORDER and summary["manifestReproducible"] is True
        and summary["manifestSha256"] == manifest_sha
        and summary["changedFiles"] == signed
        and summary["wrapperSha256"] == WRAPPER_SHA,
        "Gate summary differs from the signed revision or required execution",
    )


def main(proof_path, proof_sha, working, committed, output):
    require(output.parent == ROOT and not output.exists(), "Use a new direct review output")
    require(working.parent == committed.parent == HERE and working != committed,
            "Use distinct actual gate directories directly under scratch-134")
    proof_raw = frozen(proof_path, proof_sha)
    proof = json.loads(proof_raw)
    require(proof["batch"] == 134 and proof["status"] == "PASS"
            and proof["reviewed"] == REVIEWED and proof["lineageDepth"] == 1
            and proof["verifierSha256"] == SCOPE_VERIFIER_SHA,
            "Wrong signed correction scope proof")
    memory_ok(proof["memory"])
    frozen(LINK_HELPER, LINK_HELPER_SHA)
    helper = load_module("b134_revision002_gate_bindings", LINK_HELPER)
    guard, _ = start_guard("B134 revision-002 actual gate receipt verification")
    captured, groups = {}, {}
    try:
        git = Git(REPO, RUNNER, guard)
        candidate = proof["commit"]

        def clean():
            require(git("rev-parse", "HEAD").decode().strip() == candidate
                    and not git("status", "--porcelain=v1", "--untracked-files=all"),
                    "Gate verification requires the clean signed correction")

        clean()
        depths = {"working": lineage(git, REVIEWED), "committed": lineage(git, candidate)}
        manifest_sha = sha(git("show", f"{candidate}:manifest.json"))
        require(manifest_sha == proof["signedFiles"]["manifest.json"],
                "Scope proof manifest differs")
        paths = git("diff", "--name-only", "-z", CANDIDATE, candidate).decode("utf-8").split("\0")
        require(paths[-1] == "", "Unterminated signed path inventory")
        signed = {name: sha(git("show", f"{candidate}:{name}")) for name in paths[:-1]}
        for mode, directory in (("working", working), ("committed", committed)):
            summary_raw = frozen(directory / "summary.json")
            summary = json.loads(summary_raw)
            verify_summary(summary, mode, REVIEWED if mode == "working" else candidate,
                           depths[mode], manifest_sha, signed)
            require(set(summary["sources"]) == set(HELPERS), "Gate helper inventory differs")
            for name, digest in summary["sources"].items():
                raw = git("show", f"{CANDIDATE}:docs/n1-sources/batch-134/producers/{name}")
                require(sha(raw) == digest and (HERE / name).read_bytes() == raw,
                        "Executed helper differs from the signed original")
            bindings = helper.gate_bindings(
                directory, {"repo": str(REPO)}, manifest_sha,
                summary["sources"]["run_134_gates.py"], guard)
            require(summary["logs"] == {row["gate"]: {key: row[key] for key in
                    ("receiptSha256", "logSha256")} for row in bindings},
                    "Gate inventory differs")
            receipts, logs = {}, {}
            captured[mode + "/summary.json"] = summary_raw
            for name in ORDER:
                for suffix in ("json", "log"):
                    raw = frozen(directory / f"{name}.{suffix}", summary["logs"][name][
                        "receiptSha256" if suffix == "json" else "logSha256"])
                    captured[f"{mode}/{name}.{suffix}"] = raw
                    if suffix == "json":
                        receipts[name] = json.loads(raw)
                    else:
                        logs[name] = raw.decode("utf-8").replace("\r\n", "\n")
                require(receipts[name]["base"] == BASE, "Gate base differs")
            verify_execution(receipts, commands(), summary["sources"]["common_134.py"])
            verify_launcher(receipts, logs, summary["sources"]["bounded_launch_134.py"])
            verify_quiz(logs["quiz-safety"], 51)
            verify_reading(logs["reading-exposure"], READING_KEYS)
            groups[mode] = {
                "directory": str(directory), "summarySha256": sha(summary_raw),
                "quizWarnings": 51, "latentReadingPairs": 1, "gates": bindings,
            }
        clean()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Gate verification RAM breach")
    captured["scope-proof.json"] = proof_raw
    evidence = {name: write_frozen(output / name, raw) for name, raw in captured.items()}
    print(json.dumps(freeze_json(output / "verification.json", {
        "batch": 134, "status": "PASS", "candidate": candidate, "groups": groups,
        "sourceProof": {"path": str(proof_path), "sha256": proof_sha},
        "manifestSha256": manifest_sha, "signedFiles": signed,
        "evidence": evidence, "memory": memory,
        "verifierSha256": sha(Path(__file__).read_bytes()),
        "logParsing": "CRLF normalized only for semantic checks; original bytes retained.",
        "limits": "Actual ten host gates per run; no linguistic, reviewer, closure, "
                  "native/device or publication acceptance.",
    })))


if __name__ == "__main__":
    require(len(sys.argv) == 6, "PROOF PROOF_SHA WORKING_DIRECTORY COMMITTED_DIRECTORY OUTPUT")
    main(Path(sys.argv[1]).resolve(), sys.argv[2], Path(sys.argv[3]).resolve(),
         Path(sys.argv[4]).resolve(), Path(sys.argv[5]).resolve())

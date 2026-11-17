"""Verify the executed working/committed receipts against the signed source proof."""
import json
from pathlib import Path

from common import freeze_json, frozen, load_module, require, sha, start_guard, write_frozen
from run_b134_closure_checks import BASE, CANDIDATE, HERE, ORDER, REPO
from verify_b134_gates import (
    LINK_HELPER, LINK_HELPER_SHA, commands, memory_ok, verify_execution,
    verify_launcher, verify_quiz, verify_reading, READING_KEYS,
)

ROOT = HERE / "review"
PROOF = ROOT / "reconciliation-verification-001" / "verification.json"
PROOF_SHA = "7ea9e7dde1989b5d1eb71bed3b5789ab77f4e3713277591b4841eeb2b0295da1"
OUT = ROOT / "reconciliation-gate-verification-001"
WRAPPER_SHA = "0d7dc53c3633075fc2d345e53c9609de3abfb864ca65668e66a287c67d47123f"


def main():
    require(not OUT.exists(), "Preserve gate verification")
    proof = json.loads(frozen(PROOF, PROOF_SHA))
    require(proof["status"] == "PASS" and proof["initialSnapshot"] == CANDIDATE,
            "Source proof differs")
    memory_ok(proof["memory"])
    frozen(LINK_HELPER, LINK_HELPER_SHA)
    helper = load_module("b134_reconciliation_gate_bindings", LINK_HELPER)
    guard, _ = start_guard("B134 actual reconciliation gate receipts")
    captured, groups = {}, {}
    try:
        for mode, directory in (("working", "reconciliation-working-003"),
                                ("committed", "reconciliation-committed-001")):
            path = HERE / directory
            summary_raw = frozen(path / "summary.json")
            summary = json.loads(summary_raw)
            require(summary["batch"] == 134 and summary["status"] == "PASS"
                    and summary["mode"] == mode and summary["base"] == BASE
                    and summary["initialSnapshot"] == CANDIDATE
                    and summary["head"] == (CANDIDATE if mode == "working" else proof["candidate"])
                    and summary["reconciliationCommits"] == (0 if mode == "working" else proof["lineageDepth"])
                    and summary["checks"] == ORDER and summary["manifestReproducible"] is True
                    and summary["manifestSha256"] == proof["manifestSha256"]
                    and summary["changedFiles"] == proof["signedFiles"]
                    and summary["wrapperSha256"] == WRAPPER_SHA, "Gate summary differs from signed revision")
            for name, digest in summary["sources"].items():
                require(sha((HERE / name).read_bytes()) == digest, "Executed helper changed")
            bindings = helper.gate_bindings(
                path, {"repo": str(REPO)}, proof["manifestSha256"],
                summary["sources"]["run_134_gates.py"], guard)
            require(summary["logs"] == {row["gate"]: {k: row[k] for k in (
                "receiptSha256", "logSha256")} for row in bindings}, "Gate inventory differs")
            receipts, logs = {}, {}
            captured[directory + "/summary.json"] = summary_raw
            for name in ORDER:
                for suffix in ("json", "log"):
                    raw = frozen(path / f"{name}.{suffix}", summary["logs"][name][
                        "receiptSha256" if suffix == "json" else "logSha256"])
                    captured[directory + "/" + name + "." + suffix] = raw
                    if suffix == "json":
                        receipts[name] = json.loads(raw)
                    else:
                        logs[name] = raw.decode("utf-8").replace("\r\n", "\n")
                require(receipts[name]["base"] == BASE, "Gate base differs")
            verify_execution(receipts, commands(), summary["sources"]["common_134.py"])
            verify_launcher(receipts, logs, summary["sources"]["bounded_launch_134.py"])
            verify_quiz(logs["quiz-safety"], 51)
            verify_reading(logs["reading-exposure"], READING_KEYS)
            groups[mode] = {"directory": directory, "summarySha256": sha(summary_raw),
                            "quizWarnings": 51, "latentReadingPairs": 1, "gates": bindings}
        evidence = {name: write_frozen(OUT / name, raw) for name, raw in captured.items()}
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Gate verification RAM breach")
    print(json.dumps(freeze_json(OUT / "verification.json", {
        "batch": 134, "status": "PASS", "candidate": proof["candidate"], "groups": groups,
        "sourceProof": {"path": str(PROOF), "sha256": PROOF_SHA},
        "manifestSha256": proof["manifestSha256"], "evidence": evidence, "memory": memory,
        "logParsing": "CRLF normalized to LF only for semantic checks; original bytes/hashes retained.",
        "verifierSha256": sha(Path(__file__).read_bytes()),
        "limits": "Actual ten host gates in each run, not semantic/reviewer/native/publication acceptance.",
    })))


if __name__ == "__main__":
    main()

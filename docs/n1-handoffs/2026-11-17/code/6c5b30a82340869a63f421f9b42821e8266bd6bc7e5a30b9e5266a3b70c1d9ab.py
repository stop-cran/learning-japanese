"""Preserve valid partial outputs and complete the B132 verification preparation."""
import json
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, start_guard

TOOLS = Path(__file__).resolve().parent
HERE = WS / "scratch-132" / "review"
PREVIOUS = WS / "scratch-131" / "review"
frozen(TOOLS / "prepare_b131_source_verifier.py",
       "1c49464972263d673822b45a3445d293f439c3c03cc00ed3e1ab974e7f1544a5")
from prepare_b131_source_verifier import derive


def retained(source, expected, target, changes):
    raw = frozen(source, expected)
    transformed = raw
    for before, after in changes:
        require(before in transformed and after not in transformed, "Ambiguous retained derivation")
        transformed = transformed.replace(before, after)
    require(frozen(target) == transformed, "Existing partial output differs from its pinned source")
    return {"source": {"path": str(source), "sha256": expected},
            "output": {"path": str(target), "sha256": sha(transformed), "bytes": len(transformed)},
            "substitutions": [[a.decode(), b.decode()] for a, b in changes],
            "retainedUnchanged": True}


def main():
    guard, _ = start_guard("B132 verification preparation completion")
    try:
        runner = retained(PREVIOUS / "guarded-test-v3.py",
                          "da78564efadb90ac4c174dbf13e375327b611bc5e0fc77913c8b85c22c1aaf6b",
                          HERE / "guarded-test-v3.py",
                          [(b"b131-worktree", b"b132-worktree"), (b"scratch-131", b"scratch-132")])
        runner_tests = retained(PREVIOUS / "test-guarded-test-v3.py",
                                "49f886a233ac6d3f344dd00e050d4f0ffa3f44940cd5ed632c586fe8ea0c50ff",
                                HERE / "test-guarded-test-v3.py", [])
        schema = retained(TOOLS / "b130_source_schema.py",
                          "91df923ee8ed6750b079a7ef35d0231560591fa699df15c6274e9919b9260ffa",
                          TOOLS / "b132_source_schema.py",
                          [(b"B130", b"B132"), (b"== 130", b"== 132")])
        tests = derive("test_b130_source_schema.py",
                       "97864fc825c657af14b683525d2d2a0b1943ba412de7fb4f90d9b4e06bfd787e",
                       "test_b132_source_schema.py", [("130", "132")])
        verifier = derive("verify_b130_sources.py",
                          "222518f71e16878a49dbff51ecaa94ee2d9f6f471b8d9a5fa4fb9bd4b6d0a22b",
                          "verify_b132_sources.py", [
                              ("b130_source_schema", "b132_source_schema"),
                              ("91df923ee8ed6750b079a7ef35d0231560591fa699df15c6274e9919b9260ffa",
                               schema["output"]["sha256"]),
                              ('facts["batch"] == 130', 'facts["batch"] == 132'),
                              ("B130 verifier requires batch 130", "B132 verifier requires batch 132"),
                              ("verify_b130_sources.py", "verify_b132_sources.py"),
                          ])
        guard.check()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Preparation RAM breach")
    print(json.dumps(freeze_json(HERE / "verification-tools-preparation-001.json", {
        "batch": 132, "status": "PREPARED_NOT_EXECUTED_ON_CANDIDATE",
        "runner": runner, "runnerTests": runner_tests,
        "sourceSchema": schema, "sourceSchemaTests": tests, "sourceVerifier": verifier,
        "producer": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "memory": memory,
        "preservedFailure": "scratch-131/review/b132-verification-tools-execution-001: "
                            "ordered substitutions put132 into test identifiers before a broad130 "
                            "replacement, so the reversible derivation correctly rejected ambiguity. "
                            "Valid partial runner/schema files are byte-verified and retained. "
                            "Tests now use one reversible batch-number substitution.",
        "scope": "Coordinator tooling only; no selected members, query predicates or candidate guessed. "
                 "Source facts must be independently constructed from the completed handoff. "
                 "The source verifier requires the scan base to equal the signed candidate parent.",
        "limits": "Not content/source acceptance, reviewer admission or publication. Actual handoff "
                  "payload, gates, complete-packet and semantic checks remain required.",
    })))


if __name__ == "__main__":
    main()

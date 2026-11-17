"""Prepare B132-local command and source checks without touching authoring files."""
import json
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, start_guard

TOOLS = Path(__file__).resolve().parent
HERE = WS / "scratch-132" / "review"
PREVIOUS = WS / "scratch-131" / "review"
DERIVER_SHA = "1c49464972263d673822b45a3445d293f439c3c03cc00ed3e1ab974e7f1544a5"
frozen(TOOLS / "prepare_b131_source_verifier.py", DERIVER_SHA)
from prepare_b131_source_verifier import derive


def main():
    outputs = [HERE / "guarded-test-v3.py", HERE / "test-guarded-test-v3.py",
               TOOLS / "b132_source_schema.py", TOOLS / "test_b132_source_schema.py",
               TOOLS / "verify_b132_sources.py", HERE / "verification-tools-preparation-001.json"]
    require(all(not path.exists() for path in outputs), "Preserve existing B132 coordinator tools")
    guard, _ = start_guard("B132 coordinator verification preparation")
    try:
        runner = derive(str(PREVIOUS / "guarded-test-v3.py"),
                        "da78564efadb90ac4c174dbf13e375327b611bc5e0fc77913c8b85c22c1aaf6b",
                        str(outputs[0]), [
                            ("b131-worktree", "b132-worktree"),
                            ("scratch-131", "scratch-132"),
                        ])
        runner_tests = derive(str(PREVIOUS / "test-guarded-test-v3.py"),
                              "49f886a233ac6d3f344dd00e050d4f0ffa3f44940cd5ed632c586fe8ea0c50ff",
                              str(outputs[1]), [])
        schema = derive("b130_source_schema.py",
                        "91df923ee8ed6750b079a7ef35d0231560591fa699df15c6274e9919b9260ffa",
                        str(outputs[2]), [("B130", "B132"), ("== 130", "== 132")])
        tests = derive("test_b130_source_schema.py",
                       "97864fc825c657af14b683525d2d2a0b1943ba412de7fb4f90d9b4e06bfd787e",
                       str(outputs[3]), [
                           ("b130_source_schema", "b132_source_schema"),
                           ("B130", "B132"), ("130", "132"),
                       ])
        verifier = derive("verify_b130_sources.py",
                          "222518f71e16878a49dbff51ecaa94ee2d9f6f471b8d9a5fa4fb9bd4b6d0a22b",
                          str(outputs[4]), [
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
    print(json.dumps(freeze_json(outputs[-1], {
        "batch": 132, "status": "PREPARED_NOT_EXECUTED_ON_CANDIDATE",
        "runner": runner, "runnerTests": runner_tests,
        "sourceSchema": schema, "sourceSchemaTests": tests, "sourceVerifier": verifier,
        "producer": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "deriverSha256": DERIVER_SHA, "memory": memory,
        "scope": "Coordinator-only tooling. No selected members, queries, source counts or candidate "
                 "are guessed. Source facts must be independently constructed from the completed handoff. "
                 "The source verifier requires the scan base to equal the signed candidate's parent; "
                 "B131's special dual-base bridge is intentionally not transplanted.",
        "limits": "Not authoring, content/source acceptance, reviewer admission or publication. "
                  "Payload, gates, complete-packet and semantic checks still follow the actual handoff.",
    })))


if __name__ == "__main__":
    main()

"""Prepare B133 source checks without assuming the author's selected members."""
import json
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, start_guard

TOOLS = Path(__file__).resolve().parent
HERE = WS / "scratch-133" / "review"
DERIVER_SHA = "1c49464972263d673822b45a3445d293f439c3c03cc00ed3e1ab974e7f1544a5"
RUNNER_SHA = "03260517d250b9d8071e2e70ec76fdb3ffda906d4f947e4a049375ebb249e5eb"
SCHEMA_SHA = "6b67e3181c0788ad3578d7e80d71be8c36f2e8b8bb7b072ef9b36f7ed0c13f33"
frozen(TOOLS / "prepare_b131_source_verifier.py", DERIVER_SHA)
from prepare_b131_source_verifier import derive


def main():
    outputs = [
        HERE / "test-guarded-test-v3.py",
        TOOLS / "b133_source_schema.py",
        TOOLS / "test_b133_source_schema.py",
        TOOLS / "verify_b133_sources.py",
        HERE / "verification-tools-preparation-001.json",
    ]
    require(all(not path.exists() for path in outputs), "Preserve existing B133 outputs")
    runner_raw = frozen(HERE / "guarded-test-v3.py", RUNNER_SHA)
    producer_raw = frozen(Path(__file__))
    guard, _ = start_guard("B133 coordinator verification preparation")
    try:
        runner_tests = derive(
            str(WS / "scratch-132" / "review" / "test-guarded-test-v3.py"),
            "49f886a233ac6d3f344dd00e050d4f0ffa3f44940cd5ed632c586fe8ea0c50ff",
            str(outputs[0]), [],
        )
        schema = derive("b132_source_schema.py", SCHEMA_SHA, str(outputs[1]), [
            ("B132", "B133"), ("== 132", "== 133"),
        ])
        tests = derive(
            "test_b132_source_schema.py",
            "4875bff77d8a808f5b6c58b26ef8cd2bca3f08074737c9f1524f238c3d425e08",
            str(outputs[2]), [("132", "133")],
        )
        verifier = derive(
            "verify_b132_sources.py",
            "43ee9a6ceaf4ae023d4c9739b0a5276bdfd0c9c8573b410f99c5c06970dfe861",
            str(outputs[3]), [
                ("b132_source_schema", "b133_source_schema"),
                (SCHEMA_SHA, schema["output"]["sha256"]),
                ('facts["batch"] == 132', 'facts["batch"] == 133'),
                ("B132 verifier requires batch 132", "B133 verifier requires batch 133"),
                ("verify_b132_sources.py", "verify_b133_sources.py"),
            ],
        )
        guard.check()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Preparation RAM breach")
    print(json.dumps(freeze_json(outputs[-1], {
        "batch": 133,
        "status": "PREPARED_NOT_EXECUTED_ON_CANDIDATE",
        "base": "6858fcfb069cc56a195c3f6ed938f92f657fe96b",
        "runner": {
            "output": {
                "path": str(HERE / "guarded-test-v3.py"),
                "sha256": sha(runner_raw),
                "bytes": len(runner_raw),
            },
            "retainedUnchanged": True,
            "diagnosticLimit": "Inherited error text names scratch-132, but the path check "
                               "uses this runner's actual scratch-133 parent.",
        },
        "runnerTests": runner_tests,
        "sourceSchema": schema,
        "sourceSchemaTests": tests,
        "sourceVerifier": verifier,
        "producer": {"path": str(Path(__file__)), "sha256": sha(producer_raw)},
        "deriverSha256": DERIVER_SHA,
        "memory": memory,
        "scope": "Coordinator-only preparation. No selected members, query predicates, "
                 "source counts, scan paths or candidate SHA are assumed. All derivations "
                 "are byte-reversible to frozen B132 inputs. The source verifier retains "
                 "same-base scans, complete-record membership and baseline reproduction.",
        "limits": "The actual signed handoff must independently establish schema compatibility "
                  "and complete source selectors before this verifier is used. If incompatible, "
                  "preserve this preparation and derive a successor; do not weaken a check. "
                  "No authoring files changed. No source, payload, gate, linguistic review "
                  "or publication acceptance is claimed.",
    })))


if __name__ == "__main__":
    main()

"""Prepare B134 source checks without assuming the author's selected members."""
import json
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, start_guard

TOOLS = Path(__file__).resolve().parent
HERE = WS / "scratch-134" / "review"
DERIVER_SHA = "1c49464972263d673822b45a3445d293f439c3c03cc00ed3e1ab974e7f1544a5"
RUNNER_SHA = "52d7b2a997aa707358556d7cbb0fa621e4383df45bf67c84b52bd729a52ad283"
SCHEMA_SHA = "a2b6a6d25e10b63198d760775daa16d5c4de0f8f46b70749308a02c47bfa521a"
frozen(TOOLS / "prepare_b131_source_verifier.py", DERIVER_SHA)
from prepare_b131_source_verifier import derive


def main():
    outputs = [
        HERE / "test-guarded-test-v3.py",
        TOOLS / "b134_source_schema.py",
        TOOLS / "test_b134_source_schema.py",
        TOOLS / "verify_b134_sources.py",
        HERE / "verification-tools-preparation-001.json",
    ]
    require(all(not path.exists() for path in outputs), "Preserve existing B134 outputs")
    runner_raw = frozen(HERE / "guarded-test-v3.py", RUNNER_SHA)
    producer_raw = frozen(Path(__file__))
    guard, _ = start_guard("B134 coordinator verification preparation")
    try:
        runner_tests = derive(
            str(WS / "scratch-133" / "review" / "test-guarded-test-v3.py"),
            "49f886a233ac6d3f344dd00e050d4f0ffa3f44940cd5ed632c586fe8ea0c50ff",
            str(outputs[0]), [],
        )
        schema = derive("b133_source_schema.py", SCHEMA_SHA, str(outputs[1]), [
            ("B133", "B134"), ("== 133", "== 134"),
        ])
        tests = derive(
            "test_b133_source_schema.py",
            "71e35e298ea374da12c619ca63d402ca2b5cab458fd76d7c555211243a572c08",
            str(outputs[2]), [("133", "134")],
        )
        verifier = derive(
            "verify_b133_sources.py",
            "84135cb99ff36f31bd6ac27fa9a82dd656c14dcf4d20c98c6852c45745cd5e71",
            str(outputs[3]), [
                ("b133_source_schema", "b134_source_schema"),
                (SCHEMA_SHA, schema["output"]["sha256"]),
                ('facts["batch"] == 133', 'facts["batch"] == 134'),
                ("B133 verifier requires batch 133", "B134 verifier requires batch 134"),
                ("verify_b133_sources.py", "verify_b134_sources.py"),
            ],
        )
        guard.check()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Preparation RAM breach")
    print(json.dumps(freeze_json(outputs[-1], {
        "batch": 134,
        "status": "PREPARED_NOT_EXECUTED_ON_CANDIDATE",
        "base": "e17cb97c53ca4e3193dae5e11b52ba517fe86e76",
        "runner": {
            "output": {
                "path": str(HERE / "guarded-test-v3.py"),
                "sha256": sha(runner_raw),
                "bytes": len(runner_raw),
            },
            "retainedUnchanged": True,
            "diagnosticLimit": "Inherited error text names scratch-132, but the path check "
                               "uses this runner's actual scratch-134 parent.",
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
                 "are byte-reversible to frozen B133 inputs. The source verifier retains "
                 "same-base scans, complete-record membership and baseline reproduction.",
        "limits": "The actual signed handoff must independently establish schema compatibility "
                  "and complete source selectors before this verifier is used. If incompatible, "
                  "preserve this preparation and derive a successor; do not weaken a check. "
                  "No authoring files changed. No source, payload, gate, linguistic review "
                  "or publication acceptance is claimed.",
    })))


if __name__ == "__main__":
    main()

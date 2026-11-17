"""Resume the preserved partial derivation with one non-overlapping test rename."""
import json
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, start_guard

TOOLS = Path(__file__).resolve().parent
HERE = WS / "scratch-131" / "review"
PREDECESSOR_SHA = "1c49464972263d673822b45a3445d293f439c3c03cc00ed3e1ab974e7f1544a5"
frozen(TOOLS / "prepare_b131_source_verifier.py", PREDECESSOR_SHA)
from prepare_b131_source_verifier import BRIDGE_SHA, SCHEMA_SHA, TESTS_SHA, VERIFIER_SHA, derive


def main():
    require(not (HERE / "source-verifier-derivation-002.json").exists(), "Preserve derivation record")
    require(not (TOOLS / "test_b131_source_schema.py").exists()
            and not (TOOLS / "verify_b131_sources.py").exists(), "Preserve existing derived tools")
    failed_dir = HERE / "source-verifier-preparation-execution-001"
    failed_raw = frozen(failed_dir / "receipt.json")
    failed = json.loads(failed_raw)
    require(failed["exitCode"] == 1 and failed["cleanupError"] is None
            and not failed["memory"]["breach"], "Unexpected failed predecessor execution")
    failed_log = frozen(failed_dir / "output.log", failed["logSha256"])
    require(b"ValueError: Ambiguous substitution: 130" in failed_log,
            "Predecessor failed for a different reason")
    source_schema = frozen(TOOLS / "b130_source_schema.py", SCHEMA_SHA)
    expected_schema = source_schema.replace(b"B130", b"B131").replace(b"== 130", b"== 131")
    schema_path = TOOLS / "b131_source_schema.py"
    schema_raw = frozen(schema_path)
    require(schema_raw == expected_schema, "Partial schema differs from the original exact derivation")
    frozen(TOOLS / "b131_base_binding_v2.py", BRIDGE_SHA)
    guard, _ = start_guard("B131 source-verifier derivation recovery")
    try:
        tests = derive("test_b130_source_schema.py", TESTS_SHA, "test_b131_source_schema.py", [
            ("130", "131"),
        ])
        verifier = derive("verify_b130_sources.py", VERIFIER_SHA, "verify_b131_sources.py", [
            ("import b130_source_schema as schema",
             "import b131_source_schema as schema\nimport b131_base_binding_v2 as base_bridge"),
            (f'SCHEMA_SHA = "{SCHEMA_SHA}"',
             f'SCHEMA_SHA = "{sha(schema_raw)}"\nBRIDGE_SHA = "{BRIDGE_SHA}"'),
            ('    frozen(Path(schema.__file__), SCHEMA_SHA)\n',
             '    frozen(Path(schema.__file__), SCHEMA_SHA)\n'
             '    frozen(Path(base_bridge.__file__), BRIDGE_SHA)\n'),
            ('facts["batch"] == 130', 'facts["batch"] == 131'),
            ("B130 verifier requires batch 130", "B131 verifier requires batch 131"),
            ('        require(TRAILER in git("show", "-s", "--format=%B", candidate), "Missing trailer")\n',
             '        require(TRAILER in git("show", "-s", "--format=%B", candidate), "Missing trailer")\n'
             '        base_binding = base_bridge.verify_signed_binding(git, candidate)\n'
             '        source_base = base_binding["sourceBase"]\n'
             '        require(base == base_binding["candidateBase"], "Candidate facts use the wrong adapted base")\n'),
            ('git("ls-tree", "-rz", base, "--", "kanji")',
             'git("ls-tree", "-rz", source_base, "--", "kanji")'),
            ('baseline = json.loads(blob("manifest.json", base))["files"]',
             'baseline = json.loads(blob("manifest.json", source_base))["files"]'),
            ('schema.verify_selection(selection, signed_rows, index, members, base)',
             'schema.verify_selection(selection, signed_rows, index, members, source_base)'),
            ('title, base, helper', 'title, source_base, helper'),
            ('"batch": facts["batch"], "candidate": candidate, "base": base, "status": "PASS",',
             '"batch": facts["batch"], "candidate": candidate, "base": base, "status": "PASS",\n'
             '        "sourceBase": source_base, "baseBinding": base_binding,\n'
             '        "baseBridgeVerifier": {"path": str(Path(base_bridge.__file__)), "sha256": BRIDGE_SHA},'),
            ("Usage: verify_b130_sources.py", "Usage: verify_b131_sources.py"),
        ])
        guard.check()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "RAM breach")
    print(json.dumps(freeze_json(HERE / "source-verifier-derivation-002.json", {
        "batch": 131, "status": "PREPARATION_ONLY",
        "schema": {
            "source": {"path": str(TOOLS / "b130_source_schema.py"), "sha256": SCHEMA_SHA},
            "output": {"path": str(schema_path), "sha256": sha(schema_raw), "bytes": len(schema_raw)},
            "reuse": "Exact two-substitution output from preserved predecessor; not rewritten.",
        },
        "tests": tests, "verifier": verifier,
        "baseBridge": {"path": str(TOOLS / "b131_base_binding_v2.py"), "sha256": BRIDGE_SHA},
        "predecessor": {"path": str(TOOLS / "prepare_b131_source_verifier.py"),
                        "sha256": PREDECESSOR_SHA, "failedReceiptSha256": sha(failed_raw),
                        "failure": "Overlapping renames made the final broad test substitution ambiguous."},
        "producer": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "memory": memory,
        "limits": "Executable admission preparation only. Actual signed handoff, complete source "
                  "records, scan reproduction, payload, gates, reviews and publication remain pending.",
    })))


if __name__ == "__main__":
    main()

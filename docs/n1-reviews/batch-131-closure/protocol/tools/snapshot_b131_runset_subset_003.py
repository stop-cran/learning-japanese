"""Freeze the requested partial inspection ledger, not final readiness."""
import json
from b131_review_v3_common import (
    DEFAULT_PREFLIGHT, HERE, IMMUTABLE_BINDINGS, TOOLS, freeze_json, frozen, require, sha, start_guard)
from b131_preflight_003 import verify_protocol


def main():
    guard, _ = start_guard("B131003 immutable subset handoff")
    try:
        protocol = verify_protocol(json.loads(frozen(DEFAULT_PREFLIGHT)))
        tools = [TOOLS / name for name in (
            "b131_review_v3_common.py", "b131_preflight_003.py", "build_b131_runset_003.py",
            "prepare_chain_b131_003.py", "b131_runtime_003.py", "b131_review_admission_003.py",
            "b131_lifecycle_process_004.py", "step_b131_neutral_005.py", "test_b131_preparation_003.py")]
        paths = tools + [HERE / name for name in (
            "audit-review.py", "review_chain.py", "check-run-context.py", "check-report-structure.py",
            "source-bindings-003.json", "tooling-derivation-003.json", "path-readiness-003.json",
            "runset-build-003.json")]
        paths += [HERE / "prompts" / name for name in (
            "initial-claude-003.txt", "initial-gpt-003.txt", "kickoff-claude-003.txt", "kickoff-gpt-003.txt",
            "audit-config-N1-B131-CLAUDE-003.json", "audit-config-N1-B131-GPT-003.json",
            "preflight-compact-003.json")]
        for path, digest in IMMUTABLE_BINDINGS:
            frozen(path, digest)
        bindings = [{"path": str(path), "sha256": sha(frozen(path)), "bytes": path.stat().st_size} for path in paths]
        result = {
            "status": "IMMUTABLE_SUBSET_ONLY_VALIDATION_NOT_READY", "files": bindings,
            "protocol": protocol, "immutableInputs": [{"path": str(path), "sha256": digest}
                                                     for path, digest in IMMUTABLE_BINDINGS],
            "validation": "First32-case run had one isolated synthetic final-audit fixture error: relocated "
                          "HERE lacked batch.json. All path rejection/probe checks and24 existing controls passed. "
                          "A new frozen fixture successor supplies that unchanged config; full rerun pending.",
            "limits": "No reviewer admitted/launched/messaged. No retired reviewer observations opened."}
        result["memory"] = guard.finish()
        require(not result["memory"]["breach"], "Subset RAM breach")
        binding = freeze_json(HERE / "partial-handoff-003.json", result)
        print(json.dumps({"handoff": binding, **result}))
    except (Exception, KeyboardInterrupt):
        guard.finish()
        raise


if __name__ == "__main__":
    main()

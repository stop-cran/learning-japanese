"""Keep the failed archive attempt and use an explicit VOID-only bounded representation."""
import json
from pathlib import Path

from b130_context_confirmation import ROOT, binding
from common import TOOLS, freeze_json, frozen, load_batch, require, write_frozen
from prepare_b130_followup_engine import replace_once


def main():
    require(not (Path(load_batch(130)["repo"]) / "docs" / "n1-reviews" / "batch-130-closure").exists(),
            "The failed pre-write attempt unexpectedly created closure files")
    source = TOOLS / "close_b130_followup_v2.py"
    text = frozen(source, "d5395b9450fa7263b4e78eb17e6298c336d71bf4d828ac36022f84007aedee5f").decode()
    text = replace_once(text, "from b130_excluded_initials_v3 import archive_excluded",
                        "from b130_excluded_initials_v3 import archive_excluded\n"
                        "from b130_void_initial_audit import excluded_audit_support")
    text = replace_once(text, "                                    chain, audit_support, records)",
                        "                                    chain, excluded_audit_support(audit_support), records)")
    name = "close_b130_followup_v3.py"
    compile(text, name, "exec")
    spec_source = ROOT / "delta-closure-spec-001.json"
    spec = json.loads(frozen(spec_source))
    extra = ["b130_void_initial_audit.py", "test_b130_void_initial_audit.py",
             "prepare_b130_void_archive_retry.py", name]
    for tool in extra[:-1]:
        frozen(TOOLS / tool)
    require(not set(extra) & set(spec["additionalTools"]), "Retry tooling already present")
    output = write_frozen(TOOLS / name, text.encode())
    spec["additionalTools"] = sorted([*spec["additionalTools"], *extra])
    spec["supersedesPreparedSpec"] = binding(spec_source)
    spec["archiveAttempt001"] = {
        "status": "FAILED_BEFORE_WORKTREE_WRITES",
        "receipt": binding(ROOT / "delta-closure-archive-execution-001" / "receipt.json"),
        "reason": "The accepted-audit presenter rejected known VOID excluded initials. "
                  "Their original held validators remain unchanged; only excluded rendering now "
                  "uses a separate strict bounded VOID presenter. No failed review is accepted.",
    }
    spec_result = freeze_json(ROOT / "delta-closure-spec-002.json", spec)
    print(json.dumps(freeze_json(ROOT / "delta-closure-void-retry-001.json", {
        "source": binding(source), "output": output, "spec": spec_result,
        "support": binding(TOOLS / "b130_void_initial_audit.py"), "producer": binding(__file__),
    })))


if __name__ == "__main__":
    main()

"""Extend closure to preserve the actual context-held initial, without accepting it."""
import ast
from pathlib import Path

from common import TOOLS, WS, freeze_json, frozen, sha
from prepare_b130_review_tools import derive


VALIDATOR = '''def require_context_hold(held, mechanics, structure, context, batch, candidate):
    same_binding = lambda key: all(held[key][part] == mechanics[key][part]
                                   for part in ("path", "sha256"))
    require(batch == 130 and held["batch"] == batch and held["candidate"] == candidate
            and held["status"] == "HOLD_CONTEXT_COMPACTED" and mechanics["status"] == "HOLD"
            and held["reviewAccepted"] is False and held["finalAcceptance"] is False
            and held["run"] == mechanics["run"] and held["session"] == mechanics["session"]
            and mechanics["candidate"] == candidate
            and all(same_binding(key) for key in ("structure", "context", "finalAudit"))
            and structure["status"] == "PASS" and structure["errors"] == []
            and structure["overall"] == held["rawVerdict"]
            and context["status"] == "FAIL" and len(context["errors"]) == 1
            and [event["type"] for event in context["compactions"]]
                == ["session.compaction_start", "session.compaction_complete"]
            and context["errors"][0].startswith("Context compaction occurred:")
            and len(mechanics["problems"]) == 1
            and mechanics["problems"][0] == "context " + context["errors"][0]
            and mechanics["evidenceCheck"] is None,
            "Excluded initial is not its recorded context-held execution")
'''


def main():
    raw = frozen(TOOLS / "closure_initials.py").decode("utf-8").replace("\r\n", "\n")
    node = next(node for node in ast.parse(raw).body
                if isinstance(node, ast.FunctionDef) and node.name == "require_structure_hold")
    old_validator = "".join(raw.splitlines(keepends=True)[node.lineno - 1:node.end_lineno])
    helper = derive("closure_initials.py", "b130_context_held_initials.py", [
        (old_validator, VALIDATOR),
        ("        require_structure_hold(", "        require_context_hold("),
    ])
    extra = (
        '"b130_context_held_initials.py", "close_b130_compact.py", "verify_b130_archive_v2.py", '
        '"test_b130_context_held_closure.py", "prepare_b130_context_held_closure.py", '
        '"b130_compact_common.py", "step_b130_compact.py", "prepare-chain-b130-compact.py", '
        '"build-prompts-b130-compact.py", "prepare_b130_compact_review.py", '
        '"recover_b130_compact_preparation.py", "test_b130_compact_review.py"'
    )
    closure = derive("close_b130.py", "close_b130_compact.py", [
        ("from common import", "from b130_compact_common import"),
        ("from closure_initials import archive_excluded",
         "from b130_context_held_initials import archive_excluded"),
        ('"test_record_b130_publication.py"):', '"test_record_b130_publication.py", ' + extra + "):"),
    ])
    verifier = derive("verify_b130_archive.py", "verify_b130_archive_v2.py", [
        ('        for review in provenance["reviewLineage"]:',
         '        for review in provenance["reviewLineage"] + provenance["excludedInitialRuns"]:'),
        ('"Verifies the actual closure files and known external-snapshot labels. "',
         '"Verifies actual accepted and context-held closure chains with complete-source retention. "'),
    ])
    print(freeze_json(WS / "scratch-130" / "review" / "context-held-closure-derivation-001.json", {
        "batch": 130, "status": "PREPARATION_ONLY",
        "producer": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "derivations": [helper, closure, verifier],
        "limits": "Preserves the actual context-failed initial separately from accepted lineage. "
                  "No report rewrite or review credit. Closure still requires two actual accepted "
                  "confirmations on the final candidate and verified compact-packet inputs. "
                  "Other failure shapes and replacement confirmations need explicit successors.",
    }))


if __name__ == "__main__":
    main()

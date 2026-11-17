"""Derive closure v4: retain post-v3 tools, accept spec-listed frozen tools and archive the phase2-mismatch initial."""
from pathlib import Path

from common import WS, freeze_json, frozen, sha
from prepare_b130_review_tools import derive


NEW_TOOLS = ("close_b130_compact_v4.py", "b130_excluded_initials_v3.py", "prepare_b130_attempt004_closure.py",
             "test_b130_attempt004_closure.py", "confirm_b130_compact.py",
             "prepare_b130_compact_confirmation.py", "test_b130_compact_confirmation.py",
             "prepare_b130_review004.py", "build-prompts-b130-attempt004.py",
             "verify_b130_attempt004_prompts.py", "verify_b130_attempt004_prompts_v2.py")


def main():
    listed = "".join(f', "{name}"' for name in NEW_TOOLS)
    derivation = derive("close_b130_compact_v3.py", "close_b130_compact_v4.py", [
        ("from b130_excluded_initials_v2 import archive_excluded",
         "from b130_excluded_initials_v3 import archive_excluded"),
        ("            excluded_initials=(), confirmation_protocol=()):\n"
         '    require(batch == 130, "This closure adapter is limited to B130")\n',
         "            excluded_initials=(), confirmation_protocol=(), additional_tools=()):\n"
         '    require(batch == 130, "This closure adapter is limited to B130")\n'
         "    require(len(set(additional_tools)) == len(additional_tools)\n"
         '            and all(Path(name).name == name and name.endswith(".py") for name in additional_tools)\n'
         f"            and not set(additional_tools) & {{{listed[2:]}}},\n"
         '            "Additional tools must be distinct new top-level Python files")\n'),
        ('"test_b130_bounded_closure.py"):',
         '"test_b130_bounded_closure.py"' + listed + ", *additional_tools):"),
        ('confirmation_protocol=tuple(spec.get("confirmationProtocol", [])))',
         'confirmation_protocol=tuple(spec.get("confirmationProtocol", [])),\n'
         '            additional_tools=tuple(spec.get("additionalTools", [])))'),
    ])
    print(freeze_json(WS / "scratch-130" / "review" / "attempt004-closure-derivation-001.json", {
        "batch": 130, "status": "PREPARATION_ONLY", "derivation": derivation, "newRetainedTools": list(NEW_TOOLS),
        "producer": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "reason": "v3 cannot archive the coordinator phase2-mismatch Claude003 initial and does not retain the "
                  "compact confirmation engine or attempt-004 tools. Later frozen tools (confirmation preparer, "
                  "finalizer) are named in the closure spec's additionalTools instead of requiring v5.",
        "execution": "Invoke close_b130_compact_v4.py through run_b127_tool.py inside the outer RAM guard.",
        "limits": "No actual closure or publication. Acceptance, bounded Git routing and compact packet selection "
                  "are unchanged from v3.",
    }))


if __name__ == "__main__":
    main()

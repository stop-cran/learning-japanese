"""Keep compact packet selection while retaining the shared bounded Git adapter."""
from pathlib import Path

from common import WS, freeze_json, frozen, sha
from prepare_b130_review_tools import derive


def main():
    original = (
        "from b130_compact_common import (WS, freeze_json, frozen, git, load_batch, load_module, require,\n"
        "                    review_dir, sha, start_guard, verify_packet, write_frozen)\n"
    )
    replacement = (
        "from common import (WS, freeze_json, frozen, git, load_batch, load_module, require,\n"
        "                    review_dir, sha, start_guard, write_frozen)\n"
        "from b130_compact_common import verify_packet\n"
    )
    derivation = derive("close_b130_compact_v2.py", "close_b130_compact_v3.py", [
        (original, replacement),
        ('"build-prompts-b130-complete.py"):',
         '"build-prompts-b130-complete.py", "close_b130_compact_v3.py", '
         '"prepare_b130_bounded_closure.py", "test_b130_bounded_closure.py"):'),
    ])
    print(freeze_json(WS / "scratch-130" / "review" / "bounded-closure-derivation-001.json", {
        "batch": 130, "status": "PREPARATION_ONLY", "derivation": derivation,
        "producer": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "reason": "run_b127_tool.py patches original common.git/start_guard. Importing copied "
                  "compact helpers bypassed that bounded Git routing. Select only verify_packet "
                  "from the compact module; keep the shared adapter for all process/guard helpers.",
        "execution": "Invoke close_b130_compact_v3.py through run_b127_tool.py inside the outer RAM guard.",
        "limits": "No actual closure or publication. Acceptance and excluded-initial rules are unchanged.",
    }))


if __name__ == "__main__":
    main()

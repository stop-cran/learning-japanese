"""Derive a confirmation engine that verifies the compact B130 packet, keeping shared bounded helpers."""
from pathlib import Path

from common import WS, freeze_json, frozen, sha
from prepare_b130_review_tools import derive


def main():
    original = (
        "from common import (COORDINATOR, TOOLS, WS, at_commit, freeze_json, frozen, git, load_batch,\n"
        "                    load_module, require, review_dir, sha, start_guard, verify_packet, write_frozen)\n"
    )
    replacement = (
        "from common import (COORDINATOR, TOOLS, WS, at_commit, freeze_json, frozen, git, load_batch,\n"
        "                    load_module, require, review_dir, sha, start_guard, write_frozen)\n"
        "from b130_compact_common import verify_packet\n"
    )
    derivation = derive("confirm_b127.py", "confirm_b130_compact.py", [(original, replacement)])
    print(freeze_json(WS / "scratch-130" / "review" / "compact-confirmation-derivation-001.json", {
        "batch": 130, "status": "PREPARATION_ONLY", "derivation": derivation,
        "producer": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "reason": "confirm_b127.py imports verify_packet from original common, which resolves the "
                  "uncompacted B130 packet. Initial reviews read the lossless compact packet, so "
                  "confirmations must bind the same original-packet sources. Only verify_packet is "
                  "selected from b130_compact_common; git/at_commit/start_guard stay on original "
                  "common so run_b127_tool.py keeps bounded Git and shared RAM-guard routing.",
        "execution": "Invoke confirm_b130_compact.py build/final through run_b127_tool.py inside the outer "
                     "RAM guard; admit with scoped_confirmation_admission.py as in B129.",
        "retention": "An eventual closure successor must retain confirm_b130_compact.py, this producer, "
                     "its test and any later confirmation preparers; close_b130_compact_v3.py does not.",
        "limits": "No spec, chain, admission or delivery. Specs depend on accepted initials and reconciliation.",
    }))


if __name__ == "__main__":
    main()

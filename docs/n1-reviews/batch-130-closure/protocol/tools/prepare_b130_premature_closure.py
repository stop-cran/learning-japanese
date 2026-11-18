"""Derive closure preservation for the actual unaccepted initial phase1 failure."""
from pathlib import Path

from common import TOOLS, WS, freeze_json, frozen, sha
from prepare_b130_review_tools import derive


def main():
    extra = (
        "b130_excluded_initials_v2.py", "test_b130_premature_closure.py",
        "prepare_b130_premature_closure.py", "close_b130_compact_v2.py",
        "test_b130_held_archive.py", "prepare_b130_review003.py", "build-prompts-b130-complete.py",
    )
    derivation = derive("close_b130_compact.py", "close_b130_compact_v2.py", [
        ("from b130_context_held_initials import archive_excluded",
         "from b130_excluded_initials_v2 import archive_excluded"),
        ('"test_b130_compact_review.py"):', '"test_b130_compact_review.py", '
         + ", ".join(f'"{name}"' for name in extra) + "):"),
    ])
    print(freeze_json(WS / "scratch-130" / "review" / "premature-closure-derivation-001.json", {
        "batch": 130, "status": "PREPARATION_ONLY", "derivation": derivation,
        "additionalTools": [{"path": str(TOOLS / name), "sha256": sha(frozen(TOOLS / name))} for name in extra],
        "producer": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "limits": "Preserve the actual79/87 core coverage and absent phase2/report, not invented final evidence. "
                  "Context-held001 is still handled by its unchanged validated adapter. "
                  "Both runs remain excluded, never accepted. Real accepted reviews and confirmations remain required.",
    }))


if __name__ == "__main__":
    main()

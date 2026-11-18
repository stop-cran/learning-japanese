import importlib.util
import json
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT.parent))
from common_133 import REPO, sha, start_guard, write
from notes import PARENT, REL, expected_after

CORE = OUT.parent / "teaching-reconciliation-002" / "reconcile.py"


def main():
    mode, out = sys.argv[1], Path(sys.argv[2]).resolve()
    guard = start_guard()
    try:
        spec = importlib.util.spec_from_file_location("frozen_preservation_core_002", CORE)
        core = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(core)
        core.OUT, core.PARENT, core.REL, core.PACKET = OUT, PARENT, REL, REPO / REL
        core.expected_after = expected_after
        core.preserve(mode, out, guard)
        write(out / "wrapper-binding.json", {
            "wrapperSha256": sha(Path(__file__).read_bytes()), "corePath": str(CORE),
            "coreSha256": sha(CORE.read_bytes()), "exactTransformSha256": sha((OUT / "notes.py").read_bytes()),
            "parent": PARENT, "packet": REL,
            "scope": "Only the frozen core's preserve() function executes, with explicit current parent/output/packet and exact text transformation. Its admit()/package()/main() functions are never invoked; no predecessor file changes."
        })
    finally:
        write(out / "memory.json", guard.finish())


if __name__ == "__main__":
    main()

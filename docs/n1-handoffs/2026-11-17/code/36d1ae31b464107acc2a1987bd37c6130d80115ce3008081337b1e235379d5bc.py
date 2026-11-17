"""Preserve byte-identical pinned producer copies; never execute or edit originals."""
import sys
from pathlib import Path

sys.path.insert(0, r"C:\Users\stop-\n1-kanji-workspace\review-tools")
from b134_revision_proofs_v1 import ORIGINAL_PRODUCERS, PRODUCERS
from common import freeze_json, require, sha, start_guard, write_frozen

guard, _ = start_guard("B134 preserve coordinator producer pins")
records = {}
try:
    for name, (source, digest) in ORIGINAL_PRODUCERS.items():
        raw = source.read_bytes()
        require(sha(raw) == digest, "Coordinator producer changed: " + str(source))
        target = PRODUCERS[name][0]
        records[name] = {"originalPath": str(source), "copy": write_frozen(target, raw)}
        guard.check()
finally:
    memory = guard.finish()
require(not memory["breach"], "Producer retention RAM breach")
freeze_json(Path(__file__).parent / "coordinator-producers" / "index.json",
            {"copiedOnly": True, "executed": False, "records": records, "memory": memory})

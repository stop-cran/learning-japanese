"""Preserve the first verifier and match the actual signed reading-loader expression."""
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, write_frozen

TOOLS = Path(__file__).resolve().parent
source = frozen(TOOLS / "verify_b133_gates.py",
                "afb55f8731562ba2c7453136fde3d32cf3fddcd7ec22046c7c01a2898a5962ce")
old = b'(PACKET / "reading-keys.json").read_text(encoding="utf-8")'
new = b'(PACKET / "reading-keys.json").read_bytes()'
require(source.count(old) == 1 and new not in source, "Expected single exact loader correction")
successor = source.replace(old, new)
require(successor.replace(new, old) == source, "Non-reversible source change")
tests = frozen(TOOLS / "test_verify_b133_gates.py",
               "15c850fe5f09e586aacb3afcc8f9c29802b9c830f4b395b204aa672599f5c877")
old_import, new_import = b"from verify_b133_gates import (", b"from verify_b133_gates_v2 import ("
require(tests.count(old_import) == 1 and new_import not in tests, "Unexpected test imports")
outputs = [
    write_frozen(TOOLS / "verify_b133_gates_v2.py", successor),
    write_frozen(TOOLS / "test_verify_b133_gates_v2.py", tests.replace(old_import, new_import)),
]
print(freeze_json(WS / "scratch-133" / "review" / "gate-verifier-v2-derivation-001.json", {
    "priorSha256": sha(source), "outputs": outputs,
    "change": "Exact AST contract now uses read_bytes, as the signed producer actually does; no key or result check relaxed.",
    "preservedFailure": "gate-verification-execution-001",
    "limits": "Derivation only; controls and actual candidate verification remain required.",
}))

"""Preserve the first B134 gate verifier and parse quiz totals line-wise (CRLF-safe)."""
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, write_frozen

TOOLS = Path(__file__).resolve().parent
source = frozen(TOOLS / "verify_b134_gates.py",
                "88c39460347a0db48757193a93d587aa2f2bda88bddfc522976c6c839d0adbec")
old = b'totals = re.findall(r"^(\\d+) error\\(s\\), (\\d+) warning\\(s\\)$", log, re.M)'
new = (b'totals = [m.groups() for m in map(re.compile(r"(\\d+) error\\(s\\), (\\d+) warning\\(s\\)").fullmatch,'
       b' log.splitlines()) if m]')
require(source.count(old) == 1 and new not in source, "Expected single exact parser correction")
successor = source.replace(old, new)
require(successor.replace(new, old) == source, "Non-reversible source change")
tests = frozen(TOOLS / "test_verify_b134_gates.py",
               "3d0735ed6b84ae12b3ad0a28d04ad9f70202a231b6611250e73c9d875912ec41")
old_import, new_import = b"from verify_b134_gates import (", b"from verify_b134_gates_v2 import ("
old_case = b'        self.assertEqual(verify_quiz("0 error(s), 0 warning(s)\\n", 0), 0)\n'
new_case = old_case + b'        self.assertEqual(verify_quiz(superseded.replace("\\n", "\\r\\n"), 2), 2)\n'
require(tests.count(old_import) == 1 and tests.count(old_case) == 1 and new_import not in tests,
        "Unexpected test source")
outputs = [
    write_frozen(TOOLS / "verify_b134_gates_v2.py", successor),
    write_frozen(TOOLS / "test_verify_b134_gates_v2.py",
                 tests.replace(old_import, new_import).replace(old_case, new_case)),
]
print(freeze_json(WS / "scratch-134" / "review" / "gate-verifier-v2-derivation-001.json", {
    "priorSha256": sha(source), "outputs": outputs,
    "change": "Quiz-safety totals are full-matched per splitlines() line, so CRLF logs parse; "
              "warning count, kind and zero-error requirements are unchanged. CRLF control added.",
    "preservedFailure": "gate-verification-execution-001",
    "limits": "Derivation only; controls and actual candidate verification remain required.",
}))

import json
import sys
from pathlib import Path
from closure_common import *
from run_b130_gates import CHECKS, run_gate

require(len(sys.argv) == 3 and sys.argv[1] in ("author", "committed"), "Usage: mode NEW_DIRECTORY")
mode, directory = sys.argv[1], HERE / sys.argv[2]
require(directory.parent == HERE and not directory.exists(), "Preserve previous gate attempt")
directory.mkdir()
guard = start_guard()
try:
    head, tree = mode_tree(mode)
    check_delta(tree_entries(PARENT), tree_entries(tree))
    check_archive(guard)
    require(sha(git("show", tree + ":manifest.json")) == MANIFEST_SHA, "Wrong staged manifest")
finally:
    write(directory / "admission.json", {"head": head, "tree": tree, "mode": mode,
                                       "parent": PARENT, "memory": guard.finish()})
expected = None
for name in CHECKS:
    expected = run_gate(name, directory, expected)
guard = start_guard()
try:
    require(mode_tree(mode) == (head, tree) and expected == MANIFEST_SHA, "Closure changed during gates")
finally:
    memory = guard.finish()
summary = {
    "status": "PASS", "mode": mode, "head": head, "tree": tree, "parent": PARENT,
    "checks": list(CHECKS), "commandsUnchanged": True, "serial": True,
    "publishedBaseScope": "f237a8d590a4cb91029bc0b8485163933f44b403",
    "manifestSha256": expected, "finalMemory": memory,
    "runnerSha256": sha(raw(Path(__file__))),
    "gateImplementationSha256": sha(raw(SCRATCH / "run_b130_gates.py")),
    "commonHelperSha256": sha(raw(SCRATCH / "b130_common.py")),
    "closureHelperSha256": sha(raw(HERE / "closure_common.py")),
    "envelope": "Explicit contributor-only child admission. Original ten gate commands/order, full published-base scope, RAM monitoring and bounded cleanup reused unchanged.",
    "logs": {name: {"logSha256": sha(raw(directory / (name + ".log"))),
                    "receiptSha256": sha(raw(directory / (name + ".json")))} for name in CHECKS},
}
write(directory / "summary.json", summary)
print(json.dumps({"status": "PASS", "mode": mode, "tree": tree,
                  "summarySha256": sha(raw(directory / "summary.json"))}))

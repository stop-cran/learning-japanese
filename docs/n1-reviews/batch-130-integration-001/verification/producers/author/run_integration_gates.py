import json
import sys
from pathlib import Path
from integration_common import BASE, FIRST, HERE, SCRATCH, SECOND, git, parents, sha, start_guard, write
from run_b130_gates import CHECKS, run_gate

if len(sys.argv) != 3 or sys.argv[1] not in ("author", "committed"):
    raise SystemExit("usage: run_integration_gates.py author|committed NEW_DIRECTORY_NAME")
mode, directory = sys.argv[1], HERE / sys.argv[2]
assert directory.parent == HERE and not directory.exists()
guard = start_guard()
try:
    head = parents(mode)
    tree = git("write-tree" if mode == "author" else "rev-parse",
               *([] if mode == "author" else ["HEAD^{tree}"])).decode().strip()
    expected_manifest = sha(git("show", (":" if mode == "author" else "HEAD:") + "manifest.json"))
finally:
    admission_memory = guard.finish()
directory.mkdir()
write(directory / "admission.json", {"head": head, "tree": tree, "mode": mode,
                                    "parents": [FIRST, SECOND], "memory": admission_memory})
expected = None
for name in CHECKS:
    expected = run_gate(name, directory, expected)
guard = start_guard()
try:
    assert parents(mode) == head
    assert expected == expected_manifest
    assert not git("diff", "--name-only")
    assert not git("ls-files", "--others", "--exclude-standard")
    assert git("write-tree").decode().strip() == tree
finally:
    memory = guard.finish()
summary = {
    "status": "PASS", "mode": mode, "head": head, "tree": tree,
    "parentsInOrder": [FIRST, SECOND], "publishedBaseScope": BASE,
    "checks": list(CHECKS), "commandsUnchanged": True, "serial": True,
    "manifestSha256": expected,
    "runnerSha256": sha(Path(__file__).read_bytes()),
    "gateImplementationSha256": sha((SCRATCH / "run_b130_gates.py").read_bytes()),
    "commonHelperSha256": sha((SCRATCH / "b130_common.py").read_bytes()),
    "integrationHelperSha256": sha((HERE / "integration_common.py").read_bytes()),
    "envelope": "Only two-parent integration/tree admission changes; the original ten commands/order/published-base scope and resource/cleanup implementation are reused unchanged.",
    "logs": {name: {"logSha256": sha((directory / (name + ".log")).read_bytes()),
                    "receiptSha256": sha((directory / (name + ".json")).read_bytes())} for name in CHECKS},
    "finalMemory": memory,
}
write(directory / "summary.json", summary)
print(json.dumps({"status": "PASS", "mode": mode, "manifestSha256": expected,
                  "summarySha256": sha((directory / "summary.json").read_bytes())}))

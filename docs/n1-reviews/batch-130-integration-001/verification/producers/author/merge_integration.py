import json
import stat
from pathlib import Path
from integration_common import CONTENT, DELTA, FIRST, HERE, REPO, SECOND, command, git, live_target, load, sha, start_guard, write

guard = start_guard()
try:
    assert git("rev-parse", "HEAD").decode().strip() == FIRST
    assert not git("status", "--porcelain=v1", "--untracked-files=all")
    live_target()
    inspection = load(HERE / "inspection-001" / "summary.json")
    for rel in DELTA:
        path = REPO / rel
        assert sha(path.read_bytes()) == inspection["before"][rel]["parentSha256"], rel
        assert not path.stat().st_file_attributes & stat.FILE_ATTRIBUTE_READONLY, (
            "Checked merge target is now read-only; committed bytes already captured, no attribute adjustment attempted", rel)
    code, timed_out, stdout, stderr = command(
        ["git", "-c", "core.quotepath=false", "merge", "--no-ff", "--no-commit", SECOND],
        HERE / "merge-001", guard)
    assert not timed_out
    conflicts = git("diff", "--name-only", "--diff-filter=U").decode().splitlines()
    assert code == 0 or code == 1 and conflicts == ["manifest.json"], (
        code, conflicts, stderr.decode("utf-8", "replace"))
    assert not set(conflicts) - {"manifest.json"}
    assert git("rev-parse", "HEAD").decode().strip() == FIRST
    assert git("rev-parse", "MERGE_HEAD").decode().strip() == SECOND
    if conflicts:
        write(HERE / "merge-001" / "conflicted-manifest.json", (REPO / "manifest.json").read_bytes())
    for rel in CONTENT:
        assert (REPO / rel).read_bytes() == git("show", SECOND + ":" + rel), rel
    write(HERE / "merge-001" / "summary.json", {
        "status": "EXPECTED-MANIFEST-CONFLICT" if conflicts else "MERGED-NO-COMMIT",
        "parentsInOrder": [FIRST, SECOND], "conflicts": conflicts,
        "incomingContentByteExact": True, "attributeChanges": [],
        "producerSha256": sha(Path(__file__).read_bytes()),
    })
    print(json.dumps({"mergeExitCode": code, "conflicts": conflicts}))
finally:
    write(HERE / "merge-001" / "memory.json", guard.finish())

from run_b130_gates import run_gate
directory = HERE / "manifest-resolution-001"
directory.mkdir()
digest = run_gate("manifest", directory, None)
guard = start_guard()
try:
    git("add", "--sparse", "--", *sorted(DELTA))
    assert not git("ls-files", "-u")
    changed = git("diff", "--cached", "--name-only", FIRST).decode().splitlines()
    assert set(changed) == DELTA, changed
    assert not git("diff", "--name-only")
    assert not git("ls-files", "--others", "--exclude-standard")
    for rel in CONTENT:
        assert (REPO / rel).read_bytes() == git("show", SECOND + ":" + rel), rel
    git("-c", "core.whitespace=cr-at-eol", "diff", "--cached", "--check")
    manifest = load(REPO / "manifest.json")
    write(directory / "summary.json", {
        "status": "RESOLVED-BY-UNCHANGED-GENERATOR", "manifestSha256": digest,
        "contentVersion": manifest["contentVersion"], "stagedTree": git("write-tree").decode().strip(),
        "changedPaths": changed, "incomingContentByteExact": True,
    })
    print(json.dumps({"status": "STAGED-INTEGRATION", "paths": changed, "manifestSha256": digest,
                      "contentVersion": manifest["contentVersion"]}))
finally:
    write(directory / "memory.json", guard.finish())

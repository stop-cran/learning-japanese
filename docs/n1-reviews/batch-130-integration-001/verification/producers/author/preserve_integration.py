import importlib.util
import json
import sys
from pathlib import Path
from integration_common import CONTENT, DELTA, FINGERPRINT, FIRST, HERE, REPO, SECOND, git, load, parents, sha, start_guard, tree_entries, write

if len(sys.argv) != 3 or sys.argv[1] not in ("author", "committed"):
    raise SystemExit("usage: preserve_integration.py author|committed NEW_DIRECTORY_NAME")
mode, directory = sys.argv[1], HERE / sys.argv[2]
assert directory.parent == HERE and not directory.exists()
directory.mkdir()
guard = start_guard()
try:
    head = parents(mode)
    tree = git("write-tree").decode().strip()
    before, after = tree_entries(FIRST), tree_entries(tree)
    assert before.keys() == after.keys(), "Tracked membership changed"
    changed = {path for path in before if before[path] != after[path]}
    assert changed == DELTA, changed
    assert all(before[path] == after[path] for path in before if path not in DELTA)
    assert set(git("diff", "--cached", "--name-only", FIRST).decode().splitlines()) == DELTA
    assert not git("diff", "--name-only")
    assert not git("ls-files", "--others", "--exclude-standard")
    incoming = tree_entries(SECOND)
    for path in CONTENT:
        assert after[path] == incoming[path], path
        assert (REPO / path).read_bytes() == git("show", SECOND + ":" + path), path
        assert (REPO / path).read_bytes() == (HERE / "inspection-001" / "incoming-content" / path).read_bytes(), path
    manifest_raw = (REPO / "manifest.json").read_bytes()
    assert manifest_raw == git("show", tree + ":manifest.json")
    manifest = json.loads(manifest_raw)
    first_manifest = json.loads(git("show", FIRST + ":manifest.json"))
    incoming_manifest = json.loads(git("show", SECOND + ":manifest.json"))
    flatten = lambda data: {path: digest for group in data.values() if isinstance(group, dict) for path, digest in group.items()}
    current, previous, second = map(flatten, (manifest, first_manifest, incoming_manifest))
    assert len(current) == len(previous) == 8730
    assert current.keys() == previous.keys()
    assert {path for path in current if current[path] != previous[path]} == CONTENT
    assert manifest.keys() == first_manifest.keys()
    for key in manifest:
        if not isinstance(manifest[key], dict) and key != "contentVersion":
            assert manifest[key] == first_manifest[key]
    runtime = {}
    for path, digest in current.items():
        guard.check()
        raw = (REPO / path).read_bytes()
        normalized = raw.replace(b"\r\n", b"\n") if path.endswith((".md", ".json")) else raw
        actual = sha(normalized)
        assert actual == digest, path
        if path in CONTENT:
            assert digest == second[path], path
        else:
            assert digest == previous[path], path
        runtime[path] = {"firstParent": previous[path], "integrated": digest, "actual": actual,
                         "rawSha256": sha(raw), "unchanged": path not in CONTENT}
        if path in CONTENT:
            runtime[path]["incoming"] = second[path]
    sys.path.insert(0, str(REPO / "tools"))
    spec = importlib.util.spec_from_file_location("integration_manifest_builder", REPO / "tools" / "build_manifest.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    reproduced = (json.dumps(module.build_manifest(REPO), ensure_ascii=False, indent=1, sort_keys=True) + "\n").encode()
    assert reproduced == manifest_raw, "Existing generator does not reproduce exact manifest bytes"
    signature = None
    if mode == "committed":
        git("verify-commit", "HEAD")
        fields = git("show", "-s", "--format=%an%n%ae%n%cn%n%ce%n%GF%n%G?", "HEAD").decode().splitlines()
        assert fields == ["Roman Konstantinovskiy", "stop-cran@list.ru",
                          "Roman Konstantinovskiy", "stop-cran@list.ru", FINGERPRINT, "G"]
        assert "Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>" in git("show", "-s", "--format=%B", "HEAD").decode()
        signature = {"author": fields[:2], "committer": fields[2:4], "fingerprint": fields[4], "status": fields[5]}
    tracked = {path: {"firstParent": before[path], "integrated": after[path], "unchanged": path not in DELTA}
               for path in sorted(before)}
    write(directory / "tracked-blob-comparison.json", tracked)
    write(directory / "runtime-hashes.json", runtime)
    write(directory / "integration.patch", git("diff", FIRST, tree, "--", *sorted(DELTA)))
    assert parents(mode) == head
    assert git("write-tree").decode().strip() == tree
    summary = {
        "status": "PASS", "mode": mode, "head": head, "tree": tree, "parentsInOrder": [FIRST, SECOND],
        "ownerSignature": signature, "exactChangedPaths": sorted(changed),
        "fullTrackedMembershipPreserved": True, "trackedBlobsCompared": len(tracked),
        "allOtherTrackedBlobsAndModesUnchanged": len(tracked) - 3,
        "incomingContentFilesByteExact": True, "runtimeMembershipPreserved": True,
        "runtimeEntries": len(current), "changedRuntimePaths": sorted(CONTENT),
        "otherRuntimeEntriesHashEqual": len(current) - 2,
        "changedRuntimeValuesMatchIncomingManifest": True, "allActualRuntimeHashesChecked": True,
        "manifestSha256": sha(manifest_raw), "contentVersion": manifest["contentVersion"],
        "manifestReproducedByteExactlyByExistingGenerator": True,
        "noN1ContentSupportSourceReviewProgressNotesOrOtherTrackedChanges": True,
        "trackedComparisonSha256": sha((directory / "tracked-blob-comparison.json").read_bytes()),
        "runtimeHashesSha256": sha((directory / "runtime-hashes.json").read_bytes()),
        "integrationPatchSha256": sha((directory / "integration.patch").read_bytes()),
        "producerSha256": sha(Path(__file__).read_bytes()),
        "limits": "Author integration preservation/static evidence only. Prior closure/confirmations remain historical on their exact snapshot; no independent approval of this integrated global manifest, publication/archive/native/device acceptance or delivery credit.",
    }
    write(directory / "summary.json", summary)
    print(json.dumps(summary))
finally:
    write(directory / "memory.json", guard.finish())

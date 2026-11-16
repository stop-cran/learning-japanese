import importlib.util
import hashlib
import json
import sys
from pathlib import Path
from closure_common import *


def verify(mode, directory):
    require(not directory.exists(), "Preserve previous verification")
    directory.mkdir()
    guard = start_guard()
    try:
        head, tree = mode_tree(mode)
        before, after = tree_entries(PARENT), tree_entries(tree)
        added = check_delta(before, after)
        provenance, validation, inventory, provenance_sha, validation_sha = check_archive(guard)
        require(added == {ARCHIVE + "/" + name for name in
                         [*inventory, "provenance.json", "validation-provenance.json"]}, "New staged set differs")
        for path in added:
            data = frozen(REPO / path)
            oid = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
            require(after[path] == {"mode": "100644", "kind": "blob", "blob": oid},
                    "Staged archive blob differs from exact frozen bytes: " + path)
        previous_raw = git("show", PARENT + ":" + LEDGER)
        require(raw(REPO / ARCHIVE / "original-primary-progress.json") == previous_raw,
                "Original primary ledger copy differs")
        current_raw = raw(REPO / LEDGER)
        require(current_raw == git("show", tree + ":" + LEDGER), "Working/staged ledger differs")
        check_ledger(json.loads(previous_raw), json.loads(current_raw), provenance_sha, validation_sha)
        require(not (REPO / LEDGER).stat().st_mode & stat.S_IWRITE, "Ledger was not re-frozen")
        old_metadata = {}
        for name in ("provenance.json", "validation-provenance.json"):
            old_metadata[name] = git("show", PARENT + ":" + OLD + "/" + name)
            require(frozen(REPO / OLD / name) == old_metadata[name], "Old closure metadata bytes changed")
        old_files = {}
        for value in old_metadata.values():
            group = json.loads(value)["recordedFileSha256"]
            require(not old_files.keys() & group.keys(), "Old closure inventory overlaps")
            old_files.update(group)
        require({name.removeprefix(OLD + "/") for name in before if name.startswith(OLD + "/")}
                == set(old_files) | set(old_metadata), "Old closure membership differs")
        for name, digest in old_files.items():
            guard.check()
            frozen(REPO / OLD / name, digest)
        manifest_raw = raw(REPO / "manifest.json", MANIFEST_SHA)
        require(manifest_raw == git("show", PARENT + ":manifest.json")
                == git("show", tree + ":manifest.json"), "Manifest changed")
        manifest = json.loads(manifest_raw)
        entries = {path: digest for value in manifest.values() if isinstance(value, dict)
                   for path, digest in value.items()}
        baseline = json.loads(frozen(
            SCRATCH / "integration-001-author" / "handoff-001" / "evidence" / "committed-preserve-001" / "runtime-hashes.json",
            "3deede7ae09f478353d93c2fbb246fa83b05aec04e4d844c18995231652e5363"))
        require(entries.keys() == baseline.keys() and len(entries) == 8730
                and manifest["contentVersion"] == VERSION, "Runtime membership/version changed")
        runtime = {}
        for path, expected in entries.items():
            guard.check()
            data = raw(REPO / path)
            actual = sha(data.replace(b"\r\n", b"\n") if path.endswith((".md", ".json")) else data)
            require(actual == expected == baseline[path]["integrated"]
                    and sha(data) == baseline[path]["rawSha256"], "Runtime bytes changed: " + path)
            runtime[path] = {"manifestSha256": expected, "actualNormalizedSha256": actual,
                             "rawSha256": sha(data), "parentRawSha256": baseline[path]["rawSha256"]}
        spec = importlib.util.spec_from_file_location("closure_manifest", REPO / "tools" / "build_manifest.py")
        builder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(builder)
        reproduced = (json.dumps(builder.build_manifest(REPO), ensure_ascii=False, indent=1, sort_keys=True) + "\n").encode()
        require(reproduced == manifest_raw, "Actual runtime universe/manifest reproduction differs")
        identities = {path: {"parent": before.get(path), "closure": after[path]} for path in sorted(after)}
        write(directory / "all-tracked-identities.json", identities)
        write(directory / "runtime-hashes.json", runtime)
        write(directory / "new-staged-blobs.json", {path: after[path] for path in sorted(added)})
        write(directory / "closure.patch", git("diff", "--binary", PARENT, tree))
        require(mode_tree(mode) == (head, tree), "Snapshot changed during preservation")
        summary = {
            "status": "PASS", "mode": mode, "head": head, "tree": tree, "parent": PARENT,
            "ownerSignature": signature(head) if mode == "committed" else None,
            "parentTrackedEntries": len(before), "preservedOtherParentBlobsAndModes": len(before) - 1,
            "onlyChangedParentPath": LEDGER, "newFiles": len(added), "newPathRoot": ARCHIVE,
            "oldClosureFilesByteAndModePreserved": len(old_files) + 2,
            "all8730RuntimeMembershipAndRawBytesPreserved": True,
            "manifestSha256": MANIFEST_SHA, "contentVersion": VERSION,
            "ledgerExactAdditiveExtension": True, "ledgerReFrozen": True,
            "provenanceSha256": provenance_sha, "validationProvenanceSha256": validation_sha,
            "trackedInventorySha256": sha(raw(directory / "all-tracked-identities.json")),
            "runtimeInventorySha256": sha(raw(directory / "runtime-hashes.json")),
            "newFilesInventorySha256": sha(raw(directory / "new-staged-blobs.json")),
            "patchSha256": sha(raw(directory / "closure.patch")),
            "producerSha256": sha(raw(Path(__file__))), "limits": LIMITS,
        }
        write(directory / "summary.json", summary)
        print(json.dumps(summary))
    finally:
        write(directory / "memory.json", guard.finish())


if __name__ == "__main__":
    require(len(sys.argv) == 3 and sys.argv[1] in ("author", "committed"), "Usage: mode NEW_DIRECTORY")
    verify(sys.argv[1], HERE / sys.argv[2])

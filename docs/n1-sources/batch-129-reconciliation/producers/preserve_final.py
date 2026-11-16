import hashlib
import json
import sys
from pathlib import Path
from recon_common import *


def tree(ref):
    result = {}
    for row in git("ls-tree", "-rz", ref).split(b"\0"):
        if row:
            meta, name = row.split(b"\t", 1)
            _, kind, oid = meta.split()
            if kind == b"blob":
                result[name.decode()] = oid.decode()
    return result


def blob_oid(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def flat(manifest):
    out = {}
    for value in manifest.values():
        if isinstance(value, dict):
            for path, digest in value.items():
                assert path not in out or out[path] == digest
                out[path] = digest
    return out


if len(sys.argv) != 3 or sys.argv[1] not in ("author", "committed"):
    raise SystemExit("usage: preserve_final.py author|committed NEW_DIRECTORY")
mode, out = sys.argv[1], Path(sys.argv[2]).resolve()
assert out.parent == HERE and not out.exists()
out.mkdir()
guard, result = start_guard(), None
try:
    head = git("rev-parse", "HEAD").decode().strip()
    if mode == "author":
        assert head == PARENT
    else:
        assert git("rev-parse", "HEAD^@").decode().split() == [PARENT]
        assert not git("status", "--porcelain=v1", "--untracked-files=all")
    correction = json.loads((PACKET / "pre-sign-whitespace-revision-002.json").read_text(encoding="utf8"))
    prior_path = HERE / "author-preservation-001" / "summary.json"
    prior_hashes_path = HERE / "author-preservation-001" / "runtime-hashes.json"
    assert sha(prior_path.read_bytes()) == correction["unchangedStructuralProof"]["summarySha256"]
    assert sha(prior_hashes_path.read_bytes()) == correction["unchangedStructuralProof"]["runtimeHashesSha256"]
    prior = json.loads(prior_path.read_text(encoding="utf8"))
    prior_hashes = json.loads(prior_hashes_path.read_text(encoding="utf8"))
    assert prior["status"] == "PASS"
    raw_manifest = (REPO / "manifest.json").read_bytes()
    manifest = json.loads(raw_manifest)
    assert sha(raw_manifest) == prior["manifestSha256"]
    runtime_paths = flat(manifest)
    assert set(runtime_paths) == set(prior_hashes)
    parent_tree = tree(PARENT)
    committed_tree = tree("HEAD") if mode == "committed" else None
    parent_runtime = flat(json.loads(git("show", f"{PARENT}:manifest.json")))
    original_runtime = flat(json.loads(git("show", f"{BASE}:manifest.json")))
    assert set(runtime_paths) == set(parent_runtime)
    changed = {p for p in runtime_paths if runtime_paths[p] != parent_runtime[p]}
    assert changed == {"kanji/絹.md", "kanji/虹.md"}
    runtime = {}
    for path, digest in runtime_paths.items():
        guard.check()
        raw = (REPO / path).read_bytes()
        normal = raw.replace(b"\r\n", b"\n") if path.endswith((".md", ".json")) else raw
        assert sha(normal) == digest
        runtime[path] = {"runtimeSha256": digest, "rawSha256": sha(raw), "gitBlob": blob_oid(raw)}
        assert runtime[path] == prior_hashes[path], ("Changed since full structural proof", path)
        if path not in changed:
            assert runtime[path]["gitBlob"] == parent_tree[path]
        if committed_tree is not None:
            assert runtime[path]["gitBlob"] == committed_tree[path]
    original_packet_paths = [p for p in parent_tree if p.startswith("docs/n1-sources/batch-129/")]
    for path in original_packet_paths:
        guard.check()
        assert blob_oid((REPO / path).read_bytes()) == parent_tree[path]
    initial_inventory = json.loads((PACKET / "evidence-inventory-001.json").read_text(encoding="utf8"))
    assert sha((PACKET / "evidence-inventory-001.json").read_bytes()) == correction["preservedInventory001Sha256"]
    for name, digest in initial_inventory["files"].items():
        assert sha((PACKET / name).read_bytes()) == digest
    inventory_path = PACKET / "evidence-inventory-002.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf8"))
    packet_files = {str(p.relative_to(PACKET)).replace("\\", "/"): p for p in PACKET.rglob("*") if p.is_file()}
    assert inventory["supersedesForFinalBinding"] == "evidence-inventory-001.json"
    assert set(inventory["files"]) == set(packet_files) - {"evidence-inventory-002.json"}
    for name, digest in inventory["files"].items():
        assert sha(packet_files[name].read_bytes()) == digest
    frozen = json.loads((PACKET / "frozen-input-bindings.json").read_text(encoding="utf8"))
    for item in frozen["inputs"]:
        assert sha(Path(item["path"]).read_bytes()) == item["sha256"]
    external = json.loads((PACKET / "external-source-bindings.json").read_text(encoding="utf8"))
    for source in external["comparisonsAndExactFollowupNoun"].values():
        path = Path(source["localRawCapture"])
        assert sha(path.read_bytes()) == source["rawSha256"]
        assert sha(path.with_suffix(".json").read_bytes()) == source["allArticleJsonSha256"]
        assert sha(path.with_suffix(".txt").read_bytes()) == source["selectedCompleteArticleTextSha256"]
    expected_paths = json.loads((PACKET / "changed-file-inventory-002.json").read_text(encoding="utf8"))["paths"]
    actual_paths = set(git("diff", "--name-only", PARENT).decode().splitlines()) | set(git("ls-files", "--others", "--exclude-standard").decode().splitlines())
    assert actual_paths == set(expected_paths)
    assert actual_paths == {"kanji/絹.md", "kanji/虹.md", "manifest.json"} | {str(p.relative_to(REPO)).replace("\\", "/") for p in packet_files.values()}
    if committed_tree is not None:
        for path, oid in parent_tree.items():
            if path not in {"kanji/絹.md", "kanji/虹.md", "manifest.json"}:
                assert committed_tree[path] == oid, path
        assert set(committed_tree) - set(parent_tree) == {str(p.relative_to(REPO)).replace("\\", "/") for p in packet_files.values()}
        assert raw_manifest == git("show", "HEAD:manifest.json")
    assert not git("ls-tree", "-r", "--name-only", PARENT, "--", "kanji/網.md")
    result = {
        "status": "PASS", "mode": mode, "head": head, "requiredParent": PARENT, "originalBatchBase": BASE,
        "allManifestGroupsChecked": [k for k, v in manifest.items() if isinstance(v, dict)],
        "parentRuntimeEntries": len(parent_runtime), "candidateRuntimeEntries": len(runtime),
        "allRuntimeHashesChecked": len(runtime), "allRuntimeRawBytesEqualFullStructuralProof": True,
        "unchangedRuntimeRawBlobChecks": len(runtime) - len(changed),
        "addedRuntimePaths": [], "removedRuntimePaths": [], "changedRuntimePaths": sorted(changed),
        "originalBaselineRuntimeEntries": len(original_runtime),
        "originalBaselineUnchangedRuntimeEntries": sum(original_runtime[p] == runtime_paths[p] for p in original_runtime),
        "allOldPacketRawBlobsUnchanged": len(original_packet_paths),
        "allInitialReconciliationPacketBytesUnchanged": len(initial_inventory["files"]) + 1,
        "inheritedStructuralProof": correction["unchangedStructuralProof"],
        "structuralProofTransfer": "Every one of8724 current raw/runtime hashes exactly equals the complete initial proof. Therefore its ordered metadata, original-body preservation, three byte-identical wrappers, direct pairs, complete source-canonical and baseline identity proofs still apply. The only later additions are contributor evidence.",
        "finitePairs": prior["finitePairs"], "newDirectGuards": prior["newDirectGuards"],
        "supportWordProofs": prior["supportWordProofs"],
        "frozenInputHashesVerified": len(frozen["inputs"]), "localCapturesUnchanged": True,
        "manifestSha256": sha(raw_manifest), "contentVersion": manifest["contentVersion"],
        "finalInventorySha256": sha(inventory_path.read_bytes()), "finalInventoryOtherFiles": len(inventory["files"]),
        "exactChangedPaths": expected_paths, "producerSha256": sha(Path(__file__).read_bytes()),
        "limits": prior["limits"],
    }
    write(out / "runtime-hashes.json", runtime)
finally:
    active_error = sys.exc_info()[1]
    memory = guard.finish()
    write(out / "memory.json", memory)
    if active_error is None and result is not None:
        assert not memory["breach"]
        result["memory"] = memory
        result["runtimeHashesSha256"] = sha((out / "runtime-hashes.json").read_bytes())
        write(out / "summary.json", result)
        print(json.dumps({k: v for k, v in result.items() if k != "exactChangedPaths"}, ensure_ascii=False))
    else:
        write(out / "failure.json", {"error": str(active_error), "memory": memory})

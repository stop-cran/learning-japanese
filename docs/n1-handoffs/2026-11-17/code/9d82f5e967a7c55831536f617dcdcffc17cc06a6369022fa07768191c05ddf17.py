"""Verify signed B129 correction evidence before original-reviewer confirmations."""
import difflib
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path

import b129_revision_gates as gates
import b129_revision_pairs as pairs
from common import freeze_json, frozen, require, sha, start_guard, write_frozen
from verify_b129_payload import runtime_entries
from verify_b129_revision_runtime import ADJUDICATION_SHA, BASE, PARENT, PREFIX, REPO, REVIEW, RUNNER
from verify_b129_sources import FINGERPRINT, Git, ORIGIN, OWNER, TRAILER

HERE = REVIEW.parent / "reconciliation-001"
HELPERS = {
    "b129_revision_gates.py": "4e4b638c43d6f7a1d928208a0d09fe31e06e22d7d1c0091af6aff1ed6e3e2e25",
    "b129_revision_pairs.py": "5b7ee9f022ba17c485fd08f8c4276a6d6ec664a58adfde12b59f32c9c6d608bd",
}


def tree(git, revision):
    result = {}
    for row in git("ls-tree", "-r", "-z", revision).split(b"\0"):
        if row:
            meta, name = row.split(b"\t", 1)
            mode, kind, oid = meta.decode().split()
            require(kind == "blob", "Unexpected non-blob tree entry")
            result[name.decode("utf-8")] = (mode, oid)
    return result


def blob_oid(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def check_teaching(blob):
    patch, result = [], {}
    for character, expected_count in (("\u7d79", 1), ("\u8679", 3)):
        path = f"kanji/{character}.md"
        before = blob(path, PARENT).decode("utf-8").replace("\r\n", "\n")
        after = blob(path).decode("utf-8").replace("\r\n", "\n")
        old_line = re.search(r"^quiz_exclusions:.*$", before, re.M).group()
        new_line = re.search(r"^quiz_exclusions:.*$", after, re.M).group()
        restored = after.replace(new_line, old_line, 1)
        old_lines, new_lines = before.splitlines(keepends=True), restored.splitlines(keepends=True)
        inserted = []
        for operation, _, _, start, end in difflib.SequenceMatcher(
                None, old_lines, new_lines, autojunk=False).get_opcodes():
            if operation != "equal":
                require(operation == "insert" and all(line.startswith("- ") for line in new_lines[start:end]),
                        "Existing card body changed")
                inserted.extend(new_lines[start:end])
        require(len(inserted) == expected_count, "Teaching delta differs")
        result[path] = inserted
        patch.extend(difflib.unified_diff(before.splitlines(keepends=True), after.splitlines(keepends=True),
                                          fromfile=PARENT + ":" + path, tofile="candidate:" + path))
    require("".join(patch).encode() == blob(PREFIX + "teaching-diff.patch"), "Saved teaching diff differs")
    return result


def main(candidate, runtime_sha, source_sha, output_name):
    output = Path(output_name).resolve()
    require(output.parent == REVIEW and not output.exists(), "Use a new evidence output directory")
    for name, digest in HELPERS.items():
        frozen(Path(__file__).with_name(name), digest)
    runtime_path, source_path = REVIEW / "revision-runtime-proof-001.json", REVIEW / "revision-source-proof-001.json"
    runtime = json.loads(frozen(runtime_path, runtime_sha))
    sources = json.loads(frozen(source_path, source_sha))
    require(runtime["status"] == "PASS_RUNTIME_ONLY"
            and sources["status"] == "PASS_COMPLETE_SOURCES_ONLY"
            and runtime["candidate"] == sources["candidate"] == candidate
            and runtime["parent"] == sources["parent"] == PARENT
            and gates.memory_ok(runtime["memory"]) and gates.memory_ok(sources["memory"]),
            "Proofs do not bind the same signed correction")
    for name, proof in (("verify_b129_revision_runtime.py", runtime),
                        ("verify_b129_revision_sources.py", sources)):
        frozen(Path(__file__).with_name(name), proof["producerSha256"])
    guard, _ = start_guard("B129 signed correction evidence")
    git = Git(REPO, RUNNER, guard)
    captures = {}

    def clean():
        require(git("rev-parse", "HEAD").decode().strip() == candidate
                and not git("status", "--porcelain=v1", "--untracked-files=all"),
                "Signed correction checkout changed")

    def blob(path, revision=candidate):
        raw = git("show", f"{revision}:{path}")
        if revision == candidate:
            require((REPO / path).read_bytes() == raw, f"Signed worktree bytes differ: {path}")
        return raw

    try:
        clean()
        require(not git("ls-tree", candidate, "--", "kanji/\u7db2.md"),
                "Previously absent comparison card is now present")
        require(git("remote", "get-url", "origin").decode().strip() == ORIGIN
                and git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", candidate).decode().strip()
                == f"{PARENT}|G|{FINGERPRINT}|{OWNER}|{OWNER}"
                and TRAILER in git("show", "-s", "--format=%B", candidate),
                "Signature, parent, origin or identity differs")
        before, after = tree(git, PARENT), tree(git, candidate)
        modified = {"kanji/\u7d79.md", "kanji/\u8679.md", "manifest.json"}
        require(all(after.get(path) == record for path, record in before.items() if path not in modified),
                "An inherited file was changed outside the correction")
        added = set(after) - set(before)
        require(added and all(path.startswith(PREFIX) for path in added), "Out-of-scope added path")
        inventory_raw = blob(PREFIX + "evidence-inventory-002.json")
        inventory = json.loads(inventory_raw)
        require(inventory["parent"] == PARENT and inventory["selfExcluded"] == "evidence-inventory-002.json"
                and inventory["supersedesForFinalBinding"] == "evidence-inventory-001.json"
                and added == {PREFIX + name for name in inventory["files"]} |
                {PREFIX + "evidence-inventory-002.json"}, "Incomplete signed evidence inventory")
        for name, digest in inventory["files"].items():
            require(sha(blob(PREFIX + name)) == digest, f"Inventory hash differs: {name}")
            guard.check()
        initial = json.loads(blob(PREFIX + "evidence-inventory-001.json"))
        require(initial["selfExcluded"] == "evidence-inventory-001.json"
                and all(inventory["files"].get(name) == digest for name, digest in initial["files"].items()),
                "Initial reconciliation evidence was not preserved")
        old_inventory = initial["additiveTo"]
        require(old_inventory["path"] == pairs.ORIGINAL + "evidence-inventory-003.json"
                and sha(blob(old_inventory["path"])) == old_inventory["sha256"],
                "Original evidence inventory differs")
        changes = json.loads(blob(PREFIX + "changed-file-inventory-002.json"))
        require(changes["parent"] == PARENT and len(changes["paths"]) == len(set(changes["paths"]))
                and set(changes["paths"]) == added | modified, "Signed changed-path inventory differs")
        for name, digest in sources["signedBindings"].items():
            require(sha(blob(PREFIX + name)) == digest, "Complete source proof binding changed")
        for path, digest in runtime["signedArtifacts"].items():
            require(sha(blob(path)) == digest, "Runtime proof binding changed")
        plan = json.loads(blob(PREFIX + "validation-plan.json"))
        require(plan["parent"] == PARENT and plan["batchScopeBase"] == BASE
                and plan["serialGateOrder"] == list(gates.ORDER)
                and plan["commands"] == {name: ["python", "-B", *map(str, args)]
                                         for name, args in gates.commands().items()},
                "Signed validation plan changed")
        for name, digest in plan["producerHashes"].items():
            path = (REVIEW.parent if Path(name).name in {"b129_common.py", "extract_b129.py"} else HERE)
            require(sha(blob(PREFIX + name)) == digest
                    and (path / Path(name).name).read_bytes() == blob(PREFIX + name),
                    f"Executed producer differs: {name}")
        for path, digest in plan["toolHashes"].items():
            require(sha(Path(path).read_bytes()) == digest, f"Executed gate tool differs: {path}")
        final_plan = json.loads(blob(PREFIX + "validation-plan-002.json"))
        require(final_plan["supersedesForFinalBinding"] == "validation-plan.json"
                and final_plan["sameSerialTenGateCommands"] == "validation-plan.json"
                and final_plan["unchangedTenGateRunnerSha256"] ==
                inventory["files"]["producers/run_gates.py"]
                and final_plan["authorDirectories"] ==
                [str(HERE / "author-gates-002"), str(HERE / "author-preservation-002")]
                and final_plan["committedDirectories"] ==
                [str(HERE / "committed-gates-001"), str(HERE / "committed-preservation-001")],
                "Final execution plan differs")
        for name, digest in final_plan["producerHashes"].items():
            require(sha(blob(PREFIX + "producers/" + name)) == digest
                    and (HERE / name).read_bytes() == blob(PREFIX + "producers/" + name),
                    f"Final executed producer differs: {name}")
        correction = json.loads(blob(PREFIX + "pre-sign-whitespace-revision-002.json"))
        require(correction["parent"] == PARENT and correction["preservedInventory001Sha256"] ==
                sha(blob(PREFIX + "evidence-inventory-001.json")), "Preflight correction binding differs")
        failure_raw = Path(correction["failure"]["path"]).read_bytes()
        failure = json.loads(failure_raw)
        require(sha(failure_raw) == correction["failure"]["sha256"]
                and failure["exitCode"] is None and failure["stalled"] is False
                and correction["failure"]["commitOrGpgProcessLaunched"] is False,
                "Initial pre-sign failure differs")
        captures["pre-sign/failure.json"] = failure_raw
        patch_path = PREFIX + "teaching-diff.patch"
        patch = blob(patch_path)
        whitespace = correction["whitespace"]
        trailing = [index for index, line in enumerate(patch.splitlines(), 1)
                    if line != line.rstrip(b" \t")]
        require(trailing == whitespace["acceptedPatchLines"] == [10, 18, 29, 40]
                and all(patch.splitlines()[index - 1] == b" " for index in trailing)
                and sha(patch) == whitespace["patchSha256"], "Patch-syntax exception widened")
        expected_diagnostic = "".join(f"{patch_path}:{index}: trailing whitespace.\n+ \n"
                                      for index in trailing)
        require(whitespace["fullCheck"]["exitCode"] == 2
                and whitespace["fullCheck"]["stdout"] == expected_diagnostic
                and whitespace["fullCheck"]["stdoutSha256"] == sha(expected_diagnostic.encode())
                and whitespace["allOtherStagedFilesCheck"]["exitCode"] == 0,
                "Recorded whitespace diagnostic differs")
        git("-c", "core.whitespace=cr-at-eol", "diff", "--check", PARENT, candidate,
            "--", ".", ":(exclude)" + patch_path)
        gate_sets = {}
        for mode, name in (("author", "author-gates-002"), ("committed", "committed-gates-001")):
            directory = HERE / name
            record, files = gates.verify(
                directory, mode, candidate, runtime["manifestSha256"],
                inventory["files"]["producers/run_gates.py"],
                inventory["files"]["producers/b129_common.py"],
                inventory["files"]["producers/recon_common.py"], guard)
            gate_sets[mode] = record
            captures.update({f"{mode}-gates/{name}": raw for name, raw in files.items()})
        require(datetime.fromisoformat(gate_sets["committed"]["firstStartedAt"]) >=
                datetime.fromisoformat(gate_sets["author"]["lastCompletedAt"]),
                "Author and committed gates overlap")
        manifest_raw = blob("manifest.json")
        entries = runtime_entries(json.loads(manifest_raw))
        require(sha(manifest_raw) == runtime["manifestSha256"] and len(entries) == runtime["runtimeEntries"],
                "Signed runtime manifest differs")
        runtime_hashes = {}
        for path, (digest, binary) in entries.items():
            raw = (REPO / path).read_bytes()
            oid = blob_oid(raw)
            require(oid == after[path][1] and sha(raw if binary else raw.replace(b"\r\n", b"\n")) == digest,
                    f"Runtime bytes differ from signed tree: {path}")
            runtime_hashes[path] = {"runtimeSha256": digest, "rawSha256": sha(raw), "gitBlob": oid}
            guard.check()
        teaching = check_teaching(blob)
        structural = correction["unchangedStructuralProof"]
        structural_raw = Path(structural["path"]).read_bytes()
        structural_hashes = Path(structural["runtimeHashesPath"]).read_bytes()
        require(sha(structural_raw) == structural["summarySha256"]
                and sha(structural_hashes) == structural["runtimeHashesSha256"]
                and json.loads(structural_raw)["status"] == "PASS"
                and json.loads(structural_hashes) == runtime_hashes,
                "Initial structural proof no longer applies")
        captures["original-structural/summary.json"] = structural_raw
        captures["original-structural/runtime-hashes.json"] = structural_hashes
        preservation = {}
        for mode, name in (("author", "author-preservation-002"), ("committed", "committed-preservation-001")):
            directory = HERE / name
            require({p.name for p in directory.iterdir()} == {"summary.json", "memory.json", "runtime-hashes.json"},
                    "Preservation file set differs")
            files = {name: (directory / name).read_bytes() for name in
                     ("summary.json", "memory.json", "runtime-hashes.json")}
            summary = json.loads(files["summary.json"])
            require(summary["status"] == "PASS" and summary["mode"] == mode
                    and summary["head"] == (PARENT if mode == "author" else candidate)
                    and summary["requiredParent"] == PARENT and summary["originalBatchBase"] == BASE
                    and summary["manifestSha256"] == runtime["manifestSha256"]
                    and summary["finalInventorySha256"] == sha(inventory_raw)
                    and summary["producerSha256"] == inventory["files"]["producers/preserve_final.py"]
                    and summary["runtimeHashesSha256"] == sha(files["runtime-hashes.json"])
                    and json.loads(files["runtime-hashes.json"]) == runtime_hashes
                    and json.loads(files["memory.json"]) == summary["memory"]
                    and gates.memory_ok(summary["memory"]), "Preservation proof differs")
            captures.update({f"{mode}-preservation/{name}": raw for name, raw in files.items()})
            preservation[mode] = {"directory": str(directory),
                                  "files": {name: sha(raw) for name, raw in files.items()}}
        sys.path.insert(0, str(gates.WS / "lean"))
        from n1lib import parse
        metadata = {char: parse(blob(f"kanji/{char}.md").decode("utf-8").replace("\r\n", "\n"))[0]
                    for char in ("\u7d79", "\u8679")}
        adjudication = json.loads(frozen(REVIEW / "N1-B129-GPT-001-adjudication.json", ADJUDICATION_SHA))
        pair_proof = pairs.verify(blob, adjudication, metadata, guard)
        for char, added_guards in pair_proof["addedGuards"].items():
            require(added_guards == runtime["cardMetadata"][char]["addedGuards"],
                    "Pair decisions differ from exact runtime suffix")
        clean()
    finally:
        memory = guard.finish()
    require(gates.memory_ok(memory), "Evidence verification RAM guard breached")
    captured = {name: write_frozen(output / name, raw) for name, raw in sorted(captures.items())}
    print(json.dumps(freeze_json(output / "verification.json", {
        "batch": 129, "status": "PASS_MECHANICAL_ONLY", "candidate": candidate, "parent": PARENT,
        "base": BASE, "signature": runtime["signature"], "runtimeEntries": len(entries),
        "runtimeChanged": runtime["runtimeChanged"], "manifestSha256": runtime["manifestSha256"],
        "contentVersion": runtime["contentVersion"], "inventorySha256": sha(inventory_raw),
        "changedPaths": sorted(added | modified), "preservedInheritedFiles": len(before) - len(modified),
        "runtimeProof": {"path": str(runtime_path), "sha256": runtime_sha},
        "sourceProof": {"path": str(source_path), "sha256": source_sha},
        "pairProof": pair_proof, "gateSets": gate_sets, "preservation": preservation,
        "teachingInsertions": teaching,
        "capturedEvidence": captured, "memory": memory,
        "producerSha256": sha(Path(__file__).read_bytes()),
        "helperSha256": HELPERS, "absentComparison": "kanji/\u7db2.md",
        "reviewAccepted": False, "publicationAccepted": False,
        "limits": "Signed bytes, complete source binding, finite dispositions, preservation and "
                  "host execution only. Original-reviewer semantic confirmations remain mandatory. "
                  "No retrospective initial-review, native/device, arbitrary-pool or publication acceptance.",
    })))


if __name__ == "__main__":
    require(len(sys.argv) == 5, "Usage: verify_b129_revision_evidence.py CANDIDATE RUNTIME_SHA SOURCE_SHA OUTPUT")
    main(*sys.argv[1:])

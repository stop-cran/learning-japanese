"""Bind the actual B130 signed reconciliation without accepting its semantics."""
import json
import re
import sys
from datetime import datetime
from pathlib import Path

import b130_revision_gates as gates
import b130_revision_pairs as pairs
from b130_signed_evidence import verify_reading_keys
from common import GUARD_SHA, WS, freeze_json, frozen, require, sha, start_guard, write_frozen
from verify_b130_payload import REPO, RUNNER, runtime_entries
from verify_b130_revision_runtime_v3 import BASE, MEMBERS, PARENT, PREFIX, ROOT
from verify_b130_sources import FINGERPRINT, Git, ORIGIN, OWNER, TRAILER

ORIGINAL = "docs/n1-sources/batch-130/"
HELPERS = {
    "b130_revision_gates.py": "3a9c1baa713bdce7e7380a120d42fdafa46733f2b1b0c890cf0a51f227e7e0f7",
    "b130_revision_pairs.py": "be22c0ca3b944b0878b2a806b0f844f3cb0b1ea259466c514eec3a4451b2c57c",
    "b130_signed_evidence.py": "4b5e6ca8d73f16267e888ec512f9fc6839fcb82b563c45218fb71e7ef45a35ba",
    "verify_b130_revision_runtime_v3.py": "8ef584f020b1a9b939be2a70e422854c42f85a7b02e2f27ce23cafe0837b0e48",
    "verify_b130_revision_sources.py": "ada1659a99fce8464475ba623767b3fccd7319d93e4a77d168a243193f443605",
}
PROOFS = {
    "runtime": ("revision-runtime-proof-001.json", "4bcc85598f49936f731fb184f16e5614d6f2bd77ff910361852abbcb9bf345a2"),
    "sources": ("revision-source-proof-001.json", "6b8fc5bbfc0b8a6dacff71ae5ac677e57466e3680d1db4bb125e684434aa3995"),
    "external": ("revision-external-observation-001/manifest.json",
                 "fd31a4ba17e1b00941ae20cafd5c5bfbfc9832be7ba77e65ef0e64818f0d9194"),
}
HANDOFF_SHA = "4dc8b0ef836012d993c3cb534afa61eff55dff851bd526a012c9c6ea111b2354"


def check_inventory(inventory, prior, changed):
    require(inventory["selfExcluded"] is True and prior["selfExcluded"] is True
            and inventory["supersedesInventoryAsActiveBindingOnly"] == "evidence-inventory.json"
            and len(inventory["files"]) == 103 and len(prior["files"]) == 73,
            "Reconciliation inventory schema differs")
    require({path for path in changed if path.startswith(PREFIX)}
            == {PREFIX + name for name in inventory["files"]} | {PREFIX + "evidence-inventory-002.json"},
            "Signed packet inventory is incomplete")
    require(all(inventory["files"].get(name) == digest for name, digest in prior["files"].items()),
            "Earlier reconciliation inventory was rewritten")


def check_progress(progress, runtime, pair_proof, inventory_sha, warnings):
    require(progress["batch"] == 130 and progress["revision"] == "reconciliation-001"
            and progress["status"] == "local-author-successor-awaiting-independent-confirmation"
            and progress["parent"] == PARENT and progress["publishedBase"] == BASE
            and progress["members"] == MEMBERS and progress["sourceRows"] == [191, 419, 879]
            and (progress["publishedDelivered"], progress["undelivered"], progress["frozenTotal"],
                 progress["localUnpublishedDrafts"]) == (261, 967, 1228, 3)
            and progress["deliveryNotIncremented"] is True
            and progress["historicalOpenQuestionsPreserved"] == 24
            and progress["historicalAndRareSpellingAllocationResolved"] is False
            and progress["authorOpenQuizHolds"] == pair_proof["authorOpenQuizHolds"]
            and progress["manifestSha256"] == runtime["manifestSha256"]
            and progress["contentVersion"] == runtime["contentVersion"]
            and progress["newEvidenceInventorySha256"] == inventory_sha
            and progress["warnings"]["quizSafetyCount"] == len(warnings) == 83
            and progress["warnings"]["quizSafetyWarnings"] == warnings,
            "Progress changed its accounting, source uncertainty, warnings or acceptance boundary")
    require(all(progress["newGuards"][char] == runtime["cardMetadata"][char]["addedGuards"]
                and set(progress["newGuards"][char]) == set(pair_proof["claimedDirectGuards"][char])
                for char in MEMBERS), "Progress guard inventory differs")


def main(candidate, output_name):
    output = Path(output_name).resolve()
    require(output.parent == ROOT and not output.exists(), "Use a new direct B130 evidence directory")
    for name, digest in HELPERS.items():
        frozen(Path(__file__).with_name(name), digest)
    proofs = {key: json.loads(frozen(ROOT / name, digest)) for key, (name, digest) in PROOFS.items()}
    runtime, sources, external = (proofs[key] for key in ("runtime", "sources", "external"))
    require(runtime["status"] == "PASS_RUNTIME_ONLY"
            and sources["status"] == "PASS_COMPLETE_SOURCES_ONLY"
            and runtime["candidate"] == sources["candidate"] == candidate
            and runtime["parent"] == sources["parent"] == PARENT
            and runtime["claimResolutionAccepted"] is False
            and all(not item["reviewAccepted"] and not item["publicationAccepted"]
                    and gates.memory_ok(item["memory"]) for item in proofs.values()),
            "Proofs do not bind the same unaccepted signed correction")
    for name, item in (("verify_b130_revision_runtime_v3.py", runtime),
                       ("verify_b130_revision_sources.py", sources),
                       ("prepare_b130_revision_external.py", external)):
        frozen(Path(__file__).with_name(name), item["producerSha256"])
    handoff_dir = ROOT / "revision-handoff-capture-001"
    handoff = json.loads(frozen(handoff_dir / "handoff.json", HANDOFF_SHA))
    changed = json.loads(frozen(handoff_dir / "changed-files.json", handoff["exactChangedFiles"]["sha256"]))
    require(changed["candidate"] == handoff["candidate"] == candidate
            and changed["parent"] == handoff["parent"] == PARENT
            and len(changed["files"]) == len(set(changed["files"])) == changed["count"] == 111
            and set(changed["files"]) == set(runtime["changedPaths"])
            and changed["committedBlobSha256"] == runtime["signedArtifacts"],
            "Handoff changed-file inventory differs from the verified runtime proof")
    guard, _ = start_guard("B130 signed reconciliation evidence verification")
    git = Git(REPO, RUNNER, guard)
    captures, cache = {}, {}

    def clean():
        require(git("rev-parse", "HEAD").decode().strip() == candidate
                and not git("status", "--porcelain=v1", "--untracked-files=all"),
                "Signed successor checkout changed")

    def blob(path, revision=candidate):
        key = (revision, path)
        if key not in cache:
            cache[key] = git("show", f"{revision}:{path}")
        raw = cache[key]
        if revision == candidate:
            require((REPO / path).read_bytes() == raw, "Worktree differs from signed blob: " + path)
        guard.check()
        return raw

    def capture_group(name):
        group = handoff["serialGateAndPreservationEvidence"][name]
        directory = Path(group["directory"])
        require(directory == ROOT.parent / name and
                {path.name for path in directory.iterdir()} == set(group["files"]),
                "Unexpected execution directory inventory")
        files = {name: (directory / name).read_bytes() for name in group["files"]}
        require(all(sha(raw) == group["files"][name] for name, raw in files.items())
                and sha(files["summary.json"]) == group["summarySha256"], "Handoff execution binding differs")
        captures.update({f"{name}/{filename}": raw for filename, raw in files.items()})
        return files

    try:
        clean()
        require(git("remote", "get-url", "origin").decode().strip() == ORIGIN
                and git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", candidate).decode().strip()
                == f"{PARENT}|G|{FINGERPRINT}|{OWNER}|{OWNER}"
                and TRAILER in git("show", "-s", "--format=%B", candidate), "Signed identity differs")
        parts = git("diff", "--name-status", "--no-renames", "-z", PARENT, candidate).decode().split("\0")
        require(dict(zip(parts[1:-1:2], parts[:-1:2])) == runtime["changedPaths"], "Signed delta differs")
        for path, (_, raw) in zip(changed["files"], git.objects(
                [f"{candidate}:{path}" for path in changed["files"]])):
            cache[(candidate, path)] = raw
            require(sha(blob(path)) == runtime["signedArtifacts"][path], "Signed artifact changed")
        inventory_raw = blob(PREFIX + "evidence-inventory-002.json")
        inventory = json.loads(inventory_raw)
        prior = json.loads(blob(PREFIX + "evidence-inventory.json"))
        check_inventory(inventory, prior, changed["files"])
        require(sha(inventory_raw) == handoff["packetInventory"]["sha256"], "Active inventory differs")
        for name, digest in inventory["files"].items():
            require(sha(blob(PREFIX + name)) == digest, "Signed packet binding differs: " + name)
        original_raw = blob(ORIGINAL + "evidence-inventory.json")
        original = json.loads(original_raw)
        require(sha(original_raw) == handoff["originalInventory"]["sha256"]
                and original["selfExcluded"] is True and len(original["files"]) == 306,
                "Original packet inventory differs")
        names = [ORIGINAL + name for name in original["files"]]
        require(len(git("ls-tree", "-r", "--name-only", candidate, "--", ORIGINAL).splitlines()) == 307,
                "Original packet membership changed")
        for path, (_, raw) in zip(names, git.objects([f"{candidate}:{name}" for name in names])):
            cache[(candidate, path)] = raw
            require(sha(blob(path)) == original["files"][path[len(ORIGINAL):]], "Original evidence changed")
        for name, digest in sources["signedBindings"].items():
            path = sources["signedProducer"] if name == "reconcile_sources_b130.py" else PREFIX + name
            require(sha(blob(path)) == digest, "Complete source proof binding differs")
        for group in ("neutralSourceAndPairEvidence", "isolatedResponsesAndMappings"):
            for name, digest in handoff[group].items():
                require(sha(blob(PREFIX + name)) == digest, "Handoff source/response binding differs")
        pair_proof = pairs.verify(lambda name: blob(PREFIX + name), lambda char: blob(f"kanji/{char}.md"))
        bindings = json.loads(blob(PREFIX + "tool-bindings.json"))
        require(bindings["guardSha256"] == GUARD_SHA, "Executed guard differs")
        for name, binding in bindings["dependencies"].items():
            require(Path(binding["scratchPath"]) == ROOT.parent / name
                    and binding["immutableOriginalProducer"] == "batch-130/producers/" + name
                    and sha(blob(ORIGINAL + "producers/" + name)) == binding["sha256"]
                    and Path(binding["scratchPath"]).read_bytes() == blob(ORIGINAL + "producers/" + name),
                    "Executed original dependency differs")
        for name, digest in bindings["leanTools"].items():
            require(sha((WS / "lean" / name).read_bytes()) == digest, "Executed lean tool differs")
        for name in ("reconcile_sources_b130.py", "reconcile_decisions_b130.py",
                     "reconcile_external_b130.py", "reconcile_responses_b130.py",
                     "run_b130_reconciliation_gates.py", "package_b130_reconciliation_002.py",
                     "preserve_b130_reconciliation_002.py"):
            scratch_name = "preserve_b130_reconciliation.py" if name.endswith("_002.py") and name.startswith("preserve") else name
            require((ROOT.parent / scratch_name).read_bytes() == blob(PREFIX + "producers/" + name),
                    "Active producer differs: " + name)
        gate_sets = {}
        for mode, name in (("author", "reconciliation-author-gates-002"),
                           ("committed", "reconciliation-committed-gates-001")):
            files = capture_group(name)
            record, checked = gates.verify(
                ROOT.parent / name, mode, candidate, runtime["manifestSha256"],
                inventory["files"]["producers/run_b130_reconciliation_gates.py"],
                bindings["dependencies"]["run_b130_gates.py"]["sha256"],
                bindings["dependencies"]["b130_common.py"]["sha256"], guard)
            require(files == checked, "Gate evidence changed during verification")
            if mode == "author":
                require(all(raw == blob(PREFIX + f"author-evidence/{name}/{file}")
                            for file, raw in files.items()), "Signed author execution copy differs")
            gate_sets[mode] = record
        require(datetime.fromisoformat(gate_sets["committed"]["firstStartedAt"]) >=
                datetime.fromisoformat(gate_sets["author"]["lastCompletedAt"]), "Gate groups overlap")
        current_progress = json.loads(blob("docs/n1-sources/batch-130-progress-reconciliation-002.json"))
        original_progress = json.loads(blob("docs/n1-sources/batch-130-progress.json"))
        warnings = original_progress["warnings"]["quizSafetyWarnings"]
        check_progress(current_progress, runtime, pair_proof, sha(inventory_raw), warnings)
        for name in ("reconciliation-author-gates-002", "reconciliation-committed-gates-001"):
            log = captures[f"{name}/quiz-safety.log"].decode("utf-8")
            require([line for line in log.splitlines() if line.startswith("WARN")] == warnings,
                    "Original nonfatal warnings were dropped or changed")
            unit = captures[f"{name}/unittest.log"].decode("utf-8")
            require(re.search(r"(?m)^Ran 431 tests in .+\r?$", unit)
                    and re.search(r"(?m)^OK\r?$", unit), "Full unittest result differs")
            reading = captures[f"{name}/reading-exposure.log"]
            keys = json.loads(blob(ORIGINAL + "reading-keys.json"))["testedKeys"]
            verify_reading_keys(blob(ORIGINAL + "producers/check_reading_b130.py"),
                                blob(ORIGINAL + "reading-keys.json"), reading, keys)
            require(re.search(rb"(?m)^0 production hit\(s\).*; 0 padded-session hit\(s\).*; 2 latent collision\(s\)", reading)
                    and b"Not arbitrary/custom pools, multiple borrowing, Kotlin/native/device" in reading,
                    "Reading result or bounded limits differ")
        entries = {name: value[0] for name, value in runtime_entries(json.loads(blob("manifest.json"))).items()}
        preservation = {}
        for mode, name in (("author", "reconciliation-author-preserve-002"),
                           ("committed", "reconciliation-committed-preserve-001")):
            files = capture_group(name)
            summary, memory = (json.loads(files[file]) for file in ("summary.json", "memory.json"))
            require(summary["status"] == "PASS" and summary["mode"] == mode
                    and summary["head"] == (PARENT if mode == "author" else candidate)
                    and summary["parent"] == PARENT and summary["publishedBase"] == BASE
                    and summary["manifestSha256"] == runtime["manifestSha256"]
                    and summary["newPacketInventorySha256"] == sha(inventory_raw)
                    and summary["producerSha256"] == inventory["files"]["producers/preserve_b130_reconciliation_002.py"]
                    and summary["guardSha256"] == GUARD_SHA
                    and set(summary["exactChangedFileInventory"]) == set(changed["files"])
                    and summary["allRuntimeHashesChecked"] == len(entries) == 8730
                    and summary["otherParentRuntimeEntriesUnchanged"] == 8727
                    and json.loads(files["runtime-hashes.json"]) == entries
                    and gates.memory_ok(memory), "Actual preservation binding differs")
            preservation[mode] = {file: sha(raw) for file, raw in files.items()}
        for name in ("reconciliation-author-gates-001", "reconciliation-author-preserve-001"):
            files = capture_group(name)
            require(all(raw == blob(PREFIX + f"author-evidence/{name}/{file}")
                        for file, raw in files.items()), "Historical author execution was rewritten")
        for name, digest in external["sourceBindings"].items():
            require(sha(blob(PREFIX + name)) == digest, "External snapshot no longer matches signed evidence")
        for capture in external["captures"]:
            for item in capture["outputs"].values():
                require(Path(item["path"]).parent == ROOT / "revision-external-observation-001"
                        and len(frozen(item["path"], item["sha256"])) == item["bytes"],
                        "Complete external capture differs")
        for path, digest in handoff["localCaptureReadbackAndMemoryBindings"].items():
            source = Path(path)
            require(source.is_relative_to(ROOT.parent / "reconciliation-001")
                    and sha(source.read_bytes()) == digest, "Local source readback differs")
            if "memory" in source.name:
                require(gates.memory_ok(json.loads(source.read_bytes())), "Author source RAM guard breached")
        git("-c", "core.whitespace=cr-at-eol", "diff", "--check", PARENT, candidate)
        clean()
    finally:
        memory = guard.finish()
    require(gates.memory_ok(memory), "Evidence verification RAM guard breached")
    captured = {name: write_frozen(output / name, raw) for name, raw in sorted(captures.items())}
    print(json.dumps(freeze_json(output / "verification.json", {
        "batch": 130, "status": "PASS_SIGNED_RECONCILIATION_BINDINGS_ONLY",
        "candidate": candidate, "parent": PARENT, "base": BASE,
        "proofs": {key: {"path": str(ROOT / name), "sha256": digest}
                   for key, (name, digest) in PROOFS.items()},
        "handoffSha256": HANDOFF_SHA, "inventorySha256": sha(inventory_raw),
        "changedFileCount": 111, "originalPacketFiles": 307,
        "pairBindings": pair_proof, "gateSets": gate_sets, "preservation": preservation,
        "retainedQuizSafetyWarnings": warnings, "capturedExecutionFiles": captured,
        "memory": memory, "helpers": HELPERS, "producerSha256": sha(frozen(Path(__file__))),
        "reviewAccepted": False, "publicationAccepted": False,
        "limits": "Mechanical signed source, question mapping, execution and preservation bindings only. "
                  "No author disposition is accepted linguistically here. Both isolated confirmations, "
                  "final closure and publication remain pending. Historical lexical/image uncertainty "
                  "and bounded host reading, font, native/device and custom-pool limits remain.",
    })))


if __name__ == "__main__":
    require(len(sys.argv) == 3, "Usage: verify_b130_revision_evidence.py SHA NEW_OUTPUT_DIRECTORY")
    main(*sys.argv[1:])

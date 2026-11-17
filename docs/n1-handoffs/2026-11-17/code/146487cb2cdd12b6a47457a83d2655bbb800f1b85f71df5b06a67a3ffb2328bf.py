"""Verify an exact two-parent counter integration without transferring old review acceptance."""
import copy
import json
import re
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, start_guard, write_frozen
from verify_b130_payload import REPO, RUNNER, runtime_entries
from verify_b130_sources import FINGERPRINT, Git, ORIGIN, OWNER, TRAILER

BASE = "f237a8d590a4cb91029bc0b8485163933f44b403"
CLOSURE = "9151a6f6ad5bdba9b58178167fba4cabab876504"
INCOMING = "153c6b833f68d99f59cbbce34b0bdc6d09a59bc7"
ROOT = WS / "scratch-130" / "review"
CONTENT = {"articles/numbers-and-counters.md", "counters/age.json"}
CHANGED = CONTENT | {"manifest.json"}


def expected_manifest(previous, incoming_content):
    require(set(incoming_content) == CONTENT, "Unexpected incoming content")
    result = copy.deepcopy(previous)
    for path, raw in incoming_content.items():
        sections = [key for key, entries in result.items() if isinstance(entries, dict) and path in entries]
        require(len(sections) == 1, "Incoming path is missing or duplicated in manifest")
        result[sections[0]][path] = sha(raw.replace(b"\r\n", b"\n"))
    # This is the pinned builder's content-version calculation over the updated payload and language.
    payload = {key: value for key, value in result.items() if key not in ("schemaVersion", "contentVersion")}
    result["contentVersion"] = sha(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode())[:16]
    return (json.dumps(result, ensure_ascii=False, indent=1, sort_keys=True) + "\n").encode()


def check_trees(base, closure, incoming, merged):
    require(base.keys() == incoming.keys(), "Incoming branch adds or removes paths")
    require({path for path in base if base[path] != incoming[path]} == CHANGED,
            "Incoming branch scope differs")
    require(closure.keys() == merged.keys(), "Merge adds or removes paths")
    expected = dict(closure)
    for path in CONTENT:
        require(incoming[path][:2] == ("100644", "blob"), "Incoming content is not a regular file")
        expected[path] = incoming[path]
    require(merged["manifest.json"][:2] == ("100644", "blob"), "Manifest object mode differs")
    expected["manifest.json"] = merged["manifest.json"]
    require(merged == expected, "Merge changed or lost an unrelated tracked blob")
    require({path for path in closure if closure[path] != merged[path]} == CHANGED,
            "Merge did not apply exactly the incoming content and rebuilt manifest")


def main(candidate, output):
    require(re.fullmatch(r"[0-9a-f]{40}", candidate) and candidate not in (BASE, CLOSURE, INCOMING),
            "New full integration commit required")
    require(output.parent == ROOT and output.name.startswith("integration-runtime-") and not output.exists(),
            "Use a new direct review integration-runtime output")
    for name, digest in {
        "verify_b130_sources.py": "222518f71e16878a49dbff51ecaa94ee2d9f6f471b8d9a5fa4fb9bd4b6d0a22b",
        "verify_b130_payload.py": "f5d3791ae3b1ae301617ee90ab3625cb60aab9631724441200df22cca8ee2551",
    }.items():
        frozen(Path(__file__).with_name(name), digest)
    seed_path = ROOT / "signed-closure-verification-001" / "verification.json"
    seed = json.loads(frozen(seed_path, "a86768afa7010cab36541e872a42e8d6f0ff6f3469f5a8fedb309582b91bf3da"))
    require(seed["status"] == "PASS_IMMUTABLE_SIGNED_CLOSURE_ONLY" and seed["commit"] == CLOSURE
            and seed["parent"] == "1ac4053c5da955c3afaafc1e879e63a98ee42526"
            and not seed["publicationAccepted"] and not seed["memory"]["breach"], "Closure seed differs")
    guard, _ = start_guard("B130 exact signed integration runtime verification")
    git = Git(REPO, RUNNER, guard)
    try:
        def clean():
            require(git("rev-parse", "HEAD").decode().strip() == candidate
                    and not git("status", "--porcelain=v1", "--untracked-files=all"),
                    "Integration checkout is not the clean candidate")

        def blob(revision, path):
            return git("show", f"{revision}:{path}")

        def tree(revision):
            result = {}
            for entry in git("ls-tree", "-r", "-z", revision).split(b"\0"):
                if entry:
                    metadata, path = entry.split(b"\t", 1)
                    name = path.decode()
                    require(name not in result, "Duplicate tree path")
                    result[name] = tuple(metadata.decode().split())
            return result

        clean()
        require(git("remote", "get-url", "origin").decode().strip() == ORIGIN, "Wrong origin")
        for revision, parents in ((candidate, f"{CLOSURE} {INCOMING}"), (INCOMING, BASE)):
            require(git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", revision).decode().strip()
                    == f"{parents}|G|{FINGERPRINT}|{OWNER}|{OWNER}", "Parents, signature or owner differ")
            require(TRAILER in git("show", "-s", "--format=%B", revision), "Required trailer missing")
        require(git("merge-base", CLOSURE, INCOMING).decode().strip() == BASE, "Merge base differs")
        trees = {revision: tree(revision) for revision in (BASE, CLOSURE, INCOMING, candidate)}
        check_trees(*(trees[revision] for revision in (BASE, CLOSURE, INCOMING, candidate)))
        incoming_content = {path: blob(INCOMING, path) for path in CONTENT}
        manifests = {revision: blob(revision, "manifest.json") for revision in trees}
        require((REPO / "manifest.json").read_bytes() == manifests[candidate],
                "Worktree manifest bytes differ from the signed candidate")
        require(sha(manifests[CLOSURE]) == seed["manifestSha256"], "Verified closure manifest differs")
        for previous, result in ((BASE, INCOMING), (CLOSURE, candidate)):
            require(manifests[result] == expected_manifest(json.loads(manifests[previous]), incoming_content),
                    "Manifest is not the exact deterministic two-file update")
        before = runtime_entries(json.loads(manifests[CLOSURE]))
        after = runtime_entries(json.loads(manifests[candidate]))
        require(len(before) == len(after) == 8730 and before.keys() == after.keys()
                and {path for path in before if before[path] != after[path]} == CONTENT
                and all(before[path][1] == after[path][1] for path in before),
                "Runtime membership, classification or delta differs")
        for path, raw in incoming_content.items():
            require(blob(candidate, path) == raw == (REPO / path).read_bytes(),
                    "Incoming signed/worktree bytes differ: " + path)
            require(after[path] == (sha(raw.replace(b"\r\n", b"\n")), False),
                    "Incoming manifest hash differs")
        builder = blob(CLOSURE, "tools/build_manifest.py")
        require(blob(candidate, "tools/build_manifest.py") == builder
                and blob(INCOMING, "tools/build_manifest.py") == builder, "Manifest producer changed")
        clean()
        guard.check()
        diff = git("diff", "--no-ext-diff", "--no-renames", CLOSURE, candidate, "--", *sorted(CONTENT))
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Integration verification RAM breach")
    inputs = {
        "incoming-article.md": incoming_content["articles/numbers-and-counters.md"],
        "incoming-counter.json": incoming_content["counters/age.json"],
        "content.patch": diff,
        "manifest-producer.py": builder,
    }
    bindings = {name: write_frozen(output / name, raw) for name, raw in inputs.items()}
    print(json.dumps(freeze_json(output / "verification.json", {
        "status": "PASS_INTEGRATION_RUNTIME_ONLY", "batch": 130, "candidate": candidate,
        "parents": [CLOSURE, INCOMING], "base": BASE, "worktreeClean": True,
        "trackedPaths": len(trees[candidate]), "changedPaths": sorted(CHANGED),
        "unchangedTrackedPaths": len(trees[candidate]) - len(CHANGED),
        "runtimeEntries": len(after), "runtimeChanged": sorted(CONTENT), "unchangedRuntimeEntries": 8728,
        "beforeManifestSha256": sha(manifests[CLOSURE]), "manifestSha256": sha(manifests[candidate]),
        "contentVersion": json.loads(manifests[candidate])["contentVersion"],
        "manifestDerivation": "Exact pinned-builder serialization and payload/language version hash "
                              "after the two incoming normalized content hashes replace their old entries.",
        "preservationMethod": "Every tracked merge-tree object compared. Unchanged runtime entries "
                              "inherit their already verified signed closure bytes; the two changed "
                              "entries were recomputed from complete incoming Git blobs. Not a new lexical scan.",
        "closureProof": {"path": str(seed_path), "sha256": sha(frozen(seed_path))},
        "neutralInputs": bindings, "memory": memory, "reviewAccepted": False, "publicationAccepted": False,
        "limits": "Mechanical integration only. Earlier confirmations remain on their exact prior "
                  "snapshot. Counter semantics, integrated-snapshot confirmation, author gate receipts, "
                  "CI, served ZIP, native/device and arbitrary-pool acceptance remain separate.",
        "producerSha256": sha(frozen(Path(__file__))),
    })))


if __name__ == "__main__":
    require(len(sys.argv) == 3, "Usage: verify_b130_integration_runtime.py CANDIDATE NEW_OUTPUT_DIR")
    main(sys.argv[1], Path(sys.argv[2]).resolve())

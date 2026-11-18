"""Verify the concurrent signed school-label change and its later B134 merge.

Usage: b134_integration.py incoming NEW_OUTPUT
       b134_integration.py merged SIGNED_CLOSURE SIGNED_MERGE NEW_OUTPUT

This is mechanical preservation evidence, not integrated review or publication.
"""
import copy
import json
import re
import sys
from pathlib import Path

from common import freeze_json, frozen, require, sha, start_guard, write_frozen
from run_b134_closure_checks import BASE, CLOSURE, PROGRESS, lineage
from verify_b134_payload import REPO, RUNNER, runtime_entries
from verify_b134_sources import FINGERPRINT, Git, ORIGIN, OWNER, TRAILER

ROOT = REPO.parent / "scratch-134" / "review"
REVIEWED = "355cccb840d22e7313e79f234eb93d1367e00352"
INCOMING = "830f740bdbe33ac2207acb491cd58e6ab3ab8b8b"
CONTENT = {"articles/numbers-and-counters.md", "counters/kumiexpressions.json"}
CHANGED = CONTENT | {"manifest.json"}


def expected_manifest(previous, incoming_content):
    require(set(incoming_content) == CONTENT, "Unexpected incoming content")
    result = copy.deepcopy(previous)
    for path, raw in incoming_content.items():
        sections = [key for key, entries in result.items()
                    if isinstance(entries, dict) and path in entries]
        require(len(sections) == 1, "Incoming manifest path is missing or duplicated")
        result[sections[0]][path] = sha(raw.replace(b"\r\n", b"\n"))
    payload = {key: value for key, value in result.items()
               if key not in ("schemaVersion", "contentVersion")}
    result["contentVersion"] = sha(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode())[:16]
    return (json.dumps(result, ensure_ascii=False, indent=1, sort_keys=True) + "\n").encode()


def check_incoming(base, incoming):
    require(base.keys() == incoming.keys(), "Incoming branch adds or removes paths")
    require({path for path in base if base[path] != incoming[path]} == CHANGED,
            "Incoming branch scope differs")
    require(all(incoming[path][:2] == ("100644", "blob") for path in CHANGED),
            "Incoming object is not a regular file")


def check_merged(closure, merged, incoming):
    require(closure.keys() == merged.keys(), "Merge adds or removes paths")
    expected = dict(closure)
    for path in CONTENT:
        expected[path] = incoming[path]
    require(merged["manifest.json"][:2] == ("100644", "blob"),
            "Merged manifest is not a regular file")
    expected["manifest.json"] = merged["manifest.json"]
    require(merged == expected, "Merge changed or lost an unrelated tracked object")
    require({path for path in closure if closure[path] != merged[path]} == CHANGED,
            "Merge did not apply exactly the incoming content and rebuilt manifest")


def main(mode, output, closure=None, candidate=None):
    require(mode in ("incoming", "merged") and output.parent == ROOT and not output.exists(),
            "Use incoming|merged and a new direct review output")
    if mode == "merged":
        require(all(re.fullmatch(r"[0-9a-f]{40}", value or "")
                    for value in (closure, candidate)), "Use full closure and merge commit IDs")
    guard, _ = start_guard("B134 concurrent-main preservation")
    git = Git(REPO, RUNNER, guard)
    try:
        def blob(revision, path):
            return git("show", revision + ":" + path)

        def tree(revision):
            result = {}
            for row in git("ls-tree", "-r", "-z", revision).split(b"\0"):
                if row:
                    metadata, path = row.split(b"\t", 1)
                    name = path.decode("utf-8")
                    require(name not in result, "Duplicate tracked path")
                    result[name] = tuple(metadata.decode("ascii").split())
            guard.check()
            return result

        def identity(revision, parents):
            require(git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", revision).decode().strip()
                    == f"{parents}|G|{FINGERPRINT}|{OWNER}|{OWNER}",
                    "Commit parents, signature or owner differ")
            require(TRAILER in git("show", "-s", "--format=%B", revision),
                    "Required coauthor trailer missing")

        def clean():
            require(git("rev-parse", "HEAD").decode().strip() == (candidate or REVIEWED)
                    and not git("status", "--porcelain=v1", "--untracked-files=all"),
                    "Worktree is not the expected clean signed snapshot")

        clean()
        require(git("remote", "get-url", "origin").decode().strip() == ORIGIN, "Wrong origin")
        identity(INCOMING, BASE)
        lineage(git, REVIEWED)
        trees = {revision: tree(revision) for revision in (BASE, INCOMING, REVIEWED)}
        check_incoming(trees[BASE], trees[INCOMING])
        require(all(trees[BASE][path] == trees[REVIEWED][path] for path in CONTENT),
                "Concurrent content overlaps the B134 reviewed changes")
        incoming_content = {path: blob(INCOMING, path) for path in CONTENT}
        before_revision, after_revision = BASE, INCOMING
        if mode == "merged":
            identity(closure, REVIEWED)
            closure_delta = git("diff", "--name-only", REVIEWED, closure).decode().splitlines()
            require(closure_delta and all(path == PROGRESS or path.startswith(CLOSURE)
                                          for path in closure_delta), "Closure changed teaching content")
            identity(candidate, f"{closure} {INCOMING}")
            require(git("merge-base", closure, INCOMING).decode().strip() == BASE,
                    "Integration merge base differs")
            trees[closure], trees[candidate] = tree(closure), tree(candidate)
            check_merged(trees[closure], trees[candidate], trees[INCOMING])
            before_revision, after_revision = closure, candidate
        manifests = {revision: blob(revision, "manifest.json")
                     for revision in {BASE, INCOMING, before_revision, after_revision}}
        require(manifests[INCOMING] == expected_manifest(
                    json.loads(manifests[BASE]), incoming_content),
                "Incoming manifest differs from the exact deterministic two-file update")
        require(manifests[after_revision] == expected_manifest(
                    json.loads(manifests[before_revision]), incoming_content),
                "Integrated manifest differs from the exact deterministic two-file update")
        before = runtime_entries(json.loads(manifests[before_revision]))
        after = runtime_entries(json.loads(manifests[after_revision]))
        require(before.keys() == after.keys()
                and {path for path in before if before[path] != after[path]} == CONTENT
                and all(before[path][1] == after[path][1] for path in before),
                "Runtime membership, classification or two-file delta differs")
        builder = blob(BASE, "tools/build_manifest.py")
        require(all(blob(revision, "tools/build_manifest.py") == builder
                    for revision in {INCOMING, REVIEWED, after_revision}),
                "Manifest producer changed")
        if mode == "merged":
            require((REPO / "manifest.json").read_bytes() == manifests[candidate],
                    "Worktree manifest differs from the signed integration")
            require(all(blob(candidate, path) == raw == (REPO / path).read_bytes()
                        for path, raw in incoming_content.items()), "Merged incoming bytes differ")
        diff = git("diff", "--no-ext-diff", "--no-renames", BASE, INCOMING, "--", *sorted(CONTENT))
        clean()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Integration preservation RAM breach")
    bindings = {path: write_frozen(output / "incoming" / path, raw)
                for path, raw in incoming_content.items()}
    bindings["diff"] = write_frozen(output / "incoming.patch", diff)
    bindings["builder"] = write_frozen(output / "manifest-producer.py", builder)
    print(json.dumps(freeze_json(output / "verification.json", {
        "status": "PASS_INCOMING_SCOPE_ONLY" if mode == "incoming" else "PASS_MERGED_PRESERVATION_ONLY",
        "batch": 134, "mode": mode, "publishedBaseline": BASE, "incoming": INCOMING,
        "reviewedSnapshot": REVIEWED, "closure": closure, "candidate": candidate,
        "changedPaths": sorted(CHANGED), "runtimeChanged": sorted(CONTENT),
        "runtimeEntries": len(after), "unchangedRuntimeEntries": len(after) - len(CONTENT),
        "beforeManifestSha256": sha(manifests[before_revision]),
        "afterManifestSha256": sha(manifests[after_revision]), "inputs": bindings,
        "memory": memory, "reviewAccepted": False, "publicationAccepted": False,
        "producerSha256": sha(frozen(Path(__file__))),
        "limits": "Exact signed object/manifest preservation only. Frozen B134 reviews remain on "
                  "355cccb. Combined-tree host gates, any required integration confirmation, "
                  "CI, ZIP and served-tree equality remain outstanding.",
    })))


if __name__ == "__main__":
    require(len(sys.argv) in (3, 5), __doc__)
    if sys.argv[1] == "incoming":
        require(len(sys.argv) == 3, __doc__)
        main("incoming", Path(sys.argv[2]).resolve())
    else:
        require(sys.argv[1] == "merged" and len(sys.argv) == 5, __doc__)
        main("merged", Path(sys.argv[4]).resolve(), sys.argv[2], sys.argv[3])

"""Verify the exact incoming word-only baseline before B131 author adaptation."""
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, start_guard
from verify_b130_payload import runtime_entries, verify_runtime_delta
from verify_b130_sources import FINGERPRINT, Git, ORIGIN, OWNER, TRAILER

BASE = "6da1184b82b60553f9b65c57f53289c779f96f7c"
WORD_COMMIT = "1f13ea1108a8661a1f98dab6f7713dc36cc3518d"
INCOMING = "cb0f5581bdda84f7e673225c19126c85e242e57b"
HERE = WS / "scratch-131" / "review"
FILES = Path(r"C:\Users\stop-\.copilot\session-state\2451b10d-02a9-46ab-82d5-d90993f0cb8b\files")
RUNNER = {"path": str(HERE / "guarded-test-v3.py"),
          "sha256": "da78564efadb90ac4c174dbf13e375327b611bc5e0fc77913c8b85c22c1aaf6b"}
NEW_WORD = "words/\u308f\u3056\u308f\u3056.md"
OLD_WORD = "words/\u308f\u3056\u3068.md"
ADDED = {NEW_WORD, "docs/wazawaza-sources.json"}
MODIFIED = {OLD_WORD, "README.md", "manifest.json"}


def tree_delta(before, after):
    require(after.keys() - before.keys() == ADDED and before.keys() <= after.keys(),
            "Incoming added or removed paths differ")
    changed = {path for path in before if before[path] != after[path]}
    require(changed == MODIFIED, "Incoming existing-path changes differ")
    require(all(before[path][:2] == after[path][:2] for path in before),
            "Incoming file modes or kinds changed")
    require(all(after[path][:2] == ("100644", "blob") for path in ADDED | MODIFIED),
            "Incoming changes are not ordinary text blobs")
    return len(before) - len(changed)


def manifest_delta(before_raw, after_raw):
    before, after = json.loads(before_raw), json.loads(after_raw)
    old_entries, new_entries = runtime_entries(before), runtime_entries(after)
    verify_runtime_delta(old_entries, new_entries, {NEW_WORD}, {OLD_WORD})
    old_scalars = {key: value for key, value in before.items()
                   if not isinstance(value, dict) and key != "contentVersion"}
    new_scalars = {key: value for key, value in after.items()
                   if not isinstance(value, dict) and key != "contentVersion"}
    require(old_scalars == new_scalars, "Manifest language/schema changed")
    payload = {key: value for key, value in after.items()
               if key not in {"schemaVersion", "contentVersion"}}
    version = sha(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8"))[:16]
    require(after["contentVersion"] == version == "db3512fb1d86f1fd",
            "Manifest content version is not reproduced")
    expected = (json.dumps(after, ensure_ascii=False, indent=1, sort_keys=True) + "\n").encode("utf-8")
    require(after_raw == expected, "Manifest serialization differs from the unchanged generator")
    return old_entries, new_entries


def main():
    observation = json.loads(frozen(
        HERE / "incoming-main-observation-001.json",
        "9c2fb95ae5704968c7b2dc033e34e5743feb86518313a26f8a8825ef08ab1754"))
    require(observation["base"] == BASE and observation["incoming"] == INCOMING
            and all(item["verification"] is True and item["reason"] == "valid"
                    and item["author"] == item["committer"] == "stop-cran"
                    for item in observation["commits"]),
            "Incoming GitHub owner verification differs")
    membership_raw = frozen(FILES / "n1-published-membership-6da1184b.json",
                            "1e5647a55f3141f3ca0c8a4f8ae5d5f1dfbb0ffabeec63f11fa122387076dbbb")
    membership = json.loads(membership_raw)
    require(membership["head"] == BASE and not membership["issues"]
            and membership["counts"]["frozenPendingMembersPresent"] == 264
            and membership["counts"]["undelivered"] == 964
            and membership["counts"]["readingMetadataDeltaCards"] == 0,
            "Original published membership is not verified")
    guard, _ = start_guard("B131 incoming word-only baseline verification")
    git = Git(WS / "b130-worktree", RUNNER, guard)

    def tree(commit):
        result = {}
        for entry in git("ls-tree", "-rz", "--full-tree", commit).decode("utf-8").split("\0"):
            if entry:
                header, path = entry.split("\t", 1)
                require(path not in result, "Duplicate Git tree path")
                result[path] = tuple(header.split(" "))
        return result

    try:
        require(git("remote", "get-url", "origin").decode().strip() == ORIGIN, "Wrong origin")
        parent = BASE
        for commit in (WORD_COMMIT, INCOMING):
            require(git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", commit).decode().strip()
                    == f"{parent}|G|{FINGERPRINT}|{OWNER}|{OWNER}", "Incoming signed ancestry differs")
            git("verify-commit", commit, include_stderr=True)
            require(TRAILER in git("show", "-s", "--format=%B", commit), "Incoming trailer missing")
            parent = commit
        before_tree, after_tree = tree(BASE), tree(INCOMING)
        preserved = tree_delta(before_tree, after_tree)
        before_raw = git("show", BASE + ":manifest.json")
        after_raw = git("show", INCOMING + ":manifest.json")
        previous, current = manifest_delta(before_raw, after_raw)
        require(len(previous) == 8730 and len(current) == 8731,
                "Complete runtime count differs")
        names = sorted(current)
        identities = [after_tree[path][2] for path in names]
        for path, identity, (actual_id, raw) in zip(names, identities, git.objects(identities)):
            guard.check()
            digest, binary = current[path]
            require(actual_id == identity
                    == hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest(),
                    "Git object bytes differ: " + path)
            require(sha(raw if binary else raw.replace(b"\r\n", b"\n")) == digest,
                    "Runtime manifest hash differs: " + path)
        n1_paths = [path for path in before_tree
                    if path.startswith(("kanji/", "strokes/", "docs/n1-"))]
        require(all(before_tree[path] == after_tree[path] for path in n1_paths),
                "N1 source, archive or card entry changed")
        require(sha(before_raw) == membership["manifestSha256"], "Original audited manifest differs")
        process = subprocess.Popen(
            ["gh", "run", "view", "43905640103", "--repo", "stop-cran/learning-japanese",
             "--json", "databaseId,headSha,status,conclusion,url"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = git.wait(process)
        require(process.returncode == 0, "Incoming CI read failed: " + err.decode("utf-8", "replace"))
        ci = json.loads(out)
        require(ci["databaseId"] == 43905640103 and ci["headSha"] == INCOMING
                and ci["status"] == "completed" and ci["conclusion"] == "success",
                "Incoming exact CI is not successful")
        require(git("ls-remote", "origin", "refs/heads/main").decode().split()[0] == INCOMING,
                "Main advanced during verification")
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Incoming baseline verification RAM breach")
    print(json.dumps(freeze_json(HERE / "incoming-main-verification-001.json", {
        "status": "PASS_WORD_ONLY_BASELINE_ADAPTATION",
        "observedAt": datetime.now(timezone.utc).isoformat(),
        "originalBase": BASE, "incomingBase": INCOMING,
        "signedCommits": [WORD_COMMIT, INCOMING], "ci": ci,
        "existingTrackedEntries": len(before_tree), "unchangedTrackedEntries": preserved,
        "addedPaths": sorted(ADDED), "modifiedPaths": sorted(MODIFIED),
        "preservedN1TreeEntries": len(n1_paths), "runtimeBefore": len(previous),
        "runtimeAfter": len(current), "runtimeRawHashesVerified": len(current),
        "manifestSha256": sha(after_raw), "contentVersion": "db3512fb1d86f1fd",
        "originalMembershipSha256": sha(membership_raw),
        "membershipPreservedByExactTreeEquality": True, "delivered": 264, "remaining": 964,
        "verifierSha256": sha(frozen(Path(__file__))),
        "dependencies": {
            name: sha(frozen(Path(__file__).with_name(name)))
            for name in ("verify_b130_sources.py", "verify_b130_payload.py")
        },
        "memory": memory,
        "observationQualification": "Observation001's runtimeBefore/runtimeAfter counted only "
                                    "manifest.files (7874/7875). Complete runtime counts across "
                                    "every manifest section are8730/8731 as verified here.",
        "limits": "Baseline adaptation only. No B131 candidate, source selection, linguistic review, "
                  "native/device or publication acceptance. No independent linguistic approval of "
                  "the unrelated word changes. The author's original source/scan evidence stays "
                  "bound to its original base and needs separate new-base binding, not relabelling.",
    })))


if __name__ == "__main__":
    main()

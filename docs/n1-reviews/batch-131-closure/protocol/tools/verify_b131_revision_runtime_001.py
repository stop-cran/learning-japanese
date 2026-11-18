"""Verify a guard-only signed B131 successor without accepting its semantic claims."""
import hashlib
import json
import re
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, start_guard
from b131_reconciliation_checks_001 import check_metadata, check_notes, check_paths, check_runtime
from verify_b131_payload import BASE, MEMBERS, REPO, RUNNER, runtime_entries
from verify_b131_sources import FINGERPRINT, Git, ORIGIN, OWNER, TRAILER

PARENT = "1359b467e0edee8822c665614d6ca57e42785c4d"
ROOT = WS / "scratch-131" / "review"
INITIALS = {
    "claude": ("preparation-003", "N1-B131-CLAUDE-003"),
    "gpt": ("preparation-004", "N1-B131-GPT-004"),
}
IMPORTS = {
    "common.py": "9e181d1ae59b786e691d8efce453c3f9a4a3f61765b46b5a29a868dfaeacde1d",
    "verify_b131_sources.py": "6efda73704e0ed665c540b5cba62d9de62613df5fc4c16ffe5ba52c834078e67",
    "verify_b131_payload.py": "0b225ae7ee2d0682b66fefae70e4cf4928914e676747ea73b76ca35d47abb678",
    "b131_reconciliation_checks_001.py": "4dd67fa7b9ffe49dd9dfe7c40b1b7790b544220efe3e33f27f3abb5f1d3365cf",
}


def check_initial(family, accepted, adjudication, final):
    require(family in INITIALS, "Unknown review family")
    run = INITIALS[family][1]
    require(accepted["run"] == adjudication["run"] == final["run"] == run
            and accepted["candidate"] == adjudication["candidate"] == final["candidate"] == PARENT
            and accepted["reviewAccepted"] is True
            and adjudication["claimsAdjudicated"] is True
            and accepted["verdict"] == adjudication["verdict"]
            and accepted["acceptedFindings"] == adjudication["acceptedFindings"]
            and adjudication["publicationAccepted"] is False
            and final["status"] == "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION"
            and not final["problems"]
            and accepted["report"] == adjudication["report"],
            "Initial review is not accepted on the unchanged B131 candidate")
    claims = adjudication.get("openClaimIds", [])
    require(isinstance(claims, list) and all(isinstance(item, str) for item in claims)
            and len(claims) == len(set(claims)), "Invalid open-claim inventory")
    return list(claims)


def main(facts_path):
    facts_path = Path(facts_path).resolve()
    facts_raw = frozen(facts_path)
    facts = json.loads(facts_raw)
    require(set(facts) == {"batch", "candidate", "initials", "cards", "output"}
            and facts["batch"] == 131
            and re.fullmatch(r"[0-9a-f]{40}", facts["candidate"])
            and facts["candidate"] != PARENT
            and set(facts["initials"]) == set(INITIALS)
            and facts["cards"] and set(facts["cards"]) <= set(MEMBERS),
            "Invalid reconciliation facts")
    output = Path(facts["output"]).resolve()
    require(facts_path.parent == output.parent == ROOT and not output.exists(),
            "Use frozen facts and a new output in B131 review")
    for name, digest in IMPORTS.items():
        frozen(Path(__file__).with_name(name), digest)
    open_claims = {}
    for family, binding in facts["initials"].items():
        directory, run = INITIALS[family]
        require(Path(binding["path"]) == ROOT / directory / f"{run}-acceptance.json",
                "Unexpected initial acceptance path")
        accepted = json.loads(frozen(binding["path"], binding["sha256"]))
        adjudication_raw = frozen(accepted["adjudication"]["path"], accepted["adjudication"]["sha256"])
        final_raw = frozen(accepted["final"]["path"], accepted["final"]["sha256"])
        adjudication, final = json.loads(adjudication_raw), json.loads(final_raw)
        frozen(accepted["report"]["path"], accepted["report"]["sha256"])
        require(adjudication["finalSha256"] == sha(final_raw),
                "Adjudication refers to another final audit")
        open_claims[family] = check_initial(family, accepted, adjudication, final)
    for scopes in facts["cards"].values():
        require(set(scopes) == {"allowedAddedGuards", "requiredAddedGuards"}
                and all(isinstance(values, list) and len(values) == len(set(values))
                        for values in scopes.values()),
                "Invalid or duplicate guard specification")
    candidate = facts["candidate"]
    expected_cards = {f"kanji/{char}.md" for char in facts["cards"]}
    sys.path.insert(0, str(WS / "lean"))
    from n1lib import parse

    guard, _ = start_guard("B131 signed reconciliation runtime verification")
    git = Git(REPO, RUNNER, guard)

    def blob(path, revision=candidate):
        return git("show", f"{revision}:{path}")

    def clean():
        require(git("rev-parse", "HEAD").decode().strip() == candidate
                and not git("status", "--porcelain=v1", "--untracked-files=all"),
                "Signed reconciliation checkout changed")

    try:
        clean()
        require(git("remote", "get-url", "origin").decode().strip() == ORIGIN, "Wrong origin")
        require(git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", candidate).decode().strip()
                == f"{PARENT}|G|{FINGERPRINT}|{OWNER}|{OWNER}",
                "Wrong parent, signature or owner")
        signature = git("verify-commit", candidate, include_stderr=True)
        require(TRAILER in git("show", "-s", "--format=%B", candidate), "Missing coauthor trailer")
        parts = git("diff", "--name-status", "--no-renames", "-z", PARENT, candidate).decode().split("\0")
        require(parts[-1] == "" and (len(parts) - 1) % 2 == 0, "Invalid diff inventory")
        changes = dict(zip(parts[1:-1:2], parts[:-1:2]))
        require(len(changes) == (len(parts) - 1) // 2, "Duplicate changed path")
        check_paths(changes, expected_cards)
        signed = {}
        for path in changes:
            raw = blob(path)
            require(raw == (REPO / path).read_bytes(), f"Worktree bytes differ: {path}")
            signed[path] = sha(raw)
            guard.check()
        manifest_raw = blob("manifest.json")
        manifest = json.loads(manifest_raw)
        before = runtime_entries(json.loads(blob("manifest.json", PARENT)))
        after = runtime_entries(manifest)
        check_runtime(before, after, expected_cards)
        require(len(after) == 8737, "Unexpected runtime count")
        metadata = {}
        for character, scopes in facts["cards"].items():
            path = f"kanji/{character}.md"
            old_raw, new_raw = blob(path, PARENT), blob(path)
            old, _ = parse(old_raw.decode("utf-8").replace("\r\n", "\n"))
            new, _ = parse(new_raw.decode("utf-8").replace("\r\n", "\n"))
            require(old is not None and new is not None and old["kanji"] == character,
                    "Missing or incorrect card metadata")
            allowed = set(scopes["allowedAddedGuards"])
            require(all(f"kanji/{char}.md" in before for char in allowed),
                    "Guard names an absent comparison card")
            added = check_metadata(old, new, allowed, set(scopes["requiredAddedGuards"]))
            metadata[character] = {
                "oldSha256": sha(old_raw), "newSha256": sha(new_raw),
                "addedGuards": added, "retainedGuards": old.get("quiz_exclusions", []),
                "bodyAcceptance": "Pending substantive review of the exact signed diff.",
            }
        tree = {}
        for row in git("ls-tree", "-r", "-z", candidate).split(b"\0"):
            if row:
                header, path = row.split(b"\t", 1)
                tree[path.decode("utf-8")] = tuple(header.decode().split())
        for path, (digest, binary) in sorted(after.items()):
            raw = (REPO / path).read_bytes()
            oid = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
            require(tree.get(path) == ("100644", "blob", oid)
                    and sha(raw if binary else raw.replace(b"\r\n", b"\n")) == digest,
                    f"Runtime bytes differ from signed tree or manifest: {path}")
            guard.check()
        notes = "docs/n1-authoring-notes.md"
        if notes in changes:
            check_notes(blob(notes, PARENT), blob(notes))
        clean()
        result = {
            "batch": 131, "status": "PASS_RUNTIME_ONLY", "candidate": candidate,
            "parent": PARENT, "base": BASE, "worktreeClean": True,
            "signature": {"fingerprint": FINGERPRINT, "ownerVerified": True,
                          "verificationOutputSha256": sha(signature)},
            "facts": {"path": str(facts_path), "sha256": sha(facts_raw)},
            "initials": facts["initials"], "changedPaths": changes, "signedArtifacts": signed,
            "runtimeChanged": sorted(expected_cards), "runtimeEntries": len(after),
            "manifestSha256": sha(manifest_raw), "contentVersion": manifest["contentVersion"],
            "cardMetadata": metadata, "producerSha256": sha(frozen(Path(__file__))),
            "initialOpenClaimIds": open_claims, "claimResolutionAccepted": False,
            "reviewAccepted": False, "publicationAccepted": False,
            "limits": "Runtime, finite guard metadata and additive scope only. Every initial "
                      "adjudication and its unresolved claims remain bound, not resolved here. "
                      "Author claims, source evidence, gate receipts and signed text require "
                      "separate verification and both confirmations. No native/device acceptance.",
        }
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Reconciliation runtime verification breached its RAM guard")
    result["memory"] = memory
    print(json.dumps(freeze_json(output, result)))


if __name__ == "__main__":
    require(len(sys.argv) == 2, "Usage: verify_b131_revision_runtime_001.py FROZEN_FACTS")
    main(sys.argv[1])

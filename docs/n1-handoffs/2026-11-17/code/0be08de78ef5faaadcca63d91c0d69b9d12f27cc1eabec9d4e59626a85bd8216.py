"""Verify B130 runtime while preserving the actual initial semantic questions.

The frozen facts must be prepared from both accepted initial adjudications and the
actual author handoff. This guard-only metadata boundary is not an instruction to
the author; a broader justified correction needs an explicitly reviewed successor.
"""
import difflib
import hashlib
import json
import re
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, start_guard
from verify_b130_payload import BASE, MEMBERS, REPO, RUNNER, runtime_entries
from verify_b130_sources import FINGERPRINT, Git, ORIGIN, OWNER, TRAILER

INITIAL = "ce1b5c895fac90852143f322a115c2de4e768e20"
PARENT = "d440617274eef6ea7611e60f147d6483f29ca710"
ROOT = WS / "scratch-130" / "review"
PREFIX = "docs/n1-sources/batch-130-reconciliation/"
NOTES = "docs/n1-authoring-notes.md"
CARDS = {f"kanji/{character}.md" for character in MEMBERS}
IMPORTS = {
    "verify_b130_sources.py": "222518f71e16878a49dbff51ecaa94ee2d9f6f471b8d9a5fa4fb9bd4b6d0a22b",
    "verify_b130_payload.py": "f5d3791ae3b1ae301617ee90ab3625cb60aab9631724441200df22cca8ee2551",
}


def check_paths(changes, expected_cards):
    require(expected_cards == {"kanji/拍.md"}, "Invalid runtime correction scope")
    require(changes.get(NOTES) == "M", "Missing additive authoring-notes entry")
    require(changes.get("manifest.json") == "M"
            and all(changes.get(path) == "M" for path in expected_cards),
            "Required runtime correction is missing")
    for path, status in changes.items():
        require((status == "M" and path in expected_cards | {"manifest.json", NOTES})
                or (status == "A" and (path.startswith(PREFIX)
                    or re.fullmatch(r"docs/n1-sources/batch-130-progress-reconciliation-\d{3}\.json", path))),
                f"Out-of-scope change: {status} {path}")


def check_metadata(old, new, allowed, required):
    require(required <= allowed and all(isinstance(char, str) and len(char) == 1 for char in allowed),
            "Invalid finite guard scope")
    require({key: value for key, value in old.items() if key != "quiz_exclusions"}
            == {key: value for key, value in new.items() if key != "quiz_exclusions"},
            "Non-exclusion metadata changed")
    before, after = old.get("quiz_exclusions", []), new.get("quiz_exclusions", [])
    require(isinstance(before, list) and isinstance(after, list)
            and all(isinstance(char, str) and len(char) == 1 for char in after)
            and len(after) == len(set(after)) and set(before) <= set(after)
            and [char for char in after if char in before] == before,
            "Original guards removed, duplicated or reordered")
    added = set(after) - set(before)
    require(required <= added <= allowed, "Added guards differ from the finite correction scope")
    require(new["kanji"] not in after and not set(after) & set(new["distractors"]),
            "Self-exclusion or excluded curated option")
    return [char for char in after if char not in before]


def check_runtime(before, after, expected_cards):
    require(before.keys() == after.keys(), "Runtime membership changed")
    actual = {name for name in after if before[name] != after[name]}
    require(actual == expected_cards and actual <= CARDS, "Unexpected runtime delta")
    require(all(before[name][1] == after[name][1] for name in before),
            "Runtime text/binary classification changed")


def check_notes(before, after):
    old, new = before.splitlines(keepends=True), after.splitlines(keepends=True)
    edits = [op for op in difflib.SequenceMatcher(None, old, new, autojunk=False).get_opcodes()
             if op[0] != "equal"]
    require(edits and all(op[0] == "insert" for op in edits), "Existing authoring notes changed")
    inserted = b"".join(line for _, _, _, start, end in edits for line in new[start:end])
    require(re.search(rb"(?m)^#{2,3} Batch 130(?: reconciliation \d{3})?:", inserted), "Unlabelled authoring-notes insertion")



INITIAL_SHA = {
    "claude": "8bf0413650e2bb991d01786eab32648c7a3a4da8e6775ec5f9689c1c38ba04d1",
    "gpt": "76d056fae9ab4204fc967caa2fe0f7b83e297df279a5451fa3532daf96bc97fa",
}
GPT_OPEN = [f"D{i}" for i in [*range(2, 7), *range(8, 15), *range(17, 25), 26]] + ["E5", "E7", "E8"]


def valid_initial_claims(family, adjudication):
    expected = GPT_OPEN if family == "gpt" else []
    claims = adjudication.get("openClaimIds")
    if claims != expected:
        return False
    if family == "gpt":
        rows = adjudication.get("unresolvedComparisons", [])
        return ([row.get("id") for row in rows] == expected
                and all(row.get("disposition", "").startswith("UNVERIFIED")
                        and len(row.get("relatedNewCards", {})) == 1 for row in rows))
    return True


def claim_boundary(claims):
    require(claims == {"claude": [], "gpt": GPT_OPEN}, "Initial claim inventory changed")
    return {
        "initialOpenClaimIds": {family: list(ids) for family, ids in claims.items()},
        "claimResolutionAccepted": False,
        "claimResolutionLimit": "Open initial comparisons are preserved, not closed by runtime checks. "
                                "Actual source-backed reconciliation and both final confirmations "
                                "must establish their dispositions separately.",
    }


def check_initial(family, accepted, adjudication, final):
    run = f"N1-B130-{family.upper()}-004"
    require(family in ("claude", "gpt")
            and accepted["run"] == adjudication["run"] == final["run"] == run
            and accepted["candidate"] == adjudication["candidate"] == final["candidate"] == INITIAL
            and accepted["reviewAccepted"] is True
            and accepted["verdict"] == adjudication["verdict"]
            and accepted["acceptedFindings"] == adjudication["acceptedFindings"]
            and valid_initial_claims(family, adjudication)
            and adjudication["publicationAccepted"] is False
            and final["status"] == "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION"
            and not final["problems"]
            and accepted["report"] == adjudication["report"],
            "Initial review is not accepted on the unchanged B130 candidate")


def main(facts_path):
    facts_path = Path(facts_path).resolve()
    facts_raw = frozen(facts_path)
    facts = json.loads(facts_raw)
    require(set(facts) == {"batch", "candidate", "initials", "cards", "output"}
            and facts["batch"] == 130 and re.fullmatch(r"[0-9a-f]{40}", facts["candidate"])
            and facts["candidate"] != PARENT and set(facts["initials"]) == {"claude", "gpt"}
            and facts["cards"] == {"拍": {"allowedAddedGuards": ["響"], "requiredAddedGuards": ["響"]}},
            "Invalid reconciliation facts")
    output = Path(facts["output"]).resolve()
    require(facts_path.parent == output.parent == ROOT and not output.exists(),
            "Use frozen facts and a new output in B130 review")
    for name, digest in IMPORTS.items():
        frozen(Path(__file__).with_name(name), digest)
    open_initial_claims = {}
    for family, binding in facts["initials"].items():
        require(Path(binding["path"]) == ROOT / f"N1-B130-{family.upper()}-004-acceptance.json",
                "Unexpected initial acceptance path")
        require(binding["sha256"] == INITIAL_SHA[family], "Unexpected initial acceptance bytes")
        accepted = json.loads(frozen(binding["path"], binding["sha256"]))
        adjudication = json.loads(frozen(accepted["adjudication"]["path"],
                                       accepted["adjudication"]["sha256"]))
        final = json.loads(frozen(accepted["final"]["path"], accepted["final"]["sha256"]))
        frozen(accepted["report"]["path"], accepted["report"]["sha256"])
        check_initial(family, accepted, adjudication, final)
        open_initial_claims[family] = list(adjudication["openClaimIds"])
    for scopes in facts["cards"].values():
        require(set(scopes) == {"allowedAddedGuards", "requiredAddedGuards"}
                and all(isinstance(values, list) and len(values) == len(set(values))
                        for values in scopes.values()),
                "Invalid or duplicate guard specification")
    candidate = facts["candidate"]
    expected_cards = {f"kanji/{char}.md" for char in facts["cards"]}
    sys.path.insert(0, str(WS / "lean"))
    from n1lib import parse

    guard, _ = start_guard("B130 second signed reconciliation runtime verification")
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
                == f"{PARENT}|G|{FINGERPRINT}|{OWNER}|{OWNER}", "Wrong parent, signature or owner")
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
        require(len(after) == 8730, "Unexpected runtime count")
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
                "bodyAcceptance": "Pending substantive review of the exact signed diff; "
                                  "the direct pair is a precaution, not established synonymy.",
            }
        tree = {}
        for row in git("ls-tree", "-r", "-z", candidate).split(b"\0"):
            if row:
                header, path = row.split(b"\t", 1)
                mode, kind, oid = header.decode().split()
                tree[path.decode("utf-8")] = (mode, kind, oid)
        for path, (digest, binary) in sorted(after.items()):
            raw = (REPO / path).read_bytes()
            oid = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
            require(tree.get(path) == ("100644", "blob", oid)
                    and sha(raw if binary else raw.replace(b"\r\n", b"\n")) == digest,
                    f"Runtime bytes differ from signed tree or manifest: {path}")
            guard.check()
        if NOTES in changes:
            check_notes(blob(NOTES, PARENT), blob(NOTES))
        clean()
        result = {
            "batch": 130, "status": "PASS_RUNTIME_ONLY", "candidate": candidate,
            "parent": PARENT, "base": BASE, "worktreeClean": True,
            "signature": {"fingerprint": FINGERPRINT, "ownerVerified": True},
            "facts": {"path": str(facts_path), "sha256": sha(facts_raw)},
            "initials": facts["initials"], "changedPaths": changes, "signedArtifacts": signed,
            "runtimeChanged": sorted(expected_cards), "runtimeEntries": len(after),
            "manifestSha256": sha(manifest_raw), "contentVersion": manifest["contentVersion"],
            "cardMetadata": metadata, "producerSha256": sha(frozen(Path(__file__))),
            **claim_boundary(open_initial_claims),
            "reviewAccepted": False, "publicationAccepted": False,
            "limits": "Runtime, finite guard metadata and additive scope only. Author claims, "
                      "source evidence, gate receipts and signed text still require separate "
                      "verification and both confirmations. No native/device or publication acceptance.",
        }
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Reconciliation runtime verification breached its RAM guard")
    result["memory"] = memory
    print(json.dumps(freeze_json(output, result)))


if __name__ == "__main__":
    require(len(sys.argv) == 2, "Usage: verify_b130_revision_runtime_v3.py FROZEN_FACTS")
    main(sys.argv[1])

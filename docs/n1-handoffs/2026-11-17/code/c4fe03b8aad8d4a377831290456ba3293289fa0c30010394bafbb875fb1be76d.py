"""Verify B129 correction scope and runtime preservation, not linguistic acceptance."""
import difflib
import json
import re
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, start_guard
from verify_b129_payload import runtime_entries
from verify_b129_sources import FINGERPRINT, Git, ORIGIN, OWNER, TRAILER

PARENT = "7c662b37c647a9b300278abe2e3079fe57f09f83"
BASE = "20fda42f7b456889ae4ef82650dde227a139917c"
REPO = WS / "b129-worktree"
REVIEW = WS / "scratch-129" / "review"
PREFIX = "docs/n1-sources/batch-129-reconciliation/"
NOTES = "docs/n1-authoring-notes.md"
PROGRESS = "docs/n1-sources/batch-129-progress-reconciliation-001.json"
SILK, RAINBOW = "\u7d79", "\u8679"
CARDS = {f"kanji/{char}.md" for char in (SILK, RAINBOW)}
REQUIRED_GUARDS = set("\u8f2a\u5186\u5149")
ADJUDICATION_SHA = "ed55cd42a4dd8312b3685c685808bc7752ad1bb72583b2c226dc822b87177b0f"
PARENT_PROOF_SHA = "8d61f2797205fa51e6bfb5132e955f49cc7451b460e80ecf975cfee33465d99d"
RUNNER = {
    "path": str(REVIEW / "guarded-test-v3.py"),
    "sha256": "9326cabd53fb1ac18417dcc1f39d4316af8f1b0a945bf7523a9e73a7044a6848",
}
IMPORTS = {
    "verify_b129_sources.py": "9fb0aa1b179679638865582eed251f2c4fd4c9a84707f56099383808b18d0b33",
    "verify_b129_payload.py": "e1c364c7b2652eeb9e71ca6006fd9eb3fb74531d60ae432375ea0051635281a6",
}


def allowed_pairs(adjudication):
    pairs = list(adjudication["findingAdjudication"]["F1"]["pairs"])
    for claim in adjudication["consequentialClaims"]:
        pairs.extend(claim.get("pairs", [
            [claim.get("target"), other] for other in claim.get("comparisons", [])
        ]))
    require(len(pairs) == len({tuple(pair) for pair in pairs}) == 28,
            "Finite correction scope differs")
    return {char: {other for target, other in pairs if target == char}
            for char in (SILK, RAINBOW)}


def check_metadata(old, new, allowed):
    require({key: value for key, value in old.items() if key != "quiz_exclusions"}
            == {key: value for key, value in new.items() if key != "quiz_exclusions"},
            "Non-exclusion metadata changed")
    before, after = old.get("quiz_exclusions", []), new.get("quiz_exclusions", [])
    require(isinstance(before, list) and isinstance(after, list)
            and len(after) == len(set(after)) and set(before) <= set(after)
            and [char for char in after if char in before] == before,
            "Original guards removed, duplicated or reordered")
    added = set(after) - set(before)
    require(added <= allowed and not set(after) & set(new["distractors"]),
            "Out-of-scope guard or excluded curated option")
    if new["kanji"] == RAINBOW:
        require(REQUIRED_GUARDS <= set(after), "F1 guards missing")
    return [char for char in after if char not in before]


def check_paths(changes):
    require(changes.get(f"kanji/{RAINBOW}.md") == "M"
            and changes.get("manifest.json") == "M", "Required correction is missing")
    for path, status in changes.items():
        require((status == "M" and path in CARDS | {"manifest.json", NOTES})
                or (status == "A" and (path.startswith(PREFIX) or path == PROGRESS)),
                f"Out-of-scope change: {status} {path}")


def check_runtime(before, after, changed):
    require(before.keys() == after.keys(), "Runtime membership changed")
    actual = {name for name in after if before[name] != after[name]}
    require(actual == changed and actual <= CARDS and f"kanji/{RAINBOW}.md" in actual,
            "Runtime delta differs from the allowed card edits")
    require(all(before[name][1] == after[name][1] for name in before),
            "Runtime text/binary classification changed")


def check_notes(before, after):
    a, b = before.splitlines(keepends=True), after.splitlines(keepends=True)
    edits = [op for op in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes()
             if op[0] != "equal"]
    require(edits and all(op[0] == "insert" for op in edits), "Existing notes changed")
    inserted = b"".join(line for _, _, _, start, end in edits for line in b[start:end])
    require(re.search(rb"(?m)^#{2,3} Batch 129:", inserted), "Unlabelled notes insertion")


def main(candidate, output):
    require(re.fullmatch(r"[0-9a-f]{40}", candidate), "Full signed candidate SHA required")
    output = Path(output).resolve()
    require(output.parent == REVIEW and not output.exists(), "Use a new B129 review output")
    for name, digest in IMPORTS.items():
        frozen(Path(__file__).with_name(name), digest)
    adjudication_path = REVIEW / "N1-B129-GPT-001-adjudication.json"
    adjudication = json.loads(frozen(adjudication_path, ADJUDICATION_SHA))
    require(adjudication["candidate"] == PARENT, "Adjudication targets another parent")
    allowed = allowed_pairs(adjudication)
    proof_path = REVIEW / "payload-proof-002.json"
    parent_proof = json.loads(frozen(proof_path, PARENT_PROOF_SHA))
    require(parent_proof["status"] == "PASS" and parent_proof["candidate"] == PARENT
            and parent_proof["base"] == BASE, "Original payload proof differs")
    sys.path.insert(0, str(WS / "lean"))
    from n1lib import parse
    guard, _ = start_guard("B129 correction runtime verification")
    git = Git(REPO, RUNNER, guard)

    def blob(path, revision=candidate):
        return git("show", f"{revision}:{path}")

    def clean():
        require(git("rev-parse", "HEAD").decode().strip() == candidate
                and not git("status", "--porcelain=v1", "--untracked-files=all"),
                "Signed correction checkout changed")

    try:
        clean()
        require(git("remote", "get-url", "origin").decode().strip() == ORIGIN, "Wrong origin")
        require(git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", candidate).decode().strip()
                == f"{PARENT}|G|{FINGERPRINT}|{OWNER}|{OWNER}", "Wrong parent/signature/owner")
        require(TRAILER in git("show", "-s", "--format=%B", candidate), "Missing trailer")
        parts = git("diff", "--name-status", "--no-renames", "-z", PARENT, candidate).decode().split("\0")
        require(parts[-1] == "" and (len(parts) - 1) % 2 == 0, "Invalid diff inventory")
        changes = dict(zip(parts[1:-1:2], parts[:-1:2]))
        check_paths(changes)
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
        check_runtime(before, after, set(changes) & CARDS)
        require(len(after) == 8724, "Unexpected runtime count")
        metadata = {}
        for char in (SILK, RAINBOW):
            path = f"kanji/{char}.md"
            old_raw, new_raw = blob(path, PARENT), blob(path)
            old, _ = parse(old_raw.decode("utf-8").replace("\r\n", "\n"))
            new, _ = parse(new_raw.decode("utf-8").replace("\r\n", "\n"))
            require(old is not None and new is not None, "Missing card metadata")
            added = check_metadata(old, new, allowed[char])
            metadata[char] = {
                "oldSha256": sha(old_raw), "newSha256": sha(new_raw),
                "addedGuards": added, "retainedGuards": old["quiz_exclusions"],
                "bodyAcceptance": "Pending substantive review of the exact signed diff.",
            }
        for path, (digest, binary) in sorted(after.items()):
            raw = (REPO / path).read_bytes()
            require(sha(raw if binary else raw.replace(b"\r\n", b"\n")) == digest,
                    f"Runtime manifest hash differs: {path}")
            guard.check()
        if NOTES in changes:
            check_notes(blob(NOTES, PARENT), blob(NOTES))
        clean()
        result = {
            "batch": 129, "status": "PASS_RUNTIME_ONLY", "candidate": candidate,
            "parent": PARENT, "base": BASE, "signature": {
                "fingerprint": FINGERPRINT, "ownerVerified": True,
            }, "worktreeClean": True, "changedPaths": changes, "signedArtifacts": signed,
            "runtimeChanged": sorted(set(changes) & CARDS), "runtimeEntries": len(after),
            "manifestSha256": sha(manifest_raw), "contentVersion": manifest["contentVersion"],
            "cardMetadata": metadata,
            "originalPayloadProof": {"path": str(proof_path), "sha256": PARENT_PROOF_SHA},
            "adjudication": {"path": str(adjudication_path), "sha256": ADJUDICATION_SHA},
            "producerSha256": sha(frozen(Path(__file__))),
            "limits": "Runtime/metadata and additive scope verification only. Correction sources, "
                      "pair dispositions, text changes, gate execution and confirmations still require "
                      "independent verification. No publication or linguistic/native/device acceptance.",
            "reviewAccepted": False, "publicationAccepted": False,
        }
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Runtime verification RAM guard breached")
    result["memory"] = memory
    print(freeze_json(output, result))


if __name__ == "__main__":
    require(len(sys.argv) == 3, "Usage: verify_b129_revision_runtime.py CANDIDATE NEW_OUTPUT")
    main(*sys.argv[1:])

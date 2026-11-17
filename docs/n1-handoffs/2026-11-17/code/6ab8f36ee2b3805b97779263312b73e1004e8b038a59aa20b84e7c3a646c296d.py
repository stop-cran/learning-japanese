"""Prove reuse of already verified complete sources, not a new dictionary scan."""
import json
import re
import sys
from pathlib import Path

from b130_followup_closure_history import PREVIOUS
from common import freeze_json, frozen, require, sha, start_guard
from finalize_b130 import ROOT, SOURCES_SHA
from verify_b130_payload import BASE, REPO, RUNNER
from verify_b130_revision_runtime_v3 import PREFIX
from verify_b130_sources import FINGERPRINT, Git, ORIGIN, OWNER, TRAILER

PREVIOUS_PROOF = ROOT / "revision-source-proof-001.json"


def check_previous(previous):
    require(previous["batch"] == 130 and previous["candidate"] == PREVIOUS
            and previous["base"] == BASE and previous["status"] == "PASS_COMPLETE_SOURCES_ONLY"
            and previous["reviewAccepted"] is False and previous["publicationAccepted"] is False
            and not previous["memory"]["breach"]
            and len(previous["results"]["jmdict"]["identities"]) == 99
            and len(previous["results"]["kanjidic2"]["identities"]) == 31,
            "Prior complete-source proof differs")
    return {previous["signedProducer"] if name == "reconcile_sources_b130.py" else PREFIX + name: digest
            for name, digest in previous["signedBindings"].items()}


def check_reuse(previous, current, expected):
    require(previous.keys() == current.keys() == expected.keys()
            and all(current[name] == previous[name] and sha(current[name]) == digest
                    for name, digest in expected.items()), "Previously verified source bytes changed")


def main(candidate, output):
    require(re.fullmatch(r"[0-9a-f]{40}", candidate) and candidate != PREVIOUS,
            "A distinct signed successor is required")
    output = Path(output).resolve()
    require(output.parent == ROOT and not output.exists(), "Use a new B130 review proof path")
    previous_raw = frozen(PREVIOUS_PROOF, SOURCES_SHA)
    previous = json.loads(previous_raw)
    expected = check_previous(previous)
    guard, _ = start_guard("B130 exact source-reuse verification")
    git = Git(REPO, RUNNER, guard)

    def clean():
        require(git("rev-parse", "HEAD").decode().strip() == candidate
                and not git("status", "--porcelain=v1", "--untracked-files=all"),
                "Signed successor checkout changed")

    try:
        clean()
        require(git("remote", "get-url", "origin").decode().strip() == ORIGIN
                and git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", candidate).decode().strip()
                == f"{PREVIOUS}|G|{FINGERPRINT}|{OWNER}|{OWNER}"
                and TRAILER in git("show", "-s", "--format=%B", candidate),
                "Wrong signature, parent, owner or trailer")
        paths = sorted(expected)
        before = {name: raw for name, (_, raw) in zip(paths, git.objects(
            [f"{PREVIOUS}:{name}" for name in paths]))}
        after = {name: raw for name, (_, raw) in zip(paths, git.objects(
            [f"{candidate}:{name}" for name in paths]))}
        check_reuse(before, after, expected)
        for name, raw in after.items():
            require((REPO / name).read_bytes() == raw, "Source checkout differs: " + name)
            guard.check()
        snapshot = "docs/n1-source-snapshot.json"
        snapshot_raw = git("show", f"{candidate}:{snapshot}")
        require(snapshot_raw == git("show", f"{PREVIOUS}:{snapshot}")
                == (REPO / snapshot).read_bytes(), "Pinned source snapshot changed")
        receipt = json.loads(after[PREFIX + "source-receipt.json"])
        comparisons = receipt["comparisonCards"]
        require(len(comparisons) == 28, "Comparison count differs")
        names = [f"kanji/{char}.md" for char in comparisons]
        for name, (_, raw) in zip(names, git.objects([f"{candidate}:{name}" for name in names])):
            char = Path(name).stem
            require(comparisons[char]["path"] == f"comparison-cards/{char}.md"
                    and raw == after[PREFIX + comparisons[char]["path"]]
                    and sha(raw) == comparisons[char]["sha256"]
                    and (REPO / name).read_bytes() == raw, "Comparison no longer matches source copy")
            guard.check()
        clean()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Source-reuse RAM guard breached")
    print(json.dumps(freeze_json(output, {
        "batch": 130, "status": "PASS_SOURCE_REUSE_ONLY", "candidate": candidate,
        "parent": PREVIOUS, "base": BASE,
        "previousSourceProof": {"path": str(PREVIOUS_PROOF), "sha256": sha(previous_raw)},
        "signedBindings": expected, "sourceSnapshotSha256": sha(snapshot_raw),
        "comparisonCardsVerified": len(comparisons),
        "previousVerifiedCounts": {"jmdict": 99, "kanjidic2": 31},
        "newDictionaryScanPerformed": False,
        "producerSha256": sha(frozen(Path(__file__))), "memory": memory,
        "reviewAccepted": False, "publicationAccepted": False,
        "limits": "Byte-exact reuse of the pinned prior complete-source proof and its signed "
                  "records/comparisons only. No new dictionary scan, source interpretation, "
                  "claim closure, final confirmation or delivery acceptance.",
    })))


if __name__ == "__main__":
    require(len(sys.argv) == 3, "Usage: verify_b130_source_reuse.py SHA NEW_OUTPUT")
    main(*sys.argv[1:])

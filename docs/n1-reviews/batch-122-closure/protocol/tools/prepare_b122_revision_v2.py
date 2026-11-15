"""Bind B122 verification to its observed committed-gate summary schema."""
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, write_frozen


def main():
    here = Path(__file__).resolve().parent
    source = here / "verify_b122_revision.py"
    digest = "30d8327042e183a61324365138a3594ebfdb962d35e8a1b194f3d494db439fd7"
    original = frozen(source, digest)
    old, new = b'summary["head"]', b'summary["startingHead"]'
    require(original.count(old) == 1 and new not in original, "Unexpected summary binding")
    revised = original.replace(old, new)
    require(revised.replace(new, old) == original, "Reverse schema delta differs")
    compile(revised, "verify_b122_revision_v2.py", "exec")
    output = write_frozen(here / "verify_b122_revision_v2.py", revised)
    freeze_json(WS / "scratch-122" / "review" / "revision-verifier-v2-derivation.json", {
        "source": {"path": str(source), "sha256": digest},
        "output": output,
        "reverseExact": True,
        "reason": "The B122 committed runner records the actual initial HEAD in startingHead, "
                  "not head. Its committed mode checks a clean worktree and unchanged manifest. "
                  "Require the exact revision, base, parent, committed mode and all ten gates; "
                  "do not rewrite the author receipts.",
        "observedSummarySha256": "37d1c55a89f94f8b7a094c8e0db72a9858568b8b321634315124f1b11ec673c7",
        "runnerSha256": "597b7efde279b26533e336a463c33dbadeaaff1a6a6acba5c4c1cf2011748db2",
        "producer": {"path": str(Path(__file__)), "sha256": sha(Path(__file__).read_bytes())},
        "publicationAccepted": False,
    })


if __name__ == "__main__":
    main()

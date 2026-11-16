"""Check B131's source-base verifier against immutable prior observations only."""
import json
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, start_guard
from b131_base_binding import (
    CANDIDATE_BASE, HERE, OBSERVED_SHA, SOURCE_BASE, verify_baseline_trees,
)
from verify_b130_sources import Git


def main():
    module = Path(__file__).with_name("b131_base_binding.py")
    module_raw = frozen(module, "bfe4ce22c4630e0a96795e39f765f0cb36484d0c23912d6dcf2b74f22bd171a0")
    test_raw = frozen(Path(__file__).with_name("test_b131_base_binding.py"),
                      "f34fd60d5c42220c0e1fa9da8e23baa381d985c89e299a98d493d4807055b86b")
    receipt_raw = frozen(HERE / "base-binding-tests-001" / "receipt.json",
                         "f515a102b3df746f686ece7e2bd6e2185ce17e106b6e3d47624d95a05e774a11")
    receipt = json.loads(receipt_raw)
    frozen(HERE / "base-binding-tests-001" / "output.log", receipt["logSha256"])
    require(receipt["exitCode"] == 0 and not receipt["memory"]["breach"],
            "Source-base binding controls did not pass")
    record = json.loads(frozen(HERE / "author-base-adaptation-observed-001.json", OBSERVED_SHA))
    guard, _ = start_guard("B131 source-base verifier preparation")
    git = Git(WS / "b130-worktree", {
        "path": str(HERE / "guarded-test-v3.py"),
        "sha256": "da78564efadb90ac4c174dbf13e375327b611bc5e0fc77913c8b85c22c1aaf6b",
    }, guard)
    try:
        count = verify_baseline_trees(
            record, git("ls-tree", "-rz", SOURCE_BASE, "--", "kanji"),
            git("ls-tree", "-rz", CANDIDATE_BASE, "--", "kanji"))
        require(count == 1254, "Unexpected immutable baseline card count")
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Preparation RAM breach")
    print(json.dumps(freeze_json(HERE / "base-binding-preparation-001.json", {
        "status": "PREPARATION_ONLY",
        "sourceBase": SOURCE_BASE, "candidateBase": CANDIDATE_BASE,
        "baselineKanjiEntries": count, "moduleSha256": sha(module_raw),
        "testSha256": sha(test_raw), "testReceiptSha256": sha(receipt_raw),
        "observedAdaptationSha256": OBSERVED_SHA, "memory": memory,
        "limits": "Four focused controls and actual immutable baseline trees only. No active "
                  "author file was read. The signed candidate branch of the verifier must still "
                  "run after the handoff; no candidate, source or publication is accepted.",
    })))


if __name__ == "__main__":
    main()

"""Check B131's corrected source-base verifier against immutable observations."""
import json
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, start_guard
from b131_base_binding_v2 import (
    CANDIDATE_BASE, HERE, OBSERVED_SHA, SOURCE_BASE, verify_baseline_trees,
)
from verify_b130_sources import Git


def main():
    module_raw = frozen(Path(__file__).with_name("b131_base_binding_v2.py"),
                        "76c11728caa881ede7179266fd7060e97bb861e773933d898ce331d46dcb8c2b")
    test_raw = frozen(Path(__file__).with_name("test_b131_base_binding_v2.py"),
                      "48973a123851f5543e25858bcba2a7605497e7e0fcb7894fdf70309f293a96af")
    receipt_raw = frozen(HERE / "base-binding-tests-002" / "receipt.json",
                         "8f36033cb90bc03cc82ce45807821c63983e14d3e738294c1b8c289e44d3b6f3")
    receipt = json.loads(receipt_raw)
    frozen(HERE / "base-binding-tests-002" / "output.log", receipt["logSha256"])
    require(receipt["exitCode"] == 0 and not receipt["memory"]["breach"],
            "Source-base binding controls did not pass")
    failed_raw = frozen(HERE / "base-binding-preparation-execution-001" / "receipt.json",
                        "a61aedb6f7c7a1c03b60b353c572033aa7d59d0cb07311a9f222da6a582f7ca8")
    failed = json.loads(failed_raw)
    frozen(HERE / "base-binding-preparation-execution-001" / "output.log", failed["logSha256"])
    require(failed["exitCode"] == 1, "Failed predecessor identity differs")
    record = json.loads(frozen(HERE / "author-base-adaptation-observed-001.json", OBSERVED_SHA))
    guard, _ = start_guard("B131 source-base verifier preparation v2")
    git = Git(WS / "b130-worktree", {
        "path": str(HERE / "guarded-test-v3.py"),
        "sha256": "da78564efadb90ac4c174dbf13e375327b611bc5e0fc77913c8b85c22c1aaf6b",
    }, guard)
    try:
        original = git("ls-tree", "-rz", SOURCE_BASE, "--", "kanji")
        incoming = git("ls-tree", "-rz", CANDIDATE_BASE, "--", "kanji")
        count = verify_baseline_trees(record, original, incoming)
        require(count == 1254, "Unexpected immutable baseline card count")
        recorded_listing = git("ls-tree", "-r", SOURCE_BASE, "--", "kanji")
        require(recorded_listing == original.replace(b"\0", b"\n")
                and sha(recorded_listing) == record["baselineKanjiTreeSha256"],
                "Author's newline-delimited tree digest does not reproduce")
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Preparation RAM breach")
    print(json.dumps(freeze_json(HERE / "base-binding-preparation-002.json", {
        "status": "PREPARATION_ONLY",
        "sourceBase": SOURCE_BASE, "candidateBase": CANDIDATE_BASE,
        "baselineKanjiEntries": count, "moduleSha256": sha(module_raw),
        "testSha256": sha(test_raw), "testReceiptSha256": sha(receipt_raw),
        "observedAdaptationSha256": OBSERVED_SHA, "memory": memory,
        "preservedFailureReceiptSha256": sha(failed_raw),
        "correction": "Initial coordinator helper compared an ls-tree -rz digest to the author's "
                      "ls-tree -r digest. V2 retains exact NUL-delimited tree equality, reproduces "
                      "the original line-delimited digest and rejects unsafe path serialization. "
                      "Original author evidence is unchanged.",
        "limits": "Four focused controls and actual immutable baseline trees only. No active "
                  "author teaching draft was read. The candidate branch of the verifier must "
                  "still run after handoff with independent signature and clean-tree checks; "
                  "no candidate, source semantics or publication is accepted.",
    })))


if __name__ == "__main__":
    main()

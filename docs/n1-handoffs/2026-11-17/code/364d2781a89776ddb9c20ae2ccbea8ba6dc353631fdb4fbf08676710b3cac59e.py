"""Freeze hash-verified B123 author and coordinator evidence without changing bytes."""
import json
import stat
from pathlib import Path

from common import GUARD_SHA, WS, freeze_json, frozen, require, review_dir, sha, start_guard

RUNNER_SHA = "e641e9e26b9e76ad327586b6b54dbffc614288f67a624486524a039c1856905e"


def main():
    review = review_dir(123)
    output = review / "coordinator-source-tools-verification.json"
    require(not output.exists(), "B123 author evidence already frozen")
    proof = json.loads(frozen(
        review / "coordinator-candidate-verification.json",
        "1742946d15f4ade9607ec800bb2bc3dfa2c6ed62ced4f3f6d45e656c8a8f3528"))
    guard, _ = start_guard("Freeze verified B123 gate artifacts")
    inventory = []
    try:
        def keep(path, expected):
            require(sha(path.read_bytes()) == expected, f"Changed artifact: {path}")
            path.chmod(stat.S_IREAD)
            frozen(path, expected)
            inventory.append({"path": str(path), "sha256": expected})
            guard.check()

        def gates(directory, summary_sha, entries):
            keep(directory / "summary.json", summary_sha)
            for item in entries:
                keep(directory / (item["gate"] + ".json"), item["receiptSha256"])
                keep(directory / (item["gate"] + ".log"), item["logSha256"])

        gates(WS / "scratch-123" / "committed-gates-001",
              proof["gateSummarySha256"], proof["gates"])
        author_path = WS / "b123-worktree" / "docs" / "n1-sources" / "batch-123" / "authoring-receipt.json"
        author_raw = author_path.read_bytes()
        require(sha(author_raw) == "20412a08e7b86271f47b9033af1eea68aa8d8e3eefad19d2a992ff324c527e20",
                "Author receipt differs from the signed candidate")
        author = json.loads(author_raw)
        gates(WS / author["gateDirectory"], author["gateSummarySha256"], author["gates"])
        failed = {"source-tool-preparation-001", "candidate-binding-001"}
        for name in (
            "source-tool-preparation-001", "source-tool-preparation-002",
            "source-tool-tests-001", "source-record-verification-001",
            "candidate-binding-001", "source-contract-repair-001",
            "source-contract-v2-tests-001", "candidate-binding-002",
        ):
            directory = review / name
            receipt_raw = (directory / "receipt.json").read_bytes()
            receipt = json.loads(receipt_raw)
            require(receipt["exitCode"] == receipt["childExitCodeAfterCleanup"]
                    == (1 if name in failed else 0)
                    and receipt["memory"]["breach"] is None
                    and receipt["runnerSha256"] == RUNNER_SHA
                    and receipt["guardSha256"] == GUARD_SHA
                    and receipt["waitTimeoutSeconds"] == 0.1, f"Unexpected outcome: {name}")
            keep(directory / "output.log", receipt["logSha256"])
            keep(directory / "receipt.json", sha(receipt_raw))
        for name, digest in (
            ("source-tool-derivation.json",
             "b1b2c99a329011a790fe4b422ecc2d59c55d752def90b00a73f4c7309c0261b7"),
            ("source-contract-v2-derivation.json",
             "cbbe503cc6c64e42cfd055dd238eda0bad977e0598411939e48914535ca089cc"),
            ("source-selection-verification-001.json",
             "e6e3fe8a6f33b93eb81f270fb7e3331e8923e8a2f07285a27192d4b6cd1f5a1b"),
        ):
            raw = frozen(review / name, digest)
            keep(review / name, digest)
            record = json.loads(raw)
            if name == "source-tool-derivation.json":
                for item in record["derivations"]:
                    keep(Path(item["target"]), item["targetSha256"])
            elif name == "source-contract-v2-derivation.json":
                keep(Path(record["output"]["path"]), record["output"]["sha256"])
        keep(review / "source-tool-preparation-001" / "producer.py",
             "04834355ac0398ad317bb15c211c6d4a05a9f2ca399c2469ae7166301ececa30")
        captured_tools = []
        for path in (
            Path(__file__).with_name("prepare_b123_source_tools.py"),
            Path(__file__).with_name("repair_b123_source_contract.py"),
            review / "test-source-contract-b123.py",
            Path(__file__),
        ):
            raw = path.read_bytes()
            compile(raw, str(path), "exec")
            keep(path, sha(raw))
            captured_tools.append({"path": str(path), "sha256": sha(raw)})
    finally:
        memory = guard.finish()
    require(memory["breach"] is None, "Evidence freeze breached RAM limits")
    print(json.dumps(freeze_json(output, {
        "batch": 123, "candidate": proof["candidate"],
        "verifiedCandidateSha256": "1742946d15f4ade9607ec800bb2bc3dfa2c6ed62ced4f3f6d45e656c8a8f3528",
        "completeSourceSha256": "e6e3fe8a6f33b93eb81f270fb7e3331e8923e8a2f07285a27192d4b6cd1f5a1b",
        "passingSourceTests": 10, "v2SummaryTestsRerun": 3,
        "preservedToolingRefusals": sorted(failed), "files": inventory, "memory": memory,
        "toolsCapturedAfterRuns": captured_tools,
        "captureLimit": "Producer/manual-fixture hashes are post-run captures, not retroactive execution-time bindings.",
        "limits": "No content-review or publication acceptance.",
    })))


if __name__ == "__main__":
    main()

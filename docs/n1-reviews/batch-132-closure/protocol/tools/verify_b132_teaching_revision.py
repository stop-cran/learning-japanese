"""Verify the signed B132 reconciliation and preserve exact execution evidence."""
import json
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, start_guard, write_frozen
from confirm_b132 import CANDIDATE, REPO, ROOT, clean
from run_b132_closure_checks import BASE, ORDER
from verify_b132_gates import commands, verify_execution, verify_reading_output
from verify_b132_packet import RUNNER
from verify_b132_payload_v2 import runtime_entries
from verify_b132_sources import Git

REVISION = "009b70b2e6ec836d7364c6c3096b65b1fa9df65d"
AUTHOR = WS / "scratch-132" / "teaching-reconciliation-001"
OUT = ROOT / "teaching-revision-verification-001"
PREFIX = "docs/n1-sources/batch-132-reconciliation/"
MANIFEST_SHA = "5432522265f9efeef23103ed5ec9844e0deddd70bd06e72719143341c185b9d4"
NOTES = (
    "- [標](標.md), mark or signpost, receives a precaution because a\n"
    "  grave marker is also a mark. Not every mark is a grave, and 標\n"
    "  does not independently mean grave.\n"
    "- [塔](塔.md), tower or pagoda, receives a precaution because some\n"
    "  stone towers serve as graves or grave markers. Not every tower\n"
    "  is a grave; an ordinary 供養塔 memorial tower is not generally\n"
    "  called a grave.\n"
)
CITATIONS = ("Marker and stone-tower senses: [標](https://kotobank.jp/word/標),\n"
             "[墓標](https://kotobank.jp/word/墓標), [石塔](https://kotobank.jp/word/石塔).\n")


def main():
    require(not OUT.exists(), "Preserve previous verification")
    guard, _ = start_guard("B132 signed teaching-revision verification")
    captured = {}
    try:
        git = Git(REPO, RUNNER, guard)
        clean(git, REVISION)
        require(git("show", "-s", "--format=%P", REVISION).decode().strip() == CANDIDATE,
                "Revision must be a direct child")
        blob = lambda name, commit=REVISION: git("show", commit + ":" + name)
        before = blob("kanji/墓.md", CANDIDATE).replace(b"\r\n", b"\n").decode()
        after = blob("kanji/墓.md").replace(b"\r\n", b"\n").decode()
        expected = before.replace("quiz_exclusions: [埋, 石]", "quiz_exclusions: [埋, 石, 標, 塔]")
        expected = expected.replace("- 浅墓 is a spelling", NOTES + "- 浅墓 is a spelling")
        expected = expected.replace("entries 1514840, 1504630, 1584040 and 1609030.",
                                    "entries 1514840, 1504630, 1584040, 1609030, 1168060, 1514900 and 1703230.")
        require(after == expected + CITATIONS, "Teaching delta differs from adjudicated narrow change")
        manifest_raw = blob("manifest.json")
        require(sha(manifest_raw) == MANIFEST_SHA
                and (REPO / "manifest.json").read_bytes() == manifest_raw, "Manifest differs")
        current = runtime_entries(json.loads(manifest_raw))
        previous = runtime_entries(json.loads(blob("manifest.json", CANDIDATE)))
        require(current.keys() == previous.keys() and len(current) == 8739
                and {p for p in current if current[p] != previous[p]} == {"kanji/墓.md"},
                "Unexpected runtime delta")
        for path, (digest, binary) in current.items():
            raw = (REPO / path).read_bytes()
            require(current[path][1] == previous[path][1]
                    and sha(raw if binary else raw.replace(b"\r\n", b"\n")) == digest,
                    "Runtime bytes/classification differ: " + path)
            guard.check()
        inventory_raw = blob(PREFIX + "inventory.json")
        inventory = json.loads(inventory_raw)["files"]
        names = git("diff", "--name-only", "-z", CANDIDATE, REVISION).decode().strip("\0").split("\0")
        require(set(names) == {"kanji/墓.md", "manifest.json", PREFIX + "inventory.json"}
                | {PREFIX + name for name in inventory}, "Changed path inventory differs")
        for name, digest in inventory.items():
            require(sha(blob(PREFIX + name)) == digest
                    and sha((REPO / (PREFIX + name)).read_bytes()) == digest, "Signed inventory differs")
        source_proof = frozen(ROOT / "source-reconciliation-verification-001.json",
                              "4f64783f8810d41b778a7ccb2048ca1fc54bcff7c3ed009b20541ddd23b9bc77")
        freeze = json.loads(frozen(ROOT / "source-reconciliation-freeze-001.json",
                                  "41b27f638aa6e31e54be7c40bba3f2fd215bbc339f78cfd66670e059b3f66a93"))
        for item in freeze["files"]:
            frozen(item["path"], item["sha256"])
        signed_runner = blob("docs/n1-sources/batch-132/producers/run_132_gates.py")
        signed_common = blob("docs/n1-sources/batch-132/producers/common_132.py")
        for name in ("run_132_gates.py", "common_132.py", "check_reading_132.py"):
            require((WS / "scratch-132" / name).read_bytes()
                    == blob("docs/n1-sources/batch-132/producers/" + name), "Executed helper differs")
        for name in ("gates.py", "preserve.py"):
            require((AUTHOR / name).read_bytes() == blob(PREFIX + "producers/" + name),
                    "Revision helper differs from signed producer")
        summary_path = AUTHOR / "committed-gates-001" / "summary.json"
        summary_raw = summary_path.read_bytes()
        require(sha(summary_raw) == "2c30173ff30c821d4fa82181572bbd86332b503354fd0240fd2eb5564ff599ba",
                "Handoff gate summary changed")
        summary = json.loads(summary_raw)
        require(summary["status"] == "PASS" and summary["head"] == REVISION
                and summary["parent"] == CANDIDATE and summary["checks"] == ORDER
                and summary["serial"] is True and summary["manifestSha256"] == MANIFEST_SHA
                and summary["delegateRunnerSha256"] == sha(signed_runner)
                and summary["commonHelperSha256"] == sha(signed_common), "Gate snapshot differs")
        captured["committed-gates/summary.json"] = summary_raw
        receipts = {}
        for name in ORDER:
            for suffix, key in (("json", "receiptSha256"), ("log", "logSha256")):
                raw = (summary_path.parent / (name + "." + suffix)).read_bytes()
                require(sha(raw) == summary["logs"][name][key], "Gate evidence changed")
                captured["committed-gates/" + name + "." + suffix] = raw
            receipt = json.loads(captured["committed-gates/" + name + ".json"])
            require(receipt["gate"] == name and receipt["base"] == BASE
                    and receipt["cwd"] == str(REPO)
                    and receipt["exitCode"] == receipt["childExitCodeAfterCleanup"] == 0
                    and receipt["waitTimeoutSeconds"] == 0.1 and not receipt["memory"]["breach"]
                    and receipt["runnerSha256"] == sha(signed_runner)
                    and receipt["logSha256"] == summary["logs"][name]["logSha256"], "Failed/unbound gate")
            receipts[name] = receipt
        verify_execution(receipts, commands(), sha(signed_common))
        keys = json.loads(blob("docs/n1-sources/batch-132/reading-keys.json"))["testedKeys"]
        latent = verify_reading_output(captured["committed-gates/reading-exposure.log"].decode(), keys)
        require(latent == 3, "Latent collision count changed")
        require(all(receipts[name]["manifestSha256"] == MANIFEST_SHA for name in ("manifest", "manifest-rebuild"))
                and receipts["manifest-rebuild"]["manifestReproducible"] is True, "Manifest rebuild differs")
        preservation = (AUTHOR / "committed-preservation-001" / "summary.json").read_bytes()
        require(sha(preservation) == "0d71d6b6ee397e7bd9c23abb5633b31da9382ebbcf5896a9b131b038276e87e6",
                "Preservation handoff changed")
        captured["author-preservation.json"] = preservation
        captured["source-verification.json"] = source_proof
        clean(git, REVISION)
        result = {
            "status": "PASS_SIGNED_RECONCILIATION_BINDINGS_ONLY", "batch": 132,
            "candidate": REVISION, "parent": CANDIDATE, "base": BASE,
            "changedPaths": names, "runtimeEntries": len(current), "runtimeChanged": ["kanji/墓.md"],
            "unchangedRuntimeEntries": len(current) - 1, "sourceFilesRechecked": len(freeze["files"]),
            "manifestSha256": MANIFEST_SHA, "contentVersion": json.loads(manifest_raw)["contentVersion"],
            "committedGates": ORDER, "supplementalReadingKeys": keys, "latentCollisions": latent,
            "signedInventorySha256": sha(inventory_raw), "reviewAccepted": False, "publicationAccepted": False,
            "capturedExecutionFiles": {name: write_frozen(OUT / name, raw) for name, raw in captured.items()},
            "scope": "Independent exact delta, owner-signed lineage, all8739 actual runtime hashes, "
                     "all64 previously verified source-file hashes, signed helper/serial ten-gate bindings. "
                     "No source refetch or repeated full dictionary stream; original full-stream proof retained.",
            "limits": "Three latent smaller-pool reading collisions and Starter-plus-束 つか retained. "
                      "Not arbitrary/custom/multiple-borrow, Kotlin/native/device, rendering, linguistic or publication acceptance.",
        }
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Revision verification RAM breach")
    result["memory"] = memory
    result["verifierSha256"] = sha(frozen(Path(__file__)))
    print(json.dumps(freeze_json(OUT / "verification.json", result)))


if __name__ == "__main__":
    main()

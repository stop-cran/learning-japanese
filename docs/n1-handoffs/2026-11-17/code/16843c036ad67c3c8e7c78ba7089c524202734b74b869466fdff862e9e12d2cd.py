"""Verify the signed B133 delta, exact runtime preservation and ten committed gates."""
import json
import re
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, start_guard, write_frozen
from run_b133_closure_checks import BASE, CANDIDATE, ORDER, REPO, lineage
from verify_b133_gates_v2 import commands, verify_execution, verify_launcher, verify_reading_output
from verify_b133_packet import RUNNER
from verify_b133_payload import runtime_entries
from verify_b133_sources import Git

ROOT = WS / "scratch-133"
OUT = ROOT / "review" / "teaching-revision-verification-001"
PREFIX = "docs/n1-sources/batch-133-reconciliation/"
ADDITIONS = {"琴": ["具", "糸", "緒"], "鉛": ["鉱", "遅", "円"], "滝": ["速", "声", "激", "岩", "険"]}


def verify_article(before, after, additions):
    before, after = (raw.decode("utf-8").replace("\r\n", "\n") for raw in (before, after))
    line = re.search(r"(?m)^quiz_exclusions: \[([^\]]*)\]$", before)
    require(line is not None, "Original exclusions missing")
    old = [value.strip() for value in line[1].split(",")]
    require(not set(old) & set(additions), "An addition is already present")
    expected = before.replace(line[0], "quiz_exclusions: [" + ", ".join(old + additions) + "]", 1)
    require(expected.split("## Notes\n", 1)[0] == after.split("## Notes\n", 1)[0],
            "Revision changed teaching outside the Notes/citation boundary")
    require(after.count("## Notes\n") == expected.count("## Notes\n") == 1
            and after.count("Metadata: ") == before.count("Metadata: ") == 1,
            "Notes/citation boundary is ambiguous")
    return {"added": additions, "notesBeforeSha256": sha(before.split("## Notes\n", 1)[1].encode()),
            "notesAfterSha256": sha(after.split("## Notes\n", 1)[1].encode())}


def main(revision, summary_path, inventory_sha):
    require(re.fullmatch(r"[0-9a-f]{40}", revision) and not OUT.exists(), "Use a fresh exact revision")
    guard, _ = start_guard("B133 signed revision verification")
    captured, articles = {}, {}
    try:
        git = Git(REPO, RUNNER, guard)
        require(git("rev-parse", "HEAD").decode().strip() == revision
                and not git("status", "--porcelain=v1", "--untracked-files=all")
                and lineage(git, revision) == 1, "Revision is not a clean owner-signed direct child")
        blob = lambda name, commit=revision: git("show", commit + ":" + name)
        for char, additions in ADDITIONS.items():
            path = "kanji/" + char + ".md"
            before, after = blob(path, CANDIDATE), blob(path)
            articles[path] = {**verify_article(before, after, additions),
                              "beforeSha256": sha(before), "afterSha256": sha(after)}
            captured["articles/" + char + "-before.md"] = before
            captured["articles/" + char + "-after.md"] = after
        current_raw, previous_raw = blob("manifest.json"), blob("manifest.json", CANDIDATE)
        current, previous = (runtime_entries(json.loads(raw)) for raw in (current_raw, previous_raw))
        require(current.keys() == previous.keys() and len(current) == 8745
                and {p for p in current if current[p] != previous[p]} == set(articles),
                "Unexpected runtime delta")
        for path, (digest, binary) in current.items():
            raw = (REPO / path).read_bytes()
            require(binary == previous[path][1]
                    and sha(raw if binary else raw.replace(b"\r\n", b"\n")) == digest,
                    "Actual runtime differs: " + path)
            guard.check()
        inventory_raw = blob(PREFIX + "inventory.json")
        require(sha(inventory_raw) == inventory_sha, "Signed reconciliation inventory differs")
        inventory = json.loads(inventory_raw)["files"]
        require(isinstance(inventory, dict), "Inspect actual inventory schema before collecting")
        names = git("diff", "--name-only", "-z", CANDIDATE, revision).decode().strip("\0").split("\0")
        require(set(names) == {*articles, "manifest.json", PREFIX + "inventory.json"}
                | {PREFIX + name for name in inventory}, "Changed path inventory differs")
        for name, digest in inventory.items():
            require(sha(blob(PREFIX + name)) == digest
                    and sha((REPO / (PREFIX + name)).read_bytes()) == digest, "Signed inventory differs")
        summary_raw = frozen(summary_path)
        summary = json.loads(summary_raw)
        require(summary["status"] == "PASS" and summary["head"] == revision
                and summary["parent"] == CANDIDATE and summary["checks"] == ORDER
                and summary["serial"] is True and summary["manifestSha256"] == sha(current_raw),
                "Committed gate summary differs; inspect schema rather than substitute defaults")
        captured["committed-gates/summary.json"] = summary_raw
        signed = {}
        for name in ("run_133_gates.py", "common_133.py", "bounded_launch_133.py", "check_reading_133.py"):
            raw = blob("docs/n1-sources/batch-133/producers/" + name)
            require((ROOT / name).read_bytes() == raw, "Executed gate helper differs")
            signed[name] = sha(raw)
        receipts, logs = {}, {}
        for name in ORDER:
            for suffix, key in (("json", "receiptSha256"), ("log", "logSha256")):
                raw = frozen(summary_path.parent / (name + "." + suffix), summary["logs"][name][key])
                captured["committed-gates/" + name + "." + suffix] = raw
            receipt = json.loads(captured["committed-gates/" + name + ".json"])
            require(receipt["gate"] == name and receipt["base"] == BASE and receipt["cwd"] == str(REPO)
                    and receipt["exitCode"] == receipt["childExitCodeAfterCleanup"] == 0
                    and receipt["cleanupError"] is None and not receipt["memory"]["breach"]
                    and receipt["runnerSha256"] == signed["run_133_gates.py"]
                    and receipt["logSha256"] == summary["logs"][name]["logSha256"],
                    "Failed or unbound committed gate")
            receipts[name] = receipt
            logs[name] = captured["committed-gates/" + name + ".log"].decode()
        verify_execution(receipts, commands(), signed["common_133.py"])
        verify_launcher(receipts, logs, signed["bounded_launch_133.py"])
        keys = json.loads(blob("docs/n1-sources/batch-133/reading-keys.json"))["testedKeys"]
        latent = verify_reading_output(logs["reading-exposure"], keys)
        require(latent == 1 and receipts["manifest-rebuild"]["manifestReproducible"] is True
                and all(receipts[name]["manifestSha256"] == sha(current_raw)
                        for name in ("manifest", "manifest-rebuild")), "Reading/manifest outcomes differ")
        captured["teaching.patch"] = git("diff", "--no-color", CANDIDATE, revision, "--",
                                         *(articles.keys()))
        require(not git("status", "--porcelain=v1", "--untracked-files=all"), "Verification changed tree")
        result = {
            "batch": 133, "status": "PASS_SIGNED_RECONCILIATION_BINDINGS_ONLY",
            "candidate": revision, "parent": CANDIDATE, "base": BASE, "changedPaths": names,
            "manifestSha256": sha(current_raw), "contentVersion": json.loads(current_raw)["contentVersion"],
            "runtimeEntries": len(current), "runtimeChanged": sorted(articles),
            "unchangedRuntimeEntries": len(current) - 3, "articles": articles,
            "committedGates": ORDER, "supplementalReadingKeys": keys, "latentCollisions": latent,
            "signedInventorySha256": sha(inventory_raw), "reviewAccepted": False, "publicationAccepted": False,
            "capturedExecutionFiles": {name: write_frozen(OUT / name, raw) for name, raw in captured.items()},
            "limits": "Notes/citations require separate substantive inspection; this proves the exact "
                      "boundary, all actual runtime hashes and signed serial gates, not semantic agreement. "
                      "One latent reading collision remains; no arbitrary/custom/multiple-borrow, "
                      "Kotlin/native/device, rendering, publication or whole-set acceptance.",
        }
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Revision verification RAM breach")
    result["memory"] = memory
    result["verifierSha256"] = sha(frozen(Path(__file__)))
    print(freeze_json(OUT / "verification.json", result))


if __name__ == "__main__":
    require(len(sys.argv) == 4, "REVISION COMMITTED_GATE_SUMMARY INVENTORY_SHA256")
    main(sys.argv[1], Path(sys.argv[2]), sys.argv[3])

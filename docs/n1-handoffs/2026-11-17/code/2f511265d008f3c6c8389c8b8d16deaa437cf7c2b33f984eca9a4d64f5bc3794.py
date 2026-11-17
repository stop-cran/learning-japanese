"""Verify the signed B133 delta, exact runtime preservation and ten committed gates.

Successor of verify_b133_teaching_revision.py, adapted only to the actual author handoff schema:
inventory entries are {"sha256", "bytes"}; gates ran through the signed reconciliation wrapper
producers/gates.py (mode "committed") around the unmodified original run_133_gates.py.
"""
import json
import re
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, start_guard, write_frozen
from run_b133_closure_checks import BASE, CANDIDATE, ORDER, REPO, lineage
from verify_b131_gate_evidence_v2 import memory_ok
from verify_b133_gates_v2 import commands, verify_execution, verify_launcher, verify_reading_output
from verify_b133_packet import RUNNER
from verify_b133_payload import runtime_entries
from verify_b133_sources import Git
from verify_b133_teaching_revision import ADDITIONS, PREFIX, verify_article

ROOT = WS / "scratch-133"
HANDOFF = ROOT / "teaching-reconciliation-001"
OUT = ROOT / "review" / "teaching-revision-verification-002"
HELPERS = ("run_133_gates.py", "common_133.py", "bounded_launch_133.py", "check_reading_133.py")


def inventory_files(inventory):
    files = inventory.get("files")
    require(isinstance(files, dict) and files and "inventory.json" not in files
            and all(isinstance(e, dict) and set(e) == {"sha256", "bytes"}
                    and re.fullmatch(r"[0-9a-f]{64}", e["sha256"]) and type(e["bytes"]) is int
                    for e in files.values()), "Reconciliation inventory schema differs")
    return files


def check_summary(summary, admission, revision, manifest_sha, wrapper_sha, runner_sha):
    require(admission["head"] == revision and admission["parent"] == CANDIDATE
            and admission["originalBatchBase"] == BASE and admission["mode"] == "committed",
            "Committed gate admission binds another snapshot")
    memory_ok(admission["memory"])
    require(summary["status"] == "PASS" and summary["mode"] == "committed"
            and summary["head"] == revision and summary["parent"] == CANDIDATE
            and summary["originalBatchBase"] == BASE and summary["checks"] == ORDER
            and summary["serial"] is True and summary["manifestSha256"] == manifest_sha
            and summary["runnerSha256"] == wrapper_sha and summary["originalRunnerSha256"] == runner_sha
            and set(summary["logs"]) == set(ORDER),
            "Committed gate summary differs; inspect schema rather than substitute defaults")
    memory_ok(summary["finalMemory"])


def main(revision, summary_path, inventory_sha):
    require(re.fullmatch(r"[0-9a-f]{40}", revision) and not OUT.exists(), "Use a fresh exact revision")
    require(summary_path.parent.parent == HANDOFF, "Use the actual handoff committed-gate directory")
    guard, _ = start_guard("B133 signed revision verification v2")
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
        inventory = inventory_files(json.loads(inventory_raw))
        names = git("diff", "--name-only", "-z", CANDIDATE, revision).decode().strip("\0").split("\0")
        require(set(names) == {*articles, "manifest.json", PREFIX + "inventory.json"}
                | {PREFIX + name for name in inventory}, "Changed path inventory differs")
        for name, entry in inventory.items():
            raw = blob(PREFIX + name)
            require(sha(raw) == entry["sha256"] and len(raw) == entry["bytes"]
                    and sha((REPO / (PREFIX + name)).read_bytes()) == entry["sha256"],
                    "Signed inventory differs: " + name)
            guard.check()
        signed = {}
        for name in HELPERS:
            raw = blob("docs/n1-sources/batch-133/producers/" + name)
            require((ROOT / name).read_bytes() == raw
                    and inventory["producers/original/" + name]["sha256"] == sha(raw),
                    "Executed or packaged gate helper differs: " + name)
            signed[name] = sha(raw)
        wrapper = blob(PREFIX + "producers/gates.py")
        require((HANDOFF / "gates.py").read_bytes() == wrapper, "Executed gate wrapper differs")
        summary_raw, admission_raw = frozen(summary_path), frozen(summary_path.parent / "admission.json")
        summary, admission = json.loads(summary_raw), json.loads(admission_raw)
        check_summary(summary, admission, revision, sha(current_raw), sha(wrapper), signed["run_133_gates.py"])
        captured["committed-gates/summary.json"] = summary_raw
        captured["committed-gates/admission.json"] = admission_raw
        receipts, logs = {}, {}
        for name in ORDER:
            for suffix, key in (("json", "receiptSha256"), ("log", "logSha256")):
                raw = frozen(summary_path.parent / (name + "." + suffix), summary["logs"][name][key])
                captured["committed-gates/" + name + "." + suffix] = raw
            receipt = json.loads(captured["committed-gates/" + name + ".json"])
            require(receipt["gate"] == name and receipt["base"] == BASE and receipt["cwd"] == str(REPO)
                    and receipt["exitCode"] == receipt["childExitCodeAfterCleanup"] == 0
                    and receipt["cleanupError"] is None and receipt.get("activeError") is None
                    and not receipt["memory"]["breach"]
                    and receipt["runnerSha256"] == signed["run_133_gates.py"]
                    and receipt["logSha256"] == summary["logs"][name]["logSha256"],
                    "Failed or unbound committed gate: " + name)
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
            "committedGates": ORDER, "gateWrapperSha256": sha(wrapper), "signedHelpers": signed,
            "supplementalReadingKeys": keys, "latentCollisions": latent,
            "signedInventorySha256": sha(inventory_raw), "signedInventoryFiles": len(inventory),
            "reviewAccepted": False, "publicationAccepted": False,
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

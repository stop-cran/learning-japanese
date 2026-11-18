"""Preflight actual B127 closure inputs without closing the pending review."""
import ast
import io
import json
import sys
import unittest

from archive_b124_chains_v2 import prepare
from common import (TOOLS, WS, freeze_json, frozen, load_batch, load_module,
                    require, sha, start_guard, write_frozen)
from confirm_b127 import clean
from verify_b127_archive import verify_chain


def main():
    root = WS / "scratch-127" / "review"
    original = TOOLS / "close_b127.py"
    raw = frozen(original, "59dce57ef01327355f7261c96b29901914f1b0fdc8e2f61d0871d40293049bc9")
    substitutions = [
        ('"coordinator-gate-tests.json"', '"protocol-tooling-readiness-001.json"'),
        ('"close_b127.py", "verify_b127_archive.py"',
         '"close_b127.py", "close_b127_v2.py", "prepare_b127_closure_inputs.py", "verify_b127_archive.py"'),
    ]
    text = raw.decode("utf-8")
    for before, after in substitutions:
        require(text.count(before) == 1 and after not in text, "Unexpected closure source")
        text = text.replace(before, after)
    restored = text
    for before, after in reversed(substitutions):
        restored = restored.replace(after, before)
    require(restored.encode("utf-8") == raw, "Closure derivation is not reversible")
    compile(text, "close_b127_v2.py", "exec")
    output = write_frozen(TOOLS / "close_b127_v2.py", text.encode("utf-8"))
    derivation = freeze_json(root / "closure-v2-derivation.json", {
        "source": {"path": str(original), "sha256": sha(raw)},
        "output": output, "reverseExact": True,
        "substitutions": [{"before": a, "after": b} for a, b in substitutions],
        "reason": "The old tool requests an absent legacy coordinator-gate-tests.json. "
                  "Bind the existing actual 81-test readiness receipt under its real name, "
                  "without manufacturing an alias or altering historical evidence.",
    })
    new_module = load_module("close_b127_v2", TOOLS / "close_b127_v2.py")
    sys.modules["close_b127"] = new_module
    tests = load_module("b127_closure_input_tests", TOOLS / "test_close_b127.py")
    require(tests.require_confirmation is new_module.require_confirmation,
            "Fixtures do not exercise the derived closure")
    archive_tests = load_module("b127_archive_input_tests", TOOLS / "test_verify_b127_archive.py")
    suite = unittest.TestSuite(
        unittest.defaultTestLoader.loadTestsFromModule(module)
        for module in (tests, archive_tests)
    )
    require(suite.countTestCases() == 8, "Incomplete closure fixture suite")
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    test_log = write_frozen(root / "closure-v2-tests.txt", stream.getvalue().encode("utf-8"))
    print(stream.getvalue(), flush=True)
    require(result.wasSuccessful(), "Closure fixtures failed")
    guard, _ = start_guard("B127 actual closure input preflight")
    try:
        config = load_batch(127)
        proof = json.loads(frozen(root / "reconciliation-001-independent-proof.json",
                                 "6d63b9a10b3059a2a39ab7481e17a76ae628afc2255c7e5f0128d241cac1d6cb"))
        clean(config, proof["candidate"])
        protocol = []
        groups = {
            "audit-review.py": root,
            "audit-confirm.py": root / "confirm",
            "common.py": TOOLS,
        }
        recovery = ["tooling-preflight-recovery-001.json", "tooling-tests-recovery-001.txt"]
        for node in ast.walk(ast.parse(text)):
            if not isinstance(node, ast.For) or not isinstance(node.iter, ast.Tuple):
                continue
            first = node.iter.elts[0]
            if not isinstance(first, ast.Constant) or first.value not in groups:
                continue
            directory = groups[first.value]
            names = [item.value for item in node.iter.elts if isinstance(item, ast.Constant)]
            if first.value == "audit-confirm.py":
                names.extend(recovery)
            for name in names:
                path = directory / name
                protocol.append({"path": str(path), "sha256": sha(frozen(path))})
                guard.check()
        require(len(protocol) > 50, "Static protocol inventory was not discovered")
        chains = []
        for family in ("CLAUDE", "GPT"):
            for path in (
                root / "core-chain.json",
                root / f"N1-B127-{family}-001-extension.json",
                root / "confirm" / f"N1-B127-{family}-CONFIRM-001-chain.json",
            ):
                manifest_raw = frozen(path)
                manifest = json.loads(manifest_raw)
                files, retention = prepare(manifest_raw, {
                    segment["path"]: frozen(segment["path"], segment["sha256"])
                    for segment in manifest["segments"]
                })
                binding = {
                    "manifestSha256": sha(manifest_raw),
                    "retentionSha256": sha(files["retention.json"]),
                    "segments": len(manifest["segments"]),
                    "archivedSegmentIndices": retention["archivedSegmentIndices"],
                    "localOnlySegmentIndices": [row["index"] for row in retention["localOnlySegments"]],
                }
                chains.append({"family": family, "path": str(path), **verify_chain(files, binding)})
                guard.check()
        freeze_json(root / "closure-spec-001.json", {
            "batch": 127, "candidate": proof["candidate"],
            "finalRuns": ["N1-B127-CLAUDE-CONFIRM-001", "N1-B127-GPT-CONFIRM-001"],
            "intermediateRuns": [], "excludedInitials": [],
            "preflight": str(root / "prompts" / "preflight.json"),
            "confirmationProtocol": recovery,
        })
        print(json.dumps(freeze_json(root / "closure-input-preflight-001.json", {
            "status": "PASS_PREPARATION_ONLY", "candidate": proof["candidate"],
            "derivation": derivation, "protocolFiles": protocol, "actualChainRetention": chains,
            "tests": test_log, "testCount": result.testsRun,
            "archiveWritten": False, "confirmationAccepted": False, "published": False,
            "limits": "Only checks immutable dependencies and actual chain retention in memory. "
                      "The final GPT report, its adjudication and acceptance remain prerequisites. "
                      "No author worktree files or reviewer inputs were changed.",
        })), flush=True)
    finally:
        require(not guard.finish()["breach"], "Closure input preflight RAM guard breached")


if __name__ == "__main__":
    main()

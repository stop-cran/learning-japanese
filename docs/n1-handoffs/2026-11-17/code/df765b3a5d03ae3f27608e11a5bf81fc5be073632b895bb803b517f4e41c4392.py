"""Prepare strict runtime checks for B134's observed, provisional single-member scope."""
import json
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, start_guard, write_frozen

TOOLS = Path(__file__).resolve().parent
HERE = WS / "scratch-134" / "review"
REPO = WS / "b134-worktree"
BASE = "e17cb97c53ca4e3193dae5e11b52ba517fe86e76"
MEMBERS = ["\u7d2b"]
SUPPORTS = {"\u7d2b": ["\u7d2b"]}
SOURCE_SHA = "794a75b0a4d0f89bd7ec1066d9d917a262148c95159f18a20a71cc4e1d926aee"
PAYLOAD_SHA = "b75726e35d93210a18fe72b953e5437b90d7f4efa0caedebcdc6c9f662b6b775"
RUNNER = {"path": str(HERE / "guarded-test-v3.py"),
          "sha256": "52d7b2a997aa707358556d7cbb0fa621e4383df45bf67c84b52bd729a52ad283"}
AUTHOR_INPUTS = {
    "source-rows.json": "e896c0cb873d910bef4b12bc1cf7ae5d447e728b59bc789de50cdb21fb698b47",
    "source-receipt.json": "c28a2b71909f32b48c746979418970abff9c65c5eff1635c1f0b78adbfd47813",
}

frozen(TOOLS / "prepare_b131_source_verifier.py",
       "1c49464972263d673822b45a3445d293f439c3c03cc00ed3e1ab974e7f1544a5")
frozen(TOOLS / "verify_b134_sources.py", SOURCE_SHA)
frozen(TOOLS / "verify_b133_payload.py", PAYLOAD_SHA)
from prepare_b131_source_verifier import derive
from verify_b133_payload import runtime_entries
from verify_b134_sources import FINGERPRINT, Git, ORIGIN, OWNER


def main():
    output = HERE / "payload-verifier-derivation-001.json"
    capture = HERE / "payload-scope-observation-001"
    require(not output.exists() and not capture.exists()
            and not (TOOLS / "verify_b134_payload.py").exists()
            and not (TOOLS / "test_verify_b134_payload.py").exists(),
            "Preserve existing payload preparation")
    producer_raw = frozen(Path(__file__))
    support_tests_raw = frozen(TOOLS / "test_b134_support_inventory.py")
    guard, _ = start_guard("B134 provisional payload verification preparation")
    git = Git(REPO, RUNNER, guard)
    observed = {}
    try:
        require(git("remote", "get-url", "origin").decode().strip() == ORIGIN, "Wrong origin")
        require(git("show", "-s", "--format=%G?|%GF|%ae|%ce", BASE).decode().strip()
                == f"G|{FINGERPRINT}|{OWNER}|{OWNER}", "Baseline signature or owner differs")
        signature = git("verify-commit", BASE, include_stderr=True)
        manifest_raw = git("show", f"{BASE}:manifest.json")
        manifest = json.loads(manifest_raw)
        runtime = runtime_entries(manifest)
        index_raw = git("show", f"{BASE}:docs/n1-sources/source-index.json")
        index = {row["kanji"]: row for row in json.loads(index_raw)}
        for name, digest in AUTHOR_INPUTS.items():
            path = HERE.parent / "source-002" / name
            raw = path.read_bytes()
            require(sha(raw) == digest, "Observed author source changed: " + name)
            observed[name] = raw
        rows = json.loads(observed["source-rows.json"])
        receipt = json.loads(observed["source-receipt.json"])
        require(rows == [index[char] for char in MEMBERS]
                and all(row["statusAtFreeze"] == "pending" for row in rows)
                and all(f"kanji/{char}.md" not in runtime for char in MEMBERS),
                "Observed members differ from pending absent baseline members")
        require(receipt["base"] == BASE and receipt["indexSha256"] == sha(index_raw)
                and receipt["manifestSha256"] == sha(manifest_raw)
                and receipt["containsKeys"] == MEMBERS + ["\u8308"],
                "Observed source receipt scope or baseline differs")
        sys.path.insert(0, str(WS / "lean"))
        from n1lib import parse
        declared = {char: [] for char in MEMBERS}
        words = sorted(name for name in manifest["files"] if name.startswith("words/"))
        objects = git.objects([f"{BASE}:{name}" for name in words])
        require(len(objects) == len(words), "Incomplete baseline word objects")
        for name, (_, raw) in zip(words, objects):
            normalized = raw.replace(b"\r\n", b"\n")
            require(sha(normalized) == manifest["files"][name], "Baseline word hash differs")
            card, _ = parse(normalized.decode("utf-8"))
            require(card is not None, "Baseline word metadata missing")
            for char in MEMBERS:
                if char in card.get("kanji", []):
                    declared[char].append(Path(name).stem)
            guard.check()
        require(declared == SUPPORTS, "Complete baseline declared-support inventory differs")
        for name, raw in observed.items():
            require((HERE.parent / "source-002" / name).read_bytes() == raw,
                    "Author source changed during observation")
        captures = {name: write_frozen(capture / name, raw) for name, raw in observed.items()}
        verifier = derive("verify_b133_payload.py", PAYLOAD_SHA, "verify_b134_payload.py", [
            ("b133", "b134"), ("B133", "B134"), ("batch-133", "batch-134"),
            ("scratch-133", "scratch-134"), ("Batch 133", "Batch 134"),
            ("6858fcfb069cc56a195c3f6ed938f92f657fe96b", BASE),
            ('MEMBERS = ["\\u7434", "\\u925b", "\\u6edd"]',
             "MEMBERS = " + json.dumps(MEMBERS)),
            ('SUPPORTS = {"\\u7434": ["\\u7434"], "\\u925b": ["\\u925b\\u7b46"], "\\u6edd": ["\\u6edd"]}',
             "SUPPORTS = " + json.dumps(SUPPORTS)),
            ("84135cb99ff36f31bd6ac27fa9a82dd656c14dcf4d20c98c6852c45745cd5e71", SOURCE_SHA),
            ("03260517d250b9d8071e2e70ec76fdb3ffda906d4f947e4a049375ebb249e5eb",
             RUNNER["sha256"]),
            ('proof["batch"] == 133', 'proof["batch"] == 134'),
            ('"batch": 133', '"batch": 134'),
            ("len(previous) == 8739 and len(current) == 8745",
             f"len(previous) == {len(runtime)} and len(current) == {len(runtime) + 2 * len(MEMBERS)}"),
        ])
        tests = derive(
            "test_verify_b133_payload.py",
            "8dc0a66a4e8faf4d0144ff44d418a65a8b45f1201f729181533df7d58ad39b46",
            "test_verify_b134_payload.py",
            [("verify_b133_payload", "verify_b134_payload")],
        )
        guard.check()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Preparation RAM breach")
    print(json.dumps(freeze_json(output, {
        "batch": 134, "status": "PROVISIONAL_PREPARATION_ONLY",
        "base": BASE, "members": MEMBERS, "sourceRows": [row["sourceRow"] for row in rows],
        "supports": SUPPORTS, "baselineWordsScanned": len(words),
        "baselineRuntimeEntries": len(runtime),
        "expectedCandidateRuntimeEntries": len(runtime) + 2 * len(MEMBERS),
        "baselineManifestSha256": sha(manifest_raw),
        "baselineSourceIndexSha256": sha(index_raw),
        "baselineSignatureOutputSha256": sha(signature),
        "observedAuthorInputs": captures, "authorInputsWereReadOnly": False,
        "verifier": verifier, "tests": tests,
        "supportTests": {"path": str(TOOLS / "test_b134_support_inventory.py"),
                         "sha256": sha(support_tests_raw)},
        "producer": {"path": str(Path(__file__)), "sha256": sha(producer_raw)},
        "memory": memory,
        "scope": "Observed single-member source-002 scope, complete row compared with the "
                 "owner-signed baseline index, and all baseline word metadata independently "
                 "scanned for declared supports. Source observations are frozen coordinator "
                 "copies, not modifications or acceptance of mutable author evidence.",
        "limits": "No candidate SHA supplied or accepted. Final membership, source selectors, "
                  "selection schema and no-prose-exception claim must match the signed handoff. "
                  "The verifier preserves all owner-signature, runtime, complete metadata, "
                  "reciprocal-wrapper and generated-geometry checks. Author gates, complete "
                  "sources, semantic review, native/device and publication remain pending.",
    })))


if __name__ == "__main__":
    main()

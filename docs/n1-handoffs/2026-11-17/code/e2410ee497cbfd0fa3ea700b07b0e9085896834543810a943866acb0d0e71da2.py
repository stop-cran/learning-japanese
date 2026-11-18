"""Prepare strict runtime checks for the observed B133 three-member source scope."""
import json
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, start_guard, write_frozen

TOOLS = Path(__file__).resolve().parent
HERE = WS / "scratch-133" / "review"
REPO = WS / "b133-worktree"
BASE = "6858fcfb069cc56a195c3f6ed938f92f657fe96b"
MEMBERS = ["\u7434", "\u925b", "\u6edd"]
SUPPORTS = {"\u7434": ["\u7434"], "\u925b": ["\u925b\u7b46"], "\u6edd": ["\u6edd"]}
SOURCE_SHA = "84135cb99ff36f31bd6ac27fa9a82dd656c14dcf4d20c98c6852c45745cd5e71"
PAYLOAD_SHA = "af5091da5140b08e12dd1dd182f3a5db512751e808ed522f3a757d065cb6ecff"
RUNNER = {"path": str(HERE / "guarded-test-v3.py"),
          "sha256": "03260517d250b9d8071e2e70ec76fdb3ffda906d4f947e4a049375ebb249e5eb"}
AUTHOR_INPUTS = {
    "source-rows.json": "019c38d3567d82147cbd5523c8b55ff75245d8b8332b9f6e3af24499cabaa3f6",
    "source-receipt.json": "d25aa288234923d7f39c3e48c613efca65b619aca5500fb940e162f69f381f1d",
}

frozen(TOOLS / "prepare_b131_source_verifier.py",
       "1c49464972263d673822b45a3445d293f439c3c03cc00ed3e1ab974e7f1544a5")
frozen(TOOLS / "verify_b133_sources.py", SOURCE_SHA)
frozen(TOOLS / "verify_b132_payload_v2.py", PAYLOAD_SHA)
from prepare_b131_source_verifier import derive
from verify_b132_payload_v2 import runtime_entries
from verify_b133_sources import FINGERPRINT, Git, ORIGIN, OWNER


def main():
    output = HERE / "payload-verifier-derivation-001.json"
    capture = HERE / "payload-scope-observation-001"
    require(not output.exists() and not capture.exists()
            and not (TOOLS / "verify_b133_payload.py").exists()
            and not (TOOLS / "test_verify_b133_payload.py").exists(),
            "Preserve existing payload preparation")
    producer_raw = frozen(Path(__file__))
    support_tests_raw = frozen(TOOLS / "test_b133_support_inventory.py")
    guard, _ = start_guard("B133 provisional payload verification preparation")
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
                and receipt["containsKeys"] == MEMBERS + ["\u7027"],
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
        verifier = derive("verify_b132_payload_v2.py", PAYLOAD_SHA, "verify_b133_payload.py", [
            ("b132", "b133"), ("B132", "B133"), ("batch-132", "batch-133"),
            ("scratch-132", "scratch-133"), ("Batch 132", "Batch 133"),
            ("verify_b133_payload_v2.py", "verify_b133_payload.py"),
            ("2375ab9add0cc5d569c8ea35d229b82813fd8557", BASE),
            ('MEMBERS = ["\\u5893"]', "MEMBERS = " + json.dumps(MEMBERS)),
            ('SUPPORTS = {"\\u5893": ["\\u5893"]}', "SUPPORTS = " + json.dumps(SUPPORTS)),
            ("43ee9a6ceaf4ae023d4c9739b0a5276bdfd0c9c8573b410f99c5c06970dfe861", SOURCE_SHA),
            ("56eb7d1c12a9278e589d8adcf57652288934345dd80740e1b92fc9cffdbd0eeb",
             RUNNER["sha256"]),
            ('proof["batch"] == 132', 'proof["batch"] == 133'),
            ('"batch": 132', '"batch": 133'),
            ("len(previous) == 8737 and len(current) == 8739",
             f"len(previous) == {len(runtime)} and len(current) == {len(runtime) + 2 * len(MEMBERS)}"),
        ])
        tests = derive(
            "test_verify_b132_payload_v2.py",
            "aa97f86f80225edefc63d27508797bbde7221b859508533293dfc959831da531",
            "test_verify_b133_payload.py",
            [("verify_b132_payload_v2", "verify_b133_payload")],
        )
        guard.check()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Preparation RAM breach")
    print(json.dumps(freeze_json(output, {
        "batch": 133, "status": "PROVISIONAL_PREPARATION_ONLY",
        "base": BASE, "members": MEMBERS, "sourceRows": [row["sourceRow"] for row in rows],
        "supports": SUPPORTS, "baselineWordsScanned": len(words),
        "baselineRuntimeEntries": len(runtime),
        "expectedCandidateRuntimeEntries": len(runtime) + 2 * len(MEMBERS),
        "baselineManifestSha256": sha(manifest_raw),
        "baselineSourceIndexSha256": sha(index_raw),
        "baselineSignatureOutputSha256": sha(signature),
        "observedAuthorInputs": captures, "authorInputsWereReadOnly": False,
        "verifier": verifier, "tests": tests,
        "supportTests": {"path": str(TOOLS / "test_b133_support_inventory.py"),
                         "sha256": sha(support_tests_raw)},
        "producer": {"path": str(Path(__file__)), "sha256": sha(producer_raw)},
        "memory": memory,
        "scope": "Observed three-member source-002 scope, complete rows compared with the "
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

"""Independently reproduce B127's complete records and both baseline scans."""
import gzip
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, load_module, require, sha, start_guard

BASE = "dd45f6fb7cd3ce579422e2333860aa6d245af898"
CANDIDATE = "fcf8cb48d4e66b774189fe253dd799daadcc4015"
MEMBER = "\u5009"
WORD = "\u5009\u5eab"
DISTRACTORS = ["\u91d1", "\u5168", "\u5408"]
REPO = WS / "b127-worktree"
HERE = WS / "scratch-127" / "review"
PREFIX = "docs/n1-sources/batch-127/"
FINGERPRINT = "D4C9A275A218AF747B787AFA9D94B9D311BD26A7"
KEYWORDS = set("""godown warehouse warehouses storehouse storehouses cellar cellars
treasury treasuries store stores storage storeroom granary barn vault repository
depot treasure stock stockpile sudden suddenly hurry hurried hasty hastily""".split())
EXPANSION = set("""keep preserve contain put gather collect depository magazine
elevator silo repository prison jail gaol detention imprison imprisonment captive
perish perishing ruin ruined destroy collapse fragile fragility brittle""".split())
VERIFIER = WS / "scratch-124" / "review" / "verify-source-records.py"
VERIFIER_SHA = "21842b6d2d6040d2deb4a9f8c6d15f2c28c17386a443da52780a7ef7cc169c62"
SCAN_HELPER = Path(__file__).with_name("verify_b126_sources.py")
SCAN_SHA = "6fc5f09b2c4ed04de40f9aec2502b2e560c3b577a836b1ae7f59f587e83b20e3"
RUNNER = HERE / "guarded-test-v3.py"
RUNNER_SHA = "e2695e2517918ef6a292648708edad7db7d2cdd018e3f608f4e4cd8b059ce153"
ACTIVE_GUARD = None


def git(*args, repo=REPO, include_stderr=False):
    frozen(RUNNER, RUNNER_SHA)
    cleanup = load_module("b127_coordinator_cleanup", RUNNER)
    command = ["git", "--no-pager", "-c", "core.quotepath=false", *args]
    process = subprocess.Popen(command, cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        while True:
            try:
                out, err = process.communicate(timeout=0.1)
                break
            except subprocess.TimeoutExpired:
                if ACTIVE_GUARD is not None:
                    ACTIVE_GUARD.check()
        require(process.returncode == 0, f"Git failed: {args}: {err.decode('utf-8', 'replace')}")
        return out + err if include_stderr else out
    finally:
        cleanup.stop_child(process)


def clean():
    require(git("rev-parse", "HEAD").decode().strip() == CANDIDATE, "Candidate HEAD changed")
    require(not git("status", "--porcelain=v1", "--untracked-files=all"), "Worktree is not clean")


def blob(path, commit=CANDIDATE):
    return git("show", f"{commit}:{path}")


def verify_scans(original, expanded, rows, meanings, helper):
    common = {
        "baseCommit": BASE, "newKanji": MEMBER, "newSourceMeanings": meanings,
        "newTitle": "granary; storehouse", "literalGlossTokens": sorted(helper.tokens(meanings)),
        "caseFoldAndTokenPattern": "[a-z]+", "scannedBaselineCards": len(rows),
    }
    require(set(helper.tokens(meanings)) <= KEYWORDS, "Literal gloss token omitted")
    require(expanded["extends"] == "baseline-gloss-scan.json", "Wrong expanded scan parent")
    for recorded, words in ((original, KEYWORDS), (expanded, KEYWORDS | EXPANSION)):
        require(all(recorded[key] == value for key, value in common.items()),
                "Scan source identity or corpus count differs")
        require(recorded["expandedSemanticKeywords"] == sorted(words), "Scan token policy differs")
        actual = helper.matched_rows(rows, words)
        require(recorded["rows"] == actual, "Actual baseline rows do not reproduce")
        require(recorded["matches"] == [row["kanji"] for row in actual if row["matchedWords"]],
                "Actual baseline matches do not reproduce")
    return {"baselineCards": len(rows), "originalMatches": original["matches"],
            "expandedMatches": expanded["matches"], "expandedTokens": sorted(KEYWORDS | EXPANSION)}


def main():
    global ACTIVE_GUARD
    output = HERE / "source-selection-verification-001.json"
    require(not output.exists(), "Preserve existing verification")
    frozen(VERIFIER, VERIFIER_SHA)
    frozen(SCAN_HELPER, SCAN_SHA)
    verifier = load_module("b127_pinned_source_verifier", VERIFIER)
    verifier.MEMBER = MEMBER
    helper = load_module("b127_pinned_scan_helper", SCAN_HELPER)
    guard, _ = start_guard("B127 signed source verification")
    ACTIVE_GUARD = guard
    inputs, results = {}, []
    try:
        clean()
        require(git("remote", "get-url", "origin").decode().strip()
                == "https://github.com/stop-cran/learning-japanese.git", "Wrong origin")
        require(git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", CANDIDATE).decode().strip()
                == f"{BASE}|G|{FINGERPRINT}|stop-cran@list.ru|stop-cran@list.ru",
                "Wrong parent, signature or owner identity")
        signature = git("verify-commit", CANDIDATE, include_stderr=True)
        require(b"Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>"
                in git("show", "-s", "--format=%B", CANDIDATE), "Missing trailer")
        snapshot_raw = blob("docs/n1-source-snapshot.json")
        require(snapshot_raw == blob("docs/n1-source-snapshot.json", BASE), "Source snapshot changed")
        snapshot = json.loads(snapshot_raw)
        index_raw = blob("docs/n1-sources/source-index.json")
        require(sha(index_raw) == "0d517145b92c19ea4a17ba5aa9ca12c18f408001fdc01f0f7bb1a99659bbe1dd"
                and index_raw == blob("docs/n1-sources/source-index.json", BASE), "Source index changed")
        row = next(item for item in json.loads(index_raw) if item["kanji"] == MEMBER)
        require(row == json.loads(blob(PREFIX + "source-row.json"))
                and row["sourceRow"] == 57 and row["statusAtFreeze"] == "pending", "Wrong source row")
        scan_raw, expanded_raw = (blob(PREFIX + name) for name in
                                  ("baseline-gloss-scan.json", "baseline-gloss-scan-002.json"))
        original, expanded = json.loads(scan_raw), json.loads(expanded_raw)
        specs = {
            "jmdict": [("jmdict-selected-records.xml", "contains-member", {MEMBER})],
            "kanjidic2": [
                ("kanjidic2-selected-records.xml", "exact", {MEMBER}),
                ("kanjidic2-comparison-records.xml", "exact", set(DISTRACTORS) | set(original["matches"])),
                ("kanjidic2-expanded-comparison-records.xml", "exact", set(DISTRACTORS) | set(expanded["matches"])),
            ],
        }
        for kind, (filename, compressed_sha, tag, key) in verifier.INPUTS.items():
            path = WS / "control" / "inputs" / filename
            with path.open("rb") as stream:
                reader = helper.HashedReader(stream, guard)
                while reader.read(65536):
                    pass
            require(reader.digest.hexdigest() == compressed_sha == snapshot["inputs"][filename]["sha256"],
                    f"Compressed source differs: {kind}")
            selections = []
            for name, mode, queries in specs[kind]:
                raw = blob(PREFIX + name)
                selections.append({"name": PREFIX + name, "sha256": sha(raw), "mode": mode,
                                   "queries": queries, "expected": verifier.records(raw, tag, key)})
            with gzip.open(path, "rb") as stream:
                reader = helper.HashedReader(stream, guard)
                identities = verifier.verify_stream(reader, tag, key, selections, guard)
            require(reader.digest.hexdigest() == snapshot[kind]["xmlSha256"], "Decompressed source differs")
            inputs[kind] = {"filename": filename, "compressedSha256": compressed_sha,
                            "decompressedXmlSha256": reader.digest.hexdigest()}
            for selected, matched in zip(selections, identities):
                results.append({"path": selected["name"], "sha256": selected["sha256"],
                                "input": filename, "inputSha256": compressed_sha, "mode": selected["mode"],
                                "queries": sorted(selected["queries"]), "completeMatchingRecords": len(matched),
                                "identities": matched})
        sys.path.insert(0, str(WS / "lean"))
        from n1lib import parse
        baseline = json.loads(blob("manifest.json", BASE))["files"]
        cards = {}
        for entry in git("ls-tree", "-rz", BASE, "--", "kanji").decode("utf-8").split("\0"):
            if not entry:
                continue
            header, name = entry.split("\t", 1)
            mode, kind, identity = header.split(" ")
            require(mode == "100644" and kind == "blob" and name.endswith(".md"), "Unexpected kanji tree entry")
            raw = (REPO / Path(name)).read_bytes()
            require(hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest() == identity
                    and sha(raw.replace(b"\r\n", b"\n")) == baseline[name], f"Baseline card differs: {name}")
            metadata, _ = parse(raw.decode("utf-8").replace("\r\n", "\n"))
            require(metadata is not None, f"Missing metadata: {name}")
            char = Path(name).stem
            cards[char] = {"kanji": char, "path": name, "baselineGitBytesSha256": sha(raw),
                           "title": metadata["title"]}
            guard.check()
        require(len(cards) == 1246 and MEMBER not in cards, "Wrong baseline membership")
        with gzip.open(WS / "control" / "inputs" / verifier.INPUTS["kanjidic2"][0], "rb") as stream:
            reader = helper.HashedReader(stream, guard)
            rows = helper.scan_baseline(reader, cards, guard)
        require(reader.digest.hexdigest() == inputs["kanjidic2"]["decompressedXmlSha256"],
                "Baseline scan input changed")
        scan_proof = verify_scans(original, expanded, rows, row["metadata"]["meanings"], helper)
        comparisons = set(DISTRACTORS) | set(original["matches"]) | set(expanded["matches"])
        for char in comparisons:
            require(blob(PREFIX + f"comparison-cards/{char}.md") == blob(f"kanji/{char}.md", BASE),
                    f"Comparison differs from actual baseline: {char}")
            guard.check()
        clean()
    finally:
        memory = guard.finish()
        ACTIVE_GUARD = None
    require(not memory["breach"], "RAM breach")
    print(json.dumps(freeze_json(output, {
        "batch": 127, "candidate": CANDIDATE, "base": BASE, "status": "PASS",
        "signatureOutputSha256": sha(signature), "signatureOutput": signature.decode("utf-8", "replace"),
        "snapshotSha256": sha(snapshot_raw), "inputs": inputs, "sourceRecords": results,
        "reproducedScans": scan_proof, "originalScanSha256": sha(scan_raw),
        "expandedScanSha256": sha(expanded_raw), "comparisonCards": sorted(comparisons),
        "memory": memory, "verifierSha256": sha(Path(__file__).read_bytes()),
        "reusedVerifier": {"path": str(VERIFIER), "sha256": VERIFIER_SHA},
        "reusedScanHelper": {"path": str(SCAN_HELPER), "sha256": SCAN_SHA},
        "limits": "Complete source membership, field equality and actual corpus scans; not linguistic, "
                  "quiz-pool, native/device, review or publication acceptance.",
    })))


if __name__ == "__main__":
    main()

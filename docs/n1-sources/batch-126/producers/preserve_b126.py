import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from b126_common import BASE, HERE, PACKET, REPO, git, sha, start_guard, write

if len(sys.argv) != 3 or sys.argv[1] not in ("author", "committed"):
    raise SystemExit("usage: preserve_b126.py author|committed NEW_DIRECTORY")
mode, out = sys.argv[1], Path(sys.argv[2]).resolve()
assert out.parent == HERE and not out.exists()
out.mkdir()
guard = start_guard()
try:
    head = git("rev-parse", "HEAD").decode().strip()
    if mode == "author":
        assert head == BASE
    else:
        assert git("rev-parse", "HEAD^@").decode().split() == [BASE]
        assert not git("status", "--porcelain=v1", "--untracked-files=all")
    old_manifest = json.loads(git("show", f"{BASE}:manifest.json"))
    new_raw = (REPO / "manifest.json").read_bytes()
    new_manifest = json.loads(new_raw)
    if mode == "committed":
        assert new_raw == git("show", "HEAD:manifest.json")
    old_paths = {p: v for group in old_manifest.values() if isinstance(group, dict) for p, v in group.items()}
    new_paths = {p: v for group in new_manifest.values() if isinstance(group, dict) for p, v in group.items()}
    added, removed = set(new_paths) - set(old_paths), set(old_paths) - set(new_paths)
    changed = {p for p in set(old_paths) & set(new_paths) if old_paths[p] != new_paths[p]}
    assert added == {"kanji/傘.md", "strokes/傘.json"}
    assert not removed and changed == {"words/傘.md"}
    actual_runtime = {}
    for path, digest in new_paths.items():
        guard.check()
        raw = (REPO / path).read_bytes()
        if path.endswith((".md", ".json")):
            raw = raw.replace(b"\r\n", b"\n")
        actual_runtime[path] = sha(raw)
        assert sha(raw) == digest, path
    before = git("show", f"{BASE}:words/傘.md").replace(b"\r\n", b"\n")
    after = (REPO / "words" / "傘.md").read_bytes().replace(b"\r\n", b"\n")
    assert before.count("傘 means".encode()) == 1
    assert after == before.replace("傘 means".encode(), "[傘](../kanji/傘.md) means".encode(), 1)
    assert after.replace("[傘](../kanji/傘.md)".encode(), "傘".encode(), 1) == before
    assert "[傘](../words/傘.md)".encode() in (REPO / "kanji" / "傘.md").read_bytes()
    base_kanji = {Path(p).stem for p in old_paths if p.startswith("kanji/")}
    assert len(base_kanji) == 1245 and "傘" not in base_kanji
    assert not git("ls-tree", BASE, "--", "kanji/傘.md", "strokes/傘.json")
    for name in ("baseline-gloss-scan.json", "baseline-gloss-scan-002.json"):
        scan = json.loads((PACKET / name).read_text(encoding="utf-8"))
        assert scan["baseCommit"] == BASE and len(scan["rows"]) == 1245
        assert {r["kanji"] for r in scan["rows"]} == base_kanji
        for item in scan["rows"]:
            raw = (REPO / item["path"]).read_bytes()
            assert sha(raw) == item["baselineRawSha256"], item["kanji"]
    dispositions = json.loads((PACKET / "pair-dispositions.json").read_text(encoding="utf-8"))
    assert {p["kanji"] for p in dispositions["scanMatches"]} == set(scan["matches"])
    guarded = [p["kanji"] for p in dispositions["scanMatches"] if p["decision"] == "guard"]
    card = (REPO / "kanji" / "傘.md").read_text(encoding="utf-8")
    assert re.search(r"^quiz_exclusions: \[被\]$", card, re.M) and guarded == ["被"]
    for path in (PACKET / "comparison-cards").glob("*.md"):
        assert path.read_bytes() == git("show", f"{BASE}:kanji/{path.name}")
    assert (PACKET / "baseline-傘.md").read_bytes() == git("show", f"{BASE}:words/傘.md")
    source_row = json.loads((PACKET / "source-row.json").read_text(encoding="utf-8"))
    for field in ("onyomi", "kunyomi"):
        expected = ", ".join(source_row["metadata"][field])
        assert re.search("^" + field + r": \[" + re.escape(expected) + r"\]$", card, re.M)
    original_receipt = json.loads((PACKET / "source-receipt.json").read_text(encoding="utf-8"))
    for name, info in original_receipt["files"].items():
        assert sha((PACKET / name).read_bytes()) == info["sha256"], name
    assert len(ET.parse(PACKET / "jmdict-selected-records.xml").findall("entry")) == 56
    changed_paths = git("-c", "core.quotepath=false", "diff", "--name-only", BASE).decode("utf-8").splitlines()
    untracked = git("-c", "core.quotepath=false", "ls-files", "--others", "--exclude-standard").decode("utf-8").splitlines()
    allowed = {"kanji/傘.md", "strokes/傘.json", "words/傘.md", "manifest.json", "docs/n1-authoring-notes.md", "docs/n1-sources/batch-126-progress.json"}
    for path in changed_paths + untracked:
        assert path in allowed or path.startswith("docs/n1-sources/batch-126/"), path
    result = {
        "status": "PASS", "mode": mode, "base": BASE, "head": head,
        "baselineRuntimeCount": len(old_paths), "candidateRuntimeCount": len(new_paths),
        "added": sorted(added), "removed": sorted(removed), "changed": sorted(changed),
        "baselineUnchangedRuntimeEntries": len(old_paths) - len(changed),
        "allCandidateRuntimeHashesChecked": len(actual_runtime),
        "supportWordLinkOnly": True, "allOtherWordMetadataAndProsePreserved": True,
        "frozenEvidenceUnchanged": True, "sourceReadingsExactAndOrdered": True,
        "baselineScanCoverage": len(base_kanji), "finiteDispositionMatch": True,
        "manifestSha256": sha(new_raw), "contentVersion": new_manifest["contentVersion"],
        "changedContributorAndRuntimePaths": changed_paths, "untrackedScopeChecked": untracked,
        "producerSha256": sha(open(__file__, "rb").read()),
        "limits": "Byte/hash, source-order and scoped structural evidence only; not linguistic or native/device acceptance.",
    }
    write(out / "runtime-hashes.json", actual_runtime)
    print(json.dumps(result, ensure_ascii=False))
finally:
    memory = guard.finish()
    write(out / "memory.json", memory)
    if "result" in locals():
        result["memory"] = memory
        write(out / "summary.json", result)

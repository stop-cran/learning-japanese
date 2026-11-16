import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from b128_common import BASE, HERE, PACKET, REPO, git, sha, start_guard, write

if len(sys.argv) != 3 or sys.argv[1] not in ("author", "committed"):
    raise SystemExit("usage: preserve_b128.py author|committed NEW_DIRECTORY")
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
    assert added == {"kanji/唇.md", "strokes/唇.json"}
    assert not removed and changed == {"words/唇.md"}
    actual_runtime = {}
    for path, digest in new_paths.items():
        guard.check()
        raw = (REPO / path).read_bytes()
        if path.endswith((".md", ".json")):
            raw = raw.replace(b"\r\n", b"\n")
        actual_runtime[path] = sha(raw)
        assert sha(raw) == digest, path
    before = git("show", f"{BASE}:words/唇.md").replace(b"\r\n", b"\n")
    after = (REPO / "words" / "唇.md").read_bytes().replace(b"\r\n", b"\n")
    old = "The single kanji 唇 is".encode()
    new = "The single kanji [唇](../kanji/唇.md) is".encode()
    stale = " There is no 唇 kanji card in the current collection.".encode()
    assert before.count(old) == 1 and before.count(stale) == 1
    assert after == before.replace(old, new, 1).replace(stale, b"", 1)
    assert "[唇](../words/唇.md)".encode() in (REPO / "kanji" / "唇.md").read_bytes()
    base_kanji = {Path(p).stem for p in old_paths if p.startswith("kanji/")}
    assert len(base_kanji) == 1247 and "唇" not in base_kanji
    assert not git("ls-tree", BASE, "--", "kanji/唇.md", "strokes/唇.json")
    for name in ("baseline-gloss-scan.json", "baseline-gloss-scan-002.json"):
        scan = json.loads((PACKET / name).read_text(encoding="utf-8"))
        assert scan["baseCommit"] == BASE and len(scan["rows"]) == 1247
        assert {r["kanji"] for r in scan["rows"]} == base_kanji
        for item in scan["rows"]:
            raw = (REPO / item["path"]).read_bytes().replace(b"\r\n", b"\n")
            assert sha(raw) == old_paths[item["path"]], item["kanji"]
    dispositions = json.loads((PACKET / "pair-dispositions.json").read_text(encoding="utf-8"))
    assert {p["kanji"] for p in dispositions["scanMatches"]} == set(scan["matches"])
    guarded = {p["kanji"] for p in dispositions["scanMatches"] if p["decision"] == "conservative-direct-guard"}
    card = (REPO / "kanji" / "唇.md").read_text(encoding="utf-8")
    exclusions = re.search(r"^quiz_exclusions: \[([^\]]*)\]$", card, re.M).group(1).split(", ")
    assert set(exclusions) == guarded
    for path in (PACKET / "comparison-cards").glob("*.md"):
        assert path.read_bytes() == git("show", f"{BASE}:kanji/{path.name}")
    assert (PACKET / "baseline-唇.md").read_bytes() == git("show", f"{BASE}:words/唇.md")
    source_row = json.loads((PACKET / "source-row.json").read_text(encoding="utf-8"))
    for field in ("onyomi", "kunyomi"):
        expected = ", ".join(source_row["metadata"][field])
        assert re.search("^" + field + r": \[" + re.escape(expected) + r"\]$", card, re.M)
    original_receipt = json.loads((PACKET / "source-receipt.json").read_text(encoding="utf-8"))
    for name, info in original_receipt["files"].items():
        assert sha((PACKET / name).read_bytes()) == info["sha256"], name
    assert len(ET.parse(PACKET / "jmdict-selected-records.xml").findall("entry")) == 79
    assert len(ET.parse(PACKET / "jmdict-comparison-records.xml").findall("entry")) == 24
    changed_paths = git("-c", "core.quotepath=false", "diff", "--name-only", BASE).decode("utf-8").splitlines()
    untracked = git("-c", "core.quotepath=false", "ls-files", "--others", "--exclude-standard").decode("utf-8").splitlines()
    allowed = {"kanji/唇.md", "strokes/唇.json", "words/唇.md", "manifest.json", "docs/n1-authoring-notes.md", "docs/n1-sources/batch-128-progress.json"}
    for path in changed_paths + untracked:
        assert path in allowed or path.startswith("docs/n1-sources/batch-128/"), path
    result = {
        "status": "PASS", "mode": mode, "base": BASE, "head": head,
        "baselineRuntimeCount": len(old_paths), "candidateRuntimeCount": len(new_paths),
        "added": sorted(added), "removed": sorted(removed), "changed": sorted(changed),
        "baselineUnchangedRuntimeEntries": len(old_paths) - len(changed),
        "allCandidateRuntimeHashesChecked": len(actual_runtime),
        "supportWordChanges": "Exactly one reciprocal wrapper and removal of one now-false no-card sentence.",
        "allOtherWordMetadataAndProsePreserved": True,
        "frozenEvidenceUnchanged": True, "sourceReadingsExactAndOrdered": True,
        "baselineScanCoverage": len(base_kanji), "finiteDispositionMatch": True,
        "manifestSha256": sha(new_raw), "contentVersion": new_manifest["contentVersion"],
        "changedContributorAndRuntimePaths": changed_paths, "untrackedScopeChecked": untracked,
        "producerSha256": sha(Path(__file__).read_bytes()),
        "limits": "Byte/hash, source-order and structural evidence only; not linguistic or native/device acceptance. Runtime text hashes normalize CRLF to LF; source/report hashes do not.",
    }
    write(out / "runtime-hashes.json", actual_runtime)
    print(json.dumps({k: v for k, v in result.items() if k not in ("changedContributorAndRuntimePaths", "untrackedScopeChecked")}, ensure_ascii=False))
finally:
    memory = guard.finish()
    write(out / "memory.json", memory)
    if "result" in locals():
        result["memory"] = memory
        write(out / "summary.json", result)

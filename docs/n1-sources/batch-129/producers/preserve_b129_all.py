import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from b129_common import BASE, CHARS, HERE, PACKET, REPO, ROOT, git, normalized, sha, start_guard, write

sys.path.insert(0, str(ROOT / "lean"))
import n1lib

if len(sys.argv) != 3 or sys.argv[1] not in ("author", "committed"):
    raise SystemExit("usage: preserve_b129.py author|committed NEW_DIRECTORY")
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
    old = json.loads(git("show", f"{BASE}:manifest.json"))
    raw_manifest = (REPO / "manifest.json").read_bytes()
    new = json.loads(raw_manifest)
    if mode == "committed":
        assert raw_manifest == git("show", "HEAD:manifest.json")
    before = {p: v for group in old.values() if isinstance(group, dict) for p, v in group.items()}
    after = {p: v for group in new.values() if isinstance(group, dict) for p, v in group.items()}
    added, removed = set(after) - set(before), set(before) - set(after)
    changed = {p for p in set(before) & set(after) if before[p] != after[p]}
    assert added == {f"{folder}/{ch}.{suffix}" for ch in CHARS for folder, suffix in [("kanji", "md"), ("strokes", "json")]}
    assert not removed
    assert changed == {"words/茉莉花.md", "words/絹.md", "words/虹.md"}
    runtime = {}
    for path, digest in after.items():
        guard.check()
        data = (REPO / path).read_bytes()
        if path.endswith((".md", ".json")):
            data = data.replace(b"\r\n", b"\n")
        runtime[path] = sha(data)
        assert runtime[path] == digest, path
    supports = {"茉": "茉莉花", "絹": "絹", "虹": "虹"}
    for ch, word in supports.items():
        rel = f"words/{word}.md"
        baseline = git("show", f"{BASE}:{rel}").replace(b"\r\n", b"\n").decode()
        current = normalized(REPO / rel)
        wrapper = f"[{ch}](../kanji/{ch}.md)"
        assert current.count(wrapper) == baseline.count(wrapper) + 1
        assert current.replace(wrapper, ch) == baseline
        assert (PACKET / "baseline-words" / (word + ".md")).read_bytes() == git("show", f"{BASE}:{rel}")
        assert f"[{word}](../words/{word}.md)" in normalized(REPO / "kanji" / (ch + ".md"))
    baseline_kanji = {Path(p).stem for p in before if p.startswith("kanji/")}
    assert len(baseline_kanji) == 1248
    assert not set(CHARS) & baseline_kanji
    disposition = json.loads((PACKET / "pair-dispositions.json").read_text(encoding="utf8"))
    pair_members = {m["kanji"]: m for m in disposition["members"] if "kanji" in m}
    baseline_byte_hashes = {}
    for row in json.loads((PACKET / "source-rows.json").read_text(encoding="utf8")):
        ch = row["kanji"]
        fm, _ = n1lib.parse(normalized(REPO / "kanji" / (ch + ".md")))
        for field in ("onyomi", "kunyomi"):
            assert fm[field] == row["metadata"][field]
        assert int(fm["strokes"]) == row["metadata"]["strokes"]
        assert fm["radical"] == row["metadata"]["radical"] and int(fm["radicalNumber"]) == row["metadata"]["radicalNumber"]
        assert row["metadata"]["strokeCountAnnotations"] == [{"count": row["metadata"]["strokes"], "attributes": {}}]
        for scan_dir in ("scans", "scans-003", "scans-004"):
            scan = json.loads((PACKET / scan_dir / (ch + ".json")).read_text(encoding="utf8"))
            assert scan["base"] == BASE and len(scan["rows"]) == 1248
            assert {r["kanji"] for r in scan["rows"]} == baseline_kanji
            for item in scan["rows"]:
                guard.check()
                if item["path"] not in baseline_byte_hashes:
                    baseline_byte_hashes[item["path"]] = sha(git("show", f"{BASE}:{item['path']}"))
                assert baseline_byte_hashes[item["path"]] == item["baselineBytesSha256"]
                assert after[item["path"]] == before[item["path"]]
        pairs = pair_members[ch]["pairs"]
        assert set(scan["matches"]) <= {p["pair"][1] for p in pairs}
        assert set(fm["quiz_exclusions"]) == {p["pair"][1] for p in pairs if p["decision"] == "guard"}
        assert set(fm["distractors"]) == {p["pair"][1] for p in pairs if p["decision"] == "curated"}
        assert all(p["targetLabelOnComparison"] and p["comparisonLabelOnTarget"] for p in pairs)
        for other in fm["quiz_exclusions"]:
            ofm, _ = n1lib.parse(normalized(REPO / "kanji" / (other + ".md")))
            # Same direct OR rule as host; no transitive closure.
            assert other in fm["quiz_exclusions"] or ch in ofm.get("quiz_exclusions", [])
    for path in (PACKET / "comparison-cards").glob("*.md"):
        assert path.read_bytes() == git("show", f"{BASE}:kanji/{path.name}")
    expected_records = {}
    for receipt_name in ("source-receipt.json", "supplement-receipt-002.json", "final-source-receipt.json"):
        receipt = json.loads((PACKET / receipt_name).read_text(encoding="utf8"))
        for name, info in receipt["outputs"].items():
            path = PACKET / name
            assert sha(path.read_bytes()) == info["sha256"]
            if name.endswith(".xml"):
                actual = {n.findtext("ent_seq") or n.findtext("literal"):
                          sha(ET.canonicalize(ET.tostring(n, encoding="unicode"), strip_text=True).encode())
                          for n in ET.parse(path).getroot()}
                assert actual == info["canonicalRecordHashes"], name
    additional = json.loads((PACKET / "additional-source-receipt.json").read_text(encoding="utf8"))["output"]
    assert sha((PACKET / additional["filename"]).read_bytes()) == additional["sha256"]
    for filename in ("jmdict-complete-families.xml", "jmdict-supplemental-comparisons-002.xml",
                     "jmdict-final-comparisons.xml", "jmdict-additional-families.xml"):
        for node in ET.parse(PACKET / filename).getroot():
            eid = node.findtext("ent_seq")
            digest = sha(ET.canonicalize(ET.tostring(node, encoding="unicode"), strip_text=True).encode())
            if eid in expected_records:
                assert expected_records[eid] == digest
            expected_records[eid] = digest
    assert len(expected_records) == 252
    bundle = json.loads((PACKET / "evidence-inventory-002.json").read_text(encoding="utf8"))
    for name, digest in bundle["files"].items():
        assert sha((PACKET / name).read_bytes()) == digest, name
    changed_paths = git("diff", "--name-only", BASE).decode().splitlines()
    untracked = git("ls-files", "--others", "--exclude-standard").decode().splitlines()
    allowed = added | changed | {"manifest.json", "docs/n1-authoring-notes.md", "docs/n1-sources/batch-129-progress.json"}
    for path in changed_paths + untracked:
        assert path in allowed or path.startswith("docs/n1-sources/batch-129/"), path
    result = {
        "status": "PASS", "mode": mode, "base": BASE, "head": head,
        "baselineRuntimeCount": len(before), "candidateRuntimeCount": len(after),
        "added": sorted(added), "removed": sorted(removed), "changed": sorted(changed),
        "baselineUnchangedRuntimeEntries": len(before) - len(changed),
        "allCandidateRuntimeHashesChecked": len(runtime), "allOtherWordMetadataAndProsePreserved": True,
        "supportWordChanges": "Exactly one reciprocal wrapper each; no prose exception.",
        "frozenPredecessorEvidenceUnchanged": True, "sourceReadingsExactAndOrdered": True,
        "baselineScanCoveragePerMember": 1248, "pairRows": sum(len(m["pairs"]) for m in pair_members.values()),
        "directSymmetricExclusions": {c: [p["pair"][1] for p in pair_members[c]["pairs"] if p["decision"] == "guard"] for c in CHARS},
        "completeJmdictUnion": len(expected_records), "evidenceInventorySha256": sha((PACKET / "evidence-inventory-002.json").read_bytes()),
        "manifestGroupsChecked": [k for k, v in new.items() if isinstance(v, dict)],
        "manifestSha256": sha(raw_manifest), "contentVersion": new["contentVersion"],
        "changedContributorAndRuntimePaths": changed_paths, "untrackedScopeChecked": untracked,
        "producerSha256": sha(Path(__file__).read_bytes()),
        "limits": "Byte/hash, canonical equality, source order and structural evidence; not linguistic or native/device acceptance. Runtime text normalizes CRLF to LF; raw source/report hashes do not."}
    write(out / "runtime-hashes.json", runtime)
    print(json.dumps({k: v for k, v in result.items() if k not in ("changedContributorAndRuntimePaths", "untrackedScopeChecked")}, ensure_ascii=False))
finally:
    memory = guard.finish()
    write(out / "memory.json", memory)
    if "result" in locals():
        result["memory"] = memory
        write(out / "summary.json", result)

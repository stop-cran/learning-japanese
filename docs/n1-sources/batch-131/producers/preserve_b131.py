import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from b131_common import HERE, PACKET, REPO, ROOT, git, normalized, sha, start_guard, write
from candidate_b131 import BASE, CHARS

sys.path.insert(0, str(ROOT / "lean"))
import n1lib

if len(sys.argv) != 3 or sys.argv[1] not in ("author", "committed"):
    raise SystemExit("usage: preserve_b131.py author|committed NEW_DIRECTORY")
mode, out = sys.argv[1], Path(sys.argv[2]).resolve()
assert out.parent == HERE and not out.exists()
out.mkdir()
guard = start_guard()
try:
    head = git("rev-parse", "HEAD").decode().strip()
    signature = None
    if mode == "author":
        assert head == BASE
    else:
        assert git("rev-parse", "HEAD^@").decode().split() == [BASE]
        assert not git("status", "--porcelain=v1", "--untracked-files=all")
        git("verify-commit", "HEAD")
        fields = git("show", "-s", "--format=%an%n%ae%n%cn%n%ce%n%GF%n%G?", "HEAD").decode().splitlines()
        assert fields[:4] == ["Roman Konstantinovskiy", "stop-cran@list.ru",
                              "Roman Konstantinovskiy", "stop-cran@list.ru"], fields
        assert fields[4] == "D4C9A275A218AF747B787AFA9D94B9D311BD26A7"
        assert fields[5] == "G", fields
        assert "Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>" in git("show", "-s", "--format=%B", "HEAD").decode()
        signature = {"author": fields[:2], "committer": fields[2:4], "fingerprint": fields[4], "status": fields[5]}
    old_raw = git("show", f"{BASE}:manifest.json")
    assert sha(old_raw) == "03bcd5554cf90dc03cb31486a51fdeb953227c27f6f0f318fd3956e4ecca4fca"
    old = json.loads(old_raw)
    raw_manifest = (REPO / "manifest.json").read_bytes()
    new = json.loads(raw_manifest)
    if mode == "committed":
        assert raw_manifest == git("show", "HEAD:manifest.json")
    before = {p: v for group in old.values() if isinstance(group, dict) for p, v in group.items()}
    after = {p: v for group in new.values() if isinstance(group, dict) for p, v in group.items()}
    assert len(before) == 8731 and len(after) == 8737
    added, removed = set(after) - set(before), set(before) - set(after)
    changed = {p for p in set(before) & set(after) if before[p] != after[p]}
    assert added == {f"{folder}/{ch}.{suffix}" for ch in CHARS for folder, suffix in [("kanji", "md"), ("strokes", "json")]}
    assert not removed
    supports = [("衛", "自衛"), ("衛", "衛星"), ("羊", "羊毛"), ("霜", "霜")]
    assert changed == {f"words/{w}.md" for _, w in supports}
    runtime = {}
    for path, digest in after.items():
        guard.check()
        raw = (REPO / path).read_bytes()
        if path.endswith((".md", ".json")):
            raw = raw.replace(b"\r\n", b"\n")
        runtime[path] = sha(raw)
        assert runtime[path] == digest, path
    for ch, word in supports:
        rel = f"words/{word}.md"
        raw = git("show", f"{BASE}:{rel}")
        baseline = raw.replace(b"\r\n", b"\n").decode()
        current = normalized(REPO / rel)
        wrapper = f"[{ch}](../kanji/{ch}.md)"
        assert current.count(wrapper) == baseline.count(wrapper) + 1
        assert current.replace(wrapper, ch) == baseline
        assert (PACKET / "baseline-words" / (word + ".md")).read_bytes() == raw
        assert f"[{word}](../words/{word}.md)" in normalized(REPO / "kanji" / (ch + ".md"))
    baseline_kanji = {Path(p).stem for p in before if p.startswith("kanji/")}
    assert len(baseline_kanji) == 1254 and not set(CHARS) & baseline_kanji
    adaptation = json.loads((PACKET / "base-adaptation.json").read_text(encoding="utf8"))
    assert adaptation["candidateBase"] == BASE
    original_base = adaptation["originalSourceBase"]
    assert git("ls-tree", "-r", BASE, "--", "kanji") == git("ls-tree", "-r", original_base, "--", "kanji")
    dispositions = json.loads((PACKET / "pair-dispositions-002.json").read_text(encoding="utf8"))
    members = {m["kanji"]: m for m in dispositions["members"] if "kanji" in m}
    for row in json.loads((PACKET / "source-rows.json").read_text(encoding="utf8")):
        ch = row["kanji"]
        fm, _ = n1lib.parse(normalized(REPO / "kanji" / (ch + ".md")))
        for field in ("onyomi", "kunyomi"):
            assert fm[field] == row["metadata"][field]
        for field in ("strokes", "radicalNumber"):
            assert int(fm[field]) == row["metadata"][field]
        assert fm["radical"] == row["metadata"]["radical"]
        assert row["metadata"]["strokeCountAnnotations"] == [{"count": row["metadata"]["strokes"], "attributes": {}}]
        for directory in ("scans", "scans-002"):
            rel = f"{directory}/{ch}.json"
            scanpath = PACKET / rel
            assert sha(scanpath.read_bytes()) == adaptation["originalScans"][rel]
            scan = json.loads(scanpath.read_text(encoding="utf8"))
            assert scan["base"] == original_base and len(scan["rows"]) == 1254
            assert {r["kanji"] for r in scan["rows"]} == baseline_kanji
            for item in scan["rows"]:
                guard.check()
                assert sha((REPO / item["path"]).read_bytes()) == item["baselineWorkingBytesSha256"]
                assert before[item["path"]] == item["baselineNormalizedSha256"] == after[item["path"]]
        pairs = members[ch]["pairs"]
        assert set(scan["matches"]) <= {p["pair"][1] for p in pairs}
        assert set(fm["quiz_exclusions"]) == {p["pair"][1] for p in pairs if p["decision"] == "guard"}
        assert set(fm["distractors"]) == {p["pair"][1] for p in pairs if p["decision"] == "curated"}
        assert all(p["targetLabelOnComparison"] and p["comparisonLabelOnTarget"] for p in pairs)
        for pair in pairs:
            raw = (PACKET / "comparison-cards" / (pair["pair"][1] + ".md")).read_bytes()
            assert sha(raw) == pair["baselineCardSha256"]
    comparisons = list((PACKET / "comparison-cards").glob("*.md"))
    assert len(comparisons) == 179
    for path in comparisons:
        assert path.read_bytes() == git("show", f"{BASE}:kanji/{path.name}")
    expected_records = {}
    for name in ("source-receipt.json", "supplemental-source-receipt.json", "manual-source-receipt.json"):
        receipt = json.loads((PACKET / name).read_text(encoding="utf8"))
        for filename, info in receipt["outputs"].items():
            path = PACKET / filename
            assert sha(path.read_bytes()) == info["sha256"]
            actual = {n.findtext("ent_seq") or n.findtext("literal"):
                      sha(ET.canonicalize(ET.tostring(n, encoding="unicode"), strip_text=True).encode())
                      for n in ET.parse(path).getroot()}
            assert actual == info["canonicalRecordHashes"], filename
    final = json.loads((PACKET / "final-source-audit-002.json").read_text(encoding="utf8"))
    assert final["base"] == BASE and final["completeKanjidicRecordsRechecked"] == 182
    assert sha((PACKET / "jmdict-final-families-002.xml").read_bytes()) == final["finalAdditionalOutput"]["sha256"]
    for name in ("jmdict-complete-families.xml", "jmdict-supplemental-families.xml", "jmdict-manual-families.xml", "jmdict-final-families-002.xml"):
        for node in ET.parse(PACKET / name).getroot():
            key = node.findtext("ent_seq")
            digest = sha(ET.canonicalize(ET.tostring(node, encoding="unicode"), strip_text=True).encode())
            if key in expected_records:
                assert expected_records[key] == digest
            expected_records[key] = digest
    assert len(expected_records) == final["completeJmdictUnion"] == 874
    for item in json.loads((PACKET / "external-capture-bindings.json").read_text(encoding="utf8"))["captures"]:
        raw = Path(item["localRawCapture"])
        assert sha(raw.read_bytes()) == item["rawSha256"]
        assert sha(raw.with_suffix(".txt").read_bytes()) == item["textSha256"]
    fonts = json.loads((PACKET / "stroke-font-evidence-002.json").read_text(encoding="utf8"))
    for row in fonts["members"]:
        assert sha((REPO / "strokes" / (row["kanji"] + ".json")).read_bytes()) == row["strokeSha256"]
    for font in fonts["fonts"]:
        assert sha((ROOT / "kanji-cards-android" / "app" / "src" / "main" / "res" / "font" / font["filename"]).read_bytes()) == font["sha256"]
    for ch in CHARS:
        for identifier in re.findall(r"\b\d{7}\b", normalized(REPO / "kanji" / (ch + ".md"))):
            assert identifier in expected_records, (ch, identifier)
    inventory = json.loads((PACKET / "evidence-inventory.json").read_text(encoding="utf8"))
    for name, digest in inventory["files"].items():
        assert sha((PACKET / name).read_bytes()) == digest, name
    assert {str(p.relative_to(PACKET)).replace("\\", "/") for p in PACKET.rglob("*") if p.is_file()} == set(inventory["files"]) | {"evidence-inventory.json"}
    notes = normalized(REPO / "docs" / "n1-authoring-notes.md")
    start = notes.index("## Batch 131: local unreviewed authoring candidate")
    end = notes.index("## Batch 130 reconciliation 002: protected effect allocation", start)
    assert notes[:start] + notes[end:] == git("show", f"{BASE}:docs/n1-authoring-notes.md").replace(b"\r\n", b"\n").decode()
    paths = git("diff", "--name-only", "-z", BASE).decode().strip("\0").split("\0")
    untracked = git("ls-files", "--others", "--exclude-standard", "-z").decode().strip("\0").split("\0")
    allowed = added | changed | {"manifest.json", "docs/n1-authoring-notes.md", "docs/n1-sources/batch-131-progress.json"}
    for path in paths + untracked:
        if path:
            assert path in allowed or path.startswith("docs/n1-sources/batch-131/"), path
    for incoming in ("README.md", "docs/wazawaza-sources.json", "words/わざと.md", "words/わざわざ.md"):
        assert (REPO / incoming).read_bytes().replace(b"\r\n", b"\n") == git("show", f"{BASE}:{incoming}").replace(b"\r\n", b"\n")
    result = {
        "status": "PASS", "mode": mode, "base": BASE, "head": head, "ownerSignature": signature,
        "clean": not bool(git("status", "--porcelain=v1", "--untracked-files=all")),
        "baselineRuntimeCount": len(before), "candidateRuntimeCount": len(after),
        "added": sorted(added), "removed": sorted(removed), "changed": sorted(changed),
        "allCandidateRuntimeHashesChecked": len(runtime), "allOtherRuntimeEntriesUnchanged": len(before) - len(changed),
        "supportWordChanges": "Exactly one reciprocal wrapper in each of four supports; no prose exception or metadata change.",
        "frozenPredecessorEvidenceUnchanged": True, "incomingWordOnlyChangesPreserved": True,
        "sourceReadingsExactAndOrdered": True, "baselineScanCoveragePerMember": 1254,
        "pairRows": sum(len(m["pairs"]) for m in members.values()), "withinBatchPairs": 3,
        "completeJmdictUnion": 874, "completeKanjidicRecordsRechecked": 182, "comparisonCopies": 179,
        "manifestGroupsChecked": [k for k, v in new.items() if isinstance(v, dict)],
        "manifestSha256": sha(raw_manifest), "contentVersion": new["contentVersion"],
        "evidenceInventorySha256": sha((PACKET / "evidence-inventory.json").read_bytes()),
        "producerSha256": sha(Path(__file__).read_bytes()),
        "limits": "Raw/canonical/source-order/finite-pair evidence, not independent linguistic/native/device/visual/publication acceptance. Runtime text hashes normalize CRLF to LF; evidence hashes preserve raw bytes."}
    write(out / "runtime-hashes.json", runtime)
    print(json.dumps(result, ensure_ascii=False))
finally:
    memory = guard.finish()
    write(out / "memory.json", memory)
    if "result" in locals():
        result["memory"] = memory
        write(out / "summary.json", result)

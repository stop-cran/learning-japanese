import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from common_132 import BASE, HERE, PACKET, REPO, ROOT, git, normalized, sha, start_guard, write

sys.path.insert(0, str(ROOT / "lean"))
import n1lib

if len(sys.argv) != 3 or sys.argv[1] not in ("author", "committed"):
    raise SystemExit("usage: preserve_132.py author|committed NEW_DIRECTORY")
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
        assert fields == ["Roman Konstantinovskiy", "stop-cran@list.ru",
                          "Roman Konstantinovskiy", "stop-cran@list.ru",
                          "D4C9A275A218AF747B787AFA9D94B9D311BD26A7", "G"], fields
        assert "Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>" in git("show", "-s", "--format=%B", "HEAD").decode()
        signature = {"author": fields[:2], "committer": fields[2:4], "fingerprint": fields[4], "status": fields[5]}
    old_raw = git("show", f"{BASE}:manifest.json")
    old, raw_manifest = json.loads(old_raw), (REPO / "manifest.json").read_bytes()
    new = json.loads(raw_manifest)
    if mode == "committed":
        assert raw_manifest == git("show", "HEAD:manifest.json")
    before = {p: v for group in old.values() if isinstance(group, dict) for p, v in group.items()}
    after = {p: v for group in new.values() if isinstance(group, dict) for p, v in group.items()}
    added, removed = set(after) - set(before), set(before) - set(after)
    changed = {p for p in set(before) & set(after) if before[p] != after[p]}
    assert added == {"kanji/墓.md", "strokes/墓.json"} and not removed
    assert changed == {"words/墓.md"}
    runtime = {}
    for path, digest in after.items():
        guard.check()
        raw = (REPO / path).read_bytes()
        if path.endswith((".md", ".json")):
            raw = raw.replace(b"\r\n", b"\n")
        runtime[path] = sha(raw)
        assert runtime[path] == digest, path
    raw = git("show", f"{BASE}:words/墓.md")
    baseline = raw.replace(b"\r\n", b"\n").decode()
    current = normalized(REPO / "words" / "墓.md")
    wrapper = "[墓](../kanji/墓.md)"
    assert current.count(wrapper) == baseline.count(wrapper) + 1
    assert current.replace(wrapper, "墓") == baseline
    assert (PACKET / "baseline-words" / "墓.md").read_bytes() == raw
    assert "[墓](../words/墓.md)" in normalized(REPO / "kanji" / "墓.md")
    row = json.loads((PACKET / "source-rows.json").read_bytes())[0]
    fm, _ = n1lib.parse(normalized(REPO / "kanji" / "墓.md"))
    assert row["sourceRow"] == 197 and row["statusAtFreeze"] == "pending"
    for field in ("onyomi", "kunyomi"):
        assert fm[field] == row["metadata"][field]
    for field in ("strokes", "radicalNumber"):
        assert int(fm[field]) == row["metadata"][field]
    assert fm["radical"] == row["metadata"]["radical"] == "土"
    assert row["metadata"]["strokeCountAnnotations"] == [{"count": 13, "attributes": {}}]
    baseline_kanji = {Path(p).stem for p in before if p.startswith("kanji/")}
    assert "墓" not in baseline_kanji
    scan = json.loads((PACKET / "scans" / "墓.json").read_bytes())
    assert scan["base"] == BASE and len(scan["rows"]) == len(baseline_kanji) == 1257
    assert {r["kanji"] for r in scan["rows"]} == baseline_kanji
    for item in scan["rows"]:
        guard.check()
        assert sha((REPO / item["path"]).read_bytes()) == item["baselineWorkingBytesSha256"]
        assert before[item["path"]] == item["baselineNormalizedSha256"] == after[item["path"]]
    pairs = json.loads((PACKET / "pair-dispositions.json").read_bytes())["members"][0]["pairs"]
    assert set(scan["matches"]) <= {p["pair"][1] for p in pairs}
    assert set(fm["quiz_exclusions"]) == {p["pair"][1] for p in pairs if p["decision"] == "guard"}
    assert set(fm["distractors"]) == {p["pair"][1] for p in pairs if p["decision"] == "curated"}
    assert all(p["targetLabelOnComparison"] and p["comparisonLabelOnTarget"] for p in pairs)
    for pair in pairs:
        name = pair["pair"][1]
        raw = (PACKET / "comparison-cards" / (name + ".md")).read_bytes()
        assert sha(raw) == pair["baselineCardSha256"]
        assert raw == git("show", f"{BASE}:kanji/{name}.md")
        assert sha((PACKET / "comparison-readback" / (name + ".json")).read_bytes()) == pair["readbackSha256"]
    union = {}
    for name in ("source-receipt.json", "supplemental-source-receipt.json"):
        receipt = json.loads((PACKET / name).read_bytes())
        for filename, info in receipt["outputs"].items():
            path = PACKET / filename
            assert sha(path.read_bytes()) == info["sha256"]
            actual = {n.findtext("ent_seq") or n.findtext("literal"):
                      sha(ET.canonicalize(ET.tostring(n, encoding="unicode"), strip_text=True).encode())
                      for n in ET.parse(path).getroot()}
            assert actual == info["canonicalRecordHashes"], filename
            if filename.startswith("jmdict"):
                for key, digest in actual.items():
                    if key in union:
                        assert union[key] == digest
                    union[key] = digest
    assert len(union) == 95
    for item in json.loads((PACKET / "external-capture-bindings.json").read_bytes())["captures"]:
        raw = Path(item["localRawCapture"])
        assert sha(raw.read_bytes()) == item["rawSha256"]
        assert sha(raw.with_suffix(".txt").read_bytes()) == item["textSha256"]
    fonts = json.loads((PACKET / "stroke-font-evidence.json").read_bytes())
    assert sha((REPO / "strokes" / "墓.json").read_bytes()) == fonts["members"][0]["strokeSha256"]
    for font in fonts["fonts"]:
        assert sha((ROOT / "kanji-cards-android" / "app" / "src" / "main" / "res" / "font" / font["filename"]).read_bytes()) == font["sha256"]
    for identifier in re.findall(r"\b\d{7}\b", normalized(REPO / "kanji" / "墓.md")):
        assert identifier in union, identifier
    inventory = json.loads((PACKET / "evidence-inventory.json").read_bytes())
    for name, digest in inventory["files"].items():
        assert sha((PACKET / name).read_bytes()) == digest, name
    assert {str(p.relative_to(PACKET)).replace("\\", "/") for p in PACKET.rglob("*") if p.is_file()} == set(inventory["files"]) | {"evidence-inventory.json"}
    notes = normalized(REPO / "docs" / "n1-authoring-notes.md")
    start = notes.index("## Batch 132: local unreviewed authoring candidate")
    end = notes.index("## Batch 131 reconciliation 001: bounded direct precautions", start)
    assert notes[:start] + notes[end:] == git("show", f"{BASE}:docs/n1-authoring-notes.md").replace(b"\r\n", b"\n").decode()
    paths = git("diff", "--name-only", "-z", BASE).decode().strip("\0").split("\0")
    untracked = git("ls-files", "--others", "--exclude-standard", "-z").decode().strip("\0").split("\0")
    allowed = added | changed | {"manifest.json", "docs/n1-authoring-notes.md", "docs/n1-sources/batch-132-progress.json"}
    for path in paths + untracked:
        if path:
            assert path in allowed or path.startswith("docs/n1-sources/batch-132/"), path
    result = {
        "status": "PASS", "mode": mode, "base": BASE, "head": head, "ownerSignature": signature,
        "clean": not bool(git("status", "--porcelain=v1", "--untracked-files=all")),
        "baselineRuntimeCount": len(before), "candidateRuntimeCount": len(after),
        "added": sorted(added), "removed": sorted(removed), "changed": sorted(changed),
        "allCandidateRuntimeHashesChecked": len(runtime), "allOtherRuntimeEntriesUnchanged": len(before) - len(changed),
        "supportWordChanges": "Exactly one reciprocal wrapper; no prose exception or metadata change.",
        "frozenPredecessorEvidenceUnchanged": True, "sourceReadingsExactAndOrdered": True,
        "baselineScanCoveragePerMember": len(scan["rows"]), "pairRows": len(pairs),
        "completeJmdictUnion": len(union), "completeKanjidicRecordsRechecked": 7,
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

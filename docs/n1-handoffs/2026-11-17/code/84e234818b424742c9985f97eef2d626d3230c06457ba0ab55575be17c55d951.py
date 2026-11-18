import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from common_134 import BASE, HERE, PACKET, REPO, ROOT, canonical, git, normalized, records, sha, start_guard, write

sys.path.insert(0, str(ROOT / "lean"))
import n1lib


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("author", "committed"):
        raise SystemExit("usage: preserve_134.py author|committed NEW_DIRECTORY")
    mode, out = sys.argv[1], Path(sys.argv[2]).resolve()
    assert out.parent == HERE and not out.exists()
    out.mkdir()
    guard = start_guard()
    result = None
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
        before_manifest = json.loads(git("show", f"{BASE}:manifest.json"))
        raw_manifest = (REPO / "manifest.json").read_bytes()
        candidate = json.loads(raw_manifest)
        if mode == "committed":
            assert raw_manifest == git("show", "HEAD:manifest.json")
        before, after = before_manifest["files"], candidate["files"]
        added, removed = set(after) - set(before), set(before) - set(after)
        changed = {p for p in set(before) & set(after) if before[p] != after[p]}
        assert added == {"kanji/紫.md", "strokes/紫.json"}
        assert not removed and changed == {"words/紫.md"}
        runtime = {}
        for path, digest in after.items():
            guard.check()
            raw = (REPO / path).read_bytes()
            if path.endswith((".md", ".json")):
                raw = raw.replace(b"\r\n", b"\n")
            runtime[path] = sha(raw)
            assert runtime[path] == digest, path
        baseline_kanji = {Path(p).stem for p in before if p.startswith("kanji/")}
        assert len(baseline_kanji) == 1261 and "紫" not in baseline_kanji
        raw = git("show", f"{BASE}:words/紫.md")
        baseline = raw.replace(b"\r\n", b"\n").decode()
        current = normalized(REPO / "words" / "紫.md")
        wrapper = "[紫](../kanji/紫.md)"
        assert current.count(wrapper) == baseline.count(wrapper) + 1
        assert current.replace(wrapper, "紫") == baseline
        assert (PACKET / "baseline-words" / "紫.md").read_bytes() == raw
        card = normalized(REPO / "kanji" / "紫.md")
        fm, _ = n1lib.parse(card)
        assert set(re.findall(r"\]\(\.\./words/([^/)]+)\.md\)", card)) == {"紫"}
        row = json.loads((PACKET / "source-rows.json").read_bytes())[0]
        assert row["sourceRow"] == 831 and row["statusAtFreeze"] == "pending"
        for field in ("onyomi", "kunyomi"):
            assert fm[field] == row["metadata"][field]
        for field in ("strokes", "radicalNumber"):
            assert int(fm[field]) == row["metadata"][field]
        assert fm["radical"] == row["metadata"]["radical"] == "糸"
        assert fm["quizOnyomi"] == [] and fm["quizKunyomi"] == ["むらさき"]
        scan = json.loads((PACKET / "scans" / "紫.json").read_bytes())
        assert scan["base"] == BASE and len(scan["rows"]) == len(baseline_kanji)
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
            other = pair["pair"][1]
            raw = (PACKET / "comparison-cards" / f"{other}.md").read_bytes()
            assert sha(raw) == pair["baselineCardSha256"] and raw == git("show", f"{BASE}:kanji/{other}.md")
            assert sha((PACKET / "comparison-readback" / f"{other}.json").read_bytes()) == pair["readbackSha256"]
        receipt = json.loads((PACKET / "source-receipt.json").read_bytes())
        jmdict_union, kd_union = {}, {}
        for filename, info in receipt["outputs"].items():
            raw = (PACKET / filename).read_bytes()
            assert sha(raw) == info["sha256"]
            actual = {n.findtext("ent_seq") or n.findtext("literal"): sha(canonical(n).encode()) for n in ET.fromstring(raw)}
            assert actual == info["canonicalRecordHashes"], filename
            union = jmdict_union if filename.startswith("jmdict") else kd_union
            for key, digest in actual.items():
                assert key not in union or union[key] == digest
                union[key] = digest
        supplemental = json.loads((PACKET / "supplement" / "receipt.json").read_bytes())
        raw = (PACKET / "supplement" / "kanjidic2-components-variant.xml").read_bytes()
        assert sha(raw) == supplemental["output"]["sha256"]
        for n in ET.fromstring(raw):
            ch, digest = n.findtext("literal"), sha(canonical(n).encode())
            assert supplemental["output"]["canonicalRecordHashes"][ch] == digest
            assert ch not in kd_union or kd_union[ch] == digest
            kd_union[ch] = digest
        assert set(supplemental["selection"]) == set("紫茈此糸止比")
        found = {}
        for node in records("jmdict", guard):
            spellings = {s.text for s in node.findall("k_ele/keb")}
            readings = {r.text for r in node.findall("r_ele/reb")}
            if (any(c in s for c in receipt["containsKeys"] for s in spellings)
                    or spellings & set(receipt["allExactSpellings"])
                    or readings & set(receipt["allExactReadings"])):
                found[node.findtext("ent_seq")] = sha(canonical(node).encode())
        assert found == jmdict_union and len(found) == 399
        kd_found, baseline_meanings = {}, {}
        for node in records("kanjidic2", guard):
            ch = node.findtext("literal")
            if ch in kd_union:
                kd_found[ch] = sha(canonical(node).encode())
            if ch in baseline_kanji:
                baseline_meanings[ch] = [m.text for m in node.findall("reading_meaning/rmgroup/meaning") if m.get("m_lang") in (None, "en")]
            if ch == "紫":
                for kind in ("on", "kun"):
                    assert row["metadata"][kind + "yomi"] == [r.text for r in node.findall(f"reading_meaning/rmgroup/reading[@r_type='ja_{kind}']")]
                assert row["metadata"]["strokeCountAnnotations"] == [{"count": int(s.text), "attributes": dict(s.attrib)} for s in node.findall("misc/stroke_count")]
        assert kd_found == kd_union and len(kd_union) == 59
        keys = set(scan["expandedKeywords"])
        for item in scan["rows"]:
            assert item["completeMeanings"] == baseline_meanings[item["kanji"]]
            hits = sorted(keys & set(re.findall("[a-z]+", " ".join([item["title"], *item["completeMeanings"]]).lower())))
            assert item["matchedKeywords"] == hits
        for identifier in re.findall(r"\b\d{7}\b", card):
            assert identifier in jmdict_union, identifier
        for item in json.loads((PACKET / "external-capture-bindings.json").read_bytes())["captures"]:
            raw = Path(item["localRawCapture"])
            assert sha(raw.read_bytes()) == item["rawSha256"]
            assert sha(raw.with_suffix(".txt").read_bytes()) == item["textSha256"]
        fonts = json.loads((PACKET / "stroke-font-evidence.json").read_bytes())
        assert sha((REPO / "strokes" / "紫.json").read_bytes()) == fonts["members"][0]["strokeSha256"]
        for font in fonts["fonts"]:
            assert sha((ROOT / "kanji-cards-android" / "app" / "src" / "main" / "res" / "font" / font["filename"]).read_bytes()) == font["sha256"]
        inventory = json.loads((PACKET / "evidence-inventory.json").read_bytes())
        for name, digest in inventory["files"].items():
            assert sha((PACKET / name).read_bytes()) == digest, name
        assert {str(p.relative_to(PACKET)).replace("\\", "/") for p in PACKET.rglob("*") if p.is_file()} == set(inventory["files"]) | {"evidence-inventory.json"}
        notes = normalized(REPO / "docs" / "n1-authoring-notes.md")
        start = notes.index("## Batch 134: local unreviewed authoring candidate")
        end = notes.index("## Batch 133: local unreviewed authoring candidate", start)
        assert notes[:start] + notes[end:] == git("show", f"{BASE}:docs/n1-authoring-notes.md").replace(b"\r\n", b"\n").decode()
        paths = git("diff", "--name-only", "-z", BASE).decode().strip("\0").split("\0")
        untracked = git("ls-files", "--others", "--exclude-standard", "-z").decode().strip("\0").split("\0")
        allowed = added | changed | {"manifest.json", "docs/n1-authoring-notes.md", "docs/n1-sources/batch-134-progress.json"}
        for path in paths + untracked:
            if path:
                assert path in allowed or path.startswith("docs/n1-sources/batch-134/"), path
        result = {
            "status": "PASS", "mode": mode, "base": BASE, "head": head, "ownerSignature": signature,
            "clean": not bool(git("status", "--porcelain=v1", "--untracked-files=all")),
            "baselineRuntimeCount": len(before), "candidateRuntimeCount": len(after),
            "added": sorted(added), "removed": sorted(removed), "changed": sorted(changed),
            "allCandidateRuntimeHashesChecked": len(runtime), "allOtherRuntimeEntriesUnchanged": len(before) - len(changed),
            "supportWordChanges": "Exactly one reciprocal wrapper; no prose exception, metadata, level or exclusion change.",
            "frozenPredecessorEvidenceUnchanged": True, "sourceReadingsExactAndOrdered": True,
            "baselineScanCoveragePerMember": len(baseline_kanji), "pairRows": len(pairs),
            "completeJmdictUnion": len(jmdict_union), "completeKanjidicUnion": len(kd_union),
            "originalSourceRecomputation": "The mixed contains/exact spelling/exact reading selection, all retained complete records and every scan's complete meanings re-read against hash-pinned originals.",
            "manifestSha256": sha(raw_manifest), "contentVersion": candidate["contentVersion"],
            "evidenceInventorySha256": sha((PACKET / "evidence-inventory.json").read_bytes()),
            "producerSha256": sha(Path(__file__).read_bytes()),
            "limits": "Finite author evidence, not independent review, arbitrary/custom/multiple-borrow pools, native/device, visual fallback or publication acceptance. Runtime text hashes normalize CRLF to LF; evidence hashes preserve raw bytes."}
        write(out / "runtime-hashes.json", runtime)
        print(json.dumps(result, ensure_ascii=False))
    finally:
        memory = guard.finish()
        write(out / "memory.json", memory)
        if result is not None:
            result["memory"] = memory
            write(out / "summary.json", result)


if __name__ == "__main__":
    main()

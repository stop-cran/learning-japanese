import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from b130_common import BASE, CHARS, GUARD_SHA, HERE, PACKET, REPO, ROOT, git, normalized, sha, start_guard, write

sys.path.insert(0, str(ROOT / "lean"))
import n1lib

PARENT = "ce1b5c895fac90852143f322a115c2de4e768e20"
OUT = REPO / "docs" / "n1-sources" / "batch-130-reconciliation"
PROGRESS = "docs/n1-sources/batch-130-progress-reconciliation-002.json"
CARDS = {f"kanji/{ch}.md" for ch in CHARS}
FIXED = CARDS | {"manifest.json", "docs/n1-authoring-notes.md", PROGRESS,
                 "docs/n1-sources/batch-130-progress-reconciliation-001.json"}
PREFIX = "docs/n1-sources/batch-130-reconciliation/"


def flatten(manifest):
    return {path: value for group in manifest.values() if isinstance(group, dict) for path, value in group.items()}


def canonical(node):
    return sha(ET.canonicalize(ET.tostring(node, encoding="unicode"), strip_text=True).encode())


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("author", "committed"):
        raise SystemExit("usage: preserve_b130_reconciliation.py author|committed NEW_DIRECTORY")
    mode, dest = sys.argv[1], Path(sys.argv[2]).resolve()
    assert dest.parent == HERE and not dest.exists()
    dest.mkdir()
    guard = start_guard()
    try:
        head = git("rev-parse", "HEAD").decode().strip()
        signature = None
        if mode == "author":
            assert head == PARENT
        else:
            assert git("rev-parse", "HEAD^@").decode().split() == [PARENT]
            assert not git("status", "--porcelain=v1", "--untracked-files=all")
            git("verify-commit", "HEAD")
            fields = git("show", "-s", "--format=%an%n%ae%n%cn%n%ce%n%GF%n%G?", "HEAD").decode().splitlines()
            assert fields[:4] == ["Roman Konstantinovskiy", "stop-cran@list.ru",
                                  "Roman Konstantinovskiy", "stop-cran@list.ru"]
            assert fields[4:] == ["D4C9A275A218AF747B787AFA9D94B9D311BD26A7", "G"]
            assert "Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>" in git("show", "-s", "--format=%B", "HEAD").decode()
            signature = {"author": fields[:2], "committer": fields[2:4], "fingerprint": fields[4], "status": fields[5]}
        changed = git("diff", "--name-only", PARENT).decode().splitlines()
        untracked = git("ls-files", "--others", "--exclude-standard").decode().splitlines()
        all_paths = set(changed + untracked)
        assert all(path in FIXED or path.startswith(PREFIX) for path in all_paths), sorted(all_paths - FIXED)
        assert not git("diff", "--name-only", "--diff-filter=D", PARENT)
        manifest_raw = (REPO / "manifest.json").read_bytes()
        manifest = json.loads(manifest_raw)
        previous = json.loads(git("show", f"{PARENT}:manifest.json"))
        base = json.loads(git("show", f"{BASE}:manifest.json"))
        current, prior, published = map(flatten, (manifest, previous, base))
        assert len(current) == len(prior) == 8730 and len(published) == 8724
        assert set(current) == set(prior)
        assert {p for p in current if current[p] != prior[p]} == CARDS
        assert set(manifest) == set(previous) == set(base)
        assert {k for k in manifest if isinstance(manifest[k], dict)} == {
            k for k in previous if isinstance(previous[k], dict)}
        for key in manifest:
            if not isinstance(manifest[key], dict) and key != "contentVersion":
                assert manifest[key] == previous[key] == base[key], key
        actual_runtime = {}
        for path, digest in current.items():
            guard.check()
            raw = (REPO / path).read_bytes()
            if path.endswith((".md", ".json")):
                raw = raw.replace(b"\r\n", b"\n")
            actual_runtime[path] = sha(raw)
            assert actual_runtime[path] == digest, path
        additions = {f"{folder}/{ch}.{suffix}" for ch in CHARS for folder, suffix in (("kanji", "md"), ("strokes", "json"))}
        assert set(current) - set(published) == additions and not set(published) - set(current)
        words = {"塀": ("塀", 3), "拍": ("拍手", 3), "耗": ("消耗", 2)}
        assert {p for p in published if published[p] != current[p]} == {f"words/{word}.md" for word, _ in words.values()}
        for ch, (word, level) in words.items():
            rel = f"words/{word}.md"
            assert (REPO / rel).read_bytes() == git("show", f"{PARENT}:{rel}")
            old = git("show", f"{BASE}:{rel}").replace(b"\r\n", b"\n").decode()
            new = normalized(REPO / rel)
            wrapper = f"[{ch}](../kanji/{ch}.md)"
            assert new.count(wrapper) == old.count(wrapper) + 1 and new.replace(wrapper, ch) == old
            fm, _ = n1lib.parse(new)
            assert int(fm["jlpt"]) == level
            assert (REPO / "strokes" / (ch + ".json")).read_bytes() == git("show", f"{PARENT}:strokes/{ch}.json")
        pair_path = OUT / "pair-dispositions-001.json"
        pairs = json.loads(pair_path.read_text(encoding="utf-8"))
        assert len(pairs["rows"]) == 28 and not pairs["openQuizHolds"]
        rows = {"/".join(r["pair"]): r for r in pairs["rows"]}
        assert len(rows) == 28 and all(not row["openQuizHold"] for row in rows.values())
        for ch in CHARS:
            old, _ = n1lib.parse(git("show", f"{PARENT}:kanji/{ch}.md").replace(b"\r\n", b"\n").decode())
            new, _ = n1lib.parse(normalized(REPO / "kanji" / (ch + ".md")))
            old_guards, new_guards = old.pop("quiz_exclusions"), new.pop("quiz_exclusions")
            assert old == new, ch
            assert new_guards[:len(old_guards)] == old_guards
            expected_extra = [r["pair"][1] for r in pairs["rows"] if r["pair"][0] == ch
                              and r["decision"] != "bounded-noncollision"]
            assert new_guards[len(old_guards):] == expected_extra, (ch, expected_extra)
            for identifier in re.findall(r"\b\d{7}\b", normalized(REPO / "kanji" / (ch + ".md"))):
                available = set()
                for name in ("jmdict-complete-families.xml", "jmdict-supplemental-families.xml", "jmdict-final-families.xml"):
                    available |= {n.findtext("ent_seq") for n in ET.parse(PACKET / name).getroot()}
                available |= {n.findtext("ent_seq") for n in ET.parse(OUT / "jmdict-families.xml").getroot()}
                assert identifier in available, (ch, identifier)
        original_inventory = json.loads((PACKET / "evidence-inventory.json").read_text(encoding="utf-8"))
        assert (PACKET / "evidence-inventory.json").read_bytes() == git("show", f"{PARENT}:docs/n1-sources/batch-130/evidence-inventory.json")
        for name, digest in original_inventory["files"].items():
            guard.check()
            assert sha((PACKET / name).read_bytes()) == digest, name
        assert {p.relative_to(PACKET).as_posix() for p in PACKET.rglob("*") if p.is_file()} == set(original_inventory["files"]) | {"evidence-inventory.json"}
        old_notes = git("show", f"{PARENT}:docs/n1-authoring-notes.md")
        notes = (REPO / "docs" / "n1-authoring-notes.md").read_bytes()
        start = notes.index(b"## Batch 130 reconciliation 001: local author successor")
        end = notes.index(b"## Batch 130: local unreviewed authoring candidate", start)
        assert notes[:start] + notes[end:] == old_notes, "Earlier notes must remain byte-identical after removing the single inserted section"
        receipt = json.loads((OUT / "source-receipt.json").read_text(encoding="utf-8"))
        for name, record in receipt["outputs"].items():
            raw = (OUT / name).read_bytes()
            assert sha(raw) == record["sha256"]
            actual = {n.findtext("ent_seq") or n.findtext("literal"): canonical(n) for n in ET.fromstring(raw)}
            assert actual == record["canonicalRecordHashes"]
        for ch, record in receipt["comparisonCards"].items():
            raw = (OUT / record["path"]).read_bytes()
            assert sha(raw) == record["sha256"] and raw == git("show", f"{PARENT}:kanji/{ch}.md")
        assert len(receipt["outputs"]["jmdict-families.xml"]["canonicalRecordHashes"]) == 99
        assert len(receipt["outputs"]["kanjidic2-records.xml"]["canonicalRecordHashes"]) == 31
        assert sha((OUT / "query-membership.json").read_bytes()) == receipt["membershipSha256"]
        for row in pairs["rows"]:
            assert row["completeComparisonCard"] == receipt["comparisonCards"][row["pair"][1]]
            assert row["comparisonLabelOnTarget"] and row["targetLabelOnComparison"] and row["positiveSourceBasis"]
            for key, digest in row["completeFamilyCanonicalHashes"].items():
                assert receipt["outputs"]["jmdict-families.xml"]["canonicalRecordHashes"][key] == digest
        for packet in (PACKET, OUT):
            names = ("external-capture-bindings.json", "supplemental-external-bindings.json") if packet == PACKET else ("external-capture-bindings.json",)
            for name in names:
                for item in json.loads((packet / name).read_text(encoding="utf-8"))["captures"]:
                    raw = Path(item["localRawCapture"])
                    assert sha(raw.read_bytes()) == item["rawSha256"]
                    assert sha(raw.with_suffix(".txt").read_bytes()) == item["textSha256"]
        for family in ("claude", "gpt"):
            mapping = json.loads((OUT / "responses" / (family + "-mapping-001.json")).read_text(encoding="utf-8"))
            for binding in mapping["originalBindings"]:
                assert sha(Path(binding["path"]).read_bytes()) == binding["sha256"]
            other = "gpt" if family == "claude" else "claude"
            text = (OUT / "responses" / (family + "-response-001.md")).read_text(encoding="utf-8")
            assert other not in text.lower()
            assert other not in json.dumps(mapping, ensure_ascii=False).lower()
            if family == "gpt":
                ids = "D2 D3 D4 D5 D6 D8 D9 D10 D11 D12 D13 D14 D17 D18 D19 D20 D21 D22 D23 D24 D26 E5 E7 E8".split()
                assert mapping["originalOpenClaimIds"] == ids
                assert [r["id"] for r in mapping["comparisonDispositions"]] == ids
                assert set(mapping["limits"]) == {f"L{i}" for i in range(1, 11)}
                for item in mapping["comparisonDispositions"]:
                    assert item["authorDisposition"] == rows[item["neutralRow"]]["decision"]
                    assert item["neutralTableSha256"] == sha(pair_path.read_bytes())
            else:
                assert mapping["originalOpenClaimIds"] == []
                assert set(mapping["limits"]) == {f"L{i}" for i in range(1, 8)}
        for name in ("pair-dispositions-001.json", "authored-source-analysis-001.json", "source-receipt.json"):
            text = (OUT / name).read_text(encoding="utf-8").lower()
            assert not any(word in text for word in ("claude", "gpt", "verdict")), name
        inventory = json.loads((OUT / "evidence-inventory-002.json").read_text(encoding="utf-8"))
        assert {p.relative_to(OUT).as_posix() for p in OUT.rglob("*") if p.is_file()} == set(inventory["files"]) | {"evidence-inventory-002.json"}
        for name, digest in inventory["files"].items():
            guard.check()
            assert sha((OUT / name).read_bytes()) == digest, name
        progress = json.loads((REPO / PROGRESS).read_text(encoding="utf-8"))
        assert (progress["publishedDelivered"], progress["undelivered"], progress["frozenTotal"]) == (261, 967, 1228)
        assert progress["manifestSha256"] == sha(manifest_raw) and progress["contentVersion"] == manifest["contentVersion"]
        if mode == "committed":
            assert manifest_raw == git("show", "HEAD:manifest.json")
            assert not git("status", "--porcelain=v1", "--untracked-files=all")
        result = {
            "status": "PASS", "mode": mode, "parent": PARENT, "publishedBase": BASE, "head": head,
            "ownerSignature": signature, "clean": not bool(git("status", "--porcelain=v1", "--untracked-files=all")),
            "exactChangedFileInventory": sorted(all_paths), "runtimeChangedFromParent": sorted(CARDS),
            "allRuntimeHashesChecked": len(actual_runtime), "otherParentRuntimeEntriesUnchanged": len(current) - len(CARDS),
            "baselineRuntimeCount": len(published), "candidateRuntimeCount": len(current),
            "baselineAddedRuntime": sorted(additions), "baselineModifiedWords": [f"words/{word}.md" for word, _ in words.values()],
            "supportWordsAndEasierLevelsUnchangedFromParent": True, "baselineWrapperChangesExactlyOneEach": True,
            "geometryMetadataPracticeCurationPreserved": True, "priorGuardOrderPreserved": True,
            "allPriorTrackedEvidenceOutsideAllowedDeltaUnchanged": True,
            "originalPacketRawFilesChecked": len(original_inventory["files"]) + 1,
            "earlierNotesRawBytesPreserved": True, "newSourceCanonicalRecords": {"jmdict": 99, "kanjidic2": 31},
            "completeComparisonCards": 28, "neutralPairRows": 28, "historicalGptOpenIdsPreserved": 24,
            "familyIsolationChecked": True, "openQuizHolds": [],
            "manifestGroupsChecked": [key for key, value in manifest.items() if isinstance(value, dict)],
            "manifestSha256": sha(manifest_raw), "contentVersion": manifest["contentVersion"],
            "newPacketInventorySha256": sha((OUT / "evidence-inventory-002.json").read_bytes()),
            "producerSha256": sha(Path(__file__).read_bytes()), "guardSha256": GUARD_SHA,
            "limits": "Author finite-source reconciliation, not independent confirmation; lexical/image allocation uncertainty and bounded reading risks retained. No arbitrary/custom/multiple-borrow/native/device/visual/publication acceptance.",
        }
        write(dest / "runtime-hashes.json", actual_runtime)
        write(dest / "summary.json", result)
        print(json.dumps(result, ensure_ascii=False), flush=True)
    finally:
        write(dest / "memory.json", guard.finish())


if __name__ == "__main__":
    main()

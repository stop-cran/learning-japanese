import collections
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from b130_common import BASE, GUARD_SHA, HERE, PACKET, REPO, ROOT, git, normalized, sha, start_guard, write

sys.path.insert(0, str(ROOT / "lean"))
import n1lib

PARENT = "d440617274eef6ea7611e60f147d6483f29ca710"
OUT = REPO / "docs" / "n1-sources" / "batch-130-reconciliation"
PREFIX = OUT.relative_to(REPO).as_posix() + "/"
PROGRESS = "docs/n1-sources/batch-130-progress-reconciliation-003.json"
CHANGED_OLD = {"kanji/拍.md", "manifest.json", "docs/n1-authoring-notes.md"}


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("author", "committed"):
        raise SystemExit("usage: preserve_second_b130.py author|committed NEW_DIRECTORY")
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
            assert fields == ["Roman Konstantinovskiy", "stop-cran@list.ru",
                              "Roman Konstantinovskiy", "stop-cran@list.ru",
                              "D4C9A275A218AF747B787AFA9D94B9D311BD26A7", "G"]
            assert "Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>" in git("show", "-s", "--format=%B", "HEAD").decode()
            signature = {"author": fields[:2], "committer": fields[2:4], "fingerprint": fields[4], "status": fields[5]}
        parent_paths = set(git("ls-tree", "-r", "--name-only", PARENT).decode().splitlines())
        changed = set(git("diff", "--name-only", PARENT).decode().splitlines())
        changed |= set(git("ls-files", "--others", "--exclude-standard").decode().splitlines())
        assert changed & parent_paths == CHANGED_OLD, sorted(changed & parent_paths)
        assert all(path.startswith(PREFIX) or path == PROGRESS for path in changed - parent_paths)
        assert not git("diff", "--name-only", "--diff-filter=D", PARENT)
        manifest_raw = (REPO / "manifest.json").read_bytes()
        manifest, previous = json.loads(manifest_raw), json.loads(git("show", PARENT + ":manifest.json"))
        flatten = lambda data: {path: value for group in data.values() if isinstance(group, dict) for path, value in group.items()}
        current, prior = flatten(manifest), flatten(previous)
        assert len(current) == len(prior) == 8730 and current.keys() == prior.keys()
        assert {path for path in current if current[path] != prior[path]} == {"kanji/拍.md"}
        assert manifest.keys() == previous.keys()
        for key in manifest:
            if not isinstance(manifest[key], dict) and key != "contentVersion":
                assert manifest[key] == previous[key]
        for path, digest in current.items():
            guard.check()
            raw = (REPO / path).read_bytes()
            if path.endswith((".md", ".json")):
                raw = raw.replace(b"\r\n", b"\n")
            assert sha(raw) == digest, path
        old_card = git("show", PARENT + ":kanji/拍.md").replace(b"\r\n", b"\n").decode()
        new_card = normalized(REPO / "kanji" / "拍.md")
        old_fm, _ = n1lib.parse(old_card)
        new_fm, _ = n1lib.parse(new_card)
        old_guards, new_guards = old_fm.pop("quiz_exclusions"), new_fm.pop("quiz_exclusions")
        assert old_fm == new_fm
        assert new_guards == old_guards + ["響"] and len(new_guards) == len(set(new_guards))
        old_note = """  fingers. [響](響.md) instead concerns sound carrying or resonating,
  and an effect reaching someone: neither defines the clapping action
  or a musical pulse merely because a clap can resound."""
        new_note = """  fingers. [響](響.md) concerns sound carrying or resonating rather
  than the clapping action or a musical pulse. Its effect/impression
  senses also meet the complete 打つ/rare 拍つ family's
  move/impress/touch senses. A direct precaution protects their
  unresolved allocation to bare 拍; it does not make ordinary
  拍 and 響 synonyms."""
        assert old_card.count(old_note) == new_card.count(new_note) == 1
        assert new_card == old_card.replace(", 筆]\n", ", 筆, 響]\n").replace(old_note, new_note)
        for rel in ("kanji/塀.md", "kanji/耗.md", "kanji/響.md", "words/塀.md", "words/拍手.md", "words/消耗.md",
                    "strokes/塀.json", "strokes/拍.json", "strokes/耗.json"):
            assert (REPO / rel).read_bytes() == git("show", PARENT + ":" + rel), rel
        notes = (REPO / "docs" / "n1-authoring-notes.md").read_bytes()
        start = notes.index(b"## Batch 130 reconciliation 002: protected effect allocation")
        end = notes.index(b"## Batch 130 reconciliation 001: local author successor", start)
        assert notes[:start] + notes[end:] == git("show", PARENT + ":docs/n1-authoring-notes.md")
        old_table_raw = (OUT / "pair-dispositions-001.json").read_bytes()
        before = json.loads(old_table_raw)
        after = json.loads((OUT / "pair-dispositions-002.json").read_text(encoding="utf-8"))
        assert len(before["rows"]) == len(after["rows"]) == 28
        assert [a["pair"] for a, b in zip(before["rows"], after["rows"]) if a != b] == [["拍", "響"]]
        counts = dict(collections.Counter(row["decision"] for row in after["rows"]))
        assert counts == after["counts"] == {"guard": 8, "precaution": 17, "bounded-noncollision": 3}
        row = next(item for item in after["rows"] if item["pair"] == ["拍", "響"])
        assert row["decision"] == "precaution" and row["directExclusionOnNewEndpoint"] and not row["openQuizHold"]
        assert not after["openQuizHolds"] and after["remainingLexicalUncertainty"] == before["remainingLexicalUncertainty"]
        assert after["supersedes"]["sha256"] == sha(old_table_raw)
        reuse = json.loads((OUT / "source-reuse-002.json").read_text(encoding="utf-8"))
        for name, digest in reuse["files"].items():
            assert sha((OUT / name).read_bytes()) == digest
        records = {node.findtext("ent_seq"): node for node in ET.parse(OUT / "jmdict-families.xml").getroot()}
        for identifier, digest in reuse["completeFamiliesRead"].items():
            assert sha(ET.canonicalize(ET.tostring(records[identifier], encoding="unicode"), strip_text=True).encode()) == digest
            assert row["completeFamilyCanonicalHashes"][identifier] == digest
        previous_packet = json.loads((OUT / "evidence-inventory-002.json").read_text(encoding="utf-8"))
        for name, digest in previous_packet["files"].items():
            guard.check()
            assert sha((OUT / name).read_bytes()) == digest, name
        original_packet = json.loads((PACKET / "evidence-inventory.json").read_text(encoding="utf-8"))
        for name, digest in original_packet["files"].items():
            guard.check()
            assert sha((PACKET / name).read_bytes()) == digest, name
        inventory = json.loads((OUT / "evidence-inventory-003.json").read_text(encoding="utf-8"))
        assert set(inventory["files"]) | {"evidence-inventory-003.json"} == {p.relative_to(OUT).as_posix() for p in OUT.rglob("*") if p.is_file()}
        for name, digest in inventory["files"].items():
            guard.check()
            assert sha((OUT / name).read_bytes()) == digest, name
        original_gpt = json.loads((OUT / "responses" / "gpt-mapping-001.json").read_text(encoding="utf-8"))
        gpt = json.loads((OUT / "responses" / "gpt-mapping-002.json").read_text(encoding="utf-8"))
        assert gpt["originalOpenClaimIds"] == original_gpt["originalOpenClaimIds"]
        assert len(gpt["originalOpenClaimIds"]) == 24
        assert gpt["originalComparisonQuestions"] == [item["initialQuestion"] for item in original_gpt["comparisonDispositions"]]
        assert gpt["historicalD18Disposition"] == next(item for item in original_gpt["comparisonDispositions"] if item["id"] == "D18")
        assert gpt["currentD18"]["directPairProtected"] and not gpt["lexicalAllocationResolved"]
        for family in ("claude", "gpt"):
            other = "gpt" if family == "claude" else "claude"
            for kind, suffix in (("response", "md"), ("mapping", "json")):
                assert other not in (OUT / "responses" / (family + "-" + kind + "-002." + suffix)).read_text(encoding="utf-8").lower()
        for name in ("source-reuse-002.json", "pair-dispositions-002.json"):
            text = (OUT / name).read_text(encoding="utf-8").lower()
            assert not any(word in text for word in ("claude", "gpt", "verdict"))
        assignment = json.loads((HERE / "reconciliation-002-source-read-001" / "assignment-bindings.json").read_text(encoding="utf-8"))
        for path, digest in assignment.items():
            assert sha(Path(path).read_bytes()) == digest, path
        progress = json.loads((REPO / PROGRESS).read_text(encoding="utf-8"))
        assert progress["manifestSha256"] == sha(manifest_raw) and progress["contentVersion"] == manifest["contentVersion"]
        assert (progress["publishedDelivered"], progress["undelivered"]) == (261, 967)
        assert progress["status"] == "unpublished-author-proposal-awaiting-two-independent-confirmations"
        if mode == "committed":
            assert manifest_raw == git("show", "HEAD:manifest.json")
            assert not git("status", "--porcelain=v1", "--untracked-files=all")
        result = {
            "status": "PASS", "mode": mode, "parent": PARENT, "publishedBase": BASE, "head": head,
            "ownerSignature": signature, "clean": not bool(git("status", "--porcelain=v1", "--untracked-files=all")),
            "exactChangedFileInventory": sorted(changed), "existingTrackedFilesChanged": sorted(CHANGED_OLD),
            "runtimeChangedFromParent": ["kanji/拍.md", "manifest.json"],
            "runtimeHashesChecked": len(current), "otherRuntimeManifestEntriesUnchanged": len(current) - 1,
            "onlyGuardAppendAndQualifiedNotes": True, "allOtherParentTrackedBlobsPreserved": True,
            "metadataPracticeCurationSupportsEasierLevelsWrappersGeometryPreserved": True,
            "earlierNotesRawBytesPreserved": True, "oldReconciliationInventoryFilesChecked": len(previous_packet["files"]) + 1,
            "originalPacketFilesChecked": len(original_packet["files"]) + 1,
            "neutralPairCounts": counts, "changedPairOnly": ["拍", "響"],
            "originalQuestionsAndD18HistoricalDispositionPreserved": True,
            "familyIsolationChecked": True, "lexicalAllocationResolved": False, "ordinaryCollisionEstablished": False,
            "unprotectedAuthorQuizHolds": [], "awaitingTwoIndependentConfirmations": True,
            "manifestSha256": sha(manifest_raw), "contentVersion": manifest["contentVersion"],
            "packetInventorySha256": sha((OUT / "evidence-inventory-003.json").read_bytes()),
            "producerSha256": sha(Path(__file__).read_bytes()), "guardSha256": GUARD_SHA,
            "limits": progress["limits"],
        }
        write(dest / "summary.json", result)
        print(json.dumps(result, ensure_ascii=False))
    finally:
        write(dest / "memory.json", guard.finish())


if __name__ == "__main__":
    main()

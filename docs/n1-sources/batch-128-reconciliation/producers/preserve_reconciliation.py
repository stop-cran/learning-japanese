import hashlib
import json
import re
import sys
from pathlib import Path
from recon_common import BASE, HERE, ORIGINAL, PACKET, PARENT, REPO, SCRATCH, git, sha, start_guard, write


def flattened(manifest):
    return {p: v for group in manifest.values() if isinstance(group, dict) for p, v in group.items()}


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("author", "committed"):
        raise SystemExit("usage: preserve_reconciliation.py author|committed NEW_DIRECTORY")
    mode, out = sys.argv[1], Path(sys.argv[2]).resolve()
    assert out.parent == SCRATCH and not out.exists()
    out.mkdir()
    guard = start_guard()
    try:
        head = git("rev-parse", "HEAD").decode().strip()
        if mode == "author":
            assert head == PARENT
        else:
            assert git("rev-parse", "HEAD^@").decode().split() == [PARENT]
            assert not git("status", "--porcelain=v1", "--untracked-files=all")
        previous = json.loads(git("show", f"{PARENT}:manifest.json"))
        raw = (REPO / "manifest.json").read_bytes()
        current = json.loads(raw)
        if mode == "committed":
            assert raw == git("show", "HEAD:manifest.json")
        before, after = flattened(previous), flattened(current)
        assert before.keys() == after.keys()
        changed = {p for p in before if before[p] != after[p]}
        assert changed == {"kanji/唇.md"}
        for path, digest in after.items():
            guard.check()
            data = (REPO / path).read_bytes()
            if path.endswith((".md", ".json")):
                data = data.replace(b"\r\n", b"\n")
            assert sha(data) == digest, path
        for path in ("words/唇.md", "strokes/唇.json", "docs/n1-sources/batch-128-progress.json"):
            assert (REPO / path).read_bytes() == git("show", f"{PARENT}:{path}")
        old_card = git("show", f"{PARENT}:kanji/唇.md").decode("utf-8").replace("\r\n", "\n")
        new_card = (REPO / "kanji" / "唇.md").read_text(encoding="utf-8")
        old_meta = old_card.split("---", 2)[1]
        new_meta = new_card.split("---", 2)[1]
        assert re.sub(r"quiz_exclusions:.*", "", old_meta) == re.sub(r"quiz_exclusions:.*", "", new_meta)
        old_guards = re.search(r"quiz_exclusions: \[([^\]]*)\]", old_meta).group(1).split(", ")
        new_guards = re.search(r"quiz_exclusions: \[([^\]]*)\]", new_meta).group(1).split(", ")
        assert new_guards == old_guards + ["咲", "刃", "郊"]
        expected = old_card.replace(
            "  make a petal and an entire flower interchangeable in every context.\n",
            '  make a petal and an entire flower interchangeable in every context.\n'
            '  The English [咲](咲.md) choice, "blossom; bloom," can also be read as\n'
            '  a noun near this petal sense, so it is guarded directly. 咲く itself\n'
            '  means "to bloom," not a word for a petal or for lips.\n', 1).replace(
            "  border or shore, or that ほとり is an ordinary reading of 唇.\n",
            '  border or shore, or that ほとり is an ordinary reading of 唇.\n'
            '  The quotation lacks context fixing its reach. [刃](刃.md), "blade;\n'
            '  cutting edge," and [郊](郊.md), "outskirts; suburbs," are also guarded\n'
            '  conservatively as qualified edge or outer-area choices. This prevents\n'
            '  an unresolved broad-choice ambiguity, not a claim that lips are\n'
            '  cutting tools or suburban areas.\n', 1).replace(
            "quiz_exclusions: [" + ", ".join(old_guards) + "]",
            "quiz_exclusions: [" + ", ".join(new_guards) + "]", 1)
        assert new_card == expected
        history = {}
        for item in git("ls-tree", "-r", "-z", PARENT, "--", "docs/n1-sources/batch-128", "docs/n1-sources/batch-128-progress.json").decode("utf-8").rstrip("\0").split("\0"):
            guard.check()
            meta, path = item.split("\t", 1)
            blob = meta.split()[2]
            data = (REPO / path).read_bytes()
            assert hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest() == blob, path
            history[path] = {"gitBlob": blob, "rawSha256": sha(data), "bytes": len(data)}
        write(out / "preserved-history.json", history)
        table = json.loads((PACKET / "pair-dispositions.json").read_text(encoding="utf-8"))
        assert [r["id"] for r in table["claims"]] == ["Q" + str(i) for i in range(1, 16)]
        assert table["addedDirectGuards"] == ["咲", "刃", "郊"]
        for row in table["claims"]:
            assert row["declaredEndpointStatus"]["newEndpoint"] == (row["pair"][1] in new_guards)
        policy = json.loads((SCRATCH / "reconciliation-admission-bindings.json").read_text(encoding="utf-8"))["neutralityPolicy"]
        name_pattern = r"\b(?:" + "|".join(re.escape(t) for t in policy["isolationTokens"]) + r")\b"
        neutral = {}
        for path in PACKET.rglob("*"):
            if not path.is_file() or path.name in ("response-a.md", "response-b.md"):
                continue
            text = path.read_text(encoding="utf-8")
            if path.name.startswith("source-receipt") and path.suffix == ".json":
                obj = json.loads(text)
                obj.pop("admissionBindings", None)
                text = json.dumps(obj, ensure_ascii=False)
            assert not re.search(name_pattern, text, re.I), path
            assert not re.search(policy["outcomePattern"], text), path
            neutral[path.relative_to(PACKET).as_posix()] = sha(path.read_bytes())
        assert not re.search(r"\b" + re.escape(policy["isolationTokens"][1]) + r"\b", (PACKET / "response-a.md").read_text(encoding="utf-8"), re.I)
        assert not re.search(r"\b" + re.escape(policy["isolationTokens"][0]) + r"\b", (PACKET / "response-b.md").read_text(encoding="utf-8"), re.I)
        allowed = {"kanji/唇.md", "manifest.json", "docs/n1-authoring-notes.md", "docs/n1-sources/batch-128-progress-reconciliation-001.json"}
        paths = git("-c", "core.quotepath=false", "diff", "--name-only", PARENT).decode("utf-8").splitlines()
        paths += git("-c", "core.quotepath=false", "ls-files", "--others", "--exclude-standard").decode("utf-8").splitlines()
        assert all(p in allowed or p.startswith("docs/n1-sources/batch-128-reconciliation/") for p in paths), paths
        git("-c", "core.whitespace=blank-at-eol,blank-at-eof,space-before-tab,cr-at-eol", "diff", "--check", PARENT)
        result = {
            "status": "PASS", "mode": mode, "parentCommit": PARENT, "publishedBase": BASE, "head": head,
            "runtimeChangedFromParent": sorted(changed), "runtimeAddedOrRemoved": [],
            "manifestMappedRuntimeEntries": len(after), "parentRuntimeEntriesUnchanged": len(before) - 1,
            "allCandidateRuntimeHashesChecked": len(after), "supportWordAndGeometryRawBytesPreserved": True,
            "allOtherCardMetadataAndExactAllowedBodyEdits": True, "originalEvidenceFilesPreserved": len(history),
            "originalProgressPreserved": True, "sharedNeutralFilesChecked": len(neutral), "familyResponsesIsolated": True,
            "manifestSha256": sha(raw), "contentVersion": current["contentVersion"],
            "changedPaths": paths, "producerSha256": sha(Path(__file__).read_bytes()),
            "limits": "Runtime text hashes normalize CRLF to LF; raw evidence/word/geometry hashes do not. This is not semantic or native acceptance.",
        }
        write(out / "summary.json", result)
        print(json.dumps({k: v for k, v in result.items() if k != "changedPaths"}, ensure_ascii=False))
    finally:
        write(out / "memory.json", guard.finish())


if __name__ == "__main__":
    main()

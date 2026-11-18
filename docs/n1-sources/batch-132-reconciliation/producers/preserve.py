import ctypes
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common_132 import HERE, REPO, git, normalized, sha, start_guard, write

OUTROOT = Path(__file__).resolve().parent
PACKET = REPO / "docs" / "n1-sources" / "batch-132-reconciliation"
PARENT = "2e618b38ae5b420f7a1fe6783268093348367c51"
NOTES = (
    "- [標](標.md), mark or signpost, receives a precaution because a\n"
    "  grave marker is also a mark. Not every mark is a grave, and 標\n"
    "  does not independently mean grave.\n"
    "- [塔](塔.md), tower or pagoda, receives a precaution because some\n"
    "  stone towers serve as graves or grave markers. Not every tower\n"
    "  is a grave; an ordinary 供養塔 memorial tower is not generally\n"
    "  called a grave.\n"
)
CITATIONS = ("Marker and stone-tower senses: [標](https://kotobank.jp/word/標),\n"
             "[墓標](https://kotobank.jp/word/墓標), [石塔](https://kotobank.jp/word/石塔).\n")


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("author", "committed"):
        raise SystemExit("usage: preserve.py author|committed NEW_DIRECTORY")
    mode, out = sys.argv[1], Path(sys.argv[2]).resolve()
    assert out.parent == OUTROOT and not out.exists()
    out.mkdir()
    guard = start_guard()
    result = None
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
            assert fields == ["Roman Konstantinovskiy", "stop-cran@list.ru", "Roman Konstantinovskiy",
                              "stop-cran@list.ru", "D4C9A275A218AF747B787AFA9D94B9D311BD26A7", "G"]
            assert "Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>" in git("show", "-s", "--format=%B", "HEAD").decode()
            signature = fields
        before_raw = git("show", f"{PARENT}:kanji/墓.md")
        before = before_raw.replace(b"\r\n", b"\n").decode()
        after = normalized(REPO / "kanji" / "墓.md")
        assert before.count("quiz_exclusions: [埋, 石]") == 1
        expected = before.replace("quiz_exclusions: [埋, 石]", "quiz_exclusions: [埋, 石, 標, 塔]")
        assert expected.count("- 浅墓 is a spelling") == 1
        expected = expected.replace("- 浅墓 is a spelling", NOTES + "- 浅墓 is a spelling")
        expected = expected.replace("entries 1514840, 1504630, 1584040 and 1609030.",
                                    "entries 1514840, 1504630, 1584040, 1609030, 1168060, 1514900 and 1703230.")
        expected += CITATIONS
        assert after == expected, "Unexpected teaching change"
        assert (PACKET / "before-墓.md").read_bytes() == before_raw
        assert (PACKET / "after-墓.md").read_bytes().replace(b"\r\n", b"\n").decode() == after
        diff = git("-c", "core.quotepath=false", "diff", "--no-ext-diff", PARENT, "--", "kanji/墓.md")
        assert (PACKET / "teaching.diff").read_bytes() == diff
        old_raw = git("show", f"{PARENT}:manifest.json")
        raw_manifest = (REPO / "manifest.json").read_bytes()
        old, new = json.loads(old_raw), json.loads(raw_manifest)
        if mode == "committed":
            assert raw_manifest == git("show", "HEAD:manifest.json")
        before_map = {p: v for group in old.values() if isinstance(group, dict) for p, v in group.items()}
        after_map = {p: v for group in new.values() if isinstance(group, dict) for p, v in group.items()}
        assert set(before_map) == set(after_map)
        changed = {p for p in before_map if before_map[p] != after_map[p]}
        assert changed == {"kanji/墓.md"}, changed
        hashes = {}
        for path, digest in after_map.items():
            guard.check()
            raw = (REPO / path).read_bytes()
            if path.endswith((".md", ".json")):
                raw = raw.replace(b"\r\n", b"\n")
            hashes[path] = sha(raw)
            assert hashes[path] == digest, path
        pairs = json.loads((PACKET / "pair-dispositions.json").read_bytes())
        assert pairs["directExclusionsBefore"] == ["埋", "石"]
        assert pairs["directExclusionsAfter"] == ["埋", "石", "標", "塔"]
        assert [x["pair"] for x in pairs["pairs"]] == [["墓", "標"], ["墓", "塔"]]
        assert all(x["labelDirections"]["標_on_墓" if x["claim"] == "Q1" else "塔_on_墓"] for x in pairs["pairs"])
        assert all(x["labelDirections"]["墓_on_標" if x["claim"] == "Q1" else "墓_on_塔"] for x in pairs["pairs"])
        inventory = json.loads((PACKET / "inventory.json").read_bytes())["files"]
        for path, digest in inventory.items():
            assert sha((PACKET / path).read_bytes()) == digest, path
        assert {str(p.relative_to(PACKET)).replace("\\", "/") for p in PACKET.rglob("*") if p.is_file()} == set(inventory) | {"inventory.json"}
        freeze_path = HERE / "review" / "source-reconciliation-freeze-001.json"
        assert sha(freeze_path.read_bytes()) == "41b27f638aa6e31e54be7c40bba3f2fd215bbc339f78cfd66670e059b3f66a93"
        freeze = json.loads(freeze_path.read_bytes())
        get_attrs = ctypes.windll.kernel32.GetFileAttributesW
        get_attrs.argtypes = [ctypes.c_wchar_p]
        get_attrs.restype = ctypes.c_uint32
        for item in freeze["files"]:
            guard.check()
            p = Path(item["path"])
            assert sha(p.read_bytes()) == item["sha256"]
            attr = get_attrs(str(p))
            assert attr != 0xffffffff and attr & 1, str(p)
        changed_paths = git("diff", "--name-only", "-z", PARENT).decode().strip("\0").split("\0")
        untracked = git("ls-files", "--others", "--exclude-standard", "-z").decode().strip("\0").split("\0")
        for path in changed_paths + untracked:
            if path:
                assert path in ("kanji/墓.md", "manifest.json") or path.startswith("docs/n1-sources/batch-132-reconciliation/"), path
        if mode == "committed":
            actual = set(p for p in changed_paths if p)
            expected_paths = {"kanji/墓.md", "manifest.json"} | {
                "docs/n1-sources/batch-132-reconciliation/" + name for name in inventory} | {
                "docs/n1-sources/batch-132-reconciliation/inventory.json"}
            assert actual == expected_paths
        write(out / "runtime-hashes.json", hashes)
        result = {
            "status": "PASS", "mode": mode, "parent": PARENT, "head": head, "ownerSignature": signature,
            "clean": not bool(git("status", "--porcelain=v1", "--untracked-files=all")),
            "candidateRuntimeCount": len(after_map), "candidateRuntimeHashesChecked": len(hashes),
            "changedRuntime": sorted(changed), "unchangedRuntimeEntries": len(before_map) - len(changed),
            "teachingChange": "Exact two additional exclusions in order, two qualified notes and directly related citations only.",
            "sourceFilesHashAndReadonlyChecked": len(freeze["files"]),
            "initialEvidenceAndAllOtherTrackedPathsUnchanged": True,
            "manifestSha256": sha(raw_manifest), "contentVersion": new["contentVersion"],
            "inventorySha256": sha((PACKET / "inventory.json").read_bytes()),
            "producerSha256": sha(Path(__file__).read_bytes()),
            "limits": "Runtime text hashes normalize CRLF to LF; raw evidence hashes preserve bytes. Host/static checks do not certify independent linguistic, native/device, visual or publication acceptance."}
        print(json.dumps(result, ensure_ascii=False))
    finally:
        memory = guard.finish()
        write(out / "memory.json", memory)
    if result:
        result["memory"] = memory
        write(out / "summary.json", result)


if __name__ == "__main__":
    main()

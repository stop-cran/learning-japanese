import json
import re
import sys
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path

OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT.parent))
from common_133 import REPO, git, sha, start_guard, write

PARENT = "ad047ace020579f81bde250ac948b9a4cb597887"
PACKET = REPO / "docs" / "n1-sources" / "batch-133-reconciliation"
ADDED = {"鉛": ["鉱", "遅", "円"], "滝": ["速", "声", "激", "岩", "険"], "琴": ["具", "糸", "緒"]}


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("author", "committed"):
        raise SystemExit("usage: preserve.py author|committed NEW_DIRECTORY")
    mode, out = sys.argv[1], Path(sys.argv[2]).resolve()
    assert out.parent == OUT and not out.exists()
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
            signature = git("show", "-s", "--format=%an|%ae|%cn|%ce|%G?|%GF", "HEAD").decode().strip()
            assert signature == "Roman Konstantinovskiy|stop-cran@list.ru|Roman Konstantinovskiy|stop-cran@list.ru|G|D4C9A275A218AF747B787AFA9D94B9D311BD26A7"
            assert "Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>" in git("show", "-s", "--format=%B", "HEAD").decode()
        source = OUT.parent / "source-reconciliation-001"
        ids = set()
        for name in ("jmdict-complete-families.xml", "jmdict-supplement-complete-families.xml"):
            ids.update(n.findtext("ent_seq") for n in ET.parse(source / name).getroot())
        successful_urls = set()
        for path in (source / "captures").glob("*.receipt.json"):
            receipt = json.loads(path.read_bytes())
            if receipt["status"] == "complete-capture":
                successful_urls.update(urllib.parse.unquote(receipt[k]) for k in ("requestedUrl", "finalUrl"))
        changes = {}
        for ch, additions in ADDED.items():
            path = REPO / "kanji" / (ch + ".md")
            before_raw = git("show", f"{PARENT}:kanji/{ch}.md")
            assert before_raw == (OUT / ("before-" + ch + ".md")).read_bytes()
            raw = path.read_bytes()
            before, after = before_raw.replace(b"\r\n", b"\n").decode(), raw.replace(b"\r\n", b"\n").decode()
            pattern = r"^quiz_exclusions: \[([^\]]*)\]$"
            old = re.search(pattern, before, re.M).group(1).split(", ")
            actual = re.search(pattern, after, re.M).group(1).split(", ")
            assert actual == old + additions
            expected_prefix = re.sub(pattern, "quiz_exclusions: [" + ", ".join(old + additions) + "]", before, flags=re.M).split("## Notes\n", 1)[0]
            assert after.split("## Notes\n", 1)[0] == expected_prefix, "Changes outside admitted metadata/Notes/citations"
            old_urls, new_urls = [set(re.findall(r"https://[^)\s]+", text)) for text in (before, after)]
            assert {urllib.parse.unquote(url) for url in new_urls - old_urls} <= successful_urls
            new_ids = set(re.findall(r"\b\d{7}\b", after)) - set(re.findall(r"\b\d{7}\b", before))
            assert new_ids <= ids
            assert not set(old) & set(additions)
            changes[ch] = {"beforeRawSha256": sha(before_raw), "afterRawSha256": sha(raw),
                           "afterRuntimeSha256": sha(after.encode()), "exclusionsBefore": old,
                           "exclusionsAfter": actual, "appendedInOrder": additions,
                           "newJMdictIds": sorted(new_ids), "newSuccessfulSourceUrls": sorted(new_urls - old_urls)}
            if (PACKET / "inventory.json").exists():
                assert (PACKET / ("before-" + ch + ".md")).read_bytes() == before_raw
                assert (PACKET / ("after-" + ch + ".md")).read_bytes() == raw
            if mode == "committed":
                assert raw.replace(b"\r\n", b"\n") == git("show", "HEAD:kanji/" + ch + ".md").replace(b"\r\n", b"\n")
        before = json.loads(git("show", f"{PARENT}:manifest.json"))
        manifest_raw = (REPO / "manifest.json").read_bytes()
        after = json.loads(manifest_raw)
        assert before.keys() == after.keys()
        baseline, current, groups = {}, {}, {}
        for key in before:
            if isinstance(before[key], dict):
                groups[key] = {"before": len(before[key]), "after": len(after[key])}
                for dest, group in ((baseline, before[key]), (current, after[key])):
                    for path, digest in group.items():
                        if path in dest:
                            assert dest[path] == digest
                        dest[path] = digest
                if key != "files":
                    assert before[key] == after[key]
            elif key != "contentVersion":
                assert before[key] == after[key]
        assert len(baseline) == len(current) == 8745
        assert set(baseline) == set(current)
        changed = {p for p in baseline if baseline[p] != current[p]}
        assert changed == {"kanji/" + ch + ".md" for ch in ADDED}
        hashes = {}
        for path, expected in current.items():
            guard.check()
            raw = (REPO / path).read_bytes()
            if path.endswith((".md", ".json")):
                raw = raw.replace(b"\r\n", b"\n")
            hashes[path] = sha(raw)
            assert hashes[path] == expected, path
        if mode == "committed":
            assert manifest_raw == git("show", "HEAD:manifest.json")
        changed_paths = set(filter(None, git("diff", "--name-only", "-z", PARENT).decode().split("\0")))
        untracked = set(filter(None, git("ls-files", "--others", "--exclude-standard", "-z").decode().split("\0")))
        for path in changed_paths | untracked:
            assert path in changed | {"manifest.json"} or path.startswith("docs/n1-sources/batch-133-reconciliation/"), path
        inventory_sha = None
        if (PACKET / "inventory.json").exists():
            inventory_raw = (PACKET / "inventory.json").read_bytes()
            inventory_sha = sha(inventory_raw)
            inventory = json.loads(inventory_raw)["files"]
            actual = {str(p.relative_to(PACKET)).replace("\\", "/") for p in PACKET.rglob("*") if p.is_file()}
            assert actual == set(inventory) | {"inventory.json"}
            for path, details in inventory.items():
                raw = (PACKET / path).read_bytes()
                assert sha(raw) == details["sha256"] and len(raw) == details["bytes"]
                if mode == "committed":
                    assert raw == git("show", "HEAD:docs/n1-sources/batch-133-reconciliation/" + path)
            assert (PACKET / "teaching.diff").read_bytes() == git("diff", "--no-ext-diff", PARENT, "--", *("kanji/" + ch + ".md" for ch in ADDED))
            if mode == "committed":
                assert changed_paths == changed | {"manifest.json"} | {
                    "docs/n1-sources/batch-133-reconciliation/" + p for p in actual}
        elif mode == "committed":
            raise AssertionError("Missing reconciliation inventory")
        write(out / "all-runtime-hashes.json", hashes)
        write(out / "article-deltas.json", changes)
        result = {
            "status": "PASS", "mode": mode, "head": head, "parent": PARENT,
            "ownerSignature": signature, "clean": not bool(git("status", "--porcelain=v1", "--untracked-files=all")),
            "runtimeGroups": groups, "runtimeEntries": len(current), "changedRuntime": sorted(changed),
            "unchangedRuntimeEntries": len(baseline) - len(changed),
            "addedExclusions": ADDED, "onlyQuizExclusionsAndNotesCitationsChanged": True,
            "allOtherTrackedPathsAndOriginalAuthorEvidenceUnchanged": True,
            "manifestSha256": sha(manifest_raw), "contentVersion": after["contentVersion"],
            "reconciliationInventorySha256": inventory_sha, "changedTrackedPaths": sorted(changed_paths),
            "runtimeHashesSha256": sha((out / "all-runtime-hashes.json").read_bytes()),
            "producerSha256": sha(Path(__file__).read_bytes()),
            "limits": "Text runtime hashes normalize CRLF to LF; evidence hashes preserve bytes. Host/static provenance and preservation, not review closure, visual/native/device or publication acceptance."
        }
        print(json.dumps({k: result[k] for k in ("status", "mode", "head", "runtimeEntries", "unchangedRuntimeEntries", "changedRuntime", "manifestSha256", "contentVersion", "reconciliationInventorySha256")}))
    finally:
        memory = guard.finish()
        write(out / "memory.json", memory)
    if result is not None:
        result["memory"] = memory
        write(out / "summary.json", result)


if __name__ == "__main__":
    main()

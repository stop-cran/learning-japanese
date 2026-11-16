import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from r131_common import *

sys.path.insert(0, str(ROOT / "lean"))
import n1lib

if len(sys.argv) != 3 or sys.argv[1] not in ("author", "committed"):
    raise SystemExit("usage: r131_preserve.py author|committed NEW_DIRECTORY")
mode, out = sys.argv[1], Path(sys.argv[2]).resolve()
assert out.parent == HERE and not out.exists()
out.mkdir()
guard = start_guard()
try:
    head = git("rev-parse", "HEAD").decode().strip()
    assert git("rev-parse", f"{PARENT}^@").decode().split() == [BASE]
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
                          "D4C9A275A218AF747B787AFA9D94B9D311BD26A7", "G"], fields
        assert "Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>" in git("show", "-s", "--format=%B", "HEAD").decode()
        signature = {"author": fields[:2], "committer": fields[2:4], "fingerprint": fields[4], "status": fields[5]}
    flatten = lambda doc: {p: v for group in doc.values() if isinstance(group, dict) for p, v in group.items()}
    parent_raw = git("show", f"{PARENT}:manifest.json")
    assert sha(parent_raw) == "166f7001e28c6107da0ffe0d2887ef8fea40e843c76d4c7a49fc7af755a1d6ca"
    before = flatten(json.loads(parent_raw))
    manifest_raw = (REPO / "manifest.json").read_bytes()
    manifest = json.loads(manifest_raw)
    after = flatten(manifest)
    assert len(before) == len(after) == 8737 and set(before) == set(after)
    assert {p for p in before if before[p] != after[p]} == {"kanji/衛.md", "kanji/霜.md"}
    runtime = {}
    for path, digest in after.items():
        guard.check()
        raw = (REPO / path).read_bytes()
        if path.endswith((".md", ".json")):
            raw = raw.replace(b"\r\n", b"\n")
        runtime[path] = sha(raw)
        assert runtime[path] == digest, path
    if mode == "committed":
        assert manifest_raw == git("show", "HEAD:manifest.json")
    published = flatten(json.loads(git("show", f"{BASE}:manifest.json")))
    assert len(published) == 8731
    assert set(after) - set(published) == {f"{folder}/{ch}.{suffix}" for ch in CHARS
                                         for folder, suffix in (("kanji", "md"), ("strokes", "json"))}
    supports = {"words/自衛.md", "words/衛星.md", "words/羊毛.md", "words/霜.md"}
    assert {p for p in published if published[p] != after[p]} == supports
    additions = {"霜": list("氷凍酒涼久害枯殺卒"), "衛": list("援循番士軍送抵")}
    notes_additions = {}
    for ch in CHARS:
        rel = f"kanji/{ch}.md"
        baseline = git("show", f"{PARENT}:{rel}").replace(b"\r\n", b"\n").decode()
        current = normalized(REPO / rel)
        old, _ = n1lib.parse(baseline)
        new, _ = n1lib.parse(current)
        if ch == "羊":
            assert current == baseline
            continue
        old_guards, new_guards = old.pop("quiz_exclusions"), new.pop("quiz_exclusions")
        assert new == old
        assert new_guards == old_guards + additions[ch]
        assert len(new_guards) == len(set(new_guards))
        assert not set(new_guards) & ({ch} | set(new["distractors"]))
        restored = re.sub(r"^quiz_exclusions:.*$", re.search(r"^quiz_exclusions:.*$", baseline, re.M).group(), current, count=1, flags=re.M)
        old_body, old_tail = baseline.split("\nMetadata:", 1)
        new_body, new_tail = restored.split("\nMetadata:", 1)
        assert new_tail == old_tail and new_body.startswith(old_body)
        notes_additions[ch] = new_body[len(old_body):]
        assert notes_additions[ch].startswith("- ") and "## " not in notes_additions[ch]
    inventory = json.loads((ORIGINAL / "evidence-inventory-002.json").read_text(encoding="utf8"))
    assert sha((ORIGINAL / "evidence-inventory-002.json").read_bytes()) == "bd5653bca6b0b35f21a602e9c53541a19c07cd9ee5c5fefbdd817746a0a397d6"
    for path, digest in inventory["files"].items():
        guard.check()
        assert sha((ORIGINAL / path).read_bytes()) == digest, path
    receipt = json.loads((PACKET / "source-receipt.json").read_text(encoding="utf8"))
    for name, info in receipt["outputs"].items():
        path = PACKET / name
        assert sha(path.read_bytes()) == info["sha256"]
        actual = {n.findtext("ent_seq") or n.findtext("literal"):
                  sha(ET.canonicalize(ET.tostring(n, encoding="unicode"), strip_text=True).encode())
                  for n in ET.parse(path).getroot()}
        assert actual == info["canonicalRecordHashes"], name
    comparisons = list((PACKET / "comparison-cards").glob("*.md"))
    assert len(comparisons) == 17
    for path in comparisons:
        assert path.read_bytes() == git("show", f"{PARENT}:kanji/{path.name}")
    table_path = PACKET / "pair-dispositions-001.json"
    table = json.loads(table_path.read_text(encoding="utf8"))
    assert [r["id"] for r in table["rows"][4:]] == [f"Q{i}" for i in range(1, 14)]
    assert len(table["rows"]) == 17
    for row in table["rows"]:
        ch, comp = row["pair"]
        assert row["comparisonLabelOnTarget"] and row["targetLabelOnComparison"] and not row["openQuizHold"]
        fm, _ = n1lib.parse(normalized(REPO / "kanji" / (ch + ".md")))
        assert (comp in fm["quiz_exclusions"]) == row["directExclusionOnNewEndpoint"]
        assert row["sources"]["comparisonCardSha256"] == sha((PACKET / "comparison-cards" / (comp + ".md")).read_bytes())
    for source in json.loads((PACKET / "external-source-bindings.json").read_text(encoding="utf8"))["snapshots"]:
        for field in ("response", "extract"):
            assert sha((FROZEN / source[field]["path"]).read_bytes()) == source[field]["sha256"]
    for family, other in (("claude", "gpt"), ("gpt", "claude")):
        mapping = json.loads((PACKET / "responses" / (family + "-mapping-001.json")).read_text(encoding="utf8"))
        assert mapping["neutralTableSha256"] == sha(table_path.read_bytes())
        assert not mapping["independentConfirmation"] and not mapping["publicationAccepted"]
        for binding in mapping["originalBindings"]:
            assert sha(Path(binding["path"]).read_bytes()) == binding["sha256"]
        for suffix in ("mapping-001.json", "response-001.md"):
            assert other not in (PACKET / "responses" / (family + "-" + suffix)).read_text(encoding="utf8").lower()
    note_rel = "docs/n1-authoring-notes.md"
    notes = normalized(REPO / note_rel)
    start = notes.index("## Batch 131 reconciliation 001:")
    end = notes.index("## Batch 131: local unreviewed authoring candidate", start)
    assert notes[:start] + notes[end:] == git("show", f"{PARENT}:{note_rel}").replace(b"\r\n", b"\n").decode()
    paths = [p for p in git("diff", "--name-only", "-z", PARENT).decode().split("\0") if p]
    untracked = [p for p in git("ls-files", "--others", "--exclude-standard", "-z").decode().split("\0") if p]
    allowed = {"kanji/衛.md", "kanji/霜.md", "manifest.json", note_rel,
               "docs/n1-sources/batch-131-progress-reconciliation-001.json"}
    assert set(paths) | set(untracked) >= allowed
    for path in paths + untracked:
        assert path in allowed or path.startswith("docs/n1-sources/batch-131-reconciliation/"), path
    new_inventory = json.loads((PACKET / "evidence-inventory-001.json").read_text(encoding="utf8"))
    actual_paths = {str(p.relative_to(PACKET)).replace("\\", "/") for p in PACKET.rglob("*") if p.is_file()}
    assert actual_paths == set(new_inventory["files"]) | {"evidence-inventory-001.json"}
    for path, digest in new_inventory["files"].items():
        assert sha((PACKET / path).read_bytes()) == digest, path
    result = {"status": "PASS", "mode": mode, "head": head, "parent": PARENT, "publishedBase": BASE,
              "ownerSignature": signature, "clean": not bool(git("status", "--porcelain=v1", "--untracked-files=all")),
              "runtimeEntries": 8737, "unchangedParentRuntimeEntries": 8735,
              "changedRuntime": ["kanji/衛.md", "kanji/霜.md", "manifest.json"],
              "metadata": "Only quiz_exclusions appended in exact order. All other metadata semantically identical; 羊 unchanged.",
              "appendedGuards": additions, "notesAdditions": notes_additions,
              "oldEvidenceFilesRehashed": len(inventory["files"]) + 1,
              "oldEvidenceInventorySha256": sha((ORIGINAL / "evidence-inventory-002.json").read_bytes()),
              "newEvidenceInventorySha256": sha((PACKET / "evidence-inventory-001.json").read_bytes()),
              "originalProgressAndAllOtherTrackedFilesUnchanged": True,
              "publishedBaseRuntimePreservation": "8731 baseline entries: exactly four prior reciprocal wrappers differ; six original B131 runtime additions. Incoming word-only work unchanged.",
              "fullRuntimeHashes": "runtime-hashes.json", "manifestSha256": sha(manifest_raw),
              "contentVersion": manifest["contentVersion"], "finitePairs": 17,
              "producerSha256": sha(Path(__file__).read_bytes()),
              "scope": "Committed Git blobs and complete normalized working runtime hashes; evidence raw bytes. Bounded source/host checks, not independent linguistic/native/device/visual/publication acceptance."}
    write(out / "runtime-hashes.json", runtime)
    print(json.dumps({k: v for k, v in result.items() if k != "notesAdditions"}, ensure_ascii=False))
finally:
    memory = guard.finish()
    write(out / "memory.json", memory)
    if "result" in locals():
        result["memory"] = memory
        write(out / "summary.json", result)

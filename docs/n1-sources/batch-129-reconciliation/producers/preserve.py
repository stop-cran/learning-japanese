import difflib
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from recon_common import *

sys.path.insert(0, str(ROOT / "lean"))
import n1lib


def tree(ref):
    result = {}
    for row in git("ls-tree", "-rz", ref).split(b"\0"):
        if not row:
            continue
        meta, name = row.split(b"\t", 1)
        _, kind, oid = meta.split()
        if kind == b"blob":
            result[name.decode()] = oid.decode()
    return result


def blob_oid(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def flat(manifest):
    result = {}
    for group in manifest.values():
        if isinstance(group, dict):
            for path, digest in group.items():
                assert path not in result or result[path] == digest
                result[path] = digest
    return result


if len(sys.argv) != 3 or sys.argv[1] not in ("author", "committed"):
    raise SystemExit("usage: preserve.py author|committed NEW_DIRECTORY")
mode, out = sys.argv[1], Path(sys.argv[2]).resolve()
assert out.parent == HERE and not out.exists()
out.mkdir()
guard, result = start_guard(), None
try:
    head = git("rev-parse", "HEAD").decode().strip()
    assert head == PARENT if mode == "author" else git("rev-parse", "HEAD^@").decode().split() == [PARENT]
    if mode == "committed":
        assert not git("status", "--porcelain=v1", "--untracked-files=all")
    old_tree = tree(PARENT)
    if mode == "committed":
        current_tree = tree("HEAD")
        for path, oid in old_tree.items():
            if path not in {"kanji/絹.md", "kanji/虹.md", "manifest.json"}:
                assert current_tree[path] == oid, path
        assert set(current_tree) - set(old_tree) == {str(p.relative_to(REPO)).replace("\\", "/") for p in PACKET.rglob("*") if p.is_file()}
    old_manifest = json.loads(git("show", f"{PARENT}:manifest.json"))
    raw_manifest = (REPO / "manifest.json").read_bytes()
    new_manifest = json.loads(raw_manifest)
    before, after = flat(old_manifest), flat(new_manifest)
    assert set(before) == set(after)
    changed = {p for p in before if before[p] != after[p]}
    assert changed == {"kanji/絹.md", "kanji/虹.md"}
    runtime = {}
    for path, digest in after.items():
        guard.check()
        raw = (REPO / path).read_bytes()
        text_bytes = raw.replace(b"\r\n", b"\n") if path.endswith((".md", ".json")) else raw
        assert sha(text_bytes) == digest, path
        oid = blob_oid(raw)
        if path not in changed:
            assert oid == old_tree[path], ("Unchanged runtime raw bytes differ", path)
        if mode == "committed":
            assert oid == current_tree[path], ("Worktree differs from committed raw blob", path)
        runtime[path] = {"runtimeSha256": digest, "rawSha256": sha(raw), "gitBlob": oid}
    old_packet_paths = [p for p in old_tree if p.startswith("docs/n1-sources/batch-129/")]
    for path in old_packet_paths:
        guard.check()
        assert blob_oid((REPO / path).read_bytes()) == old_tree[path], path
    old_inventory = json.loads((ORIGINAL_PACKET / "evidence-inventory-003.json").read_text(encoding="utf8"))
    for name, digest in old_inventory["files"].items():
        assert sha((ORIGINAL_PACKET / name).read_bytes()) == digest
    frozen = json.loads((PACKET / "frozen-input-bindings.json").read_text(encoding="utf8"))
    for item in frozen["inputs"]:
        assert sha(Path(item["path"]).read_bytes()) == item["sha256"]
    pairs = json.loads((PACKET / "pair-dispositions.json").read_text(encoding="utf8"))
    assert len(pairs["rows"]) == 28 and sum(r["guard"] for r in pairs["rows"]) == 26
    assert {tuple(r["pair"]) for r in pairs["rows"]} == {(c, o) for c, others in PAIRS.items() for o in others}
    card_proofs = {}
    for ch in CHARS:
        rel = f"kanji/{ch}.md"
        baseline = git("show", f"{PARENT}:{rel}").replace(b"\r\n", b"\n").decode()
        current = normalized(REPO / rel)
        fm_before, _ = n1lib.parse(baseline)
        fm_after, _ = n1lib.parse(current)
        assert set(fm_before) == set(fm_after)
        for key in fm_before:
            if key != "quiz_exclusions":
                assert fm_before[key] == fm_after[key], (ch, key)
        additions = [r["pair"][1] for r in pairs["rows"] if r["pair"][0] == ch and r["guard"]]
        assert fm_after["quiz_exclusions"] == fm_before["quiz_exclusions"] + additions
        modified_line = re.search(r"^quiz_exclusions:.*$", current, re.M).group()
        old_line = re.search(r"^quiz_exclusions:.*$", baseline, re.M).group()
        restored = current.replace(modified_line, old_line, 1)
        a, b = baseline.splitlines(keepends=True), restored.splitlines(keepends=True)
        inserted = []
        for opcode, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
            if opcode != "equal":
                assert opcode == "insert", (ch, opcode)
                assert all(line.startswith("- ") for line in b[j1:j2])
                inserted.extend(b[j1:j2])
        assert len(inserted) == {"茉": 0, "絹": 1, "虹": 3}[ch]
        for other in additions:
            ofm, _ = n1lib.parse(normalized(REPO / "kanji" / f"{other}.md"))
            assert other in fm_after["quiz_exclusions"] or ch in ofm.get("quiz_exclusions", [])
        card_proofs[ch] = {"allOtherOrderedFieldsPreserved": True,
                          "oldExclusionsOrderedPrefix": fm_before["quiz_exclusions"],
                          "newDirectGuards": additions, "addedNoteLines": inserted,
                          "allOriginalBodyTextPreserved": True}
    wrappers = {}
    original_manifest = json.loads(git("show", f"{BASE}:manifest.json"))
    original_runtime = flat(original_manifest)
    assert set(after) - set(original_runtime) == {f"{folder}/{ch}.{suffix}" for ch in CHARS for folder, suffix in [("kanji", "md"), ("strokes", "json")]}
    assert not set(original_runtime) - set(after)
    assert {p for p in original_runtime if original_runtime[p] != after[p]} == {"words/茉莉花.md", "words/絹.md", "words/虹.md"}
    for ch, word in {"茉": "茉莉花", "絹": "絹", "虹": "虹"}.items():
        rel = f"words/{word}.md"
        current = (REPO / rel).read_bytes()
        assert current == git("show", f"{PARENT}:{rel}")
        baseline = git("show", f"{BASE}:{rel}").replace(b"\r\n", b"\n").decode()
        wrapper = f"[{ch}](../kanji/{ch}.md)"
        text = current.replace(b"\r\n", b"\n").decode()
        assert text.count(wrapper) == baseline.count(wrapper) + 1 and text.replace(wrapper, ch) == baseline
        wrappers[rel] = {"rawSha256": sha(current), "parentByteIdentical": True,
                         "originalBaseDelta": "Exactly one reciprocal wrapper, no prose exception."}
    for item in json.loads((PACKET / "comparison-bindings.json").read_text(encoding="utf8")):
        target, ch = item["pair"]
        raw = (PACKET / "comparison-cards" / f"{ch}.md").read_bytes()
        assert raw == git("show", f"{PARENT}:kanji/{ch}.md")
        assert sha(raw) == item["rawSha256"]
    inv_path = PACKET / "evidence-inventory-001.json"
    inventory = json.loads(inv_path.read_text(encoding="utf8"))
    packet_files = {str(p.relative_to(PACKET)).replace("\\", "/"): p for p in PACKET.rglob("*") if p.is_file()}
    assert set(inventory["files"]) == set(packet_files) - {"evidence-inventory-001.json"}
    for name, digest in inventory["files"].items():
        assert sha(packet_files[name].read_bytes()) == digest, name
    src = json.loads((PACKET / "complete-source-receipt.json").read_text(encoding="utf8"))
    receipts = [v["output"] for v in src["sources"].values()]
    for receipt_name in ("supplement-source-receipt.json", "noose-source-receipt.json"):
        receipts.append(json.loads((PACKET / receipt_name).read_text(encoding="utf8"))["output"])
    for receipt in receipts:
        path = PACKET / receipt["path"]
        assert sha(path.read_bytes()) == receipt["sha256"]
        actual = {n.findtext("ent_seq") or n.findtext("literal"):
                  sha(ET.canonicalize(ET.tostring(n, encoding="unicode"), strip_text=True).encode())
                  for n in ET.parse(path).getroot()}
        assert actual == receipt["canonicalRecordHashes"]
    for source in json.loads((PACKET / "external-source-bindings.json").read_text(encoding="utf8"))["comparisonsAndExactFollowupNoun"].values():
        path = Path(source["localRawCapture"])
        assert sha(path.read_bytes()) == source["rawSha256"]
        assert sha(path.with_suffix(".json").read_bytes()) == source["allArticleJsonSha256"]
        assert sha(path.with_suffix(".txt").read_bytes()) == source["selectedCompleteArticleTextSha256"]
    expected_paths = json.loads((PACKET / "changed-file-inventory.json").read_text(encoding="utf8"))["paths"]
    changed_paths = git("diff", "--name-only", PARENT).decode().splitlines()
    untracked = git("ls-files", "--others", "--exclude-standard").decode().splitlines()
    assert set(changed_paths) | set(untracked) == set(expected_paths)
    assert set(expected_paths) == {"kanji/絹.md", "kanji/虹.md", "manifest.json"} | {str(p.relative_to(REPO)).replace("\\", "/") for p in packet_files.values()}
    assert not git("ls-tree", "-r", "--name-only", PARENT, "--", "kanji/網.md")
    if mode == "committed":
        assert raw_manifest == git("show", "HEAD:manifest.json")
    result = {
        "status": "PASS", "mode": mode, "head": head, "requiredParent": PARENT, "originalBatchBase": BASE,
        "allManifestGroupsChecked": [k for k, v in new_manifest.items() if isinstance(v, dict)],
        "parentRuntimeEntries": len(before), "candidateRuntimeEntries": len(after),
        "addedRuntimePaths": [], "removedRuntimePaths": [], "changedRuntimePaths": sorted(changed),
        "allRuntimeHashesChecked": len(runtime), "unchangedRuntimeRawBlobChecks": len(after) - len(changed),
        "originalBaselineRuntimeEntries": len(original_runtime),
        "originalBaselineUnchangedRuntimeEntries": sum(original_runtime[p] == after[p] for p in original_runtime),
        "allOldPacketRawBlobsUnchanged": len(old_packet_paths),
        "frozenInputHashesVerified": len(frozen["inputs"]), "finitePairs": 28, "newDirectGuards": 26,
        "orderedMetadataAndBodyProofs": card_proofs, "supportWordProofs": wrappers,
        "completeSourceOutputCanonicalHashesVerified": True, "localCapturesUnchanged": True,
        "manifestSha256": sha(raw_manifest), "contentVersion": new_manifest["contentVersion"],
        "finalInventorySha256": sha(inv_path.read_bytes()), "finalInventoryOtherFiles": len(inventory["files"]),
        "exactChangedPaths": expected_paths, "producerSha256": sha(Path(__file__).read_bytes()),
        "limits": "Exact byte/hash/order/canonical and structural checks, not linguistic/native/device/publication acceptance. Text runtime SHA256 normalises CRLF to LF; raw captures, evidence and Git blobs do not.",
    }
    write(out / "runtime-hashes.json", runtime)
finally:
    active_error = sys.exc_info()[1]
    memory = guard.finish()
    write(out / "memory.json", memory)
    if active_error is None and result is not None:
        assert not memory["breach"]
        result["memory"] = memory
        result["runtimeHashesSha256"] = sha((out / "runtime-hashes.json").read_bytes())
        write(out / "summary.json", result)
        print(json.dumps({k: v for k, v in result.items() if k not in ("orderedMetadataAndBodyProofs", "exactChangedPaths")}, ensure_ascii=False))
    else:
        write(out / "failure.json", {"error": str(active_error), "memory": memory,
                                    "producerSha256": sha(Path(__file__).read_bytes())})

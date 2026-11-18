import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from b127_common import HERE, PACKET, REPO, ROOT, git, sha, start_guard, write
from reconcile_sources_b127 import CLAIMS, OUT, PARENT, canonical
from reconcile_author_b127 import ORIGINAL, ADDED

mode, out = sys.argv[1], Path(sys.argv[2]).resolve()
assert mode in ("author", "committed") and out.parent == HERE and not out.exists()
out.mkdir()
guard = start_guard()
try:
    head = git("rev-parse", "HEAD").decode().strip()
    if mode == "author":
        assert head == PARENT
    else:
        assert git("rev-parse", "HEAD^@").decode().split() == [PARENT]
        assert not git("status", "--porcelain=v1", "--untracked-files=all")
    old_manifest = json.loads(git("show", f"{PARENT}:manifest.json"))
    manifest_raw = (REPO / "manifest.json").read_bytes()
    manifest = json.loads(manifest_raw)
    if mode == "committed":
        assert manifest_raw == git("show", "HEAD:manifest.json")
    old_paths = {p: v for group in old_manifest.values() if isinstance(group, dict) for p, v in group.items()}
    new_paths = {p: v for group in manifest.values() if isinstance(group, dict) for p, v in group.items()}
    assert set(new_paths) == set(old_paths) and len(new_paths) == 8716
    assert {p for p in old_paths if new_paths[p] != old_paths[p]} == {"kanji/倉.md"}
    for path, digest in new_paths.items():
        guard.check()
        raw = (REPO / path).read_bytes()
        assert sha(raw.replace(b"\r\n", b"\n") if path.endswith((".md", ".json")) else raw) == digest, path
    for path in ["words/倉庫.md", "strokes/倉.json"]:
        assert (REPO / path).read_bytes() == git("show", f"{PARENT}:{path}")
    card = (REPO / "kanji" / "倉.md").read_text(encoding="utf-8")
    prior = git("show", f"{PARENT}:kanji/倉.md").decode("utf-8").replace("\r\n", "\n")
    exclusions = re.search(r"^quiz_exclusions: \[([^\]]*)\]$", card, re.M).group(1).split(", ")
    assert exclusions == ORIGINAL + ADDED and len(set(exclusions)) == 23
    header = lambda text: re.sub(r"^quiz_exclusions:.*\n", "", text.split("---", 2)[1], flags=re.M)
    assert header(card) == header(prior)
    assert all((REPO / "kanji" / (ch + ".md")).is_file() for ch in exclusions)
    assert not set(exclusions) & {"金", "全", "合"}
    history = json.loads((OUT / "preserved-history.json").read_text(encoding="utf-8"))
    for name, info in history["files"].items():
        guard.check()
        assert sha((REPO / name).read_bytes()) == info["sha256"], name
    for info in history["externalPriorAuthorReceipts"].values():
        assert sha(Path(info["path"]).read_bytes()) == info["sha256"]
    inv = json.loads((OUT / "packet-files.json").read_text(encoding="utf-8"))
    assert set(inv["files"]) == {p.relative_to(OUT).as_posix() for p in OUT.rglob("*") if p.is_file()} - {"packet-files.json"}
    for name, info in inv["files"].items():
        guard.check()
        assert sha((OUT / name).read_bytes()) == info["sha256"], name
    source = json.loads((OUT / "source-receipt.json").read_text(encoding="utf-8"))
    for info in source["admissionBindings"].values():
        assert sha(Path(info["path"]).read_bytes()) == info["sha256"]
    for info in source["reusedImmutableEvidence"].values():
        assert sha(Path(info["path"]).read_bytes()) == info["sha256"]
    for name, info in source["outputs"].items():
        raw = (OUT / name).read_bytes()
        assert sha(raw) == info["sha256"]
        nodes = ET.fromstring(raw)
        actual = {(n.findtext("ent_seq") or n.findtext("literal")): sha(canonical(n).encode()) for n in nodes}
        assert actual == info["canonicalCompleteRecordHashes"]
    entries = ET.parse(OUT / "jmdict-comparison-records.xml").findall("entry")
    for term, expected in source["exactQueryMembership"].items():
        actual = [n.findtext("ent_seq") for n in entries if any(k.findtext("keb") == term for k in n.findall("k_ele"))]
        assert actual == expected, term
    for name, info in source["reusedExternalSnapshots"].items():
        assert sha(Path(info["path"]).read_bytes()) == info["sha256"]
    ext = json.loads(Path(source["reusedExternalSnapshots"]["manifest.json"]["path"]).read_text(encoding="utf-8"))
    for snap in ext["snapshots"]:
        for field in ("response", "extract"):
            item = snap[field]
            local = Path(source["reusedExternalSnapshots"][Path(item["path"]).name]["path"])
            assert sha(local.read_bytes()) == item["sha256"] and local.stat().st_size == item["bytes"]
    pairs = json.loads((OUT / "pair-dispositions.json").read_text(encoding="utf-8"))
    assert [r["id"] for r in pairs["claims"]] == list(CLAIMS)
    assert not pairs["unguardedOpenClaimIds"]
    for row in pairs["claims"]:
        qid, ch = row["id"], row["pair"][1]
        assert ch == CLAIMS[qid][0]
        assert row["declaredEndpointStatus"]["revision"]["倉"] == (ch in exclusions)
        assert row["declaredEndpointStatus"]["revision"][ch] is False
        assert row["recordBindings"]["completeWordFamilies"]["entryIds"] == source["selectors"][qid]["entryIds"]
        assert all(row["directions"].values()) and row["strongestPlausibleOverlap"] and row["citations"]
        assert (OUT / "comparison-cards" / (ch + ".md")).read_bytes() == git("show", f"{PARENT}:kanji/{ch}.md")
    claude = (OUT / "claude-author-response.md").read_text(encoding="utf-8")
    gpt = (OUT / "gpt-author-response.md").read_text(encoding="utf-8")
    assert not re.search(r"\bGPT\b|UNVERIFIED|another reviewer|other reviewer|NEEDS FIX", claude, re.I)
    assert not re.search(r"\bClaude\b|other reviewer|another reviewer", gpt, re.I)
    ledger = json.loads((REPO / "docs" / "n1-sources" / "batch-127-progress-002.json").read_text(encoding="utf-8"))
    assert ledger["parentCandidate"] == PARENT and not ledger["published"] and not ledger["reviewClosed"]
    assert ledger["accounting"]["publishedPendingRecordsWithCards"] == 256 and ledger["accounting"]["undelivered"] == 972
    changed = git("-c", "core.quotepath=false", "diff", "--name-only", PARENT).decode("utf-8").splitlines()
    untracked = git("-c", "core.quotepath=false", "ls-files", "--others", "--exclude-standard").decode("utf-8").splitlines()
    allowed = {"kanji/倉.md", "manifest.json", "docs/n1-authoring-notes.md", "docs/n1-sources/batch-127-progress-002.json"}
    assert all(p in allowed or p.startswith("docs/n1-sources/batch-127-reconciliation/") for p in changed + untracked)
    notes_before = git("show", f"{PARENT}:docs/n1-authoring-notes.md").decode("utf-8").replace("\r\n", "\n")
    notes_after = (REPO / "docs" / "n1-authoring-notes.md").read_text(encoding="utf-8")
    insertion = "The [B127 reconciliation packet](n1-sources/batch-127-reconciliation/) adds\ncomplete finite comparison families, Q1-Q13 dispositions and qualified\ncancellation guards. Its [new ledger revision](n1-sources/batch-127-progress-002.json)\nkeeps the original ledger historical and the revised candidate unconfirmed\nand unpublished; delivered accounting remains unchanged.\n\n"
    assert notes_after.count(insertion) == 1 and notes_after.replace(insertion, "", 1) == notes_before
    write(out / "diff-check.log", git("-c", "core.whitespace=cr-at-eol", "diff", "--check", PARENT))
    result = {
        "status": "PASS", "mode": mode, "parent": PARENT, "head": head,
        "runtimeEntries": len(new_paths), "unchangedRuntimeEntries": len(new_paths) - 1,
        "addedRuntime": [], "removedRuntime": [], "changedRuntime": ["kanji/倉.md"],
        "supportWordAndStrokeByteIdentical": True, "allOtherHeaderFieldsExactAndOrdered": True,
        "originalGuardsRetained": ORIGINAL, "addedGuards": ADDED, "totalGuards": 23,
        "completeClaims": 13, "unguardedOpen": [], "conservativeUncertaintyExplicit": True,
        "preservedHistoricalFiles": len(history["files"]), "packetFiles": len(inv["files"]) + 1,
        "completeSourceRecords": {"JMdict": len(entries), "KANJIDIC2": len(ET.parse(OUT / "kanjidic2-comparison-records.xml").getroot())},
        "familyIsolationChecked": True, "externalCapturesMatchManifest": True,
        "changedFiles": sorted(set(changed + untracked)), "manifestSha256": sha(manifest_raw),
        "contentVersion": manifest["contentVersion"], "producerSha256": sha(Path(__file__).read_bytes()),
        "notesChangeIsAdditiveOnly": True, "crlfAwareDiffCheck": "PASS; command-scoped only, no configuration changed",
        "limits": "Byte/structure/source-binding/finite editorial evidence, not independent linguistic/native/device/publication acceptance.",
    }
    print(json.dumps({k: v for k, v in result.items() if k != "changedFiles"}, ensure_ascii=False))
finally:
    memory = guard.finish()
    write(out / "memory.json", memory)
    if "result" in locals():
        result["memory"] = memory
        write(out / "summary.json", result)

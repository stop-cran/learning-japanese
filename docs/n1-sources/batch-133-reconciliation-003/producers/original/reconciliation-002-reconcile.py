import json
import re
import stat
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT.parent))
from common_133 import REPO, git, sha, start_guard, write
from notes import PARENT, REL, expected_after

ROOT = OUT.parent.parent
PACKET = REPO / REL
SOURCE = OUT.parent / "source-reconciliation-001"


def load(path):
    return json.loads(path.read_bytes())


def section(relative, header, filename):
    path = SOURCE / relative
    raw = path.read_bytes()
    lines = raw.decode("utf-8").splitlines()
    first = lines.index(header)
    last = next(i for i in range(first + 1, len(lines)) if lines[i].startswith("出典"))
    selected = ("\n".join(lines[first:last + 1]) + "\n").encode()
    destination = OUT / "source-sections" / filename
    write(destination, selected)
    return {"sourceTextPath": str(path), "sourceTextSha256": sha(raw),
            "completePublisherSection": header, "sourceLines": [first + 1, last + 1],
            "completeLocalSection": str(destination), "completeSectionSha256": sha(selected),
            "completeSectionBytes": len(selected),
            "scope": "Complete named publisher section through attribution, not isolated favorable lines; full external section stays local. Only short attributable excerpts and bindings are committed."}


def admit(guard):
    assert git("rev-parse", "HEAD").decode().strip() == PARENT
    assert not git("status", "--porcelain=v1", "--untracked-files=all")
    assert not PACKET.exists()
    admission_path = OUT.parent / "review" / "teaching-reconciliation-admission-002" / "admission.json"
    admission = load(admission_path)
    bindings = [admission["brief"], admission["decision"], *admission["bindings"].values(),
                {"path": str(admission_path), "sha256": "b3561458f5f6b09f5ed11af8d968ce2e572c3e736b905a93aa96f1a828c7089f"}]
    for binding in bindings:
        guard.check()
        path = Path(binding["path"])
        assert sha(path.read_bytes()) == binding["sha256"]
        assert path.stat().st_file_attributes & stat.FILE_ATTRIBUTE_READONLY
    write(OUT / "authority-bindings.json", bindings)
    raw = git("show", f"{PARENT}:kanji/滝.md")
    assert raw.replace(b"\r\n", b"\n") == (REPO / "kanji" / "滝.md").read_bytes().replace(b"\r\n", b"\n")
    expected_after(raw.replace(b"\r\n", b"\n").decode())
    write(OUT / "before-滝.md", raw)
    write(OUT / "counterpart-液.md", git("show", f"{PARENT}:kanji/液.md"))
    inventory = load(SOURCE / "inventory.json")
    assert sha((SOURCE / "inventory.json").read_bytes()) == "771407a30005890503babae922f454e672f1d92ee504111bd83a7974960d4eb7"
    assert {str(p.relative_to(SOURCE)) for p in SOURCE.rglob("*") if p.is_file()} == {
        row["relativePath"] for row in inventory["files"]} | {"inventory.json"}
    for row in inventory["files"]:
        guard.check()
        p = SOURCE / row["relativePath"]
        assert sha(p.read_bytes()) == row["sha256"] and p.stat().st_file_attributes & stat.FILE_ATTRIBUTE_READONLY
    sections = [
        section("captures/液-kotobank.txt", "デジタル大辞泉", "液-daijisen.txt"),
        section("reused-captures/滝-kotobank.txt", "精選版 日本国語大辞典", "滝-nikkoku.txt"),
        section("reused-captures/滝-kotobank.txt", "普及版 字通", "滝-jitsu.txt"),
    ]
    receipt_path = SOURCE / "captures" / "液-kotobank.receipt.json"
    receipt = load(receipt_path)
    assert receipt["status"] == "complete-capture" and receipt["httpStatus"] == 200
    assert sha((receipt_path.parent / "液-kotobank.html").read_bytes()) == receipt["htmlSha256"]
    assert sha((receipt_path.parent / "液-kotobank.txt").read_bytes()) == receipt["textSha256"]
    target_capture = next(r for r in load(SOURCE / "reused-captures-index.json") if r["character"] == "滝" and r["provider"] == "kotobank")
    write(OUT / "source-bindings.json", {
        "sections": sections,
        "liquidCapture": {k: receipt[k] for k in ("requestedUrl", "finalUrl", "canonicalUrl", "status", "startedAt", "completedAt", "htmlSha256", "htmlBytes", "textSha256")},
        "liquidReceiptSha256": sha(receipt_path.read_bytes()), "waterfallCapture": target_capture,
        "frozenSourceInventorySha256": sha((SOURCE / "inventory.json").read_bytes()),
        "limits": "Existing successful complete captures, no refetch. Complete HTML, full text/sections and image omissions remain local; no glyph reconstruction or historical derivation is taught."
    })
    print(json.dumps({"status": "PASS", "parent": PARENT, "completeLocalPublisherSections": len(sections)}))


def preserve(mode, out, guard):
    assert mode in ("author", "committed") and out.parent == OUT and not out.exists()
    out.mkdir()
    head = git("rev-parse", "HEAD").decode().strip()
    if mode == "author":
        assert head == PARENT
    else:
        assert git("rev-parse", "HEAD^@").decode().split() == [PARENT]
        assert not git("status", "--porcelain=v1", "--untracked-files=all")
        git("verify-commit", "HEAD")
        identity = git("show", "-s", "--format=%an|%ae|%cn|%ce|%G?|%GF", "HEAD").decode().strip()
        assert identity == "Roman Konstantinovskiy|stop-cran@list.ru|Roman Konstantinovskiy|stop-cran@list.ru|G|D4C9A275A218AF747B787AFA9D94B9D311BD26A7"
        assert "Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>" in git("show", "-s", "--format=%B", "HEAD").decode()
    before_raw = git("show", f"{PARENT}:kanji/滝.md")
    raw = (REPO / "kanji" / "滝.md").read_bytes()
    assert before_raw == (OUT / "before-滝.md").read_bytes()
    assert raw.replace(b"\r\n", b"\n").decode() == expected_after(before_raw.replace(b"\r\n", b"\n").decode())
    old = load_json_bytes(git("show", f"{PARENT}:manifest.json"))
    manifest_raw = (REPO / "manifest.json").read_bytes()
    new = load_json_bytes(manifest_raw)
    assert old.keys() == new.keys()
    before, after, groups = {}, {}, {}
    for key in old:
        if isinstance(old[key], dict):
            groups[key] = {"before": len(old[key]), "after": len(new[key])}
            before.update(old[key])
            after.update(new[key])
            if key != "files":
                assert old[key] == new[key]
        elif key != "contentVersion":
            assert old[key] == new[key]
    assert len(groups) == 9 and len(before) == len(after) == 8745
    assert set(before) == set(after)
    assert {p for p in before if before[p] != after[p]} == {"kanji/滝.md"}
    hashes = {}
    for path, digest in after.items():
        guard.check()
        content = (REPO / path).read_bytes()
        if path.endswith((".md", ".json")):
            content = content.replace(b"\r\n", b"\n")
        hashes[path] = sha(content)
        assert hashes[path] == digest, path
    paths = set(filter(None, git("diff", "--name-only", "-z", PARENT).decode().split("\0")))
    untracked = set(filter(None, git("ls-files", "--others", "--exclude-standard", "-z").decode().split("\0")))
    for path in paths | untracked:
        assert path in {"kanji/滝.md", "manifest.json"} or path.startswith(REL + "/"), path
    inventory_sha = None
    if (PACKET / "inventory.json").exists():
        inventory_sha = sha((PACKET / "inventory.json").read_bytes())
        inventory = load(PACKET / "inventory.json")["files"]
        packet_paths = {str(p.relative_to(PACKET)).replace("\\", "/") for p in PACKET.rglob("*") if p.is_file()}
        assert packet_paths == set(inventory) | {"inventory.json"}
        for path, info in inventory.items():
            guard.check()
            contents = (PACKET / path).read_bytes()
            assert sha(contents) == info["sha256"] and len(contents) == info["bytes"]
            if mode == "committed":
                assert contents == git("show", "HEAD:" + REL + "/" + path)
        assert (PACKET / "before-滝.md").read_bytes() == before_raw
        assert (PACKET / "after-滝.md").read_bytes() == raw
        assert (PACKET / "teaching.diff").read_bytes() == git("diff", "--no-ext-diff", PARENT, "--", "kanji/滝.md")
        if mode == "committed":
            assert paths == {"kanji/滝.md", "manifest.json"} | {REL + "/" + p for p in packet_paths}
            assert manifest_raw == git("show", "HEAD:manifest.json")
    elif mode == "committed":
        raise AssertionError("Missing new inventory")
    write(out / "all-runtime-hashes.json", hashes)
    result = {
        "status": "PASS", "mode": mode, "head": head, "parent": PARENT,
        "runtimeGroups": groups, "runtimeEntries": 8745, "unchangedRuntimeEntries": 8744,
        "changedRuntime": ["kanji/滝.md"], "exactAdmittedTextTransform": True,
        "allOtherTrackedPathsAndHistoricalReconciliationsUnchanged": True,
        "changedPaths": sorted(paths), "clean": not bool(git("status", "--porcelain=v1", "--untracked-files=all")),
        "manifestSha256": sha(manifest_raw), "contentVersion": new["contentVersion"],
        "inventorySha256": inventory_sha, "runtimeHashesSha256": sha((out / "all-runtime-hashes.json").read_bytes()),
        "producerSha256": sha(Path(__file__).read_bytes())
    }
    write(out / "summary.json", result)
    print(json.dumps({k: result[k] for k in ("status", "mode", "head", "changedRuntime", "unchangedRuntimeEntries", "manifestSha256", "contentVersion", "inventorySha256")}))


def load_json_bytes(raw):
    return json.loads(raw)


def package():
    assert not PACKET.exists() and git("rev-parse", "HEAD").decode().strip() == PARENT
    gates = load(OUT / "author-gates-001" / "summary.json")
    assert gates["status"] == "PASS"
    assert load(OUT / "author-preservation-001" / "summary.json")["status"] == "PASS"
    write(PACKET / "before-滝.md", (OUT / "before-滝.md").read_bytes())
    write(PACKET / "after-滝.md", (REPO / "kanji" / "滝.md").read_bytes())
    write(PACKET / "teaching.diff", git("diff", "--no-ext-diff", PARENT, "--", "kanji/滝.md"))
    decision = OUT.parent / "review" / "gpt-confirm-001-adjudication-001.json"
    write(PACKET / "source" / decision.name, decision.read_bytes())
    write(PACKET / "source" / "source-bindings.json", (OUT / "source-bindings.json").read_bytes())
    write(PACKET / "source" / "bounded-excerpts.json", {
        "liquid": {"publisher": "小学館 デジタル大辞泉", "url": "https://kotobank.jp/word/液",
                   "quote": "水や油のような、形のない流動する物体。液体。"},
        "waterfallWater": {"publisher": "小学館 精選版 日本国語大辞典", "url": "https://kotobank.jp/word/滝",
                          "quote": "[ 2 ] 「たきすい（滝水）」の略。"},
        "moistening": {"publisher": "平凡社 普及版 字通", "url": "https://kotobank.jp/word/滝",
                      "quote": "3. ひたす、うるおす。"},
        "completeSections": "Complete named publisher sections, including the entire Digital Daijisen 液 section, are retained locally and hash/line-bound in source-bindings.json. Full external captures and sections are not committed."
    })
    write(PACKET / "pair-disposition.json", {
        "pair": ["滝", "液"], "claim": "GPT coordinator C6",
        "previousDecision": "RETAIN_DISTINCTION", "decision": "ADD_QUALIFIED_DIRECT_PRECAUTION",
        "supersedes": "Only the 滝-液 retained decision in coordinator-adjudication-001.json and historical reconciliation-001; original files/verdicts remain unchanged.",
        "reason": "Direct comparison of sourced waterfall-water abbreviation and moistening layer with the actual broad liquid/fluid label; the preexisting 水 guard is not a direct-pair justification.",
        "directions": {
            "liquidTitleForWaterfall": "The water-substance abbreviation can admit the broad liquid/fluid answer; protect that sourced secondary range.",
            "waterfallTitleForLiquid": "Waterfall/rapids are not all liquids; this is a qualified broad-label precaution, not universal synonymy or a generic-liquid sense taught for 滝."
        },
        "declaration": "Append 液 only on 滝. Direct exclusions apply symmetrically; no counterpart edit or transitivity.",
        "reviewStatus": "Earlier Claude confirmation and GPT UNVERIFIED preserved. Both original reviewers must confirm this new delta separately; no closure or publication."
    })
    for directory, target in (("author-gates-001", "author-gates"), ("author-preservation-001", "author-preservation")):
        for path in sorted((OUT / directory).iterdir()):
            if path.is_file():
                write(PACKET / target / path.name, path.read_bytes())
    for name in ("notes.py", "gates.py", "reconcile.py"):
        write(PACKET / "producers" / name, (OUT / name).read_bytes())
    for name in ("common_133.py", "run_133_gates.py", "check_reading_133.py", "bounded_launch_133.py"):
        write(PACKET / "producers" / "original" / name, (OUT.parent / name).read_bytes())
    write(PACKET / "provenance.json", {
        "parent": PARENT, "decisionSha256": sha(decision.read_bytes()),
        "sourceBindingsSha256": sha((OUT / "source-bindings.json").read_bytes()),
        "authorGatesSummarySha256": sha((OUT / "author-gates-001" / "summary.json").read_bytes()),
        "manifestSha256": gates["manifestSha256"],
        "scope": "Exactly one appended exclusion, one qualified Note and one source citation in 滝; all other lines/cards and original/historical evidence preserved.",
        "gatePhase": "Author gates before signing on packaged runtime; same ten gates run again on the committed child with receipts local, avoiding self-referential commit hashes.",
        "earlierEvidence": "Prior source packet and reconciliation-001 remain frozen/unchanged. GPT confirmation is a claim report, not independent linguistic source evidence.",
        "limits": "No reviewer closure, custom/multiple-borrow pool, Kotlin/native/device, rendered, whole-set or publication acceptance.",
        "delivered": 268, "remaining": 960
    })
    inventory = {str(p.relative_to(PACKET)).replace("\\", "/"): {"sha256": sha(p.read_bytes()), "bytes": p.stat().st_size}
                 for p in sorted(PACKET.rglob("*")) if p.is_file()}
    write(PACKET / "inventory.json", {"files": inventory, "selfExcluded": True})
    print(json.dumps({"status": "PASS", "files": len(inventory) + 1, "inventorySha256": sha((PACKET / "inventory.json").read_bytes())}))


def main():
    guard = start_guard()
    try:
        action = sys.argv[1]
        if action == "admit":
            admit(guard)
        elif action == "package":
            package()
        elif action == "preserve":
            preserve(sys.argv[2], Path(sys.argv[3]).resolve(), guard)
        else:
            raise ValueError("Unknown reconciliation action")
    finally:
        memory_path = Path(sys.argv[3]) / "memory.json" if sys.argv[1] == "preserve" else OUT / (sys.argv[1] + "-001-memory.json")
        write(memory_path, guard.finish())


if __name__ == "__main__":
    main()

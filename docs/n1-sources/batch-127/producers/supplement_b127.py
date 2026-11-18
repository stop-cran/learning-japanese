import json
from pathlib import Path
from b127_common import BASE, HERE, PACKET, git, sha, start_guard, write

guard = start_guard()
try:
    coordinator = Path(r"C:\Users\stop-\.copilot\session-state\2451b10d-02a9-46ab-82d5-d90993f0cb8b\files")
    bindings = {}
    for name, expected in (
        ("b127-author-kickoff.txt", "80e8edec4c09882b0ba8a744a4efadc6278f6f919debf3d9477f4a990e5642b0"),
        ("b127-preparation-001/prepared.json", "5262b66816a7f492bd4f41268ed4819a07aa440d46122cb5d632f43284256cce"),
        ("n1-published-membership-dd45f6fb.json", "ded4adf88df1a7305bf323daf5f44a62393ea9373ec06f8d68e17b901d655ebd"),
    ):
        path = coordinator / name
        raw = path.read_bytes()
        assert sha(raw) == expected
        bindings[name] = {"path": str(path), "sha256": expected, "bytes": len(raw)}
    write(PACKET / "admission-bindings.json", {
        "base": BASE, "files": bindings,
        "limits": "Mechanical source/provenance bindings, not linguistic acceptance.",
    })
    for source, target in (
        ("commit_b127.py", "producers/commit_b127_002.py"),
        ("write_handoff_b127.py", "producers/write_handoff_b127_002.py"),
        ("check_diff_b127.py", "producers/check_diff_b127.py"),
        ("supplement_b127.py", "producers/supplement_b127.py"),
        ("finalization-memory-002.json", "execution-evidence/finalization-memory-002.json"),
        ("prestage-inspection-memory-001.json", "execution-evidence/prestage-inspection-memory-001.json"),
    ):
        write(PACKET / target, (HERE / source).read_bytes())
    for path in sorted((HERE / "diff-check-001").iterdir()):
        write(PACKET / "diff-check-001" / path.name, path.read_bytes())
    for path in sorted((HERE / "git-failures").glob("*.json")):
        write(PACKET / "execution-evidence" / "git-failures" / path.name, path.read_bytes())
    assert git("config", "user.email").decode().strip() == "stop-cran@list.ru"
    assert git("config", "user.signingkey").decode().strip() == "D4C9A275A218AF747B787AFA9D94B9D311BD26A7"
    assert git("config", "user.name").decode("utf-8").strip() == git("show", "-s", "--format=%an", BASE).decode("utf-8").strip()
    write(PACKET / "author-supplement-002.json", {
        "scope": "Contributor-only pre-signing supplement; no runtime content changed after final author gates.",
        "packetInventory": "packet-files-002.json",
        "supersededUnexecutedProducerDrafts": {
            "producers/commit_b127.py": "producers/commit_b127_002.py",
            "producers/write_handoff_b127.py": "producers/write_handoff_b127_002.py",
        },
        "identity": "Use the configured owner display name, matching the signed supplied base; GitHub account slug is not a required Git display name. Owner email and fingerprint remain the exact required values. No Git configuration was changed.",
        "ordinaryWhitespaceCheck": "Exit 2: seventeen new CRLF lines in the pre-existing CRLF authoring notes are reported as trailing whitespace by plain git diff --check. Exact output and receipt retained.",
        "crlfAwareWhitespaceCheck": "Exit 0 using command-scoped -c core.whitespace=cr-at-eol; no shared/local Git whitespace configuration or frozen file line endings changed.",
        "preservedFailures": "The original bounded Git helper exception receipt and the later exact diff stdout/stderr are retained.",
        "publication": "Unreviewed local candidate only; delivered accounting stays 256/1228, 972 remain.",
    })
    inventory = {p.relative_to(PACKET).as_posix(): {"bytes": p.stat().st_size, "sha256": sha(p.read_bytes())} for p in sorted(PACKET.rglob("*")) if p.is_file()}
    write(PACKET / "packet-files-002.json", {"hashMode": "raw bytes, no line-ending normalization", "files": inventory, "excludes": ["packet-files-002.json"], "extends": "packet-files.json"})
    print(json.dumps({"files": len(inventory) + 1, "inventorySha256": sha((PACKET / "packet-files-002.json").read_bytes()), "runtimeUnchanged": True}))
finally:
    write(HERE / "supplement-memory-001.json", guard.finish())

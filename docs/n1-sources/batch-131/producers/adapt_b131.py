import json
from pathlib import Path
from b131_common import BASE, HERE, PACKET, REPO, git, sha, start_guard, write

NEW_BASE = "cb0f5581bdda84f7e673225c19126c85e242e57b"
ADDENDUM = Path(r"C:\Users\stop-\.copilot\session-state\2451b10d-02a9-46ab-82d5-d90993f0cb8b\files\b131-base-adaptation-001.txt")
PROOF = HERE / "review" / "incoming-main-verification-001.json"

guard = start_guard()
try:
    assert sha(ADDENDUM.read_bytes()) == "f88e6d83a997a7a608359f84b7e95b20521095173aa8640a1221dc21db0d53a0"
    assert sha(PROOF.read_bytes()) == "0448941d3d420612eb6bc07a1c677a15c06ee72e0786d4d9e3eb1c5dcf578f3e"
    assert git("rev-parse", "HEAD").decode().strip() == BASE
    before_status = git("status", "--porcelain=v1", "--untracked-files=all").decode()
    local = set(git("diff", "--name-only", "-z").decode().strip("\0").split("\0"))
    incoming = set(git("diff", "--name-only", "-z", BASE, NEW_BASE).decode().strip("\0").split("\0"))
    untracked = set(git("ls-files", "--others", "--exclude-standard", "-z").decode().strip("\0").split("\0"))
    assert not incoming & (local | untracked), sorted(incoming & (local | untracked))
    changed = {p: sha((REPO / p).read_bytes()) for p in (local | untracked) if p}
    old_tree = git("ls-tree", "-r", BASE, "--", "kanji").decode()
    assert old_tree == git("ls-tree", "-r", NEW_BASE, "--", "kanji").decode()
    assert sha(git("show", f"{NEW_BASE}:manifest.json")) == "03bcd5554cf90dc03cb31486a51fdeb953227c27f6f0f318fd3956e4ecca4fca"
    result = git("merge", "--ff-only", NEW_BASE).decode()
    assert git("rev-parse", "HEAD").decode().strip() == NEW_BASE
    assert all(sha((REPO / p).read_bytes()) == h for p, h in changed.items())
    assert sha((REPO / "manifest.json").read_bytes()) == "03bcd5554cf90dc03cb31486a51fdeb953227c27f6f0f318fd3956e4ecca4fca"
    receipt = {
        "originalSourceBase": BASE, "candidateBase": NEW_BASE, "method": "ordinary git merge --ff-only",
        "incomingPaths": sorted(incoming), "localTrackedPathsBefore": sorted(local), "localPathHashesPreserved": changed,
        "runtimeEditsTiming": "Four reciprocal wrappers and three new draft cards/strokes were authored before the verified addendum arrived. No incoming/local path overlap; all local raw bytes preserved by fast-forward.",
        "coordinatorAddendumSha256": sha(ADDENDUM.read_bytes()), "coordinatorProofSha256": sha(PROOF.read_bytes()),
        "completeBaselineKanjiTreeEquality": True, "baselineKanjiTreeSha256": sha(old_tree.encode()),
        "baselineKanjiEntries": len(old_tree.splitlines()),
        "originalScans": {str(p.relative_to(PACKET)).replace("\\", "/"): sha(p.read_bytes())
                          for d in ("scans", "scans-002") for p in sorted((PACKET / d).glob("*.json"))},
        "binding": "Every original baseline kanji blob, path and mode is identical at the new base. Therefore every preserved complete-title/meaning scan row and exact comparison copy still applies. Original scan/source BASE fields and failed evidence are not overwritten or relabelled.",
        "baselineManifestSha256": sha((REPO / "manifest.json").read_bytes()),
        "baselineContentVersion": "db3512fb1d86f1fd", "delivered": 264, "remaining": 964,
        "statusBefore": before_status, "fastForwardOutput": result, "producerSha256": sha(Path(__file__).read_bytes())
    }
    write(PACKET / "base-adaptation.json", receipt)
    write(HERE / "adaptation-001.json", receipt)
    print(json.dumps({"candidateBase": NEW_BASE, "incomingPaths": sorted(incoming), "localRawBytesPreserved": len(changed)}, ensure_ascii=False))
finally:
    write(HERE / "adaptation-memory-001.json", guard.finish())

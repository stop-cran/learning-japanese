import json
import stat
import sys
from pathlib import Path

SCRATCH = Path(r"C:\Users\stop-\n1-kanji-workspace\scratch-130")
sys.path.insert(0, str(SCRATCH))
from b130_common import REPO, git, sha, start_guard, write

HERE = Path(__file__).resolve().parent
FIRST = "9151a6f6ad5bdba9b58178167fba4cabab876504"
SECOND = "153c6b833f68d99f59cbbce34b0bdc6d09a59bc7"
BASE = "f237a8d590a4cb91029bc0b8485163933f44b403"
PATHS = ("articles/numbers-and-counters.md", "counters/age.json", "manifest.json")
guard = start_guard()
try:
    brief = Path(r"C:\Users\stop-\.copilot\session-state\2451b10d-02a9-46ab-82d5-d90993f0cb8b\files\b130-integration-author-brief.txt")
    admission = SCRATCH / "review" / "integration-author-admission-001" / "admission.json"
    assert sha(brief.read_bytes()) == "6093d654febcc61aded4e9fe1060edb3d3ce4511605532461b159c9eca39e0a6"
    assert sha(admission.read_bytes()) == "6d0309c40c7778cbeceb12ff2b2dd70f160108976f15e64532f34312133fbfd3"
    assert git("rev-parse", "HEAD").decode().strip() == FIRST
    assert not git("status", "--porcelain=v1", "--untracked-files=all")
    assert git("rev-parse", "HEAD^{tree}").decode().strip() == "6265c0a9a9aa3a99bcb9ff1443da02c71deaa008"
    assert git("rev-parse", FIRST + "^@").decode().split() == ["1ac4053c5da955c3afaafc1e879e63a98ee42526"]
    assert git("rev-parse", "origin/main").decode().strip() == SECOND
    live = git("ls-remote", "origin", "refs/heads/main").decode().split()
    assert live == [SECOND, "refs/heads/main"], live
    assert git("merge-base", FIRST, SECOND).decode().strip() == BASE
    assert git("rev-parse", SECOND + "^@").decode().split() == [BASE]
    changed = git("diff", "--name-only", BASE, SECOND).decode().splitlines()
    assert sorted(changed) == sorted(PATHS), changed
    signatures = {}
    for label, commit in (("closure", FIRST), ("incoming", SECOND)):
        git("verify-commit", commit)
        fields = git("show", "-s", "--format=%an%n%ae%n%cn%n%ce%n%GF%n%G?", commit).decode().splitlines()
        assert fields == ["Roman Konstantinovskiy", "stop-cran@list.ru",
                          "Roman Konstantinovskiy", "stop-cran@list.ru",
                          "D4C9A275A218AF747B787AFA9D94B9D311BD26A7", "G"], fields
        signature = git("show", "-s", "--show-signature", "--format=fuller", commit)
        write(HERE / "inspection-001" / (label + "-signature.log"), signature)
        signatures[label] = {"commit": commit, "fields": fields, "logSha256": sha(signature)}
    before = {}
    for rel in PATHS:
        committed = git("show", FIRST + ":" + rel)
        incoming = git("show", SECOND + ":" + rel)
        current = (REPO / rel).read_bytes()
        assert current == committed, rel
        write(HERE / "inspection-001" / "parent-content" / rel, committed)
        write(HERE / "inspection-001" / "incoming-content" / rel, incoming)
        before[rel] = {
            "parentSha256": sha(committed), "incomingSha256": sha(incoming),
            "workspaceSha256": sha(current),
            "readOnly": bool((REPO / rel).stat().st_file_attributes & stat.FILE_ATTRIBUTE_READONLY),
        }
    patch = git("diff", BASE, SECOND, "--", *PATHS[:2])
    write(HERE / "inspection-001" / "incoming-content.patch", patch)
    write(HERE / "inspection-001" / "summary.json", {
        "status": "ADMITTED", "firstParent": FIRST, "secondParent": SECOND, "mergeBase": BASE,
        "liveRemoteMain": live[0], "incomingPaths": changed, "signatures": signatures,
        "before": before, "incomingContentPatchSha256": sha(patch),
        "briefSha256": sha(brief.read_bytes()), "coordinatorAdmissionSha256": sha(admission.read_bytes()),
        "producerSha256": sha(Path(__file__).read_bytes()),
    })
    print(patch.decode("utf-8"))
    for rel in PATHS[:2]:
        print("COMPLETE INCOMING FILE: " + rel)
        print((HERE / "inspection-001" / "incoming-content" / rel).read_text(encoding="utf-8"))
    print(json.dumps({"status": "ADMITTED", "before": before, "signatures": signatures}, ensure_ascii=False))
finally:
    write(HERE / "inspection-001" / "memory.json", guard.finish())

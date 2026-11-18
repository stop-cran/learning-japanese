import json
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT.parent))
from common_133 import REPO, git, sha, start_guard, write

PARENT = "ad047ace020579f81bde250ac948b9a4cb597887"


def main():
    guard = start_guard()
    try:
        assert git("rev-parse", "HEAD").decode().strip() == PARENT
        assert not git("status", "--porcelain=v1", "--untracked-files=all")
        git("verify-commit", "HEAD")
        assert git("remote", "get-url", "origin").decode().strip() == "https://github.com/stop-cran/learning-japanese.git"
        assert not (REPO / "docs" / "n1-sources" / "batch-133-reconciliation").exists()
        for ch in "鉛滝琴":
            raw = git("show", f"{PARENT}:kanji/{ch}.md")
            assert raw.replace(b"\r\n", b"\n") == (REPO / "kanji" / (ch + ".md")).read_bytes().replace(b"\r\n", b"\n")
            write(OUT / ("before-" + ch + ".md"), raw)
        write(OUT / "manifest-before.json", git("show", f"{PARENT}:manifest.json"))
        write(OUT / "sparse-patterns.txt", git("sparse-checkout", "list"))
        write(OUT / "admission.json", {
            "parent": PARENT, "clean": True, "ownerSignatureVerified": True,
            "origin": "https://github.com/stop-cran/learning-japanese.git",
            "gitAutocrlf": git("config", "--default", "false", "--get", "core.autocrlf").decode().strip(),
            "coordinatorAdmissionSha256": sha((OUT.parent / "review" / "teaching-reconciliation-admission-001" / "admission.json").read_bytes()),
            "adjudicationSha256": sha((OUT.parent / "review" / "coordinator-adjudication-001.json").read_bytes()),
            "sourceVerificationSha256": sha((OUT.parent / "review" / "source-reconciliation-verification-001.json").read_bytes()),
            "sourceInventorySha256": sha((OUT.parent / "source-reconciliation-001" / "inventory.json").read_bytes()),
            "producerSha256": sha(Path(__file__).read_bytes())
        })
        print(json.dumps({"status": "PASS", "parent": PARENT, "beforeCopies": 3}))
    finally:
        write(OUT / "admission-memory.json", guard.finish())


if __name__ == "__main__":
    main()

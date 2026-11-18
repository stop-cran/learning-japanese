"""Recheck B130's published base without modifying the active author checkout."""
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, start_guard
from verify_b129_sources import FINGERPRINT, Git, ORIGIN, OWNER, TRAILER

BASE = "f237a8d590a4cb91029bc0b8485163933f44b403"
PUBLICATION = "d38c262eff1bea07ec74ad34cd095af723056ffc"
HERE = WS / "scratch-130" / "review"
SESSION_FILES = Path(r"C:\Users\stop-\.copilot\session-state\2451b10d-02a9-46ab-82d5-d90993f0cb8b\files")
RUNNER = {"path": str(HERE / "guarded-test-v3.py"),
          "sha256": "f95c7bc6867cf08977e2ada07630564441790ad31a50141126fec8de3a7d8b84"}


def main():
    frozen(Path(__file__).with_name("verify_b129_sources.py"),
           "9fb0aa1b179679638865582eed251f2c4fd4c9a84707f56099383808b18d0b33")
    guard, _ = start_guard("B130 published-base recheck")
    git = Git(WS / "b129-worktree", RUNNER, guard)
    evidence = [
        (WS / "scratch-129" / "issue60-checkpoint-receipt-001.json",
         "96c3f00cab9a26ab6b2e767f95dbecc9b1ab2099e42292d623d29180d1379cc7"),
        (WS / "scratch-129" / "receipt-tree-check-001" / "receipt.json",
         "4b103dbca46a56fb890da30ff6dea107b399723b64c1031d62724caa1b7f1eec"),
        (SESSION_FILES / "n1-published-membership-f237a8d5.json",
         "77774e98bb329d1b68b6615bb04cb289cb85d9c4d8606a6d6d6cdf0ccf1a9848"),
    ]
    records, signatures, runs = [], [], []

    def gh(*args):
        process = subprocess.Popen(["gh", *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = git.wait(process)
        require(process.returncode == 0, f"GitHub read failed: {err.decode('utf-8', 'replace')}")
        return json.loads(out)

    try:
        require(git("remote", "get-url", "origin").decode().strip() == ORIGIN, "Wrong origin")
        git("fetch", "--quiet", "origin", "main")
        require(git("rev-parse", "origin/main").decode().strip() == BASE, "Remote main advanced")
        require(git("rev-parse", BASE + "^").decode().strip() == PUBLICATION, "Receipt parent differs")
        for commit in (PUBLICATION, BASE):
            require(git("show", "-s", "--format=%G?|%GF|%ae|%ce", commit).decode().strip()
                    == f"G|{FINGERPRINT}|{OWNER}|{OWNER}", "Owner signature differs")
            signature = git("verify-commit", commit, include_stderr=True)
            require(TRAILER in git("show", "-s", "--format=%B", commit), "Missing trailer")
            signatures.append({"commit": commit, "verificationOutputSha256": sha(signature)})
        for path, digest in evidence:
            data = frozen(path, digest)
            records.append({"path": str(path), "sha256": digest})
        membership = json.loads(frozen(evidence[-1][0], evidence[-1][1]))
        require(membership["head"] == BASE and not membership["issues"]
                and membership["counts"]["frozenPendingMembersPresent"] == 261
                and membership["counts"]["undelivered"] == 967
                and sha(git("show", BASE + ":manifest.json")) == membership["manifestSha256"],
                "Published membership or manifest differs")
        require(git("show", BASE + ":manifest.json") == git("show", PUBLICATION + ":manifest.json"),
                "Receipt changed the runtime manifest")
        for run, commit in ((43843967590, PUBLICATION), (43844463431, BASE)):
            actual = gh("run", "view", str(run), "--repo", "stop-cran/learning-japanese",
                        "--json", "databaseId,headSha,status,conclusion,url")
            require(actual["databaseId"] == run and actual["headSha"] == commit
                    and actual["status"] == "completed" and actual["conclusion"] == "success",
                    "Publication CI is not successful for the exact commit")
            runs.append(actual)
        comment = gh("api", "repos/stop-cran/learning-japanese/issues/comments/6913257127")
        checkpoint = json.loads(frozen(evidence[0][0], evidence[0][1]))["comment"]
        require(comment["id"] == checkpoint["id"] and comment["user"]["login"] == "stop-cran"
                and comment["body"] == checkpoint["body"], "Published issue checkpoint changed")
        require(git("ls-remote", "origin", "refs/heads/main").decode().split()[0] == BASE,
                "Remote main changed during verification")
    finally:
        memory = guard.finish()
    require(not memory["breach"], "RAM breach")
    print(json.dumps(freeze_json(HERE / "published-base-recheck-001.json", {
        "observedAt": datetime.now(timezone.utc).isoformat(),
        "base": BASE, "publication": PUBLICATION, "signatures": signatures,
        "evidence": records, "ciRuns": runs, "checkpoint": comment["html_url"],
        "delivered": 261, "remaining": 967, "memory": memory,
        "verifierSha256": sha(frozen(Path(__file__))),
        "limits": "Live remote, signatures, CI, checkpoint and prior evidence hashes rechecked. "
                  "Archive equality and membership audit were not re-executed; their original "
                  "receipts remain historical. No B130 author work or review accepted.",
    })))


if __name__ == "__main__":
    main()

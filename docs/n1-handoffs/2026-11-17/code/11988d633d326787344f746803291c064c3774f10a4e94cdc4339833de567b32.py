"""Record B117 delivery only after owner-signed main, CI and exact ZIP verification."""
import json
import subprocess
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, git, json_bytes, load_batch, require, sha, write_frozen
from confirm_v2 import clean


def validate_delivery(commit, manifest_bytes, ci, archive):
    require(ci["status"] == "completed" and ci["conclusion"] == "success"
            and ci["headSha"] == commit, "CI has not succeeded on the published commit")
    require(archive["commit"] == commit and archive["pendingChecks"] == []
            and not archive["memory"]["breach"], "ZIP verification is incomplete or stale")
    for field in ("manifestEqual", "manifestBytesEqualGitBlob", "zipNamesEqualExportedTree",
                  "allPublishingBudgetsPassed", "contributorEvidenceExcluded",
                  "perFileLimitsAndSafePathsPassed"):
        require(archive[field] is True, f"ZIP acceptance failed: {field}")
    manifest = json.loads(manifest_bytes)
    entries = sum(len(value) for value in manifest.values() if isinstance(value, dict))
    require(archive["manifestSha256"] == sha(manifest_bytes)
            and archive["contentVersion"] == manifest["contentVersion"]
            and archive["verifiedRuntimeHashes"] == entries, "ZIP does not bind every runtime entry")


def main(commit, run_id, archive_path):
    config = load_batch(117)
    clean(config, commit)
    repo = Path(config["repo"])
    api = lambda *args: subprocess.check_output(["gh", *args])
    require(json.loads(api("api", "user"))["login"] == "stop-cran", "Wrong publishing account")
    require(git(config, "ls-remote", "origin", "refs/heads/main").decode().split()[0] == commit,
            "Remote main is not the claimed publication")
    remote = json.loads(api("api", f"repos/stop-cran/learning-japanese/commits/{commit}"))
    require(remote["sha"] == commit and remote["commit"]["verification"]["verified"]
            and remote["author"]["login"] == remote["committer"]["login"] == "stop-cran",
            "GitHub did not verify the owner-signed publication")
    ci_bytes = api("run", "view", run_id, "--repo", "stop-cran/learning-japanese", "--json",
                   "databaseId,headSha,status,conclusion,url,workflowName,jobs,createdAt,updatedAt")
    ci = json.loads(ci_bytes)
    archive_bytes = archive_path.read_bytes()
    archive = json.loads(archive_bytes)
    manifest_bytes = git(config, "show", f"{commit}:manifest.json")
    validate_delivery(commit, manifest_bytes, ci, archive)
    ledger_path = repo / "docs" / "n1-sources" / "batch-117-progress.json"
    old_ledger = git(config, "show", f"{commit}:docs/n1-sources/batch-117-progress.json")
    ledger = json.loads(old_ledger)
    require(ledger["status"] == "textual-review-closed-publication-pending"
            and not ledger["published"] and ledger_path.read_bytes() == old_ledger,
            "Unexpected delivery ledger state")
    reviewed = ledger["reviewedSnapshot"]
    require(git(config, "show", f"{reviewed}:manifest.json") == manifest_bytes,
            "Published teaching differs from the confirmed revision")
    require(all(path.startswith("docs/") for path in git(
        config, "diff", "--name-only", reviewed, commit).decode("utf-8").splitlines()),
        "Post-review changes are not contributor-only")
    index = json.loads(git(config, "show", f"{commit}:docs/n1-sources/source-index.json"))
    pending = {row["kanji"] for row in index if row["statusAtFreeze"] == "pending"}
    manifest = json.loads(manifest_bytes)
    present = {Path(path).stem for values in manifest.values() if isinstance(values, dict)
               for path in values if path.startswith("kanji/")}
    require(len(pending) == 1228 and len(pending & present) == 246, "Delivery membership mismatch")
    closure_path = repo / "docs" / "n1-reviews" / "batch-117-closure"
    closure_bytes = frozen(closure_path / "provenance.json")
    require(sha(closure_bytes) == ledger["review"]["closureProvenanceSha256"], "Closure changed")
    closure = json.loads(closure_bytes)
    for path, digest in closure["recordedFileSha256"].items():
        require(sha(frozen(closure_path / path)) == digest, f"Closure artifact changed: {path}")
    validation = json.loads(frozen(closure_path / "validation-provenance.json"))
    require(validation["candidate"] == reviewed and validation["reviewClosureSha256"] == sha(closure_bytes),
            "Closure validation describes another revision")
    for path, digest in validation["recordedFileSha256"].items():
        require(sha(frozen(closure_path / path)) == digest, f"Validation artifact changed: {path}")

    out = repo / "docs" / "n1-reviews" / "batch-117-publication"
    require(not out.exists(), "Preserve the existing publication receipt")
    out.mkdir()
    write_frozen(out / ".gitattributes", b"* -text\n")
    write_frozen(out / "ci-run.json", ci_bytes)
    write_frozen(out / "zip-receipt.json", archive_bytes)
    provenance = {
        "schemaVersion": 1, "batch": 117, "status": "published-verified-with-disclosed-review-limits",
        "publishedCommit": commit, "publishedCommitUrl": remote["html_url"],
        "base": config["base"], "initialSnapshot": config["candidate"], "reviewedSnapshot": reviewed,
        "method": "Normal owner-authenticated fast-forward; signed remote commit, CI and exact ZIP verified.",
        "ci": {"url": ci["url"], "runId": ci["databaseId"], "receiptSha256": sha(ci_bytes)},
        "archive": {"zipSha256": archive["sha256"], "receiptSha256": sha(archive_bytes),
                    "verifiedRuntimeHashes": archive["verifiedRuntimeHashes"],
                    "contentVersion": archive["contentVersion"]},
        "reviewIdentity": "Original GPT and continuing fresh Claude-family replacement; "
                          "original context-compacted Claude confirmation quarantined.",
        "sourceAccounting": {"delivered": 246, "n1Additions": 240, "n2Placements": 6, "remaining": 982,
                             "overallN1TaskComplete": False},
        "limits": ledger["limits"][:2] + [
            "This exact published runtime and ZIP are verified, not the remaining N1 set.",
            "A later contributor-only receipt commit needs its own CI and exported-tree equality check.",
        ],
    }
    freeze_json(out / "provenance.json", provenance)
    ledger.update(status=provenance["status"], published=ledger["membership"], runtimePublished=True)
    ledger["accounting"].update(publishedPendingRecordsWithCards=246, publishedN1Additions=240,
                                undelivered=982)
    ledger["publication"] = {"commit": commit, "url": remote["html_url"],
                             "receipt": "../n1-reviews/batch-117-publication/provenance.json"}
    ledger["limits"] = provenance["limits"]
    ledger_path.chmod(0o644)
    ledger_path.write_bytes(json_bytes(ledger))
    require(ledger_path.read_bytes() == json_bytes(ledger), "Ledger readback failed")
    body = (
        f"B117 **紀・索・維・賃** is published at [{commit[:8]}]({remote['html_url']}). "
        "Both independent initial reviews are preserved. Final confirmation was provided by the "
        "original GPT reviewer and a fresh Claude-family replacement. The context-compacted "
        "original Claude confirmation remains quarantined, not counted as acceptance. "
        "The revision adds source-backed direct meaning guards, replaces 維's deficient reading option, "
        "and corrects its source-specific ユイ/audit explanation without changing source metadata. "
        "Four generated stroke files and four link-only word updates are included.\n\n"
        f"[CI passed]({ci['url']}); the exact served ZIP preserves all "
        f"**{archive['verifiedRuntimeHashes']:,} runtime hashes**, content version "
        f"`{archive['contentVersion']}`, and existing archive limits. "
        f"[Review evidence](https://github.com/stop-cran/learning-japanese/tree/{commit}"
        "/docs/n1-reviews/batch-117-closure).\n\n"
        "**246/1,228 delivered** (240 N1 additions and six earlier N2 placements); **982 remain**. "
        "Native/phone and arbitrary-pool acceptance remain outstanding. Next is the next bounded serial "
        "batch after this delivery checkpoint; this does not close the full N1 task."
    )
    freeze_json(WS / "scratch-117" / "issue60-publication-comment.json", {"body": body})
    print(json.dumps({"published": commit, "delivered": 246, "remaining": 982, "ci": ci["url"]}))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], Path(sys.argv[3]))

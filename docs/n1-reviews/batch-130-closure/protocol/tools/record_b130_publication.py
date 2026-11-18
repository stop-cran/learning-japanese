"""Batch-generic delivery recorder: owner-signed main, CI and exact ZIP verification first.

Derived from record_b117_publication_v3.py; accounting comes from the frozen review ledger
and the batch narrative comes from a ReadOnly scratch-<N>/publication-narrative.json.
"""
import json
import subprocess
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, git, json_bytes, load_batch, require, sha, write_frozen
from confirm_v2 import clean
from record_b117_publication_v3 import validate_delivery

FROZEN_PENDING = 1228
NARRATIVE_KEYS = ("reviewIdentity", "changeSummary")


def delivery_accounting(ledger):
    acc = ledger["accounting"]
    delivered = acc["reviewClosedPendingRecordsWithCards"]
    members = len(ledger["membership"])
    require(acc["frozenPendingRecords"] == FROZEN_PENDING
            and acc["publishedPendingRecordsWithCards"] + members == delivered
            and acc["publishedN1Additions"] + members == delivered - acc["n2Placements"]
            and acc["undelivered"] - members == acc["notStarted"] == FROZEN_PENDING - delivered,
            "Ledger accounting is inconsistent with batch membership")
    return {"delivered": delivered, "n1Additions": delivered - acc["n2Placements"],
            "n2Placements": acc["n2Placements"], "remaining": FROZEN_PENDING - delivered}


def load_narrative(path):
    narrative = json.loads(frozen(path))
    require(set(narrative) == set(NARRATIVE_KEYS)
            and all(isinstance(narrative[k], str) and narrative[k].strip() for k in NARRATIVE_KEYS),
            "Narrative must contain exactly reviewIdentity and changeSummary")
    return narrative


def comment_body(batch, members, commit, url, ci_url, archive, counts, narrative):
    return (
        f"B{batch} **{'・'.join(members)}** is published at [{commit[:8]}]({url}). "
        f"{narrative['reviewIdentity']} {narrative['changeSummary']}\n\n"
        f"[CI passed]({ci_url}); the exact served ZIP preserves all "
        f"**{archive['verifiedRuntimeHashes']:,} runtime hashes**, content version "
        f"`{archive['contentVersion']}`, and existing archive limits. "
        f"[Review evidence](https://github.com/stop-cran/learning-japanese/tree/{commit}"
        f"/docs/n1-reviews/batch-{batch}-closure).\n\n"
        f"**{counts['delivered']:,}/{FROZEN_PENDING:,} delivered** ({counts['n1Additions']} N1 additions "
        f"and {counts['n2Placements']} earlier N2 placements); **{counts['remaining']} remain**. "
        "Native/phone and arbitrary-pool acceptance remain outstanding. Next is the next bounded serial "
        "batch after this delivery checkpoint; this does not close the full N1 task."
    )


def main(batch, commit, run_id, archive_path, narrative_path):
    config = load_batch(batch)
    batch = config["batch"]
    narrative = load_narrative(narrative_path)
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
    ledger_rel = f"docs/n1-sources/batch-{batch}-progress.json"
    ledger_path = repo / ledger_rel
    old_ledger = git(config, "show", f"{commit}:{ledger_rel}")
    ledger = json.loads(old_ledger)
    require(ledger["status"] == "textual-review-closed-publication-pending"
            and not ledger["published"] and ledger_path.read_bytes() == old_ledger
            and str(ledger["batch"]) == str(batch) and ledger["membership"] == config["members"],
            "Unexpected delivery ledger state")
    counts = delivery_accounting(ledger)
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
    require(len(pending) == FROZEN_PENDING and len(pending & present) == counts["delivered"],
            "Delivery membership mismatch")
    closure_path = repo / "docs" / "n1-reviews" / f"batch-{batch}-closure"
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

    out = repo / "docs" / "n1-reviews" / f"batch-{batch}-publication"
    require(not out.exists(), "Preserve the existing publication receipt")
    out.mkdir()
    write_frozen(out / ".gitattributes", b"* -text\n")
    write_frozen(out / "ci-run.json", ci_bytes)
    write_frozen(out / "zip-receipt.json", archive_bytes)
    provenance = {
        "schemaVersion": 1, "batch": batch, "status": "published-verified-with-disclosed-review-limits",
        "publishedCommit": commit, "publishedCommitUrl": remote["html_url"],
        "base": config["base"], "initialSnapshot": config["candidate"], "reviewedSnapshot": reviewed,
        "method": "Normal owner-authenticated fast-forward; signed remote commit, CI and exact ZIP verified.",
        "ci": {"url": ci["url"], "runId": ci["databaseId"], "receiptSha256": sha(ci_bytes)},
        "archive": {"zipSha256": archive["sha256"], "receiptSha256": sha(archive_bytes),
                    "verifiedRuntimeHashes": archive["verifiedRuntimeHashes"],
                    "contentVersion": archive["contentVersion"]},
        "reviewIdentity": narrative["reviewIdentity"],
        "sourceAccounting": {**counts, "overallN1TaskComplete": False},
        "limits": ledger["limits"] + [
            "This exact published runtime and ZIP are verified, not the remaining N1 set.",
            "A later contributor-only receipt commit needs its own CI and exported-tree equality check.",
        ],
    }
    freeze_json(out / "provenance.json", provenance)
    ledger.update(status=provenance["status"], published=ledger["membership"], runtimePublished=True)
    ledger["accounting"].update(publishedPendingRecordsWithCards=counts["delivered"],
                                publishedN1Additions=counts["n1Additions"],
                                undelivered=counts["remaining"])
    ledger["publication"] = {"commit": commit, "url": remote["html_url"],
                             "receipt": f"../n1-reviews/batch-{batch}-publication/provenance.json"}
    ledger["limits"] = provenance["limits"]
    ledger_path.chmod(0o644)
    ledger_path.write_bytes(json_bytes(ledger))
    require(ledger_path.read_bytes() == json_bytes(ledger), "Ledger readback failed")
    body = comment_body(batch, ledger["membership"], commit, remote["html_url"], ci["url"],
                        archive, counts, narrative)
    freeze_json(WS / f"scratch-{batch}" / "issue60-publication-comment.json", {"body": body})
    print(json.dumps({"published": commit, **counts, "ci": ci["url"]}))


if __name__ == "__main__":
    main(int(sys.argv[1]), sys.argv[2], sys.argv[3], Path(sys.argv[4]), Path(sys.argv[5]))

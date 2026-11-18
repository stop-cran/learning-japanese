"""B131 delivery recorder: owner-signed fast-forward main, CI and exact ZIP verification first.

Derived from record_b130_publication.py. B131 has no batch.json or closure validation-provenance.json;
the closure is instead bound to the frozen closure-mode and committed-mode host-gate summaries, which
are copied into the publication receipt.

Usage: record_b131_publication.py COMMIT CI_RUN_ID ZIP_RECEIPT NARRATIVE
"""
import json
import subprocess
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, git, json_bytes, require, sha, write_frozen
from record_b117_publication_v3 import validate_delivery
from record_b130_publication import FROZEN_PENDING, comment_body, delivery_accounting, load_narrative

BATCH = 131
MEMBERS = ["\u885b", "\u7f8a", "\u971c"]
REPO = WS / "b131-worktree"
CONFIG = {"repo": str(REPO)}
HERE = WS / "scratch-131"
BASE = "cb0f5581bdda84f7e673225c19126c85e242e57b"
INITIAL = "1359b467e0edee8822c665614d6ca57e42785c4d"
REVIEWED = "88a9dfab6a783b082659b742a24242342bb2e461"
GATES = {"closure": HERE / "closure-gates-closure-001" / "summary.json",
         "committed": HERE / "closure-gates-committed-001" / "summary.json"}


def main(commit, run_id, archive_path, narrative_path):
    narrative = load_narrative(narrative_path)
    require(git(CONFIG, "rev-parse", "HEAD").decode().strip() == commit
            and not git(CONFIG, "status", "--porcelain").strip(), "Publication is not the clean HEAD")
    require(git(CONFIG, "show", "-s", "--format=%G?|%ae|%ce|%P", commit).decode().strip()
            == f"G|stop-cran@list.ru|stop-cran@list.ru|{REVIEWED}", "Publication identity or parent differs")
    api = lambda *args: subprocess.check_output(["gh", *args])
    require(json.loads(api("api", "user"))["login"] == "stop-cran", "Wrong publishing account")
    require(git(CONFIG, "ls-remote", "origin", "refs/heads/main").decode().split()[0] == commit,
            "Remote main is not the claimed publication")
    remote = json.loads(api("api", f"repos/stop-cran/learning-japanese/commits/{commit}"))
    require(remote["sha"] == commit and remote["commit"]["verification"]["verified"]
            and remote["author"]["login"] == remote["committer"]["login"] == "stop-cran",
            "GitHub did not verify the owner-signed publication")
    ci_bytes = api("run", "view", run_id, "--repo", "stop-cran/learning-japanese", "--json",
                   "databaseId,headSha,status,conclusion,url,workflowName,jobs,createdAt,updatedAt")
    ci = json.loads(ci_bytes)
    archive_bytes = frozen(archive_path)
    archive = json.loads(archive_bytes)
    manifest_bytes = git(CONFIG, "show", f"{commit}:manifest.json")
    validate_delivery(commit, manifest_bytes, ci, archive)
    ledger_rel = f"docs/n1-sources/batch-{BATCH}-progress.json"
    ledger_path = REPO / ledger_rel
    old_ledger = git(CONFIG, "show", f"{commit}:{ledger_rel}")
    ledger = json.loads(old_ledger)
    require(ledger["status"] == "textual-review-closed-publication-pending"
            and not ledger["published"] and not ledger["runtimePublished"]
            and ledger_path.read_bytes() == old_ledger and ledger["batch"] == BATCH
            and ledger["membership"] == MEMBERS and ledger["base"] == BASE
            and ledger["initialSnapshot"] == INITIAL and ledger["reviewedSnapshot"] == REVIEWED,
            "Unexpected delivery ledger state")
    counts = delivery_accounting(ledger)
    require(git(CONFIG, "show", f"{REVIEWED}:manifest.json") == manifest_bytes,
            "Published teaching differs from the confirmed revision")
    require(all(path.startswith("docs/") for path in git(
        CONFIG, "diff", "--name-only", REVIEWED, commit).decode("utf-8").splitlines()),
        "Post-review changes are not contributor-only")
    git(CONFIG, "merge-base", "--is-ancestor", BASE, commit)
    index = json.loads(git(CONFIG, "show", f"{commit}:docs/n1-sources/source-index.json"))
    pending = {row["kanji"] for row in index if row["statusAtFreeze"] == "pending"}
    manifest = json.loads(manifest_bytes)
    present = {Path(path).stem for values in manifest.values() if isinstance(values, dict)
               for path in values if path.startswith("kanji/")}
    require(len(pending) == FROZEN_PENDING and len(pending & present) == counts["delivered"]
            and set(MEMBERS) <= pending & present, "Delivery membership mismatch")
    closure_path = REPO / "docs" / "n1-reviews" / f"batch-{BATCH}-closure"
    closure_bytes = frozen(closure_path / "provenance.json")
    closure_sha = sha(closure_bytes)
    require(closure_sha == ledger["review"]["closureProvenanceSha256"], "Closure changed")
    closure = json.loads(closure_bytes)
    require(closure["reviewedSnapshot"] == REVIEWED and closure["publication"] == "PENDING",
            "Closure describes another revision")
    for path, digest in closure["recordedFileSha256"].items():
        require(sha(frozen(closure_path / path)) == digest, f"Closure artifact changed: {path}")
    gates = {}
    for mode, path in GATES.items():
        raw = frozen(path)
        summary = json.loads(raw)
        require(summary["status"] == "PASS" and summary["mode"] == mode and summary["batch"] == BATCH
                and summary["reviewedSnapshot"] == REVIEWED and summary["manifestReproducible"] is True
                and summary["manifestSha256"] == sha(manifest_bytes)
                and summary["closureProvenanceSha256"] == closure_sha
                and summary["head"] == (REVIEWED if mode == "closure" else commit),
                f"{mode} closure gates do not bind this publication")
        gates[mode] = raw

    out = REPO / "docs" / "n1-reviews" / f"batch-{BATCH}-publication"
    require(not out.exists(), "Preserve the existing publication receipt")
    out.mkdir()
    write_frozen(out / ".gitattributes", b"* -text\n")
    write_frozen(out / "ci-run.json", ci_bytes)
    write_frozen(out / "zip-receipt.json", archive_bytes)
    (out / "gates").mkdir()
    for mode, raw in gates.items():
        write_frozen(out / "gates" / f"{mode}-summary.json", raw)
    provenance = {
        "schemaVersion": 1, "batch": BATCH, "status": "published-verified-with-disclosed-review-limits",
        "publishedCommit": commit, "publishedCommitUrl": remote["html_url"],
        "base": BASE, "initialSnapshot": INITIAL, "reviewedSnapshot": REVIEWED,
        "method": "Normal owner-authenticated fast-forward; signed remote commit, CI and exact ZIP verified.",
        "ci": {"url": ci["url"], "runId": ci["databaseId"], "receiptSha256": sha(ci_bytes)},
        "archive": {"zipSha256": archive["sha256"], "receiptSha256": sha(archive_bytes),
                    "verifiedRuntimeHashes": archive["verifiedRuntimeHashes"],
                    "contentVersion": archive["contentVersion"]},
        "closureGates": {mode: {"path": f"gates/{mode}-summary.json", "sha256": sha(raw)}
                         for mode, raw in gates.items()},
        "closureProvenanceSha256": closure_sha,
        "reviewIdentity": narrative["reviewIdentity"],
        "sourceAccounting": {**counts, "overallN1TaskComplete": False},
        "limits": [item for item in ledger["limits"] if not item.startswith("No delivery or whole-set credit")] + [
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
                             "receipt": f"../n1-reviews/batch-{BATCH}-publication/provenance.json"}
    ledger["limits"] = provenance["limits"]
    ledger_path.chmod(0o644)
    ledger_path.write_bytes(json_bytes(ledger))
    require(ledger_path.read_bytes() == json_bytes(ledger), "Ledger readback failed")
    body = comment_body(BATCH, ledger["membership"], commit, remote["html_url"], ci["url"],
                        archive, counts, narrative)
    freeze_json(HERE / "issue60-publication-comment.json", {"body": body})
    print(json.dumps({"published": commit, **counts, "ci": ci["url"]}, ensure_ascii=False))


if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise SystemExit("usage: record_b131_publication.py COMMIT CI_RUN_ID ZIP_RECEIPT NARRATIVE")
    main(sys.argv[1], sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4]))

"""Record a verified N1 batch publication (issue #60 receipt commit).

python -X utf8 tools/n1_record_publication.py --batch N --commit SHA \
    --run-id ID --zip-receipt PATH [--review-identity TEXT]

Requires GH_TOKEN for `gh run view`. Refuses to record unless the CI run
succeeded on the exact commit and the ZIP receipt verifies that commit.
Writes docs/n1-reviews/batch-N-publication/ and advances
docs/n1-sources/batch-N-progress.json to published.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = "stop-cran/learning-japanese"
VERIFIER = "docs/n1-reviews/batch-112-publication/verify-zip.py"
ZIP_TRUE_KEYS = (
    "manifestEqual", "zipNamesEqualExportedTree", "allPublishingBudgetsPassed",
    "contributorEvidenceExcluded", "perFileLimitsAndSafePathsPassed",
)
STATUS = "published-verified-with-disclosed-review-limits"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def dump(value) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def write(path: Path, text: str) -> bytes:
    data = text.encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return data


def advance_accounting(accounting: dict, published: int) -> dict:
    result = dict(accounting)
    result["publishedPendingRecordsWithCards"] += published
    result["publishedN1Additions"] += published
    result["undelivered"] -= published
    result["overallN1TaskComplete"] = result["undelivered"] == 0
    return result


def check_ci(run: dict, commit: str) -> None:
    if run.get("headSha") != commit or run.get("conclusion") != "success":
        raise SystemExit(f"CI run {run.get('databaseId')} is not a success on {commit}")


def check_zip(receipt: dict, commit: str) -> None:
    if receipt.get("commit") != commit or not all(receipt.get(k) is True for k in ZIP_TRUE_KEYS):
        raise SystemExit("ZIP receipt does not verify the published commit")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", type=int, required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--run-id", type=int, required=True)
    parser.add_argument("--zip-receipt", type=Path, required=True)
    parser.add_argument("--review-identity", default="")
    args = parser.parse_args()

    progress_path = ROOT / f"docs/n1-sources/batch-{args.batch}-progress.json"
    progress = json.loads(progress_path.read_text(encoding="utf-8"))
    if progress.get("runtimePublished"):
        raise SystemExit(f"batch {args.batch} is already recorded as published")
    commit = subprocess.check_output(
        ["git", "rev-parse", args.commit], cwd=ROOT, text=True).strip()

    run = json.loads(subprocess.check_output(
        ["gh", "run", "view", str(args.run_id), "--repo", REPO, "--json",
         "conclusion,createdAt,databaseId,headSha,jobs,status,updatedAt,url,workflowName"],
        cwd=ROOT, text=True, encoding="utf-8"))
    check_ci(run, commit)
    receipt = json.loads(args.zip_receipt.read_text(encoding="utf-8"))
    check_zip(receipt, commit)
    receipt = {
        "baseVerifier": VERIFIER,
        "verifierSha256": sha256((ROOT / VERIFIER).read_bytes()),
        **receipt,
    }

    out = ROOT / f"docs/n1-reviews/batch-{args.batch}-publication"
    write(out / ".gitattributes", "* -text\n")
    ci_bytes = write(out / "ci-run.json", json.dumps(run, ensure_ascii=False, separators=(",", ":")) + "\n")
    zip_bytes = write(out / "zip-receipt.json", dump(receipt))

    members = progress["members"]
    accounting = advance_accounting(progress["accounting"], len(members))
    url = f"https://github.com/{REPO}/commit/{commit}"
    limits = list(progress.get("limits", [])) + [
        "This exact published runtime and ZIP are verified, not the remaining N1 set.",
        "A later contributor-only receipt commit needs its own CI and exported-tree equality check.",
    ]
    provenance = {
        "schemaVersion": 1,
        "batch": args.batch,
        "status": STATUS,
        "publishedCommit": commit,
        "publishedCommitUrl": url,
        "base": progress.get("base"),
        "initialSnapshot": progress.get("initialSnapshot"),
        "reviewedSnapshot": progress.get("reviewedSnapshot"),
        "method": "Owner-signed fast-forward main, matching Validate content CI, exact ZIP/runtime equality.",
        "ci": {"url": run["url"], "runId": run["databaseId"], "receiptSha256": sha256(ci_bytes)},
        "archive": {
            "zipSha256": receipt["sha256"],
            "receiptSha256": sha256(zip_bytes),
            "verifiedRuntimeHashes": receipt["verifiedRuntimeHashes"],
            "contentVersion": receipt["contentVersion"],
            "manifestSha256": receipt["manifestSha256"],
        },
        "reviewIdentity": args.review_identity,
        "sourceAccounting": {
            "delivered": accounting["publishedPendingRecordsWithCards"],
            "n1Additions": accounting["publishedN1Additions"],
            "n2Placements": accounting["n2Placements"],
            "remaining": accounting["undelivered"],
            "overallN1TaskComplete": accounting["overallN1TaskComplete"],
        },
        "limits": limits,
    }
    write(out / "provenance.json", dump(provenance))

    progress.update({
        "status": STATUS,
        "published": members,
        "runtimePublished": True,
        "accounting": accounting,
        "limits": limits,
        "publication": {
            "commit": commit,
            "url": url,
            "receipt": f"../n1-reviews/batch-{args.batch}-publication/provenance.json",
        },
    })
    write(progress_path, dump(progress))
    print(json.dumps(provenance["sourceAccounting"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())

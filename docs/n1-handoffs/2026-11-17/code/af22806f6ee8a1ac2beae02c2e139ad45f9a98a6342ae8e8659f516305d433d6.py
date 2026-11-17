"""Bind actual accepted FRESH003 collections and explicit decisions for closure."""
import json
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, write_frozen

ROOT = WS / "scratch-134" / "review"
EVIDENCE = (
    ("coordinator-runtime-repair-retention-001",
     "ff68d6204a3da6e21cef9371debf8a9bf74f90b5d5a00be144bcaf6356759617"),
    ("coordinator-final-repairs-retention-001",
     "f3455d92e738103afca9efc6251a156f3b4276472f713b0b788b6487533179fd"),
)


def main(output):
    require(output.parent == ROOT and not output.exists(), "Use a new review directory")
    reviews, adjudications, dispositions, evidence = [], {}, [], []
    for family in ("claude", "gpt"):
        path = ROOT / (family + "-fresh003-collector-001") / "review-input.json"
        collection = json.loads(frozen(path))
        require(collection["status"] == "PASS_ACCEPTED_REVIEW_COLLECTION_NOT_CLOSURE",
                "Actual accepted collection is required")
        review = collection["review"]
        run = review["spec"]["run"]
        require(run == "N1-B134-" + family.upper() + "-FRESH-003"
                and review["spec"]["family"] == family, "Unexpected review identity")
        ref = collection["adjudication"]
        adjudication = json.loads(frozen(ref["path"], ref["sha256"]))
        require(adjudication["run"] == run and adjudication["claimsAdjudicated"] is True,
                "Unadjudicated review")
        decisions = adjudication["decisions"]
        require(len(decisions) == len({row["id"] for row in decisions})
                and {row["id"] for row in decisions}
                == set(collection["requiredDispositionIds"]),
                "Every actual report/adjudication claim needs exactly one decision")
        for row in decisions:
            require(row["status"] in ("resolved", "withdrawn", "optional")
                    and row["reason"].strip(), "Unresolved fresh claim")
            dispositions.append({
                "run": run, "id": row["id"], "status": row["status"],
                "reason": row["reason"],
                "evidence": ["reviews/" + run + "/adjudication.json"],
            })
        reviews.append(review)
        adjudications[run] = ref
    require(reviews[0]["spec"]["session"] != reviews[1]["spec"]["session"]
            and reviews[0]["spec"]["snapshot"] == reviews[1]["spec"]["snapshot"]
            == "355cccb840d22e7313e79f234eb93d1367e00352", "Review snapshot differs")
    for directory, digest in EVIDENCE:
        rows = json.loads(frozen(ROOT / directory / "evidence.json", digest))
        for row in rows:
            frozen(row["path"], row["sha256"])
            evidence.append({key: row[key] for key in ("archivePath", "path", "sha256")})
    require(len({row["archivePath"] for row in evidence}) == len(evidence) == 18,
            "Repair evidence inventory differs")
    source = write_frozen(output / "assemble-b134-fresh003.py", Path(__file__).read_bytes())
    evidence.append({"archivePath": "protocol/assemble-b134-fresh003.py",
                     "path": source["path"], "sha256": source["sha256"]})
    request = {
        "reviews": reviews,
        "adjudications": adjudications,
        "evidence": evidence,
        "protectedSources": [],
        "dispositions": dispositions,
        "limits": [
            "The original and fresh reviewer verdicts are preserved verbatim. "
            "Coordinator reconciliation is separate from the reviewers' judgments.",
            "The complete actual fresh core and selected extension reads, runtime "
            "models, zero compaction and report readbacks were audited; that proves "
            "execution coverage, not exhaustive linguistic correctness.",
            "All 51 expected Notes-mention warnings remain disclosed; exhaustive "
            "contributor pair accounting was not duplicated into learner Notes.",
            "Original lifecycle/import/checker/scope failures and exact external "
            "repairs are retained; they are not passing review evidence.",
            "This closure grants no delivery credit. Combined-main integration, "
            "publication checks and the remaining N1 work are still outstanding.",
        ],
    }
    result = freeze_json(output / "fresh-input.json", request)
    print(json.dumps({"input": result, "freshDispositions": len(dispositions)}))


if __name__ == "__main__":
    require(len(sys.argv) == 2, "assemble-b134-fresh003.py NEW_REVIEW_DIRECTORY")
    main(Path(sys.argv[1]).resolve())

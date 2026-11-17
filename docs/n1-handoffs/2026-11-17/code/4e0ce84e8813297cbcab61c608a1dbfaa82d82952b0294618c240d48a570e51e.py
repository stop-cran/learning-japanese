"""Prepare delivery checks for the three-card batch; never publish or generate a receipt."""
import json

from common import freeze_json, frozen, require, sha, start_guard, write_frozen
from prepare_b133_closure_checks import BASE, CANDIDATE, HERE, REPO, TOOLS, derive
from verify_b133_packet import RUNNER
from verify_b133_sources import Git

SOURCES = {
    "record_b132_publication.py": "8eb94fdc0834fd04a2f1f0aed552823b0c931ef93117dd6ac130d68157d5a5ef",
    "test_record_b132_publication.py": "a99c94183e5a5d04b1d50057e387965b05ac45fe90a6fefe602aba4acc2f14d9",
}


def main():
    guard, _ = start_guard("B133 publication-recorder preparation only")
    git = Git(REPO, RUNNER, guard)
    try:
        require(git("rev-parse", "HEAD").decode().strip() == CANDIDATE
                and not git("status", "--porcelain=v1", "--untracked-files=all"),
                "Candidate is no longer clean and unchanged")
        frozen(TOOLS / "run_b133_closure_checks.py",
               "9e3c87bb4e0a899990dde66ea9c1c760bcd1d222977842ed5721b15daa19224f")
        source_changes = [
            ("B132", "B133"), ("b132", "b133"),
            ('acc["publishedPendingRecordsWithCards"] == 267', 'acc["publishedPendingRecordsWithCards"] == 268'),
            ('acc["publishedN1Additions"] == 261', 'acc["publishedN1Additions"] == 262'),
            ('acc["undelivered"] == 961', 'acc["undelivered"] == 960'),
        ]
        test_changes = [
            ("b132", "b133"),
            ('"publishedPendingRecordsWithCards": 267', '"publishedPendingRecordsWithCards": 268'),
            ('"publishedN1Additions": 261', '"publishedN1Additions": 262'),
            ('"undelivered": 961', '"undelivered": 960'),
            ('"reviewClosedPendingRecordsWithCards": 268', '"reviewClosedPendingRecordsWithCards": 271'),
            ('"notStarted": 960', '"notStarted": 957'),
            ('{"delivered": 268, "n1Additions": 262, "n2Placements": 6, "remaining": 960}',
             '{"delivered": 271, "n1Additions": 265, "n2Placements": 6, "remaining": 957}'),
            ("update(publishedPendingRecordsWithCards=268)", "update(publishedPendingRecordsWithCards=269)"),
            ("update(notStarted=959)", "update(notStarted=956)"),
            ("update(reviewClosedPendingRecordsWithCards=269)", "update(reviewClosedPendingRecordsWithCards=272)"),
        ]
        outputs = {}
        for name, changes in (("record_b132_publication.py", source_changes),
                              ("test_record_b132_publication.py", test_changes)):
            raw = frozen(TOOLS / name, SOURCES[name])
            derived, applied = derive(raw, changes)
            path = TOOLS / name.replace("b132", "b133")
            outputs[path.name] = {**write_frozen(path, derived),
                                  "source": name, "sourceSha256": SOURCES[name], "replacements": applied}
        require(not git("status", "--porcelain=v1", "--untracked-files=all"), "Preparation changed candidate")
        print(json.dumps(freeze_json(HERE / "review" / "publication-recorder-preparation-001.json", {
            "status": "PREPARED_NOT_EXECUTED", "candidate": CANDIDATE, "base": BASE, "outputs": outputs,
            "requiredBefore": {"delivered": 268, "n1Additions": 262, "n2Placements": 6, "remaining": 960},
            "conditionalAfter": {"delivered": 271, "n1Additions": 265, "n2Placements": 6, "remaining": 957},
            "limits": "Focused controls still required. Conditional accounting is not delivery credit. "
                      "No actual closure/review/publication accepted; no commit, push or receipt created.",
        })))
    finally:
        require(not guard.finish()["breach"], "Preparation RAM breach")


if __name__ == "__main__":
    main()

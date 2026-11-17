"""Prepare B134 from B133's verified delivery without changing previous worktrees."""
import datetime
import json
import sys
from pathlib import Path

FILES = Path(__file__).resolve().parent
ROOT = Path(r"C:\Users\stop-\n1-kanji-workspace")
sys.path.insert(0, str(ROOT / "review-tools"))
from common import freeze_json, frozen, require, sha, start_guard, write_frozen
from prepare_b126_publication_tools_v2 import replace
from scoped_admission import assess_status
from verify_b133_packet import RUNNER
from verify_b133_sources import FINGERPRINT, OWNER, Git
import audit_n1_membership as membership

BASE = "e17cb97c53ca4e3193dae5e11b52ba517fe86e76"
PUBLICATION = "c12af4c508ba7d2f82d92d86569b83e8ad4204f1"
OLD, NEW = ROOT / "b133-worktree", ROOT / "b134-worktree"
OUTPUT = FILES / "b134-preparation-001"


def main(snapshot):
    require(not OUTPUT.exists() and not NEW.exists() and not (ROOT / "scratch-134").exists(),
            "Preserve existing B134 work")
    require(0 <= datetime.datetime.now().timestamp() - snapshot.stat().st_mtime < 180, "Stale full status")
    guard, resource = start_guard("B134 worktree preparation")
    try:
        status_raw = snapshot.read_bytes()
        assessment = assess_status(json.loads(status_raw), "B134 kanji authoring", resource.available_ram())
        require(assessment["statusAllowsAdmission"], json.dumps(assessment))
        checkpoint_path = ROOT / "scratch-133" / "issue60-checkpoint-receipt-001.json"
        checkpoint_raw = frozen(checkpoint_path)
        checkpoint = json.loads(checkpoint_raw)
        require(checkpoint["receiptCommit"] == BASE and checkpoint["publishedCommit"] == PUBLICATION
                and checkpoint["delivered"] == 271 and checkpoint["remaining"] == 957
                and checkpoint["comment"]["user"]["login"] == "stop-cran", "Previous checkpoint differs")
        git = Git(OLD, RUNNER, guard)
        require(git("rev-parse", "HEAD").decode().strip() == BASE and not git("status", "--porcelain"),
                "Previous worktree changed")
        require(git("remote", "get-url", "origin").decode().strip()
                == "https://github.com/stop-cran/learning-japanese.git", "Origin differs")
        require(git("show", "-s", "--format=%G?|%GF|%ae|%ce", BASE).decode().strip()
                == f"G|{FINGERPRINT}|{OWNER}|{OWNER}", "Previous owner signature differs")
        git("fetch", "--quiet", "origin", "main")
        require(git("rev-parse", "FETCH_HEAD").decode().strip() == BASE
                and git("ls-remote", "origin", "refs/heads/main").decode().split()[0] == BASE,
                "Remote main advanced; inspect before choosing another base")
        source_raw = git("show", BASE + ":docs/n1-sources/community-list-20261102.json")
        require(sha(source_raw) == membership.SOURCE_SHA, "Frozen source changed")
        source = json.loads(source_raw)
        index_raw = git("show", BASE + ":docs/n1-sources/source-index.json")
        rows = json.loads(index_raw)
        require(len(source) == len(set(source)) == len(rows) == 1232
                and set(source) == {row["kanji"] for row in rows}
                and {row["kanji"] for row in rows if row["statusAtFreeze"] != "pending"}
                == membership.ORIGINAL_MEMBERS, "Source membership differs")
        manifest_raw = git("show", BASE + ":manifest.json")
        cards, present, missing, measured, issues = membership.audit_payload(OLD, rows, json.loads(manifest_raw))
        require(not issues and len(present) == 271 and len(missing) == 957
                and membership.ORIGINAL_MEMBERS <= cards.keys()
                and membership.EARLIER_N2 <= {row["kanji"] for row in present}
                and cards[membership.EXCEPTION]["jlpt"] == "1"
                and not any(row["readingMetadataDeltas"] for row in measured), "Membership preflight failed")
        progress_raw = frozen(OLD / "docs/n1-sources/batch-133-progress.json")
        progress = json.loads(progress_raw)
        require(progress["runtimePublished"] and progress["accounting"]["publishedN1Additions"] == 265
                and progress["accounting"]["publishedPendingRecordsWithCards"] == 271
                and progress["accounting"]["undelivered"] == 957, "Published accounting differs")
        membership_path = FILES / "n1-published-membership-e17cb97c.json"
        membership_record = freeze_json(membership_path, {
            "scope": "Mechanical membership on the verified published tree,not linguistic or native acceptance",
            "head": BASE, "sourceSha256": sha(source_raw), "indexSha256": sha(index_raw),
            "manifestSha256": sha(manifest_raw), "progressSha256": sha(progress_raw),
            "counts": {"allKanjiCards": len(cards), "frozenPendingMembersPresent": 271,
                       "publishedN1Additions": 265, "earlierN2Placements": 6,
                       "undelivered": 957, "readingMetadataDeltaCards": 0},
            "present": measured, "undelivered": [{"sourceRow": row["sourceRow"], "kanji": row["kanji"]}
                                               for row in missing],
            "issues": issues, "overallN1TaskComplete": False,
            "payloadHelperSha256": sha((FILES / "audit_n1_membership.py").read_bytes()),
        })
        require(git("config", "--get", "extensions.worktreeConfig").strip() == b"true",
                "Worktree-scoped configuration unavailable")
        sparse = Path(git("rev-parse", "--path-format=absolute", "--git-path",
                          "info/sparse-checkout").decode().strip())
        previous = sparse.read_bytes()
        patterns = previous.decode().splitlines() + [
            "/docs/n1-sources/batch-134-*", "/docs/n1-reviews/batch-134-*", "/docs/n1-sources/batch-134/"]
        OUTPUT.mkdir()
        status_record = write_frozen(OUTPUT / "full-status.json", status_raw)
        write_frozen(OUTPUT / "previous-sparse-checkout.txt", previous)
        git("worktree", "add", "--detach", "--no-checkout", str(NEW), BASE)
        new_git = Git(NEW, RUNNER, guard)
        new_git("config", "--worktree", "core.autocrlf", "false")
        new_git("sparse-checkout", "set", "--no-cone", *patterns)
        new_git("checkout", "--quiet", "--detach", BASE)
        new_git("verify-commit", "HEAD")
        require(new_git("rev-parse", "HEAD").decode().strip() == BASE
                and not new_git("status", "--porcelain")
                and new_git("config", "user.email").decode().strip() == OWNER
                and new_git("config", "user.signingkey").decode().strip().rstrip("!") == FINGERPRINT,
                "New worktree identity or state differs")
        require(sparse.read_bytes() == previous and not git("status", "--porcelain"),
                "Previous tree or sparse settings changed")
        new_sparse = Path(new_git("rev-parse", "--path-format=absolute", "--git-path",
                                  "info/sparse-checkout").decode().strip())
        require(new_sparse.read_text().splitlines() == patterns, "New sparse patterns differ")
        original = frozen(FILES / "b133-author-kickoff.txt").decode("utf-8").replace("\r\n", "\n")
        prior_defer = "B131 left 皇 and 桜 for separate packets because of unresolved native/secondary senses; its notSelected/deferred records apply."
        require(prior_defer in original, "Prior deferred-scope anchor differs")
        original = original.replace(prior_defer, "PRIOR_DEFERRED_SCOPE")
        substitutions = {
            "B132": "B133",
            "B133": "B134",
            "b132": "b133",
            "b133": "b134",
            "scratch-132": "scratch-133",
            "scratch-133": "scratch-134",
            "batch-132": "batch-133",
            "batch-133": "batch-134",
            "6858fcfb069cc56a195c3f6ed938f92f657fe96b": "e17cb97c53ca4e3193dae5e11b52ba517fe86e76",
            "902d6021214aaf28f8bdf41b9920b0d76a79b83c": "c12af4c508ba7d2f82d92d86569b83e8ad4204f1",
            "6932902315": "6937922786",
            "n1-published-membership-6858fcfb.json": "n1-published-membership-e17cb97c.json",
            "268 of 1,228": "271 of 1,228",
            "960 remain": "957 remain",
            "They contain \u5893-specific facts": "They contain \u7434/\u925b/\u6edd-specific facts",
            "including \u5d50 (\u5d50), \u7434 (\u7434), \u7d2b (\u7d2b), \u8a69 (\u8a69/\u8a69\u4eba), \u925b (\u925b\u7b46), \u77e2 (\u77e2\u5370) and \u6edd (\u6edd)": "including \u5d50 (\u5d50), \u7d2b (\u7d2b), \u8a69 (\u8a69/\u8a69\u4eba) and \u77e2 (\u77e2\u5370)",
            "Recent one-card batches leave substantial work outstanding. Evaluate a practical multi-card subset, approximately 5-10 if complete evidence fits one independent review context, rather than defaulting to one.": "B133 delivered three cards; its complete review core measured 1,152,852 UTF-8 bytes before extension and prompt overhead. Select a practical small multi-card subset only if complete source and comparison evidence fits the independent review budget; split on actual complexity, not a row-count target. This byte measurement is not a tokenizer count."
        }
        kickoff_text = replace(original, substitutions).replace("PRIOR_DEFERRED_SCOPE", prior_defer)
        require("B134 AUTHORING ONLY" in kickoff_text and "271 of 1,228" in kickoff_text
                and "墓 (墓)" not in kickoff_text and BASE in kickoff_text, "Kickoff derivation differs")
        kickoff = write_frozen(FILES / "b134-author-kickoff.txt", kickoff_text.encode("utf-8"))
        raw_runner = frozen(ROOT / "scratch-133" / "review" / "guarded-test-v3.py", RUNNER["sha256"])
        runner_text = raw_runner.decode().replace("b133-worktree", "b134-worktree")
        require(runner_text != raw_runner.decode(), "Runner checkout anchor absent")
        new_runner = write_frozen(ROOT / "scratch-134" / "review" / "guarded-test-v3.py", runner_text.encode())
        result = {
            "batch": 134, "base": BASE, "worktree": str(NEW), "clean": True,
            "publishedRecords": 271, "remaining": 957, "overallN1TaskComplete": False,
            "checkpointSha256": sha(checkpoint_raw), "membership": membership_record,
            "kickoff": kickoff, "kickoffDerivation": substitutions, "runner": new_runner,
            "sparsePatternsSha256": sha(new_sparse.read_bytes()), "statusSnapshot": status_record,
            "preparationAssessment": assessment, "toolSha256": sha(frozen(Path(__file__))),
            "note": "Prepared only;fresh launch admission remains required.",
        }
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Preparation RAM breach")
    result["memory"] = memory
    print(json.dumps(freeze_json(OUTPUT / "prepared.json", result)))


if __name__ == "__main__":
    main(Path(sys.argv[1]))

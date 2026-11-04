import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

c = Path(__file__).resolve().parent
r = c.parent / "learning-japanese"
reviews = r / "docs" / "n1-reviews"
acceptance_path = reviews / "batch-055-native-acceptance.json"
execution_path = r / "docs" / "n1-sources" / "execution-314.json"
load = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def save(path, data):
    temporary = path.with_suffix(path.suffix + ".execution314.tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def git(*args):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=r, text=True, encoding="utf-8").strip()


mode = sys.argv[1]
assert mode in ("prepare", "finish")
p = load(c / "progress.json")
assert p["checkpoint"] == 313 and p["batch"] == "055"
acceptance, execution = load(acceptance_path), load(execution_path)
if mode == "prepare":
    result = subprocess.run(["git", "--no-pager", "diff", "--cached", "--check"], cwd=r, text=True, capture_output=True)
    expected = "docs/n1-reviews/batch-055-native/receipts/copilot-config-execution-314.txt:262: new blank line at EOF."
    assert result.returncode == 2 and result.stdout.strip() == expected and not result.stderr
    observation = {
        "exitCode": result.returncode, "stdout": result.stdout, "stderr": result.stderr,
        "disposition": "Retain exact authoritative CLI catalog output bytes/hash. One raw-help EOF blank-line diagnostic; no teaching, manifest or whitespace-guard change. This is NOT a clean whitespace-check claim.",
    }
    source = Path(__file__)
    copy = reviews / "batch-055-native" / "receipts" / source.name
    assert not copy.exists()
    shutil.copyfile(source, copy)
    acceptance["receiptFiles"].append({"path": str(copy.relative_to(r)), "sha256": sha(copy)})
    acceptance["stagedWhitespaceCheck"] = observation
    execution["stagedWhitespaceCheck"] = observation
    save(acceptance_path, acceptance)
    execution["acceptanceRecordSha256"] = sha(acceptance_path)
    save(execution_path, execution)
    p["execution314VisualCheckpoint"]["recordSha256"] = sha(execution_path)
    save(c / "progress.json", p)
    print("Exact raw catalog EOF whitespace diagnostic preserved; no clean-check claim.")
else:
    assert not git("status", "--porcelain")
    head = git("rev-parse", "HEAD")
    assert git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "HEAD^") == "c4fc279c44541b3d99ddaa56ca5d1ce0452e9026"
    assert not git("diff", "HEAD^", "HEAD", "--", "kanji", "words", "articles", "strokes", "manifest.json")
    p["checkpoint"] = 314
    p["status"] = "continue"
    p["stage"] = "batch-055-native-visual-review-closed-pending-combined-main-publication"
    p["nextAction"] = execution["nextAction"]
    p["blocker"] = None
    p["execution314StartingState"]["status"] = "signed-native-visual-evidence-checkpoint-complete"
    p["execution314VisualCheckpoint"].update(
        status="signed-native-visual-evidence-closed",
        recordSha256=sha(execution_path),
        savedCommit=head, signature="G",
        completedAt=datetime.now().astimezone().isoformat(),
        publishedAdditions=81, remainingAdditions=1147, publicationAttempted=False,
    )
    save(c / "progress.json", p)
    issue = (
        f"Batch 055 advanced to a **signed local native/visual evidence checkpoint**, `{head}`; "
        "it is **not published**.\n\n"
        "The original Claude Opus 5.5 and GPT-6.1 Sol sessions completed dependent visual confirmation "
        "serially on the same frozen snapshot: 27 serial view calls each, 20 distinct screenshot payloads each, "
        "zero observed overlaps, failures or truncated reads. Both retained CLEAN correctness, scoped coverage "
        "and bounded comprehensibility verdicts for 丞 and 丞相. No teaching edits were needed. Complete original "
        "reports, actual model/session/process evidence and separately hashed source/resized image payloads "
        "are archived in `docs/n1-reviews/batch-055-*`; reconciliation is in "
        "`docs/n1-reviews/batch-055-native-acceptance.json`.\n\n"
        "The accepted native two-case terminal-status-0 result (85.809 s) and Android 3+1 results were reverified, "
        "not rerun. Reading metadata/order and practice on [ジョウ]/kun [] remain intact. Historical whole-word "
        "しょうじょう constituent allocation remains UNVERIFIED and excluded from positive allocation teaching/practice. "
        "Clipped table labels/long-line viewport limits remain explicit, with no full-article/all-device claim. "
        "Reference-touch drawing with unavailable ML Kit is not successful human recall or recognition evidence. "
        "The original cleanup-verification denial and exact parent shell-status-1 qualification are preserved. "
        "Validator, unchanged regenerated manifest and original archive budgets pass; the exact CLI catalog's "
        "single EOF whitespace diagnostic is retained, not claimed clean.\n\n"
        "**Next bounded checkpoint:** latest-main non-rewriting integration and all combined-tree acceptance, "
        "normal signing, owner fast-forward push, remote/terminal-green-CI and every immutable public ZIP runtime "
        "hash/budget gate before counting batch 055 delivered or starting 056. Published remains **81/1,228**, "
        "**1,147 remaining**. Compatible Android f9b59a2+ required; physical-phone/general-release and whole-set "
        "acceptance remain outstanding. Full control history preserved; no second runner."
    )
    (c / "execution-314-issue-body.txt").write_text(issue + "\n", encoding="utf-8")
    print(f"Checkpoint314 saved; signed G {head}; status continue, SAME055 combined-main publication next.")

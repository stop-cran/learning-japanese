"""Regenerate the confirmation-packet checks and evidence for an N1 batch at the repo's HEAD.

Usage:
  python n1_run_checks.py --repo WT --batch 157 --base e2c25363 --kanji 佐 佳 ... --words 佳作 ... \
      --extra 佐=すけ,... --tools DIR --checks OUT1 --evidence OUT2 [--wq-out FILE] [--only NAME ...]

Each check file starts with "Command (at <short HEAD>): <command>" and ends with "exit N".
The tree must be clean; the manifest check also asserts that a rebuild leaves it clean.
"""
import argparse
import hashlib
import os
import subprocess
import sys
from pathlib import Path

LEAN = Path(__file__).resolve().parent
WORKSPACE = LEAN.parent


def git(repo, *args):
    return subprocess.run(["git", "-c", "core.quotepath=false", *args], cwd=repo, capture_output=True,
                          text=True, encoding="utf-8", check=True).stdout.strip()


def run(cmd, cwd, env):
    p = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    return p.returncode, (p.stdout + (p.stderr if p.stderr else "")).rstrip("\n")


def write(path, header, body, code):
    path.write_text(f"{header}\n{body}\nexit {code}\n", encoding="utf-8")
    print(f"{path.name}: exit {code}")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--batch", required=True)
    ap.add_argument("--base", required=True)
    ap.add_argument("--kanji", nargs="+", required=True)
    ap.add_argument("--words", nargs="+", required=True)
    ap.add_argument("--extra", action="append", default=[])
    ap.add_argument("--tools", required=True, help="dir with meta_scan.py, evidence/, wordquiz/")
    ap.add_argument("--distractor-gen", required=True, help="gen_distractor_use.py")
    ap.add_argument("--checks", required=True)
    ap.add_argument("--evidence", required=True)
    ap.add_argument("--wq-out", required=True)
    ap.add_argument("--seeds", default="200")
    ap.add_argument("--stale-reviewed", action="append", default=[],
                    help="PATH:LINE:KANJI=REASON for a reviewed stale_remarks.py hit")
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args()

    repo = Path(a.repo).resolve()
    if git(repo, "status", "--porcelain"):
        sys.exit("tree not clean")
    head = git(repo, "rev-parse", "HEAD")
    short = head[:8]
    checks, evidence = Path(a.checks).resolve(), Path(a.evidence).resolve()
    checks.mkdir(parents=True, exist_ok=True)
    evidence.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, PYTHONIOENCODING="utf-8", N1_REPO=str(repo), PYTHONPATH=str(LEAN))
    py = sys.executable
    extras = [x for e in a.extra for x in ("--extra", e)]
    extra_disp = " ".join(f"--extra {e}" for e in a.extra)
    kanji_disp = " ".join(a.kanji)

    def want(name):
        return not a.only or name in a.only

    def check(name, display, cmd, cwd):
        if want(name):
            code, out = run(cmd, cwd, env)
            write(checks / f"{name}.txt", f"Command (at {short}): {display}", out, code)

    if want("manifest"):
        m = repo / "manifest.json"
        before = sha(m)
        code, out = run([py, "tools/build_manifest.py"], repo, env)
        after = sha(m)
        dirty = git(repo, "status", "--porcelain")
        out += (f"\nmanifest.json sha256 before {before}, after {after}; "
                f"tracked tree after rebuild: {'clean' if not dirty else 'DIRTY'}")
        write(checks / "manifest.txt", f"Command (at {short}): python tools\\build_manifest.py", out, code)
        if dirty:
            sys.exit("manifest rebuild changed the tree")
    check("validate", "python tools\\validate.py", [py, "tools/validate.py"], repo)
    check("audit", f"python tools\\audit_n1_batch.py --batch {a.batch}",
          [py, "tools/audit_n1_batch.py", "--batch", a.batch], repo)
    check("budget", "python tools\\check_content_budget.py", [py, "tools/check_content_budget.py"], repo)
    check("unittest", 'python -m unittest discover -s tools -p "test_*.py"',
          [py, "-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"], repo)
    check("diffcheck", f"git -c core.whitespace=cr-at-eol diff --check {a.base} {short} "
          "(whole range from the batch base, including any merged-in main commits)",
          ["git", "-c", "core.whitespace=cr-at-eol", "diff", "--check", a.base, head], repo)
    check("lint", f"python lean\\n1_batch_tool.py lint --base {a.base}",
          [py, str(LEAN / "n1_batch_tool.py"), "lint", "--base", a.base], WORKSPACE)
    check("vocabulary", "python tools\\grammar_vocabulary.py check",
          [py, "tools/grammar_vocabulary.py", "check"], repo)
    check("quiz-safety", f"python quiz_safety.py {kanji_disp}",
          [py, "quiz_safety.py", *a.kanji], LEAN)
    check("reading-exposure", f"python reading_exposure.py {extra_disp} --seeds {a.seeds} {kanji_disp}",
          [py, "reading_exposure.py", *extras, "--seeds", a.seeds, *a.kanji], LEAN)
    check("reading-options", f"python reading_options.py {extra_disp} {kanji_disp}",
          [py, "reading_options.py", *extras, *a.kanji], LEAN)
    stale_args = [x for r in a.stale_reviewed for x in ("--reviewed", r)]
    stale_disp = "".join(f' --reviewed "{r}"' for r in a.stale_reviewed)
    check("stale-remarks", f"python lean\\stale_remarks.py <repo>{stale_disp}",
          [py, str(LEAN / "stale_remarks.py"), str(repo), *stale_args], WORKSPACE)

    tools = Path(a.tools).resolve()
    if want("meta-scan"):
        code, out = run([py, "-X", "utf8", str(tools / "meta_scan.py"), str(repo), *a.kanji], tools, env)
        write(evidence / "meta-scan.txt",
              f"command: python -X utf8 meta_scan.py <repo at {short}> {kanji_disp}", out, code)
    if want("corpus-attested"):
        code, out = run([py, str(tools / "evidence" / "gen_corpus_attested.py"), str(repo), short],
                        tools / "wordquiz", env)
        if code:
            sys.exit(out)
        (evidence / "corpus-attested.txt").write_text(out + "\n", encoding="utf-8")
        print("corpus-attested.txt: exit 0")
    if want("distractors"):
        code, out = run([py, str(Path(a.distractor_gen).resolve()), str(repo), str(evidence)], LEAN, env)
        if code:
            sys.exit(out)
        print("distractor-use.tsv, distractor-senses.txt: exit 0")
    if want("word-quiz"):
        code, out = run([py, str(tools / "wordquiz" / "word_quiz_audit.py"), str(repo), *a.words],
                        tools / "wordquiz", env)
        out = out.replace("<repo at the candidate>", f"<repo at {short}>", 1)
        Path(a.wq_out).write_text(f"{out}\nexit {code}\n", encoding="utf-8")
        print(f"word-quiz: exit {code}")
    if git(repo, "status", "--porcelain"):
        sys.exit("tree changed during checks")


if __name__ == "__main__":
    main()

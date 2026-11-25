# -*- coding: utf-8 -*-
"""Build a confirmation packet for the revised snapshot of a reviewed batch.

Run once per reviewer: the packets differ only in RESPONSE.md and the report path.

  python n1_confirm_packet.py --batch 109 --freeze 0a20f4bf --fix a3e0610a --out DIR \
      --response RESPONSE.md --changes CHANGES.md --report REPORT.md \
      --orig-packet DIR --orig-report FILE [--jm-id N]... --joyo-pdf PDF [--joyo PAGE:KANJI]... \
      [--kvg FILE]... [--quizbuilder FILE] [--check NAME=FILE]...

Requires HEAD == fix, a clean tracked tree, fix descended from freeze and a non-existent out dir.
"""
import argparse
import datetime
import json
import posixpath
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import n1cmds  # noqa: E402
from n1lib import JMDICT_GZ, KANJIDIC_GZ, REPO, sha256_file  # noqa: E402

JOYO_URL = "https://www.bunka.go.jp/kokugo_nihongo/sisaku/joho/joho/kijun/naikaku/pdf/joyokanjihyo_20101130.pdf"
KVG_URL = "https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/kanji/%s"
DEFAULT_QUIZBUILDER = Path(r"C:\Users\stop-\n1-kanji-workspace\rollout-recovered\kanji-cards-android"
                           r"\core\src\main\kotlin\io\github\stopcran\kanji\core\quiz\QuizBuilder.kt")

INSTR = """# Confirmation packet: N1 kanji batch {batch}, revised snapshot {fix8}

You are the same reviewer who wrote the initial report on this batch (reviewed snapshot {freeze8}). The author has
since revised the batch. Your job now is to CONFIRM the revision independently: give a disposition for each of your own
earlier points, and check every changed line for new defects. You will not see any other reviewer's report; do not look
for one.

## Mandate

- **Read-only.** Do not edit, stage, commit, push or run any command that changes files, except that you write your
  report to the one path named in your assignment. Do not start other agents, sessions or background jobs.
- **Serial.** Make exactly ONE tool call per response, wait for its result, then decide the next call. Read large files
  in ranges. Never list a directory recursively.
- **Allowed local reads.** (1) this packet; (2) the original packet `{orig_packet}` (read-only);
  (3) your own initial report `{orig_report}`. Open no other local path: no repository checkouts, no `docs\\n1-reviews`,
  no other packets and no other reports. Public web sources are allowed and encouraged.
- **The original packet holds the OLD text of the changed cards.** Its `snapshot\\kanji\\<card>.md` and
  `repo\\kanji\\<card>.md` show the reviewed snapshot. The revised text exists only in `snapshot\\kanji\\` of THIS packet.
  Every other file of the original packet (word articles, titles, other cards, `evidence\\`, `rubric\\`) is unchanged at the
  revised snapshot{word_exception} and remains valid context.
- **Report path.** Write your report to this one path only: `{report}`

## What the batch is

Teaching cards for JLPT N1 kanji (community list): {members}. The revision changes {n_changed} of these cards
({changed}); the unchanged cards are: {unchanged}. {word_note} Audience: an English speaker
at roughly JLPT N5-N4 reading on a phone. The review contract is `rubric\\copilot-instructions.md` of the original packet.

## What to read

1. `CHANGES.md`: a neutral list of every changed line, by card.
2. `RESPONSE.md`: the author's statement on each of YOUR earlier findings, optional points and limits. These are claims
   to verify, **not evidence**: check each one against the revised card text, `diffs\\fix.patch` and independent sources.
3. `diffs\\fix.patch` (exact patch from the reviewed snapshot to the revised snapshot, `manifest.json`{diff_excl} excluded),
   `diffs\\changed-lines.txt` and the revised cards in `snapshot\\kanji\\`.
4. `evidence\\`: new evidence for this round; `evidence\\README.md` describes each file (the complete JMdict entries cited by
   the new text, official Joyo kanji table pages when supplied, the app's `QuizBuilder.kt` and anything else it lists).
5. `checks\\`: automatic checks at the revised snapshot. `checks\\quiz-safety.txt` shows, for each card, the correct
   title in parentheses after the kanji, followed by the three wrong meaning options now offered.
   `checks\\reading-options.txt`, when present, lists for
   every reading prompt the excluded readings, the curated and fallback candidates for the wrong options, and a check that
   no reading attested for the card but not listed in its metadata can be offered as a wrong option.
   `checks\\link-targets.tsv` lists every link on a changed
   line: whether the target exists at the revised snapshot, its real `title:`, the gloss quoted after the link and whether
   the two are equal. These are outputs, not verdicts.

## Tasks

1. **Dispositions.** Give one disposition for every item in `RESPONSE.md`, using its ID, after verifying it yourself:
   - `RESOLVED`: the revised snapshot fixes the point.
   - `PARTIALLY RESOLVED` or `NOT RESOLVED`: say precisely what remains and where.
   - `DECLINE ACCEPTED` or `DECLINE REJECTED`: for a point the author chose not to change; judge the stated reason.
   - `DISPUTE ACCEPTED` or `DISPUTE REJECTED`: for a point the author says was mis-stated or mis-attributed.
2. **Regression check.** Read every changed card in full (a correct hunk can still contradict untouched text), and check
   every changed hunk against all four facets: correctness (every claim true, readings, glosses and component
   statements), scoped coverage, consistency and quiz safety (links and quoted titles resolve, exclusions are real direct
   pairs and never also listed as distractors, distractors cannot also be correct) and comprehensibility for a beginner
   on a phone.
3. **Quiz options.** Check the post-fix options in `checks\\quiz-safety.txt` and the mechanics in
   `evidence\\QuizBuilder.kt` for every card of the batch, not only the changed ones. Where `checks\\reading-options.txt`
   and the app's reading-quiz sources are supplied, check the reading prompts the same way and say what the audit cannot show.
4. **New findings.** Report only what is new and established. Do not re-raise a point you have dispositioned unless the
   revision itself is wrong. No finding quota.

Verify consequential claims yourself against reputable sources. A search snippet is not verification. Say what you could
not verify.

## Report contract (use exactly this shape)

```text
Snapshot: <commit {fix8}; reviewer model as you identify it>
Scope: <files opened and how deeply>
Dispositions: <one line per ID in RESPONSE.md: ID - DISPOSITION - short reason and evidence>
Verdicts: <for each facet - correctness, scoped coverage, consistency and quiz safety, comprehensibility: CLEAN | NEEDS FIX | UNVERIFIED, one line each, listing cards that differ>
Confirmation: <CONFIRMED | NEEDS FIX | UNVERIFIED - CONFIRMED only if every item is RESOLVED, DECLINE ACCEPTED or DISPUTE ACCEPTED and you established no new actionable defect>
Findings: <new findings only: numbered; severity (blocker/major/minor); facet; file:lines; claim and impact; remedy; evidence; confidence; or none>
Optional: <nonblocking polish, or none>
Limits: <unverified claims and review limitations, or none>
```

CLEAN means no actionable defect established within the reviewed scope, not exhaustive correctness. Do not label a
consequential unresolved claim CLEAN. Separate defects from optional polish and editorial preference.
"""

INSTR2_HEAD = """# Confirmation packet (round {round}): N1 kanji batch {batch}, revised snapshot {fix8}

You are the same reviewer who wrote the initial report on this batch (reviewed snapshot {orig8}) and the confirmation
report on its earlier revision {prior8}. The author has revised the batch again after that confirmation.{merge_note} Your job now is
to CONFIRM this new revision independently: give a disposition for each point of your confirmation report that
`RESPONSE.md` answers, and check every changed line for new defects. You will not see any other reviewer's report; do not
look for one.

## Mandate

- **Read-only.** Do not edit, stage, commit, push or run any command that changes files, except that you write your
  report to the one path named in your assignment. Do not start other agents, sessions or background jobs.
- **Serial.** Make exactly ONE tool call per response, wait for its result, then decide the next call. Read large files
  in ranges. Never list a directory recursively.
- **Allowed local reads.** (1) this packet; (2) the earlier confirmation packet `{prior_packet}` (read-only);
  (3) the original packet `{orig_packet}` (read-only); (4) your own initial report `{orig_report}`; (5) your own
  confirmation report `{prior_report}`. Open no other local path: no repository checkouts, no `docs\\n1-reviews`, no other
  packets and no other reports. Public web sources are allowed and encouraged.
- **Where the OLD and NEW text is.** This packet's `snapshot\\kanji\\` holds the revised text {fix8} of all {n_members}
  cards. The earlier confirmation packet's `snapshot\\kanji\\<card>.md` holds the text at {prior8}, the OLD text of the
  cards changed now. The original packet holds the initially reviewed snapshot {orig8}; its word articles, titles, other
  cards' files, `evidence\\` and `rubric\\` are unchanged at the revised snapshot{word_exception} and remain valid context,
  but its text of the batch cards is superseded by this packet's `snapshot\\kanji\\`.
- **Report path.** Write your report to this one path only: `{report}`

## What the batch is

Teaching cards for JLPT N1 kanji (community list): {members}. {card_note} {word_note} Audience: an English speaker
at roughly JLPT N5-N4 reading on a phone. The review contract is `rubric\\copilot-instructions.md` of the original packet.

## What to read

1. `CHANGES.md`: a neutral list of every changed line of this revision, by card.
2. `RESPONSE.md`: the author's statement on each point of YOUR confirmation report that this revision answers. These are
   claims to verify, **not evidence**: check each one against the revised card text, `diffs\\fix.patch` and independent
   sources.
3. `diffs\\fix.patch` (exact patch from {freeze8} to {fix8}, `manifest.json`{diff_excl} excluded), `diffs\\changed-lines.txt` and the
   revised cards in `snapshot\\kanji\\`.
"""

INSTR2_TAIL_FROM = "4. `evidence\\`: new evidence for this round"


def instr2_template():
    """Round-2 instructions: the round-1 template with a new head (mandate and reading list) and the same tasks and contract."""
    return INSTR2_HEAD + INSTR[INSTR.index(INSTR2_TAIL_FROM):]


EVIDENCE_README = """# Evidence added for the confirmation round

- `jmdict-cited-entries.xml`: complete JMdict entries ({jm_ids}) {jm_note}. Pinned input
  `{jm_file}` (sha256 {jm_sha}). Today's online JMdict may differ slightly.
{joyo_line}{kvg_line}- `QuizBuilder.kt`: the app's answer-option builder (how `distractors` and `quiz_exclusions` are used).
{extra}- Pinned KANJIDIC2 input: `{kd_file}` (sha256 {kd_sha}). The {n_members} KANJIDIC2 records are in the original packet
  (`evidence\\kanjidic2-records.xml`){orig_tail}.
"""

DEFAULT_ORIG_TAIL = ", together with the retrieved Digital Daijisen text (`evidence\\public-source\\`)"


def git_bytes(repo, *args):
    p = subprocess.run(["git", "-c", "core.quotepath=false", *args], cwd=repo, capture_output=True)
    if p.returncode:
        raise SystemExit("git %s failed: %s" % (" ".join(args), p.stderr.decode("utf-8", "replace")))
    return p.stdout


def git_text(repo, *args):
    return git_bytes(repo, *args).decode("utf-8")


def changed_line_ranges(patch_text):
    cur, res = None, {}
    for line in patch_text.splitlines():
        if line.startswith("+++ b/"):
            cur = line[6:]
            res[cur] = []
        m = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", line)
        if m and cur:
            start = int(m.group(1))
            count = int(m.group(2)) if m.group(2) is not None else 1
            if count:
                res[cur].append(str(start) if count == 1 else "%d-%d" % (start, start + count - 1))
    return res


LINK = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)\s]+)\)")


def front_title(text):
    m = re.search(r"^title:\s*(.+?)\s*$", text, re.M)
    return m.group(1).strip().strip('"') if m else ""


def link_table(repo, fix, ranges):
    """Every internal link on a changed line of a changed card, checked against the revised snapshot."""
    rows, bad = [], 0
    for path, rs in sorted(ranges.items()):
        if not path.endswith(".md"):
            continue
        lines = git_text(repo, "show", "%s:%s" % (fix, path)).replace("\r\n", "\n").split("\n")
        nums = set()
        for r in rs:
            lo, _, hi = r.partition("-")
            nums.update(range(int(lo), int(hi or lo) + 1))
        for n in sorted(nums):
            line = lines[n - 1]
            for m in LINK.finditer(line):
                target = m.group(2)
                if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", target) or target.startswith("#"):
                    continue
                resolved = posixpath.normpath(posixpath.join(posixpath.dirname(path), target.split("#")[0]))
                probe = subprocess.run(["git", "cat-file", "-e", "%s:%s" % (fix, resolved)], cwd=repo, capture_output=True)
                exists = probe.returncode == 0
                title = front_title(git_text(repo, "show", "%s:%s" % (fix, resolved))) if exists else ""
                q = re.match(r'^[,;]?\s*"([^"]+)"', line[m.end():])
                quoted = q.group(1).rstrip(",.;") if q else ""
                verdict = "n/a" if not quoted else ("yes" if quoted == title else "NO")
                if not exists or verdict == "NO":
                    bad += 1
                rows.append("%s:%d\t%s\t%s\t%s\t%s\t%s\t%s" % (
                    Path(path).name, n, m.group(1), resolved, "yes" if exists else "NO", title, quoted, verdict))
    head = "card:line\tlink text\tresolved path\texists\ttarget title\tquoted gloss after link\tquoted equals title"
    tail = "\n%d link(s) on changed lines; %d unresolved or mismatched." % (len(rows), bad)
    return head + "\n" + "\n".join(rows) + tail + "\n", len(rows), bad


def joyo_pages(pdf, specs, out):
    import pdfplumber
    out.mkdir(parents=True, exist_ok=True)
    with pdfplumber.open(str(pdf)) as doc:
        for spec in specs:
            page, _, kanji = spec.partition(":")
            text = doc.pages[int(page) - 1].extract_text() or ""
            missing = [k for k in kanji if k not in text]
            if missing:
                raise SystemExit("Joyo page %s lacks %s" % (page, missing))
            header = "Source: %s#page=%s\nPDF sha256: %s\nExtracted with pdfplumber; kanji expected on this page: %s\n\n" % (
                JOYO_URL, page, sha256_file(pdf), kanji)
            (out / ("p%s.txt" % page)).write_text(header + text + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=str(REPO))
    ap.add_argument("--batch", required=True)
    ap.add_argument("--freeze", required=True)
    ap.add_argument("--fix", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--response", required=True)
    ap.add_argument("--changes", required=True)
    ap.add_argument("--report", required=True)
    ap.add_argument("--orig-packet", required=True)
    ap.add_argument("--orig-report", required=True)
    ap.add_argument("--allow-deleted", action="store_true",
                    help="accept files deleted by the revision; they are listed in INSTRUCTIONS.md and diffs\\changed-files.txt")
    ap.add_argument("--members", help="kanji of the batch (default: cards added by the freeze commit)")
    ap.add_argument("--jm-id", action="append", default=[])
    ap.add_argument("--jm-note", default="cited by the revised text",
                    help="phrase after the JMdict entry ids in evidence\\README.md")
    ap.add_argument("--joyo-pdf")
    ap.add_argument("--joyo", action="append", default=[], help="PAGE:KANJI, e.g. 144:摩")
    ap.add_argument("--kvg", action="append", default=[])
    ap.add_argument("--quizbuilder", default=str(DEFAULT_QUIZBUILDER))
    ap.add_argument("--evidence", action="append", default=[], help="NAME=FILE copied to evidence\\NAME")
    ap.add_argument("--evidence-dir", action="append", default=[], help="NAME=DIR copied recursively to evidence\\NAME")
    ap.add_argument("--evidence-note", action="append", default=[], help="one README bullet describing an --evidence file")
    ap.add_argument("--check", action="append", default=[], help="NAME=FILE")
    ap.add_argument("--check-raw", action="append", default=[],
                    help="NAME=FILE copied byte for byte (keeps blank lines, so cited line numbers hold)")
    ap.add_argument("--orig-tail", default=DEFAULT_ORIG_TAIL,
                    help="text after the KANJIDIC2 records reference in evidence\\README.md; '' if the original packet has no public-source")
    ap.add_argument("--prior-confirm-packet",
                    help="round 2+: this reviewer's earlier confirmation packet (its candidate must be --freeze)")
    ap.add_argument("--prior-confirm-report", help="round 2+: this reviewer's earlier confirmation report")
    ap.add_argument("--via-merge", action="store_true",
                    help="round 2+: --freeze is a merge of current main whose first parent is the earlier packet's candidate "
                         "and which changed no path of the batch; diffs are taken from the merge")
    ap.add_argument("--intermediate", action="store_true",
                    help="with --via-merge: the merge's first parent may be a descendant of the earlier packet's candidate; "
                         "the batch changes between them, which this reviewer has not seen, go to diffs\\intermediate.patch")
    ap.add_argument("--exclude-merge", action="append", default=[],
                    help="round 1: a merge of main on the first-parent line from --freeze to --fix; the paths it changed "
                         "(none may be a batch path) are left out of diffs\\ and summarized in evidence\\merge-scope.txt")
    a = ap.parse_args()
    if a.intermediate and not a.via_merge:
        raise SystemExit("--intermediate needs --via-merge")
    if bool(a.prior_confirm_packet) != bool(a.prior_confirm_report):
        raise SystemExit("--prior-confirm-packet and --prior-confirm-report go together")

    repo = Path(a.repo)
    fix = git_text(repo, "rev-parse", a.fix).strip()
    freeze = git_text(repo, "rev-parse", a.freeze).strip()
    head = git_text(repo, "rev-parse", "HEAD").strip()
    if fix != head:
        raise SystemExit("fix %s is not HEAD %s" % (fix, head))
    if subprocess.run(["git", "merge-base", "--is-ancestor", freeze, fix], cwd=repo).returncode:
        raise SystemExit("fix does not descend from freeze")
    dirty = [l for l in git_text(repo, "status", "--porcelain", "--untracked-files=no").split("\n") if l.strip()]
    if dirty:
        raise SystemExit("tracked changes present: %s" % dirty[:5])
    out = Path(a.out)
    if out.exists():
        raise SystemExit("packet dir exists: %s" % out)
    prior, orig_candidate, rnd = None, None, 1
    if a.prior_confirm_packet:
        prior = json.loads((Path(a.prior_confirm_packet) / "packet-manifest.json").read_text(encoding="utf-8"))
        orig_candidate = json.loads((Path(a.orig_packet) / "packet-manifest.json").read_text(encoding="utf-8"))["candidate"]
        prior_cand = prior.get("candidate")
        base_cand = prior_cand
        if a.via_merge:
            parents = git_text(repo, "rev-list", "--parents", "-n", "1", freeze).split()[1:]
            if len(parents) != 2:
                raise SystemExit("--via-merge: %s is not a merge" % freeze)
            if parents[0] != prior_cand:
                if not a.intermediate:
                    raise SystemExit("--via-merge: %s is not a merge whose first parent is %s" % (freeze, prior_cand))
                if subprocess.run(["git", "merge-base", "--is-ancestor", prior_cand, parents[0]], cwd=repo).returncode:
                    raise SystemExit("--intermediate: %s does not descend from %s" % (parents[0], prior_cand))
                base_cand = parents[0]
            # the batch's own commits only: an earlier merge of main into the batch is on the first-parent line but not counted
            batch_paths = sorted(set(git_text(
                repo, "log", "--first-parent", "--no-merges", "--no-renames", "--name-only", "--format=", orig_candidate + "^.." + base_cand
            ).splitlines()))
            batch_paths = [q for q in batch_paths if q and q != "manifest.json"]
            moved = git_text(repo, "diff", "--name-only", base_cand, freeze, "--", *batch_paths).split()
            if moved:
                raise SystemExit("--via-merge: the merge changed batch paths %s" % moved[:5])
        elif prior_cand != freeze:
            raise SystemExit("prior confirmation packet reviewed %s, not --freeze %s" % (prior_cand, freeze))
        else:
            # the batch's own commits only, so that merges of main (excluded in round 1) are not reported as batch changes
            batch_paths = sorted(set(git_text(
                repo, "log", "--first-parent", "--no-merges", "--no-renames", "--name-only", "--format=", orig_candidate + "^.." + freeze
            ).splitlines()))
            batch_paths = [q for q in batch_paths if q and q != "manifest.json"]
        if prior.get("freeze") != orig_candidate and prior.get("originalCandidate") != orig_candidate:
            raise SystemExit("prior confirmation packet does not descend from the original packet's candidate %s" % orig_candidate)
        if not Path(a.prior_confirm_report).is_file():
            raise SystemExit("missing prior confirmation report %s" % a.prior_confirm_report)
        rnd = int(prior.get("round", 1)) + 1

    via = bool(prior) and a.via_merge
    prior8 = (prior["candidate"] if prior else freeze)[:8]
    if a.members:
        members = list(a.members)
    else:
        added = git_text(repo, "diff", "--name-status", "--no-renames", freeze + "^", freeze, "--", "kanji")
        members = [Path(l.split("\t")[1]).stem for l in added.splitlines() if l.startswith("A\t")]
    if not members:
        raise SystemExit("no batch members found")

    excluded, scope = set(), []
    if a.exclude_merge:
        if prior:
            raise SystemExit("--exclude-merge is for round 1; use --via-merge in later rounds")
        first_parent = git_text(repo, "rev-list", "--first-parent", freeze + ".." + fix).split()
        own_paths = set(p for p in git_text(repo, "log", "--first-parent", "--no-merges", "--no-renames", "--name-only",
                                            "--format=", freeze + "^.." + fix).splitlines() if p)
        for spec in a.exclude_merge:
            merge = git_text(repo, "rev-parse", spec).strip()
            if merge not in first_parent:
                raise SystemExit("--exclude-merge: %s is not on the first-parent line %s..%s" % (spec, freeze[:8], fix[:8]))
            parents = git_text(repo, "rev-list", "--parents", "-n", "1", merge).split()[1:]
            if len(parents) != 2:
                raise SystemExit("--exclude-merge: %s is not a merge" % spec)
            rows = [l.partition("\t") for l in git_text(repo, "diff", "--name-status", "--no-renames", parents[0],
                                                       merge).splitlines() if l.strip()]
            clash = sorted(p for s, _, p in rows if p in own_paths and p != "manifest.json")
            if clash:
                raise SystemExit("--exclude-merge: %s changed batch paths %s" % (spec, clash[:5]))
            excluded.update(p for s, _, p in rows)
            scope.append((merge, parents, rows))

    status = git_text(repo, "diff", "--name-status", "--no-renames", freeze, fix)
    changed = {}
    for line in status.splitlines():
        st, _, path = line.partition("\t")
        if path in excluded and path != "manifest.json":
            continue
        changed[path] = st
    diff_paths = ([p for p in sorted(changed) if p != "manifest.json"] if excluded
                  else [".", ":(exclude)manifest.json"])
    content_changed = {p: s for p, s in changed.items() if p != "manifest.json"}
    deleted = sorted(p for p, s in content_changed.items() if s == "D")
    if deleted and not a.allow_deleted:
        raise SystemExit("deleted file in the revision: %s" % deleted[0])
    for p in deleted:
        if p.startswith("kanji/") and Path(p).stem in members:
            raise SystemExit("deleted batch card: %s" % p)
        del content_changed[p]

    # round 2+: files outside the batch cards that an earlier revision changed; the original packet's copy is stale
    earlier_other, earlier_deleted = [], []
    if prior:
        for line in (git_text(repo, "diff", "--name-status", "--no-renames", orig_candidate,
                              base_cand if a.via_merge else freeze, "--", *batch_paths).splitlines() if batch_paths else []):
            s0, _, p0 = line.partition("\t")
            if s0 == "D" and p0 not in content_changed:
                earlier_deleted.append(p0)
            if (s0 != "D" and p0 != "manifest.json" and p0 not in content_changed and p0 not in deleted
                    and not (p0.startswith("kanji/") and Path(p0).stem in members)):
                earlier_other.append(p0)

    out.mkdir(parents=True)
    # snapshot of every member card plus any other changed content file
    for k in members:
        dst = out / "snapshot" / "kanji" / (k + ".md")
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes((repo / "kanji" / (k + ".md")).read_bytes())
    for p in list(content_changed) + earlier_other:
        if not p.startswith("kanji/") or Path(p).stem not in members:
            dst = out / "snapshot" / p
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes((repo / p).read_bytes())
    blobs = {("snapshot/" + p): git_text(repo, "rev-parse", "%s:%s" % (fix, p)).strip()
             for p in [("kanji/%s.md" % k) for k in members]
             + [p for p in content_changed if not (p.startswith("kanji/") and Path(p).stem in members)]
             + earlier_other}

    # diffs
    (out / "diffs").mkdir()
    patch = git_bytes(repo, "diff", "--no-color", freeze, fix, "--", *diff_paths)
    (out / "diffs" / "fix.patch").write_bytes(patch)
    (out / "diffs" / "changed-files.txt").write_text(
        "".join("%s\t%s\n" % (s, p) for p, s in sorted(changed.items())), encoding="utf-8")
    u0 = git_text(repo, "diff", "--no-color", "-U0", freeze, fix, "--", *diff_paths)
    ranges = changed_line_ranges(u0)
    inter8 = ""
    if via and base_cand != prior_cand:
        inter8 = base_cand[:8]
        (out / "diffs" / "intermediate.patch").write_bytes(
            git_bytes(repo, "diff", "--no-color", prior_cand, base_cand, "--", *batch_paths))
    (out / "diffs" / "changed-lines.txt").write_text(
        "Changed line numbers on the revised (new) side, by file.\n" +
        "".join("%s: %s\n" % (p, ", ".join(r)) for p, r in sorted(ranges.items())), encoding="utf-8")

    # evidence
    ev = out / "evidence"
    ev.mkdir()
    jm_ids = sorted(set(a.jm_id), key=int)
    if jm_ids:
        (ev / "jmdict-cited-entries.xml").write_bytes(n1cmds.jmdict_xml(jm_ids))
    if a.joyo:
        if not a.joyo_pdf:
            raise SystemExit("--joyo needs --joyo-pdf")
        joyo_pages(Path(a.joyo_pdf), a.joyo, ev / "joyo")
    if a.kvg:
        (ev / "kanjivg").mkdir()
        for f in a.kvg:
            shutil.copy2(f, ev / "kanjivg" / Path(f).name)
    shutil.copy2(a.quizbuilder, ev / "QuizBuilder.kt")
    for spec in a.evidence:
        name, _, path = spec.partition("=")
        if not name or not Path(path).is_file() or "/" in name or "\\" in name:
            raise SystemExit("bad --evidence %s" % spec)
        shutil.copy2(path, ev / name)
    for spec in a.evidence_dir:
        name, _, path = spec.partition("=")
        if not name or not Path(path).is_dir() or "/" in name or "\\" in name or (ev / name).exists():
            raise SystemExit("bad --evidence-dir %s" % spec)
        shutil.copytree(path, ev / name)
    if scope:
        lines = ["Paths changed by merges of main into the batch. They are left out of diffs\\; none is a path that a batch",
                 "commit from %s to %s changed (checked by the packet builder)." % (freeze[:8], fix[:8]), ""]
        for merge, parents, rows in scope:
            lines.append("Merge %s (first parent %s, second parent %s): %d path(s)." % (
                merge, parents[0], parents[1], len(rows)))
            lines.append("Reproduce: git diff --name-status --no-renames %s %s" % (parents[0], merge))
            groups = {}
            for s, _, p in rows:
                key = (s, "/".join(p.split("/")[:3]) if p.count("/") >= 3 else p)
                groups[key] = groups.get(key, 0) + 1
            lines.extend("  %s %6d  %s" % (s, n, k) for (s, k), n in sorted(groups.items(), key=lambda x: (x[0][1], x[0][0])))
            lines.append("")
        (ev / "merge-scope.txt").write_text("\n".join(lines), encoding="utf-8")
        a.evidence_note.append("`merge-scope.txt`: the paths that merges of main into the batch changed, grouped by"
                               " directory; they are not batch files and are left out of `diffs\\`.")
    kvg_line = ("- `kanjivg\\<hex>.svg`: KanjiVG records at the pinned revision 70a0b7ae0c18ceb5cb358274b029cce0234a43bc\n"
                "  (`%s`). They show component structure and the `kvg:original` and `kvg:variant` attributes.\n"
                % (KVG_URL % "<hex>.svg")) if a.kvg else ""
    (ev / "README.md").write_text(EVIDENCE_README.format(
        jm_ids=", ".join(jm_ids) or "none", jm_note=a.jm_note, jm_file=JMDICT_GZ.name, jm_sha=sha256_file(JMDICT_GZ),
        joyo_line=("- `joyo\\p<N>.txt`: text extracted with pdfplumber from page N of the official Joyo kanji table (2010, MEXT),\n"
                   "  `%s#page=N` (PDF file sha256 %s). The extraction is a convenience; verify against the PDF when it matters.\n"
                   % (JOYO_URL, sha256_file(a.joyo_pdf))) if a.joyo else "",
        kvg_line=kvg_line, kd_file=KANJIDIC_GZ.name, kd_sha=sha256_file(KANJIDIC_GZ), orig_tail=a.orig_tail,
        n_members=len(members),
        extra="".join("- %s\n" % n for n in a.evidence_note)), encoding="utf-8")

    # checks
    (out / "checks").mkdir()
    table, n_links, n_bad = link_table(repo, fix, ranges)
    (out / "checks" / "link-targets.tsv").write_text(table, encoding="utf-8")
    print("links on changed lines: %d, unresolved or mismatched: %d" % (n_links, n_bad))
    for spec in a.check:
        name, _, path = spec.partition("=")
        body = n1cmds.read_log(path) if Path(path).is_file() else "(missing %s)" % path
        if "unit" in name.lower():
            lines = body.split("\n")
            ran = [i for i, l in enumerate(lines) if re.match(r"^Ran \d+ tests? in ", l)]
            if ran:
                i = ran[-1]
                body = "\n".join(lines[i - 1 if i and lines[i - 1].startswith("---") else i:i + 2])
            else:
                body = "\n".join(lines[-3:])
        (out / "checks" / (name + ".txt")).write_text(body.strip() + "\n", encoding="utf-8")
    for spec in a.check_raw:
        name, _, path = spec.partition("=")
        shutil.copyfile(path, out / "checks" / (name + ".txt"))

    # author statements and instructions
    shutil.copy2(a.response, out / "RESPONSE.md")
    shutil.copy2(a.changes, out / "CHANGES.md")
    def is_member(p):
        return p.startswith("kanji/") and Path(p).stem in members
    changed_cards = [Path(p).stem for p in sorted(content_changed) if is_member(p)]
    unchanged = [k for k in members if k not in changed_cards]
    other_changed = [p for p in sorted(content_changed) if not is_member(p)]
    def fmt(ps):
        return ", ".join("`%s`" % p.replace("/", "\\") for p in ps)
    excepts = []
    if other_changed:
        modified_other = [p for p in other_changed if content_changed[p] != "A"]
        added_other = [p for p in other_changed if content_changed[p] == "A"]
        parts = []
        if modified_other:
            if prior:
                in_prior = [p for p in modified_other if (Path(a.prior_confirm_packet) / "snapshot" / p).is_file()]
                old_where = (" (revised text under `snapshot\\`; the text at %s is in the earlier confirmation packet's "
                             "`snapshot\\`%s)" % (prior8, "" if len(in_prior) == len(modified_other) else
                             " where it has a copy, otherwise in the original packet's `snapshot\\` and `repo\\`"))
            else:
                old_where = (" (revised text under `snapshot\\`; the reviewed text is in the original packet's `snapshot\\` "
                             "and `repo\\`)")
            parts.append("changes %d file(s) outside the batch cards: %s%s" % (
                len(modified_other), ", ".join("`%s`" % p.replace("/", "\\") for p in modified_other), old_where))
        if added_other:
            parts.append("adds %d new file(s): %s (text under `snapshot\\`; not in the original packet)" % (
                len(added_other), ", ".join("`%s`" % p.replace("/", "\\") for p in added_other)))
        if added_other:
            excepts.append("%s, added by this revision" % fmt(added_other))
        if modified_other:
            excepts.append("%s, changed by this revision" % fmt(modified_other))
        word_note = "The revision also " + "; it also ".join(parts) + "."
    else:
        word_note = "No word article changed in this revision."
    if earlier_other:
        listed0 = fmt(earlier_other)
        excepts.append("%s, changed by an earlier revision" % listed0)
        word_note += (" An earlier revision changed %d file(s) outside the batch cards: %s; this revision leaves them unchanged, "
                      "and their current text is in this packet's `snapshot\\`." % (len(earlier_other), listed0))
    if earlier_deleted:
        listed_e = fmt(earlier_deleted)
        word_note += (" An earlier revision deleted %d file(s): %s. The original packet's copy is the deleted text; it is not part "
                      "of the revised snapshot." % (len(earlier_deleted), listed_e))
        excepts.append("%s, deleted by an earlier revision" % listed_e)
    if deleted:
        listed_d = fmt(deleted)
        if prior and all((Path(a.prior_confirm_packet) / "snapshot" / p).is_file() for p in deleted):
            where_d = "The earlier confirmation packet's `snapshot\\` copy is the deleted text"
        else:
            where_d = "The original packet's copy is the deleted text"
        word_note += (" The revision deletes %d file(s): %s. %s; it is not part of the "
                      "revised snapshot, and `diffs\\fix.patch` shows the deletion." % (len(deleted), listed_d, where_d))
        excepts.append("%s, deleted by this revision" % listed_d)
    inner = []
    if excepts:
        inner.append("except: %s; the current text of every added or changed file is in this packet's `snapshot\\`"
                     % "; ".join(excepts))
    if scope:
        inner.append("%sain's own files that %s of main into the batch (%s) changed also differ; none is a batch file, they"
                     " are left out of `diffs\\`, and `evidence\\merge-scope.txt` of this packet lists them"
                     % ("M" if inner else "m", "a merge" if len(scope) == 1 else "merges",
                        ", ".join(m[:8] for m, _, _ in scope)))
    if via:
        inner.append("%sain's own files that a merge of main into the batch changed also differ; none is a batch file, and"
                     " the `merge-scope` files in `evidence\\` of this packet or the earlier confirmation packet list them"
                     % ("M" if inner else "m"))
    word_exception = (" (%s)" % ". ".join(inner)) if inner else ""
    if changed_cards:
        card_note = ("This revision changes %d of these cards (%s) relative to %s; the cards not changed by it are: %s." % (
            len(changed_cards), " ".join(changed_cards), freeze[:8], " ".join(unchanged) or "none"))
    else:
        card_note = "This revision changes none of these cards relative to %s." % freeze[:8]
    merge_note = ((" Before this revision the author merged current main into the batch (merge %s, a child of %s);"
                   " the merge changed no file of the batch, so the batch text at %s is the text at %s, and this"
                   " revision is a child of the merge." % (freeze[:8], prior8, freeze[:8], prior8)) if via and not inter8 else "")
    if inter8:
        merge_note = ((" You have not seen an intermediate revision: %s, a descendant of %s, changed batch files after your"
                       " confirmation report. `diffs\\intermediate.patch` is its exact batch-path patch from %s to %s (main's"
                       " other content, merged in between, excluded); review it as part of this round, with the same tasks"
                       " as `diffs\\fix.patch`. The author then merged current main into the batch again (merge %s, a child of"
                       " %s); that merge changed no file of the batch, so the batch text at %s is the text at %s, and this"
                       " revision is a child of the merge. The earlier confirmation packet's `snapshot\\` holds the text at %s,"
                       " before the intermediate revision." % (inter8, prior8, prior8, inter8, freeze[:8], inter8, freeze[:8],
                                                              inter8, prior8)))
    (out / "INSTRUCTIONS.md").write_text((instr2_template() if prior else INSTR).format(
        batch=a.batch, fix8=fix[:8], freeze8=freeze[:8], orig_packet=a.orig_packet, orig_report=a.orig_report,
        report=a.report, members=" ".join(members), n_changed=len(changed_cards),
        changed=" ".join(changed_cards), unchanged=" ".join(unchanged) or "none",
        word_exception=word_exception, word_note=word_note, round=rnd, card_note=card_note, orig8=(orig_candidate or freeze)[:8],
        prior_packet=a.prior_confirm_packet, prior_report=a.prior_confirm_report, n_members=len(members),
        prior8=prior8, merge_note=merge_note,
        diff_excl=" and the merged-in files of main listed in `evidence\\merge-scope.txt`" if scope else ""),
        encoding="utf-8")

    files = {}
    for p in sorted(out.rglob("*")):
        if p.is_file() and p.name != "packet-manifest.json":
            files[p.relative_to(out).as_posix()] = {"sha256": sha256_file(p), "bytes": p.stat().st_size}
    extra_meta = {"round": rnd, "originalCandidate": orig_candidate, "priorConfirmPacket": a.prior_confirm_packet,
                  "priorConfirmReport": a.prior_confirm_report} if prior else {}
    if scope:
        extra_meta.update(excludedMerges=[m for m, _, _ in scope], excludedPathCount=len(excluded))
    if via:
        extra_meta.update(priorCandidate=prior["candidate"], integrationMerge=freeze)
        if inter8:
            extra_meta.update(intermediateCandidate=base_cand)
    (out / "packet-manifest.json").write_text(json.dumps(dict({
        "kind": "confirmation", "batch": a.batch, "candidate": fix, "freeze": freeze, "builtAt": n1cmds.now_utc(),
        "members": members, "changed": changed, "snapshotBlobs": blobs, "originalPacket": a.orig_packet,
        "originalReport": a.orig_report, "report": a.report}, **extra_meta, fileCount=len(files), files=files),
        ensure_ascii=False, indent=1), encoding="utf-8")
    total = sum(v["bytes"] for v in files.values())
    print("confirmation packet %s: %d files, %.2f MB; changed cards %s; unchanged %s" % (
        out, len(files), total / 1e6, changed_cards, unchanged))
    return 0


if __name__ == "__main__":
    sys.exit(main())

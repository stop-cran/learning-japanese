# B134 integration-impact confirmation — reviewer instructions

You are a **fresh replacement reviewer**. You did not author or review B134.
The original B134 reviewer sessions could not be resumed on this PC, so this
confirmation is labelled as a replacement review, not as reuse of an earlier
reviewer session. Work independently and do not assume another reviewer's
conclusions.

## Frozen snapshot

- Repository worktree (READ-ONLY for you):
  `C:\Users\romanko\n1-kanji-workspace\learning-japanese`
- Frozen merge commit under review: `bf9aa740208cceb660788f150b2a4e76930d41d1` (M2)
  - Parent 1: `2eb0e9c97d44e61bf611153ce5899714c1aec35a` — B134 handoff (紫 card, already
    closed by two-family review on snapshot `cc374051`, closure `ae155573`).
  - Parent 2: `9d7b512133f536027c0b601ae0273273b42072ce` — current `origin/main`
    (29 commits of N3 grammar articles and 気 see-also links since merge base
    `830f740b`).
- Packet evidence: `packet\evidence\` next to this file.

You may run only read-only commands, for example `git show`, `git diff`,
`git ls-tree`, `git log`, and reading files. Use `git -c core.quotepath=false`
for Japanese paths. Do NOT edit, stage, commit, checkout, reset, merge, or
push anything, and do not create files anywhere except your single report.

## Mandate

The B134 teaching content was reviewed and closed before this merge. Decide
only whether integrating current `origin/main` **changes the teaching or quiz
behaviour of B134** or creates an **overlapping substantive conflict**. Do not
re-review the 紫 card's prose from scratch; report a pre-existing card issue
only if the merge makes it newly wrong or newly unsafe.

Check at least:

1. The mechanical claim in `evidence/merge-proof.json`: every non-derived path in
   M2 equals one parent byte-for-byte, and `kanji/紫.md`, `strokes/紫.json`,
   `words/紫.md` are identical to `cc374051` and `ae155573`. Spot-check it
   independently with git.
2. `manifest.json` (the only textual conflict) in M2 matches what
   `tools/build_manifest.py` would derive, and its 紫 entries and hashes are present.
   You may reason from the tool's source and the tree; do not run tools that write files.
3. Whether any main-side change (see `evidence/main-changes-stat.txt` and
   `evidence/main-runtime-diff.patch`) alters a file 紫 links to, a kanji in its
   `distractors` or `quiz_exclusions`, a word article it relies on, the quiz
   meaning pools, or reading practice for 紫, シ or むらさき.
4. Whether main introduces new content using 紫 (for example in N3 grammar
   example sentences) that would conflict with the 紫 card's teaching.

## Report contract

Write exactly one Markdown file to the report path given in your prompt, with
these sections:

- `## Snapshot` — the commit you reviewed.
- `## Scope` — what you checked and how (commands at a summary level).
- `## Verdicts` — one line each, value `CLEAN`, `NEEDS FIX`, or `UNVERIFIED`:
  - Mechanical merge integrity
  - Manifest derivation
  - Teaching/quiz impact on B134
  - Overlapping substantive conflict
- `## Findings` — numbered; each with evidence (path, commit, line) and the
  smallest fix. Write "None." if there are none.
- `## Limits` — anything you could not verify.

End with a single line: `OVERALL: CLEAN` or `OVERALL: NEEDS FIX`.

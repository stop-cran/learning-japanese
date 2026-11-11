# Confirmation packet: N1 kanji batch 109, revised snapshot a3e0610a

You are the same reviewer who wrote the initial report on this batch (reviewed snapshot 0a20f4bf). The author has
since revised the batch. Your job now is to CONFIRM the revision independently: give a disposition for each of your own
earlier points, and check every changed line for new defects. You will not see any other reviewer's report; do not look
for one.

## Mandate

- **Read-only.** Do not edit, stage, commit, push or run any command that changes files, except that you write your
  report to the one path named in your assignment. Do not start other agents, sessions or background jobs.
- **Serial.** Make exactly ONE tool call per response, wait for its result, then decide the next call. Read large files
  in ranges. Never list a directory recursively.
- **Allowed local reads.** (1) this packet; (2) the original packet `C:\Users\stop-\n1-kanji-workspace\review-packets\batch-109-0a20f4bf` (read-only);
  (3) your own initial report `C:\Users\stop-\n1-kanji-workspace\review-packets\reports-109\initial-claude.md`. Open no other local path: no repository checkouts, no `docs\n1-reviews`,
  no other packets and no other reports. Public web sources are allowed and encouraged.
- **The original packet holds the OLD text of the changed cards.** Its `snapshot\kanji\<card>.md` and
  `repo\kanji\<card>.md` show the reviewed snapshot. The revised text exists only in `snapshot\kanji\` of THIS packet.
  Every other file of the original packet (word articles, titles, other cards, `evidence\`, `rubric\`) is unchanged at the
  revised snapshot and remains valid context.
- **Report path.** Write your report to this one path only: `C:\Users\stop-\n1-kanji-workspace\review-packets\reports-109\confirm-claude.md`

## What the batch is

Teaching cards for JLPT N1 kanji (community list): 促 催 弧 影 批 抗 択 抵 括 掲 摩 撃 撮 擦 攻. The revision changes 13 of these cards
(促 催 弧 影 抗 抵 括 掲 摩 撃 撮 擦 攻); the unchanged cards are: 批 択. No word article changed in this revision. Audience: an English speaker
at roughly JLPT N5-N4 reading on a phone. The review contract is `rubric\copilot-instructions.md` of the original packet.

## What to read

1. `CHANGES.md`: a neutral list of every changed line, by card.
2. `RESPONSE.md`: the author's statement on each of YOUR earlier findings, optional points and limits. These are claims
   to verify, **not evidence**: check each one against the revised card text, `diffs\fix.patch` and independent sources.
3. `diffs\fix.patch` (exact patch from the reviewed snapshot to the revised snapshot, `manifest.json` excluded),
   `diffs\changed-lines.txt` and the revised cards in `snapshot\kanji\`.
4. `evidence\`: new evidence for this round (see `evidence\README.md`): the complete JMdict entries cited by the new
   text, the official Joyo kanji table pages, KanjiVG records, and the app's `QuizBuilder.kt`.
5. `checks\`: automatic checks at the revised snapshot. `checks\quiz-safety.txt` shows the four answer options now
   offered for each card (the first option is the correct title). `checks\link-targets.tsv` lists every link on a changed
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
3. **Quiz options.** Check the post-fix options in `checks\quiz-safety.txt` and the mechanics in
   `evidence\QuizBuilder.kt` for every card of the batch, not only the changed ones.
4. **New findings.** Report only what is new and established. Do not re-raise a point you have dispositioned unless the
   revision itself is wrong. No finding quota.

Verify consequential claims yourself against reputable sources. A search snippet is not verification. Say what you could
not verify.

## Report contract (use exactly this shape)

```text
Snapshot: <commit a3e0610a; reviewer model as you identify it>
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

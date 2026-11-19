# Confirmation packet (round 2): N1 kanji batch 148, revised snapshot 4162ea2c

You are the same reviewer who wrote the initial report on this batch (reviewed snapshot 8408b3a5) and the confirmation
report on its earlier revision cc286cc3. The author has revised the batch again after that confirmation. Your job now is
to CONFIRM this new revision independently: give a disposition for each point of your confirmation report that
`RESPONSE.md` answers, and check every changed line for new defects. You will not see any other reviewer's report; do not
look for one.

## Mandate

- **Read-only.** Do not edit, stage, commit, push or run any command that changes files, except that you write your
  report to the one path named in your assignment. Do not start other agents, sessions or background jobs.
- **Serial.** Make exactly ONE tool call per response, wait for its result, then decide the next call. Read large files
  in ranges. Never list a directory recursively.
- **Allowed local reads.** (1) this packet; (2) the earlier confirmation packet `C:\Users\romanko\n1-kanji-workspace\review-packets\confirm-148-claude` (read-only);
  (3) the original packet `C:\Users\romanko\n1-kanji-workspace\review-packets\batch-148-8408b3a5` (read-only); (4) your own initial report `C:\Users\romanko\n1-kanji-workspace\review-packets\reports-148\initial-claude.md`; (5) your own
  confirmation report `C:\Users\romanko\n1-kanji-workspace\review-packets\reports-148\confirm-claude.md`. Open no other local path: no repository checkouts, no `docs\n1-reviews`, no other
  packets and no other reports. Public web sources are allowed and encouraged.
- **Where the OLD and NEW text is.** This packet's `snapshot\kanji\` holds the revised text 4162ea2c of all 15
  cards. The earlier confirmation packet's `snapshot\kanji\<card>.md` holds the text at cc286cc3, the OLD text of the
  cards changed now. The original packet holds the initially reviewed snapshot 8408b3a5; its word articles, titles, other
  cards' files, `evidence\` and `rubric\` are unchanged at the revised snapshot and remain valid context,
  but its text of the batch cards is superseded by this packet's `snapshot\kanji\`.
- **Report path.** Write your report to this one path only: `C:\Users\romanko\n1-kanji-workspace\review-packets\reports-148\confirm2-claude.md`

## What the batch is

Teaching cards for JLPT N1 kanji (community list): 絞 継 綱 緊 締 緩 緯 縁 縄 縛 縦 織 繕 繰 罰. This revision changes 2 of these cards
(緊 締) relative to cc286cc3; the cards not changed by it are: 絞 継 綱 緩 緯 縁 縄 縛 縦 織 繕 繰 罰. No word article changed in this revision. Audience: an English speaker
at roughly JLPT N5-N4 reading on a phone. The review contract is `rubric\copilot-instructions.md` of the original packet.

## What to read

1. `CHANGES.md`: a neutral list of every changed line of this revision, by card.
2. `RESPONSE.md`: the author's statement on each point of YOUR confirmation report that this revision answers. These are
   claims to verify, **not evidence**: check each one against the revised card text, `diffs\fix.patch` and independent
   sources.
3. `diffs\fix.patch` (exact patch from cc286cc3 to 4162ea2c, `manifest.json` excluded), `diffs\changed-lines.txt` and the
   revised cards in `snapshot\kanji\`.
4. `evidence\`: new evidence for this round; `evidence\README.md` describes each file (the complete JMdict entries cited by
   the new text, official Joyo kanji table pages when supplied, the app's `QuizBuilder.kt` and anything else it lists).
5. `checks\`: automatic checks at the revised snapshot. `checks\quiz-safety.txt` shows, for each card, the correct
   title in parentheses after the kanji, followed by the three wrong meaning options now offered.
   `checks\reading-options.txt`, when present, lists for
   every reading prompt the excluded readings, the curated and fallback candidates for the wrong options, and a check that
   no reading attested for the card but not listed in its metadata can be offered as a wrong option.
   `checks\link-targets.tsv` lists every link on a changed
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
   `evidence\QuizBuilder.kt` for every card of the batch, not only the changed ones. Where `checks\reading-options.txt`
   and the app's reading-quiz sources are supplied, check the reading prompts the same way and say what the audit cannot show.
4. **New findings.** Report only what is new and established. Do not re-raise a point you have dispositioned unless the
   revision itself is wrong. No finding quota.

Verify consequential claims yourself against reputable sources. A search snippet is not verification. Say what you could
not verify.

## Report contract (use exactly this shape)

```text
Snapshot: <commit 4162ea2c; reviewer model as you identify it>
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

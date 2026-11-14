# Author's statement for the reviewer of `reports-115\initial-claude-004-coordinator-normalized.md`

This statement answers only the points in YOUR initial report. That file is your report with only two cells of its
verdict table normalized (`NEEDS FIX (F1)` for 卓 and `NEEDS FIX (F2)` for 寸 now read `NEEDS FIX`); no judgment, label or
citation differs from what you wrote. F1, F2, O1 to O6 and
L1 to L7 are your report's own labels. The statement is the author's claim about what changed and why. Verify each claim
against the revised card text in `snapshot\kanji\`, `diffs\fix.patch` and the evidence; do not rely on this text as
evidence. Line numbers refer to the revised cards in this packet. 6 of the 8 cards changed (卓 厄 宙 寸 票 魔); 康 and 漠
did not (see `CHANGES.md`). Give a disposition for each of F1, F2 and O1 to O6. L1 to L7 need none; see the notes at the
end.

## Pair mechanics (applies to F1, F2, O1 and O5)

Every pair added in this revision is declared once, on the batch card's side; no counterpart card changed, and no
exclusion was added between two counterparts. Author's script over all 1,229 cards at the revised snapshot, for the
eleven added pairs: no counterpart lists its batch card in `quiz_exclusions` or `distractors`; no batch card lists a
counterpart in `distractors`; no card lists both members of an added pair in `distractors`; every counterpart still has
three `distractors`. Of the counterparts, only 微 has `quiz_exclusions` (細, 小, 少, 薄, 弱, 分, 軽), and 寸 is not among
them. `excluded(a, b)` in `evidence\QuizBuilder.kt` (line 26) is true if either card lists the other, and `tryAdd`
(lines 28-32) refuses a candidate excluded against the target or against an option already chosen, for curated and
fallback candidates alike (lines 34-36). `checks\quiz-safety.txt` is byte-identical to the original packet's copy: the
three wrong options shown for each of the 8 cards in the modelled pools did not change.

## Findings

### F1 (medium): 卓 quiz_exclusions omit 英, 冠 and 越

Author action: **changed, as required, with a Notes line.**

- `卓.md:14` now reads `quiz_exclusions: [机, 台, 高, 優, 超, 表, 偉, 英, 著, 冠, 凌, 越]` (it read
  `[机, 台, 高, 優, 超, 表]`). 英, 冠 and 越 answer F1; 偉 and 著 answer O1; 凌 is listed under "Changes that do not
  answer a point in your report".
- `卓.md:59-63` are a new Notes bullet after the unchanged 机/台/高/優/超 bullet (lines 56-58): `The eminence branch also
  overlaps [偉](偉.md), great, [英](英.md), outstanding, [著](著.md), remarkable, and [冠](冠.md), peerless. [凌](凌.md)
  and [越](越.md) share surpassing or exceeding with 超. These direct pairs are excluded from meaning choices; their
  Japanese words are not interchangeable with 卓越 or 卓抜.`
- The title `table; eminent` is unchanged; the author chose the exclusion route rather than narrowing the title.

To verify: that 英, 冠 and 越 are declared, and that the new bullet explains the comparisons in the way the 優/超 bullet
does without claiming the Japanese words are interchangeable.

### F2 (medium): 寸 quiz_exclusions omit 微

Author action: **changed, as required.**

- `寸.md:14` now reads `quiz_exclusions: [小, 少, 短, 細, 微, 計, 測]` (微 added after 細).
- `寸.md:59-61`: the smallness bullet now reads `[小](小.md), small, [少](少.md), a little, [短](短.md), short,
  [細](細.md), fine/small in detail, and [微](微.md), minute/tiny, overlap aspects of smallness.` "tiny" is the author's
  gloss of minute in the smallness sense, which 微's card explains as very small or tiny; 微's title is `minute; faint`.
  Lines 62-63 (計/測) are unchanged.

To verify: that 微 is declared and mentioned in Notes.

## Optional

### O1: 偉 and 著 also approach 卓's "eminent"

Author action: **changed, as suggested**, together with F1: both are in `卓.md:14` and named in `卓.md:59-60`
(`[偉](偉.md), great, ... [著](著.md), remarkable`).

### O2: 軽 and 粒 near 寸's "small"

Author action: **declined.** Neither is added. 軽's title `lightweight; slight` leads with weight, and 粒's title
`grain; small particle` leads with a particle; in each, the smallness cue qualifies a different leading meaning, so the
author does not treat either label as a defensible answer for 寸. Your report noted that each has a distinguishing first
gloss.

To answer: DECLINE ACCEPTED or DECLINE REJECTED, with the reason.

### O3: 害 and 損 near 厄's "calamity"

Author action: **declined.** Neither is added. 害 `harm` and 損 `loss; damage` name consequences that misfortune can
cause, not glosses of misfortune or calamity itself; 厄's exclusions cover labels that display ill fortune, difficulty,
suffering, trouble or evil (`厄.md:54-64`).

To answer: DECLINE ACCEPTED or DECLINE REJECTED, with the reason.

### O4: 幸 and 福 near 康's "well-being"

Author action: **declined.** Neither is added, and 康 is unchanged. 幸 `happiness; good fortune` and 福 `good fortune`
name luck and happiness, not health; the 幸福 link is a compound of 幸 and 福, not of 康.

To answer: DECLINE ACCEPTED or DECLINE REJECTED, with the reason.

### O5: Reverse exclusions on existing cards

Author action: **symmetric handling confirmed from the app source; no reciprocal declaration added.** Your suggestion
offered confirming symmetric handling as an alternative to adding 魔 to 魅 and 寸 to 微. `evidence\QuizBuilder.kt`, the
app's answer-option builder, is now supplied: `excluded(a, b)` (line 26) is true if either card lists the other, and
`tryAdd` (lines 28-32) applies it to curated and fallback candidates alike (lines 34-36). 魅 and 微 are unchanged. See
"Pair mechanics" above.

To answer: RESOLVED if the supplied source settles the symmetry question; otherwise DECLINE ACCEPTED or DECLINE REJECTED,
with the reason.

### O6: Reduced reading-quiz distractor pools for 票 and 魔

Author action: **deferred.** No `distractors` list changed. A replacement shape distractor is recorded as separate later
polish, not part of batch 115. `checks\reading-options.txt`, new in this round, models the on-reading prompts over the
whole card pool with 100 seeds: for 票, 栗 has no usable on reading and its slot is filled from the fallback (lines
90-101; 0 seeds with fewer than three wrong options); for 魔, 摩 is skipped as excluded and 鹿's slot is filled from the
fallback (lines 104-115; 0 seeds with fewer than three wrong options). The model is a host audit, not app execution.

To answer: DECLINE ACCEPTED if deferral is acceptable for this batch, otherwise DECLINE REJECTED, with the reason.

## Limits

No action is claimed, and no disposition is needed. Notes:

- L1: no stroke file, Joyo row or asset changed in this revision.
- L2: 災, 禍, 鬼, 霊, 尺 and 曖 still have no card at the revised snapshot; nothing was added for them.
- L3: 康 is unchanged; no statement about 康 or 康健 was added.
- L4: the checks in `checks\` were rerun at the revised snapshot. One discrepancy concerns your original chain: the
  original packet's `checks\lint.txt` reports `0 error(s), 0 warning(s)`, but that result cannot be reproduced from the
  reviewed snapshot. The same lint rerun at both the reviewed and the revised snapshot gives `0 error(s), 4 warning(s)`,
  all pre-existing and accepted as non-blocking. The frozen log is left unchanged and is not relied on. See "Lint" in
  `CHANGES.md`.
- L5: the quiz engine's exclusion handling is now visible in `evidence\QuizBuilder.kt`; see O5.
- L6 and L7: unchanged. No Kotlin, JVM, native, phone or emulator execution occurred for this revision. Installed APK
  `5c000bd` predates `quiz_exclusions`, so none of the new pairs protects that build.

## Changes that do not answer a point in your report

They are listed in `CHANGES.md`; please review them like any other changed hunk. Each states what the author claims and
why.

- `卓.md:14` and `:61`: 凌 `endure; surpass` was added: `[凌](凌.md) and [越](越.md) share surpassing or exceeding
  with 超.` The author's reason: 卓 already excludes 超 `exceed; surpass` for the eminence sense, and 凌's title displays
  surpass, the same reason that applies to 越 in F1.
- `厄.md:14` and `:58-61`: 労 `labor; trouble` was added: `[労](労.md), labor/trouble, also displays trouble, as in
  [苦労](../words/苦労.md) くろう, hardship. That direct pair is excluded from meaning choices; work itself is not
  misfortune, and the care use of 厄介 is not labor.` The author's reason: 厄 already excludes 苦, 困 and 難 for trouble
  and hardship, and 労's own title displays trouble. 苦労 is JMdict 1244680 (supplied in
  `evidence\jmdict-cited-entries.xml`); the article is supplied as `evidence\word-苦労.md`.
- `宙.md:14` and `:58-59`: 時 `time, hour` was added. The Daijisen 宇宙 bullet (lines 54-59; lines 54-57 unchanged) now
  ends `Because the source keeps that interval-of-time sense, 時 is still excluded from meaning choices.` The author's
  reason: the card keeps the classical account of 宙 as time extending from past to present, so a bare English time label
  is a defensible answer for that retained sense, as 覚 is already excluded for the by-heart sense (lines 51-53). The bullet's
  statement that 宙 is not the ordinary replacement for 時 in a clock time (line 57) is unchanged.
- `寸.md:45-46` (Readings section): `Daijisen records an ancient 寸 き separately; it is outside this metadata.` now reads
  `Daijisen separately records き, an ancient length-unit suffix written 寸; it is outside this metadata.` The author's
  reason: the old wording could be read as a bare reading of 寸. The author checked the Digital Daijisen entries on
  `https://www.weblio.jp/content/寸`: a separate heading き【▽寸】, marked ［接尾］ (suffix), whose first sense is an
  ancient length unit, and the character heading すん【寸】. That page is not supplied in this packet.
- `票.md:14` and `:56-58`: 署 `sign; government office` was added: `[署](署.md) displays *sign* for signing one's name, as
  in [署名](../words/署名.md). Because English *sign* is ambiguous, that pair is also excluded from meaning choices; a
  ballot is not a signature.` The author's reason: 票's card teaches a sign/label branch, and 署's title begins with an
  unqualified *sign*. Relabeling 署 instead would change an existing card, which is outside this batch. 署名 is JMdict
  1343640 (supplied); the article is supplied as `evidence\word-署名.md`.
- `魔.md:14` and `:58-60`: 怖 `frightening` was added: `JMdict also records 魔 before の with the sense dreaded or
  terrible. That overlaps [怖](怖.md), frightening, so the pair is excluded from meaning choices; it does not make every
  fear supernatural.` The author's reason: JMdict 1633990 (魔; supplied) has a separate sense marked as a noun that may
  take の, glossed dreaded, terrible, awful, dreadful, which makes frightening a defensible answer.
- `魔.md:68-70`: the 悪魔 bullet now attributes the religious senses to JMdict: `JMdict separately labels Christian and
  Buddhist senses of 悪魔; these are not a universal identity between religious figures.` (it read `Its separately
  labelled Christian and Buddhist dictionary senses are not a universal identity between religious figures.`). The
  author's reason: "Its" after the link to the 悪魔 article could be read as citing that article, which does not itself
  carry those labels; JMdict 1152510 (悪魔; supplied) has a Christianity sense (Satan) and a Buddhism sense (Māra).

# Author's statement for the reviewer of `reports-115\initial-gpt-coordinator-normalized.md`

This statement answers only the points in YOUR initial report. That file is your report with only the format of its
`- Citations:` lines normalized; no judgment, label or citation target differs from what you wrote. F1 to F6, O1 and L1
to L10 are your report's own labels. The statement is the author's claim about what changed and why. Verify each claim
against the revised card text in `snapshot\kanji\`, `diffs\fix.patch` and the evidence; do not rely on this text as
evidence. Line numbers refer to the revised cards in this packet. 6 of the 8 cards changed (卓 厄 宙 寸 票 魔); 康 and 漠
did not (see `CHANGES.md`). Give a disposition for each of F1 to F6 and O1. L1 to L10 need none; see the notes at the
end.

## Pair mechanics (applies to F1-F6)

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

### F1 (medium): 卓 is missing six direct excellence comparisons

Author action: **changed, as required: all six pairs are declared** (卓-偉, 卓-英, 卓-著, 卓-冠, 卓-凌, 卓-越).

- `卓.md:14` now reads `quiz_exclusions: [机, 台, 高, 優, 超, 表, 偉, 英, 著, 冠, 凌, 越]` (it read
  `[机, 台, 高, 優, 超, 表]`); the existing guards are kept.
- `卓.md:59-63` are a new Notes bullet after the unchanged 机/台/高/優/超 bullet (lines 56-58): `The eminence branch also
  overlaps [偉](偉.md), great, [英](英.md), outstanding, [著](著.md), remarkable, and [冠](冠.md), peerless. [凌](凌.md)
  and [越](越.md) share surpassing or exceeding with 超. These direct pairs are excluded from meaning choices; their
  Japanese words are not interchangeable with 卓越 or 卓抜.`

To verify: that the six pairs are declared and that the bullet presents them as choice protection, not as free
interchange of the Japanese words.

### F2 (medium): 厄 lacks the direct trouble comparison with 労

Author action: **changed, as required.**

- `厄.md:14` now reads `quiz_exclusions: [凶, 難, 困, 苦, 悪, 労]` (労 added; the existing exclusions are kept).
- `厄.md:58-61` are a new bullet between the 凶/難/困/苦 bullet and the JMdict *evil* bullet: `[労](労.md),
  labor/trouble, also displays trouble, as in [苦労](../words/苦労.md) くろう, hardship. That direct pair is excluded from
  meaning choices; work itself is not misfortune, and the care use of 厄介 is not labor.`
- 苦労 is JMdict 1244680 (supplied in `evidence\jmdict-cited-entries.xml`); the linked article is supplied as
  `evidence\word-苦労.md`.

To verify: that the pair is declared and that the bullet keeps misfortune, labor and the care use of 厄介 distinct.

### F3 (medium): 宙's retained time sense is not guarded against 時

Author action: **changed, as required, keeping the classical-versus-clock-time distinction.**

- `宙.md:14` now reads `quiz_exclusions: [宇, 空, 天, 気, 間, 覚, 時]` (時 added).
- `宙.md:54-59`: the Daijisen 宇宙 bullet keeps lines 54-57 unchanged, including `宙 is not the ordinary replacement for
  [時](時.md) in a clock time.`, and now ends `Because the source keeps that interval-of-time sense, 時 is still excluded
  from meaning choices.` (lines 58-59).

To verify: that the pair is declared, that the sourced temporal explanation is kept, and that the clock-time distinction
is not erased.

### F4 (medium): 寸 and 微 remain eligible together despite explicit smallness

Author action: **changed, as required (on 寸's side).**

- `寸.md:14` now reads `quiz_exclusions: [小, 少, 短, 細, 微, 計, 測]` (微 added after 細).
- `寸.md:59-61`: the smallness bullet now reads `[小](小.md), small, [少](少.md), a little, [短](短.md), short,
  [細](細.md), fine/small in detail, and [微](微.md), minute/tiny, overlap aspects of smallness.` "tiny" is the author's
  gloss of minute in the smallness sense, which 微's card explains; 微's title is `minute; faint`. The 細 phrase was only
  reflowed to make room. Lines 62-63 (計/測) and the unit explanation are unchanged.

To verify: that the pair is declared and the unit explanation and existing smallness exclusions are preserved.

### F5 (medium): 票's sign sense collides with the displayed English sign on 署

Author action: **changed: the direct exclusion was chosen.** 署's title is not changed; relabeling it would change an
existing card, which is outside this batch.

- `票.md:14` now reads `quiz_exclusions: [札, 券, 符, 標, 印, 署]` (署 added; the existing guards are kept).
- `票.md:56-58` are a new bullet after the 札/券/符/標/印 bullet: `[署](署.md) displays *sign* for signing one's name, as
  in [署名](../words/署名.md). Because English *sign* is ambiguous, that pair is also excluded from meaning choices; a
  ballot is not a signature.`
- 署名 is JMdict 1343640 (supplied); the linked article is supplied as `evidence\word-署名.md`.

To verify: that the pair is declared and the text keeps the Japanese distinction.

### F6 (medium): 魔's ordinary dreadful branch leaves 怖 as a defensible wrong answer

Author action: **changed, as required.**

- `魔.md:14` now reads `quiz_exclusions: [妖, 魅, 怪, 悪, 凶, 符, 怖]` (怖 added).
- `魔.md:58-60` are a new bullet after the 妖/魅/怪/悪/凶 bullet: `JMdict also records 魔 before の with the sense dreaded
  or terrible. That overlaps [怖](怖.md), frightening, so the pair is excluded from meaning choices; it does not make every
  fear supernatural.`
- The complete JMdict 1633990 (魔) entry is supplied in `evidence\jmdict-cited-entries.xml`; its third sense is marked as a
  noun that may take の and glossed dreaded, terrible, awful, dreadful.

To verify: that the pair is declared on that secondary sense and that no transitive fear or supernatural group is
implied.

## Optional

### O1: Make the source of the religious sense labels explicit

Author action: **changed, as suggested.** `魔.md:67-70`: the 悪魔 bullet keeps `The linked 悪魔 article distinguishes a
fictional being from a figurative description.` and now continues `JMdict separately labels Christian and Buddhist senses
of 悪魔; these are not a universal identity between religious figures.` (it read `Its separately labelled Christian and
Buddhist dictionary senses are not a universal identity between religious figures.`). JMdict 1152510 (悪魔) is supplied:
its Christianity sense is Satan and its Buddhism sense is Māra. The Metadata line, which already cited 1152510, is
unchanged, and the 悪魔 article is unchanged.

To answer: RESOLVED, PARTIALLY RESOLVED or NOT RESOLVED, with the reason.

## Limits

No action is claimed for these unless stated, and no disposition is needed. Notes:

- L1: no stroke file, Joyo row or asset changed in this revision.
- L2: acted on. `寸.md:45-46` (Readings section) now read `Daijisen separately records き, an ancient length-unit suffix
  written 寸; it is outside this metadata.` (it read `Daijisen records an ancient 寸 き separately; it is outside this
  metadata.`). The author checked the Digital Daijisen entries on `https://www.weblio.jp/content/寸`: a separate heading
  き【▽寸】, marked ［接尾］ (suffix), whose first sense is an ancient length unit, and the character heading すん【寸】.
  That page is not supplied in this packet. The selected reading スン is unchanged. Please review this hunk like any
  other changed hunk.
- L3 and L4: 康 is unchanged, and no existing exclusion target changed.
- L5: none of these candidates was added: 軽; 識 and 知; 強, 剛, 勁 and 力; 道, 路 and 通; nor any pair from the 微/漠, 薄/漠
  or 勝/抜 relations. Your report asserted no defect for them, and the author has no further lexical evidence to promote
  them.
- L6: the revision adds meaning-quiz exclusions only; no reading, reading selection or distractor changed.
  `checks\reading-exposure.txt` is byte-identical to the original packet's `checks\reading-exposure-final.txt`;
  `checks\reading-options.txt` is new in this round and was produced at the revised snapshot (0 problems). No Kotlin, JVM,
  native, phone or emulator execution occurred. Installed APK `5c000bd` predates `quiz_exclusions`, so none of the new
  pairs protects that build.
- L7: unchanged.
- L8: the checks in `checks\` were rerun at the revised snapshot. One correction concerns the logs you read: the original
  packet's `checks\lint.txt` reports `0 error(s), 0 warning(s)`, but that result cannot be reproduced from the reviewed
  snapshot. The same lint rerun at both the reviewed and the revised snapshot gives `0 error(s), 4 warning(s)`, all
  pre-existing and accepted as non-blocking. The frozen log is left unchanged and is not relied on. See "Lint" in
  `CHANGES.md`. Nothing in batch 115 is published; the stated published total is unchanged.
- L9 and L10: unchanged.

## Changes that do not answer a point in your report

None beyond the L2 sentence above. Every other changed hunk answers F1 to F6 or O1; `CHANGES.md` lists them all.

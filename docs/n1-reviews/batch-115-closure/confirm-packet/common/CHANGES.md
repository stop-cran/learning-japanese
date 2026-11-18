# Batch 115 revision: what changed from f36cd819 to 206f9893

Revised snapshot: `206f98936307a77937fb38346299af11044af761`, a child of the reviewed snapshot
`f36cd819dcf6ac8b4a3ee8ee29b6e750cd6f09ab`. Nothing in batch 115 is published.

## Binding

This packet is bound to the following exact bytes. Commands run in the repository, with no pager.

| Item | Value |
| --- | --- |
| Revised commit | `206f98936307a77937fb38346299af11044af761`, tree `9664f13167b56f55075230f2bdbb4af421fa834a`; single parent `f36cd819dcf6ac8b4a3ee8ee29b6e750cd6f09ab` (tree `c9b040e80919f12ca1f071a24d0eb51ed7e8ed35`) |
| Commit object | `git cat-file commit 206f98936307a77937fb38346299af11044af761`: 3,776 bytes, SHA-256 `c634f1bd5bc4a8fc774db6e76d210d036eff4c7b85eb9dc84a681c0dcb0e8a9e` |
| Full diff | `git -c core.quotepath=false diff --binary f36cd819 206f9893`: 12,534 bytes, SHA-256 `4c016f3544ef8ace083b0eb4753b8ec4b12ca80131e61397f4f5a0225b594bda` (7 files, including `manifest.json`) |
| `diffs\fix.patch` | `git -c core.quotepath=false diff --no-color f36cd819 206f9893 -- . ":(exclude)manifest.json"`: 7,772 bytes, SHA-256 `eedd3585d6860f0011c48be42931453ab85d74ce834efe90d76aa4ccbb681ba6` |

## What changed

- 6 of the 8 kanji cards changed: 卓, 厄, 宙, 寸, 票 and 魔. The other two (康 and 漠) are unchanged, and so are all 8
  stroke files, all titles, all `distractors`, all reading rows and selections, and every word article.
- Front matter changed only in `quiz_exclusions` (line 14) of the six changed cards. Each list only gained entries; none
  was removed. Eleven direct pairs were added in total.
- Body text changed in Notes bullets of all six cards, and in one Readings-section sentence of 寸 (lines 45-46). No
  Meaning line, reading row, Common words row or Metadata line changed.
- No existing card outside the batch changed. Every pair added in this revision is declared on the batch card's side.
- `manifest.json` was regenerated (contentVersion `8a1b246322fb62d9`; it was `8c5b266340bd34bc`); it is a generated index
  and outside the review.
- Line numbers below refer to `snapshot\kanji\<card>.md` in this packet (the revised snapshot).
- `diffs\fix.patch` is the exact patch. `diffs\changed-lines.txt` lists the changed lines per file.
- Links: `checks\link-targets.tsv` lists every link on a changed line. The new links are followed by unquoted descriptive
  phrases, not quoted titles, so the table's title comparison shows `n/a` for them. The author compared each phrase with
  the linked card's real `title:`: 偉 "great" (title `admirable; great`), 英 "outstanding" (`English; outstanding`), 著
  "remarkable" (`write; remarkable`), 冠 "peerless" (`crown; peerless`), 労 "labor/trouble" (`labor; trouble`), 微
  "minute/tiny" (`minute; faint`; "tiny" is the author's gloss of minute, not part of the title), 署 "*sign*"
  (`sign; government office`) and 怖 "frightening" (`frightening`). 凌 (`endure; surpass`) and 越 (`cross over; exceed`)
  are linked without a phrase; the sentence says they share surpassing or exceeding with 超.
- Two new links go to word articles: `../words/苦労.md` (title `hardship; trouble`; the phrase after it is "hardship") and
  `../words/署名.md` (title `signature; signing`). Both articles exist, unchanged, at the revised snapshot and at the
  base; they were not in the original packet, so their full text is supplied as `evidence\word-苦労.md` and
  `evidence\word-署名.md`.
- `checks\quiz-safety.txt`, `checks\reading-exposure.txt` and `checks\linkplan.txt` are byte-identical to the original
  packet's `checks\quiz-safety.txt`, `checks\reading-exposure-final.txt` and `checks\linkplan.txt`: no curated wrong option,
  modelled reading draw or word-article link changed. `checks\reading-options.txt` is new in this round; it was produced at
  the revised snapshot (0 problems). `checks\validate.txt` and `checks\vocabulary.txt` also equal the original packet's.
- New evidence in this packet is everything under `evidence\` (see `evidence\README.md`): the complete JMdict entries cited
  by the new text or by the author's statement, the app's `QuizBuilder.kt`, the two word articles above, and the lint
  evidence described below. No Joyo page or KanjiVG record is supplied, because no reading metadata or stroke file
  changed. All other evidence stays in the original packet.

## Lint

Lint is accepted as non-blocking for this revision. The facts:

- `checks\lint.txt` is the batch lint (`lean\n1_batch_tool.py lint`, base `origin/main` = `c7a7c8a7`) rerun at the
  revised snapshot: `kanji checked: 9, words checked: 12`, `0 error(s), 4 warning(s)`. All four warnings are
  `Dictionary: line cites no JMdict entry id`, in the word articles 寸法, 標本, 標準 and 標識.
- These four warnings are pre-existing. None of the four articles changed in this revision, and the same command rerun at
  the reviewed snapshot f36cd819 gives byte-identical output (`evidence\lint-rerun-f36cd819.txt`). The warned
  `Dictionary:` lines are also identical at the base c7a7c8a7; of the four articles, the reviewed snapshot edited only
  寸法, and only its line 29 (a link to 寸).
- The original packet's `checks\lint.txt` reports `0 error(s), 0 warning(s)` for the same scope. That zero-warning result
  cannot be reproduced from the reviewed snapshot, and its cause has not been established. The frozen log is left
  unchanged and is not relied on.
- Basis for treating them as warnings (author's statement; the tool is not in this packet): the lint covers the 8 batch
  cards plus 標, whose card the reviewed snapshot also edited, and 12 word articles: the 8 the reviewed snapshot edited
  and the other articles that declare one of those 9 kanji. The rule reads only the first physical `Dictionary:` line. It
  is an error only for files added since the base; all four articles existed at the base, so it is reported as a warning.
  In each of them the JMdict entry id sits on the wrapped continuation of the `Dictionary:` line: 寸法 1373810, 標本
  1488820, 標準 1488710, 標識 1488700 (`evidence\lint-warning-basis.txt`).

## Per card

| Card | Changed lines | Change |
| --- | --- | --- |
| 卓 | 14, 59-63 | Line 14 gains 偉, 英, 著, 冠, 凌 and 越 at the end: `[机, 台, 高, 優, 超, 表, 偉, 英, 著, 冠, 凌, 越]` (it read `[机, 台, 高, 優, 超, 表]`). Lines 59-63 are a new Notes bullet after the 机/台/高/優/超 bullet: `The eminence branch also overlaps [偉](偉.md), great, [英](英.md), outstanding, [著](著.md), remarkable, and [冠](冠.md), peerless. [凌](凌.md) and [越](越.md) share surpassing or exceeding with 超. These direct pairs are excluded from meaning choices; their Japanese words are not interchangeable with 卓越 or 卓抜.` |
| 厄 | 14, 58-61 | Line 14 gains 労: `[凶, 難, 困, 苦, 悪, 労]` (it read `[凶, 難, 困, 苦, 悪]`). Lines 58-61 are a new bullet after the 凶/難/困/苦 bullet and before the JMdict *evil* bullet: `[労](労.md), labor/trouble, also displays trouble, as in [苦労](../words/苦労.md) くろう, hardship. That direct pair is excluded from meaning choices; work itself is not misfortune, and the care use of 厄介 is not labor.` |
| 宙 | 14, 58-59 | Line 14 gains 時: `[宇, 空, 天, 気, 間, 覚, 時]` (it read `[宇, 空, 天, 気, 間, 覚]`). Lines 58-59 extend the Daijisen 宇宙 bullet (lines 54-59), whose lines 54-57 are unchanged: `Because the source keeps that interval-of-time sense, 時 is still excluded from meaning choices.` |
| 寸 | 14, 45-46, 59-61 | Line 14 gains 微 after 細: `[小, 少, 短, 細, 微, 計, 測]` (it read `[小, 少, 短, 細, 計, 測]`). Lines 45-46 (Readings section) now read `Daijisen separately records き, an ancient length-unit suffix written 寸; it is outside this metadata.` (it read `Daijisen records an ancient 寸 き separately; it is outside this metadata.`). Lines 59-61: the smallness bullet now reads `[小](小.md), small, [少](少.md), a little, [短](短.md), short, [細](細.md), fine/small in detail, and [微](微.md), minute/tiny, overlap aspects of smallness.` (it ended `[短](短.md), short, and [細](細.md), fine/small in detail, overlap aspects of smallness.`); lines 62-63 are unchanged. |
| 票 | 14, 56-58 | Line 14 gains 署: `[札, 券, 符, 標, 印, 署]` (it read `[札, 券, 符, 標, 印]`). Lines 56-58 are a new bullet after the 札/券/符/標/印 bullet: `[署](署.md) displays *sign* for signing one's name, as in [署名](../words/署名.md). Because English *sign* is ambiguous, that pair is also excluded from meaning choices; a ballot is not a signature.` |
| 魔 | 14, 58-60, 68-70 | Line 14 gains 怖: `[妖, 魅, 怪, 悪, 凶, 符, 怖]` (it read `[妖, 魅, 怪, 悪, 凶, 符]`). Lines 58-60 are a new bullet after the 妖/魅/怪/悪/凶 bullet: `JMdict also records 魔 before の with the sense dreaded or terrible. That overlaps [怖](怖.md), frightening, so the pair is excluded from meaning choices; it does not make every fear supernatural.` Lines 68-70: the 悪魔 bullet keeps line 67 and now continues `figurative description. JMdict separately labels Christian and Buddhist senses of 悪魔; these are not a universal identity between religious figures.` (it read `figurative description. Its separately labelled Christian and Buddhist dictionary senses are not a universal identity between religious figures.`). |

# Author's statement for the reviewer of `reports-140\initial-gpt.md`

This statement answers only the points in YOUR initial report. G1 and G2 are your report's own Findings labels.
Optional 1, 2 and 3 are the three bullets under "Optional:" in your report, in their order there (幣's 中/内/南 set;
弁護士; 徐ろに). The statement is the author's claim about what changed and why. Verify each claim against the revised
text in `snapshot\`, `diffs\fix.patch` and independent sources; do not rely on this text as evidence. Card line numbers
refer to the revised cards in this packet; other line numbers refer to the named file in this packet unless the
original packet is named. Eight of the 15 cards changed (帳 幕 幣 弁 径 徐 従 徴), the other seven did not, and no word
article or stroke file changed (see `CHANGES.md`). Give a disposition for each of G1, G2 and Optional 1 to 3.

## Findings

### G1 (minor): 幕 and 徐 — paraphrases in quotation marks

Author action: **changed** as you proposed (quotation marks removed; no reading, exclusion or title changed).

- `幕.md:62` now reads `… overlap the senses "act of a play" and "end; close" that 幕 and its word carry, and the
  covering-cloth sense in the Daijisen entry; 末 appears with 幕 in 幕末.` (it read `overlap the senses "act of a
  play," "covering cloth" and "end; close" that 幕 and its word carry;`). The two quoted strings left are source-real:
  "act of a play" is part of 幕's own title, `curtain; act of a play; shogunate`, and "end; close" is sense 4 of JMdict
  1524750.
- `徐.md:48` now reads `… overlap the slow, unhurried sense that 徐 carries.` (it read `overlap the sense "slow,
  unhurried" that 徐 carries.`).
- Support: `evidence\jmdict-cited-entries.xml` or the original packet's `evidence\jmdict-families.xml`, entry 1524750;
  `checks\link-targets.tsv` for 幕's title.

### G2 (minor): 弁 and 従 — sense catalogues before the Readings table

Author action: **changed** as you proposed (compressed, remainder moved to reference bullets in the Notes).

- `弁.md:25`: the eleven-bullet list of Daijisen senses (old lines 25 to 39) is replaced by one paragraph that groups
  the main senses with their examples: 弁償, 駅弁, 弁解, 東北弁, 花弁, 安全弁, plus 弁護士 (Optional 2) and the note on
  the old forms 辨, 辯 and 瓣. The full list of eleven senses with their remaining examples is a new reference bullet at
  `弁.md:55`, after the core teaching.
- `従.md:25`: the six ジュウ bullets and the ショウ and ジュ paragraph (old lines 25 to 34) are replaced by one paragraph
  with 服従, 従事, 従来, 追従, 従三位 and the noun じゅう. The other examples (従軍, 主従, 従弟, 合従, 従容), the kun
  readings したがう, したがえる and より, and the archaic prefix ひろい move to a new reference bullet at `従.md:56`.
- No reading row, linked word, example or qualification is removed: the old forms, the whole-word readings and the
  statements of what is not quizzed are all still on the cards. `diffs\fix.patch` shows every removed line and where its
  content went.
- Words before the Readings heading, counted as you did (whitespace-separated, from after the front matter): 弁 378 →
  341 and 従 455 → 342. For comparison, 幕 has 343 and 帳 294 in this batch, and the published cards 属, 寂 and 宜 have
  354, 322 and 303 (their files are in the original packet's `repo\kanji\`).
- Line counts: 弁 73 → 60 and 従 69 → 61.

## Optional points

| ID | Author action | Where | Reason |
| --- | --- | --- | --- |
| Optional 1 | **changed** | `幣.md:13`, `:53` | `distractors: [中, 南, 雨]` (it was `[中, 内, 南]`). 内, whose title "within, inner" overlapped 中's "middle, inside," is replaced by 雨, "rain," which has a vertical stroke from its top bar through the middle of 冂 (stroke 4 in `evidence\雨.json`). Following your caution, the reading side was kept collision-free: the closer look-alikes 常, 帯 and 希 are not Starter cards, and with them a short Starter practice session that borrows 幣 would use the fallback for the ヘイ question and could offer まい, an archaic reading of 幣 (JMdict 2789910). An unreviewed local version that used them showed exactly this (`evidence\superseded-775debde.txt`, the line labelled `78:`, `PAD-HIT`). 中, 南 and 雨 are all Starter cards; `checks\reading-exposure.txt` (幣 block) shows the curated options filling every slot in every pool, with no hit. Line 53 describes 中, 雨 and 南, and still names 常, 帯 and 希 as having the same 巾 at the bottom. |
| Optional 2 | **changed** | `弁.md:25`, `:58` | 弁護士 べんごし, `which JMdict glosses "lawyer; attorney."`, is in the new sense paragraph; JMdict 1512850 is added to the Metadata line. Support: `evidence\jmdict-cited-entries.xml`, entry 1512850. |
| Optional 3 | **changed** | `徐.md:36` | The sentence on 徐ろに now ends `the spelling that KANJIDIC2's おもむ.ろに reflects, with ろに as okurigana.` |

## Limits in your report

No disposition is needed. The Android JVM content tests and the Kotlin reading-audit cross-check were not run for this
revision either (see `CHANGES.md`). The four lint warnings on 往復, 従姉妹, 直径 and 通帳 are unchanged.

## Changes that do not answer a point in your report

They are listed in `CHANGES.md`; review them like any other changed hunk.

- **徴 and 署** (`徴.md:14`, `:56`): 署, "sign; government office," is added to 徴's quiz_exclusions, because English
  "sign" covers both 徴's indication sense and 署's signing sense; the Notes line now says it is kept out of the quiz
  options (it said 署 `remains an ordinary wrong option for 徴`).
- **帳 and 幕** (`帳.md:14`, `:50`; `幕.md:60`): 幕 is added to 帳's quiz_exclusions for the shared hanging-curtain sense
  (exclusions apply to the pair in both directions, `evidence\QuizBuilder.kt`). Both Notes lines say the two are kept
  out of each other's quiz options.
- **弁's title** (`弁.md:3`, `:17`): `speech; discern; valve; bento` (it was `speech; discern; valve`); "bento" is the
  sense of both linked words, 弁当 and お弁当. No other card quotes the old title.
- **径's path example** (`径.md:28`, `:60`): the sense "a small path or a shortcut" is now illustrated by 小径 しょうけい,
  "path; lane," which JMdict (2859605) marks formal or literary; 径庭, "great difference," moves to the end of the
  reference bullet.
- **幣's other readings** (`幣.md:31`, `:57`): line 31 now also names ぜに, which Kanjipedia lists, and にきて, a Daijisen
  headword that can be written 幣, and says neither is in KANJIDIC2 or JMdict. Its first sentence now ties ぬさ and
  みてぐら to the Daijisen character entry. JMdict 2175880 (銭 ぜに) is added to the Metadata line. Your report found the
  omission not to be a defect; this adds the readings without changing any quiz behaviour (the reading audits already
  counted both as attested for 幣).

## Process notes

- `1b24a5f9` is the only fix commit; `diffs\fix.patch` is the whole change from the reviewed snapshot `28831314`. Two
  earlier local versions of it, `775debde` and `88ab6f48`, were replaced before this packet was built; neither was
  reviewed or published. Both differed only in 幣. `775debde` had the distractors `[常, 帯, 希]`, which produced the
  Starter-session `PAD-HIT` described under Optional 1 (`evidence\superseded-775debde.txt`); `88ab6f48` had the final
  distractors but not yet the change to line 31.
- The checks in `checks\` were run on the committed revision.

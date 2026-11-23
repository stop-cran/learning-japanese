# Batch 152 revision: what changed from cdd8fd01 to b81299f3

Revised snapshot: `b81299f3` (full hash `b81299f38d9d5184b94f7c05e6355ca7de085466`; also in `packet-manifest.json`). It is one
commit after the reviewed snapshot `cdd8fd016161d54a3d21cbf46450a6219f5bbedb`. Nothing is published.

- Eight of the 15 new kanji cards changed (跳 踏 載 輝 迫 遂 遣 避). 趣 躍 較 輩 逸 郡 郷, every existing kanji card (including the
  four remark edits on 仮, 故 and 響), every stroke file and every word article are unchanged.
- **Front-matter changes:** only `quiz_exclusions` (line 14 of seven cards) gained entries; nothing was removed:
  - 跳: `[飛, 踊, 弾]` (弾 added).
  - 踏: `[歩, 履, 執, 施, 遂]` (執 施 遂 added).
  - 載: `[乗, 刊, 掲, 記, 録, 書, 積, 年, 荷, 置, 駄, 運]` (運 added).
  - 輝: `[光, 照, 射, 艶, 華]` (艶 華 added).
  - 迫: `[寄, 近, 圧, 促, 督, 詰, 追, 押]` (押 added).
  - 遂: `[完, 了, 終, 卒, 果, 達, 到, 至, 成, 執, 施, 履]` (執 施 履 added).
  - 避: `[逃, 防, 除, 免, 脱]` (脱 added).
  No title, tag, `distractors` list, metadata reading, `quizOnyomi` or `quizKunyomi` changed in any card. No existing card's
  front matter changed; each new pair is declared once, on the new card.
- `manifest.json` was regenerated; it is a generated index and outside the review.
- Line numbers below refer to the revised snapshot in this packet. Six cards gained lines, so their later lines moved down: 跳 +1
  from line 50, 踏 +2 from line 49, 輝 +2 from line 49, 迫 +1 from line 50, 遂 +1 from line 54 and 避 +1 from line 52. 載 and 遣
  kept their line numbers. `diffs\fix.patch` is the exact patch from `cdd8fd01` to `b81299f3`; `diffs\changed-lines.txt` lists the
  changed lines per file.
- New evidence in this packet is everything under `evidence\`; `evidence\README.md` describes each file. The original packet's
  `evidence\audits\` files (quiz safety, reading exposure, reading options) describe the reviewed snapshot and are superseded by this
  packet's `checks\`.

## Changed lines

| File | Changed lines | Change |
| --- | --- | --- |
| 跳 | 14, 46, 50, 56 | 14: 弾 excluded. 46: "These three cards". 50 (new): "[弾](弾.md) (“bullet; play strings; bounce”): JMdict's first sense of 弾む はずむ is “to spring; to bound; to bounce” (entry 1419400), close to 跳ねる's “to spring up; to bound; to hop”." 56: JMdict entry 1419400 added to the Metadata ids. |
| 踏 | 14, 45, 49, 50, 54 | 14: 執 施 遂 excluded. 45: "These five cards". 49 (new): 執 (“take hold; carry out; cling”) and 施 (“carry out; give; alms”): "both titles include “carry out”, which matches Kanjipedia's ふみ行う and KANJIDIC2's “carry through” for 踏." 50 (new): 遂 (“accomplish; at last”): "KANJIDIC2 lists “carry through” for 踏 and “accomplish” for 遂; JMdict 踏む sense 4 ends “to complete”, and JMdict 遂げる とげる begins “to accomplish; to achieve; to carry out” (entry 1372620)." 54: entry 1372620 added to the Metadata ids. |
| 載 | 14, 45, 50 | 14: 運 excluded. 45: "These twelve cards". 50: 運 (“carry; luck”) joins the existing 積/荷 bullet, whose evidence is unchanged: Kanjipedia's first sense of 載 includes 車や船に積む。, JMdict 積載 “loading; carrying” (entry 1383040), and JMdict entry 1600270 sense 3 “to load (luggage); to carry; to take on board”. |
| 輝 | 14, 44, 49, 50, 54 | 14: 艶 華 excluded. 44: "These five cards". 49 (new): 艶 (“gloss; luster; allure”): "JMdict's first sense of 艶 つや is “gloss; luster; lustre; shine; sheen; polish” (entry 1177680)." 50 (new): 華 (“flower; splendor; showiness”): "KANJIDIC2 lists “shine” and “luster” for 華 as well as “shine” for 輝, and JMdict's 光輝 gloss includes “splendor”." 54: entry 1177680 added to the Metadata ids (光輝, entry 1272940, was already cited). |
| 迫 | 14, 44, 50, 54 | 14: 押 excluded. 44: "These eight cards". 50 (new): 押 (“push”): "JMdict 押す sense 5 is “to push (someone for something); to press; to put pressure on (someone)” (entry 1180470), close to 迫る sense 2 and to this card's “press”." 54: entry 1180470 added to the Metadata ids. |
| 遂 | 14, 46, 54 | 14: 執 施 履 excluded. 46: "These twelve cards". 54 (new): 執, 施 and 履 (“footwear; put on shoes; carry out”): "each title includes “carry out”, which is in JMdict's first sense of 遂げる, “to accomplish; to achieve; to carry out” (entry 1372620)." Entry 1372620 was already in the Metadata ids. |
| 遣 | 33, 63 | 33: the -つか.い example row is now "蛇遣い へびつかい — snake charmer; JMdict entry 1753470 also spells it 蛇使い. Not selected for questions here." (was 人形遣い にんぎょうつかい, entry 1367140). 63: Metadata id 1367140 replaced by 1753470. |
| 避 | 14, 46, 52, 56 | 14: 脱 excluded. 46: "These five cards". 52 (new): 脱 (“undress; remove; escape”): "Kanjipedia gives のがれる (escape) for 避, KANJIDIC2 gives 脱 “escape from”, and JMdict glosses 脱税 だつぜい “tax evasion” (entry 1416550)." 56: entry 1416550 added to the Metadata ids. |

## Checks run on the revised snapshot (outputs in `checks\`)

- `lint.txt`: 0 errors, 7 warnings (legacy word articles whose Dictionary line cites no JMdict entry id), as at the freeze.
  `unittest.txt`: 439 tests, OK. `validate.txt`: 0 errors. `manifest.txt`: rebuilding `manifest.json` leaves it unchanged and the
  tree clean. `budget.txt` and `vocabulary.txt`: informational.
- `linkplan.txt`: 20 changed word files, 20 added link pairs, 0 problems, as at the freeze.
- `kanji-remarks.txt`: 15 new cards, 3 modified existing cards, 4 declared remark edits applied, 0 problems, as at the freeze.
- `quiz-safety.txt`: 0 errors, 0 warnings; identical to the freeze apart from the command line. The curated distractors still fill
  every wrong meaning slot of the seven cards whose exclusions grew, and none of the newly excluded cards is a curated distractor of
  any batch card.
- `reading-exposure.txt`: 0 production hits, 0 padded-session hits, the same 20 latent collisions and 0 one-holder hits (plus the
  same 2 KANJIDIC2 name-only one-holder cases, 載 のり and 輝 ひかる); identical to the freeze apart from the command line.
- `reading-options.txt`: identical to the freeze apart from the command line, including its 1 problem (迫 せる offered by 競), which
  the freeze packet's audits already showed is masked by 迫's curated 出 入 休 in every pool the app builds.
- The Android JVM tests that read the real content were not run, as at the freeze (no JDK on this machine).

## Process notes

- `b81299f3` is the single fix commit; `diffs\fix.patch` is the whole change from the reviewed snapshot `cdd8fd01`.
- The checks in `checks\` were run on the committed revision `b81299f3`.

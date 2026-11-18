# Author's statement for the reviewer of `reports-140\initial-claude.md`

This statement answers only the points in YOUR initial report. C1 to C3 are your report's own Findings labels, and O1 to
O5 are your Optional labels. The statement is the author's claim about what changed and why. Verify each claim against
the revised text in `snapshot\`, `diffs\fix.patch` and independent sources; do not rely on this text as evidence. Card
line numbers refer to the revised cards in this packet; other line numbers refer to the named file in this packet unless
the original packet is named. Eight of the 15 cards changed (帳 幕 幣 弁 径 徐 従 徴), the other seven did not, and no
word article or stroke file changed (see `CHANGES.md`). Give a disposition for each of C1 to C3 and O1 to O5.

## Findings

### C1 (minor): 幣 — distractors

Author action: **changed**, but not to the look-alikes you proposed.

- `幣.md:13`: `distractors: [中, 南, 雨]` (it was `[中, 内, 南]`). 内, "within, inner," whose label overlapped 中's
  "middle, inside," is replaced by 雨, "rain." 中, "middle, inside," 南, "south," and 雨, "rain," do not overlap each
  other or 幣's title, `currency; Shinto offering`.
- `幣.md:53` now reads `[中](中.md), "middle, inside," has a vertical stroke running through a box, much as 巾 at the
  bottom of 幣 has a vertical stroke running through the open frame 冂. [雨](雨.md), "rain," has a vertical stroke
  running down from its top bar through the middle of 冂, and [南](南.md), "south," is also built on 冂. [常](常.md),
  "usual; constant," [帯](帯.md), "sash; zone," and [希](希.md), "hope; rare," have the same 巾 at the bottom with a
  different upper part. All are different kanji.`
- Why not 常, 帯 and 希: none of them is a Starter card, and 中, 内 and 南 all were. A short Starter "Practice more"
  session can borrow 幣; its pool is then the 118 Starter cards plus 幣. With 常, 帯 and 希 as distractors, no curated
  option is in that pool, so the fallback fills all three wrong slots of the ヘイ question, and it can offer まい from
  埋, 妹, 枚, 毎 or 米. まい is an archaic reading of 幣 itself (JMdict 2789910, which the card names at line 31). The
  author made that change first, in a version that was never reviewed (see Process notes); its audit is in
  `evidence\superseded-775debde.txt`, the line labelled `78:`, `PAD-HIT`. 中, 南 and 雨 are all Starter cards, so the curated options
  fill every slot in every pool.
- Support: `checks\reading-exposure.txt`, the 幣 block (Starter practice session: `curated 中 南 雨`; no `PAD-HIT` line)
  and its summary line (0 production hits, 0 padded-session hits); `checks\quiz-safety.txt` for the meaning options;
  `checks\link-targets.tsv` for the titles of 中, 雨, 南, 常, 帯 and 希; `evidence\雨.json`, the repository's KanjiVG
  stroke data for 雨 (stroke 4 runs from (52.2, 23.5), just under the top bar, stroke 1, down to (53.5, 87.3), through
  the middle of the frame drawn by strokes 2 and 3).

### C2 (minor): 徴 and 署

Author action: **changed** as you proposed (the exclusion, not the retitle).

- `徴.md:14`: `quiz_exclusions: [兆, 符, 印, 標, 症, 収, 採, 税, 召, 募, 署]` (署 added).
- `徴.md:56` now ends `English "sign" covers both ideas, so [署](署.md), "sign; government office," is also kept out of
  this card's quiz options.` (it ended `remains an ordinary wrong option for 徴.`). The title stays `sign; indication;
  levy`.
- Support: `evidence\QuizBuilder.kt` (exclusions apply to the pair in both directions); `checks\quiz-safety.txt`.

### C3 (minor): 帳 and 幕

Author action: **changed** (one side, as you noted is enough).

- `帳.md:14`: `quiz_exclusions: [録, 籍, 記, 誌, 冊, 本, 巻, 幕]` (幕 added).
- `帳.md:50` now ends `this card's title keeps to the book sense, and 幕 is also kept out of this card's quiz
  options.`
- `幕.md:60` now ends `also has a hanging-curtain sense and is the usual spelling of とばり, so the two are kept out of
  each other's quiz options.` `幕.md:14` is unchanged.
- Support: `evidence\QuizBuilder.kt`; `checks\quiz-safety.txt`.

## Optional points

| ID | Author action | Where | Reason |
| --- | --- | --- | --- |
| O1 | **changed** | `径.md:28`, `:60` | Line 28 now reads `a small path or a shortcut: 小径 しょうけい, "path; lane," which JMdict marks formal or literary;` (it used 径庭 けいてい, "great difference"). 径庭 moves to the end of the reference bullet at line 60: `… 捷径 しょうけい, "shortcut; expedient," and 径庭 けいてい, "great difference," also written 逕庭.` JMdict 2859605 (小径) was already on the Metadata line. Support: `evidence\jmdict-cited-entries.xml`, entry 2859605 (sense 1 "path; lane", formal or literary term). |
| O2 | **changed** | `幣.md:31`, `:57` | Line 31 now adds `Two more readings are in neither KANJIDIC2 nor JMdict: [Kanjipedia's character entry](https://www.kanjipedia.jp/kanji/0006218900) also lists ぜに, a word for money that JMdict writes 銭, and another Daijisen headword reads 幣 as にきて, cloth hung on a sakaki branch as an offering to the gods, also written 和幣 or 幣帛.` Its first sentence now says `Its kun readings in that entry are ぬさ and みてぐら`, which ties them to the Daijisen character entry named at line 25, since Kanjipedia also lists ぜに as a kun reading. The Metadata line (57) adds JMdict 2175880 (銭 ぜに). Support: the original packet's `evidence\kanjipedia-outside-readings.json` (幣: kun ぜに, ぬさ, みてぐら) and `evidence\daijisen-heads.txt` (にき‐て【▽和▽幣／幣＝帛／▽幣】); `evidence\jmdict-cited-entries.xml`, entry 2175880. The quiz audits already counted both readings as attested for 幣 (`checks\reading-exposure.txt`, the 幣 block), and no card offers either. |
| O3 | **no change** | `幕.md:13` | 墓, 暮 and 募 are the look-alikes that share 莫, and they serve the meaning question in full. For the マク reading question the fallback fills two slots, and `checks\reading-exposure.txt` (the 幕 block) finds no hit and no latent collision for 幕 in any pool. |
| O4 | **changed** | `弁.md:3`, `:17` | Title and heading: `speech; discern; valve; bento` (it was `speech; discern; valve`). Four-part titles are used on published cards, for example `筋` and `納` in the original packet's `repo\kanji\`. No other card quotes the old title. `checks\quiz-safety.txt` has no new warning for 弁. |
| O5 | **no change** | `怠.md:13`, `:49` | 治, "govern; heal," is a look-alike with 台 at the right. The sense you mention belongs to the word 怠る, and the card labels it dated (`怠.md:23`). It is not part of 怠's title, `neglect; be lazy`, so "govern; heal" remains a wrong answer to the meaning question, as you found. |

## Limits in your report

No disposition is needed. The Android JVM content tests and the Kotlin reading-audit cross-check were not run for this
revision either (see `CHANGES.md`). The four lint warnings on 往復, 従姉妹, 直径 and 通帳 are unchanged.

## Changes that do not answer a point in your report

They are listed in `CHANGES.md`; review them like any other changed hunk.

- **幕 and 徐: quotation marks** (`幕.md:62`, `徐.md:48`). Two explanatory paraphrases are no longer set in quotation
  marks as if they were source glosses. 幕 line 62 now says the exclusions `overlap the senses "act of a play" and "end;
  close" that 幕 and its word carry, and the covering-cloth sense in the Daijisen entry`; 徐 line 48 now says they
  `overlap the slow, unhurried sense that 徐 carries`. "act of a play" is part of 幕's own title, and "end; close" is
  sense 4 of JMdict 1524750 (幕).
- **弁 and 従: shorter sense lists before the Readings section** (`弁.md:25`, `:55`, `:58`; `従.md:25`, `:56`). The
  eleven-bullet list of 弁's Daijisen senses and 従's six ジュウ bullets with the ショウ and ジュ paragraph are each
  compressed into one paragraph with the main examples. The full sense lists, 従's kun readings and the archaic prefix
  ひろい move to new "For reference" bullets in the Notes (`弁.md:55`, `従.md:56`). No reading row, word, example or
  qualification is removed. 弁 line 25 adds 弁護士 べんごし, `which JMdict glosses "lawyer; attorney."`, and line 58
  (Metadata) adds entry 1512850. Support: `evidence\jmdict-cited-entries.xml`, entry 1512850.
- **徐: おもむ.ろに** (`徐.md:36`). The sentence on 徐ろに now adds `the spelling that KANJIDIC2's おもむ.ろに reflects,
  with ろに as okurigana.`

## Process notes

- `1b24a5f9` is the only fix commit; `diffs\fix.patch` is the whole change from the reviewed snapshot `28831314`. Two
  earlier local versions of it, `775debde` and `88ab6f48`, were replaced before this packet was built; neither was
  reviewed or published. Both differed only in 幣. `775debde` had the distractors `[常, 帯, 希]`, which produced the
  Starter-session `PAD-HIT` described under C1 (`evidence\superseded-775debde.txt`); `88ab6f48` had the final
  distractors but not yet the O2 change.
- The checks in `checks\` were run on the committed revision.

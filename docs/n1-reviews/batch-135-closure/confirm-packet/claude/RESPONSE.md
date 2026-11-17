# Author's statement for the reviewer of `reports-135\initial-claude.md`

This statement answers only the points in YOUR initial report. IDs C1 and C2 are your report's own Findings labels, and
O1 to O5 are your Optional labels. The statement is the author's claim about what changed and why. Verify each claim
against the revised card text in `snapshot\kanji\`, `diffs\fix.patch` and independent sources; do not rely on this text
as evidence. Line numbers refer to the revised cards in this packet. Nine of the 15 cards changed (博 履 巡 弾 恵 憶 揚 救
模) and the other six did not (see `CHANGES.md`). Give a disposition for each of C1, C2, O1, O2, O3, O4 and O5.

## Findings

### C1 (minor): 博 mnemonic misstates the right-hand component

Author action: **changed.**

- `博.md:27` now reads `At the right is 甫, which has no card here, standing over [寸](寸.md), "sun (length unit); small";
  the dot at the top right is part of 甫 itself.` The phrase `a shape like 甫 with an extra dot` is gone. The rest of the
  paragraph, including the modern-shape disclaimer, is unchanged.
- Your optional addition (the same right-hand part as 薄 under 艹) was not repeated in the mnemonic, because `博.md:48`
  already says it.
- Support: KANJIDIC2 gives 甫 7 strokes (`evidence\kanjidic2-甫.xml`, line 20). In `evidence\kanjivg\0535a.svg`, the
  right-hand group 尃 (line 44) holds 甫 (lines 45-59: strokes 3 to 9, the dot being stroke 9 at lines 56-57) over 寸
  (lines 61-65: strokes 10 to 12). 十 2 + 甫 7 + 寸 3 = 12, the card's `strokes: 12`. `evidence\kanjivg\0752b.svg` is 甫
  alone (7 paths).
- Disclosure: KanjiVG marks this 甫 `kvg:variant="true"`, marks 尃 `kvg:phon="尃"` and also tags strokes 3 to 8 (甫
  without its dot) and 寸 as parts 1 and 2 of 専 (lines 46 and 60). The card names only the visible shapes and still
  makes no claim about formation or sound.

To verify: that line 27 now describes the shape accurately, and that nothing else on the card still implies an extra
stroke.

### C2 (minor): 憶 presents 臆測 as a rare spelling without the Joyo table's counterweight

Author action: **changed.** The JMdict sentence is kept and the Joyo table's treatment is added, with one difference from
your remedy: the card does not say that both spellings are "in ordinary use", because no source in either packet measures
usage. It reports what the table says.

- `憶.md:25` now ends: `JMdict also lists 臆説 and 臆念 as spellings of 憶説 and 憶念, and 臆測 as a rarely used spelling
  of 憶測. The official Joyo table, however, gives 臆, which does not have a kanji card here, its own row, with オク and the
  examples 臆説, 臆測 and 臆病 おくびょう, "cowardly; timid; easily frightened," and notes that 臆説 and 臆測 are also
  written 憶説 and 憶測, so the table accepts both spellings.` (It ended `...a rarely used spelling of 憶測; 臆 does not
  have a kanji card here.`)
- `憶.md:49`: JMdict entry 1182790 (臆病) is added to the Metadata entry list.
- Support: `evidence\joyo\p18.txt` lines 45-47 (臆, `オク 臆説，臆測，臆病`, and the note `「臆説」，「臆測」は，「憶説」，
  「憶測」とも書く。`); `evidence\jmdict-cited-entries.xml`: 1182790 (lines 23-45; 臆病 at 25, 憶病 tagged `rarely used
  kanji form` at 29-30, the three glosses at 43-45), 1182750 (憶説 and 臆説, no tag, lines 4-19) and 1589020 (憶測, with
  臆測 tagged `rarely used kanji form`, lines 49-70).
- 臆病 was added as the everyday 臆 word, as you suggested. The card does not mention 憶病.

To verify: that the new sentence reports the table and JMdict accurately, and that it is a sufficient counterweight to the
JMdict "rarely used" wording.

## Optional points

| ID | Author action | Where | Reason |
| --- | --- | --- | --- |
| O1 | **changed** | `履.md:36`, `履.md:51` | Line 36 now says `The ぞう belongs to 草: Daijisen spells it ザウ in historical kana, the voiced form of サウ, its historical spelling of 草's ソウ.` and uses `accordingly` instead of `which is why`. Line 51 adds Digital Daijisen links for 草履 and 草. Support: `evidence\daijisen-草履.txt` line 7 (`ぞう‐り〔ザウ‐〕【草履】`) and `evidence\daijisen-草.txt` line 7 (`［音］ ソウ （ サウ ）`). The 草履 word article was not changed (no word article changed in this revision); its advice to learn ぞうり whole does not contradict the card. |
| O2 | **changed** | `模.md:36` | `Each is read as a whole word, so its reading is not split between its kanji.` (it read `Both are learned here as whole words.`). This wording was chosen instead of "模 has no separate reading in them" so the card makes no claim about which kana belong to which kanji in 相模 and 酸模. |
| O3 | **declined** | `揚.md:14`, `:51`; `模.md:14`, `:49`; `巡.md:14`, `:50`; `暇.md:14`, `:50` | Each of these exclusions rests on a sense the card itself teaches, so a learner who studied the card could reasonably pick the excluded kanji's title: 揚's first Daijisen sense is rising or raising high and its fourth is praising, as in 称揚 (`揚.md:25`), against 起 "wake; rise" and 賛 "approve; praise"; 模's fifth sense is being hard to see clearly, as in 模糊 "dim; vague" (`模.md:25`), against 漠 "desert; vague"; 査 appears in 巡査 (`巡.md:37`, `:50`); and お暇 おいとま means taking one's leave (`暇.md:50`), against 去 "leave, elapse". Each card's Notes bullet states the reason. As you note, they only shrink fallback pools: the three curated distractors already fill all three meaning options of 揚, 模, 巡 and 暇 (`checks\quiz-safety.txt` lines 34, 43, 15 and 40), and an exclusion only stops the two kanji from appearing in the same question, in either direction (`evidence\QuizBuilder.kt` line 26). Removing them would allow an option the card's own text supports, for no gain. |
| O4 | **partly changed** | `弾.md:25-33`, `弾.md:67` | Only 弾 was restructured. Its sense paragraph was the longest (1,050 characters: five senses and 16 example words, 15 of them glossed, plus the two counter glosses; your report counted 14 glosses). It is now a one-line intro, a five-bullet list with one example per sense (弾劾 is kept beside 弾圧), and a pointer sentence (line 33); the other ten example words, their glosses and the counter glosses moved to the last Notes bullet (line 67), with only trailing punctuation changed. Nothing was added or dropped (`CHANGES.md`). The sense paragraphs of 博 (704 characters), 我 (636) and 揚 (829) are unchanged: each is already ordered sense by sense with the central idea stated first on the card, and rewriting three more reviewed, correct paragraphs in a confirmation round adds regression risk for a style gain. The author will record the 弾 layout in the authoring notes as the preferred form for long sense lists in later batches. |
| O5 | **declined** | `及.md:13` | 吸, 扱 and 級 are 及's closest shape look-alikes and give the meaning quiz its look-alike options (`checks\quiz-safety.txt` line 6). They supply no curated option for the キュウ prompt (吸 and 級 are キュウ and excluded; 扱 has no on reading), so the fallback fills all three slots, with 40 drawable wrong options in the N1 and All stacks and 15 in the Starter session and no attested reading among them (`checks\reading-exposure.txt` lines 62-68). Replacing a look-alike with a different-reading card would weaken the meaning quiz to gain a curated reading option that the fallback already supplies safely. |

## Other limits in your report

No disposition is needed for these.

- You did not open `evidence\app-code\`. This round, `evidence\` holds the app's `QuizBuilder.kt`, `KanjiReadings.kt` and
  `Words.kt` so that the reading-quiz claims in `CHANGES.md` can be checked against the code.
- The Android JVM content tests and the Kotlin reading-audit cross-check were not run for this revision either (see
  `CHANGES.md`).
- The Joyo pages cited by the revision are supplied as text extracts with the PDF's URL and hash (`evidence\README.md`).
- Your lead (h) counted 19 latent collisions. This round the audit also treats every reading Kanjipedia marks as outside
  the official table (外) as attested for all 15 kanji. With those readings the reviewed snapshot has 2 production hits
  (巡 まわる and 救 ぐ, `evidence\reading-exposure-163b384e.txt` line 392); the revised snapshot has 0 production and 0
  padded-session hits and 25 latent collisions (`CHANGES.md`, last section).
- The 7 lint warnings are unchanged and all on unchanged word articles.

## Changes that do not answer a point in your report

They are listed in `CHANGES.md`; please review them like any other changed hunk.

- **巡: distractors and Kanjipedia まわる** (`巡.md:13`, `:37`, `:49`). Kanjipedia lists まわる as a kun reading of 巡
  outside the official table (`evidence\kanjipedia-巡.txt`, line 6). At the reviewed snapshot only 川 supplied a curated
  kun option for めぐる, so the fallback filled two slots from 285 candidates (original packet
  `evidence\audits\reading-exposure.txt`, line 112). Run on the reviewed snapshot with the Kanjipedia readings added,
  the audit finds that 回's まわる could be drawn there in the N1 and All stacks (`evidence\reading-exposure-163b384e.txt`,
  line 148). `distractors` is now `[川, 道, 達]`: 道 and 達 have the same 辶 as 巡 and, like 川, are starter cards, so the
  three curated cards fill every wrong slot of both reading prompts in the N1 stack, the All stack and the Starter
  session, and the fallback is never consulted (`checks\reading-exposure.txt` lines 131-154). The meaning options are now
  `river | road, way | reach, plural suffix` (`checks\quiz-safety.txt` line 15). Line 37 adds a sentence saying
  Kanjipedia lists まわる and the quiz does not offer it as a wrong answer. Line 49 adds 道 and 達 to the look-alike
  bullet; 順 and 純 stay there as same-reading kanji. The cards 道, 達 and 回 are in the original packet's `repo\kanji\`
  and are unchanged.
- **救: distractors and Kanjipedia グ, ク, たすける** (`救.md:13`, `:48`, `:49`). Kanjipedia marks グ, ク and たすける as
  readings of 救 outside the official table (`evidence\kanjipedia-救.txt`, line 6). The curated distractor 求 has the
  metadata on reading グ, and on the reviewed snapshot the same audit finds ぐ drawable as a wrong answer to the キュウ
  prompt in the N1 and All stacks, offered by 供, 具, 工 and 求 (`evidence\reading-exposure-163b384e.txt`, line 338).
  `distractors` is now `[敬, 球, 教]`; 敬, which also has 攵 at the right, offers ケイ or キョウ. Line 48 adds 敬 to the
  look-alike bullet, and line 49 is a new bullet on the Kanjipedia readings and why 求 is not a curated wrong-answer card.
  The mnemonic (line 27) still names 求 as the shape at the left. In `checks\reading-exposure.txt`, ぐ, く and たすける
  cannot be drawn in any pool or with any single extra holder (lines 340-345 and 353-355). 敬, 球 and 教 are not starter
  cards, so in the Starter session both 救 prompts take all three wrong options from the fallback (lines 339 and 352),
  as they did at the reviewed snapshot (original packet `evidence\audits\reading-exposure.txt`, lines 255 and 259). 敬
  is in the original packet's `repo\kanji\`.
- **Stem wording** (`巡.md:39`, `恵.md:40`, `揚.md:40`). `so めぐ.る supplies the one question for that stem, shown as
  めぐる`, and likewise めぐむ and あげる (they read `supplies the めぐ question` or `the あ question comes from`), so the
  card names the form the learner actually sees.

## Process notes

- `2ef25d33` is the third local version of the fix commit; the two earlier ones (`bf9262a0`, `7e178bfd`) were never
  published or reviewed. `diffs\fix.patch` is the whole change from the reviewed snapshot `163b384e`.
- An earlier local draft used 返 and 送 instead of 道 and 達 for 巡. They are not starter cards, so the Starter session
  still had to use the fallback; they were replaced before this snapshot.

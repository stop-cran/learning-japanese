# Author's statement for the reviewer of `reports-136\initial-claude.md`

This statement answers only the points in YOUR initial report. C1 is your report's own Findings label, and O1 to O11 are
your Optional labels. LD is the "Reading audits disagree on drawability" bullet in your Limits section. The statement is
the author's claim about what changed and why. Verify each claim against the revised text in `snapshot\`,
`diffs\fix.patch` and independent sources; do not rely on this text as evidence. Card line numbers refer to the revised
cards in this packet; other line numbers refer to the named file in this packet unless the original packet is named. Five
of the 15 cards changed (炊 端 粗 請 駄), the other ten did not, and one word article changed (透明; see `CHANGES.md`).
Give a disposition for each of C1, O1 to O11 and LD.

## Findings

### C1 (minor): 炊く's dialect sense is presented as general Japanese

Author action: **changed.**

- `炊.md:23` now ends: `JMdict glosses the verb 炊く "to cook (grains, e.g. rice)" and, in a second sense that it marks
  as Kansai dialect, "to boil; to simmer; to stew; to seethe," where standard Japanese uses [煮る](../words/煮る.md) にる.`
  (it read `and, in a second sense, "to boil; to simmer; to stew; to seethe."`).
- `炊.md:50` now says `the Kansai-dialect sense of 炊く in JMdict also has "to seethe."` (it read `JMdict's 炊く also has
  "to seethe."`). As you advised, the exclusion of 沸, 飯 and 蒸 stays.
- `炊.md:52`: JMdict entry 1322540 (煮る) is added to the Metadata entry list.
- Difference from your remedy: the quotation keeps JMdict's fourth gloss, "to seethe," because line 50 refers to it.
- Support: `evidence\jmdict-cited-entries.xml`, entry 1596830 (sense 2: `<dial>Kansai-ben</dial>`, `<xref>煮る</xref>`)
  and entry 1322540 (煮る にる: "to boil; to simmer; to stew; to seethe"). The link target `words\煮る.md` exists and is
    unchanged (`checks\link-targets.tsv`). The word article 炊く already gave the Kansai restriction and is unchanged (the
    original packet's `snapshot\words\炊く.md:45-48`).

To verify: that lines 23 and 50 now present the sense as regional and that nothing else on the card implies a general
"boil" sense for the verb.

## Optional points

The batch rule behind O1 to O3: each card mentions every reading in its KANJIDIC2 metadata and every reading that its
Digital Daijisen character entry lists in ［音］ and ［訓］ (the card's character source, linked in its Metadata line),
even when KANJIDIC2 lacks it. Readings that Kanjipedia gives but neither KANJIDIC2 nor Daijisen does are mentioned
selectively: in this batch, only 脱 タツ (`脱.md:33`); 異 あやしい, 焦 やく, 膨 ホウ and ふくよか, 端 ただしい and はじめ, and
駄 のせる are not mentioned. Across the collection, 41 of the 1,292 kanji cards cite Kanjipedia. Before this revision, two
Daijisen kun readings were missing (端 はした, 駄 においうま); both are now added. All the Kanjipedia readings above are
among the `--extra` readings of `checks\reading-exposure.txt` (line 1), and none can be drawn as a wrong answer in the
three pools the audit checks, the N1 stack, the All stack and the Starter practice session (line 363).

| ID | Author action | Where | Reason |
| --- | --- | --- | --- |
| O1 | **partly changed** | `駄.md:31` | Added: `The character entry also lists the kun reading においうま, which KANJIDIC2 does not list and no JMdict entry has.` Support: the original packet's `evidence\public-source\weblio-駄.txt` line 6 (`［訓］ においうま`). Kanjipedia's の.せる is not added: Daijisen does not list it (same line), and the batch rule above mentions Daijisen readings. The non-ateji ダ examples you suggest are already on the card: 駄作 (line 29), 駄菓子 (line 31), 駄目 in the ダ row (line 39), and the official table's examples 駄菓子, 駄作 and 無駄 (line 46). Making ダ quizzable would need a new ダ word article, which is outside this revision. |
| O2 | **declined** | `膨.md` (unchanged) | The Daijisen 膨 entry lists only ボウ and ふくらむ, ふくれる (the original packet's `evidence\public-source\weblio-膨.txt` line 6; ホウ appears on that page only in the separate Wiktionary block, marked 表外, and in the 漢字辞典 block, which draws on KANJIDIC2, whereas the pinned KANJIDIC2 record lists only ボウ, `evidence\kanjidic2-records.xml` in the original packet). So 膨 already meets the batch rule. A premise correction: 炊 かしぐ (`炊.md:25`), 粗 ほぼ (`粗.md:30`) and 納 いれる (`納.md:32`) are mentioned because their Daijisen entries list them, and the cards attribute them to Daijisen; Kanjipedia also lists them, but that is not why they are there. Of your four examples, only 脱 タツ is a Kanjipedia mention, and it is the exception. JMdict has 膨よか only as a rarely used kanji form of ふくよか, which is usually written in kana (`evidence\jmdict-cited-entries.xml`, entry 1011000). |
| O3 | **partly changed** | `端.md:33`, `:65` | Added はした: `The kun list also includes はした, which has no word group of its own; KANJIDIC2 does not list はした, and JMdict has the noun 端 はした, "fraction; odd sum."`, with JMdict entry 2590770 in the Metadata list. Support: the original packet's `evidence\public-source\weblio-端.txt` line 6 (`［訓］ はし は はた はした`; word groups follow only for 〈はし〉, 〈は〉 and 〈はた（ばた）〉), and `evidence\jmdict-cited-entries.xml`, entry 2590770. The はた example is unchanged: 道端, 井戸端 and 炉端 are read ばた, which has its own row with 道端 (line 45), and the はた row (line 44) already says 端から is usually written in kana. はじめ is not added: Daijisen lists it only as a name reading (［名のり］, same line 6), and Kanjipedia-only readings follow the rule above. It cannot be offered as a wrong answer (see LD). |
| O4 | **no change** | `納.md` (unchanged) | You found no defect. A ノウ word article would be new vocabulary and is outside this revision; the gap is recorded as a known limit of the batch. |
| O5 | **changed** | `粗.md:42` | The JMdict sentence now ends `and marks the noun as usually written in kana in the sense of a flaw or fault.` The card glosses the noun 粗 あら as "flaw; fault" (line 39), which is JMdict's sense 2, tagged `word usually written using kana alone` (`evidence\jmdict-cited-entries.xml`, entry 1586730). Sense 1 (the bony parts of a fish, `usu. アラ`) is not taught on the card and is not mentioned. |
| O6 | **changed** | `炊.md:25` | The 雑炊 gloss is now JMdict's full gloss: `"rice porridge made by simmering cooked rice in a seasoned broth, often containing vegetables, fish, etc. (usu. made from leftovers)."` (`evidence\jmdict-cited-entries.xml`, entry 1299440). |
| O7 | **no change** | `脱.md:13`, `致.md:13` | You judged both sets acceptable as meaning-quiz distractors. Look-alikes such as 説, 税 or 鋭 would make harder reading options, but changing `distractors` changes the quiz options of two cards that both reviewers found clean on quiz safety, and it would need the whole quiz audit redone. Recorded as polish, not adopted. |
| O8 | **declined (premise disputed)** | `致.md:48`, `:58`; `端.md` | はじめ and おこす cannot be offered as wrong answers, so a sentence saying the quiz could show おこす would be false. See LD for the audit lines. Card text states facts about the chosen cards and sources and does not predict quiz output; `致.md:48` says that none of 話, 買 and 学 is read おこす or おくす, which is true. |
| O9 | **no change** | `炊.md` (unchanged) | You rate this low risk. い is a KANJIDIC2 name-only reading of 炊 and can be drawn on the スイ prompt in the N1 and All stacks (`checks\reading-exposure.txt` line 18); the prompt asks for an on reading, and this is recorded as a known limit of the batch. You found the 吹 and 八 fallbacks safe; nothing about them changed. |
| O10 | **no change** | — | You found every exclusion justified. |
| O11 | **declined** | the original packet's `snapshot\words\鉢.md:28` (unchanged) | All 34 link wraps of the batch use one placement rule: the first occurrence of the kanji in the word article's "How the kanji combine" section. That section explains the kanji. In 鉢.md the section's first 鉢 is in 鉢多羅 (line 27 has no 鉢); the earlier stand-alone 鉢 are in the heading and the Meaning section, including its example sentences (lines 12 to 22). The original packet's `repo\docs\content-format.md` requires only that each carded kanji is linked; the placement is unchanged, so this word article differs from the published one only by its wrap. |

## Limits point

### LD: "Reading audits disagree on drawability"

Author action: **disputed; no change.** The two audits agree.

- In `checks\reading-options.txt`, `HIT (can be drawn)` means the reading is in a fallback tier of the full pool (lines 95
  and 232). The simulation lines count distinct wrong options, not seeds: `6 wrong options seen over 100 seeds` for はし
  (line 98) are exactly the six readings of the curated cards 新 (あたらしい あらた あら にい), 山 (やま) and 短 (みじかい)
  (lines 88-90). `4 wrong options seen` for いたす (line 233) are exactly はなす はなし, かう and まなぶ of 話, 買 and 学
  (lines 226-228). So the simulation never reached the fallback, and neither はじめ nor おこす was drawn.
- `checks\reading-exposure.txt` says the same for all three pools it checks: in the N1 stack, the All stack and the
  Starter practice session the curated options fill all three wrong slots and the fallback is never consulted (lines
  98-100 and 251-253), and はじめ and おこす cannot be drawn (lines 107 and 254).
- The app code is in `evidence\` (`QuizBuilder.kt`, `KanjiReadings.kt`, `Words.kt`, unchanged copies from the original
  packet's `evidence\app-code\`); both audits are the author's Python ports of it. Both audit files are unchanged from the
  original packet apart from line 1 (the command line).

## Other limits in your report

No disposition is needed for these.

- You read only the diff hunks of the word articles. This round, the one changed word article, `words\透明.md`, is in
  `snapshot\words\` in full.
- The Android JVM content tests and the Kotlin reading-audit cross-check were not run for this revision either (see
  `CHANGES.md`).

## Changes that do not answer a point in your report

They are listed in `CHANGES.md`; review them like any other changed hunk.

- **請: the position of 青 in 静** (`請.md:54`). The look-alike bullet said that 清, 晴 and 静 all have 青 at the right.
  In 静, 青 is at the left and 争 at the right. The bullet now reads `[清](清.md), "pure, clean," and [晴](晴.md), "clear
  skies," have 青 at the right as 請 does, and [静](静.md), "quiet," has 青 at the left; all three are read セイ, and 清 also
  has the readings シン and ショウ. All are different kanji.` Support: `evidence\kanjivg\09759.svg` (静), 青 group
  `kvg:position="left"` (line 40) and 争 group `kvg:position="right"` (line 54).
- **透明: stale sentence removed** (`words\透明.md`). The article said `There is no separate 透 card in this collection.`,
  two lines below the batch's new link to the 透 card (line 30). The sentence is deleted, and nothing else in the article
  changed. This is the one change in the batch's word articles besides link wraps.

## Process notes

- `7a525b06` is the only fix commit; `diffs\fix.patch` is the whole change from the reviewed snapshot `420a6669`.
- The checks in `checks\` were run on the committed revision.

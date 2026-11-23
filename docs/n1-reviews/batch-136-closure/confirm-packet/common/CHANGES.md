# Batch 136 revision: what changed from 420a6669 to 7a525b06

Revised snapshot: `7a525b065ee613535c71d559bfc4ce0aea00beb1`, a child of the reviewed snapshot
`420a6669a2f1dafcc3a237e8b8604ff8cbc4201e`. Nothing is published.

- Five of the 15 kanji cards changed: 炊, 端, 粗, 請 and 駄. The other ten (焦, 異, 筋, 納, 脱, 膨, 致, 透, 鉢, 隔) are
  unchanged, and so are all 15 stroke files and the whole front matter of every card (titles, tags, metadata readings,
  `distractors` and `quiz_exclusions`).
- One word article changed: `words\透明.md` loses one sentence (see the table). The other 33 word articles touched by the
  batch are unchanged from the reviewed snapshot, so each still differs from the published text only by its one link
  wrap. The 透明 change is the one exception to "link wraps only" in the batch's word edits.
- `manifest.json` was regenerated; it is a generated index and outside the review.
- Line numbers below refer to `snapshot\kanji\<card>.md` and `snapshot\words\透明.md` in this packet (the revised
  snapshot).
- `diffs\fix.patch` is the exact patch. `diffs\changed-lines.txt` lists the changed lines per file.
- Every quoted title in the new text was checked by script against the linked card's real `title:` (see
  `checks\link-targets.tsv`).
- New evidence in this packet is everything under `evidence\`; `evidence\README.md` describes each file. All other evidence
  stays in the original packet; in particular the Digital Daijisen character entries are the original packet's
  `evidence\public-source\weblio-<kanji>.txt`.

| File | Changed lines | Change |
| --- | --- | --- |
| 炊 | 23, 25, 50, 52 | Line 23: the second sense of 炊く is now introduced as `in a second sense that it marks as Kansai dialect, "to boil; to simmer; to stew; to seethe," where standard Japanese uses [煮る](../words/煮る.md) にる.` (it read `in a second sense, "to boil; to simmer; to stew; to seethe."`). Line 25: the 雑炊 gloss is now JMdict's full gloss, `"rice porridge made by simmering cooked rice in a seasoned broth, often containing vegetables, fish, etc. (usu. made from leftovers)."` (it stopped after `seasoned broth`). Line 50: `the Kansai-dialect sense of 炊く in JMdict also has "to seethe."` (it read `JMdict's 炊く also has "to seethe."`); the exclusion of 沸, 飯 and 蒸 is unchanged. Line 52: JMdict entry 1322540 (煮る) is added to the entry list. Support: `evidence\jmdict-cited-entries.xml`, entry 1596830 (sense 2 carries `<dial>Kansai-ben</dial>` and `<xref>煮る</xref>`), entry 1322540 (煮る にる, "to boil; to simmer; to stew; to seethe") and entry 1299440 (雑炊). The word article `words\煮る.md` exists and is unchanged; its `title:` is in `checks\link-targets.tsv`. |
| 端 | 33, 65 | Line 33 gains, before the closing pointer sentence: `The kun list also includes はした, which has no word group of its own; KANJIDIC2 does not list はした, and JMdict has the noun 端 はした, "fraction; odd sum."` Line 65: JMdict entry 2590770 is added to the entry list. Support: the original packet's `evidence\public-source\weblio-端.txt` line 6 (`［訓］ はし は はた はした`, followed by word groups only for 〈はし（ばし・ぱし）〉, 〈は（ば・ぱ）〉 and 〈はた（ばた）〉); `evidence\jmdict-cited-entries.xml`, entry 2590770 (端 and 端た, はした; sense 1 "fraction; odd sum"). No reading row, metadata reading or quiz setting changed. |
| 粗 | 42 | The JMdict sentence now ends `"rough" and "crude; raw; natural; wild," and marks the noun as usually written in kana in the sense of a flaw or fault.` (it ended at `"crude; raw; natural; wild."`). The card's gloss of the noun 粗 あら is "flaw; fault" (line 39). Support: `evidence\jmdict-cited-entries.xml`, entry 1586730 (sense 2, "flaw (esp. of a person); fault; defect", carries `word usually written using kana alone`; sense 1, the bony parts of a fish, carries the same tag and `usu. アラ`). |
| 請 | 54 | `[清](清.md), "pure, clean," and [晴](晴.md), "clear skies," have 青 at the right as 請 does, and [静](静.md), "quiet," has 青 at the left; all three are read セイ, and 清 also has the readings シン and ショウ. All are different kanji.` (it said all three `have 青 at the right as 請 does and are all read セイ`). Support: `evidence\kanjivg\09759.svg` (静): the 青 group at line 40 is `kvg:position="left"` and the 争 group at line 54 is `kvg:position="right"`. The card 静 is in the original packet's `repo\kanji\` and is unchanged. |
| 駄 | 31 | Line 31 gains, before the closing pointer sentence: `The character entry also lists the kun reading においうま, which KANJIDIC2 does not list and no JMdict entry has.` Support: the original packet's `evidence\public-source\weblio-駄.txt` line 6 (`［訓］ においうま`). No JMdict entry in the pinned file has the reading においうま or the spelling 荷負い馬 (the author's search of the pinned JMdict; there is no entry to supply). |
| 透明 (word) | old 32 | The sentence `There is no separate 透 card in this collection.` is deleted; it stood two lines below the batch's new link `[透](../kanji/透.md)` (line 30). Lines 30 and 31 are unchanged from the reviewed snapshot, and nothing else in the article changed. |

## Checks run on the revised snapshot (outputs in `checks\`)

- `lint.txt`: the batch linter on the 15 kanji cards and their 34 word articles: 0 errors, 8 warnings, all on word
  articles (6 say the Dictionary line cites no JMdict entry id, 2 say there is no Dictionary line). Same as for the
  reviewed snapshot; one of the 6 is `words\透明.md`, whose Dictionary line this revision did not touch.
- `unittest.txt`: 436 tests, OK. `validate.txt`: 0 errors. `budget.txt`: the content budget script's size summary; it
  raised no budget error. `vocabulary.txt`: vocabulary coverage check passes (3201 of 3336 reviewed prompts, stage pilot).
  `manifest.txt`: `manifest.json` regenerated, rebuild idempotent.
- The Android app's JVM tests that read the real content and the Kotlin reading-audit cross-check were not run for this
  revision either, so there is no `jvm.txt`.
- `link-targets.tsv`: every link on a changed line, with the existence of its target, the target's `title:` and whether the
  gloss quoted after the link equals that title.
- `quiz-safety.txt`, `reading-options.txt` and `reading-exposure.txt`: no front matter changed, so the quiz options are
  unchanged. `quiz-safety.txt` is identical to the original packet's `evidence\audits\quiz-safety.txt`, and the other two
  differ from the same files there only in line 1 (the command line, which names the revision).
  - `reading-exposure.txt` line 1 shows the `--extra` readings: the outside readings named in card text or in Kanjipedia
    for the 15 kanji, including 端 はした and はじ.め, 駄 においうま and の.せる, and 膨 ふく.よか. The tool labels every
    `--extra` reading `(card text)`. Line 363: 0 production hits, 0 padded-session hits, 17 latent collisions.
  - `reading-options.txt` line 330 reports `2 problem(s)`: the `HIT (can be drawn)` lines for 端 はじめ via 初 (line 95)
    and 致 おこす via 起 (line 232). That audit labels a reading HIT when it is in a fallback tier of the full pool; its own
    simulation lines show that the fallback is not reached for these prompts: 6 wrong options seen over 100 seeds for
    はし (line 98), which are exactly the six readings of the curated cards 新, 山 and 短 (lines 88-90), and 4 for いたす
    (line 233), exactly those of 話, 買 and 学 (lines 226-228). `reading-exposure.txt` states the same for all three pools
        it checks, the N1 stack, the All stack and the Starter practice session: the curated options fill all three wrong
        slots and the fallback is never consulted (lines 98-100 and 251-253), and はじめ and おこす cannot be drawn (lines 107
        and 254).

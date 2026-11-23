# Batch 138 revision: what changed from b6020f9e to acf7297e

Revised snapshot: `acf7297ef66a82f620a6c5551d95a2e3fa356bc7`. It is reached from the reviewed snapshot
`b6020f9e490298de1756e33c51bf9ce314132f4e` by one commit. Nothing is published.

- Ten of the 15 kanji cards changed: 垣, 執, 堅, 塊, 壊, 奏, 契, 奪, 妨 and 威. The other five (噴, 垂, 墨, 壁, 奨) are
  unchanged. So are all 15 stroke files, the older kanji card the batch edits (張) and all 17 word articles the batch
  edits; each of those 33 files still differs from the published text exactly as in the reviewed snapshot.
- Front matter: only `quiz_exclusions` changed, on three cards: 垣 adds 壁, 塊 adds 組 and 奪 adds 魅. Titles, tags,
  metadata readings and every `distractors` list are unchanged. The app treats two cards as excluded when either lists
  the other (`evidence\QuizBuilder.kt` line 26), so 壁, 組 and 魅 need no change. None of the three new pairs removes an
  authored distractor of any card: `checks\quiz-safety.txt`, which also lists every existing card whose curated options
  fall short, is identical to the reviewed snapshot's.
- `manifest.json` was regenerated; it is a generated index and outside the review.
- Line numbers below refer to `snapshot\kanji\<card>.md` in this packet (the revised snapshot). 奏 gained two lines (a new
  paragraph at line 31 and the blank line 32 after it), so 奏's lines from 33 on are two more than in the reviewed
  snapshot; every other card has the same line numbers as before.
- `diffs\fix.patch` is the exact patch from `b6020f9e` to `acf7297e`. `diffs\changed-lines.txt` lists the changed lines
  per file.
- Every link on a changed line and the title quoted after it are listed in `checks\link-targets.tsv`, with the target's
  real `title:`.
- The Metadata lines. The author's writing rule for these cards is that the Metadata line lists the JMdict entry of
  every word the card names. The two new words, 執り行う and 功を奏する, have their entries added (執 line 58, 奏 line
  59). 押妨 (妨 line 25) has no JMdict entry; its gloss follows Digital Daijisen, the card's linked character source
  (`evidence\weblio-押妨.txt`). `evidence\meta-scan.txt`, made by `evidence\meta_scan.py`, finds no word without its
  entry. The script checks every run of Japanese script that has at least two characters, contains a kanji and exactly
  matches a JMdict kanji spelling. It does not check words written only in kana, single-kanji words, or words that
  appear only inside a longer word; it lists these separately, 26 of them, four more than in the reviewed snapshot
  (行う in 執り行う, and 功を奏す, 奏す and 奏する in 功を奏する).
- New evidence in this packet is everything under `evidence\`; `evidence\README.md` describes each file. All other
  evidence stays in the original packet.

| File | Changed lines | Change |
| --- | --- | --- |
| 垣 | 14, 48 | Line 14: `quiz_exclusions: [塀, 囲, 境, 界, 関, 限, 壁]` (壁 added). Line 48, the Notes bullet on the excluded characters, now also names `[壁](壁.md), "wall; barrier,"`, adds "wall" to the senses that 垣 and 垣根 carry, and ends `Do not treat "fence," "wall" or "boundary" as exclusive to any one character.` (it ended `Do not treat "fence" or "boundary" …`). Support: `evidence\jmdict-cited-entries.xml`, entries 1204780 (垣, sense 2 "barrier; wall") and 1509290 (壁). |
| 執 | 43, 58 | Line 43: after `In 執る, 執 writes と and る is okurigana, the kana ending that follows the kanji` the sentence continues `; the same と begins 執り行う とりおこなう, "to hold (a ceremony); to perform."` Line 58 (Metadata): entry 1319610 (執り行う) is added after 2655810. Support: `evidence\jmdict-cited-entries.xml`, entry 1319610. |
| 堅 | 41 | 硬い and 固い are now `two other spellings in JMdict's かたい entry; that entry also lists 緊い, marked as irregular kanji usage.` (it read `the other two spellings in JMdict's かたい entry.`). Support: `evidence\jmdict-cited-entries.xml`, entry 1257110 (硬い, 固い, 堅い and 緊い; 緊い carries `word containing irregular kanji usage`). |
| 塊 | 14, 52 | Line 14: `quiz_exclusions: [団, 固, 群, 束, 凝, 組]` (組 added). Line 52 now also names `[組](組.md), "group; assemble,"` and adds "group" to the senses that 塊 and its words carry. Support: `evidence\jmdict-cited-entries.xml`, entry 1590410 (塊, sense 2 "group; crowd"). |
| 壊 | 27 | The modern-shape mnemonic now reads `at the right [十](十.md), "ten," at the top, a box-like 罒 in the middle and the full shape of [衣](衣.md), "clothing; garment," at the bottom.` (it read `at the right [十](十.md), "ten," above a box-like 罒 and a shape like the lower part of [衣](衣.md), "clothing; garment."`). Support: `evidence\stroke-summaries.txt` (壊 strokes 11 to 16 have the stroke types of 衣 strokes 1 to 6 in the same order, and all lie below 罒, strokes 6 to 10). |
| 奏 | 31, 32, 59 | Lines 31 and 32 are new: the paragraph `The third sense also appears in the common phrase 功を奏する こうをそうする, "to succeed; to bear fruit."` after the list of the three Daijisen senses, and a blank line. Line 59 (Metadata; line 57 in the reviewed snapshot): entry 2080870 (功を奏する) is added after 1648640. Support: `evidence\jmdict-cited-entries.xml`, entry 2080870 (功を奏する, 効を奏する; こうをそうする). |
| 契 | 43 | The last sentence, `契丹 is different: its reading きったん belongs to the whole word and is not one of the KANJIDIC2 readings of 契.`, is replaced by `In 契丹 きったん, 契 supplies きっ: キツ shortens to きっ, with a small っ that doubles the next sound (gemination). [Kanjipedia's character entry](https://www.kanjipedia.jp/kanji/0001765100) marks キツ as a reading outside the official table, used in this country name, and also lists ケツ outside the table, as in 契闊 ケッカツ, not seeing someone for a long time. KANJIDIC2 lists neither reading, and JMdict also reads 契丹 as けいたん, with ケイ.` Support: `evidence\kanjipedia-契.txt`; `evidence\jmdict-cited-entries.xml`, entry 2714430 (契丹: きったん, けいたん, キタイ, キタン). |
| 奪 | 14, 48 | Line 14: `quiz_exclusions: [盗, 取, 捕, 魅]` (魅 added). Line 48 now adds, after the senses that 盗, 取 and 捕 overlap, `and [魅](魅.md), "charm; bewitch," overlaps the second sense of 奪う, "to fascinate; to captivate; to charm"`, then reads `These four are kept out of this card's quiz options` (it read `They are kept …`) and ends `Do not treat "take," "rob" or "charm" as exclusive to any one character.` Support: `evidence\jmdict-cited-entries.xml`, entry 1416340 (奪う, sense 2). |
| 妨 | 25 | `Its examples are 妨害 ぼうがい, "…," and 押妨 おうぼう, a historical term for breaking into another's domain to commit violence or impose unjust taxes.` (it read `Its example is 妨害 ぼうがい, "…"`). Support: the original packet's `evidence\public-source\weblio-妨.txt` line 6 (`「 妨害 ／ 押妨 」`); `evidence\weblio-押妨.txt` (Daijisen おう‐ぼう【押妨】 and a dictionary of historical terms). |
| 威 | 33, 44 | Line 33: the frame is `a long horizontal stroke on top, …; inside it sit a short horizontal stroke and [女](女.md)` (the top stroke was `a short horizontal stroke` and the inner one `a horizontal stroke`). Support: `evidence\stroke-summaries.txt` (stroke 2, on top, is 56.5 wide; stroke 3, inside, is 23.7 wide). Line 44 now begins `威張る mixes an on reading and a kun reading: 威 supplies い, its KANJIDIC2 on reading イ, and 張 supplies ば, …` (it began `威張る is a native verb whose reading is learned as a whole, but its parts can still be seen: 威 supplies い, which matches the KANJIDIC2 on reading イ, and 張 supplies ば, …`). |

## Checks run on the revised snapshot (outputs in `checks\`)

- `lint.txt`: the batch linter on 16 kanji cards (the 15 new cards and 張) and 24 word articles: 0 errors, 3 warnings,
  all on word articles whose Dictionary line cites no JMdict entry id (噴火, 墨, 威張る). The output is identical to the
  reviewed snapshot's (the original packet's `mechanical-checks.md` lines 5-11); this revision touched no word article.
- `unittest.txt`: 436 tests, OK. `validate.txt`: 0 errors. `budget.txt`: the content budget script's size summary; it
  raised no budget error. `vocabulary.txt`: vocabulary coverage check passes (3201 of 3336 reviewed prompts, stage pilot).
  `manifest.txt`: `manifest.json` regenerated, rebuild idempotent, tracked tree clean.
- The Android app's JVM tests that read the real content and the Kotlin reading-audit cross-check were not run for this
  revision either (no JDK on the authoring machine; the original packet's `mechanical-checks.md` line 257), so there is no
  `jvm.txt`.
- `link-targets.tsv`: every link on a changed line, with the existence of its target, the target's `title:` and whether the
  gloss quoted after the link equals that title.
- `quiz-safety.txt` matches the original packet's `evidence\audits\quiz-safety.txt` line for line. `reading-exposure.txt`
  and `reading-options.txt` differ from the same files there only in line 1 (the command line, which names the revision);
  the revision changed no reading, `distractors` list or reading-quiz setting.
  - `reading-exposure.txt` line 258: 0 production hits, 0 padded-session hits, 8 latent collisions; line 259: 0
    one-holder padded hits, 0 more for KANJIDIC2 name-only readings.
  - `reading-options.txt` line 222: 2 problems, the two HIT labels at lines 17 (噴 ほん) and 160 (契 けつ). This tool does
    not model curated slots that are already filled; `reading-exposure.txt`, which models the actual pools, finds both
    readings not drawable.

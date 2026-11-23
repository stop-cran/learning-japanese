# Author's statement for the reviewer of `reports-138\initial-claude.md`

This statement answers only the points in YOUR initial report. C1 to C4 are your report's own Findings labels, and O1 to
O9 are your Optional labels. The statement is the author's claim about what changed and why. Verify each claim against
the revised text in `snapshot\`, `diffs\fix.patch` and independent sources; do not rely on this text as evidence. Card
line numbers refer to the revised cards in this packet; other line numbers refer to the named file in this packet unless
the original packet is named. Ten of the 15 cards changed (垣 執 堅 塊 壊 奏 契 奪 妨 威), the other five did not, and no
word article or stroke file changed (see `CHANGES.md`). Give a disposition for each of C1 to C4 and O1 to O9.

## Findings

### C1 (minor): 堅 — incomplete "other two spellings" claim

Author action: **changed.**

- `堅.md:41` now reads `marked as a pair to compare with 硬い and 固い, two other spellings in JMdict's かたい entry;
  that entry also lists 緊い, marked as irregular kanji usage.` (it read `… 硬い and 固い, the other two spellings in
  JMdict's かたい entry.`).
- Support: `evidence\jmdict-cited-entries.xml`, entry 1257110 (four kanji spellings 硬い, 固い, 堅い and 緊い; 緊い
  carries `word containing irregular kanji usage`).

### C2 (minor): 契 — the outside-table on readings

Author action: **changed in part, disputed in part.** The whole-word statement is replaced. The attribution of セツ to
Kanjipedia is disputed, so your suggested sentence is not used as it stands.

- `契.md:43`, the sentence about 契丹, now reads: `In 契丹 きったん, 契 supplies きっ: キツ shortens to きっ, with a small
  っ that doubles the next sound (gemination). [Kanjipedia's character entry](https://www.kanjipedia.jp/kanji/0001765100)
  marks キツ as a reading outside the official table, used in this country name, and also lists ケツ outside the table, as
  in 契闊 ケッカツ, not seeing someone for a long time. KANJIDIC2 lists neither reading, and JMdict also reads 契丹 as
  けいたん, with ケイ.` (it read `契丹 is different: its reading きったん belongs to the whole word and is not one of the
  KANJIDIC2 readings of 契.`).
- Support: `evidence\kanjipedia-契.txt` (the Kanjipedia page with its sha256: reading list `[音] ケイ [外]キツ・ケツ
  [訓] ちぎる [外]きざむ・わりふ`; meanings `[二]キツ 国の名。「契丹」` and `[三]ケツ … ②久しく会わない。「契闊(ケッカツ)」`);
  `evidence\jmdict-cited-entries.xml`, entry 2714430 (契丹: きったん, けいたん, キタイ, キタン). The original packet's
  `evidence\kanjipedia-outside-readings.json` gives the same outside readings for 契: キツ, ケツ, きざ.む and わりふ, and
  no セツ.
- Why セツ is not added: Kanjipedia's reading list has no セツ; on that page セツ occurs once, inside the formation note
  (なりたち), as part of the etymology (`evidence\kanjipedia-契.txt`, item 3). The audits list セツ among 契's extra
  readings because Digital Daijisen has a separate headword せつ【契】 (the original packet's `evidence\daijisen-heads.txt`
  line 59). That headword names a legendary figure of ancient China, a son of 帝嚳 who is said to have laid the
  foundation of the Yin (殷) dynasty; it is a proper name, not a reading used in words. The batch rule below does not call
  for it, and the card does not mention it.
- The two Kanjipedia-only kun readings きざ.む and わりふ are not added either (batch rule below); both are among the
  `--extra` readings of `checks\reading-exposure.txt` line 1.

To verify: that line 43 now says what 契 contributes to きったん and that the readings it attributes to Kanjipedia are on
the page.

### C3 (minor): 妨 — the Daijisen example claim

Author action: **changed.**

- `妨.md:25` now reads `Its examples are 妨害 ぼうがい, "obstruction; hindrance; blocking; disturbance; interference," and
  押妨 おうぼう, a historical term for breaking into another's domain to commit violence or impose unjust taxes.` (it
  read `Its example is 妨害 ぼうがい, "…"`).
- Support: the original packet's `evidence\public-source\weblio-妨.txt` line 6 (`「 妨害 ／ 押妨 」`); for the gloss of
  押妨, which has no JMdict entry, `evidence\weblio-押妨.txt` (Daijisen おう‐ぼう【押妨】: 他人の所領などに押し入って乱暴を
  働いたり、不当な課税をしたりすること, with an example from the Heike monogatari; and 歴史民俗用語辞典's entry).

### C4 (minor): 壊 — the bottom-right shape in the mnemonic

Author action: **changed**, with different wording from your remedy.

- `壊.md:27` now reads `at the right [十](十.md), "ten," at the top, a box-like 罒 in the middle and the full shape of
  [衣](衣.md), "clothing; garment," at the bottom.` (it read `above a box-like 罒 and a shape like the lower part of
  [衣](衣.md), …`).
- Why not "a split 衣": in the stroke data all six strokes that match 衣 lie below 罒. Strokes 11 to 16 of 壊 have the
  stroke types of strokes 1 to 6 of 衣 in the same order, and stroke 11, the short top vertical, starts at y 50.8, below
  罒 (strokes 6 to 10, y 30.0 to 49.9). A 衣 split around 罒 describes the historical form, but the mnemonic describes
  the modern shape only.
- Support: `evidence\stroke-summaries.txt` (computed from the stroke files of 壊, in the original packet's
  `snapshot\strokes\壊.json`, and of the published card 衣; neither changed).

## Optional points

The batch rule behind O5 to O7 and part of C2: each card mentions every reading in its KANJIDIC2 metadata and every
reading that its Digital Daijisen character entry lists in ［音］ and ［訓］ (the card's character source, linked in its
Metadata line), even when KANJIDIC2 lacks it. Readings that only Kanjipedia gives are mentioned selectively.

| ID | Author action | Where | Reason |
| --- | --- | --- | --- |
| O1 | **changed** | `威.md:33` | The frame is now `a long horizontal stroke on top, a long sweeping stroke at the left and, at the right, a long hooked stroke with a slash and a dot; inside it sit a short horizontal stroke and [女](女.md)` (the top was `a short horizontal stroke` and the inner stroke `a horizontal stroke`). Support: `evidence\stroke-summaries.txt` (威 stroke 2 spans x 27.0 to 83.5, width 56.5; stroke 3 spans x 32.8 to 56.5, width 23.7). |
| O2 | **changed** | `威.md:44` | The sentence now begins `威張る mixes an on reading and a kun reading: 威 supplies い, its KANJIDIC2 on reading イ, and 張 supplies ば, the voiced form of the は of 張る はる, …` (it began `威張る is a native verb whose reading is learned as a whole, but its parts can still be seen: 威 supplies い, which matches the KANJIDIC2 on reading イ, …`). |
| O3 | **declined** | `威.md` (no change for this point) | JMdict 2581990 is the word 縅 おどし, "leather strap binding the plates of traditional Japanese armor," and marks 威 as an ateji spelling of it (the original packet's `evidence\jmdict-families.xml`). It is specialist vocabulary under another main spelling, it has no word article and is not practiced, and 威 is already the second-longest card of the batch. The おど.し row keeps 威し "threat." |
| O4 | **changed** | `執.md:43`, `:58` | Line 43 now continues after the 執る sentence: `; the same と begins 執り行う とりおこなう, "to hold (a ceremony); to perform."` Line 58 (Metadata) adds entry 1319610 after 2655810. Support: `evidence\jmdict-cited-entries.xml`, entry 1319610 (執り行う, とりおこなう). 指揮を執る was not added; one example makes the point. |
| O5 | **declined** | `噴.md` (unchanged) | ホン and は.く are in neither KANJIDIC2 nor the ［音］ and ［訓］ list of 噴's Daijisen character entry (the original packet's `evidence\kanjidic2-records.xml` and `evidence\public-source\weblio-噴.txt` line 6: ［音］フン ［訓］ふく). They are Kanjipedia-only readings, so the batch rule does not call for them. Both are among the `--extra` readings of `checks\reading-exposure.txt` line 1; ほん and はく are latent collisions only (see O9). |
| O6 | **declined** | `垂.md` (unchanged) | しで is in neither KANJIDIC2 nor 垂's Daijisen ［訓］ list (たれる, たらす, しだれる, しずる, なんなんとする; the original packet's `evidence\public-source\weblio-垂.txt` line 6). As you say, JMdict 1767000 lists 垂 among the five spellings of しで, after the main spelling 四手 (the original packet's `evidence\jmdict-families.xml`), but as a reading of 垂 しで is Kanjipedia-only, so the batch rule does not call for it. The card already discusses the Daijisen-listed しだれる, しずる and なんなんとする and is the longest card of the batch. しで is among the `--extra` readings in `checks\reading-exposure.txt` line 1. |
| O7 | **declined** | `壁.md`, `墨.md`, `奪.md` (unchanged) | 壁 がけ, 墨 モク and 奪 タツ are each in neither KANJIDIC2 nor the card's Daijisen ［音］ and ［訓］ list (the original packet's `evidence\kanjidic2-records.xml` and `evidence\public-source\weblio-<kanji>.txt` line 6). They are Kanjipedia-only, and all three are among the `--extra` readings in `checks\reading-exposure.txt` line 1. |
| O8 | **changed** | `奏.md:31`, `:59` | A new paragraph after the list of three Daijisen senses: `The third sense also appears in the common phrase 功を奏する こうをそうする, "to succeed; to bear fruit."` (line 31; line 32 is the blank line after it, so every later line of 奏 moves down by two). Line 59 (Metadata, line 57 before) adds entry 2080870 after 1648640. Support: `evidence\jmdict-cited-entries.xml`, entry 2080870 (功を奏する, 効を奏する; こうをそうする). The phrase illustrates the third sense, achieving a result, rather than the reporting sense. |
| O9 | **declined for this revision** | tools (no change) | As you say, the two HIT labels in `reading-options.txt` are an audit-model difference, not a card defect. Both tools are left unchanged so that their outputs stay comparable with the original packet's `evidence\audits\`. The difference is recorded in the batch's closure notes. |

## Other limits in your report

No disposition is needed for these.

- The execution-rule breach (two tool calls in one response) is noted as you disclosed it.
- `checks\quiz-safety.txt` in this packet is the complete output on the revised snapshot; please read it in full this
  round.
- The Android JVM content tests and the Kotlin reading-audit cross-check were not run for this revision either (see
  `CHANGES.md`).

## Changes that do not answer a point in your report

They are listed in `CHANGES.md`; review them like any other changed hunk.

- **垣–壁** (`垣.md:14`, `:48`). JMdict's 垣 entry (1204780) has a second sense, "barrier; wall," and 壁's title is
  "wall; barrier." 壁 joins 垣's `quiz_exclusions` and its Notes bullet, which now also names the sense "wall."
- **奪–魅** (`奪.md:14`, `:48`). The second sense of 奪う (1416340) includes "to fascinate; to captivate; to charm," and
  魅's title is "charm; bewitch." 魅 joins 奪's `quiz_exclusions` and its Notes bullet. 魅 stays a distractor of 塊.
- **塊–組** (`塊.md:14`, `:52`). The second sense of 塊 (1590410) is "group; crowd," which is why 団, "group;
  association," was already excluded; 組's title is "group; assemble." 組 joins 塊's `quiz_exclusions` and its Notes
  bullet.
- One declaration covers both directions: the app treats two cards as excluded when either lists the other
  (`evidence\QuizBuilder.kt` line 26). No authored `distractors` list changed. Support:
  `evidence\jmdict-cited-entries.xml`, entries 1204780, 1509290, 1416340 and 1590410; `checks\link-targets.tsv` gives
  the titles of 壁, 魅 and 組.

## Process notes

- `acf7297e` is the only fix commit; `diffs\fix.patch` is the whole change from the reviewed snapshot `b6020f9e`. An
  earlier local version of it, `f8f488d1`, glossed 押妨 as `an old word for breaking into another's land and acting
  violently there`, which left out the unjust taxes in the Daijisen definition. It was replaced before this packet was
  built and was neither reviewed nor published.
- The checks in `checks\` were run on the committed revision.

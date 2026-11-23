# Author's statement for the reviewer of `reports-138\initial-gpt.md`

This statement answers only the points in YOUR initial report. G1 and G2 are your report's own Findings labels. Your two
Optional bullets had no labels; here the first (phone-reading polish) is OP and the second (keeping the eight latent
reading collisions as regression cases) is OR. The statement is the author's claim about what changed and why. Verify
each claim against the revised text in `snapshot\`, `diffs\fix.patch` and independent sources; do not rely on this text
as evidence. Card line numbers refer to the revised cards in this packet; other line numbers refer to the named file in
this packet unless the original packet is named. Ten of the 15 cards changed (垣 執 堅 塊 壊 奏 契 奪 妨 威), the other
five did not, and no word article or stroke file changed. In the front matter only the `quiz_exclusions` of 垣, 塊 and 奪
changed (see `CHANGES.md`). Give a disposition for each of G1, G2, OP and OR.

## Findings

### G1 (minor): missing direct 垣–壁 exclusion

Author action: **changed**, as your remedy describes.

- `垣.md:14` now reads `quiz_exclusions: [塀, 囲, 境, 界, 関, 限, 壁]` (壁 added). One declaration is enough: the app
  treats two cards as excluded when either lists the other (`evidence\QuizBuilder.kt` line 26), so 壁 is unchanged.
- `垣.md:48`, the Notes bullet on the excluded characters, now also names `[壁](壁.md), "wall; barrier,"` and the sense
  "wall", and ends `Do not treat "fence," "wall" or "boundary" as exclusive to any one character.` The prose distinction
  stays.
- Support: `evidence\jmdict-cited-entries.xml`, entries 1204780 (垣, sense 2 "barrier; wall") and 1509290 (壁, "wall;
  partition" and "barrier; obstacle"); `checks\link-targets.tsv` gives 壁's title.

To verify: that in your pool `{垣, 壁, 噴, 契}` neither 垣 nor 壁 is now offered as an option when the other is the target.

### G2 (minor): missing direct 奪–魅 exclusion

Author action: **changed**, as your remedy describes.

- `奪.md:14` now reads `quiz_exclusions: [盗, 取, 捕, 魅]` (魅 added); 魅's card is unchanged and is still an authored
  distractor of 塊.
- `奪.md:48` now adds, after the 盗, 取 and 捕 overlaps, `and [魅](魅.md), "charm; bewitch," overlaps the second sense of
  奪う, "to fascinate; to captivate; to charm"`, says `These four are kept out of this card's quiz options` and ends `Do
  not treat "take," "rob" or "charm" as exclusive to any one character.` The card still teaches the second sense.
- Support: `evidence\jmdict-cited-entries.xml`, entry 1416340 (奪う, sense 2); `checks\link-targets.tsv` gives 魅's
  title.

To verify: the same check for your pool `{奪, 魅, 噴, 契}`, and that no other exclusion was added beyond the direct pair.

## Optional points

| ID | Author action | Where | Reason |
| --- | --- | --- | --- |
| OP | **declined** | all cards (unchanged by this point) | The sense inventories and the closing reference bullet follow the current card layout, not this batch alone. For example, a closing `For reference, more Daijisen examples …` bullet is in 9 cards of this batch, including 垂, 執, 墨 and 威, and in 21 published cards, and the sentence `Being outside the practice set is not proof that a reading is invalid.` is in all 15 cards of this batch and in 57 published cards. Moving or condensing this material is a presentation change for the whole collection, outside this revision. |
| OR | **accepted as practice; no card change** | none | The eight latent collisions stay listed in every run of `reading-exposure.txt` (here `checks\reading-exposure.txt`), which is run for each batch and before each publication, so a change to reading pools, curated candidates or quiz size that makes one reachable shows up as a production or padded hit. They are also recorded in the batch's closure notes. |

## Other limits in your report

No disposition is needed for these.

- The Android JVM content tests and the Kotlin reading-audit cross-check were not run for this revision either (see
  `CHANGES.md`).
- A correction to your report's coverage notes, which needs no disposition: the reviewed cards did not mention 噴's
  ホン and は.く, 壁's がけ, 墨's モク, 奪's タツ, or 契's キツ and ケツ. These readings appear only in the audits'
  `--extra` lists (`checks\reading-exposure.txt` line 1). The revision now mentions 契's キツ and ケツ (`契.md:43`, next
  section); the others are still not on the cards.

## Changes that do not answer a point in your report

They are listed in `CHANGES.md`; review them like any other changed hunk.

- **塊–組** (`塊.md:14`, `:52`). The second sense of 塊 (JMdict 1590410) is "group; crowd," which is why 団, "group;
  association," was already excluded; 組's title is "group; assemble." 組 joins 塊's `quiz_exclusions` and its Notes
  bullet, which now also names the sense "group." Support: `evidence\jmdict-cited-entries.xml`, entry 1590410.
- **堅: the spellings in JMdict's かたい entry** (`堅.md:41`). The card called 硬い and 固い `the other two spellings` in that
  entry, but the entry has a fourth, 緊い. The text now reads `two other spellings in JMdict's かたい entry; that entry also
  lists 緊い, marked as irregular kanji usage.` Support: `evidence\jmdict-cited-entries.xml`, entry 1257110.
- **契: what 契 supplies in 契丹** (`契.md:43`). The card said that the reading きったん belongs to the whole word. The
  sentence now explains that 契 supplies きっ, from キツ with gemination, that Kanjipedia's character entry lists キツ
  (used in this country name) and ケツ (as in 契闊 ケッカツ) as readings outside the official table, that KANJIDIC2
  lists neither, and that JMdict also reads 契丹 as けいたん. Support: `evidence\kanjipedia-契.txt`;
  `evidence\jmdict-cited-entries.xml`, entry 2714430.
- **妨: Daijisen's examples** (`妨.md:25`). The card gave 妨害 as the Daijisen character entry's only example; the entry
  also gives 押妨 おうぼう, now glossed as `a historical term for breaking into another's domain to commit violence or
  impose unjust taxes.` Support: the original packet's `evidence\public-source\weblio-妨.txt` line 6;
  `evidence\weblio-押妨.txt` (Daijisen's おうぼう entry).
- **壊: the modern-shape mnemonic** (`壊.md:27`). The right side is now described as 十 at the top, 罒 in the middle and
  the full shape of 衣 at the bottom (it said `a shape like the lower part of 衣`). Support:
  `evidence\stroke-summaries.txt` (壊 strokes 11 to 16 have the stroke types of 衣 1 to 6 in order, all below 罒).
- **威: the frame in the mnemonic and the reading of 威張る** (`威.md:33`, `:44`). The frame's top stroke is now `a long
  horizontal stroke` and the inner stroke `a short horizontal stroke` (the two lengths were swapped; stroke widths in
  `evidence\stroke-summaries.txt`). The 威張る sentence now begins `威張る mixes an on reading and a kun reading: 威
  supplies い, its KANJIDIC2 on reading イ, and 張 supplies ば, …` (it began `威張る is a native verb whose reading is
  learned as a whole, but its parts can still be seen: …`).
- **執 and 奏: one more example each** (`執.md:43`, `:58`; `奏.md:31`, `:59`). 執 line 43 adds `the same と begins 執り行う
  とりおこなう, "to hold (a ceremony); to perform."`; 奏 gains the paragraph `The third sense also appears in the common
  phrase 功を奏する こうをそうする, "to succeed; to bear fruit."` (line 31, followed by a blank line, so every later line
  of 奏 moves down by two). Both Metadata lines add the new entries (1319610 and 2080870). Support:
  `evidence\jmdict-cited-entries.xml`, entries 1319610 and 2080870.

## Process notes

- `acf7297e` is the only fix commit; `diffs\fix.patch` is the whole change from the reviewed snapshot `b6020f9e`. An
  earlier local version of it, `f8f488d1`, glossed 押妨 differently; it was replaced before this packet was built and was
  neither reviewed nor published.
- The checks in `checks\` were run on the committed revision.

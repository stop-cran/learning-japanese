# Author's statement for the reviewer of `reports-136\initial-gpt.md`

This statement answers only the points in YOUR initial report. G1 to G3 are your report's own Findings labels. Your one
Optional bullet had no label; here it is OA. The statement is the author's claim about what changed and why. Verify each
claim against the revised text in `snapshot\`, `diffs\fix.patch` and independent sources; do not rely on this text as
evidence. Card line numbers refer to the revised cards in this packet; other line numbers refer to the named file in this
packet unless the original packet is named. Five of the 15 cards changed (炊 端 粗 請 駄), the other ten did not, and one
word article changed (透明; see `CHANGES.md`). Give a disposition for each of G1, G2, G3 and OA.

## Findings

### G1 (minor): 請 — 静 does not have 青 at the right

Author action: **changed**, as your remedy describes.

- `請.md:54` now reads `[清](清.md), "pure, clean," and [晴](晴.md), "clear skies," have 青 at the right as 請 does, and
  [静](静.md), "quiet," has 青 at the left; all three are read セイ, and 清 also has the readings シン and ショウ. All are
  different kanji.` (it said that all three `have 青 at the right as 請 does`). The shared セイ observation stays.
- Support: `evidence\kanjivg\09759.svg` (静, pinned KanjiVG): the 青 group is `kvg:position="left"` (line 40) and the 争
  group is `kvg:position="right"` (line 54).

To verify: that line 54 now describes all three characters correctly.

### G2 (minor): 透明 — stale claim that there is no 透 card

Author action: **changed**, as your remedy describes, and recorded as an exception.

- `words\透明.md`: the sentence `There is no separate 透 card in this collection.` is deleted. Nothing else in the article
  changed; the batch's link to the 透 card stays at line 30, and line 31 (`Together they express transparency. The on
  readings are トウ + メイ.`) now ends the paragraph. The whole revised article is in `snapshot\words\透明.md`.
- This is the one change in the batch's word articles besides the 34 link wraps. `CHANGES.md` lists it, and the closure
  record will list it as the exception to the batch's link-wrap-only rule for existing word articles.

To verify: that the article no longer contradicts the new card and that nothing else in it changed.

### G3 (minor): 炊 — the Kansai sense of 炊く loses its restriction

Author action: **changed**, as your remedy describes.

- `炊.md:23` now ends: `JMdict glosses the verb 炊く "to cook (grains, e.g. rice)" and, in a second sense that it marks
  as Kansai dialect, "to boil; to simmer; to stew; to seethe," where standard Japanese uses [煮る](../words/煮る.md) にる.`
  (it read `and, in a second sense, "to boil; to simmer; to stew; to seethe."`).
- `炊.md:50` keeps the restriction in the Notes: `the Kansai-dialect sense of 炊く in JMdict also has "to seethe."` (it read
  `JMdict's 炊く also has "to seethe."`). The exclusion of 沸, 飯 and 蒸 is unchanged.
- `炊.md:52`: JMdict entry 1322540 (煮る) is added to the Metadata entry list.
- The card's title `cook rice; boil` (line 3) and the Daijisen character sense at line 25 are unchanged, as your remedy
  allows.
- Support: `evidence\jmdict-cited-entries.xml`, entry 1596830 (sense 2: `<dial>Kansai-ben</dial>`, `<xref>煮る</xref>`)
  and entry 1322540 (煮る にる: "to boil; to simmer; to stew; to seethe"). The link target `words\煮る.md` exists and is
  unchanged (`checks\link-targets.tsv`). The word article 炊く is unchanged and still gives the Kansai restriction (the
  original packet's `snapshot\words\炊く.md:45-48`).

To verify: that lines 23 and 50 now agree with the 炊く word article and with Digital Daijisen's 炊く sense 2
(（西日本で）煮る).

## Optional points

| ID | Author action | Where | Reason |
| --- | --- | --- | --- |
| OA | **declined** | — | You rate it nonblocking polish and find the cards lead with a clear meaning. Moving the source inventories and the "no word article yet / not selected" explanations into a reference block would restructure ten or more reviewed cards whose content you found correct; in a confirmation round that adds regression risk for a style gain. The cards changed in this revision got only local edits. |

## Other limits in your report

No disposition is needed for these.

- Kanjipedia's live 膨 page was unavailable to you. The 膨 card is unchanged; the original packet's
  `evidence\kanjipedia-outside-readings.json` and `evidence\public-source\weblio-膨.txt` are what the author used.
- The Android JVM content tests and the Kotlin reading-audit cross-check were not run for this revision either (see
  `CHANGES.md`).

## Changes that do not answer a point in your report

They are listed in `CHANGES.md`; review them like any other changed hunk. They answer the other reviewer's report.

- **粗: kana note** (`粗.md:42`). The JMdict sentence now ends `and marks the noun as usually written in kana in the sense
  of a flaw or fault.` The card glosses the noun 粗 あら "flaw; fault" (line 39), JMdict's sense 2 of entry 1586730, which
  is tagged `word usually written using kana alone`; sense 1 (the bony parts of a fish) is not taught on the card.
- **炊: full 雑炊 gloss** (`炊.md:25`). 雑炊 is now glossed with JMdict's full gloss (entry 1299440): `"rice porridge made
  by simmering cooked rice in a seasoned broth, often containing vegetables, fish, etc. (usu. made from leftovers)."`
- **端: はした** (`端.md:33`, `:65`). Added: `The kun list also includes はした, which has no word group of its own;
  KANJIDIC2 does not list はした, and JMdict has the noun 端 はした, "fraction; odd sum."`, with JMdict entry 2590770 in the
  Metadata list. Digital Daijisen's 端 entry lists はした among its kun readings (the original packet's
  `evidence\public-source\weblio-端.txt` line 6).
- **駄: においうま** (`駄.md:31`). Added: `The character entry also lists the kun reading においうま, which KANJIDIC2 does
  not list and no JMdict entry has.` Support: the original packet's `evidence\public-source\weblio-駄.txt` line 6.
- With these two additions, every reading in each card's Digital Daijisen character entry (［音］ and ［訓］) is mentioned
  on the card. Neither reading is in the card's metadata, so neither is asked; both are among the `--extra` readings of
  `checks\reading-exposure.txt` (line 1).

## Process notes

- `7a525b06` is the only fix commit; `diffs\fix.patch` is the whole change from the reviewed snapshot `420a6669`.
- The checks in `checks\` were run on the committed revision.

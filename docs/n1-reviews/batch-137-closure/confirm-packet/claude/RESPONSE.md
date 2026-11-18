# Author's statement for the reviewer of `reports-137\initial-claude.md`

This statement answers only the points in YOUR initial report. C1 is your report's own Findings label, and O1 to O7 are
your Optional labels. LW and LE are two bullets in your Limits section: LW is "卸 Daijisen headword" and LE is "Labels in
the exposure audit". The statement is the author's claim about what changed and why. Verify each claim against the
revised text in `snapshot\`, `diffs\fix.patch` and independent sources; do not rely on this text as evidence. Card line
numbers refer to the revised cards in this packet; other line numbers refer to the named file in this packet unless the
original packet is named. Eleven of the 15 cards changed (丁 仰 但 傑 僕 卸 司 吐 呂 哲 善), the other four did not, and no
word article, stroke file or front matter changed (see `CHANGES.md`). Give a disposition for each of C1, O1 to O7, LW and
LE.

## Findings

### C1 (minor): quoted titles with a comma lose their space, so they are not the exact card titles

Author action: **changed.**

- All 16 quotations in your list now copy the linked card's title exactly: 丁 line 68; 仰 line 58 (two); 但 lines 27 and
  47; 傑 lines 27, 46 and 47; 僕 line 50; 司 lines 55 and 56; 吐 lines 48 and 49; 呂 line 52; 哲 line 55; 善 line 58.
  Each change only adds the space after the comma inside the quotation; `CHANGES.md` gives the old and new text.
- Cause: the author's working table of card titles, used when drafting the Notes, had lost the space after every comma
  inside a title. It was rebuilt from the cards' front matter.
- Scope check: a script compared every quoted title of a linked card or word article in all 15 cards (143 quotations)
  with the target's `title:` and found no other mismatch.
- Support: `checks\link-targets.tsv` lists every link on a changed line, the target's `title:` and whether the quotation
  equals it.

To verify: that the 16 quotations now equal the titles and that no other quoted title in the 15 cards differs from its
target's title.

## Optional points

The batch rule behind O6: each card mentions every reading in its KANJIDIC2 metadata and every reading that its Digital
Daijisen character entry lists in ［音］ and ［訓］ (the card's character source, linked in its Metadata line), even when
KANJIDIC2 lacks it. Readings that only Kanjipedia gives are mentioned selectively; no card in this batch mentions one.

| ID | Author action | Where | Reason |
| --- | --- | --- | --- |
| O1 | **changed** | `丁.md:40` | The sentence now ends `KANJIDIC2 does not list よほろ, and JMdict has no standalone entry for it; it appears only in つかえのよほろ, one reading of 仕丁 しちょう, which JMdict marks archaic and glosses "men pressed into forced labor (ritsuryō system)."` (it ended `and JMdict has no entry for it.`). Support: `evidence\jmdict-cited-entries.xml`, entry 2829360 (仕丁; sense 1, tagged `archaic`, applies to all four readings including つかえのよほろ; sense 2 is restricted to しちょう, じちょう and してい). In the pinned JMdict, 2829360 is the only entry with a reading containing よほろ (author's search). |
| O2 | **changed** | `傑.md:33`, `:42` | Both glosses of 傑作 now read `masterpiece; hilarious absurdity (jocular, dated)`. Support: `evidence\jmdict-cited-entries.xml`, entry 1253840 (sense 2 carries `jocular, humorous term` and `dated term`; sense 1 carries neither). The word article `words\傑作.md` (unchanged; the original packet's `snapshot\words\傑作.md`) already says that JMdict marks the second use jocular and dated. |
| O3 | **changed** | `卸.md:33` | The シャ row now glosses 卸下 しゃが as `cargo unloading (military term)`. Support: `evidence\jmdict-cited-entries.xml`, entry 2537870 (`<field>military</field>`). |
| O4 | **declined** | `井.md:14`, `:56`; `司.md:14`, `:56` (unchanged) | You judged these exclusions not wrong and harmless. Each has a stated basis on its card: 額 is titled "forehead; frame; sum," and 井 carries the sense "frame" (`井.md:56`); 営, 治 and 御 carry "manage" or "govern," and JMdict's 司る includes "to rule; to govern; to control" (`司.md:56`). An exclusion only removes a card from the wrong options. Dropping one would change `quiz_exclusions` and the meaning-quiz option pools, which `checks\quiz-safety.txt` shows clean, in exchange for no correctness gain. |
| O5 | **declined** | `哲.md` (unchanged) | You marked it not required. 何の変哲もない (JMdict 1642670, in `evidence\jmdict-cited-entries.xml`) has no word article, and the card already gives the テツ examples of its Readings row, Common words and official-table sentence (lines 39, 45 and 49). Adding it would lengthen a card that your O7 asks to shorten. |
| O6 | **declined** | — | None of 吐 ぬ.かす, 哀 かな.しむ, 傷 そこ.なう, 仰 あおの.く and の.く, and 但 ダン is in KANJIDIC2 or in the ［音］ and ［訓］ list of a Daijisen character entry (the original packet's `evidence\kanjidic2-records.xml` and `evidence\public-source\weblio-<kanji>.txt` line 6; 但 has no character entry, as `但.md:25` says). So the batch rule above does not call for them. All are among the `--extra` readings in `checks\reading-exposure.txt` line 1, and none can be offered as a wrong answer in the N1 stack, the All stack or the Starter practice session (line 264). Three of them are latent only: 傷 そこなう via 損 and 残 (line 104), 吐 ぬかす via 抜 (line 173) and 哀 かなしむ via 悲 (line 206). |
| O7 | **declined** | all cards (unchanged) | These are parts of the current card layout, not of this batch alone. The sentence `Being outside the practice set is not proof that a reading is invalid.` is in all 15 cards of this batch and in 42 published cards. A closing `For reference, more Daijisen examples …` bullet is in 11 cards of this batch and in 10 published cards. Trimming or collapsing them is a presentation change for the whole collection, outside this revision. |

## Limits points

### LW: "卸 Daijisen headword"

Author action: **evidence added; no card change for this point.**

- `evidence\weblio-卸-daijisen.txt` holds the Weblio 卸 page's only Digital Daijisen block, verbatim and flattened, with
  the page URL, retrieval time and the sha256 of the cached raw HTML. The block's headword is おろし【卸（し）】, and the
  page has no ［音］ or ［訓］ block for 卸, so it has no Daijisen character entry. The definition text is
  `《「下ろし」と同語源》問屋が商品を小売店に売り渡すこと。「―の値段」`.
- Why the original packet's files miss it (the evidence file explains both): `evidence\public-source\weblio-卸.txt` came
  from a separate retrieval that kept only the page header text before the block. `evidence\daijisen-heads.txt` lists
  only headwords whose bracketed form list contains the queried form exactly; the tool removes the parentheses, so
  卸（し） is compared as 卸し and is not listed under 卸.
- `卸.md:25` was reworded for another reason; see the last section.

To verify: that the evidence supports line 25's statements that the page has no character entry for 卸 and that its
only Daijisen entry is おろし, written 卸 or 卸し.

### LE: "Labels in the exposure audit"

Author action: **no change in this round.** As you say, the label is the tool's, not the cards'. The tool labels every
`--extra` reading `(card text)`. Line 2 of `checks\reading-exposure.txt` states where the extras actually come from:
Kanjipedia's outside-table readings, Daijisen kun readings and ▽ headword readings, and JMdict kanji-plus-okurigana
headword readings. The tool is left unchanged for this round so that its output stays comparable with the original
packet's `evidence\audits\reading-exposure.txt`, which differs from this packet's only in line 1.

## Other limits in your report

No disposition is needed for these.

- Your notes on 丁 to 卸 were summarized after a context compaction. Of those eight cards, 丁, 仰, 但, 傑, 僕 and 卸 changed
  and are in `snapshot\kanji\` in full; 井 and 傷 did not change.
- The Android JVM content tests and the Kotlin reading-audit cross-check were not run for this revision either (see
  `CHANGES.md`).

## Changes that do not answer a point in your report

They are listed in `CHANGES.md`; review them like any other changed hunk.

- **仰: Kansai dialect** (`仰.md:59`). The reference example 仰山 ぎょうさん, "a lot; plenty; abundant; great many," now
  ends `which JMdict marks as Kansai dialect in this sense and as usually written in kana.` (it said only `as usually
  written in kana`). Support: `evidence\jmdict-cited-entries.xml`, entry 1238920 (sense 1 carries
  `<dial>Kansai-ben</dial>`; sense 2, "exaggerated; grandiose", has no dialect tag).
- **卸: what the Daijisen おろし entry defines** (`卸.md:25`). The definition is now described as `the act of a wholesaler
  selling goods to retail shops` (it read `a wholesale dealer selling goods to retail shops`). The Daijisen text is
  `問屋が商品を小売店に売り渡すこと`, an act (こと) whose actor is the wholesaler (問屋); see
  `evidence\weblio-卸-daijisen.txt`.

## Process notes

- `2bc8e9b1` is the only fix commit; `diffs\fix.patch` is the whole change from the reviewed snapshot `d3c7394d`.
- The checks in `checks\` were run on the committed revision.

# Author's statement for the reviewer of `reports-111\initial-claude.md`

This statement answers only the points in YOUR initial report. IDs F1 and F2 are your report's own labels. Your Optional
section is a numbered list; the author calls its points 1 to 4 **O1** to **O4**, and the three sub-points of your point 2
**O2(a)** (眼鏡 がんきょう), **O2(b)** (眼鏡 written in kana) and **O2(c)** (めいきょう as the usual reading of 明鏡). **L1** is
a question the author adds, based on your Assumption (a) (the leading hyphen of a kun reading). The statement is the
author's claim about what changed and why. Verify each claim against the revised card text in `snapshot\kanji\`,
`diffs\fix.patch` and independent sources; do not rely on this text as evidence. Line numbers refer to the revised cards in
this packet. Six of the 15 cards changed (房 敷 節 義 評 鏡) and the other nine did not (see `CHANGES.md`). Give a
disposition for each of F1, F2, O1, O2(a), O2(b), O2(c), O3, O4 and L1.

## Findings

### F1 (low): 敷地 is filed under the suffix reading -し.き, and the card defines the dash wrongly

Author action: **changed.** Both of your remedies were applied together, with one difference: the card does not say that
しき is the stem form of 敷く, because no source in the packet states that analysis.

- `敷.md:34`: 敷地 now stands in the し.く row: `[敷地](../words/敷地.md) しきち — site; plot; grounds`.
- `敷.md:35`: the -し.き row is typed `kun suffix` (it was `kun, bound form`; `氏.md:32` and `始.md:30` in the original
  packet's `repo\kanji\` use the same type) and lists only 座敷 and 風呂敷, in which しき follows another element.
- `敷.md:37`: the dash sentence now reads `The leading dash in -し.き marks a suffix use, one that follows another element;
  it is not pronounced.` A new sentence says `In 敷地, 敷 reads しき at the start of the word, as in 敷居 and 敷金`.
- `敷.md:39`: new sentences say where the card files each word and why, starting `The Daijisen lists its しき words in two
  groups separated by a slash: words that begin with 敷`. The Daijisen extract (`evidence\public-source\weblio-敷.txt` in the
  original packet) prints the slash but does not label the groups; the labels are the author's description of where 敷
  stands in the words listed on each side. The other support for the placement is the Joyo table, which has no separate しき
  row (`evidence\joyo\p134.txt`, lines 39 to 41).
- Disclosures. The Joyo table files 屋敷, which stands in the Daijisen's second group (words that end with 敷), under しく
  (`p134.txt`, line 41); the card reports that listing at `敷.md:39` and does not list 屋敷 in its table. `content-format.md`
  line 89 (original packet `repo\docs\`) says only that kunyomi uses "-" for affixes; it states no side (see L1). The
  repository is not uniform: `稲.md:33` (original packet `repo\kanji\`) still reads `kun, bound form`, `編.md:45` says "a
  bound use" and `御.md:31` reads `kun prefix`; none of these cards is in this batch. No sentence in the 15 batch cards now
  says "bound form", "inside compounds", "bound use" or "kun prefix" (author's script check).
- The same dash wording stood in the -ぶし row of 節, so `節.md:36` and `節.md:39` were changed in the same way. Please check
  those two hunks as well.

To verify: that placing 敷地 in the し.く row is defensible on this evidence without the stem-form claim; that the dash
sentence is accurate; that `敷.md:39` matches the Daijisen extract; and that no remaining sentence of `敷.md` contradicts
lines 34 to 39.

### F2 (low): 鏡 "lens" in the title is not a meaning of 鏡

Author action: **declined.** The title is unchanged: `title: mirror; lens` (`鏡.md:3`).

- Kanjipedia's entry for 鏡 lists the sense ②「めがね。レンズ。」 (`evidence\kanjipedia-鏡.txt`, line 20; the first three lines
  of the file record the source URL, the retrieval time and the method). The card does not cite Kanjipedia; the file is
  supplied so that this answer can be checked, and public web sources are allowed this round.
- JMdict glosses 鏡面 (1238590) "mirror surface; lens surface" (`evidence\jmdict-cited-entries.xml`; the id is in the card's
  Metadata line, `鏡.md:56`).
- The Daijisen's second キョウ sense is an instrument that uses lenses (`レンズ を 用いた 器具` in the original packet's
  `evidence\public-source\weblio-鏡.txt`), as `鏡.md:23` and `鏡.md:25` say.
- Collision check over all 1,176 cards: 器, whose title is `vessel; instrument`, is the only card whose title contains
  "instrument"; "lens" occurs only in 鏡's title; no title contains "scope", "optical" or "glass". A title such as "mirror;
  optical instrument" would therefore overlap 器 and need a new quiz exclusion.
- Conceded: KANJIDIC2 lists "mirror", "speculum", "barrel-head" and "round rice-cake offering" for 鏡 and no "lens"
  (`evidence\kanjidic2-records.xml` in the original packet), and no English source in the packet glosses 鏡 itself as
  "optical instrument" or "-scope". JMdict does gloss compounds ending in 鏡 with "-scope" words (顕微鏡 1260660
  "microscope", 望遠鏡 1519650 "telescope"; both in `evidence\jmdict-cited-entries.xml`), which supports your reading of the
  Daijisen sense as a description of those compounds.

Give a disposition: `DECLINE ACCEPTED` or `DECLINE REJECTED`. If rejected, please name the title you would accept.

## Optional points

| ID | Author action | Where | Reason |
| --- | --- | --- | --- |
| O1 | **changed** | `房.md:25` | The sentence now reads `and the old province of Awa, as in 房州 and 房総. JMdict has the province name as 安房 あわ`, and the next sentence begins `For ふさ the Daijisen gives`. The Daijisen's fourth ボウ sense (`evidence\public-source\weblio-房.txt` in the original packet) prints 安房 (あわ)国 and illustrates it with 房州 and 房総, without readings; the gloss of 安房 あわ is JMdict's and is now attributed to JMdict. Your suggested reading ぼうそう for 房総 was not added: neither 房州 nor 房総 occurs in the original packet's `evidence\jmdict-families.xml` (every JMdict entry written with 房), and the Daijisen prints no reading for either, so the packet has no source for it. The card claims only what the Daijisen lists. |
| O2(a) | **changed** | `鏡.md:25`, `鏡.md:39`, `鏡.md:56` | Instead of a parenthesis, line 25 now gives the Daijisen's キョウ word with its own reading and gloss, `眼鏡 がんきょう, "glasses; eyeglasses; spectacles,"`, which is the separate JMdict entry 2862467 (added to the Metadata list at line 56; in `evidence\jmdict-cited-entries.xml`). Line 39 adds `The Daijisen lists 眼鏡 twice: once among its キョウ words, where it matches the separate JMdict entry 眼鏡 がんきょう, and once among its hard-to-read words, as めがね.` |
| O2(b) | **declined** | `鏡.md:39` | No statement of the card depends on how 眼鏡 is usually spelled. The card's point is that JMdict marks めがね as gikun or jukujikun, a reading assigned to the whole word, so the word gives 鏡 no reading of its own; a note on kana spelling would add an orthographic fact that supports no claim. |
| O2(c) | **declined** | `鏡.md:34`, `鏡.md:37` | The card does not say which reading of 明鏡 is the usual one. Line 25 already gives 明鏡 めいきょう as a Daijisen キョウ word, and line 37 explains the ケイ row: it rests on JMdict, which lists めいけい as the third reading of 明鏡 after めいきょう and みょうきょう. The row itself (line 34) is marked `no word article yet, not selected for questions here`. |
| O3 | **declined** | `checks\reading-options.txt`, lines 162-175 | Your report says it is not required. The 義 section shows the same figures as for the reviewed snapshot: 143 wrong options seen over 400 seeds, 0 seeds with fewer than three, 0 problems. The readings of 義 are unchanged. |
| O4 | **declined** | `words\節約.md` | The article is not among the files changed in this revision (`diffs\changed-files.txt`). Your report calls its title context, not scope. |

## Limits

### L1: the side of the leading dash (your Assumption (a); author's question)

Your Assumption (a) says that a leading "-" in a KANJIDIC2 kun reading means a suffix, "as in KANJIDIC2's own convention
and the repo's content-format". The wording now in `敷.md:35`, `:37` and `:39` and in `節.md:36` and `:39` relies on that.
What the sources say: `content-format.md` line 89 (original packet `repo\docs\`) says only that kunyomi uses "-" for affixes,
and KANJIDIC2's DTD (https://www.edrdg.org/kanjidic/kanjidic2_dtdh.html, the `ja_kun` entry) says only that readings
associated with prefixes and suffixes are marked with a hyphen; neither names the side. The author's understanding is that
the side is positional and that the repository's cards follow it: a leading hyphen for a suffix (`混.md:49`, `氏.md:32`,
`始.md:30`) and a trailing hyphen for a prefix (`御.md:31`, `お-`), all in the original packet's `repo\kanji\`. The dashed
readings in question are in `evidence\kanjidic2-records.xml` (original packet): 敷 し.く and -し.き; 節 ふし, -ぶし and のっと.

To verify and answer: whether the cards' present wording of the leading dash is correct, and a disposition for L1 itself:
`RESOLVED` (nothing remains open), or a statement of what remains.

### Other limits in your report

The two-call overlap you disclosed, the call with a wrong supplement path, the partial reads of the rubric and of
`content-format.md`, the source of your line numbers and your Assumption (b): no action is claimed and no disposition is
needed. Two facts for this round: public web sources are allowed (`INSTRUCTIONS.md`), so you can open Kanjipedia's page for
鏡 yourself (its text as retrieved by the author is in `evidence\kanjipedia-鏡.txt`); and the Android JVM content tests were
not run for this revision either (see `CHANGES.md`).

## Changes that do not answer a point in your report

They are listed in `CHANGES.md`; please review them like any other changed hunk. Each states what the author claims and why.

- `節.md:14`, `:25` and `:56`: 句 and 旬 were added to 節's `quiz_exclusions`, and the card text was extended to match. The
  titles are 節 `joint; season; restraint`, 句 `phrase; verse` and 旬 `ten days; peak season`. 節 and 旬 share "season" in their
  titles. 節 and 句 share "verse": it is in 句's title, in KANJIDIC2's meanings for 節 ("verse", "clause", "stanza") and in
  the second sense of JMdict 1386140, the separate noun 節 せつ ("section (of a literary work or piece of music); passage;
  paragraph; verse; stanza"); KANJIDIC2's meanings for 句 include "clause", "passage" and "paragraph". Line 25 now shows
  that second sense, and line 56 names 句 and 旬 and adds "verse" to the overlapping senses. Each pair is declared once, on
  節's side; `excluded(a, b)` in `evidence\QuizBuilder.kt` is true if either card lists the other, so both directions are
  guarded. `句.md` and `旬.md` are unchanged, and no 句/旬
  exclusion was added. The three wrong options shown for 節, 句 and 旬 are unchanged (`checks\quiz-safety.txt`, lines 22, 3
  and 12).
- `義.md:14` and `:52`: 税 was removed from 義's `quiz_exclusions` and from the overlap bullet. 税's title is `tax; fiscal
  duty`; its "duty" is a levy, a different English sense from the "duty" (obligation) that 義 and 義務 carry, so listing 税
  among the cards that overlap that sense was not accurate. `税.md` is unchanged, and neither card lists the other in
  `quiz_exclusions` or `distractors`.
- `評.md:35`: `in 評判, 判 supplies バン, an on reading of 判 besides ハン` (it read `in 評判, 判 supplies ハン`). 評判 is read
  ひょうばん (JMdict 1490070), and バン is a listed on reading of 判 (`evidence\kanjidic2-judge.xml`: ハン and バン; original
  packet `repo\kanji\判.md:9` and `:34`).

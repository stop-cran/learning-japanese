# Author's statement for the reviewer of `reports-111-gpt\initial-gpt.md`

This statement answers only the points in YOUR initial report. Your report numbers its findings 1 and 2; the author's
labels are: Finding 1 = **#1** (the pairs 節/句 and 節/旬) and Finding 2 = **#2** (税 in the exclusions of 義). The two
bullets of your Optional list are **OA** (compress the dictionary and exclusion explanations of 義) and **OB** (the 評判
reading in 評). The first bullet under Limits is **L1** (supplied Python ports, no executed Android client); the remaining
three Limits bullets (the second, third and fourth) are **L2**. The statement is the author's claim about what changed and
why. Verify each claim against the revised card text in `snapshot\kanji\`, `diffs\fix.patch` and independent sources; do
not rely on this text as evidence. Line numbers refer to the revised cards in this packet. Six of the 15 cards changed
(房 敷 節 義 評 鏡) and the other nine did not (see `CHANGES.md`). Give a disposition for each of #1, #2, OA, OB and L1; L2
needs none.

## Findings

### #1 (minor): two missing direct exclusions involving 節

Author action: **changed, once per pair, on 節 only.** Both pairs you named were declared, and no 句/旬 exclusion was
inferred.

- `節.md:14`: `quiz_exclusions: [季, 春, 期, 接, 制, 倹, 限, 際, 祭, 部, 句, 旬]`. 句 and 旬 are the two additions; the list
  ended at 部 before. `句.md` and `旬.md` are unchanged: their `quiz_exclusions` are still `[文, 語, 詞, 辞, 言, 俳]` and
  `[季, 期, 十, 春, 月, 日]`.
- Symmetry: `excluded(a, b)` in `evidence\QuizBuilder.kt` (line 26) is true if either card lists the other, so one
  declaration guards both directions, and the repository lists each pair once. The documented structural rules for the
  field (no overlap with the card's own `distractors`, no missing or duplicate IDs; `content-format.md`, original packet
  `repo\docs\`) hold: 節's `distractors` are `[雪, 殺, 笑]`, and the validator reports 0 errors (`checks\validate.txt`).
- Basis for the pairs. The displayed titles are 節 `joint; season; restraint`, 句 `phrase; verse` and 旬 `ten days; peak
  season`. 節 and 旬 share "season" in their titles, and KANJIDIC2 gives 旬 "season (for specific products)". 節 and 句
  share "verse": it is in 句's title, KANJIDIC2 lists "verse", "clause" and "stanza" for 節, and the second sense of the
  separate JMdict noun 節 せつ (1386140) is "section (of a literary work or piece of music); passage; paragraph; verse;
  stanza". The overlap you described is the one in a 節 question; the declaration is symmetric, so it also applies when 句
  is the target (the field cannot name one direction only).
- `節.md:25` now ends `The separate noun 節 せつ, which has no word article here, is glossed "occasion; time" in its first
  JMdict sense and "section (of a literary work or piece of music); passage; paragraph; verse; stanza" in its second.`
  `節.md:56` now names the two cards with their titles, `[句](句.md), "phrase; verse," and [旬](旬.md), "ten days; peak
  season,"`, and adds "verse" to the overlapping senses.
- All-card scan (author's script, all 1,176 cards): 節 is the only card that lists 句 or 旬 in `quiz_exclusions`; no card
  lists 句 or 旬 in `distractors`; 句 and 旬 list neither each other nor 節. The three wrong options shown for 節, 句 and 旬
  are unchanged (`checks\quiz-safety.txt`, lines 22, 3 and 12).
- Custom-pool exposure: see L1.

To verify: that each pair is justified by the cited evidence and is not over-broad (including the symmetric direction),
that no 句/旬 exclusion is needed, and that 節, 句 and 旬 keep three defensible wrong options.

### #2 (minor): 義 conflates fiscal duty with obligation

Author action: **changed, by removal.** The other remedy you offered (keep 税 as a teaching comparison and explain fiscal
duty versus obligation) was not taken.

- `義.md:14`: `quiz_exclusions: [役, 務, 意, 理, 正, 替, 敬]` (税 was the eighth entry).
- `義.md:52`: the overlap bullet no longer names 税. It now begins `[役](役.md), "role; duty," and [務](務.md), "duties,"
  overlap the sense "duty" that 義 and 義務 carry`. No line of `義.md` mentions 税 any more (author's script check).
- `税.md` is unchanged: its title is `tax; fiscal duty`, and the original packet's `repo\kanji\税.md:20` says that English
  duty there means a monetary tax, not a person's general obligation. With the exclusion gone, 税 can again appear among
  the fallback options of 義, and 義 among those of 税. Neither card lists the other in `quiz_exclusions` or
  `distractors` (義 `[議, 疑, 技]`; 税 `[祝, 況, 説]`, and 税 has no `quiz_exclusions`). The three wrong options shown for
  義 are unchanged (`checks\quiz-safety.txt`, line 25).

To verify: that `義.md` no longer states or implies the fiscal-duty comparison, and that 義 keeps defensible wrong options.

## Optional points

| ID | Author action | Where | Change |
| --- | --- | --- | --- |
| OA | **declined** | `義.md:52` | Editorial. The bullet changed only by losing the 税 clause (#2): it is 101 words long, counted as whitespace-separated tokens (105 before), and the longest prose paragraph of the card is 81 words (`義.md:25`), before and after. The teaching paragraphs come first, as your report notes, and the bullet only records which cards are kept out of the quiz options and why. |
| OB | **changed differently** | `評.md:35` | The text now reads `in 評判, 判 supplies バン, an on reading of 判 besides ハン` (it read `in 評判, 判 supplies ハン`). The card does not call it a sound change: バン is itself a listed on reading of 判 (`evidence\kanjidic2-judge.xml`: ハン and バン; original packet `repo\kanji\判.md:9`, `onyomi: [ハン, バン]`, and the バン row at `:34`, which lists 評判 ひょうばん), and no source in the packet says that the バン of 評判 is a voiced form of ハン. 評判 ひょうばん is JMdict 1490070 (`evidence\jmdict-cited-entries.xml`). The 論評 sentence, `In 論評 ろんぴょう, the sound changes to ぴょう after the ン of 論.`, is unchanged. |

## Limits

### L1: supplied Python ports, no executed Android client (UNVERIFIED in your report)

Your first Limits bullet says that the quiz audits are supplied Python ports, not an executed Android client, and that the
custom-pool consequence of your Finding 1 is unverified on a device. The packet now carries the app's own sources, taken
from the Android checkout at commit `10d98d0`: `evidence\QuizBuilder.kt` (the meaning quiz) and `evidence\KanjiReadings.kt`
and `evidence\Words.kt` (the reading quiz); `evidence\README.md` describes each of them. In `QuizBuilder.kt`,
`excluded(a, b)` (line 26) is true if either card lists the other, and `tryAdd` (lines 28 to 32) returns without choosing a
candidate that is excluded against the target or against any option already chosen (line 30). The curated `distractors`
go through `tryAdd` (line 34), and so do the tag-ordered fallback candidates (line 36). The file does not show how a custom
pool is built and passed in as `all`, so the author makes no claim about which cards a given pool holds; the guard
applies to every candidate that reaches `tryAdd`. The field's documented contract (the original packet's
`repo\docs\content-format.md`, lines 102 to 107) says the same for All, level and custom pools: a declaration on either
card excludes the pair among curated and fallback choices, and a small pool may yield fewer choices.

Caveats: `checks\quiz-safety.txt` is the author's audit of the displayed meaning options of the 15 cards, and
`checks\reading-options.txt` and `checks\reading-exposure.txt` are author-written ports of the reading-quiz option logic.
The audit pool is every card in `kanji\`, and the audits' random generator is not the app's, so they report candidate sets
and not exact draws. The two reading audits were rerun on the revised snapshot and their output is identical to the output
supplied for the reviewed snapshot, including the six latent collisions that you read as illustrations only. No APK and no
running phone UI is supplied, and the Android JVM content tests were not run for this revision either (see `CHANGES.md`).
One compatibility fact: `quiz_exclusions` are honoured only by app builds from the commit "Honor explicit kanji meaning
pair exclusions" (`2edbf36`) onward, which the `10d98d0` checkout contains; no claim is made about what any installed
build does.

To verify and answer: whether reading `QuizBuilder.kt` settles the custom-pool consequence of #1, what still cannot be
shown, and a disposition for L1 itself: `RESOLVED` (nothing remains open), or a statement of what remains.

### L2: other limits in your report

Your second Limits bullet (the Joyo PDF itself was not rendered): `evidence\joyo\p<N>.txt` are the text extracts of the
pages for the six changed cards (pages 34, 39, 93, 132, 134 and 142: 義, 鏡, 節, 評, 敷 and 房), and `evidence\README.md`
gives the PDF's SHA-256 and URL; public web sources are allowed, so you can open the page at
`...joyokanjihyo_20101130.pdf#page=N` yourself. The third bullet (live public dictionaries, the kanjiapi HTTP 403) and the
fourth (bounded queries, spill files not opened): no action is claimed and no disposition is needed.

## Changes that do not answer a point in your report

They are listed in `CHANGES.md`; please review them like any other changed hunk. Each states what the author claims and why.

- `房.md:25`: the Daijisen's ボウ sense for the old province of Awa is now illustrated with 房州 and 房総, which the
  Daijisen prints without readings, and the gloss of 安房 あわ is attributed to JMdict: `and the old province of Awa, as in
  房州 and 房総. JMdict has the province name as 安房 あわ`. The next sentence begins `For ふさ the Daijisen gives`.
- `敷.md:34`, `:35`, `:37` and `:39`, and `節.md:36` and `:39`: 敷地 is now listed in the し.く row,
  `[敷地](../words/敷地.md) しきち — site; plot; grounds`, because its しき begins the word. The -し.き row of 敷 and the
  -ぶし row of 節 are typed `kun suffix` (they read `kun, bound form`), and `敷.md:35` lists only 座敷 and 風呂敷, in
  which しき follows another element. The dash sentences now read `The leading dash in -し.き marks a suffix use, one that
  follows another element; it is not pronounced.` (`敷.md:37`) and `The leading dash in -ぶし marks a suffix use, one that
  follows another element; it is not pronounced.` (`節.md:39`); they said "bound form, one that appears inside compounds".
  `敷.md:37` adds `In 敷地, 敷 reads しき at the start of the word, as in 敷居 and 敷金`, and `敷.md:39` adds `The Daijisen
  lists its しき words in two groups separated by a slash: words that begin with 敷`. The Daijisen extract
  (`evidence\public-source\weblio-敷.txt` in the original packet) prints the slash but does not label the groups; the
  labels are the author's description of where 敷 stands in the listed words. The Joyo table has no しき row and files 屋敷
  under しく (`evidence\joyo\p134.txt`, lines 39 to 41), which `敷.md:39` reports. KANJIDIC2's DTD
  (https://www.edrdg.org/kanjidic/kanjidic2_dtdh.html, the `ja_kun` entry) says only that readings with prefixes and
  suffixes are marked with a hyphen, without naming a side; the side in these cards is the author's understanding of the
  repository's convention (`混.md:49`, `氏.md:32` and `始.md:30` in the original packet's `repo\kanji\`).
- `鏡.md:25`, `:39` and `:56`: `眼鏡 がんきょう, "glasses; eyeglasses; spectacles,"` is added at line 25 (the separate JMdict
  entry 2862467, added to the Metadata list at line 56 and held in `evidence\jmdict-cited-entries.xml`), and line 39 adds
  `The Daijisen lists 眼鏡 twice: once among its キョウ words, where it matches the separate JMdict entry 眼鏡 がんきょう, and
  once among its hard-to-read words, as めがね.`

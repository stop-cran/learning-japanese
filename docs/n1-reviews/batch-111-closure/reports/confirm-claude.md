# Batch 111 — confirmation review (Claude)

Reviewer: Claude Opus 5.5 (model ID claude-opus-5.5). This is the first-round reviewer confirming the author's revision. I worked blind and read-only.

## Snapshot

- Revised snapshot: commit bf9ee9622723078438a021d54cac5ce8252f95d8.
- Parent (reviewed in round 1): 3b30803e33438dab7a1071aea34ceb7764189c1f.
- Changed files (diffs\changed-files.txt): kanji/房.md, kanji/敷.md, kanji/節.md, kanji/義.md, kanji/評.md, kanji/鏡.md and manifest.json.
- Unchanged: the other nine cards (修 句 授 旬 標 独 率 製 養), every stroke file and every word article.

## Scope

**Confirmation packet** `confirm-111-bf9ee962-claude\`:
- INSTRUCTIONS.md, CHANGES.md, RESPONSE.md: read in full.
- diffs\fix.patch: read in full, in line ranges.
- diffs\changed-files.txt: read in full.
- snapshot\kanji\房.md, 敷.md, 節.md, 義.md, 評.md, 鏡.md: read in full.
- evidence\README.md: read in full.
- evidence\jmdict-cited-entries.xml: read in part. I extracted the entries for 1386140 (節 せつ), 2862467 (眼鏡 がんきょう), 1577670 (眼鏡 めがね), 1490070 (評判) and 1238590 (鏡面).
- evidence\kanjipedia-鏡.txt: read in full.
- evidence\kanjidic2-judge.xml: read in full.
- evidence\QuizBuilder.kt and evidence\KanjiReadings.kt: read in full.
- evidence\Words.kt: read in part (the `mutations` function, the voicing tail and `closeness`).
- checks\quiz-safety.txt, checks\link-targets.tsv, checks\validate.txt and checks\unittest.txt: read in full.
- checks\reading-options.txt: read in part. I grepped every section header, the note lines and the summary, and read lines 56–69 (敷), 141–175 (節 and 義) and 215–237 (鏡).
- checks\reading-exposure.txt: read in part (its last 3 lines, including the summary).
- Non-recursive listings of the packet root and of evidence\, checks\ and diffs\.
- Not opened: checks\lint.txt, budget.txt, vocabulary.txt and manifest.txt; diffs\changed-lines.txt; packet-manifest.json; snapshot\kanji\ cards other than the six; evidence\joyo\*.

**Original packet** `batch-111-3b30803e\`:
- evidence\public-source\weblio-敷.txt and weblio-鏡.txt: read in full.
- repo\kanji\税.md, 句.md and 旬.md: read in part (the first 15 lines, front matter only).

**Own report:** reports-111\initial-claude.md, consulted for the finding IDs.

**Public web:** I fetched the live Kanjipedia entry for 鏡 (https://www.kanjipedia.jp/kanji/0001550400).

## Dispositions

- **F1** (敷 filed 敷地 under -し.き and called the dash a "bound form"): **RESOLVED**.
  - Line 34: the し.く row now lists 敷く and 敷地.
  - Line 35: the -し.き row is "kun suffix" with 座敷 and 風呂敷.
  - Line 37: says that in 敷地 the しき comes at the start of the word, as in 敷居 and 敷金, and defines the dash as "suffix use, one that follows another element".
  - Line 39: the Daijisen quotation matches weblio-敷.txt: 〈しき（じき）〉「敷居・敷金・敷地・敷布／座敷・屋敷・河川敷・千畳敷・風呂敷」. The "begin with" and "end with" labels for the two groups are accurate.
  - No untouched line now contradicts this.
  - The reading quiz is consistent: the stem rule (`ReadingKey.stem`) folds -し.き into し.く, so only one kun prompt (し.く) exists.
  - The same suffix wording was applied to 節 lines 36 and 39. 削り節 けずりぶし follows another element, so that wording is correct too.
- **F2** (鏡 title "mirror; lens"): **DECLINE ACCEPTED**.
  - I checked the live Kanjipedia page (漢検協会). It gives sense ②「めがね。レンズ。」 with 眼鏡 as the example, so "lens" is an attested dictionary sense of the kanji even though KANJIDIC2's English meanings do not include it.
  - Supporting sources: JMdict 鏡面 1238590 glosses "lens surface", and the Daijisen gives sense ２ as 「レンズを用いた器具」.
  - Quiz safety: the meaning options for 鏡 are boundary; border | silver | dull; blunt. None overlaps with mirror or lens.
  - My alternative wording ("instrument") would have collided with 器 "vessel; instrument", so the current title is the better choice.
- **O1** (房 Awa attribution): **RESOLVED**.
  - Line 25 now reads "as in 房州 and 房総. JMdict has the province name as 安房 あわ".
  - The JMdict data is attributed to JMdict, and the ふさ words are attributed to the Daijisen.
- **O2(a)** (鏡 がんきょう): **RESOLVED**.
  - Line 25 cites 眼鏡 がんきょう "glasses; eyeglasses; spectacles". These are exactly the glosses of JMdict 2862467, and the id is on the Metadata line.
  - New line 39: "The Daijisen lists 眼鏡 twice". This matches weblio-鏡.txt, which has 眼鏡 under キョウ sense ２ and under ［難読］ as 眼鏡(めがね).
  - It is consistent with the Joyo remark on line 41.
- **O2(b)** (kana spelling of 眼鏡): **DECLINE ACCEPTED**. This was polish only, and no claim on the card depends on it. JMdict 1577670 confirms めがね and メガネ.
- **O2(c)** (めいきょう as the usual reading of 明鏡): **DECLINE ACCEPTED**. Line 25 gives めいきょう, Kanjipedia gives 明鏡(メイキョウ), and line 37 already explains the ケイ row.
- **O3** (義 reading quiz: the three curated options are all ギ): **DECLINE ACCEPTED**.
  - reading-options.txt lines 165–174: all three curated options are skipped as excluded, and the fallback fills the slots.
  - The fallback shows 143 distinct wrong options over 400 seeds, with 0 seeds short of three options and 0 problems. There is no unsafe or degenerate prompt.
- **O4** (the 節約 word title): **DECLINE ACCEPTED**. The word article is unchanged and outside the unit under review.
- **L1** (which side of the dash means suffix): **RESOLVED**.
  - The cards now say that a leading dash marks suffix use, one that follows another element. This matches the KANJIDIC2 and EDICT convention that the hyphen stands on the side where the other element attaches.
  - It also matches repo practice: 御 uses お- for a prefix.
  - The DTD text itself does not name the side, so this rests on convention. That is acceptable.

## Verdicts

Facet verdicts apply to the six changed cards and to the post-fix quiz and reading options for all 15 cards.

- **Facet 1, correctness: CLEAN.**
  - 評 line 35 changed from "判 supplies ハン" to "判 supplies バン, an on reading of 判 besides ハン". This fixes an error I missed in round 1. KANJIDIC2 判 (kanjidic2-judge.xml) has ja_on ハン and バン, and JMdict 1490070 gives 評判 as ひょうばん.
  - 節 line 25 quotes JMdict 1386140 sense 2 verbatim: "section (of a literary work or piece of music); passage; paragraph; verse; stanza".
  - 鏡 and 房: correct, as described under Dispositions.
- **Facet 2, scoped coverage: CLEAN.** No row or reading was lost. The し.く row gained 敷地, and the -し.き row keeps 座敷 and 風呂敷.
- **Facet 3, consistency and quiz safety: CLEAN.**
  - quiz-safety.txt: the meaning options for all 15 cards are unchanged and reach 0 errors and 0 warnings. I re-judged them in both directions and found none that is defensibly correct.
  - 節 quiz_exclusions gained 句 and 旬. These are real direct overlaps: 節 means verse or stanza, sharing "verse" with 句, and season, sharing "peak season" with 旬. `excluded()` in QuizBuilder.kt is symmetric, so declaring them on one side is enough.
  - 義 dropped 税 from quiz_exclusions and from Notes line 52. 税 "tax; fiscal duty" names a levy, not a moral duty, so "righteousness; duty; meaning" is defensibly wrong for 税. In the other direction, 税 keeps three curated distractors (祝 況 説) with no fallback, so 義's title cannot appear among 税's options.
  - link-targets.tsv: 23 links on changed lines, 0 mismatches, and every quoted title equals the target card's title.
  - validate.txt: 0 errors. unittest.txt: 431 tests OK.
  - reading-options.txt: 0 problems.
  - reading-exposure.txt: 0 production hits and 0 padded-session hits. The 6 latent collisions (房 お and わ, 節 よ, 養 や, 鏡 あき) are unchanged and fall in a lower closeness tier, so they cannot be drawn.
  - I checked the excludedKeys and mutation logic against KanjiReadings.kt and Words.kt.
- **Facet 4, comprehensibility: CLEAN.** The revised sentences are short, gloss their terms and put the central idea first.

## Confirmation

**CONFIRMED.** Every round-1 item is either RESOLVED or DECLINE ACCEPTED, and I found no new actionable defect.

## Findings

None.

## Optional

1. 敷 lines 34 and 37: one clause such as "しき is the noun form of 敷く" would show a beginner why 敷地 しきち sits in the し.く row rather than the -し.き row. The current wording is correct without it.
2. 房 line 25: kana for 房州 (ぼうしゅう) and 房総 (ぼうそう) would help an N5–N4 reader. These are standard readings in public dictionaries.
3. 鏡 on prompt キョウ (reading-options.txt lines 221–227): only 3 distinct wrong options appear over 400 seeds (ぎん, どん and the single tier-4 きゅう), so the prompt is fully predictable. It is safe, unchanged from round 1 and polish only.

## Limits

- **Contract slip:** one response, at about 16:15:39 UTC, contained two view calls in parallel (fix.patch lines 60–140 and 115–125). Every other response made exactly one call.
- My first PowerShell call printed fix.patch plus a listing. The tool saved its oversized output to a temporary file outside the allowed paths. I did not open that file and re-read fix.patch through the allowed path instead.
- One PowerShell call failed harmlessly (a Substring length error) and was re-run.
- **Not re-opened:** the evidence\joyo\ extracts. My reading of fix.patch shows no changed hunk that adds or alters a claim about the Joyo table; the Joyo claims that remain were verified in round 1.
- I did not re-read the nine unchanged cards. I relied on the packet's statement and on changed-files.txt that they are byte-identical.
- The Android JVM content tests were not run at this snapshot. This is a known limit of the packet.
- The audits draw from the full 1,176-card pool, while the app draws from the cards the learner has studied. Their RNG also differs from the app's, so the audit shows which options are possible, not the exact ones the app will draw.
- **Assumption:** my reading of the side of the dash rests on the KANJIDIC2 and EDICT convention, not on explicit DTD wording.

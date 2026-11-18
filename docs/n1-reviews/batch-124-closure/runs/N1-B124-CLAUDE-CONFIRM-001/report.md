# B124 confirmation — N1-B124-CLAUDE-CONFIRM-001

## Snapshot
Commit: fa394d237e28df96319495a003718cc9c880a069
Model: runtime-reported Claude Opus 5.5 (claude-opus-5.5); execution-model identity not independently verified

## Scope
Chain: segments 1-21 of n1-b124-claude-confirm-001, each read once in order; no re-views
Fetches: none

## Dispositions
- F1 - RESOLVED - 広 is now a direct quiz_exclusions entry on 裕 (snapshot/kanji/裕.md:14) with a learner note (snapshot/kanji/裕.md:46); the overlap is supported by the card's own roominess teaching (snapshot/kanji/裕.md:23-25), 広's title and KANJIDIC2/JMdict spacious senses, and the attributed Weblio ひろ-い; one declaration on 裕 suffices because exclusions are symmetric direct pairs, and 広 is not a curated distractor, so no overlap with distractors arises.
- F2 - RESOLVED - snapshot/kanji/裕.md:33 now says Daijisen omits のり and ゆ and adds まさ and みち, which matches the Daijisen 名のり line (original-packet/evidence/external-snapshots/01-extract.txt:8) against the KANJIDIC2 nanori すけ, のり, ひろ, ひろし, やす, ゆ, ゆたか.
- O1 - DECLINE ACCEPTED - The author's no-guard decision for 余 is supported: KANJIDIC2 gives 余 too much/surplus/remainder and 余る/余分 are left over, excess, extra, while surplus/margin/leeway are whole-word 余裕 senses (JMdict 1544590), not 裕 character senses; my original point was optional with no defect established.
- O2 - RESOLVED - A direct 多 guard was added (snapshot/kanji/裕.md:14, snapshot/kanji/裕.md:46); JMdict 1407460 多い sense 2 gives large amount of, large quantity of, much, which supplies the dictionary evidence my optional point asked for and supports a quantity reading of "abundant".
- O3 - RESOLVED - snapshot/kanji/裕.md:33 now names the separate Wiktionary section (ユ 呉音・漢音, ユウ 慣用音, out-of-table kun ゆた-か and ひろ-い) and the 漢字辞典 section (ユウ, ユ, ゆたか, credited to KANJIDIC2), matching the extract, and keeps them out of metadata and quiz choices.

## Verdicts
Correctness: CLEAN
Scoped coverage: CLEAN
Consistency and quiz safety: CLEAN
Comprehensibility: CLEAN

## Confirmation
Verdict: CONFIRMED
Basis: Both findings are resolved by the actual fa394d23 changes and every optional point has an accepting disposition; the only changed card lines are the quiz_exclusions list (adding 多, 楽, 広), the rewritten source-comparison sentence and one new Notes line, all of which match the supplied KANJIDIC2, JMdict 1407460/1207230/1278410 and Weblio extract; the unrequested 楽 guard is supported by JMdict 1207230 sense 3 "(economically) comfortable"; curated distractors 容/補/複 and the sole quiz reading ユウ are unchanged and do not overlap the exclusions; committed host checks pass (lint, validate, quiz-safety, linkplan, reading-exposure, unittest, manifest, budget, vocabulary) within their stated bounds; no new established defect was found.

## Findings
None.

## Optional
### O1: KANJIDIC2 wealth glosses on 福 and 宝 remain unguarded by judgment
- Facet: Consistency and quiz safety
- Severity: optional
- Confidence: medium
- Citations: snapshot/docs/n1-sources/batch-124-reconciliation/kanjidic2-records.xml:971-974; snapshot/docs/n1-sources/batch-124-reconciliation/kanjidic2-records.xml:1053-1055; neutral-author-evidence/dispositions.json:27-45; snapshot/kanji/裕.md:14
- Evidence: The newly supplied KANJIDIC2 records list "wealth" among the meanings of both 福 (blessing, fortune, luck, wealth) and 宝 (treasure, wealth, valuables), which my initial review did not see. The author's Q1/Q5 no-guard decisions rely on the complete JMdict standalone families (福: good fortune, happiness, blessing, good luck; 宝: treasure), and the displayed titles "good fortune" and "treasure; valuables" do not present a wealth label. I accept that reasoning as sufficient for no defect, but the character-level gloss keeps a weak English association with 裕's "rich".
- Suggestion: Optionally record in the batch evidence that the KANJIDIC2 wealth glosses were weighed and declined, so future batches reusing "rich"/"wealth" titles revisit the same pairs consistently.

### O2: Disposition record normalizes some displayed titles
- Facet: Consistency and quiz safety
- Severity: optional
- Confidence: high
- Citations: neutral-author-evidence/dispositions.json:247; neutral-author-evidence/dispositions.json:268; neutral-author-evidence/dispositions.json:314; neutral-author-evidence/dispositions.json:353; snapshot/docs/n1-sources/batch-124-reconciliation/comparison-cards/楽.md:3; snapshot/docs/n1-sources/batch-124-reconciliation/comparison-cards/金.md:3; snapshot/docs/n1-sources/batch-124-reconciliation/comparison-cards/足.md:3; snapshot/docs/n1-sources/batch-124-reconciliation/comparison-cards/広.md:3
- Evidence: The contributor dispositions record candidateLabel values "music; enjoyment; ease", "gold; money", "foot; leg" and "wide; spacious", while the actual card titles are "music, enjoyment, ease", "gold, money", "foot, leg" and "wide, spacious". This is contributor evidence, not learner-facing text, and does not change any semantic decision.
- Suggestion: Optionally copy displayed labels byte-exactly into future disposition records so they can be matched mechanically to the cards.

## Limits
- L1: Raw stroke SVGs, the raw Weblio response HTML, the binary Joyo PDF and every input outside this 21-segment chain were not read; no geometry claim is made, and the stroke JSON is unchanged by the fix patch.
- L2: JMdict families are complete only for the exact selectors in the source receipt; KANJIDIC2 records cover the 18 listed characters. No other lexical family was checked, and characters outside the frozen comparison set were not reconsidered.
- L3: The 厚, 富, 豊 and 財 counterpart cards were re-read here unchanged; their existing guards were not re-adjudicated beyond confirming the cards and the initial evidence.
- L4: Committed check logs are bounded host models; caller-built, multi-borrow or arbitrary pools, Kotlin execution, native/device acceptance and compatibility with the older installed APK 5c000bd (which ignores quiz_exclusions) are not established.
- L5: Several citation line numbers in the reconciliation XML and dispositions JSON were derived by counting segment lines against the stated source/segment mapping, not from a line-numbered view; small offsets are possible, but the cited content was read directly.
- L6: The kanjiapi N1 snapshot was not opened; the N1 label remains bounded by source row 986.

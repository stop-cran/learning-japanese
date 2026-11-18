# B117 confirmation — N1-B117-CLAUDE-REPLAY-CONFIRM-006

## Snapshot
Commit: c5741ccdbce41ff4c8ba2cd7ed9de585561a38e7
Model: runtime-reported Claude Opus 5.5 (claude-opus-5.5); identity not independently verified

## Scope
Chain: segments 1-21 of n1-b117-claude-replay-confirm-006, each viewed once in order; no re-views
Fetches: none

## Dispositions


## Verdicts
Correctness: CLEAN
Scoped coverage: CLEAN
Consistency and quiz safety: CLEAN
Comprehensibility: CLEAN

## Confirmation
Verdict: CONFIRMED
Basis: The prior accepted report has no finding or optional item (previous-confirmation/N1-B117-CLAUDE-REPLACEMENT-CONFIRM-004.md:23-30), so no disposition is due; the actual delta touches only 維 among the scoped cards, replacing distractors [録, 催, 集] with [銀, 語, 休] and rewriting the two Notes that described them, while every quiz exclusion, on/kun/quiz metadata and the other prose stay unchanged (diffs/fix.patch:1-27; snapshot/kanji/維.md:9-14; snapshot/kanji/維.md:46; snapshot/kanji/維.md:50; snapshot/docs/n1-sources/batch-117/reconciliation-004/correction-receipt.json:6-8; coordinator/round4-source-verification.json:33-36), and the complete card contains no remaining reference to the old choices; the new choices are semantically distinct in both directions, because 銀 is silver (metal, colour, medal, historical coin, shogi and bank abbreviations, archaic money), 語 is word/term, language, speech and telling/narrating, and 休 is rest, day off, sleep/retire and suspending activity (snapshot/docs/n1-sources/batch-117/reconciliation-004/comparison-cards/銀.md:3; snapshot/docs/n1-sources/batch-117/reconciliation-004/comparison-cards/語.md:3; snapshot/docs/n1-sources/batch-117/reconciliation-004/comparison-cards/休.md:3; snapshot/docs/n1-sources/batch-117/reconciliation-004/kanjidic2-records.xml:1-376; snapshot/docs/n1-sources/batch-117/reconciliation-004/jmdict-families.xml:1-695), none of which is a defensible answer for 維's KANJIDIC2 fiber/tie/rope or Daijisen principle, cord/strand, hold-fast, corner and rhythm-particle senses (snapshot/docs/n1-sources/batch-117/reconciliation-004/kanjidic2-records.xml:1-80; original-packet/evidence/external-snapshots/03-extract.txt:16-25), and "fiber" is no defensible answer for any of them, so no new exclusion is required and the displayed meaning options become silver | language, word | rest (fresh-gates/quiz-safety.log:5-6); 維 has only the イ on prompt and no kun prompt (snapshot/kanji/維.md:11-12), each new card offers exactly one usable on reading, ギン, ゴ and キュウ, none of which equals or is a mutation of い or is the attested ゆい, and all three cards carry the starter and JLPT tags (snapshot/docs/n1-sources/batch-117/reconciliation-004/comparison-cards/銀.md:5; snapshot/docs/n1-sources/batch-117/reconciliation-004/comparison-cards/語.md:5; snapshot/docs/n1-sources/batch-117/reconciliation-004/comparison-cards/休.md:5), so under the supplied model's curated step (snapshot/docs/n1-sources/batch-117/reconciliation-004/model-snapshots/reading_options.py:132-154) the three slots fill deterministically with no fallback, which the fresh focused check confirms in N1, All, Starter+維 and Starter+維+由 with deficits {0:1}, reachable {ぎん, ご, きゅう}, no ゆい witness in 1000 seeds, and a positive seed-1 ゆい control on the parent (fresh-gates/focused-check.json:1-307; fresh-gates/focused-check.log:1; fresh-gates/reading-exposure-supplemental.log:40-55; fresh-gates/reading-exposure-supplemental.log:75); this repairs, within those four modeled pools only, the single-borrow Starter 由 ユイ residual preserved in the prior limits (previous-confirmation/N1-B117-CLAUDE-REPLACEMENT-CONFIRM-004.md:34), and the rewritten Notes state exactly that bounded claim while expressly denying a shape, phonetic or etymological relationship (snapshot/kanji/維.md:46; snapshot/kanji/維.md:50); 紀, 索 and 賃 are unchanged in scope and their supplied audit output is unchanged in kind (fresh-gates/reading-exposure-supplemental.log:9-39; fresh-gates/reading-exposure-supplemental.log:56-73), and fresh host gates pass bound to c5741cc (coordinator/revision-verification-004.json:1-70; fresh-gates/summary.json:1-26; fresh-gates/suite-summary.json:1-18), so no new established defect or consequential unresolved claim remains in this delta.

## Findings
None.

## Optional
### O1: New reading choices trade confusability for pool coverage
- Facet: Consistency and quiz safety
- Severity: optional
- Confidence: medium
- Citations: original-packet/rubric/content-structure.instructions.md:38-41; snapshot/kanji/維.md:50; reconciliation-004/correction-decisions.json:47-52; fresh-gates/quiz-safety.log:5-6
- Evidence: The authoring rubric describes distractors as easily confused kanji, while 銀, 語 and 休 are chosen
    expressly for shared-pool reading availability and are declared not close in shape or phonetics; the meaning
    choices silver | language, word | rest are therefore safe but easy. This is a disclosed, justified trade-off
    that removes a positively reproduced ゆい exposure, not an established defect.
- Suggestion: In a later pass, consider whether Starter-tagged cards with an on reading and closer shape or
    meaning plausibility (for example a 糸-radical Starter card, if one exists) could fill the same three slots
    without reintroducing a fallback; keep the current choices until such a set is verified.

## Limits
- L1: The model identity is runtime-reported only; no tool in this pass verified it. The instruction file was read once at kickoff, then only the 21 chain segments.
- L2: The manifest.json diff and the full current 紀, 索 and 賃 card snapshots were not supplied; their unchanged state rests on the receipt, the scope verification and the supplied gate outputs, not on a byte comparison I performed.
- L3: Gate and focused-check outputs are supplied records, not re-executed. They are bounded host Python-model evidence for exactly the N1, All, Starter+維 and Starter+維+由 pools and the イ prompt; no Kotlin/JVM, native/device, older installed APK, arbitrary-pool or other multiple-borrow claim is made, and the hypothetical [維 由] risk-class pool still reaches ゆい.
- L4: All prior limits remain in force, including the unverified coordinator gloss-overlap scan record, the 紀/編 decline accepted on earlier-round evidence, the historical reconciliation-001 receipt and authoring-notes completeness; the receipt's statement that the Batch 117 authoring-note subsection needs no change was not checked because that subsection was not supplied.
- L5: KANJIDIC2 and JMdict citations are given as whole-file or record ranges, and other line numbers were counted from segment mappings and may be off by a line.

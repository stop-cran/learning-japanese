# B117 confirmation — N1-B117-CLAUDE-REPLACEMENT-CONFIRM-005

## Snapshot
Commit: c5741ccdbce41ff4c8ba2cd7ed9de585561a38e7
Model: runtime-reported Claude Opus 5.5 (claude-opus-5.5); identity not independently verified

## Scope
Chain: segments 1-21 of n1-b117-claude-replacement-confirm-005, each viewed once in order; no re-views
Fetches: none

## Dispositions


## Verdicts
Correctness: CLEAN
Scoped coverage: CLEAN
Consistency and quiz safety: CLEAN
Comprehensibility: CLEAN

## Confirmation
Verdict: CONFIRMED
Basis: The actual delta touches only 維: its curated choices change from 録/催/集 to 銀/語/休, and two Notes are rewritten (diffs/fix.patch:1-27; snapshot/kanji/維.md:13; snapshot/kanji/維.md:46; snapshot/kanji/維.md:50); every exclusion, reading field and other scoped card is unchanged (snapshot/kanji/維.md:9-14; snapshot/docs/n1-sources/batch-117/reconciliation-004/correction-receipt.json:6-8). This repairs the single-borrow Starter 由 ユイ residual that my prior limit preserved (previous-confirmation/N1-B117-CLAUDE-REPLACEMENT-CONFIRM-004.md:34): the focused check reproduces the parent exposure at seed 1 and then shows the curated 銀/語/休 filling all three イ slots with no fallback and no reachable ゆい in N1, All, Starter+target and Starter+target+由 (fresh-gates/focused-check.json:1-307; fresh-gates/check-starter-yui-reconciliation-004.py:1-155), which the unchanged supplemental audit independently matches (fresh-gates/reading-exposure-supplemental.log:42-58). The three counterparts carry single, distinct on readings ギン, ゴ and キュウ, are tagged starter, and are absent from 維's exclusions (snapshot/docs/n1-sources/batch-117/reconciliation-004/comparison-cards/銀.md:3-11; snapshot/docs/n1-sources/batch-117/reconciliation-004/comparison-cards/語.md:3-12; snapshot/docs/n1-sources/batch-117/reconciliation-004/comparison-cards/休.md:3-11). Their complete KANJIDIC2 and JMdict families (silver, money, shogi; word, language, speech, telling, narration, pledging; rest, absence, sleep, suspending) do not answer 維's fiber/tie/rope, hold-fast, principle, corner or particle senses (snapshot/docs/n1-sources/batch-117/reconciliation-004/kanjidic2-records.xml:1-376; snapshot/docs/n1-sources/batch-117/reconciliation-004/jmdict-families.xml:1-695; original-packet/evidence/external-snapshots/03-extract.txt:18-24; original-packet/evidence/source-metadata.json:56-74). The meaning options silver | language, word | rest are therefore semantically safe (fresh-gates/quiz-safety.log:5-6), and correction-decisions.json reasons from those positive definitions rather than title difference (reconciliation-004/correction-decisions.json:1-59). The new Notes accurately state the bounded pools and disclaim shape, phonetic and device claims; their glosses silver, language/word/tell and rest/time off match the counterpart cards and dictionaries. Fresh gates pass and are bound to c5741cc (fresh-gates/summary.json:1-26; fresh-gates/suite-summary.json:1-18; coordinator/revision-verification-004.json:1-70; coordinator/round4-source-verification.json:1-356), so no new established defect or consequential unresolved claim remains in scope.

## Findings
None.

## Optional
None.

## Limits
- L1: The model identity is runtime-reported only; no tool in this pass verified it. The instruction file was read once at kickoff, then only the 21 chain segments.
- L2: The authoring rubric's preference for "easily confused" distractors (original-packet/rubric/content-structure.instructions.md:47-49) is deliberately traded here for shared-pool reading safety, and the Note says so explicitly. I judge this a design choice rather than an established defect: the options are valid, semantically distinct and plausible wrong answers, but they make the 維 meaning quiz easier than shape-similar choices would.
- L3: The named author response (scratch-117/review/reconciliation-004/author-response-gpt-confirm-003.md), the runtime diff and the inventories cited by the receipt were not supplied. I verified the neutral correction decisions, receipt, actual diff, snapshot, sources and fresh outputs instead.
- L4: All prior limits remain in force. The repair is proven only for the four named pools and the イ prompt in the frozen Python model; arbitrary or other multiple-borrow pools, Kotlin/JVM, native/device execution and compatibility with the older installed APK are not established. The earlier 紀/編 decline, the gloss-scan record gap and the round-2 to round-4 authoring-notes completeness remain as previously disclosed, and gates were not re-executed by me.

# B116 confirmation — N1-B116-CONSTITUTION-CONFIRM-004

## Snapshot
Commit: 34687354b531a32fea9c10b745e80ac963ac1d4b
Model: runtime-reported Claude Opus 5.5; execution-model identity is not independently verifiable within this pass

## Scope
Chain: segments 1-11 of n1-b116-constitution-confirm-004, each read once in order with no re-views; the kickoff instruction file was viewed once at the start as authorized. Scoped card: 憲 (revised snapshot read in full with fix.patch, changed-lines, link-targets, all ten checks, QuizBuilder.kt, Daijisen entries for 僚 権 任 士 数, JMdict cited entries, KANJIDIC2 meanings and the full 僚 権 任 係 士 数 cards). 監 and 督 were read as context only.
Fetches: none

## Dispositions


## Verdicts
Correctness: CLEAN
Scoped coverage: CLEAN
Consistency and quiz safety: CLEAN
Comprehensibility: CLEAN

## Confirmation
Verdict: CONFIRMED
Basis: I checked every changed 憲 line (confirm-packet/snapshot/kanji/憲.md:14, 87-102, 118-122, 127-128, 142-145) against the supplied evidence, and each new claim holds. 僚 has an official sense, 役人。つかさ with 官僚, and JMdict 1211860 glosses 官僚 "bureaucrat; government official". 官憲 is "officials; authorities" (JMdict 1211670), and 憲 sense 3 is 取り締まる。役人. 権 is power (他を従わせる力) or entitlement (資格), not an officeholder, as the card says. 任 sense 2 is assignment to a post, with 任官 "appointment (to an office)" (JMdict 1467180). JMdict 1589850 glosses 係員 "person in charge; official", and KANJIDIC2 lists "person in charge" for 係. 士 sense 2 is an ancient-Chinese official rank below 大夫, and the card keeps it restricted. The 数 note lists Daijisen senses 1-6 accurately and isolates the guard to KANJIDIC2's English "law". My previous Basis judged 権 and 数 harmless without guards; these guards are explicitly conservative and non-synonymous, and over-exclusion creates no defect. Each guard is plausibly motivated (English "authority" versus 官憲 "the authorities"; 数's KANJIDIC2 "law"). All six new exclusions resolve to existing cards (link-targets: 0 unresolved). None overlaps distractors 寄 害 寒. The new JMdict IDs match the four cited words. Prior exclusions, readings, selections, distractors, words, strokes and wrappers are unchanged. Lint, validate, quiz-safety, reading exposure and 431 unit tests pass, and the curated 憲 options and reading quiz are unchanged. No consequential claim remains unresolved within this text and host-model scope.

## Findings
None.

## Optional
None.

## Limits
- L1: No network fetch was made. The Daijisen entries are coordinator-retrieved excerpts with response hashes, relied on as quoted text without re-fetching; no Daijisen character entry for 係 was supplied, so its guard rests on KANJIDIC2, JMdict 1589850 and the 係 card.
- L2: Raw KanjiVG SVGs, the binary Joyo PDF and full Weblio HTML responses were not read in this pass.
- L3: Quiz-safety and reading-exposure outputs are host-side Python models of the N1, All and Starter pools. They do not establish caller-built or multi-borrow pools, Kotlin execution, native/device acceptance or compatibility with the older installed APK 5c000bd, which predates quiz_exclusions. QuizBuilder.kt was read, not executed.
- L4: The 監 and 督 changes (士 and 員 guards, 員 notes, JMdict metadata) were read only as context and are not adjudicated. The 憲/監 and 憲/督 pairs are unchanged. Reciprocal declarations on other existing cards were not exhaustively checked.
- L5: This delta pass relies on my previous confirmation for content unchanged since 2b81b65b and does not re-read that round's full counterpart corpus.
- L6: The supplied unchanged 員 card was not part of this chain; 憲 does not declare 員, and its "member, employee" title was judged only from the KANJIDIC2 meanings shown here.

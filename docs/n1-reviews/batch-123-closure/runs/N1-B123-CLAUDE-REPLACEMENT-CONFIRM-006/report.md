# B123 confirmation — N1-B123-CLAUDE-REPLACEMENT-CONFIRM-006

## Snapshot
Commit: 60db6255f5c74bc039884d13640966dbe74fee99
Model: runtime reports Claude Sonnet 5.5 (claude-sonnet-5.5); execution-model identity not independently verified

## Scope
Chain: segments 1-21 of n1-b123-claude-replacement-confirm-006, each read once in order after the forced prompt read; no re-views
Fetches: none (no network, web or local reads outside the prompt and chain)

## Dispositions


## Verdicts
Correctness: CLEAN
Scoped coverage: CLEAN
Consistency and quiz safety: CLEAN
Comprehensibility: CLEAN

## Confirmation
Verdict: CONFIRMED
Basis: The actual diff (diffs/fix.patch:1-25) only adds 本, 度, 像, 計, 測 and 量 to 範's quiz_exclusions, adds two note bullets and extends the character-source links; title, readings, distractors 車/書/達, mnemonic, strokes and the 範囲 wrapper are unchanged, and all six new IDs are existing single-character cards that do not overlap the distractors (snapshot/kanji/範.md:13-14). Each new guard is supported on the supplied evidence: 本 and 度 carry independently attested model/exemplar branches (source-references/direct-phrases.json:7-16; snapshot/docs/n1-sources/batch-123/reconciliation-003/pair-dispositions.json:7-31) that the card states as separate from the book/origin and degree/occurrence senses without deriving them from 手本 (snapshot/kanji/範.md:51); 像 is a conservative English-label guard for "model" as representation, with 範 not claimed to mean a likeness and no exemplar sense claimed for 像 (snapshot/kanji/範.md:51; snapshot/kanji/像.md:20); 計, 測 and 量 are conservative measure/amount guards resting on JMdict 1438050 "transverse measurement" and the Daijisen 基準とする長さ extract, against JMdict 1252050 meter/measuring device, 1600650 measure/infer and 1554640 quantity (snapshot/docs/n1-sources/batch-123/reconciliation-001/jmdict-records.xml:1-2227), and the new note keeps action, instrument, result and standard length separate and disclaims any 範 measuring verb or device, any spelling equivalence and any frequency (snapshot/kanji/範.md:52). I checked the three no-new-guard pairs against the actual cards and displayed titles, including secondary senses: 囲 "surround; enclose" gives an action or surroundings, not a model or standard (snapshot/kanji/囲.md:20); 方 "direction, method" has method, side, category and field senses (JMdict 1516925/1516930) and no exemplar or standard sense, and 範疇 category is a whole-word sense; 理 "reason, logic" gives reason, principle and logic (JMdict 1957060, 2412900, KANJIDIC2 理) and no model-to-imitate sense, so none is a defensible answer for 範 or vice versa, and the neutral dispositions keep the moral-principle and category associations (snapshot/docs/n1-sources/batch-123/reconciliation-003/pair-dispositions.json:100-168). All exclusions are direct symmetric pairs declared at one endpoint, none is inferred transitively, and all earlier accepted guards and notes are unchanged. KANJIDIC2 supports the 範 pattern/example/model, 本 book/origin, 度 degrees/occurrence, 像 statue/image, 計 plan/measure, 測 measure and 量 quantity/measure glosses. The committed host checks pass (lint, validate, linkplan, manifest and rebuild, budget, vocabulary, 431 unit tests, quiz-safety with the three curated wrong options and reading-exposure with 0 hits), and are bounded host models, not native, device, arbitrary-pool or multi-borrow acceptance. No new defect is established.

## Findings
None.

## Optional
None.

## Limits
- L1: The nine new Digital Daijisen captures (本, 像, 囲, 方, 度, 計, 測, 量, 理) were not supplied; the 本, 度, 像, 計, 測, 量, 囲, 方 and 理 sense claims rest on the author's signed summaries, short quoted phrases with line numbers and the manifest hashes (snapshot/docs/n1-sources/batch-123/reconciliation-003/source-manifest.json:1-89; source-references/direct-phrases.json:1-54), which I could not compare with the raw captures. The Daijisen 範 sense and のり "基準とする長さ" claims rest on source-references/han.json and the earlier supplied extract, not a re-read.
- L2: The actualComparisonCard files in reconciliation-001/comparison-cards and the rest of the reconciliation-001 query manifest were not supplied. Comparison-card content was checked through the snapshot cards 囲, 度, 方, 本, 測, 理, 計, 量 and 像 plus the supplied KANJIDIC2 and JMdict records.
- L3: pair-dispositions.json lists JMdict 1235960 (境界) among the independent sources for 囲 (Q3); that entry is not about 囲, and the 囲 and 方 cards do not cite it. The citation is cosmetic and does not affect the no-new-guard decision, but it is not verified as an intended source.
- L4: Quiz-safety, reading-exposure, unittest and the other committed checks are bounded Python host models. They do not cover caller-built or multi-borrow pools, Kotlin execution, native/device acceptance, whole-set acceptance or compatibility with the older installed APK. The unittest log shows HTTP 429 retries from an unrelated test and OK overall.
- L5: The 範 stroke JSON, raw HTML responses, the binary Joyo PDF, the manifest bytes and the gate receipts and logs beyond those in the chain were not read; the revision-verification and adjudication JSON files are the coordinator's own statements, treated as context, not independent proof.
- L6: The three no-new-guard decisions (囲, 方, 理) and the six new guards are bounded judgements on the supplied records and displayed labels, not exhaustive negative claims, and no unrequested guard pairs outside the nine questions were assessed. The prior reviewer's accepted limits (L1-L6 of N1-B123-CLAUDE-CONFIRM-002 and L1-L8 of the initial report) are preserved and still apply.

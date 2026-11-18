# B125 confirmation — N1-B125-CLAUDE-CONFIRM-002

## Snapshot
Commit: f2d2ddf87a0f1a721920241a88a61e28a98fa6f2
Model: runtime reports Claude Opus 5.5; identity not independently verifiable from within this pass

## Scope
Chain: segments 1-30 of n1-b125-claude-confirm-002, each read once in order; no re-views
Fetches: none

## Dispositions


## Verdicts
Correctness: CLEAN
Scoped coverage: CLEAN
Consistency and quiz safety: CLEAN
Comprehensibility: CLEAN

## Confirmation
Verdict: CONFIRMED
Basis: The only change to 侵 since dbca519 is four added direct guards (低, 短, 小, 容) and one Notes bullet; the bullet accurately paraphrases Kanji Pedia's ②みにくい appearance branch (背が低くて容姿がみすぼらしい), each guard has a defensible partial link (低 short height per JMdict 1434180 sense 3, 短/小 broad short/small labels, 容 appearance/looks per KANJIDIC2), none overlaps distractors 寝/進/掃 or the card itself, title/readings/practice selections are unchanged, the complete 1,245-card inventory shows no card reading みにくい, the curated meaning options and reading-exposure output (including the explicit みにくい run) are unchanged with no hits, all ten committed host checks pass, and all prior F1/O1/O2 resolutions still hold; remaining points are optional polish.

## Findings
None.

## Optional
### O1: Qualify the appearance branch as an out-of-table character-dictionary sense
- Facet: Comprehensibility
- Severity: optional
- Confidence: medium
- Citations: snapshot/kanji/侵.md:50; evidence/external-snapshots/reconciliation-003/shin-response-plus-lf.html:95-125; snapshot/docs/n1-sources/batch-125-reconciliation-003/disposition.md:7
- Evidence: The new bullet says only that "a character dictionary also describes an unattractive appearance". Kanji Pedia attaches that sense to the kun reading みにくい marked 外 (outside the standard reading table), and the author's disposition confirms it is absent from KANJIDIC2, the card metadata and practice. Without that qualifier a learner may read it as an ordinary modern meaning of 侵.
- Suggestion: Add a short qualifier such as "linked to the out-of-table reading みにくい; not an ordinary modern use taught here" without asserting frequency or age.

### O2: Apply the appearance-guard rationale consistently or narrow it
- Facet: Consistency and quiz safety
- Severity: optional
- Confidence: low
- Citations: snapshot/kanji/侵.md:14; evidence/complete-title-reading-inventory.txt:368; evidence/complete-title-reading-inventory.txt:949; snapshot/docs/n1-sources/batch-125-reconciliation-003/disposition.md:13
- Evidence: The guards cover 小 "small, little" and 容 "contain; appearance" as broad size/appearance labels, but 寸 "sun (length unit); small" and 背 "back; stature" carry the same head word or category and are unguarded. Because the appearance branch is obscure, none of these pairs is a credible meaning-quiz ambiguity, so this is an internal-rationale gap, not a quiz defect.
- Suggestion: Either add 寸 and 背 under the same rationale, or keep the current set and note in the disposition that the remaining broad labels were judged not to need guarding.

## Limits
- L1: Host checks (lint, validate, quiz-safety, reading-exposure, manifest, budget, unittest, vocabulary) are bounded static evidence; caller-built or multi-borrow pools, Kotlin execution, native/device acceptance and compatibility with installed APK 5c000bd (predates quiz_exclusions) are not established.
- L2: The Kanji Pedia ②みにくい branch is now noted on the card and guarded by bounded direct exclusions; its frequency, age and modern usage remain unestablished by the opened evidence, and the Shinjigen 会意 formation is still not adopted on the card (structure-unclassified and the labelled mnemonic are retained).
- L3: My initial report misattributed 侵撃 to repo/kanji/撃.md:23; the 侵–撃 exclusion stands on the attack sense alone (JMdict 1359830 separately records 侵撃).
- L4: The 25 direct guards are conservative; several (患, 病, 毒, 徹, 凌, 占, 低, 短, 小, 容) rest on secondary or broad English-choice overlaps rather than near-synonymy, and are accepted as bounded guards, not as proof of ambiguity in every pool.
- L5: Earlier lower-priority candidates (暴, 軍, 領, 越, 荒) remain assessed only at their earlier bounded level; 汚 was read in this chain and its dirt/defilement senses do not plausibly answer invade/encroach. Raw stroke SVGs, the binary Joyo PDF and assets outside this chain remain unread; Kanji Pedia line citations are approximate ranges over the supplied HTML.
- L6: Runtime-reported model identity is not independently verified.

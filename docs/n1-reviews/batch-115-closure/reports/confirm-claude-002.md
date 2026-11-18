# B115 confirmation — N1-B115-CLAUDE-CONFIRM-002

## Snapshot

Commit: revised 206f9893 (reviewed f36cd819)
Model: Claude Opus 5.5 (self-reported, unverified)

## Scope

Chain: b115-confirm-claude-v1 segments 1-25 read in order, ending at END OF CHAIN
Fetches: 0 of 3 used

## Dispositions

- F1 - RESOLVED - 卓 now excludes 英, 冠 and 越 (with 偉, 著, 凌) and a Notes bullet distinguishes them (confirm-packet/snapshot/kanji/卓.md:14; confirm-packet/snapshot/kanji/卓.md:59-63)
- F2 - RESOLVED - 寸 now excludes 微 "minute; faint", and Notes contrasts it as minute/tiny (confirm-packet/snapshot/kanji/寸.md:14; confirm-packet/snapshot/kanji/寸.md:59-61)
- O1 - RESOLVED - 偉 and 著 added to 卓 exclusions (confirm-packet/snapshot/kanji/卓.md:14)
- O2 - DECLINE ACCEPTED - 軽 "lightweight; slight" and 粒 "grain; small particle" lead with glosses that do not answer 寸 "sun (length unit); small" (original-packet/evidence/title-index.txt:1121; original-packet/evidence/title-index.txt:878)
- O3 - DECLINE ACCEPTED - 害 "harm" and 損 "loss; damage" name consequences, not misfortune/calamity labels (original-packet/evidence/title-index.txt:419; original-packet/evidence/title-index.txt:507)
- O4 - DECLINE ACCEPTED - 幸 "happiness; good fortune" and 福 "good fortune" do not answer 康 "health; well-being" (original-packet/evidence/title-index.txt:453; original-packet/evidence/title-index.txt:775)
- O5 - RESOLVED - exclusions are symmetric and also checked among chosen distractors (confirm-packet/evidence/QuizBuilder.kt:26-32; original-packet/repo/docs/content-format.md:89-91)
- O6 - DECLINE ACCEPTED - reduced curated reading pools for 票 and 魔 are still filled to three options by fallback (confirm-packet/checks/reading-options.txt:90-115; confirm-packet/checks/quiz-safety.txt:1-30)

## Verdicts

Correctness: CLEAN
Scoped coverage: CLEAN
Consistency and quiz safety: CLEAN
Comprehensibility: CLEAN

## Confirmation

Verdict: CONFIRMED
Basis: Both findings are resolved, every observation is resolved or has an acceptable decline, new card claims match the cited JMdict/KANJIDIC2 records, and the packet checks report no errors or reading collisions in drawable pools.

## Findings

None.

## Optional

### O1: 宙 Notes wording on 時
- Facet: Comprehensibility
- Severity: optional
- Confidence: medium
- Citations: confirm-packet/snapshot/kanji/宙.md:58-59; original-packet/evidence/kanjidic2-records.xml:202; original-packet/evidence/title-index.txt:617
- Evidence: The bullet says "interval-of-time sense" and that 時 is "still excluded", but 時 is newly excluded in this revision. "Interval" also echoes 間 "interval, between" rather than 時 "time, hour".
- Suggestion: Say "is excluded" and consider "a span of time" to avoid suggesting a pre-existing exclusion or 間.

### O2: reading-options unlisted-reading check scope
- Facet: Consistency and quiz safety
- Severity: optional
- Confidence: medium
- Citations: confirm-packet/checks/reading-options.txt:1-118; confirm-packet/checks/reading-exposure.txt:1-144; original-packet/evidence/jmdict-families.xml:375-387
- Evidence: The unlisted-reading check considers KANJIDIC2 name readings only. Card-text readings such as 卓 しょく (attested in JMdict 1415580) appear only as tier-3 fallback candidates. reading-exposure.txt covers this case and finds no drawable collision, so it is safe now.
- Suggestion: Fold card-text attested readings into the reading-options check.

## Limits

- L1: The model identity is self-reported and unverified.
- L2: No Kotlin/JVM, emulator or phone execution took place. The installed APK 5c000bd predates quiz_exclusions, so device behavior depends on an upgraded client.
- L3: QuizBuilder.kt covers meaning choices only. The reading-quiz source was not supplied, so the O6 reasoning relies on reading-options.txt host modelling.
- L4: Custom/caller-built and multi-borrow Starter pools are not modelled beyond the packet checks.
- L5: The Daijisen/Weblio entry for the 寸 き suffix (confirm-packet/snapshot/kanji/寸.md:45-46) was not fetched or re-verified, and neither was Daijisen for 時/宙.
- L6: Initial limits L1-L7 still stand: no stroke or asset changes were reviewed, 災/禍/鬼/霊/尺/曖 cards are still absent, and the lint frozen-log discrepancy is accepted as documented (confirm-packet/evidence/lint-rerun-f36cd819.txt:1-6).
- L7: The 票/署 exclusion is weakly motivated, since 票's title has no "sign" (KANJIDIC2 lists "sign"), but it is harmless and is not raised.

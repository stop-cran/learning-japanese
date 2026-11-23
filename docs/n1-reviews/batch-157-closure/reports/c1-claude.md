# Batch 157 confirmation report (Claude)

## Snapshot
Revised commit cd5d75d186efa11b89e64e215dbb239a09d93639 (first-round snapshot a5c6a0ff). Reviewer model: Claude (Anthropic); exact version not identifiable.

## Scope
Read in full: the ten revised kanji cards (佐 佳 併 侍 侮 侯 俊 俗 俵 倫), 助 and 理, the ten word articles, the ledger, the audit tool diff, the JMdict supplement selection, CHANGES.md, RESPONSE.md. Checked against evidence\jmdict-cited-entries.xml, the Kotobank/Weblio extracts, checks\quiz-safety.txt, reading-exposure.txt, reading-options.txt, link-targets.tsv (no missing targets), QuizBuilder.kt, and the original packet's Weblio public-source files.

## Dispositions
- C1 (侍/武士 sense): RESOLVED. Matches JMdict 1314780 sense 1.
- C2 (侮る / あなずる): RESOLVED. Weblio gives あなずる as the older form of あなどる.
- C3 (補佐): RESOLVED. Glosses match JMdict 1603460.
- C4 (kanji exclusions): RESOLVED.
- C5 (諸侯 exception): RESOLVED. The ledger exceptionReason is adequate and 諸侯 is sourced to JMdict 1344250 and 王侯 1588830.
- C6 (倫 title "ethics; moral principles"): RESOLVED. Matches Weblio sense 1.
- C7 (不倫, 絶倫, 大佐): RESOLVED. Matches JMdict 1495370, 1387000, 1413740.
- C8: RESOLVED.
- C9 (併用 example 1 kept): DECLINE ACCEPTED. It is an everyday instruction and the framing was removed.
- C10: RESOLVED. The 佳 mnemonic was removed.
- O1–O4: RESOLVED.
- O5: RESOLVED for 理 (ことわり, JMdict 2412900). The 語 `phonetic` item is out of batch: DECLINE ACCEPTED.
- L1: RESOLVED. 内侍 is now sourced from the Kotobank extracts and JMdict 1582520.
- L2: RESOLVED.
- L3: RESOLVED. Curated options fill all wrong slots for every batch card.

## Verdicts
- Correctness: NEEDS FIX (minor; one gloss, F1).
- Scoped coverage: CLEAN.
- Consistency and quiz safety: CLEAN (optional notes O1–O3).
- Comprehensibility: CLEAN apart from F1 and the "source-only" wording (O4).

## Confirmation
CONFIRMED, with one minor to fix (F1). No new blocking finding. quiz-safety: 0 errors, 0 warnings. Reading-options: 0 problems. Reading-exposure: 0 production hits and 0 padded-session hits (4 latent collisions are pre-existing and not batch-caused). I judged each of the ten new distractor sets: no distractor can also be a correct meaning answer. The sets are not rejectable by category alone, with the caveat in O1.

## Findings
**F1 (minor, correctness/comprehensibility).** 倫.md Notes quote 五倫 as "the five Confucian filial-piety relationships". This is JMdict's literal gloss (1593605), but it misleads a beginner, because the five relationships are ruler–subject, parent–child, husband–wife, elder–younger and friends. Suggest "the five Confucian human relationships".

## Optional
- O1: Several distractor sets let a learner guess by category. 侍 (父 母 子, all family), 俵 (田 土 木, all nature) and 俊 (安 少 多, with 少/多 an antonym pair) make the odd one out guessable. 佐 (母 友 子) is a weaker leak. Not a correctness error.
- O2: On 倫, the distractor 事 "matter, affair" sits next to the card's own example 不倫 "affair". It is a mild confusion risk, not a correct answer.
- O3: Some word exclusions go beyond the two displayed titles: 制作 for 佳作 (the 制作 JMdict sense is "work", but the displayed title is not), and 用途, 使う and 用 for 併用. They are harmless over-exclusions. Possible leftover mild overlaps: 憎 "hate" with 侮 "despise", and 無視 with 侮る (low confidence).
- O4: Labels question: do NOT adopt a "kun, source-only here" label on the batch. The batch's explanatory row text ("older form of あなどる", "usually written in kana") helps a beginner more. "source-only" is authoring jargon. The 助 rows (kanjiapi.dev lists たす.ける, たす.かる, す.ける, すけ, matching the card) and the 理 intro line are acceptable as the existing repo convention, but could be reworded in plain language.
- O5: The 俗 card cites the sex-service sense of 風俗 (JMdict 1499960). It is sourced, but sensitive for a beginner card.

## Limits
- I did not run the Kotlin tests or check phone rendering.
- I did not verify KANJIDIC2 for 卑 and 併, nor the full ledger JSON.
- I read only part of reading-exposure.txt (sampled lines plus totals).
- Word-quiz ties for 併用, 倫理, 俗語, 諸侯 and 俵 and the reverse pairs I took from CHANGES.md; I read only the 佳作 and 補佐 blocks directly.
- The 俊/佐/佳/併 Daijisen extracts were relied on from my first-round check.
- The audits cannot show learner-perceived plausibility of distractors or phone readability.
- Every response made exactly one tool call; I noticed no parallel calls.

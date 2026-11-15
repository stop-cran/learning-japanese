# B117 confirmation — N1-B117-CLAUDE-CONFIRM-002

## Snapshot

- Commit: 1c2fc20527c935306d241ad7bf8d68b27c12140a
- Model: runtime-reported Claude Opus 5.5 (claude-opus-5.5); not independently verified

## Scope

- Chain: C:\Users\stop-\n1-kanji-workspace\review-chains\n1-b117-claude-confirm-002\ segments 01-41, each read once, serially, in order
- Fetches: none

## Dispositions

- F1 - RESOLVED - 著, 歳 and 偵 are now direct exclusions on 紀/索 with qualified Notes; each pair is supported by the full comparison card, KANJIDIC2 and complete JMdict families, and no new guard overlaps the curated distractors.

## Verdicts

- Correctness: CLEAN
- Scoped coverage: CLEAN
- Consistency and quiz safety: CLEAN
- Comprehensibility: CLEAN

## Confirmation

Verdict: CONFIRMED
Basis: Prior F1 is resolved, the L3 pairs 紀/筆 and 紀/文 are now guarded, the 紀/系 and 索/題 declines are evidence-based, the fresh gates pass, and no new actionable defect was found.

## Findings

None.

## Optional

None.

## Limits

- L1: The F1 evidence is snapshot/kanji/紀.md:14; snapshot/kanji/紀.md:47-48; snapshot/kanji/索.md:48-49; reconciliation-002/pair-dispositions.json:15-29; author-response/author-response-claude-confirm-001.md:7-9; snapshot/docs/n1-sources/batch-117/reconciliation-002/jmdict-families.xml:1-608. It was read from chain copies, not live repository files.
- L2: The new guards 紀/字・時・刻・準, 索/頼, 維/絡・接・挟・線 and 賃/使・補 are judged acceptable conservative over-exclusions (reconciliation-002/pair-dispositions.json:45-114). Over-exclusion is not a quiz-safety defect. Whether any of these guards is unnecessarily broad is an editorial question that this run does not adjudicate.
- L3: The declines 紀/系 and 索/题 rest on bounded semantic distinctions (reconciliation-002/pair-dispositions.json:63-80). I accept them as reasonable, but they are not proof that no learner could hesitate between these labels.
- L4: Host gates are static evidence only: fresh-gates/summary.json:3; fresh-gates/quiz-safety.log:1-22; fresh-gates/validate.log:1; fresh-gates/unittest.log:1-22. No Kotlin/native/device check was made, and no compatibility with the 5c000bd APK is claimed. Arbitrary-pool and multiple-borrow cases are unmodeled.
- L5: The 由 ユイ reading can still be drawn in the single-borrow Starter practice case (fresh-gates/reading-exposure-supplemental.log:49-51). This is the known residual. It has no production hit in the N1 or All pools.
- L6: The author response covers only the prior F1 and L3. The other added guards are documented solely in pair-dispositions.json, which I treat as the authoritative rationale.

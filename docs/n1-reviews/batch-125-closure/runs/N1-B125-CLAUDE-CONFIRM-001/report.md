# B125 confirmation — N1-B125-CLAUDE-CONFIRM-001

## Snapshot
Commit: dbca5192a4308dc6e8d954af37775e0fcd1986ea
Model: runtime reports Claude Opus 5.5; identity not independently verifiable from within this pass

## Scope
Chain: segments 1-29 of n1-b125-claude-confirm-001, each read once in order; no re-views
Fetches: none

## Dispositions
- F1 - RESOLVED - snapshot/kanji/侵.md:14 now declares 討 in quiz_exclusions and snapshot/kanji/侵.md:46 explains the attack overlap; diffs/fix.patch:8 is the only metadata change. JMdict 1478010 討つ attack/defeat/conquer (batch-125-reconciliation/jmdict-records.xml) and 1359800 侵す raid support the direct pair; one endpoint declaration suffices and it does not rely on 攻/撃 transitivity.
- O1 - RESOLVED - 損 is declared at snapshot/kanji/侵.md:14 with the harm rationale at snapshot/kanji/侵.md:46; JMdict 1406660 損 loss/damage/harm, 1406690 損ねる harm/hurt and 1596510 損なう harm/damage, plus KANJIDIC2 損 damage/hurt/injure, support the 侵す harm/afflict overlap.
- O2 - RESOLVED - 略 is declared at snapshot/kanji/侵.md:14 with snapshot/kanji/侵.md:46 citing capture and plunder; KANJIDIC2 略 lists capture/plunder and JMdict 1551960 略す sense 3 take/capture/steal, 1552020 略取 and 1606250 略奪 confirm a raid/taking overlap independent of the shared おか.す reading or the whole word 侵略.

## Verdicts
Correctness: CLEAN
Scoped coverage: CLEAN
Consistency and quiz safety: CLEAN
Comprehensibility: CLEAN

## Confirmation
Verdict: CONFIRMED
Basis: The only changes to 侵 are 15 added direct exclusions and four hedged Notes bullets; each added pair's stated sense is supported by opened evidence (損/痛/毒 harm, 討/戦/突 attack, 略 capture/plunder, 患/病 illness/affliction, 破る/触れる/違反/違える violation or infringement, 徹 penetrate, Kanji Pedia 凌 ②おかす・あなどる and 占 ②しめる・自分のものにする), none overlaps distractors 寝/進/掃 or the card itself, the curated meaning options and reading exposure are unchanged, all ten committed host checks pass, and F1, O1 and O2 are resolved with no new established defect.

## Findings
None.

## Optional
None.

## Limits
- L1: Host checks (lint, validate, quiz-safety, reading-exposure, manifest, budget, unittest, vocabulary) are bounded static evidence; caller-built or multi-borrow pools, Kotlin execution, native/device acceptance and compatibility with installed APK 5c000bd (predates quiz_exclusions) are not established.
- L2: Kanji Pedia's 侵 entry also records ②みにくい (ugly/shabby appearance, an out-of-table reading) and a Shinjigen 会意 broom-in-hand formation; neither is in the frozen KANJIDIC2 record or the card, which keeps structure-unclassified and a labelled modern-shape mnemonic. I did not assess that branch as a quiz comparison; the card makes no contrary claim.
- L3: My initial report misattributed 侵撃 to repo/kanji/撃.md:23; the 撃 card does not mention 侵撃. JMdict 1359830 separately records 侵撃, and the 侵–撃 exclusion stands on the attack sense alone.
- L4: The added guards are conservative; several (患, 病, 毒, 徹, 凌, 占) rest on secondary or broad English-choice overlaps rather than near-synonymy. I accept them as bounded direct guards, not as proof that each pair is ambiguous in every pool.
- L5: Earlier unread lower-priority candidates from the initial pass other than 戦 (暴, 軍, 領, 越 beyond its card, 荒) remain unassessed beyond the earlier bounded observations; raw stroke SVGs, the binary Joyo PDF and assets outside this chain remain unread.
- L6: Runtime-reported model identity is not independently verified.

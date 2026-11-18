# B121 confirmation — N1-B121-CLAUDE-002-CONFIRM-001

## Snapshot
Commit: b7369b9502f7f5c14a4f2081fe9e6a0e2b276e42
Model: runtime reports Claude Opus 5.5; identity not independently verifiable in this pass

## Scope
Chain: segments 1-50 read once each, in order, no re-views
Fetches: none

## Dispositions
- F1 - RESOLVED - snapshot/kanji/徳.md:14 now declares 幸 and 財, and snapshot/kanji/徳.md:44 names them in the limited blessing/wealth comparison. The counterpart evidence supports both guards: 幸's title "happiness; good fortune" (snapshot/kanji/幸.md:3) and JMdict 幸せ "happiness; good fortune; luck; blessing" (snapshot/docs/n1-sources/batch-121/reconciliation-001/jmdict-records.xml, entry 1594060); 財's title "wealth; property" (snapshot/kanji/財.md:3), matching Daijisen 徳 sense 4 富。財産 (original-packet/evidence/external-snapshots/01-extract.txt:25). Both pairs are now declared on the 徳 endpoint.
- F2 - RESOLVED - snapshot/kanji/徳.md:14 declares 偉, and snapshot/kanji/徳.md:44 lists it. The guard is supported by KANJIDIC2 徳 "commanding respect" (original-packet/evidence/kanjidic2-records.xml:59) and by JMdict 偉い "admirable; commendable; laudable" (snapshot/docs/n1-sources/batch-121/reconciliation-001/jmdict-records.xml:136-146).
- O1 - RESOLVED - snapshot/kanji/徳.md:47 now quotes 教 exactly as "teach, instruct", which matches snapshot/kanji/教.md:3.
- O2 - RESOLVED - The distractors are now 後, 側 and 達 (snapshot/kanji/徳.md:13). Meaning checks: their displayed titles are "behind, after", "side" and "reach, plural suffix" (snapshot/kanji/後.md:3; snapshot/kanji/側.md:3; snapshot/kanji/達.md:3). The full JMdict and KANJIDIC2 senses add back, rear, remainder, descendant, vicinity, leaning, arrival, accomplished and progress; none matches virtue, benevolence, blessing, wealth or excellent character, so none is a defensible answer for 徳 in either direction. Shape: 後 shares 彳, and 側 and 達 are explained honestly as partial contrasts (snapshot/kanji/徳.md:49). Readings ゴ/コウ, ソク and タツ/ダ do not collide with トク, and the committed reading-exposure log reports 0 production and 0 padded-session hits (gates-committed-revision/reading-exposure.log:6-34). The committed quiz-safety log shows the new options (gates-committed-revision/quiz-safety.log:1).
- O3 - RESOLVED - snapshot/kanji/徳.md:14 declares 性 and 能, and also 格. snapshot/kanji/徳.md:44 attributes the innate nature/ability sense to the character source and states that the old examples do not establish present-day frequency. This avoids the unsupported currency claim.
- O4 - RESOLVED - The suggestion was to keep the conservative classification unless a reputable source was cited. structure-unclassified and the labelled modern-shape mnemonic are retained (snapshot/kanji/徳.md:5; snapshot/kanji/徳.md:25), and no phonetic or historical claim was added.

## Verdicts
Correctness: CLEAN
Scoped coverage: CLEAN
Consistency and quiz safety: CLEAN
Comprehensibility: CLEAN

## Confirmation
Verdict: CONFIRMED
Basis: All six items are resolved by the actual changed lines in snapshot/kanji/徳.md (fix.patch, the 13-14 and 44-49 hunks). I checked each new note claim against counterpart cards and records: 礼 reward/gift is in JMdict 1557450; 師 exemplar is in KANJIDIC2 師; 道 moral principles is in JMdict 1454080 sense 5; 品 refinement, 儀 formal conduct, 厚 kind/cordial, 愛 care, 助/援 help, and 与/給/贈/授/受/享 giving or receiving all appear on their cards and records. The 42 exclusions contain no duplicate, self-reference or distractor overlap; the validator reports 0 errors; and all extra guards are conservative direct pairs (non-transitive) that do not create a false meaning. The new distractors are meaning-safe, reading-safe and visually reasonable. No new established defect or consequential unresolved claim remains in scope.

## Findings
None.

## Optional
None.

## Limits
- L1: Only the chain was read. The raw SVGs, raw Weblio HTML, Joyo PDF, extract scripts, held-initial-disposition.md, author-response-gpt.md, and the comparison cards for 待, 律, 徒, 復, 循, 徹 and 行 were not supplied or not read. The rejected-candidate cards were not reviewed.
- L2: Host checks and the reading-exposure model are bounded Python evidence. They do not establish caller-built or multi-borrow pools, Kotlin execution, native/device acceptance or compatibility with the older installed APK, which predates quiz_exclusions.
- L3: The current-day frequency of Daijisen 徳 senses 4 and 5 remains unestablished. Both are now guarded conservatively, so the uncertainty no longer affects quiz safety.
- L4: I made no visual-confusability or font-rendering judgment beyond the card text and stroke descriptions.
- L5: Only 徳 and its directly cited comparisons were reviewed. This is not a whole-corpus audit of other cards' exclusions.

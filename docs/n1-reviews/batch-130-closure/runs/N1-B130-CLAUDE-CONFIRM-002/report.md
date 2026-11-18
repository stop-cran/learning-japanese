# B130 confirmation — N1-B130-CLAUDE-CONFIRM-002

## Snapshot
Commit: d440617274eef6ea7611e60f147d6483f29ca710
Model: Claude Opus 5.5 as reported by the runtime; identity unverified from evidence

## Scope
Chain: segments 1-80 read in order, each exactly once, ending at END OF CHAIN in segment 80; no re-views; the run prompt was read once as the forced first call
Fetches: None

## Dispositions
- F1 - RESOLVED - 擦 and 摩 (plus 磨) are now direct exclusions on 耗 (snapshot/kanji/耗.md:14), and the Notes bullet at snapshot/kanji/耗.md:61-65 explains frictional wear without claiming that rubbing equals depletion. Complete JMdict 1595930 positively gives すれる "to wear out; to become worn" with rare 磨れる/摩れる spellings (evidence/reconciliation/jmdict-families.xml:68), which supports the qualified wording. The committed quiz-safety log raises no unmentioned-exclusion warning for these guards (committed-checks/quiz-safety.log:1-103), and validate/manifest/manifest-rebuild pass.
- F2 - RESOLVED - 削 is a direct exclusion on 耗 (snapshot/kanji/耗.md:14). snapshot/kanji/耗.md:66-71 gives the reduction rationale and states that not every reduction is consumption. Complete 削る includes "to cut down; to curtail; to reduce" (evidence/reconciliation/jmdict-families.xml:18), and 削減 means "reduction" (evidence/reconciliation/jmdict-families.xml:20).
- O1 - RESOLVED - snapshot/kanji/塀.md:40-41 now says that ベイ appears voiced inside 土塀 and 板塀 while keeping its separate pinned KANJIDIC2 on-reading entry (evidence/reconciliation/kanjidic2-records.xml:22). The note is accurate and clear.
- O2 - RESOLVED - 用 is now guarded on 耗 (snapshot/kanji/耗.md:14). snapshot/kanji/耗.md:68-69 explains that the guard covers using up, not every use. This addresses the 用/使 inconsistency that O2 raised.
- O3 - DECLINE ACCEPTED - The point was optional consistency polish with low confidence and no demonstrated collision. The 際 card means edge, brink or occasion and has no wall or fence sense (original-packet/evidence/jmdict-families.xml:72-73). snapshot/kanji/塀.md:60-66 states the existing boundary/edge rationale for guarding 辺. No new defect arises from leaving 際 unguarded.
- O4 - DECLINE ACCEPTED - This was optional documentation polish. The existing Notes already group the unresolved separation, change, return, hatred and emptiness guards as conservative precautions based on 字通's old-dictionary strings. The 83 retained warnings are nonfatal and predate this revision (committed-checks/quiz-safety.log:15-103). 断 remains a harmless precaution, and leaving 絶 unguarded creates no established collision.
- O5 - RESOLVED - snapshot/kanji/耗.md:105-111 now names the curated 右, 川 and 本 and labels 石 and 未 "comparisons only, not curated choices". This removes the stale-distractor ambiguity.

## Verdicts
Correctness: CLEAN
Scoped coverage: CLEAN
Consistency and quiz safety: CLEAN
Comprehensibility: CLEAN

## Confirmation
Verdict: CONFIRMED
Basis: All seven dispositions are accepting. I checked each changed line in diffs/fix.patch for 塀, 拍 and 耗 against the supplied sources. Correctness: 城's historical カキ is supported by the 字通 名義抄 citation and by Daijisen き "垣をめぐらした所". The 拍 guards are supported by 突く "hit; strike", 鳴らす "beat; snap (fingers)", 勉 "encourage", 勇 "cheer up", 乗り "rhythm" (kana-preferred), 記す, 識 "write" / "written by", and 筆's writing senses. The 耗 guards are supported by 便り, Daijisen 信 and 音 (たより), 疲れる "worn out (of a well-used object)", 欠ける "wane", 下げる and 落ちる "reduce/decrease", rare 退く ひく "lessen", rare 磨れる "wear out", and 字通's impoverished-land and plant-decline senses. Each guard keeps its rarity, kana or historical qualification and makes no etymology claim. Comprehensibility: the four bounded non-collisions (耗/文, 耗/研, 耗/書, 拍/響) are reasonable distinctions between content and writing, surface working and depletion, and resonance and striking. New reading options are unchanged. Host checks show zero production or padded hits. No new defect was established.

## Findings
None.

## Optional
None.

## Limits
- L1: Model identity is runtime-reported only and was not independently verified.
- L2: The only evidence was chain material. Raw HTML responses, image-only historical glyphs in the 字通 and 漢字ペディア extracts, unchanged comparison cards outside the 28 reconciliation pairs, and the title index were not reread. Claims that depend on image glyphs stay as the cards qualify them.
- L3: Runtime exposure is evidenced only by bounded host logs for the N1, All and Starter pools plus one borrowed card. I did not verify whether a one-endpoint exclusion behaves symmetrically in the Kotlin app. Caller-built or multiple-borrow pools, native or device behaviour, font rendering, and compatibility with the older installed APK are unassessed. Latent ひゃく (拍/百) and ぼう (耗/乏, 耗/亡) reading collisions remain outside the shipped pools.
- L4: Allocation of the rare 拍つ family and of 字通's old-dictionary strings remains unresolved. The new 拍 writing/marking and 耗 historical guards are accepted as precautions only, not as proof of ordinary bare-character senses.
- L5: The host and static check logs (lint, quiz-safety, linkplan, reading-exposure, validate, manifest, unittest, budget, vocabulary and manifest-rebuild) were taken as supplied. They are not linguistic proof.

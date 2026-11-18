# B128 confirmation — N1-B128-CLAUDE-CONFIRM-001

## Snapshot
Commit: 7b3fd5c13c20f4b456723abe3de0ac42c4390bd4
Model: identity unverified (runtime reports Claude Opus 5.5; not independently confirmed)

## Scope
Chain: segments 1-32 read once each in order; no re-views
Fetches: none

## Dispositions
- F1 - RESOLVED - snapshot/kanji/唇.md:14 now declares 咲 directly on 唇 (fix diff diffs/fix.patch:9-10), and snapshot/kanji/唇.md:66-68 explains that the noun-like English "blossom; bloom" choice sits near the sourced petal sense while 咲く itself means "to bloom"; this matches JMdict 1194500 (flower/blossom/bloom/petal in one noun sense) and 1297210 (to bloom; archaic rising waves), and the Daijisen/Nikkoku petal sense in original-packet/evidence/external-snapshots/02-extract.txt:16 and :27. Exclusions are symmetric, so the single declaration covers the pair; 咲.md is unchanged and needs no change.
- O1 - DECLINE ACCEPTED - The author defers the optional phonetic-compound enrichment; the card keeps structure-unclassified, no phonetic field and an explicitly non-etymological mnemonic (snapshot/kanji/唇.md:5, :29-32). That hedge is not false and O1 was optional, so declining it leaves no defect.

## Verdicts
Correctness: CLEAN
Scoped coverage: CLEAN
Consistency and quiz safety: CLEAN
Comprehensibility: CLEAN

## Confirmation
Verdict: CONFIRMED
Basis: The only change affecting the scoped card is kanji/唇.md (diffs/fix.patch:1-35): F1's 咲 guard and note are correct against the complete JMdict/KANJIDIC2 records; the unrequested 刃 and 郊 guards (Q1, Q12) are conservative, accurately described as precautions for the context-poor 名義抄 脣=ホトリ gloss (original-packet/evidence/external-snapshots/02-extract.txt:64) without claiming synonymy, and they reference existing cards without overlapping distractors; curated 古/右/石 choices, readings, quiz selections, the word article and stroke data are unchanged; committed host checks pass with identical quiz-safety and reading-exposure logs; O1's decline is acceptable and no new defect was found.

## Findings
None.

## Optional
None.

## Limits
- L1: Raw stroke SVGs, raw HTML responses, the binary Joyo PDF, the superseded batch-128 source records referenced by path, and any chain-external file were not read; stroke JSON was not re-reviewed because it is unchanged.
- L2: The added 刃 and 郊 guards rest on the unresolved reach of a single old-dictionary quotation; I accept them as harmless conservative precautions, not as established lexical overlap. Their only cost is reduced fallback-pool variety, which was not modelled for custom pools.
- L3: Previously identified unread candidates 末, 隅, 葉, 紅 and 顔 remain unassessed; 鳴, 叫, 騒, 差, 房, 案, 在 and 鋭 were read in this chain and their no-guard dispositions (pair-dispositions Q3-Q14) are consistent with the opened records.
- L4: Host checks are static/bounded models only; custom/caller-built pools, multi-borrow Starter behaviour, Kotlin execution, native/device acceptance and compatibility with installed APK 5c000bd are not established.
- L5: Rendering of the variant 脣 (absent from bundled font cmaps) remains untested.
- L6: Execution-model identity is unverified.

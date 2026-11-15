# B120 confirmation — N1-B120-CLAUDE-001-CONFIRM-001

## Snapshot
Commit: c986ae49e844c08afc294d9381c7e486f2c9315d
Model: identity unverified (runtime reports Claude Opus 5.5; not independently verifiable in this pass)

## Scope
Chain: segments 1-35 of n1-b120-claude-001-confirm-001, each read once in order; no re-views. The run prompt was read once at kickoff as authorized.
Fetches: none

## Dispositions
- O1 - DECLINE ACCEPTED - The byte proof shows words/逮捕.md is CRLF in the candidate (34 CRLFs) and that the runtime tree is preserved except for the required wrapper after CRLF-to-LF normalization, which is how the manifest hashes text (coordinator/candidate-verification.json:14-15; coordinator/candidate-verification.json:26-30). The content format explicitly allows LF or CRLF (original-packet/repo/docs/content-format.md:76). Not restoring LF is therefore acceptable; the visible change remains only the 逮 wrapper, and linkplan still reports 1 added link and 0 problems (gates-committed-revision/linkplan.log:1).
- O2 - DECLINE ACCEPTED - The card still says only that the Joyo table lists タイ in 逮捕 (snapshot/kanji/逮.md:33). That remains true against the cached row "タイ 逮捕，逮夜" (original-packet/evidence/joyo-rows.json:10). My point was optional completeness, and the author's decline to add 逮夜 introduces no error.
- O3 - RESOLVED - The meaning line now attributes the gloss: "KANJIDIC2 glosses 逮 as apprehend and chase" (snapshot/kanji/逮.md:23; diffs/fix.patch:18-19). This matches KANJIDIC2 apprehend/chase (snapshot/docs/n1-sources/batch-120/reconciliation-001/kanjidic2-reconciliation-001.xml:617-618), so the "chase" label is no longer presented as an established modern usage.
- O4 - RESOLVED - 循 is now a direct exclusion on 逮 (snapshot/kanji/逮.md:14; diffs/fix.patch:10), with a qualified note (snapshot/kanji/逮.md:42). It is supported by 循's KANJIDIC2 follow/sequential glosses and by JMdict 追う, which places chase and follow after in one sense (snapshot/docs/n1-sources/batch-120/reconciliation-001/kanjidic2-reconciliation-001.xml:440-441; snapshot/docs/n1-sources/batch-120/reconciliation-001/jmdict-reconciliation-001.xml:886-891).

## Verdicts
Correctness: CLEAN
Scoped coverage: CLEAN
Consistency and quiz safety: UNVERIFIED
Comprehensibility: CLEAN

## Confirmation
Verdict: UNVERIFIED
Basis: All four optional points are accepted (O3 and O4 resolved; O1 and O2 declines supported by evidence), and every changed line in kanji/逮.md checks out against supplied sources. The prior open 逮/留 pair (D1/L1) is now settled and guarded: KANJIDIC2 留 lists detain/halt/stop and JMdict 1310670 sense 7 gives "to detain; to keep in custody" (esp. 留める), and the pair is declared on 逮. The other new guards 得/持/収/凌 are conservative English-label precautions that each rest on cited dictionary senses, and over-exclusion creates no ambiguity. However, reassessing my initial D5 disposition shows it inferred absence from a short title and card text: 押's card documents 押さえる "hold down", and no JMdict 押さえる/取り押さえる family was supplied to settle whether an ordinary seize/apprehend secondary sense makes "arrest; chase" a defensible answer for 押. This is the same kind of hold/custody overlap the author guarded for 持. The 逮/押 pair is declared on neither endpoint, so that consequential pair remains unsettled. No new defect is established.

## Findings
None.

## Optional
### O1: Assess 押 alongside the added 持 holding guard
- Facet: Consistency and quiz safety
- Severity: optional
- Confidence: low
- Citations: snapshot/kanji/逮.md:14; snapshot/kanji/逮.md:46; coordinator/pair-dispositions-neutral.md:28
- Evidence: The revision guards 持 as a "conservative English hold/custody versus taking into custody precaution", and the note groups holding with apprehension. 押 is not guarded. My initial D5 relied on 押's card documenting only push and hold down (押さえる), but the 押さえる/取り押さえる dictionary family was not in either packet, so a seizing/apprehending secondary sense was never ruled out.
- Suggestion: Extract the complete JMdict 押さえる and 取り押さえる families, then either add 押 to 逮's quiz_exclusions or record why the push/hold-down senses do not overlap apprehension.

## Limits
- L1: The 逮/押 direct pair is UNVERIFIED because no 押さえる/取り押さえる dictionary evidence was supplied, and my initial D5 harmless disposition rested on absence in the card text. This alone keeps the consistency facet and the confirmation at UNVERIFIED.
- L2: My initial D2/D3 claim that a chased target must be in view was categorical and is withdrawn. The harmless 捜/探 dispositions rest only on search versus pursuit having different goals in the opened card text. D6, D7, D9-D11 and D12 remain bounded observations, not certification of every secondary sense. The L3 candidates 禁, 束, 防 and 制 remain unread screening limits.
- L3: The O1 byte claim relies on the coordinator's mechanical proof. I did not inspect the raw base or candidate bytes of words/逮捕.md.
- L4: The bundled fonts contain 逮 but not standalone 辶 or 隶 (coordinator/font-coverage/output.log). The card names 辶 in its facts line and mnemonic, so native rendering of that glyph depends on system fallback and is unverified. Native, phone, arbitrary-pool, multi-borrow, Kotlin and old-APK (5c000bd) behavior and publication acceptance remain unverified. The committed-tree gates are host and structural evidence only.
- L5: Large supplied context sections (original-packet content-format.md and jlpt-levels.md, and the title index) were read but were not newly adjudicated beyond the scoped card. Raw SVG, raw HTML captures, the Joyo PDF and files not in the chain were not read.

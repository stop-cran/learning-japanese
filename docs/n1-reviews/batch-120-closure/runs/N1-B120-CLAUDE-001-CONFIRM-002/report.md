# B120 confirmation — N1-B120-CLAUDE-001-CONFIRM-002

## Snapshot
Commit: 356375e1d340573dc76e4f61826dfb9af9640bdd
Model: identity unverified (runtime reports Claude Opus 5.5; not independently verifiable in this pass)

## Scope
Chain: segments 1-38 of n1-b120-claude-001-confirm-002, each read once in order; no re-views. The run prompt was read once at kickoff as authorized.
Fetches: none

## Dispositions
- O1 - DECLINE ACCEPTED - The byte proof records that runtime content is preserved except for required wrappers, with CRLF-to-LF text hashing (coordinator/candidate-verification.json:13-14). words/逮捕.md is CRLF with 34 CRLFs (coordinator/candidate-verification.json:26-30). The format allows LF or CRLF (original-packet/repo/docs/content-format.md:76). The only visible change is the 逮 wrapper, and linkplan reports 0 problems (gates-correction-002/linkplan.log:1). No formatting repair is needed.
- O2 - DECLINE ACCEPTED - The card's sentence that the Joyo table lists タイ in 逮捕 (snapshot/kanji/逮.md:33) is true against the cached row "タイ 逮捕，逮夜" (original-packet/evidence/joyo-rows.json:10). Mentioning 逮夜 was optional completeness, and declining it introduces no error.
- O3 - RESOLVED - The meaning line now attributes "chase" to KANJIDIC2 (snapshot/kanji/逮.md:23; diffs/fix.patch:18-19), which matches the apprehend/chase glosses (original-packet/evidence/kanjidic2-records.xml:56-57) without claiming modern usage of "chase".
- O4 - RESOLVED - 循 is now a direct exclusion on 逮 with a qualified note (snapshot/kanji/逮.md:14; snapshot/kanji/逮.md:42). This is supported by JMdict 追う, which places chase and follow after in one sense (original-packet/evidence/jmdict-families.xml:217-224).

## Verdicts
Correctness: CLEAN
Scoped coverage: CLEAN
Consistency and quiz safety: CLEAN
Comprehensibility: CLEAN

## Confirmation
Verdict: CONFIRMED
Basis: All four optional points are accepted (O3 and O4 resolved; the O1 and O2 declines are supported by evidence). The only new runtime change since c986ae4 appends 押 to 逮's exclusions and adds one note (diffs/fix.patch). The previously open 逮/押 pair, my initial D5, is now settled. Complete JMdict 1589080 押さえる sense 3 gives "to get a hold of; to obtain; to seize; to catch; to arrest" with no spelling or reading restriction. JMdict 2011120 取り押さえる gives seize/capture/arrest, and KANJIDIC2 押 independently lists seize, stop, check and subdue. "arrest; chase" is therefore a defensible answer for 押 in the 押→逮 direction, and the direct pair is now declared on 逮. The added note accurately states that 押さえる has a seize/arrest sense alongside holding down, and that pushing itself is not arrest. The 逮/留 pair and the 得/持/収/凌/循 guards from the prior revision remain justified by the complete records reread here. Over-exclusion creates no answer ambiguity. The curated options 休/人/本 and the quiz-safety and reading-exposure logs are unchanged, and the 10 committed-tree gates pass. The coordinator erratum corrects only a spelling count in the author's source summary; the XML and the runtime card are unaffected. No new defect is established. The remaining limits are bounded screening, host-model and native-rendering limits, not consequential unresolved claims about the scoped card.

## Findings
None.

## Optional
None.

## Limits
- L1: Candidates 禁, 束, 防 and 制 from my initial L3 remain unread screening comparisons, not safety approvals. I judged them lower-risk than the now-guarded pairs, and no evidence opened in this pass raises them.
- L2: My initial D2/D3 claim that a chased target must be in view is withdrawn; the 捜/探 dispositions rest only on search and pursuit having different goals. D6, D7, D9-D11 and D12 remain bounded observations, not certification of every secondary sense.
- L3: The O1 byte claim relies on the coordinator's mechanical proof. I did not inspect raw base or candidate bytes.
- L4: The bundled fonts contain 逮 but not standalone 辶 or 隶 (coordinator/font-coverage/output.log). The card names 辶, so native rendering depends on system fallback and is unverified. Reading-exposure and quiz-safety logs are bounded host models. Arbitrary or multi-borrow pools, Kotlin, native/phone, the older installed APK 5c000bd (which predates quiz_exclusions) and publication acceptance remain unverified.
- L5: The JMdict and KANJIDIC2 extracts are reserialized complete records, not raw slices; I relied on their receipts for source binding. Raw SVG, raw HTML captures, the Joyo PDF and files outside the chain were not read. Supplied context documents (content-format.md, jlpt-levels.md, the title index) were read but not newly adjudicated beyond the scoped card.

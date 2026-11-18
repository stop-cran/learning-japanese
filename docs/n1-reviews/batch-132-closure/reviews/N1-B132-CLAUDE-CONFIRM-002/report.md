# B132 confirmation — N1-B132-CLAUDE-CONFIRM-002

## Snapshot
Commit: 009b70b2e6ec836d7364c6c3096b65b1fa9df65d
Model: identity unverified (session reports Claude Opus 5.5; no independent telemetry opened)

## Scope
Chain: segments 1-29 read once each in order; no re-views
Fetches: none

## Dispositions
- O1 - DECLINE ACCEPTED - Optional only; author keeps structure-unclassified with no phonetic (own-response.json:5; snapshot/kanji/墓.md:5), which the contract permits; no teaching claim depends on it.
- O2 - DECLINE ACCEPTED - Optional only; Common words unchanged (snapshot/kanji/墓.md:45-47). The gravestone basis for the 石 precaution is still stated in Meaning and Notes (snapshot/kanji/墓.md:23-25, 58-59), so omitting 墓石/墓参り is not a defect.

## Verdicts
Correctness: CLEAN
Scoped coverage: CLEAN
Consistency and quiz safety: CLEAN
Comprehensibility: CLEAN

## Confirmation
Verdict: CONFIRMED
Basis: The only runtime change (diffs/fix.patch:1-38) adds direct exclusions 標 and 塔 on 墓 with qualified Notes and citations. My initial review found neither pair required. Both are nevertheless supported as conservative guards. はか covers a grave marker or gravestone (survey-001 墓 Kotobank 日国), and 標 has a standalone しるし/mark sense, JMdict 1168060 esp. 印・標. 石塔 has stone-tower and gravestone senses (JMdict 1703230; 日国 石塔 ①②), 五輪塔 is glossed as a gravestone (JMdict 2843930), and 日国 says 塔 originally meant an Indian grave mound. The Notes accurately say 標 does not independently mean grave and that ordinary 供養塔 are generally not called graves (Nipponica 墓). The pairs are declared once on 墓, are direct and symmetric, and do not overlap the unchanged distractors 暮/募/川. Readings, quiz lists, distractors and the reading-exposure result are unchanged, and the committed gates report 0 errors. The 墓 card was not re-reviewed beyond the changed lines and their context. O1/O2 remain optional declines.

## Findings
None.

## Optional
### O1: Kana reading for 供養塔 in the new 塔 note
- Facet: Comprehensibility
- Severity: optional
- Confidence: medium
- Citations: snapshot/kanji/墓.md:63-66; source-reconciliation-001/jmdict-exact-families.xml:59-70
- Evidence: The new note uses 供養塔 with the English "memorial tower" but no kana. JMdict entry 1233930 reads it くようとう. Other Japanese words on the card carry kana readings.
- Suggestion: Write 供養塔 くようとう in the note for consistency with the card's other examples.

## Limits
- L1: The Weblio 墓 extract and the unchanged 暮, 募, 川 and words/墓.md articles were not reread in this delta pass. Their assessment rests on my initial review and the supplied unchanged-bytes verification.
- L2: Kotobank 墓塔 returned 404 and several Weblio captures were not supplied. Raw HTML, images and layout were not inspected. The committed gate logs are receipts, not linguistic proof.
- L3: The reading-exposure model covers only N1/All/Starter plus one borrowed card; its latent つか collision with 束 remains. Custom or multi-borrow pools, Kotlin/native/device behavior and older APK compatibility are not established. The added exclusions can reduce choices in small fallback pools; that is not modeled here.
- L4: Line citations into long external extracts are approximate where layout made exact counting uncertain; conclusions rest on text actually read in this chain.

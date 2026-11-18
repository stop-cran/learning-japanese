# B127 confirmation — N1-B127-CLAUDE-CONFIRM-001

## Snapshot
Commit: 6541c81fa9d58f25849562f19ab7b04282f392e3
Model: identity-unverified (runtime reports Claude Opus 5.5; not independently verified)

## Scope
Chain: segments 1-40 read once each, in order, with no re-views; the instruction file was read once at kickoff.
Fetches: none

## Dispositions
- O1 - DECLINE ACCEPTED - The optional pictograph tag was not adopted. The card keeps structure-unclassified and an explicitly labelled non-etymological mnemonic (snapshot/kanji/倉.md:5, snapshot/kanji/倉.md:29-33). The author correctly notes that Kanjipedia's 象形 account (original-packet/evidence/external-snapshots/01-extract.txt:29) and Jitsu's account (original-packet/evidence/external-snapshots/02-extract.txt:43-44) differ in detail and that the ancient-form images were not inspected. The rubric permits the conservative tag, so no defect remains.
- O2 - DECLINE ACCEPTED - The 亡 guard is kept and a 死 guard is added. The revised note now says the old ホロブ quotation's "ordinary currency is not established" (snapshot/kanji/倉.md:94-98), which states the precautionary basis I asked for. No guard is required for the もろし lookup, and no weak/fragile title is promoted. The remaining asymmetry with 倒 and 弱 is a precaution, not a contract requirement.

## Verdicts
Correctness: CLEAN
Scoped coverage: CLEAN
Consistency and quiz safety: CLEAN
Comprehensibility: CLEAN

## Confirmation
Verdict: CONFIRMED
Basis: The only runtime change is kanji/倉.md, which adds 12 direct exclusions (囲 保 預 容 留 持 忙 速 死 延 止 停) and matching notes. Each new claim checks out against the supplied sources: 囲い/囲う storage (JMdict 1155950 and 1155960), 忙しい hurried (JMdict 1519290 sense 2), standalone くら cancellation (Daijisen くら sense 2; Nikkoku くら sense 4), お倉入り postponement as a whole-word sense, and ほろぶ perish. No exclusion overlaps the unchanged curated 金/全/合, all targets exist, and the original 11 exclusions plus the 庫/蔵 required pair are kept. The reading selections, the 倉庫 article and the stroke data are unchanged, and the committed lint, validate, manifest, quiz-safety, reading-exposure, unittest, budget and vocabulary checks pass. Both of my optional items were declined acceptably, and I found no new established defect.

## Findings
None.

## Optional
### O1: Note the usual spelling of お蔵入り
- Facet: Comprehensibility
- Severity: optional
- Confidence: high
- Citations: snapshot/kanji/倉.md:84-85; snapshot/docs/n1-sources/batch-127-reconciliation/jmdict-comparison-records.xml:1987-1988
- Evidence: The new note writes the idiom as お倉入り, but JMdict flags that kanji form as rarely used; お蔵入り is the main form. A learner may read the 倉 spelling as the usual one.
- Suggestion: Write お蔵入り (rarely お倉入り), or add a brief spelling qualifier, without changing the guard rationale.

### O2: Nikkoku くら money-source sense compared with the curated 金 option
- Facet: Consistency and quiz safety
- Severity: optional
- Confidence: low
- Citations: original-packet/evidence/external-snapshots/02-extract.txt:25; snapshot/kanji/倉.md:13; snapshot/kanji/倉.md:25-27
- Evidence: Nihon Kokugo Daijiten くら sense 3 is a historical, 金蔵-derived "source of money" use. The revision guards the comparably qualified sense 4 (cancellation) with 止/停, but 金 "gold, money" remains a curated option that is always shown in the N1 and All pools. The card already separates the treasury place from the money itself, and a money source is not "money", so I do not establish a defect.
- Suggestion: Optionally add a short note that the historical money-source sense does not make 金 a correct answer, or record the decision in the pair-disposition table.

## Limits
- L1: My execution-model identity is unverified. Raw HTML responses, SVGs, the Joyo PDF, uncached sources and images were not read, and nothing was fetched.
- L2: The runtime evidence is supplied host/static logs. It does not cover caller-built or multi-borrow pools, Kotlin execution, native or phone acceptance, or the older installed APK, which ignores quiz_exclusions.
- L3: My initial report has small citation offsets that do not change its conclusions. Kanjipedia's pictograph line is 01-extract.txt:29, not :28. Its sense ② (にわか・あわてる) is :24, not :23. The 囲 store/keep KANJIDIC lines differ from the cited range.
- L4: Candidates listed as unread in the initial report remain unread, except 存 and 持, which this chain supplied. The 倒/弱 pairs remain deliberately unguarded. The new guards are conservative and are not proofs of synonymy.
- L5: Harmless and conservative dispositions are bounded by the supplied complete records and cards, not exhaustive proof against learner confusion.

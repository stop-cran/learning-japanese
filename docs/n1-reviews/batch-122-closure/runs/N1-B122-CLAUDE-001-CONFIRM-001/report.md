# B122 confirmation — N1-B122-CLAUDE-001-CONFIRM-001

## Snapshot
Commit: 4659f3a2e44ac01dc2e1a455db2fee300496b080
Model: identity unverified (the runtime reports Claude Opus 5.5, claude-opus-5.5; this pass cannot independently verify that)

## Scope
Chain: segments 1-31 of n1-b122-claude-001-confirm-001, each read once in order; no re-views. The instruction prompt was read once at kickoff as authorized.
Fetches: none

## Dispositions
- O1 - RESOLVED - The revised 悠 card adds 易 to quiz_exclusions (snapshot/kanji/悠.md:14; diffs/fix.patch:14-15) and explains it in Notes (snapshot/kanji/悠.md:47). The rationale matches the supplied evidence: JMdict 1605700 gives 悠々 easily/without difficulty (original-packet/evidence/jmdict-families.xml:131-136), and 易 is easy (neutral-kanjidic2.xml and 1157000/1545350/2672340). The pair is declared on 悠 and therefore symmetric. 易 is not one of 悠's distractors, and validate/lint report 0 errors.
- O2 - RESOLVED - The note now separates Weblio's character-dictionary section (はるか/とおい, original-packet/evidence/external-snapshots/01-extract.txt:94) from Digital Daijisen (はるか plus the name readings ちか/ひさ/ひさし, original-packet/evidence/external-snapshots/01-extract.txt:6-9) at snapshot/kanji/悠.md:43. It says that these readings change neither the KANJIDIC2 metadata nor the ユウ practice selection. The wording is accurate and clearer.
- O3 - DECLINE ACCEPTED - The author keeps 悠長 as comparison evidence and adds no word article (author-response/response.md:29-30; dispositions.md:78-79). The revised Notes do mention 悠長 slow/leisurely (snapshot/kanji/悠.md:47), but it is not in the common-words list. O3 was optional, and the card already covers the leisurely sense through 悠々 with a linked word and recognition compounds, so declining it leaves no defect.

## Verdicts
Correctness: CLEAN
Scoped coverage: CLEAN
Consistency and quiz safety: CLEAN
Comprehensibility: CLEAN

## Confirmation
Verdict: CONFIRMED
Basis: The only learner-facing change is to kanji/悠.md: ten added direct exclusions (常, 続, 易, 慢, 延, 伸, 幅, 遊, 娯, 快) and four revised or added Notes lines. Each new pair rests on cited displayed labels and ordinary senses I verified in the supplied KANJIDIC2/JMdict records and comparison cards: 常 long-lasting and とこ constant/eternal; 続 continue/last; 易 easy versus 悠々 easily; 慢 laziness and 緩慢 slow/sluggish versus 悠長 slow/leisurely; 延 and 伸 prolong/extend; 幅 width/latitude; 遊 idle/recreation and 娯 recreation versus 悠 leisure; 快 comfortable versus 悠々 comfortably. All fifteen earlier guards and the curated 側/後/達 options are unchanged. Every new target exists as a card, none overlaps a distractor, and the Notes claims about 常, 続, 凪 (wind or sea lull), 易, 快, 慢, 遊, 娯, 延, 伸 and 幅 match the evidence. The author's no-guard decisions for 優, 余, 簡 and 単 are defensible on the displayed labels; 優 is noted as optional below. The reading-exposure, quiz-safety and linkplan logs are byte-identical to the reviewed parent, and validate, lint, manifest, budget and unit tests pass. All three optional points are accepted, and there is no new established defect.

## Findings
None.

## Optional
### O1: Same-standard check for 優 and 優雅
- Facet: Consistency and quiz safety
- Severity: optional
- Confidence: medium
- Citations: snapshot/docs/n1-sources/batch-122-reconciliation/additional-jmdict.xml:746-773; snapshot/kanji/悠.md:14; snapshot/kanji/悠.md:47; original-packet/repo/kanji/優.md:3
- Evidence: JMdict 1539180 優雅 (news1) has a second sense: leisurely, comfortable, easy, carefree. The revision guards 易 and 快 on comparable word-level evidence from 悠々 (easily, comfortably), but leaves 優 "gentle; superior" unguarded. The author's character-level label judgment is defensible, since 優's character glosses are tenderness, gentleness and excellence, so this is not a defect.
- Suggestion: Optionally add 優 as a conservative direct guard, or record in the dispositions why the word-level 優雅 leisurely sense is treated differently from the 悠々 easily/comfortably senses used for 易 and 快.

## Limits
- L1: Execution-model identity is unverified.
- L2: The receipt JSON files (neutral-receipt.json, additional-receipt.json, author-reconciliation-receipt.json), the raw compressed KANJIDIC2/JMdict inputs, gate receipts, the summary.json gate file, the revised manifest.json and the commit signature were not supplied in the chain. Their hashes, membership and signature claims rest on the supplied verification JSON, not on fresh inspection.
- L3: Semantic dispositions are bounded by the displayed titles, the comparison cards and the complete records supplied. They are not an exhaustive lexical search; candidates beyond the author's 16 comparison cards were not re-surveyed in this pass.
- L4: Host reading-exposure and quiz-safety models do not establish caller-built or multi-borrow pools, Kotlin execution, native or device acceptance, or compatibility with the older installed APK 5c000bd, which ignores quiz_exclusions.
- L5: The 悠々 word article is byte-identical to the reviewed parent (same SHA-256) and was not re-reviewed beyond confirming that. The long content-format.md context was read but does not change the scoped card verdicts.

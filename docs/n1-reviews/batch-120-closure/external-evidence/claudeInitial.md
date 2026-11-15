# B120 initial review — N1-B120-CLAUDE-001

## Overall verdict
Verdict: UNVERIFIED

## Facet verdicts
### Correctness
Verdict: CLEAN
Basis: 逮 metadata (strokes 11, radical 辵/162, grade 8, JLPT 1, on タイ, no kun) matches evidence/kanjidic2-records.xml:9-57 and evidence/source-metadata.json:1-28; the meaning text and reading row match JMdict 1411470 (evidence/jmdict-families.xml:3-24), the Joyo row (evidence/joyo-rows.json:10) and the Daijisen/Wiktionary/漢字辞典 sections (evidence/external-snapshots/01-extract.txt:4-30). No established factual defect; the title's "chase" rests on KANJIDIC2 only (see O3).

### Scoped coverage
Verdict: CLEAN
Basis: The card teaches the sole Joyo reading タイ with the linked support 逮捕, labels the shape note as a mnemonic, uses structure-unclassified without a phonetic claim, and discloses the source-only ダイ/テイ/およぶ readings. The omission of 逮夜 from the Joyo example is optional (O2), not a coverage defect.

### Consistency/quiz safety
Verdict: UNVERIFIED
Basis: Curated distractors 休/人/本 are semantically and phonologically safe, and the 13 declared exclusions cover capture, chase, reach, stop and touch comparisons. However, the direct 逮/留 pair (arrest vs retain; stay, with a detention/stop branch asserted for 留 on another card) cannot be settled from the opened evidence and is declared on neither endpoint. The whole-file rewrite in diffs/existing.diff also hides any invisible byte change (O1).

### Comprehensibility
Verdict: CLEAN
Basis: The card is short, gives kana for its word, labels the mnemonic as not etymology, and qualifies each comparison note. The note contrasting "chase" with 追 while 逮's own title says "chase" could be clearer (O3), but no learner-blocking confusion is established.

## Segments read
Core chain: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 (each read once, in order; no re-views)
Extension chain: 1, 2, 3, 4, 5 (each read once, in order; no re-views)
Title index: I read evidence/title-index.txt source lines 1-1240 in full across core segments 12-14. Line 1 is "一 one" and line 1240 is "齢 age; years lived".
Also read: REVIEW.md, packet.json, both rubric files, repo/docs/content-format.md lines 1-139, repo/docs/jlpt-levels.md in full, snapshot/kanji/逮.md, snapshot/strokes/逮.json, diffs/existing.diff, snapshot/words/逮捕.md, all ten checks, the seven evidence files, the three C distractor cards (休, 人, 本), evidence/external-snapshots/manifest.json and its one SUPPLIED extract, 01-extract.txt.
I also read the run instruction file once at kickoff, as authorized.

## Phase-1 D/E lists
D: D1 留, D2 捜, D3 探, D4 循, D5 押, D6 障, D7 寄, D8 得, D9 過, D10 越, D11 超, D12 監
E: E1 捕, E2 追
Missing entries: none

## D/E cards read
| ID | Character | Displayed title | Related new card(s) | Reason | Disposition |
| --- | --- | --- | --- | --- | --- |
| D1 | 留 | retain; stay | 逮 | Possible overlap between arrest (take into custody, or stop) and 留's keep-in-place, stay and と.める/と.まる senses. 監 cites 留 for "detaining or keeping in place" (repo/kanji/監.md:146-151). | UNVERIFIED. 留's own text gives only retain, stay and fasten (repo/kanji/留.md:3, repo/kanji/留.md:20-22). No JMdict family for 留 or its detention compounds was supplied, so whether "arrest" is a defensible answer for 留 is unsettled. The pair is declared on neither endpoint (snapshot/kanji/逮.md:14, repo/kanji/留.md:11); 逮's curated options do not currently expose it. |
| D2 | 捜 | search; look for | 逮 | Hunting a suspect: "chase" vs searching, plus police-investigation context (捜査) (repo/kanji/捜.md:20). | Harmless. Searching seeks something whose location is unknown, while chasing pursues a target in view. The card notes that searching does not imply catching or finding. Shared crime context alone does not decide this (REVIEW.md:21-22). Declared on neither endpoint. |
| D3 | 探 | search | 逮 | Same seek-vs-chase comparison; 探る means probe or investigate (repo/kanji/探.md:20-22). | Harmless for the same reason as D2. No pursue, catch or arrest sense appears in 探's text. Declared on neither endpoint. |
| D4 | 循 | follow; cycle | 逮 | 逮's "chase" against 循's "follow". JMdict 追う glosses chase as "follow after" (evidence/jmdict-families.xml:217-224), and 循 itself excludes 追 because 追 includes following (repo/kanji/循.md:15, repo/kanji/循.md:43). | Harmless, medium confidence. 循 means following a course, rule or cycle (repo/kanji/循.md:24), which matches 追う sense 2, "follow a set order" (evidence/jmdict-families.xml:225-229). None of 逮's evidence gives a follow or cycle sense (evidence/external-snapshots/01-extract.txt:7-8, evidence/kanjidic2-records.xml:56-57). Declared on neither endpoint; see O4. |
| D5 | 押 | push | 逮 | Seize or hold down a person: 押さえる "hold down" (repo/kanji/押.md:22). | Harmless. The displayed title "push" and the documented hold-down/keep-steady senses do not give arrest or chase. The opened evidence contains no arrest sense for 押. Declared on neither endpoint. |
| D6 | 障 | obstruct; hinder | 逮 | English "arrest" in the sense of checking progress, against obstruct or hinder (repo/kanji/障.md:3, repo/kanji/障.md:20-21). | Harmless. 逮's card itself says arrest-as-stop does not make 逮捕 a word for stopping (snapshot/kanji/逮.md:44). Hindering is impeding, not apprehending or chasing, and 障's senses (malfunction, obstacle, screen) contain no custody or pursuit sense. Declared on neither endpoint; 障's exclusions are 害, 防 and 関 only. |
| D7 | 寄 | draw near; stop by | 逮 | Reach (及ぶ) against draw near, and stop by against arrest-as-stop (repo/kanji/寄.md:20-22). | Harmless. Approaching or dropping in is neither reaching a limit or extent nor apprehending someone. The "stop" in "stop by" means visiting, not halting someone. Declared on neither endpoint. |
| D8 | 得 | gain; acquire | 逮 | Capture vs obtain (repo/kanji/得.md:20). | Harmless. 逮's displayed title has no capture or obtain label, and 得 covers obtaining or advantage, not seizing a person. Declared on neither endpoint. |
| D9 | 過 | exceed; go beyond | 逮 | 逮's Daijisen sense 1, 及ぶ "reach", against passing beyond. JMdict supplies both families (evidence/jmdict-families.xml:25-130). | Harmless. 過ぎる glosses are pass, elapse and exceed, while 及ぶ glosses are reach and extend. Reaching a point is not going past it, and 逮's displayed title does not include reach. Declared on neither endpoint. |
| D10 | 越 | cross over; exceed | 逮 | Reach vs cross over (repo/kanji/越.md:20-22). | Harmless for the same reach-vs-beyond reason as D9. The 越える glosses are cross over and go beyond. Declared on neither endpoint. |
| D11 | 超 | exceed; surpass | 逮 | Reach vs exceed (repo/kanji/超.md:20). | Harmless for the same reason as D9. Declared on neither endpoint. |
| D12 | 監 | oversee; watch over | 逮 | Custody and confinement: 監禁 confinement, and Daijisen's prison branch (repo/kanji/監.md:28-35). | Harmless. 監's confinement compounds hold people after the fact, and the card distinguishes them from supervision. 監 has no apprehend or chase sense, and its 76-item exclusion list omits 逮 (repo/kanji/監.md:14). Declared on neither endpoint. |
| E1 | 捕 | capture | 逮 | Verifies 逮's note that 捕 means capture, and the constituent statement in 逮捕. | Already handled. 捕's text matches "catching or capturing" (repo/kanji/捕.md:3, repo/kanji/捕.md:20). The pair is declared on 逮 (snapshot/kanji/逮.md:14). |
| E2 | 追 | chase; pursue | 逮 | Verifies 逮's note that 追 means chase or pursue, against 逮's own "chase" title. | Already handled. The identical "chase" label makes exclusion necessary (repo/kanji/追.md:3, repo/kanji/追.md:20), and the pair is declared on 逮 (snapshot/kanji/逮.md:14). See O3 for the wording. |

## Per-card results
| Card | Correctness | Scoped coverage | Consistency/quiz safety | Comprehensibility | Evidence |
| --- | --- | --- | --- | --- | --- |
| 逮 | CLEAN | CLEAN | UNVERIFIED | CLEAN | KANJIDIC2, JMdict 1411470, Joyo row, Weblio extract, stroke JSON (11 strokes = card = KanjiVG canonical 11), checks; D1 unverified pair; O1-O4 |

## Findings
None.

## Optional points
### O1: Whole-file rewrite in the 逮捕 diff
- Facet: Consistency/quiz safety
- Severity: optional
- Confidence: medium
- Citations: diffs/existing.diff:5-73; snapshot/words/逮捕.md:25
- Evidence: The hunk removes and re-adds all 34 lines, but the only visible text difference is the [逮](../kanji/逮.md) wrapper on line 25. Its target (../kanji/逮.md from words/) is correct, and checks/linkplan.txt reports one added link and 0 problems. Rewriting every line implies an invisible byte change such as line endings, a BOM or trailing whitespace. Content-format allows LF or CRLF, so this is not shown to be a defect, but the raw bytes were outside my access.
- Suggestion: Confirm that the line endings and encoding of words/逮捕.md match the base file, and restore them if they changed, so the edit is limited to the link wrapper.

### O2: Joyo example list omits 逮夜
- Facet: Scoped coverage
- Severity: optional
- Confidence: high
- Citations: snapshot/kanji/逮.md:33; evidence/joyo-rows.json:10; evidence/external-snapshots/01-extract.txt:7
- Evidence: The card says the Joyo table lists タイ in 逮捕. The cached row is "タイ 逮捕，逮夜", and Daijisen's sense 1 (及ぶ) is illustrated by 逮夜. The statement is true but partial.
- Suggestion: Say that the Joyo table's examples are 逮捕 and 逮夜. Optionally mention 逮夜 as the vocabulary behind the reaching sense, without adding an article.

### O3: Title "chase" versus the note contrasting chase with 追
- Facet: Comprehensibility
- Severity: optional
- Confidence: medium
- Citations: snapshot/kanji/逮.md:3; snapshot/kanji/逮.md:42; evidence/kanjidic2-records.xml:56-57; evidence/external-snapshots/01-extract.txt:7-8
- Evidence: The title gives "chase" from the KANJIDIC2 gloss, but Daijisen gives only 及ぶ and 相手に手が届く/捕らえる, with no chase sense. The note then says 追 means chase and that an arrest and a chase are not the same event. A learner may be unsure whether 逮 itself means chase.
- Suggestion: Make clear that "chase" is KANJIDIC2's character gloss and that modern use is essentially 逮捕, catching someone. Alternatively, consider a title closer to Daijisen, such as "apprehend; reach", subject to title uniqueness and re-checking exclusions.

### O4: Conservative 逮/循 guard
- Facet: Consistency/quiz safety
- Severity: optional
- Confidence: low
- Citations: repo/kanji/循.md:3; repo/kanji/循.md:15; repo/kanji/循.md:43; repo/kanji/追.md:20; evidence/jmdict-families.xml:217-224
- Evidence: 循 (follow; cycle) excludes 追 because 追's chase sense includes following, and 追's card glosses chasing as following after. 逮 shares the "chase" label and has the same tags as 循 (jlpt-n1, grade-8, structure-unclassified), which are preferred in fallback. I judge the pair harmless because 逮 has no follow sense, but the precedent makes it borderline.
- Suggestion: Optionally add 循 to 逮's quiz_exclusions, or record why chase vs follow-a-course is safe here.

## Limits
- L1: The 逮/留 direct pair is UNVERIFIED. No JMdict family for 留める/留まる/留置/拘留 was supplied, and the only claim of a detention sense comes from another card (repo/kanji/監.md:146-151). This alone keeps the Consistency/quiz safety facet and the overall verdict at UNVERIFIED.
- L2: The raw stroke SVG, raw Weblio response HTML, binary Joyo PDF and every other packet asset outside the two chains were not read. Stroke JSON was checked only for stroke count, source revision and consistency with the card and shape-evidence; I made no visual geometry claim.
- L3: Identified but unread candidates: 及 has no card in the title index, so I made no request. 拘, 獲, 執 and 掴 likewise have no card, so there is no pair. 禁 (prohibit; ban, which has a confinement sense), 束 (bundle; 拘束 restraint), 防 (defend; ward off) and 制 (system; regulate; 制止 restrain) were judged lower-risk than the selected D entries and were not requested. They remain unread comparisons.
- L4: Reading-exposure and quiz-safety results are bounded host models of the N1, All and Starter pools. They do not cover custom or multi-borrow pools, Kotlin execution, native or phone acceptance, or compatibility with installed APK 5c000bd, which predates quiz_exclusions. JVM, emulator and device work remain on hold.
- L5: Automated checks (lint, validate, manifest, budget, unittest, vocabulary) are structural evidence only, not linguistic proof.
- L6: Execution-model identity is unverified. The runtime reports Claude Opus 5.5, but this pass cannot independently verify that.
- L7: No missing D/E entries were reported. All 14 requested cards were read through the extension chain.

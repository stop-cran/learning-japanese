# B132 initial review — N1-B132-CLAUDE-001

## Overall verdict
Verdict: CLEAN

## Facet verdicts
### Correctness
Verdict: CLEAN
Basis: Metadata (13 strokes, radical 土 no. 32, grade 5, ボ/はか, N1) matches KANJIDIC2 and the source row; meaning, gravestone note, モ/おくつき disclosures, 浅墓 ateji note and cited JMdict entries match the supplied JMdict, Kotobank and Weblio evidence.

### Scoped coverage
Verdict: CLEAN
Basis: Both KANJIDIC2 readings have rows with a dispositioned example; the only kun quiz reading はか has the linked existing word article; the on reading is deliberately not quizzed; the one required word-to-kanji link is added; source-only readings are disclosed rather than added to practice.

### Consistency/quiz safety
Verdict: CLEAN
Basis: Title "grave; tomb" is unique in the 1258-line index; 暮/募/川 are semantically distinct options; direct 墓/埋 and 墓/石 exclusions are declared on 墓 and are supportable; the four D comparisons (標, 塔, 寺, 亡) show no ordinary-sense ambiguity needing an exclusion; gates, manifest rebuild and link plan are clean.

### Comprehensibility
Verdict: CLEAN
Basis: The card states the meaning plainly, labels the mnemonic as non-etymological, explains why each distractor and exclusion differs, and qualifies the 浅墓 spelling; only optional polish remains.

## Segments read
Core chain: 1-37, each read once in order; no re-views.
Extension chain: 1-2, each read once in order; no re-views.
Both title indices were read in full: baseline-title-index.txt lines 1-1257 (first line 一 one, last line 齢 age; years lived) and title-index.txt lines 1-1258 (first line 一 one, last line 齢 age; years lived), the only addition being 墓 grave; tomb at title-index.txt:307.
All other core sources were read in full as delivered: REVIEW.md, packet.json, both rubric files, content-format.md, jlpt-levels.md, snapshot card, stroke JSON, baseline and snapshot word article, both diffs, all ten gate logs and receipts, all evidence JSON, all 95 JMdict and 7 KANJIDIC2 records, joyo row, cmap, shape, provenance, the 暮/募/川 cards and both complete external extracts.

## Phase-1 D/E lists
D: D1 標, D2 塔, D3 寺, D4 亡
E: E1 埋, E2 石
Missing entries: none

## D/E cards read
| ID | Character | Displayed title | Related new card(s) | Reason | Disposition |
| --- | --- | --- | --- | --- | --- |
| D1 | 標 | mark; signpost; goal | 墓 | 墓 can denote a grave marker or gravestone (01-extract.txt:22); 標 has mark/signpost/goal/standard/guide senses (repo/kanji/標.md:21-23, 30-32) | Harmless: no 標 sense in its card or readings is a grave, and a generic mark or signpost is not an ordinary meaning of 墓; neither endpoint declares the pair and neither lists the other as a distractor; no exclusion needed |
| D2 | 塔 | tower; pagoda | 墓 | Pagoda-shaped 五輪塔/宝篋印塔 served as grave markers (01-extract.txt:126) | Harmless: 塔 senses are tower, steeple, pagoda, stupa (repo/kanji/塔.md:18-20); a funerary use of a tower form does not make tower an ordinary meaning of 墓 or grave a meaning of 塔; pair undeclared on both endpoints; no exclusion needed |
| D3 | 寺 | Buddhist temple | 墓 | 隠語大辞典 lists regional slang 墓 = 寺院 (02-extract.txt:83-91 region of the Weblio extract) | Harmless: that is marked regional cant, not an ordinary sense; 寺 card gives only temple senses (repo/kanji/寺.md:18-20) and the encyclopedic sources separate temples and memorial halls from 墓 (01-extract.txt:59); pair undeclared on both endpoints; no exclusion needed |
| D4 | 亡 | deceased | 墓 | Shared death domain | Harmless: 亡 means death, perishing or passing away (repo/kanji/亡.md:18-20); 墓 names the place or structure, explicitly not the deceased person (snapshot/words/墓.md:32); pair undeclared on both endpoints; no exclusion needed |
| E1 | 埋 | bury; embed | 墓 | Existing 墓 quiz_exclusions target; burial overlap | Already handled: 埋 covers burying, covering and filling (repo/kanji/埋.md:18-20, 25-31); a learner could plausibly pick bury for a burial place; direct pair declared on 墓 (snapshot/kanji/墓.md:14), not on 埋; justified and accurately described at snapshot/kanji/墓.md:55-57 |
| E2 | 石 | stone | 墓 | Existing 墓 quiz_exclusions target; gravestone sense | Already handled: 日国 and Wiktionary include the gravestone or marker among things called はか (01-extract.txt:22); 石 card has only stone senses (repo/kanji/石.md:18-20); conservative direct pair declared on 墓 (snapshot/kanji/墓.md:14), not on 石; accurately described at snapshot/kanji/墓.md:58-59 |

## Per-card results
| Card | Correctness | Scoped coverage | Consistency/quiz safety | Comprehensibility | Evidence |
| --- | --- | --- | --- | --- | --- |
| 墓 | CLEAN | CLEAN | CLEAN | CLEAN | snapshot/kanji/墓.md:1-70 against kanjidic2-records.xml:5, jmdict-families.xml:17-36, 01-extract.txt:10-22, title-index.txt:307, quiz-safety.log:1-2, reading-exposure.log:1-33, diffs/existing.diff:1-13; D1-D4, E1-E2 table; O1-O2 |

## Findings
None.

## Optional points
### O1: Structure tag versus available phonetic evidence
- Facet: Correctness
- Severity: optional
- Confidence: medium
- Citations: snapshot/kanji/墓.md:5; evidence/shape-evidence.json:24-27; evidence/external-snapshots/01-extract.txt:103-104
- Evidence: The card uses structure-unclassified and gives no phonetic. KanjiVG marks the top 莫 group as phon, and 字通 classifies 墓 as 形声 with a phonetic element. The current conservative choice is allowed by the contract and is not a defect.
- Suggestion: Optionally record 字通's 形声 classification as sourced, hedged context, or keep structure-unclassified with a note that a phonetic analysis exists but is not adopted here.

### O2: Common gravestone and grave-visit words
- Facet: Scoped coverage
- Severity: optional
- Confidence: medium
- Citations: evidence/jmdict-families.xml:36-37; snapshot/kanji/墓.md:45-47; snapshot/kanji/墓.md:58-59
- Evidence: JMdict lists 墓参り はかまいり (ichi1) and 墓石 ぼせき／はかいし (gravestone). The card's 石 note relies on the gravestone sense, but Common words gives only 墓, 墳墓 and 墓地.
- Suggestion: Optionally add 墓石 and 墓参り as unlinked common words. 墓石 also shows the gravestone link behind the 石 precaution.

## Limits
- L1: Execution-model identity is unverified from within this pass; the session reports itself as Claude Opus 5.5, but no independent telemetry was opened.
- L2: Original selection XML, raw HTML responses, the KanjiVG SVG, font binaries and any non-chain asset were not opened. Stroke JSON was checked only for 13 strokes, matching the card, KANJIDIC2 and shape evidence; no visual geometry claim is made. Cmap coverage is not rendered acceptance.
- L3: Unread comparison candidates were identified but not requested because the opened evidence showed only shared subject matter, not ordinary-sense overlap: 死 death, 祖 ancestor, 骨 bone; place words 地 ground, land, 場 place, site, 所 location, 園 park; garden; and 跡 trace; footprint. Their dispositions rest only on displayed titles. 塚 (tomb, burial mound) and 碑, 葬, 陵, 墳 have no cards in either title index.
- L4: The reading-exposure audit models only N1/All/Starter pools plus one borrowed card; its latent つか collision with 束 in a Starter session borrowing 束 involves an archaic 名義抄 gloss, not card metadata. Custom or multi-borrow pools, Kotlin/native/device behavior and older APK compatibility are not established.
- L5: Line citations into external extracts beyond the first Kotobank page segment are approximate where the extract layout made exact counting uncertain (notably the Weblio 隠語大辞典 and Wiktionary sections). The claims rest on text actually read in core segments 36-37. Weblio's 隠語大辞典 entry is marked regional slang and was not treated as an ordinary sense.
- L6: Automated gates (lint, quiz safety, link plan, unittest, validate, manifest and reproducible rebuild, budget, vocabulary) are reported as receipts only and are not linguistic proof; JVM/emulator, publication and phone acceptance are out of scope.

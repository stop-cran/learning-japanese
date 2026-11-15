# B118 initial review — N1-B118-CLAUDE-001

## Overall verdict
Verdict: NEEDS FIX

## Facet verdicts
### Correctness
Verdict: CLEAN
Basis: 析 metadata (8 strokes, radical 木/75, grade 8, セキ, no kun) matches KANJIDIC2; the analysis meaning matches Daijisen and JMdict 分析/解析/析出; source-only readings シャク, さく and へぎ are attributed to Weblio sections that actually contain them; the mnemonic is labelled as non-etymological. No established defect.

### Scoped coverage
Verdict: CLEAN
Basis: The sole on-reading セキ is selected with its own linked 分析 example; 解析 and 析出 are shown as unlinked common words; the single required 分析 → 析 link wrapper is present. Nothing needed for the card's stated scope is missing.

### Consistency/quiz safety
Verdict: NEEDS FIX
Basis: 析's dividing/separating sense, which the card itself uses to justify excluding 分 and 割, is also covered by the displayed "separate" titles of 離 and 別. Neither direct pair is declared on either endpoint (F1). The seven declared exclusions and the three curated distractors are otherwise sound.

### Comprehensibility
Verdict: CLEAN
Basis: The card's short explanation, labelled mnemonic, single-row reading table and the notes that separate source-only readings are clear for learners; the one-link change to 分析 does not alter its prose.

## Segments read
Core chain: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 (each read once, in order; no re-views)
Extension chain: 1, 2, 3, 4, 5 (each read once, in order; no re-views)
Title index: I read evidence/title-index.txt source lines 1-1237 in full (core segments 10 and 11). Line 1 is "一 one" and line 1237 is "齢 age; years lived".
External snapshots: I read evidence/external-snapshots/manifest.json and its one SUPPLIED extract, 01-extract.txt, lines 1-78 (Daijisen, 歴史民俗用語辞典, 三国志小事典, Wiktionary, 漢字辞典, Weblio example sentences).
The instruction file was read once at kickoff, as authorized.

## Phase-1 D/E lists
D: D1 離, D2 別, D3 断, D4 絶, D5 刻, D6 削, D7 査, D8 調, D9 究, D10 研, D11 察, D12 診, D13 折, D14 片
E: E1 分, E2 解, E3 割, E4 切, E5 破, E6 剖, E7 板
Missing entries: none

## D/E cards read
| ID | Character | Displayed title | Related new card(s) | Reason | Disposition |
| --- | --- | --- | --- | --- | --- |
| D1 | 離 | separate; detach | 析 | 析 has a divide/separate sense: KANJIDIC2 "divide" (evidence/kanjidic2-records.xml:52), Daijisen こまかく分かつ (01-extract.txt:7), JMdict 析出 "separation" (jmdict-families.xml:69), and the card's own "separating things into parts" (snapshot/kanji/析.md:23) | Collision needing exclusion. "Separate" is a defensible answer for 析, and the same dividing basis already justifies the 析/分 and 析/割 guards. The pair is not declared on 析 (析.md:14) or 離 (repo/kanji/離.md:14, which guards only 別 分 放 去). Not currently in curated options, but fallback choices remain possible. See F1 |
| D2 | 別 | separate, another | 析 | Shares the English head word "separate" with 析's divide/separate sense (sources as D1). 別 itself means separation or distinctness (repo/kanji/別.md:20), and 切.md:45 groups 別 with separation | Collision needing exclusion. The "another" sense does not cancel the "separate" sense in the displayed title. 別 has no quiz_exclusions field (別.md:1-12) and 析 does not list 別. Not declared on either endpoint. See F1 |
| D3 | 断 | sever; refuse | 析 | KANJIDIC2 "chop" (kanjidic2-records.xml:51) versus "sever", which 断.md:46 glosses as "cut off" | Harmless, with medium confidence. Daijisen (01-extract.txt:7) gives 析 only as dividing finely and untangling; no opened source gives 析 a cut-off, terminate or refuse sense. Not declared on either endpoint. See O1 |
| D4 | 絶 | sever; cease | 析 | "sever" versus "chop" (as D3); 絶 concerns cutting off a connection or flow (repo/kanji/絶.md:20) | Harmless, with medium confidence. The opened 析 sources give no cut-off or cease sense, and "cease" is unrelated. Not declared on either endpoint. See O1 |
| D5 | 刻 | carve; time | 析 | 刻む means "chop finely; engrave" (repo/kanji/刻.md:30) versus 析 "chop" | Harmless. The displayed title says carve and time; carving or engraving is not a sense of 析 in KANJIDIC2 or Daijisen (01-extract.txt:7). Chopping finely is a 刻 word sense that is not displayed. Not declared on either endpoint |
| D6 | 削 | shave; sharpen; pare | 析 | 析 へぎ, a board made by thinly shaving and splitting wood (01-extract.txt:13-14) | Harmless. へぎ is a historical noun for a board, not a shaving verb sense of 析. No opened 析 source gives shave, sharpen or pare. Not declared on either endpoint |
| D7 | 査 | investigate; inspect | 析 | Investigation versus analysis | Harmless, with medium confidence. The repo's 分析 article separates investigation from analysis (snapshot/words/分析.md:28). KANJIDIC2 (kanjidic2-records.xml:51-54) and Daijisen (01-extract.txt:7) give no investigate or inspect sense for 析. Not declared on either endpoint |
| D8 | 調 | investigate; tune | 析 | Investigation versus analysis | Harmless, with medium confidence, on the same evidence as D7 (分析.md:28; 01-extract.txt:7). Not declared on either endpoint |
| D9 | 究 | investigate thoroughly | 析 | Thorough investigation or research versus analysis | Harmless, with medium confidence. 究 concerns research and pursuing a subject deeply (repo/kanji/究.md:20); 析 sources have no research sense (01-extract.txt:7). Not declared on either endpoint |
| D10 | 研 | polish; study closely | 析 | "study closely" is the closest English paraphrase of analyze in the index | Harmless, with medium confidence. 研's study sense is research or training (repo/kanji/研.md:20). 析's 解きほぐす sense (01-extract.txt:7) is untangling complexity, not study, and KANJIDIC2 lists no study sense. This is a borderline English-paraphrase risk, not a sourced shared sense. Not declared on either endpoint |
| D11 | 察 | observe; infer | 析 | Examining or judging from clues versus analysis | Harmless. 察 covers observation and inference (repo/kanji/察.md:20-21); no opened 析 source gives observe or infer. Not declared on either endpoint |
| D12 | 診 | diagnose; examine medically | 析 | Examination or assessment versus analysis | Harmless. The displayed title is specifically medical (repo/kanji/診.md:3, 診.md:20-21), and 析 has no medical sense. 診 guards 察 調 試 見 観 判 査 but not 析 (診.md:14). Not declared on either endpoint |
| D13 | 折 | fold | 析 | 折 also means break by bending (repo/kanji/折.md:20); 析 has "tear" and "chop"; the shapes are near look-alikes (扌 versus 木 plus 斤) | Harmless. The displayed "fold" is not a 析 sense, and bending or snapping is distinct from 析's divide or tear sense (kanjidic2-records.xml:51-54). Only the shape is similar. Not declared on either endpoint |
| D14 | 片 | one-sided; sheet | 析 | へぎ has the alias 片木, a thin split board (01-extract.txt:13-15), while 片 means a thin piece or sheet (repo/kanji/片.md:20) | Harmless. へぎ is a historical terminology reading of 析, and 片 appears only in its alias spelling. No opened source gives 析 a sheet or one-sided sense. Not declared on either endpoint |
| E1 | 分 | minute, part | 析 | 分's core is divide, and its わける reading is glossed "divide, separate" (repo/kanji/分.md:21, 分.md:30). This matches 析 "divide" | Already handled. The direct pair is declared on 析 (snapshot/kanji/析.md:14). Its basis also supports F1 |
| E2 | 解 | unravel; solve | 析 | 解 is unravelling (repo/kanji/解.md:20); 析 is こみ入ったものを解きほぐす (01-extract.txt:7); 解剖 has a figurative analysis sense (解.md:38) | Already handled. Declared on 析 (析.md:14) |
| E3 | 割 | split; proportion | 析 | Split or divide (repo/kanji/割.md:20) versus 析 divide | Already handled. Declared on 析 (析.md:14) |
| E4 | 切 | cut | 析 | Cut or sever (repo/kanji/切.md:20) versus 析 KANJIDIC2 chop (kanjidic2-records.xml:51) | Already handled. Declared on 析 (析.md:14); this is a conservative guard |
| E5 | 破 | tear; break | 析 | "tear" is an exact match for KANJIDIC2 "tear" (kanjidic2-records.xml:53; repo/kanji/破.md:3) | Already handled. Declared on 析 (析.md:14) |
| E6 | 剖 | dissect; split open | 析 | Separating something to examine it (repo/kanji/剖.md:20) versus 析's divide and analyze senses | Already handled. Declared on 析 (析.md:14) |
| E7 | 板 | plank; board | 析 | 析 へぎ is a thin split board (01-extract.txt:13-14); 板 is a board or plank (repo/kanji/板.md:20) | Already handled. Declared on 析 (析.md:14). This conservatively guards a historical sense and is harmless |

## Per-card results
| Card | Correctness | Scoped coverage | Consistency/quiz safety | Comprehensibility | Evidence |
| --- | --- | --- | --- | --- | --- |
| 析 | CLEAN | NEEDS FIX | NEEDS FIX | CLEAN | KANJIDIC2 record; JMdict 1199060/1503870/1645910/2139510; Joyo row; Weblio extract; shape evidence; title index; D1-D14 and E1-E7; F1, O1, O2 |

## Findings
### F1: Missing direct exclusions for the "separate" titles 離 and 別
- Facet: Consistency/quiz safety
- Severity: low
- Confidence: medium
- Citations: snapshot/kanji/析.md:14; snapshot/kanji/析.md:23; snapshot/kanji/析.md:44; evidence/kanjidic2-records.xml:52; evidence/external-snapshots/01-extract.txt:7; evidence/jmdict-families.xml:69; repo/kanji/離.md:3; repo/kanji/離.md:14; repo/kanji/離.md:59-61; repo/kanji/別.md:3; repo/kanji/別.md:20; repo/kanji/分.md:30; repo/docs/content-format.md:111-117
- Evidence: 析 has a sourced divide/separate sense: KANJIDIC2 "divide", Daijisen こまかく分かつ, and JMdict 析出 "separation". The card itself describes 析 as "separating things into parts" and guards 分 and 割 because of their dividing senses. The repo's 分 card glosses わける as "divide, separate", and 離's own notes treat separation as a direct overlap with 別 and 分. Yet 離 "separate; detach" and 別 "separate, another" display the head word "separate". Neither 析/離 nor 析/別 is declared on either endpoint (析.md:14; 離.md:14; 別 has no quiz_exclusions). The content-format contract says fallback choices can fill tag/random slots in larger quizzes and in level or custom pools. Then "separate" would be a defensible second answer for 析. With three curated options, the four-choice default does not currently expose this pair (checks/quiz-safety.txt), which limits severity, not the semantic collision.
- Required change: Add 離 and 別 to 析's quiz_exclusions; alternatively, declare 析 on each of those cards. Then rerun validate, the manifest build and the quiz-safety check.

## Optional points
### O1: Consider whether "sever" titles need guards alongside 切
- Facet: Consistency/quiz safety
- Severity: optional
- Confidence: low
- Citations: snapshot/kanji/析.md:44; evidence/kanjidic2-records.xml:51; evidence/external-snapshots/01-extract.txt:7; repo/kanji/断.md:46; repo/kanji/絶.md:20
- Evidence: 析 guards 切 "cut" on the basis of KANJIDIC2 "chop". 断 and 絶 display "sever", which 断.md glosses as "cut off". The Japanese Daijisen sense of 析 is dividing finely and untangling, not cutting off, so I judged these pairs harmless (D3, D4). Still, a reviewer who weights the English "chop" gloss heavily might see a weak overlap.
- Suggestion: Optionally record why 析/断 and 析/絶 are left unguarded, or add conservative guards if the 切 guard is meant to cover the whole cutting family.

### O2: Joyo sentence omits 析出, which the Joyo row lists
- Facet: Comprehensibility
- Severity: optional
- Confidence: high
- Citations: snapshot/kanji/析.md:33; evidence/joyo-rows.json:10
- Evidence: The Joyo extract lists 析出, 分析 and 解析 under セキ. The card says the table "also lists セキ in 分析 and 解析". That is accurate but incomplete, even though 析出 appears in Common words.
- Suggestion: Optionally mention all three Joyo examples (析出, 分析, 解析) in that sentence.

## Limits
- L1: The raw KanjiVG SVG, the raw Weblio HTML response (01-response.html), the binary Joyo PDF and every other packet asset outside the chains were not read. Joyo evidence is the pinned cached text only, and I make no fresh glyph or stroke-geometry claim. I checked the stroke JSON only for an 8-stroke count and a revision that matches shape-evidence.json.
- L2: I identified but did not request or read these candidates; I judged them weaker than the selected D entries: 散 (scatter), 判 (judge), 評 (appraise), 論 (argument; discourse), 理 (reason, logic), 観 (view; observe), 計 and 測 (measure), 験 and 試 (test), 区 (ward; district), 素 (unadorned; element). Any title-only judgments about them are UNVERIFIED.
- L3: Reading-exposure and quiz-safety outputs are bounded host models. They do not establish custom or multi-borrow Starter behavior, Kotlin execution, native or phone acceptance, or compatibility with installed APK 5c000bd, which predates quiz_exclusions. JVM and emulator work remain on hold and were not performed. Exclusion runtime semantics come from the content-format text, not app code.
- L4: The source-only readings シャク, さく and へぎ are checked only against the single supplied Weblio extract. Its sections come from separate dictionaries and are not a unified entry, and I did not independently verify the Wiktionary or 漢字辞典 content beyond that extract.
- L5: Execution-model identity is unverified by any evidence opened in this pass. The host environment reports Claude Opus 5.5, but this report does not certify it.
- L6: Semantic dispositions in the D/E table that are marked medium confidence (D3, D4, D7-D10) rest on the absence of the relevant sense in KANJIDIC2 and the Daijisen extract. That is not an exhaustive negative across all dictionaries.

# B118 initial review — N1-B118-CLAUDE-002

## Overall verdict
Verdict: NEEDS FIX

## Facet verdicts
### Correctness
Verdict: CLEAN
Basis: Metadata (8 strokes, radical 木 no. 75, onyomi セキ, empty kunyomi, grade 8) matches KANJIDIC2 and source-metadata; title "analyze" is a KANJIDIC2 meaning; word glosses match JMdict 1503870, 1199060 and 1645910; Joyo row lists セキ in 析出, 分析, 解析; source-only シャク, さく and へぎ statements match the Weblio Wiktionary, 漢字辞典 and 歴史民俗用語辞典 sections; the shape mnemonic is labelled and matches KanjiVG 木 left / 斤 right. No established defect.

### Scoped coverage
Verdict: CLEAN
Basis: The sole on-reading セキ has its own reading row with a linked 分析 example and is the only quiz selection; the empty kun list is explained; common words, source-only readings and look-alike/guard rationale are present. The one link wrapper in 分析 is the only required link pair. No missing in-scope content established.

### Consistency/quiz safety
Verdict: NEEDS FIX
Basis: The card's own meaning text ("separating things into parts"), KANJIDIC2 "divide", Daijisen こまかく分かつ and the JMdict 析出 gloss "separation" make the displayed title "separate" defensible for 析, yet the direct pairs 析/別 (separate, another) and 析/離 (separate; detach) are declared on neither endpoint, while the weaker-titled 分 (minute, part) is excluded for the same dividing sense. See F1. Curated options, readings, manifest and checks are otherwise consistent.

### Comprehensibility
Verdict: CLEAN
Basis: Explanations are short and standalone, kana is supplied for every Japanese word, the whole-word versus character distinction is explicit, mnemonic status is labelled, and source-only readings are clearly separated from practice readings.

## Segments read
Core chain: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 (each read once in order; no re-views)
Extension chain: 1, 2, 3, 4, 5, 6 (each read once in order; no re-views)
Title index: I read evidence/title-index.txt source lines 1-1237 (core segments 10 and 11); line 1 is "一 one" and line 1237 is "齢 age; years lived".
Also read in full: REVIEW.md, packet.json, both rubric files, repo/docs/content-format.md lines 1-139, repo/docs/jlpt-levels.md, snapshot/kanji/析.md, snapshot/strokes/析.json, diffs/existing.diff, snapshot/words/分析.md, all ten checks, the seven evidence files, the three C distractor cards (新, 本, 休), evidence/external-snapshots/manifest.json and its one SUPPLIED extract 01-extract.txt.

## Phase-1 D/E lists
D: D1 別, D2 離, D3 断, D4 絶, D5 査, D6 究, D7 調, D8 研, D9 察, D10 診, D11 判, D12 刻, D13 削, D14 区, D15 片, D16 盤, D17 折, D18 細, D19 論, D20 批
E: E1 分, E2 解, E3 割, E4 切, E5 破, E6 剖, E7 板
Missing entries: none

## D/E cards read
| ID | Character | Displayed title | Related new card(s) | Reason | Disposition |
| --- | --- | --- | --- | --- | --- |
| D1 | 別 | separate, another | 析 | Displayed "separate" versus 析 separating into parts (snapshot/kanji/析.md:23), KANJIDIC2 divide (evidence/source-metadata.json:18-23), 析出 separation (evidence/jmdict-families.xml:55-73); 別 also lists わ.ける (repo/kanji/別.md:10) | Collision needing exclusion (F1); direct pair declared on neither endpoint (snapshot/kanji/析.md:14; repo/kanji/別.md:1-12); curated options currently fill all slots so runtime exposure is fallback-only |
| D2 | 離 | separate; detach | 析 | Displayed "separate" versus the same 析 separating/division evidence; 離 itself guards 別 and 分 for separation (repo/kanji/離.md:14; repo/kanji/離.md:61-64) | Collision needing exclusion (F1); 離 declares 別, 分, 放, 去 but not 析 and 析 does not declare 離, so the direct pair is undeclared; 析/分 and 分/離 exclusions do not cover it (non-transitive) |
| D3 | 断 | sever; refuse | 析 | Sever = cut off (repo/kanji/断.md:41-46) versus KANJIDIC2 raw chop/divide for 析 (evidence/kanjidic2-records.xml:57-60) | Harmless: no opened source glosses 析 as sever, cut off or refuse; Daijisen gives こまかく分かつ and 解きほぐす (evidence/external-snapshots/01-extract.txt:7); pair undeclared on both endpoints; see optional O2 on consistency with the 切 guard |
| D4 | 絶 | sever; cease | 析 | Sever/cut off connection (repo/kanji/絶.md:20) versus 析 chop/divide | Harmless: neither sever nor cease is an opened 析 gloss (evidence/source-metadata.json:18-23); pair undeclared on both endpoints |
| D5 | 査 | investigate; inspect | 析 | Investigation versus analysis (repo/kanji/査.md:20) | Harmless: the 分析 article distinguishes 調査 investigation from 分析 analysis (snapshot/words/分析.md:28); no 析 gloss is investigate or inspect; undeclared |
| D6 | 究 | investigate thoroughly | 析 | Research/deep investigation versus analysis (repo/kanji/究.md:20) | Harmless: investigation and analysis are distinguished in snapshot/words/分析.md:28; no opened 析 gloss is investigate; undeclared |
| D7 | 調 | investigate; tune | 析 | Investigate/look up versus analyze (repo/kanji/調.md:20-22) | Harmless: snapshot/words/分析.md:28 separates information gathering from examining what it shows; tune is unrelated; undeclared |
| D8 | 研 | polish; study closely | 析 | Study closely/research versus analyze (repo/kanji/研.md:20-21) | Harmless: 研究 is research more broadly than analysis (snapshot/words/分析.md:28); polish is unrelated; no 析 gloss study; undeclared |
| D9 | 察 | observe; infer | 析 | Observation/inference from clues versus analysis (repo/kanji/察.md:20-22) | Harmless: no opened 析 source glosses observe or infer (evidence/source-metadata.json:18-23; evidence/external-snapshots/01-extract.txt:7); undeclared |
| D10 | 診 | diagnose; examine medically | 析 | Medical examination/assessment versus analysis (repo/kanji/診.md:23-27) | Harmless: displayed sense is restricted to medical examination; 析 has no medical gloss; 診 guards 察, 調, 査, 判 but not 析 (repo/kanji/診.md:14); undeclared |
| D11 | 判 | judge; seal | 析 | Judging/evaluating versus analysis (repo/kanji/判.md:20-22) | Harmless: judgment is a conclusion, not analysis; 析 sources give no judge sense; metadata わ.かる is not displayed or taught; undeclared |
| D12 | 刻 | carve; time | 析 | 刻む chop finely (repo/kanji/刻.md:20-21) versus KANJIDIC2 raw chop for 析 | Harmless: displayed carve/time are not 析 senses; the chop overlap is only through 刻's secondary verb and a raw KANJIDIC2 gloss not taught on 析; undeclared |
| D13 | 削 | shave; sharpen; pare | 析 | Shaving material away (repo/kanji/削.md:22); へぎ board is shaved thin (evidence/external-snapshots/01-extract.txt:14) | Harmless: shaving is how a へぎ board is made, not a sense of 析; no 析 gloss shave/pare; undeclared |
| D14 | 区 | ward; district | 析 | Division of an area and conceptual 区別 distinction (repo/kanji/区.md:20) | Harmless: displayed ward/district are administrative areas, not dividing into parts; undeclared |
| D15 | 片 | one-sided; sheet | 析 | Thin piece or sheet (repo/kanji/片.md:20) versus へぎ thin board, alias 片木 (evidence/external-snapshots/01-extract.txt:13-15) | Harmless: the へぎ reading is a single historical-terminology entry, not a KANJIDIC2, JMdict or Daijisen sense of 析; "sheet" is not an ordinary 析 meaning; undeclared |
| D16 | 盤 | board; disc | 析 | Board versus へぎ board sense that the card uses to guard 板 (snapshot/kanji/析.md:45) | Harmless on the ordinary-sense standard (へぎ is historical terminology only, evidence/external-snapshots/01-extract.txt:13-15); undeclared on both endpoints (repo/kanji/盤.md:14); inconsistent with the 板 guard, see O1 |
| D17 | 折 | fold | 析 | Shared 斤 shape and break-by-bending sense (repo/kanji/折.md:20); JMdict records 解折 as an irregular spelling of 解析 (evidence/jmdict-families.xml:10-13) | Harmless for meaning: fold/break are not 析 glosses; the overlap is visual and the irregular spelling, not meaning; undeclared |
| D18 | 細 | slender; fine; detailed | 析 | Fine/detail versus こまかく分かつ divide finely (evidence/external-snapshots/01-extract.txt:7; repo/kanji/細.md:20) | Harmless: こまかく is only the manner of 析's dividing; slender/fine/detailed are adjectives not glossed for 析; undeclared |
| D19 | 論 | argument; discourse | 析 | Reasoned argument versus analysis (repo/kanji/論.md:20-22) | Harmless: discussion and argument are not analysis glosses in any opened 析 source; undeclared |
| D20 | 批 | criticize; critique | 析 | Examining by comparison and judging (repo/kanji/批.md:23) | Harmless: displayed critique/criticize is evaluative judgment; 析 sources give no criticize sense; 批 guards 判 and 責 only (repo/kanji/批.md:14); undeclared |
| E1 | 分 | minute, part | 析 | Dividing core idea and わける divide, separate (repo/kanji/分.md:20; repo/kanji/分.md:30) | Already handled: declared on 析 (snapshot/kanji/析.md:14); exclusion justified by the secondary dividing sense, which also shows separate is within this family |
| E2 | 解 | unravel; solve | 析 | Unravel versus 解きほぐす; 解剖 figurative analysis (repo/kanji/解.md:39); 解析 analysis (evidence/jmdict-families.xml:3-33) | Already handled: declared on 析 (snapshot/kanji/析.md:14); needed |
| E3 | 割 | split; proportion | 析 | Split/divide (repo/kanji/割.md:20-21) versus 析 divide | Already handled: declared on 析; needed |
| E4 | 切 | cut | 析 | Cutting/severing (repo/kanji/切.md:20) versus KANJIDIC2 chop | Already handled: declared on 析; conservative but defensible given the chop gloss |
| E5 | 破 | tear; break | 析 | Tear (repo/kanji/破.md:3) versus KANJIDIC2 tear (evidence/source-metadata.json:21) | Already handled: declared on 析; conservative but defensible |
| E6 | 剖 | dissect; split open | 析 | Separating to examine; 解剖 figurative analysis (repo/kanji/剖.md:22) | Already handled: declared on 析; needed |
| E7 | 板 | plank; board | 析 | Board versus へぎ thin board (evidence/external-snapshots/01-extract.txt:13-15; repo/kanji/板.md:20) | Already handled: declared on 析 (snapshot/kanji/析.md:14); conservative given the historical-only へぎ sense |

## Per-card results
| Card | Correctness | Scoped coverage | Consistency/quiz safety | Comprehensibility | Evidence |
| --- | --- | --- | --- | --- | --- |
| 析 | CLEAN | CLEAN | NEEDS FIX | CLEAN | KANJIDIC2 record, source-metadata, JMdict families 1199060/1503870/1645910/2139510, Joyo row, shape evidence, Weblio extract, 分析 article and diff, checks; F1, O1, O2 |

## Findings
### F1: Missing direct 析/別 and 析/離 quiz exclusions for the separate sense
- Facet: Consistency/quiz safety
- Severity: medium
- Confidence: medium
- Citations: snapshot/kanji/析.md:14; snapshot/kanji/析.md:23; snapshot/kanji/析.md:44; evidence/source-metadata.json:18-23; evidence/external-snapshots/01-extract.txt:7; evidence/jmdict-families.xml:55-73; repo/kanji/別.md:3; repo/kanji/離.md:3; repo/kanji/離.md:14; repo/kanji/分.md:30; repo/kanji/剖.md:22
- Evidence: The card teaches 析 as "associated with separating things into parts" (line 23); KANJIDIC2 gives divide, Daijisen こまかく分かつ, and JMdict glosses 析出 as separation. The card excludes 分 (displayed "minute, part") for its dividing sense, and the corpus treats separate as part of that family (分 わける "divide, separate"; 剖 card "divide; separate"). Yet 別 displays "separate, another" and 離 displays "separate; detach", and neither direct pair with 析 is declared on either endpoint. 離 guards 別 and 分 but not 析; exclusions are not transitive. A learner shown "analyze" and "separate" for 析 has two defensible answers on the card's own wording. Current curated four-choice quizzes fill all slots from 新/本/休 (checks/quiz-safety.txt), so exposure is through fallback, larger or custom pools.
- Required change: Add 別 and 離 to quiz_exclusions on 析 (or on the other endpoints) and mention the separation overlap in the Notes, or reword the meaning text so it no longer presents separating as a standalone meaning of 析 and document why the pairs are safe.

## Optional points
### O1: Board guard for 板 is not applied to 盤
- Facet: Consistency/quiz safety
- Severity: optional
- Confidence: medium
- Citations: snapshot/kanji/析.md:45; repo/kanji/盤.md:3; repo/kanji/盤.md:14; evidence/external-snapshots/01-extract.txt:13-15
- Evidence: 析 guards 板 because of the separate historical へぎ thin-board sense, but 盤 also displays "board; disc" and the 析/盤 pair is undeclared on both endpoints. Because へぎ is attested only in one historical-terminology section, I judge 析/盤 harmless on the ordinary-sense standard, which makes the 板 guard conservative rather than required; the rationale is uneven.
- Suggestion: Either also guard 盤 for consistency with the stated board rationale, or state in Notes that the 板 guard is precautionary because へぎ is a historical-terminology reading only.

### O2: Cut guard for 切 is not applied to 断
- Facet: Consistency/quiz safety
- Severity: optional
- Confidence: low
- Citations: snapshot/kanji/析.md:44; repo/kanji/断.md:3; repo/kanji/断.md:41-46; evidence/kanjidic2-records.xml:57-60
- Evidence: 析 guards 切 (cut) for overlap with cutting, based on the raw KANJIDIC2 chop gloss. 断 displays "sever; refuse" and its card says sever means cut off. No opened source glosses 析 as sever, so I judge 析/断 harmless, but the cutting rationale used for 切 would apply similarly.
- Suggestion: Consider guarding 断 as well, or narrow the Notes rationale for 切 so that it does not imply all cutting-family titles are unsafe.

## Limits
- L1: Unread inputs outside the chains: raw KanjiVG SVG, the raw Weblio response HTML, the binary Joyo PDF, the pinned N1 source file, the source contract and every other packet asset. Stroke JSON was checked only against card, shape-evidence and contract text (8 strokes, matching revision); no visual geometry claim is made.
- L2: N1 membership rests on sourceRow 528 in source-metadata and provenance pins; the KANJIDIC2 jlpt field 1 is an old-level value and was not treated as N1 proof. The N1 source file itself was not opened.
- L3: Execution-model identity is unverified; the host labels this session Claude Opus 5.5, but I cannot independently verify that.
- L4: Reading-exposure and quiz-safety evidence model bounded host pools only; no custom or multi-borrow Starter behavior, Kotlin execution, native or phone acceptance, or compatibility with installed APK 5c000bd (which predates quiz_exclusions) is claimed. JVM and emulator work were not performed.
- L5: Identified but unread candidates, judged lower ambiguity and not requested: 半 half, 散 scatter, 理 reason/logic, 計 and 測 measure, 算 calculate, 評 appraise, 験 test/verify, 観 view/observe, 刈 mow, 刃 blade, 版 printing plate, 札 tag. 検 and 裂 have no cards in the title index.
- L6: repo/docs/content-format.md was read only for lines 1-139; repo/words in the packet contains only 分析, so 解析 and 析出 have no articles and their status was judged from JMdict only.
- L7: JMdict 2139510 records 析 as a search-only form of 柝 (wooden clappers); the card does not mention it. I treat this as a non-teaching spelling note, not a defect, but did not verify any further 柝-related usage.
- L8: F1's NEEDS FIX rests on a semantic judgment that "separate" is a defensible answer for 析; automated checks do not test semantic ambiguity, and the decision ultimately requires editorial adjudication.

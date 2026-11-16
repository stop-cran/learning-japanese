# B130 initial review — N1-B130-CLAUDE-004

## Overall verdict
Verdict: NEEDS FIX

## Facet verdicts
### Correctness
Verdict: CLEAN
Basis: Metadata, readings, senses, source attributions and supplemental-form claims on all three cards match the opened KANJIDIC2 records, JMdict families, cached Joyo rows and the supplied Daijisen, 字通, 漢字ペディア, Wiktionary and KANJIDIC-derived Weblio extracts; the three link wrappers point to the correct cards; no established factual error was found.

### Scoped coverage
Verdict: CLEAN
Basis: Each card covers its displayed senses, full on-reading inventory with dispositions, the selected practice reading with a linked article, supplemental forms with qualification, and the needed look-alike and comparison notes; no needed distinction is missing for the scoped task.

### Consistency/quiz safety
Verdict: NEEDS FIX
Basis: Two direct pairs involving 耗 have ordinary overlapping senses but no declared exclusion on either endpoint: 耗/擦 (擦れる "wear out") together with 耗/摩 (摩耗 wear; "chafe"), and 耗/削 ("pare", 削る "cut down", 削減 "reduction"); the card's own conservative standard guards far weaker labels.

### Comprehensibility
Verdict: CLEAN
Basis: Titles, explanations, mnemonic labelling, reading tables and notes are clear and qualified; the points below are optional polish, not established defects.

## Segments read
Core chain: segments 1-87 read in order, each once, ending with the END OF CHAIN terminator in segment 87; no re-views.
Extension chain: segments 1-8 read in order, each once, ending with END OF CHAIN in segment 8; no re-views.
Title index: read evidence/title-index.txt source lines 1-1254 in full (core segments 78-79); line 1 is "一 one" and line 1254 is "齢 age; years lived".
Also read in core: REVIEW.md, packet.json, both rubric files, content-format.md lines 1-139, jlpt-levels.md, the three snapshot cards, three stroke JSON files, diffs/existing.diff, the three changed word articles, all ten checks, xml-presentation.json, source-metadata.json, kanjidic2-records.xml, jmdict-families.xml, dictionary-index.json, joyo-rows.json, shape-evidence.json, provenance.json, the five curated distractor cards (古 右 石 川 本), the external-snapshot manifest and all seven supplied extracts.

## Phase-1 D/E lists
D: D1 際, D2 限, D3 門, D4 城, D5 節, D6 歌, D7 鳴, D8 響, D9 討, D10 拝, D11 度, D12 符, D13 用, D14 磨, D15 削, D16 疲, D17 乏, D18 欠, D19 枯, D20 着, D21 絶, D22 劣
E: E1 摩, E2 擦, E3 断, E4 使, E5 曲, E6 辺
Missing entries: none

## D/E cards read
| ID | Character | Displayed title | Related new card(s) | Reason | Disposition |
| --- | --- | --- | --- | --- | --- |
| D1 | 際 | edge; occasion | 塀 | edge/side vs boundary wall (repo/kanji/際.md:3, 21-22) | Harmless: 際 covers an edge or occasion (窓際, その際), not a wall or fence; no direct pair declared; consistency with the 辺 guard noted as O3 |
| D2 | 限 | limit | 塀 | limit/boundary on amount or time (repo/kanji/限.md:21-22) | Harmless: 限 limits amount, time or eligibility; no structure sense; no pair declared |
| D3 | 門 | gate; doorway | 塀 | boundary structure (repo/kanji/門.md:21) | Harmless: a gate is an entrance, and the 塀 word article treats a gate as related, not as the wall itself (snapshot/words/塀.md:31); no pair declared |
| D4 | 城 | castle | 塀 | fortification walls (repo/kanji/城.md:21) | Harmless: 城 names a castle only; no wall or fence sense in the card; no pair declared |
| D5 | 節 | joint; season; restraint | 拍 | music senses (tune, section, verse) (repo/kanji/節.md:25-26, 32) | Harmless: 節's music senses are melody, section and verse, not beat or clapping, and its title shows no music label; no pair declared |
| D6 | 歌 | song, sing | 拍 | music domain (repo/kanji/歌.md:21) | Harmless: singing and songs are not clapping or a beat; the 曲 guard on 拍 is a precaution, not a requirement (repo/kanji/曲.md:21-23) |
| D7 | 鳴 | animal call; ring | 拍 | sounding/ringing (repo/kanji/鳴.md:21-24) | Harmless: animal calls and ringing are not clapping or a beat; no pair declared |
| D8 | 響 | resound; echo | 拍 | sounding (repo/kanji/響.md:22-28) | Harmless: resounding and influence, not clapping or beat; 響 guards 音 and 鳴 but not 拍, which is adequate |
| D9 | 討 | attack; discuss | 拍 | 討つ うつ attack vs 拍つ strike (repo/kanji/討.md:22-26) | Harmless: 討つ is attacking or defeating an enemy, not clapping; 拍つ is a rare spelling in the separate 打つ family (evidence/jmdict-families.xml:116); no pair declared |
| D10 | 拝 | worship; bow in respect | 拍 | shrine prayer clapping context (repo/kanji/拝.md:21) | Harmless: 拝 means worship or bowing; ritual clapping belongs to the word 拍手 or 柏手, not to 拝 (evidence/jmdict-families.xml:254) |
| D11 | 度 | degree, number of times | 拍 | counter (repo/kanji/度.md:21) | Harmless: degrees and counting occasions; a beat is a musical unit, not an occurrence counter |
| D12 | 符 | token; sign; charm | 拍 | marking senses in the 打つ family (repo/kanji/符.md:21) | Harmless: 符 is a token, sign or ticket; the 打つ "mark" sense is not an ordinary bare-拍 sense (snapshot/kanji/拍.md:54-60) |
| D13 | 用 | use, purpose | 耗 | use vs wear down through use (repo/kanji/用.md:3, 21) | Harmless as a semantic choice: 耗 does not mean "use"; inconsistency with the declared 耗/使 guard noted as O2 |
| D14 | 磨 | polish; grind | 耗 | 磨耗 wear (repo/kanji/磨.md:21, 33) | Harmless: polishing and grinding are not decrease; 磨 itself lists rubbing only through 磨る する; lower overlap than 擦 (F1) |
| D15 | 削 | shave; sharpen; pare | 耗 | pare/reduce vs decrease (repo/kanji/削.md:23, 32, 42) | Collision needing exclusion: 削る covers reducing an amount and 削減 means reduction; no pair declared on either card (F2) |
| D16 | 疲 | grow tired | 耗 | exhaustion in 消耗 (repo/kanji/疲.md:21-23) | Harmless: tiredness is a 消耗 whole-word sense; 耗's character senses are decrease and wearing down (evidence/external-snapshots/04-extract.txt:11) |
| D17 | 乏 | scarce; lacking | 耗 | scarcity vs depletion (repo/kanji/乏.md:23-27) | Harmless: 乏 describes an insufficient state, not a decrease process; no pair declared |
| D18 | 欠 | lack; gap | 耗 | lack vs depletion (repo/kanji/欠.md:21-23) | Harmless: missing or chipped, not decreasing through use |
| D19 | 枯 | wither; dry up | 耗 | depletion as drying up (repo/kanji/枯.md:21) | Harmless: the card limits 枯 to plants withering and explicitly warns against extending it |
| D20 | 着 | wear; arrive | 耗 | shared English head word "wear" (repo/kanji/着.md:3, 21-22) | Harmless: 着's "wear" is putting on clothes, a different English sense; the full 耗 title "decrease; wear down through use" is distinct |
| D21 | 絶 | sever; cease | 耗 | 絶える die out vs used up (repo/kanji/絶.md:21, 31) | Harmless: ceasing and severing are not decrease; consistency with the unexplained 断 guard noted as O4 |
| D22 | 劣 | inferior; worse | 耗 | deterioration (repo/kanji/劣.md:21-23) | Harmless: comparison of quality, not depletion |
| E1 | 摩 | rub; chafe | 耗 | exclusion target of 拍; 摩耗 wear and "chafe" (repo/kanji/摩.md:3, 14, 23) | Collision needing exclusion, together with 擦: the 摩/拍 pair is declared but 摩/耗 is not declared on either card (F1) |
| E2 | 擦 | scrape; scrub | 耗 | exclusion target of 拍; 擦れる "wear out" (repo/kanji/擦.md:14, 33) | Collision needing exclusion: 擦's own reading row glosses "wear out"; pair undeclared on both 耗 (snapshot/kanji/耗.md:14) and 擦 (F1) |
| E3 | 断 | sever; refuse | 耗 | exclusion target of 耗 (repo/kanji/断.md:21-23) | Already handled: 耗/断 declared on 耗; 断's card shows no depletion sense, so the rationale is unstated (O4) |
| E4 | 使 | use, employ | 耗 | exclusion target of 耗 (repo/kanji/使.md:21-22) | Already handled: 耗/使 declared on 耗; 使う also covers spending, which supports the precaution; comparison with 用 in O2 |
| E5 | 曲 | bend; musical piece | 拍 | exclusion target of 拍 (repo/kanji/曲.md:21-23) | Already handled: 拍/曲 declared on 拍; a musical piece is not a beat, so the guard is precautionary and does not require guarding 歌 or 節 |
| E6 | 辺 | vicinity; edge | 塀 | exclusion target of 塀 (repo/kanji/辺.md:21) | Already handled: 塀/辺 declared on 塀; edge/vicinity is not a wall, so the guard is precautionary (O3) |

## Per-card results
| Card | Correctness | Scoped coverage | Consistency/quiz safety | Comprehensibility | Evidence |
| --- | --- | --- | --- | --- | --- |
| 塀 | CLEAN | CLEAN | CLEAN | CLEAN | KANJIDIC2 record, JMdict 1506870 and 塀 families, Daijisen/字通/Wiktionary extracts, cached Joyo row, title index, distractors 古 右 石, D1-D4 and E6; O1, O3 |
| 拍 | CLEAN | CLEAN | CLEAN | CLEAN | KANJIDIC2 record, JMdict 2236150 and 1408810 families, Daijisen/字通/Wiktionary extracts, cached Joyo row, title index, distractors 古 右 川, D5-D12 and E5 |
| 耗 | CLEAN | CLEAN | NEEDS FIX | CLEAN | KANJIDIC2 record, JMdict 消耗/摩耗 families, Daijisen/字通/漢字ペディア extracts, cached Joyo row, title index, distractors 右 川 本, D13-D22 and E1-E4; F1, F2, O2, O4, O5 |

## Findings
### F1: Undeclared 耗/擦 and 耗/摩 wear pairs
- Facet: Consistency/quiz safety
- Severity: medium
- Confidence: medium
- Citations: snapshot/kanji/耗.md:3; snapshot/kanji/耗.md:14; snapshot/kanji/耗.md:26-27; repo/kanji/擦.md:14; repo/kanji/擦.md:33; repo/kanji/摩.md:3; repo/kanji/摩.md:14; repo/kanji/摩.md:23; evidence/jmdict-families.xml:243; evidence/external-snapshots/04-extract.txt:11
- Evidence: 耗's title is "decrease; wear down through use", and Daijisen glosses it すりへる (wear down by rubbing), with 摩耗 among its examples. The 耗 card says 摩耗 "specifically illustrates wear through friction", and JMdict glosses 摩耗/磨耗 "wear; abrasion". 擦's own reading row glosses 擦れる すれる "to rub; to chafe; to wear out", and 摩's title "rub; chafe" names wearing by friction. Neither direct pair is declared: 耗's list lacks 擦 and 摩, 擦's list is only 磨 and 掃, and 摩's list is only 擦, 磨 and 研. In 擦's meaning quiz, "decrease; wear down through use" is defensible for its ordinary すれる "wear out" sense. 耗 meanwhile guards far weaker labels such as 殺 and 濃. The current N1/All/Starter pools never show these options because the curated choices fill every slot. Fallback, custom or smaller pools could show them.
- Required change: Add 擦 and 摩 to 耗's quiz_exclusions, or declare them on 擦/摩, and mention them in 耗's Notes. Then re-run validation and the manifest rebuild.

### F2: Undeclared 耗/削 reduce pair
- Facet: Consistency/quiz safety
- Severity: low
- Confidence: medium
- Citations: snapshot/kanji/耗.md:3; snapshot/kanji/耗.md:14; repo/kanji/削.md:3; repo/kanji/削.md:23; repo/kanji/削.md:32; repo/kanji/削.md:42; repo/kanji/削.md:45; evidence/kanjidic2-records.xml:124
- Evidence: 削's displayed title includes "pare". Its meaning section says 削る can mean "reducing an amount", its reading row glosses けず.る "cut down", its common words list 削減 "reduction; cut", and its example is 予算を削る "cut the budget". 耗's displayed first sense is "decrease". In 削's meaning quiz, "decrease; wear down through use" is defensible for 削る's reduce and shave-away senses. Neither card declares the pair. 耗 already guards 殺, whose only overlap is the KANJIDIC2 "diminish; reduce" gloss, so it applies a stricter standard to a weaker candidate.
- Required change: Declare the direct 耗/削 pair on either card and mention it in Notes, or record a sourced reason why the reduce sense is not an ordinary meaning choice.

## Optional points
### O1: Clarify the ベイ row as voiced compound forms
- Facet: Comprehensibility
- Severity: optional
- Confidence: medium
- Citations: snapshot/kanji/塀.md:37; evidence/joyo-rows.json:9; evidence/external-snapshots/01-extract.txt:12-14; evidence/external-snapshots/06-extract.txt:5-7
- Evidence: KANJIDIC2 lists ベイ, and the card illustrates it with 土塀 どべい and 板塀 いたべい. The cached Joyo row and Daijisen's character entry list only ヘイ and place 板塀, 土塀 and 石塀 under it. Learners may therefore read ベイ as an independent reading rather than the voiced form inside compounds.
- Suggestion: Add a short note that ベイ appears as the voiced form in compounds such as 土塀 and 板塀, while the standard character tables list ヘイ.

### O2: 用 left unguarded while 使 is guarded on 耗
- Facet: Consistency/quiz safety
- Severity: optional
- Confidence: low
- Citations: snapshot/kanji/耗.md:57-58; repo/kanji/使.md:3; repo/kanji/使.md:21-22; repo/kanji/用.md:3; repo/kanji/用.md:21
- Evidence: 耗 guards 使 "use, employ" for "using up", but 用 "use, purpose" carries the same displayed head word and is not declared. 使う also covers spending, which 用's card does not mention, so the difference is defensible but unstated.
- Suggestion: Either add 用 as a precaution or state in Notes why 使 is guarded and 用 is not.

### O3: 際 left unguarded while 辺 is guarded on 塀
- Facet: Consistency/quiz safety
- Severity: optional
- Confidence: low
- Citations: snapshot/kanji/塀.md:56-61; repo/kanji/辺.md:3; repo/kanji/際.md:3; repo/kanji/際.md:21
- Evidence: 塀 guards 辺 "vicinity; edge" as a broad boundary or edge label, while 際 "edge; occasion" shares the displayed head word "edge" and is not declared. Neither card means a wall, so this is consistency polish rather than a demonstrated collision.
- Suggestion: Apply one stated threshold for edge labels: add 際 or note why 辺 alone is guarded.

### O4: Unstated rationale for several 耗 guards, including 断
- Facet: Consistency/quiz safety
- Severity: optional
- Confidence: medium
- Citations: checks/quiz-safety.txt:20-103; repo/kanji/断.md:3; repo/kanji/断.md:21-23; repo/kanji/絶.md:3; repo/kanji/絶.md:31
- Evidence: The quiz-safety check reports 83 warnings for exclusions that the Notes do not mention, including 耗/断. 断's card shows severing, refusing and judgment, not depletion. 絶 "sever; cease" (絶える "die out") is unguarded, so reviewers cannot tell which threshold the 断 guard follows.
- Suggestion: Briefly group the unexplained guards in Notes (for example, which 字通 or old-dictionary allocation motivates 断) so future comparisons are consistent.

### O5: 耗 look-alike note names non-curated 石 and 未
- Facet: Comprehensibility
- Severity: optional
- Confidence: low
- Citations: snapshot/kanji/耗.md:13; snapshot/kanji/耗.md:83-89
- Evidence: The curated distractors are 右, 川 and 本, but the note also says 石 and 未 "instead have distinct lexical ranges" before turning to "the curated choices". This may read like stale distractor commentary.
- Suggestion: Say why 石 and 未 are mentioned (shape or comparison only), or drop them.

## Limits
- L1: Execution-model identity is not independently verified; the runtime describes this reviewer as Claude Opus 5.5, but I could not verify that from evidence in this pass.
- L2: Raw stroke SVGs, raw external HTML responses, the binary Joyo PDF and all other packet assets outside the two chains were not read. Stroke JSON was checked only for stroke counts (12, 8, 10) matching the cards and KANJIDIC2; no visual geometry claim is made.
- L3: Glyphs shown as images in the 字通 and 漢字ペディア extracts were unreadable, so claims depending on them stay as qualified by the cards and were not independently verified.
- L4: The reading-exposure and quiz-safety logs model only the bounded N1/All/Starter host pools. Custom or caller-built pools, multiple borrowing, Kotlin execution, native or phone acceptance and compatibility with installed APK 5c000bd (which predates quiz_exclusions) were not assessed; JVM/emulator work remains on hold.
- L5: Unread candidates not requested in phase 1, judged less plausible from the title index alone: for 拍, 祝 celebrate, 賞 prize, 遊 play, 突 thrust, 心 heart, 秒 second, 回 times, 歩 steps; for 耗, 少 few, 低 low, 落 fall down, 退 retreat, 老 grow old, 旧 former, 燥 dry up, 便 convenience and 信 trust (news senses only via supplemental 耗 たより); for 塀, 防 defend, 閉 shut, 域 region, 築 build, 囚 prisoner (塀の中 metonym). No 壁, 垣, 柵, 堤, 屏, 脈, 鼓, 叩, 奏, 衰, 尽, 廃, 滅 or 壊 card exists in the 1254-line title index.
- L6: Some 拍 and 耗 guards rest on unresolved JMdict family or old-dictionary allocations (for example the 拍つ spelling in the 打つ family). Their necessity was not adjudicated beyond confirming that the pairs are declared and harmless to keep.
- L7: The checks are host/static logs and are not linguistic proof; lint, validate, manifest, unittest and budget results are taken as supplied.

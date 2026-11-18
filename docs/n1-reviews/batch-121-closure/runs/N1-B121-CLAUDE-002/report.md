# B121 initial review — N1-B121-CLAUDE-002

## Overall verdict
Verdict: NEEDS FIX

## Facet verdicts
### Correctness
Verdict: CLEAN
Basis: Metadata (14 strokes, radical 彳 no. 60, grade 4, on トク, no kun, five name readings unselected) matches KANJIDIC2; the profit/benefit cross-reference to 得, 徳行 とっこう, 徳利 ateji, Joyo トク in 道徳 and the source-only おしえ claim all match JMdict, the Joyo row and the Weblio 漢字辞典 section; the mnemonic is labelled and structure-unclassified is a permitted conservative choice (O4).

### Scoped coverage
Verdict: CLEAN
Basis: The card teaches the main virtue/benevolence sense, the ordinary profit/benefit secondary sense, the selected トク reading with its one linked word, and qualifies source-only readings and compound sound changes; the one required 道徳 back-link is added.

### Consistency/quiz safety
Verdict: NEEDS FIX
Basis: The card's own declared exclusion basis (blessing to 福, wealth to 富, esteem/respect to 尊 and 敬) is applied inconsistently: 幸 "happiness; good fortune", 財 "wealth; property" and 偉 "admirable; great" carry the same or closer senses and are not declared as direct pairs on either endpoint (F1, F2). Curated options 休/本/木 are semantically safe and share no reading with トク.

### Comprehensibility
Verdict: CLEAN
Basis: Notes distinguish moral virtue from the financial sense, label limited comparisons as not synonyms, and mark the mnemonic as non-etymological; only a minor title misquote remains (O1).

## Segments read
Core chain: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22 (each read once, no re-views)
Extension chain: 1, 2, 3, 4, 5, 6, 7 (each read once, no re-views)
Title index: I read evidence/title-index.txt source lines 1-1241 in full (core segments 19 and 20); line 1 is "一 one" and line 1241 is "齢 age; years lived".
I read the external snapshot manifest and its one SUPPLIED extract (01-extract.txt, lines 1-192) in index order.
The instruction file was read once at kickoff, as authorized.

## Phase-1 D/E lists
D: D1 偉, D2 幸, D3 財, D4 豊, D5 栄, D6 愛, D7 厚, D8 好, D9 道, D10 礼, D11 儀, D12 格, D13 品, D14 者, D15 訓, D16 授, D17 拝, D18 賞, D19 績, D20 直, D21 性, D22 能
E: E1 優, E2 正, E3 人, E4 享, E5 富, E6 福, E7 教, E8 得, E9 利, E10 恩
Missing entries: none

## D/E cards read
| ID | Character | Displayed title | Related new card(s) | Reason | Disposition |
| --- | --- | --- | --- | --- | --- |
| D1 | 偉 | admirable; great | 徳 | 徳 is glossed "commanding respect" (evidence/kanjidic2-records.xml:59); 偉 praises admirable conduct (repo/kanji/偉.md:20-21) | Collision needing exclusion (F2); the 徳/偉 pair is not declared on either endpoint (snapshot/kanji/徳.md:14; 偉 has no quiz_exclusions); "admirable" is closer to "commanding respect" than the declared 尊 and 敬 |
| D2 | 幸 | happiness; good fortune | 徳 | 徳 has a blessing/grace sense (evidence/external-snapshots/01-extract.txt:17, 23), and the card excludes 福 "good fortune" on that basis (snapshot/kanji/徳.md:44) | Collision needing exclusion (F1); 幸 shares the exact "good fortune" label (repo/kanji/幸.md:3) and the 恩 card already excludes both 福 and 幸 for a blessing sense (repo/kanji/恩.md:61-63); the pair is not declared on either endpoint |
| D3 | 財 | wealth; property | 徳 | Daijisen gives 徳 the sense 富。財産 (evidence/external-snapshots/01-extract.txt:25), and the card excludes 富 on that basis (snapshot/kanji/徳.md:44) | Collision needing exclusion (F1); 財's title translates 財産 directly (repo/kanji/財.md:3, 20-21); the pair is not declared on either endpoint |
| D4 | 豊 | bountiful; abundant | 徳 | Wealth vs abundance (repo/kanji/豊.md:20) | Harmless: the 徳 sources give wealth/property (01-extract.txt:25) but no abundance or plentiful-supply sense (kanjidic2-records.xml:56-59; 01-extract.txt:15-28); 豊 shares "abundant" only with 富, and exclusions are not transitive; no exclusion is declared |
| D5 | 栄 | flourish; glory | 徳 | Prosperity (repo/kanji/栄.md:21) | Harmless: no 徳 gloss gives prosperity or glory (01-extract.txt:15-28; kanjidic2-records.xml:56-59); "happiness and prosperity" belongs to the compound 福徳 (jmdict-families.xml entry 1624780); no exclusion is declared |
| D6 | 愛 | love | 徳 | Benevolence vs love/affection (repo/kanji/愛.md:20-21) | Harmless: the 徳 sources treat benevolence as a moral virtue (01-extract.txt:15, 22) with no love or affection gloss; 愛徳 "charity" is a Christian compound meaning; 恩 excludes 愛 only because of its own いつくしみ gloss (repo/kanji/恩.md:29-30), which 徳 does not share; no exclusion is declared |
| D7 | 厚 | thick; cordial | 徳 | Cordiality as kindness shown in 厚意 (repo/kanji/厚.md:20) | Harmless: "cordial" describes warm treatment, not moral excellence, and the 徳 sources contain no cordial or thickness gloss (01-extract.txt:15-28); no exclusion is declared |
| D8 | 好 | liking; favorable | 徳 | Goodness vs favorable/goodwill (repo/kanji/好.md:20) | Harmless: 好 concerns liking and preference, and 徳's "goodness" (kanjidic2-records.xml:58) is moral; no 徳 gloss gives liking; no exclusion is declared |
| D9 | 道 | road, way | 徳 | The way-of-conduct sense in 道徳 (repo/kanji/道.md:21) | Harmless: the displayed "road, way" is not a 徳 meaning, and the morality sense belongs to the whole word 道徳 (jmdict entry 1454240); no exclusion is declared |
| D10 | 礼 | bow; thanks | 徳 | Propriety as a virtue (repo/kanji/礼.md:20) | Harmless: the displayed bow/thanks senses do not occur in the 徳 sources (01-extract.txt:15-28); 礼 appears with 徳 only as one listed Confucian virtue (01-extract.txt:56); no exclusion is declared |
| D11 | 儀 | ceremony; formal conduct | 徳 | Virtuous conduct (01-extract.txt:15) vs formal conduct (repo/kanji/儀.md:22-24) | Harmless: 儀's conduct is ceremony, manners and etiquette, while 徳's conduct is moral excellence; no 徳 gloss gives ceremony or etiquette; no exclusion is declared |
| D12 | 格 | rank; character | 徳 | The English stem "character": 徳 means 品性 (01-extract.txt:15), and 格 means character/standing (repo/kanji/格.md:20) | Harmless (medium confidence): 格's "character" means personality or standing (repo/kanji/格.md:43), not moral excellence, and 徳 has no rank sense; no exclusion is declared |
| D13 | 品 | goods, refinement | 徳 | Refinement or dignity (repo/kanji/品.md:20) vs 品性 | Harmless: refinement and dignity are not moral virtue or benevolence; the displayed title leads with goods; no exclusion is declared |
| D14 | 者 | person in a role | 徳 | The "excellent person" sense (01-extract.txt:16) | Harmless: that sense is bound in compounds such as 碩徳 and 大徳, while 者 is a generic role marker (repo/kanji/者.md:20); 人 is declared conservatively, and exclusions are not transitive; no 徳/者 exclusion is declared |
| D15 | 訓 | instruction; kun reading | 徳 | Source-only おしえ (snapshot/kanji/徳.md:45) | Harmless: おしえ appears only as a 漢字辞典 kun reading, with no teaching meaning for 徳 in Daijisen (01-extract.txt:15-28); 訓 concerns instruction (repo/kanji/訓.md:20); no exclusion is declared |
| D16 | 授 | grant; impart; teach | 徳 | Teach or impart; 徳を授かる (01-extract.txt:23) | Harmless: 授 is the act of bestowing (repo/kanji/授.md:23), whereas 徳 is what is bestowed in that example, and 徳 has no teaching sense; no exclusion is declared |
| D17 | 拝 | worship; bow in respect | 徳 | Respect | Harmless: 拝 is the act of paying respect (repo/kanji/拝.md:20), while 徳's "commanding respect" (kanjidic2-records.xml:59) is a quality that attracts respect; no exclusion is declared |
| D18 | 賞 | prize; reward | 徳 | Benefit or reward (01-extract.txt:17) | Harmless (medium confidence): 賞 is an award (repo/kanji/賞.md:20), while 徳's 恩恵 is grace bestowed; 恩賞 appears only in Wikipedia's Legalist-history section (01-extract.txt:61); no exclusion is declared |
| D19 | 績 | achievements; results | 徳 | Merit or achievement | Harmless: no 徳 gloss gives achievement (kanjidic2-records.xml:56-59; 01-extract.txt:15-28); 績 is a record of results (repo/kanji/績.md:20); 功 is declared via 功徳 merit, and exclusions are not transitive; no exclusion is declared |
| D20 | 直 | direct; repair | 徳 | Uprightness | Harmless: honesty belongs only to the compound 正直 (repo/kanji/直.md:21), and the displayed title is not a 徳 meaning; no exclusion is declared |
| D21 | 性 | nature; gender | 徳 | Daijisen sense 5, innate nature 天性 (01-extract.txt:27) | UNVERIFIED: the sense is illustrated only by an early-modern citation (01-extract.txt:28), and the supplied evidence does not establish whether it is current (O3); 性's "nature" (repo/kanji/性.md:20) overlaps it; no exclusion is declared |
| D22 | 能 | ability; capacity | 徳 | Daijisen sense 5, innate ability 能力 (01-extract.txt:27) | UNVERIFIED: same basis as D21 (O3); 能 "ability" (repo/kanji/能.md:20) matches the gloss wording; no exclusion is declared |
| E1 | 優 | gentle; superior | 徳 | The card note says 優 includes kindness (snapshot/kanji/徳.md:43) | Already handled: the pair is declared on the 徳 side (徳.md:14); the kindness claim is supported by 優しい (repo/kanji/優.md:20); kindness overlaps benevolence |
| E2 | 正 | correct, proper | 徳 | The card note says 正 can describe proper conduct (徳.md:43) | Already handled (conservative): the pair is declared on the 徳 side; 正しい can judge conduct (repo/kanji/正.md:20) |
| E3 | 人 | person | 徳 | Virtuous-person sense (01-extract.txt:16) | Already handled (over-cautious but harmless): the pair is declared on the 徳 side; the person sense is compound-bound, and 人.md:3 is generic |
| E4 | 享 | enjoy; receive benefits | 徳 | Benefit or blessing (01-extract.txt:17) | Already handled: the pair is declared on the 徳 side; 享 means enjoying benefits (repo/kanji/享.md:22) |
| E5 | 富 | wealth; abundance | 徳 | Wealth sense (01-extract.txt:25) | Already handled: the pair is declared on the 徳 side; 富 means wealth (repo/kanji/富.md:20); it is the parallel for D3 |
| E6 | 福 | good fortune | 徳 | Blessing sense (01-extract.txt:23) | Already handled: the pair is declared on the 徳 side; 福 names fortune or a blessing (repo/kanji/福.md:20); it is the parallel for D2 |
| E7 | 教 | teach, instruct | 徳 | Source-only おしえ (徳.md:45) | Already handled (conservative): the pair is declared on the 徳 side; the card quotes the title with a semicolon instead of the actual comma (repo/kanji/教.md:3; O1) |
| E8 | 得 | gain; acquire | 徳 | Profit/benefit cross-reference (jmdict-families.xml:2231-2236) | Already handled: the pair is declared on the 徳 side; 得 means gaining an advantage (repo/kanji/得.md:20), which supports the card note |
| E9 | 利 | benefit; advantage | 徳 | Profit, benefit or advantage sense (jmdict-families.xml:2234-2236) | Already handled: the pair is declared on the 徳 side; the title is quoted accurately (repo/kanji/利.md:3) |
| E10 | 恩 | favor; debt of gratitude | 徳 | Benevolence; JMdict 恩 sense 2 is kindness or benevolence | Already handled: the pair is declared on the 徳 side only (恩.md:14 lacks 徳); this is sufficient because a declaration on either endpoint applies; the card note matches 恩.md:29-30 |

## Per-card results
| Card | Correctness | Scoped coverage | Consistency/quiz safety | Comprehensibility | Evidence |
| --- | --- | --- | --- | --- | --- |
| 徳 | CLEAN | CLEAN | NEEDS FIX | CLEAN | KANJIDIC2 record, JMdict 2080970/1454240/1661670/1454660, Joyo row, Weblio extract lines 11-28, stroke JSON (14 strokes), diffs/existing.diff; F1, F2, O1-O4 |

## Findings
### F1: Missing direct exclusions 徳/幸 and 徳/財 parallel to declared 福 and 富
- Facet: Consistency/quiz safety
- Severity: low
- Confidence: medium
- Citations: snapshot/kanji/徳.md:14; snapshot/kanji/徳.md:44; evidence/external-snapshots/01-extract.txt:23; evidence/external-snapshots/01-extract.txt:25; repo/kanji/幸.md:3; repo/kanji/財.md:3; repo/kanji/福.md:20; repo/kanji/恩.md:61-63
- Evidence: The card excludes 福 "good fortune" and 富 "wealth; abundance" because the character source describes blessings and wealth (徳.md:44). Daijisen gives 徳 the senses めぐみ・恩恵・加護 and 富・財産 (extract:23, 25). 幸's displayed title contains the same label, "good fortune", and the repository's 恩 card already excludes both 福 and 幸 for a blessing sense. 財's displayed title, "wealth; property", translates 財産 directly. Neither pair is declared on either endpoint. If those 徳 senses make 福 and 富 defensible answers, as the card's declarations assert, then 幸 and 財 are equally defensible. Current curated options (休/本/木) do not expose these pairs, but fallback in smaller pools could.
- Required change: Add 幸 and 財 to 徳's quiz_exclusions, and mention them in the existing blessing/wealth note. Alternatively, record evidence that the blessing and wealth senses do not make these displayed titles defensible, and remove the 福 and 富 exclusions on that same basis.

### F2: Missing direct exclusion 徳/偉 for the respect/admirable sense
- Facet: Consistency/quiz safety
- Severity: low
- Confidence: medium
- Citations: evidence/kanjidic2-records.xml:59; snapshot/kanji/徳.md:14; snapshot/kanji/徳.md:44; repo/kanji/偉.md:3; repo/kanji/偉.md:20-21
- Evidence: KANJIDIC2 glosses 徳 as "commanding respect", and the card excludes 尊 and 敬 because they "concern esteem or respect". 偉 is displayed as "admirable; great", and its card says 偉い can praise a person's conduct. "Admirable" (worthy of admiration) is semantically closer to "commanding respect" than the respecting actions of 尊 and 敬. The pair is not declared on either endpoint.
- Required change: Add 偉 to 徳's quiz_exclusions, with a note that it is a limited comparison. Alternatively, document evidence that "admirable; great" cannot be a defensible answer for 徳.

## Optional points
### O1: 教 title quoted with the wrong separator
- Facet: Comprehensibility
- Severity: optional
- Confidence: high
- Citations: snapshot/kanji/徳.md:45; repo/kanji/教.md:3
- Evidence: The note quotes 教 as "teach; instruct", but the card title is "teach, instruct".
- Suggestion: Quote the displayed title exactly.

### O2: Curated distractors are loose shape contrasts
- Facet: Consistency/quiz safety
- Severity: optional
- Confidence: medium
- Citations: snapshot/kanji/徳.md:13; snapshot/kanji/徳.md:47; rubric/content-structure.instructions.md:41-42
- Evidence: The card itself calls 休/本/木 "loose contrasts, not the closest shapes". The rubric asks for easily confused kanji. These options are semantically and reading-safe, but they give weak visual practice.
- Suggestion: Consider a closer non-excluded 彳-family shape contrast such as 徹 or 徒 in place of one loose option, after checking its title and readings.

### O3: Currency of Daijisen sense 5 (innate nature/ability) is unestablished
- Facet: Consistency/quiz safety
- Severity: optional
- Confidence: low
- Citations: evidence/external-snapshots/01-extract.txt:27-28; repo/kanji/性.md:3; repo/kanji/能.md:3
- Evidence: Daijisen lists 生まれつき備わった能力・性質。天性 with only an early-modern citation. 性 "nature; gender" and 能 "ability; capacity" overlap the wording. The supplied evidence does not establish whether this sense is ordinary today.
- Suggestion: Decide and record whether sense 5 is quiz-relevant. If it is, declare 性 and 能 as direct exclusions.

### O4: Structural classification is conservative despite available phonetic analyses
- Facet: Correctness
- Severity: optional
- Confidence: medium
- Citations: evidence/shape-evidence.json:36; evidence/external-snapshots/01-extract.txt:54; snapshot/kanji/徳.md:5
- Evidence: KanjiVG marks a 直 phonetic group, and the Wikipedia section, which carries accuracy warnings, calls 徳 a phono-semantic compound of 徝 and 心. The card uses structure-unclassified and gives no phonetic, which the contract permits.
- Suggestion: Keep the card as is unless a reputable character dictionary is cited; if one is, the phonetic analysis could be added with hedging.

## Limits
- L1: Raw KanjiVG SVGs, the raw Weblio HTML response, the binary Joyo PDF and every packet file outside the chains were not read. Stroke JSON was checked only for its 14-stroke count against the card and KANJIDIC2, with no geometry claim.
- L2: Exclusion targets 義, 良, 功, 尊 and 敬 were not requested in E, so their card text was not read. I judged those declared pairs only from their index titles and the 徳 card notes. Other index titles, such as 清, 純, 美 and 運, were judged too remote to request and were not read.
- L3: The ten checks are host/static evidence. Reading-exposure models limited pools only; no Kotlin, native/phone, custom or multi-borrow pool, or APK 5c000bd compatibility claim is made.
- L4: The currency of Daijisen senses 4 (wealth) and 5 (innate nature/ability), both shown only with classical citations, is not established by the supplied evidence. F1 rests on the card's own declared basis, not on independent proof that sense 4 is current.
- L5: The N1 level relies on packet source row 347 and the KANJIDIC2 jlpt field; kanjiapi data itself is not in the chains.
- L6: Execution model identity is reported by the runtime as Claude Opus 5.5; this is not independently verifiable within this pass.

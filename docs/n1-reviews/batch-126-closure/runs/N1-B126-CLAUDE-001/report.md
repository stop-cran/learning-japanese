# B126 initial review — N1-B126-CLAUDE-001

## Overall verdict
Verdict: CLEAN

## Facet verdicts
### Correctness
Verdict: CLEAN
Basis: The 傘 title, metadata (12 strokes, radical 人 no. 9, grade 8, サン/かさ), readings, compounds and glosses match KANJIDIC2 (evidence/kanjidic2-records.xml:2-61), JMdict 1301940/1301960/1464080/1548660/1586610/1774770 (evidence/jmdict-families.xml), the cached Joyo row (evidence/joyo-rows.json:5-12) and Daijisen (evidence/external-snapshots/01-extract.txt:4-16). Mnemonic is labelled as such and matches the KanjiVG grouping (evidence/shape-evidence.json); no defect established.

### Scoped coverage
Verdict: CLEAN
Basis: Both metadata readings have reading rows; the only selected quiz reading かさ has its own row with a linked word article; サン is explained with sourced compounds; the からかさ whole-word reading and the lampshade/mushroom-cap secondary sense are addressed (snapshot/kanji/傘.md:27-49). The one required link wrapper is present. Optional 傘寿 omission is not a coverage defect (O1).

### Consistency/quiz safety
Verdict: CLEAN
Basis: The three curated distractors 金, 全, 合 have distinct titles, no umbrella sense and no かさ/サン reading overlap. The only declared direct exclusion 傘–被 (declared on 傘, not on 被) is defensible from 被's cover/shelter senses. All 18 D comparisons read were judged harmless on sense evidence; no further direct exclusion pair was found to be required. Checks report 0 errors and 0 reading-exposure hits.

### Comprehensibility
Verdict: CLEAN
Basis: The card explains rendaku in 日傘/雨傘, keeps the からかさ reading distinct from the selected reading, separates object "shade" from 暗's darkness and a mushroom cap from 帽's headgear, labels the mnemonic, and states why サン is not practised without making a rarity claim (snapshot/kanji/傘.md:23-49).

## Segments read
Core chain: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23 (each read once, in order; no re-views)
Extension chain: 1, 2, 3, 4, 5 (each read once, in order; no re-views)
Title index: I read evidence/title-index.txt source lines 1-1246 in full (core segments 14-16); line 1 is "一 one" and line 1246 is "齢 age; years lived".
I also read the instruction file once at kickoff, as the run instruction permits.
Execution model: the runtime declares Claude Opus 5.5; this identity is not independently verifiable from within the pass.

## Phase-1 D/E lists
D: D1 帽, D2 暗, D3 影, D4 包, D5 灯, D6 防, D7 守, D8 保, D9 宇, D10 軒, D11 屋, D12 領, D13 系, D14 竹, D15 紙, D16 雨, D17 陽, D18 布
E: E1 被
Missing entries: none

## D/E cards read
| ID | Character | Displayed title | Related new card(s) | Reason | Disposition |
| --- | --- | --- | --- | --- | --- |
| D1 | 帽 | hat; headgear | 傘 | JMdict 1301940 sense 2 is "something shaped like an umbrella or a conical hat; mushroom cap" (evidence/jmdict-families.xml:21-27) | Harmless, not declared on either card: 帽 is a hat or head covering (repo/kanji/帽.md:20); Daijisen defines 傘 as held over the head and distinct from the head-worn 笠 (evidence/external-snapshots/01-extract.txt:6); sense 2 names umbrella-shaped objects, not headgear |
| D2 | 暗 | dark | 傘 | KANJIDIC2 lists "shade" for 暗; 傘 sense 2 has "shade (of a lamp)" | Harmless, not declared: 暗 teaches darkness or lack of light (repo/kanji/暗.md:20-21); 傘's shade is a physical lampshade object (evidence/jmdict-families.xml:25), as 傘.md:47 says |
| D3 | 影 | shadow; silhouette | 傘 | A sunshade casts shade; 日傘 is glossed "sunshade" | Harmless, not declared: 影's senses are shadow, silhouette, image, light and trace (repo/kanji/影.md:23); no 傘 sense names a shadow (evidence/jmdict-families.xml:16-27) |
| D4 | 包 | wrap; enclose | 傘 | KANJIDIC2 lists "cover" for 包; an umbrella covers from above | Harmless, not declared: 包 teaches wrapping, enclosing, parcels and encirclement (repo/kanji/包.md:20); 傘 is a held overhead object, not an act of wrapping or enclosing (evidence/external-snapshots/01-extract.txt:6) |
| D5 | 灯 | lamp; lamplight | 傘 | 傘 sense 2 includes "shade (of a lamp)" | Harmless, not declared: 灯 names the light or lamp itself (repo/kanji/灯.md:20); 傘 names only the shade part (evidence/jmdict-families.xml:25), not the light |
| D6 | 防 | defend; ward off | 傘 | An umbrella protects against rain or sun | Harmless, not declared: 防 is protection or prevention as an action (repo/kanji/防.md:20); 傘 names the object (snapshot/words/傘.md:29); shared function is only shared subject matter |
| D7 | 守 | guard; obey | 傘 | Protection or shelter | Harmless, not declared: 守 means guarding or keeping rules (repo/kanji/守.md:20); no 傘 dictionary sense means guard (evidence/jmdict-families.xml:16-27) |
| D8 | 保 | protect; preserve | 傘 | Protection | Harmless, not declared: 保 means protecting, preserving or maintaining a state (repo/kanji/保.md:22); 傘 is a concrete umbrella object (evidence/kanjidic2-records.xml:53) |
| D9 | 宇 | eaves; space | 傘 | Overhead shelter; KANJIDIC2 gives 宇 roof and eaves | Harmless, not declared: 宇's senses are eaves, roof, house, heaven and space (repo/kanji/宇.md:20); 傘 is a hand-held umbrella, not a building part (evidence/external-snapshots/01-extract.txt:6) |
| D10 | 軒 | eaves; building counter | 傘 | Overhead shelter | Harmless, not declared: 軒 names building eaves and is a counter for buildings (repo/kanji/軒.md:20); no umbrella sense |
| D11 | 屋 | roof, shop | 傘 | Overhead covering | Harmless, not declared: 屋 covers buildings, roofs and shops (repo/kanji/屋.md:20); a held umbrella is not a roof (evidence/external-snapshots/01-extract.txt:6) |
| D12 | 領 | territory; jurisdiction | 傘 | 傘下 is glossed "under jurisdiction of" (evidence/jmdict-families.xml:43-61) | Harmless, not declared: the jurisdiction sense belongs to the whole compound with 下, and Daijisen gives 傘 in 傘下 the sense かさ (evidence/external-snapshots/01-extract.txt:14); 領 is territory or jurisdiction (repo/kanji/領.md:20) |
| D13 | 系 | lineage; system | 傘 | 傘下 "affiliated with" overlaps 系列's group of affiliated businesses | Harmless, not declared: the affiliation sense is compound-level (evidence/jmdict-families.xml:43-61), and 系's senses are lineage, system, group and type (repo/kanji/系.md:23-31). 系's own exclusion of distractor 全 is a different pair and is not transitive |
| D14 | 竹 | bamboo | 傘 | からかさ is a bamboo-and-oiled-paper umbrella | Harmless, not declared: material only; 竹 names bamboo (repo/kanji/竹.md:20), and 傘 does not mean bamboo (evidence/jmdict-families.xml:16-27) |
| D15 | 紙 | paper | 傘 | からかさ is a paper umbrella | Harmless, not declared: material only; 紙 means paper (repo/kanji/紙.md:20) |
| D16 | 雨 | rain | 傘 | 雨傘 means rain umbrella | Harmless, not declared: 雨 is rain itself (repo/kanji/雨.md:20); the word article says 傘 names the protective object, not the rain (snapshot/words/傘.md:29) |
| D17 | 陽 | sunshine | 傘 | 日傘 (parasol, sunshade) protects against the sun | Harmless, not declared: 陽 means sunlight or the sun (repo/kanji/陽.md:20); the parasol is the object, not sunshine |
| D18 | 布 | cloth; distribute | 傘 | 傘布 is umbrella fabric | Harmless, not declared: material only; 布 means cloth or distribution (repo/kanji/布.md:20) |
| E1 | 被 | cover; incur | 傘 | Existing direct exclusion target; KANJIDIC2 gives 被 cover, veil and shelter (evidence/kanjidic2-records.xml:836-849) | Already handled: declared on 傘 (snapshot/kanji/傘.md:14), not on 被 (repo/kanji/被.md:1-12, no quiz_exclusions). "cover" could defensibly describe an umbrella or lampshade; a conservative exclusion is justified, and one endpoint is enough |

## Per-card results
| Card | Correctness | Scoped coverage | Consistency/quiz safety | Comprehensibility | Evidence |
| --- | --- | --- | --- | --- | --- |
| 傘 | CLEAN | CLEAN | CLEAN | CLEAN | snapshot/kanji/傘.md:1-51; KANJIDIC2 傘; JMdict 1301940, 1301960, 1774770; joyo-rows; Daijisen extract lines 4-16; shape-evidence; quiz-safety and reading-exposure checks; D1-D18 and E1 dispositions; O1 |

## Findings
None.

## Optional points
### O1: 傘寿 eightieth-birthday sense not mentioned
- Facet: Scoped coverage
- Severity: optional
- Confidence: high
- Citations: evidence/external-snapshots/01-extract.txt:15; evidence/jmdict-families.xml:107-117; snapshot/kanji/傘.md:36-41
- Evidence: Daijisen gives a second サン character sense, eighty years of age, from the abbreviated form 仐, as in 傘寿; JMdict entry 1302010 has 傘寿 さんじゅ "80th birthday". The card's common words omit it.
- Suggestion: Optionally add 傘寿 さんじゅ, "80th birthday," as a recognition note under the サン row, labelled as a convention based on the character's shape.

## Limits
- L1: I did not read the raw stroke SVG, the raw Weblio response, the binary Joyo PDF or any other packet asset outside the chains. I checked the stroke JSON only for its stroke count, revision and KanjiVG grouping against the card and shape-evidence; I make no visual geometry claim.
- L2: N1 membership rests on packet sourceRow 70 and source-metadata. I did not open the pinned N1 source snapshot itself. KANJIDIC2's jlpt=1 uses the historical scale and is not independent N1 evidence.
- L3: Candidates I identified but did not request, because they were judged implausible as meaning-quiz collisions: 衣 and 装 (clothing or accessory category), 開 (開傘), 骨 (umbrella frame), 落 (落下傘), 笹 (bamboo grass), 札, 雪, 面. Characters such as 笠, 蓋, 覆 and 茸 are not in the 1246-card index.
- L4: Fallback composition of the Starter practice session (8 fallback options) was not enumerated. Cards not read in this pass are unadjudicated for that pool. Reading-exposure is a bounded Python model; it does not cover custom or multi-borrow pools, Kotlin, native or phone acceptance, or compatibility with installed APK 5c000bd, which predates quiz_exclusions.
- L5: Automated checks (lint, validate, quiz-safety, linkplan, manifest, budget, unittest, vocabulary) are host or static evidence, not linguistic proof. JMdict line citations for E1's KANJIDIC2 range were derived by counting lines in the chain.
- L6: Execution-model identity is unverified (runtime-declared Claude Opus 5.5).

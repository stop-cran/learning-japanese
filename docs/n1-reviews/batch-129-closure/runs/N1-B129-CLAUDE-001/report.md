# B129 initial review — N1-B129-CLAUDE-001

## Overall verdict
Verdict: CLEAN

## Facet verdicts
### Correctness
Verdict: CLEAN
Basis: All metadata (strokes, radicals, on/kun lists and order, grades, tags, quiz selections) in 茉, 絹 and 虹 matches source-metadata.json and kanjidic2-records.xml; every card claim checked against the supplied JMdict families and the Daijisen, 日本国語大辞典, 字通 and Wiktionary snapshots was supported (茉 マ as conventional on and 字通 まつり; 絹 布帛 broader cloth sense, 字通 羂/わな, かとり/カク; 虹 のじ/ぬじ, ヲニジ, 字通 flag/bridge/oil-dish/訌 glosses). Stroke JSON counts and component groups agree with the cards. No established defect.

### Scoped coverage
Verdict: CLEAN
Basis: Each card explains its full reading list, practises only a linked, dictionary-supported reading (茉 マツ via 茉莉花, 絹 きぬ, 虹 にじ), covers the necessary common words and the key secondary or restricted senses (絹糸 けんし corn silk, 生絹, 紅絹, 二次 search-only 虹, 虹彩). The three link wrappers are the only word-article changes and target the correct kanji cards.

### Consistency/quiz safety
Verdict: CLEAN
Basis: Required direct pairs are declared (茉/莉 on 茉; 絹/綿, 絹/布, 絹/維, 絹/糸, 絹/紅 on 絹; 虹/弧 on 虹). All nine curated distractor slots have distinct, non-defensible titles. Of 21 D candidates read, none showed an ordinary-sense overlap requiring a new direct exclusion; residual conservative-guard inconsistencies are optional points only. Checks report 0 lint, validate and quiz-safety errors and 0 production reading hits.

### Comprehensibility
Verdict: CLEAN
Basis: The cards give clear meanings, labelled modern-shape mnemonics, reading tables with dispositions, and qualified historical notes. Some Notes are dense or use internal wording (O3, O5), but nothing impedes learning of the taught meaning and readings.

## Segments read
Core chain: 1-59, each read once in order, no re-views.
Extension chain: 1-9, each read once in order, no re-views.
I read evidence/title-index.txt source lines 1-1251 in full (segments 42-43); line 1 is "一 one" and line 1251 is "齢 age; years lived".
I read all required core inputs, including all 9 curated distractor slots (8 distinct cards: 本 古 石 紙 約 級 紅 功), the external-snapshot manifest and all seven SUPPLIED extracts in index order.

## Phase-1 D/E lists
D: D1 香, D2 椿, D3 苗, D4 衣, D5 繭, D6 蚕, D7 逮, D8 色, D9 光, D10 輪, D11 虫, D12 辰, D13 撃, D14 劾, D15 批, D16 議, D17 騒, D18 抗, D19 競, D20 油, D21 盆
E: E1 莉, E2 綿, E3 布, E4 糸, E5 維, E6 掛, E7 弧, E8 蛇, E9 攻, E10 皿
Missing entries: none

## D/E cards read
| ID | Character | Displayed title | Related new card(s) | Reason | Disposition |
| --- | --- | --- | --- | --- | --- |
| D1 | 香 | fragrance; incense | 茉 | Daijisen calls 茉莉 a fragrant tree (evidence/external-snapshots/01-extract.txt:9-11); 香 senses are aroma, incense, shogi lance (repo/kanji/香.md:1-23) | Harmless: 香 names scent, not any plant; 茉 has no fragrance or incense sense. No direct pair declared on either endpoint; none needed |
| D2 | 椿 | camellia | 茉 | Another named flowering shrub (repo/kanji/椿.md:1-21) | Harmless: a different species; jasmine and camellia cannot both answer for either card. No pair declared; none needed |
| D3 | 苗 | seedling; young plant | 茉 | Title contains "plant"; 茉 names a plant (repo/kanji/苗.md:1-23) | Harmless: 苗 is a growth stage, not a species; JMdict 1490470 gives seedling and rice seedling only. No pair declared; none needed |
| D4 | 衣 | clothing; garment | 絹 | Shares きぬ reading; 日国 gives 絹 a broader 布帛 cloth sense (evidence/external-snapshots/02-extract.txt:20-30) | Harmless: 布帛 is cloth, not garments; 衣 card says 衣 きぬ is not silk (repo/kanji/衣.md:44-46); JMdict 2266110 glosses clothing only. 布 (cloth) is already a declared 絹 guard. No 絹/衣 pair declared; none needed |
| D5 | 繭 | cocoon | 絹 | Silk source; KANJIDIC2 kun きぬ for 繭 and 繭糸 listed as a 絹糸 spelling (repo/kanji/繭.md:10-36) | Harmless for ordinary meanings: the 繭 card itself says the record does not make 繭 alone mean silk; no opened source gives 絹 a cocoon sense. No pair declared on either endpoint; see O1 |
| D6 | 蚕 | silkworm | 絹 | Silk producer (repo/kanji/蚕.md:1-23) | Harmless: the insect is distinct from the material, as both cards state. No pair declared; none needed |
| D7 | 逮 | arrest; chase | 絹 | Capture sense vs 字通 羂 snare gloss guarded through 捕 (repo/kanji/逮.md:1-23) | Harmless: snare/set-a-snare is a 通假 use, not an ordinary 絹 sense (02-extract.txt:20-40); arrest is not silk. No pair declared; none needed |
| D8 | 色 | color | 虹 | 虹色 means rainbow-coloured (repo/kanji/色.md:1-21) | Harmless: JMdict 1463760 attaches the colour sense to the whole word 虹色; 虹 alone means rainbow. No pair declared; none needed |
| D9 | 光 | light; radiance | 虹 | Rainbow is an optical phenomenon (repo/kanji/光.md:1-22) | Harmless: Daijisen defines 虹 as an arc-shaped band of colours, not light itself (04-extract.txt:18-21). No pair declared; none needed |
| D10 | 輪 | wheel; ring | 虹 | Ring/circle vs 円弧状 rainbow (repo/kanji/輪.md:1-21) | Harmless: 虹 never glosses as ring or wheel; the arc overlap is with 弧, which is declared on 虹. No 虹/輪 pair declared; none needed |
| D11 | 虫 | insect; bug | 虹 | Radical and the old creature conception (repo/kanji/虫.md:1-21; 04-extract.txt:66-127) | Harmless: no modern source gives 虹 an insect sense; card states this (snapshot/kanji/虹.md:23-27). No pair declared; none needed |
| D12 | 辰 | Dragon zodiac sign | 虹 | 字通 dragon-shaped beast conception (repo/kanji/辰.md:1-27) | Harmless: 辰 is the zodiac sign, not a creature noun; rainbow is not a zodiac sign. No pair declared; none needed |
| D13 | 撃 | shoot; strike | 虹 | Attack overlap with the guarded 字通 せめる gloss; 撃 itself excludes 攻 (repo/kanji/撃.md:14-25) | Harmless semantically (せめる is a 訌 通假 use, not ordinary); unguarded although 攻 is guarded. No 虹/撃 pair declared; see O2 |
| D14 | 劾 | censure; impeach | 虹 | Blame overlap; 劾 excludes 責 (repo/kanji/劾.md:14-22) | Harmless semantically; unguarded although 責 is guarded. No pair declared; see O2 |
| D15 | 批 | criticize; critique | 虹 | せめる includes criticize; 批 excludes 責, and 攻 excludes 批 (repo/kanji/批.md:14-22) | Harmless semantically; unguarded. No pair declared; see O2 |
| D16 | 議 | deliberate; debate | 虹 | Debate vs guarded 論/争 dispute gloss (repo/kanji/議.md:1-22) | Harmless: 議 need not imply a quarrel and 虹 has no ordinary dispute sense. No pair declared; none needed |
| D17 | 騒 | make noise; uproar | 虹 | Disturbance overlap; 騒 excludes 乱 (repo/kanji/騒.md:14-24) | Harmless semantically; unguarded although 乱 is guarded. No pair declared; see O2 |
| D18 | 抗 | defy; oppose | 虹 | あらそう includes "to oppose" (JMdict 1400620) (repo/kanji/抗.md:1-23) | Harmless semantically; unguarded. No pair declared; see O2 |
| D19 | 競 | compete; bid | 虹 | あらそう sense 1 is compete (repo/kanji/競.md:1-21) | Harmless semantically; unguarded. No pair declared; see O2 |
| D20 | 油 | oil; grease | 虹 | 字通 oil-dish gloss (repo/kanji/油.md:1-20) | Harmless: 虹 card itself states an oil dish is not oil (snapshot/kanji/虹.md:56). No pair declared; none needed |
| D21 | 盆 | tray; basin | 虹 | Shallow-vessel overlap with the guarded 皿; 盆 excludes 皿 (repo/kanji/盆.md:14-30) | Harmless semantically; unguarded although 皿 is guarded for the same gloss. No pair declared; see O2 |
| E1 | 莉 | jasmine in compounds | 茉 | Required jasmine pair (repo/kanji/莉.md:1-24) | Collision needing exclusion: already handled, declared on 茉 (snapshot/kanji/茉.md:14); not declared on 莉, which suffices |
| E2 | 綿 | cotton | 絹 | わた wadding includes 絹綿/真綿; 字通 字訓 きぬわた (03-extract.txt:1-41; repo/kanji/綿.md:19-20) | Collision via secondary sense: handled, declared on 絹 only |
| E3 | 布 | cloth; distribute | 絹 | 日国 絹 sense 2 includes 布帛 (02-extract.txt:20-30; repo/kanji/布.md:1-21) | Collision: handled, declared on 絹 only |
| E4 | 糸 | thread; yarn | 絹 | Silk is a thread/fibre; 糸 card notes 絹糸 (repo/kanji/糸.md:19-35) | Plausible overlap: handled, declared on 絹 only |
| E5 | 維 | fiber | 絹 | Daijisen 絹 sense 1 is 繊維 (02-extract.txt:7-13; repo/kanji/維.md:1-23) | Collision: handled, declared on 絹 only |
| E6 | 掛 | hang | 絹 | Guard rests on 字通 羂 snare gloss; JMdict 掛ける includes catch in a trap (repo/kanji/掛.md:1-23) | Harmless semantically (precautionary); declared on 絹 only; costs nothing in curated pools |
| E7 | 弧 | arc; curved line | 虹 | Daijisen calls the rainbow 円弧状 (04-extract.txt:1-21; repo/kanji/弧.md:1-21) | Plausible overlap: handled, declared on 虹 only |
| E8 | 蛇 | snake; serpent | 虹 | Rainbow-as-serpent belief in the encyclopedia extracts (04-extract.txt:66-127; repo/kanji/蛇.md:1-25) | Harmless semantically (belief, not a word sense); precautionary guard declared on 虹 only |
| E9 | 攻 | attack; go on the offensive | 虹 | 字通 訌 せめる gloss (repo/kanji/攻.md:1-25) | Harmless semantically; precautionary guard declared on 虹 only; consistency issue with D13-D15 in O2 |
| E10 | 皿 | dish; plate | 虹 | 字通 油皿 gloss (repo/kanji/皿.md:1-21) | Harmless semantically; precautionary guard declared on 虹 only; 盆 left unguarded (O2) |

## Per-card results
| Card | Correctness | Scoped coverage | Consistency/quiz safety | Comprehensibility | Evidence |
| --- | --- | --- | --- | --- | --- |
| 茉 | CLEAN | CLEAN | CLEAN | CLEAN | KANJIDIC2 record and source-metadata match; Daijisen マツ/マ and 字通 まつり verified; Wiktionary マチ/み verified; JMdict 1641120, 1909630, 2067250; 莉 pair declared; distractors 本 古 石 harmless; D1-D3 harmless; O3, O4 |
| 絹 | CLEAN | CLEAN | CLEAN | CLEAN | KANJIDIC2 and Joyo row (ケン, きぬ); Daijisen/日国/字通 絹 and 綿 extracts; JMdict 1258710, 1592710, 1378940, 2854159, 2414440; guards on 布 糸 維 紅 綿 present; distractors 紙 約 級 harmless; D4-D7 harmless; O1, O4 |
| 虹 | CLEAN | CLEAN | CLEAN | CLEAN | KANJIDIC2; Joyo row にじ only; Daijisen/日国/字通 虹 extracts; JMdict 1463740, 1461870, 1463750, 1463760; 弧 guard present; distractors 紅 功 石 harmless; D8-D21 harmless; O2, O4, O5 |

## Findings
None.

## Optional points
### O1: Consider a conservative 絹/繭 guard
- Facet: Consistency/quiz safety
- Severity: optional
- Confidence: medium
- Citations: repo/kanji/繭.md:10; repo/kanji/繭.md:36; snapshot/kanji/絹.md:14; snapshot/kanji/絹.md:56
- Evidence: KANJIDIC2 lists きぬ among 繭's kun readings, and JMdict records 繭糸 as a spelling of the silk-thread word きぬいと. The 繭 card treats this as source-only, and no opened source gives 絹 a cocoon sense. However, 絹 already guards 掛 and 捕 on the weaker 字通 snare gloss.
- Suggestion: For consistent conservatism, consider declaring 繭 in 絹's quiz_exclusions, or note why the cocoon pair is left open.

### O2: Historical-gloss guards on 虹 are selectively applied
- Facet: Consistency/quiz safety
- Severity: optional
- Confidence: high
- Citations: snapshot/kanji/虹.md:14; snapshot/kanji/虹.md:56; repo/kanji/撃.md:14; repo/kanji/劾.md:14; repo/kanji/批.md:14; repo/kanji/騒.md:14; repo/kanji/盆.md:14; evidence/external-snapshots/04-extract.txt:66-127
- Evidence: The 字通 glosses (訌 disorder, dispute, せめる; 油皿) are 通假 uses, not ordinary modern senses; Daijisen gives only にじ and にじのような. The card says its guards cover "the unresolved range" of these glosses. It guards 攻 責 論 乱 皿 but leaves 撃, 劾, 批, 騒, 抗 and 盆 unguarded, although those cards exclude 攻, 責, 乱 or 皿 for the same overlaps. No direct pair is semantically required either way.
- Suggestion: Either describe the guards as a bounded selection, or reduce them to the pairs supported by ordinary meanings, such as 弧. content-format.md asks for pairs grounded in displayed labels and ordinary meanings.

### O3: Clarify the 未 distractor note on 茉
- Facet: Comprehensibility
- Severity: optional
- Confidence: medium
- Citations: snapshot/kanji/茉.md:61; snapshot/kanji/茉.md:45-48; rubric/content-structure.instructions.md:55-56
- Evidence: The note explains avoiding 未 by "the conservatively supplied み claim", but み is a KANJIDIC2 nanori (and only a Wiktionary kun label). The rubric puts nanori out of scope, and the phrase is internal wording that learners cannot interpret.
- Suggestion: Rephrase, for example: "未 is avoided as a reading option because some sources associate み with 茉".

### O4: Structural classification left unclassified despite supplied 形声 analyses
- Facet: Correctness
- Severity: optional
- Confidence: medium
- Citations: snapshot/kanji/茉.md:5; snapshot/kanji/絹.md:5; snapshot/kanji/虹.md:5; evidence/external-snapshots/01-extract.txt:20-22; evidence/external-snapshots/04-extract.txt:66-127; evidence/external-snapshots/02-extract.txt:20-40
- Evidence: 字通 classifies 茉 (phonetic 末), 絹 (phonetic 肙) and 虹 (phonetic 工) as 形声. The Wikipedia extract also gives 虹 as phonetic 工 with sources. All three cards use structure-unclassified. This conservative choice is allowed by the rubric and is not an error.
- Suggestion: Optionally add hedged ("commonly explained as") phonetic-compound notes with these sources.

### O5: Note that 虹 コウ is outside the Joyo table
- Facet: Comprehensibility
- Severity: optional
- Confidence: high
- Citations: snapshot/kanji/虹.md:38; evidence/joyo-rows.json:18-25; evidence/external-snapshots/07-extract.txt:728-732
- Evidence: The cached Joyo row lists only にじ for 虹, and Wiktionary marks コウ as 表外. The card says コウ is not practised only because no support article is linked.
- Suggestion: Add that コウ is a non-Joyo reading used in compounds such as 虹彩.

## Limits
- L1: Execution-model identity is not independently verifiable; the runtime reports Claude Opus 5.5.
- L2: Unread inputs: raw stroke SVGs, raw HTML responses, the binary Joyo PDF, and every packet file outside the two chains, including all other repo/kanji cards and words articles.
- L3: Identified but unread candidates: 菊, 梅 and 桃 (other plant names, 茉); 服 (clothing), 裏 (lining, 紅絹), 毛, 索 and 緒 (絹); 円 and 曲 (curve/circle; 弧 excludes them), 雨 and 雲 (weather), 戦 (battle), 叫 (all 虹). Their dispositions are inferred from titles only and are not established.
- L4: shape-evidence.json reports U+8309 (茉) absent from all three bundled kanji fonts; rendered display, fallback fonts and device behaviour were not assessed.
- L5: Reading-exposure and quiz-safety checks are bounded host/static models; Kotlin execution, custom or multi-borrow pools, native/phone acceptance and compatibility with installed APK 5c000bd (which predates quiz_exclusions) are not verified.
- L6: JLPT N1 membership relies on the source row numbers in source-metadata.json; the kanjiapi snapshot itself was not supplied.
- L7: Stroke geometry was reviewed only as JSON data against card text and KanjiVG group metadata; no visual geometry claim is made.

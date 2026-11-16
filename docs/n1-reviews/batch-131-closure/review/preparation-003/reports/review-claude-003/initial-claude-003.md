# B131 initial review — N1-B131-CLAUDE-003

## Overall verdict
Verdict: NEEDS FIX

## Facet verdicts
### Correctness
Verdict: CLEAN
Basis: Metadata of all three cards matches the KANJIDIC2 projection and source-metadata.json (strokes 16/6/17, radicals 144/123/173, grades 5/3/8, readings); every supplemental claim checked (まもる/まもり, 字通 マホリ/メグル/カクム, エ as 呉音 with 近衛 このえ as 難読, 羊 slang for paper/banknotes/hairdressing/head hair, 羊 for 祥, 相羊, 霜 white hair/years/charred powder/ほろぶ・うしなう, ショウ, はつじも) is supported by the opened Kotobank/Weblio extracts or JMdict; stroke JSON counts match cards; the four link wrappers are correct.

### Scoped coverage
Verdict: CLEAN
Basis: Each card explains its displayed meaning, every metadata reading with a disposition, the linked existing word articles and the secondary senses that motivate its exclusions; the conservative structure-unclassified choice is not a defect (see O1).

### Consistency/quiz safety
Verdict: NEEDS FIX
Basis: Two direct pairs with overlap established by the opened evidence and by the cards' own stated exclusion logic are declared on neither endpoint: 霜–凍 (and 霜–氷), and 衛–援 (F1, F2). Curated C options, titles, index uniqueness and wrappers are otherwise consistent.

### Comprehensibility
Verdict: CLEAN
Basis: Prose separates mnemonics from history, qualifies rare/historical/slang senses and whole-word readings, and gives kana for every non-linked word; no confusing or misleading passage found.

## Segments read
Core chain: 1-66, each read once in order, no re-views; segment 66 ended with END OF CHAIN.
Extension chain: 1-9, each read once in order, no re-views; segment 9 ended with END OF CHAIN.
Title index evidence/title-index.txt confirmed as source lines 1-1257, first line "一 one", last line "齢 age; years lived"; the delta has exactly three additions (羊 at 936, 衛 at 1011, 霜 at 1197), zero removals and zero changes. The baseline title index itself was not read.
Instruction file read once at kickoff as authorized.

## Phase-1 D/E lists
D: D1 氷, D2 凍, D3 雪, D4 冴, D5 老, D6 枯, D7 苦, D8 剣, D9 酒, D10 軍, D11 隊, D12 武, D13 送, D14 援, D15 塀, D16 循, D17 畜, D18 獣, D19 群, D20 美, D21 義, D22 富, D23 宝, D24 符
E: E1 未, E2 宙, E3 令, E4 兵, E5 卒
Missing entries: none

## D/E cards read
| ID | Character | Displayed title | Related new card(s) | Reason | Disposition |
| --- | --- | --- | --- | --- | --- |
| D1 | 氷 | ice; freeze | 霜 | Frost is defined as ice crystals (evidence/external-snapshots/05-extract.txt:17); 氷 means ice/hail (evidence/jmdict-extension-records/1488840.xml:2, 1488850.xml:2) | Collision needing exclusion (hypernym ice plus shared freeze label); not declared on 霜 or 氷 (repo/kanji/氷.md:1-12); see F1 |
| D2 | 凍 | freeze; frozen | 霜 | English frost also names freezing phenomena such as frost heaving (evidence/external-snapshots/06-extract.txt:177); 凍 is freezing/frozen state (repo/kanji/凍.md:22) | Collision needing exclusion; not declared on either card (repo/kanji/凍.md:1-12; snapshot/kanji/霜.md:13); see F1 |
| D3 | 雪 | snow | 霜 | Wintry white cover; 雪 is snow/snowfall only (evidence/jmdict-extension-records/1386500.xml:2) | Harmless: frost forms by deposition and is not snow (evidence/external-snapshots/05-extract.txt:17); 霜 card states the contrast (snapshot/kanji/霜.md:55-58) |
| D4 | 冴 | clear; sharp-minded | 霜 | Older intense-cold sense (repo/kanji/冴.md:24) | Harmless: displayed title and JMdict 冴え senses are clarity/skill (evidence/jmdict-extension-records/1297040.xml:2); 霜 has no clarity sense |
| D5 | 老 | grow old | 霜 | 霜 poetic white hair and passing years (evidence/jmdict-review-core.xml:85) | Harmless: 老 means aging/old age (evidence/jmdict-extension-records/1957100.xml:2); 霜 names hair colour and elapsed years, not growing old |
| D6 | 枯 | wither; dry up | 霜 | 霜枯れ and 字通 perishing branch (evidence/external-snapshots/05-extract.txt:48) | Harmless: withering is a compound effect (霜枯れ), not a bare-霜 sense; 枯 article teaches plant withering only (repo/kanji/枯.md:22) |
| D7 | 苦 | bitter; suffering | 霜 | 風霜 hardships (evidence/jmdict-review-core.xml:219) | Harmless: hardship belongs to the whole word 風霜; 苦 is pain/hardship (evidence/jmdict-extension-records/2037710.xml:2) |
| D8 | 剣 | sword; double-edged blade | 霜 | 霜剣/秋霜 sword metaphor (evidence/jmdict-review-core.xml:213) | Harmless: sword sense is restricted to 秋霜 しゅうそう and 霜剣, as the 霜 card notes (snapshot/kanji/霜.md:75-76) |
| D9 | 酒 | alcohol; sake | 霜 | 隠語大辞典 lists 霜 as slang for all alcoholic drinks (evidence/external-snapshots/06-extract.txt:32) | Harmless as an ordinary meaning (single jargon source); unmentioned on the card, see O3 |
| D10 | 軍 | army; troops | 衛 | Guard-person branch versus troops (evidence/external-snapshots/01-extract.txt:12) | Harmless: 衛 is a guarding person or function, not an army (repo/kanji/軍.md:22); 衛's 兵 exclusion is explicitly conservative |
| D11 | 隊 | squad; troop | 衛 | Guard units such as 親衛隊 (evidence/jmdict-review-core.xml:191) | Harmless: 隊 is an organized group (repo/kanji/隊.md:24-30); 衛 does not name a unit; 隊 itself excludes 軍/兵/武 but not 衛 |
| D12 | 武 | military; warrior | 衛 | Military/guard-person overlap (evidence/jmdict-extension-records/2083510.xml:2) | Harmless: 武 is martial arts/force/officer; guarding/defending is a different function |
| D13 | 送 | send; escort | 衛 | 護衛/衛護 gloss guard; escort (evidence/jmdict-review-core.xml:35) | Harmless with medium confidence: 送's escort is seeing someone off or taking them home (repo/kanji/送.md:22-23), not protective guarding |
| D14 | 援 | aid; assistance | 衛 | 援 card itself excludes 保/守/防 because its save/protect senses overlap guarding and defending (repo/kanji/援.md:67-74) | Collision needing exclusion; not declared on 衛 (snapshot/kanji/衛.md:15) or 援 (repo/kanji/援.md:15); see F2 |
| D15 | 塀 | boundary wall; fence | 衛 | 衛 surrounding branch (evidence/external-snapshots/01-extract.txt:13) | Harmless: 塀 is a physical wall/fence noun (evidence/jmdict-extension-records/1506870.xml:2); 衛 does not name a structure |
| D16 | 循 | follow; cycle | 衛 | 循 excludes 回/周 for going around (repo/kanji/循.md:44); 衛 orbits/circles (evidence/external-snapshots/01-extract.txt:13) | Harmless: cycle/circulation is not orbiting a centre; optional precaution in O2 |
| D17 | 畜 | livestock; domestic animals | 羊 | Sheep are livestock (evidence/external-snapshots/03-extract.txt:16) | Harmless with medium confidence: category versus one species; 羊 has the single sense sheep (evidence/jmdict-review-core.xml:123) |
| D18 | 獣 | beast; animal | 羊 | General animal category (repo/kanji/獣.md:22-24) | Harmless: category label; 羊 is the specific species (evidence/jmdict-review-core.xml:123) |
| D19 | 群 | flock; cluster; crowd | 羊 | 羊群/群羊 flock of sheep (evidence/jmdict-review-core.xml:175) | Harmless: 群 names groups of any kind (repo/kanji/群.md:22); flock is a whole-word meaning, not bare 羊 |
| D20 | 美 | beauty | 羊 | 羊 standing for 祥 good/auspicious (evidence/external-snapshots/03-extract.txt:42) | Harmless: 美 senses are beauty/beautiful only (evidence/jmdict-extension-records/1486350.xml:2, 2259710.xml:2); good is not beauty |
| D21 | 義 | righteousness; duty; meaning | 羊 | Auspicious-good branch versus virtue (snapshot/kanji/羊.md:65-70) | Harmless: 義's senses (repo/kanji/義.md:22-26) do not include good-omen or animal senses |
| D22 | 富 | wealth; abundance | 羊 | Slang money sense (evidence/external-snapshots/04-extract.txt:141) shares head word wealth with excluded 財 | Harmless: slang denotes paper/banknotes/cash, not riches or abundance (repo/kanji/富.md:22-23); exclusions are not transitive |
| D23 | 宝 | treasure; valuables | 羊 | Slang money sense | Harmless: treasure (repo/kanji/宝.md:22) is not banknotes or paper |
| D24 | 符 | token; sign; charm | 羊 | 羊 for 祥 auspicious sign | Harmless: 符 senses are charm/tally/sign mark (evidence/jmdict-extension-records/2703290.xml:2), not good omen; 兆 already covers omen |
| E1 | 未 | not yet | 羊 | Sheep zodiac branch ひつじ (evidence/jmdict-review-core.xml:133) | Already handled: declared on 羊 (snapshot/kanji/羊.md:15); 未 metadata keeps ひつじ (repo/kanji/未.md:10) |
| E2 | 宙 | space; midair | 霜 | 宙 retains an interval-of-time sense (repo/kanji/宙.md:46-51) | Already handled: declared on 霜 (snapshot/kanji/霜.md:13); the card's "qualified time branch" wording matches 宙's article |
| E3 | 令 | command; decree | 羊 | KANJIDIC 令 includes good (evidence/kanjidic2-review-projection.xml:13) | Already handled: declared on 羊 (snapshot/kanji/羊.md:15); 令 article retains a favorable sense (repo/kanji/令.md:22) |
| E4 | 兵 | soldier; troops | 衛 | Guard-person branch | Already handled conservatively: declared on 衛 (snapshot/kanji/衛.md:15); 兵 article is soldiers/troops only (repo/kanji/兵.md:22) |
| E5 | 卒 | graduate; finish | 衛 | Soldier source sense (repo/kanji/卒.md:22) | Already handled conservatively: declared on 衛 (snapshot/kanji/衛.md:15); displayed title shows no soldier sense |

## Per-card results
| Card | Correctness | Scoped coverage | Consistency/quiz safety | Comprehensibility | Evidence |
| --- | --- | --- | --- | --- | --- |
| 衛 | CLEAN | CLEAN | NEEDS FIX | CLEAN | F2, O2; KANJIDIC projection line 2; 01/02 extracts; diffs/existing.diff; strokes 16 |
| 羊 | CLEAN | CLEAN | CLEAN | CLEAN | O1; KANJIDIC projection line 3; 03/04 extracts; JMdict 1546490/1546530; strokes 6 |
| 霜 | CLEAN | CLEAN | NEEDS FIX | CLEAN | F1, O1, O3; KANJIDIC projection line 4; 05/06 extracts; JMdict 1402930; strokes 17 |

## Findings
### F1: 霜 lacks direct exclusions with 凍 and 氷
- Facet: Consistency/quiz safety
- Severity: low
- Confidence: medium
- Citations: snapshot/kanji/霜.md:13; snapshot/kanji/霜.md:59-62; repo/kanji/凍.md:1-12; repo/kanji/氷.md:1-12; evidence/external-snapshots/05-extract.txt:17; evidence/external-snapshots/06-extract.txt:177
- Evidence: Frost is defined as ice crystals formed below freezing (05-extract:17), and English "frost" also names freezing phenomena such as frost heaving (06-extract:177). The displayed titles "freeze; frozen" (凍) and "ice; freeze" (氷) therefore overlap "frost" more closely than "cold; chill" (冷) and "cold weather" (寒), which 霜 already excludes for its cold comparisons (霜.md:59-62). Neither direct pair is declared on 霜 (霜.md:13) or on 凍/氷, whose front matter has no quiz_exclusions. Current curated options (古右川) do not expose the pairs, but tag/random fallback or custom pools could.
- Required change: Add 凍 and 氷 to 霜's quiz_exclusions (or declare 霜 on those cards), with a brief Notes line on the ice/freezing overlap; rerun validate and rebuild the manifest.

### F2: 衛 and 援 share the protection overlap but declare no direct pair
- Facet: Consistency/quiz safety
- Severity: low
- Confidence: medium
- Citations: snapshot/kanji/衛.md:15; snapshot/kanji/衛.md:60-64; repo/kanji/援.md:15; repo/kanji/援.md:67-74; evidence/external-snapshots/01-extract.txt:12
- Evidence: 衛 is defined as guarding/protecting (01-extract:12) and its displayed label is "guard; defense". 援's card excludes 守 "guard; obey" and 防 "defend; ward off" specifically because its save/rescue sense overlaps protection (援.md:67-74), and 衛 excludes 保/守/防 for the same overlap (衛.md:15, 60-64). The same reasoning applies directly to 衛's label "guard; defense" against 援's label "aid; assistance", yet neither card declares the 衛–援 pair. Exclusions are not transitive, so the existing 守/防 pairs do not cover it.
- Required change: Declare the direct 衛–援 pair on one card (for example add 援 to 衛's quiz_exclusions with a Notes mention of protective aid), then validate and rebuild the manifest.

## Optional points
### O1: Sourced structure classifications are available for 羊 and 霜
- Facet: Scoped coverage
- Severity: optional
- Confidence: medium
- Citations: snapshot/kanji/羊.md:5; snapshot/kanji/羊.md:26-28; evidence/external-snapshots/03-extract.txt:38-39; snapshot/kanji/霜.md:5; snapshot/kanji/霜.md:27-30; evidence/external-snapshots/05-extract.txt:42-43
- Evidence: The cited 字通 entries classify 羊 as a pictograph of a sheep seen from the front (03-extract:38-39) and 霜 as a phonetic compound with 相 as the phonetic (05-extract:42-43; KanjiVG also marks 相 phon in shape-evidence.json). The cards keep structure-unclassified and present only mnemonics. This is conservative rather than wrong, and 衛's phonetic glyph is image-only in the extract.
- Suggestion: Optionally tag 羊 pictograph and 霜 phonetic-compound with a hedged, cited sentence (single-source, "commonly explained"), keeping the mnemonics labelled.

### O2: Optional precaution for the 衛–循 pair
- Facet: Consistency/quiz safety
- Severity: optional
- Confidence: low
- Citations: snapshot/kanji/衛.md:65-69; repo/kanji/循.md:15; repo/kanji/循.md:44
- Evidence: 衛 conservatively excludes circling labels down to 輪 "wheel; ring" and 舞 "dance"; 循 "follow; cycle" excludes 回/周 for its going-around sense. Cycle/circulation is not orbiting, so no collision is established.
- Suggestion: Consider adding 循 for symmetry with the existing circling precautions, or note why "cycle" is not included.

### O3: 霜's jargon alcohol sense is not mentioned
- Facet: Scoped coverage
- Severity: optional
- Confidence: medium
- Citations: evidence/external-snapshots/06-extract.txt:32; snapshot/kanji/羊.md:58-63
- Evidence: 隠語大辞典 records 霜 as slang for all alcoholic drinks (06-extract:32). The 羊 card treats comparable jargon/slang senses explicitly, while the 霜 card is silent; the single jargon source does not make this an ordinary meaning, so no 酒 exclusion is required.
- Suggestion: Optionally add a qualified one-line note so the two cards treat cited slang consistently.

## Limits
- L1: Execution model identity is reported by the runtime as Claude Opus 5.5 but is not independently verified.
- L2: JMdict evidence is limited to the 615-record core plus extension records; the coordinator reported no exact-keb match in the frozen union for 凍 枯 酒 隊 送 援 循 畜 獣 群 義 富, so those dispositions rest on their articles, KANJIDIC projection lines where present and opened extracts, not on unread dictionary records. This is not evidence of linguistic absence.
- L3: Not read under the chain-only contract: xml-presentation.json, font-cmap.json, baseline-title-index.txt, dictionary-index.json, full kanjidic2-records.xml and jmdict-families.xml, raw HTML/SVG responses, the binary Joyo PDF and receipts. Glyphs shown only as images in the 字通 extracts (including 衛's phonetic component) were not verified.
- L4: Identified but unrequested candidates, judged lower priority: 冬, 灰, 炭, 黒, 秋, 晩 (霜); 健, 康, 士, 城, 門, 督, 監-adjacent observation labels (衛); 牛, 豚, 綿, 糸, 皮, 革, 栄, 資, 吉-type good-luck labels absent from the index (羊). Their direct pairs are unassessed.
- L5: The font summary states U+885E (衛 itself) is absent from all three bundled cmaps; rendered fallback, native and device display were not assessed.
- L6: Stroke JSON was checked only for counts, revision and consistency with the cards and shape evidence; no visual geometry claim is made.
- L7: The reading-exposure audit covers bounded N1/All/Starter pools only; custom pools, multiple borrowing, Kotlin execution, installed-APK compatibility and device acceptance are outside this review. Runtime exposure of F1/F2 in fallback pools is not measured.

# B133 initial review — N1-B133-CLAUDE-001

## Overall verdict
Verdict: CLEAN

## Facet verdicts
### Correctness
Verdict: CLEAN
Basis: Every material lexical claim checked in the three new cards and three wrappers is supported by opened evidence: the JMdict families (1241450, 2229960, 1241460, 2204940, 1178500, 1178590, 1287560, 1415520, 1415530, 1415540, 1475290, 2254980), the KANJIDIC2 projection (readings, radicals, stroke counts, らき as nanori), the Joyo rows, and the Kotobank/Weblio extracts (字通 senses and old dictionary forms; 日本国語大辞典 counterfeit-money, heavy/dull, 滝水, たるみ and たぎ; the Daijisen おしろい and lead-like-substance senses). Mnemonics are labelled and make no historical claim.

### Scoped coverage
Verdict: CLEAN
Basis: Each card supplies the required facts line, meaning, a reading table covering every metadata reading (on readings with dispositions, each kun reading with a real word), common words and notes. Each card has a reciprocal link to its existing support word, and each support article gains exactly one substantive reciprocal link. Rare, historical and source-only forms are retained as recognition evidence, not inflated into practice.

### Consistency/quiz safety
Verdict: CLEAN
Basis: For every D/E comparison I read, I found no plausible meaning-choice ambiguity that lacks a declared direct exclusion. The curated distractors 古, 右, 川 and 寺 are semantically and phonetically distinct from their targets. The quiz-safety, reading-exposure, lint, validate, linkplan, manifest and budget gates passed. These are mechanical checks, not linguistic proof. The one notable label overlap (率 "lead") is judged harmless and recorded as optional point O1.

### Comprehensibility
Verdict: CLEAN
Basis: The explanations are short and standalone. They give kana for unfamiliar words and explicitly separate whole-word senses (琴線, 琴瑟, 白滝, 黒鉛) from the bare character. They warn about English homographs: lead the metal versus lead meaning guide, and the koto versus a Western harp. Optional clarity improvements are listed as O-items.

## Segments read
Core chain: 1-69, each read once in order through END OF CHAIN; no re-views.
Extension chain: 1-3, each read once in order through END OF CHAIN; no re-views.
Baseline representation: I read the complete candidate title index (evidence/title-index.txt, 1261 lines) and the exact three-line deletion delta (evidence/baseline-title-delta.json). I did not read the raw baseline index.
I read all three new cards, their stroke JSON, and the before/after texts of the three support words (琴, 鉛筆, 滝). Both diffs, all gate logs and receipts, all evidence files and all six external extracts were read through the core chain.

## Phase-1 D/E lists
D: D1 率, D2 鉱, D3 鉄, D4 管, D5 拍, D6 張, D7 泉, D8 速, D9 滴
E: E1 急, E2 金
O: none
Missing entries: none

## D/E cards read
| ID | Character | Displayed title | Related new card(s) | Reason | Disposition |
| --- | --- | --- | --- | --- | --- |
| D1 | 率 | rate; lead; frank | 鉛 | The English head word "lead" is shared (repo/kanji/率.md:3 versus snapshot/kanji/鉛.md:3). | Harmless: 率's "lead" is the verb 率いる, to command, and its other senses are rate and frank (repo/kanji/率.md:23-25). 鉛 means the metal Pb, and its label carries the (metal) qualifier. Its card also states that it is not the verb "lead" (snapshot/kanji/鉛.md:23-24). The two characters share no ordinary sense. The direct pair is not declared on either endpoint. See O1. |
| D2 | 鉱 | ore; mineral | 鉛 | 鉛鉱 means lead ore, so an ore/mineral sense was a candidate overlap. | Harmless: 鉱 covers unrefined ore and mineral material (repo/kanji/鉱.md:21). Lead is a refined metal element. Its Daijisen lead-like-substance sense covers graphite, zinc and bismuth compounds, not ore (evidence/external-snapshots/03-extract.txt:15). The pair is not declared on either endpoint, and none is needed. |
| D3 | 鉄 | iron | 鉛 | Both carry a metal label. | Harmless: 鉄 names one specific metal, iron (repo/kanji/鉄.md:21), and has no broad metal or money label. Iron and lead are different elements. The pair is not declared on either endpoint, and none is needed. |
| D4 | 管 | pipe; supervise | 琴 | 管 has a secondary wind-instrument sense (evidence/jmdict-families.xml:245; repo/kanji/管.md:36). | Harmless: a wind instrument is not a zither. The displayed title "pipe; supervise" is not an answer for 琴, and "koto; zither" does not describe 管. The pair is not declared on either endpoint. |
| D5 | 拍 | clap; musical beat | 琴 | Both have music senses; 字通 also records wooden clappers for 拍 (repo/kanji/拍.md:59-62). | Harmless: a beat, clapping or a clapper is not a stringed zither, and koto does not mean a beat. 拍 declares guards against broad music labels (楽, 曲, 調, 整, 律), not instrument names. The 拍-琴 pair is not declared on either endpoint. |
| D6 | 張 | stretch tight; assert | 琴 | 張 is a counter for strung things such as bows and koto (repo/kanji/張.md:23). | Harmless: a counter for kotos does not name the instrument, and neither displayed title fits the other card. The pair is not declared on either endpoint. |
| D7 | 泉 | spring; water source | 滝 | Both are water features. | Harmless: a spring is a water source emerging from the ground (repo/kanji/泉.md:20). A waterfall, or archaic rapids, is water falling or running fast in a watercourse. The 滝水 sense means water from a waterfall, not a spring. The pair is not declared on either endpoint. |
| D8 | 速 | fast | 滝 | 速 shows a speed adjective; 滝's title shows the noun "rapids". | Harmless: the "rapids" sense of 滝 denotes a fast-flowing stretch of a river (evidence/jmdict-families.xml:162), while 速 is general speed (repo/kanji/速.md:20). A learner would not accept "fast" as the name of a river feature. The pair is not declared on either endpoint. The declared 滝-急 pair is more conservative than this one (see E1). |
| D9 | 滴 | drip; drop | 滝 | Falling water and "drop" as a possible fall or descent were candidate overlaps. | Harmless with medium confidence: 滴 means droplets and dripping (repo/kanji/滴.md:20), and "drop" paired with "drip" reads as a droplet. 滝 is a mass of water falling or rushing. The broad falling labels 落 and 降 are declared on 滝, but 滴 has no fall or descent sense. The pair is not declared on either endpoint. |
| E1 | 急 | urgent, sudden | 滝 | This is a declared 滝 exclusion target (snapshot/kanji/滝.md:14). I read it to check the rapid/swift basis. | Already handled: the 急 card shows urgency, suddenness and steepness (repo/kanji/急.md:20). JMdict adds "rapid; swift" (evidence/jmdict-families.xml:61). The direct pair is declared on 滝 only. This conservative guard is harmless and a symmetric declaration is not required. |
| E2 | 金 | gold, money | 鉛 | This is a declared 鉛 exclusion target (snapshot/kanji/鉛.md:14). I read it to check the metal-label basis. | Already handled: the 金 card teaches "metal" as well as gold and money (repo/kanji/金.md:20). JMdict 金 かね sense 2 is "metal" (evidence/jmdict-families.xml:69). This supports the direct guard declared on 鉛. |

## Per-card results
| Card | Correctness | Scoped coverage | Consistency/quiz safety | Comprehensibility | Evidence |
| --- | --- | --- | --- | --- | --- |
| 琴 | CLEAN | CLEAN | CLEAN | CLEAN | JMdict 1241450 (archaic こと sense; そう restricted to 箏/筝), 2229960, 1241460 and 2204940. KANJIDIC2 gives キン, ゴン, こと and 12 strokes, matching the 12-stroke JSON. 字通 supports the ことのを, キノコト and Chu-language mound senses, and Weblio/Wiktionary gives ゴム and キム. The distractors 古, 右 and 川 are distinct. D4, D5 and D6 are harmless. The single changed line in words/琴.md links to ../kanji/琴.md. See O2. |
| 鉛 | CLEAN | CLEAN | CLEAN | CLEAN | JMdict 1178500, 1178590 and 1287560. KANJIDIC2 gives エン, なまり and 13 strokes, matching the 13-stroke JSON. 日国 supports the counterfeit-money and heavy/dull senses, and Daijisen the おしろい and lead-like-substance senses. The declared money, metal, powder and heavy guards cover its senses (E2). D1, D2 and D3 are harmless. The single changed line in words/鉛筆.md links to ../kanji/鉛.md. See O1. |
| 滝 | CLEAN | CLEAN | CLEAN | CLEAN | JMdict 1415520 gives archaic rapids, plus 1415530, 1415540, 1475290 and 2254980. KANJIDIC2 gives ロウ, ソウ, たき, nanori らき and 13 strokes, matching the 13-stroke JSON. 字通 senses and 日国 たるみ/たぎ are verified. The water, falling and sound guards are declared (E1). D7, D8 and D9 are harmless. The single changed line in words/滝.md links to ../kanji/滝.md. See O2, O3 and O4. |

## Findings
None.

## Optional points
### O1: Optional direct guard for the English homograph "lead"
- Facet: Consistency/quiz safety
- Severity: optional
- Confidence: medium
- Citations: snapshot/kanji/鉛.md:3; snapshot/kanji/鉛.md:14; snapshot/kanji/鉛.md:23-24; repo/kanji/率.md:3; repo/kanji/率.md:14
- Evidence: Both displayed titles contain the bare English string "lead". In 鉛's title it is qualified "(metal)"; in 率's title, "rate; lead; frank", it is not. Neither card declares the direct pair. The meanings do not overlap, and the 鉛 card explicitly distinguishes the verb "lead", so I judge the pair harmless. Even so, a fallback choice showing two "lead" labels relies entirely on the learner noticing the qualifier.
- Suggestion: Optionally add 率 to 鉛's quiz_exclusions as a cheap homograph guard, consistent with the batch's conservative guards. Alternatively, record why the (metal) qualifier is judged sufficient.

### O2: Source-attested phonetic analyses are not mentioned
- Facet: Scoped coverage
- Severity: optional
- Confidence: medium
- Citations: evidence/external-snapshots/01-extract.txt:41-42; evidence/external-snapshots/05-extract.txt:111-112; snapshot/kanji/琴.md:4; snapshot/kanji/滝.md:4
- Evidence: 字通 classifies 琴 as 形声 with 声符 今, and 滝 as 形声 with 竜 (龍) as the phonetic. The KanjiVG shape evidence marks 今, 㕣 and 竜 as phon. The cards use structure-unclassified, which the rubric allows when no historical analysis is established. I found no contradiction.
- Suggestion: Optionally add a hedged, cited note such as "字通 analyses this as a phonetic compound with 今 (or 竜)". This should not replace the labelled mnemonic or change the tag unless the author judges the analysis established.

### O3: The quiz label foregrounds the archaic "rapids" sense
- Facet: Comprehensibility
- Severity: optional
- Confidence: medium
- Citations: snapshot/kanji/滝.md:3; snapshot/kanji/滝.md:23-24; evidence/jmdict-families.xml:162; snapshot/words/滝.md:3
- Evidence: The displayed title "waterfall; rapids" follows KANJIDIC2, but JMdict marks the rapids sense archaic. The body qualifies this, and the support word's title is just "waterfall". A learner who sees only the quiz label could take "rapids" to be an equal modern meaning.
- Suggestion: Optionally consider "waterfall" alone, or "waterfall; (archaic) rapids", if the app's labels allow it. Any title change needs a fresh exclusion check.

### O4: The on readings of 滝 are not in the Joyo table
- Facet: Comprehensibility
- Severity: optional
- Confidence: high
- Citations: evidence/joyo-rows.json:27; snapshot/kanji/滝.md:38-39
- Evidence: The Joyo row for 滝 lists only たき. The card describes ロウ and ソウ only as retained from KANJIDIC2, without supporting words.
- Suggestion: Optionally state that ロウ and ソウ are outside the official Joyo readings, so learners do not treat them as ordinary standard readings.

## Limits
- L1: My execution model is reported by the host as Claude Opus 5.5, but that identity is not verifiable from the evidence opened in this pass, so it is disclosed as unverified.
- L2: The baseline title index is represented by the candidate index plus the exact deletion delta, not a raw baseline read. The original XML selections, raw HTML/SVG, full KANJIDIC2 records and derived indices were not read (O: none).
- L3: The stroke JSON was checked only for stroke count, source and revision consistency against the card and the KanjiVG group evidence. I made no visual geometry, rendered-font, fallback-glyph or device judgment; historical glyph images are unavailable.
- L4: Reading-exposure results cover only the bounded N1, All and Starter pools plus one borrow. They do not cover custom or multiple-borrow pools, Kotlin, native or phone behaviour, or compatibility with older APKs. The latent 滝/湿 うるおす key is a non-drawable hypothetical, accepted as reported and not independently re-run.
- L5: Candidates identified but not read: 銅 (copper; same metal-label reasoning as the harmless 鉄), 冶 (smelt; work metals), 歌 (song), 浅 (shallow), 激 (intense) and 筒 (cylinder; tube). I judged none plausibly ambiguous from its displayed title, but their full card texts were not opened.
- L6: The harmless dispositions for D9 (滴) and O1 (率) depend on how learners read English labels; that judgment cannot be fully settled from dictionary evidence alone.
- L7: Gate logs and receipts were read as supplied; I did not re-execute validators, the manifest build, unit tests or budget checks. Mechanical passes are not linguistic acceptance.

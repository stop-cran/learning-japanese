# B134 initial review — N1-B134-CLAUDE-001

## Overall verdict
Verdict: UNVERIFIED

## Facet verdicts
### Correctness
Verdict: CLEAN
Basis: Every material claim in snapshot/kanji/紫.md (purple/violet, purple gromwell with white flowers and dye root, soy sauce, 日本国語大辞典 secondary senses, 字通 11-stroke label and ツツム gloss, KANJIDIC2 name readings さい/ゆかり, 紫陽花 jukujikun, シ/むらさき, 12 strokes, 糸 no. 120, grade 8) is supported by opened JMdict, KANJIDIC2 projection and Kotobank/Weblio extracts; the stroke JSON has 12 strokes from the pinned KanjiVG revision; the support-article diff adds exactly one correct reciprocal link.

### Scoped coverage
Verdict: CLEAN
Basis: The card teaches the color meaning, the sourced plant/condiment uses, both readings with dispositions, common words and qualified historical senses; the mnemonic is labelled as non-etymological, which the contract permits. A sourced 形声 formation is available but its omission is optional (O2), not a defect.

### Consistency/quiz safety
Verdict: UNVERIFIED
Basis: Curated distractors 古/右/川 are semantically and phonologically safe, and no read D/E card established a missing pair; however the direct 紫/紺 pair is declared on neither endpoint while the 紺 card itself asserts a Daijisen purplish cast, and the decisive Daijisen 紺 text is not in the opened evidence, so whether "navy blue" and "purple; violet" are both defensible cannot be settled (O1, L2).

### Comprehensibility
Verdict: CLEAN
Basis: Meaning, reading table, dispositions of name/historical readings and the stroke discrepancy are explained in plain English with kana; the dense precaution list is understandable though some groupings are unexplained (O3).

## Segments read
Core chain: segments 1-49, each read once in order, no re-views.
Extension chain: segments 1-7, each read once in order, no re-views.
Title index: evidence/title-index.txt lines 1-1262 read in full (core segments 42-43). The baseline is represented by that complete candidate index plus the exact one-line deletion delta in evidence/baseline-title-delta.json; the raw baseline index was not read.
Complete external extracts 01-extract.txt and 02-extract.txt were read in full through the chain.

## Phase-1 D/E lists
D: D1 紺, D2 紅, D3 青, D4 根, D5 花, D6 絹, D7 層, D8 列, D9 稲, D10 殿, D11 書, D12 妻, D13 町, D14 油, D15 被, D16 系, D17 濃, D18 薄
E: E1 久, E2 色, E3 包, E4 統, E5 館, E6 札, E7 植, E8 極
O: none
Missing entries: none

## D/E cards read
| ID | Character | Displayed title | Related new card(s) | Reason | Disposition |
| --- | --- | --- | --- | --- | --- |
| D1 | 紺 | navy blue | 紫 | Possible hue overlap: 紫紺 is glossed dark/bluish purple (evidence/jmdict-families.xml:88) and the 紺 card says Daijisen gives 紺 a purplish cast (repo/kanji/紺.md:24) | UNVERIFIED; pair not declared on either endpoint (snapshot/kanji/紫.md:14; repo/kanji/紺.md:14). The purplish-cast claim is a candidate assertion and Daijisen 紺 is not in the evidence, so defensibility of "purple; violet" for 紺 is unsettled; see O1 |
| D2 | 紅 | crimson; deep red | 紫 | English "purple" can include crimson (evidence/external-snapshots/02-extract.txt:213-217) and 紅紫 is red-purple (evidence/jmdict-families.xml:354) | Harmless: 紅紫 lists crimson and purple as two colors and the 紅 card teaches only crimson/red and rouge (repo/kanji/紅.md:3); no ordinary 紫 sense is crimson. Pair not declared on either endpoint |
| D3 | 青 | blue, green | 紫 | Violet as spectral blue-purple; 青紫 bluish purple (evidence/external-snapshots/02-extract.txt:198-212; evidence/jmdict-families.xml:321) | Harmless: 青 card covers blue/green and youth senses only (repo/kanji/青.md:3); 青紫 is a compound shade, not a 紫 sense of 青. Pair not declared |
| D4 | 根 | root; foundation | 紫 | 紫根 is the gromwell root used for dye (evidence/jmdict-families.xml:280) | Harmless: 紫 names the plant and color (evidence/jmdict-families.xml:83), not a root; 根 card has no plant-name or color sense (repo/kanji/根.md:3). Pair not declared |
| D5 | 花 | flower | 紫 | 紫 names the flowering plant gromwell; English "violet" can name a flower | Harmless: 紫 is a plant name whose flowers are white (evidence/external-snapshots/01-extract.txt:10), not "flower"; 花 card (repo/kanji/花.md:3) has no purple sense, and a specific flower name is not a defensible answer for generic flower. Pair not declared |
| D6 | 絹 | silk | 紫 | One theory makes the original meaning purple-dyed silk; 紫 also names purple cloth (evidence/external-snapshots/02-extract.txt:204; evidence/external-snapshots/01-extract.txt:32) | Harmless: the silk link is an etymological theory and the cloth sense is purple-colored cloth, not silk as such; 絹 card (repo/kanji/絹.md:3) has no purple sense. Pair not declared |
| D7 | 層 | layer; stratum | 紫 | 紫 as the rank 検校 (evidence/external-snapshots/01-extract.txt:36); KANJIDIC2 層 social class (evidence/kanjidic2-review-projection.xml:38) | Harmless: 紫 is one specific historical rank title, while 層 teaches layers and class strata (repo/kanji/層.md:3); neither title fits the other. Pair not declared |
| D8 | 列 | row; queue | 紫 | Rank sense; JMdict 列 includes rank in the row sense (evidence/jmdict-families.xml:181) | Harmless: 列's rank is a line of people, not a status title (repo/kanji/列.md:3); 紫's rank use is the specific title 検校. Pair not declared |
| D9 | 稲 | rice plant | 紫 | Plant sense of 紫 | Harmless: both name specific different plants (evidence/jmdict-families.xml:10; evidence/jmdict-families.xml:83); repo/kanji/稲.md:3. Pair not declared |
| D10 | 殿 | palace; lord | 紫 | 紫 appears in palace words 紫宸殿/紫闥 (evidence/jmdict-families.xml:268) and 殿 との palace (evidence/jmdict-families.xml:137) | Harmless: palace meaning belongs to whole compounds, not to 紫 alone; no source gives 紫 the sense palace or lord; repo/kanji/殿.md:3. Pair not declared |
| D11 | 書 | write | 紫 | Book/writing precautions (Genji, a poetry collection titled 紫) (evidence/external-snapshots/01-extract.txt:23-24; evidence/external-snapshots/01-extract.txt:39) | Harmless: these are specific titles, not a write/book meaning; 書 card (repo/kanji/書.md:3) has no purple sense. Pair not declared; the card's inclusion of 著 "write" is merely more conservative |
| D12 | 妻 | wife | 紫 | 紫 recorded for woman in 日葡辞書 (evidence/external-snapshots/01-extract.txt:34) | Harmless: woman is not wife; 妻 card specifies a marriage relationship (repo/kanji/妻.md:3). Pair not declared |
| D13 | 町 | town, neighborhood | 紫 | 紫 as an abbreviation for Edo (evidence/external-snapshots/01-extract.txt:37) | Harmless: a historical abbreviation for one city does not make "town" a 紫 meaning; repo/kanji/町.md:3. Pair not declared |
| D14 | 油 | oil; grease | 紫 | 紫 means soy sauce (evidence/external-snapshots/01-extract.txt:35) | Harmless: soy sauce is not oil; 油 card links 醤油 only as a word containing 油 (repo/kanji/油.md:3). Pair not declared |
| D15 | 被 | cover; incur | 紫 | Historical ツツム gloss of 紫 (evidence/external-snapshots/01-extract.txt:59) | Harmless: the gloss has unresolved scope and is only a 名義抄 lookup gloss; it is not an ordinary sense, and 被 is cover/incur (repo/kanji/被.md:3). Pair not declared |
| D16 | 系 | lineage; system | 紫 | ゆかり association of 紫 (evidence/external-snapshots/01-extract.txt:44; evidence/external-snapshots/01-extract.txt:77) | Harmless: ゆかり is a name reading and a literary association, not a lineage/system meaning; 系 card (repo/kanji/系.md:3) has no color sense. Pair not declared |
| D17 | 濃 | concentrated; dark | 紫 | Heian 濃(き色) alone could mean deep purple (evidence/external-snapshots/01-extract.txt:76; evidence/external-snapshots/01-extract.txt:100) | Harmless for modern display: this is a historical court usage; 濃 card teaches concentration/darkness (repo/kanji/濃.md:3) and "dark" is not a defensible meaning of 紫. Pair not declared |
| D18 | 薄 | thin; dilute | 紫 | Heian 薄色 meant light purple (evidence/external-snapshots/01-extract.txt:100) | Harmless: historical color-term convention only; 薄 card (repo/kanji/薄.md:3) has no purple sense. Pair not declared |
| E1 | 久 | a long time | 紫 | Declared exclusion target (snapshot/kanji/紫.md:14) grouped under book or writing | Already handled (declared on 紫); only link is 久しい "old (story)" (repo/kanji/久.md:29), a weak precautionary basis; see O3 |
| E2 | 色 | color | 紫 | Declared; Heian 色 alone could mean purple (evidence/external-snapshots/02-extract.txt:208) | Already handled by declaration on 紫 (snapshot/kanji/紫.md:14); color category vs specific color justifies the guard |
| E3 | 包 | wrap; enclose | 紫 | Declared; つつむ latent reading collision (checks/reading-exposure.log:19-20) | Already handled for meaning by declaration on 紫; the reading latent collision is not drawable in checked pools; 包 card readings つつ.む/くる.む (repo/kanji/包.md:3) |
| E4 | 統 | unify; lineage | 紫 | Declared; KANJIDIC2 relationship gloss (evidence/kanjidic2-review-projection.xml:84) | Already handled by declaration on 紫; precautionary only, 統 card teaches unify/lineage (repo/kanji/統.md:3) |
| E5 | 館 | hall; large building | 紫 | Declared; JMdict 館 noblewoman sense (evidence/jmdict-families.xml:34) | Already handled by declaration on 紫; basis is an archaic honorific, precautionary (repo/kanji/館.md:3) |
| E6 | 札 | tag; banknote | 紫 | Declared; purple paper or cloth sense (evidence/external-snapshots/01-extract.txt:32) | Already handled by declaration on 紫; precautionary (repo/kanji/札.md:3) |
| E7 | 植 | plant; put in the ground | 紫 | Declared; plant headword overlaps gromwell plant sense (evidence/jmdict-families.xml:83) | Already handled by declaration on 紫; consistent with D5/D9 harmless dispositions because "plant" is generic (repo/kanji/植.md:3) |
| E8 | 極 | extreme; pole | 紫 | Declared; KANJIDIC2 highest rank (evidence/kanjidic2-review-projection.xml:62) | Already handled by declaration on 紫; precautionary for the 検校 rank use (repo/kanji/極.md:3) |

## Per-card results
| Card | Correctness | Scoped coverage | Consistency/quiz safety | Comprehensibility | Evidence |
| --- | --- | --- | --- | --- | --- |
| 紫 | CLEAN | CLEAN | UNVERIFIED | CLEAN | snapshot/kanji/紫.md:1-80 against JMdict 1311640, KANJIDIC2 紫, Kotobank/Weblio extracts, diffs/existing.diff; O1, O2, O3; L2 |

## Findings
None.

## Optional points
### O1: Decide and record the direct 紫/紺 pair
- Facet: Consistency/quiz safety
- Severity: optional
- Confidence: medium
- Citations: snapshot/kanji/紫.md:14; repo/kanji/紺.md:14; repo/kanji/紺.md:24; evidence/jmdict-families.xml:88; evidence/external-snapshots/02-extract.txt:198-212
- Evidence: Neither card declares the direct pair. The 紺 card attributes a purplish cast to Daijisen, 紫紺 is glossed bluish purple, and the Wikipedia extract notes that violet sits at the blue/purple boundary. The batch excludes far weaker precautionary pairs (for example 久), while 紺 itself excludes 濃 for a mere "dark" cue.
- Suggestion: Verify the Daijisen 紺 entry; if it supports a purplish cast, add 紺 to 紫 quiz_exclusions (or 紫 to 紺), otherwise record why the pair is distinguishable.

### O2: Mention the sourced phonetic-compound analysis
- Facet: Scoped coverage
- Severity: optional
- Confidence: medium
- Citations: evidence/external-snapshots/01-extract.txt:54; evidence/shape-evidence.json:22; snapshot/kanji/紫.md:5; snapshot/kanji/紫.md:27-29
- Evidence: 字通 classifies 紫 as 形声 with phonetic 此, and KanjiVG marks 此 as phon; the card uses structure-unclassified and only an invented mnemonic.
- Suggestion: Optionally add a qualified line such as "字通 analyses 紫 as 糸 with phonetic 此", keeping the mnemonic label.

### O3: Explain or trim the weakest precaution groupings
- Facet: Comprehensibility
- Severity: optional
- Confidence: medium
- Citations: snapshot/kanji/紫.md:65-69; repo/kanji/久.md:29; repo/kanji/館.md:3
- Evidence: The learner-facing list puts 久 "a long time" under book or writing and 館 "hall; large building" under woman without saying why; the only visible links are 久しい "old (story)" and an archaic noblewoman sense of 館.
- Suggestion: Add a brief reason for these groupings or drop pairs with no ordinary-meaning basis.

## Limits
- L1: Execution-model identity is not independently verifiable from within this pass; the environment reports Claude Opus 5.5, which is disclosed but unverified.
- L2: The Daijisen 紺 entry was not in the opened evidence; the purplish-cast claim is only a candidate-card assertion, so the 紫/紺 semantic decision and the consistency facet remain UNVERIFIED.
- L3: Identified but unread candidates: 赤 (red; 赤紫), 典, 紀 and 史 (book or chronicle neighbours of the Genji precaution), 括 and 囲 (enclose, near the ツツム precaution), 菜 (紫菜), 鮎/鯉/鯛 (fish, near the sardine sense) and 神 (sacred uses per 字通). They were not selected because their titles showed no plausible ordinary overlap; they are not adjudicated.
- L4: The baseline title index was represented by the complete candidate index plus the one-line deletion delta; the raw baseline file was not read. Missing historical glyph images in the extracts are unavailable.
- L5: No optional KANJIDIC2 complete records or derived indices were requested (O: none); the projection was relied on for KANJIDIC2 facts.
- L6: Automated gate logs were read as evidence of structural checks only; reading-exposure covers bounded N1/All/Starter pools only, not custom or multi-borrow pools, Kotlin, native/device, rendering or installed-APK behavior. Stroke JSON was checked only for count, source and card consistency; no visual geometry claim is made.
- L7: The JLPT N1 label rests on the source-row metadata and jlpt-levels.md policy in the packet; no independent JLPT source was opened.

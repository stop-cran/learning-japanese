# B122 initial review — N1-B122-CLAUDE-001

## Overall verdict
Verdict: CLEAN

## Facet verdicts
### Correctness
Verdict: CLEAN
Basis: Metadata (11 strokes, radical 心 no. 61, grade 8, on ユウ, empty kun, nanori ゆ not selected) matches the KANJIDIC2 record; title senses "leisurely" and "distant" match Daijisen senses 1-2 and JMdict 2844201; 悠々/悠久/悠遠 glosses match JMdict; the Joyo claim matches the cached row; source-only はるか/とおい and name readings are correctly attributed to the Weblio sections. No established defect.

### Scoped coverage
Verdict: CLEAN
Basis: The card covers both core sense groups, the sole selected reading with a linked word, practical compounds, a labelled modern-shape mnemonic and the source-only readings; the one required link wrapper is present. Possible additions (悠長, 悠然) are optional, not required.

### Consistency/quiz safety
Verdict: CLEAN
Basis: Curated distractors 側/後/達 are semantically distinct with no ユウ reading overlap; all direct exclusion pairs that the evidence requires (遠, 久, 永, 静, 楽, 安, 平, 寧, 凪, 遅, 長, 広, 休) are declared on 悠; the six D comparisons are harmless at character level on the opened evidence; the diff adds only the one correct link wrapper; stroke count agrees across card, JSON, KANJIDIC2 and KanjiVG evidence.

### Comprehensibility
Verdict: CLEAN
Basis: Prose is short, qualified and distinguishes word-level 悠々 senses from the character, labels the mnemonic as non-etymological and explains comparison cards without claiming interchangeability. One wording point on source naming is optional (O2).

## Segments read
Core chain: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14 (each read once, in order; no re-views)
Extension chain: 1, 2, 3, 4 (each read once, in order; no re-views)
Title index: I read evidence/title-index.txt source lines 1-1242 across core segments 11-13; line 1 is "一 one" and line 1242 is "齢 age; years lived".
The initial instruction file was read once at kickoff as authorized. The external snapshot manifest and its one SUPPLIED extract (01-extract.txt, lines 1-125) were read in core segment 14.

## Phase-1 D/E lists
D: D1 易, D2 常, D3 遊, D4 優, D5 慢, D6 快
E: E1 和, E2 息, E3 凪, E4 寧, E5 楽, E6 遠, E7 久, E8 永, E9 広, E10 遅
Missing entries: none

## D/E cards read
| ID | Character | Displayed title | Related new card(s) | Reason | Disposition |
| --- | --- | --- | --- | --- | --- |
| D1 | 易 | easy | 悠 | Word 悠々 has an "easily; without difficulty" sense (evidence/jmdict-families.xml:140-146); 易 means not difficult (repo/kanji/易.md:20-22). | Harmless at character level: 悠's own character evidence (Daijisen senses evidence/external-snapshots/01-extract.txt:7-8; JMdict 2844201 evidence/jmdict-families.xml:255-280; KANJIDIC2 evidence/kanjidic2-records.xml:52-55) has no easy/not-difficult sense; the easily sense is word-level 悠々. Pair not declared on either endpoint; see O1 for an optional defensive exclusion. |
| D2 | 常 | usual; constant | 悠 | KANJIDIC2 gives 悠 "permanence" (evidence/kanjidic2-records.xml:52); 常 covers usual, regular, continuing and always (repo/kanji/常.md:20-22). | Harmless: 悠's extent sense is endless/far-reaching extent in time or space (evidence/external-snapshots/01-extract.txt:7), not regularity or "always"; the eternity overlap is handled by the declared 悠/永 and 悠/久 pairs. Pair 悠/常 not declared on either endpoint; not required. |
| D3 | 遊 | play | 悠 | 悠 "leisure" (evidence/kanjidic2-records.xml:55) versus play/recreation (repo/kanji/遊.md:20-21). | Harmless: 遊 is play and recreation, enjoying oneself; 悠 is an unhurried manner or far extent (evidence/external-snapshots/01-extract.txt:7-8), and neither card gives a play or leisure-time-activity sense for 悠. Not declared on either endpoint; not required. Shared ユウ reading does not affect the meaning quiz. |
| D4 | 優 | gentle; superior | 悠 | 優游自適 is a search-only spelling of 悠々自適 (evidence/jmdict-families.xml:13); 優 means kind/gentle and excellent (repo/kanji/優.md:20-22). | Harmless: "gentle" is kindness (優しい), not calmness or leisure, and the spelling variant is search-only; 悠 evidence has no kindness or superiority sense. Not declared on either endpoint; not required. |
| D5 | 慢 | arrogance; slackness | 悠 | 慢 includes a slack or negligent attitude and sluggish pace (repo/kanji/慢.md:33-36); 悠長 glosses include slow and easygoing (evidence/jmdict-families.xml:94-97). | Harmless, medium confidence: slackness is negligence or sluggishness, while 悠's character senses are a relaxed, unhurried, composed mood and far extent (evidence/external-snapshots/01-extract.txt:7-8; evidence/jmdict-families.xml:255-280); the slow overlap of each card is handled by its own declared exclusion with 遅. Not declared on either endpoint. |
| D6 | 快 | pleasant; agreeable | 悠 | Word 悠々 has a "comfortably" gloss (evidence/jmdict-families.xml:140-146); 快 covers pleasant feeling and 快適 comfortable (repo/kanji/快.md:20). | Harmless: "comfortably" belongs to the word 悠々's ease sense, not to 悠's character senses (evidence/external-snapshots/01-extract.txt:7-8), and "pleasant; agreeable" names a feeling, not a manner or extent. Not declared on either endpoint; not required. |
| E1 | 和 | harmony; Japanese style | 悠 | Card Notes say 和 includes peace or calm (snapshot/kanji/悠.md:45). | Already handled: 和 has a harmony or peace sense (repo/kanji/和.md:20-21). The overlap with 悠's calm sense is weak, but 悠 declares the direct pair, a conservative exclusion. |
| E2 | 息 | breath | 悠 | Card Notes rely on 休息, rest (snapshot/kanji/悠.md:46). | Already handled, though not semantically required: 息 card confirms the 休息 connection is compound-level and its title is breath (repo/kanji/息.md:20-22). A "breath" option is not a defensible answer for 悠, but 悠 declares the pair; this over-exclusion is harmless. |
| E3 | 凪 | calm seas; lull | 悠 | Calm overlap with 悠's calm/quiet sense (evidence/jmdict-families.xml:255-280). | Already handled: 凪 is a lull or calm at sea (repo/kanji/凪.md:23-26), which matches the Notes claim at snapshot/kanji/悠.md:45; 悠 declares the pair. |
| E4 | 寧 | polite; peaceful | 悠 | Peace/calm overlap (snapshot/kanji/悠.md:45). | Already handled and required: 寧 concerns calm, settled peace (repo/kanji/寧.md:23-28), overlapping 悠's quiet/calm sense; declared on 悠, not on 寧. |
| E5 | 楽 | music, enjoyment, ease | 悠 | Ease/comfort overlap with relaxed manner (snapshot/kanji/悠.md:46). | Already handled and required: 楽 らく means ease or comfortable (repo/kanji/楽.md:20), overlapping Daijisen's relaxed-mood sense (evidence/external-snapshots/01-extract.txt:8); declared on 悠. |
| E6 | 遠 | far | 悠 | Direct overlap with title "distant" (snapshot/kanji/悠.md:3). | Already handled and required: 遠 describes distance (repo/kanji/遠.md:20-21), and 遠い glosses include distant and remote in time (evidence/jmdict-families.xml:316-330); declared on 悠. |
| E7 | 久 | a long time | 悠 | KANJIDIC2 gives 悠 "long time" (evidence/kanjidic2-records.xml:54). | Already handled and required: 久 points to a long stretch of time (repo/kanji/久.md:20); declared on 悠. |
| E8 | 永 | eternity; enduring duration | 悠 | 悠 eternal and permanence (evidence/jmdict-families.xml:255-280; evidence/kanjidic2-records.xml:52). | Already handled and required: 永 concerns eternity or permanence (repo/kanji/永.md:20); declared on 悠. |
| E9 | 広 | wide, spacious | 悠 | Card Notes link 広 to the boundless sense (snapshot/kanji/悠.md:46). | Already handled, conservative: 広 concerns width, space or spreading (repo/kanji/広.md:20), with only partial overlap with "boundless" extent; declared on 悠. |
| E10 | 遅 | late; slow | 悠 | Slowness overlap: 悠長 slow, leisurely (evidence/jmdict-families.xml:94-97). | Already handled: 遅 covers lateness and slowness (repo/kanji/遅.md:20-21); "slow" is plausibly confused with "leisurely", and 悠 declares the pair. |

## Per-card results
| Card | Correctness | Scoped coverage | Consistency/quiz safety | Comprehensibility | Evidence |
| --- | --- | --- | --- | --- | --- |
| 悠 | CLEAN | CLEAN | CLEAN | CLEAN | KANJIDIC2 record, JMdict 2844201/1605700/1540690/1662390, Daijisen extract senses 1-2, Joyo row, quiz-safety and reading-exposure logs, stroke JSON and shape evidence, D/E table; O1-O3 |

## Findings
None.

## Optional points
### O1: Optional defensive 悠/易 exclusion
- Facet: Consistency/quiz safety
- Severity: optional
- Confidence: medium
- Citations: snapshot/kanji/悠.md:23; snapshot/kanji/悠.md:14; evidence/jmdict-families.xml:140-146; repo/kanji/易.md:3
- Evidence: The card teaches that 悠々 expresses "doing something easily", and JMdict 1605700 gives easily/without difficulty. 悠 already excludes 楽 partly for ease, while 易 "easy" is not excluded. Character-level evidence for 悠 has no easy sense, so this is not a required pair.
- Suggestion: Optionally add 易 to 悠's quiz_exclusions so a learner who links 悠 with the taught 悠々 "easily" sense never sees "easy" as a competing option.

### O2: Name the two Weblio sources in the reading note
- Facet: Comprehensibility
- Severity: optional
- Confidence: high
- Citations: snapshot/kanji/悠.md:43; evidence/external-snapshots/01-extract.txt:6; evidence/external-snapshots/01-extract.txt:9; evidence/external-snapshots/01-extract.txt:94
- Evidence: とおい and はるか appear in the 漢字辞典 section; Daijisen gives only はるか as kun, plus the name readings ちか, ひさ and ひさし. The note's "The character dictionary ... Its Daijisen entry" reads as if one source had a Daijisen entry.
- Suggestion: Write "Weblio's 漢字辞典 lists はるか and とおい; Digital Daijisen lists はるか and the name readings ちか, ひさ and ひさし".

### O3: Consider listing 悠長 among common words
- Facet: Scoped coverage
- Severity: optional
- Confidence: medium
- Citations: evidence/joyo-rows.json:10; evidence/jmdict-families.xml:78-99; snapshot/kanji/悠.md:37-39
- Evidence: The Joyo row gives 悠然, 悠長 and 悠々 as examples. 悠長 carries news2/spec2 priority markers and glosses leisurely, slow, deliberate, easygoing. The common-words list has 悠々, 悠久 and 悠遠 only.
- Suggestion: Optionally add 悠長 ゆうちょう (leisurely; slow; easygoing) as a recognition word for the leisurely sense.

## Limits
- L1: Execution-model identity is unverified. The runtime reports Claude Opus 5.5 (claude-opus-5.5), but this pass cannot independently verify that.
- L2: Not read (outside the permitted chain inputs): raw stroke SVG (kanji/060a0.svg), the raw Weblio response 01-response.html, the binary Joyo PDF, the N1 source snapshot list and every other packet asset outside the chains. The JLPT N1 label relies on the supplied sourceRow 367 (packet.json, source-metadata.json), not on a fresh list read. Joyo evidence is the cached text row, not a PDF-glyph check.
- L3: Stroke JSON was checked only for stroke count (11), KanjiVG revision and source attribution against the card and shape evidence. I made no visual geometry or stroke-order judgement.
- L4: Unread candidates I considered weaker and did not request: 余 (surplus; 余裕 room to spare), 冷 (cold; 冷静 composure), 簡 (simplicity), 漠 (vague; boundless desert), 凜 (dignified), 軽 (lightweight; 軽々 easily), 昔 and 古 (old times or old, versus distant in time). Their titles alone suggest low ambiguity, but their card texts were not read. Related characters 閑, 暇, 遥, 緩, 穏, 泰 and 徐 have no line in the 1242-line title index, so they have no card.
- L5: Reading audits are the supplied bounded Python model only. They do not cover custom or multi-borrow Starter pools, Kotlin execution, native or phone acceptance, or compatibility with the installed APK 5c000bd, which predates quiz_exclusions. Automated check logs are host/static evidence, not linguistic proof.
- L6: I reviewed the 悠々 word article only for the one link wrapper in diffs/existing.diff and its target. Its other existing content and its JLPT level were not re-reviewed because the diff does not change them.
- L7: D/E dispositions rest on the card texts and the supplied dictionary families. JMdict families for 易, 常, 遊, 優, 慢 and 快 were not supplied, so their secondary senses come from their cards only.

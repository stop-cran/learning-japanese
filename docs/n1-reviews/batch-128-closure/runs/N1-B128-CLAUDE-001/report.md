# B128 initial review — N1-B128-CLAUDE-001

## Overall verdict
Verdict: NEEDS FIX

## Facet verdicts
### Correctness
Verdict: CLEAN
Basis: Metadata, readings, compounds, spelling flags and the qualified source senses in snapshot/kanji/唇.md agree with the opened KANJIDIC2, JMdict, Joyo-row and Kotobank/Kanjipedia/Weblio extracts; the word-article edit removes a now-false statement and links the correct target. No incorrect claim was established.

### Scoped coverage
Verdict: CLEAN
Basis: The card covers the lip meaning, both readings with a justified curated selection, ordinary compounds, the rare 脣 spelling and the cited secondary senses; the omitted sourced phonetic-compound analysis is an optional expansion (O1), not a missing prerequisite.

### Consistency/quiz safety
Verdict: NEEDS FIX
Basis: The card guards 花 "flower" because of the cited flower-petal sense of くちびる, but leaves the direct 唇/咲 pair undeclared although 咲's displayed title "blossom; bloom" sits in the same flower-related answer space (F1). All other requested comparisons are handled or harmless.

### Comprehensibility
Verdict: CLEAN
Basis: Explanations are short, readings are given in kana, the mnemonic is explicitly labelled, and source-specific senses are qualified as lookup information rather than ordinary readings.

## Segments read
Core chain: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31 (each viewed once; no re-views)
Extension chain: 1, 2, 3, 4 (each viewed once; no re-views)
Title index evidence/title-index.txt source lines 1-1248 were read in full (core segments 25-26); line 1 is "一 one" and line 1248 is "齢 age; years lived".
repo/docs/content-format.md was read only for lines 1-139 as supplied.

## Phase-1 D/E lists
D: D1 咲, D2 声, D3 刃, D4 横, D5 片, D6 郊, D7 危, D8 話, D9 語, D10 歯, D11 響
E: E1 口, E2 花, E3 震, E4 辺, E5 畔, E6 音
Missing entries: none

## D/E cards read
| ID | Character | Displayed title | Related new card(s) | Reason | Disposition |
| --- | --- | --- | --- | --- | --- |
| D1 | 咲 | blossom; bloom | 唇 | Daijisen and Nikkoku record a flower-petal sense of くちびる (evidence/external-snapshots/02-extract.txt:16, :27); 咲 teaches flowers blooming (repo/kanji/咲.md:20) | Collision needing exclusion at the card's own standard: the 花 guard is justified by flower-related ambiguity (snapshot/kanji/唇.md:62-65) and 花 itself is glossed flower/blossom/bloom/petal (evidence/jmdict-families.xml:140-146); "blossom; bloom" is the same answer space. Not declared on either endpoint (snapshot/kanji/唇.md:14; repo/kanji/咲.md:1-12). See F1 |
| D2 | 声 | voice | 唇 | Nikkoku noun しん includes a labial speech sound (evidence/external-snapshots/02-extract.txt:29); 声 also has a linguistics "voiced sound" sense | Harmless: a labial consonant is a place of articulation, not a voice or voicing; the 唇 card itself limits the sound guard to the broad 音 label (snapshot/kanji/唇.md:79-81) and 声 card centres on voice of a speaker or animal (repo/kanji/声.md:20). Pair not declared; none needed |
| D3 | 刃 | blade; cutting edge | 唇 | Shared head word "edge" with the old-dictionary ホトリ gloss under variant 脣 (evidence/external-snapshots/02-extract.txt:64) whose JMdict family means side/edge/bank/shore of water | Harmless: "cutting edge" names the sharpened part of a blade (repo/kanji/刃.md:20), not a border or waterside; ホトリ is a variant-only historical gloss. Pair not declared; none needed |
| D4 | 横 | horizontal | 唇 | ホトリ side gloss vs 横's secondary noun sense "side of something" (repo/kanji/横.md:20) | Harmless: displayed label is "horizontal"; the lateral-side sense is not the waterside/edge sense of ほとり and neither is an ordinary meaning of 唇 (snapshot/kanji/唇.md:73-78). Pair not declared; none needed |
| D5 | 片 | one-sided; sheet | 唇 | Petal sense; 花片 is a rare petal spelling in the はなびら family | Harmless: 片 alone means one side or a thin piece (repo/kanji/片.md:20); the petal meaning belongs to the whole word 花片/はなびら, not to "one-sided; sheet". Pair not declared; none needed |
| D6 | 郊 | outskirts; suburbs | 唇 | ホトリ vicinity-type gloss | Harmless: ほとり glosses are side/edge/bank/shore of a waterbody (repo/kanji/辺.md:20), not suburbs; 郊 concerns a town's outskirts (repo/kanji/郊.md:20). Pair not declared; none needed |
| D7 | 危 | danger | 唇 | Jitsu おどろく surprise/fright sense (evidence/external-snapshots/02-extract.txt:61); KANJIDIC2 lists "fear" for 危 | Harmless: displayed "danger" and the card's teaching (repo/kanji/危.md:20-21) describe hazard, not being startled; the fear-type labels 恐/怖 are already guarded on 唇. Pair not declared; none needed |
| D8 | 話 | talk, speak | 唇 | Lips as a speech organ | Harmless: no opened evidence gives 唇 a speaking/talk sense; the 口 family has speech senses but 唇 (evidence/jmdict-families.xml) and the card do not; 話 card teaches talking (repo/kanji/話.md:22). Pair not declared; none needed |
| D9 | 語 | language, word | 唇 | Lips as a speech organ; labial speech sound | Harmless: 語 means word/language (repo/kanji/語.md:20-21); a labial sound is not a word or language. Pair not declared; none needed |
| D10 | 歯 | tooth | 唇 | Adjacent mouth part; 唇歯 "lips and teeth" | Harmless: distinct body part (repo/kanji/歯.md:19); 唇歯 pairs the two rather than equating them. Pair not declared; none needed |
| D11 | 響 | resound; echo | 唇 | Labial speech-sound sense vs sound-family titles | Harmless: 響 concerns sound resounding or carrying (repo/kanji/響.md:21-23), not a speech sound produced by the lips. Pair not declared; none needed |
| E1 | 口 | mouth | 唇 | 唇 is the lips around the mouth; 口 card lists openings and speech uses (repo/kanji/口.md:19-21) | Already handled: lips are part of the mouth, so "mouth" is defensible for 唇; direct exclusion declared on 唇 (snapshot/kanji/唇.md:14), not on 口 |
| E2 | 花 | flower | 唇 | Petal sense of くちびる; 花 card says it also means blossom (repo/kanji/花.md:22) | Already handled: declared on 唇 (snapshot/kanji/唇.md:14); supports F1 parity because 花's own teaching includes "blossom" |
| E3 | 震 | quake; tremble | 唇 | Kanjipedia's 口をふるわせておどろく account (evidence/external-snapshots/01-extract.txt:28); 震 teaches trembling (repo/kanji/震.md:20) | Already handled: declared on 唇 (snapshot/kanji/唇.md:14); latent ふるえる reading key is not drawable per checks/reading-exposure.txt:21-23 |
| E4 | 辺 | vicinity; edge | 唇 | ホトリ gloss; 辺 has ほと.り and teaches side/bank/shore (repo/kanji/辺.md:20, :30) | Already handled: declared on 唇 (snapshot/kanji/唇.md:14); latent ほとり key not drawable per checks/reading-exposure.txt:17-19 |
| E5 | 畔 | paddy boundary; waterside | 唇 | ホトリ waterside; 畔 lists ほとり (repo/kanji/畔.md:10, :32) | Already handled: "waterside" overlaps the ホトリ gloss; declared on 唇 (snapshot/kanji/唇.md:14), not on 畔 |
| E6 | 音 | sound | 唇 | Nikkoku しん labial speech sound; 音 card includes speech sound (repo/kanji/音.md:19) | Already handled: declared on 唇 (snapshot/kanji/唇.md:14), not on 音 |

## Per-card results
| Card | Correctness | Scoped coverage | Consistency/quiz safety | Comprehensibility | Evidence |
| --- | --- | --- | --- | --- | --- |
| 唇 | CLEAN | CLEAN | NEEDS FIX | CLEAN | KANJIDIC2 and source-metadata match frontmatter; JMdict 1359940, 1276410, 1576940, 1580410; Joyo row; Kotobank, Kanjipedia and Weblio extracts; strokes JSON 10 strokes; C distractors 古 old, 右 right, 石 stone have no semantic or reading overlap; F1; O1 |

## Findings
### F1: Undeclared 唇/咲 pair despite the petal-based 花 guard
- Facet: Consistency/quiz safety
- Severity: low
- Confidence: medium
- Citations: snapshot/kanji/唇.md:14; snapshot/kanji/唇.md:62-65; evidence/external-snapshots/02-extract.txt:16; evidence/external-snapshots/02-extract.txt:27; repo/kanji/咲.md:3; repo/kanji/咲.md:20; repo/kanji/花.md:22; evidence/jmdict-families.xml:140-146
- Evidence: The card teaches a flower-petal sense of くちびる and declares 花 "flower" a guarded comparison, "not a reliably wrong flower-related choice". 花 is itself taught and glossed as flower/blossom/bloom/petal. 咲's displayed title "blossom; bloom" names the same flower-related answer space, yet neither 唇 nor 咲 declares the direct pair. Exclusions are not transitive, so the 唇/花 guard does not cover 咲. Curated choices currently fill all slots (checks/reading-exposure.txt), so exposure is limited to fallback/custom pools, but the semantic ambiguity is the same one the 花 guard addresses.
- Required change: Add 咲 to 唇's quiz_exclusions (and mention it with the 花 note), or document positive evidence for treating "blossom; bloom" as reliably wrong while "flower" is not.

## Optional points
### O1: Sourced phonetic-compound analysis is cited but not taught
- Facet: Scoped coverage
- Severity: optional
- Confidence: medium
- Citations: snapshot/kanji/唇.md:5; snapshot/kanji/唇.md:29-32; evidence/external-snapshots/01-extract.txt:28; evidence/external-snapshots/02-extract.txt:58-59; evidence/shape-evidence.json:19-24
- Evidence: The card tags structure-unclassified and calls its 辰 mnemonic not an account of the sound component, while both cited character sources classify 唇 as 形声 with 辰 (シン) as the sound element, and KanjiVG marks 辰 as phon. The hedge is not false, but the card cites these sources for other senses without reporting their agreed structural analysis.
- Suggestion: Optionally state, with attribution, that Kanjipedia (Kadokawa Shinjigen) and Jitsu analyse 唇 as a phonetic compound of 口 with sound element 辰, adjusting the tag/phonetic fields if the editorial standard accepts this as established; keep the mnemonic labelled.

## Limits
- L1: Raw stroke SVGs, raw HTML responses, the binary Joyo PDF and every packet asset outside the two chains were not read; stroke JSON was checked only against card, KANJIDIC2 and shape-evidence text (10 strokes, KanjiVG revision 70a0b7ae), with no visual geometry claim.
- L2: Identified but unread candidates (not requested): 鳴 "animal call; ring" (sound family), 末 "end; tip" and 隅 "corner; nook" (edge-type labels), 葉 "leaf" (petal-adjacent), 紅 "crimson; deep red" (紅唇), 顔 "face; expression". Their dispositions are unassessed; I judge them low-likelihood from titles only.
- L3: Shape-evidence shows the variant 脣 (U+8123) is absent from all three bundled fonts; rendering of 脣 in the card's Notes and the word article on device is unverified.
- L4: Reading-exposure and quiz-safety logs model bounded host pools only; custom/caller-built pools, multi-borrow Starter behaviour, Kotlin execution, native/phone acceptance and compatibility with installed APK 5c000bd (which predates quiz_exclusions) are not established.
- L5: Execution-model identity is unverified; the runtime reports Claude Opus 5.5, which I cannot independently confirm.
- L6: repo/words articles other than the changed 唇 article (e.g. linked 口紅.md) and the full word corpus were not available; only the declared one-line prose removal and link were checked against diffs/existing.diff and the complete changed article.
- L7: The "literary" characterisation of the petal sense rests on classical poetic examples in the Daijisen and Nikkoku extracts; neither extract labels the sense with an explicit register tag.

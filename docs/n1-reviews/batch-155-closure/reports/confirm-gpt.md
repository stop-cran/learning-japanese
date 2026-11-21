Snapshot: 25609582e7d44eed71b10b3fe8ab7e9a5a3931e9, compared with 97c49eb27abbd2961ed93de7c67ece0fa53b5c8a. Reviewer: OpenAI GPT-family model; the exact deployed model/version is not exposed to this session.

Scope:

- Read confirmation `INSTRUCTIONS.md`, `CHANGES.md`, `RESPONSE.md`, `diffs\fix.patch`, `diffs\changed-lines.txt`, `evidence\README.md` and `evidence\exclusion-proofs.md` completely. Read all six revised `snapshot\kanji\` cards completely: 卑, 汰, 沙, 沢, 胡 and 鼓.
- Read my initial report and the original packet's complete `rubric\copilot-instructions.md`. Compared each original card with its revision; independently reconstructed all six revised files from the supplied patch in memory. All six SHA-256 values and Git blob identities match the confirmation manifest. Independently verified that every moved meaning paragraph and Notes passage occurs unchanged in `exclusion-proofs.md`.
- Read all three requested quiz audits and `checks\link-targets.tsv` completely. Read the complete `QuizBuilder.kt` and `KanjiMeaningMetadata.kt`, `KanjiReadings.kt:1–210` including the complete question builder, and `Words.kt:216–240` covering reading mutations.
- Inspected spelling, reading, restriction, register and sense fields for all 45 entries in `evidence\jmdict-cited-entries.xml`. From the original packet, inspected all six applicable KANJIDIC2 records' Japanese readings, English meanings, name readings, grade and stroke counts; read `joyo-pages.md`, `kanjipedia-senses.txt`, `kanjipedia-outside-readings.json`, `daijisen-heads.txt` and all six supplied Digital Daijisen extracts completely.
- Independently fetched and inspected the actual six linked Kanjipedia entries. Read the original 底 and 漠 cards completely, the 18 curated distractors' relevant front matter, and the actual titles of every retained exclusion target. Read the confirmation manifest, metadata scan and bounded lint, validation and unit-test summaries.
- Considered every changed hunk against correctness, scoped coverage, consistency/quiz safety and beginner comprehensibility. Unchanged word articles and stroke geometry were not re-reviewed in this confirmation.

Dispositions:

G1 - RESOLVED - `卑.md:14,45–52` removes 底 and correctly changes the count to eleven. 底's “bottom; base” is a physical noun; 卑's “lowly; despicable” concerns status or character. Neither displayed title becomes a correct answer for the other character. The original 底 card confirms the physical reading. Omitting the optional learner contrast does not leave the finding unresolved; the distinction remains in the editorial evidence.

G2 - RESOLVED - `沙.md:14,47,49–56` removes 漠, correctly counts nine exclusions and retains an accurate material-versus-region contrast. JMdict 1593800 actually marks 沙漠 as a rarely used kanji form of 砂漠, with reading さばく and gloss “desert”; the supplied Daijisen entry places 沙漠 under 沙's sand sense. Neither “sand; sift” nor “desert; vague” is a correct answer for the other character merely because 沙漠 is a word.

G3 - RESOLVED - All six line-23 paragraphs now explain the character principally in English, and the Notes use concise grouped reasons instead of repeating source-by-source proofs and entry IDs. The moved passages really are preserved off-card. Each teaching core retains an explicit meaning, qualified modern-shape mnemonic, reading table, kana-supported common word and clear quiz-reading selection. The remaining reference material does not establish a continuing actionable phone-level comprehensibility defect.

Verdicts:

- Correctness: CLEAN — 卑, 汰, 沙, 沢, 胡, 鼓; no differing card.
- Scoped coverage: CLEAN — 卑, 汰, 沙, 沢, 胡, 鼓; no differing card.
- Consistency and quiz safety: CLEAN — 卑, 汰, 沙, 沢, 胡, 鼓 within the supplied snapshot and audited pools; limitations below.
- Comprehensibility: CLEAN — 卑, 汰, 沙, 沢, 胡, 鼓; no differing card.

Confirmation: CONFIRMED — G1, G2 and G3 are resolved; no new actionable defect established.

Findings: None.

The following records the substantive regression checks, not additional findings.

**Changed prose and source fidelity**

- 卑's low status/character, self-reference and near/familiar senses match Kanjipedia. The complete quoted 卑怯 senses, 卑近 gloss, humility comparison and shortened reading note match the cited evidence.
- 汰's sorting, washing away, muddy/unclean conduct and luxury/boasting senses are genuinely present in the character sources. The 淘汰 example and qualified selection/extraction glosses match JMdict; the revised 沙汰 line quotes its first JMdict sense, not a purported English gloss supplied by Joyo.
- 沙's sandy waterside and water-sifting senses match Kanjipedia. The source's 沙汰 example supports the character-sense illustration; it should not be read as a claim that every modern use of the whole word means literal sifting. The sand/rare-spelling contrast is accurate.
- 沢's added stream/valley explanation matches JMdict 1415850. Its moisture, abundance, blessing and brilliance senses match the character sources. The new 沼沢/泥沼 comparison does not imply that 泥沼 contains 沢.
- 胡's added long-life, old-person and question-word senses are present in Kanjipedia. 胡散臭い, 異民族 and archaic 乱り have the quoted senses and qualifications in JMdict.
- 鼓's hourglass-shaped drum description is supported by JMdict 1267900; its beating and encouragement senses match both character dictionaries. The complete 鼓舞 gloss and 小鼓 こつづみ “small hand drum” are supported. Removing the additional 小鼓 reading from this note does not falsely make こつづみ exclusive.

All quoted KANJIDIC2 meaning lists match the pinned records. The five cited Joyo rows support the stated readings and examples, including 沢's old form 澤. Revised Kanjipedia and Daijisen quotations/paraphrases agree with the inspected entries or supplied extracts. The revised wording does not add an unsupported frequency ranking. The retained JMdict IDs cover the cited lexical evidence; the removed IDs no longer support an explicitly retained gloss that requires them.

**Retained exclusions**

I checked all 64 declarations against the actual comparison titles, shortened reasons and source evidence. Each remains a defensible direct guard under the initial review's ordinary-secondary-sense standard, rather than a transitive exclusion:

| Target | Retained comparisons and supported reason |
|---|---|
| 卑 | 低/下/劣: low or inferior; 汚/悪: dirty/vile; 謙: humility; 凡/近: common/near; 粗/貧: coarse or poor-looking; 軽: looking down on/making light of. |
| 汰 | 択/選: selection; 洗/濯: washing; 捨/除: elimination; 抜/抽: picking/extracting; 濁/汚: muddy or unclean; 誇: boasting. |
| 沙 | 砂: sand; 岸: waterside ground; 粒/石: fine stone particles; 汰: sifting; 択/選: sorting; 洗/濯: washing. |
| 沢 | 湿/泥: moisture or marsh/mire; 谷/川: valley/stream; 富/豊/裕/多: abundance; 恵/恩: blessing/favor; 艶/光/輝: gloss/brilliance. |
| 胡 | 外/異/洋: foreignness; 怪/嫌/疑: suspicion; 何: what; 乱: disregard for order; 長/老: long life/old age; 蝶: the specifically attested 胡蝶 use. |
| 鼓 | 打/撃/拍: striking/beating; 脈: pulsation; 励/勧/奨: encouragement; 激/扇: rousing/inciting. |

These are not claims that the complete titles or compounds are interchangeable. In particular, the 胡/蝶 comparison has Daijisen's explicit 胡/蝴 interchangeability evidence; it is not justified merely by transferring an arbitrary compound's meaning to its first character. The new short reasons do not contradict that evidence. Counts are 11/11/9/13/11/9; no declared exclusion is also its card's curated distractor. 沙 still protects the 汰/沙 pair through the builder's symmetric exclusion rule.

**Meaning and reading options**

`QuizBuilder.options` prefers available curated cards, rejects exclusions in either direction, also checks exclusions between wrong options, and deduplicates titles before tag-ranked fallback. Distinct strings alone do not prove semantic safety. I independently assessed the displayed choices:

| Target and correct meaning | Wrong meaning choices | On-reading question and wrong readings |
|---|---|---|
| 卑 — lowly; despicable | courage; bravery / wise; intelligent / sharp; keen | ヒ: ユウ, ケン, エイ |
| 汰 — sift; weed out | sew; stitch / polish; grind / paint; coat | タ: ホウ, マ, ト |
| 沙 — sand; sift | iron / copper / salt | サ: テツ, ドウ, エン |
| 沢 — marsh; luster | frost / rock; boulder / hill; knoll | タク: ガン, キュウ, plus one top-tier fallback |
| 胡 — foreign; dubious | sweet; pamper / soft; supple / quiet | コ: カン, one of ジュウ/ニュウ, one of セイ/ジョウ |
| 鼓 — drum; rouse | flute; whistle / koto; zither / brush; writing | コ: ヒツ, plus two of コク/コツ/コン |

All 18 meaning distractors remain defensibly wrong: for example, polishing is not sifting, salt is not sand, and other musical instruments are not drums. Removing 底 and 漠 does not change these full-pool curated sets.

The actual distractor metadata explains the reading options: 霜, 笛 and 琴 have disabled on-reading quizzes and therefore supply no on-reading option. The reading builder protects all target on/kun metadata readings and their defined mutations, not only the selected prompt, then ranks fallback readings by kana/length closeness. None of the listed drawable alternatives is another attested reading of its target. All six cards select one on prompt and no kun prompts.

沢's unlisted name reading さ remains a latent collision: 作/再/左/差/査/沙/砂/茶 can supply it, but higher-ranked alternatives prevent it in the audited N1, All and Starter-padded pools. No reading metadata changed, and the supplied exposure accounting is consistent with the inspected builder. The two removed meaning exclusions do not control reading-option selection.

Optional: None.

Limits:

- CLEAN is a bounded confirmation, not exhaustive linguistic certification. I did not reopen another reviewer's report, inspect a checkout, scan the corpus, use another agent/session, start a background job or issue parallel tool calls. Every tool-using response contained exactly one call.
- Several combined reads exceeded the tool output cap. I did not open generated spill files; the necessary material was subsequently obtained through bounded reads or selected structured fields. One inline XML inspection initially failed on the console encoding and was rerun successfully with UTF-8. No helper script or temporary file was intentionally created.
- Joyo and Daijisen verification used the supplied source extracts; I did not independently download the complete official PDF or re-fetch every Daijisen page. Kanjipedia was independently fetched for all six characters. Supplied source hashes were not treated as proof of interpretation.
- I inspected the real option-building source and supplied audits, but did not execute Kotlin, rebuild the shipped pools or independently rerun the audit programs. Seed samples alone are not exhaustive proofs; abbreviated fallback lists do not expose every holder. The audits cannot establish semantic correctness, dictionary completeness, arbitrary reduced/future-pool safety, or actual phone readability. They do not eliminate 沢's disclosed hypothetical small-pool collision.
- `link-targets.tsv` reports its quoted-gloss equality fields as `n/a`; its zero-problem summary alone therefore cannot establish quotation accuracy. I checked the relevant actual titles independently.
- No APK/device rendering or Android/JVM tests were performed. Unchanged word articles, strokes and out-of-scope corpus material retain the initial review's scope and limitations; this report does not claim a fresh full-batch geometry or corpus audit. The sole intentional write is this report.

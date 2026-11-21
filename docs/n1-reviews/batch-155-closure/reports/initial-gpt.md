Snapshot: 97c49eb27abbd2961ed93de7c67ece0fa53b5c8a, batch 155. Reviewer: OpenAI GPT-family model; the exact deployed model/version is not exposed to this session. Independently calculated packet-manifest SHA-256: `669b1560dfc0756df69c98a6ecb1e938ef69d37bbeb049ab0fbc6a4a97e9d1aa`, matching the assignment.

Scope:

All four facets were considered for every new card, with consistency/quiz safety and phone-level comprehensibility examined deepest. The six word changes and all six stroke files were also reviewed. Paths below are relative to the supplied packet; grouped filenames share the stated directory.

**Read in full:**

- `INSTRUCTIONS.md`; `mechanical-checks.md` (both requested line ranges).
- `snapshot\kanji\卑.md`, `snapshot\kanji\汰.md`, `snapshot\kanji\沙.md`, `snapshot\kanji\沢.md`, `snapshot\kanji\胡.md`, `snapshot\kanji\鼓.md`.
- `snapshot\words\卑怯.md`, `snapshot\words\太鼓.md`, `snapshot\words\御無沙汰.md`, `snapshot\words\無沙汰.md`, `snapshot\words\胡椒.md`, `snapshot\words\贅沢.md`.
- `diffs\words__卑怯.md.diff`, `diffs\words__太鼓.md.diff`, `diffs\words__御無沙汰.md.diff`, `diffs\words__無沙汰.md.diff`, `diffs\words__胡椒.md.diff`, `diffs\words__贅沢.md.diff`.
- `evidence\source-metadata.json`; `evidence\provenance.json`; `evidence\joyo-pages.md`; `evidence\kanjipedia-senses.txt`; `evidence\kanjipedia-outside-readings.json`; `evidence\daijisen-heads.txt`; `evidence\okurigana-scan.txt`; `evidence\kanjivg-components.txt`.
- `evidence\public-source\weblio-卑.txt`, `weblio-汰.txt`, `weblio-沙.txt`, `weblio-沢.txt`, `weblio-胡.txt`, `weblio-鼓.txt`.
- `evidence\audits\quiz-safety.txt`; `evidence\audits\reading-exposure.txt`; `evidence\audits\reading-options.txt`; `evidence\audits\extra-readings.json`; `evidence\audits\word-remarks.json`; `evidence\audits\kanji-remarks.json`.
- `evidence\app-code\QuizBuilder.kt`; `evidence\app-code\KanjiMeaningMetadata.kt`.
- Context cards `repo\kanji\慢.md`, `底.md`, `石.md`, `粒.md`, `漠.md`, `虚.md`.

**Read completely by structured parsing, with the indicated inspection:**

- `snapshot\strokes\卑.json`, `汰.json`, `沙.json`, `沢.json`, `胡.json`, `鼓.json`: every field and all 832 coordinate pairs checked; all 52 ordered strokes compared with the pinned SVG paths.
- `evidence\kanjivg-svgs.txt`: all six SVG documents parsed and every stroke path inspected; component annotations checked against the component report. Not every license/comment line was manually read.

**Read/reviewed in part:**

- `packet-manifest.json`: first 22 lines; complete bytes hashed.
- `rubric\copilot-instructions.md`: lines 1–200.
- `repo\docs\content-format.md`: lines 86–161 and 289–313, plus targeted matches concerning headings and quiz fields.
- `repo\docs\confusable-words.md`: lines 1–90.
- `evidence\app-code\KanjiReadings.kt`: lines 1–210, including the complete option builder.
- `evidence\kanjidic2-records.xml`: complete records for the six new characters; other character records not substantively reviewed.
- `evidence\jmdict-families.xml`: spelling, reading, restriction, register and sense fields for every entry listed on the six cards' Metadata lines, plus entries 1482840, 1584980, 2450760 and 2450770. Other families were not comprehensively reviewed.
- `evidence\jmdict-digest.tsv`: header/initial rows and all priority-tagged rows for these six characters.
- `titles\kanji-titles.tsv`: initial rows, targeted semantic searches, exact title/identity lookups for every new card, distractor, exclusion, mnemonic component and supplied non-excluded comparison. `titles\word-titles.tsv`: initial rows and exact linked-word/identity lookups. The indexes were parsed, not every row linguistically reviewed.
- Front matter only in these `repo\kanji\` files: `勇.md`, `賢.md`, `鋭.md`, `縫.md`, `磨.md`, `塗.md`, `鉄.md`, `銅.md`, `塩.md`, `霜.md`, `岩.md`, `丘.md`, `甘.md`, `柔.md`, `静.md`, `笛.md`, `琴.md`, `筆.md`, `低.md`, `下.md`, `近.md`, `軽.md`, `選.md`, `洗.md`, `抜.md`, `濁.md`, `誇.md`, `疑.md`, `何.md`, `乱.md`, `長.md`, `湿.md`.

**Independent public verification:** inspected the actual six linked Kanjipedia entries and the six corresponding Digital Daijisen entries on Weblio, plus Daijisen entries for 底, 漠, 慢 and 採. Inspected Jisho's 卑怯 entry and 沢 kanji page, and actual Jisho API entries for 卑劣, 卑しい, 卑しむ, 卑しめる, 無沙汰, 御無沙汰, 淘汰, 淘げる, 沙門, 砂, 贅沢, 光沢, 沢, 胡椒, 胡, 胡散, 胡散臭い, 胡麻, 鼓, 小鼓, 太鼓 and 鼓動. These were entry inspections, not search-snippet evidence.

Verdicts:

- Correctness: **CLEAN** within the reviewed evidence and stated limits.
- Scoped coverage: **CLEAN**.
- Consistency and quiz safety: **NEEDS FIX** — the over-exclusions in G1–G2; no actually drawable incorrect reading answer was established.
- Comprehensibility: **NEEDS FIX** — G3 affects all six cards.

| Card | Correctness | Scoped coverage | Consistency / quiz safety | Comprehensibility |
|---|---|---|---|---|
| 卑 | CLEAN | CLEAN | NEEDS FIX — G1 | NEEDS FIX — G3 |
| 汰 | CLEAN | CLEAN | CLEAN | NEEDS FIX — G3 |
| 沙 | CLEAN | CLEAN | NEEDS FIX — G2 | NEEDS FIX — G3 |
| 沢 | CLEAN | CLEAN | CLEAN | NEEDS FIX — G3 |
| 胡 | CLEAN | CLEAN | CLEAN | NEEDS FIX — G3 |
| 鼓 | CLEAN | CLEAN | CLEAN | NEEDS FIX — G3 |

**Correctness and coverage observations**

- **卑:** metadata matches the pinned record. All four reading rows, the outside-table ひくい note, the four Kanjipedia senses and the comparison with Daijisen check out. 卑怯's two senses and the other cited word senses are correctly represented. The selected ヒ is supported by linked 卑怯.
- **汰:** metadata, including タイ and the three kun readings, matches. The source-only qualifications correctly distinguish character-dictionary recognition from checked JMdict examples. 淘げる does not establish a 汰 spelling. The にごる and おごる/ほこる senses and KANJIDIC2's “luxury” are genuinely sourced. Linked 無沙汰 and 御無沙汰 support タ.
- **沙:** サ, シャ, すな, よなげる and the additional いさご row have the claimed support. JMdict permits both readings of 沙門, and permits 沙 with すな and いさご; its すな restriction is correctly described. The Sanskrit-transcription explanation and the outside-table みぎわ note are supported. Linked contact expressions support サ.
- **沢:** metadata and all five rows check out. The qualifications concerning 潤い, 潤す and 艶 correctly avoid presenting those entries as 沢 spellings. The stream/valley, abundance, blessing and luster senses are supported; standalone たく is correctly marked archaic. 贅沢 supports タク.
- **胡:** the three on readings, source-only なんぞ and additional Kanjipedia readings are accurately separated from quiz selection. 胡椒 and 胡麻 have the claimed kana preference; standalone 胡 こ is historical. The non-Joyo, 人名用漢字 and grade-9 statements are consistent with the sources. 胡椒 supports コ.
- **鼓:** コ and つづみ, the three character senses, both readings of 小鼓 and the 皷 variant note check out. 太鼓 supports コ. No kun reading is selected for questions.

Every metadata reading is covered or explicitly qualified. Priority-family inspection did not establish a consequential common-word omission; this is not a request to add every family member. No new kanji card contains an example sentence requiring a separate sentence correction.

All six mnemonics explicitly identify themselves as modern-shape mnemonics, not etymology. Their component positions and stroke statements match the pinned evidence, including 卑's two separate 丿 strokes, 太's bottom dot, 少's final 丿, 胡's 肉-derived 月 shape, and 鼓's overlapping 士/豆 analysis. Quoted component-card titles match after allowing ordinary sentence punctuation. Dense cubic-path resampling put every stored stroke point within 0.071 SVG units of the expected arc-length sample.

**Meaning options and exclusions**

I assessed each listed distractor against both the new character and the distractor's displayed title/ordinary meanings:

| Target | Actual curated meaning choices | Assessment |
|---|---|---|
| 卑 | courage; bravery / wise; intelligent / sharp; keen | All defensibly wrong; sharpness does not mean moral baseness. |
| 汰 | sew; stitch / polish; grind / paint; coat | All defensibly wrong; grinding/refining is not sifting or selecting. |
| 沙 | iron / copper / salt | All defensibly wrong; granular salt is not sand. |
| 沢 | frost / rock; boulder / hill; knoll | All defensibly wrong; neither shiny rock nor a wet/frosted landscape makes these equivalent meanings. |
| 胡 | sweet; pamper / soft; supple / quiet | Broadly related as qualities but semantically distinct. |
| 鼓 | flute; whistle / koto; zither / brush; writing | The instrument distinctions are sound; neither flute nor koto means drum. |

These are introductory recognition choices, not uniformly difficult contrasts, but no set was established to be educationally worthless.

I would retain the other supplied exclusions as conservative direct guards, rather than infer a transitive clique. In particular, the dictionary-supported secondary senses explain the less obvious 下, 凡, 貧, 近, 軽; 抜, 抽, 濁, 汚, 誇; 岸 and the sorting/washing pairs; 谷, 川, 多, 恵, 恩, 光, 輝; 洋, 嫌, 何, 乱, 長, 老, 蝶; and 撃, 拍, 脈, 激, 扇 comparisons. This does not make the paired characters interchangeable in compounds.

The sibling 汰/沙 pair is correctly protected on 沙 alone. 沢/沙 is a terrain association, not the same displayed answer; 卑/胡 shares unfavorable evaluation, not a meaning; and 汰's secondary “luxury” does not make “marsh; luster” a second correct displayed answer. I established no required missing exclusion among the supplied non-excluded comparisons: opposites, related substances/landforms, suspicion versus falsity, and producing sound versus playing/rousing are not automatically synonyms.

**Reading options and audit accounting**

- 卑 ヒ displays wrong readings ユウ, ケン and エイ.
- 汰 タ uses ホウ, マ and ト.
- 沙 サ uses テツ, ドウ and エン.
- 沢 タク uses ガン and キュウ, plus one higher-closeness fallback.
- 胡 コ uses カン, one of ジュウ/ニュウ, and one of セイ/ジョウ.
- 鼓 コ uses ヒツ plus two of コク, コツ and コン.

The curated cards' own usable reading selections do not introduce a correct alternative. 霜's disabled on quiz and 笛/琴's disabled on quizzes explain the respective fallback slots; they are not missing-reading defects in this batch.

The two complete audits are consistent with the option-builder code: full target on/kun lists are protected, even when only one reading is quizzed. Their reported zero production hits, zero padded-session hits, one latent collision and zero one-holder hits are not contradictory. 沢's name reading さ is offered by the eight named holder cards, but is a lower-closeness candidate than the fallback tier actually reached in the audited pools. The new 沙 therefore does not establish a production collision.

The okurigana extras appear in the actual audit commands, although they are not stored in `extra-readings.json` itself. Treat ひわい from 卑わい and こす/こする from 鼓す/鼓する as conservative lexical scan candidates, not newly established kun readings of the bare character. Their inclusion produces no reported collision and does not justify adding those forms to the teaching tables.

**Word changes and stroke files**

All six word diffs contain exactly one removed and one added line. Removing the link markup reproduces the old line exactly, except for the one declared 無沙汰 remark replacement. The eight added links point to the intended cards. No Dictionary line changes.

- 卑怯: 卑 link and surrounding low/base association remain correct.
- 太鼓: 鼓 link and drum association remain correct.
- 胡椒: 胡 link preserves the historical foreign/non-Han association.
- 贅沢: 沢 link preserves its abundance/richness association and タク explanation.
- 無沙汰: both links are correct; “無 does not have a card yet” matches the declared edit and exact-path/index checks.
- 御無沙汰: both links are correct. Its unchanged full-spelling sentence remains true; 無 still lacks a card.

The six changed passages are **CLEAN across the four facets within their one-line scope**. The pre-existing JMdict-line warnings do not establish an in-scope defect. All six stroke files are **CLEAN for the reviewed identity, source revision, stroke order/type and coordinate geometry**.

Findings:

1. **G1 — minor; consistency and quiz safety; `snapshot\kanji\卑.md:14,53`.**
   **Claim and impact:** the 卑/底 exclusion is justified solely by the English spelling “base.” Here 卑 is morally low/base, whereas 底's displayed “bottom; base” is a noun for a bottom/foundation. In either direction these are defensibly different answers. Suppressing the pair on a false-friend gloss match is not a direct semantic ambiguity and misses an opportunity to explain the distinction.
   **Remedy:** remove 底 from this exclusion list and replace/remove the exclusion rationale; update the stated count. A short contrast between moral baseness and a physical base would be useful.
   **Evidence:** the bullet itself supplies only the shared English word. `repo\kanji\底.md:20,28–29` identifies the physical noun. [Daijisen 卑](https://www.weblio.jp/content/%E5%8D%91) gives low status/inferior character, while [Daijisen 底](https://www.weblio.jp/content/%E5%BA%95) begins 物のいちばん下 and distinguishes physical bottoms/depths. The format contract requires evidence about displayed labels and ordinary meanings, not a shared gloss string.
   **Confidence:** high.

2. **G2 — minor; consistency and quiz safety; `snapshot\kanji\沙.md:14,51`.**
   **Claim and impact:** the 沙/漠 exclusion transfers the meaning of the complete word 沙漠, “desert,” onto 沙. The cited character sense actually identifies 沙 as sand, not a desert; 漠's displayed “desert; vague” denotes a region/indistinctness, not the material sand or sifting. Neither direction creates two defensible answers merely because the characters can form this compound.
   **Remedy:** remove 漠 from the exclusion list and change the paragraph to a material-versus-region contrast; update the stated count. Preserve the useful rare-spelling information if desired.
   **Evidence:** JMdict 1593800 supports 沙漠 as a spelling of the complete word, not a desert sense of 沙. [Daijisen 沙](https://www.weblio.jp/content/%E6%B2%99) puts 沙漠 under すな; [Daijisen 漠](https://www.weblio.jp/content/%E6%BC%A0) defines its first sense as 広い砂原. `repo\kanji\漠.md:56–58` already explains the material/region distinction.
   **Confidence:** high about the linguistic distinction; medium-high about the exclusion-policy application.

3. **G3 — minor; comprehensibility; all six `snapshot\kanji\` cards: line 23 and Notes — 卑:40–60; 汰:42–60; 沙:42–58; 沢:41–58; 胡:40–59; 鼓:38–52.**
   **Claim and impact:** the learner-facing cards embed an editorial proof dossier. Each starts with an 82–121-token dictionary-comparison paragraph; the Notes then explain 9–13 excluded cards with repeated source names, entry IDs and Japanese definition fragments. Before the final Metadata line, the bodies run roughly 570–830 whitespace-separated tokens, with about half occupied by Notes. For the specified N5–N4 English-speaking phone reader, this obscures which meanings, words and readings to remember. This is a specific audience/structure problem, not an assertion that the underlying dictionary facts are wrong.
   **Remedy:** retain the central English explanation, honest mnemonic, reading table and a few practical, kana-supported contrasts. Move the exhaustive exclusion proofs/source reconciliation to editorial evidence; keep concise source links and only learner-useful rare-reading qualifications on the card. Do not remove the complete metadata or its safety protections.
   **Evidence:** all six inspected cards exhibit the same structure. For example, 卑's Notes alone contain about 486 space-separated tokens; 沢's contain about 452. Their long exclusion rationales teach the quiz configuration more than usable Japanese. The assignment explicitly requires no padding/wall of text and comprehensibility at N5–N4.
   **Confidence:** high that the presentation conflicts with the stated audience; the exact amount of shortening is editorial.

Optional: None beyond the remedies above. I do not recommend adding every dictionary family, making every distractor harder, or promoting source-only readings into quiz prompts.

Limits:

- Exact model/version and the other reviewer's model family were not independently observable. No other review, author rationale, checkout, session or agent was accessed.
- This was serial, read-only work, with one tool call per tool-using response; no parallel calls, subagents, background jobs, recursive listings or corpus-file scans. Only the title indexes were used for corpus-level checks. The sole intentional write is this report.
- Initial combined evidence/XML output and one web fetch exceeded the tool's output cap. I did not open generated spill files; the necessary evidence was subsequently obtained through bounded entry/field output or smaller fetches. Partial reads are identified in Scope.
- The public kanjiapi.dev requests returned HTTP 403. The pinned KANJIDIC2 records, live Kanjipedia entries and Jisho's 沢 kanji page supplied the relevant alternative verification. Live Jisho is an independently retrieved JMdict presentation, not an independent lexicographic tradition.
- I inspected all cited JMdict families, not every uncited family. I reviewed the supplied complete reading audits against the actual option-builder logic, but did not independently rebuild every shipped pool or execute the Python audit scripts/Kotlin implementation. The audit's abbreviated fallback lists are not a claim that I manually inspected every fallback holder card.
- No APK, device or phone rendering was tested. The packet's absent Android/JVM tests and Kotlin cross-check are known evidence limits, not findings. Reading-safety conclusions concern the supplied snapshot, compatible code and audited pools, not arbitrary future content or smaller hypothetical pools.
- CLEAN means no additional actionable defect was established within these bounds, not exhaustive verification of every possible dictionary sense or quiz pool.

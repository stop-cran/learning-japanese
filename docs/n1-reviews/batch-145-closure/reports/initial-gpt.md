Snapshot: 845aefbb37e40aeb737f32de8066959968cc2cf6 — batch 145.

Reviewer: ChatGPT, OpenAI. The exact runtime model/version identifier is not exposed to me.

Packet-manifest SHA-256 verified: `78b790f2d213e6de96ddb144054b6498864ea40caacb80cb8ae406579a96bd09`.

Scope:

Independent, blind, read-only review of all 15 new kanji cards, their 15 stroke files, all 20 modified word articles, and both existing-card edits. Facets 3 and 4 received the deepest examination. Paths below are relative to `C:\Users\romanko\n1-kanji-workspace\review-packets\batch-145-845aefbb`. Braced lists enumerate individual files, not folders scanned.

**Read in full:**

- `INSTRUCTIONS.md`; `mechanical-checks.md`; `rubric\copilot-instructions.md`.
- `snapshot\kanji\{湧,源,滅,滑,滞,漫,漬,潔,潜,澄,濁,瀬,災,炎,為,渋,暑}.md`.
- `snapshot\words\{不潔,清潔,渋滞,湧く,滅多に,滑る,滞在,漫画,漬ける,潜る,澄む,濁る,瀬戸物,火災,災難,炎,為す,為替,絶滅,資源}.md`.
- `diffs\words__{不潔,清潔,渋滞,湧く,滅多に,滑る,滞在,漫画,漬ける,潜る,澄む,濁る,瀬戸物,火災,災難,炎,為す,為替,絶滅,資源}.md.diff`; `diffs\kanji__渋.md.diff`; `diffs\kanji__暑.md.diff`.
- `evidence\source-metadata.json`; `evidence\provenance.json`; `evidence\joyo-pages.md`; `evidence\kanjipedia-outside-readings.json`; `evidence\daijisen-heads.txt`; `evidence\okurigana-scan.txt`.
- `evidence\public-source\weblio-{湧,源,滅,滑,滞,漫,漬,潔,潜,澄,濁,瀬,災,炎,為}.txt`.
- `evidence\audits\quiz-safety.txt`; `evidence\audits\reading-exposure.txt`; `evidence\audits\reading-options.txt`; `evidence\audits\kanji_remarks.py`; `evidence\audits\kanji-remarks.json`.
- `evidence\app-code\QuizBuilder.kt`; `evidence\app-code\KanjiMeaningMetadata.kt`.
- `snapshot\strokes\{湧,源,滅,滑,滞,漫,漬,潔,潜,澄,濁,瀬,災,炎,為}.json`: complete machine parsing and structural inspection, supplemented by comparison with the pinned public KanjiVG paths.

**Read/consulted in part:**

- `repo\docs\content-format.md`: kanji requirements, especially lines 86–154; stroke requirements, lines 289–304; heading/key matches elsewhere. Initial broader output was truncated.
- `repo\docs\confusable-words.md`: first 100 lines; an initial broader request was truncated.
- `evidence\app-code\KanjiReadings.kt`: lines 1–210.
- `evidence\kanjidic2-records.xml`: header and complete records for the 15 new kanji.
- `evidence\jmdict-families.xml`: header and complete selected entries cited by the 15 new cards, including their forms, readings, senses, restrictions and register labels; not every family in the file.
- `evidence\jmdict-digest.tsv`: header and relevant rows for the 15 kanji, including priority-tagged common-word leads.
- `titles\kanji-titles.tsv`: loaded the index to compare all declared exclusion titles, target-title uniqueness and possible shared-English-word collisions; did not manually read every row.
- `titles\word-titles.tsv`: header and relevant modified-word identity/reading rows.
- `packet-manifest.json`: bytes read for SHA-256 verification; manifest contents not reviewed.

**Independent public evidence:** inspected actual Weblio/Digital Daijisen character entries and Jisho kanji entries for all 15 kanji, not search snippets. Inspected the linked Kanjipedia entries for 滅, 滑, 漫, 漬, 潔, 潜, 濁, 瀬, 炎 and 為. Inspected actual Jisho dictionary API entries for all 20 modified words and additional consequential examples including 湧水, 湧出, 滑稽, 潔い, 浸漬, 滞る and 瀬. Additional Daijisen word-entry checks covered 漫歩, 散漫, 潜む, 澄ます, 災い, 為す, 滅ぼす, 滅ぶ, 漬物 and 為せる. Compared every stroke file with its character’s SVG at KanjiVG revision `70a0b7ae0c18ceb5cb358274b029cce0234a43bc`.

Verdicts:

- **Correctness: NEEDS FIX** — G1–G5.
- **Scoped coverage: CLEAN** — metadata readings are covered or expressly qualified; no consequential common-word omission established.
- **Consistency and quiz safety: NEEDS FIX** — stale cross-content assertions in G1 and G5. No actually drawable ambiguous meaning answer or attested-reading wrong answer established.
- **Comprehensibility: NEEDS FIX** — G6; the main ideas are generally clear, but several reading explanations retain reviewer-facing machinery.

Per-new-card verdicts follow. `C` means CLEAN; `F` means NEEDS FIX. Verdicts here concern the new card itself; modified-word and existing-card findings are listed separately below.

| Card | Correctness | Coverage | Consistency/quiz | Comprehensibility | Reviewed practice reading; curated distractors |
|---|---|---|---|---|---|
| 湧 | C | C | C | C | わく; 港 濃 漁 |
| 源 | C | C | C | C | ゲン; 漠 湿 港 |
| 滅 | C | C | C | C | メツ; 海 水 火 |
| 滑 | C | C | C | C | すべる; 湖 濃 涙 |
| 滞 | C | C | C | C | タイ; 漁 涼 湖 |
| 漫 | F: G2, G3 | C | C | F: G6 | マン; 海 水 日 |
| 漬 | C | C | C | F: G6 | つける; 責 漁 渡 |
| 潔 | C | C | C | C | ケツ; 漁 溶 渡 |
| 潜 | C | C | C | C | もぐる; 漁 溶 渡 |
| 澄 | C | C | C | C | すむ; 海 水 川 |
| 濁 | C | C | C | C | にごる; 触 渡 湯 |
| 瀬 | F: G4 | C | C | C | せ; 湯 湿 滴 |
| 災 | C | C | C | C | サイ; 巡 炊 灰 |
| 炎 | C | C | C | C | ほのお; 淡 談 炊 |
| 為 | C | C | C | F: G6 | なす; 黒 魚 火 |

For the modified existing content: `snapshot\words\湧く.md` needs correctness/consistency fixes under G1; `snapshot\kanji\暑.md` needs correctness/consistency fixes under G5. No additional actionable defect was established in the other 19 word articles or the changed 渋 passage. All 22 diffs have the declared mechanical extent: each word diff adds exactly one intended kanji link without changing the underlying sentence; the two existing-kanji diffs contain only their declared remark changes. Mechanical conformity does not resolve G1 or G5.

**Quiz-safety conclusions:**

- Examined every new card’s displayed title, curated distractors and exclusions in both directions. The visual/radical-based distractors are defensibly wrong, including the repeated 漁/渡/溶 group. The explicitly explained Starter choices are easy but safe. Title matches such as 湧’s “well up” versus 井’s noun “well,” and 漬’s “steep” versus 険’s adjective, do not establish alternate correct answers.
- Exclusions are symmetric in the implementation, not transitively expanded. The one-sided declarations covering 湧–源, 滑–滞, 漫–滑, 漬–潜 and 潔–澄 therefore work. No missing transitive clique should be added.
- Each selected quiz reading has an appropriate linked word example. Nonselected metadata readings are not incorrectly represented as quiz readings.
- The complete exposure audit accounts for ten latent collisions: 滅べつ; 滑かり; 漫ばん; 澄すみ and み; 瀬せい; 炎ぬく and もえる; 為す and た. It reports no production, padded-session or one-holder padded hit.
- The `reading-options.txt` HIT labels for 滅べつ/別 and 漫ばん/万・判・晩・板・満・番・盤 are not drawable wrong options in the reviewed pools: three usable Starter distractors already occupy the three slots. They must not be reported as production failures.
- Also checked the less obvious fallback cases. 滞 can lose a curated slot when 漁 and 涼 both contribute りょう; the audit includes the resulting fallback exposure. 炎 has only 炊 as a usable curated kun distractor, but its remaining slots are filled from closer-ranked keys; the attested もえる and ぬく collisions do not reach those slots in the reviewed pools.
- Independent metadata/link checks found no mismatched stroke count, grade tag, radical, on/kun list, duplicate target title or unresolved new-card local link. All stroke counts, source-path starts and ends matched; sampled points lay within approximately 0.24 viewBox units of a densely sampled pinned source path.

Findings:

**G1 — Minor; correctness and consistency — `snapshot\words\湧く.md:29–32`.**

The newly linked 湧 is immediately followed by “Neither character currently has a kanji card.” That is false at this snapshot and contradicts the working link two lines above. Although the stale sentence predates the link-wrap, the assignment explicitly includes the truth and coherence of the remaining passage.

**Remedy:** declare and make the necessary remark correction, for example: “湧 has a kanji card; the rare alternate 涌 is not taught here.” Preserve the accurate written-kanji metadata explanation without asserting that 湧 lacks a card.

**Evidence:** the complete article, its one-line diff and `snapshot\kanji\湧.md`. **Confidence: high.**

**G2 — Minor; correctness — `snapshot\kanji\漫.md:46`.**

“Daijisen’s entry also lists すず and そぞろ as kun readings” truncates the first reading. The actual character entry prints **すずろ**, not すず. Weblio links the substring すず and leaves ろ outside that hyperlink; an HTML/text-extraction boundary must not be treated as a reading boundary.

**Remedy:** replace すず with すずろ. Do not add a standalone すず reading on this evidence.

**Evidence:** independently inspected [Digital Daijisen, 漫](https://www.weblio.jp/content/漫), whose kun-reading line is `すずろ　そぞろ`; the same paragraph already correctly mentions the obsolete form すずろ. **Confidence: high.**

**G3 — Minor; correctness — `snapshot\kanji\漫.md:44`.**

The phrase “the small ん in まんぽ and まんだん” is incorrect. Both spellings use ordinary full-sized ん. Calling it small teaches the wrong kana category, particularly to a beginner familiar with small っ or ゃ.

**Remedy:** remove “small”; if explanation is needed, say that ん is the final mora of マン.

**Evidence:** the printed spellings and the actual 漫歩/漫談 dictionary readings, まんぽ and まんだん. **Confidence: high.**

**G4 — Minor; correctness — `snapshot\kanji\瀬.md:27`.**

The mnemonic describes the entire right-hand part of 瀬 as a shape that “also stands at the right of 頼.” The whole right-hand component of 瀬 is **頼** itself. The right-hand component of 頼 is **頁**. As written, the sentence conflates those two component levels and gives a misleading visual instruction.

**Remedy:** write “The whole right-hand part is 頼,” or explicitly identify 頁 as the shared far-right subcomponent if that is the intended comparison. Keep the modern-shape, non-etymological qualification.

**Evidence:** 瀬 and 頼 as printed, plus the pinned KanjiVG decomposition of 瀬 into 氵 and 頼, with 束 and 頁 inside 頼. [Pinned 瀬 SVG](https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/kanji/0702c.svg). **Confidence: high.**

**G5 — Minor; correctness and consistency — `snapshot\kanji\暑.md:49`, changed final sentence.**

The unqualified statement that 炎 “names fire rather than weather heat” overstates the distinction between the characters. The standalone noun 炎ほのお names a flame, but 炎 also expresses burning/scorching heat in weather words such as 炎天, 炎暑 and 炎熱. The new 炎 card itself discusses this overlap and excludes 暑, so the existing-card update now contradicts that teaching.

**Remedy:** qualify the contrast: “The standalone noun 炎ほのお means flame, not ordinary weather heat; compounds such as 炎天 can describe scorching heat.” Do not imply that the character never carries the weather-heat sense.

**Evidence:** independently inspected [Digital Daijisen, 炎](https://www.weblio.jp/content/炎), including the sense `燃えるように熱い` and its 炎暑・炎天・炎熱 examples; `snapshot\kanji\炎.md`. **Confidence: high.**

**G6 — Minor; comprehensibility — `snapshot\kanji\漫.md:44`; `snapshot\kanji\漬.md:23,39`; `snapshot\kanji\為.md:42`.**

These learner explanations retain source-maintenance details rather than just the distinctions being taught. 漫 and 漬 introduce the unexplained priority code `spec1`; 漬 additionally exposes `stagk=漬ける`; 為 opens a long reading paragraph by explaining how the repository checker labels な as な.る. The latter unnecessarily presents an incorrect-looking reading association before recovering the intended なす. In combination with long spelling/tag inventories, this obstructs an N5–N4 phone reader’s route to the useful reading and spelling rule.

**Remedy:** remove raw priority/restriction codes and the checker implementation discussion from learner prose. Retain the plain-English spelling restriction already supplied for 漬ける and a direct “為す is read なす” explanation. Split the remaining alternate-spelling/compound material into short, clearly separated points; maintenance details can remain in non-learner evidence.

**Evidence:** the cited paragraphs; `repo\docs\content-format.md` and the review contract’s requirement for explained jargon and phone-readable prose. This finding concerns presentation, not incorrect JMdict tagging or an unsafe quiz reading. **Confidence: high for the unexplained codes and checker leakage; medium for the degree of reading difficulty.**

Optional:

- Apply the same short-paragraph treatment to the particularly dense reading explanation in 潜 and some long Notes bullets in 濁 and 炎. Their core teaching is sound; this is additional polish beyond G6.
- Some meaning exclusions are deliberately conservative: 滑–滞 are contrasted as opposites, and 為–幕 share an English “act” label in different senses. Reconsider these individually if reducing unnecessary exclusions becomes a goal. I found no unsafe option or transitive-clique behavior resulting from them, so they are not established defects.
- Keep the restrained whole-word treatment of 為替: the card correctly avoids inventing separate か/わ/せ readings for the characters. Likewise preserve the distinction between 滑るすべる and the separate ぬめる entry, and the explicit qualification of source-only readings.

Limits:

- CLEAN means no actionable defect established within the reviewed scope, not exhaustive linguistic correctness. Public dictionaries can differ from the pinned snapshots; the identified Daijisen truncation is a reading-boundary error, not merely a snapshot difference.
- Exact runtime model/version was unavailable; I have identified the model/provider only to the extent exposed.
- No Android UI/phone rendering, JVM content suite or Kotlin cross-check was run. The latter two omissions are already declared packet limitations, not findings. Quiz reachability conclusions combine the complete supplied audits with inspection of the supplied implementation; I did not independently rerun the Kotlin builder.
- Stroke checks covered complete JSON structure, source identity/count/order identifiers, endpoints and sampled-path geometry against pinned KanjiVG. I did not render the app’s stroke animation.
- Failed public `kanjiapi.dev` requests returned HTTP 403; actual Jisho kanji entries supplied the independent metadata-reading checks instead.
- Some early oversized tool outputs were truncated. Relevant evidence was reread in bounded portions; automatically offered temporary-output files were not opened.
- No other reviewer report, author rationale, outside local checkout, background job, subagent or other session was consulted. Tool calls were serial, one per tool-using response; no parallel-call violation occurred. No content was edited except this report.

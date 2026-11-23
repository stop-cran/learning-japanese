Snapshot: `c6afa16315d5a88b5045eeb85d429b8f7fd90b1f`, batch 156; base `0638544ce1967ccec58ca7f9208c51ce8eaf4f8d`. Reviewer: OpenAI ChatGPT, GPT family; the exact serving-model identifier is not exposed. Packet-manifest byte SHA256 verified: `b378c4a9c2937355a1cde6f9a20e8a30c08181140b5e480e3a0c79c83bb5b0b5`.

Scope:

All paths below are relative to `C:\Users\romanko\n1-kanji-workspace\review-packets\batch-156-c6afa163`, unless stated otherwise. All four facets were considered for every new card and word article and both existing-file changes; consistency/quiz safety and phone comprehensibility received the deepest review.

Fully read content and changes:

- Under `snapshot\kanji\`: `丹.md`, `乙.md`, `亜.md`, `仁.md`, `仙.md`, `伎.md`, `伏.md`, `伐.md`, `伯.md`, `伴.md`, `潜.md`.
- Under `snapshot\words\`: `丹念.md`, `乙.md`, `亜熱帯.md`, `仁.md`, `仙人.md`, `歌舞伎.md`, `降伏.md`, `伐採.md`, `伯仲.md`, `同伴.md`, `伯母さん.md`.
- Both `diffs\kanji__潜.md.diff` and `diffs\words__伯母さん.md.diff`.
- Under `snapshot\strokes\`: `丹.json`, `乙.json`, `亜.json`, `仁.json`, `仙.json`, `伎.json`, `伏.json`, `伐.json`, `伯.json`, `伴.json` were fully parsed and checked programmatically for stroke counts, source revision, stroke types, finite coordinates and 16 sampled points per stroke. They were not rendered.

Fully read supporting text:

- `INSTRUCTIONS.md`; `mechanical-checks.md`.
- `evidence\provenance.json`; `evidence\source-metadata.json`; `evidence\kanjivg-components.txt`; `evidence\kanjipedia-senses.txt`; `evidence\kanjipedia-outside-readings.json`; `evidence\daijisen-word-text.md`; `evidence\daijisen-heads.txt`; `evidence\daijisen-word-heads.txt`; `evidence\okurigana-scan.txt`.
- Under `evidence\public-source\`: `weblio-丹.txt`, `weblio-乙.txt`, `weblio-亜.txt`, `weblio-仁.txt`, `weblio-仙.txt`, `weblio-伎.txt`, `weblio-伏.txt`, `weblio-伐.txt`, `weblio-伯.txt`, `weblio-伴.txt`.
- `evidence\audits\kanji-remarks.json`; `evidence\audits\word-remarks.json`; `evidence\audits\manifest-diff.md`; `evidence\audits\quiz-safety.txt`; `evidence\audits\reading-options.txt`; `evidence\audits\reading-exposure.txt`; `evidence\audits\extra-readings.json`; `evidence\audits\word_quiz_audit.py`.
- `evidence\app-code\Words.kt`; `evidence\app-code\QuizBuilder.kt`.
- Under `repo\words\`: `人物.md`, `個人.md`, `音.md`, `共同.md`, `礼.md`, `真剣.md`, `一致.md`, `同様.md`, `同一.md`.

Fully parsed files with selective inspection:

- `packet-manifest.json`: full JSON parsed; manifest hash and scoped change map checked, not every unrelated exported entry investigated.
- `titles\kanji-titles.tsv` and `titles\word-titles.tsv`: full inventories parsed for scoped title uniqueness and comparison-title checks.
- `evidence\kanjidic2-records.xml`: full XML parsed; all ten batch records and their name-reading lists inspected.
- `evidence\jmdict-families.xml`: full XML parsed; cited records, relevant spelling/reading restrictions and consequential senses inspected, not every family independently reviewed.
- `evidence\kanjivg-svgs.txt`: initial text inspected and all ten SVG sections parsed for stroke counts/types; component descriptions checked against `kanjivg-components.txt`.
- `evidence\jmdict-digest.tsv`: full TSV parsed; initial rows and the first nine priority-ordered family entries for each batch kanji inspected.
- `evidence\audits\word-quiz.txt`: parsed and inspected in sections. All forward meaning-candidate labels, per-word reading summaries and all 74 reverse reading pairs were reviewed. The 1,212 reverse meaning pairs were screened for shared English words and close senses, followed by targeted inspection; this was not a line-by-line semantic verification of every reverse pair.

Partially read context:

- `rubric\copilot-instructions.md`: through line 150.
- `repo\docs\content-format.md`: heading index and kanji, word and stroke contracts, particularly lines 86–205 and 289–304.
- `repo\docs\confusable-words.md`: first 65 lines, including direct-pair/nontransitive policy.
- `evidence\joyo-pages.md`: front matter and relevant target rows with context.
- `evidence\app-code\KanjiReadings.kt`: relevant selection and reading-normalization sections, including lines 62–142.
- `evidence\app-code\WordQuizViewModel.kt`: direction, answer-key, option-building and selected-stack filtering sections.
- `evidence\app-code\SrsMapping.kt`: direction and word-stack filtering sections.
- `repo\words\高級.md`: first 48 lines.

Outside the packet, only the authorized instruction file `C:\Users\romanko\n1-kanji-workspace\review-packets\prompts-156\initial-gpt.txt` was read; its supplied SHA256 was verified. No other local source or report was opened.

Independent public checks inspected actual entries, not just search snippets: all ten Kanjipedia character entries; all ten Jisho/KANJIDIC character entries; Digital Daijisen entries for all ten new words through Weblio; and Jisho word records for consequential uncommon readings/spellings and comparison senses, including 乙夜, 乙子, 杏仁, 伎楽, 調伏, 次ぐ, 伎, 仙, 伴, 討つ, 伯父, 伯母, お疲れ様 and 人物. Takoboto entry `1002570` additionally confirmed the otherwise locally absent お疲れ様 citation.

Verdicts:

- **Correctness: CLEAN** within the reviewed scope. No actionable factual defect established in the ten new kanji cards, ten new word articles, stroke structures or two edited passages.
- **Scoped coverage: CLEAN.** All ten new cards and ten new words cover their stated readings/main senses adequately; rare, historical and source-only material is distinguished rather than silently promoted to ordinary usage.
- **Consistency and quiz safety: NEEDS FIX.** Exceptions: `snapshot\words\乙.md` (G1), `snapshot\words\仁.md` (G2), and `snapshot\kanji\仙.md` / `snapshot\kanji\伎.md` (G3). Separately, destination existence/content for the compound-sound-changes article links in `snapshot\kanji\伐.md`, `snapshot\kanji\潜.md`, `snapshot\words\亜熱帯.md` and `snapshot\words\伐採.md` remains **UNVERIFIED** because that article is not exported in this packet; this is not evidence that the repository links are broken.
- **Comprehensibility: CLEAN** for the reviewed textual content, with nonblocking phone-oriented polish below. Central meanings, kana, contrasts and explicitly modern-shape mnemonics are understandable; no rendered phone-layout claim is made.

Additional adjudications:

- The kanji exclusion counts match their lists: 丹 5, 乙 15, 亜 9, 仁 9, 仙 3, 伎 8, 伏 13, 伐 10, 伯 6, 伴 8. Quoted comparison-card titles matched the supplied title inventory. Name-reading counts matched the pinned records.
- No additional kanji meaning-answer collision was established. Recording 乙/亜 only on 亜 is sufficient because exclusions are symmetric. Shared exclusions do not require transitive exclusions between 丹/仁, 仁/仙, 伏/伐, 伏/伴 or 伯/伴.
- The apparent 伯/は HIT is not production-reachable at this snapshot: 伯's three curated cards supply all three wrong on-reading options. The ten latent name-reading collisions are correctly distinguished from production, padded-session and one-holder hits. The missing on-reading choices on 鳩, 絹, 鶏 and 墨 trigger fallback rather than silently supplying invalid readings.
- No additional word-quiz collision was established from the reviewed close pairs. In particular, 伯仲 versus 一致/同一/同様, 同伴 versus 共同, and 降伏 versus 提出 retain meaningful distinctions; a shared English word or overlapping topic alone does not establish synonymy.
- All scoped card/word navigation links checked against the exported snapshot/context resolve, except for the unavailable article-target verification identified above. Both existing-file diffs are exactly the declared one-line changes; the new 伏 reading explanation in 潜 and the 伯 link in 伯母さん are accurate.
- Manifest integration accounts for 30 additions and two changed entries, with the expected contentVersion change. All 32 scoped committed-file hashes match after normalizing the export's CRLF line endings to committed LF bytes; this export normalization is not a content defect.

Findings:

1. **G1 — major — facet 3, consistency and quiz safety.**
   - **Location:** `snapshot\words\乙.md:2–3`; supporting audit `evidence\audits\word-quiz.txt:133–137`.
   - **Claim and impact:** A reading question displaying bare 乙 can offer both おつ and the attested reading おと, while accepting only おつ. おと is an archaic reading of this written form, not a fabricated pronunciation. Marking it wrong without sense/context disambiguation teaches an overbroad claim about how 乙 can be read.
   - **Reachability:** The audit leaves one corpus-derived slot after generated おうつ and おず, and 音 supplies おと in the reachable closeness-3 tier. `evidence\app-code\Words.kt:250–261` protects only `target.reading`, then fills from corpus readings; `WordQuizViewModel.kt:74–75` accepts only `word.reading`. This is a reachable option, not merely an unused dictionary reading.
   - **Remedy:** Protect attested alternative readings in the client, disambiguate the question with actual sense/context, or suppress this ambiguous reading prompt until a supported protection exists. The current content-only `quiz_exclusions` and `quiz_distractors` fields do **not** control `ReadingOptions.build`; adding 音 to the exclusion list would not fix this. Do not falsify 音's reading.
   - **Evidence:** Pinned JMdict entry `2837087` includes 乙 with おと and an archaic younger-sibling sense. Independently inspected [Kanjipedia 乙](https://www.kanjipedia.jp/kanji/0000578500) lists おと; [Digital Daijisen through Weblio](https://www.weblio.jp/content/%E4%B9%99) includes `おと【▽弟／▽乙】`.
   - **Confidence:** High for both attestation and option/answer-key behavior.

2. **G2 — major — facet 3, consistency and quiz safety.**
   - **Location:** `snapshot\words\仁.md:8,38`; supporting audit `evidence\audits\word-quiz.txt:152–159,259`.
   - **Claim and impact:** 人物, displayed as “person; figure; character,” remains drawable as a wrong meaning answer for 仁 even though the article itself correctly teaches 仁's “human” sense. A Japanese-to-English question showing 仁 can therefore have the intended “benevolence; compassion” answer and a defensible person/human answer. The warning that 仁 is not the ordinary everyday word for a person does not erase its dictionary sense.
   - **Reachability:** 人物 is in the 1,413-way score-5 tier supplying all three scored slots. 仁 excludes 人類 and 人間 but not 人物; `repo\words\人物.md:9` excludes only 人 and 性格. The symmetric check in `evidence\app-code\Words.kt:177–187` therefore does not block this pair.
   - **Remedy:** Add a direct 仁/人物 word-quiz exclusion on either side, then rerun the forward and reverse audits. Keep the true secondary human sense; this needs a direct exclusion, not a transitive expansion of unrelated ethics words.
   - **Evidence:** Pinned JMdict entry `1369620` assigns “human” to reading じん. Independently inspected [Digital Daijisen 仁](https://www.weblio.jp/content/%E4%BB%81) gives `ひと。→御仁`; [Kanjipedia 仁](https://www.kanjipedia.jp/kanji/0003694400) likewise gives ひと. The inspected [Jisho 人物 record](https://jisho.org/api/v1/search/words?keyword=%E4%BA%BA%E7%89%A9) confirms “person; character; figure; personage.”
   - **Confidence:** High.

3. **G3 — minor — facet 3, distractor plausibility.**
   - **Location:** `snapshot\kanji\仙.md:13,49`; `snapshot\kanji\伎.md:13,50`.
   - **Claim and impact:** These curated meaning sets are safely wrong but insufficiently plausible. 仙 (“hermit; immortal”) is contrasted only with wheat, a dish and a tube; 伎 (“skill; performer”) only with a plant, a snake and charcoal. The complete meaning simulation confirms these are the actual three wrong choices. A learner can exploit broad semantic category and the person radical rather than distinguish the target's meaning; the prose itself explicitly advertises those category differences. This fails the requested plausible-distractor criterion, although it does not create multiple correct answers.
   - **Remedy:** Replace at least part of each set with visually plausible but semantically distinct cards—for example, suitable other 亻 cards—without introducing synonyms or attested-reading collisions. Recheck both meaning directions, all curated reading slots and fallback reachability after replacement. Do not “improve” difficulty by adding genuinely synonymous answers.
   - **Evidence:** The two quoted distractor-explanation passages, matching front matter and `evidence\audits\quiz-safety.txt`; the person-radical structures are corroborated by the pinned KanjiVG component data.
   - **Confidence:** High for the displayed options and category shortcut; medium for the pedagogical impact assessment.

Optional:

- Shorten or move audit-oriented explanations out of the main learner path: long exclusion justifications, repeated “none means …” distractor paragraphs and repeated mnemonic disclaimers make the phone cards denser than necessary. Retain rare-reading qualifications and essential contrasts.
- Briefly explain specialist English such as “epigone” and “ateji” where used.
- In `snapshot\words\仁.md:22`, “This book discusses benevolence in Confucianism” is more natural English than “This book writes about …”. The Japanese sentence and intended translation are understandable.

Limits:

- The exact serving-model identifier was unavailable; none is invented.
- The packet lacks `repo\articles\compound-sound-changes.md`. The four relative links name the intended article, and the supplied mechanical check passed, but its actual destination/content could not be independently inspected locally. This is the localized UNVERIFIED item above.
- Source checks combined pinned XML, supplied official-table extracts and independently fetched public dictionaries. Not every related family entry or reverse meaning pair received a separate live lookup; the reverse meaning review was targeted semantic screening.
- The お疲れ様 entry `1002570` was absent from the local family XML. Its identity, reading and two senses were checked publicly through Jisho and [Takoboto's numbered entry](https://takoboto.jp/?w=1002570), rather than inferred from the missing local record.
- kanjiapi.dev requests returned HTTP 403; Jisho/KANJIDIC supplied the independent character-reading checks instead. A Kanjipedia おと word page returned HTTP 500; the actual Daijisen entry supplied independent confirmation. The direct JMdictDB entry endpoint presented an access gate; no access bypass was attempted.
- Stroke data was structurally checked against the pinned source but not visually rendered. No native-app run or phone screenshot review was performed. Reading-question risk is assessed for a written-form question without sense-disambiguating context, consistent with the supplied audit and answer model.
- The packet's known unrun JVM/Kotlin checks and unrelated 潜る lint warning are not findings. No whole-corpus content traversal, delegation, background work or parallel tool calling was used. No source file was changed; only this authorized report was written.

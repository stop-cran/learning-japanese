Snapshot: `38833c7f58bdd2406dbb808c6b2a74257ef29f12` — batch 146. Reviewer: OpenAI ChatGPT; exact deployed model identifier is not exposed to me.

Scope:

Independent, blind review of all 15 new kanji cards, their stroke files, all 23 modified word articles and their diffs, and the declared sentence change in 潔. Facets 3 and 4 received the deepest examination. Paths below are relative to the supplied packet.

**Read in full:**

- `INSTRUCTIONS.md`; `mechanical-checks.md`; `rubric\copilot-instructions.md`.
- `snapshot\kanji\`: `煮.md`, `熟.md`, `牧.md`, `狂.md`, `狭.md`, `献.md`, `玄.md`, `環.md`, `甚.md`, `癖.md`, `益.md`, `盛.md`, `盾.md`, `眺.md`, `睡.md`, `潔.md`.
- `snapshot\words\`: `利益.md`, `循環.md`, `文献.md`, `煮える.md`, `煮る.md`, `熟語.md`, `牧場.md`, `牧畜.md`, `狂う.md`, `狭い.md`, `献立.md`, `玄関.md`, `環境.md`, `甚だしい.md`, `癖.md`, `盛り.md`, `盛る.md`, `盛ん.md`, `眺め.md`, `眺める.md`, `睡眠.md`, `矛盾.md`, `貢献.md`.
- `diffs\`: `kanji__潔.md.diff`, `words__利益.md.diff`, `words__循環.md.diff`, `words__文献.md.diff`, `words__煮える.md.diff`, `words__煮る.md.diff`, `words__熟語.md.diff`, `words__牧場.md.diff`, `words__牧畜.md.diff`, `words__狂う.md.diff`, `words__狭い.md.diff`, `words__献立.md.diff`, `words__玄関.md.diff`, `words__環境.md.diff`, `words__甚だしい.md.diff`, `words__癖.md.diff`, `words__盛り.md.diff`, `words__盛る.md.diff`, `words__盛ん.md.diff`, `words__眺め.md.diff`, `words__眺める.md.diff`, `words__睡眠.md.diff`, `words__矛盾.md.diff`, `words__貢献.md.diff`.
- `evidence\source-metadata.json`; `evidence\kanjipedia-outside-readings.json`; `evidence\daijisen-heads.txt`; `evidence\okurigana-scan.txt`; `evidence\joyo-pages.md`.
- `evidence\audits\quiz-safety.txt`; `evidence\audits\reading-exposure.txt`; `evidence\audits\reading-options.txt`; `evidence\audits\kanji-remarks.json`; `evidence\audits\kanji_remarks.py`.
- `evidence\public-source\`: `weblio-煮.txt`, `weblio-熟.txt`, `weblio-牧.txt`, `weblio-狂.txt`, `weblio-狭.txt`, `weblio-献.txt`, `weblio-玄.txt`, `weblio-環.txt`, `weblio-甚.txt`, `weblio-癖.txt`, `weblio-益.txt`, `weblio-盛.txt`, `weblio-盾.txt`, `weblio-眺.txt`, `weblio-睡.txt`.
- `evidence\app-code\QuizBuilder.kt`; `evidence\app-code\KanjiMeaningMetadata.kt`; `evidence\app-code\KanjiReadings.kt`.
- `repo\kanji\仕.md` — context only.

**Opened in full for structured validation, with selected content inspected rather than every record read editorially:**

- `snapshot\strokes\`: `煮.json`, `熟.json`, `牧.json`, `狂.json`, `狭.json`, `献.json`, `玄.json`, `環.json`, `甚.json`, `癖.json`, `益.json`, `盛.json`, `盾.json`, `眺.json`, `睡.json`. All parsed; identities, counts, ordered IDs, coordinate validity and source stroke starts checked. The complete 玄 JSON was also displayed.
- `evidence\kanjidic2-records.xml` — batch records, metadata, readings and relevant meanings.
- `evidence\jmdict-families.xml` — introductory excerpt and cited families, including spelling/reading restrictions and sense/register information.
- `evidence\jmdict-digest.tsv` — header and selected records, including the sleep variants, 献る, 玄米, 牧場, 熟語 and 盛る/盛り.
- `titles\kanji-titles.tsv`; `titles\word-titles.tsv` — parsed for exact labels, targeted semantic comparisons and article existence; not a semantic review of every corpus title.

**Read in part or hash-only:**

- `repo\docs\content-format.md` — lines 1–190 inspected; an earlier request through line 240 produced truncated output.
- `repo\docs\confusable-words.md` — first 55 lines inspected; an earlier longer request produced truncated output.
- `evidence\provenance.json` — first 100 lines requested.
- `evidence\app-code\Words.kt` — first 100 lines.
- `packet-manifest.json` — hashed, not read editorially. SHA-256 matched `d51bc2fb9137ee513c0c80ae717f58190ae8730a3c8843682bffec87df8d5c88`.

Only nonrecursive directory metadata listings were used for the packet root, `evidence`, its `audits`, `public-source` and `app-code` subfolders, `diffs`, and `snapshot\strokes`. Link checks tested destination existence without opening additional article bodies.

Independent public verification used actual Digital Daijisen entries on Weblio for all 15 kanji and relevant headwords, including 牛, 馬, 羊, 甚だしい and 半濁音; actual Kanjipedia entries for 狂, 狭, 献, 甚 and 環; and actual Jisho/JMdict JSON entries for the linked words and consequential additional examples. These were entry inspections, not search-snippet verification. Ordered stroke starts and counts were compared with public KanjiVG at the pinned revision `70a0b7ae0c18ceb5cb358274b029cce0234a43bc`.

Verdicts:

- **Correctness: NEEDS FIX** — G1 and G2.
- **Scoped coverage: CLEAN** — all 15 cards.
- **Consistency and quiz safety: NEEDS FIX** — G3 concerns unnecessary exclusions, not an observed ambiguous answer.
- **Comprehensibility: NEEDS FIX** — G1 and G2 teach misleading character/reading relationships.

Per-card verdicts:

| Card | Correctness | Scoped coverage | Consistency and quiz safety | Comprehensibility |
|---|---|---|---|---|
| 煮 | CLEAN | CLEAN | CLEAN | CLEAN |
| 熟 | CLEAN | CLEAN | CLEAN | CLEAN |
| 牧 | CLEAN | CLEAN | NEEDS FIX — G3 | CLEAN |
| 狂 | CLEAN | CLEAN | CLEAN | CLEAN |
| 狭 | CLEAN | CLEAN | CLEAN | CLEAN |
| 献 | CLEAN | CLEAN | CLEAN | CLEAN |
| 玄 | CLEAN | CLEAN | CLEAN | CLEAN |
| 環 | CLEAN | CLEAN | CLEAN | CLEAN |
| 甚 | NEEDS FIX — G1 | CLEAN | CLEAN | NEEDS FIX — G1 |
| 癖 | NEEDS FIX — G2 | CLEAN | CLEAN | NEEDS FIX — G2 |
| 益 | CLEAN | CLEAN | CLEAN | CLEAN |
| 盛 | CLEAN | CLEAN | CLEAN | CLEAN |
| 盾 | CLEAN | CLEAN | CLEAN | CLEAN |
| 眺 | CLEAN | CLEAN | CLEAN | CLEAN |
| 睡 | CLEAN | CLEAN | CLEAN | CLEAN |

The changed 潔 sentence and all 23 word articles/diffs are CLEAN on all four facets within this review. All 23 word diffs are exactly one intended kanji-link wrap, with no other prose or Dictionary-line change. 潔 has only the declared sentence replacement, linking 癖 and correctly identifying its underlying ヘキ reading in 潔癖. The surrounding passages remain coherent. The 452 relative links checked across the scoped Markdown files resolve.

**Substantive checks supporting these verdicts:**

- All 15 cards agree with the pinned metadata on grade, stroke count, radical and ordered on/kun lists. Tags and section order are correct. Quiz reading lists are subsets of the full lists, and every selected reading has a linked word example. Listed but unselected readings are accounted for.
- The mnemonics are explicitly modern-shape mnemonics, not historical derivations. No unsupported etymology or incorrect component placement was established. 環's reference to 王-shaped components in 琴 is defensible as a shape observation.
- The Joyo reading rows, examples, old-form parentheses and distinctions between official and outside-table readings match the supplied official extracts. Kanjipedia/Daijisen claims checked against actual entries do not establish another defect.
- 牧場's two readings belong to one JMdict entry. 献る's restrictions distinguish まつる from source-only たてまつる; 玄米's くろごめ is not interchangeable with every reading of 黒米. The cards preserve those distinctions.
- 熟語's compound/idiom explanation, 盛る's separate もる and さかる entries, and 盛り's さかり versus もり are appropriately distinguished. 狭苦しい and 盾突く were evaluated as whole words, not mistaken for independent readings of their linked substrings.
- 睡る and 睡い are supported written variants in JMdict 1529390 and 1529330 without a rare-spelling tag; 睡り is tagged rare in 1529370. The card correctly distinguishes them. Its 睡眠, 熟睡, 午睡 and 昏睡 descriptions are supported.
- No additional actionable sentence, translation, register or quoted-gloss error was established in the scoped articles.

**Meaning options:** I judged the actual title combinations in both directions, including ordinary secondary senses, rather than treating a passing simulation as a semantic verdict:

| Target | Curated wrong cards | Judgment |
|---|---|---|
| 煮 | 火・水・肉 | Defensibly wrong; cooking ingredients/conditions are not boiling or simmering. |
| 熟 | 語・木・田 | Defensibly wrong; word/plant/field identities are not ripening, maturity or skill. |
| 牧 | 歌・山・雨 | Defensibly wrong; compound or pasture-scene associations do not supply 牧's meaning. |
| 狂 | 犬・気・風 | Defensibly wrong; components and thematic associations do not mean going mad or awry. |
| 狭 | 道・室・店 | Defensibly wrong; things that can be narrow are not the property “narrow.” |
| 献 | 猫・独・状 | Defensibly wrong despite shape similarities. |
| 玄 | 率・畜・玉 | Defensibly wrong despite shape/component associations. |
| 環 | 現・理・琴 | Defensibly wrong; their displayed senses do not mean a ring or surrounding. |
| 甚 | 甘・匹・基 | Defensibly wrong despite visible component associations. |
| 癖 | 疲・痛・療 | Defensibly wrong; a shared sickness radical does not make these habits or quirks. |
| 益 | 皿・雨・魚 | Defensibly wrong; container/scene associations do not mean benefit or profit. |
| 盛 | 山・海・店 | Defensibly wrong; heaps, abundance and food-service scenes do not equate these titles with 盛. |
| 盾 | 目・直・真 | Defensibly wrong despite visual similarities. |
| 眺 | 相・県・省 | Defensibly wrong; their ordinary displayed meanings do not mean gazing out over something. |
| 睡 | 真・着・直 | Defensibly wrong despite visual similarities. |

The Notes justify the shared and Starter-card distractors without claiming they are synonyms. Reusing 雨, 店, 直, 真 or other distractors across different targets is not itself a collision. 煮's one-sided exclusion of 熟 is effective in both directions in the supplied app code, and 熟's cooking sense supports that pair. I found no further defensible wrong answer from the highlighted 熟/癖, 狂/狭 or 益/盛 comparisons. Apart from G3, no actionable exclusion defect was established; related English vocabulary was not automatically treated as synonymy.

**Reading options:** The complete audits and the supplied builder agree that no attested extra reading is actually offered incorrectly in the reported production, padded-session or one-holder cases. The count of **10 latent collisions across nine distinct target/reading pairs is correct**:

- 牧: ま, まい, もく.
- 狂: ふれる.
- 狭: せ.
- 甚: じ, いたい.
- 益: よう.
- 盛: もり, counted once under each of its two selected prompts.

These are latent candidate-pool observations, not ten shipped wrong-answer exposures. 盛's three curated Starter choices fill every slot for both prompts; もり is additionally a genuine 盛 word reading, not only a name-reading coincidence. 環 and 癖 each need a fallback in the relevant reading mode because a curated holder lacks that mode; the complete option audit accounts for those slots. Exclusions are symmetric and nontransitive in meaning quizzes and are not incorrectly assumed to protect reading quizzes.

Findings:

**G1 — minor; correctness and comprehensibility; `snapshot\kanji\甚.md:35–41`, especially line 37.**

- **Claim and impact:** “In 甚だしい, 甚 writes はなはだ and しい is okurigana” assigns the already written だ to the kanji. In the actual spelling, 甚 supplies はなは and だしい is the written kana ending. The sentence also contradicts the correct account in the table immediately above it. A beginner can learn the wrong kanji/kana boundary even though the complete word pronunciation and quiz answer are correct.
- **Remedy:** Say that 甚 represents はなは in 甚だしい, followed by okurigana だしい. Explain the app's selected `はなは.だ` grouping separately, without treating its だ as sound supplied by the printed kanji. Likewise distinguish 甚 + だ in the adverb 甚だ.
- **Evidence:** The card's own line 35; pinned KANJIDIC2 `はなは.だ` / `はなは.だしい`; the official examples in `evidence\joyo-pages.md`; and the inspected [Kanjipedia entry](https://www.kanjipedia.jp/kanji/0003700700), which explicitly divides `甚だ(はなは－だ)` and `甚だしい(はなは－だしい)`.
- **Confidence:** High.

**G2 — minor; correctness and comprehensibility; `snapshot\kanji\癖.md:37`.**

- **Claim and impact:** “ヘキ is voiced to ペキ” in 潔癖 is phonetically wrong: p is voiceless, not the voiced counterpart of h. The opening “Joined to another word, くせ is voiced to ぐせ” also sounds unconditional, although the paragraph itself includes 難癖 なんくせ and the dictionary allows unvoiced variants in other compounds. This presents sound changes as rules that learners cannot reliably apply.
- **Remedy:** Use plain language: “くせ often becomes ぐせ in compounds, as in 口癖 くちぐせ; it remains くせ in 難癖 なんくせ.” For 潔癖, say “ヘキ changes to ペキ after the small っ,” rather than calling this voicing. No additional phonetic jargon is necessary.
- **Evidence:** Actual JMdict/Jisho entries for 口癖 (1276890), 酒癖 (1663290: さけぐせ and さけくせ), 手癖 (1699540: てくせ and てぐせ), 難癖 (1461100: なんくせ) and 潔癖 (1254470: けっぺき); inspected [Digital Daijisen 半濁音](https://www.weblio.jp/content/半濁音), identifying the p-series as voiceless.
- **Confidence:** High.

**G3 — minor; consistency and quiz safety; `snapshot\kanji\牧.md:14,53–54`.**

- **Claim and impact:** At least the exclusions 牧–牛, 牧–馬 and 牧–羊 are topical associations, not direct ambiguous-answer pairs. The actual labels are “pasture; raise livestock; pastor,” “cattle, cow,” “horse” and “sheep.” An animal that can be raised on a pasture is not the act of raising it or the pasture itself, in either quiz direction. The exclusions unnecessarily suppress valid distinctions, and the Notes justify them as overlapping meanings. This is not an observed two-correct-answer bug.
- **Remedy:** Remove these three pairs from `quiz_exclusions` and adjust the “all seventeen” explanation. The animals can remain useful contextual comparisons without being excluded. Retain exclusions supported by an actual overlapping displayed meaning rather than by participation in the same farming scene.
- **Evidence:** Exact titles in `titles\kanji-titles.tsv`; actual Digital Daijisen entries for [牧](https://www.weblio.jp/content/牧), [牛](https://www.weblio.jp/content/牛), [馬](https://www.weblio.jp/content/馬) and [羊](https://www.weblio.jp/content/羊); `repo\docs\content-format.md:117–125`, requiring direct pairs based on displayed labels and ordinary meanings. The card itself correctly accepts other pasture-scene associations as distractors at line 52.
- **Confidence:** High for these three pairs; this finding does not assert that every other 牧 exclusion is invalid.

Optional:

- Shorten learner-facing audit explanations and long exclusion inventories. Preserve the kana, concrete contrasts and rare-reading qualifications, but move repo-aligner details and exhaustive quiz bookkeeping out of the main phone-reading flow.
- Prefer “not quizzed here” to “source-only here” for ordinary readings such as 甚's ジン and 癖's ヘキ. The current text explains the intended distinction, but the shorter label could otherwise suggest that the reading itself is doubtful.
- In 癖, “the 潔 card discusses this compound and links 癖” would make the destination clearer than “links this word.” In 熟, “other examples” would be clearer than “linked words” when discussing 熟練 and 熟慮, for which the card correctly says there are no word articles.

Limits:

- CLEAN means no actionable defect established in the reviewed scope, not exhaustive correctness. Corpus-wide semantic coverage was not claimed; title indexes supported bounded comparisons, and no whole-corpus scan or recursive listing was performed.
- Reading reachability conclusions apply to the supplied pools, prompts, extra-reading set and app reference. I inspected the complete audits and relevant builder code; I did not independently execute the app or establish behavior for arbitrary future/custom pools or older clients.
- Stroke checks covered structured validity and ordered source starts/counts, not an on-device animation or pixel-perfect rendering comparison.
- Several early tool outputs were truncated; scoped card/rubric material was subsequently reread in bounded outputs. No automatically saved temporary output was opened. No parallel or multiple-tool response, sub-agent, background job or other session was used.
- No other reviewer report or author rationale was sought. No packet content was changed; the only authored file is this report.

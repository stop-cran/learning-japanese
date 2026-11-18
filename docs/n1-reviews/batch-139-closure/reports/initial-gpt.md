Snapshot: `a47efe9af926316eaa86656033bf6e109f2be697` — batch 139. Reviewer: GPT (OpenAI; the exact runtime model identifier is not exposed to me).

Scope:

Independent, blind, read-only review of all 15 new kanji cards, all 15 stroke datasets, and all 20 modified word articles and their diffs. Facets 3 and 4 received the deepest examination. No other review or author rationale was consulted.

The following inventory names every packet file opened. Braces enumerate individual filenames, not additional files searched.

**Read in full:**

- `INSTRUCTIONS.md`
- `mechanical-checks.md`
- `rubric\copilot-instructions.md`
- `snapshot\kanji\{嫁,嬢,宗,宜,宣,宴,寂,密,審,尋,屈,属,岬,峠,崩}.md`
- `snapshot\strokes\{嫁,嬢,宗,宜,宣,宴,寂,密,審,尋,屈,属,岬,峠,崩}.json`
- `snapshot\words\{お嬢さん,嫁,宗教,宜しく,宣伝,宴会,寂しい,密,審判,尋ねる,属する,岬,峠,崩す,崩れる,秘密,花嫁,退屈,金属,附属}.md`
- `diffs\words__{お嬢さん,嫁,宗教,宜しく,宣伝,宴会,寂しい,密,審判,尋ねる,属する,岬,峠,崩す,崩れる,秘密,花嫁,退屈,金属,附属}.md.diff`
- `evidence\source-metadata.json`
- `evidence\provenance.json`
- `evidence\joyo-pages.md`
- `evidence\kanjipedia-outside-readings.json`
- `evidence\daijisen-heads.txt`
- `evidence\okurigana-scan.txt`
- `evidence\audits\quiz-safety.txt`
- `evidence\audits\reading-exposure.txt`
- `evidence\audits\reading-options.txt`
- `evidence\audits\word-remarks.json`
- `evidence\audits\kanji_remarks.py`
- `evidence\app-code\QuizBuilder.kt`
- `evidence\app-code\KanjiMeaningMetadata.kt`
- `evidence\public-source\weblio-{嫁,嬢,宗,宜,宣,宴,寂,密,審,尋,屈,属,岬,峠,崩}.txt`
- `repo\kanji\通.md`

**Opened in part, or read programmatically for a bounded check:**

- `repo\docs\content-format.md`: lines 1–205, including the relevant kanji/reading/quiz format guidance.
- `repo\docs\confusable-words.md`: lines 1–115 and targeted matching lines later in the file; not the whole inventory.
- `evidence\kanjidic2-records.xml`: the 15 scoped records' Japanese metadata and meanings; other records/languages were not reviewed comprehensively.
- `evidence\jmdict-families.xml`: initial raw lines and structured extraction of the cited entries for the 15 cards, including their readings, spelling restrictions, complete senses and register labels; not all 1,612 families.
- `evidence\jmdict-digest.tsv`: header and targeted vocabulary rows, including 嫁き遅れ, 嬢さん, 宜なるかな, 寂然, 雅楽属, 属する, 岬湾, 岬角 and 千尋; not every digest row.
- `titles\kanji-titles.tsv`: full-index programmatic title-uniqueness checks, plus scoped distractor/exclusion titles and missing-card checks; not a review of every indexed article.
- `titles\word-titles.tsv`: header, size and the 20 modified words' indexed titles/readings.
- `evidence\app-code\KanjiReadings.kt`: lines 1–180.
- `packet-manifest.json`: bytes read to verify its SHA-256, not a content review of every manifest entry.
- `repo\kanji\{婦,娘,主,良,善,好,具,均,経,酒,党}.md`: first 16 lines of each, for displayed titles/readings.

Independent public checks used actual Jisho kanji entries for all 15 characters, actual Digital Daijisen entries served by Weblio for all 15 characters, and actual Jisho word-entry responses for important or consequential examples and alternative readings. Checks included 宜い/宜なるかな, 嫁き遅れ, 嬢さん/嬢ちゃん, 寂然, 属する, 雅楽属/主典 and 岬角/岬湾. Additional actual Daijisen entries verified 寂しい/さむしい, 密か/みそか and 属する/しょくする. These were entry inspections, not search-snippet verification.

Verdicts:

- Correctness: **NEEDS FIX** — the specific sense-overlap assertion in `snapshot\kanji\峠.md:48` needs narrowing (G1). Otherwise no actionable correctness defect established.
- Scoped coverage: **CLEAN** — every metadata reading is represented or explicitly qualified; no consequential common-word omission established.
- Consistency and quiz safety: **NEEDS FIX** — two unjustified exclusion edges on 峠 (G1). No ambiguous answer established in the supplied actual meaning questions or reachable non-name reading questions.
- Comprehensibility: **CLEAN** — clear central explanations and honest mnemonics; substantial nonblocking opportunities to shorten reference material.

Per-card coverage and exceptions:

| Card | Correctness | Coverage | Quiz consistency | Comprehensibility | Specific adjudication |
|---|---|---|---|---|---|
| 嫁 | CLEAN | CLEAN | CLEAN | CLEAN | カ, とつぐ and the restricted いく/ゆく spellings are distinguished from the selected よめ. The card does not invent an ordinary standalone 嫁く example. |
| 嬢 | CLEAN | CLEAN | CLEAN | CLEAN | むすめ is identified as a source reading rather than an invented JMdict word spelling. お嬢さん is correctly segmented. 嬢さん/嬢ちゃん dictionary evidence does not require adding new character-reading prompts. |
| 宗 | CLEAN | CLEAN | CLEAN | CLEAN | シュウ, ソウ and むね are accounted for. The limited 宗 spelling of むね is not extended indiscriminately to every sense of 旨. |
| 宜 | CLEAN | CLEAN | CLEAN | CLEAN | ギ examples, usually-kana よろしい/よろしく, and extra よい/うべ/むべ evidence are separated. The title is supported; only よろしく is selected. |
| 宣 | CLEAN | CLEAN | CLEAN | CLEAN | セン is selected; のたまう is accurately qualified and not treated as an ordinary selected practice reading. |
| 宴 | CLEAN | CLEAN | CLEAN | CLEAN | エン and poetic うたげ are distinguished. The extra enjoy/relax sense is dictionary-supported; the reference compounds are accurate. |
| 寂 | CLEAN | CLEAN | CLEAN | CLEAN | さびしい and さみしい are legitimate alternatives; さむしい is separately sourced. ジャク/セキ, さび and さびれる, including 寂然 restrictions, are treated accurately. |
| 密 | CLEAN | CLEAN | CLEAN | CLEAN | ミツ and its みっ sound changes are illustrated correctly. ひそか and extra みそか are distinguished from the selected practice reading. |
| 審 | CLEAN | CLEAN | CLEAN | CLEAN | シン examples are sound. つまびらか and つぶさに are qualified without claiming a nonexistent JMdict 審 spelling for the latter. |
| 尋 | CLEAN | CLEAN | CLEAN | CLEAN | たずねる, ジン and the measure ひろ are distinguished; the variable historical fathom length is not presented as one universally fixed measure. |
| 屈 | CLEAN | CLEAN | CLEAN | CLEAN | クツ and the nonselected bending verbs are covered; alternative/old readings and usually-kana usage are identified. |
| 属 | CLEAN | CLEAN | CLEAN | CLEAN | ゾク versus ショク/しょくする is handled correctly. Historical さかん and 主典 are explained; source-only つく/やから are not supplied with fabricated ordinary examples. |
| 岬 | CLEAN | CLEAN | CLEAN | CLEAN | コウ is supported by 岬角/岬湾. さき is a real additional dictionary reading, not merely a name reading; its apparent audit collision is unreachable in the supplied shipped pools. |
| 峠 | NEEDS FIX | CLEAN | NEEDS FIX | CLEAN | Japanese-created character, lack of on reading, word-origin qualification and figurative peak/climax senses are supported. G1 concerns only the 通/経 overlap claim and exclusions. |
| 崩 | CLEAN | CLEAN | CLEAN | CLEAN | ホウ, both verbs, suffix notation, transitivity and irregular 雪崩 are handled correctly. See Optional concerning shared-stem scheduling. |

Additional scope results:

- All 15 cards' grade, stroke count, radical and Japanese on/kun lists match the pinned metadata. Selected quiz readings come from those lists and have linked word examples. Section structure, tags and grade labels show no actionable mismatch.
- The modern-shape mnemonics are explicitly labelled as memory aids rather than historical derivations. The component positions and comparisons checked are defensible, including the 山/田/中 comparisons for 岬 and the partial-shape distractors elsewhere.
- All 15 stroke datasets have the expected character, count, ordered stroke IDs and bounded finite points. Independent comparison with the pinned public KanjiVG revision `70a0b7ae0c18ceb5cb358274b029cce0234a43bc` matched stroke counts, order/types and start positions within approximately 0.11 units.
- All 301 local Markdown links extracted from the 35 scoped Markdown files resolve using the snapshot with the packet's repository context. The 15 new kanji titles are unique in the title index.
- The 20 word diffs contain only the declared link wrapping and the four declared remark changes. The links point to the intended new cards. Removing the obsolete 宴/崩 no-card statements and narrowing 附属 to 附 alone are correct; the resulting passages remain grammatical. The title index also supports the remaining no-card statements about 附 and 秘.
- The two existing Dictionary lint warnings are not new defects: the diffs do not alter those citations.
- The official Joyo reading/example/bracket claims checked against the supplied complete page extracts match them. No unsupported example-sentence translation or quoted dictionary gloss was established.

Quiz-specific adjudication:

- I considered all three curated meaning distractors for every new card, both as wrong labels for the new character and in the reverse character/label direction, including ordinary secondary senses. None of the 45 curated alternatives was established as an alternative correct answer. Their plausibility is often component-based, not whole-character resemblance.
- The complete meaning simulation fills the actual three wrong-answer slots for each card. Symmetric pairwise exclusions in `QuizBuilder.kt` are not a transitive synonym closure.
- The full reading-exposure audit reports no production non-name collisions and no collisions in its padded Starter or single-holder padded cases. Its 11 latent collisions concern hypothetical reduced pools; they are not demonstrated failures of the supplied shipped pools.
- The `reading-options.txt` HIT for 岬/さき via 先 is not an actual offered option in the supplied full/Starter simulations: the curated 山/田/中 readings already occupy the three slots. Daijisen independently confirms さき as a real reading, so the distinction between validity and reachability matters.
- 宗/し can be drawn from 示, but the evidence identifies し as a name-only reading, not an ordinary on/kun reading. For an explicitly on-reading question asking シュウ, this does not establish a second correct on-reading answer.
- Most broad-looking exclusions have a defensible secondary-sense or English-label rationale rather than requiring identical primary meanings. I did not treat the lead list as an automatic defect list. G1 identifies the narrower case where the displayed labels and Japanese senses already resolve the apparent English collision.

Findings:

**G1 — minor — facets 3 and 1 — `snapshot\kanji\峠.md:14,48`: distinguish a mountain pass from passing through.**

**Claim and impact:** 通 and 経 are excluded, and the Notes group them among characters overlapping 峠's “pass,” “peak” and “mountain” senses. Here the apparent overlap comes from different senses and grammatical uses of English *pass*. 峠 is a mountain pass or a figurative critical peak; 通る is to go/pass through, and 経る is to pass/elapse or go through. The displayed titles already say `mountain pass; peak; climax`, `pass through; commute` and `pass through; sutra`. Neither of the latter two labels is an alternative correct meaning of 峠, nor does 峠's label correctly answer 通 or 経.

This unnecessarily removes defensibly wrong alternatives in both directions and, more importantly, teaches a sense-overlap claim that the examples do not support. It does **not** make the current three curated 峠 answers ambiguous; the severity is minor.

**Remedy:** Remove 通 and 経 from this card's exclusions unless a specific source-backed overlapping sense relevant to the displayed quiz labels is supplied. Rewrite the corresponding Notes sentence as a distinction: a *mountain pass* is 峠; *passing through* is expressed by verbs such as 通る/経る. Retain independently justified peak/mountain guards.

**Evidence:** The card's exact declarations and Notes; the indexed titles; `repo\kanji\通.md`; the header of `repo\kanji\経.md`; the scoped 峠 dictionary evidence; actual Jisho entries for [通る](https://jisho.org/api/v1/search/words?keyword=通る) and [経る](https://jisho.org/api/v1/search/words?keyword=経る), including their complete returned sense lists. The supplied format/review contract calls for real synonym or confusable pairs, not a shared English substring with different senses.

**Confidence:** High for the sense distinction and inaccurate grouping; medium-high for removing the two conservative exclusion edges.

Optional:

1. **Shorten reference inventories for phone reading.** In particular, `密.md:57` places approximately sixteen additional compounds, readings, full gloss strings and historical/religious qualifications in one bullet. Similar, shorter inventories occur in 宣, 審, 屈, 属 and 寂. Keep two or three useful examples per idea, split by sense, and move exhaustive dictionary evidence out of the learner-facing prose where the format permits. This is nonblocking because the cards already present their main idea first and explicitly label the later material as reference.
2. **Clarify 崩's selected readings versus scheduled questions.** The metadata selects both くずれる and くずす, and both are taught correctly. `ReadingCard.quizReadings` nevertheless deduplicates by the pre-dot stem, so the ordinary scheduled queue retains the first shared くず stem rather than creating two independent reading memories. A brief explanation would prevent “Practice selects” from being mistaken for a promise of two separately scheduled questions. This is not a request to change the reading metadata or app.
3. **Keep the English-homonym rationale explicit.** 宴's note honestly says 党 shares only the English word *party*, not the Japanese banquet sense. If exclusion sets are later tightened, prefer more precise displayed labels and direct sense evidence over adding further topic-related or homonym-only pairs. I have not established an unsafe actual question from that conservative guard.

Limits:

- The exact underlying GPT model/version was not available; I have not invented one.
- This was a packet review, not an independent checkout/diff against the remote commit. The manifest hash was independently verified as `95f5b71e73fb72c354c91bd246095984a4bd09cc88e9704773954e398296aad3`.
- I did not render the Android UI or animations, run app tests, fully resample every SVG curve, or certify every conceivable dynamically reduced quiz pool. Stroke validation covered the complete supplied datasets structurally and the bounded upstream comparisons described above.
- Public dictionary checks are current entry inspections; the pinned JMdict/KANJIDIC2 snapshots remain the reference for their exact recorded wording. Kanjipedia outside-table markings were checked through the supplied extraction and official Joyo evidence, not by independently opening every live Kanjipedia page. No consequential unresolved discrepancy remained from that distinction.
- `kanjiapi.dev` returned HTTP 403; actual Jisho kanji entries supplied the independent metadata cross-check instead.
- Two overlong early tool results were automatically redirected by the tool. I did not open those generated paths; I reread the intended packet evidence in smaller bounded calls.
- No parallel tool calls, sub-agents, other sessions, background jobs, recursive listings, or corpus-article scans were used. No evidence/content files were edited. The only intentional file write is this report.

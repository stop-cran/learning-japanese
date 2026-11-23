Snapshot: 9d393a8f7bbf04114668b40f84b67a9a4b2ef7e3 — batch 142. Reviewer: GPT, an OpenAI model; exact model identifier unavailable.

Scope:

Independent, blind review, deepest on consistency/quiz safety and beginner/phone comprehensibility. Paths below are relative to the supplied packet.

Read in full:

- `INSTRUCTIONS.md`, `mechanical-checks.md`, `rubric\copilot-instructions.md`.
- `snapshot\kanji\挙.md`, `振.md`, `挿.md`, `掌.md`, `推.md`, `描.md`, `提.md`, `揮.md`, `揺.md`, `操.md`, `故.md`, `敵.md`, `斉.md`, `斎.md`, `斜.md`; also `snapshot\kanji\仮.md`, with only its changed remark judged as new work.
- `snapshot\words\一斉.md`, `事故.md`, `体操.md`, `匹敵.md`, `挙げる.md`, `振り仮名.md`, `振る.md`, `振舞う.md`, `挿す.md`, `推定.md`, `推薦.md`, `描く.md`, `提出.md`, `提案.md`, `揺れる.md`, `操作.md`, `故郷.md`, `故障.md`, `敵.md`, `斜.md`, `斜め.md`, `書斎.md`, `発揮.md`, `車掌.md`.
- `diffs\words__一斉.md.diff`, `words__事故.md.diff`, `words__体操.md.diff`, `words__匹敵.md.diff`, `words__挙げる.md.diff`, `words__振り仮名.md.diff`, `words__振る.md.diff`, `words__振舞う.md.diff`, `words__挿す.md.diff`, `words__推定.md.diff`, `words__推薦.md.diff`, `words__描く.md.diff`, `words__提出.md.diff`, `words__提案.md.diff`, `words__揺れる.md.diff`, `words__操作.md.diff`, `words__故郷.md.diff`, `words__故障.md.diff`, `words__敵.md.diff`, `words__斜.md.diff`, `words__斜め.md.diff`, `words__書斎.md.diff`, `words__発揮.md.diff`, `words__車掌.md.diff`, `kanji__仮.md.diff`.
- `evidence\source-metadata.json`, `provenance.json`, `joyo-pages.md`, `kanjipedia-outside-readings.json`, `daijisen-heads.txt`, `okurigana-scan.txt`.
- `evidence\audits\quiz-safety.txt`, `reading-options.txt`, `reading-exposure.txt`, `kanji-remarks.json`, `word-remarks.json`, `kanji_remarks.py`.
- `evidence\app-code\QuizBuilder.kt`, `KanjiMeaningMetadata.kt`.
- `repo\kanji\缶.md`.

Programmatically read/parsed in full, with bounded substantive inspection:

- `snapshot\strokes\挙.json`, `振.json`, `挿.json`, `掌.json`, `推.json`, `描.json`, `提.json`, `揮.json`, `揺.json`, `操.json`, `故.json`, `敵.json`, `斉.json`, `斎.json`, `斜.json`: all stroke records and coordinates parsed; ordered types, endpoints, bounds and counts inspected.
- `titles\kanji-titles.tsv`, `titles\word-titles.tsv`: indexes processed for exact titles, uniqueness, declared-kanji links and target existence; not every unrelated row substantively reviewed.
- `evidence\kanjidic2-records.xml`: full XML parsed; the 15 new-character records inspected and compared with front matter and metadata.
- `evidence\jmdict-families.xml`: full XML parsed; all families cited in the 15 cards inspected for spellings, readings, restrictions, sense/register labels and glosses; additionally inspected the すがき family and 提灯 compounds.
- `evidence\jmdict-digest.tsv`: full TSV parsed; relevant priority-marked families inspected for scoped coverage, not every unrelated entry.

Read in part:

- `repo\docs\content-format.md`, lines 1–220.
- `repo\docs\confusable-words.md`, opening sections and returned portion through approximately line 156.
- `evidence\app-code\KanjiReadings.kt`, lines 1–220, including option-generation and reading-protection logic.

Nonrecursive directory listings only: `snapshot\strokes`, `diffs`, `evidence\public-source`, `evidence\app-code`. No individual `evidence\public-source` extract was substantively read.

Independent public checks inspected actual Weblio/Digital Daijisen character entries and kanjiapi.dev records for all 15 characters. Additional actual entries included Kanjipedia 提; Weblio 提灯, 揺る, 揺く, 斎王 and 斎宮; Jisho 挙げる, 振る舞う, 挟む/挿む, 掌, 推す, 描く, 提げる, 菩提, 振るう/揮う, 揺る, 操, 敵う, 斎行/斉行, 忌む/斎む, 祝う/斎う, 斎く, 故 and 斜; and KanjiVG's actual 揺 SVG.

Verdicts:

Correctness: NEEDS FIX — 提 (G1), 斎 (G2), 揺 (G3); otherwise CLEAN within the reviewed scope.
Scoped coverage: NEEDS FIX — 提's account of チョウ misclassifies an attested example (G1); otherwise CLEAN.
Consistency and quiz safety: CLEAN — no established production ambiguity or unsafe reachable reading option.
Comprehensibility: NEEDS FIX — especially 揺, 斉 and 斎 (G4); 揺 also needs the shape clarification in G3.

| New card | Correctness | Scoped coverage | Consistency/quiz safety | Comprehensibility |
|---|---|---|---|---|
| 挙 | CLEAN | CLEAN | CLEAN | CLEAN |
| 振 | CLEAN | CLEAN | CLEAN | CLEAN |
| 挿 | CLEAN | CLEAN | CLEAN | CLEAN |
| 掌 | CLEAN | CLEAN | CLEAN | CLEAN |
| 推 | CLEAN | CLEAN | CLEAN | CLEAN |
| 描 | CLEAN | CLEAN | CLEAN | CLEAN |
| 提 | NEEDS FIX | NEEDS FIX | CLEAN | CLEAN |
| 揮 | CLEAN | CLEAN | CLEAN | CLEAN |
| 揺 | NEEDS FIX | CLEAN | CLEAN | NEEDS FIX |
| 操 | CLEAN | CLEAN | CLEAN | CLEAN |
| 故 | CLEAN | CLEAN | CLEAN | CLEAN |
| 敵 | CLEAN | CLEAN | CLEAN | CLEAN |
| 斉 | CLEAN | CLEAN | CLEAN | NEEDS FIX |
| 斎 | NEEDS FIX | CLEAN | CLEAN | NEEDS FIX |
| 斜 | CLEAN | CLEAN | CLEAN | CLEAN |

All 24 word changes and the 仮 remark change are CLEAN across the applicable facets. Each word diff is exactly one link-only replacement; the 仮 diff is exactly the declared replacement, and its remaining statement about 遣 agrees with the index. New-card links resolve, titles are unique, selected quiz readings have linked examples, and the reviewed metadata agrees with the pinned records.

Quiz-specific conclusions:

- The cross-card exclusions are symmetric in `QuizBuilder.kt`; one-sided declarations therefore support the reciprocal Notes statements. They are not transitive cliques.
- All 15 meaning-option sets and all 16 selected reading prompts were considered, including reverse-direction sense overlap. No curated option was established as another correct answer.
- 揺's 入/見/休 and 斎's 海/毎/買 are legitimate reading-oriented distractors despite not being look-alikes. 揺's cited verbs illustrate the choice; they are not a promise that every randomly selected reading ends in る.
- The 12 latent reading collisions do not establish shipped-pool exposure. The complete audit reports zero production, Starter-padded and one-holder-padded hits.
- The 斎 イ HIT ignores already-filled slots; サイ receives カイ, マイ and バイ. 故's protected コウ candidate is skipped and fallback supplies a third wrong option. Neither is a content defect.
- Unquizzed name readings and additional historical readings need not all be taught merely because the audit inventories them.

Findings:

1. **G1 — minor; correctness and scoped coverage; `snapshot\kanji\提.md:40,46`. チョウ is not merely an unassignable whole-word reading.**

   The table says no source assigns ちょう to 提 alone and subsequently says チョウ has no ordinary example. Kanjipedia explicitly lists チョウ as an outside-Joyo on reading; the packet's own Kanjipedia JSON does too. Daijisen's actual 提灯 entry is `ちょう‐ちん【▽提▽灯】` and explicitly labels it 唐音. “Hard-to-guess reading” does not establish indivisible jukujikun.

   This incorrectly teaches away the connection between 提 and チョウ in a familiar word. Moreover, “its only JMdict word” is too broad: the pinned families include 提灯行列 (1734790), 提灯持ち (1734800) and others.

   **Remedy:** present チョウ as an outside-Joyo on reading exemplified by 提灯, retain its unquizzed status because no linked article supplies practice, and remove the unsupported exclusivity/indivisibility claims.

   **Evidence:** [Kanjipedia 提](https://www.kanjipedia.jp/kanji/0004972900); [Daijisen 提灯](https://www.weblio.jp/content/提灯); `evidence\kanjipedia-outside-readings.json`; JMdict 1436450 and the compound families above. **Confidence: high.**

2. **G2 — minor; correctness; `snapshot\kanji\斎.md:32`. The blanket “not split between the kanji” statement is unsupported.**

   The paragraph moves from Daijisen's difficult-word listing to claiming that いつきのみこ and いつきのみや cannot be divided between their characters. The actual entries distinguish `いつき‐の‐みこ【▽斎皇＝女／▽斎▽王】` and `いつき‐の‐みや【▽斎宮】`; いつき is also independently attested for 斎. In particular, 斎宮 transparently includes 宮 みや and an unwritten の. Difficult or nonstandard spelling does not by itself make a reading indivisible.

   **Remedy:** retain these as historical word pronunciations but remove the categorical non-segmentation claim. If explaining their parts, distinguish いつき, the intervening の, and the final noun rather than inventing a general reading rule.

   **Evidence:** actual [Daijisen 斎王](https://www.weblio.jp/content/斎王), [斎宮](https://www.weblio.jp/content/斎宮) and 斎 entries. **Confidence: high.**

3. **G3 — minor; correctness and comprehensibility; `snapshot\kanji\揺.md:29,56`. Identify the 缶-shaped part as a reduced variant.**

   The mnemonic and Notes identify the bottom-right shape simply as the linked 缶. That card teaches the complete six-stroke character, whereas modern 揺 has only five strokes in this part: the initial ノ of full 缶 is absent. Treating the linked form as an exact visual component invites a beginner to reconstruct a 13-stroke shape instead of the correct 12-stroke 揺.

   **Remedy:** say “a 缶-like shape without its initial ノ” or “a five-stroke variant of 缶.” Keep the tin-can image; no historical derivation is needed.

   **Evidence:** `snapshot\strokes\揺.json`, strokes 8–12; `repo\kanji\缶.md:6,16`; [KanjiVG 揺](https://raw.githubusercontent.com/KanjiVG/kanjivg/master/kanji/063fa.svg), whose bottom group explicitly marks 缶 as a variant and contains five paths. **Confidence: high.**

4. **G4 — minor; comprehensibility; `snapshot\kanji\斎.md:32`, `snapshot\kanji\斉.md:25`, `snapshot\kanji\揺.md:27,47`. Reference apparatus becomes an uninterrupted phone-reading burden.**

   The core definitions are helpfully first, but the next teaching layer repeatedly becomes a dictionary/audit inventory. The cited 斎 paragraph is approximately 183 whitespace-separated words covering numerous historical readings, princess titles, prefixes, metadata differences and distractor safety without a paragraph break. The 斉 paragraph similarly combines approximately 173 words of compounds, historical geography, reading classifications and rare spellings. 揺 inserts archaic forms and wrong-option assurances before its mnemonic, then packs the official-table inventory into another long paragraph.

   This is a concrete “no wall of text” issue for the specified N5–N4 phone audience, not a request to omit necessary reading coverage.

   **Remedy:** preserve concise, qualified reading rows; move secondary source inventories and audit assurances into short reference bullets at the end of Notes. Keep the principal meaning, mnemonic and practice readings readily scannable.

   **Evidence:** the cited paragraphs and their placement before the principal practice material; the packet's explicit phone/beginner rubric. **Confidence: high for the structural problem; no device usability test performed.**

Optional:

- In 描's source list, add JMdict 2751570 for the quoted すがき gloss “uncolored sketch; line sketch; rough sketch.” The gloss itself is valid; this is citation completeness, not a false definition.
- When shortening the other cards, favor useful compounds and contrastive examples over repeated source disclaimers. No additional finding is made solely from word count.
- Some exclusions are conservatively associative, notably 挿/苗 and 敵/恨. Their pruning could improve option variety, but I established neither a harmful quiz outcome nor a transitive-clique defect and do not require changes to them.

Limits:

- CLEAN means no actionable defect established, not exhaustive linguistic certification. All listed metadata readings received independent public-record checks; detailed live word checks were targeted to consequential reading, sense and register claims rather than every ancillary compound.
- Pinned dictionaries govern snapshot comparisons. Live kanjiapi.dev reports a different grade for 敵 from the pinned grade-6 record; this source-version discrepancy is not treated as a batch defect.
- Stroke geometry was parsed and inspected but not rendered on a device or independently resampled against every source curve. Phone comprehensibility was assessed from the content structure, not an app usability session.
- I inspected the supplied simulations and relevant implementation, not a running Android build. The packet's absent JVM/Kotlin execution remains a known validation limit, not a finding.
- All tool calls were serial, one per response; no agents, other reviews or out-of-packet local evidence were consulted. Oversized responses were reread from their permitted originals, not from generated temporary output files. Apart from the explicitly permitted assignment prompt, the only local output is this report.

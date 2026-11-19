Snapshot: b073abd8f2ab578f29cf2b5e25f36e02fc1aab58, batch 144. Reviewer: OpenAI GPT; the exact model/version identifier is not exposed in this review session. Packet-manifest SHA-256 independently matched `4f9ef67815b2befda589d5202a86046ee89eb69fdc5e647f1a2fd1b65af62a52`.

Scope:

Independent, blind, read-only review of all 15 new kanji cards, their 15 stroke resources, all 18 modified word articles, and the changed 討 passage. Consistency/quiz safety and comprehensibility received the deepest review. Paths below are relative to `batch-144-b073abd8`; “part” identifies material actually inspected rather than claiming that loading a file established review of every line.

- **Full:** `INSTRUCTIONS.md`; `mechanical-checks.md`.
- **Full bytes hashed, contents not substantively reviewed:** `packet-manifest.json`.
- **Part:** `rubric\copilot-instructions.md` (lines 1–280); `repo\docs\content-format.md` (kanji contract, lines 86–155); `repo\docs\confusable-words.md` (lines 1–32 and 308–340).
- **Full, each:** `snapshot\kanji\棋.md`, `snapshot\kanji\棚.md`, `snapshot\kanji\検.md`, `snapshot\kanji\概.md`, `snapshot\kanji\欄.md`, `snapshot\kanji\歓.md`, `snapshot\kanji\殊.md`, `snapshot\kanji\殻.md`, `snapshot\kanji\汁.md`, `snapshot\kanji\沖.md`, `snapshot\kanji\泡.md`, `snapshot\kanji\泣.md`, `snapshot\kanji\淡.md`, `snapshot\kanji\渇.md`, `snapshot\kanji\渋.md`.
- **Part:** `snapshot\kanji\討.md` (lines 75–101, including the changed bullet and its surrounding Notes).
- **Full JSON parsed, each:** `snapshot\strokes\棋.json`, `snapshot\strokes\棚.json`, `snapshot\strokes\検.json`, `snapshot\strokes\概.json`, `snapshot\strokes\欄.json`, `snapshot\strokes\歓.json`, `snapshot\strokes\殊.json`, `snapshot\strokes\殻.json`, `snapshot\strokes\汁.json`, `snapshot\strokes\沖.json`, `snapshot\strokes\泡.json`, `snapshot\strokes\泣.json`, `snapshot\strokes\淡.json`, `snapshot\strokes\渇.json`, `snapshot\strokes\渋.json`. 棋 was also read as raw JSON. All supplied stroke points were independently compared with the corresponding ordered curves in public KanjiVG revision `70a0b7ae0c18ceb5cb358274b029cce0234a43bc`.
- **Full, each:** `snapshot\words\将棋.md`, `snapshot\words\戸棚.md`, `snapshot\words\本棚.md`, `snapshot\words\棚.md`, `snapshot\words\検査.md`, `snapshot\words\検討.md`, `snapshot\words\概論.md`, `snapshot\words\欄.md`, `snapshot\words\歓迎.md`, `snapshot\words\特殊.md`, `snapshot\words\殻.md`, `snapshot\words\汁.md`, `snapshot\words\沖.md`, `snapshot\words\泡.md`, `snapshot\words\泣く.md`, `snapshot\words\淡水.md`, `snapshot\words\渇く.md`, `snapshot\words\渋滞.md`.
- **Full, each:** `diffs\kanji__討.md.diff`, `diffs\words__将棋.md.diff`, `diffs\words__戸棚.md.diff`, `diffs\words__本棚.md.diff`, `diffs\words__棚.md.diff`, `diffs\words__検査.md.diff`, `diffs\words__検討.md.diff`, `diffs\words__概論.md.diff`, `diffs\words__欄.md.diff`, `diffs\words__歓迎.md.diff`, `diffs\words__特殊.md.diff`, `diffs\words__殻.md.diff`, `diffs\words__汁.md.diff`, `diffs\words__沖.md.diff`, `diffs\words__泡.md.diff`, `diffs\words__泣く.md.diff`, `diffs\words__淡水.md.diff`, `diffs\words__渇く.md.diff`, `diffs\words__渋滞.md.diff`.
- **Full:** `evidence\source-metadata.json`; `evidence\provenance.json`; `evidence\joyo-pages.md`; `evidence\kanjipedia-outside-readings.json`; `evidence\daijisen-heads.txt`; `evidence\okurigana-scan.txt`.
- **Part, structured inspection:** `evidence\kanjidic2-records.xml` (complete records for the 15 new characters); `evidence\jmdict-families.xml` (complete entries cited in the 15 cards, plus entries 2504560, 2229800, 2229780, 2647520, 2410350, 2006610, 1284640 and 1284650); `evidence\jmdict-digest.tsv` (lines 1–35 and the first five listed families for each of the 15 characters).
- **Full:** `evidence\public-source\weblio-棋.txt`; `evidence\public-source\weblio-棚.txt`; `evidence\public-source\weblio-渋.txt`.
- **Full:** `evidence\audits\quiz-safety.txt`; `evidence\audits\reading-exposure.txt`; `evidence\audits\reading-options.txt`; `evidence\audits\kanji-remarks.json`; `evidence\audits\word-remarks.json`; `evidence\audits\kanji_remarks.py`.
- **Full:** `evidence\app-code\QuizBuilder.kt`; `evidence\app-code\KanjiMeaningMetadata.kt`.
- **Part:** `evidence\app-code\KanjiReadings.kt` (lines 1–160, including the complete option builder); `evidence\app-code\Words.kt` (matching word-model/exclusion excerpts and lines 216–270, including reading mutations).
- **Part:** `titles\kanji-titles.tsv` (complete index used for exact-title uniqueness checks; relevant comparison/distractor/exclusion rows inspected); `titles\word-titles.tsv` (the 18 scoped word rows and header).
- **Full context cards:** `repo\kanji\権.md`, `repo\kanji\高.md`, `repo\kanji\原.md`, `repo\kanji\穂.md`.

Independent public checks inspected actual entries, not search snippets:

- Jisho's kanji entries for **all 15 characters** independently confirmed every metadata reading, including uncommon readings such as 殻 コク/バイ and 沖 おきつ/ちゅう.する/わく.
- Live Digital Daijisen entries on Weblio were inspected for **all 15 characters**, and for 戸棚, 渇く, 渋い, 渋る and 権.
- Live Kanjipedia entries were inspected for 棚, 検, 概, 欄, 汁, 沖, 泡, 淡, 渇 and 渋, covering the consequential additional-reading claims.
- Jisho's actual dictionary API entries were inspected for **all 18 scoped word headwords**, and for 氷棚, 棚機, 検非違使, 検する, 概ね, 概して, 手すり, 歓ぶ, 合歓, 殊に, 殊な, 船殻, 味噌汁, 沖つ, 沖する, 発泡, 泡立つ, 淡雪, 淡い, 渇す, 渇する, 渋い and 渋る.
- Public source patterns: `https://jisho.org/search/<character>%20%23kanji`, `https://jisho.org/api/v1/search/words?keyword=<word>`, and `https://www.weblio.jp/content/<headword>`. Kanjipedia URLs are the exact entry URLs in the inspected JSON. Public KanjiVG SVGs were fetched from the pinned revision, not current HEAD.

Verdicts:

- **Correctness: NEEDS FIX** — G1 and G2.
- **Scoped coverage: CLEAN** — all metadata readings are represented or explicitly qualified; no essential coverage defect established.
- **Consistency and quiz safety: CLEAN** — for the documented default four-choice questions and audited shipped pools; qualifications below.
- **Comprehensibility: NEEDS FIX** — G3.

| New card | Correctness | Scoped coverage | Consistency / quiz safety | Comprehensibility |
|---|---|---|---|---|
| 棋 | CLEAN | CLEAN | CLEAN | CLEAN |
| 棚 | NEEDS FIX — G2 | CLEAN | CLEAN | CLEAN |
| 検 | CLEAN | CLEAN | CLEAN | CLEAN |
| 概 | CLEAN | CLEAN | CLEAN | CLEAN |
| 欄 | CLEAN | CLEAN | CLEAN | CLEAN |
| 歓 | NEEDS FIX — G1 | CLEAN | CLEAN | CLEAN |
| 殊 | CLEAN | CLEAN | CLEAN | CLEAN |
| 殻 | CLEAN | CLEAN | CLEAN | NEEDS FIX — G3 |
| 汁 | CLEAN | CLEAN | CLEAN | NEEDS FIX — G3 |
| 沖 | CLEAN | CLEAN | CLEAN | CLEAN |
| 泡 | CLEAN | CLEAN | CLEAN | CLEAN |
| 泣 | CLEAN | CLEAN | CLEAN | CLEAN |
| 淡 | CLEAN | CLEAN | CLEAN | CLEAN |
| 渇 | CLEAN | CLEAN | CLEAN | CLEAN |
| 渋 | CLEAN | CLEAN | CLEAN | NEEDS FIX — G3 |

The 18 word edits and changed 討 passage are **CLEAN in all four facets within their scoped changes and inspected surrounding context**. The diffs establish 17 link-only word edits, the declared 特殊 link plus sentence deletion, and only the declared 討 bullet replacement. All added links identify the intended new cards; the retained explanations and examples read correctly.

All 15 stroke resources are **CLEAN for the inspected data**: identities, counts, ordered source correspondence and coordinate checks passed. Maximum endpoint discrepancy against the pinned source was approximately 0.071 units in the 109-unit view box; maximum sampled-point distance from its corresponding source curve was also approximately 0.071 units.

Quiz conclusions:

- All 15 English titles are exact-string unique. Each selected reading has its own linked example. All relative links checked in the 33 complete scoped articles resolve within the packet export. Metadata grades, radicals, stroke counts, reading lists and quiz subsets agree with the pinned records.
- I judged the listed meaning distractors in both directions. The shared 木/氵 distractors do not acquire the target's meaning merely by sharing a component. No displayed default quartet established two correct answers. 殻's choices are unusually easy rather than semantically ambiguous; see Optional.
- The six latent reading collisions are correctly enumerated: 欄 わく; 歓 ぶ; 殊 け; 殻 かい; 沖 とぶ and むなしい. The name-only status of 歓 ぶ is correctly separated. No reachable attested wrong answer was established in the supplied N1/All, Starter-padding or one-holder cases.
- The older audit's 殻 かい “HIT” is not a production hit: 休, 本 and 木 each supply a usable, distinct, nonexcluded kun option, and all three are present in Starter as well. The actual builder fills all three slots before fallback can add 貝's かい. The source code supports the exposure audit's interpretation.
- Shared English substrings do not establish the proposed cross-sense collisions: a **form field** is not bodily **form**; **open sea** is not **split open**; personal **bearing** is not a **grain-bearing head**. Likewise, being **high** is not the action **rise high**, and an open land **plain** is not an unadorned manner. I found no actionable default-question defect from those pairs.
- The exclusions were assessed as direct comparisons, not as transitive synonym classes. Some are conservative contrasts or related confusions rather than interchangeable meanings. I found no demonstrated harmful exclusion requiring a change. 検–討 and 検–偵 have direct investigation support; 検–剖 has the specific examination/dissection connection, including Daijisen's 剖検 example.

Findings:

**G1 — minor; correctness; `snapshot\kanji\歓.md:45` — the shared complex component is put on the wrong side of 権.**

The Notes say 権 “has a similar-looking left part.” 権 has 木 on its left; the complex shape resembling the **left** of 歓 is on the **right** of 権. This is precisely the location a learner needs when distinguishing these two cards.

**Remedy:** Say, for example, “The complex left-hand part of 歓 resembles the right-hand part of 権.” Keep the separate, correct observation that 欠 is on the right of 歓.

**Evidence:** The displayed characters, the reviewed 歓 stroke resource and pinned KanjiVG source, and `repo\kanji\権.md`, which explicitly locates 木 on the left and the dense shape on the right. **Confidence: high.**

**G2 — minor; correctness; `snapshot\kanji\棚.md:25` — the Daijisen nonstandard-reading mark is assigned to the wrong spelling.**

The card describes the shop/rented-house entry as “written with 棚 as a non-standard form.” The actual Daijisen headword is **たな【▽店／棚】**: the ▽ is attached to 店, not 棚. The separate lexical entry and its shop/rental senses are real, but this spelling qualification misreports the source.

**Remedy:** Remove the assertion that 棚 is marked nonstandard. Describe it simply as a separate shop/rented-house word, or reproduce and explain the actual headword marking accurately.

**Evidence:** Independently inspected [Digital Daijisen, 棚](https://www.weblio.jp/content/%E6%A3%9A), specifically たな【▽店／棚】; the same heading is recorded in `evidence\daijisen-heads.txt`. The cached `weblio-棚.txt` contains only navigation/header text, so the live entry—not that cache—establishes this finding. **Confidence: high.**

**G3 — minor; comprehensibility; `snapshot\kanji\殻.md:37`, `snapshot\kanji\汁.md:36`, `snapshot\kanji\渋.md:44` — important reading guidance is buried inside unbroken reference paragraphs.**

Each paragraph mixes several different learning tasks without a visual break:

- 殻 combines the basic noun, がら, electron shells, compound alignment, four additional expressions and spelling/register flags in about 177 whitespace-delimited words.
- 汁 combines the important しる/つゆ restriction, suffix voicing and compound readings with 灰汁/苦汁 and a lengthy chemical definition, in about 152 words.
- 渋 combines the selected reading, okurigana, four adjective senses, verb senses, derived nouns and a search-only spelling in about 153 words.

The problem is not an invented maximum word count: the learner cannot easily locate the practical rule separately from optional dictionary-reference material on a phone. These are walls of prose in the audience's principal reading-help section.

**Remedy:** Split each into short, single-purpose paragraphs or bullets: ordinary reading/use first, the essential contrast next, uncommon spellings/reference expressions last. Shorten repeated English synonym strings, especially the 苦汁 definition. Preserve the sourced reading qualifications and useful common examples.

**Evidence:** The complete scoped paragraphs and the packet's explicit N5–N4 phone-readability mandate. Their underlying dictionary facts are not being challenged. **Confidence: high about the layout/density; medium about the magnitude of learner impact.**

Optional:

- **Nonblocking hardening:** 汁 and 渋 have a real one-directional secondary-sense connection: 渋 can name persimmon juice, and Daijisen also records liquid seeping from something. A future meaning question for 渋 could therefore make 汁's “juice; soup; sap” defensible if fallback became reachable. Both current default questions fill all three meaning distractor slots without the other card, so I have not reported a demonstrated current unsafe question. Consider a direct 汁–渋 exclusion before changing those curated sets or supporting larger/reduced-pool quizzes.
- 殻's 休/本/木 distractors are safe but much less visually instructive than the 殳 comparisons already explained in its Notes. A closer-looking replacement would be an improvement only if the full reading-reachability audit remains clean, including Starter padding.
- For extra English clarity, “plain” on 淡 could be qualified as “unadorned” or “simple.” I did not establish that the current default quiz confuses it with 原's land sense.
- The newly rewritten 討 bullet is true, but “This does not change the complete word's reading” has lost the original missing-card antecedent. Dropping that reassurance would be slightly clearer; it is not an established teaching error.

Limits:

- Exact GPT model/version identity is unavailable to me; I have not guessed a specific version.
- This was a source/content review, not a rendered phone or animation usability test. Stroke data were independently checked against public source curves, but no device result is claimed.
- I inspected the complete supplied simulations and their relevant Kotlin option-building logic; I did not independently reconstruct or scan the approximately 1,412-card production corpus. The zero-hit conclusion is bounded to the documented four-choice pools and evidence, not arbitrary future subsets, option counts or metadata changes.
- Not every supplemental example was independently fetched online. All cited families were checked against the pinned XML; public checks covered every metadata reading, all 18 linked word headwords, and the consequential unusual readings, spellings, senses and registers listed in Scope. Pinned dictionary versions remain authoritative for snapshot-specific flags.
- Initial combined reads of the standards and several cards exceeded the tool's output limit. I did not open the tool-generated external output files; I reread the cards individually and the relevant standards in bounded ranges. The large standards files are therefore listed as partial, not fully reviewed.
- Tool calls were serial, one per tool-bearing assistant response. No parallel calls, subagents, background jobs or other sessions were used. No other reviewer's report or author rationale was sought. No local path outside the packet was opened, and no content file was changed; the only authored file is this report.

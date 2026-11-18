Snapshot: `3b6f972767928e01261440466899f32df398d7f1`, confirming the revision from `a47efe9af926316eaa86656033bf6e109f2be697`. Reviewer: GPT (OpenAI; the exact runtime model identifier is not exposed to me).

Scope:

Independent, blind confirmation of every changed hunk against all four facets, with full rereads of the four revised kanji cards and the revised word article. I also examined the post-fix meaning and reading audits for all 15 batch cards, not just the changed cards.

Files opened in the confirmation packet:

- **Full:** `INSTRUCTIONS.md`, `CHANGES.md`, `RESPONSE.md`, `diffs\fix.patch`, `diffs\changed-lines.txt`.
- **Full:** `snapshot\kanji\{嫁,嬢,宣,峠}.md` and `snapshot\words\宴会.md`.
- **Full:** `evidence\README.md`, `evidence\jmdict-cited-entries.xml`, `evidence\QuizBuilder.kt`, `evidence\extras-correction.txt`, `evidence\word-remarks.json`.
- **Part:** `evidence\KanjiReadings.kt`, lines 1–180, including normalization, selected-reading deduplication, answer construction and queue eligibility.
- **Part:** `evidence\Words.kt`, targeted location matches and lines 211–274, including the complete `ReadingOptions.mutations` implementation.
- **Full:** `checks\{quiz-safety.txt,reading-exposure.txt,reading-options.txt,link-targets.tsv,lint.txt,unittest.txt,validate.txt,budget.txt,vocabulary.txt,manifest.txt,linkplan.txt,kanji-remarks.txt}`.

Files reopened in the original packet:

- `snapshot\kanji\{嫁,嬢,宣,峠}.md` and `snapshot\words\宴会.md`: complete programmatic comparison against the supplied patch and revised files.
- `snapshot\kanji\{宗,宜,宴,寂,密,審,尋,屈,属,岬,崩}.md`: front-matter inspection for the batch-wide regression check; additionally, 宴 lines 46–49, 密 lines 54–57 and 崩 lines 38–41 for the optional-point dispositions. The unchanged bodies retain their initial-round review; they were not all freshly reread.
- `evidence\jmdict-families.xml`: selected complete entries for citation comparison, and the 宣 entries relevant to the のべ/のる assertions; not a new linguistic review of every family.
- `evidence\audits\{quiz-safety.txt,reading-exposure.txt,reading-options.txt}`: complete programmatic comparisons with the revised outputs.
- `evidence\app-code\{QuizBuilder.kt,KanjiReadings.kt}`: complete byte comparisons with the confirmation copies.
- `titles\kanji-titles.tsv`: programmatic lookups for the batch's displayed titles, distractors and newly restated comparison links.
- `repo\kanji\{通,経}.md`: lines 1–16, checking titles and reciprocal exclusion declarations.
- `repo\kanji\{節,隔,請,義}.md`: targeted reference-bullet extraction only, not full card reviews.
- `rubric\copilot-instructions.md`: targeted source/quotation-rule matches, supplementing its full initial-round review.

Fresh independent public verification inspected actual Jisho word-entry responses for 嫁, お嬢様, 嬢ちゃん, 嬢さん, 宣う, 宣べる, 宣べ伝える, 通る and 経る, and the actual Digital Daijisen character entry for 宣 on Weblio. No other reviewer's report was opened.

Dispositions:

- **G1 — RESOLVED** — `峠.md:14,48–49` removes 通/経 from the exclusions, removes the inaccurate sense-overlap grouping, and teaches the noun/verb distinction. Neither context card declares the reverse exclusion. The linked titles match, the added 通る/経る citations support their readings and senses, and the three curated meaning options remain unchanged.
- **Optional 1 — DECLINE ACCEPTED** — reference compression was nonblocking in the initial report. The material still follows the core explanations and is explicitly reference material; inspected precedents in 隔/請 also contain reference inventories. Deferring a consistent format-level improvement is reasonable. This does not certify that the current paragraphs are optimal on a phone.
- **Optional 2 — DECLINE ACCEPTED** — `崩.md:40` accurately names the two metadata selections, not two independently scheduled memories. `ReadingCard.quizReadings` and queue eligibility confirm the shared-stem behavior. Explaining that scheduling distinction in app/format guidance rather than adding an isolated card-specific explanation is reasonable.
- **Optional 3 — RESOLVED** — the requested distinction remains explicit: revised 峠 separates the two senses of English “pass,” and the unchanged 宴 note still says 党 shares only the English word “party.” No new synonym claim was introduced.

Verdicts:

- Correctness: **NEEDS FIX** — 嬢 only, for the new source-quotation mismatch in G2. No other new actionable correctness defect established.
- Scoped coverage: **CLEAN** — the added examples/readings are supported and appropriately distinguished from selected quiz readings; no regression established.
- Consistency and quiz safety: **CLEAN** — G1 is fixed; no new ambiguous actual option established for any batch card.
- Comprehensibility: **CLEAN** — the new distinctions are understandable and do not contradict the surrounding cards. The previously optional density concerns remain nonblocking.

Changed-hunk results:

- **嫁:** the Kansai qualification is attached specifically to JMdict's third, “wife,” sense, matching both the pinned entry and the live entry. It does not incorrectly label the bride/daughter-in-law senses dialectal.
- **嬢:** the new forms and readings are supported; お嬢様's polite-language label is confined to its first sense, and とうさん is correctly distinguished as Kansai honorific usage. The added entry IDs are appropriate. The shortened quoted gloss for じょうさん is the sole new defect identified below.
- **宣:** the live Daijisen entry gives のべる, のる and のたまう. The pinned families support 宣べる as a rare spelling of 述べる and 宣べ伝える as its own entry; the relevant family check found no 宣 spelling read のる. The added sarcastic-use qualification matches both pinned and live 宣う entries. Metadata and selected quiz readings are unchanged.
- **峠:** both the exclusion removal and the new contrast are correct. 頂/山/旬 remain separate, direct peak/mountain guards. “Ordinary wrong options” describes 通/経's eligibility, not a promise that they appear in the full-pool question.
- **宴会:** the revised sentence now introduces `エン + カイ` as readings, rather than making that kana line appear to define a kind of gathering. The surrounding explanation, kana and examples remain coherent.

Verification results:

- Reconstructing each of the five revised files from its original file and `fix.patch` reproduced the supplied revised text exactly after newline normalization.
- The only front-matter change among the four revised cards is the declared 峠 exclusion removal.
- All 59 local links in the five revised articles resolve within the allowed packet overlay. The five quoted kanji titles on changed lines independently match the title index. The eight added Metadata IDs correspond to the newly named words.
- `QuizBuilder.kt` and `KanjiReadings.kt` are byte-identical to their original-packet copies.
- The complete meaning simulation is unchanged, line for line. All 15 cards still have three curated, defensibly wrong meaning alternatives; no target lists one of its own distractors as an exclusion. The initial bidirectional meaning assessment therefore carries forward, with the corrected 通/経 edges now also checked explicitly.
- The reading-audit comparisons independently reproduce the declared differences: exposure lines 1, 46 and 95; options lines 1, 37, 72 and 80. The added extras are 宗/たっとぶ and 宣/のる; no other output line changed.

Batch-wide quiz regression coverage:

| Card | Scheduled reading prompt checked | Post-fix assessment |
|---|---|---|
| 嫁 | kun よめ | Meaning alternatives unchanged; two curated reading slots plus fallback examined. |
| 嬢 | on ジョウ | Meaning alternatives unchanged; ゴ/ミョウ/シ fill the full-pool reading slots. |
| 宗 | on シュウ | Meaning alternatives unchanged; new extra たっとぶ introduces no on-option collision. Name-only し is discussed below. |
| 宜 | kun よろしく | Meaning alternatives unchanged; curated choices and fallback tiers examined; よい remains unreachable in the modeled shipped pools. |
| 宣 | on セン | Meaning alternatives unchanged; two curated reading slots plus fallback examined; new extra のる introduces no on-option collision. |
| 宴 | on エン | Meaning alternatives unchanged; シツ/ヨウ/シュク fill the full-pool reading slots. |
| 寂 | kun さびしい | Meaning alternatives unchanged; curated choices and fallback examined; しずか remains a latent, not shipped-pool, collision. |
| 密 | on ミツ | Meaning alternatives unchanged; ヒツ/ホウ/トウ fill the full-pool reading slots. |
| 審 | on シン | Meaning alternatives unchanged; バン/チュウ/シュク fill the full-pool reading slots. |
| 尋 | kun たずねる | Meaning alternatives unchanged; curated reading variants examined; reported つぐ/つね collisions remain latent. |
| 屈 | on クツ | Meaning alternatives unchanged; curated on-reading variants and Starter fallback examined. |
| 属 | on ゾク | Meaning alternatives unchanged; ソウ/オク/リ fill the full-pool reading slots. |
| 岬 | kun みさき | Meaning alternatives unchanged; 山/田/中 fill all three reading slots in each modeled shipped pool. |
| 峠 | kun とうげ | Meaning alternatives remain 岸/島/上; reading variants and Starter fallback examined. Exclusion removal does not change reading selection. |
| 崩 | kun くずれる | Meaning alternatives unchanged; curated reading variants examined. くずす remains metadata-selected but shares the scheduled くず stem. |

The exposure audit still reports zero production non-name collisions, zero Starter padded-session collisions, zero one-holder padded collisions and eleven latent collisions. I did not reinterpret those eleven hypothetical reduced-pool cases as new production defects.

The `reading-options.txt` 岬/さき HIT remains an overinclusive candidate warning: the source adds curated readings before fallback and stops adding after three wrong slots. The three curated 岬 holders supply distinct usable readings in the reported pools, so 先/さき cannot enter those questions. Conversely, 宗/し can actually be drawn, but the supplied evidence identifies it as name-only, not an ordinary on/kun reading; it does not establish a second correct answer to the on-reading prompt.

Confirmation: **NEEDS FIX** — all four earlier items are resolved or their declines accepted, but the revision introduces the minor quotation defect G2.

Findings:

**G2 — minor — correctness — `snapshot\kanji\嬢.md:47`: the new attributed JMdict gloss omits its qualification.**

**Claim and impact:** the new “Related forms in JMdict” bullet quotes 嬢さん じょうさん as `"(another's) daughter; young lady."` Entry 2230740 instead gives the second sense as `young lady (esp. of respectable upbringing)`. Both the supplied complete entry and the independently inspected live entry retain that parenthetical.

The broad meaning and reading are valid; this is not a fabricated word or a quiz-safety defect. However, the newly attributed quotation silently drops the source's qualification, losing a useful nuance alongside the neighboring お嬢様 comparison and failing the review's source-faithful gloss requirement.

**Remedy:** quote the second gloss as `young lady (esp. of respectable upbringing)`, or make the shortened wording an explicitly unquoted paraphrase. Do not turn “especially” into an absolute usage restriction.

**Evidence:** `evidence\jmdict-cited-entries.xml`, entry 2230740; revised `嬢.md:47`; actual [Jisho 嬢さん entry response](https://jisho.org/api/v1/search/words?keyword=嬢さん), distinguishing the じょうさん entry from the separate とうさん entry.

**Confidence:** High for the quotation mismatch; the impact is minor and limited to source fidelity/nuance.

Optional:

None new. The two accepted deferrals above remain nonblocking.

Limits:

- The exact GPT runtime model/version was not exposed; I have not invented one.
- This confirms the supplied packet, not an independently fetched Git tree or regenerated manifest. Unchanged cards, stroke files and word articles retain their initial-round review except for the explicit regression checks described above.
- The audit outputs are supplied Python analyses, not fresh execution of the Kotlin app. I checked the relevant Kotlin mechanics but did not run Android JVM content tests, the Kotlin cross-check, or the Python audit programs. The supplied 436-test log is evidence of the author's run, not mine.
- Seeded simulations alone do not prove all random outcomes. Some long fallback lists are abbreviated, so I could inspect their tiers, protection logic and reported reachability, not individually inspect every omitted kana candidate. Conclusions about those pools rely in part on the supplied exposure enumeration.
- The extra-reading list is bounded dictionary evidence, not proof that every historical, dialectal or name reading has been enumerated. The modeled Starter cases do not certify every possible combination of multiple borrowed holder cards, future content or arbitrary reduced pools. Labels such as “card text” in these audits also include externally supplied extras, not necessarily literal card prose.
- No phone rendering or animation check was performed. I did not independently count the claimed 184 corpus-wide uses of “Practice selects,” or verify durable tracking of a future format pass; neither is necessary to accept the nonblocking deferrals.
- One bounded verification command stopped on the TSV summary footer after successfully checking the five quoted kanji titles. The remaining citation checks were completed in a subsequent bounded call; no file was changed by either command.
- Exactly one tool call was made per tool-bearing response, serially. No parallel calls, sub-agents, other sessions, background jobs, recursive listings or corpus-article scans were used. The only intentional file write is this report.

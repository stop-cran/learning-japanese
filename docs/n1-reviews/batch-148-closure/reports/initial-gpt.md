Snapshot: `8408b3a5a52cccea74fe2eaf65601568968b6b26` — batch 148. Reviewer: OpenAI ChatGPT, GPT family; the exact runtime model identifier is not exposed to this reviewer. The packet-manifest SHA-256 matches `205a8761609d31bf0edc12f920ef8f98303204050e94baf2366081e7e9c322ea`.

Scope:

All paths below are relative to `C:\Users\romanko\n1-kanji-workspace\review-packets\batch-148-8408b3a5`. Brace lists enumerate individual files. Facets 3 and 4 received the deepest examination; all four facets were considered for every new card.

**Read completely as text:**

- `INSTRUCTIONS.md`; `mechanical-checks.md`.
- `snapshot\kanji\{絞,継,綱,緊,締,緩,緯,縁,縄,縛,縦,織,繕,繰,罰}.md`.
- `snapshot\words\{修繕,組織,絞る,継続,綱,緊張,締める,締め切り,締め切る,緩い,緯度,縁,縄,縛る,縦,繰り返す,罰する}.md`.
- `diffs\kanji__{張,慢,修}.md.diff`.
- `diffs\words__{修繕,組織,絞る,継続,綱,緊張,締める,締め切り,締め切る,緩い,緯度,縁,縄,縛る,縦,繰り返す,罰する}.md.diff`.
- `evidence\source-metadata.json`; `evidence\kanjipedia-outside-readings.json`; `evidence\daijisen-heads.txt`; `evidence\okurigana-scan.txt`.
- `evidence\audits\quiz-safety.txt`; `evidence\audits\reading-exposure.txt`; `evidence\audits\reading-options.txt`; `evidence\audits\kanji-remarks.json`; `evidence\audits\word-remarks.json`; `evidence\audits\kanji_remarks.py`. The script was inspected, not run against an external checkout.
- `evidence\public-source\weblio-{絞,継,綱,緊,締,緩,緯,縁,縄,縛,縦,織,繕,繰,罰}.txt`.
- `evidence\app-code\QuizBuilder.kt`; `evidence\app-code\KanjiMeaningMetadata.kt`.

**Complete programmatic reads, with the following substantive inspection:**

- `snapshot\strokes\{絞,継,綱,緊,締,緩,緯,縁,縄,縛,縦,織,繕,繰,罰}.json`: all JSON parsed; every stroke count, identifier, type and coordinate sequence checked structurally. Independently fetched the 15 corresponding KanjiVG SVGs at revision `70a0b7ae0c18ceb5cb358274b029cce0234a43bc`; compared counts, types, endpoints and relevant component groups.
- `evidence\kanjidic2-records.xml`: parsed completely; inspected the 15 target records and selected comparison meanings.
- `evidence\jmdict-families.xml`: parsed completely; inspected entries cited by the 15 cards, including their spellings, readings, glosses and restrictions. Not every unrelated family was read.
- `evidence\jmdict-digest.tsv`: parsed completely; inspected the header, initial entries and target-family summaries, not every row manually.
- `titles\kanji-titles.tsv`: indexed completely; checked target-title uniqueness and exclusion/distractor titles, including exact candidate lookups.
- `titles\word-titles.tsv`: parsed completely; inspected its header, initial row and the 17 modified articles' title/reading records.
- `packet-manifest.json`: the complete byte stream was hashed; its complete contents were not substantively reviewed.

**Read in part:**

- `snapshot\kanji\張.md`: lines 50–68/to EOF; `snapshot\kanji\慢.md`: lines 69–89; `snapshot\kanji\修.md`: lines 42–60/to EOF.
- `repo\docs\content-format.md`: lines 1–210; `repo\docs\confusable-words.md`: lines 1–48; `rubric\copilot-instructions.md`: lines 1–65.
- `repo\kanji\{経,級,科,筋,犯,期,任}.md`: lines 1–27 of each.
- `evidence\joyo-pages.md`: lines 1–130, including the front matter, and each target character's row plus approximately 12 following lines. Target rows begin at 418, 376, 441, 257, 732, 196, 94, 157, 549, 745, 523, 602, 663, 325 and 783 respectively in batch order.
- `evidence\app-code\KanjiReadings.kt`: lines 1–210; `evidence\app-code\Words.kt`: relevant search matches and lines 212–311.
- `evidence\provenance.json`: first 3,000 characters.

Independent public checks inspected actual entries, not search snippets: Jisho kanji pages for all 15 characters; Jisho word entries for all 17 linked examples, consequential alternate-reading examples and homographs; live Weblio/Daijisen character entries for the 14 characters other than 繰, plus 繰る; Weblio entries for 縁取る, 緊縛, 経, 級, 科, 筋 and 犯; and Kanjipedia's 緊 entry. Entry-specific evidence for findings appears below.

Verdicts:

Correctness: NEEDS FIX — 締, 縁 and 継, findings G1–G3.

Scoped coverage: CLEAN.

Consistency and quiz safety: NEEDS FIX — 綱, 緊, 緯, 罰 and 縦, findings G4–G5. No ambiguous curated default meaning option or reachable attested wrong reading was established in the supplied production-pool results.

Comprehensibility: CLEAN — central ideas and mnemonics are understandable; substantial but nonblocking phone-readability polish remains.

| New card | Correctness | Scoped coverage | Consistency / quiz safety | Comprehensibility |
|---|---|---|---|---|
| 絞 | CLEAN | CLEAN | CLEAN | CLEAN |
| 継 | NEEDS FIX: G3 | CLEAN | CLEAN | CLEAN |
| 綱 | CLEAN | CLEAN | NEEDS FIX: G4 | CLEAN |
| 緊 | CLEAN | CLEAN | NEEDS FIX: G4 | CLEAN |
| 締 | NEEDS FIX: G1 | CLEAN | CLEAN | CLEAN |
| 緩 | CLEAN | CLEAN | CLEAN | CLEAN |
| 緯 | CLEAN | CLEAN | NEEDS FIX: G4 | CLEAN |
| 縁 | NEEDS FIX: G2 | CLEAN | CLEAN | CLEAN |
| 縄 | CLEAN | CLEAN | CLEAN | CLEAN |
| 縛 | CLEAN | CLEAN | CLEAN | CLEAN |
| 縦 | CLEAN | CLEAN | NEEDS FIX: G5 | CLEAN |
| 織 | CLEAN | CLEAN | CLEAN | CLEAN |
| 繕 | CLEAN | CLEAN | CLEAN | CLEAN |
| 繰 | CLEAN | CLEAN | CLEAN | CLEAN |
| 罰 | CLEAN | CLEAN | NEEDS FIX: G4 | CLEAN |

Other reviewed scope and consequential checks:

- All 15 stroke assets: no defect established. Metadata lists, grades, radicals and totals match the pinned records. Modern-shape mnemonics are explicitly distinguished from etymology; the inspected component statements and counts are supportable.
- All 17 word diffs: exactly one link-wrap line each, unchanged visible wording, intended kanji target, and no changed `Dictionary:` line. All three existing-kanji diffs match the declared remark replacements; their revised links and surrounding passages remain correct. No defect established in these 20 diffs.
- Every selected quiz reading has a linked supporting word. 締's `し.める`, 織's シキ through 組織, 繰's `く.る` through 繰り返す and 罰's バツ through ばっする are defensible. The automatic 締 alignment is not grounds to substitute `し.まる`.
- The homographs are kept separate: 緩い ゆるい versus the ぬるい entry, 縁 ふち versus よし and the other nominal readings, and 綱 つな versus biological こう. No wrong-entry reading claim was established.
- Curated meaning distractors were assessed in both directions. 紙 and 終 remain wrong answers despite visual similarity or repetition. 綱/縄 and 継/繕 have genuine overlap and are protected symmetrically by one declaration.
- The tightening group has five protected pairs, not six: 緊/縛 is undeclared on both sides. “Tense; tight; urgent” and “bind; tie up; restrain” distinguish a state from binding/restraint sufficiently that I do not demand another exclusion merely to complete this group. The compound 緊縛 alone would not prove synonymous individual labels.
- The exposure report contains exactly nine latent card/reading collisions: 締–むすぶ; 縁–よる, え, よし; 縛–いましめる; 縦–はなつ, ゆるす, よし; 繰–くり. Its production, padded-session and single-holder checks report no hit, and the reading-options report reports zero problems. Inspection of the option-selection code supports the distinction between an attested reading being available from some holder and actually reaching a wrong-option slot. These latent records are not presented as shipped reading-quiz defects.

Findings:

1. **G1 — minor; correctness — `snapshot\kanji\締.md:40`.**

   **Claim and impact:** “締 supplies しめ” and “切 … supplies きり and きる” confuse whole written stems with the sounds represented by the individual kanji. In 締め切り and 締め切る, 締 represents し, め is kana, 切 represents き, and り/る are kana. This contradicts line 50's correct attribution of き to 切 and teaches incorrect okurigana accounting.

   **Remedy:** Say that the written stem 締め is しめ, and that 切り/切る are きり/きる, with the kana endings distinguished from the kanji. Keep the correct quiz selection `し.める`.

   **Evidence:** The displayed spellings; `snapshot\words\締める.md:25`; the Joyo examples; actual Daijisen entries at [締める](https://www.weblio.jp/content/締める) and [締め切る](https://www.weblio.jp/content/締め切る).

   **Confidence:** High.

2. **G2 — minor; correctness — `snapshot\kanji\縁.md:43,49,59`.**

   **Claim and impact:** For the explicitly displayed spelling 縁取る, line 49 calls どる okurigana. But 取 is written: it represents ど, the voiced counterpart of と, while only る is the following kana ending. The claim also conflicts with the later attribution to 取. This is a spelling-specific error, not evidence that the full word's reading is wrong.

   **Remedy:** Explain 縁取る as 縁＝ふち, 取＝ど, る＝kana ending. If explaining `ふち.どる`, use the attested spelling 縁どる and distinguish it from 縁取る. Preserve the pinned metadata rather than deleting the reading.

   **Evidence:** JMdict entry `1602750` includes 縁取る and 縁どる with ふちどる; the actual [Daijisen entry](https://www.weblio.jp/content/縁取る) has ふち‐ど・る【縁取る】. The displayed spelling itself establishes where kana is present.

   **Confidence:** High.

3. **G3 — minor; correctness — `snapshot\kanji\継.md:25`.**

   **Claim and impact:** “Sense 1 is to take over what follows” reverses the succession relationship in Daijisen's あとを受けつぐ. 継 takes over from what or whom came before; it does not take over a future successor. The correct opening at line 23 makes this a localized but real contradiction.

   **Remedy:** Replace with “take over from a predecessor” or “carry on what came before.”

   **Evidence:** The actual [Daijisen 継 entry](https://www.weblio.jp/content/継), its 継承・後継 examples, and the correct explanation already at line 23.

   **Confidence:** High.

4. **G4 — minor; consistency and quiz safety — association-only exclusions and their explanations.**

   **Locations:** `snapshot\kanji\緊.md:14,54`; `snapshot\kanji\罰.md:14,55`; `snapshot\kanji\緯.md:14,54`; `snapshot\kanji\綱.md:14,53`.

   **Claim and impact:** These particular pairs are justified by association rather than a shared ordinary meaning that makes the displayed titles defensible alternatives:

   - **緊/筋:** tension can affect a muscle, but “tense; tight; urgent” does not mean “muscle; sinew; line; plot.” A whole phrase's reference to muscle tone does not give 緊 a muscle sense.
   - **罰/犯:** “punishment; penalty; divine retribution” and “commit an offense” are consequence and act, not interchangeable meanings.
   - **緯/経:** weft and warp are complementary, distinct directions. The card expressly justifies exclusion because 経 is the “warp partner.”
   - **緯/織:** a weft thread participates in weaving; it does not mean weaving, fabric or organization merely by participating in that process.
   - **綱/科:** a biological class and a biological family are different ranks; “department; course” is not a synonym for “thick rope; hawser; main outline” either.

   These declarations suppress useful valid contrasts and their prose encourages false equivalence. This finding does **not** claim that their removal exposes an ambiguous curated default answer.

   **Remedy:** Remove these five pair declarations and revise the associated overlap claims. Keep useful factual comparisons in the body, but distinguish “associated with/opposite to” from “could also correctly describe this character.” Do not remove genuinely overlapping exclusions wholesale.

   **Evidence:** Actual displayed titles in `titles\kanji-titles.tsv`; inspected comparison-card headers; actual Daijisen entries for [筋](https://www.weblio.jp/content/筋), [犯](https://www.weblio.jp/content/犯), [経](https://www.weblio.jp/content/経), [綱](https://www.weblio.jp/content/綱), [科](https://www.weblio.jp/content/科), and [織](https://www.weblio.jp/content/織). The authoring rule at `repo\docs\content-format.md:124–131` requires actual labels and ordinary meanings; `repo\docs\confusable-words.md:45–46` explicitly distinguishes form similarity from overlapping displayed meanings.

   **Confidence:** High on the semantic distinctions and the absence of the claimed direct overlap.

5. **G5 — minor; consistency and quiz safety — `snapshot\kanji\縦.md:14,53,56`, with context `repo\kanji\経.md:1–27`.**

   **Claim and impact:** In contrast to the excluded 緯/経 pair, **縦/経** has direct semantic overlap but no exclusion on either side. 経's ordinary character meanings include warp/vertical direction, so the 縦 answer title “vertical; lengthwise; at will” contains a defensible answer to an 経 prompt. The 縦 card itself acknowledges the warp sense and the alternate 経 spelling.

   This is a missing semantic guard for supported custom/reduced pools or fallback choices, not a reported collision in the supplied default four-option simulation. For example, a pool containing 経 and 縦 has no pair declaration preventing that choice; the current curated defaults can conceal the gap.

   **Remedy:** Add 経 to 縦's `quiz_exclusions` and explain the shared vertical/warp sense. One declaration is sufficient; do not make a transitive exclusion clique.

   **Evidence:** The actual [Daijisen 経 entry](https://www.weblio.jp/content/経) gives 織物の縦糸 and vertical/north–south senses; the pinned JMdict 縦 family and line 56 corroborate the relationship. `QuizBuilder.kt` applies explicit symmetric pairs, not semantic inference; `repo\docs\content-format.md:117–131` includes custom pools and fallbacks in the contract.

   **Confidence:** High on the semantic overlap and missing pair; the custom-pool consequence is a static code-path assessment, not an executed Android test.

Optional:

- Shorten or split the long reading/source-inventory paragraphs, particularly on 締 and 縁. The central explanations are accessible, but dense lists of rare forms, quotations and audit qualifications make phone reading unnecessarily demanding. Preserve the reading rows and meaningful qualifications.
- Remove learner-facing implementation debugging such as 締's “the quiz tool labels the stem…” sentence. Simply teach the correct reading; keep alignment diagnostics in editorial evidence.
- Soften 繕's “only about mending” comparison: its own examples include grooming, keeping up appearances and covering mistakes. “Repairing or putting things into presentable order” better accommodates the documented figurative uses.
- Repetition of 紙 on eight cards is safe but makes some questions easy and predictable. More varied visual confusables could improve discrimination without sacrificing semantic safety.
- 綱's explanation of 級 via biological “class” deserves clearer wording: distinguish generic rank/grade from a school class rather than relying on an English pun. I have not classified the broader rank relationship as an established additional exclusion defect.

Limits:

- Exact model/version identification was unavailable; none is invented above.
- This was static content/code review, not phone rendering or animation testing. Stroke structure, source types and endpoints were checked, but every intermediate sampled coordinate was not independently regenerated.
- All metadata readings and the linked reading examples received live entry checks. Peripheral compounds were checked against the pinned JMdict families, but not every ancillary word was independently refetched from a second live dictionary. Jisho independently verifies retrieval, but its JMdict/KANJIDIC-derived data is not a separate lexicographic source.
- All supplied Joyo target extracts and Kanjipedia outside-reading records were inspected; Kanjipedia's 緊 page was independently fetched, not every Kanjipedia page. Source-only annotations are judged against the supplied records and corroborating dictionaries.
- Some kanjiapi.dev requests failed with HTTP 403; actual Jisho and Daijisen entries provided alternative verification. Current Jisho presentation can omit search-only spellings such as the ぬるい entry's 緩い; the pinned XML preserves the relevant restriction.
- The nine latent collision records were independently counted and their reachability distinctions inspected, but the complete corpus-level simulations were not rerun. Reported zero-hit totals are corroborated static evidence, not an independent full-device execution or a guarantee for every conceivable reading pool.
- No other reviewer report or author rationale was consulted. Investigative calls were serial, one tool call per response; no agents, other sessions, background jobs or corpus scans were used. No local content outside the authorized packet was opened. The only intentional file write is this report.

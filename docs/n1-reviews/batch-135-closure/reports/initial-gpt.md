Snapshot: `163b384e6cb8f75c06fe395f7b144cdd8b105673` — batch 135. Reviewer: GPT; the exact runtime model identifier is not exposed to me. The packet-manifest SHA-256 matches `9254e071de197bc2ea7cfbe29b3744a3fb68af9cef88788c340e0dd44d79b796`.

Scope:

Independent, blind review of all 15 new kanji cards, all 15 stroke files, and all 32 modified word articles within the assigned change boundary. Facets 3 and 4 received the deepest examination. Paths below are relative to the assigned packet. Brace lists explicitly enumerate filenames, not directories that were scanned.

**Files read in full as review text:**

- `INSTRUCTIONS.md`; `mechanical-checks.md`.
- `evidence\provenance.json`; `evidence\joyo-pages.md`, including the supplied front matter and appendix.
- `evidence\audits\quiz-safety.txt`; `evidence\audits\reading-exposure.txt`; `evidence\audits\reading-options.txt`.
- `evidence\app-code\QuizBuilder.kt`.
- `snapshot\kanji\{博,厳,及,姿,履,巡,弾,彫,恵,憶,我,揚,救,暇,模}.md` — every card, including front matter, readings, examples, mnemonic, comparisons, exclusions and sources.
- `repo\kanji\{求,回,愛}.md`.
- Every diff in this explicit set: `diffs\words__{休暇,博士,博物館,厳しい,厳重,及ぼす,姿,姿勢,履く,巡る,巡査,弾,弾く,弾劾,彫る,彫刻,怪我,恩恵,恵まれる,我々,我慢,揚げる,救う,救助,普及,暇,模倣,模様,知恵,草履,記憶,鷹揚}.md.diff`.

**Files read or processed in part, with the extent specified:**

- `rubric\copilot-instructions.md`: visible text through line 180; not a verified full-file read.
- `repo\docs\content-format.md`: lines 71–139 and 274–289 in detail, plus heading/matching lines elsewhere.
- `repo\docs\confusable-words.md`: lines 1–39 in detail, plus heading/matching lines elsewhere.
- `evidence\app-code\KanjiReadings.kt`: lines 1–155, covering reading normalization, scheduling and option generation.
- `evidence\app-code\Words.kt`: lines 210–292, particularly the reading-mutation helper; also the matching declaration lines.
- `evidence\source-metadata.json`: complete structured parse and comparison of all 15 target records; selected raw text inspected.
- `evidence\kanjidic2-records.xml`: complete XML parse; the 15 target records' relevant metadata inspected and compared. This was not a prose review of unrelated records.
- `evidence\jmdict-families.xml`: complete XML parse; selected card-cited entries' readings, senses, restrictions and register inspected, together with priority-headword coverage. Not every entry in the families received individual semantic review.
- `evidence\jmdict-digest.tsv`: complete structured read for inventory and selected family/headword checks; header and selected records inspected, not every gloss individually.
- `titles\kanji-titles.tsv`: complete structured read for uniqueness, referenced labels and targeted title comparisons. `titles\word-titles.tsv`: complete inventory parse, not a full prose review.
- `packet-manifest.json`: bytes read for SHA-256 verification; manifest contents not individually reviewed.
- `snapshot\strokes\{博,厳,及,姿,履,巡,弾,彫,恵,憶,我,揚,救,暇,模}.json`: complete machine parsing of structure, identities, counts, sequential IDs and finite coordinate pairs; stroke endpoints/types inspected. Not rendered or animated.
- `snapshot\words\{休暇,博士,博物館,厳しい,厳重,及ぼす,姿,姿勢,履く,巡る,巡査,弾,弾く,弾劾,彫る,彫刻,怪我,恩恵,恵まれる,我々,我慢,揚げる,救う,救助,普及,暇,模倣,模様,知恵,草履,記憶,鷹揚}.md`: complete machine reads; metadata, kanji links and changed passages inspected. The unchanged articles were not independently re-reviewed in full.
- The following context files were opened programmatically in full, but only their titles were inspected: `repo\kanji\{薄,協,爆,広,普,識,医,原,厚,減,凜,激,硬,固,難,吸,扱,級,届,至,到,達,且,次,資,委,形,体,状,象,容,影,態,構,像,復,屋,理,靴,着,演,順,川,純,周,循,囲,旅,査,引,単,段,玉,球,圧,劾,責,批,遊,掘,刻,削,専,思,絵,恩,福,幸,利,享,与,贈,徳,賢,億,意,覚,想,念,考,察,記,義,成,画,私,自,身,場,湯,陽,上,掲,昇,起,飛,賛,教,助,丞,援,貯,保,暖,映,歌,休,時,悠,去,暮,墓,横,倣,範,則,型,写,似,漠}.md`.

No other packet file was opened. In particular, I did not read the coordinator's `evidence\public-source\` extracts, another review, or author rationale.

**Independent public verification:**

- Actual Weblio entries, including Daijisen and the available character-reading sections, for all 15 target characters.
- Actual Weblio entries for 博士, 博物館, 厳しい, 厳重, 及ぼす, 普及, 姿, 姿勢, 履く, 巡る, 巡査, 弾, 弾く, 弾劾, 彫る, 彫刻, 怪我, 恩恵, 恵まれる, 知恵, 我々, 我慢, 揚げる, 鷹揚, 救う, 救助, 休暇, 記憶, 模倣, 模様, 規模, お暇 and 草履; additional sensitive entries 甫, 木履, 荘厳, 厳めしい, 及び, 及び腰, 救済 and 弾棋. Weblio URLs use `https://www.weblio.jp/content/` followed by the headword. These checks were entry inspections, not reliance on search snippets.
- Actual Kanjipedia entries for [救](https://www.kanjipedia.jp/kanji/0001400000) and [巡](https://www.kanjipedia.jp/kanji/0003246000), published by the Japan Kanji Aptitude Testing Foundation.
- Public KanjiVG SVGs for 博 and 甫 at revision `70a0b7ae0c18ceb5cb358274b029cce0234a43bc`, files `0535a.svg` and `0752b.svg`; component groups and stroke counts inspected.

Verdicts:

Correctness: **NEEDS FIX** — 博, G3. No other actionable correctness defect established.

Scoped coverage: **CLEAN** — all 15 cards.

Consistency and quiz safety: **NEEDS FIX** — 救 and 巡, G1–G2. The supplied audits' zero-hit conclusion does not cover these independently verified readings.

Comprehensibility: **NEEDS FIX** — 弾, G4; the remaining cards have no established comprehension defect, with nonblocking compression suggestions below.

| Card | Correctness | Scoped coverage | Consistency / quiz safety | Comprehensibility |
|---|---|---|---|---|
| 博 | NEEDS FIX — G3 | CLEAN | CLEAN | CLEAN |
| 厳 | CLEAN | CLEAN | CLEAN | CLEAN |
| 及 | CLEAN | CLEAN | CLEAN | CLEAN |
| 姿 | CLEAN | CLEAN | CLEAN | CLEAN |
| 履 | CLEAN | CLEAN | CLEAN | CLEAN |
| 巡 | CLEAN | CLEAN | NEEDS FIX — G2 | CLEAN |
| 弾 | CLEAN | CLEAN | CLEAN | NEEDS FIX — G4 |
| 彫 | CLEAN | CLEAN | CLEAN | CLEAN |
| 恵 | CLEAN | CLEAN | CLEAN | CLEAN |
| 憶 | CLEAN | CLEAN | CLEAN | CLEAN |
| 我 | CLEAN | CLEAN | CLEAN | CLEAN |
| 揚 | CLEAN | CLEAN | CLEAN | CLEAN |
| 救 | CLEAN | CLEAN | NEEDS FIX — G1 | CLEAN |
| 暇 | CLEAN | CLEAN | CLEAN | CLEAN |
| 模 | CLEAN | CLEAN | CLEAN | CLEAN |

**Other scoped files:** all 32 diffs are CLEAN within their link-wrap-only scope. Each changes exactly one line, wraps the intended first mention with the intended new-card link, and leaves the surrounding text unchanged and readable. The inspected word-card kanji links resolve. All 15 stroke files are CLEAN for the structural and coordinate checks performed; graphical presentation was not tested.

**Adjudication of important leads:**

- Metadata fields agree with the frozen source records. Reading coverage includes explicit qualifications for the retained rare/source-only readings; a current dictionary listing additional readings is not, by itself, a pinned-metadata defect.
- 履's リ example is defensible: Daijisen's `ぞう‐り` supports the segmentation used for 草履. Its bracketed Joyo/appendix status is separately acknowledged.
- 博 distinguishes 博物館's ハク from 博士 はかせ and retains バク. 模 retains ボ and explains 規模 without pretending it has a linked article.
- 及's キュウ distractor readings are skipped rather than displayed as wrong choices. The fallback options were considered; sharing the target's reading is not itself a defect when the option generator excludes it. The same applies to 模's ボ-bearing distractors.
- 恵まれる supplies a legitimate connection to the めぐ stem of 恵む; 憶's lack of a pinned kun reading is not contradicted by mentioning independently qualified outside-source readings.
- Meaning-quiz choices were judged from the displayed titles and ordinary secondary senses, not shape alone. Exclusions such as 救–貯 and 暇–去 can be justified by direct English-answer ambiguity even where the Japanese words are not unrestricted synonyms. I did not establish a transitive-clique or missing-exclusion defect.
- The 19 latent collisions in the supplied audit are not 19 demonstrated production defects. Conversely, that list is not exhaustive: G1 and G2 concern dictionary readings its attestation inventory misses.

Findings:

**G1 — major; consistency and quiz safety; `snapshot\kanji\救.md:9–13` — グ can be marked wrong although it is a reading of 救.**

**Claim and impact:** The on-reading question selects キュウ, but curated distractor 求 can contribute グ. Kanjipedia explicitly lists 救's on-readings as キュウ and the outside-Joyo readings グ・ク. A learner can therefore be offered a second dictionary-correct on-reading and penalized for choosing it.

**Evidence:** `repo\kanji\求.md` has `onyomi: [キュウ, グ]` and no narrower quiz-on list. The 救 block of `evidence\audits\reading-options.txt` explicitly shows `curated 求: きゅう(skipped: excluded) ぐ`. In `KanjiReadings.kt:80–87`, protection derives only from the target's metadata readings and their mutations; グ is absent. Lines 98–110 admit it directly when 求 randomly supplies that reading. A bounded independent reproduction of this logic confirmed that the protected keys do not include `ぐ`. This is a reachable curated-option path in the supplied full pool, not a tiny-pool or merely latent fallback hypothesis. The actual [Kanjipedia 救 entry](https://www.kanjipedia.jp/kanji/0001400000) verifies the reading.

**Remedy:** Preserve the pinned metadata policy, but remove this drawable valid answer: replace the problematic curated provider and verify its replacement/fallback paths, or introduce separately sourced protection for legitimate readings outside the pinned lists. Add a regression covering 救–グ. Merely leaving グ outside `quizOnyomi` does not make it safe as a wrong answer.

**Confidence:** high.

**G2 — major; consistency and quiz safety; `snapshot\kanji\巡.md:10–14` — the fallback can offer the valid kun-reading まわる as wrong.**

**Claim and impact:** The めぐる question can display まわる as a distractor. Kanjipedia expressly lists まわる as an outside-Joyo kun-reading of 巡. The existing meaning exclusion for 回 does not protect the reading quiz.

**Evidence:** The supplied reading-options audit shows that 順 and 純 supply no kun choices, 川 supplies かわ, and the fallback has one tier-4 key, めでる, followed by 284 tier-3 keys. `repo\kanji\回.md` supplies `まわ.る`; under the actual `maxByOrNull` rule this is its first best-scoring reading for めぐる. It scores 3: length within one and matching final る. The target's six protected keys do not include まわる. Thus a permitted shuffled tier-3 ordering can produce:

- correct: めぐる;
- wrong: かわ, めでる, **まわる**.

The code path is `KanjiReadings.kt:98–112`; the mutation helper is `Words.kt:228–241`. I independently checked the relevant target/provider metadata, exclusions and scores without scanning the corpus. 愛 supplies the tier-4 めでる. The actual [Kanjipedia 巡 entry](https://www.kanjipedia.jp/kanji/0003246000) verifies まわる. Its existence does not depend on guessing a reading from お巡りさん.

**Remedy:** Protect the attested reading separately from the pinned teaching metadata, or choose curated providers that safely fill all three kun distractor slots and verify that no allowed path reintroduces まわる. Add a regression for this question. Retaining 回 in `quiz_exclusions` alone cannot fix it because that field is not consumed by this reading-option builder.

**Confidence:** high.

**G3 — minor; correctness; `snapshot\kanji\博.md:27` — the mnemonic adds a dot that 甫 already has.**

**Claim and impact:** “A shape like 甫 with an extra dot at its top right” is an inaccurate component description. Standalone 甫 already contains that upper-right dot. A learner following the instruction literally would add a nonexistent extra stroke.

**Evidence:** The public KanjiVG files at the inspected revision give 甫 seven strokes, including its dot. 博's corresponding upper-right component also has seven strokes, including its dot, above the three strokes of 寸; with 十's two strokes, this totals twelve. The packet's 博 stroke file is consistent with that decomposition. Sources: [博 SVG](https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/kanji/0535a.svg) and [甫 SVG](https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/kanji/0752b.svg).

**Remedy:** Remove “extra”: for example, “a 甫-like seven-stroke shape, including its upper-right dot, above 寸.” Keep the modern-mnemonic qualification.

**Confidence:** high.

**G4 — minor; comprehensibility; `snapshot\kanji\弾.md:25` — the introductory sense catalog is a wall of text before the reading aid.**

**Claim and impact:** One unbroken paragraph presents five ダン senses through sixteen compounds, followed by two counter glosses. Learners encounter this before the mnemonic and reading table, despite the preceding paragraph already introducing the three linked core words. Dense quoted synonym chains make it hard to distinguish the handful of words to learn now from reference-only vocabulary on a phone. This conflicts with the explicit beginner-phone/no-wall-of-text requirement; it is not a request to omit valid metadata readings.

**Evidence:** The paragraph itself runs from 弾琴 and 弾奏 through 指弾, 弾性, six ammunition compounds and the counter senses, without a list break or a core/reference distinction.

**Remedy:** Give the sense overview short bullets with one useful example per sense, retaining kana. Move the remaining dictionary inventory into a clearly secondary reference note after the core teaching content, or omit redundant examples. Preserve the rare-reading qualifications in the reading table.

**Confidence:** high.

Optional:

- Consider the same compression pass for the long source catalogs in 博, 厳, 履, 恵, 揚 and 模. Their central ideas are already stated clearly; repeating extensive dictionary gloss chains immediately afterward adds avoidable reading load. This broader stylistic pass is nonblocking beyond G4's clearest instance.
- Separate learner contrasts from implementation commentary where practical. In particular, describe one question per reading stem without calling a displayed めぐる or あげる answer simply a “めぐ question” or “あ question.” The current explanation is recoverable, but full displayed forms are clearer.
- Extend the reading audit's attestation inventory beyond name readings and standalone JMdict entries. Its existing latent-collision list is useful, but cannot establish safety against legitimate outside-Joyo readings listed by the public character dictionaries.

Limits:

- This is a bounded content review, not exhaustive proof. CLEAN has the packet's defined meaning: no actionable defect established within the inspected scope.
- I did not launch the app, render the cards on a phone, animate the stroke files, or run Kotlin/JVM tests. G1 and G2 are analytical reachability proofs against the supplied builder, supported by bounded independent logic checks; they are not claims of a captured UI session or a newly run full-pool Kotlin simulation. The packet's stated unrun Android/Kotlin checks are not findings.
- Reading questions were interpreted according to the supplied builder's stated contract: pick the on'yomi/kun'yomi of the kanji, with no second valid reading among the wrong options. Nothing in that contract narrows wrong-answer validity to Joyo readings or only the scheduled teaching subset.
- Public dictionaries can legitimately differ from the frozen KANJIDIC2 inventory. G1 and G2 do not demand silently replacing pinned metadata; they identify the separate consequence of drawing those legitimate readings as wrong options.
- Independent public checks covered every target character and the principal/sensitive word readings listed in Scope. I did not individually fetch a live dictionary page for every incidental compound. Remaining checked glosses/restrictions rely on the supplied JMdict records and official-table extracts. Where a Weblio page contains multiple dictionaries, I did not treat a preceding general explanation as Daijisen evidence.
- Some early oversized tool outputs were truncated. I retrieved the needed material in bounded follow-ups and have not represented the remaining partial reads as complete. A Windows text-encoding failure was corrected before using the affected output. An initially overbroad link regex was corrected; the corrected checks passed all 32 modified articles.
- `kanjiapi.dev` returned HTTP 403; actual Weblio and Kanjipedia entries supplied the independent checks instead.
- All tool calls were serial, one per tool-bearing response. No parallel calls, subagents, background jobs, other sessions, recursive listings or whole-corpus scans were used. No other review or author rationale was sought. No local file outside the permitted packet was opened, and the only intentional write is this report.

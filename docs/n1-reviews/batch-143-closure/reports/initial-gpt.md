Snapshot: 6b5934e71945ed215cf57a8291117762e67b1d9e, batch 143. Reviewer: ChatGPT, OpenAI GPT family; the exact model/version is not exposed to me. Packet-manifest SHA-256 independently matches 0958b56bb788c25212c320adad22f17d9155108c276d84728e933a9df16a331b.

Scope:

Independent, blind, read-only review, emphasizing consistency/quiz safety and beginner-phone comprehensibility. Paths below are relative to the supplied packet.

**Files read in full:**

- `INSTRUCTIONS.md`; `mechanical-checks.md`; `rubric\copilot-instructions.md`.
- `snapshot\kanji\施.md`, `旋.md`, `旗.md`, `既.md`, `旦.md`, `旨.md`, `暑.md`, `暦.md`, `朗.md`, `条.md`, `架.md`, `柄.md`, `染.md`, `株.md`, `桜.md`.
- `snapshot\words\一旦.md`, `伝染.md`, `凱旋.md`, `実施.md`, `旗.md`, `既に.md`, `暑い.md`, `朗らか.md`, `条件.md`, `架空.md`, `柄.md`, `株.md`, `桜.md`, `汚染.md`, `蒸し暑い.md`, `西暦.md`, `要旨.md`.
- `diffs\words__一旦.md.diff`, `words__伝染.md.diff`, `words__凱旋.md.diff`, `words__実施.md.diff`, `words__旗.md.diff`, `words__既に.md.diff`, `words__暑い.md.diff`, `words__朗らか.md.diff`, `words__条件.md.diff`, `words__架空.md.diff`, `words__柄.md.diff`, `words__株.md.diff`, `words__桜.md.diff`, `words__汚染.md.diff`, `words__蒸し暑い.md.diff`, `words__西暦.md.diff`, `words__要旨.md.diff`.
- `evidence\source-metadata.json`; `evidence\provenance.json`; `evidence\joyo-pages.md`; `evidence\kanjipedia-outside-readings.json`; `evidence\daijisen-heads.txt`; `evidence\okurigana-scan.txt`.
- `evidence\audits\quiz-safety.txt`; `reading-exposure.txt`; `reading-options.txt`; `kanji-remarks.json`; `word-remarks.json`; `kanji_remarks.py`, all under `evidence\audits\`.
- `evidence\app-code\QuizBuilder.kt`; `evidence\app-code\KanjiMeaningMetadata.kt`.

**Files opened completely for programmatic inspection, rather than full verbatim presentation:**

- `snapshot\strokes\施.json`, `旋.json`, `旗.json`, `既.json`, `旦.json`, `旨.json`, `暑.json`, `暦.json`, `朗.json`, `条.json`, `架.json`, `柄.json`, `染.json`, `株.json`, `桜.json`: identities, counts, ordered stroke IDs, every coordinate's finiteness/bounds, and stroke endpoints inspected. `朗.json` was additionally read verbatim in full.
- `titles\kanji-titles.tsv`: complete index parsed; new-title uniqueness and every batch exclusion/distractor title examined, together with the additional title-overlap leads.
- `titles\word-titles.tsv`: complete index parsed; only its header was displayed/examined, so no additional lexical verification is claimed from this file.

**Files read in part:**

- `repo\docs\content-format.md`: heading/key locations and lines 86–162.
- `repo\docs\confusable-words.md`: lines 1–100.
- `packet-manifest.json`: initial portion attempted; complete bytes independently hashed, not a complete manifest-content review.
- `evidence\kanjidic2-records.xml`: selected batch records' identity, grade, radical, stroke count, on/kun readings and name readings.
- `evidence\jmdict-families.xml`: cited entries' spellings, readings, restrictions, usage flags and senses; complete XML records additionally inspected for 1220240, 1310520, 1391130, 1634480, 2208960 and 2860958. Other family records were not exhaustively reviewed.
- `evidence\jmdict-digest.tsv`: header/initial rows and the first eight priority-ordered family rows for each of the 15 kanji.
- `evidence\app-code\KanjiReadings.kt`: lines 1–120 and function locations elsewhere.
- `evidence\app-code\Words.kt`: function locations and lines 212–272.

Public verification inspected actual Weblio/Digital Daijisen entry text for all 15 kanji, plus 施す, 既に, 旦つく, 旨い, 実施, 凱旋, 一旦, 元旦, 旦那, 要旨, 暑い, 蒸し暑い, 西暦, 朗らか, 条件, 架空, 伝染 and 汚染. Relevant entries for 在, 存, 有, 凱, 歳 and 齢 were also inspected. Live Kanjipedia entries for 旦, 条, 朗 and 柄 were inspected. Retrieval of 染みる initially exposed introductory editorial material rather than its dictionary entry; that material was not accepted as dictionary verification.

Verdicts:

- **Correctness: NEEDS FIX** — G1–G4 below. Per-card exceptions: 柄, 旦, 暑 and 旋 need fixes; no actionable correctness defect established for 施, 旗, 既, 旨, 暦, 朗, 条, 架, 染, 株 or 桜 within the stated verification limits.
- **Scoped coverage: CLEAN** — all 15 cards account for every pinned on/kun metadata reading, with source-only qualifications where appropriate. No mandatory expansion established. Name readings such as 朗「あき」「お」 need not be added as ordinary on/kun teaching rows.
- **Consistency and quiz safety: NEEDS FIX** — G4 affects 既 and 旋. All other new cards, all 17 word diffs and the stroke structures are CLEAN within this review's bounds. No actually drawable attested-reading collision was established in the supplied production/session pools.
- **Comprehensibility: NEEDS FIX** — 柄 and 旦 need the local clarification in G1/G2. The other 13 cards are CLEAN on this facet, with nonblocking compression suggested below.

**Checks supporting those verdicts**

- Every new card's on/kun lists, grade, radical number and stroke count agree with the pinned metadata inspected. Quiz selections have appropriate linked examples; every new-card relative link resolves in the packet.
- All 17 diffs were checked textually and by an independent bounded comparison: 16 are exactly the intended one-link wrap; 西暦 is that wrap plus precisely the declared sentence replacement. Each diff adds exactly one intended kanji link. The edited 西暦 passage is accurate and reads naturally.
- The displayed curated meaning choices are defensibly wrong in both directions. The 方-group curation is particularly reasonable. 日/早/者 are plausible visual distractors for 旨 and 暑 without a competing relevant meaning. 杏 is an apricot, not a cherry tree. 木/本/休 do not supply 柄's meanings or readings.
- A shared English word alone does not establish a missing exclusion: military “standard” versus a normative standard, “carry out” versus carrying an object, and hot weather versus cold/cloudy weather remain distinguishable. I found no demonstrated ambiguous answer among the complete meaning simulation's displayed sets.
- The 株–桜 exclusion works in both directions despite being declared only on 株: the meaning builder checks either card's declaration. It does not create a transitive exclusion clique.
- The reading-exposure count is internally consistent: seven target/attested-reading pairs produce ten prompt-level collisions because 柄's three pairs recur for both がら and え. The complete curated slots prevent those 柄 fallbacks, including in Starter practice. The other named latent readings lose to the reachable higher-tier candidates. The reading-options wording that 柄「ら」“can be drawn” describes a fallback tier, not an available fourth wrong-answer slot.
- I agree with the reported absence of production, padded-session and one-holder hits for the audited pools, based on the complete reports and inspected builder logic. Rare full-metadata readings remain protected even when not selected for questions. The seven part-of-run metadata matches do not establish missing word identities or new character readings.
- Mnemonics are explicitly modern-shape memory aids, not unsupported histories. The changed word articles' example sentences and surrounding explanations present no newly established grammatical or translation defect.

Findings:

1. **G1 — Minor; correctness and comprehensibility; `snapshot\kanji\柄.md:48`.**
   **Claim/impact:** The Common words line pairs **え** with “handle; pattern.” That locally teaches the wrong reading for “pattern,” directly undoing the otherwise helpful distinction elsewhere on the card. The linked article's combined title does not make “pattern” a sense of the え lexical identity.
   **Remedy:** Give separate bullets, e.g. 柄 え — handle; grip, and 柄 がら — pattern; design, linking the same article if necessary.
   **Evidence:** Pinned JMdict 1508290 gives え “handle; grip” and a stalk sense; 1508300 gives がら “pattern; design.” The live [Daijisen 柄 entry](https://www.weblio.jp/content/柄) independently separates those readings and senses. The card's own Readings table already does so correctly.
   **Confidence:** High.

2. **G2 — Minor; correctness and comprehensibility; `snapshot\kanji\旦.md:34`.**
   **Claim/impact:** 旦つく だんつく is presented simply as “husband.” Unlike a neutral vocabulary equivalent, this word carries a belittling tone. A beginner is not warned against using it as an ordinary substitute, although the adjacent 旦那 example receives a register qualification.
   **Remedy:** Add a short qualification such as “disparaging term for a husband,” or omit this unnecessary extra example while retaining 旦那 for ダン.
   **Evidence:** The actual [Daijisen 旦つく entry](https://www.weblio.jp/content/旦つく) defines it as a way of referring slightingly to 旦那. Pinned JMdict 1634480 supplies only “husband” and does not preserve that register information; the public entry therefore materially supplements it.
   **Confidence:** High that a register warning is missing; the precise English tone label can be chosen editorially.

3. **G3 — Minor; correctness; `snapshot\kanji\暑.md:36`.**
   **Claim/impact:** “In 蒸し暑い, 蒸 supplies むし” incorrectly assigns the following kana し to 蒸 itself. This is especially confusing in a paragraph explaining how kanji readings and okurigana divide.
   **Remedy:** Say “蒸 writes む, followed by し; 蒸し is むし,” then retain the correct explanation of 暑い.
   **Evidence:** The spelling and reading むしあつい in JMdict 1356870 and the live [Daijisen entry](https://www.weblio.jp/content/蒸し暑い). The linked `snapshot\words\蒸し暑い.md` already accurately says 蒸 supplies む in 蒸し.
   **Confidence:** High.

4. **G4 — Minor; consistency/quiz safety, plus one false comparison; `snapshot\kanji\既.md:14,48`; `snapshot\kanji\旋.md:14,54`.**
   **Claim/impact:** At least four exclusions are association-based rather than direct meaning confusions: **既–在, 既–存, 既–有**, and **旋–凱**. Existence is not “already; previously”; an existing thing can be new. Triumph is not returning. Moreover, 旋's Notes explicitly group 凱 with characters that “overlap returning,” contradicting the accurate division of 凱旋 elsewhere.
   **Remedy:** Remove these four pairs and correct the Notes. Preserve the genuine return and prior-time/completion comparisons; do not infer an exclusion merely because two characters occur in a relevant compound.
   **Evidence:** The indexed displayed titles are 在 “exist; be located,” 存 “exist; be aware,” 有 “have, exist,” and 凱 “victory song; triumph.” The actual Daijisen entries for [既](https://www.weblio.jp/content/既), [在](https://www.weblio.jp/content/在), [存](https://www.weblio.jp/content/存), [有](https://www.weblio.jp/content/有) and [凱](https://www.weblio.jp/content/凱) support those distinctions. Its [凱旋 entry](https://www.weblio.jp/content/凱旋) expressly attributes victory music to 凱 and returning to 旋. `repo\docs\content-format.md:122–125` requires evidence from displayed labels and ordinary meanings. Current curation prevents a demonstrated ambiguous production question here; the demonstrated effect is unnecessary suppression of valid contrasts and a misleading explanatory claim.
   **Confidence:** High for the four specified pairs; this is not a request to remove every broadly worded exclusion.

Optional:

- Reduce dictionary/audit inventory in learner-facing prose, particularly 条's seven-sense enumeration and 架's long Joyo/alternative-spelling paragraph. Keep the principal contrast, the complete reading rows and the useful examples; consolidate repeated explanations about quiz selection into one short note. This would improve phone scanning without demanding additional content.
- In 朗, “a compressed/modified 良-like shape” would be more visually precise than unqualified “良 at the left.” The supplied 10-stroke diagram has six left-side strokes, unlike standalone 良's usual seven. Kanjipedia recognizes 良 as the related component, so I do not treat the mnemonic's shorthand as an established etymological defect.

Limits:

- No other reviewer report, author rationale, checkout, session or agent was accessed. All calls were serial, with exactly one tool call per tool-using assistant response; no parallel calls or background jobs were issued.
- Some early oversized aggregate tool results were truncated. They were not counted as complete reads; needed card, contract and audit material was subsequently obtained in bounded outputs.
- Public dictionary verification was independent but not an exhaustive live lookup of every compound cited. Pinned JMdict restrictions/senses supply the remaining lexical evidence. Source-only readings, especially 旋「いばり」, 条「チョウ」「デキ」 and 桜「ヨウ」, were verified as pinned metadata, not independently established as ordinary contemporary usage. The cards appropriately do not present them as such.
- The public kanjiapi.dev requests returned HTTP 403, so no independent API corroboration is claimed. Live Weblio material sometimes differs from the frozen source, including additional readings; it was not used to overwrite the pinned metadata.
- I inspected stroke structures/coordinates, not an animated or physical-phone rendering. The complete shipped reading pools were assessed from the supplied audits and builder logic, not independently rebuilt from the approximately 6,400 context files. Arbitrary future content, different clients and every possible multi-borrow custom pool are not certified.
- The four unchanged Dictionary-line warnings were not treated as defects. No Android/Kotlin/device result is claimed, and their stated absence is not a finding.
- All CLEAN judgments are bounded as above, not assertions of exhaustive linguistic correctness or release acceptance.

I found no blocking defects. All three teaching files are CLEAN on all three facets, within the bounded scope below. I made no edits.

**Snapshot:** I reviewed the supplied signed snapshot `38ab6072d2041325142c54cf54be5d126928eb31`, read from the working tree at `C:\Users\stop-\n1-kanji-workspace\learning-japanese`. I had no shell or git access, so I couldn't confirm that the working tree matches that SHA or has no uncommitted changes. No uncommitted teaching was supplied.

**Scope:** Model: Claude Opus 5.5 (`claude-opus-5.5`). This is a single blind initial review covering correctness, scoped coverage and phone-text comprehensibility.
- **Fully reviewed:** `kanji\俸.md` (lines 1–63) and `words\俸給.md` (lines 1–53).
- **Read for context:** `kanji\給.md` (lines 1–45). I reviewed only the added 俸給 Common-words line (line 37) and the behaviour tied to it.
- **Frozen sources, all read in full:**
  - All 42 JMdict families: 16 lexical, 22 comparison and 4 quiz.
  - All 6 KANJIDIC2 records: 給, 年, 付, 俸, 奉, 棒.
  - The pinned KanjiVG SVG for 俸 (U+4FF8).
- **Comparison cards:** kanji 棒, 借, 付, 人; words 給料, 給与, 月給, 収入, 支給, 支払, 払う, 支払う, 代金, 料金, 小遣い, 領収, サラリーマン.
- **Guidance:** `copilot-instructions.md`, `content-structure.instructions.md`, `docs\content-format.md` (lines 1–1405) and `docs\jlpt-levels.md` (lines 1–401).
- **Quiz searches:** titles and distractors for the eleven legacy two-distractor cards, kanji and word title-overlap searches, and `docs\confusable-words.md` (no rows match).
- **Fresh Kotobank retrieval:** the three assigned pages for 俸, 年俸 and 俸給.

**Verdicts:**
- **`kanji\俸.md` (new):** correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
  - Metadata matches KANJIDIC2: ホウ is the sole on-reading, there are no kun-readings, 10 strokes, radical 人 no. 9, grade 8. The SVG also has 10 strokes, drawn as 亻 + 奉.
  - Practice settings: `quizOnyomi: [ホウ]` has its own reading row with a linked example, 俸給. `quizKunyomi: []` is correct.
  - The side form 亻 is explained without changing the radical metadata.
  - The mnemonic is clearly labelled and explicitly disclaims being etymology or a claim about 奉.
  - 年俸 is ねんぽう, and Daijisen states 「ねんぼう」とは読まない. The card treats it as annual basis, not a payment schedule, which matches Daijisen and Nikkoku. JMdict marks 年棒 as irregular kanji usage, as the card says.
  - The 減俸 and 俸禄 glosses match JMdict.
  - Wrong answers 棒 ("rod; stick"), 借 ("borrow, rent") and 付 ("attach") can't reasonably be accepted for "salary; stipend". The kanji title "salary; stipend" is unique.
- **`words\俸給.md` (new):** correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
  - The pair 俸給 / ほうきゅう matches JMdict 1515280, glossed "salary (esp. public employees); wages; pay". The reading splits as ホウ + キュウ.
  - The official-pay association without a government-only limit matches Nikkoku Seisen: 官公吏などの職務… and also 一般に、会社などの勤め人に支給する賃金。給料.
  - Both examples are grammatical, have correct kana and translations, and the を note is accurate.
  - No `jlpt` level is inferred from the kanji. No fixed payroll categories are invented.
  - The nine quiz exclusions are reasonable direct pairs. In my bounded title search, I found no missing guard that the evidence establishes. 料金, 小遣い, 領収 and サラリーマン have different focuses and need no guard.
- **`kanji\給.md` (only the added line 37):** correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN. Its gloss matches JMdict. The other lines are unchanged context and I did not assess them.
- **Reciprocal links:** all four directed links are present with the reading ほうきゅう: 俸.md → 俸給 (lines 22, 34, 40), 俸給 → 俸 (line 30), 給.md → 俸給 (line 37), 俸給 → 給 (line 31).
- **Legacy two-distractor fallback:** none of the eleven cards (人, 休, 何, 入, 出, 口, 女, 日, 月, 男, 買) shares a tag with 俸. None of their titles makes "salary; stipend" a defensible answer.

**Findings:** None.

**Optional:**
1. **`kanji\俸.md` line 59.** "does not make modern 俸給 a payment in rice" assumes the reader knows 俸禄 was often paid in rice. Either say so (as in JMdict's 俸禄米, "rice given as salary") or drop the rice clause.
2. **`words\俸給.md`.** Could say that 給料 is the usual everyday word. I found no register label in the sources; only JMdict's frequency markers differ (給料 ichi1/nf06, 俸給 news2/nf41), so this is unverified as a register claim.
3. **`words\俸給.md` line 31.** Could name the relationship between the two kanji explicitly, for example "reinforcing near-synonyms", as the 給与 article does.
4. **`kanji\俸.md`.** Could cite 字通's 形声 analysis (phonetic 奉), which KanjiVG also marks. Leaving the card as `structure-unclassified` is still valid.
5. **Outside the changed passage.** 月給 is unlinked in `給.md`'s Common words even though `words\月給.md` exists.

**Limits:**
- **Read discipline:** I broke the strict serial rule once. My second response requested `俸給.md` and `給.md` together. All other calls were one per response. Every XML and guidance range stayed within 140 lines.
- **Kotobank (my own retrieval, separate from the frozen XML):**
  - The 俸 page was truncated at 5,000 characters, inside 字通's compound list; the definitions I needed came before the cut.
  - On the 俸給 page, the Daijisen, 字通 and Britannica headings returned attribution only, with no definition text.
  - I did not adopt the historical kun-readings 字通 gives for 俸.
- **Not read:** `strokes\俸.json`, the N1 source-snapshot membership file, and the manifest.
- **Not verified:** git state, validator results or manifest freshness.
- **Quiz checks:** these do not certify larger, random or live choice pools.
- **Text only:** no native-speaker, device or physical-phone evidence was supplied, so this says nothing about glyph rendering or drawing. Compatible Android `f9b59a2` or later is required, and phone/general-release acceptance remains outstanding.

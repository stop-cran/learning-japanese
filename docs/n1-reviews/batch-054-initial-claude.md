**Snapshot:** 4fb51498f6912169499456031380ce2353373397, as stated in the task. There were no uncommitted teaching changes. I had no shell access, so I could not check the Git SHA or the working-tree state myself.

**Scope:** One reviewer, Claude Opus 5.5 (claude-opus-5.5). I reviewed all of `kanji\且.md` (lines 1–55) and `words\且つ.md` (lines 1–51) for correctness, scoped coverage and comprehensibility. I also read:
- **Dictionary families:** all 31 frozen JMdict families (6 lexical, 18 comparison, 4 additive, 3 follow-up).
- **Comparison cards:** 目/日/助 and the words しかも, 更に, また, それに, そのうえ, それと, そして, そうして, そのほか, それから, 勝つ and 目.
- **Guidance:** the review instructions, the content-structure rules, `content-format.md` lines 1–180 and `jlpt-levels.md` lines 1–32.
- **Raw source data:** KANJIDIC2 entries for 一/且/査/助/祖/組/日/目.
- **Archived pages (supplied copies, not fetched fresh):** Digital Daijisen entries for かつ, 且, かりそめ and こうしょ; the Nichigai difficult-readings dictionary entry for 暫且; the Kanjipedia page for 且; and the KanjiVG drawing file for 且 (04e14).
- **Searches:** `confusable-words.md` (with a search, then lines 1–40), similar kanji and word titles across the repository, and the twelve cards the quiz uses as backup choices.

**Verdicts:**
- `kanji\且.md`: correctness **CLEAN**; scoped coverage **CLEAN**; comprehensibility **CLEAN**.
- `words\且つ.md`: correctness **CLEAN**; scoped coverage **CLEAN**; comprehensibility **CLEAN**.

What I checked against the sources:
- **Kanji metadata matches KANJIDIC2.** Readings ショ/ソ/ショウ/か.つ are in source order, with 5 strokes, radical 一 (no. 1), grade 8 and level N1. The KanjiVG file marks stroke 5 as the 一 radical.
- **Quiz settings are correct.** `quizOnyomi: []` and `quizKunyomi: [か.つ]`. The か.つ row links to 且つ, which JMdict 1208840 supports (spellings 且つ/且, "usually kana").
- **ショ is assigned to 且 correctly.** Daijisen's 且 entry gives ショ（慣） and lists 苟且(こうしょ) as its example. JMdict 2847852 marks こうしょ as archaic, and the card labels it "recognition only."
- **ソ and ショウ are handled correctly.** They stay in the metadata and are honestly marked as having no assigned example. The card does not take a reading from a related character (the 俎 note on Kanjipedia) or from part of かりそめ, and it says so.
- **The mnemonic is clearly labelled as not historical.** The 目, 日 and 助 shape comparisons match the stroke data.
- **Both 且つ examples match the sources.** The Daijisen example adds only a comma. The explanations of おもしろく before かつ and of 必要かつ十分な + noun are correct and qualified.
- **"Parallel actions" is supported.** Daijisen gives 「かつ飲み、かつ歌う」 and Kanjipedia gives 「一方で…し、一方で…する」.
- **Nothing is overclaimed.** The article makes no register, frequency or noun-listing claims. 且つ has no inferred word level.
- **Links and quiz exclusions are correct.** There is one reciprocal pair (two directed links). 目.md and 助.md mention 且 without linking it. The nine exclusions are direct pairs, each with a real overlapping sense. 勝つ is only a homophone, so no exclusion is needed.
- **Quiz choices are safe.** None of the twelve backup cards' titles (person, rest, what, enter, go out, mouth, woman, mountain, sun/day, moon, man, buy), or 等 ("equal; and so on"), could pass as "moreover; also." The ordinary meanings of 目, 日 and 助 don't overlap it either.

**Findings:** None.

**Optional:**
1. `words\且つ.md` 18–19 and 45: the parallel-action claim has no example. You could add the attested かつ飲み、かつ歌う with readings and a translation.
2. `words\且つ.md` 19: Kanjipedia actually writes 必要且つ十分な条件. Either keep the source spelling or note the kana adaptation.
3. Exclusions: それから ("after that; and then") is not excluded. Its card and frozen JMdict entry give only the sequence sense, so leaving it out is defensible. Revisit only if its additive sense is added later.
4. `kanji\且.md`: you could mention the character's "for the time being" sense (Daijisen しばらく; Kanjipedia ②), which explains 苟且.
5. `kanji\且.md`: Kanjipedia attributes a pictograph explanation (an offering vessel) to 角川新字源. That could become a hedged, cited origin; the current unclassified tag is not wrong.

**Limits:**
- **Not freshly retrieved:** all archived pages were supplied copies. I made no web fetches.
- **Not read:** `strokes\且.json`, the manifest and validator output, and `confusable-words.md` beyond lines 1–40 plus the search.
- **Text only:** there was no native, device or physical-phone evidence. 苟 is missing from the bundled fonts, so whether it renders through a fallback font is still unknown. Android f9b59a2+ compatibility and general-release acceptance remain outstanding.
- **Quiz audit covers the default four-choice quiz only;** larger quizzes are not certified.
- **One rule breach:** I once sent two read calls in a single response (raw JSON line 13 and the Daijisen かつ page, lines 1740–1759). Every other call was single and serial. No shell, editing or delegation was used.

I found one minor correctness defect, in `words/椋.md`, and no actionable defects in the other three teaching files. This was a read-only review: nothing was edited, committed or written to disk.

**Snapshot:** commit `69640717b7ce459bfe121cc57efcf632ed450db8`, committed content only. No uncommitted teaching changes were included.

**Scope:**
- **Reviewer:** Claude Opus 5.5 (`claude-opus-5.5`), one blind initial reviewer. Every tool call was made one at a time.
- **Teaching files:** I read all of `kanji\笹.md`, `kanji\椋.md`, `words\笹.md` and `words\椋.md` for correctness, scoped coverage and textual comprehensibility.
- **Guidance files:** I read all of `.github\copilot-instructions.md` and `content-structure.instructions.md`, `content-format.md` lines 42–148 and `jlpt-levels.md` lines 1–105.
- **Raw metadata:** I read all of `batch-010-input-metadata.json`. All three source readings are preserved in source order: 笹 ささ (no on-reading), 椋 リョウ and 椋 むく.
- **JMdict packets:** I read every line of all three packets and counted the families: main 34, comparisons 27, supplement 12.
- **Comparison kanji (all lines):** 竹, 世, 苗, 荷, 京, 涼, 村, 相.
- **Comparison words (all lines):** 竹, 木, 植物, 植える, 植木, 草, 鳥, 小鳥, 酒, お酒, 果実, 果物, 実.
- **Live dictionary lookups:** I fetched the six specified Kotobank pages.

**Verdicts:**
- **`kanji/笹.md`:** correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- **`kanji/椋.md`:** correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- **`words/笹.md`:** correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- **`words/椋.md`:** correctness NEEDS FIX; scoped coverage CLEAN; comprehensibility CLEAN.

**Findings:**
1. **Minor; correctness; `words/椋.md:26`.**
   - **Claim and impact:** The article says JMdict "permits むく specifically for 椋", that むくのき "belongs to the listed plant-name spellings", and warns against assuming every spelling takes every reading. This gets the restriction backwards. The likely reading is that 椋 written alone can only be read むく. In fact, JMdict 2216250 restricts only the short reading むく (to 椋). The longer むくのき has no restriction, so it applies to every listed spelling, including 椋 alone.
   - **Remedy:** Say that the short reading むく is restricted to the single character 椋. The longer むくのき applies to all the listed spellings, including 椋 alone. Keep the caution as a statement about むく only.
   - **Evidence:** In 2216250, `<reb>むく</reb><re_restr>椋</re_restr>`, while `<reb>むくのき</reb>` has no `re_restr`. The spellings are 椋木, 椋の木, 樸樹 and 椋.
   - **Confidence:** high on the dictionary structure; medium on how a learner would read the sentence.

**Checked and found sound:**
- **Readings and links:** The two quizzed readings, ささ and むく, each have a reading row and a useful linked word article. On-reading questions are switched off for both cards; 椋 keeps its source reading リョウ in the metadata. JMdict does not list 椋樹, but 字通 does, under 【椋樹】りようじゆ; that is old full-size kana for りょうじゅ.
- **笹 entry (Seisenban Nihon Kokugo Daijiten):** The heading is ささ【笹・篠】.
  - Sense ① describes the plant and notes that sasa keeps its sheaths, unlike bamboo. JMdict 1956300 agrees.
  - Sense ② is (酒), a court ladies' word for sake. JMdict 2862891 lists that sense under the spelling 酒, marked "dated".
  - 字通 calls 笹 a kokuji (a character made in Japan) and says its origin is unclear.
- **椋 entry (Daijisen and Seisenban):** Both give the tree, its fruit, and a short form of ムクドリ (starling).
- **Tree and bird pages:** The 椋の木 page confirms a deciduous tree with rough leaves used for polishing; むく is listed as another name. The 椋鳥 page explains the bird's name by its liking for muku fruit. The 笹舟 page confirms the leaf-boat meaning.
- **Kana spelling:** The kana-writing notes match JMdict's "usually written in kana" flags for 椋鳥 and 熊笹.
- **Example sentences:** They are grammatical and correctly translated.
- **Quiz exclusions:**
  - Each exclusion is a direct pair, matched against the other word's real title: 竹 "bamboo", 草 "grass; weeds", 植える "plant", 植木 "garden tree; potted plant", 木 "tree; wood", "fruit", "bird", "alcoholic drink".
  - I found no exclusion clique and no applicable pair in `docs\confusable-words.md`.
  - The kanji-card distractors are clearly distinct in meaning, and 竹 is left out of 笹's distractors.

**Optional:**
- **椋 phonetic component:** 字通 classifies 椋 as a phonetic compound with 京 as the sound part, shared with 涼 and 諒 (リョウ). The card could mention this as sourced background beside the `structure-unclassified` tag and the 涼 comparison. The current mnemonic disclaimer is still accurate.
- **"Older dictionaries" wording (`words/笹.md:36`):** The source is a modern dictionary recording historical usage. "Dictionaries record an older court-ladies' word" would be clearer, and "nyōbō kotoba" could be glossed.
- **Kana spellings for learners:** 笹身 is usually written ささみ or ささ身 (JMdict lists ささ身 first and flags it as usually kana). The tree is often written ムクノキ, which the 椋 kanji card's 椋の木 line could also note.
- **Season-word use:** The fruit and bird uses of 椋 are marked as season words (autumn) in Daijisen and Nihon Kokugo Daijiten. The bird example is from a haikai poem. A register hint is possible but not established as required.
- **Second reading of 椋樹:** A plant-name dictionary also reads 椋樹 as ムクノキ. This does not invalidate りょうじゅ.

**Limits:**
- **Kotobank extraction:** For the 笹 and 椋鳥 entries, the Daijisen sections returned only headings. The 椋鳥 page's 字通 and plant-name dictionary sections, and the plant-name dictionary section on the 笹 and 椋 pages, also had no body text. Their verification rests on Seisenban Nihon Kokugo Daijiten, 字通 and JMdict.
- **Partial read:** `docs\confusable-words.md` was searched with two grep queries, not read in full.
- **Files not consulted:** I did not consult `n1-source-snapshot.json`. Comparison articles were read only for these pairs.
- **What this review is not:** It is textual only, with no phone execution, native-speaker check, or measurement of frequency or learning effect.
- **Instruction overlap:** The content of `copilot-instructions.md` and `content-structure.instructions.md` was also supplied in my session context before I read the files. No other reports, author records or rationale were read.

I found no actionable defects in the four batch 006 files. Every facet of every file is CLEAN.

**Snapshot:** The task names 8602dc702dccc11de5fbcccace4ba204fafb930e (base 45d973442c19e0a0b73e9fe7fece453fdb066536), plus the evidence-only `docs\n1-reviews\batch-006-input-metadata.json`. I read the files in the working tree. Without a shell I couldn't confirm that the checkout matches that commit or that there are no uncommitted changes. The metadata file's own snapshot field matches the commit.

**Scope:**
- **Reviewer:** Claude Opus 5.5, working alone, one read-only tool call at a time. I made no edits.
- **Read in full:**
  - The four in-scope files: `kanji\栗.md`, `kanji\梨.md`, `words\栗.md`, `words\梨.md`.
  - All four dictionary packets: 7 + 9 + 1 + 1 = 18 dictionary families.
  - The input metadata file.
  - Kanji comparison cards: 西 要 相 利 村 木 園.
  - Word comparison articles: 木 植物 植える 果物 果実 実 木材 材木 茶色 茶色い 植木 大木 桃 無し.
- **Partial read:** `docs\content-format.md` lines 40–157 only.
- **Other checks:**
  - A search of kanji card titles: "chestnut" and "pear tree" are each used only once.
  - Four Kotobank pages: 栗, 栗色, 梨, 梨園.
- **Not read:** other review reports, progress records and the author's evidence notes.

**Verdicts (correctness / scoped coverage / comprehensibility):**
- `kanji\栗.md`: CLEAN / CLEAN / CLEAN
- `kanji\梨.md`: CLEAN / CLEAN / CLEAN
- `words\栗.md`: CLEAN / CLEAN / CLEAN
- `words\梨.md`: CLEAN / CLEAN / CLEAN

**Findings:** None. The checks behind this result:

- **Metadata:** Both cards keep the full reading lists from the source exactly, in order: 栗 has on リツ, リ and kun くり, おののく; 梨 has on リ and kun なし. Every reading has its own table row. Name readings were not reviewed, as instructed.
- **栗 rows that are kept but not taught:**
  - The リツ and リ rows correctly mark these as kept from the source with no example word.
  - The おののく row correctly says the dictionary's trembling verb おののく is spelled 戦く/慄く (entry 1390130), not 栗.
- **Claims checked against dictionaries:**
  - **栗:** The Seisenban くり entry supports tree and nut (sense ①), including other cultivated chestnuts such as アマグリ and ヨーロッパグリ. It also supports timber (②) and an abbreviation of 栗色 (③).
  - **栗色:** Daijisen defines 栗色 as 栗の実の皮のような焦げ茶色, a dark brown like the chestnut's skin, so "chestnut brown" is correct.
  - **梨:** The Seisenban なし entry ① says the word can also cover 西洋梨や野生種 (European pears and wild species). The Daijisen character heading gives 音リ / 訓なし and lists 梨園.
  - **梨園:** Seisenban gives ① pear orchard and ② 演劇界, 特に歌舞伎役者の世界 (the theatrical world, especially kabuki). This supports the card and its "not every occurrence literally" hedge.
  - **Other words:** 洋梨, 西洋梨, 栗色 and the rarely used 梨子 all match their dictionary entries. The "usually written in kana" notes are correctly attributed to the dictionary.
  - **Example sentences:** These are natural, and the translations are accurate.
- **Links:** The kanji card and word article link to each other in both directions, for both 栗 and 梨.
- **Kanji wrong answers:** 栗 uses west, necessity; essentials, and mutual; aspect. 梨 uses benefit; advantage, village, and mutual; aspect. None of these overlaps an ordinary sense of chestnut or pear.
- **Word exclusions:** These are justified by the actual senses: tree, plant, plant (verb), fruit, fruit/nut, timber (栗 sense ②) and brown (栗 sense ③). 梨 correctly leaves out timber and colour. 植木, 大木, 桃 and 無し need no exclusion: none of their titles is a reasonable answer for 栗 or 梨, and 無し is only a homophone.
- **Reading questions:** Only 栗 kun くり and 梨 kun なし would be asked; all on'yomi questions are disabled. Each matches its own row and linked word. Both are the standalone, high-priority native nouns, so the questions suit learners.
  - Turning off リツ and リ for 栗 is justified because the reviewed sources give no modern example word. Leaving out おののく is justified because the dictionary's verb isn't spelled with 栗.
  - Turning off リ for 梨 is a reasonable choice: 梨園 is a specialised word, though a real one. All full readings stay protected from being used as wrong answers.

**Optional:**
- `kanji\栗.md:22`: "name-use classification" could say "jinmeiyō (name-use) list".
- `kanji\梨.md:30`: could add that 梨園 is a somewhat elegant/literary term (Nipponica calls it 雅称) and that the literal "pear orchard" sense exists.

**Limits:**
- **Dictionaries:** The dictionary packets were supplied to me, not fetched live. The Kotobank pages were live fetches. The Daijisen bodies for 栗 and 梨園 did not come through in the page text, so I relied on Seisenban there.
- **Not assessed:** how common the kanji spelling is in practice, and the historical origin of either character.
- **Not certified:** this was a text review only. It does not certify app behaviour, phone display, native-speaker judgement or learning results.

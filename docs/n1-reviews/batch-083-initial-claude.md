**Snapshot:** 4b8bfcc4bc4fff4c73185a8cc6c27d4cb5736efc, as provided in the packet. I did not check Git or upstream sources myself. Uncommitted state is unknown.

**Scope:** A read-only first-pass text review. One reviewer: Claude Opus 5.5 (`claude-opus-5.5`). I read one resource, `control\batch-083-initial-packet.txt`, with one `view` call (`forceReadLargeFiles=true`, no range).
- **Reviewed:** the new `kanji\凌.md` (1–61), `words\凌ぐ.md` (1–52) and `words\凌駕.md` (1–53), plus the diff.
- **Used as evidence only:** the 14 unchanged comparison bodies, the 42 distinct JMdict families (44 occurrences), the eight KANJIDIC2 records with their flags and restrictions, the stroke JSON, the instruction excerpts and four supplied Kotobank observations.

**Verdicts:**
- `kanji\凌.md`: correctness CLEAN; scoped coverage CLEAN; text comprehensibility CLEAN.
- `words\凌ぐ.md`: correctness CLEAN; scoped coverage CLEAN; text comprehensibility CLEAN.
- `words\凌駕.md`: correctness CLEAN; scoped coverage CLEAN; text comprehensibility CLEAN.

CLEAN means I found no actionable defect. It does not mean the cards are exhaustively correct.

**Findings:** None. These checks found no defect:

- **Metadata (凌.md 1–13):** All metadata matches the 凌 KANJIDIC2 record: grade 9, 10 strokes, radical 冫 no. 15, JLPT 1, on リョウ and kun しの.ぐ.
  - Both readings are selected. Each has its own reading-table row (36–37) linking a real word.
  - No name readings (nanori) or 駕 readings (including 駕's しのぐ) were imported.
  - Strokes 1–2 in the stroke file are the two 冫 marks, which supports the description on line 18.
- **Reading allocation (凌駕.md 26–29):**
  - りょう+が is supported separately for each kanji: 駕 lists ガ as an on-reading in KANJIDIC2.
  - Daijisen's 駕 entry, sense 2, gives "rise above others" with 凌駕 as its example. So the card's account of the meaning is sourced, and it says not to use the vehicle meaning.
- **Word data:**
  - 凌ぐ: JMdict 1554200 lists it as a transitive verb ending in ぐ. The forms しのぎ/しのいで/しのいだ/しのがない are correct.
  - The contrast with 忍ぶ (しのぶ, ending in ぶ, so しのんで) is correct.
  - 凌駕: JMdict 1606270 lists it as a noun, a する-verb and transitive. 陵駕 is correctly described as a rarely used spelling, not a rare pronunciation.
  - 優れる is correctly called intransitive (JMdict 1539080).
  - 上回る's "esp. figures" use is fairly described as "also suits."
  - Neither word has a JLPT level.
- **Meaning distinctions:**
  - 風雨を凌ぐ is presented as protection from weather. 前作を凌ぐ傑作 is presented as better quality. 前作を凌駕する売れ行き is presented as higher sales, not artistic quality.
  - All three phrases appear in the supplied Daijisen observations.
  - The cards add no unsourced rule about temporary-only use, permanent solutions or formal register. 凌ぐ.md 45–46 hedges both ways, consistent with the 一時しのぎ and 糊口を凌ぐ entries.
- **Shape notes:**
  - The mnemonic is clearly labelled as modern-shape memory aid, not history.
  - `structure-unclassified` does not deny a phonetic component.
  - Grade 9 is handled correctly: it does not make しのぐ a name-only reading.
  - The JLPT level is labelled as a community list, not official.
- **Wrong kanji choices:** 准 ("quasi-; associate rank"; also ratification), 冶 ("smelt"; also 陶冶, cultivation) and 次 ("next"; also order or sequence). None of these overlaps with endure or surpass.
- **Word quiz exclusions:** There are 17 direct pairs, and each matches a real endurance or surpassing gloss. 凌駕 correctly does not exclude こらえる or 我慢 (exclusions are pairwise, not chained). Excluding 超過 and オーバー is cautious and harmless.
- **Links:**
  - Both kanji–word pairs link in all four directions.
  - The ten extra navigation links are present: 凌ぐ↔凌駕, 凌ぐ→こらえる, 凌ぐ→我慢, 凌駕→優れる, and 凌→准/冶/台/次/欠.
  - 駕, 上回る and 忍ぶ appear as plain text with kana.
  - The cards are new, so no existing identities, readings, levels or exclusions changed.

**Optional:**
- `words\凌ぐ.md:20`: "keep out wind and rain" would be closer to JMdict's wording than "shelter from."
- `words\凌ぐ.md:15–17`: could briefly mention JMdict sense 3's "defy; slight." This is not required.

**Limits:**
- **Read scope:** The single `view` returned the packet through its final scope paragraph with no truncation marker, so I did no recovery reads. The tool showed no byte or line counts, so I could not confirm the 166,941 bytes / 3,425 lines myself.
- **Unverified links:** That 台.md and 欠.md exist is inferred only from links in other cards.
- **Not checked:** I checked the 凌 kanji title only against 准/冶/次. I did not check whether it or the word titles are unique across the corpus, or how the quiz behaves when it fills extra choices itself.
- **No other evidence:** I have no evidence from native fonts or drawing, the app UI, a physical phone or measured learning effectiveness.

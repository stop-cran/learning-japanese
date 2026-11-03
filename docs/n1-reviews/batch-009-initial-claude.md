Snapshot: 09e480adadc433f54cdbe20e3691ab38126bb711. No uncommitted teaching changes were included. I did not run Git, so this commit is the one given in the task, not one I checked myself.

Scope: Reviewer: Claude Opus 5.5 (ID `claude-opus-5.5`), one blind initial reviewer working read-only. I made one tool call per response and saw no overlapping calls.

Files read in full:
- `.github\copilot-instructions.md` and `content-structure.instructions.md`
- `docs\content-format.md` lines 42–148 and `docs\jlpt-levels.md` lines 1–105
- The four teaching files: `kanji\杏.md`, `kanji\李.md`, `words\杏.md`, `words\李.md`
- `batch-009-input-metadata.json`
- `batch-009-jmdict.xml` (44 entries) and `batch-009-comparisons-jmdict.xml` (22 entries)
- Comparison kanji: 古, 村, 相, 子, 木, 口, 下, 梅
- Comparison words: 梅, 桃, 木, 植物, 植える, 植木, 果物, 果実, 実

`confusable-words.md` and the `title:` lines in `words` and `kanji` were only searched, not read in full. All three facets were reviewed: correctness, scoped coverage and comprehensibility.

Verdicts:
- `kanji\杏.md`: correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- `kanji\李.md`: correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- `words\杏.md`: correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- `words\李.md`: correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.

What supports these verdicts:
- **Readings match the source.** 杏 has キョウ, アン, コウ and あんず in source order. 李 has リ and すもも. Nanori (name readings) are left out. Both cards use `quizOnyomi: []`, so on-reading questions are off. The quizzes ask only あんず and すもも.
- **Each asked reading has a reading-table row and a linked word article.** Those words are JMdict 1586930 (杏/杏子 あんず) and 1549830 (李 すもも; 酢桃/酸桃 marked rare; Prunus salicina).
- **The unasked on readings each have a real word.** キョウ/アン: 杏仁 and 杏仁豆腐 (both readings in JMdict 1154990 and 2101710). Seisenban says the あん of あんにん is the 唐宋音 (a later Chinese-derived on reading) of 杏. リ: 李下 (JMdict 2826232, Daijisen, Seisenban).
- **コウ is labelled as KANJIDIC2-only** ("no word example established in this lesson"). That does not claim the reading never occurs.
- **The 杏子 and 銀杏 whole-word readings are handled correctly.** The cards don't take ず or other readings from them as standalone readings.
- **The botanical scope is accurate.** It matches Nipponica and Sekai Daihyakka: European plums are often grouped under スモモ, and ヨーロッパ李 has its own JMdict entry, 1969470.
- **The proverb and its literal explanation match** JMdict 1549840.
- **The mnemonics are labelled as modern-shape memory aids.** The component descriptions of 古, 村 and 相 are accurate.
- **The word-quiz guards are justified.** 杏 and 李 each exclude 梅, which has the overlapping title "ume; Japanese apricot". They also guard 木, 植物, 植える ("plant"), 植木, 果物, 果実 and 実. 杏 against 李 and either against 桃 need no guard. Titles such as ジャム ("fruit jam"), 並木, 大木, 実る and 生る are not answers someone could defend.
- **No vocabulary level is inferred** for the two support words.

Findings: None.

Optional:
1. `words\李.md` (example 2) and `kanji\李.md` (Common words, 李の花) translate this as "plum blossoms". In English that phrase usually suggests 梅の花. "Japanese plum (sumomo) blossoms" would match the page's own warning about English labels. JMdict 李花 also glosses it as "plum blossoms", so the current wording is not wrong.
2. In `kanji\杏.md`, the reading table and Common words call 杏仁豆腐 "Chinese-style almond jelly" without qualification. The word article says "often translated", which is clearer. A short "(named for apricot kernels)" would explain why an apricot kanji leads to "almond".
3. Possible kanji-quiz overlap (not a defect): if fallback choices appear, "Japanese plum" (李) or "apricot" (杏) could be argued as answers for 梅. Kanji cards have no exclusion mechanism. Today all three cards curate three distractors, so the default four-choice quiz doesn't use fallback. The titles follow JMdict and KANJIDIC.

Limits:
- **Not fetched:** the optional Kotobank pages for 杏仁豆腐 and あんず.
- **Fetched but truncated:** the 杏仁 page (Seisenban/Daijisen headings checked; some dictionary panels empty), the すもも page (Nipponica and Sekai read; later panels not) and the 李下 page (the definitions were read in full).
- **Not checked:** distractor counts on other N1 cards that could show 杏 or 李 as fallback choices.
- **Not run or verified:** `validate.py` and the manifest (no shell), strokes JSON, phone rendering, native-speaker judgement, frequency and learning effectiveness. This is a text-only review.

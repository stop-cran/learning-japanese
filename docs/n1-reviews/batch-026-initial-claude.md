I found no actionable defects in `kanji\鶴.md` or `words\鶴.md`; all six facet verdicts are CLEAN. One process breach: during step 1 I issued three reads in a single response, against the one-tool-call rule. The reports below are unaffected, but the read wasn't fully serial.

**Snapshot:** Frozen batch026 at `e6c59b6b80af44320f5a5cfe0a8cf0961643b8c1`, worktree `C:\Users\stop-\n1-kanji-workspace\learning-japanese`. No uncommitted teaching included. Without a shell I couldn't confirm that HEAD equals this commit; I relied on the task's statement.

**Scope:** Single reviewer, Claude Opus 5.5 (as exposed). Read-only.
- **Rules read:** `.github\copilot-instructions.md` 1–160 and 161–244; `content-structure.instructions.md` (complete); `docs\content-format.md` 42–148; `docs\jlpt-levels.md` 1–160, 161–300 and 301–386.
- **Teaching files:** `kanji\鶴.md` and `words\鶴.md`, complete.
- **Metadata:** `batch-026-input-metadata.json`, complete, including the raw KANJIDIC2 element.
- **Dictionary packets:**
  - `batch-026-jmdict.xml`: lines 1–200, 201–400, 401–600 and 601–748 (44 families).
  - `batch-026-comparisons-jmdict.xml`: lines 1–200 and 201–389 (12 families).
  - `batch-026-support-comparisons-jmdict.xml`: lines 1–14 (1 family).
  - Total: 57 families; every line returned.
- **Comparison kanji:** 確, 観, 権, 鷹, complete.
- **Comparison words:** 鳥, 動物, 鷹, 見る, 紙, 折る, complete.
- **Searches:** a scoped grep of `docs\confusable-words.md`, and a grep for overlapping bird titles in `kanji\` and `words\`.
- **Independent lookup:** one Kotobank fetch of the 鶴 entry.

**Verdicts:**
- **`kanji\鶴.md`:** correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- **`words\鶴.md`:** correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.

What I checked to reach those verdicts:
- **Metadata:** The card matches KANJIDIC2: 21 strokes, radical 196, grade 8, readings カク then つる.
- **Quiz readings:** `quizOnyomi: []` and `quizKunyomi: [つる]` are exact subsets. つる has its own reading row with a link to the word article.
- **カク:** It is kept as a recognition reading through 鶴翼 かくよく. JMdict 2858035 gives "V-shape (battle formation)" and "crane wings". The supplied 精選版 senses match "crane wings; also a wing-shaped battle formation".
- **たず/たづ:**
  - JMdict 2855588 lists 田鶴/鶴 with readings たず and たづ, marked as a poetical term.
  - I fetched Daijisen myself: its heading たず〔たづ〕【▽鶴／田▽鶴】 calls it 歌語 (a poetic word).
  - So "poetic … たず (historically たづ)" is supported. The card offers it as a separately documented word, not a quiz reading.
- **折り鶴:** JMdict 1784750 gives 折り鶴 / 折鶴, read おりづる. The づる note describes only this compound.
- **Stork:** The card rightly says KANJIDIC2's "stork" gloss doesn't make the bird names interchangeable. コウノトリ is a separate JMdict entry (2079550). The 精選版 entry I fetched says the "crane on a pine" motif is a misidentified コウノトリ.
- **Shape mnemonic:** It is labelled as a mnemonic and correctly places 鳥 on the right.
- **Example sentences:** 鶴を見ました and あの鳥は鶴です are natural, and their translations are accurate.
- **Word front matter:** No vocabulary `jlpt` is given, so none is inferred from the N1 kanji. The type is wago and `kanji: [鶴]`.
- **Links:** The kanji card and word article link to each other. All linked comparison files exist.
- **Kanji distractors:** "certain", "view; observe" and "authority; rights" don't overlap with "crane (bird)". The component descriptions (石 left, 見 at the end, 木 left) are accurate.
- **Word exclusions:** Excluding 鳥 "bird" and 動物 "animal" is justified, because each could be accepted as a broader answer. 鷹 "hawk; falcon" and 小鳥 "small bird" don't need exclusions. `confusable-words.md` has no applicable pair.

**Findings:** None.

**Optional:**
1. **`kanji\鶴.md` (Notes):** 確's right side contains the same visible part (隺) as 鶴's left side, and both have the on-reading カク. Saying "the same part appears on the other side in 確" would make this distractor's comparison sharper. Describe it as visual only, with no phonetic claim.
2. **`words\鶴.md` (Distinctive meaning):** "クレーン (くれーん)" is an odd hiragana rendering of a katakana loanword. It could simply be dropped.
3. **`kanji\鶴.md` (Common words):** 折り鶴 could link to the existing [折る](../words/折る.md) or [折](折.md) pages. This is navigation only, not required.

**Limits:**
- **Process breach:** Disclosed above; it covered `content-structure.instructions.md`, `content-format.md` and `jlpt-levels.md` 1–160. Every later call was a single serial call.
- **Kotobank:** I fetched only the 鶴 entry, and only its first 8,000 characters, which covered Daijisen and 精選版. For 鶴翼 and 折鶴 I relied on the supplied facts plus the frozen JMdict packets; I didn't look those up myself. The frozen packets are not a fresh upstream retrieval.
- **Grade:** I didn't independently check 鶴's jōyō status beyond the frozen KANJIDIC2 `grade 8`.
- **Not reviewed:**
  - The larger-quiz fallback was not reviewed; the kanji 鳥 "bird" could be a defensible fallback choice in a bigger quiz.
  - `confusable-words.md` was only searched, not read in full.
- **Textual only:** No native, phone or font check was done. The 13-glyph limit and the pending Android, combined-main, CI and public-ZIP checks were stated by you, not verified by me. Physical-phone and general-release acceptance remain outstanding.

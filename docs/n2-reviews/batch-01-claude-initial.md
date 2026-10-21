**Snapshot:** a73354e75917d4758b386c870a4284cd70dfacee. `.git\HEAD` points to `jlpt-n2-kanji` at this commit. I had no shell, so I couldn't run `git status` to confirm the working tree is clean.

**Scope:** Reviewer model: Claude Opus 5.5 (claude-opus-5.5).
- **Fully read:** all 15 new cards; `下.md` and `長.md`; the "How the kanji combine" passage in all 22 word files.
- **Evidence read:** all of `batch-01.json`, `n2-source-snapshot.json` and the assigned rules.
- **Not reviewed:** stroke JSON drawing paths; anything outside the scope; the documents you excluded (not opened).

**Verdicts:**

| Card | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 並 | CLEAN | CLEAN | CLEAN |
| 丸 | CLEAN | CLEAN | CLEAN |
| 久 | CLEAN | CLEAN | CLEAN |
| 乱 | NEEDS FIX (F4) | CLEAN | CLEAN |
| 乳 | CLEAN | NEEDS FIX (F3) | CLEAN |
| 乾 | NEEDS FIX (F1) | CLEAN | CLEAN |
| 了 | CLEAN | CLEAN | CLEAN |
| 介 | CLEAN | CLEAN | CLEAN |
| 仏 | NEEDS FIX (F2) | CLEAN | CLEAN |
| 令 | CLEAN | CLEAN | CLEAN |
| 仲 | CLEAN | CLEAN | CLEAN |
| 伸 | CLEAN | CLEAN | CLEAN |
| 伺 | CLEAN | CLEAN | CLEAN |
| 低 | CLEAN | CLEAN | CLEAN |
| 依 | CLEAN | NEEDS FIX (F5) | CLEAN |
| 下 / 長 distractors | CLEAN | CLEAN | CLEAN |
| 22 word-file links | CLEAN | CLEAN | CLEAN |

What these verdicts rest on:
- **Metadata:** readings, radical, stroke count and grade match KANJIDIC2 exactly on all 15 cards.
- **Reading examples:** every example matches a JMdict record, with no spelling or reading restriction violations.
- **Distractors:** all 15 cards have three plausible, semantically wrong options.
- **下 and 長:** each differs from the baseline only by the added distractor, 不 or 良. These prevent 低 or 久 being offered as a fallback answer.
- **Word files:** all 22 now link the new kanji at its first mention in that section.

**Findings:**

- **F1 — Minor; correctness (spelling qualification); `kanji\乾.md:34-35`**
  - **Claim:** 乾す ほす and 乾る ひる are listed as plain typical words, with no qualification.
  - **Impact:** learners may write 洗濯物を乾す instead of 干す.
  - **Remedy:** mark both as variant spellings and give 干す and 干る as the usual ones, the way the card already flags 依る and 伸す.
  - **Evidence:**
    - WWWJDIC shows the entry as "干す[P]; 乾す", so the common marker is on 干す only.
    - Jisho (JMdict data) lists 干る before 乾る.
    - The batch priority tags for 乾す (1603510) don't specify which spelling they belong to.
  - **Confidence:** high.

- **F2 — Minor; correctness (homograph); `kanji\仏.md:43`**
  - **Claim:** the note says "仏語 ふつご means French, not 'Buddhist words'".
  - **Impact:** this denies a real word, 仏語 ぶつご.
  - **Remedy:** read ふつご it means French; read ぶつご it means a Buddhist term or the Buddha's words.
  - **Evidence:** Jisho (JMdict data) has a separate entry, 仏語 ぶつご: "Buddhist term; teaching of the Buddha".
  - **Confidence:** high.

- **F3 — Minor; coverage (special reading); `kanji\乳.md:38,43`**
  - **Claim:** 乳房 is given only as にゅうぼう.
  - **Impact:** learners won't recognise ちぶさ.
  - **Remedy:** add "also ちぶさ".
  - **Evidence:**
    - JMdict entry 1582760 lists both ちぶさ and にゅうぼう (seen via Jisho).
    - The batch record contains only にゅうぼう.
    - Which reading is more frequent is not established.
  - **Confidence:** high that both readings exist; tentative on frequency.

- **F4 — Minor; correctness (evidence statement); `kanji\乱.md:31,33,35,39`**
  - **Claim:** "No matching word example was established in the inspected JMdict snapshot" for ロン and the みだ readings.
  - **Remedy:** either cite these words, labelled "uncommon, usually kana", or reword to "no common word".
  - **Evidence:**
    - JMdict has 胡乱 うろん, where 乱 is read ろん, marked usually written in kana.
    - It also has 乱りに みだりに as a variant spelling, also usually kana. Linking it to みだ(.る) is my tentative analysis.
  - **Confidence:** medium-high. I checked against current JMdict data, not the pinned snapshot file.

- **F5 — Minor; coverage (commonness); `kanji\依.md:31,38`**
  - **Claim:** 依怙 えこ is listed under "Common words".
  - **Remedy:** move it to the reading row with a note that it is mainly met in 依怙贔屓 えこひいき, which is usually written in kana.
  - **Evidence:**
    - Batch entry 1155750 has no priority tags (`priority: []`).
    - Jisho (JMdict data) marks 依怙贔屓 as usually kana.
  - **Confidence:** high that nothing supports calling it common; medium that it is rarely used alone.

**Optional:**
- **O1 — `kanji\久.md:29`:** 久遠 くおん has no priority tags and no literary label. JMdict's gloss is only "eternity"; the card's extra "the remote past or future" is unsourced.
- **O2 — `kanji\丸.md:37`:** 丸薬 がんやく has no priority tags but sits under "Common words".
- **O3 — `kanji\伺.md:30`, `kanji\低.md:33`:** 伺候 しこう and 低まる ひくまる have no priority tags; consider labelling them formal or uncommon.
- **O4 — `kanji\依.md:32`:** "rare spelling/reading" should say "rare kanji spelling"; the reading よる itself is common.
- **O5 — `kanji\仏.md:43`:** mention フランス語 as the everyday word for French.
- **O6 — `kanji\伸.md:33`:** the 伸べる futon gloss is supported by JMdict. 差し伸べる may be a more representative example, but this is tentative.

**Limits:**
- **Stroke JSON:** drawing paths not audited.
- **Baseline comparison:** checked only for 下, 長, 仲, 命令 and 紹介. The other 19 word files were checked in their current state only. The GitHub API returned 422 for the frozen commit (it is likely not pushed), so a full comparison wasn't possible.
- **Dictionary checks:** the outside lookups used current Jisho/WWWJDIC data, not the pinned JMdict file.
- **Remaining readings:** I did not search exhaustively for words matching 並 ホウ, 乱 おさ.める or 乱 わた.る.
- **Frequency and naturalness:** none of this is corpus-verified or native-speaker certified.


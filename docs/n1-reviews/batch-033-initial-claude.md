I found no actionable defects in the three files, and I judge that both proposed quiz exclusions are justified. I made no edits and used one tool call per response throughout.

**Snapshot:** Commit `fc5bf4d83fb551b1f616976a64d8106771f95857`, as stated in the task. I couldn't confirm HEAD or a clean tree because shell access wasn't allowed. I reviewed only the files in the worktree, with no uncommitted teaching changes known.

**Scope:** I'm Claude Opus 5.5 (model ID: claude-opus-5.5), working as a blind initial reviewer. I read these files in full, one at a time:
- **Instructions:** `copilot-instructions.md` (244 lines), `content-structure.instructions.md` (85 lines), `content-format.md` lines 42–148, and `jlpt-levels.md` (386 lines). These counts matched the task.
- **Teaching files:** `kanji\豚.md`, `words\豚.md` and `words\豚肉.md`, checked for correctness, scoped coverage and how clearly they read as text.
- **Sources:** the batch input metadata (KANJIDIC2 entries for 豚, 月, 服 and 腹). Both dictionary packets were read in full in chunks of 200 lines or fewer (2,737 and 682 lines). I read the five required families (1457390, 1457440, 2763370, 1547210, 1201670) and the comparison entries.
- **Comparison cards:** 月, 服, 腹, ぶうぶう, 家畜, 肉, 牛肉, 鶏肉, 飼う and 鳴く, plus the matching rows of `confusable-words.md`. I also searched titles for pig/pork/boar/hog/swine (words) and pig/pork/boar/hog/swine/livestock/meat (kanji), and searched the N1 source files for 豚.

**Verdicts:**
- `kanji\豚.md`: correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- `words\豚.md`: correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- `words\豚肉.md` (one changed link back to the kanji card): correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.

**Findings:** None.

What the reading and source checks confirmed:
- **Kanji data:** the readings, their order, 11 strokes, radical 152, grade 8 and the N1 level match KANJIDIC2. 豚 appears in the community N1 list.
- **Quiz readings:** on'yomi questions are switched off (`quizOnyomi: []`), and ぶた, the only selected kun'yomi, has its own row linking to `words/豚.md`. トン is taught for recognition through 養豚/ようとん (JMdict 1547210).
- **Rare forms:** the rare spelling 豕 isn't added as an extra reading. 海豚/いるか is kept as a whole-word reading (JMdict 1201670: rare kanji spelling, usually written in kana).
- **Senses:**
  - The pig, pork and derogatory senses match JMdict 1457390 senses 1–3 and the supplied Nikkoku summary.
  - ブタ is a valid kana-only spelling.
  - とんにく is a real alternative reading of 豚肉 (JMdict 1457440).
  - 豚肉's level 5, reading ぶたにく and `wago` type with its mixed-reading explanation are preserved.
- **Links:** both pairs of links between the kanji card and the word articles are present in both directions.
- **Lookalike answers:** the three wrong answers in the kanji quiz (moon/month, clothing, belly) look similar but mean something clearly different.
- **Quiz exclusions:**
  - **豚 / 豚肉 — keep.** 豚 sense 2 is "pork" and points to 豚肉, so "pork" is a reasonable answer for 豚.
  - **豚 / ぶうぶう — keep.** The supplied Digital Daijisen text (自動車または豚をいう幼児語) and the ぶうぶう article itself teach a child-language "pig" use. There is precedent: ぶうぶう/車 (`confusable-words.md:80`) and ぶうぶう's own exclusions of 車, 自動車 and カー. Confidence is medium-high, because JMdict 1011120 lists only the "car" noun sense.
  - **No guard needed:** 家畜, 肉, 牛肉, 鶏肉, 飼う and 鳴く. They are broader categories, other ingredients or verbs, not other names for a pig. No other word title says pig, pork or boar.

**Optional:**
1. `kanji\豚.md`, Meaning and origin section: "The indexing radical is the right-hand 豕" could say "classical indexing radical". KANJIDIC also lists Nelson's radical 130 (肉).
2. The card could add 豚カツ/とんかつ (JMdict 1457410, usually written in kana) as a familiar example of the トン reading.
3. The 腹 card says its left-hand 月 stands for 肉, while 豚's memory aid only calls it a 月-shaped outline. That's consistent, but any wording that treats it as 肉 would need a source, because it is a history claim.

**Limits:**
- I relied on the coordinator's summaries of Kotobank and Weblio and fetched nothing myself, so the Daijisen pig sense is supplied evidence only.
- I didn't count the 138 and 22 dictionary families entry by entry. I read every line, but checked closely only the families and comparisons the task named.
- I checked `confusable-words.md` only by search plus lines 70–90.
- I ran no validator, manifest or git check.
- This was a text-only review: no native rendering, phone, Android, CI or ZIP checks.
- In the absolute (fallback) quiz, the 肉 card ("meat; flesh") could appear as a choice for 豚. "pig; pork" stays clearly the best answer.
- The review guide also appeared in my session instructions, so I had seen it before reading the file.

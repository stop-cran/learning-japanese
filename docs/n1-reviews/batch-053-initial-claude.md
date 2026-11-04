The review found no actionable defects in the three teaching files, so all nine verdicts are CLEAN. I broke your one-call rule twice; details are under Limits.

**Snapshot:** Supplied SHA `3e37ebdac9af2880ceaa810ca34a7588d8c1d602`, with no uncommitted teaching included. I had no shell access, so I couldn't check the SHA against Git myself.

**Scope:** Model: Claude Opus 5.5 (`claude-opus-5.5`). I reviewed `kanji\丙.md` (lines 1–66), `words\丙.md` (1–49) and `words\丙午.md` (1–57) for correctness, scoped coverage and comprehensibility. Sources read:
- **JMdict:** all 33 frozen families in full, 11 lexical and 22 comparison.
- **Comparison cards:** 内, 肉, 病, 三, 一 and 午; word articles 三, 内, 肉, 位, 級, クラス, 火 and 馬.
- **Guidance:** `.github\copilot-instructions.md`, `content-structure.instructions.md`, `docs\content-format.md` (1–180) and `docs\jlpt-levels.md` (1–32).
- **Archived evidence:** the raw KANJIDIC JSON, the eight assigned sections across seven archived pages (Daijisen 丙, 丙午, 十干, 干支 えと/かんし; Kanjipedia 丙 and 丙午; Nikkoku and 字通 丙) and KanjiVG `04e19.svg`.
- **Searches:** `docs\confusable-words.md`, kanji 位/格, and the titles and distractors of the twelve legacy cards.

**Verdicts:**
- `kanji\丙.md`: correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- `words\丙.md`: correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- `words\丙午.md`: correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.

**Findings:** None.

Main checks behind the verdicts:
- **Kanji metadata:** KANJIDIC gives radical 1, 5 strokes, ヘイ/ひのえ in that order, and the JLPT 1 label; the card matches. KanjiVG confirms 5 strokes as 一 + 内, with stroke 4 rising to just under the top bar, as the mnemonic says.
- **Quiz selections:** The ヘイ row links `words\丙.md` (へい); JMdict ties the rank sense to へい only. The ひのえ row links `words\丙午.md` (ひのえうま); Kanjipedia and Daijisen support reading 丙 as ひのえ in that word.
- **Calendar readings:** へい for the calendar stem and the alternate へいご are both documented.
- **Calendar facts:** Term 43 and the years 1906, 1966 and 2026 are confirmed by JMdict, Daijisen and Kanjipedia, and the arithmetic checks out (43 is the 3rd stem and 7th branch). 午 is the 7th branch, the ten stems and twelve branches are correct, and the cycle is 60. The year examples are qualified as not converting historical dates.
- **Two senses of 干支:** えと can mean the 60-term cycle or only the 12-year animal signs (JMdict えと-only sense; Daijisen sense 2).
- **"Below standard" nuance:** Nikkoku supports it (標準以下という感じで用いられる), and the article hedges it with "can suggest."
- **Origin:** Shinjigen (fish tail) and 字通 (pedestal/butt-end) disagree. The card correctly asserts no origin and labels the mnemonic as modern-shape only.
- **Links:** All four directed links between the 丙 kanji card and its two word articles are present, plus 丙午 → 午. All link targets exist.
- **Quiz safety:**
  - 丙's distractors (内 "within, inner", 肉 "meat; flesh", 病 "illness") are semantically distinct.
  - 位, 格 and 三 each have three curated wrongs.
  - None of the twelve legacy titles overlaps "third rank."
  - No 丙 pair is listed in `confusable-words.md`.

**Optional:**
- `words\丙午.md`, lines 47–51: the final "does not predict a person's character" sentence has no context. A short mention of the historical superstition recorded in Daijisen and Kanjipedia would explain it, without endorsing it.
- `words\丙.md`: the JMdict "third party (in a contract)" sense could be noted. The article makes no claim that requires it.
- `kanji\丙.md`, look-alikes note: "instead" in the 肉 comparison is slightly ambiguous.
- `words\丙.md`, line 16: the example "この表では、丙は三番目です。" is grammatical but nearly circular.

**Limits:**
- **Serial-call rule:** I made two parallel calls by mistake: (1) the lexical JMdict XML lines 176–195 alongside the comparison XML lines 1–175; (2) 十干 lines 1868–1870 alongside 干支 lines 1867–1886. Both were read-only views and complete, but they break the one-call rule.
- **Evidence and reads:** Archived sections are supplied evidence, not fresh retrievals, and I made no `web_fetch` calls. I didn't read the unassigned 干支 table at line 1897 or any author records.
- **Quiz checks:** The quiz audit covers the default four-choice kanji quiz only, taken from the labels. I didn't run the app's word-quiz candidate selection (位/級/クラス co-occurrence) or check larger quizzes.
- **Phone checks:** This is a textual review only, with no native-speaker or physical-phone evidence; it can't certify glyph rendering or stroke drawing. Android f9b59a2+ compatibility and native/physical-phone/general-release acceptance remain outstanding.

## Batch 040 initial review: 鵬

**Snapshot:** `baa525f2d6c2331530bab235ce97a5eaf38b33af`, as stated in the task, with no uncommitted teaching changes. I could not check Git myself because I had no shell access. I did not inspect the canonical checkout.

**Scope:** Claude Opus 5.5 (`claude-opus-5.5`) did this review on its own, one tool call at a time. I did not read other reports, author records or author rationale.
- **Instructions:** `.github/copilot-instructions.md` (to the end), the content-structure instructions, `content-format.md` lines 42–148, and `jlpt-levels.md` to its end.
- **Teaching files:** all of `kanji/鵬.md` and `words/鵬.md`, checked for correctness, scoped coverage and how clearly they read as text.
- **Source metadata:** the input metadata file with all eight KANJIDIC2 elements.
- **Frozen JMdict packets:** 9 + 16 + 4 = 29 entry families, every line returned (159, 1–200 and 201–382, and 95 lines).
- **Comparison cards:** the six kanji cards and ten word articles listed in the task.
- **Other checks:** a bounded search of `confusable-words.md` for 鵬, 鳳, 鴻, peng, phoenix, おおとり and mythical (no matches).
- **Supplied dictionary pages:** the seven supplied Digital Daijisen and Kanjipedia sections, at the exact line ranges given.

**Verdicts:**
- **kanji/鵬.md:** correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- **words/鵬.md:** correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.

What I checked:
- **Metadata and quiz settings:** The readings ホウ and おおとり, their order, 19 strokes and radical 196 all match KANJIDIC2. Only ホウ is offered in quizzes, and the explicit empty kun list switches off kun questions.
- **Readings:**
  - ほう, the variant ぼう, and おおとり as a peng word all match JMdict 2267690 and sense 2 of 2267700, which notes "esp. 鵬".
  - Digital Daijisen and Kanjipedia support おおとり as a kun reading and as a word.
  - The 大トリ "last/key performer" boundary matches the spelling restrictions in JMdict 2732830.
- **Meaning:** "Peng" versus fenghuang matches Daijisen's two separate senses (one for 鵬, one for 鳳).
- **Example sentence:** 鵬は想像上の鳥です is natural, and its reading and translation are correct.
- **Links:** Reciprocal links between the kanji card and the word article are present.
- **Quiz choices:** The three kanji distractors (月 "moon, month", 鳴 "animal call; ring", 島 "island") cannot be mistaken for the answer. All seven word exclusions point to existing articles.
- **Fenghuang pair:** 鳳凰 ("Chinese phoenix; fenghuang") is not excluded. I judge that acceptable, because telling the two birds apart is the point of the lesson.
- **Grade 9:** Calling grade 9 a name-use classification is correct; Daijisen labels the character 人名用漢字.

**Findings:** None.

**Optional:**
1. **kanji/鵬.md (Meaning and origin; tags).** The supplied Kanjipedia page quotes 角川新字源 (Kadokawa Shinjigen): 形声。鳥と、音符朋(ホウ)とから成る. That is, 鳥 plus the sound element 朋, read ホウ. A sourced note on this would help with ホウ, the reading the card practises, and could justify a `phonetic-compound` tag.
   - The current `structure-unclassified` tag and the clearly labelled "two moons" memory aid are cautious but not wrong.
   - There is no 朋 card, so the note would have to stay plain text.
   - Confidence: medium that this would help; high that it is not an error.
2. **kanji/鵬.md, Notes.** The 鳳 comparison could link `kanji/鳳.md`, which exists. Learners can already reach it through `words/鳳凰.md`.
3. **Both files.** A few words explaining *Zhuangzi* (a classical Chinese text) would help readers who don't know it.
4. **Recognition compounds (not required).** 鵬程, 鵬翼 and 大鵬 could be added. All three appear in JMdict and Daijisen.

**Limits:**
- I used only the supplied, frozen evidence; I did no web lookups of my own. The JMdict packets are the author's extract, not something I retrieved upstream.
- The HTML pages were read only within the given line ranges.
- The `jlpt-levels.md` read reached the end of the file before the requested line 460.
- The confusable-words check was a regex search for those terms, not a full read.
- I did not check fonts, glyph rendering or anything native, and nothing was tested on a phone. That includes fresh Android, current-main, CI and public ZIP acceptance, which remain pending.
- No calls overlapped or failed.

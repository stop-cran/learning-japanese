**Snapshot:** I was given commit `5cb2ea4bc804ac218b17d5c583d4fba95e60971c` as a signed, frozen snapshot. I could not check that independently because no Git or shell tool was available. I read the working-tree files as they stand, so I can't tell whether there are uncommitted changes.

**Scope:** The runtime identified the model as Claude Opus 5.5 (`claude-opus-5.5`). I made one tool call per response and read every required range in full, with no guidance or XML read longer than 140 lines:
- **Teaching files:** all of `kanji\僧.md` (1-59) and `words\僧侶.md` (1-48). I read all of `words\坊さん.md` (1-41) for context but reviewed only line 30.
- **Frozen dictionary data:** `batch-067-jmdict.xml` 1-1716, read in 13 consecutive ranges; `batch-067-comparison-jmdict.xml` 1-172, with 7 entries; `batch-067-kanjidic2.xml` 1-406, with 6 records (人, 僧, 増, 値, 倍, 侶).
- **Related cards:** 増, 値, 倍, 人, `words\寺.md` and `words\仏.md`.
- **Generated and source stroke data:** `strokes\僧.json` and the pinned KanjiVG SVG.
- **Guidance:** `copilot-instructions.md`, `content-structure.instructions.md`, `content-format.md` (71-177, 260-275, 1389-1405) and `jlpt-levels.md` (1-20, 192-234, 255-287).
- **Targeted searches:** the eleven two-distractor cards and their titles; kanji and word titles mentioning monk, priest or Buddhism; 僧, 坊, priest and monk in `confusable-words.md`; and whether cards exist for 侶, 坊, 神父, お坊さん, 小僧 and 高僧.
- **Fresh Kotobank fetches:** all four assigned URLs.

**Verdicts:**
- `kanji\僧.md`: correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- `words\僧侶.md`: correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- `words\坊さん.md`, line 30 only: correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.

**Findings:** None. What I checked:

- **僧 metadata matches the sources.**
  - ソウ only, no kun reading, 13 strokes, radical 人 (no. 9) and grade 8 all match the raw KANJIDIC2 record.
  - The generated stroke file has 13 strokes and comes from KanjiVG revision `70a0b7ae`. The SVG marks the left part as 亻 with 人 as its original form.
  - The facts line explains that the radical 人 appears as 亻 while keeping 人 as the radical in the metadata.
- **Reading practice is set up correctly.** `quizOnyomi: [ソウ]` has its own reading row with a link to the 僧侶 article, and `quizKunyomi: []` turns off kun-reading questions.
- **The mnemonic is labelled as a memory aid.** It says it is not a historical or phonetic explanation, and the card is tagged structure-unclassified. KanjiVG marks 曽 as a phonetic component, but the card makes no claim either way, so there is no conflict.
- **Monk, believer and community are kept apart.** The card does not treat believers as clergy. Its sangha note matches JMdict 1398030 sense 2 (an abbreviation of 僧伽), and World Encyclopedia describes 僧 as Buddhist renunciant practitioners and the sangha as a community.
- **小僧 and 高僧 are accurate.** 小僧 こぞう's boy, young monk and apprentice senses match JMdict 1348480. 高僧 こうそう matches JMdict 1283680's two senses (high-ranking; virtuous).
- **僧侶 そうりょ is spelled and read correctly.** This matches JMdict 1398240, which marks it as a Buddhism term.
  - The ソウ + リョ split follows the KANJIDIC2 on-readings for each character.
  - KANJIDIC2 and Jitsū both give 侶 the meaning companion or fellow.
  - Nikkoku supports both uses: a group of clergy, or one person. The article's note about the "fellow" part fits that.
  - The article's broader-usage note matches World Encyclopedia, which notes the word has also been used for Christian clergy.
  - Both example sentences are natural, and their translations are accurate.
  - 侶 is listed in the `kanji:` field but left unlinked, which is correct because it has no card.
- **Comparisons are accurate.**
  - 坊さん and お坊さん are marked as familiar and respectful in JMdict 1519050 and 1612830, and in Daijisen sense 1.
  - The article treats the difference from 僧侶 as register, not a different occupation.
  - 神父 is a Catholic priest (JMdict 1364860), and 寺 is a Buddhist temple (JMdict 1315240).
  - No vocabulary level is inferred for 僧侶; its card leaves out `jlpt`.
- **All four required links are present.** 僧 links to 僧侶 (lines 23, 34, 40) and 僧侶 links back to 僧 (line 23). 僧侶 links to 坊さん (line 30), and 坊さん links to 僧侶 (line 30, changed only from plain text to a link).
- **Quiz choices are safe.**
  - The wrong choices for 僧 (increase; value, price; multiple, double) mean clearly different things.
  - The eleven two-distractor cards are confirmed by search. None shares a tag with 僧, and "Buddhist monk; priest" could not reasonably answer any of their titles.
  - 僧侶 and 坊さん have exactly the same title. The format contract says the app already keeps exact-title duplicates apart, so they need no exclusion. `confusable-words.md` has no entry for them, and no other kanji or word title is a near-synonym.

**Optional:**
- In `kanji\僧.md` at about line 37, it could say that こぞう shows ソウ voiced to ぞう, to make the "don't substitute mechanically" point explicit.
- `words\僧侶.md` line 18 uses the same sentence frame as an example in 坊さん. A short note on register would make that pairing an explicit contrast.

**Limits:**
- **Kotobank:** All four pages were fetched fresh. The 僧 page was cut off after 8,000 characters, but its opening definition was enough. On the 僧侶 page, only the Nikkoku and World Encyclopedia entries had text; Daijisen, Jitsū, Nipponica and Daijisen Plus showed only their headings.
- **"僧侶 is more formal":** No source I fetched says this directly. It is supported because JMdict and Daijisen label 坊さん familiar and respectful. I have moderate confidence in it.
- **N1 kanji level:** It depends on the kanjiapi.dev freeze snapshot, which wasn't assigned and which I didn't inspect. Raw KANJIDIC2 gives its old JLPT level 1.
- **Not checked:** larger, random or live quiz pools; how the app behaves at runtime; and the validator or manifest (I couldn't run them).
- **Native and device checks:** No native-speaker, device or physical-phone evidence was supplied. Phone-text readability does not cover how 僧, 侶, 亻 and 曽 render or draw on screen, or how the comparisons display. Native checks, physical-phone testing and general-release acceptance are still outstanding. This review does not certify any of them.

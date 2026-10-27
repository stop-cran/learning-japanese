**Snapshot:** 455bfb27a10d61be997b75261e180cb089a8bbf7, committed content only.
- `.git\HEAD` points to `refs/heads/jlpt-n2-kanji`, and that ref holds this commit.
- I had file tools only and did not run Git, so I could not confirm the worktree is clean; that rests on your report.
- I compared against a73354e using the diff you supplied (`n2-batch-01-corrections.diff`). It covers only the nine cards, so for `batch-01.json` and `n2-source-snapshot.json` I read only their current state.

**Scope:** Reviewer model: claude-opus-5.5.
- **Read in full:** the nine revised cards (丸, 久, 乱, 乳, 乾, 仏, 仲, 伺, 依); the new 仲 distractor 住.md; the titles of 中, 伸 and 使; my initial report; both `.github` instruction files.
- **Source records checked:** the `externalSources` and `sourceOnlyReadings` sections of `batch-01.json`, plus the records for 久遠, 胡乱, 乳房 (both readings), 母乳, 乾す, 乾る, 仏語 (both readings), 伺候, 依存, 依怙 and 依る.
- **Sources fetched:**
  - Kotobank: 久遠, 伺候, 干す, 干る, 乾く and the Daijisen notation guide.
  - Kanjipedia: 仲.
- **Not reviewed:** unchanged cards, the 22 word files, 下 and 長, and stroke JSON. Excluded documents were not opened.

**Verdicts:**

| Card | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 丸 | CLEAN | CLEAN | CLEAN |
| 久 | CLEAN | CLEAN | CLEAN |
| 乱 | CLEAN | CLEAN | CLEAN |
| 乳 | CLEAN | CLEAN | CLEAN |
| 乾 | CLEAN | CLEAN | CLEAN |
| 仏 | CLEAN | CLEAN | CLEAN |
| 仲 | CLEAN | CLEAN | CLEAN |
| 伺 | CLEAN | CLEAN | CLEAN |
| 依 | CLEAN | CLEAN | CLEAN |

**Findings:** None established. Checks on the specific points you raised:

- **仲 distractors (`仲.md:11`), now 住 / 伸 / 使:**
  - The titles are "reside, dwell", "stretch; lengthen" and "use, employ". All are wrong for "relations between people", and 住 is visually plausible (亻 + 主).
  - Removing 中 ("middle, inside") is justified. Kanjipedia gives 仲 meaning ③: 「なか。四季それぞれのまんなか。「仲秋」」 (the middle of each season), so "middle" could be defended as a correct answer.
- **胡乱 and ロン (`乱.md:31`):**
  - JMdict 1267590 うろん: "suspicious-looking; fishy", marked usually written in kana, with no priority tags.
  - Assigning ろん to 乱 (and う to 胡) is consistent with KANJIDIC's ロン reading. The row stays out of Common words, so there is no commonness claim.
- **乱りに (`乱.md:39`):**
  - It was not added, and the みだ readings stay listed as source-only. That is defensible.
  - It is absent from `batch-01.json`. From my earlier lookup it is a variant, usually-kana spelling of 妄りに, so 乱 is not its main spelling.
  - KANJIDIC2 does not tie it to みだ rather than みだ.る. The りに ending fits みだ better, but that is only my inference.
  - "No matching word example was established" describes the author's process and does not deny the word exists.
- **干 / 乾 (`乾.md:34-35, 47`):**
  - Daijisen's headings are ほ・す【干す／▽乾す】 and ひる【干る／▽乾る】.
  - The notation guide defines ▽ as 「常用漢字音訓表にない読み」 (a reading not in the Joyo list). JMdict 1603510 and 1212010 give the 乾 spellings no spelling-level priority.
  - The "alternative spelling" labels and the outside-Joyo note are therefore supported.
- **仏語 (`仏.md:43`):** matches JMdict 1501970 (ふつご, French) and 1501980 (ぶつご, "Buddhist term" and "teaching/saying/words of the Buddha"). Both readings are presented as valid separate words.
- **乳房 (`乳.md:43`):** one JMdict entry (1582760) has both にゅうぼう and ちぶさ, with the same "breast; udder" senses. "Also read ちぶさ" is accurate.
- **伺候 (`伺.md:30`):** the gloss matches Seisenban sense ① (貴人のおそば近くに仕えること, serving close to a high-ranking person) and JMdict "waiting upon (someone)".
- **久遠 (`久.md:29`):** Seisenban's く‐おん entry has a single sense: 「仏語。久しく遠いこと。現在からみて遠い過去、または遠い未来。無窮。」 So both the gloss and the Buddhist label are sourced.
- **Spelling vs. reading labels:** all correct.
  - Spelling labels: 依る "rare kanji spelling; usually written in kana" (spellingInfo "rarely used kanji form" plus usually kana); 乾す and 乾る as alternative spellings; 胡乱 usually kana.
  - Reading labels: ▽ for the outside-Joyo readings, and ちぶさ given as a second reading of 乳房.

**Original-report dispositions:**
- **F1 (乾す / 乾る):** resolved. Both rows are labelled, and the note names 干す and 干る as the usual spellings, with sources.
- **F2 (仏語 ぶつご):** resolved.
- **F3 (乳房 ちぶさ):** resolved.
- **F4 (乱 evidence statement):** partially resolved. ロン is fixed with 胡乱. The みだ part is downgraded to optional because the 乱りに assignment is uncertain and the remaining wording is honest.
- **F5 (依怙 in Common words):** resolved. 依怙 now appears only in the エ row. The 依怙贔屓 pointer from my remedy was not added; that is optional.
- **O1 (久遠):** resolved.
- **O2 (丸薬):** resolved. It stays in the ガン reading row (`丸.md:28`).
- **O3 (伺候 / 低まる):** partially resolved. 伺候 now has a label and a source. 低まる is unchanged and remains optional.
- **O4 (依る wording):** resolved.
- **O5 (フランス語):** not taken; remains optional.
- **O6 (伸べる / 差し伸べる):** not taken; remains optional.

**Optional:** none of these is a correctness fix.
- **伺 (`伺.md:30`):** "respectful" is the usual English name for 尊敬語 (honorific language). On a card that contrasts humble and honorific use, "formal/dated; the attendant's own action" would be clearer.
- **乳 (`乳.md:38, 43`):** consider giving both readings in Common words. JMdict puts the reading-level priority tags on ちぶさ only, but that is not frequency evidence.
- **乱 (`乱.md:39`):** could say "no word example was assigned" instead of "established".
- **久 (`久.md:29`):** Daijisen also has a general sense 2, 永遠 (「久遠の理想」), so the Buddhist label could read as exclusive.
- **仲:** the body could mention 仲秋 (mid-autumn) to explain why 中 is not a safe wrong answer.
- **依 (`依.md:31`):** add a pointer to 依怙贔屓.

**Limits:**
- No Git was run.
- The changes to `batch-01.json` and `n2-source-snapshot.json` were not in the diff.
- The 乱りに re-lookups failed (Jisho, WWWJDIC and the Kotobank search). Its details rely on my earlier current-data lookup, not the pinned JMdict snapshot.
- Kotobank's Daijisen text for 乾く did not load, so I did not directly verify the "unlike かわく / かわかす" half of the 乾 note. It agrees with the standard 2010 Joyo list.
- Stroke JSON drawing paths were not audited.
- Nothing here is frequency, naturalness or native-speaker certification.

## Snapshot
d3166cb43733fa6c45908151ec3633044200d54f (baseline cd32544fdfeaa6ea81e107d42bedf0cf58f8f516), committed files only. Without Git I could not confirm the commit, the clean worktree or the exact 55-file diff. I relied on the author's statement and read the files as they are on disk.

## Scope
**Model:** claude-opus-5.5 (Claude family). I worked sequentially, edited nothing and did not delegate.

**Guidance read:** `.github\copilot-instructions.md`, `.github\instructions\content-structure.instructions.md` and `docs\content-format.md:18-109`, plus targeted lines elsewhere in content-format.md.

**Read in full:** the 15 new kanji cards, the 4 new word articles and `kanji\上.md`.

**Related edits (narrow scope):** I read the linked "How the kanji combine" passages, in context, in all 15 related word articles:
- 乗り換える, 交換, 尊敬, 拾う, 捨てる
- 掃除, 換える, 損, 損害, 改善
- 敬意, 旧, 星, 直接, 衛星

Every link is accurate and agrees with its card.

**上.md:** the answer is "up, above" and the choices are 下, 中 and 土 ("earth, soil"). 土 is visually close but means something different, so it adds no new ambiguity.

**Evidence used:**
- `batch-09.json`: metadata, the 50 reading rows and all 52 word-evidence records.
- `docs\confusable-words.md`: entries CW019, CW022 and CW093.
- Public lookups: the Jisho API (a JMdict mirror) and Kotobank.

**Checks completed:**
- **Metadata:** every reading, stroke count, radical with its number, and grade tag matches the KANJIDIC2 data in batch-09.json for all 15 kanji. The readings marked as source-only (no example word) also match.
- **Examples:** all of them realise the indicated reading, including written endings, and fit the JMdict part of speech and spelling restrictions.
- **Kanji distractors:** all 45 assignments are semantically wrong, and every target card exists. Each new kanji links a useful word article.
- **Word-quiz exclusions:** 挟む, 捜す and 昇る have justified exclusions. 採掘 overlaps no other title. I found no other English-label clash that would make two choices both correct.

**Not covered:**
- Forbidden files were not read.
- `docs\n2-source-snapshot.json` was not opened, and its hashes were not recomputed.
- Unchanged teaching text in the 15 related articles and in 上.md was not reviewed.
- For the 15 stroke files, only their existence was checked, not the drawing paths.

## Verdicts
| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| kanji\拾.md | CLEAN | CLEAN | CLEAN |
| kanji\挟.md | CLEAN | CLEAN | CLEAN |
| kanji\捜.md | CLEAN | CLEAN | CLEAN |
| kanji\捨.md | CLEAN | CLEAN | CLEAN |
| kanji\掃.md | CLEAN | CLEAN | CLEAN |
| kanji\掘.md | CLEAN | CLEAN | CLEAN |
| kanji\採.md | CLEAN | CLEAN | CLEAN |
| kanji\接.md | CLEAN | CLEAN | CLEAN |
| kanji\換.md | CLEAN | CLEAN | CLEAN |
| kanji\損.md | CLEAN | CLEAN | CLEAN |
| kanji\改.md | CLEAN | CLEAN | CLEAN |
| kanji\敬.md | CLEAN | CLEAN | CLEAN |
| kanji\旧.md | CLEAN | CLEAN | CLEAN |
| kanji\昇.md | CLEAN | CLEAN | CLEAN |
| kanji\星.md | NEEDS FIX (B9-01) | CLEAN | NEEDS FIX (B9-02) |
| words\挟む.md | CLEAN | CLEAN | CLEAN |
| words\捜す.md | CLEAN | CLEAN | CLEAN |
| words\採掘.md | CLEAN | CLEAN | CLEAN |
| words\昇る.md | CLEAN | CLEAN | CLEAN |

## Findings
**B9-01: Low; correctness (reading qualification); `kanji\星.md:29, 42`**
- **Claim and impact:** The only example for the reading ショウ is 客星 きゃくしょう. The card calls it astronomy vocabulary but doesn't say that major dictionaries treat かくせい as the main reading of this word. Learners may assume 客星 is normally read きゃくしょう. The rubric asks pages to separate a rare pronunciation from a rare word, and this example blurs that.
- **Minimal remedy:** Add a qualification, for example: "客星 きゃくしょう (a dictionary-listed reading; the word is also, and in major Japanese dictionaries primarily, read かくせい/きゃくせい)." Alternatively, replace it with a better-known example after sourcing one, such as 明星 みょうじょう with an explanation of the ジョウ sound change.
- **Evidence:**
  - `batch-09.json` (record for entry 2563200, about lines 3772-3797) keeps only the reading きゃくしょう, with no priority flags.
  - The Jisho API (JMdict) lists the readings かくせい, きゃくせい and きゃくしょう, in that order.
  - On Kotobank, デジタル大辞泉 and 精選版 日本国語大辞典 headword the word as かく‐せい. Their きゃく‐しょう entries are only cross-references (「＝かくせい」 / 「⇒かくせい」).
- **Confidence:** high on the dictionary facts; medium on severity.

**B9-02: Low; comprehensibility; `kanji\星.md:20`**
- **Claim and impact:** "In other words the character can refer to a spot or mark…" uses an English idiom that signals a restatement. It reads as if the spot/mark sense simply rephrases the preceding "visible planet" sentence. The intended meaning is "in other vocabulary items", such as 白星.
- **Minimal remedy:** "In some other words, such as 白星, the character can refer to a spot or mark, including a mark for a victory."
- **Evidence:** the sentence itself. JMdict 1841410 (白星) gives "white circle; white star" and "victory mark; victory" as a separate word.
- **Confidence:** high.

## Optional
- **`kanji\採.md:20`:** the phrase "…employing someone in particular words" is awkward. "…in certain compounds such as 採用" would be clearer.
- **`kanji\敬.md:31, 42`:** could note that JMdict 1150620 lists 愛嬌 first (Jisho uses 愛嬌 as the headword). This is not a claim that 愛敬 is rare.
- **`kanji\旧.md:30`:** could mention that 元 is listed first for もと "former" in entry 2219590, parallel to the existing 旧い→古い note.
- **`words\挟む.md:37-41`:** could add JMdict sense 5, "on either side of" (e.g. 川を挟んで).
- **Larger kanji quizzes:** if the app ever needs automatically chosen extra options, these pairs could produce English-label clashes:
  - 拾 and 集 ("gather")
  - 採 and 収 ("collect")
  - 旧, 古 and 元 ("old", "former")
  - 損 and 失 ("loss")
  - 昇, 登 and 起 ("ascend", "rise")
  - 換 and 代 ("replace")
  - 敬 and 拝 ("respect")

  The current three curated distractors avoid all of them.

## Limits
- **Git:** I couldn't run Git, so the diff, scope and clean state are unverified.
- **Stroke files:** I didn't review the drawing paths or check that each JSON's stroke count matches the card.
- **Dictionary evidence:** batch-09.json is a selection, not the full dictionary.
  - I confirmed the 昇る sense restrictions in entry 1352570 (sense 1 limited to 上る and 登る, sense 2 to 上る and 昇る, sense 4 to 昇る) through the Jisho API. Its JMdict version isn't pinned.
  - The EDRDG JMdictDB site needs a password, and the WWWJDIC ID lookup returned unrelated entries. Those are gaps, not evidence either way.
- **Naturalness:** examples written for the app are not certified by a native speaker. For example, `words\昇る.md:19` (彼は部長の地位に昇りました) matches the "be promoted" sense, but its collocation wasn't independently attested.
- **Validation:** I did not run the validator or exercise the app's quiz-building code.
- **Unreviewed text:** unchanged material in the 15 related articles and 上.md's teaching text are out of scope.

## Snapshot
The frozen commit is `87860502861f01aebed7664f7ad5d6081425e277`. The snapshot JSON records the branch as jlpt-n2-kanji, a clean worktree, 58 scope files and a baseline of `483dd12e7c53315527dc861859231ad8bae7cc02`. I reviewed committed files only.

I could only read files, not run Git. So I did not check the 58-file scope, the diff or file cleanliness myself; that rests on the author's verification.

## Scope
**Model:** claude-opus-5.5 (Claude family).

**Read in full:**
- The three instruction sources: `.github\copilot-instructions.md`, `content-structure.instructions.md` and `docs\content-format.md:18-112`.
- All 16 assigned pages: kanji 陸 隅 階 隻 雇 雲 零 震 革 順 預 領 額 香 駐, and `words\隻.md`.
- `docs\n2-batch-sources\batch-24.json`, in bounded ranges.

**Related passages:** I inspected all 22 link passages in context. Six of those articles I read whole (総額, 金額, 震える, 駐車, 額, 隅); the rest at ±1 line. For comparison I also read `words\零.md` and `words\ゼロ.md`.

**Also checked:**
- All 45 distractor titles.
- The older cards whose English titles overlap the new ones.
- The 13 older cards with only two curated distractors.
- Word titles and tags that could collide with 隻 (counters and ship nouns).
- `docs\confusable-words.md`, by targeted search only: no counter or ship rows.

**Omitted:**
- Drawing paths in the 15 stroke files.
- Unchanged non-link text in the 22 related articles.
- `docs\n2-source-snapshot.json`: hashes not recomputed.
- The forbidden ledgers and reviews, which I did not open.

## Verdicts
| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| kanji\陸 | CLEAN | CLEAN | CLEAN |
| kanji\隅 | CLEAN | CLEAN | CLEAN |
| kanji\階 | CLEAN | CLEAN | NEEDS FIX (F1) |
| kanji\隻 | CLEAN | CLEAN | CLEAN |
| kanji\雇 | CLEAN | CLEAN | CLEAN |
| kanji\雲 | CLEAN | CLEAN | CLEAN |
| kanji\零 | CLEAN | CLEAN | CLEAN |
| kanji\震 | CLEAN | CLEAN | CLEAN |
| kanji\革 | CLEAN | CLEAN | CLEAN |
| kanji\順 | CLEAN | CLEAN | CLEAN |
| kanji\預 | CLEAN | CLEAN | CLEAN |
| kanji\領 | CLEAN | CLEAN | NEEDS FIX (F2) |
| kanji\額 | CLEAN | CLEAN | CLEAN |
| kanji\香 | CLEAN | CLEAN | CLEAN |
| kanji\駐 | CLEAN | CLEAN | CLEAN |
| words\隻 | CLEAN | CLEAN | CLEAN |

What these verdicts rest on:
- **Metadata:** Every card's KANJIDIC2 data matches the source exactly: on/kun readings, primary stroke count, canonical radical and number, and grade tag.
- **Examples:** Every example matches its JMdict entry ID, reading, okurigana, spelling restrictions and transitivity.
- **Distractors:** All 45 are semantically wrong and resolve to existing cards. Each new card has three curated distractors.
- **隻 word quiz:** No existing word title is a true synonym of "counter for ships", so no quiz exclusion is needed. Counters checked: 枚, 台, 軒, 回, 束, 切れ, 段. Ship nouns checked: 船, 舟, ボート, ヨット.
- **Two-choice fallback:** The new titles create no direct-synonym risk for the 13 older two-distractor cards.
- **Related passages:** All 22 link the correct card, and their component glosses are consistent.

## Findings
**F1 — Minor — comprehensibility (register) — `kanji\階.md:31, 42`**
- **Claim and impact:** Line 31 lists "階 きざはし - stairs" with no register label. Line 42 only says JMdict has no rarity flag. Learners may treat きざはし as a modern alternative to 階段. Existing cards label such readings, e.g. `kanji\銀.md:29` ("literary, rare") and `kanji\台.md:32` ("literary; archaic").
- **Remedy:** Label the row archaic or literary (雅語) and name 階段 かいだん as the everyday word. Keep the statement that JMdict has no flag.
- **Evidence:** Japanese Wiktionary (きざはし): 「階段」の古語ないし雅語的表現 ("the archaic or literary expression for 階段"). Japanese Wikipedia's 階段 article, read via Weblio: 古語および雅語ではきざはし（階） ("in archaic and literary language, きざはし (階)"). JMdict 2543170 has no flag, which does not contradict this.
- **Confidence:** Medium-high.

**F2 — Minor — comprehensibility (spelling status) — `kanji\領.md:31, 41`**
- **Claim and impact:** The kun row teaches 領 えり "collar". Line 41 explicitly leaves open "how frequent or usual that spelling is". It never says that えり is normally written 襟, so learners may write collar as 領. Existing cards name the everyday spelling, e.g. `kanji\多.md:29` ("normally written 正に").
- **Remedy:** Add that えり is normally written 襟, which is the jōyō reading. Using 領 for えり is outside the jōyō reading table and is for recognition only. Do not infer frequency from JMdict flags.
- **Evidence:** Japanese Wiktionary (領): only リョウ is marked 表内 (inside the jōyō table); えり is not. Japanese Wiktionary (襟): 訓読み えり 表内. JMdict 1588750 lists the spellings 襟, 衿, 領.
- **Confidence:** High on the jōyō status; medium on the impact.

## Optional
1. **`words\隻.md:15` and `kanji\隻.md:20`:** Note that 隻 tends toward larger vessels, and contrast it with 艘 (そう) for small boats. Japanese Wiktionary (隻) says 大きい船…に用いる助数詞 ("counter used for large ships"). JMdict's "one boat; one ship" means the current wording is not wrong.
2. **`kanji\香.md:40`:** 香車 has no priority flags and is a specialist shogi term. Consider 香水 or 線香 under Common words, and keep 香車 in the キョウ readings row.
3. **`kanji\零.md:31, 42`:** Link the existing `words\ゼロ.md` and state that ゼロ is a loanword.
4. **`kanji\隅.md:20`:** "rather than a complete room" reads awkwardly. Suggest: "一隅 is a formal word for one corner of a larger space."
5. **`kanji\駐.md:3`:** "station" can be read as a noun, overlapping 駅's label. "be stationed; stay" would be clearer. The current default quiz does not expose this.
6. **`kanji\震.md:31`:** Say 震う is intransitive, and contrast it with the homophone 振るう.
7. **`kanji\革.md`:** Add 革命 (revolution) as a common カク compound.
8. **`kanji\階.md:37`:** "second floor" uses US numbering while the page uses British "storey". This matches the source and existing articles, so it is a site-wide choice, not a batch defect.

## Limits
- **No Git:** I could not verify the scope or diff myself, or confirm that the 22 related articles changed only in their links.
- **Stroke files:** Drawing paths in the 15 stroke files were not reviewed (they came from the pinned converter).
- **Quiz overlaps:** Several English labels overlap older cards: 隅/角, 陸/地, 預/任/委, 雇/使, 革/改, 駐/駅/残, 額/総, 領/域, 順/番, 雲/曇 and 階/段. Today each of these cards has three curated distractors, so the default quiz never shows them together. A larger or revised quiz has not been certified.
- **External evidence:**
  - The sources are Wiktionary and Wikipedia via Weblio, not authoritative dictionaries such as Daijisen.
  - Kotobank returned an unrelated entry and then a search page without results.
  - Jisho returned no content.
  - These failed lookups are limits, not evidence either way.
- **Naturalness:** This is not a native-speaker certification that the examples sound natural.

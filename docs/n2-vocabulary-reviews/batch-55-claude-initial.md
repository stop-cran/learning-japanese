## Snapshot
- **Commit:** `f467750c0645c7d3f0f07d24068f418a84887b0e`. Parent: `b005473a6a1dda6e0b52dd1f43c94bf7d7b22d75`. Both come from `frozen-snapshot.json`, which reports `cleanCommittedContent: true`.
- **Git limitation:** my file tools can't run Git. I read the files on disk and could not confirm they match that commit. The hashes and equivalence checks are the author's, not mine.

## Scope
**Model:** claude-opus-5.5 (claude family). I made no edits and used no agents.

**Assigned files, read completely:**
- All 18 new articles.
- `words\通じる.md` and `words\月日.md` (the narrow edits only).
- `kanji\貨.md` and `related.patch`.
- `.github\copilot-instructions.md`, `content-structure.instructions.md` and `content-format.md:18-126`.

**Private evidence:**
- Read: `frozen-snapshot.json`, the mappings, components, labels and principals JSONL files, `principal-reading.txt`, `family-inspection-01` to `-09` (complete), `supplement-comparison-reading.txt` and `public-bodies.txt`.
- Partly read: `review-evidence.json`, lines 1–80 and 3430–3700 only.
- Not read: `public-bodies.json`.

**Other repository files:**
- `docs\n2-vocabulary-sources.tsv`: only rows N2:1082–1101.
- `confusable-words.md` and `jlpt-levels.md`: searched for batch terms only; no matches.
- The two snapshot JSONs: not read.
- Old comparison articles read in full: 届ける, 通行, 奥, 解釈. Read in part: 感ずる:36-56 and 応ずる:30-50. Every other comparison was judged only from its complete title and exclusions in the labels file.
- I checked which cards exist in `words\` and `kanji\` by listing them.

**Scope deviation:** one search over `.github\` also returned lines from two `.github\agents\*.md` files that were not assigned. I did not rely on them.

**Not done:** no web fetches, and none of the forbidden ledgers or files were read.

## Verdicts
Cells are correctness / scoped coverage / comprehensibility.

| ID | Article | Status | Correct. | Coverage | Compreh. |
|---|---|---|---|---|---|
| N2:1082 | 散らす | new | CLEAN | CLEAN | CLEAN |
| N2:1083 | ちり紙 (raw 塵紙) | new | CLEAN | CLEAN | CLEAN |
| N2:1084 | 散る | new | CLEAN | CLEAN | CLEAN |
| N2:1085 | 追加 | new | CLEAN | CLEAN | CLEAN |
| N2:1086 | ついで (raw 序で) | new | CLEAN | CLEAN | CLEAN |
| N2:1087 | 通貨 | new | CLEAN | CLEAN | CLEAN |
| N2:1088 | 通勤 | new | CLEAN | CLEAN | CLEAN |
| N2:1089 | 通じる (raw 通ずる 1983740) | reused | CLEAN | CLEAN | NEEDS FIX (B55-05) |
| N2:1090 | 通知 | new | NEEDS FIX (B55-02) | CLEAN | CLEAN |
| N2:1091 | 通帳 | new | CLEAN | CLEAN | CLEAN |
| N2:1092 | 通訳 | new | NEEDS FIX (B55-01) | CLEAN | CLEAN |
| N2:1093 | 通用 | new | CLEAN | NEEDS FIX (B55-04) | CLEAN |
| N2:1094 | 通路 | new | CLEAN | CLEAN | CLEAN |
| N2:1095 | 付き合う (raw 付合う) | new | CLEAN | CLEAN | CLEAN |
| N2:1096 | 突き当たり | new | CLEAN | CLEAN | CLEAN |
| N2:1097 | 突き当たる | new | CLEAN | CLEAN | CLEAN |
| N2:1098 | 月日 (つきひ) | reused | CLEAN | CLEAN | CLEAN |
| N2:1099 | 点く | new | CLEAN | CLEAN | CLEAN |
| N2:1100 | 突く | new | CLEAN | CLEAN | NEEDS FIX (B55-03) |
| N2:1101 | 次ぐ | new | CLEAN | CLEAN | CLEAN |

The 通じる and 月日 rows cover only the narrow added text, not the original teaching.

**貨 edit: CLEAN.**
- The カ reading row now includes 通貨 つうか (line 25).
- Common words includes 通貨 (line 33).
- JMdict entry 1433050 was added to the sources (line 41).
- The word side links to 貨 at `通貨.md` lines 7 and 29.

**Baseline metadata preservation: CLEAN.**
- `貨.md` front matter (lines 1–12) is unchanged.
- 通じる keeps its word, primary reading つうじる, title, jlpt 3, kanji and tags.
- 月日 only gains `jlpt: 2` and a provenance note. つきひ and the title are kept, and がっぴ is not given its own level.

**Kanji metadata for new words: CLEAN.**
- Every written kanji in a primary form is listed.
- 帳 has no card, so it stays plain text. ちり紙 lists only 紙, and ついで has an empty list.
- Every existing component card is linked from the word.

**Mappings: CLEAN.**
- All 20 TSV rows match the article paths, levels and entries.
- Their selected and additional senses match the sense numbers each article cites.
- N2:1089 keeps article level 3, and N2:1100's raw gloss is correctly placed inside sense 2.
- No pinned sense numbers were invented for claims backed only by the public dictionary.

## Findings
**B55-01: Moderate, quiz exclusions.** `words\通訳.md:9` (body lines 45–47); `words\解釈.md:9`.
- **Claim:** 解釈's whole title, "interpretation", is the exact N2:1092 source gloss. It also matches JMdict 1433560 sense 1, "interpretation (i.e. oral translation)". Neither article excludes the other.
- **Impact:** a 通訳 question with "interpretation" as a wrong choice has two defensible answers. The body text explains the difference, but quiz titles appear without it.
- **Evidence:** `principal-reading.txt:112`; labels lines 103 and 106. `解釈.md:47` itself says it is not a term for language interpreting.
- **Remedy:** add 解釈 to 通訳's exclusions; consider 読み "reading; interpretation" too.
- **Confidence:** high.

**B55-02: Minor, quiz exclusions.** `words\通知.md:9`.
- **Claim:** 届ける's title is "deliver; notify" (labels line 51). Its body teaches the notify sense with 住所の変更を会社に届けました, which parallels 通知's example 日程の変更を通知しました.
- **Impact:** 通知 already excludes 知らせる "to notify" and the partial overlaps 伝える and 連絡, but not 届ける, so a 通知 question can show a choice containing "notify".
- **Remedy:** add 届ける.
- **Confidence:** medium.

**B55-03: Minor, comprehensibility.** `words\突く.md:47` (example at lines 20–21).
- **Claim:** line 47 says つつく is "a separate related verb" but gives no way to tell them apart.
- **Evidence:** JMdict 1456895 つつく is also written 突く (common-word tag ichi1). Daijisen defines つつく as 何度も軽く突く ("poke lightly, repeatedly"), with 「ひじで―・いて注意する」. The article's first example, a light finger poke on the shoulder, falls in that territory.
- **Remedy:** add one line: つつく (also written 突く) means repeated light poking, nudging or pecking, for example 肩をつつく, and context decides the reading.
- **Confidence:** medium.

**B55-04: Minor, coverage (particles).** `words\通用.md:16-18`.
- **Claim:** the article teaches only が and で. Both captured Daijisen headline examples use に: 全館に通用する優待券 and 世界に通用する新技術.
- **Remedy:** add the Nに通用する pattern, for example 世界に通用する技術.
- **Confidence:** medium.

**B55-05: Minor, comprehensibility.** `words\通じる.md:41-43`.
- **Claim:** "サ変" is not explained. The sentence tells learners what not to do, then shows the ichidan-looking form 通じない without reconciling the two.
- **Comparison:** `感ずる.md:45-46` glosses サ変 as an irregular conjugation and sends learners to the じる article for everyday forms.
- **Remedy:** gloss サ変 the same way and tell learners to use the 通じ- forms taught on the page.
- **Confidence:** medium.

**B55-06: Informational; already in the baseline, not part of this batch, not counted in the verdicts.** `words\月日.md:29`.
- **Claim:** the article says reversing the kanji in 日月 changes the meaning.
- **Evidence:** JMdict 1255780 sense 2 gives 月日 as "the Moon and the Sun", and 1635330 sense 2 gives 日月 as "time".
- **Remedy:** soften the wording when the article is next revised.

## Optional
- **次ぐ.md:44-45:** "adverbial entry" could say "adverb/conjunction" (JMdict 1316390; Daijisen ［接］).
- **付き合う:** mention 食事を付き合う and 残業に付き合う (Daijisen sense 2).
- **ついで:** mention JMdict's 序 spelling.
- **突く:** mention the spellings 衝く and 撞く.
- **散らす:** "conjugation stem" could say "ます-stem".
- **Possible extra guards:** 突く/当たる, 通路/通行, 突き当たる/届く, ついで/せっかく, 散らす/散らかる and 通用/通貨. Each pair overlaps only partly in its titles, so none is an established defect.
- **N2:1086 mapping:** it lists 1316390:1 as an additional sense, while the article calls it a "Comparison". The terms could be aligned.

## Limits
- I couldn't run Git, and the author's hash and equivalence checks were not reproduced.
- **Evidence not read:** the middle ranges of `review-evidence.json` (family and component records) and `public-bodies.json`. I relied on the family inspections and `public-bodies.txt` for the same material.
- **Single source:** public bodies come from one dictionary service, captured by the author; I did not retrieve them again.
- **Comparison articles:** most were judged by title and exclusions only.
- **Naturalness:** my judgments are not a native-speaker review. For example, この切符は市内のバスで通用します is acceptable but slightly formal.
- **Frequency:** register and frequency (for example ちり紙 versus ティッシュ) were not measured.

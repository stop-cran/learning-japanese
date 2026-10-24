## Snapshot
The frozen commit is `68a03b7c32e03b23a6aad5ff7edfbde37fa6ea03`, with parent `64925b2d2e2ed6a78b52860848090b7b7d5bd2c3`. I reviewed committed content only. I had file tools but could not run Git or compute hashes. That means I couldn't confirm that the files on disk match the commit, or check the hashes and equivalence claims in the receipt and evidence. I did not edit any files.

## Scope
- **Model:** claude-opus-5.5 (Claude family). I worked sequentially and did not delegate.
- **Rules and format:** I read `.github\copilot-instructions.md`, the content-structure instructions, and `docs\content-format.md` lines 18–126.
- **Articles:** I read all twenty new articles completely.
- **Kanji edits:** I read `batch-36-related.patch` and the full current 湿, 弱, 庫 and 輪 kanji files to see the changes in context.
- **Mappings:** I read source rows N2:702–721.
- **Evidence packet:**
  - Read: the rows, all twenty principal dictionary families, the component and kanji-card evidence, the quiz declarations, the existing comparison labels, the inspected-article list, the author's public-entry receipts, and the access limits.
  - Only partly read: the full comparison-family records.
  - Not read: the three compact comparison text files, `docs\n2-vocabulary-snapshot.json` and `docs\n2-source-snapshot.json`.
- **Other existing files:** I checked titles in `words\` for confusable English labels and read `デモ.md`, `締め切る.md`, `集会.md` and the front matter of related cards.
- **Forbidden files:** I did not read any of them, including `batch-36.json`.

## Verdicts
Each cell is correctness / scoped coverage / comprehensibility.

| Article | Verdict |
|---|---|
| 氏名 | CLEAN / CLEAN / CLEAN |
| 締め切り | CLEAN / CLEAN / CLEAN |
| 締め切る | CLEAN / CLEAN / CLEAN |
| 湿る | CLEAN / CLEAN / CLEAN |
| ジャーナリスト | CLEAN / CLEAN / CLEAN |
| 社会科学 | CLEAN / CLEAN / CLEAN |
| しゃがむ | CLEAN / CLEAN / CLEAN |
| 蛇口 | CLEAN / CLEAN / CLEAN |
| 弱点 | CLEAN / CLEAN / CLEAN |
| 車庫 | CLEAN / CLEAN / CLEAN |
| 車掌 | CLEAN / CLEAN / CLEAN |
| 写生 | CLEAN / CLEAN / CLEAN |
| 社説 | CLEAN / CLEAN / CLEAN |
| しゃっくり | CLEAN / CLEAN / CLEAN |
| シャッター | CLEAN / CLEAN / CLEAN |
| しゃぶる | CLEAN / CLEAN / CLEAN |
| 車輪 | CLEAN / CLEAN / CLEAN |
| 洒落 | CLEAN / CLEAN / **NEEDS FIX** (B36-02) |
| じゃんけん | CLEAN / CLEAN / CLEAN |
| 集会 | **NEEDS FIX** (B36-01, quiz metadata) / CLEAN / CLEAN |

**Kanji edits:** all four are CLEAN on all three facets.
- 湿: 湿る is linked in the しめ.る reading row, the common words and the note.
- 弱: 弱点 is added at ジャク.
- 庫: 車庫 is added at コ.
- 輪: 車輪 is linked at リン.
- All existing reading rows and source-only qualifications are kept.
- The only kanji among the components that has an N2 card is the one each edit touches. Components with no kanji card (氏, 締, 蛇, 掌, 洒) correctly stay as metadata only, with no invented kanji files.

**Mappings N2:702–721:** all twenty are CLEAN on all three facets. The dictionary entry IDs match the principal entries:

| Word | Entry | Word | Entry |
|---|---|---|---|
| 氏名 | 1311060 | 写生 | 1322120 |
| 締め切り | 1594590 | 社説 | 1322890 |
| 締め切る | 1594600 | しゃっくり | 1005650 |
| 湿る | 1320390 | シャッター | 1061440 |
| ジャーナリスト | 1064980 | しゃぶる | 1005670 |
| 社会科学 | 1322720 | 車輪 | 1323280 |
| しゃがむ | 1005630 | 洒落 | 1568640 |
| 蛇口 | 1323370 | じゃんけん | 1005970 |
| 弱点 | 1324870 | 集会 | 1333600 |
| 車庫 | 1323120 | | |
| 車掌 | 1323170 | | |

- **締め切り:** senses 1–2 are taught and the cofferdam sense (3) is correctly left out.
- **Additional senses:** 締め切る sense 2, 湿る sense 2 (しめる only) and 洒落 sense 2 are taught without being given their own N2 level.
- **Spelling and reading restrictions:** the kana-only forms シャレ and ジャンケン, search-only じゃ口, and the rare kanji spellings are all handled correctly.

## Findings
**B36-01 · Minor · Correctness (quiz metadata) · `words\集会.md:9`, `:16`, `:20-21`; `words\デモ.md:4`, `:15`**
- **Problem:** 集会 ("meeting; assembly; rally") is not excluded from quizzes with デモ ("demonstration; protest; demo"), and neither card excludes the other.
- **Learning impact:** a protest rally (抗議集会) is a reasonable answer for the デモ prompt, so a correct-looking choice could be marked wrong.
- **Remedy:** add デモ to 集会's `quiz_exclusions`. Declaring it on one side is enough (`content-format.md:85-86`). Optionally add one sentence telling デモ (a march or demonstration) apart from 集会 (a gathering).
- **Evidence:**
  - The overlap is real: the two cards have nearly parallel peace examples (平和を願う集会 / 平和を求めるデモ).
  - 集会's own text says "demonstrating support for a cause can also be the purpose."
  - デモ is missing from the author's comparison families and labels.
  - Tags only influence which choices are drawn (`content-format.md:80-81`), so the pair can still appear together.
- **Confidence:** medium.

**B36-02 · Minor · Comprehensibility · `words\洒落.md:37`, `:39`**
- **Problem:** 洒落た店 is given as a "related expression" without saying that 洒落た is the past/attributive form of the separate verb 洒落る (しゃれる). Line 39 says not to use the noun as a な-adjective but never names the right construction.
- **Learning impact:** a learner may read it as the noun 洒落 + た and copy that pattern.
- **Remedy:** add a clause: "洒落た is the attributive past form of the verb 洒落る (しゃれる), 'be stylish'; おしゃれ takes な."
- **Evidence:** the 1568640 entry's sense 2 cross-references only お洒落. 洒落る is a separate ichidan verb. That last point comes from my own general knowledge; it is not in the evidence packet.
- **Confidence:** high on the linguistic fact; medium on severity.

## Optional
- **`締め切り.md:29`:** the claim that the raw "Closed/No Entrance" glosses belong to the closed-door meaning is a reasonable inference (締切 door notices), but it is stated too firmly. "Closed" can also appear on notices that applications are closed (受付締切). Consider wording it as "mainly."
- **締め切り / 締め切る:** the pair shares both kanji, which favours drawing them together, yet neither excludes the other. The repo is inconsistent here: 売り切れ/売り切れる, 手伝い/手伝う and 終わり/終わる are excluded, while 始まり, 間違い and 考え have no noun-side exclusion. The part of speech in the labels tells the two apart, so this is a judgement call.
- **締め切る excluding 止す:** the overlap supporting this exclusion is thin.
- **洒落 example:** "This is no joke" idiomatically means "this is serious." "This isn't a joke/pun" is closer to the Japanese.
- **`水道.md:23`:** 蛇口 is mentioned as plain text and could now be linked.
- **出会い, 議会, 群れ versus 集会:** the English labels overlap, but leaving them unexcluded matches existing practice.

## Limits
- **No Git or hashing:** see Snapshot.
- **No independent public-dictionary check:** Weblio pages came back without the dictionary text, and Kotobank returned a 404 or nothing relevant. Claims attributed to Digital Daijisen therefore rest on the author's receipts plus my own knowledge. These cover:
  - the separate へびくち heading for 蛇口;
  - 打線が湿る (natural to my knowledge);
  - the うじな heading for 氏名;
  - the origin of じゃんけん, which the article hedges;
  - the bus duties of a 車掌;
  - 写生 covering haiku and prose.
- **Partly read evidence:** the full comparison-family records and the compact comparison files were only partly consulted. Fifteen other existing articles that mention the new words were not inspected; links back from them are optional.
- **No app run:** I did not execute the app, so quiz draws are not simulated.
- **No native-speaker certification.**

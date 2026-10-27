## Snapshot
Frozen commit `a14eb7276298c2231ac00aa70cea55948bb3e7fc`; parent `760cf55d180e2ce3105ea569f9443632c653408c`. I reviewed committed content only. I had file tools and no Git execution, so I could not confirm the commit, a clean tree, or the file hashes myself. I assumed the files on disk match the receipt.

## Scope
- **Reviewer:** claude-opus-5.5 (Claude family). I worked sequentially and read only; I did not delegate or edit.
- **New articles:** all 18, read completely: 育児, 幾分, 生け花, 以後, 以降, イコール, 勇ましい, 衣食住, 意地悪, いちいち, 一応, 一段, 一流, 佚, 一斉, 一旦, 一定, いってらっしゃい.
- **Related edits:** the patch for kanji 児, 勇 and 衣, checked in context.
- **Reuse claims:** only the いっさくじつ claim in 一昨日.md and the いっさくねん claim in 一昨年.md.
- **Evidence used:**
  - TSV rows N2:62–81, batch-04.json and the snapshot files.
  - Kotobank pages fetched myself: 以後, 以降, 佚, and 佚を以て労を待つ.
  - Existing word and kanji cards, checked for links, titles and quiz exclusions.
- **Not reviewed:** the unchanged teaching on 児/勇/衣, the rest of 一昨日/一昨年, and every forbidden file.

## Verdicts
| Article | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 育児 | CLEAN | NEEDS FIX (F3) | CLEAN |
| 幾分 | NEEDS FIX (F1) | NEEDS FIX (F1) | CLEAN |
| 生け花 | CLEAN | CLEAN | CLEAN |
| 以後 | CLEAN | NEEDS FIX (F3) | CLEAN |
| 以降 | NEEDS FIX (F4) | NEEDS FIX (F3) | CLEAN |
| イコール | CLEAN | CLEAN | CLEAN |
| 勇ましい | CLEAN | CLEAN | CLEAN |
| 衣食住 | NEEDS FIX (F2) | NEEDS FIX (F3) | NEEDS FIX (F2) |
| 意地悪 | CLEAN | CLEAN | CLEAN |
| いちいち | CLEAN | CLEAN | CLEAN |
| 一応 | NEEDS FIX (F5) | CLEAN | CLEAN |
| 一段 | CLEAN | CLEAN | CLEAN |
| 一流 | NEEDS FIX (F6) | CLEAN | CLEAN |
| 佚 | CLEAN | CLEAN | CLEAN |
| 一斉 | CLEAN | CLEAN | CLEAN |
| 一旦 | CLEAN | CLEAN | CLEAN |
| 一定 | CLEAN | NEEDS FIX (F3) | CLEAN |
| いってらっしゃい | CLEAN | CLEAN | CLEAN |

**Related edits:** 児, 勇 and 衣 are CLEAN on all three facets. Each gains a link at the right reading (育児 with ジ, 勇ましい with いさ-, 衣食住 with イ), and the JMdict entry lists are updated: 1539660 added on 勇, 1158780 added on 衣, and 1160630 was already listed on 児. No made-up reading for a single kanji was introduced.

**Reuse claims:** both are CLEAN on all three facets.
- 一昨日.md:25 explicitly teaches いっさくじつ as a more formal reading; the main reading おととい and level N5 are kept.
- 一昨年.md:25 explicitly teaches いっさくねん. It is tied only to the spelling 一昨年, which matches the dictionary restriction (it does not apply to おと年).

## Findings
- **F1** · Minor · correctness/coverage · 幾分.md:6, 8, 28–30
  - **Problem:** いくぶん starts with a native reading (いく) followed by an on reading (ぶん), but the card is labelled `kango` and never explains that the reading is mixed. TSV row 63 says "Mixed native/on reading is described," which the article does not do. Learners may wrongly treat いく as an on reading.
  - **Fix:** add a sentence saying the reading is mixed, native いく + on ぶん (yutoyomi), and set `type: wago` with that note, as other cards do.
  - **Evidence:** KANJIDIC2 lists 幾 as on キ, kun いく-. Cards with the same pattern all use `wago` plus a note: 場所.md:24, 家賃.md:29–30, 生地.md:25, 合図.md:29–30, 荷物.md:21. content-format.md:63 assigns `kango` only to mixed words that start with an on reading.
  - **Confidence:** high.
- **F2** · Minor–Moderate · correctness/comprehensibility · 衣食住.md:4
  - **Problem:** the title `food; clothing and shelter` uses a semicolon, which in this repo separates alternative meanings. It therefore reads as "food" or "clothing and shelter," and conflicts with the H1 at line 11 ("food, clothing and shelter"). That risks confusion in quizzes with 食べ物 (food) and 衣服 (clothing).
  - **Fix:** change the title to `food, clothing and shelter`.
  - **Evidence:** JMdict 1158780; other titles already use commas (冷える, 午後).
  - **Confidence:** high.
- **F3** · Minor · coverage/navigation · existing cards mentioned in a comparison but not linked:
  - 育児.md:33 (教育)
  - 以後.md:37 and 以降.md:37 (以前)
  - 衣食住.md:34 (生活)
  - 一定.md:35 (変化)

  **Fix:** add links. **Evidence:** the content-structure rule to link existing cards at a substantive comparison; all five cards exist. **Confidence:** high.
- **F4** · Minor · quiz metadata · 以降.md:4, 9
  - **Problem:** the title includes "since," which overlaps with 来.md:4 ("coming; since; for a period"). 以来.md excludes 来 for the same reason, but exclusions don't carry over automatically, so 以降 needs its own.
  - **Fix:** add 来 to 以降's quiz_exclusions.
  - **Confidence:** medium-high.
- **F5** · Minor · quiz metadata · 一応.md:4, 9
  - **Problem:** "roughly" in the title matches およそ ("approximately; generally"), 約 ("approximately; about") and ほぼ ("almost; approximately"). 大体 ("generally; approximately") is already excluded, but these are not.
  - **Fix:** add およそ/約/ほぼ, or replace "roughly" with "more or less" (多少 is already excluded).
  - **Confidence:** medium.
- **F6** · Minor · quiz metadata · 一流.md:9
  - **Problem:** 上等 ("superior quality; excellent"; kango with the shared `quality` tag) is a defensible English answer for "first-rate." 松 ("top grade") is already excluded on similar grounds.
  - **Fix:** add 上等.
  - **Confidence:** medium.

## Optional
- 以後: the gloss for 以後の予定 could be tightened.
- 一段: 一段の努力 is a more common collocation than 一段の進歩.
- イコール: consider excluding 平等, 同一 and 同様.
- 一流: consider excluding 優秀.
- 一斉: consider excluding 一緒 ("together").
- 一定: consider excluding 安定 and 常に.
- 一昨年: add "more formal" for いっさくねん, as 一昨日 does.
- いってらっしゃい: mention the polite form いってらっしゃいませ.
- 勇 kanji card: note that 勇ましい shares the いさ- stem with 勇む.

## Limits
- Without Git, I could not confirm the commit or hashes. No validator or tests were run.
- My Kotobank lookup for 一定 hit the wrong page and is not evidence. The claim that 一定 is not a な-adjective rests only on JMdict (where 一定 takes の).
- The Kotobank pages for 以後, 以降, 佚 and 佚を以て労を待つ were fetched by me and support the articles. The other external dictionary claims rely on the author's inspection receipts and were not checked independently.
- The F4–F6 quiz risks come from comparing titles and tags; I did not run the quiz selection logic.
- I can't certify native naturalness, for example of 衣食住が足りる.
- The selected JMdict evidence is not the whole dictionary.

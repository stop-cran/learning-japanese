# Batch 34 N2 vocabulary review (read-only): seven minor or low fixes, no blockers

## Snapshot
I reviewed frozen commit `7c8c93f153dd5909bc467106d1c6f2ecdb386f89` (parent `e99ab822cef8fb4819f24dc0f688d7ac3326da49`) and committed content only. I had file tools but no Git, so I couldn't confirm that the files I read match that commit or compute any hashes.

## Scope
- **Model:** `claude-opus-5.5` (Claude family).
- **Read in full:**
  - the 19 new articles;
  - the related patch and the five kanji files: 捨, 勢, 孫, 湿, 績;
  - source rows N2:662–681 in `docs\n2-vocabulary-sources.tsv`;
  - the three guidance files, including `docs\content-format.md` lines 18–126.
- **Evidence packet:** source rows, principal JMdict entries, every existing comparison-card title and exclusion, public lookups and quiz declarations. Comparison families and component records were checked only where a claim depended on them.
- **Also checked:** the titles of 止む, 連れる, いつでも, 孫 and other possible quiz pairs, and the JLPT levels of every kanji in the batch.
- **Not read:** all forbidden files, including `batch-34.json`.

## Verdicts
Columns are correctness / scoped coverage / comprehensibility.

| Article | Verdicts |
|---|---|
| 持参 | NEEDS FIX (R02) / CLEAN / CLEAN |
| 磁石 | CLEAN / CLEAN / CLEAN |
| 四捨五入 | CLEAN / CLEAN / CLEAN |
| 始終 | NEEDS FIX (R03, R05) / CLEAN / NEEDS FIX (R06) |
| 自習 | CLEAN / CLEAN / CLEAN |
| 静まる | NEEDS FIX (R01) / NEEDS FIX (R04) / NEEDS FIX (R04) |
| 姿勢 | CLEAN / CLEAN / CLEAN |
| 自然科学 | CLEAN / CLEAN / CLEAN |
| 時速 | CLEAN / CLEAN / CLEAN |
| 子孫 | CLEAN / CLEAN / CLEAN |
| 死体 | CLEAN / CLEAN / CLEAN |
| 下書き | CLEAN / CLEAN / CLEAN |
| 下町 | CLEAN / CLEAN / CLEAN |
| 自治 | CLEAN / CLEAN / CLEAN |
| 実感 | CLEAN / CLEAN / CLEAN |
| 湿気 | CLEAN / CLEAN / NEEDS FIX (R07) |
| しつこい | CLEAN / CLEAN / CLEAN |
| 実習 | CLEAN / CLEAN / CLEAN |
| 実績 | CLEAN / CLEAN / CLEAN |

**Kanji edits:** 捨, 勢, 孫, 湿 and 績 are each CLEAN / CLEAN / CLEAN.
- Each new word appears at its actual reading, and all existing reading rows and source-only notes remain.
- 姿 and 磁 have no kanji cards, so they correctly stay as metadata and plain text.
- The only other kanji in these words that has an N2 card is none: the five edited cards are the complete set.

**Mappings:** all twenty (N2:662–681) are CLEAN / CLEAN / CLEAN.
- Each points to the right dictionary entry, sense and article.
- Both 湿気 rows (しっけ and しっき) map to the one article, which names しっき explicitly.
- R04 is a problem in the 静まる article, not in its mapping.

## Findings
- **B34-R01 · Minor · correctness (quiz exclusions) · `words\静まる.md:9`**
  - **Problem:** 止む isn't excluded. Its title "cease; let up" and its example "wait until the wind dies down" (`words\止む.md:4,18`) match 静まる's second meaning: JMdict 1594270 gives "to calm down; to die down; to subside". Both entries are tagged wago, verb and intransitive, so the quiz is likely to pair them. Meanwhile the less similar 止まる is excluded.
  - **Fix:** add 止む to the exclusion list.
  - **Confidence:** high.
- **B34-R02 · Minor · correctness (quiz exclusions) · `words\持参.md:4,9`**
  - **Problem:** 連れる ("take someone along", `words\連れる.md:4`) isn't excluded. The English title "bring or take along" also describes 連れる, and both share the movement tag.
  - **Fix:** add 連れる. Optionally, near lines 34–37, add that people take 連れていく or 連れてくる, not 持参.
  - **Confidence:** high.
- **B34-R03 · Minor · correctness (quiz exclusions) · `words\始終.md:9`**
  - **Problem:** いつでも ("anytime; at all times") isn't excluded, though "all the time" and "at all times" are near-synonyms. The existing card 年中 ("all year round; all the time") already excludes いつでも.
  - **Fix:** add いつでも.
  - **Confidence:** high.
- **B34-R04 · Minor · coverage and comprehensibility · `words\静まる.md:21, 29–32`**
  - **Problem:** the only example of the "subside" meaning is written 怒りが鎮まりました, and it appears before the article introduces the 鎮まる spelling. So the source spelling 静まる is never shown with that meaning.
  - **Evidence:** JMdict marks "esp. 鎮まる" as a preference, not a restriction, and mapping N2:667 selects both senses. Daijisen lists 「嵐が―・る」 and 「怒りが―・る」 under 静まる.
  - **Fix:** use 嵐が静まりました or 怒りが静まりました, or label 鎮 inline as the alternate spelling.
  - **Confidence:** medium-high.
- **B34-R05 · Minor · correctness · `words\始終.md:45–46`**
  - **Problem:** the article dismisses noun uses as "older … found in a historical dictionary". JMdict 1307570 lists both adverb and noun for its "from beginning to end" sense, and Daijisen gives the current noun use 「事件の始終を語る」.
  - **Fix:** note the current noun use, with 一部始終 as the more common form, while keeping the focus on the adverb.
  - **Confidence:** medium.
- **B34-R06 · Low · comprehensibility · `words\始終.md:30`**
  - **Problem:** "The on readings are シ + ジュウ", but the 終 card lists only シュウ (`kanji\終.md:9,33`).
  - **Fix:** write "シ + シュウ, voiced to じゅう here".
  - **Confidence:** high.
- **B34-R07 · Low · comprehensibility · `words\湿気.md:32`**
  - **Problem:** "気's け or キ" writes the on reading ケ in hiragana, which reads as a kun reading. The 気 card lists ケ as on (`kanji\気.md:9,29`).
  - **Fix:** write ケ in katakana.
  - **Confidence:** high.

## Optional
- **子孫 / 孫, and 自然科学 / 物理, 化学, 生物:** each pair is a general term next to a specific one. They are fair distractors, since the specific title is always the single best answer. Excluding 孫 is optional, to match the existing 子 and 子供 exclusions.
- **湿気:** state that しっけ is the usual reading (only しっけ is marked common in JMdict). The 気 kanji card's ケ row lists 湿気 in plain text with the readings しっけ／しけ, which is outside this batch.
- **自治:** add an example of the shortened 地方自治 meaning, such as 自治体.
- **持参:** add a note on its formal register, as in ご持参ください.
- **Possibly over-broad exclusions:** 実習 → 学問 and 学; 姿勢 → 形 and 様子; 始終 → 続く, 続ける and 重ねる. These are defensible but shrink the pool of wrong answers. 静まる → 収める is supported, because JMdict's eighth sense of 収める is "subdue; settle".

## Limits
- I couldn't confirm the commit or compute hashes.
- I read the evidence packet selectively, not in full.
- For public checks, Kotobank returned only the truncated Daijisen summaries for 静まる and 始終, and Weblio returned no entry text. My other usage judgements rely on the packet's JMdict data and lookups.
- How often the quiz pairs two entries is inferred from shared tags; I didn't inspect the app's scoring code.
- This review is not a native-speaker certification.
